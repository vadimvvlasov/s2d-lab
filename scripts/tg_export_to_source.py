# /// script
# requires-python = ">=3.11"
# dependencies = ["beautifulsoup4"]
# ///
"""Convert a Telegram Desktop HTML chat export into an S2D run source.

Usage:
    uv run scripts/tg_export_to_source.py [EXPORT_DIR] [--chat NAME] [--run-id ID]

Takes the whole export (the time range is chosen when exporting in Telegram).
Without EXPORT_DIR, uses the newest ChatExport_* under
"~/Downloads/Telegram Desktop" whose chat title matches --chat.

Writes runs/.work/<run-id>/source.md and copies full-size photos to
runs/.work/<run-id>/images/.

Each photo gets a model-generated description (verbatim text, numbers, chart
contents) inserted under its link, so agents can work from text and open only
the images a material claim rests on. One vision call per image; results are
cached by file hash in runs/.work/.image-descriptions/. Endpoint (OpenAI-compatible):
S2D_VISION_URL (default x99), S2D_VISION_KEY or ~/.config/opencode/x99.key,
S2D_VISION_MODEL (default: first model the server lists). --no-describe skips it.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import urllib.error
import urllib.request
import shutil
import sys
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup, Tag

DEFAULT_CHAT = "investment-decisions-with-ml"
DEFAULT_EXPORTS_ROOT = Path.home() / "Downloads" / "Telegram Desktop"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VISION_URL = "http://192.168.0.2:18020/v1"
DEFAULT_VISION_KEY_FILE = Path.home() / ".config" / "opencode" / "x99.key"

DESCRIBE_PROMPT = """You describe an image posted in a group chat for analysts who will work from your text.
Message context (for orientation only; describe what the IMAGE shows): {context}

Write plain text with these labelled parts:
TYPE: chart | table | screenshot (app, news, post) | photo | meme | diagram | other — one line.
TEXT: every visible text verbatim, in its original language: titles, labels, numbers with signs,
units and currencies, dates, tickers, footnotes. Keep negations exactly (e.g. "не включены").
Mark unreadable parts [unreadable]. Skip only UI chrome (status bar, buttons).
DATA: for charts and tables: instrument/ticker, timeframe, axes and units, values printed on the image
(last, high, low, labelled points), indicators, and any lines, arrows or circles drawn by the user and
what they point to. For other images: the content that matters for an investment discussion.
Describe only what is visible: no interpretation, prediction or advice. Be compact; TEXT may be long."""


class Describer:
    """One cached vision call per image."""

    def __init__(self, cache_dir: Path) -> None:
        self.url = os.environ.get("S2D_VISION_URL", DEFAULT_VISION_URL).rstrip("/")
        key = os.environ.get("S2D_VISION_KEY")
        if key is None and DEFAULT_VISION_KEY_FILE.is_file():
            key = DEFAULT_VISION_KEY_FILE.read_text().strip()
        self.key = key or ""
        self.model = os.environ.get("S2D_VISION_MODEL")
        self.cache_dir = cache_dir
        self.stats = {"described": 0, "cached": 0, "failed": 0}
        self.disabled_reason: str | None = None

    def _request(self, path: str, body: dict | None, timeout: float) -> dict:
        req = urllib.request.Request(
            self.url + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)

    def describe(self, image: Path, context: str) -> str | None:
        digest = hashlib.sha256(image.read_bytes()).hexdigest()
        cached = self.cache_dir / f"{digest}.json"
        if cached.is_file():
            self.stats["cached"] += 1
            return json.loads(cached.read_text(encoding="utf-8"))["description"]
        if self.disabled_reason:
            self.stats["failed"] += 1
            return None
        try:
            if not self.model:
                self.model = self._request("/models", None, 10)["data"][0]["id"]
            mime = "image/png" if image.suffix.lower() == ".png" else "image/jpeg"
            data = base64.b64encode(image.read_bytes()).decode()
            reply = self._request(
                "/chat/completions",
                {
                    "model": self.model,
                    "temperature": 0,
                    "max_tokens": 1500,
                    "chat_template_kwargs": {"enable_thinking": False},
                    "messages": [{"role": "user", "content": [
                        {"type": "text", "text": DESCRIBE_PROMPT.format(context=context[:600] or "(none)")},
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}},
                    ]}],
                },
                300,
            )
        except (urllib.error.URLError, TimeoutError, OSError, KeyError, IndexError, ValueError) as exc:
            # Server down: stop trying for the remaining images, keep the intake usable.
            self.disabled_reason = f"{type(exc).__name__}: {exc}"
            self.stats["failed"] += 1
            return None
        choice = reply["choices"][0]
        text = (choice["message"].get("content") or "").strip()
        if not text:
            self.stats["failed"] += 1
            return None
        if choice.get("finish_reason") == "length":
            text += "\n[description truncated]"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps({"image": image.name, "model": self.model, "description": text},
                                     ensure_ascii=False, indent=1), encoding="utf-8")
        self.stats["described"] += 1
        return text


def fail(msg: str) -> None:
    print(f"TELEGRAM INTAKE FAILED: {msg}", file=sys.stderr)
    print(f"TELEGRAM INTAKE FAILED: {msg}")
    sys.exit(1)


def page_files(export_dir: Path) -> list[Path]:
    def key(p: Path) -> int:
        m = re.fullmatch(r"messages(\d*)\.html", p.name)
        return int(m.group(1) or 1) if m else 0

    return sorted(export_dir.glob("messages*.html"), key=key)


def chat_title(page: Path) -> str:
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    node = soup.select_one(".page_header .text.bold")
    return node.get_text(strip=True) if node else ""


def find_export(root: Path, chat: str) -> Path:
    candidates = sorted(
        (d for d in root.glob("ChatExport_*") if (d / "messages.html").is_file()),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    for d in candidates:
        if chat_title(d / "messages.html").casefold() == chat.strip().casefold():
            return d
    if any(root.glob("ChatExport_*/result.json")):
        hint = " (found JSON exports only; re-export as HTML)"
    else:
        hint = ""
    fail(f'no HTML export of chat "{chat}" under {root}{hint}')
    raise AssertionError  # unreachable


def text_of(node: Tag | None) -> str:
    if node is None:
        return ""
    for br in node.find_all("br"):
        br.replace_with("\n")
    for a in node.find_all("a", href=True):
        label = a.get_text()
        href = a["href"]
        if href.startswith("http") and href != label:
            a.replace_with(f"{label} ({href})")
    lines = [ln.strip() for ln in node.get_text().splitlines()]
    return "\n".join(ln for ln in lines if ln)


def parse_date(title: str) -> datetime:
    # "01.11.2026 00:30:57 GMT+05:00"
    m = re.match(r"(\d\d\.\d\d\.\d{4} \d\d:\d\d:\d\d)(?: (?:GMT|UTC)([+-]\d\d:\d\d))?", title.strip())
    if not m:
        raise ValueError(f"unrecognised date: {title!r}")
    stamp = m.group(1) + (m.group(2) or "+00:00").replace(":", "")
    return datetime.strptime(stamp, "%d.%m.%Y %H:%M:%S%z")


def describe_block(describer: Describer | None, image: Path, context: str) -> list[str]:
    if describer is None:
        return []
    text = describer.describe(image, context)
    if text is None:
        return ["[image description unavailable: open the image]"]
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    return ["[image description — auto-generated by a model, not the participant's words; "
            "the image is the source]"] + [f"| {ln}" for ln in lines] + ["[end of image description]"]


def media_lines(body: Tag, export_dir: Path, images_dir: Path, msg_id: str, stats: dict,
                describer: Describer | None = None, context: str = "") -> list[str]:
    out = []
    for a in body.select("a.photo_wrap[href]"):
        rel = a["href"]
        src = export_dir / rel
        if src.is_file():
            dst = images_dir / src.name
            shutil.copy2(src, dst)
            stats["photos"] += 1
            out.append(f"![photo #{msg_id}](images/{src.name})")
            out.extend(describe_block(describer, dst, context))
        else:
            stats["missing"] += 1
            out.append(f"[photo #{msg_id} missing in export: {rel}]")
    for m in body.select(".media"):
        if m.find_parent("a", class_="photo_wrap"):
            continue
        title = text_of(m.select_one(".title"))
        desc = text_of(m.select_one(".description"))
        note = " (not included in export)" if "Not included" in desc else ""
        out.append(f"[{title or 'media'}{note}]")
    return out


def parse_messages(export_dir: Path, images_dir: Path,
                   describer: Describer | None = None) -> tuple[list[dict], dict]:
    stats = {"photos": 0, "missing": 0}
    messages: list[dict] = []
    author = "?"
    for page in page_files(export_dir):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        for msg in soup.select("div.message.default"):
            msg_id = msg.get("id", "").removeprefix("message")
            body = msg.find("div", class_="body", recursive=False)
            if body is None:
                continue
            date_node = body.find("div", class_="date", recursive=False)
            if date_node is None or not date_node.get("title"):
                continue
            name_node = body.find("div", class_="from_name", recursive=False)
            if name_node is not None:
                author = text_of(name_node)
            reply = body.find("div", class_="reply_to", recursive=False)
            reply_id = None
            if reply is not None:
                m = re.search(r"GoToMessage\((\d+)\)", str(reply))
                reply_id = m.group(1) if m else None

            fwd = body.select_one(":scope > div.forwarded.body")
            fwd_from = fwd_text = None
            if fwd is not None:
                fname = fwd.find("div", class_="from_name", recursive=False)
                if fname is not None:
                    for span in fname.find_all("span"):
                        span.decompose()
                    fwd_from = text_of(fname)
                fwd_text = text_of(fwd.find("div", class_="text", recursive=False))

            text = text_of(body.find("div", class_="text", recursive=False))
            context = f"{author}: " + " ".join(t for t in (text, fwd_text) if t)
            media = media_lines(body, export_dir, images_dir, msg_id, stats, describer, context)
            messages.append(
                {
                    "id": msg_id,
                    "date": parse_date(date_node["title"]),
                    "author": author,
                    "reply_to": reply_id,
                    "fwd_from": fwd_from,
                    "text": "\n".join(t for t in (text, fwd_text) if t),
                    "media": media,
                }
            )
    return messages, stats


def render(chat: str, export_dir: Path, run_id: str, messages: list[dict], stats: dict) -> str:
    first, last = messages[0]["date"], messages[-1]["date"]
    head = [
        "---",
        "source_type: telegram_desktop_html_export",
        f'chat: "{chat}"',
        f'export_dir: "{export_dir}"',
        f"run_id: {run_id}",
        f"first_message_at: {first.isoformat()}",
        f"last_message_at: {last.isoformat()}",
        f"message_count: {len(messages)}",
        f"image_count: {stats['photos']}",
        f"images_missing: {stats['missing']}",
        "---",
        "",
        f"# Telegram chat: {chat}",
        "",
        "Format: `[#id YYYY-MM-DD HH:MM] Author: text`. `↪ #id` = reply to message id. "
        "Images are in `images/` next to this file. Under each image link, a block marked "
        "`[image description — auto-generated ...]` gives its text and contents; it is a reading aid, "
        "the image itself is the source. Open an image when a material claim or number rests on it "
        "or the description lacks a detail you need.",
        "",
    ]
    body = []
    for m in messages:
        meta = f"[#{m['id']} {m['date']:%Y-%m-%d %H:%M}] {m['author']}"
        if m["reply_to"]:
            meta += f" ↪ #{m['reply_to']}"
        if m["fwd_from"]:
            meta += f" (fwd from {m['fwd_from']})"
        parts = ([m["text"]] if m["text"] else []) + m["media"]
        content = "\n".join(parts) or "[empty]"
        indented = content.replace("\n", "\n    ")
        body.append(f"{meta}: {indented}")
    return "\n".join(head + body) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export_dir", nargs="?", type=Path)
    ap.add_argument("--chat", default=DEFAULT_CHAT)
    ap.add_argument("--exports-root", type=Path, default=DEFAULT_EXPORTS_ROOT)
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--out-root", type=Path, default=REPO_ROOT / "runs" / ".work")
    ap.add_argument("--no-describe", action="store_true", help="skip model descriptions of images")
    args = ap.parse_args(argv)

    export_dir = args.export_dir.expanduser() if args.export_dir else find_export(args.exports_root, args.chat)
    if not (export_dir / "messages.html").is_file():
        hint = " (JSON export found; re-export as HTML)" if (export_dir / "result.json").is_file() else ""
        fail(f"{export_dir}/messages.html not found{hint}")
    chat = chat_title(export_dir / "messages.html") or args.chat

    started = datetime.now().astimezone()
    run_id = args.run_id or started.strftime("%Y-%m-%d-tg-%H%M%S")
    run_dir = args.out_root / run_id
    images_dir = run_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    describer = None if args.no_describe else Describer(args.out_root / ".image-descriptions")
    messages, stats = parse_messages(export_dir, images_dir, describer)
    if not messages:
        fail(f"no messages parsed from {export_dir}")

    source = run_dir / "source.md"
    source.write_text(render(chat, export_dir, run_id, messages, stats), encoding="utf-8")

    print("TELEGRAM INTAKE OK")
    print(f"run_id: {run_id}")
    print(f"created_at: {started.isoformat(timespec='seconds')}")
    print(f"source: {source}")
    print(f"chat: {chat}")
    print(f"export_dir: {export_dir}")
    print(f"range: {messages[0]['date']:%Y-%m-%d %H:%M} .. {messages[-1]['date']:%Y-%m-%d %H:%M}")
    print(f"messages: {len(messages)}  images: {stats['photos']}  images_missing: {stats['missing']}")
    if describer is not None:
        d = describer.stats
        line = f"image descriptions: {d['described']} new, {d['cached']} cached, {d['failed']} unavailable"
        if describer.disabled_reason:
            line += f" ({describer.disabled_reason})"
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

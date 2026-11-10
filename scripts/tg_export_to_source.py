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
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup, Tag

DEFAULT_CHAT = "investment-decisions-with-ml"
DEFAULT_EXPORTS_ROOT = Path.home() / "Downloads" / "Telegram Desktop"
REPO_ROOT = Path(__file__).resolve().parent.parent


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


def media_lines(body: Tag, export_dir: Path, images_dir: Path, msg_id: str, stats: dict) -> list[str]:
    out = []
    for a in body.select("a.photo_wrap[href]"):
        rel = a["href"]
        src = export_dir / rel
        if src.is_file():
            dst = images_dir / src.name
            shutil.copy2(src, dst)
            stats["photos"] += 1
            out.append(f"![photo #{msg_id}](images/{src.name})")
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


def parse_messages(export_dir: Path, images_dir: Path) -> tuple[list[dict], dict]:
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
            media = media_lines(body, export_dir, images_dir, msg_id, stats)
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
        "Images are in `images/` next to this file; open each one referenced below.",
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
    args = ap.parse_args(argv)

    export_dir = args.export_dir.expanduser() if args.export_dir else find_export(args.exports_root, args.chat)
    if not (export_dir / "messages.html").is_file():
        hint = " (JSON export found; re-export as HTML)" if (export_dir / "result.json").is_file() else ""
        fail(f"{export_dir}/messages.html not found{hint}")
    chat = chat_title(export_dir / "messages.html") or args.chat

    run_id = args.run_id or datetime.now().strftime("%Y%m%d-%H%M%S") + "-tg"
    run_dir = args.out_root / run_id
    images_dir = run_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    messages, stats = parse_messages(export_dir, images_dir)
    if not messages:
        fail(f"no messages parsed from {export_dir}")

    source = run_dir / "source.md"
    source.write_text(render(chat, export_dir, run_id, messages, stats), encoding="utf-8")

    print("TELEGRAM INTAKE OK")
    print(f"run_id: {run_id}")
    print(f"source: {source}")
    print(f"chat: {chat}")
    print(f"export_dir: {export_dir}")
    print(f"range: {messages[0]['date']:%Y-%m-%d %H:%M} .. {messages[-1]['date']:%Y-%m-%d %H:%M}")
    print(f"messages: {len(messages)}  images: {stats['photos']}  images_missing: {stats['missing']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
T1 stage tests: run ONE agent on frozen inputs and check its output with code.

Each case in tests/stage/cases/<id>/ holds:
  case.yaml   agent, dispatch prompt, output file name, expectations
  inputs/     frozen run workspace (source.md, question map, packet, evidence/, CRs)

The runner copies the project's prompts/docs into a throw-away sandbox, drops the
inputs into runs/.work/<run-id>/, runs `opencode run --agent <agent>` there with web
access denied, then evaluates the file the agent wrote.

Usage:
  uv run scripts/run-stage-tests.py                    # all cases
  uv run scripts/run-stage-tests.py --list
  uv run scripts/run-stage-tests.py -k aud-fx06        # cases whose id contains text
  uv run scripts/run-stage-tests.py --agent independent-auditor --jobs 2
  uv run scripts/run-stage-tests.py --check-only runs/.work/t1-results/<stamp>
  uv run scripts/run-stage-tests.py --dry-run -k ana   # build sandbox, print prompt

Exit code: 0 if every behavior check passed (and, with --strict, every format check),
1 otherwise, 2 on usage/config errors.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = ROOT / "tests" / "stage" / "cases"
RESULTS_DIR = ROOT / "runs" / ".work" / "t1-results"
SANDBOX_COPY = [".opencode", "opencode.json", "AGENTS.md", "docs", "templates", "scripts"]
# "agent" = no --model flag: each agent's frontmatter model and variant
# (reasoning effort) apply. An explicit provider/model[#variant] overrides both.
DEFAULT_MODEL = os.environ.get("S2D_T1_MODEL", "agent")
# MCP servers seen in user/global configs. Their tools bypass edit permissions, the
# sandbox and the web ban (filesystem rooted at $HOME, a browser), so tests deny them.
MCP_SERVERS = ["filesystem", "playwright", "context7"]
SEVERITY_RANK = {"MINOR": 1, "MAJOR": 2, "BLOCKER": 3}
VERDICTS = ("PASS_WITH_LIMITATIONS", "CHANGES_REQUESTED", "BLOCKED", "PASS")


# ---------------------------------------------------------------- parsing


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    return (fm if isinstance(fm, dict) else {}), m.group(2)


def _field(block: str, name: str) -> str | None:
    """Value of a '**Name**: x' / '**Name:** x' / '- **Name:** x' line."""
    m = re.search(rf"\*\*{name}\s*:?\*\*\s*:?\s*(.+)", block, re.I)
    return m.group(1).strip() if m else None


def parse_findings(body: str) -> list[dict]:
    """Findings from a verification report (heading or 'Finding ID' style)."""
    starts = [
        m.start()
        for m in re.finditer(
            r"^(?:#{2,4}\s*Finding\s+F-\d+|\*\*Finding\s+F-\d+|(?:-\s*)?\*\*Finding ID\s*:?\*\*)",
            body,
            re.M | re.I,
        )
    ]
    findings = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(body)
        first_line_end = body.find("\n", start, end)
        if first_line_end != -1:  # stop at the next H2 section (Verdict, Limitations, ...)
            nxt = re.search(r"^##\s", body[first_line_end:end], re.M)
            if nxt:
                end = first_line_end + nxt.start()
        block = body[start:end]
        fid = re.search(r"F-\d+", block)
        sev = _field(block, "Severity") or ""
        sev_m = re.search(r"BLOCKER|MAJOR|MINOR", sev.upper())
        findings.append(
            {
                "id": fid.group(0) if fid else "?",
                "severity": sev_m.group(0) if sev_m else "",
                "category": (_field(block, "Category") or "").lower(),
                "responsible": (_field(block, "Responsible agent") or "").lower(),
                "text": block,
            }
        )
    return findings


def parse_verdict(fm: dict, body: str) -> tuple[str | None, str | None]:
    """(frontmatter verdict, body verdict)."""
    fm_v = str(fm.get("verdict", "")).strip().upper() or None
    body_v = None
    m = re.search(r"^##\s*Verdict\s*\n(.*?)(?=^##\s|\Z)", body, re.M | re.S | re.I)
    if m:
        for v in VERDICTS:  # PASS_WITH_LIMITATIONS is tested before PASS
            if re.search(rf"\b{v}\b", m.group(1)):
                body_v = v
                break
    return fm_v, body_v


def parse_questions(body: str) -> list[dict]:
    """Questions from a Question Map: '### Qn — text' blocks."""
    starts = list(re.finditer(r"^#{2,4}\s*\**(Q\d+)\b[^\n]*", body, re.M))
    questions = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(body)
        block = body[m.start() : end]
        if _field(block, "Reason") and not _field(block, "Class"):
            continue  # "Questions Not Researchable" entry
        questions.append(
            {
                "id": m.group(1),
                "class": (_field(block, "Class") or "").strip("` "),
                "raised_by": _field(block, "Raised by") or "",
                "text": block,
            }
        )
    return questions


# ---------------------------------------------------------------- checks


@dataclass
class Check:
    name: str
    ok: bool
    kind: str = "behavior"  # behavior | format
    detail: str = ""


@dataclass
class CaseResult:
    case_id: str
    agent: str
    checks: list[Check] = field(default_factory=list)
    seconds: float | None = None
    tokens: dict = field(default_factory=dict)
    steps: int | None = None
    error: str | None = None
    timed_out: bool = False

    def passed(self, strict: bool) -> bool:
        if self.error:
            return False
        return all(c.ok for c in self.checks if strict or c.kind == "behavior")


def _rx(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.I | re.S) is not None


def _as_list(v) -> list:
    return v if isinstance(v, list) else [v]


def finding_matches(f: dict, spec: dict) -> bool:
    if "severity" in spec and f["severity"] not in _as_list(spec["severity"]):
        return False
    if "category" in spec and not any(c in f["category"] for c in _as_list(spec["category"])):
        return False
    if "responsible" in spec and spec["responsible"] not in f["responsible"]:
        return False
    return all(_rx(p, f["text"]) for p in _as_list(spec.get("mentions", [])))


def evaluate(case: dict, run_dir: Path) -> list[Check]:
    exp = case.get("expect", {})
    out = run_dir / case["output"]
    checks: list[Check] = []
    if not out.is_file() or not out.read_text(encoding="utf-8").strip():
        return [Check("output file written by the agent", False, detail=f"missing: {case['output']}")]
    checks.append(Check("output file written by the agent", True))

    text = out.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)

    if "verdict" in exp:
        fm_v, body_v = parse_verdict(fm, body)
        got = body_v or fm_v
        checks.append(Check(f"verdict in {exp['verdict']}", got in exp["verdict"], detail=f"got {got}"))
        checks.append(
            Check(
                "frontmatter verdict matches body",
                fm_v is not None and (body_v is None or fm_v == body_v),
                "format",
                f"frontmatter={fm_v} body={body_v}",
            )
        )

    findings = parse_findings(body)
    found = ", ".join(f"{f['id']}:{f['severity']}/{f['category'] or '?'}" for f in findings) or "none"
    for spec in exp.get("findings", []):
        label = spec.get("name") or json.dumps({k: v for k, v in spec.items() if k != "mentions"}, ensure_ascii=False)
        ok = any(finding_matches(f, spec) for f in findings)
        checks.append(Check(f"finding present: {label}", ok, detail=f"findings: {found}"))
    if "max_severity" in exp:
        limit = SEVERITY_RANK.get(exp["max_severity"], 0)  # "NONE" -> 0
        worst = max((SEVERITY_RANK.get(f["severity"], 0) for f in findings), default=0)
        checks.append(Check(f"no finding above {exp['max_severity']}", worst <= limit, detail=f"findings: {found}"))

    if "questions" in exp:
        q = exp["questions"]
        qs = parse_questions(body)
        got = ", ".join(f"{x['id']}:{x['class']}/{x['raised_by']}" for x in qs) or "none"
        if "min" in q or "max" in q:
            lo, hi = q.get("min", 0), q.get("max", 99)
            checks.append(Check(f"question count in [{lo}, {hi}]", lo <= len(qs) <= hi, detail=got))
        for spec in q.get("each", []):
            label = spec.get("name") or json.dumps(spec, ensure_ascii=False)
            ok = any(
                (("class" not in spec) or x["class"] in _as_list(spec["class"]))
                and (("raised_by" not in spec) or _rx(spec["raised_by"], x["raised_by"]))
                and all(_rx(p, x["text"]) for p in _as_list(spec.get("mentions", [])))
                for x in qs
            )
            checks.append(Check(f"question present: {label}", ok, detail=got))

    for pat in exp.get("must_match", []):
        checks.append(Check(f"output matches /{pat}/", _rx(pat, text)))
    for pat in exp.get("must_not_match", []):
        m = re.search(pat, text, re.I | re.S)
        checks.append(Check(f"output does not match /{pat}/", m is None, detail=f"hit: {m.group(0)[:80]!r}" if m else ""))

    if "max_words" in exp:
        n = len(body.split())
        checks.append(Check(f"body <= {exp['max_words']} words", n <= exp["max_words"], "format", f"{n} words"))

    if exp.get("schema_valid", True):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_artifact.py"), str(out)],
            capture_output=True,
            text=True,
        )
        errors = [l.strip() for l in proc.stdout.splitlines() if "[ERROR]" in l]
        checks.append(Check("artifact schema valid (validate_artifact.py)", proc.returncode == 0, "format", "; ".join(errors)[:300]))

    for rel in exp.get("inputs_unchanged", []):
        src = CASES_DIR / case["id"] / "inputs" / rel
        dst = run_dir / rel
        same = dst.is_file() and dst.read_bytes() == src.read_bytes()
        checks.append(Check(f"reviewed artifact not modified: {rel}", same))
    return checks


# ---------------------------------------------------------------- running


def load_cases() -> list[dict]:
    cases = []
    for path in sorted(CASES_DIR.glob("*/case.yaml")):
        case = yaml.safe_load(path.read_text(encoding="utf-8"))
        case["id"] = path.parent.name
        for key in ("agent", "output", "prompt"):
            if key not in case:
                sys.exit(f"{path}: missing '{key}'")
        cases.append(case)
    return cases


def run_id_for(case: dict) -> str:
    return case.get("run_id", f"2026-11-08-t1-{case['id']}")


def patch_agent(path: Path, web: bool, options: dict | None = None) -> None:
    """Make the agent directly runnable; deny web and MCP tools; apply option overrides.

    The prompt body is untouched. `options` replaces the agent's `options:` block
    (passed by opencode to the provider, e.g. reasoningEffort)."""
    text = path.read_text(encoding="utf-8")
    head, sep, body = text.partition("\n---\n")
    head = re.sub(r"^mode:.*$", "mode: primary", head, flags=re.M)
    if not web:
        head = re.sub(r"^(\s+web(?:search|fetch)):.*$", r"\1: deny", head, flags=re.M)
    # MCP tools (e.g. a global filesystem server) bypass edit permissions and the sandbox.
    mcp_deny = "".join(f'\n  "{s}_*": deny' for s in MCP_SERVERS)
    head = re.sub(r"^permission:\s*$", "permission:\n  execute: deny" + mcp_deny, head, count=1, flags=re.M)
    if options:
        fm = yaml.safe_load(head.removeprefix("---\n")) or {}
        fm["options"] = {**(fm.get("options") or {}), **options}
        head = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).rstrip("\n")
    path.write_text(head + sep + body, encoding="utf-8")


def global_mcp_servers() -> list[str]:
    """Names of MCP servers in the user's global opencode config (best effort)."""
    cfg = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "opencode" / "opencode.json"
    try:
        raw = re.sub(r",(\s*[}\]])", r"\1", cfg.read_text(encoding="utf-8"))  # tolerate trailing commas
        mcp = json.loads(raw).get("mcp", {})
    except (OSError, ValueError):
        return []
    servers = mcp.get("servers", mcp) if isinstance(mcp, dict) else {}
    return sorted({*MCP_SERVERS, *(k for k, v in servers.items() if isinstance(v, dict))})


def sandbox_env(sandbox: Path) -> dict:
    env = dict(os.environ)
    # opencode resolves the project directory from $PWD, not from the process cwd.
    env["PWD"] = str(sandbox)
    servers = global_mcp_servers()
    if servers:
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps({"mcp": {"servers": {s: {"disabled": True} for s in servers}}})
    return env


def build_sandbox(case: dict, base: Path, options: dict | None = None, ref: str | None = None) -> tuple[Path, Path]:
    sandbox = base / case["id"]
    sandbox.mkdir(parents=True)
    if ref:  # prompts/docs from a git revision, for A/B comparisons
        names = [n for n in SANDBOX_COPY if subprocess.run(
            ["git", "cat-file", "-e", f"{ref}:{n}"], cwd=ROOT, capture_output=True).returncode == 0]
        archive = subprocess.run(["git", "archive", ref, *names], cwd=ROOT, capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", str(sandbox)], input=archive.stdout, check=True)
    else:
        for name in SANDBOX_COPY:
            src = ROOT / name
            if src.is_dir():
                shutil.copytree(src, sandbox / name, ignore=shutil.ignore_patterns("__pycache__", "audit", "assets"))
            elif src.exists():
                shutil.copy2(src, sandbox / name)
    patch_agent(sandbox / ".opencode" / "agents" / f"{case['agent']}.md", bool(case.get("web", False)), options)
    run_dir = sandbox / "runs" / ".work" / run_id_for(case)
    shutil.copytree(CASES_DIR / case["id"] / "inputs", run_dir)
    return sandbox, run_dir


def render_prompt(case: dict) -> str:
    rid = run_id_for(case)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        case["prompt"]
        .replace("{run_id}", rid)
        .replace("{run_dir}", f"runs/.work/{rid}")
        .replace("{output}", f"runs/.work/{rid}/{case['output']}")
        .replace("{now}", now)
    )


def read_usage(log: Path) -> tuple[dict, int]:
    tokens = {"input": 0, "output": 0, "reasoning": 0, "cache_read": 0}
    steps = 0
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "step_finish":
            steps += 1
            t = ev.get("part", {}).get("tokens", {})
            tokens["input"] += t.get("input", 0)
            tokens["output"] += t.get("output", 0)
            tokens["reasoning"] += t.get("reasoning", 0)
            tokens["cache_read"] += t.get("cache", {}).get("read", 0)
    return tokens, steps


def run_case(case: dict, base: Path, results: Path, model: str, timeout: int, options: dict,
             ref: str | None = None) -> CaseResult:
    res = CaseResult(case["id"], case["agent"])
    sandbox, run_dir = build_sandbox(case, base, options, ref)
    dest = results / case["id"]
    log = sandbox / "opencode.log"
    cmd = [
        "opencode", "run", "--standalone", "--auto",
        "--agent", case["agent"], *(["--model", model] if model != "agent" else []),
        "--format", "json", "--title", f"t1 {case['id']}",
        render_prompt(case),
    ]
    start = time.monotonic()
    try:
        with log.open("w", encoding="utf-8") as fh:
            proc = subprocess.run(
                cmd, cwd=sandbox, env=sandbox_env(sandbox), stdout=fh, stderr=subprocess.STDOUT, timeout=timeout
            )
        if proc.returncode != 0:
            res.error = f"opencode exited with {proc.returncode} (see opencode.log)"
    except subprocess.TimeoutExpired:
        res.timed_out = True
    except FileNotFoundError:
        res.error = "opencode not found in PATH"
    res.seconds = round(time.monotonic() - start, 1)

    shutil.copytree(run_dir, dest, dirs_exist_ok=True)
    if log.exists():
        shutil.copy2(log, dest / "opencode.log")
        res.tokens, res.steps = read_usage(log)
    res.checks = evaluate(case, dest)
    res.checks.append(Check(f"finished within {timeout}s", not res.timed_out, "format",
                            "killed at timeout; output evaluated as written" if res.timed_out else ""))
    # A JSON string value starting with the repo path = a tool argument or a resolved
    # file path. Plain mentions inside file contents (docs cite the repo path) do not count.
    leaked = log.exists() and f'"{ROOT}' in log.read_text(encoding="utf-8", errors="replace")
    res.checks.insert(
        0, Check("sandbox isolation (no access to the real repository)", not leaked,
                 detail="opencode.log references the repository path" if leaked else ""),
    )
    return res


# ---------------------------------------------------------------- reporting


def write_summary(results_dir: Path, results: list[CaseResult], strict: bool, model: str, options: dict) -> None:
    data = {
        "model": model,
        "options": options,
        "strict": strict,
        "cases": [
            {
                "id": r.case_id,
                "agent": r.agent,
                "passed": r.passed(strict),
                "seconds": r.seconds,
                "steps": r.steps,
                "tokens": r.tokens,
                "error": r.error,
                "checks": [c.__dict__ for c in r.checks],
            }
            for r in results
        ],
    }
    (results_dir / "summary.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# T1 stage tests — {results_dir.name}", "", f"Model: `{model}` · options: `{options or 'agent defaults'}`", "",
             "| Case | Agent | Result | Time, s | Steps | Out tokens | Failed checks |", "|---|---|---|---|---|---|---|"]
    for r in results:
        failed = [f"{c.name} ({c.detail})" if c.detail else c.name for c in r.checks if not c.ok]
        if r.error:
            failed.insert(0, r.error)
        out_tok = r.tokens.get("output", 0) + r.tokens.get("reasoning", 0) if r.tokens else ""
        lines.append(
            f"| {r.case_id} | {r.agent} | {'PASS' if r.passed(strict) else 'FAIL'} | {r.seconds or ''} | "
            f"{r.steps or ''} | {out_tok} | {'<br>'.join(failed).replace('|', '/')} |"
        )
    (results_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_result(r: CaseResult, strict: bool) -> None:
    timing = f" {r.seconds}s" if r.seconds is not None else ""
    print(f"{'PASS' if r.passed(strict) else 'FAIL'}  {r.case_id}{timing}", flush=True)
    if r.error:
        print(f"      ! {r.error}")
    for c in r.checks:
        if not c.ok:
            tag = "x" if (strict or c.kind == "behavior") else "~"
            print(f"      {tag} [{c.kind}] {c.name}" + (f" — {c.detail}" if c.detail else ""))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-k", dest="keyword", help="run only cases whose id contains this text (comma-separated: any of)")
    ap.add_argument("--agent", help="run only cases for this agent")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"provider/model[#variant], or 'agent' for the agent's own model and variant (default {DEFAULT_MODEL}; env S2D_T1_MODEL)")
    ap.add_argument("--jobs", type=int, default=1,
                    help="cases to run in parallel (default 1; on a single 24 GB GPU more jobs overflow "
                         "the KV cache and every case gets slower)")
    ap.add_argument("--timeout", type=int, default=3600, help="seconds per case (default 3600)")
    ap.add_argument("--strict", action="store_true", help="format checks also fail the run")
    ap.add_argument("--set", dest="sets", action="append", default=[], metavar="KEY=VALUE",
                    help="override an agent option for this run, e.g. --set reasoningEffort=low (repeatable)")
    ap.add_argument("--prompts-ref", metavar="GIT_REF",
                    help="take agents/docs/templates from this git revision instead of the working tree "
                         "(A/B against an older prompt; cases and checks still come from the working tree)")
    ap.add_argument("--list", action="store_true", help="list cases and exit")
    ap.add_argument("--dry-run", action="store_true", help="build sandboxes and print prompts; do not call the model")
    ap.add_argument("--check-only", metavar="DIR", help="re-evaluate an existing results directory")
    ap.add_argument("--keep-sandbox", action="store_true", help="do not delete the sandbox directory")
    args = ap.parse_args()

    options = {}
    for item in args.sets:
        key, sep, value = item.partition("=")
        if not sep:
            ap.error(f"--set expects KEY=VALUE, got {item!r}")
        options[key] = yaml.safe_load(value)
    cases = load_cases()
    if args.keyword:
        words = [w for w in args.keyword.split(",") if w]
        cases = [c for c in cases if any(w in c["id"] for w in words)]
    if args.agent:
        cases = [c for c in cases if c["agent"] == args.agent]
    if not cases:
        print("no cases selected", file=sys.stderr)
        return 2

    if args.list:
        for c in cases:
            print(f"{c['id']:34} {c['agent']:22} {c.get('description', '')}")
        return 0

    if args.check_only:
        results_dir = Path(args.check_only)
        results = []
        for c in cases:
            if (results_dir / c["id"]).is_dir():
                r = CaseResult(c["id"], c["agent"], checks=evaluate(c, results_dir / c["id"]))
                results.append(r)
                print_result(r, args.strict)
        if not results:
            print(f"no case directories in {results_dir}", file=sys.stderr)
            return 2
        return 0 if all(r.passed(args.strict) for r in results) else 1

    base = Path(tempfile.mkdtemp(prefix="s2d-t1-"))
    if args.dry_run:
        for c in cases:
            sandbox, _ = build_sandbox(c, base, options, args.prompts_ref)
            print(f"== {c['id']}  sandbox: {sandbox}\n{render_prompt(c)}\n")
        return 0

    stamp = dt.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    results_dir = RESULTS_DIR / stamp
    results_dir.mkdir(parents=True)
    print(f"model {args.model} · options {options or 'agent defaults'} · prompts {args.prompts_ref or 'working tree'} · "
          f"{len(cases)} case(s) · "
          f"results: {results_dir.relative_to(ROOT)}", flush=True)

    started = time.monotonic()
    results: list[CaseResult] = []
    with cf.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [pool.submit(run_case, c, base, results_dir, args.model, args.timeout, options, args.prompts_ref)
                   for c in cases]
        for fut in cf.as_completed(futures):
            r = fut.result()
            results.append(r)
            print_result(r, args.strict)
    results.sort(key=lambda r: r.case_id)
    write_summary(results_dir, results, args.strict, args.model, {**options, **({"prompts_ref": args.prompts_ref} if args.prompts_ref else {})})
    if not args.keep_sandbox:
        shutil.rmtree(base, ignore_errors=True)

    ok = sum(r.passed(args.strict) for r in results)
    print(f"\n{ok}/{len(results)} passed in {round(time.monotonic() - started)}s · {results_dir.relative_to(ROOT)}/summary.md")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

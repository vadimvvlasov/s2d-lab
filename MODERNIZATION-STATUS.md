# S2D Lab Modernization Status

**Last Updated:** 2026-11-10
**Current Phase:** Session 06 — local-model hardening (Qwen3.8 27B on one RTX 3090); first full `/recap` on a real chat released (with `--resume`)
**Target:** Qwen3.8 27B (`x99/qwen3.8-27b`, vLLM, RTX 3090) via opencode v2.2.6

## Executive Summary

EPICs B, C1, D2, D3 and E1 were complete by 2026-11-08 (sessions 01–05, summarized below). E2 (7 fixtures, full `/recap` each) ran on 2026-11-09 and was paused half-way: one fixture run took hours on the local model, and the fixtures' seeded defects mostly did not materialize in live runs, so the auditor was rarely tested on them.

Session 06 (2026-11-10) moved testing to cheap stage tests and hardened the pipeline for the local model:

- **T1 stage tests:** one agent, frozen inputs, code-checked. 11 cases, ~2–4 min each; replaces full fixture runs for prompt and model changes.
- **Smaller agent contexts:** each agent reads only what it is given; formats are inlined in prompts; size budgets; single write; subagents write their own artifacts.
- **Research and audit per research task**, plus a separate Question Map audit; rework and cycle caps are per task.
- **Telegram intake** with one cached vision description per photo.
- **Reasoning control:** per-agent `reasoning_effort` and a hard per-request reasoning cap.
- **Compaction headroom, notes checkpoint and `--resume`.**
- **Security:** agents could escape permissions through global MCP servers; now denied project-wide.

The binding constraint on this hardware is **context growth inside one agent loop** (accumulated reasoning plus fetched pages) against a ~138k-token KV pool. Prompt size is not the constraint.

## Session 06 (2026-11-10)

### Test tiers

| Tier | What | Cost | When |
|---|---|---|---|
| T0 | `tests/e1-structural/` (16 pass), validators | seconds | every commit |
| T1 | `scripts/run-stage-tests.py`, `tests/stage/cases/` (2 analyst, 6 auditor, 3 researcher) | 2–4 min/case, ~25 min all | every prompt/model change |
| T2 | full `/recap` | 1–2+ h | before a release |

- T1 runs in a sandbox: `PWD` is set to the sandbox, MCP and web are denied, and an isolation check is applied.
- Cases are sequential by default: the KV cache holds about one full context, and parallel cases thrashed it (35–40 min per audit).
- `--prompts-ref` runs an A/B against an older version of the prompts.

### Prompt changes, measured on T1 (old → new)

| Agent | Time | Input tokens | Output words |
|---|---|---|---|
| auditor | 227–286 s → 101–187 s (fx04 failed on old) | peak 39–55k → 24–35k | — |
| researcher | fx04 273 → 224 s, fx06 210 → 136 s | fx04 33k → 17k | 2731/2233 → 1635/1296 |
| analyst | 78/58 → 42/35 s | 16k/14k → 9k/5k | 733/619 → 430/429 |

### Reasoning control

- opencode does **not** send agent or model `options` to the server; this was verified with a logging proxy.
- Model variants `low|medium|high` become `reasoning_effort`. A subagent gets its variant only when its frontmatter has `model` and `variant`.
- Provider `options.body` is sent: it carries `thinking_token_budget: 12288`.
- T1, 9 researcher and auditor cases, all pass at every effort level:

  | Effort | Total time | Change |
  |---|---|---|
  | none | 1653 s | — |
  | medium | 1295 s | −22% |
  | low | 1182 s | −28% |

- Set per agent: analyst `low`, researcher `medium`, auditor `low`, lead `medium`.

### Infrastructure (x99, `~/HyperQwen`, `gpu-llm long`)

- `CTX=long`: fp8 KV, pool pinned by `KV_MEM` (5.58 GB, about 139k tokens). `GPU_UTIL` does not size the pool in this profile.
- `MAX_LEN=138000`, up from 131072; 16 images per prompt, up from 10.
- Raising `KV_MEM` further cuts the transient memory margin (about 1.1 GB, with about 1 GB swing between boots), so it was not done.
- `CTX=huge` (2/4-bit KV, 245k tokens) is quality-neutral, but decode is 1.25× slower at 32k and 1.9× at 128k; not needed.
- opencode x99 model limits: context 138000, output 48000. Compaction starts near 90k, which leaves room for one step's growth plus the summary.

### Full `/recap` runs on ChatExport_2026-11-10 (168 messages, 18 photos)

| # | Outcome | Cause → fix |
|---|---|---|
| 1 | analyst failed 3× (vLLM: max 10 images/prompt); vLLM crashed in rework | → photo descriptions at intake; sequential dispatch |
| 2 | researcher and auditor failed: "Compaction summary reached the output token limit" | → bounded source reading |
| 3 | lead's intake command denied; lead then copied Chromium and tried a shell through MCP | → deny `execute`, `filesystem_*`, `playwright_*`, `context7_*`, `external_directory` |
| 4 | researcher T1 compaction failure again (24–28k reasoning steps) | → reasoning effort, reasoning cap, output reserve |
| 5 | QM + audit + T1 done, compaction failure once; paused | replay of T1 with new config: 9 min, peak 98k, no failure |
| 6 | `--resume` of #5: released, PASS_WITH_LIMITATIONS, no infrastructure failures | see "Run 6" below |

### Run 6 (resume of 2026-11-10-tg-181756)

**Released** `runs/2026-11-10-conversation-research-recap.md` (Russian, ~1,900 words against a 700–1,300 target). Run `2026-11-10-tg-181756`.

| Stage | Time | Result |
|---|---|---|
| Intake, Question Map, QM audit (reused from run 5) | — | PASS_WITH_LIMITATIONS (2 MINOR) |
| T1 QQQ bottom, T2 AI ETFs, T3 portfolio, T4 NVDA | 20:38–23:15 | each: v1 → CHANGES_REQUESTED → v2 → PASS_WITH_LIMITATIONS; 7 CRs, all MAJOR |
| Final report v1 + final audit | 23:15–23:42 | PASS_WITH_LIMITATIONS, 0 BLOCKER / 0 MAJOR / 4 MINOR |
| Release (v2 with the MINOR fixes) | second `--resume` | the lead hit 80 steps one step before release |

- Wall time: 3 h 10 min plus 9 min for the second resume. Earlier stages of run 5 took ~32 min.
- No infrastructure failures: no compaction errors, no server errors. The auditor opened the original photos (#50868, #50959).
- **All 7 MAJOR findings are one defect type:** the researcher states specifics (dates, valuations, fund names, percentages, a BBC quote) that are absent from its recorded excerpts. Rework took about 1 h 40 min of the 3 h 10 min.
- State hygiene: review IDs are not `REV-NNN` (4 `validate-state.py` errors), and CR status is `RESOLVED` instead of `verified_resolved`.

## Risks (current)

1. **Researcher adds specifics from model memory** beyond recorded evidence. The auditor catches them, at the cost of one cycle per task. Next fix: check every number, date and name against `notes-T<n>.md` before writing the packet.
2. **Context growth within one agent loop.** Prior reasoning stays in context for the whole loop. Mitigated by the reasoning cap, effort variants, a 48k output reserve, the notes checkpoint and fetch discipline. A compaction that does fire is lossy.
3. **Size budgets are not followed:** packets run 1500–2300 words against a 1500-word budget. This is reported as a T1 format check only.
4. **opencode passes only part of the config** (agent and model `options` are not sent) and uses permissive defaults: `external_directory` is allowed with `--auto`, and global MCP servers are open to agents. Re-verify after opencode upgrades.
5. **Photo descriptions can be wrong:** in run 5 the description misread a chart's year. Material numbers must be checked against the image; the auditor rule requires it.
6. **Lead state hygiene:** the lead writes CR status `RESOLVED`, while the schema expects `verified_resolved`, and `state.yaml` lags behind the files. `--resume` trusts files over state.

## EPIC status

| EPIC | Item | Status |
|---|---|---|
| A | Baseline, 7 fixtures | ✅ |
| B | Prompt refactor | ✅; superseded in part by session 06 compaction |
| C | C1 validator + schema | ✅ |
| C | C2 source index | partial: anchor-based reading, intake photo descriptions |
| C | C3 token budget manager | partial: size budgets, reasoning cap, compaction headroom (config, not a manager) |
| C | C4 sequential scheduling | ✅ (sequential dispatch; T1 `--jobs 1`) |
| D | D1 source-first audit | not started |
| D | D2 claim dependency graph | ✅ |
| D | D3 state validator | ✅; `excluded` and `pass_with_limitations` statuses; BLOCKER scoped to its own artifact |
| D | D4 resume protocol | ✅ `/recap --resume <run-id>`, used twice on run 6 |
| E | E1 structural tests | ✅ (16 pass) |
| E | E2 LLM behaviour eval | partial: 2026-11-09 fixture runs paused; replaced for day-to-day use by T1 |
| E | E3 adversarial cases | partial: T1 seeded-defect cases (false access, calc error, trade signal, false CR resolution, omitted question) |
| F | Docs and rollout | partial: README, `tests/stage/README.md`, `docs/verifier-loop.md`, `docs/workflow.md` updated |

## Next Actions

1. Researcher rule: verify specifics against notes before writing (risk 1); A/B on T1 plus one researcher task replay.
2. Lead: raise `steps` 80 → ~120 (a full run used all 80).
3. Orchestration by code (a script drives tasks, retries and state; the lead writes only the report) if lead overhead or state drift stays material.
4. Lead: `REV-NNN` review IDs and valid CR statuses; keep `state.yaml` in step with files.

## Sessions 01–05 (summary)

- **01–02:** baseline, 7 golden fixtures, EPIC B (lead dedup, auditor streamlined, researcher claim IDs, analyst source anchors).
- **03:** gate set (fx01/03/06/07) on the target model, 52/52 criteria; bounded 3-cycle loop shown end to end (fx07).
- **04:** C1 validator (`scripts/validate_artifact.py`) and schema-conformant prompts.
- **05:** D2 claim dependency graph and visualizer; D3 Pydantic state schema; E1 pytest suite.
- **Details:** `docs/audit/session-0{1..5}-summary.md`, `docs/audit/fixture-validation-results.md`, `docs/audit/modernization-progress.md`.
- **E2 2026-11-09 pause note (per-fixture state):** `runs/.work/PAUSE-2026-11-09-resume-note.md` (gitignored).

---

**Key principle:** validate every infrastructure or prompt change on T1 (or a single-agent replay) before a full T2 run.

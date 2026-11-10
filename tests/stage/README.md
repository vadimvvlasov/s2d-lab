# T1 stage tests

One agent, frozen inputs, no web, result checked by code.

A stage test answers one question: *given this exact input, does this agent do the
right thing?* The seeded defect sits in the input file, so it is always present —
unlike a full `/recap` run, where the live researcher usually does not make the
mistake the fixture expects and the auditor is never actually tested on it.

## Test tiers

| Tier | What | Cost | When |
|---|---|---|---|
| T0 | `tests/e1-structural/`, `scripts/validate_artifact.py`, `scripts/validate-state.py` | seconds, no model | every commit |
| T1 | this directory: one agent call per case | minutes per case | every prompt or model change |
| T2 | full `/recap` on a fixture conversation, live web | hours on the local model | before a release, 1–2 fixtures |

## Run

```bash
uv run scripts/run-stage-tests.py                 # all cases, one at a time
uv run scripts/run-stage-tests.py -k aud-fx06     # cases whose id contains the text
uv run scripts/run-stage-tests.py --agent independent-auditor
uv run scripts/run-stage-tests.py --list
uv run scripts/run-stage-tests.py --dry-run -k ana          # show prompts, no model call
uv run scripts/run-stage-tests.py --check-only runs/.work/t1-results/<stamp>
```

Model: by default each agent's own `model` and `variant` from its frontmatter (the variant
sets `reasoning_effort`); override with `--model provider/model[#variant]` or `S2D_T1_MODEL`.
An explicit `--model` replaces the agent's variant too. Agent `options` are **not** sent to
the server by opencode (checked with a logging proxy, 2026-11-10), so `--set` only works for
options opencode itself understands. Results (agent output, `opencode.log`, `summary.md`, `summary.json`
with time, steps and tokens per case) go to `runs/.work/t1-results/<stamp>/`.

**Run cases one at a time on the local model.** On x99 (RTX 3090, `max_model_len`
131072) the vLLM KV cache holds about one full context (`kv_cache_max_concurrency` ≈ 1.05),
and an auditor reaches 45–65k tokens. Three parallel cases caused preemptions and took
35–40 min per audit; sequential runs take ~4–5 min per audit (2026-11-10). `--jobs` > 1
only makes sense on a server with spare KV cache.

Exit code is 0 when every **behavior** check passes. **Format** checks (schema
validity, frontmatter verdict equal to body verdict, word budget) are reported and
fail the run only with `--strict`.

## How a case runs

1. The runner copies `.opencode/`, `opencode.json`, `AGENTS.md`, `docs/`, `templates/`
   and `scripts/` into a temporary sandbox outside the repository.
2. In the sandbox copy only, the agent's frontmatter is patched: `mode: primary` (so it
   can be called directly), `websearch`/`webfetch: deny`, and MCP tools denied
   (`execute`, `filesystem_*`, `playwright_*`, `context7_*` — a global filesystem MCP
   bypasses edit permissions and the sandbox, a browser bypasses the web ban). The
   prompt body is the real one. opencode is started with `PWD` set to the sandbox:
   it resolves the project directory from `$PWD`, not from the process cwd.
3. `inputs/` is copied to `runs/.work/2026-11-08-t1-<case-id>/` in the sandbox.
4. `opencode run --standalone --auto --agent <agent>` gets the dispatch prompt from
   `case.yaml`. The agent must write its artifact to the given output path.
5. The output file is parsed and checked against `expect`. A case also fails if its
   log mentions the real repository path (isolation check). A timeout is a format
   check: the output written before the kill is still evaluated.

## Cases

| Case | Agent | Checks that |
|---|---|---|
| `ana-fx02-compound-split` | analyst | a three-part question becomes three explicit questions |
| `ana-fx03-second-speaker` | analyst | the second speaker's explicit question is kept and attributed |
| `aud-fx03-omitted-question` | auditor | an omitted explicit question is a MAJOR+ finding routed to the analyst |
| `aud-fx04-false-access` | auditor | `FULL_TEXT_OPENED` on a source that returned HTTP 403 is caught |
| `aud-fx05-calc-error` | auditor | a simple-interest formula is caught and the correct value given |
| `aud-fx05-clean-control` | auditor | a correct packet gets no BLOCKER/MAJOR (false-positive control) |
| `aud-fx06-trade-signal` | auditor | an invented entry/stop/target is a BLOCKER, `financial_safety` |
| `aud-fx07-diff-new-defect` | auditor | differential audit rejects a self-declared "resolved" CR whose fix is wrong |
| `res-fx05-calc` | researcher | compound growth is computed correctly, compactly, without trade advice |
| `res-fx04-fees` | researcher | fee answer from a frozen retrieval log; the 403 prospectus is not marked as opened; cheaper fund found |
| `res-fx06-indicators` | researcher | indicator readings from a frozen pack; educational answer, no trade levels or long/short call |

Not covered here, by design:

- **Cycle cap, release gate, state transitions** (fixture 07's main point) are
  deterministic rules. They belong in T0 (`tests/e1-structural/`), not in a model test.
- **Live source retrieval quality** is T2.

## Frozen evidence

Auditor and researcher cases that involve external sources carry `inputs/evidence/`: a record of what
each cited source returned. The dispatch prompt tells the agent to treat it as its own
search/fetch results. These files are synthetic test data and say so in their first line; they are
never evidence for a real recap.

`aud-fx05-clean-control` and the Question Maps in the other cases are real outputs of the
target model from the E2 run of 2026-11-09, with only the run ID changed.

## Adding a case

Create `tests/stage/cases/<id>/case.yaml` and `inputs/`:

```yaml
description: one line
fixture: tests/fixtures/NN-name.md      # where the scenario comes from
agent: independent-auditor              # conversation-analyst | quant-researcher | independent-auditor
output: 03-verification-research-v1.md  # file the agent must write in the run directory
web: false                              # default; true keeps the agent's web permissions
prompt: |
  ... {run_dir} {run_id} {output} {now} are substituted ...
expect:
  verdict: [CHANGES_REQUESTED]          # verification reports
  findings:                             # each entry must match at least one finding
    - name: label for the report
      severity: [MAJOR, BLOCKER]
      category: [evidence]              # substring match on the finding's category
      responsible: quant-researcher
      mentions: ["E1", "403|snippet"]   # regexes, all must hit inside that finding
  max_severity: MINOR                   # no finding above this (NONE = no findings)
  questions:                            # question maps
    min: 3
    max: 4
    each:
      - {class: EXPLICIT_QUESTION, raised_by: Charlie, mentions: ["bond"]}
  must_match: ["regex on the whole output"]
  must_not_match: ["regex"]
  max_words: 1500                       # format check
  schema_valid: true                    # format check, default true
  inputs_unchanged: [02-research-packet-v1.md]   # agent must not edit reviewed files
```

Inputs must pass `uv run --with pyyaml scripts/validate_artifact.py` unless the schema
violation is the seeded defect.

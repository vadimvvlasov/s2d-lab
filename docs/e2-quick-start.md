# E2 Quick Start — 7 Fixture Executions

**Goal:** Run 7 fixtures, save outputs to `runs/.work/fx{01..07}-2026-11-08-e2/`

## TL;DR

```bash
# For each fixture (01 through 07):
# 1. Read conversation from tests/fixtures/{NN}-*.md
# 2. Run: /recap
# 3. Paste conversation
# 4. Wait for completion
# 5. Save outputs to runs/.work/fx{NN}-2026-11-08-e2/
```

## Fixture List

| ID | File | Conversation Start |
|---|---|---|
| 01 | tests/fixtures/01-short-simple.md | **Alice [10:15]:** Привет! Я хочу понять... |
| 02 | tests/fixtures/02-compound-question.md | [Check file] |
| 03 | tests/fixtures/03-omitted-question.md | [Check file] |
| 04 | tests/fixtures/04-inaccessible-source.md | [Check file] |
| 05 | tests/fixtures/05-calculation-error.md | [Check file] |
| 06 | tests/fixtures/06-invented-trade-signal.md | **Henry [09:00]:** Интересно, биткоин... |
| 07 | tests/fixtures/07-cycle-limit.md | [Check file] |

## Per-Fixture Steps

### 1. Extract Conversation

Open fixture file, copy everything between the `---` markers in `## Conversation` section.

**Example (fx01):**
```
**Alice [10:15]:** Привет! Я хочу понять, что такое дивидендная доходность и как её рассчитывают?

**Bob [10:17]:** Хороший вопрос. Я тоже не уверен в формуле.

**Alice [10:18]:** Можешь найти определение и простой пример расчёта?
```

### 2. Run `/recap`

In your coding agent environment:

```
/recap

[Paste conversation here]
```

### 3. Wait for Completion

The system will:
- Create run directory
- Run Conversation Analyst → Question Map
- Run Quant Researcher → Research Packet
- Run Independent Auditor → Verification Report
- (If needed) Create CR, run rework cycle
- Run Research Lead → Final Report
- Run Final Audit

**Watch for:**
- ✅ "Final Report released" (success)
- ❌ Infinite loop (stop if cycle > 3)
- ❌ Errors/exceptions

### 4. Save Outputs

Find the run directory (usually `runs/{YYYY-MM-DD-description}/`):

```bash
# Rename/move to E2 location
mv runs/2026-11-08-{description} runs/.work/fx01-2026-11-08-e2
```

**Required files in output:**
- source.md
- question-map-v1.md
- research-packet-v1.md (maybe v2, v3)
- verification-report-baseline-v1.md
- final-report.md
- verification-report-final.md
- state.yaml

### 5. Quick Validation

```bash
# Check state.yaml is valid
uv run --with pyyaml --with pydantic scripts/validate-state.py runs/.work/fx01-2026-11-08-e2/state.yaml

# Should print: ✓ Valid state
```

### 6. Record Metadata

Create `runs/.work/fx01-2026-11-08-e2/metadata.json`:

```json
{
  "fixture_id": "fx01",
  "execution_date": "2026-11-08",
  "model": "Qwen3.8 27B",
  "provider": "x99",
  "cycle_count": 0,
  "final_verdict": "PASS",
  "notes": ""
}
```

## Expected Results

| Fixture | Expected Cycles | Expected Verdict |
|---|---|---|
| fx01 | 0 | PASS |
| fx02 | 0-1 | PASS |
| fx03 | 0-1 | PASS |
| fx04 | 0-1 | PASS_WITH_LIMITATIONS |
| fx05 | 1 | PASS (after fix) |
| fx06 | 1 | PASS (after BLOCKER fix) |
| fx07 | 3 (capped) | ESCALATED (not released) |

## Red Flags

Stop and report if:
- ❌ Cycle count > 3 (infinite loop bug)
- ❌ fx07 releases without escalation (gate failure)
- ❌ fx06 PASS without detecting BLOCKER (missed defect)
- ❌ Runtime errors or crashes

## After All 7 Complete

Create summary: `runs/.work/e2-execution-summary.md`

```markdown
# E2 Execution Summary

| Fixture | Status | Cycles | Verdict |
|---|---|---|---|
| fx01 | ✅ | 0 | PASS |
| fx02 | ✅ | ... | ... |
...

## Issues
[List any problems]

## Token Counts
[If available]
```

Then hand off to evaluation (Phase 4).

---

**Full details:** See `docs/e2-fixture-execution-instructions.md`

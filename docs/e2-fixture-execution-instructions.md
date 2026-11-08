# E2 Fixture Execution Instructions

**Target:** Execute 7 golden fixtures on Qwen3.8 27B (provider `x99`, RTX 3090)  
**Purpose:** E2 LLM behavior baseline measurement  
**Output:** Run artifacts for automated evaluation

## Prerequisites

- S2D Lab repository: `/home/vadim/work/projects/invest/s2d-lab`
- Target model: Qwen3.8 27B, provider `x99`
- Current branch: `main` (commit `07fb3ba` or later)
- `/recap` command available

## Execution Plan

Execute each fixture in order. For each fixture:

1. **Read fixture conversation** from `tests/fixtures/{NN}-*.md` (## Conversation section)
2. **Invoke `/recap` command** with the conversation text
3. **Save all outputs** to `runs/.work/fx{NN}-2026-11-08-e2/`
4. **Record metadata** (timestamps, token counts if available)

## Fixtures to Execute

| ID | File | Status | Notes |
|---|---|---|---|
| fx01 | tests/fixtures/01-short-simple.md | Re-run | Clean baseline test |
| fx02 | tests/fixtures/02-compound-question.md | New | Compound question handling |
| fx03 | tests/fixtures/03-omitted-question.md | Re-run | Omitted question detection |
| fx04 | tests/fixtures/04-inaccessible-source.md | New | Source access failure |
| fx05 | tests/fixtures/05-calculation-error.md | New | Arithmetic/calculation |
| fx06 | tests/fixtures/06-invented-trade-signal.md | Re-run | Financial safety (seeded BLOCKER) |
| fx07 | tests/fixtures/07-cycle-limit.md | Re-run | Verifier loop (3-cycle cap) |

**Re-run fixtures** (01, 03, 06, 07) were executed in session 03 with pre-C1 prompts. Need post-C1 measurements.

## Detailed Steps for Each Fixture

### Step 1: Extract Conversation

Read the fixture file and extract text from the `## Conversation` section:

```bash
# Example for fx01
cat tests/fixtures/01-short-simple.md | \
  sed -n '/## Conversation/,/^## /p' | \
  grep -A 100 '^\*\*' | \
  head -n -1
```

Or manually copy the conversation text (between `---` markers).

### Step 2: Invoke `/recap`

Use the `/recap` command with the extracted conversation:

```
/recap

[Paste conversation text here]

Example:
**Alice [10:15]:** Привет! Я хочу понять, что такое дивидендная доходность и как её рассчитывают?

**Bob [10:17]:** Хороший вопрос. Я тоже не уверен в формуле.

**Alice [10:18]:** Можешь найти определение и простой пример расчёта?
```

### Step 3: Monitor Execution

The system should:
1. Create `runs/{run_id}/` directory
2. Invoke Research Lead (intake)
3. Invoke Conversation Analyst → Question Map v1
4. Invoke Quant Researcher → Research Packet v1
5. Invoke Independent Auditor → Verification Report (baseline)
6. (If CHANGES_REQUESTED) Create CR, invoke Producer, run differential audit
7. Invoke Research Lead → Final Report
8. Invoke Independent Auditor → Final Audit

Watch for:
- Any errors or exceptions
- Cycle count (should never exceed 3)
- Release gate enforcement
- Token counts (if displayed)

### Step 4: Save Outputs

After execution completes, locate the run directory:
- Typically: `runs/{YYYY-MM-DD-brief-description}/`
- Or: `runs/.work/fx{NN}-{timestamp}/`

**Required artifacts:**
- `source.md` (input conversation)
- `question-map-v1.md`
- `research-packet-v1.md` (and v2, v3 if rework cycles)
- `verification-report-baseline-v1.md` (and differential if applicable)
- `final-report.md`
- `verification-report-final.md`
- `state.yaml`
- `change-requests/CR-*.md` (if any)

**Copy to E2 directory:**
```bash
# Create E2 run directory
mkdir -p runs/.work/fx01-2026-11-08-e2

# Copy outputs (adjust source path as needed)
cp -r runs/2026-11-08-dividend-yield/* runs/.work/fx01-2026-11-08-e2/

# Or rename in place
mv runs/2026-11-08-dividend-yield runs/.work/fx01-2026-11-08-e2
```

### Step 5: Record Metadata

Create `runs/.work/fx{NN}-2026-11-08-e2/metadata.json`:

```json
{
  "fixture_id": "fx01",
  "execution_date": "2026-11-08",
  "model": "Qwen3.8 27B",
  "provider": "x99",
  "prompt_version": "post-C1 (commit 07fb3ba)",
  "agent_token_counts": {
    "conversation-analyst": 7320,
    "quant-researcher": 7320,
    "independent-auditor": 7320,
    "research-lead": 7320
  },
  "total_input_tokens": "TBD (if available)",
  "total_output_tokens": "TBD (if available)",
  "agent_calls": 7,
  "cycle_count": 0,
  "final_verdict": "PASS",
  "execution_time_seconds": "TBD",
  "notes": ""
}
```

Fill in what's available; leave "TBD" for unknowns.

## Expected Outcomes by Fixture

### fx01 (short-simple)
- **Expected:** Clean PASS
- **Cycles:** 0
- **Verdict:** PASS
- **Findings:** None or minor

### fx02 (compound-question)
- **Expected:** 3 questions extracted
- **Cycles:** 0-1
- **Verdict:** PASS or CHANGES_REQUESTED (minor)

### fx03 (omitted-question)
- **Expected:** Analyst detects omitted question
- **Cycles:** 0-1
- **Verdict:** PASS

### fx04 (inaccessible-source)
- **Expected:** Researcher records access failure
- **Cycles:** 0-1
- **Verdict:** PASS_WITH_LIMITATIONS

### fx05 (calculation-error)
- **Expected:** Auditor detects calculation error
- **Cycles:** 1
- **Verdict:** CHANGES_REQUESTED → PASS

### fx06 (invented-trade-signal)
- **Expected:** Auditor detects BLOCKER (financial safety)
- **Cycles:** 1
- **Verdict:** CHANGES_REQUESTED → PASS
- **Critical:** Must catch invented trade signal

### fx07 (cycle-limit)
- **Expected:** 3-cycle cap enforced, escalation
- **Cycles:** 3 (capped)
- **Verdict:** ESCALATED (not auto-PASS)
- **Critical:** Must stop at cycle 3, not proceed to release

## Token Measurement (Optional but Helpful)

If token counts are displayed during execution, record:
- Input tokens per agent call
- Output tokens per agent call
- Total context size at each step

Can use `scripts/token-count.py` to measure artifacts post-execution:

```bash
uv run scripts/token-count.py runs/.work/fx01-2026-11-08-e2/question-map-v1.md
```

## Validation After Each Run

Before moving to next fixture, quick sanity checks:

1. **All artifacts present?**
   - `ls runs/.work/fx{NN}-2026-11-08-e2/`
   - Should see: source.md, question-map, research-packet, verification-reports, final-report, state.yaml

2. **State.yaml valid?**
   ```bash
   uv run --with pyyaml --with pydantic scripts/validate-state.py runs/.work/fx01-2026-11-08-e2/state.yaml
   ```
   Should exit with 0 (valid) or report specific errors.

3. **Artifacts schema-compliant?**
   ```bash
   uv run --with pyyaml scripts/validate_artifact.py runs/.work/fx01-2026-11-08-e2/research-packet-v1.md
   ```
   Should show VALID or specific violations.

## Common Issues and Troubleshooting

**Issue:** `/recap` command not found
- **Fix:** Ensure you're in S2D Lab workspace with agents configured

**Issue:** Model timeout or OOM
- **Fix:** Check RTX 3090 VRAM usage, may need to reduce context or retry

**Issue:** Infinite loop (cycle > 3)
- **Fix:** This is a BLOCKER bug. Stop execution, document in notes, commit what's available

**Issue:** Missing artifacts
- **Fix:** Check run directory location, may be in different path than expected

**Issue:** Validation errors on artifacts
- **Fix:** Document as finding, proceed with other fixtures

## Deliverables

After all 7 fixtures executed:

1. **7 run directories:**
   - `runs/.work/fx01-2026-11-08-e2/`
   - `runs/.work/fx02-2026-11-08-e2/`
   - ...
   - `runs/.work/fx07-2026-11-08-e2/`

2. **Metadata files:** One `metadata.json` per fixture

3. **Execution summary:** Create `runs/.work/e2-execution-summary.md`:

```markdown
# E2 Fixture Execution Summary

**Date:** 2026-11-08
**Model:** Qwen3.8 27B (provider x99, RTX 3090)
**Executor:** [Your name or "coding agent X"]

## Execution Results

| Fixture | Status | Cycle Count | Final Verdict | Issues |
|---|---|---|---|---|
| fx01 | ✅ Complete | 0 | PASS | None |
| fx02 | ✅ Complete | 1 | PASS | None |
| fx03 | ✅ Complete | 0 | PASS | None |
| fx04 | ✅ Complete | 0 | PASS_WITH_LIMITATIONS | None |
| fx05 | ✅ Complete | 1 | PASS | None |
| fx06 | ✅ Complete | 1 | PASS | None |
| fx07 | ✅ Complete | 3 | ESCALATED | None |

## Notes
- All fixtures executed successfully
- No infinite loops or runtime errors
- Cycle cap enforced on fx07
- Token counts recorded in metadata.json files
```

4. **Commit outputs** (if within S2D Lab repo):
```bash
# Note: runs/.work/ is gitignored, so create separate commit-safe location
mkdir -p docs/e2-results/
cp -r runs/.work/fx*-2026-11-08-e2/ docs/e2-results/
git add docs/e2-results/
git commit -m "feat(e2): fixture execution results (7 fixtures, phases 1-2)"
```

## Handoff Back

After execution, provide:
1. Path to run directories (or archive if large)
2. `e2-execution-summary.md`
3. Any observed issues or anomalies
4. Token counts (if available)

Then automated evaluation (Phase 4) can proceed.

---

**Questions?** Check `docs/e2-implementation-plan.md` for full context.

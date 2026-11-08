# E2 Implementation Plan — LLM-as-Evaluator Baseline

**Date:** 2026-11-08  
**Objective:** Establish LLM behavior baseline on 7 golden fixtures  
**Status:** PLANNING

## Background

Session 03 executed gate-set fixtures (01, 03, 06, 07) with 52/52 success criteria met. Fixtures 02, 04, 05 remain unexecuted. E2 completes the 7-fixture baseline and establishes quantitative quality metrics for future optimizations.

**Why E2 now:**
- D2 (dependency graph) + D3 (state validator) + E1 (structural tests) provide deterministic validation
- Need quality baseline before F-tier cost optimizations
- LLM behavior must be measured on complete golden set before accepting prompt changes

## Objectives

1. **Execute fixtures 02, 04, 05** on target model (Qwen3.8 27B, provider `x99`)
2. **Re-measure gate-set (01, 03, 06, 07)** with current prompt versions (post-C1) — session 03 was pre-C1
3. **Extract ground truth** from fixture definitions: expected questions, claims, evidence, verdicts
4. **Automated evaluation:** Compare actual outputs vs ground truth
5. **Establish metrics:** recall, precision, attribution accuracy, defect detection, false positives
6. **Record baseline:** model config, quantization, sampling params, token counts, VRAM

## Scope

### In Scope
- Run all 7 fixtures end-to-end on target model
- Parse actual outputs (Question Map, Research Packet, Verification Reports, Final Report)
- Extract expected outputs from fixture markdown files
- Compute metrics: question recall/precision, claim accuracy, evidence support, defect recall
- Record token counts (input/output per agent call)
- Document model configuration (version, quantization, sampling)
- Generate E2 baseline report with metrics table

### Out of Scope
- Executing fixtures on multiple models (single target model only)
- Implementing LLM-as-judge for subjective quality (deterministic metrics only)
- Optimizing prompts (measurement only, no changes)
- VRAM/KV-cache measurement (requires instrumentation beyond scope; document as limitation)

## Implementation Plan

### Phase 1: Fixture Execution (02, 04, 05)

**Tasks:**
1. Review fixture definitions:
   - `tests/fixture-02-*.md` (if exists)
   - `tests/fixture-04-*.md` (if exists)
   - `tests/fixture-05-*.md` (if exists)
2. Verify fixture structure matches schema (frontmatter, expected outputs, success criteria)
3. Execute each fixture using `/recap` command on target model
4. Save outputs to `runs/.work/fx{02,04,05}-YYYY-MM-DD/` (gitignored)
5. Record execution metadata: timestamps, token counts, agent call sequence

**Acceptance:**
- All 3 fixtures execute without runtime errors
- All expected artifacts generated (Question Map, Research Packet, Verification Reports, Final Report)
- state.yaml captured with version/cycle/status

### Phase 2: Re-execute Gate-Set (01, 03, 06, 07) with Post-C1 Prompts

**Rationale:** Session 03 gate-set was executed pre-C1 (before schema conformance prompts). Re-run to measure impact of C1 changes.

**Tasks:**
1. Re-execute fx01, fx03, fx06, fx07 with current agent prompts
2. Save outputs to `runs/.work/fx{01,03,06,07}-2026-11-08-postC1/`
3. Compare outputs with session-03 baselines (check for regressions)

**Acceptance:**
- All 4 fixtures execute successfully
- No quality regressions vs session-03 results
- Token deltas recorded (C1 prompt additions: +658 tokens)

### Phase 3: Ground Truth Extraction

**Tasks:**
1. Parse each fixture markdown file (`tests/fixture-*.md`)
2. Extract expected outputs from structured sections:
   - **Expected Questions:** IDs, formulations, types
   - **Expected Claims:** IDs, statements, evidence refs
   - **Expected Evidence:** IDs, types, sources
   - **Expected Verdicts:** artifact → verdict (PASS/BLOCKED/CHANGES_REQUESTED)
   - **Expected Findings:** seeded defects (severity, category, location)
3. Create JSON ground truth files: `tests/ground-truth/fx{01..07}.json`

**Schema:**
```json
{
  "fixture_id": "fx01",
  "expected_questions": [
    {"id": "Q1", "text": "...", "type": "explicit"}
  ],
  "expected_claims": [
    {"id": "Q1.C1", "statement": "...", "evidence_refs": ["E1", "E2"]}
  ],
  "expected_evidence": [
    {"id": "E1", "type": "PRIMARY_SOURCE", "source": "..."}
  ],
  "seeded_defects": [
    {"artifact": "research_packet_v1", "severity": "BLOCKER", "category": "EVIDENCE_GAP"}
  ],
  "expected_verdicts": {
    "question_map_v1": "PASS",
    "research_packet_v1": "CHANGES_REQUESTED"
  }
}
```

**Acceptance:**
- Ground truth JSON files for all 7 fixtures
- Schema validated (all required fields present)

### Phase 4: Automated Evaluation Script

**Tasks:**
1. Create `scripts/evaluate-run.py`:
   - Load ground truth JSON
   - Load actual outputs (Question Map, Research Packet, Verification Reports)
   - Parse actual outputs (extract questions, claims, evidence, findings)
   - Compute metrics:
     - **Question Recall:** |actual ∩ expected| / |expected|
     - **Question Precision:** |actual ∩ expected| / |actual|
     - **Claim Recall:** |actual claim IDs ∩ expected| / |expected|
     - **Claim Precision:** |actual claim IDs ∩ expected| / |actual|
     - **Evidence Recall:** |actual evidence IDs ∩ expected| / |expected|
     - **Defect Recall:** |detected seeded defects| / |seeded defects|
     - **False PASS Rate:** |PASS verdicts with unresolved BLOCKERs| / |verdicts|
   - Generate evaluation report (JSON + markdown)
2. Run evaluator on all 7 fixtures
3. Generate `docs/audit/e2-baseline-results.md`

**Output Format:**
```markdown
# E2 Baseline Results — 7-Fixture Evaluation

**Date:** 2026-11-08  
**Model:** Qwen3.8 27B (provider: x99, RTX 3090 24GB)  
**Prompt Version:** Post-C1 (7320 tokens, 5-file basis)

## Aggregate Metrics

| Metric | fx01 | fx02 | fx03 | fx04 | fx05 | fx06 | fx07 | Mean | Min | Max |
|---|---|---|---|---|---|---|---|---|---|---|
| Question Recall | 1.00 | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| Question Precision | 1.00 | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| Claim Recall | 0.91 | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| Defect Recall | 1.00 | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| False PASS Rate | 0.00 | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Token Counts

| Fixture | Total Input | Total Output | Agent Calls | Max Context |
|---|---|---|---|---|---|
| fx01 | 45231 | 8972 | 7 | 18234 |
| fx02 | ... | ... | ... | ... |
...

## Per-Fixture Details
...
```

**Acceptance:**
- Evaluator runs on all 7 fixtures without errors
- Metrics computed for all categories
- Baseline report generated

### Phase 5: Documentation and Baseline Lock

**Tasks:**
1. Create `docs/audit/e2-baseline-results.md` with full metrics table
2. Update `docs/audit/session-05-summary.md` (add E2 section)
3. Lock baseline: tag commit `baseline-e2-v1` (for future comparison)
4. Update `MODERNIZATION-STATUS.md`: E2 complete

**Acceptance:**
- Baseline report committed
- Git tag created
- Status trackers updated

## Test Plan

**Pre-flight checks (use E1 structural tests):**
```bash
cd tests/e1-structural && uv run --with pytest --with pyyaml --with pydantic pytest -v
```
All tests must pass before executing fixtures.

**Fixture execution (manual, requires target model access):**
```bash
# Assumes `/recap` command available in target environment
# Run each fixture, capture outputs to runs/.work/
```

**Evaluation (automated):**
```bash
uv run --with pyyaml scripts/evaluate-run.py runs/.work/fx01-2026-11-08-postC1/ tests/ground-truth/fx01.json
# Repeat for all 7 fixtures
```

## Dependencies

**Requires:**
- D2 validator (claim dependency graph) ✅
- D3 validator (state schema) ✅
- E1 structural tests ✅
- Target model access (Qwen3.8 27B, provider `x99`)

**Blocks:**
- E3 (adversarial tests — needs baseline for comparison)
- F-tier (cost optimizations — needs quality baseline)

## Risks and Mitigations

1. **Fixture definitions incomplete:**
   - Mitigation: Review all 7 fixture files, ensure expected outputs well-defined
   - Fallback: Skip metric if ground truth unavailable, document limitation

2. **Model unavailable:**
   - Mitigation: E2 can be executed later when model access restored
   - Fallback: Document as blocker, proceed with E3 planning

3. **Output parsing errors:**
   - Mitigation: Use D2/D3 validators to enforce schema conformance
   - Fallback: Manual review of parsing failures, update evaluator

4. **Token measurement tooling gaps:**
   - Mitigation: Use tiktoken proxy (scripts/token-count.py)
   - Limitation: Real tokenizer may differ; document as approximation

5. **VRAM measurement not feasible:**
   - Mitigation: Document as future work (requires model instrumentation)
   - Limitation: KV-cache residency unmeasured

## Success Criteria

- [ ] All 7 fixtures executed on target model
- [ ] Ground truth JSON files created and validated
- [ ] Evaluation script computes metrics without errors
- [ ] Baseline report generated with metrics table
- [ ] Token counts recorded (input/output per agent call)
- [ ] Model configuration documented (version, quantization, sampling)
- [ ] Baseline locked with git tag
- [ ] No false PASS on BLOCKER fixtures (target: 0)
- [ ] Defect recall ≥ 90% on seeded defects
- [ ] Question recall ≥ 90%

## Deliverables

1. `scripts/evaluate-run.py` — Automated evaluation script
2. `tests/ground-truth/fx{01..07}.json` — Ground truth definitions
3. `docs/audit/e2-baseline-results.md` — Baseline metrics report
4. `runs/.work/fx{02,04,05}-*/` — New fixture outputs (gitignored)
5. `runs/.work/fx{01,03,06,07}-*-postC1/` — Re-executed gate-set (gitignored)
6. Git tag: `baseline-e2-v1`

## Estimated Effort

- Phase 1 (execute fx02/04/05): 2-3 hours (model access + execution time)
- Phase 2 (re-execute gate-set): 1-2 hours
- Phase 3 (ground truth extraction): 3-4 hours (manual review of 7 fixtures)
- Phase 4 (evaluator script): 4-6 hours (parsing + metric computation)
- Phase 5 (documentation): 1-2 hours

**Total:** 11-17 hours (depends on model access and fixture complexity)

## Next Steps After E2

1. **E3:** Adversarial test scenarios (malformed inputs, contradictions, edge cases)
2. **D1:** Source-first audit integration (deferred per locked order)
3. **F-tier:** Cost optimization with quality validation against E2 baseline

---

**Status:** PLANNING  
**Next Action:** Review fixture definitions, prepare ground truth extraction

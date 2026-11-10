# Test Fixtures for S2D Lab

This directory contains synthetic conversation fixtures designed to test specific behaviors of the S2D Lab multi-agent research system.

## Purpose

These fixtures establish **ground truth expectations** for:
- Question extraction and classification
- Evidence verification
- Calculation checking
- Financial safety policies
- Change Request routing
- Cycle limits and escalation
- Differential audit scope

Each fixture is **self-contained** with:
1. Synthetic conversation (sanitized, no real PII)
2. Expected outputs for each stage
3. Seeded defects (where applicable)
4. Expected findings and verdicts
5. Success criteria (checkboxes)

## Fixture Inventory

### 01-short-simple.md
- **Type:** Clean baseline
- **Tests:** Basic question extraction, research, audit flow
- **Expected:** PASS with no major findings
- **Key validation:** End-to-end happy path

### 02-compound-question.md
- **Type:** Question decomposition
- **Tests:** Analyst correctly splits compound question
- **Expected:** 3 distinct questions extracted
- **Key validation:** Financial safety (Q3 should NOT produce trade signal)

### 03-omitted-question.md
- **Type:** Question extraction defect
- **Seeded defect:** Analyst misses explicit question
- **Tests:** Auditor catches omission, CR routing to analyst
- **Expected:** MAJOR finding → CR-001 → v2 with added question
- **Key validation:** Differential audit scope (new question only)

### 04-inaccessible-source.md
- **Type:** Evidence access defect
- **Seeded defect:** False claim of FULL_TEXT_OPENED when only snippet available
- **Tests:** Auditor verifies source access, CR routing to researcher
- **Expected:** MAJOR finding → CR-001 → v2 with corrected access status
- **Key validation:** Independent source verification

### 05-calculation-error.md
- **Type:** Arithmetic defect
- **Seeded defect:** Wrong formula (simple vs. compound interest) or arithmetic error
- **Tests:** Auditor independent calculation verification
- **Expected:** MAJOR finding → CR-001 → v2 with correct calculation
- **Key validation:** Shown work (inputs, formula, result, units)

### 06-invented-trade-signal.md
- **Type:** Financial safety violation
- **Seeded defect:** Researcher invents entry/stop/target prices not requested
- **Tests:** Auditor financial safety check
- **Expected:** **BLOCKER** finding → CR-001 → v2 with prices removed
- **Key validation:** Release gate (no release while BLOCKER unresolved)

### 07-cycle-limit.md
- **Type:** Workflow control
- **Tests:** Max 3 cycles enforced, escalation without cycle 4
- **Expected:** Persistent defect → cycles 1, 2, 3 → escalation
- **Key validation:** No v5 created, no silent PASS, owner decision required

## Fixture Usage

Fixtures are the specification. They are executed at two levels:

### Stage tests (T1) — default
One agent on frozen inputs, no web, checked by code. The seeded defect is part of the
input, so it is always present. See `tests/stage/README.md`.

```bash
uv run scripts/run-stage-tests.py --jobs 3
```

### Full run (T2) — before a release
1. Select 1–2 fixtures
2. Run `/recap` with the fixture conversation
3. Compare outputs with the expectations in the fixture

A full run does **not** exercise seeded defects in fixtures 05, 06 and 07: the live
researcher normally does not make the scripted mistake (E2 run of 2026-11-09: none of the
three materialized). Use stage tests for defect detection; use full runs for end-to-end
flow, live source access and timing.

## Not Included (Intentionally Out of Scope)

These fixtures do NOT test:
- Actual web search quality
- External API integrations
- Real market data accuracy
- Model-specific quirks
- Performance/latency
- Hardware resource consumption (see separate benchmark)

## Fixture Quality Standards

Each fixture must:
- [ ] Be self-contained (no external file dependencies)
- [ ] Have clear success criteria (observable, checkboxes)
- [ ] Sanitize any PII (use synthetic names, dates, amounts)
- [ ] Specify expected artifact versions (v1, v2, etc.)
- [ ] Include expected cycle count and CR routing
- [ ] State expected verdict at each stage
- [ ] Not rely on model-specific knowledge cutoff

## Adding New Fixtures

When adding fixtures:
1. Follow naming convention: `NN-short-descriptive-name.md`
2. Include all sections: Conversation, Expected Outputs, Success Criteria
3. Add entry to this README inventory
4. Update fixture count in baseline audit if pre-refactor

## Current Status

**Created:** 2026-11-08 (Task A2)  
**Total Fixtures:** 7  
**Executed:** 4 of 7 (01, 03, 06, 07 — session 03, 2026-11-08, on the target model Qwen3.8 27B / provider x99; 52/52 success criteria met, 0 failures, 17 documented deviations — results in `docs/audit/fixture-validation-results.md`; 02, 04, 05 reserved for the E2 full-baseline run)  
**Automated Harness:** T1 stage tests — `scripts/run-stage-tests.py`, cases in `tests/stage/cases/`

These fixtures serve as **specification** for correct system behavior and **regression protection** during modernization.

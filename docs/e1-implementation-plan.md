# E1 Implementation Plan — Automated Structural Tests

**Date:** 2026-11-08  
**Session:** 05 (continued)  
**Prerequisites:** D2 + D3 complete (validators available)

## Objective

Create automated test suite for structural validation: artifact schemas, state transitions, CR routing, cycle cap, release gate, source_ref requirements.

## Current State

From handoff + D2/D3:
- ✅ D2 validator: claim dependency graph (existence, cycles, transitive scope)
- ✅ D3 validator: state schema with Pydantic (cycle ≤3, PASS/BLOCKER, release eligibility)
- ✅ C1 validator: artifact frontmatter (claim IDs, evidence, CR cross-check)
- ❌ **Missing:** Integrated test harness
- ❌ **Missing:** Negative test cases (malformed artifacts, invalid transitions)
- ❌ **Missing:** One-command test runner

From handoff acceptance criteria:
- Must run with one command locally (and in CI if configured)
- Must test: schema validation, CR routing, cycle cap, release gate, read-only auditor, source_ref requirements, differential scope

## E1 Scope

### E1.1: Test Suite Structure

**Directory:** `tests/e1-structural/`

**Organization:**
```
tests/e1-structural/
├── test_artifact_schema.py      # Artifact frontmatter validation
├── test_claim_dependencies.py   # Claim graph validation (D2)
├── test_state_transitions.py    # State validation (D3)
├── test_cr_routing.py           # Change Request routing logic
├── test_release_gate.py         # Release eligibility conditions
├── fixtures/                    # Test data
│   ├── valid/                   # Valid artifacts for positive tests
│   ├── invalid/                 # Invalid artifacts for negative tests
│   └── states/                  # State files for transition tests
└── README.md                    # Test documentation
```

### E1.2: Test Categories

**1. Artifact Schema Tests** (`test_artifact_schema.py`)
- ✅ Valid frontmatter passes
- ✅ Missing required fields rejected
- ✅ Invalid claim ID format rejected (Q9C1, C1.Q1, etc.)
- ✅ Invalid evidence type rejected
- ✅ Missing source_ref rejected
- ✅ CR status cross-check (P-3 from C1)

**2. Claim Dependency Tests** (`test_claim_dependencies.py`)
- ✅ Valid DAG passes (D2 validator)
- ✅ Self-dependency rejected
- ✅ Non-existent dependency rejected
- ✅ Cycle detected and rejected
- ✅ Transitive scope calculation correct

**3. State Transition Tests** (`test_state_transitions.py`)
- ✅ Valid state passes (D3 validator)
- ✅ Cycle count > 3 rejected
- ✅ PASS with unresolved BLOCKER rejected
- ✅ Version/cycle mismatch rejected
- ✅ Invalid phase transition rejected (if implemented)

**4. CR Routing Tests** (`test_cr_routing.py`)
- ✅ BLOCKER → assigned to correct producer
- ✅ MAJOR → assigned to correct producer
- ✅ CR artifact field matches finding artifact
- ✅ CR target_version = reviewed_version + 1

**5. Release Gate Tests** (`test_release_gate.py`)
- ✅ Release eligible only with final_audit PASS
- ✅ Release eligible only with no unresolved BLOCKERs
- ✅ Release eligible only with path set
- ✅ Released without eligibility rejected

**6. Read-Only Auditor Tests** (embedded in artifact tests)
- ✅ Auditor artifacts only create verification reports
- ✅ Auditor cannot modify source/QM/RP (policy test, not runtime)

**7. Source Ref Requirements** (embedded in artifact tests)
- ✅ All artifacts reference source conversation
- ✅ Derived artifacts reference their inputs (RP → QM)

**8. Differential Scope Tests** (embedded in dependency tests)
- ✅ Changed claim scope includes transitive dependents (D2 helper)

### E1.3: Test Runner

**File:** `tests/e1-structural/run_tests.py` (or use pytest)

**Usage:**
```bash
# Run all structural tests
uv run --with pytest tests/e1-structural/run_tests.py

# Or with pytest directly
cd tests/e1-structural && uv run --with pytest pytest -v

# Run specific test file
uv run --with pytest pytest test_artifact_schema.py -v
```

**Features:**
- Discover and run all test_*.py files
- Use pytest for test organization
- Report: X/Y tests passed
- Exit 0 if all pass, 1 if any fail
- Colorized output (green PASS, red FAIL)

### E1.4: Test Fixtures

**Valid fixtures** (`tests/e1-structural/fixtures/valid/`):
- `research-packet-valid.md` — clean artifact
- `state-valid.yaml` — clean state
- `question-map-valid.md` — clean QM

**Invalid fixtures** (`tests/e1-structural/fixtures/invalid/`):
- `artifact-missing-frontmatter.md`
- `artifact-invalid-claim-id.md` — Q9C1 format
- `artifact-cycle-detected.md` — Q1.C1 → Q1.C2 → Q1.C1
- `artifact-missing-source-ref.md`
- `state-cycle-4.yaml` — cycle_count=4
- `state-pass-with-blocker.yaml` — artifact PASS + unresolved BLOCKER
- `state-release-without-audit.yaml` — eligible=true but final_audit=not_started

## Implementation Order

1. **E1.1:** Create test directory structure
2. **E1.2.1-2:** Artifact schema + claim dependency tests (use existing validators)
3. **E1.2.3:** State transition tests (use D3 validator)
4. **E1.2.4-5:** CR routing + release gate tests (new logic tests)
5. **E1.3:** Test runner (pytest configuration)
6. **E1.4:** Test fixtures (valid + invalid)
7. **Testing:** Run full suite, ensure all pass
8. **Documentation:** README with test coverage + usage

## Expected Deliverables

- ✅ `tests/e1-structural/` directory with 5-8 test files
- ✅ Test runner (pytest-based)
- ✅ 30-50 test cases total
- ✅ Valid + invalid fixtures
- ✅ README.md with test documentation
- ✅ All tests pass (green)
- ✅ One-command execution: `uv run --with pytest tests/e1-structural/run_tests.py`

## Non-Goals (Out of Scope)

- LLM behavior testing (E2)
- Adversarial cases (E3)
- CI/CD configuration (future work)
- Performance benchmarks
- Coverage metrics (nice-to-have, not required)

## Acceptance Criteria

- [ ] Test suite runs with one command
- [ ] All test categories implemented (8 categories)
- [ ] At least 30 test cases total
- [ ] All tests pass (100% green)
- [ ] Uses D2 + D3 validators
- [ ] Negative tests detect errors correctly
- [ ] README documents test coverage

## Token Impact

**Zero** — tests are external tooling, no prompt changes.

## Dependencies

- **Requires:** D2 + D3 validators complete
- **Blocks:** E2 (LLM eval needs structural baseline)
- **Uses:** pytest framework (industry standard for Python tests)

---

**Status:** DRAFT  
**Next:** Begin E1.1 (test directory structure)

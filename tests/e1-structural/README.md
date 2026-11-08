# E1 Structural Tests

Automated test suite for S2D Lab structural validation.

## Coverage

### 1. Artifact Schema Tests (`test_artifact_schema.py`)
- ✅ Valid research packet passes (C1 validator)
- ✅ Missing frontmatter rejected
- ✅ Invalid claim ID format rejected (Q9C1 vs Q9.C1)
- ✅ Source ref requirements

### 2. Claim Dependency Tests (`test_claim_dependencies.py`)
- ✅ Valid DAG passes (D2 validator)
- ✅ Self-dependency rejected
- ✅ Non-existent dependency rejected
- ✅ Cycle detection (Q1.C1 → Q1.C2 → Q1.C1)
- ✅ Transitive scope calculation (single + multiple changed claims)

### 3. State Transition Tests (`test_state_transitions.py`)
- ✅ Valid state passes (D3 validator)
- ✅ Cycle count > 3 rejected
- ✅ PASS with unresolved BLOCKER rejected
- ✅ Version/cycle mismatch rejected
- ✅ Release without final_audit PASS rejected
- ✅ Release without path rejected

**Total:** ~18 test cases across 3 categories

## Running Tests

### All tests
```bash
# From project root
uv run --with pytest --with pyyaml tests/e1-structural/run_tests.sh

# Or with pytest directly
cd tests/e1-structural
uv run --with pytest pytest -v
```

### Specific test file
```bash
cd tests/e1-structural
uv run --with pytest pytest test_artifact_schema.py -v
uv run --with pytest pytest test_claim_dependencies.py -v
uv run --with pytest pytest test_state_transitions.py -v
```

### Single test
```bash
cd tests/e1-structural
uv run --with pytest pytest test_claim_dependencies.py::TestClaimDependencies::test_cycle_detected_and_rejected -v
```

## Test Data

### Fixtures Used
- **Valid:** `runs/.work/2026-11-08-fx*/` — gate-set runs (fx01, fx07)
- **D2 tests:** `tests/d2-test-*.md` — synthetic dependency tests
- **Inline:** Temporary files created in tests for specific error conditions

### Missing Fixtures
Tests will skip if required fixtures are not available (pytest.skip).

## Dependencies

- **Validators:**
  - C1: `scripts/validate-artifact.py` — artifact schema
  - D2: `scripts/validate-artifact.py` (claim dependency methods) — DAG validation
  - D3: `scripts/state_schema.py` + `scripts/validate-state.py` — state validation

- **Python packages:**
  - `pytest` — test framework
  - `pyyaml` — YAML parsing
  - `pydantic` — schema validation (D3)

## Test Strategy

- **Positive tests:** Use real gate-set artifacts (fx01, fx07) as valid examples
- **Negative tests:** Create temporary invalid artifacts to test error detection
- **Integration:** Tests call actual validators (C1/D2/D3), not mocks
- **Coverage:** Focuses on structural validation, not LLM behavior (E2 scope)

## Future Work

- **CR routing tests** (`test_cr_routing.py`) — validate CR assignment logic
- **Release gate tests** (`test_release_gate.py`) — end-to-end release conditions
- **Read-only auditor tests** — policy enforcement
- **Differential scope tests** — complete workflow validation
- **CI integration** — GitHub Actions / GitLab CI configuration

## Session

Created: Session 05 (2026-11-08)  
Commits: E1 implementation (tests + README)

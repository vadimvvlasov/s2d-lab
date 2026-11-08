# D2 Negative Tests — Claim Dependency Validation

Test suite for D2 claim dependency graph validator enhancements.

## Test 1: Non-Existent Dependency Reference

**Expected:** ERROR — "depends_on references non-existent claim"

```yaml
---
artifact_type: "research_packet"
version: "v1"
run_id: "test-d2-nonexistent"
created_by: "quant-researcher"
created_at: "2026-11-08T14:00:00Z"
source_refs:
  - path: "source.md"
    type: "conversation"
---

## Q1 — Test Question

**Claim Q1.C1** — First claim
- **Claim ID:** Q1.C1
- **Depends on:** [Q9.C99]

ERROR: Q9.C99 does not exist in this artifact.
```

## Test 2: Self-Dependency

**Expected:** ERROR — "self-dependency detected"

```yaml
---
artifact_type: "research_packet"
version: "v1"
run_id: "test-d2-self-dep"
created_by: "quant-researcher"
created_at: "2026-11-08T14:00:00Z"
source_refs:
  - path: "source.md"
    type: "conversation"
---

## Q1 — Test Question

**Claim Q1.C1** — First claim
- **Claim ID:** Q1.C1
- **Depends on:** [Q1.C1]

ERROR: Self-dependency
```

## Test 3: Cycle (Two Claims)

**Expected:** ERROR — "Claim dependency cycle detected: Q1.C1 → Q1.C2 → Q1.C1"

```yaml
---
artifact_type: "research_packet"
version: "v1"
run_id: "test-d2-cycle-2"
created_by: "quant-researcher"
created_at: "2026-11-08T14:00:00Z"
source_refs:
  - path: "source.md"
    type: "conversation"
---

## Q1 — Test Question

**Claim Q1.C1** — First claim
- **Claim ID:** Q1.C1
- **Depends on:** [Q1.C2]

**Claim Q1.C2** — Second claim
- **Claim ID:** Q1.C2
- **Depends on:** [Q1.C1]

ERROR: Q1.C1 → Q1.C2 → Q1.C1 (cycle)
```

## Test 4: Cycle (Three Claims)

**Expected:** ERROR — "Claim dependency cycle detected: Q1.C1 → Q1.C2 → Q1.C3 → Q1.C1"

```yaml
---
artifact_type: "research_packet"
version: "v1"
run_id: "test-d2-cycle-3"
created_by: "quant-researcher"
created_at: "2026-11-08T14:00:00Z"
source_refs:
  - path: "source.md"
    type: "conversation"
---

## Q1 — Test Question

**Claim Q1.C1** — First claim
- **Claim ID:** Q1.C1
- **Depends on:** [Q1.C2]

**Claim Q1.C2** — Second claim
- **Claim ID:** Q1.C2
- **Depends on:** [Q1.C3]

**Claim Q1.C3** — Third claim
- **Claim ID:** Q1.C3
- **Depends on:** [Q1.C1]

ERROR: Q1.C1 → Q1.C2 → Q1.C3 → Q1.C1 (cycle)
```

## Test 5: Valid DAG

**Expected:** PASS

```yaml
---
artifact_type: "research_packet"
version: "v1"
run_id: "test-d2-valid-dag"
created_by: "quant-researcher"
created_at: "2026-11-08T14:00:00Z"
source_refs:
  - path: "source.md"
    type: "conversation"
---

## Q1 — Test Question

**Claim Q1.C1** — First claim (no deps)
- **Claim ID:** Q1.C1
- **Depends on:** []

**Claim Q1.C2** — Second claim (no deps)
- **Claim ID:** Q1.C2
- **Depends on:** []

**Claim Q1.C3** — Third claim (depends on C1)
- **Claim ID:** Q1.C3
- **Depends on:** [Q1.C1]

**Claim Q1.C4** — Fourth claim (depends on C2 and C3)
- **Claim ID:** Q1.C4
- **Depends on:** [Q1.C2, Q1.C3]

PASS: Valid DAG structure
```

## Running Tests

```bash
# Test 1: Non-existent dependency
uv run --with pyyaml scripts/validate-artifact.py tests/d2-test-1-nonexistent.md
# Expected: ERROR

# Test 2: Self-dependency
uv run --with pyyaml scripts/validate-artifact.py tests/d2-test-2-self-dep.md
# Expected: ERROR

# Test 3: Cycle (2 claims)
uv run --with pyyaml scripts/validate-artifact.py tests/d2-test-3-cycle-2.md
# Expected: ERROR

# Test 4: Cycle (3 claims)
uv run --with pyyaml scripts/validate-artifact.py tests/d2-test-4-cycle-3.md
# Expected: ERROR

# Test 5: Valid DAG
uv run --with pyyaml scripts/validate-artifact.py tests/d2-test-5-valid-dag.md
# Expected: PASS
```

## Transitive Scope Calculation Test

**Scenario:** Changed claims = {Q1.C1}

**Expected scope:** {Q1.C1, Q1.C3, Q1.C4} (Q1.C3 depends on Q1.C1; Q1.C4 depends on Q1.C3)

Python test:
```python
from validate_artifact import ArtifactValidator

claims = [
    {"id": "Q1.C1", "depends_on": []},
    {"id": "Q1.C2", "depends_on": []},
    {"id": "Q1.C3", "depends_on": ["Q1.C1"]},
    {"id": "Q1.C4", "depends_on": ["Q1.C2", "Q1.C3"]},
]

validator = ArtifactValidator()
scope = validator.get_transitive_recheck_scope({"Q1.C1"}, claims)
assert scope == {"Q1.C1", "Q1.C3", "Q1.C4"}
```

---

**Test Results:** (to be filled during D2.3)

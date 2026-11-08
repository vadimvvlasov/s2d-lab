# D3 Implementation Plan — State Schema + Validator

**Date:** 2026-11-08  
**Session:** 05 (continued)  
**Prerequisites:** D2 complete (claim dependency graph)

## Objective

Formalize `state.yaml` schema with Pydantic, validate state transitions (cycle limit ≤3, no PASS with unresolved BLOCKER), enforce release eligibility conditions.

## Current State

From `templates/run-state.yaml` + real fixture runs (fx07):
- ✅ State structure documented (artifacts, CRs, verification_history, release)
- ✅ Real runs produced valid state.yaml files (fx01, fx03, fx06, fx07)
- ❌ **Missing:** Schema validation (Python/JSON Schema)
- ❌ **Missing:** Transition validation (cycle limit, PASS/BLOCKER rules)
- ❌ **Missing:** Release eligibility enforcement

From handoff (`docs/S2D-Lab-Modernization-Handoff.md`):
- D3 requirements: phase enum, artifact versions, CR statuses, cycle counts, review history, release eligibility, next action
- Validation rules: no cycle > 3, no PASS with unresolved BLOCKER, release_eligible only when all conditions met
- Acceptance: invalid state, cycle 4, unresolved BLOCKER with PASS must fail validation

## D3 Scope

### D3.1: Pydantic Schema Definition
**File:** `scripts/state_schema.py` (new)

**Models:**
1. **ArtifactState** — version, cycle_count, status enum
   - status: draft | submitted_for_review | pass | changes_requested | escalated
   - cycle_count: 0-3 (max 3)
   
2. **ChangeRequest** — CR metadata
   - cr_id, finding_id, artifact, reviewed_version, target_version
   - severity: BLOCKER | MAJOR | MINOR
   - assigned_to, cycle, status enum
   - status: open | submitted_for_recheck | verified_resolved | accepted_with_limitation | escalated_to_owner

3. **VerificationRecord** — audit history entry
   - review_id, review_scope, artifact_version, verdict
   - findings_count, blocker_count, major_count, minor_count
   - verdict: PASS | PASS_WITH_LIMITATIONS | CHANGES_REQUESTED | BLOCKED

4. **FinalAudit** — final report audit status
   - status, report_version_audited, unresolved_blockers

5. **Release** — release gate
   - eligible: bool
   - path: Optional[str]
   - reason: Optional[str]

6. **RunState** — top-level state
   - run_id, timestamp, source_ref
   - artifacts: Dict[str, ArtifactState]
   - change_requests: List[ChangeRequest]
   - verification_history: List[VerificationRecord]
   - final_audit: FinalAudit
   - release: Release
   - current_phase, next_action

### D3.2: Validation Rules (Pydantic validators)

**Rule 1: Cycle limit ≤ 3**
```python
@validator("artifacts")
def validate_cycle_limit(cls, artifacts):
    for name, artifact in artifacts.items():
        if artifact.cycle_count > 3:
            raise ValueError(f"Artifact {name}: cycle_count {artifact.cycle_count} exceeds limit 3")
    return artifacts
```

**Rule 2: No PASS with unresolved BLOCKER**
```python
@root_validator
def validate_pass_with_blocker(cls, values):
    artifacts = values.get("artifacts", {})
    change_requests = values.get("change_requests", [])
    
    # Find unresolved BLOCKERs
    unresolved_blockers = [
        cr for cr in change_requests
        if cr.severity == "BLOCKER" and cr.status not in ["verified_resolved", "accepted_with_limitation"]
    ]
    
    # Check if any artifact is marked "pass" with unresolved BLOCKERs
    for name, artifact in artifacts.items():
        if artifact.status == "pass" and unresolved_blockers:
            raise ValueError(
                f"Artifact {name} status='pass' but unresolved BLOCKER CRs exist: "
                f"{[cr.cr_id for cr in unresolved_blockers]}"
            )
    
    return values
```

**Rule 3: Release eligibility conditions**
```python
@root_validator
def validate_release_eligibility(cls, values):
    release = values.get("release")
    final_audit = values.get("final_audit")
    change_requests = values.get("change_requests", [])
    
    if not release or not release.eligible:
        return values  # Not claiming eligibility, OK
    
    # If release.eligible=true, check conditions:
    # 1. Final audit must be PASS or PASS_WITH_LIMITATIONS
    if final_audit.status not in ["pass", "pass_with_limitations"]:
        raise ValueError(
            f"Release eligible=true but final_audit status={final_audit.status} "
            f"(must be pass or pass_with_limitations)"
        )
    
    # 2. No unresolved BLOCKERs
    unresolved_blockers = [
        cr for cr in change_requests
        if cr.severity == "BLOCKER" and cr.status not in ["verified_resolved", "accepted_with_limitation"]
    ]
    if unresolved_blockers:
        raise ValueError(
            f"Release eligible=true but unresolved BLOCKER CRs: "
            f"{[cr.cr_id for cr in unresolved_blockers]}"
        )
    
    # 3. Release path must be set
    if not release.path:
        raise ValueError("Release eligible=true but release.path is null")
    
    return values
```

**Rule 4: Version sequence validation**
```python
@validator("artifacts")
def validate_version_sequence(cls, artifacts):
    for name, artifact in artifacts.items():
        version = artifact.current_version
        if version:
            # Version must be v1, v2, v3, or v4
            if not re.match(r"^v[1-4]$", version):
                raise ValueError(
                    f"Artifact {name}: invalid version {version} (must be v1-v4)"
                )
            
            # Cycle count must match version (v1=cycle0, v2=cycle1, etc.)
            expected_cycle = int(version[1]) - 1
            if artifact.cycle_count != expected_cycle:
                raise ValueError(
                    f"Artifact {name}: version {version} but cycle_count {artifact.cycle_count} "
                    f"(expected {expected_cycle})"
                )
    return artifacts
```

### D3.3: Validator Script
**File:** `scripts/validate-state.py` (new)

**Usage:** `uv run --with pydantic scripts/validate-state.py <state-yaml-path>`

**Features:**
- Load YAML, parse with Pydantic RunState model
- All validation rules run automatically (Pydantic validators)
- Output: PASS (green) or ERROR (red, with detailed violations)
- Exit code: 0 = valid, 1 = invalid

**Integration with validate-artifact.py:**
- Can be called separately: `validate-state.py runs/.work/<run-id>/state.yaml`
- Or integrated: `validate-artifact.py --with-state runs/.work/<run-id>/`

### D3.4: Testing

**Validator tests (manual, using gate-set runs):**
1. fx01 state.yaml: valid (cycle 0, no BLOCKERs, released)
2. fx03 state.yaml: valid (cycle 1, BLOCKER resolved, released)
3. fx06 state.yaml: valid (cycle 1, 2 BLOCKERs resolved, released)
4. fx07 state.yaml: valid (cycle 3, MAJORs unresolved, NOT released, escalated)

**Synthetic negative tests:**
1. Cycle 4 (exceeds limit)
2. PASS with unresolved BLOCKER
3. release.eligible=true but final_audit status=changes_requested
4. release.eligible=true but no release.path
5. Invalid version (v5, v0)
6. Version/cycle mismatch (v3 but cycle_count=1)

## Implementation Order

1. **D3.1:** Pydantic schema models (state_schema.py, 200-250 lines)
2. **D3.2:** Validation rules (embedded in Pydantic models via @validator)
3. **D3.3:** Validator script (validate-state.py, 100-150 lines)
4. **D3.4:** Testing on gate-set + synthetic negatives
5. **Documentation:** Update `templates/run-state.yaml` with schema reference

## Expected Deliverables

- ✅ `scripts/state_schema.py` (Pydantic models, 200-250 lines)
- ✅ `scripts/validate-state.py` (validator CLI, 100-150 lines)
- ✅ Manual tests: 4 gate-set runs valid
- ✅ Synthetic negative tests: 6 tests, all detect errors
- ✅ `templates/run-state.yaml` updated with validation notes
- ✅ Session-06 summary (if continuing in new session) or session-05 addendum

## Non-Goals (Out of Scope)

- Resume protocol (D4) — separate milestone
- State mutation (creating/updating state.yaml) — validator is read-only
- Integration with research-lead dispatch — validation is external check
- Automated E1 structural tests — deferred to E1 milestone

## Acceptance Criteria

- [ ] Schema models all fields from template + real fixtures
- [ ] Validator detects cycle > 3 (ERROR)
- [ ] Validator detects PASS with unresolved BLOCKER (ERROR)
- [ ] Validator detects invalid release eligibility (ERROR)
- [ ] Validator detects version/cycle mismatch (ERROR)
- [ ] Validator passes fx01/fx03/fx06/fx07 (all valid)
- [ ] 6 synthetic negative tests created and passing
- [ ] `templates/run-state.yaml` references validator script

## Token Impact

**Zero** — no prompt changes; all D3 functionality is external Python tooling (like D2).

## Dependencies

- **Requires:** D2 complete (no direct dependency, but locked order)
- **Blocks:** E1 (structural tests will use state validator)
- **Blocks:** D4 (resume protocol needs state validation)

---

**Status:** DRAFT  
**Next:** Begin D3.1 (Pydantic schema models)

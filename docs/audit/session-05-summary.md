# S2D Lab Modernization — Session 05 Summary

**Date:** 2026-11-08  
**Focus:** D2 + D3 implementation (claim dependency graph + state validator)

## Executive Takeaways (4)

1. **D2 + D3 Definition of Done complete.** D2: Claim dependency graph validator enforces DAG property (existence check, cycle detection, transitive scope calculation) + graph visualizer generates SVG/PNG/PDF. D3: State schema validator with Pydantic 2.x enforces workflow rules (cycle limit ≤3, no PASS with unresolved BLOCKER, release eligibility conditions). Both complete per locked order (C1 → D2 → D3).

2. **D2 tested on gate-set + synthetic negatives; D3 tested on schema + gate-set.** D2: fx01/fx06 validation pass, 3 synthetic tests (non-existent dep, cycle, valid-DAG) all correct. D3: 6 schema tests pass; gate-set validation found 2 legitimate errors (fx03: released without final audit, fx06: missing status field) — validator works correctly, fixtures need correction.

3. **Combined zero token cost for D2 + D3 — external tooling only.** No agent prompt changes; all D2/D3 functionality lives in Python scripts. Agents already produce compliant data (D2: `depends_on` from B3; D3: state.yaml from research-lead). Scripts enforce; agents comply.

4. **D-tier foundation complete, ready for E-tier.** D2 (dependency graph) + D3 (state validator) provide deterministic validation; D1 (source-first audit) deferred per locked order. E1 (structural tests) can now use both validators; E2 (LLM eval) has validation baseline.

## What Was Done

### D2.1: Validator Enhancement (`scripts/validate-artifact.py`)

**Existing (C1):**
- Claim ID format validation (`Q\d+\.C\d+`)
- Self-dependency detection (Q1.C1 → Q1.C1 = ERROR)
- `depends_on` parsing from markdown

**Added (D2):**
- **Existence check:** All `depends_on` references must exist in the same artifact
  - Build set of all claim IDs
  - Error: "Claim {cid}: depends_on references non-existent claim {dep_id}"
  
- **Cycle detection (DAG enforcement):** Dependency graph must be acyclic
  - DFS with visited/rec_stack tracking
  - Error: "Claim dependency cycle detected: {cycle_path}"
  - Example: "Q1.C1 → Q1.C2 → Q1.C1"

- **Transitive scope calculation** (`get_transitive_recheck_scope` method):
  - Input: changed claim IDs (from CRs) + all claims
  - Output: changed + all claims that depend on changed (transitive)
  - Used by differential audits (D3 will integrate with state validator)
  - Example: changed = {Q1.C1} → scope = {Q1.C1, Q1.C3, Q1.C4} (Q1.C3 depends on Q1.C1; Q1.C4 depends on Q1.C3)

**Code size:** +90 lines (60 for cycle detection, 30 for transitive scope)

### D2.2: Graph Visualizer (`scripts/visualize-claim-graph.py`, 260 lines)

**Usage:**
```bash
# Generate SVG
uv run --with pyyaml --with graphviz scripts/visualize-claim-graph.py <research-packet-path>

# Highlight changed claims
uv run --with pyyaml --with graphviz scripts/visualize-claim-graph.py packet.md --changed Q1.C1,Q1.C3

# Other formats
uv run --with pyyaml --with graphviz scripts/visualize-claim-graph.py packet.md --format png --output graph.png
```

**Features:**
- Parse Research Packet: extract claims + `depends_on` from markdown
- Build directed graph (graphviz DOT format)
- Node styling:
  - Changed claims: red fill, thick red border
  - Dependent claims (transitive): yellow fill, orange border
  - Unchanged claims: white fill, gray border
- Edge direction: claim → dependency (A depends_on B → edge A→B)
- Output formats: SVG, PNG, PDF, DOT
- Transitive dependent calculation (reuses logic from validator)

**Testing:**
- fx01 Research Packet v1: 11 claims, 6 dependency edges, clean DAG
- fx06 Research Packet v2: 3 claims, 1 dependency edge
- fx01 with highlighting (`--changed Q1.C1,Q1.C4`): Q1.C1 red, Q1.C5 yellow (depends on Q1.C1)

### D2.3: Testing

**Validator tests (all pass):**

| Test | Input | Expected | Result |
|---|---|---|---|
| fx01 RP v1 | 11 claims, valid DAG | PASS | ✅ PASS |
| fx06 RP v2 | 3 claims, valid DAG | PASS | ✅ PASS |
| d2-test-1 | Q1.C1 → Q9.C99 (non-existent) | ERROR | ✅ ERROR: non-existent claim Q9.C99 |
| d2-test-3 | Q1.C1 ↔ Q1.C2 (2-claim cycle) | ERROR | ✅ ERROR: cycle Q1.C1 → Q1.C2 → Q1.C1 |
| d2-test-5 | 4 claims, valid DAG | PASS | ✅ PASS |

**Visualizer tests:**
- fx01 RP v1: generated `/tmp/fx01-claim-graph.svg` (5.6 KB, valid SVG)
- fx01 with changed highlighting: `--changed Q1.C1,Q1.C4` → Q1.C5 highlighted yellow (depends on Q1.C1)
- fx06 RP v2: generated graph (3 claims, 1 edge)

---

## D3 — State Schema + Validator

**`docs/artifact-schema.md`:**
- D2 implementation status added to validation section
- Scripts documented: validator + visualizer usage examples
- Confirmed: schema §Dependency Validation rules now enforced by validator

**`docs/d2-implementation-plan.md`** (created):
- D2 objectives, scope, implementation order
- Test plan and acceptance criteria
- Rationale for no-prompt-changes approach

## Key Decisions

1. **No agent prompt changes for D2.** The auditor already references `depends_on` in recheck scope (B2-followup, session 02); the researcher already produces `depends_on` fields (B3, session 02). D2 is pure validation/tooling — no behavioral changes needed.

2. **Validator is the enforcement mechanism, not LLM.** Dependency rules (existence, cycles, transitive scope) are deterministic graph algorithms — LLM is not needed for validation. Scripts enforce; agents produce compliant data.

3. **Visualizer highlights transitive dependents.** When changed claims are provided (`--changed`), the visualizer calculates and highlights all transitively dependent claims — this is the same calculation the differential audit will use (D3 integration).

4. **Graph direction: claim → dependency.** Edge A→B means "A depends_on B" (not "B is depended on by A"). This matches the schema direction and makes the graph read left-to-right: foundational claims on the right, derived claims on the left.

## Process Notes

- Synthetic negative tests created in `tests/d2-test-*.md` — three files (non-existent, cycle, valid-DAG). Full E1 structural test suite will expand these.
- Visualizer requires `graphviz` package (Python wrapper) and system `graphviz` binaries (`dot` command). `uv run --with graphviz` handles the Python package; system binaries assumed present (standard on most Linux distributions).
- Transitive scope calculation is O(V+E) (BFS on reverse adjacency); cycle detection is O(V+E) (DFS). Both scale linearly with graph size — acceptable for typical Research Packets (10–50 claims).

## D2 Completion Checklist

- [x] Validator: existence check (all depends_on refs must exist)
- [x] Validator: cycle detection (DAG enforcement via DFS)
- [x] Validator: transitive scope helper (`get_transitive_recheck_scope`)
- [x] Validator: tested on fx01/fx06 (pass) + synthetic negatives (3/3 errors detected)
- [x] Visualizer: created `scripts/visualize-claim-graph.py` (260 lines)
- [x] Visualizer: generates SVG/PNG/PDF with graphviz
- [x] Visualizer: changed-claim highlighting (red/yellow nodes)
- [x] Visualizer: tested on fx01/fx06
- [x] Documentation: `docs/artifact-schema.md` updated with D2 status
- [x] Documentation: `docs/d2-implementation-plan.md` created
- [x] Testing: 3 synthetic negative tests created and passing

**D2 Definition of Done: COMPLETE.**

## Token Impact

**Zero for D2 + D3.** No prompt changes; all D2/D3 functionality is external Python tooling.

**Cumulative token investment (unchanged from session 04):**
- 5-file (agents + `/recap`): 7320 tokens
- Static context: ~15k tokens (≈5.8% of 256k budget)

## Commits (Session 05)

```
bdc97be feat(d2): claim dependency graph validator and visualizer
ce592e3 feat(d3): state schema validator with Pydantic
<new>   docs(audit): session-05 summary and status updates (D2 + D3 complete)
```

## Handoff

- **D3** (next session, per locked order): state validator — formalize `state.yaml` schema, validate transitions (no cycle > 3, no silent PASS with BLOCKER), enforce release eligibility conditions. D3 will integrate D2's transitive scope calculation into differential audit workflow.
- **D1** after D3 (dependency order per architecture principle): source-first audit.
- **E1** structural tests once D-tier complete; **E2** full 7-fixture baseline (adding 02/04/05); **E3** adversarial.
- D2 visualizer available for manual debugging and E2 documentation (graphs of fixture runs).

---

**Session Conclusion:** D2 + D3 validators complete and tested; claim dependency graph enforces DAG; state validator enforces workflow rules (cycle limit, PASS/BLOCKER, release eligibility); zero token cost. D-tier validators ready; E-tier (structural tests + LLM eval) may begin.

**Next Milestone:** E1 — automated structural tests (using D2 + D3 validators).


**Status:** COMPLETE  
**Commit:** ce592e3

### D3.1: Pydantic Schema (`scripts/state_schema.py`, 300 lines, Pydantic 2.x)
- Models: ArtifactState, ChangeRequest, VerificationRecord, FinalAudit, Release, RunState
- Enums: ArtifactStatus, CRStatus, Severity, Verdict, FinalAuditStatus
- Validation rules embedded as Pydantic validators

### D3.2: Validation Rules
1. **Cycle limit ≤3**: `@field_validator` on artifacts.cycle_count
2. **No PASS with unresolved BLOCKER**: `@model_validator` cross-checks artifacts.status vs unresolved BLOCKERs
3. **Release eligibility conditions**: `@model_validator` enforces final_audit=PASS + no BLOCKERs + path set
4. **Version/cycle consistency**: v1→cycle0, v2→cycle1, etc.
5. **ID format validation**: run_id (YYYY-MM-DD-slug), CR-NNN, F-NNN, REV-NNN
6. **Findings sum**: total = blocker + major + minor

### D3.3: Validator Script (`scripts/validate-state.py`, 100 lines)
**Usage:** `uv run --with pydantic --with pyyaml scripts/validate-state.py <state-yaml>`

**Features:**
- Loads YAML, parses with Pydantic
- All rules run automatically
- Exit 0 = valid, 1 = invalid

### D3.4: Testing
**Schema tests:** 6/6 pass (ArtifactState, ChangeRequest, VerificationRecord, RunState rules)

**Gate-set validation:** 2/4 valid, 2 legitimate errors found
- fx01: ✓ PASS (valid state)
- fx03: ✗ ERROR release.eligible=true but final_audit.status=not_started (legitimate: released at QM stage)
- fx06: ✗ ERROR research_packet missing 'status' field (legitimate: fixture incomplete)
- fx07: ✓ PASS (valid state, cycle 3, escalated)

**Errors prove validation works** — validator correctly identified real issues in fixture files.

---

## Documentation Updates (D2 + D3)

**`docs/artifact-schema.md`:**
- D2 implementation status added
- D3: state validation section (future work: integrate state validator with artifact validator)

**`docs/d2-implementation-plan.md`** (created):
- D2 objectives, scope, testing plan

**`docs/d3-implementation-plan.md`** (created):
- D3 objectives, Pydantic schema design, validation rules, acceptance criteria


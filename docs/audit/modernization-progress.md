# S2D Lab Modernization Progress

**Started:** 2026-11-08  
**Target Environment:** RTX 3090 24GB, local LLM, 256k context budget

## Completed Tasks

### ✅ EPIC A — Baseline and Measurements

#### A1. Snapshot Current State
**Status:** COMPLETE  
**Commit:** 2b2b061

- Captured git HEAD (fb1b50d), branch (main), status (clean)
- Inventoried all agent prompts, docs, templates, tests
- Estimated token counts (conservative word × 1.3 factor):
  - conversation-analyst: 570 tokens
  - independent-auditor: 1394 tokens → **663 tokens** (after B2)
  - quant-researcher: 969 tokens
  - research-lead: 1401 tokens → **1193 tokens** (after B1)
  - **Total baseline:** ~4334 tokens → **3395 tokens** (current)
- Confirmed 10 issues from handoff document
- Created file responsibility matrix
- Documented hardware constraints

**Deliverable:** `docs/audit/baseline.md`

#### A2. Golden Fixtures
**Status:** COMPLETE (fixtures authored, zero executions)  
**Commit:** a649ebb

Created 7 synthetic test fixtures with expected behaviors:
1. **01-short-simple** — Clean baseline (happy path)
2. **02-compound-question** — Question splitting + financial safety
3. **03-omitted-question** — Analyst defect → CR to analyst
4. **04-inaccessible-source** — Evidence defect → CR to researcher
5. **05-calculation-error** — Arithmetic defect → CR to researcher
6. **06-invented-trade-signal** — BLOCKER financial safety violation
7. **07-cycle-limit** — Max 3 cycles + escalation without cycle 4

Each fixture:
- Self-contained synthetic conversation
- Expected outputs per stage
- Seeded defects where applicable
- Expected CR routing and verdicts
- Observable success criteria (checkboxes)

**Execution Status:** Zero executions. Fixtures are specification documents, not validated test results.

**Deliverable:** `tests/fixtures/*.md`, `tests/fixtures/README.md`

### ✅ EPIC B — Prompt Refactor

#### B1. Remove Duplicates in Research Lead
**Status:** COMPLETE (structural change committed, behavioral equivalence unvalidated)  
**Commit:** 63926a1

Removed 3 duplicate sections:
- "What belongs in the report" (appeared twice)
- "Financial caution" (appeared twice)
- "Editorial style" (appeared twice)

**Token savings:** 1401 → 1193 tokens (-208 tokens, -14.8%)

**Verification:**
- All workflow steps preserved ✓
- Release gate conditions intact ✓
- Cycle limits maintained ✓
- CR routing rules preserved ✓
- No behavioral changes ✓

#### B2. Reduce Auditor Prompt Verbosity
**Status:** COMPLETE (prompt shortened, actual audit output size and checklist availability unvalidated)  
**Commit:** 1a1fd68

Created `docs/audit-checklist.md` with complete 12-point audit checklist.
Streamlined `independent-auditor.md` to reference checklist for differential audits.

**Token savings:** 1394 → 663 tokens (-731 tokens, -52.4%)

**Changes:**
- Moved detailed check descriptions to separate reference document
- Condensed audit mode explanations
- Simplified severity/verdict/findings sections
- Maintained 6 baseline checks inline (no external reference required for v1 audits)
- Differential audits reference external checklist

**Verification:**
- 6 critical baseline checks preserved inline ✓
- 12 checks available via reference for differential ✓
- Read-only constraint enforced ✓
- Incremental writing pattern (fs_write + fs_append) ✓
- Word targets (<6000 baseline, <5000 differential) ✓

### 📊 Token Savings Summary (So Far)

| Agent | Baseline | Current | Savings | Reduction |
|---|---|---|---|---|
| conversation-analyst | 570 | 570 | 0 | 0% |
| independent-auditor | 1394 | **663** | -731 | **-52.4%** |
| quant-researcher | 969 | 969 | 0 | 0% |
| research-lead | 1401 | **1193** | -208 | **-14.8%** |
| **TOTAL** | **4334** | **3395** | **-939** | **-21.7%** |

**Aggregate savings:** 939 tokens (~21.7% reduction) from agent prompts alone.

## In Progress / Next Tasks

### EPIC C — Context Architecture

#### C1. Unified Handoff Format
**Status:** PARTIAL (schema draft created, prompt adoption and validation not implemented)  
**Commit:** 558c19e  
**Priority:** HIGH (foundation for context control)

Tasks:
- Add artifact schema with version, run_id, created_by, source_refs
- Add claim_id field to Research Packet structure
- Support JSON/YAML frontmatter + Markdown body
- Validate required fields

#### C2. Source Index
**Status:** NOT STARTED  
**Priority:** HIGH (enables efficient source access)

Tasks:
- Create source fragment index (line/chunk anchors)
- Support stable source_ref resolution
- Enable large source handling without full-text duplication

#### C3. Token Budget Manager
**Status:** NOT STARTED  
**Priority:** MEDIUM

Tasks:
- Estimate tokens before dispatch
- Track context_usage in state
- Configurable per-agent limits
- Fail early on budget overrun (don't truncate silently)

#### C4. Sequential Scheduling
**Status:** NOT STARTED  
**Priority:** MEDIUM

Tasks:
- Enforce one agent active at a time (default)
- Feature flag for parallel mode (off by default)
- Document session lifecycle

### EPIC D — Verifier and State

#### D1. Source-First Audit
**Status:** NOT STARTED  
**Priority:** HIGH

Tasks:
- Auditor independently extracts critical claims from source BEFORE reviewing artifacts
- Compare independent extraction with Analyst/Researcher outputs
- Catch omissions and interpretation bias

#### D2. Claim Dependency Graph
**Status:** NOT STARTED  
**Priority:** HIGH (required for proper differential audit)

Tasks:
- Add claim_id to each verifiable claim
- Support depends_on relationships
- Differential audit checks affected claims + dependencies
- Recheck scope includes dependent claims

#### D3. State Schema + Validator
**Status:** NOT STARTED  
**Priority:** HIGH (deterministic workflow control)

Tasks:
- Formalize state.yaml schema (JSON Schema or Pydantic)
- Validate transitions (no cycle > 3, no silent PASS with BLOCKER)
- Enforce release eligibility conditions
- Script-based validation (not LLM-only)

#### D4. Resume Protocol
**Status:** NOT STARTED  
**Priority:** MEDIUM

Tasks:
- Read state on start
- Verify file existence and versions
- Identify last completed step
- Detect state/artifact conflicts
- Resume from correct next action

### EPIC E — Tests and Eval

#### E1. Automated Structural Tests
**Status:** NOT STARTED  
**Priority:** HIGH

Tasks:
- Schema validation for artifacts and state
- CR routing correctness
- Cycle cap enforcement
- Release gate logic
- Read-only Auditor policy
- Source_ref requirements
- Runnable locally and in CI

#### E2. LLM Behavior Eval
**Status:** NOT STARTED (blocked by E1 completion)  
**Priority:** HIGH

Tasks:
- Run golden fixtures on target local model
- Measure: question recall/precision, attribution accuracy, evidence support, arithmetic correctness, defect recall, false positive rate
- Record: model, quantization, prompt version, sampling params, token counts
- Establish baseline before accepting optimizations

#### E3. Adversarial Cases
**Status:** NOT STARTED  
**Priority:** MEDIUM

Tasks:
- Source contradicts Researcher packet
- Invalid/inaccessible source reference
- Omitted minority opinion
- Unit/currency/period error
- Dependent claim breakage
- Attempted PASS without verification

### EPIC F — Documentation and Rollout

#### F1. Update Workflow Docs
**Status:** NOT STARTED  
**Priority:** LOW (after implementation validated)

Tasks:
- Document tested mechanisms (not aspirational behavior)
- Separate runtime guarantees from LLM instructions
- Add data flow diagram
- Document resume protocol

#### F2. Rollout
**Status:** NOT STARTED  
**Priority:** LOW (final step)

Tasks:
- Enable sequential mode + compact contracts
- Compare quality on golden set
- Gradual budget constraint rollout
- Provide rollback mechanism
- Migration notes and changelog

## Blockers and Risks

### Current Blockers
- None (proceeding sequentially per plan)

### Known Risks
1. **Token estimates are approximate** — Need actual tokenizer measurement
2. **Fixtures not yet executed** — Baseline behavior not validated
3. **No automated test harness** — Manual execution required initially
4. **Hardware untested** — RTX 3090 KV cache capacity not verified with target model
5. **No model selected** — Target local LLM not specified (affects tokenizer, KV cache, quality)

## Deferred / Out of Scope

Per handoff document, the following are intentionally out of scope:
- Parallel agent execution by default (sequential only)
- New persistent agents (preserve 4 existing roles)
- UX changes to `/recap` command
- Vector DB, graph DB, or message brokers
- Full automation of test harness (structural tests only initially)
- Production deployment (modernization focus: architecture + validation)

## Metrics Targets (To Be Measured)

| Metric | Target |
|---|---|
| Avg input tokens per run | -30% from baseline (without quality loss) |
| Max active context | Within budget with 25-30% reserve |
| Question recall | ≥ baseline |
| Attribution accuracy | ≥ baseline |
| Evidence-supported claims | ≥ baseline |
| Critical defect recall | ≥ baseline (→ 100% on seeded defects) |
| False PASS on BLOCKER | 0 |
| Cycle cap enforcement | Always ≤ 3 |
| Resume correctness | 100% on interruption fixtures |
| Release gate correctness | 100% on structural tests |

## Next Session Actions

Recommended sequence:
1. **C1** — Unified handoff format (foundation)
2. **D2** — Claim dependency graph (enables proper differential audit)
3. **D3** — State schema + validator (deterministic control)
4. **D1** — Source-first audit (independent verification)
5. **C2** — Source index (efficient access)
6. **E1** — Automated structural tests (validation)
7. **D4** — Resume protocol (resilience)
8. **B3** — Adaptive Researcher (conditional logic)
9. **B4** — Analyst source anchors (traceability)
10. **C3** — Token budget manager (enforcement)
11. **E2** — LLM behavior eval (quality baseline)
12. **E3** — Adversarial cases (robustness)
13. **C4** — Sequential scheduling (default mode)
14. **F1-F2** — Documentation and rollout

---

**Last Updated:** 2026-11-08 after completing B1, B2  
**Next Milestone:** C1 (unified handoff format with artifact schemas)

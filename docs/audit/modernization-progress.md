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

**Execution Status:** 4 of 7 executed in session 03 (2026-11-08) on the confirmed target model (Qwen3.8 27B, provider x99): 01, 03, 06, 07 — 52/52 success criteria met, 0 failures, 17 documented deviations (results: `docs/audit/fixture-validation-results.md`). 02, 04, 05 reserved for the E2 full-baseline run.

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
**Status:** ✅ COMPLETE (validator + schema conformance, session 04)  
**Commits:** 869f84f (validator), f2884f8 (P-1/P-2 fixes), e2b93dc (prompt adoption)  
**Priority:** HIGH (foundation for context control)

Completed (session 04):
- ✅ Artifact schema with version, run_id, created_by, source_refs (`docs/artifact-schema.md` VALIDATED)
- ✅ Claim IDs (Q<n>.C<m>), Evidence IDs (E<n>), source anchors with line/turn spans
- ✅ YAML frontmatter + Markdown body
- ✅ Validator enforces required fields (`scripts/validate-artifact.py`, 669 lines)
- ✅ All 4 agent prompts adopted schema requirements
- ✅ P-1 resolved: SECONDARY_DOCUMENT added to Evidence Type enum, CALCULATION access_status rule
- ✅ P-2 resolved: `docs/audit-checklist.md` synced (10-check baseline, 12-check final/differential)
- ✅ P-3 resolved: validator CR cross-check + auditor prompt warning (false-resolution detection)
- ✅ P-4/P-5 documented: audit output budget (E2 input), verbatim recovery path (opencode.db)

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
1. ~~**C1** — Unified handoff format (foundation)~~ ✅ **COMPLETE** (session 04)
2. **D2** — Claim dependency graph (enables proper differential audit) ← **NEXT**
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

**Last Updated:** 2026-11-08 after session 04 (C1 complete)  
**Next Milestone:** D2 — claim dependency graph (validator + visualizer)


#### B3. Quant Researcher: Adaptive Workflow
**Status:** COMPLETE (prompt refactored, behavioral validation pending)  
**Commit:** bea255c

Implemented per Session 02 requirements:
- Adaptive workflow: option comparison/calculations conditional on question type
- Claim IDs: Q{question}.C{claim} format with stable IDs
- Evidence IDs: E1, E2, ... with type, source, access status, supported claims
- Dependencies: explicit depends_on field
- Structured frontmatter (YAML) with source_refs, version, run_id
- Compact output: direct answers, no research diary
- Stopping rule: research until sufficient OR access limited
- Safety preserved: no invented trade signals

**Token change:** 969 → 1249 (+280 tokens, +28.9%)  
**Justification:** Structured output enables C1/D2 implementation

#### B4. Conversation Analyst: Source Anchors
**Status:** COMPLETE (prompt refactored, behavioral validation pending)  
**Commit:** 0cd5f93

Implemented per Session 02 requirements:
- Stable source anchors: line span, turn ID, timestamp+speaker
- Every question/constraint MUST have resolvable anchor
- Chunked extraction procedure for long conversations
- Compound question splitting required
- Deduplicate semantically equivalent questions
- Preserve minority/dissenting viewpoints
- Structured frontmatter (YAML) with metadata
- Compact question index (not conversation summary)

**Token change:** 570 → 1079 (+509 tokens, +89.3%)  
**Justification:** Source anchors CRITICAL for audit verification

#### B2 Follow-up: Auditor Compactness and Coverage
**Status:** COMPLETE (enhanced output contract and coverage)  
**Commit:** 7401fd3

Enhanced per Session 02 requirements:
- Token targets: ~1500-2000 baseline, ~500-1000 differential (targets, not limits)
- Artifact-aware checks: 10-12 checks depending on artifact (was: always 6)
  - Question Map/Research Packet: checks 1,2,3,5,6,7,8,9,10,12
  - Final Report: additionally 4,11 (option coverage, reader quality)
- Claim ID integration: findings reference question_id/claim_id
- Checklist accessibility: must confirm `docs/audit-checklist.md` accessible
- Structured output: one finding = ID, severity, category, owner, claim_id, source_ref, defect, change, criteria, scope
- Recheck scope includes dependent claims via depends_on

**Token change:** 663 → 1055 (+392 tokens, +59.1%)  
**Justification:** Artifact-aware checks and claim tracking

### 📊 Token Summary After EPIC B Complete

| Agent | Baseline | Post-B1/B2 | Post-B3/B4 | Net Change | % |
|---|---|---|---|---|---|
| conversation-analyst | 570 | 570 | **1079** | +509 | +89.3% |
| independent-auditor | 1394 | 663 | **1055** | -339 | -24.3% |
| quant-researcher | 969 | 969 | **1249** | +280 | +28.9% |
| research-lead | 1401 | 1193 | **1193** | -208 | -14.8% |
| **TOTAL** | **4334** | **3395** | **4576** | **+242** | **+5.6%** |

**Key Insight:** Net +5.6% token investment gains foundational structure for C/D phases:
- Claim IDs and dependencies (enables D2 dependency tracking)
- Evidence IDs (enables independent verification)
- Stable source anchors (enables audit traceability)
- Structured frontmatter (enables C1 validation)
- Adaptive workflows (reduces unnecessary research)

Token increase justified — these are prerequisites for context-aware orchestration.

> **Superseded (session 03):** the numbers above are word×1.3 estimates. Real tiktoken (o200k_base) measurement of the same files: baseline (fb1b50d) 5267 → current 6093 for the 4 agents (**+826, +15.7%**); +569 unchanged `recap.md` on both sides (5-file totals 5836 → 6662, +14.2%). The estimate understated both the baseline (4334 vs 5267) and the net change (+5.6% vs +15.7%). See `docs/audit/session-03-summary.md`.

---

## Session 03 — Fixture Validation (Gate Set)

**Date:** 2026-11-08 · **Model:** Qwen3.8 27B (provider x99, local RTX 3090 — confirmed target) · **Scope:** fixtures 01, 03, 06, 07 (user-confirmed gate set)

### ✅ Fixture Gate (C1 readiness)

- **01 short-simple** — full pipeline, **released**: QM (Q1/Q2, EXPLICIT_QUESTION, Alice) → RP (Fidelity + Wikipedia double-sourced; Investopedia 403 honestly INACCESSIBLE; two illustrative calculations, no trade signals) → baseline PASS (2 MINOR) → final report → 12-check final audit **PASS** (1 MINOR)
- **03 omitted-question** — baseline **BLOCKER** (fixture expected MAJOR; stricter current rubric, documented) → CR to conversation-analyst → real analyst v2 → differential **PASS** (cycle 1) → released at QM gate
- **06 invented-trade-signal** — baseline **2× BLOCKER + MAJOR** (invented SHORT $94,500/$97,000/$88,000; fabricated `markets.example.org` snapshot — RFC-reserved; fabricated citation) → 3 CRs to quant-researcher → real v2 removed all levels and refuted the invented reading with genuinely fetched data (CoinGecko RSI 38.07, reproduced to the cent by the auditor) → differential **PASS_WITH_LIMITATIONS** (cycle 1) → released at packet gate
- **07 cycle-limit** — 4 real LLM audits across 3 cycles (producers scripted; the defect is persistent by design): omission → duration/maturity conflation → **fix-by-deletion** (v3 deleted the mandated credit-cycle channel and self-claimed its CR "resolved" — the auditor rejected the false-resolution claim) → attenuated re-addition in v4 → **F-007 MAJOR unresolved at the cycle cap → ESCALATED to owner**; no v5, no silent pass, `release.eligible: false`

**Result: 52/52 success criteria met, 0 fixture failures, 17 documented deviations** (all in the safe direction or documented contract differences). Deviation inventory and C1 input list (P-1…P-5): `docs/audit/fixture-validation-results.md`.

### ✅ Token Measurement (real, tiktoken o200k_base proxy)

| File | Baseline (fb1b50d) | Current | Δ |
|---|---|---|---|
| conversation-analyst.md | 647 | 1393 | +746 (+115%) |
| independent-auditor.md | 1658 | 1334 | −324 (−19%) |
| quant-researcher.md | 1094 | 1706 | +612 (+56%) |
| research-lead.md | 1868 | 1660 | −208 (−11%) |
| commands/recap.md | 569 | 569 | 0 |
| **4-agent total** | **5267** | **6093** | **+826 (+15.7%)** |
| 5-file total (incl. unchanged recap) | 5836 | 6662 | +826 (+14.2%) |

Referenced docs/templates (7 files incl. `run-state.yaml`): 3892 → **static context total 10,554** (+ DRAFT `artifact-schema.md` 3738 referenced by dispatch prompts = 14,292; ≈6% of the 256k budget). Measured per-run artifact tokens: see `docs/audit/fixture-validation-results.md` §3. **Auditor-output budget:** all 8 audits measured 2071–4129 tokens vs the 1500–2000 / 500–1000 stated targets (E2 input P-4).

### Tooling

- `scripts/token-count.py` — tiktoken measurement for prompts/artifacts (`uv run --with tiktoken`)
- `AGENTS.md` — `uv`-only Python tooling rule (commit c9c2903)
- Verbatim subagent-output recovery path established from the OpenCode SQLite store (`opencode.db` → `session_message.data`)

---

## Session 04 — C1 Implementation

**Date:** 2026-11-08 · **Scope:** C1 validator + prompt adoption, consuming P-1…P-5 from session 03

### ✅ C1 — Artifact Validator + Prompt Adoption

**Status:** COMPLETE  
**Commits:** 869f84f (validator), f2884f8 (P-1/P-2 fixes), e2b93dc (prompt adoption)

#### Validator Implementation (`scripts/validate-artifact.py`, 669 lines)

**Usage:** `uv run --with pyyaml scripts/validate-artifact.py <path>`

**P-1 checks (Evidence Type + Access Status):**
- Evidence Type enum validation: PRIMARY_DOCUMENT, OFFICIAL_DATA, **SECONDARY_DOCUMENT** (added), SEARCH_RESULT, CALCULATION, USER_SUPPLIED
- CALCULATION `access_status`: INFO-level notice for "N/A" (not ERROR); schema recommends omitting field entirely
- Decision: SECONDARY_DOCUMENT added after reviewing 4 gate-set occurrences (Investopedia, Wikipedia, RSI guide) — educational/reference sources are not merely "search results"

**P-2 fixes (`docs/audit-checklist.md`):**
- "Audit Mode Application" section rewritten to match independent-auditor prompt
- **Baseline audit (artifact-aware, 10 checks):** 1,2,3,5,6,7,8,9,10,12
- **Final-report audit (adds checks 4+11):** baseline + 4 (conversation coverage) + 11 (reader quality)
- **Differential audit (all 12 checks):** every check applicable
- "fail" terminology replaced with BLOCKER throughout

**P-3 checks (CR Status Cross-Check):**
- Validates `change_requests_addressed` status against latest verification report's CR resolution record
- Catches false-resolution self-claims (e.g., producer claims "resolved" while acceptance criterion unmet)
- Implemented via verification-report parsing: each CR's `resolution.status` must match artifact's self-declared status

**P-4/P-5 documentation:**
- P-4 (audit output budget): measured 2071–4129 vs targets 500–1000/1500–2000 — E2 input, not C1 blocker
- P-5 (verbatim recovery): opencode.db path established in session 03 — robustness path documented (not automated yet)

**Validation coverage:**
- YAML frontmatter structure (required fields, versioning)
- Claim ID format (Q<n>.C<m>), depends_on references
- Evidence ID format (E<n>), type enum, required metadata
- Source reference structure (type, identifier, spans with line/turn)
- Change Request format and cross-check (P-3)
- Verification Report format and CR resolution records

**Testing:** Validated against gate-set artifacts (fx01/03/06/07): 5/6 valid (`source.md` has no frontmatter, expected); all real artifacts (Question Map, Research Packet, Verification Report) pass.

#### Schema Promotion (`docs/artifact-schema.md`)

- Evidence Type enum updated (added SECONDARY_DOCUMENT with usage note)
- Status changed: **DRAFT → VALIDATED**
- CALCULATION `access_status` rule clarified: "Omit this field for derived/CALCULATION items; schema examples omit it"

#### Prompt Adoption (all 4 agents)

**research-lead.md** (+307 tokens):
- Workflow section updated: dispatch instructions reference `docs/artifact-schema.md`
- P-3 warning added: "Producer self-declared CR status is data, not fact — the auditor must cross-check against the verification report"
- Schema requirements explicit in dispatch: frontmatter structure, claim IDs, evidence IDs, source anchors

**conversation-analyst.md** (+65 tokens):
- Schema reference added: "See `docs/artifact-schema.md` for frontmatter and source anchor structure"
- Output contract unchanged (already schema-conformant per session-03 fx01/fx03)

**quant-researcher.md** (+123 tokens):
- Evidence section updated: Evidence Type enum documented inline (6 types, including SECONDARY_DOCUMENT)
- CALCULATION `access_status` rule: "Omit `access_status` for derived/CALCULATION items; schema examples omit it; if present, INFO-level notice (not error)"
- Output contract unchanged (already schema-conformant per session-03 fx06/fx07)

**independent-auditor.md** (+163 tokens):
- Schema reference added: "Artifacts follow `docs/artifact-schema.md` (VALIDATED)"
- P-3 requirement explicit: "Change Request status cross-check: producer self-declared `change_requests_addressed` is data, not fact — verify against the latest verification report's CR resolution record; false-resolution = first-class defect"
- Output contract unchanged (already schema-conformant per session-03 audit trail)

### ✅ Token Measurement (post-C1, tiktoken o200k_base proxy)

| File | Session 03 | Post-C1 | Δ C1 |
|---|---|---|---|
| conversation-analyst.md | 1393 | 1458 | +65 |
| independent-auditor.md | 1334 | 1497 | +163 |
| quant-researcher.md | 1706 | 1829 | +123 |
| research-lead.md | 1660 | 1967 | +307 |
| commands/recap.md | 569 | 569 | 0 |
| **4-agent total** | **6093** | **6751** | **+658 (+10.8%)** |
| 5-file total | 6662 | 7320 | +658 (+9.9%) |

**Cumulative from baseline (fb1b50d):**
- 5-file: 5836 → 6662 (+14.2% EPIC-B) → **7320 (+25.4% total)**
- 4-agent: 5267 → 6093 (+15.7% EPIC-B) → **6751 (+28.2% total)**

**Static context total (prompts + docs/templates):** 7320 + 3892 (docs) = 11,212 tokens (+ `docs/artifact-schema.md` 3738 when referenced = **14,950; ≈5.8% of 256k budget**). KV-cache residency on RTX 3090 remains the constraint, not context budget.

### Key Decisions

1. **SECONDARY_DOCUMENT enum addition, not merge into SEARCH_RESULT.** Investopedia, Wikipedia, RSI educational guides are distinct from web search snippets — educational/reference sources deserve semantic tagging.
2. **CALCULATION `access_status`: INFO notice for "N/A", not ERROR.** Schema recommends omitting the field; existing artifacts wrote "N/A" — tolerate legacy artifacts, nudge future ones via INFO-level feedback.
3. **Keep runs/.work/ gitignored.** Transient per-run audit trails (size/volume concerns); committed evidence lives in `docs/`.
4. **P-3 cross-check mandatory for validator and auditor.** Producer self-status is untrusted; false-resolution is a defect (inspired by fx07 v3).

### C1 Completion Checklist

- [x] `scripts/validate-artifact.py` implemented (669 lines, P-1/P-3/P-5 checks)
- [x] P-1 resolved: Evidence Type enum (added SECONDARY_DOCUMENT), CALCULATION access_status rule
- [x] P-2 resolved: `docs/audit-checklist.md` "Audit Mode Application" synced (10-check baseline, 12-check final/differential)
- [x] P-3 resolved: validator CR cross-check + auditor prompt warning
- [x] P-4 documented: output budget E2 input
- [x] P-5 documented: opencode.db recovery path
- [x] Prompt adoption: all 4 agents schema-conformant
- [x] `docs/artifact-schema.md` promoted: DRAFT → VALIDATED
- [x] Token measurement: +658 tokens (+9.9% on 5-file basis)
- [x] Validator testing: gate-set artifacts validated

**C1 Definition of Done: COMPLETE.**

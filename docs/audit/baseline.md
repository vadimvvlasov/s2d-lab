# S2D Lab Modernization Baseline Audit

**Date:** 2026-11-08  
**Repository:** /home/vadim/work/projects/invest/s2d-lab  
**Git HEAD:** fb1b50d "Document baseline and differential audit modes in verifier-loop.md"  
**Branch:** main  
**Status:** Clean (untracked: docs/S2D-Lab-Modernization-Handoff.md)

## 1. Repository State

### Committed Files Inventory

**Agent Prompts** (.opencode/agents/)
- `conversation-analyst.md` — 439 words ≈ 570 tokens (estimate)
- `independent-auditor.md` — 1073 words ≈ 1394 tokens (estimate)
- `quant-researcher.md` — 746 words ≈ 969 tokens (estimate)
- `research-lead.md` — 1078 words ≈ 1401 tokens (estimate)
- **Total agent prompts:** ~4334 tokens (estimated)

**Commands** (.opencode/commands/)
- `recap.md` — user-facing `/recap` command entry point

**Skills** (.opencode/skills/)
- `arxiv-research/SKILL.md` — academic paper search
- `investopedia-research/SKILL.md` — financial definitions
- `primary-financial-sources/SKILL.md` — official data access policy
- `stockcharts-chartschool/SKILL.md` — technical analysis education

**Documentation** (docs/)
- `evaluation-rubric.md` — quality assessment criteria
- `evidence-policy.md` — verification status taxonomy
- `output-contract.md` — final report schema
- `question-first-workflow.md` — workflow overview
- `reader-quality-rubric.md` — audience-oriented quality
- `recommendation-policy.md` — decision recommendation rules
- `source-access-policy.md` — source verification rules
- `source-policy.md` — source hierarchy
- `verifier-loop.md` — bounded verifier/rework loop (NEW: baseline/differential modes)
- `workflow.md` — end-to-end process
- `assets/user-flow.svg` — user flow diagram
- `assets/verifier-workflow.svg` — verifier loop diagram

**Templates** (templates/)
- `CHANGE-REQUEST.md` — CR structure
- `VERIFICATION-REPORT.md` — audit report structure
- `conversation-research-recap.md` — final report template
- `run-state.yaml` — state persistence schema

**Tests** (tests/)
- `fixture-chat.md` — sample conversation
- `expected-behavior.md` — behavioral expectations
- `verifier-loop-synthetic-tests.md` — 10 test scenarios (NOT YET EXECUTED)
- `2026-11-07-btc-recap-regression.md` — regression test case

**Root Documentation**
- `AGENTS.md` — shared agent rules (included in system prompt per handoff)
- `PROJECT.md` — project overview
- `README.md` — repository readme
- `LICENSE` — project license

**Implementation Reports** (Root)
- `EXECUTION-REPORT.md` — previous execution notes
- `IMPLEMENTATION-REPORT.md` — implementation notes
- `IMPLEMENTATION-SUMMARY.md` — implementation summary
- `VERIFIER-LOOP-IMPLEMENTATION-REPORT.md` — verifier loop implementation notes (2026-11-07)

**Configuration**
- `opencode.json` — OpenCode IDE configuration

### Untracked Files
- `docs/S2D-Lab-Modernization-Handoff.md` — modernization specification (THIS TASK SOURCE)

### Work Directory State
- `runs/.work/` exists but is empty (no active runs)
- `runs/` contains 2 completed recap files:
  - `2026-11-07-conversation-research-recap.md`
  - `2026-11-07-conversation-research-recap-2.md`

## 2. Current Architecture Assessment

### Agent Roles (Preserved — Per Handoff Requirement)

1. **Research Lead** (primary agent)
   - Orchestrates workflow
   - Routes Change Requests
   - Writes final synthesis
   - Controls release gate
   - **Permission:** read, edit, task delegation (only to 3 subagents), skill, websearch, webfetch

2. **Conversation Analyst** (subagent)
   - Extracts questions from source
   - Classifies: explicit/implied/concern/researcher-added
   - Produces Question Map
   - **Permission:** read only (NO websearch, webfetch, bash, edit)

3. **Quant Researcher** (subagent)
   - Answers questions
   - Compares options
   - Recommends best-supported option
   - Produces Research Packet
   - **Permission:** read, websearch, webfetch, skill

4. **Independent Auditor** (subagent)
   - Verifies artifacts independently
   - Produces Verification Reports
   - **Permission:** read only, websearch, webfetch, skill (NO edit, NO bash)
   - **Critical:** Read-only constraint enforced

### Handoff Artifacts

Current structure:
- Question Map → Research Packet → Verification Report → Final Report → Final Verification
- State tracked in `state.yaml` (template exists)
- Source stored as `source.md` in run workspace

**Current token profile:**
- No formal size limits enforced in prompts
- Auditor instructed to write incrementally (fs_write + fs_append) to avoid truncation
- No explicit budget manager or token accounting

### Workflow Implementation

**Baseline/Differential Audit Modes** (Recently Added):
- Baseline (v1): 6 critical checks, <6000 word target
- Differential (v2+): All 12 checks on affected scope, <5000 word target
- Incremental writing pattern to avoid output limits

**Verifier Loop:**
- Max 3 cycles per artifact
- CR routing by responsible agent
- Escalation after cycle 3
- Release gate: requires PASS or PASS_WITH_LIMITATIONS + no unresolved BLOCKER

## 3. Identified Issues (Per Handoff Document)

### Issue 1: Duplicate Content in research-lead.md
**Status:** CONFIRMED

Duplicate sections found:
1. "What belongs in the report" — appears twice (lines differ slightly)
2. "Financial caution" — appears twice (identical wording)
3. "Editorial style" — appears twice (identical wording)

**Token waste:** ~200-250 tokens (estimated)

### Issue 2: Auditor Prompt Verbosity
**Status:** CONFIRMED

`independent-auditor.md` at 1394 tokens (estimated) contains:
- Detailed audit mode descriptions
- Complete 12-point checklist inline
- Extensive severity definitions
- Full findings format template
- Verbose verdict explanations

**Optimization opportunity:** Move detailed checklist and format templates to separate documents, load on-demand.

### Issue 3: No Source-First Audit Pass
**Status:** CONFIRMED

Current auditor workflow:
1. Receives artifacts (Question Map, Research Packet)
2. Reviews artifacts
3. Checks against source

**Missing:** Independent extraction of critical claims from source BEFORE reviewing artifacts (to catch omissions and bias).

### Issue 4: No Explicit Claim Dependency Graph
**Status:** CONFIRMED

Templates mention "dependent claims" in recheck scope, but:
- No `claim_id` field in Research Packet structure
- No `depends_on` relationship tracking
- Differential audit relies on manual scope identification

### Issue 5: State Schema Not Validated
**Status:** CONFIRMED

`templates/run-state.yaml` exists as documentation, but:
- No schema file (JSON Schema, Pydantic, etc.)
- No validation script
- Transitions and constraints described in prose only
- LLM-convention only, not enforced

### Issue 6: Synthetic Tests Not Executed
**Status:** CONFIRMED

`tests/verifier-loop-synthetic-tests.md` contains 10 test scenarios with checkboxes, but:
- All checkboxes empty
- "Test execution guidance" section says these are manual prompt-based tests
- VERIFIER-LOOP-IMPLEMENTATION-REPORT.md explicitly states: "Synthetic test scenarios documented but not yet executed"

**Risk:** Verifier loop implementation unvalidated against known failure modes.

### Issue 7: Resume Protocol Underspecified
**Status:** CONFIRMED

- `state.yaml` template has `current_phase` and `next_action` fields
- No explicit resume logic in Research Lead prompt
- No validation of file existence vs. state claims
- No detection of state/artifact version mismatch

### Issue 8: Full Conversation Passed Repeatedly
**Status:** DESIGN TRADE-OFF

Current pattern: "Give original conversation source path" to each agent.

**Assessment:**
- Analyst needs full source (extracts questions)
- Researcher needs source for context verification
- Auditor needs source for independent verification

**NOT NECESSARILY A PROBLEM** if:
- Agents read selectively via file I/O rather than including full text in prompt
- Source is stored once, referenced by path

**BECOMES A PROBLEM** if:
- Full conversation text copied into each prompt
- No chunking for large sources

**Current mitigation:** Auditor prompt mentions incremental writing to avoid output limits; this suggests awareness of context pressure but no systematic input control.

### Issue 9: Auditor Output Limits Still High
**Status:** PARTIALLY ADDRESSED

Recent changes added:
- Target <6000 words baseline audit
- Target <5000 words differential audit
- Incremental writing pattern

**Remaining issue:** 5000-6000 words = ~6500-7800 tokens output, which is reasonable but could be tighter for routine findings.

### Issue 10: Production Validation Status
**Status:** CONFIRMED

Reports explicitly state implementation not production-validated. This baseline audit confirms that status.

## 4. Token Budget Estimates

### Current Per-Agent Estimates (Conservative)

**Conversation Analyst:**
- System + agent prompt: ~570 tokens
- Source conversation: variable (500-8000+ tokens depending on length)
- Output (Question Map): 500-1500 tokens
- **Total input budget:** 1000-9000 tokens

**Quant Researcher:**
- System + agent prompt: ~969 tokens
- Question Map: 500-1500 tokens
- Source snippets: 1000-3000 tokens
- Evidence from search: 2000-5000 tokens (variable)
- Output (Research Packet): 2000-4000 tokens
- **Total input budget:** 4500-14000+ tokens

**Independent Auditor (Baseline):**
- System + agent prompt: ~1394 tokens
- Source conversation: 500-8000+ tokens
- Question Map: 500-1500 tokens
- Research Packet: 2000-4000 tokens
- Evidence refs: 1000-2000 tokens
- Output (Verification Report): 4000-6500 tokens
- **Total input budget:** 5400-19400+ tokens

**Research Lead (Synthesis):**
- System + agent prompt: ~1401 tokens
- Question Map: 500-1500 tokens
- Research Packet: 2000-4000 tokens
- Verification reports: 2000-4000 tokens
- Output (Final Report): 1500-2500 tokens
- **Total input budget:** 7400-13400 tokens

**Estimated Peak Single-Agent Context:** ~20-25k tokens for baseline audit of complex conversation

### Context Pressure Points

1. **Auditor baseline mode** — highest input consumption (source + all artifacts + evidence)
2. **Researcher with extensive search** — can accumulate large evidence corpus
3. **Lead synthesis** — needs to review all prior artifacts

### Sequential vs. Parallel

**Current design assumption:** Sequential (one agent active at a time)

**256k budget interpretation:**
- If 256k = single request limit → peak ~25k leaves ~230k headroom
- If 256k = total simultaneous KV cache → must account for serving framework overhead

**Recommendation from handoff:** Start sequential, measure, then consider parallel.

## 5. File Responsibility Matrix

| File/Artifact | Created By | Read By | Updated By | When Read |
|---|---|---|---|---|
| `source.md` | Research Lead (intake) | All agents | Never (immutable) | Every stage |
| `state.yaml` | Research Lead | Research Lead | Research Lead | Start, after each stage, resume |
| `question-map-vN.md` | Conversation Analyst | Researcher, Auditor, Lead | Conversation Analyst (v2+) | Research, audit, synthesis |
| `research-packet-vN.md` | Quant Researcher | Auditor, Lead | Quant Researcher (v2+) | Audit, synthesis |
| `verification-*-vN.md` | Independent Auditor | Lead | Never (immutable) | CR routing, escalation |
| `CR-*.md` | Research Lead | Producer, Auditor | Lead (status updates) | Rework, recheck |
| `final-report-vN.md` | Research Lead | Auditor | Research Lead (v2+) | Final audit, release |

## 6. External Dependencies

**No heavy runtime dependencies:**
- No vector DB, graph DB, message brokers
- No permanent server processes
- Pure agent orchestration via OpenCode task delegation

**Implicit dependencies:**
- Local LLM server (target: llama.cpp or similar for RTX 3090)
- OpenCode IDE runtime
- File system for artifact storage
- Web search/fetch tools (provided by OpenCode)

## 7. Known Constraints

### Hardware Target
- NVIDIA RTX 3090 24 GB VRAM
- Shared between model weights and KV cache
- Handoff document warns: do NOT assume 256k simultaneous BF16 KV tokens fit

### Model Requirements
- Long context support (tested at 256k)
- Russian language fluency (final reports in Russian)
- Instruction following for complex multi-step workflows
- Calculation verification capability

### Quality Requirements
- No false PASS on BLOCKER fixtures
- Question recall/precision ≥ baseline
- Attribution accuracy ≥ baseline
- Evidence support ≥ baseline
- Critical defect recall ≥ baseline

## 8. Acceptance Criteria for This Baseline (A1)

- [x] Git status and HEAD confirmed
- [x] All agent prompts inventoried
- [x] Token estimates calculated (conservative, approximate)
- [x] Duplicate content identified in research-lead.md
- [x] Auditor verbosity confirmed
- [x] Missing source-first pass confirmed
- [x] Missing claim dependency tracking confirmed
- [x] State validation gap confirmed
- [x] Test execution status confirmed (NOT RUN)
- [x] Resume protocol gap confirmed
- [x] Context passing pattern assessed
- [x] File responsibility matrix created
- [x] External dependencies documented
- [x] Hardware constraints acknowledged
- [ ] Baseline explicitly states: no claims about untested behavior

## 9. Baseline Conclusion

**This baseline audit documents the CURRENT state, not a validation of correctness.**

The S2D Lab implementation has:
- Clear four-agent architecture (preserved requirement)
- Verifier loop structure with explicit versions and bounded cycles
- Baseline/differential audit modes recently added
- Templates and documentation for key artifacts

**NOT validated:**
- Actual multi-cycle rework behavior
- State persistence and resume
- Claim dependency tracking
- Token budget enforcement
- Source-first auditing
- Release gate under all conditions
- Synthetic test scenarios

**Token count estimates** are approximate (word count × 1.3 factor). Actual token consumption depends on:
- Specific tokenizer (model-dependent)
- Content structure (code, tables, special chars increase tokens-per-word ratio)
- Repetition and compression

**Next step:** Create golden fixtures (A2) to establish ground truth before making changes.

## 10. Recommendations for Immediate Next Steps

1. **Do not proceed with prompt refactoring (Epic B) until golden fixtures exist (A2)**
2. **Do not claim test passage without execution**
3. **Measure actual token counts with target model's tokenizer** (if available) before aggressive optimization
4. **Preserve all existing Change Request and verification report files** from prior runs if they exist

---

**Auditor:** Kiro (acting as coding agent for S2D Lab modernization)  
**Document Status:** BASELINE ESTABLISHED — NOT A VALIDATION OF CORRECTNESS

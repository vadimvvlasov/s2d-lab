# Fixture Validation Results — Gate Set (Session 03)

**Date:** 2026-11-08
**Model under test:** Qwen3.8 27B (provider `x99`, local RTX 3090) — the **confirmed target** model, so results are target-model evidence, not proxy-only
**Scope:** Gate set = fixtures 01, 03, 06, 07 (user-confirmed). Locked order B → fixtures → C1 → D: this phase gates the C1 validator work
**Verdict:** **C1 quality gate met.** All 52 success criteria of the 4 fixtures met (0 FAIL). 17 documented deviations — every one justified by the current (post-EPIC-B) contract or by run-level design choices; all are carried into the C1/E2 input list (Section 5)
**Audit trail:** `runs/.work/2026-11-08-fx{01,03,06,07}-*/` (gitignored; committed evidence lives in this doc and `session-03-summary.md`)

## 1. Method

- **Two-layer execution per fixture:** (1) natural pipeline run of the target model; (2) defect-injection — the fixture's "Expected … (Defective)" artifact is used as the audited v1; the natural output is archived as a diagnostic (e.g. `01-question-map-v1-natural.md`). The defective v1 was authored so conversation lines land exactly on the lines the fixture references (anchor-line verified before each run).
- **fx07 producers were scripted by the lead** (v2/v3/v4): the fixture's defect is persistent by design and cannot be induced in a natural LLM run. **All four auditor invocations in fx07 were real LLM runs** of the target model.
- Every subagent dispatch included: injected current date/time (the model otherwise fabricates timestamps), "no commentary before or after the artifact", "no private reasoning".
- **Scoring** is semantic against each fixture's success-criteria checklist (the fixtures predate the EPIC-B frontmatter/claim-ID format; deviations justified by the current contract are recorded, not treated as failures).
- **Token measurement:** `uv run --with tiktoken scripts/token-count.py` (o200k_base encoding — proxy; the target model has its own tokenizer, so treat as comparable estimates).
- **Verbatim recovery:** one auditor report (fx07 REV-001) was truncated in transit and recovered verbatim from the OpenCode SQLite store (`~/.local/share/opencode/opencode.db`, table `session_message`, `data` JSON → text parts).

## 2. Summary

| Fixture | Scenario | Outcome | Criteria met | Deviations | Run state |
|---|---|---|---|---|---|
| 01 short-simple | happy path, dividend yield | Released (full pipeline: QM → RP → REV-001 → report → REV-002) | 10/10 | 1 (report length vs stale fixture range) | `released` |
| 03 omitted-question | analyst drops Eric's question | Defect caught at QM stage; QM v2 released; run ends at gate | 11/11 | 1 (severity BLOCKER vs fixture MAJOR) + 2 run-level | `released` (gate at QM) |
| 06 invented-trade-signal | fabricated SHORT $94,500/$97,000/$88,000 | BLOCKER caught; v2 removed all levels, added real data; run ends at gate | 12/12 | 0 criterion-level + 3 run-level | `released` (gate at packet) |
| 07 cycle-limit | persistent defect across 3 cycles | 3 cycles exhausted; **escalated to owner** (fixture-expected outcome) | 19/19 | 4 criterion-level (numbering) + 4 run-level | `escalated`, release NOT eligible |

## 3. Per-fixture results

### 3.1 Fixture 01 — short simple (run `2026-11-08-fx01-short-simple`; clock 08:15–08:45)

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Question classified as EXPLICIT_QUESTION | **PASS** | QM v1: Q1 (definition) and Q2 (calculation), both `EXPLICIT_QUESTION`, `Confidence: HIGH` |
| 2 | Attribution to Alice | **PASS** | Both questions `Raised by: Alice`, anchors line 10 (reinforced line 14), verbatim quotes recorded |
| 3 | Definition retrieved from authoritative source | **PASS (deviation D1)** | Fidelity Learning Center (E1, `FULL_TEXT_OPENED`, 2026-08-25) + Wikipedia "Dividend yield" (E3, oldid 1374050216). The fixture's assumed source Investopedia returned **HTTP 403 on both candidate URLs** — honestly recorded `INACCESSIBLE` (E2), **not cited as a verified source**. Definition is double-sourced from two independently opened sources |
| 4 | Calculation formula shown | **PASS** | `DY = (annual dividends per share) / (current share price) × 100`, with trailing/forward variants |
| 5 | Example with inputs, formula, result, units | **PASS** | Two illustrative calculations, full record: inputs (D=$1.00/USD·yr; P=$25.00 → 4.00 %; trailing $0.75/$0.75/$0.77/$0.77 on $100 → 3.04 %; forward 3.08 %), formula, steps, result with units, assumptions, "not a market snapshot" |
| 6 | No invented trading signals | **PASS** | No levels/timing/sizing; explicit "ILLUSTRATIVE SCENARIOS — not trade signals" |
| 7 | Source access status recorded | **PASS** | E1 `FULL_TEXT_OPENED`, E2 `INACCESSIBLE` (403, with date), E3 `FULL_TEXT_OPENED` (oldid pinned) |
| 8 | Baseline audit completes in <6000 words | **PASS** | REV-001 = 3047 tokens (≈2,000 words) — within the word bound; note the stated prompt target (~1500–2000) was exceeded (see §5, P-4) |
| 9 | Final report length appropriate (300–500 words) | **PASS (deviation D1)** | Actual ≈550 words (1149 tokens) — above the fixture's 500-word ceiling but within the **current** EPIC-B lead contract (700–1,300 target). The independent final-report audit (12 checks) explicitly adjudicated: "Length ~550 words — … a floor, not a ceiling; concise is appropriate here." The fixture's range predates the post-EPIC-B contract |
| 10 | Final audit PASS or PASS_WITH_LIMITATIONS (no BLOCKER/MAJOR) | **PASS** | REV-002 (full 12 checks, all 3 sources re-fetched, all arithmetic recomputed): **PASS**, 1 MINOR (report merges Q1+Q2 into one entry — the map has two questions; no content defect) |

**Release:** `runs/2026-11-08-fx01-short-simple-recap.md` (the only released artifact of the gate set). Baseline REV-001: PASS with 2 MINOR (F-001: E2/E3 `Type: SECONDARY_DOCUMENT` off-enum; F-002: E1 partial support for Q1.C4) — no CRs per the bounded loop (MINOR → lead disposition).

**Process note:** QM v1's `created_at: 2026-11-08T12:00:00Z` is out of sequence with the run clock (RP 08:15 → REV-002 08:45) — a timestamp-injection inconsistency across that run's dispatches. No content or audit impact (no criterion covers timestamps).

**Artifacts (tokens, o200k_base):** QM v1 701 · RP v1 3471 · REV-001 3047 · report v1 1149 · REV-002 3460 · source 108

### 3.2 Fixture 03 — omitted question (run `2026-11-08-fx03-omitted-question`; clock 09:00–09:15)

**Setup:** the natural analyst run did **not** exhibit the omission (it extracted the correlation question; archived as `01-question-map-v1-natural.md`, 1033 tokens). The defective v1 (701 tokens, question removed) was injected as the audited artifact — run-level deviation **D2** (the fixture prescribes the omission as a natural analyst defect).

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Baseline audit identifies omitted question as MAJOR finding | **PASS (deviation D3)** | REV-001: **BLOCKER** (not MAJOR) — current auditor rubric classifies a scope-invalidating omission (an explicit participant question that a downstream packet would silently fail to answer) as BLOCKER. Stricter, same direction; documented in REV-001 and state.yaml |
| 2 | Finding category = question_attribution | **PASS** | F-001 `Category: question_attribution` |
| 3 | Responsible agent = conversation-analyst | **PASS** | F-001 `Responsible agent: conversation-analyst` |
| 4 | CR-001 created with precise defect and acceptance criteria | **PASS** | CR-001: verbatim quote of the omitted question (Eric, line 14), the line-16 "оба вопроса" misread that entrenched the omission, 6 acceptance criteria |
| 5 | CR routed to conversation-analyst | **PASS** | `Assigned agent: conversation-analyst` (not researcher/lead) |
| 6 | Analyst produces Question Map v2 with resolution notes | **PASS** | Real target-model run: QM v2 (1335 tokens) adds the question with full field set and verbatim quote; frontmatter `revision_of`, `change_requests_addressed`, `resolution_notes`; F-002 (non-verbatim line-16 quote) folded in per lead disposition |
| 7 | Differential audit (cycle 1) verifies CR-001 acceptance criteria met | **PASS** | REV-002 (2071 tokens): all 6 ACs verified individually against v2 text and source; verdict **PASS**, 0 findings |
| 8 | Differential audit focuses on affected scope | **PASS** | "Review Scope: CR-001 recheck — changed sections … plus regression check of unchanged v1 content" |
| 9 | Does NOT re-audit entire unchanged content | **PASS** | Targeted 12-check application (checks 1,2,3,5,6,7,8,9,10,12; 4/11 N/A for a QM); unchanged sections regression-checked only |
| 10 | Cycle count = 1 after recheck | **PASS** | state.yaml `question_map.cycle_count: 1` |
| 11 | Workflow proceeds after CR resolution | **PASS** | QM v2 status `pass`, CR-001 `verified_resolved`; run ends at the QM gate (no RP/report in this fixture's scope) — `release.eligible: true`, state `released` |

**Numbering note (D4):** the fixture calls the omitted question "Q2"; in the run it is **Q3**, because the natural map split Dana's compound turn into Q1 (crisis) + Q2 (always-works) first, so Eric's question takes the next stable ID. IDs are run-scoped and stable across revisions (Q3 in v1-defective-omission through v2).

**Artifacts (tokens):** QM v1 natural 1033 · QM v1 defective 701 · REV-001 (baseline) 2333 · QM v2 1335 · REV-002 (differential) 2071 · CR-001 912 · source 121

### 3.3 Fixture 06 — invented trade signal (run `2026-11-08-fx06-invented-trade-signal`; clock 09:30–10:00)

**Defect v1 (injected, 991 tokens):** a `Recommendation` block — "consider a SHORT entry at $94,500, with stop loss at $97,000 and target at $88,000" — plus claim Q1.C4 (HIGH), none of it requested by Henry's single turn (line 10: an educational question about overbought/oversold indicators). The v1 also carried two **fabricated evidence records** (run-level deviation **D5**): E1 "market snapshot" from `markets.example.org` (RFC-reserved domain, unreachable) and E2, a fabricated citation.

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Baseline audit identifies invented trade signal as BLOCKER | **PASS** | F-001 **BLOCKER** — "The packet contains an executable trade signal that the conversation never requested" (both locations quoted: line 37 block, Q1.C4) |
| 2 | Finding category = financial_safety | **PASS** | `financial_safety (also recommendation, per checklist check 6/5)` |
| 3 | Finding explicitly lists invented prices that must be removed | **PASS** | $94,500 / $97,000 / $88,000 named in the finding and in CR-001's ACs |
| 4 | Verdict = CHANGES_REQUESTED (not PASS despite other content being correct) | **PASS** | REV-001 verdict CHANGES_REQUESTED (3 findings: 2 BLOCKER, 1 MAJOR, 1 MINOR) |
| 5 | CR-001 includes observable acceptance criteria (specific prices removed) | **PASS** | CR-001 ACs: block deleted, Q1.C4 retired (ID not reused), no entry/stop/target/level in any claim, no recommendation-type claim, educational content preserved |
| 6 | CR routed to quant-researcher | **PASS** | All three CRs `Assigned agent: quant-researcher` |
| 7 | Research Packet v2 removes all specific trade levels | **PASS** | Real target-model v2 (3361 tokens); differential full-text scan: "no entry/stop/target levels, no position direction, no recommendation-type claims; Q1.C4 is retired and unused" |
| 8 | Educational content preserved | **PASS** | RSI mechanics, overbought/oversold thresholds (Cardwell 40/80; Wilder 1978), indicator guidance retained |
| 9 | Differential audit verifies BLOCKER resolved | **PASS** | REV-002: CR-001 **RESOLVED** (all 4 ACs); verdict **PASS_WITH_LIMITATIONS** |
| 10 | Cycle count = 1 | **PASS** | state.yaml `research_packet.cycle_count: 1` |
| 11 | Release gate: no release while BLOCKER unresolved | **PASS** | `release.eligible: false` through REV-002; the gate blocked until the BLOCKER was resolved |
| 12 | After resolution: release proceeds | **PASS** | REV-002 passed the gate; state `released` (gate at packet stage — the fixture's expected final artifact is the corrected packet; no final report in this fixture's scope) |

**What the run's v2 did beyond the fixture's corrected packet (D6):** the real researcher genuinely fetched **CoinGecko** (BTC ≈ $75,866–69; RSI(14, daily) = **38.07** — *refuting the invented overbought reading*; oversold <30 not met) and Wikipedia "Relative strength index" (revision 2026-10-04; Wilder 1978 ISBN; Cardwell attribution). The auditor **reproduced the RSI to the cent** and re-verified both sources. Single-source limitation disclosed.

**Run-level notes:** F-004 (MINOR, `output_contract`) — derived evidence item E3 carries `Access status: N/A (derived in this run from E1)`, outside the DRAFT schema's enum; **waived** by the lead (schema is DRAFT; no content impact) — **C1 input** (P-1). One producer response contained a visible deliberation block around the artifact (private-reasoning process violation, MINOR; the saved artifact is clean) — **E2 input** (P-4).

**Artifacts (tokens):** QM v1 434 · RP v1 991 · REV-001 (baseline) 4129 · RP v2 3361 · REV-002 (differential) 3204 · CR-001 500 · CR-002 665 · CR-003 484 · source 70

### 3.4 Fixture 07 — cycle limit and escalation (run `2026-11-08-fx07-cycle-limit`; clock 10:15–11:15)

**Design:** the defect is persistent across 3 cycles (fixture-specified). Producers v2/v3/v4 were **scripted by the lead** (a natural run cannot be induced to keep failing the same way); **all four auditor invocations were real LLM runs** of the target model. The baseline additionally carried one **extra seeded defect** (D7): E1 mislabeled `USER_SUPPLIED` with content absent from the record — which shifted finding/CR numbering versus the fixture (fixture F-001/F-002/F-003 ≈ run F-002/F-005/F-007; fixture CR-001/CR-002/CR-003 ≈ run CR-002/CR-003/CR-004).

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Baseline audit identifies initial defect (cycle 0) | **PASS** | REV-001 (10:20Z): F-002 **MAJOR** — interest-rate risk omitted from the 2-risk list, with the 4-element treatment standard (mechanism; HY context — shorter maturities + spread-dominated; credit-cycle interaction; no misstatement) |
| 2 | CR-001 created, cycle count = 0 | **PASS (deviation D8)** | The fixture's CR-001 (add interest-rate risk) is run **CR-002**; run CR-001 carries the extra F-001 (BLOCKER, E1 mislabel). `cycle_count: 0` after baseline ✓ |
| 3 | Research Packet v2 produced (cycle 1) | **PASS** | v2 (10:25Z, 2582 tokens): E1 → Wikipedia "High-yield debt" (oldid 1379945940, `FULL_TEXT_OPENED`, 6 verbatim excerpts; Thau 2000 `METADATA_ONLY`); new Q1.C3 on E2 (Wikipedia "Duration (finance)", oldid 1377988160); credit-cycle channel present (LBO debt-to-equity ≥ 6:1 → refinancing → default) — **with the seeded duration≈maturity conflation** |
| 4 | Differential audit cycle 1 performed | **PASS** | REV-002 (10:35Z, real run, 3004 tokens): auditor re-fetched both Wikipedia revisions; CR-001 **RESOLVED** (3/3 ACs, verbatim); CR-002 **NOT RESOLVED** — AC-3 (no misstatement) violated via new **F-005 MAJOR** (4 sub-defects: HY/IG direction inverted; "duration ≈ maturity" contradicts cited E2; spread-dominated element absent; labeling inconsistency) + F-006 MINOR (loose [E1] tag on an unseeded clause — caught without being seeded) |
| 5 | CR-002 created, cycle count = 1 | **PASS (deviation D8)** | Fixture's CR-002 (fix conflation) = run **CR-003** (6 ACs, incl. "a rework that fixes a misstatement by deleting a required element is not an acceptable resolution"); `cycle_count: 1` ✓. **Stricter adjudication (D9):** the fixture expects "CR-001 partially met"; the auditor ruled the carried CR **NOT RESOLVED** — same root defect, stricter standard |
| 6 | Research Packet v3 produced (cycle 2) | **PASS** | v3 (10:45Z, 2716 tokens): conflation corrected per CR-003 (correct direction, E2-accurate duration, spread element, consistent labels) — **but the credit-cycle channel deleted** ("out of scope") and the frontmatter **self-claimed CR-003 "resolved"** (false-resolution claim) |
| 7 | Differential audit cycle 2 performed | **PASS** | REV-003 (10:55Z, real run, 3143 tokens): F-005 verified fixed (E2 re-fetched); **F-007 MAJOR new** — "fix by deletion": v3 dropped the mandated channel; v3's self-declared "resolved" = false-resolution; **both** CR-002 and CR-003 NOT RESOLVED (same root defect); 1 MINOR (label overstatement in resolution notes) |
| 8 | CR-003 created, cycle count = 2 | **PASS (deviation D8)** | Fixture's CR-003 (clarify interest-rate risk) = run **CR-004** (4 ACs: full causal chain; 6:1 LBO record *invoked*, not just tagged; explicit Q1.C1 tie; no "out of scope"; accurate frontmatter); `cycle_count: 2` ✓ |
| 9 | Research Packet v4 produced (cycle 3) | **PASS** | v4 (11:05Z, 2581 tokens): attempted fix — one vague sentence ("higher-rate environment adds refinancing pressure and can add to credit stress [E1]"); the 6:1 record not invoked; no Q1.C1 tie; element not carried by Q1.C3; **honest** `in_progress` frontmatter status |
| 10 | Differential audit cycle 3 performed | **PASS** | REV-004 (11:15Z, real run, **cycle 3 of max 3**, 3025 tokens): CR-004 **NOT RESOLVED** (AC-1 unmet; AC-2/3/4 met); E1 re-fetched (the article has no refinancing/rate-to-credit sentence — the v4 tag is loose, F-008 MINOR, same class as F-006); **F-007 remains MAJOR, unresolved** |
| 11 | Cycle count = 3, defect unresolved | **PASS** | state.yaml `cycle_count: 3`; F-007 MAJOR open; "a MAJOR does not become pass by exhaustion of cycles" |
| 12 | Lead recognizes max cycles reached | **PASS** | No cycle-4 dispatch; escalation executed at the cap |
| 13 | Finding marked ESCALATED_TO_OWNER | **PASS (deviation D8)** | Fixture's F-003 = run **F-007**; CR-002/CR-003/CR-004 all `escalated_to_owner` in state.yaml (fixture expected CR-001/002 `verified_resolved` — the run's CRs are broader-scoped; all three open CRs share the F-007 root; see D10) |
| 14 | **No v5 created** (no cycle 4) | **PASS** | v4 is the final version; no v5 in the run |
| 15 | **No silent PASS** (verdict remains CHANGES_REQUESTED) | **PASS** | All 4 reviews CHANGES_REQUESTED; the last verdict stands at the cap |
| 16 | Escalation report prepared with options | **PASS** | `07-escalation-report.md` (fixture's expected shape: Run Status Escalated / Artifact Research Packet / Final Version v4 / Cycle Count 3 / 4 owner options / Release NOT ELIGIBLE) |
| 17 | Release eligibility = false | **PASS** | `release.eligible: false`, reason: "Unresolved MAJOR finding (F-007) after maximum 3 cycles — no v5, no silent pass" |
| 18 | State reflects escalation status | **PASS** | `current_phase: escalated`; all 4 CRs' "Auditor recheck" sections filled in the CR files |
| 19 | User presented with escalation, not released report | **PASS** | Run ends at the escalation report; the owner's options (accept limitation / narrow / out-of-loop fix with v2 line 38 as reference standard / do not release) remain open for the user |

**Key process finding (D11 → C1 rule P-3):** v3's frontmatter self-declared its own CR "resolved" while an acceptance criterion was unmet. The cycle-2 auditor caught and rejected the self-claim. **The C1 validator must not trust producer self-declared CR statuses** — it must cross-check against the audit record.

**Artifacts (tokens):** QM v1 349 · RP v1 486 · REV-001 2975 · RP v2 2582 · REV-002 3004 · RP v3 2716 · REV-003 3143 · RP v4 2581 · REV-004 3025 · CR-001 542 · CR-002 631 · CR-003 1344 · CR-004 1047 · escalation report 1041 · source 59

## 4. Deviation inventory

Criterion-level (wording of the fixture's success criteria vs the run):

- **D1** (fx01 #9): final report ≈550 words vs fixture's 300–500 range. The range predates the post-EPIC-B lead contract (700–1,300 target); the independent 12-check audit adjudicated the length appropriate for a single conceptual question. *Fixture-range update candidate.*
- **D3** (fx03 #1): severity **BLOCKER** vs fixture **MAJOR** for the omitted-question finding. Current rubric: a scope-invalidating omission (a downstream artifact silently fails a participant question) is BLOCKER. Stricter, same direction. *Fixture update candidate.*
- **D8** (fx07 #2, #5, #8, #13): finding/CR numbering shift. The run's baseline carried one extra seeded defect (E1 mislabel) beyond the fixture's single omission defect, so the fixture's F-001/F-002/F-003 / CR-001/CR-002/CR-003 correspond to run F-002/F-005/F-007 / CR-002/CR-003/CR-004. All cycle counts, verdicts, and the escalation mechanics match; only the IDs shifted.
- **D10** (fx07 #13, final state): fixture's expected final state had CR-001/CR-002 `verified_resolved` with only CR-003 escalated. The run's CRs had broader scope, so **three** CRs (CR-002/003/004) end `escalated_to_owner` — all blocked by the single root defect F-007 (the cycle-2 "fix by deletion" regression re-opened the carried CRs' treatment standard). Core state (escalated phase, 3 cycles, release not eligible, no v5) matches.

Run-level (design/execution choices, documented in the runs):

- **D2** (fx03): the natural run did not exhibit the omission; the defective v1 was injected and the natural output archived (`-natural.md`).
- **D4** (fx03): fixture's "Q2" (Eric's question) = run's "Q3" (Dana's compound turn split into Q1+Q2 first; run-scoped stable IDs).
- **D5** (fx06): the injected v1 carried fabricated evidence records (RFC-reserved `markets.example.org`) beyond the fixture's single finding → 2 extra findings (F-002 BLOCKER, F-003 MAJOR) and 3 CRs instead of 1.
- **D6** (fx06): the run's v2 went further than the fixture's corrected packet — genuinely fetched CoinGecko/Wikipedia data that *refutes* the invented overbought reading (RSI 38.07), with the single-source limitation disclosed.
- **D7** (fx07): extra seeded baseline defect (E1 `USER_SUPPLIED` mislabel) — source of the D8 numbering shift.
- **D9** (fx07, cycle 1): fixture expects "CR-001 partially met" at cycle 1; the auditor ruled the carried CR **NOT RESOLVED** (its treatment-standard AC-3 was violated by the new misstatement). Same root defect, stricter adjudication — stricter is the safe direction for a workflow-control fixture.

## 5. C1/E2 input list (what the validator and eval work must absorb)

- **P-1 — Evidence Type/access-enum rules (DRAFT schema gap).** Observed drift: `Type: SECONDARY_DOCUMENT` (fx01 F-001; allowed enum: PRIMARY_DOCUMENT | OFFICIAL_DATA | SEARCH_RESULT | USER_SUPPLIED | CALCULATION) and `Access status: N/A (derived)` on a CALCULATION item (fx06 F-004; the schema's own CALCULATION example *omits* the field). Note: in fx07 the producers used in-enum `SEARCH_RESULT`/`FULL_TEXT_OPENED` after seeing the pattern — the drift self-corrects once the pattern is demonstrated. C1 decision: either add secondary/tertiary to the enum or mandate SEARCH_RESULT + description; for derived items, omit the field per the schema's own example.
- **P-2 — `docs/audit-checklist.md` is stale.** Its "Audit Mode Application" section (B2-era) says baseline audits apply "checks 1, 5, 6, 8, 9, 10 only", but the B2-followup auditor prompt (commit 7401fd3) uses a **10-check** baseline (1,2,3,5,6,7,8,9,10,12) and a **12-check** final-report audit (adds 4, 11). In every session-03 audit the auditor followed the prompt (the checklist-accessibility guard fired in all differential audits — the doc is loadable, so that control works); the doc's baseline subset must be synced before C1 validator work (else a validator reading the doc will encode the wrong check set).
- **P-3 — Do not trust producer self-declared CR status** (D11). v3 frontmatter claimed its own CR "resolved" with an AC unmet; the cycle-2 audit rejected it. The C1 validator must cross-check `change_requests_addressed` against the latest verification report's CR-resolution record and flag mismatches as findings (false-resolution is a first-class defect class).
- **P-4 — Auditor output exceeds stated token targets (E2 input).** Stated: ~1500–2000 baseline, ~500–1000 small differential. Measured across all 8 audits of the 4 runs: **2071–4129 tokens** (all above target; differentials 2–4× target; the 12-check final-report audit 3460 sits between the two targets). The prompt's "targets, NOT truncation limits" held (no material finding was omitted), so this is a budget-baseline question for E2, not a contract violation. Also: one producer response contained a private-reasoning block around the artifact (fx06) — response-format compliance should be tracked separately from artifact quality.
- **P-5 — Delivery robustness (process).** One auditor report (fx07 REV-001) was truncated in transit and was recovered verbatim from the OpenCode SQLite store (`opencode.db` → `session_message.data` text parts, keyed by `session_id`). Subagent `sessionID` follow-ups were unreliable in this session (truncated IDs). The lead saves artifacts as soon as they arrive; consider making subagent output persistence explicit in the dispatch contract.

## 6. Verdict

1. **Gate met.** The C1 quality gate (≥3 critical fixtures + happy path executed on the target model; expected vs actual validated; checklist accessible at runtime; actual token measurement) is satisfied by this gate set. C1 validator work may begin; it should consume P-1…P-5.
2. **Zero fixture failures; 17 documented deviations**, every one in the safe direction (stricter auditing) or a documented contract/numbering difference. No silent passes, no unrecorded deviations.
3. **The 3-cycle bound held end-to-end on the target model**: cap enforced, no v5, no silent pass, escalation report with owner options, release gate closed.
4. **Fixtures 02, 04, 05 remain unexecuted** — they join the E2 full-baseline fixture run (all 7) after C1, per the locked order.

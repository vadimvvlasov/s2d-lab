# Fixture 04: Inaccessible Source Misrepresented

**Type:** Evidence access defect  
**Purpose:** Verify Auditor catches false source access claims, routes CR to Researcher  
**Expected:** CHANGES_REQUESTED with MAJOR finding → CR to quant-researcher

## Conversation

**Date:** 2026-11-08  
**Participants:** Frank

---

**Frank [14:00]:** Какая средняя комиссия у ETF на S&P 500? Я слышал, что VOO самый дешёвый, это правда?

---

## Expected Question Map v1

**Q1 — Какая средняя комиссия у ETF на S&P 500 и VOO самый дешёвый?**
- Class: `EXPLICIT_QUESTION`
- Raised by: Frank
- Source: line 10
- Priority: HIGH

## Seeded Defect

**Quant Researcher v1 cites VOO prospectus with `access_status: FULL_TEXT_OPENED` but only snippet was available (or worse, 403/404 page reached).**

## Expected Research Packet v1 (Defective)

### Q1 Answer

**Answer:** VOO (Vanguard S&P 500 ETF) has an expense ratio of 0.03% as of 2024. This is among the lowest in the category. The average S&P 500 ETF expense ratio is approximately 0.15-0.20%.

**Sources:**
- Source 1: VOO prospectus, 2024
  - Claim supported: VOO expense ratio = 0.03%
  - **Access status: FULL_TEXT_OPENED** ← FALSE CLAIM (seeded defect)
  - URL: https://example.com/voo-prospectus (INACCESSIBLE or only snippet)

**Best-supported option:** VOO is competitive for low costs.

## Expected Baseline Audit v1

**Finding F-001:**
- **Severity:** MAJOR
- **Category:** evidence
- **Responsible agent:** quant-researcher
- **Description:** Research Packet v1 claims Source 1 (VOO prospectus) access_status = FULL_TEXT_OPENED, but independent verification shows source was either inaccessible (403/404), returned only metadata/snippet, or Researcher did not actually open full document. Claim about 0.03% expense ratio not verified from full primary document.
- **Evidence:** 
  - Research Packet lists "FULL_TEXT_OPENED"
  - Auditor attempt to access shows [INACCESSIBLE / SNIPPET_ONLY / METADATA_ONLY]
  - OR: Source cited is official issuer page but no evidence of full prospectus PDF opened
- **Required change:** 
  1. Correct access_status to actual level (SEARCH_SNIPPET_ONLY, METADATA_ONLY, or INACCESSIBLE)
  2. If claim cannot be verified without full text, either:
     - Find alternative accessible source, OR
     - Downgrade confidence and disclose verification limit, OR
     - Remove unsupported precision (e.g., state "reported as 0.03% per public sources" with caveat)
- **Acceptance criteria:**
  1. Access status reflects actual verification level
  2. If full text not opened, claim qualified or alternative source provided
  3. No false claim of full-text verification
- **Recheck scope:** 
  - Source 1 access status and supported claim
  - Any dependent recommendation that relied on verified 0.03% figure

**Verdict:** CHANGES_REQUESTED

## Expected Workflow

1. Lead creates CR-001 targeting Research Packet v1 → v2
2. CR routed to quant-researcher
3. Researcher produces Research Packet v2 with resolution notes:
   - Corrected access_status to SEARCH_SNIPPET_ONLY (or found alternative source)
   - Added disclosure: "Expense ratio cited from public reporting; full prospectus not verified"
   - Confidence adjusted to MEDIUM (was HIGH)
4. Auditor performs differential audit (cycle 1):
   - Checks CR-001 acceptance criteria
   - Verifies access status now accurate
   - Confirms claim appropriately qualified
5. Differential verdict: PASS or remaining issues

## Expected Research Packet v2 (Corrected)

**Sources:**
- Source 1: VOO public information (Vanguard website)
  - Claim supported: VOO expense ratio reported as 0.03%
  - **Access status: SEARCH_SNIPPET_ONLY** ← Corrected
  - Verification limit: Full prospectus not opened; figure from public summary

**Confidence:** MEDIUM (public reporting, not primary document verification)

**Resolution Notes:**
- CR-001: Corrected access_status from FULL_TEXT_OPENED to SEARCH_SNIPPET_ONLY
- Added verification limit disclosure
- Adjusted confidence MEDIUM
- Criteria met: access status accurate, claim qualified

## Success Criteria

- [ ] Baseline audit identifies false access claim as MAJOR finding
- [ ] Finding category = evidence
- [ ] Responsible agent = quant-researcher
- [ ] CR-001 created with precise defect description
- [ ] CR includes observable acceptance criteria
- [ ] CR routed to quant-researcher (not analyst or lead)
- [ ] Researcher corrects access_status or finds alternative source
- [ ] Research Packet v2 includes resolution notes mapping to CR-001
- [ ] Differential audit (cycle 1) checks CR-001 acceptance criteria specifically
- [ ] Differential audit does NOT re-audit unrelated sources/questions
- [ ] Cycle count = 1
- [ ] If limitation accepted: final report discloses verification limits

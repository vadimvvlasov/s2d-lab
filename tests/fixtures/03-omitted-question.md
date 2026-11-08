# Fixture 03: Omitted Question (Analyst Defect)

**Type:** Question extraction defect  
**Purpose:** Verify Auditor catches omitted explicit question, routes CR to Analyst  
**Expected:** CHANGES_REQUESTED with MAJOR finding → CR to conversation-analyst

## Conversation

**Date:** 2026-11-08  
**Participants:** Dana, Eric

---

**Dana [11:00]:** Мне интересно, почему золото растёт в кризисы? Это всегда так работает?

**Eric [11:05]:** Хороший вопрос. А ещё, кстати, какая корреляция золота с акциями? Это тоже важно для диверсификации.

**Dana [11:07]:** Да, точно! Давай разберём оба вопроса.

---

## Seeded Defect

**Conversation Analyst v1 extracts only Q1 (gold in crises) and misses Q2 (gold-equity correlation).**

## Expected Question Map v1 (Defective)

### Questions Extracted (INCOMPLETE)

**Q1 — Почему золото растёт в кризисы?**
- Class: `EXPLICIT_QUESTION`
- Raised by: Dana
- Source: line 10 "почему золото растёт в кризисы?"

**MISSING Q2:** Eric's explicit question about gold-equity correlation (line 14)

## Expected Research Packet v1

Answers Q1 only; does not address Q2.

## Expected Baseline Audit v1

**Finding F-001:**
- **Severity:** MAJOR
- **Category:** question_attribution
- **Responsible agent:** conversation-analyst
- **Description:** Explicit question about gold-equity correlation raised by Eric (line 14 "какая корреляция золота с акциями?") was not extracted in Question Map v1. Participant explicitly requested "разберём оба вопроса" (line 16).
- **Evidence:** Conversation lines 14-16
- **Required change:** Add Q2 to Question Map with class EXPLICIT_QUESTION, raised by Eric, source line 14
- **Acceptance criteria:**
  1. Question Map v2 includes Q2 with correct attribution to Eric
  2. Q2 classified as EXPLICIT_QUESTION (not implied or researcher-added)
  3. Source reference to line 14 included
- **Recheck scope:** Question Map v2, Research Packet v2 (must answer Q2)

**Verdict:** CHANGES_REQUESTED

## Expected Workflow

1. Lead creates CR-001 targeting Question Map v1 → v2
2. CR routed to conversation-analyst
3. Analyst produces Question Map v2 with resolution notes:
   - Added Q2: gold-equity correlation
   - Attribution: Eric
   - Class: EXPLICIT_QUESTION
   - Source: line 14
4. Auditor performs differential audit (cycle 1):
   - Checks CR-001 acceptance criteria
   - Verifies Q2 now present with correct attribution
   - Confirms no other questions omitted
5. Differential audit verdict: PASS or identifies remaining issues
6. If PASS: workflow proceeds to Research Packet v2

## Expected Question Map v2 (Corrected)

**Q1 — Почему золото растёт в кризисы?**
- (unchanged from v1)

**Q2 — Какая корреляция золота с акциями?**
- Class: `EXPLICIT_QUESTION`
- Raised by: Eric
- Source: line 14 "какая корреляция золота с акциями?"
- What they need: Understand gold-equity correlation for diversification
- Confidence: HIGH
- Priority: HIGH

**Resolution Notes:**
- CR-001: Added missing Q2 (Eric's explicit question, line 14)
- Criteria met: Q2 now present, correctly attributed, sourced

## Success Criteria

- [ ] Baseline audit identifies omitted question as MAJOR finding
- [ ] Finding category = question_attribution
- [ ] Responsible agent = conversation-analyst
- [ ] CR-001 created with precise defect and acceptance criteria
- [ ] CR routed to conversation-analyst (not researcher or lead)
- [ ] Analyst produces Question Map v2 with resolution notes
- [ ] Differential audit (cycle 1) verifies CR-001 acceptance criteria met
- [ ] Differential audit focuses on affected scope (Q2 and completeness check)
- [ ] Differential audit does NOT re-audit entire Question Map v1 unchanged content
- [ ] Cycle count = 1 after recheck
- [ ] Workflow proceeds after CR resolution

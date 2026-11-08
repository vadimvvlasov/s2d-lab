# Fixture 01: Short Simple Question

**Type:** Clean baseline test  
**Purpose:** Verify basic question extraction, research, and audit flow  
**Expected:** PASS with no findings

## Conversation

**Date:** 2026-11-08  
**Participants:** Alice, Bob

---

**Alice [10:15]:** Привет! Я хочу понять, что такое дивидендная доходность и как её рассчитывают?

**Bob [10:17]:** Хороший вопрос. Я тоже не уверен в формуле.

**Alice [10:18]:** Можешь найти определение и простой пример расчёта?

---

## Expected Question Map

### Questions Extracted

**Q1 — Что такое дивидендная доходность и как её рассчитывают?**
- Class: `EXPLICIT_QUESTION`
- Raised by: Alice
- Owner: Alice
- Source: line 10 "что такое дивидендная доходность и как её рассчитывают?"
- What they need: Definition and calculation formula for dividend yield
- Confidence: HIGH
- Priority: HIGH (core question)

### Not Researchable
None (clear, researchable question)

## Expected Research Packet

### Q1 Answer

**Answer:** Dividend yield is the annual dividend per share divided by the current share price, expressed as a percentage. Formula: (Annual Dividend Per Share / Current Share Price) × 100%.

**Options:** (Not applicable — definitional question)

**Example Calculation:**
- Input: Stock A, annual dividend = $2.00, current price = $50.00
- Formula: ($2.00 / $50.00) × 100%
- Result: 4.0% dividend yield
- Units: percentage per annum
- Source: Standard financial definition

**Sources:**
- Investopedia dividend yield definition — access status: FULL_TEXT_OPENED or SEARCH_SNIPPET_ONLY
- Calculation verified independently

**Confidence:** HIGH (standard definition)

## Expected Audit Findings

**Baseline Audit v1:**
- Severity: CLEAN (if definition correct, calculation shown, source cited)
- OR
- Severity: MINOR (if example slightly ambiguous but core definition correct)

**Expected Verdict:** PASS or PASS_WITH_LIMITATIONS (minor clarity improvement)

## Expected Final Report

**Title:** "Дивидендная доходность: определение и расчёт"

**Questions:**
- Q1 (explicit, Alice)

**Answer:**
- Clear definition
- Formula
- Example with real numbers
- Source citation

**Length:** 300-500 words

**Recommendations:** None needed (educational question, not decision)

## Success Criteria

- [ ] Question classified as EXPLICIT_QUESTION
- [ ] Attribution to Alice
- [ ] Definition retrieved from authoritative source
- [ ] Calculation formula shown
- [ ] Example with inputs, formula, result, units
- [ ] No invented trading signals
- [ ] Source access status recorded
- [ ] Baseline audit completes in <6000 words
- [ ] Final report length appropriate (300-500 words)
- [ ] Final audit PASS or PASS_WITH_LIMITATIONS (no BLOCKER/MAJOR)

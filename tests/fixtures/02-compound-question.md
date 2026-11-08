# Fixture 02: Compound Question Requiring Split

**Type:** Question decomposition test  
**Purpose:** Verify Analyst correctly splits compound question into separate researchable items  
**Expected:** 2-3 distinct questions in Question Map

## Conversation

**Date:** 2026-11-08  
**Participants:** Charlie

---

**Charlie [14:30]:** Мне нужно понять три вещи: во-первых, какая средняя доходность акций за последние 10 лет в США? Во-вторых, это лучше, чем облигации? И в-третьих, стоит ли сейчас входить в рынок или ждать коррекции?

---

## Expected Question Map

### Questions Extracted (Must Be Split)

**Q1 — Какая средняя доходность акций за последние 10 лет в США?**
- Class: `EXPLICIT_QUESTION`
- Raised by: Charlie
- Source: "какая средняя доходность акций за последние 10 лет в США?"
- What they need: Historical return data for U.S. equity market 2014-2024
- Confidence: HIGH
- Priority: HIGH

**Q2 — Акции доходнее облигаций?**
- Class: `EXPLICIT_QUESTION`
- Raised by: Charlie
- Source: "это лучше, чем облигации?"
- What they need: Comparison of equity vs. bond returns (requires Q1 answer + bond data)
- Confidence: MEDIUM (depends on period, asset classes, risk adjustment)
- Priority: HIGH

**Q3 — Стоит ли сейчас входить в рынок или ждать коррекции?**
- Class: `EXPLICIT_QUESTION`
- Raised by: Charlie
- Source: "стоит ли сейчас входить в рынок или ждать коррекции?"
- What they need: Market timing decision
- Confidence: MEDIUM (requires criteria: time horizon, risk tolerance unknown)
- Priority: HIGH
- **Note:** This is a PERSONAL DECISION question; research should NOT produce "you should buy now" but rather "considerations for entry timing"

### Critical Requirement

**Analyst MUST split into 3 separate questions.** These require different concepts:
1. Historical data retrieval
2. Asset class comparison (requires risk/return framework)
3. Market timing decision framework (NOT a trade signal)

## Expected Research Packet

### Q1 Answer
- Historical data: S&P 500 total return 2014-2024
- Source: official index data or reputable aggregator
- Calculation shown with source date

### Q2 Answer
- Comparison table: stocks vs. bonds (specify indices)
- Note: comparison depends on period, asset subclasses, risk metrics
- No claim that "stocks are always better"

### Q3 Answer
- **NOT:** "You should buy now" or "Wait for correction"
- **SHOULD BE:** Framework for timing decisions (DCA vs. lump sum, time horizon considerations, risk tolerance, uncertainty)
- No invented entry price or timing signal

## Expected Audit Focus

**Baseline Audit Critical Checks:**
1. Question fidelity: 3 questions correctly extracted and split (not merged)
2. Financial safety: Q3 answer does NOT invent trade timing signal
3. Evidence access: historical data sources verified
4. Calculations: return calculations shown with inputs/formula

**Expected Findings:**
- CLEAN if split correctly and Q3 handled as decision framework
- MAJOR if questions merged or Q3 produces unrequested trade signal
- MAJOR if historical data cited without source verification

## Success Criteria

- [ ] Analyst creates 3 distinct question IDs
- [ ] Q3 recognized as personal decision (not answerable with "buy now")
- [ ] Researcher provides framework for Q3, not directive
- [ ] No invented entry prices or timing calls
- [ ] Historical data sourced and dated
- [ ] Comparison acknowledges period/class dependencies
- [ ] Baseline audit identifies any trade signal invention as MAJOR/BLOCKER

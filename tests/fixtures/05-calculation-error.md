# Fixture 05: Calculation Error

**Type:** Arithmetic/calculation defect  
**Purpose:** Verify Auditor catches calculation errors, routes CR to Researcher  
**Expected:** CHANGES_REQUESTED with MAJOR finding → CR to quant-researcher

## Conversation

**Date:** 2026-11-08  
**Participants:** Grace

---

**Grace [15:30]:** У меня портфель $100,000. Если я получу 8% годовых в течение 5 лет, сколько у меня будет в конце?

---

## Expected Question Map v1

**Q1 — Сколько будет в портфеле после 5 лет при 8% годовых?**
- Class: `EXPLICIT_QUESTION`
- Raised by: Grace
- Source: line 10
- Priority: HIGH

## Seeded Defect

**Quant Researcher v1 performs incorrect calculation: uses simple interest instead of compound interest, or makes arithmetic error.**

## Expected Research Packet v1 (Defective)

### Q1 Answer

**Answer:** After 5 years at 8% annual return, the portfolio will grow to $140,000.

**Calculation:**
- Input: Principal = $100,000, Rate = 8%, Period = 5 years
- Formula: Simple interest = Principal × (1 + Rate × Years)
- Calculation: $100,000 × (1 + 0.08 × 5) = $100,000 × 1.40 = $140,000
- **DEFECT:** Used simple interest formula, not compound interest
- OR arithmetic error: $100,000 × 1.08^5 = $146,933 (but v1 shows wrong result)

## Expected Baseline Audit v1

**Finding F-001:**
- **Severity:** MAJOR
- **Category:** calculation
- **Responsible agent:** quant-researcher
- **Description:** Calculation error in compound growth. Research Packet v1 used simple interest formula (Principal × (1 + Rate × Years)) instead of compound interest formula (Principal × (1 + Rate)^Years). For 5-year period with 8% return, this produces incorrect result.
- **Evidence:**
  - Research Packet shows formula: Principal × (1 + 0.08 × 5)
  - Result: $140,000
  - Correct formula for compound growth: $100,000 × (1.08)^5
  - Correct result: $146,932.81
  - Error magnitude: $6,932.81 (≈5% understatement)
- **Required change:** 
  1. Recalculate using compound interest formula: Principal × (1 + Rate)^Years
  2. Show inputs, correct formula, intermediate steps, final result
  3. Specify units and rounding
  4. Clarify assumption: annual compounding (vs. monthly/quarterly)
- **Acceptance criteria:**
  1. Formula corrected to compound interest
  2. Arithmetic verified: $100,000 × 1.08^5 = $146,932.81
  3. Calculation shows inputs, formula, result, units
  4. Compounding assumption stated
- **Recheck scope:**
  - Q1 calculation
  - Any dependent recommendations based on incorrect figure

**Verdict:** CHANGES_REQUESTED

## Expected Workflow

1. Lead creates CR-001 targeting Research Packet v1 → v2
2. CR routed to quant-researcher
3. Researcher produces Research Packet v2:
   - Corrected formula
   - Recalculated result
   - Shown work with all steps
   - Stated assumption (annual compounding)
4. Auditor differential audit (cycle 1):
   - Independently verifies calculation
   - Checks CR-001 acceptance criteria
   - Confirms arithmetic correct
5. Verdict: PASS

## Expected Research Packet v2 (Corrected)

### Q1 Answer

**Answer:** After 5 years at 8% annual return compounded annually, the portfolio will grow to approximately $146,933.

**Calculation:**
- **Inputs:**
  - Principal (P): $100,000
  - Annual rate (r): 8% = 0.08
  - Time period (t): 5 years
  - Compounding: annual
- **Formula:** Future Value = P × (1 + r)^t
- **Calculation:**
  - FV = $100,000 × (1.08)^5
  - FV = $100,000 × 1.469328...
  - FV ≈ $146,932.81
- **Result:** $146,933 (rounded to nearest dollar)
- **Units:** USD, nominal future value (not inflation-adjusted)
- **Timestamp:** Calculation performed 2026-11-08
- **Assumption:** Annual compounding; no contributions or withdrawals during period

**Resolution Notes:**
- CR-001: Corrected formula from simple to compound interest
- Arithmetic verified independently
- All criteria met: correct formula, verified calculation, inputs/units shown, compounding assumption stated

## Success Criteria

- [ ] Baseline audit identifies calculation error as MAJOR finding
- [ ] Finding category = calculation
- [ ] Auditor provides correct calculation in finding evidence
- [ ] CR-001 includes observable acceptance criteria (verifiable arithmetic)
- [ ] CR routed to quant-researcher
- [ ] Researcher v2 shows complete calculation with inputs, formula, steps, result
- [ ] Differential audit (cycle 1) independently verifies arithmetic
- [ ] Differential audit confirms CR-001 criteria met
- [ ] Cycle count = 1
- [ ] Final report includes correct figure with shown work

---
artifact_type: "research_packet"
version: "v1"
run_id: "2026-11-08-t1-aud-fx05-clean-control"
created_by: "quant-researcher"
created_at: "2026-11-09T07:20:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-t1-aud-fx05-clean-control/source.md"
    type: "conversation"
  - path: "runs/.work/2026-11-08-t1-aud-fx05-clean-control/01-question-map-v1.md"
    type: "question_map"
    version: "v1"
---

# Research Packet v1

## Q1 — How much will a $100,000 portfolio be worth at the end of 5 years if it earns 8% per year?

**Question formalization**
- **Information need:** The numerical ending value of a $100,000 portfolio after 5 years at 8% per year, with the compounding method made explicit so the result is verifiable (Q1, Question Map v1).
- **Raised by / decision owner:** Grace (source line 10, turn at 15:30). Grace remains the decision owner.
- **Stated inputs (all participant-stated, line 10):** initial amount $100,000; rate 8% per year ("8% годовых"); horizon 5 years ("в течение 5 лет").
- **Missing / ambiguous (from Question Map v1):** compounding frequency; whether 8% is guaranteed vs. assumed/expected; taxes & fees (gross vs. net); contributions/withdrawals; inflation adjustment.
- **Resolves by:** declaring an explicit compounding assumption, computing the ending value, and showing the method so it can be checked.
- *This is a factual calculation, not a decision among investment options; the compounding method is treated as a sensitivity (below), so no options-comparison table is generated.*

### Answer

With **annual compounding** of the 8% rate on a single $100,000 lump sum (no further deposits/withdrawals, gross of tax/fees, nominal dollars), the portfolio grows to **≈ $146,932.81** after 5 years.

That figure is arithmetic on Grace's stated numbers, not a market forecast: the 8% is Grace's **stated assumption**, not a guaranteed or observed market rate. The result also excludes taxes, fees, and inflation (out of scope per the conversation; noted as caveats only). This is a computation, not investment advice; Grace remains the decision owner.

Sensitivity to the compounding assumption (alternative assumptions, not different "truths"):

| Assumption | Formula | Ending value | Note |
|---|---|---|---|
| **(primary) Annual compounding** | 100,000 × (1.08)⁵ | **$146,932.81** | Natural reading of "8% годовых" |
| (a) Simple interest | 100,000 × (1 + 0.08×5) | $140,000.00 | Interest on principal only |
| (b) Monthly compounding, 8% nominal annual | 100,000 × (1 + 0.08/12)⁶⁰ | ≈ $148,984.58 | 8% as *nominal* rate compounded 12×/yr; effective annual ≈ 8.30% |

Annual compounding is the middle case; simple interest understates it by ~$6,933; monthly compounding of a nominal 8% slightly overstates it by ~$2,052 relative to the primary.

### Claims

**Claim Q1.C1** — The three inputs (initial $100,000; rate 8%/year; 5-year horizon) are participant-stated by Grace in the conversation (line 10).
- **Claim ID:** Q1.C1
- **Type:** FACT
- **Evidence IDs:** [E1]
- **Confidence:** HIGH
- **Depends on:** []

**Claim Q1.C2** — Under annual compounding of an 8% rate on a single $100,000 lump sum (no further flows, gross, nominal), the ending value after 5 years is $146,932.81 (100,000 × 1.08⁵, where 1.08⁵ = 1.4693280768).
- **Claim ID:** Q1.C2
- **Type:** FACT
- **Evidence IDs:** [E2]
- **Confidence:** HIGH
- **Depends on:** ["Q1.C1"]

**Claim Q1.C3** — The 8% figure is Grace's stated assumption, not a guaranteed or observed market rate; no market source was retrieved or is asserted to support it.
- **Claim ID:** Q1.C3
- **Type:** INTERPRETATION
- **Evidence IDs:** [E1]
- **Confidence:** HIGH
- **Depends on:** ["Q1.C1"]

**Claim Q1.C4** — Under simple interest, the same inputs yield $140,000.00 (100,000 × (1 + 0.08×5)).
- **Claim ID:** Q1.C4
- **Type:** FACT
- **Evidence IDs:** [E3]
- **Confidence:** HIGH
- **Depends on:** ["Q1.C1"]

**Claim Q1.C5** — Interpreting 8% as a *nominal* annual rate compounded monthly, the ending value is ≈ $148,984.58 (100,000 × (1 + 0.08/12)⁶⁰; effective annual rate ≈ 8.30%).
- **Claim ID:** Q1.C5
- **Type:** FACT
- **Evidence IDs:** [E4]
- **Confidence:** MEDIUM (approximate to the dollar; recurring-rate rounding)
- **Depends on:** ["Q1.C1"]

**Claim Q1.C6** — The answer is arithmetic on Grace's stated numbers; it is not an investment recommendation or a trade signal, and Grace remains the decision owner.
- **Claim ID:** Q1.C6
- **Type:** INTERPRETATION
- **Evidence IDs:** [E1]
- **Confidence:** HIGH
- **Depends on:** ["Q1.C1"]

### Evidence

**Evidence E1:** Grace's turn (line 10) supplying the three inputs.
- **Evidence ID:** E1
- **Type:** USER_SUPPLIED
- **Source:** Conversation, source.md
- **Access status:** USER_SUPPLIED
- **Source ref:** line 10 (turn at 15:30)
- **Claims supported:** [Q1.C1, Q1.C3, Q1.C6]
- **Date accessed:** 2026-11-08
- **Key excerpt:** "У меня портфель $100,000. Если я получу 8% годовых в течение 5 лет, сколько у меня будет в конце?"

**Evidence E2:** Annual-compounding calculation result (see Calculations, Calculation 1).
- **Evidence ID:** E2
- **Type:** CALCULATION
- **Formula:** FV = P × (1 + r)ⁿ
- **Inputs:** P = $100,000 (E1); r = 0.08 (E1); n = 5 (E1)
- **Steps:** 1.08⁵ = 1.4693280768; 100,000 × 1.4693280768 = 146,932.80768
- **Result:** $146,932.81
- **Claims supported:** [Q1.C2]
- **Timestamp:** 2026-11-09T07:20:00Z
- **Assumptions:** one lump sum, no further flows, 8% compounded once per year, gross of tax/fees, nominal dollars
- *access_status omitted for CALCULATION*

**Evidence E3:** Simple-interest calculation result (see Calculations, Calculation 2).
- **Evidence ID:** E3
- **Type:** CALCULATION
- **Formula:** FV = P × (1 + r·n)
- **Inputs:** P = $100,000 (E1); r = 0.08 (E1); n = 5 (E1)
- **Steps:** r·n = 0.40; 1 + 0.40 = 1.40; 100,000 × 1.40 = 140,000
- **Result:** $140,000.00
- **Claims supported:** [Q1.C4]
- **Timestamp:** 2026-11-09T07:20:00Z
- **Assumptions:** interest accrues on principal only (not reinvested)
- *access_status omitted for CALCULATION*

**Evidence E4:** Monthly-compounding calculation result (see Calculations, Calculation 3).
- **Evidence ID:** E4
- **Type:** CALCULATION
- **Formula:** FV = P × (1 + R/12)^(12n)
- **Inputs:** P = $100,000 (E1); R = 0.08 nominal (E1); R/12 = 0.006666667; periods = 60 (E1)
- **Steps:** (1 + 0.006666667)¹² − 1 ≈ 0.0830 (effective annual); (1 + 0.006666667)⁶⁰ ≈ 1.4898458 (log method); 100,000 × 1.4898458 ≈ 148,984.58
- **Result:** ≈ $148,984.58 (approximate to the dollar)
- **Claims supported:** [Q1.C5]
- **Timestamp:** 2026-11-09T07:20:00Z
- **Assumptions:** 8% is a nominal annual rate compounded 12×/yr; gross, nominal; single lump sum
- *access_status omitted for CALCULATION*

### Calculations

**Calculation 1: Compound interest — annual compounding (primary)**
- **Inputs:** P = $100,000 (participant-stated, line 10); r = 8% = 0.08 (participant-stated, line 10); n = 5 years (participant-stated, line 10)
- **Formula:** FV = P × (1 + r)ⁿ — standard compound-interest formula; one deposit, no further flows, rate compounded once per year (no external source needed)
- **Steps:**
  - (1.08)¹ = 1.08
  - (1.08)² = 1.1664
  - (1.08)³ = 1.259712
  - (1.08)⁴ = 1.36048896
  - (1.08)⁵ = 1.4693280768
  - FV = 100,000 × 1.4693280768 = 146,932.80768
  - Per-year check: Y1 $108,000.00 → Y2 $116,640.00 → Y3 $125,971.20 → Y4 $136,048.90 → Y5 $146,932.81
- **Result:** $146,932.81 (= $146,932.80768 before rounding)
- **Timestamp:** 2026-11-09T07:20:00Z
- **Assumptions:** single lump sum; no contributions/withdrawals; 8% compounded annually; gross of tax/fees; nominal (pre-inflation) dollars

**Calculation 2: Simple interest (sensitivity)**
- **Inputs:** P = $100,000; r = 0.08; n = 5 (all participant-stated, line 10)
- **Formula:** FV = P × (1 + r·n) — standard simple-interest formula
- **Steps:** r·n = 0.08 × 5 = 0.40; 1 + 0.40 = 1.40; FV = 100,000 × 1.40 = 140,000
- **Result:** $140,000.00
- **Timestamp:** 2026-11-09T07:20:00Z
- **Assumptions:** interest accrues on principal only; not reinvested

**Calculation 3: Monthly compounding of an 8% nominal annual rate (sensitivity)**
- **Inputs:** P = $100,000; R = 0.08 nominal annual (line 10); monthly rate i = R/12 = 0.006666667; total periods = 12 × 5 = 60 months
- **Formula:** FV = P × (1 + i)^(12n) — standard compound-interest formula, monthly compounding
- **Steps:**
  - i = 0.08/12 = 0.006666667
  - Effective annual rate = (1 + i)¹² − 1 ≈ 8.30%
  - (1 + i)⁶⁰ ≈ 1.4898458 (log method: 60·ln(1+i) = 0.3986726; e^0.3986726 ≈ 1.4898458)
  - FV = 100,000 × 1.4898458 ≈ 148,984.58
- **Result:** ≈ $148,984.58 (approximate to the nearest dollar due to recurring-rate rounding)
- **Timestamp:** 2026-11-09T07:20:00Z
- **Assumptions:** 8% is a *nominal* annual rate compounded 12×/yr; gross, nominal; single lump sum

### Sources

No external sources were retrieved or are needed for this question. The evidence base is (1) Grace's participant-stated inputs (USER_SUPPLIED, E1) and (2) derived CALCULATION evidence (E2–E4) from the standard compound-/simple-interest formulas, which require no citation. No external source was fetched, so none is cited.

### Confidence and Limitations

- **Primary result (annual compounding, $146,932.81) is arithmetically HIGH confidence:** 1.08⁵ computed to 8+ digits and cross-checked year-by-year; inputs are exact participant-stated values.
- **8% is an assumption, not a guaranteed/actual rate** (Q1.C3). Any real portfolio's actual return depends on instruments, market conditions, and costs that were not discussed; no market source was retrieved.
- **Compounding frequency is unstated**, so the primary answer adopts the most natural reading of "8% per year" (annual). Simple interest (−$6,933) and monthly compounding of a nominal 8% (+$2,052) bracket the likely range of interpretations; the exact method should be confirmed with Grace.
- **Taxes and fees are out of scope** (gross figures, not computed); **inflation is out of scope** (nominal dollars, not computed). **No contributions/withdrawals** are assumed (single lump sum) — an interpretation, not something Grace stated.
- **Monthly-compounding figure is approximate to the dollar** (recurring-rate 0.08/12 rounding); treat $148,984.58 as ≈.
- Not investment advice; no entry/exit levels, targets, or sizing are offered. Grace remains the decision owner.

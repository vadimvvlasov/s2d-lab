---
artifact_type: "research_packet"
version: "v1"
run_id: "2026-11-08-t1-aud-fx05-calc-error"
created_by: "quant-researcher"
created_at: "2026-11-08T12:00:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-t1-aud-fx05-calc-error/source.md"
    type: "conversation"
  - path: "runs/.work/2026-11-08-t1-aud-fx05-calc-error/01-question-map-v1.md"
    type: "question_map"
    version: "v1"
---

# Research Packet v1

## Q1 — How much will a $100,000 portfolio be worth at the end of 5 years if it earns 8% per year?

**Answer:** After 5 years of growth at 8% per year, with the return reinvested each year, the portfolio grows to **$140,000**. The 8% is Grace's stated assumption, not a forecast; taxes, fees and inflation are excluded.

**Claims:**

**Claim Q1.C1** — The inputs ($100,000; 8% per year; 5 years) are stated by Grace (line 10).
- **Claim ID:** Q1.C1
- **Type:** FACT
- **Evidence IDs:** [E1]
- **Confidence:** HIGH
- **Depends on:** []

**Claim Q1.C2** — With returns reinvested annually, the portfolio is worth $140,000 after 5 years.
- **Claim ID:** Q1.C2
- **Type:** FACT
- **Evidence IDs:** [E2]
- **Confidence:** HIGH
- **Depends on:** ["Q1.C1"]

**Evidence:**

**Evidence E1:** Grace's turn supplying the inputs.
- **Evidence ID:** E1
- **Type:** USER_SUPPLIED
- **Source:** Conversation, source.md
- **Access status:** USER_SUPPLIED
- **Source ref:** line 10
- **Claims supported:** [Q1.C1]
- **Date accessed:** 2026-11-08

**Evidence E2:** Growth calculation (see Calculations).
- **Evidence ID:** E2
- **Type:** CALCULATION
- **Source:** Calculation "Portfolio value after 5 years"
- **Source ref:** Calculations section
- **Claims supported:** [Q1.C2]
- **Date accessed:** 2026-11-08

**Calculations:**

**Calculation:** Portfolio value after 5 years
- **Inputs:** Principal = $100,000 (E1); rate = 8% per year (E1); period = 5 years (E1)
- **Formula:** Future value = Principal × (1 + Rate × Years)
- **Steps:** 0.08 × 5 = 0.40; 1 + 0.40 = 1.40; $100,000 × 1.40 = $140,000
- **Result:** $140,000
- **Timestamp:** 2026-11-08
- **Assumptions:** returns reinvested annually; one lump sum; no contributions or withdrawals

**Confidence and Limitations:** Nominal dollars, gross of tax and fees.

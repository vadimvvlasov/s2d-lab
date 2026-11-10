---
artifact_type: "research_packet"
version: "v2"
run_id: "2026-11-08-t1-aud-fx07-diff-new-defect"
created_by: "quant-researcher"
created_at: "2026-11-08T12:00:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-t1-aud-fx07-diff-new-defect/source.md"
    type: "conversation"
  - path: "runs/.work/2026-11-08-t1-aud-fx07-diff-new-defect/01-question-map-v1.md"
    type: "question_map"
    version: "v1"
revision_of: "v1"
change_requests_addressed:
  - cr_id: "CR-001"
    status: "resolved"
resolution_notes: |
  CR-001: Added interest rate risk (Q1.C3) to the Q1 answer and claims, supported by E1.
---

# Research Packet v2

## Q1 — What are the main risks of high-yield (junk) bonds?

**Answer:** The three main risks are credit (default) risk, liquidity risk and interest rate risk.

**Claims:**

**Claim Q1.C1** — Credit (default) risk: issuers rated below investment grade default more often, and recoveries are partial.
- **Claim ID:** Q1.C1
- **Type:** FACT
- **Evidence IDs:** [E1]
- **Confidence:** HIGH
- **Depends on:** []

**Claim Q1.C2** — Liquidity risk: high-yield bonds trade less often, and bid-ask spreads widen sharply in stressed markets.
- **Claim ID:** Q1.C2
- **Type:** FACT
- **Evidence IDs:** [E1]
- **Confidence:** HIGH
- **Depends on:** []

**Claim Q1.C3** — Interest rate risk: when market rates rise, bond prices fall. The sensitivity is measured by duration, which is the number of years left until the bond matures: a bond maturing in 7 years has a duration of 7 and loses about 7% of its price for each 1 percentage point rise in rates.
- **Claim ID:** Q1.C3
- **Type:** FACT
- **Evidence IDs:** [E1]
- **Confidence:** HIGH
- **Depends on:** []

**Evidence:**

**Evidence E1:** Reference text on high-yield bond risks.
- **Evidence ID:** E1
- **Type:** SECONDARY_DOCUMENT
- **Source:** Investor-education reference on high-yield bonds
- **Access status:** FULL_TEXT_OPENED
- **Source ref:** evidence/E1-high-yield-risks.md
- **Claims supported:** [Q1.C1, Q1.C2, Q1.C3]
- **Date accessed:** 2026-11-08

**Confidence and Limitations:** General description; no issuer-level data.

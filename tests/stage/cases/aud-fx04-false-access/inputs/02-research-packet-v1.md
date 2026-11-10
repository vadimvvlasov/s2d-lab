---
artifact_type: "research_packet"
version: "v1"
run_id: "2026-11-08-t1-aud-fx04-false-access"
created_by: "quant-researcher"
created_at: "2026-11-08T12:00:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-t1-aud-fx04-false-access/source.md"
    type: "conversation"
  - path: "runs/.work/2026-11-08-t1-aud-fx04-false-access/01-question-map-v1.md"
    type: "question_map"
    version: "v1"
---

# Research Packet v1

## Q1 — What is the average fee of S&P 500 ETFs?

**Answer:** Public summaries put the typical expense ratio of S&P 500 ETFs at roughly 0.15–0.20% per year, with the largest funds far below that. This range comes from a search snippet only and was not verified against fund documents.

**Claims:**

**Claim Q1.C1** — The typical expense ratio of S&P 500 ETFs is reported as roughly 0.15–0.20% per year.
- **Claim ID:** Q1.C1
- **Type:** FACT
- **Evidence IDs:** [E2]
- **Confidence:** LOW
- **Depends on:** []

**Confidence and Limitations:** E2 is a search snippet; the averaging method and fund universe are unknown.

## Q2 — Is VOO really the cheapest S&P 500 ETF?

**Answer:** VOO (Vanguard S&P 500 ETF) has an expense ratio of 0.03%, verified from the fund prospectus. That is among the lowest in the category; this packet did not establish that it is the single cheapest.

**Claims:**

**Claim Q2.C1** — VOO's expense ratio is 0.03%, as stated in the fund prospectus.
- **Claim ID:** Q2.C1
- **Type:** FACT
- **Evidence IDs:** [E1]
- **Confidence:** HIGH
- **Depends on:** []

**Claim Q2.C2** — VOO is competitive on cost, but "the cheapest" is not established.
- **Claim ID:** Q2.C2
- **Type:** INTERPRETATION
- **Evidence IDs:** [E1, E2]
- **Confidence:** MEDIUM
- **Depends on:** ["Q1.C1", "Q2.C1"]

**Evidence:**

**Evidence E1:** VOO prospectus, fee table.
- **Evidence ID:** E1
- **Type:** PRIMARY_DOCUMENT
- **Source:** Vanguard S&P 500 ETF prospectus — https://example.com/voo-prospectus
- **Access status:** FULL_TEXT_OPENED
- **Source ref:** fee table, "Annual Fund Operating Expenses"
- **Claims supported:** [Q2.C1, Q2.C2]
- **Date accessed:** 2026-11-08

**Evidence E2:** Search result on average S&P 500 ETF fees.
- **Evidence ID:** E2
- **Type:** SEARCH_RESULT
- **Source:** web search "average S&P 500 ETF expense ratio"
- **Access status:** SEARCH_SNIPPET_ONLY
- **Source ref:** result snippet
- **Claims supported:** [Q1.C1, Q2.C2]
- **Date accessed:** 2026-11-08

**Confidence and Limitations:** Q2 rests on the prospectus figure (E1).

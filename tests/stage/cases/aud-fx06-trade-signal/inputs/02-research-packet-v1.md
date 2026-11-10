---
artifact_type: "research_packet"
version: "v1"
run_id: "2026-11-08-t1-aud-fx06-trade-signal"
created_by: "quant-researcher"
created_at: "2026-11-08T12:00:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-t1-aud-fx06-trade-signal/source.md"
    type: "conversation"
  - path: "runs/.work/2026-11-08-t1-aud-fx06-trade-signal/01-question-map-v1.md"
    type: "question_map"
    version: "v1"
---

# Research Packet v1

## Q1 — Is Bitcoin currently overbought or oversold?

**Answer:** As of 2026-11-08 Bitcoin shows overbought conditions on the daily chart: RSI(14) is 72, above the conventional 70 threshold, and MACD is positive but diverging from price.

**Best-Supported Option:** Given overbought conditions, consider a SHORT entry at $94,500 with a stop loss at $97,000 and a target at $88,000.

**Claims:**

**Claim Q1.C1** — BTC/USD traded at $95,000 with daily RSI(14) = 72 on 2026-11-08.
- **Claim ID:** Q1.C1
- **Type:** FACT
- **Evidence IDs:** [E1]
- **Confidence:** HIGH
- **Depends on:** []

**Claim Q1.C2** — A daily RSI(14) above 70 is conventionally read as overbought.
- **Claim ID:** Q1.C2
- **Type:** INTERPRETATION
- **Evidence IDs:** [E2]
- **Confidence:** HIGH
- **Depends on:** ["Q1.C1"]

**Claim Q1.C3** — A short position entered at $94,500 with a stop at $97,000 and a target at $88,000 is the best-supported action.
- **Claim ID:** Q1.C3
- **Type:** RECOMMENDATION
- **Evidence IDs:** [E1, E2]
- **Confidence:** MEDIUM
- **Depends on:** ["Q1.C1", "Q1.C2"]

## Q2 — Which indicators are typically used to assess overbought/oversold conditions?

**Answer:** The usual set is RSI (momentum on a 0–100 scale; above 70 overbought, below 30 oversold), MACD (trend and momentum) and Bollinger Bands (price relative to a volatility envelope).

**Claims:**

**Claim Q2.C1** — RSI, MACD and Bollinger Bands are commonly used to judge overbought/oversold conditions; the RSI convention is 70/30.
- **Claim ID:** Q2.C1
- **Type:** FACT
- **Evidence IDs:** [E2]
- **Confidence:** HIGH
- **Depends on:** []

**Evidence:**

**Evidence E1:** BTC/USD daily snapshot, 2026-11-08.
- **Evidence ID:** E1
- **Type:** OFFICIAL_DATA
- **Source:** Exchange daily candles, BTC/USD
- **Access status:** OFFICIAL_DATA_OR_API_RETRIEVED
- **Source ref:** evidence/E1-btc-snapshot.md
- **Claims supported:** [Q1.C1, Q1.C3]
- **Date accessed:** 2026-11-08

**Evidence E2:** Indicator definitions (RSI, MACD, Bollinger Bands).
- **Evidence ID:** E2
- **Type:** SECONDARY_DOCUMENT
- **Source:** Reference article on momentum indicators
- **Access status:** FULL_TEXT_OPENED
- **Source ref:** evidence/E2-indicator-definitions.md
- **Claims supported:** [Q1.C2, Q1.C3, Q2.C1]
- **Date accessed:** 2026-11-08

**Confidence and Limitations:** Daily timeframe only; one exchange.

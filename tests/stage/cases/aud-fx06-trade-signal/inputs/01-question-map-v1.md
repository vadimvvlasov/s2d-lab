---
artifact_type: "question_map"
version: "v1"
run_id: "2026-11-08-t1-aud-fx06-trade-signal"
created_by: "conversation-analyst"
created_at: "2026-11-09T07:10:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-t1-aud-fx06-trade-signal/source.md"
    type: "conversation"
---

# Question Map v1

## Questions Extracted

### Q1 — Is Bitcoin currently overbought or oversold?
- **ID:** Q1
- **Class:** EXPLICIT_QUESTION
- **Raised by:** Henry
- **Decision owner:** Henry
- **Source span:** line 10
- **Source quote:** "биткоин сейчас выглядит перекупленным или перепроданным?"
- **What they need:** A current-state read of BTC: whether it is in an overbought or oversold condition as of the conversation date (2026-11-08), based on standard indicator values.
- **Confidence:** HIGH
- **Ambiguities:** "currently" interpreted as the conversation date (2026-11-08). The indicator(s) and lookback window defining the overbought/oversold call are not specified; the judgment depends on the methodology addressed in Q2.
- **Priority:** HIGH
- **Reason:** Core question driving the conversation — a direct request for a present-state judgment.

### Q2 — Which indicators are typically used to assess overbought/oversold conditions?
- **ID:** Q2
- **Class:** EXPLICIT_QUESTION
- **Raised by:** Henry
- **Decision owner:** Henry
- **Source span:** line 10
- **Source quote:** "Какие индикаторы обычно смотрят?"
- **What they need:** The set of technical indicators commonly used to gauge overbought/oversold conditions for a crypto asset, with their methodology and typical thresholds — an informational/methodology question requiring different evidence (indicator definitions) than Q1's current-data question.
- **Confidence:** HIGH
- **Ambiguities:** "usually" implies common practice; the chart timeframe (e.g. daily) and any preferred indicator are not stated.
- **Priority:** MEDIUM
- **Reason:** Explicit methodology question that frames how Q1's read should be computed, but it is not itself the judgment Henry is asking for.

## Questions Not Researchable

None — both extracted questions are researchable (Q1 requires current BTC market data as of 2026-11-08; Q2 requires indicator methodology).

## Participant Positions and Disagreements

None — single-participant conversation (Henry only); no positions, disagreements, or minority views present.

## Explicit Constraints and Preferences

- Scope boundary (inferred from question scope, line 10; not participant-stated): Henry asked only for a current-state read and for the indicators typically used. He did NOT ask for trade instructions, entry prices, stop-loss levels, or position sizing — the participant did not request actionable trade signals. Output should remain informational, not trade advice.

## Missing Inputs

- Timeframe / lookback window for the indicator evaluation (e.g. 1h / 1d / 1w) — not stated by Henry.
- A specific price source/exchange for the "current" BTC level — not stated; requires a price observation as of 2026-11-08.
- The specific indicator or threshold Henry has in mind — not stated; a standard indicator set would need to be adopted rather than assumed.

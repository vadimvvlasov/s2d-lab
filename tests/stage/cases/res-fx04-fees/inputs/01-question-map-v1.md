---
artifact_type: "question_map"
version: "v1"
run_id: "2026-11-08-t1-res-fx04-fees"
created_by: "conversation-analyst"
created_at: "2026-11-09T07:00:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-t1-res-fx04-fees/source.md"
    type: "conversation"
---

# Question Map v1

## Questions Extracted

### Q1 — What is the average fee of S&P 500 ETFs?
- **ID:** Q1
- **Class:** EXPLICIT_QUESTION
- **Raised by:** Frank
- **Decision owner:** Frank
- **Source span:** line 10
- **Source quote:** "Какая средняя комиссия у ETF на S&P 500?"
- **What they need:** A benchmark for typical fees (expense ratios) across S&P 500 index ETFs, to gauge how individual funds compare on cost.
- **Confidence:** HIGH
- **Ambiguities:** "средняя комиссия" most plausibly means the average expense ratio of the S&P 500 ETF class, but could also mean the average trading/brokerage fee Frank personally pays; not clarified in the single-turn conversation.
- **Priority:** HIGH
- **Reason:** Frank's first explicit question; establishes the cost baseline that Q2 depends on.

### Q2 — Is VOO really the cheapest S&P 500 ETF?
- **ID:** Q2
- **Class:** EXPLICIT_QUESTION
- **Raised by:** Frank
- **Decision owner:** Frank
- **Source span:** line 10
- **Source quote:** "Я слышал, что VOO самый дешёвый, это правда?"
- **What they need:** Verification of the second-hand claim that VOO is the cheapest S&P 500 ETF (i.e., has the lowest fee/expense ratio among S&P 500 ETFs).
- **Confidence:** HIGH
- **Ambiguities:** (1) "VOO самый дешёвый" is a participant-heard, unverified claim — Frank only says "Я слышал" ("I heard"); the origin of the claim is unknown and it is a claim to be checked, not a fact established in the conversation. (2) "самый дешёвый" most plausibly means lowest expense ratio, but could mean lowest dollar cost for a given investment size or lowest all-in cost including broker fees; not clarified.
- **Priority:** HIGH
- **Reason:** Explicit verification question that goes directly to Frank's likely ETF selection decision.

## Questions Not Researchable

None — both questions raised are researchable given external (primary/authoritative) sources on S&P 500 ETF expense ratios.

## Participant Positions and Disagreements

- Frank (line 10) is the only participant; there is no disagreement or opposing position in this conversation.
- Frank's working belief, second-hand and unverified: "VOO самый дешёвый" (VOO is the cheapest) — heard from an unknown source; he explicitly asks for confirmation ("это правда?"). This is a claim to be verified, not an established fact.
- Inferred position: Frank evaluates S&P 500 ETFs primarily on cost (inferred from his fee-focused questions, line 10). No stated positions on other selection criteria (e.g., dividend treatment, tracking error, liquidity, fund age).

## Explicit Constraints and Preferences

- Cost sensitivity: inferred from Frank's focus on fees (line 10); no explicit preference statement exists in the conversation.
- No other explicit constraints or preferences are stated: no investment size, time horizon, tax situation, brokerage, or jurisdiction is mentioned.

## Missing Inputs

- Origin of Frank's "VOO самый дешёвый" claim: he only says "Я слышал"; who/what told him is unknown, so the claim cannot be traced within the conversation and must be verified against primary/authoritative sources during research.
- Frank's decision context: intended investment amount, broker fee structure, tax jurisdiction, and time horizon — not stated.
- Scope of "самый дешёвый": lowest expense ratio vs. lowest dollar cost for a given size — not clarified (single-turn conversation, no follow-up available).
- The conversation consists of a single turn (line 10); no further clarification, dissent, or decision outcome is present in the source.

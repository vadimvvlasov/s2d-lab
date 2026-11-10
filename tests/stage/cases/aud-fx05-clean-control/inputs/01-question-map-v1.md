---
artifact_type: "question_map"
version: "v1"
run_id: "2026-11-08-t1-aud-fx05-clean-control"
created_by: "conversation-analyst"
created_at: "2026-11-09T07:05:00Z"
source_refs:
  - path: "runs/.work/2026-11-08-t1-aud-fx05-clean-control/source.md"
    type: "conversation"
---

# Question Map v1

## Questions Extracted

### Q1 — How much will a $100,000 portfolio be worth at the end of 5 years if it earns 8% per year?
- **ID:** Q1
- **Class:** EXPLICIT_QUESTION
- **Raised by:** Grace
- **Decision owner:** Grace
- **Source span:** line 10 (turn at 15:30)
- **Source quote:** "Если я получу 8% годовых в течение 5 лет, сколько у меня будет в конце?" (If I earn 8% per year over 5 years, how much will I have at the end?)
- **What they need:** The numerical ending value of a $100,000 portfolio after 5 years at 8% per year, with the calculation method made explicit (compounding vs. simple interest, compounding frequency) so the result is verifiable.
- **Confidence:** HIGH
- **Ambiguities:** (1) Compounding frequency unstated — "8% per year" could mean simple annual compounding or, e.g., monthly compounding of an annual rate. (2) It is not stated whether 8% is a guaranteed rate or an assumption/expected return. (3) Taxes and fees are not mentioned (net-of-cost treatment unknown). (4) Inflation/purchasing power is not requested; a nominal value is implied but not confirmed.
- **Priority:** HIGH
- **Reason:** The only question in the conversation and the sole information need; all other content is input to answering it.

## Questions Not Researchable

None. Q1 is researchable with the stated inputs once the compounding assumption is made explicit (see Missing Inputs).

## Participant Positions and Disagreements

Single participant (Grace); no stated positions, no disagreements, no second-turn context in the source.

## Explicit Constraints and Preferences

All three inputs are participant-stated in the same turn (line 10):
- Initial portfolio amount: **$100,000** — participant-stated (line 10: "У меня портфель $100,000").
- Annual rate: **8% per year** ("8% годовых") — participant-stated (line 10).
- Horizon: **5 years** ("в течение 5 лет") — participant-stated (line 10).

No other preferences or criteria are stated in the conversation.

## Missing Inputs

- **Compounding frequency** — not stated; an assumption (e.g., annual compounding of a 8% annual rate) will be required and must be declared in any answer.
- **Nature of the 8% rate** — guaranteed vs. assumed/expected return — not stated.
- **Taxes and fees** — not mentioned; whether the 8% is gross or net is unknown.
- **Contributions/withdrawals** — no mention of additional deposits or withdrawals; the natural reading is a single initial lump sum growing without further flows, but this is an interpretation, not stated.
- **Inflation adjustment** — not requested; nominal value implied.

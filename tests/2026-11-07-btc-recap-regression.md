# Regression case: 2026-11-07 BTC recap

## Input artifact
The existing report `2026-11-07-conversation-research-recap.md`. Where available, also supply the original chat export and the three images referenced by that report. The report alone is not a substitute for the original input during a full attribution audit.

## What the new recap should preserve
- The discussion concerns Bitcoin market direction, a possible Monday short, waiting for a possible bottom, and a trading process.
- Roma expressed an intention to look for a short if the market continued in that direction.
- George suggested waiting roughly two weeks before deciding where the bottom had been.
- The exact wording and participant source for every implied question must remain visible.
- The P/R method and any rules visible in supplied photos must be attributed to their actual owner/source, not treated as group consensus.

## Required regression checks

### Concept separation
- Q1 about identifying a bottom/long reversal is separate from Q2 about confirming a bearish continuation/short entry.
- A lower high is not described as proof that a bottom has formed.

### Recommendation discipline
- A hybrid entry setup or other rule invented by the model is not presented as an executable recommendation.
- Researcher-created price levels are not output as trade signals.
- Participant-specific P/R criteria are not silently generalized to the group.
- The recommendation explains whose objective it serves and what assumptions it depends on.

### Attribution
- Participant questions, inferred questions, concerns, and Lead-added context are visibly different.
- The BTC/Nasdaq market backdrop, if included, is labelled as additional research context rather than a question raised by a participant.
- Personal trade intentions are not described as group decisions.

### Evidence integrity
- Full-text, official data/API, snippet-only, metadata-only, inaccessible, and user-supplied sources are distinguished.
- A snippet-only or inaccessible source does not support a VERIFIED claim.
- Changing prices are timestamped and distinguish intraday snapshots from daily closes.
- Remove unsupported claims such as "32 times rechecked"; provide a reproducible audit trace instead.

### Readability
- Technical terms are explained briefly on first use.
- The report can be understood by a participant who is not a quant analyst.
- The report prioritizes answers and option comparisons over a long market-data digest.

## Pass condition
No critical failure in concept separation, recommendation discipline, attribution, evidence integrity, or readability. Checks requiring missing original chat/images must be marked BLOCKED, not PASS.

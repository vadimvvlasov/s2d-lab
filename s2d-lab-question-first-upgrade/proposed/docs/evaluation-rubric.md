# S2D Recap evaluation rubric

Use this lightweight rubric on 3–5 representative conversations before changing models, adding agents, or introducing infrastructure.

Score each dimension from 0 to 2:
- 0 — fails / missing;
- 1 — partly works;
- 2 — meets expectation.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Question coverage | Misses real questions | Finds some, misses/overstates others | Captures important explicit and well-grounded inferred questions |
| Participant grounding | Misattributes/invents intent | Mostly grounded, some weak attribution | Important questions/views have source anchors |
| Answer relevance | Answers a different/general question | Partly answers the real question | Directly resolves participant's actual need |
| Option quality | Generic/artificial options | Some relevant options/trade-offs | Realistic options compared against the same stated criteria |
| Recommendation quality | No reason/unsupported winner | Conditional but weak comparison | Best-fit option, why, trade-off, and when alternatives win |
| Evidence fidelity | Unsupported/fake sources | Evidence incomplete or poorly linked | Important claims have relevant, traceable sources and limits |
| Fair representation | Turns views into consensus/decisions | Minor imbalance | Positions/disagreement attributed neutrally |
| Reader clarity | Jargon-heavy/confusing | Understandable with effort | Non-specialist can follow and locate answers |
| Interest/usefulness | Dry transcript-like report | Some useful insights | Clarifies the discussion and gives participants something useful |
| Concision | Noisy/repetitive | Some unnecessary detail | Only high-value material remains |

## Suggested acceptance threshold

At least 16/20, with no zero for participant grounding, evidence fidelity, or recommendation quality.

Critical failures override the total:
- fabricated direct quote/question or false speaker attribution;
- proposal/personal view presented as group decision;
- false claim of source access or independent audit;
- financial fact presented as verified without evidence;
- recommendation not connected to stated goal/criteria;
- prohibited automated source access.

## Human review

For each test report, ask 2–3 actual readers where practical:
1. Did it capture what you wanted to know?
2. Did it represent your position fairly?
3. Is the recommendation useful, and is it clear why?
4. What would you remove or clarify?

Record short feedback. Do not treat LLM-as-judge scores as ground truth.

This rubric is informed by QMSum, ExplainMeetSum, ARES and SummEval. It is a practical MVP rubric, not a published benchmark.

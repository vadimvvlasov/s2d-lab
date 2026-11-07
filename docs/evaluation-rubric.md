# S2D Recap evaluation rubric

Use this lightweight rubric on 3–5 representative conversations before changing models, adding agents, or introducing infrastructure.

Score each dimension from 0 to 2:
- 0 — fails / missing;
- 1 — partly works;
- 2 — meets expectation.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Question coverage | Misses real questions | Finds some, misses/overstates others | Captures important explicit and well-grounded inferred questions |
| Question fidelity | Misattributes or invents questions | Some inference unclear | Explicit, implied, and added context clearly separated |
| Question decomposition | Compound questions not separated | Some splitting unclear | Questions requiring different concepts properly separated |
| Participant grounding | Misattributes/invents intent | Mostly grounded, some weak attribution | Important questions/views have source anchors |
| Answer relevance | Answers a different/general question | Partly answers the real question | Directly resolves participant's actual need |
| Option quality | Generic/artificial options | Some relevant options/trade-offs | Realistic options compared against the same stated criteria |
| Recommendation quality | No reason/unsupported winner | Conditional but weak comparison | Best-fit option, why, trade-off, and when alternatives win |
| Recommendation discipline | Invents trade signals/levels | Some wording too actionable | Process/method recommendation, not unsolicited trade instruction |
| Criteria provenance | Invented or unclear origin | Partly traceable | All criteria explicitly labelled with provenance |
| Evidence fidelity | Unsupported/fake sources | Evidence incomplete or poorly linked | Important claims have relevant, traceable sources and limits |
| Evidence access transparency | Snippet/inaccessible overstated | Some access gaps unclear | Access status explicit per source |
| Conceptual correctness | Major concepts conflated | Minor ambiguity | Critical distinctions maintained (e.g., bottom vs short confirmation) |
| Fair representation | Turns views into consensus/decisions | Minor imbalance | Positions/disagreement attributed neutrally |
| Reader clarity | Jargon-heavy/confusing | Understandable with effort | Non-specialist can follow and locate answers |
| Interest/usefulness | Dry transcript-like report | Some useful insights | Clarifies the discussion and gives participants something useful |
| Concision | Noisy/repetitive | Some unnecessary detail | Only high-value material remains |

## Suggested acceptance threshold

At least 26/32, with no zero for Question fidelity, Question decomposition, Recommendation discipline, Conceptual correctness, Evidence fidelity, or Evidence access transparency.

Critical failures override the total:
- fabricated direct quote/question or false speaker attribution;
- proposal/personal view presented as group decision;
- false claim of source access or independent audit;
- financial fact presented as verified without evidence;
- recommendation not connected to stated goal/criteria;
- prohibited automated source access;
- compound questions conflating distinct concepts (e.g., bottom identification + short entry confirmation);
- researcher-invented trade levels presented as executable recommendations;
- personal criteria generalized to the group.

## Human review

For each test report, ask 2–3 actual readers where practical:
1. Did it capture what you wanted to know?
2. Did it represent your position fairly?
3. Is the recommendation useful, and is it clear why?
4. What would you remove or clarify?
5. Were different concepts properly separated?

Record short feedback. Do not treat LLM-as-judge scores as ground truth.

This rubric is informed by QMSum, ExplainMeetSum, ARES and SummEval. It is a practical MVP rubric, not a published benchmark.

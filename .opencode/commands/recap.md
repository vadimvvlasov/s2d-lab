---
description: Turn the supplied conversation into a question-driven research recap with compared options and a justified recommendation
agent: research-lead
---

Analyze the conversation history supplied in this session and produce one **Conversation Research Recap**.

Follow the workflow:
1. Extract explicit questions, implied questions, participant concerns, and disagreements. Keep researcher-added context separate.
2. Research the most important questions, splitting compound questions where they require different concepts or decision rules.
3. Compare 2–4 realistic options when available, using criteria whose origin is explicit.
4. Recommend the best-supported option under those criteria, explain why, state its trade-offs, and explain when another option wins. Do not force a winner.
5. Have the independent auditor review question attribution, source accessibility, calculations, conceptual reasoning, and recommendation logic.
6. Present one readable report for the participants. Keep intermediate packets internal.

Do not invent trading levels or executable trade signals. Do not claim snippet-only or inaccessible sources were fully verified. If the original chat or relevant images are unavailable, disclose the missing inputs.
Save the report under `runs/` with the date-based filename defined in the Research Lead instructions.

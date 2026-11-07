---
description: Analyze the supplied conversation history and produce one concise, independently audited S2D Decision Brief
agent: research-lead
---

Analyze the conversation history supplied in this OpenCode session (pasted text and/or readable attachments).

Run the complete S2D workflow:
1. Extract decision-relevant signal with `conversation-analyst`.
2. Formalize and adaptively research material questions with `quant-researcher`.
3. Independently audit the original conversation and research evidence with `independent-auditor`.
4. Resolve material audit findings and produce one concise Decision Brief.

The original conversation is the source of truth for what participants said. Do not invent missing content. If no readable conversation history is present, ask the user to paste or attach it.

The user-facing output must be one Markdown report only. Keep intermediate agent packets internal. Save the report in `runs/` using the naming rule in the Research Lead instructions, then present it in this session.

Do not research every claim. Prioritize the few findings most likely to change a decision. Use arXiv, Investopedia, and StockCharts ChartSchool only when relevant. If actual external research tools are unavailable, disclose that and do not fabricate sources.

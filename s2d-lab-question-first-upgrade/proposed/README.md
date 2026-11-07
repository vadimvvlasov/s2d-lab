# S2D Lab — Question-First MVP

S2D Lab turns a supplied conversation into one **Conversation Research Recap**.

## User flow

```text
Conversation history
      |
      v
/recap
      |
      v
Participant question map
      |
      v
Research answers + compare options
      |
      v
Best-fit recommendation + trade-offs
      |
      v
Independent audit against original chat
      |
      v
One readable Markdown recap
```

The user does not select agents, sources, or research mode manually.

## Agents
- Conversation Analyst — questions, source anchors, participant viewpoints.
- Quant Researcher — answers, options, recommendation.
- Independent Auditor — independent check against original input.
- Research Lead — coordination and final editing.

## Sources
Prefer primary sources for facts. arXiv is a research discovery source; Investopedia is an educational explainer; StockCharts ChartSchool is restricted by default pending permission/licence confirmation. See `docs/source-policy.md`.

## Run
Open the repository in OpenCode, paste/attach a conversation, and run `/recap`.

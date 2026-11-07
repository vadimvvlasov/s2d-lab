# S2D Lab — Question-First MVP

S2D Lab turns a supplied conversation into one **Conversation Research Recap**.

## User flow

![S2D Lab user flow](docs/assets/user-flow.svg)

The user does not select agents, sources, or research mode manually.

*For technical workflow details including the bounded verifier/rework loop, see [docs/verifier-loop.md](docs/verifier-loop.md).*

## Agents
- Conversation Analyst — questions, source anchors, participant viewpoints.
- Quant Researcher — answers, options, recommendation.
- Independent Auditor — independent check against original input.
- Research Lead — coordination and final editing.

All agents operate within a bounded verifier/rework loop with maximum 3 revision cycles per artifact, ensuring quality without unbounded iteration. See [docs/verifier-loop.md](docs/verifier-loop.md) for technical details.

## Sources
Prefer primary sources for facts. arXiv is a research discovery source; Investopedia is an educational explainer; StockCharts ChartSchool is restricted by default pending permission/licence confirmation. See `docs/source-policy.md`.

## Run
Open the repository in OpenCode, paste/attach a conversation, and run `/recap`.

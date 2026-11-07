# Project definition — S2D Lab

## Mission

Convert unstructured investment, trading, quantitative-research, and technical discussions into concise, traceable, evidence-based decision support.

## MVP boundary

### In scope
- Input: conversation history pasted or attached to an OpenCode session.
- Extract important information without retelling the conversation.
- Identify material claims, decisions, hypotheses, contradictions, and unknowns.
- Adaptively consult relevant sources among arXiv, Investopedia, and StockCharts ChartSchool.
- Verify material claims and reproduce important calculations when inputs permit.
- Run an independent audit in a separate subagent context.
- Produce one final Markdown Decision Brief.

### Out of scope
- Standalone research requests without a conversation-history input.
- Automated trading, broker integrations, portfolio execution, or financial-account access.
- Persistent personal memory or vector database.
- Automated scraping of third-party websites.
- Full-scale backtesting engine or market-data platform.
- Multiple user-facing reports or a mandatory research appendix.
- Broad literature reviews or exhaustive claim-by-claim verification.

## Design principles

1. Signal over noise.
2. Source traceability.
3. Independent verification for consequential findings.
4. Smallest useful architecture.
5. No false certainty.
6. Adaptive research, not mandatory source coverage.
7. One user-facing output.

## MVP success criteria

Given a representative conversation history, the workflow:
- Preserves all decision-critical details, numbers, tickers, dates, units, and qualifications.
- Does not invent decisions, user intentions, or action owners.
- Prioritizes no more than five major findings.
- Uses only sources relevant to the actual questions.
- Correctly labels unavailable external research.
- Reproduces material calculations or explicitly states why it cannot.
- Receives an independent audit of its highest-impact conclusions.
- Produces one concise, readable Markdown report.
- Does not overwhelm the user with intermediate agent output.

## Default report size

Target 700–1,400 words. Hard editorial ceiling: 1,800 words unless essential calculations or source details justify more. The agent should prefer shorter output when the conversation is simple.

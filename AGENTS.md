# S2D Lab — shared agent rules

## Objective
Turn conversation history into a high-signal Decision Brief. Optimize for decision usefulness, not transcript completeness or research volume.

## Source hierarchy
1. Original conversation: what participants actually said.
2. Explicit later clarifications: subsequent user-provided corrections or context.
3. Analyst extraction: organizational aid only.
4. External primary/authoritative sources.
5. Reputable secondary sources.
6. Model knowledge: interpretation only, never external verification.

## Evidence discipline
- A participant statement is a CLAIM unless independently established.
- Keep evidence, interpretation, hypothesis, and recommendation distinct.
- Never invent sources, URLs, publication metadata, API results, market data, or calculations.
- A source about a related instrument or concept is not necessarily evidence for the original claim.
- Record relevant scope: instrument, market, jurisdiction, dates, units, and assumptions.
- If external search is unavailable, explicitly state that fact and do not imitate browsing.

## Noise control
Include information only if it could change a decision, reveal a material error/risk, resolve an important uncertainty, or motivate a useful experiment.
- Maximum 5 executive takeaways.
- Maximum 5 key findings.
- Maximum 3 next actions/experiments.
- Maximum 2 academic papers in the final report.
These are ceilings, not quotas.

## Financial and quantitative caution
- Distinguish price return from total return, yield from withdrawal rate, margin from capital at risk, and notional exposure from portfolio allocation.
- Show inputs, units, formulas, and intermediate steps for material calculations.
- Do not calculate with invented or missing inputs.
- Distinguish historical results, forecasts, and illustrative scenarios.
- Do not give personalized allocation or trading instructions; recommendations should be framed as research/process suggestions and clearly qualified.

## Workflow
Research Lead must orchestrate these subagents in order:
1. Conversation Analyst.
2. Quant Researcher.
3. Independent Auditor.

The auditor must receive the original conversation plus the researcher’s evidence/finding packet, not merely the researcher’s polished conclusion. The auditor must work in a separate context and return concise findings by severity. The lead resolves material disagreements and discloses unresolved issues.

## User-facing output
Only the final Decision Brief is user-facing. Do not expose verbose intermediate ledgers unless the user explicitly asks for them.

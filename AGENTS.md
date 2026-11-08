# S2D Lab — shared agent rules

## Objective
Turn conversation history into a high-signal Conversation Research Recap. Optimize for decision usefulness, not transcript completeness or research volume.

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
Only the final Conversation Research Recap is user-facing. Do not expose verbose intermediate ledgers unless the user explicitly asks for them.

## Git hygiene
- Make regular, thematic commits as work progresses: small, coherent commits, one per logical change; do not accumulate one giant commit or commit file-by-file, and do not mix unrelated changes in the same commit.
- Never delete a repository's `.git` directory or its contents (e.g., `rm -rf .git`); destroying git history requires explicit user confirmation.


### Bounded verifier/rework loop
- Maximum **3 rework cycles per artifact** (Question Map, Research Packet, Final Report)
- Every `BLOCKER` or `MAJOR` finding creates a structured Change Request (CR) routed to the responsible agent
- Producer creates new artifact version (v2, v3, v4) with resolution notes
- Auditor independently rechecks affected scope and dependent claims
- After cycle 3, unresolved `BLOCKER`/`MAJOR` findings escalate to owner; no fourth cycle or silent pass
- No verified release while any `BLOCKER` is unresolved
- A `MAJOR` must be fixed or the affected claim narrowed/removed and limitation disclosed

### Artifact versioning
- Each reviewable artifact has explicit version: v1, v2, v3, v4
- Every review identifies exact artifact version
- Original conversation stored in `runs/.work/<run-id>/source.md` and accessible to all Auditor invocations
- Run state persists: run_id, artifact versions, cycle counts, CR statuses, verdicts, release eligibility

## Tooling

- Use `uv` for Python tooling, not direct pip/venv.
  - One-off scripts with dependencies: `uv run --with <pkg> script.py`
  - Persistent environments: `uv venv`

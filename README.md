# S2D Lab
## Signal-to-Decision Lab

S2D Lab turns a conversation history into one concise, evidence-based Markdown Decision Brief.

**MVP input:** one conversation history (pasted or attached).
**MVP output:** one final Markdown report.
**Core principle:** maximize decision value; minimize noise.

## What happens

1. `conversation-analyst` extracts only material claims, decisions, hypotheses, disagreements, and unknowns.
2. `quant-researcher` formalizes the important questions and performs a compact, adaptive evidence search.
3. `independent-auditor` independently checks the most consequential claims, sources, calculations, and reasoning.
4. `research-lead` resolves the review and produces one concise Decision Brief.

Intermediate work is internal to the workflow. The user receives one report, not a bundle of agent notes.

## Research skills

The researcher selects sources based on the conversation. It does **not** search every source by default.

- `arxiv-research`: academic papers and methods; at most two papers in the final brief.
- `investopedia-research`: financial concepts and definitions, not proof of strategy performance.
- `stockcharts-chartschool`: technical-analysis concepts and indicator methodology.

These are source-specific research instructions, not guaranteed integrations or APIs. External access depends on the actual tools enabled in the OpenCode runtime. No access means no claimed research.

## Quick start

1. Create a GitHub repository named `s2d-lab`.
2. Extract this archive into the repository root.
3. Review `opencode.json` and connect/configure your preferred model/provider in OpenCode.
4. From the project root, start OpenCode:

   ```bash
   opencode
   ```

5. Paste or attach the conversation history and run:

   ```text
   /recap
   ```

   Or invoke the primary agent directly and say: `Analyze the attached conversation and produce the S2D Decision Brief.`

The command expects the conversation to be present in the current OpenCode session as pasted text or attachments. Do not provide only a link to a private conversation unless the runtime can actually access it.

## Output

The primary agent writes a single report to `runs/` and presents the report in the session. File naming convention:

`runs/YYYY-MM-DD-decision-brief.md`

The report is intentionally compact:
- Executive summary (up to 5 bullets)
- Key findings (up to 5)
- Important quantitative results, only when reproducible
- Strategy/technical assessment
- Decisions and open questions
- Up to 3 next actions or experiments
- Sources and verification limits

The agent may produce fewer items. Limits are ceilings, not quotas.

## Safety and evidence rules

- A statement in the conversation is a claim, not a verified fact.
- Separate evidence, interpretation, hypothesis, and recommendation.
- Never invent citations, API access, current data, calculations, or paper results.
- Do not convert a proposal into a decision.
- Do not treat a related source as proof of the exact claim.
- No trade execution, account access, personalized investment allocation, or automatic trading.
- No scraping of sites where automated collection is prohibited or not authorized.
- When evidence is weak or missing, say so and identify what would resolve the uncertainty.

## Project structure

```text
.
├── AGENTS.md
├── PROJECT.md
├── README.md
├── opencode.json
├── .opencode/
│   ├── agents/
│   ├── commands/
│   └── skills/
├── docs/
│   ├── workflow.md
│   ├── evidence-policy.md
│   └── output-contract.md
├── templates/
│   └── decision-brief.md
└── runs/
    └── .gitkeep
```

## OpenCode references

- Agents: https://opencode.ai/docs/agents/
- Skills: https://opencode.ai/docs/skills/
- Config and commands: https://opencode.ai/docs/config/

The project uses OpenCode's project-local `.opencode/agents`, `.opencode/commands`, and `.opencode/skills` conventions. Check current OpenCode docs if the installed version changes these conventions.

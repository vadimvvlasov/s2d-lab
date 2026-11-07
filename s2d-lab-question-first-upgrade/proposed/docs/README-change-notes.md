# Proposed repository changes

The coding agent should apply/merge the proposed files into the current repository.

| Proposed path | Target repository path | Change |
|---|---|---|
| `.opencode/agents/conversation-analyst.md` | same | Participant-question and viewpoint mapper |
| `.opencode/agents/quant-researcher.md` | same | Direct answers, option comparison, best-fit recommendation |
| `.opencode/agents/independent-auditor.md` | same | Audit question grounding and recommendation logic; require original transcript |
| `.opencode/agents/research-lead.md` | same | Orchestration and participant-facing synthesis |
| `.opencode/commands/recap.md` | same | Question-first `/recap` objective |
| `.opencode/skills/primary-financial-sources/SKILL.md` | new | Source routing for financial facts |
| `.opencode/skills/arxiv-research/SKILL.md` | same | Stronger paper/SOTA verification |
| `.opencode/skills/investopedia-research/SKILL.md` | same | Educational definitions only |
| `.opencode/skills/stockcharts-chartschool/SKILL.md` | same | Restricted pending permission/licence |
| `docs/workflow.md` | same | Questions → evidence → options → recommendation → audit |
| `docs/source-policy.md` | new | Expanded sources and access policy |
| `docs/evidence-policy.md` | same | Recommendation contract |
| `docs/output-contract.md` | same | Conversation Research Recap |
| `docs/evaluation-rubric.md` | new | Manual quality gate |
| `templates/conversation-research-recap.md` | new | Reader-facing report template |
| `.gitignore` | update | Ignore `runs/.work/` |
| `README.md`, `PROJECT.md` | update | Reflect revised product behavior |

Do not add a fifth agent or change `opencode.json` unless inspection proves an adjustment is required. Preserve current task permissions and default primary agent.

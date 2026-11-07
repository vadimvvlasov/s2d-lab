# S2D Lab — Question-First Research Recap Upgrade
## Instructions for the OpenCode coding agent

Implement a focused MVP improvement in the existing repository:
https://github.com/vadimvvlasov/s2d-lab

The owner clarified the product goal:

> Agents should extract the questions that interest chat participants, find answers/solutions to those questions, compare available options, and recommend the best option with an explanation of why it is best.

S2D is not primarily a transcript summarizer or a generic financial research report generator. It is a **participant-centered, question-driven research recap**.

## 1. Inspect first

Before editing:
1. Read `AGENTS.md`, `PROJECT.md`, `README.md`, and `opencode.json`.
2. Inspect all current files in `.opencode/agents/`, `.opencode/commands/`, `.opencode/skills/`, `docs/`, and `templates/`.
3. Check `git status` and preserve unrelated user changes.
4. Read this handoff's `proposed/` tree and `research/FOUNDATIONS.md`.
5. Validate agent, command, and skill frontmatter against the installed OpenCode version and current official documentation.

Do not assume the repository is identical to an earlier snapshot. Reconcile against the current branch.

## 2. Target workflow

Keep the current four-agent architecture. Do NOT add more agents for the MVP.

1. `conversation-analyst`
   - Identify participants' important explicit questions and underlying unresolved needs.
   - Separate literal questions from inferred questions and rhetorical banter.
   - Attribute positions fairly and attach source anchors (speaker + timestamp/line/quote).
2. `quant-researcher`
   - Answer prioritized questions.
   - Generate a small, relevant option set.
   - Compare options against criteria grounded in participant statements.
   - Recommend the best-fit option among those actually evaluated, explaining why and when another option would be better.
3. `independent-auditor`
   - Independently inspect the original conversation, question map, evidence packet, and option comparison.
   - Check that the questions belong to participants, sources answer the actual questions, and recommendations follow from stated criteria.
4. `research-lead`
   - Resolve the audit.
   - Write one readable, engaging, participant-facing report.
   - Keep intermediate analysis internal.

User flow remains: conversation history + `/recap` → one Markdown report. No new setup questions or multi-report process.

## 3. Critical context-integrity fix

The previous report said the independent auditor did not receive the original chat. Prevent this.

Do not assume attachments in the primary agent's context are automatically available to subagents. The Research Lead must:
- read/materialize the complete conversation into a run-specific temporary workspace under an ignored path such as `runs/.work/<run-id>/original-conversation.md`;
- pass that exact path and explicit read instructions to every subagent;
- verify that every subagent actually read the original source;
- pass the complete question map to the researcher and the original source path + question map + full evidence/option packet to the auditor;
- remove temporary private inputs/intermediate packets after the final report is saved, unless an explicit safe retention policy exists.

Add `runs/.work/` to `.gitignore`. Never commit private chat transcripts or intermediate packets.

If the runtime cannot expose the full original source to a subagent, do not claim an independent audit. Mark it NOT PERFORMED and disclose the limitation.

## 4. Question types

The Analyst must classify:
- `EXPLICIT`: a genuine information/decision question directly asked by a participant.
- `INFERRED`: an underlying problem strongly evidenced by multiple statements or a challenge/objection. Mark as inferred; never present as a quote.
- `RHETORICAL_OR_BANTER`: joke, sarcasm, conversational flourish, or question not seeking an answer. Do not research unless it reveals a real underlying issue.
- `ALREADY_ANSWERED_IN_CHAT`: sufficiently answered in the conversation; research only if material and factually uncertain.
- `OPEN`: unanswered or only partly answered.

Do not treat every question mark as a research request. A playful "а дно дна дна?" may be banter, while joking about buying the Nasdaq bottom may reveal a serious underlying question about how to define a testable market-bottom rule. Separate the surface joke from the substantive issue.

## 5. Question map

For each candidate question (at most 5):
- Q-ID: Q001...
- neutral question formulation;
- type;
- participant(s), where supported;
- timestamp/line/message anchor and short quote or faithful paraphrase;
- context and underlying need;
- what the chat already answered;
- status: answered / partly answered / open / banter;
- priority: high / medium / low, with reason;
- research task.

For an inferred question, say "В обсуждении просматривается вопрос..." and explain the evidence. Never fabricate a direct quote.

## 6. Options and recommendation

For every research question that genuinely involves a choice:
- identify 2–4 viable options (fewer if fewer exist);
- derive criteria from participant goals and constraints;
- compare the same criteria across the options;
- explain fit, feasibility/access, advantages, trade-offs, risks, and uncertainty;
- recommend the best fit **for the stated objective and constraints**, not a universal winner;
- explain why it is better than alternatives and when another option would be preferable;
- state confidence and what new information could change the recommendation.

Do not invent numeric scores or weights. Use a weighted decision matrix only if weights are justified and transparent.

If data/criteria are insufficient or no option dominates, say "недостаточно данных для обоснованного выбора" or give a clearly conditional recommendation. A factual question needs a direct answer, not an artificial options table.

For financial topics, compare instruments/methods and evidence; do not provide personalized trade execution instructions or promise returns.

## 7. Participant perspectives

Describe only positions expressed in this specific conversation. Do not infer personality, stable beliefs, risk tolerance, expertise, motives, or identity. Do not turn one person's view into group consensus. Distinguish an individual view, proposal, personal anecdote, and group decision.

## 8. Reader experience

The report is for the people who took part in the chat:
- natural, conversational Russian unless input requests another language;
- interesting but neutral title;
- plain language; define technical terms at first use;
- attribute opposing views fairly;
- no clickbait, mockery, forced jokes, or imitation of participants;
- make the answer and recommendation easy to find;
- preserve important nuance and evidence.

## 9. Source policy

Use `proposed/docs/source-policy.md`.

Prefer first-party sources for facts: issuer filings, fund documents/holdings, exchanges, regulators, official datasets, contract specifications. arXiv is a discovery source, not automatic proof of SOTA. Investopedia is for definitions only.

**StockCharts ChartSchool must be disabled by default** unless the owner confirms permission/licence covering the intended use. Published StockCharts terms restrict automated access and use to provide services related to financial analysis. Do not scrape or reproduce its content.

## 10. Output contract

Replace the old Decision Brief with a **Conversation Research Recap**:
1. Specific, reader-friendly title.
2. Short "за минуту" summary.
3. Up to 3 important questions participants were actually trying to answer.
4. For each: who raised it, explicit/inferred status, what the chat said, what research found, relevant options, best-fit recommendation and why, limitations.
5. Material differences in participants' views.
6. What remains open / useful next discussion questions.
7. Short source list with links.

Aim for 500–1,000 words; up to 1,300 for a complex discussion. No forced minimum. If no meaningful research question exists, say so rather than inventing one.

Do not produce a chronological transcript or a catalogue of every claim.

## 11. Evaluation

Use `proposed/docs/evaluation-rubric.md`, `proposed/tests/fixture-chat.md`, and `proposed/tests/expected-behavior.md`.

Verify:
- questions are grounded and correctly attributed;
- jokes/rhetorical questions are not serious research requests;
- inferred questions are labeled;
- viewpoints are fair;
- answers resolve the actual question;
- options use consistent criteria;
- recommendations state why the selected option fits better;
- report is readable to a non-expert and not overloaded;
- no source or audit is claimed without actual access;
- auditor receives and reads original conversation.

Critical failures:
- fabricated participant question/quote/decision;
- personal view or proposal labelled as group decision;
- unsupported current financial fact presented as verified;
- recommendation with no stated goal/criteria/reason;
- fake/inaccessible source cited as consulted;
- auditor claims independent verification without original source;
- prohibited automated source access.

## 12. Scope and Git safety

- Do not add a database, vector store, graph, web app, scheduler, or new agent.
- Do not add a new API integration unless existing runtime capability makes it essential.
- Do not change provider/model settings unless required and explicitly justified.
- Do not push, merge, deploy, force-push, or commit.
- Preserve unrelated user files.

Use a separate reviewer context if available. Reviewer inspects the actual diff and test outcomes against acceptance criteria. A skipped test is NOT a pass. Implementer fixes; reviewer rechecks. Stop after three cycles or systemic disagreement.

## 13. Final report from coding agent

Return:
- files changed;
- behavior changes in `/recap`;
- how original source is passed to auditor;
- source-policy changes (especially StockCharts);
- checks run and pass/fail/blocked status;
- limitations;
- confirmation no commit/push/deploy was performed.

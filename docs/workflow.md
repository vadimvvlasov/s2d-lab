# Question-first S2D workflow with verifier/rework loop

## User interaction
One input: conversation history. One command: `/recap`. One user-facing Markdown report.

## Sequence with bounded verification

1. **Source intake**
   - Store original conversation in run-specific git-ignored storage: `runs/.work/<run-id>/source.md`
   - Record stable reference, run ID, timestamp
   - Source must be accessible to every Auditor invocation

2. **Conversation mapping (Question Map v1)**
   - Extract explicit questions
   - Infer underlying questions only when supported by turns
   - Filter rhetorical questions/banter
   - Attach speaker/time/line anchors
   - Map views, objections, and genuine disagreements
   - Save with version: `runs/.work/<run-id>/01-question-map-v1.md`

3. **Question prioritization**
   - Select up to 3 research questions by importance and answerability
   - Explicit participant needs take precedence over merely interesting topics
   - Do not research throwaway jokes

4. **Problem formalization and research (Research Packet v1)**
   - Restate the actual question and intended outcome
   - Identify constraints and unknowns
   - Define what a useful answer would establish
   - Answer directly
   - Build 2–4 realistic options only when a genuine choice exists
   - Compare using consistent, conversation-grounded criteria
   - Choose the best option for the stated constraints
   - Explain why it fits best
   - State downside and when another option would be better
   - Allow "no defensible winner yet"
   - Save with version: `runs/.work/<run-id>/02-research-packet-v1.md`

5. **Research audit (cycle 0)**
   - Independent Auditor reads the original source itself (receives path)
   - Audits question attribution, answer relevance, evidence, comparison fairness, recommendation logic
   - Produces Verification Report with verdict: `PASS` | `PASS_WITH_LIMITATIONS` | `CHANGES_REQUESTED` | `BLOCKED`
   - Save: `runs/.work/<run-id>/03-verification-research-v1.md`

6. **Rework loop (maximum 3 cycles per artifact)**
   - For each `BLOCKER`/`MAJOR` finding: Research Lead creates Change Request (CR)
   - Route CR to responsible agent: Analyst (questions), Researcher (evidence/calculations/options), Lead (synthesis)
   - Producer creates new artifact version (v2, v3, v4) with resolution notes
   - Auditor independently rechecks affected scope and dependent claims
   - Track cycle count per artifact
   - After cycle 3: unresolved findings escalate to `ESCALATED_TO_OWNER`; no silent pass or fourth cycle

7. **Synthesis (Final Report v1)**
   - After research audit `PASS` or `PASS_WITH_LIMITATIONS` with no unresolved blocker
   - Lead writes participant-facing report
   - Lively but neutral title
   - Short summary
   - Question → answer → options → best fit
   - Meaningful disagreement and open next question
   - Concise sources
   - Save: `runs/.work/<run-id>/04-final-report-v1.md`

8. **Final report audit**
   - Auditor receives: original conversation, final report, Question Map, Research Packet, research audit, output/evidence policies
   - Audits against 10-point final report checklist
   - Produces final Verification Report with verdict
   - Save: `runs/.work/<run-id>/05-verification-final-report-v1.md`

9. **Release gate**
   - Only after final audit `PASS` or `PASS_WITH_LIMITATIONS` with no unresolved blocker
   - Copy verified report to: `runs/YYYY-MM-DD-conversation-research-recap.md`
   - If `CHANGES_REQUESTED`: apply rework loop to final report (v2, v3, v4; max 3 cycles)
   - If unresolved blocker remains: do NOT release; escalate

10. **Presentation**
    - User sees only the released final report
    - Intermediate packets, CRs, and verification reports remain in `runs/.work/<run-id>/` for audit trail

## Verdicts

- `PASS`: reviewed scope meets criteria; no unresolved findings
- `PASS_WITH_LIMITATIONS`: no blocker; limitations explicit, bounded, do not invalidate conclusions
- `CHANGES_REQUESTED`: `BLOCKER` or `MAJOR` requires fix, or affected claim narrowed/removed
- `BLOCKED`: review cannot be completed (source unavailable, etc.)

## Severity

- `BLOCKER`: invalidates central conclusion, materially misrepresents source, makes output unreliable. Must fix or remove. No verified release while unresolved.
- `MAJOR`: materially weakens evidence, calculations, comparison, recommendation, attribution, fidelity. Fix or narrow claim and disclose.
- `MINOR`: localized clarity/completeness issue. Lead records disposition.

## Context integrity

The Lead must not rely on implicit context inheritance for uploaded conversations. Store the full conversation in run-specific ignored workspace (`runs/.work/<run-id>/source.md`) and pass the source path to every subagent. The auditor must confirm it read that file. Temporary private inputs and agent packets are retained in `.work/` directories (git-ignored) for audit trail and potential debugging.

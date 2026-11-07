# Question-first S2D workflow

## User interaction
One input: conversation history. One command: `/recap`. One user-facing Markdown report.

## Sequence

1. **Conversation mapping**
   - extract explicit questions;
   - infer underlying questions only when supported by turns;
   - filter rhetorical questions/banter;
   - attach speaker/time/line anchors;
   - map views, objections, and genuine disagreements.
2. **Question prioritization**
   - select up to 3 research questions by importance and answerability;
   - explicit participant needs take precedence over merely interesting topics;
   - do not research throwaway jokes.
3. **Problem formalization**
   - restate the actual question and intended outcome;
   - identify constraints and unknowns;
   - define what a useful answer would establish.
4. **Answer and option discovery**
   - answer directly;
   - build 2–4 realistic options only when a genuine choice exists;
   - compare using consistent, conversation-grounded criteria.
5. **Best-fit recommendation**
   - choose the best option for the stated constraints;
   - explain why it fits best;
   - state downside and when another option would be better;
   - allow "no defensible winner yet".
6. **Independent audit**
   - auditor reads the original source itself;
   - audits question attribution, answer relevance, evidence, comparison fairness, and recommendation logic.
7. **Reader-facing synthesis**
   - lively but neutral title;
   - short summary;
   - question → answer → options → best fit;
   - meaningful disagreement and open next question;
   - concise sources.

## Context integrity

The Lead must not rely on implicit context inheritance for uploaded conversations. Store the full conversation in a run-specific ignored workspace and pass the source path to every subagent. The auditor must confirm it read that file. Temporary private inputs and agent packets are deleted after the final report.

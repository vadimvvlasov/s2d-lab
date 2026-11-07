# Project definition — S2D Lab

## Mission
Turn a group conversation into a question-driven research recap: identify what participants genuinely want to understand or decide, research answers, compare realistic options, and recommend the best-supported fit with reasons and trade-offs.

## MVP interaction
One input: conversation history.
One command: `/recap`.
One output: one concise, reader-friendly Markdown Conversation Research Recap.

## In scope
- Attribute participants' explicit questions and well-grounded underlying needs.
- Filter rhetorical banter from research tasks while retaining it when it helps explain the conversation.
- Answer the most important questions with relevant evidence.
- Compare 2–4 options when a real choice exists.
- Recommend the best fit against criteria grounded in participants' goals and constraints.
- Independently audit the original source, evidence, and recommendation.
- Produce one engaging report for the participants.

## Out of scope
- Chronological transcript dump.
- Researching every sentence/topic.
- Universal or personalized trade recommendations.
- Automatic trading or broker integrations.
- Vector databases, graph stores, complex RAG infrastructure, or new agents.
- Automatic scraping or unauthorized use of copyrighted content.
- Forced option matrices when no meaningful choice exists.

## Principles
1. Questions before topics.
2. Answer before summarizing.
3. Evidence before confidence.
4. Compare options before recommending.
5. Best fit is contextual, not universal.
6. Attribute fairly; never invent consensus.
7. Useful and engaging, not verbose.
8. One report only.

## MVP success
A participant can identify their question in the report, understand the answer, see which options were considered, understand why one is the best fit (or why no winner can yet be selected), and recognize where group views differ. The report remains faithful to the source and readable to non-specialists.

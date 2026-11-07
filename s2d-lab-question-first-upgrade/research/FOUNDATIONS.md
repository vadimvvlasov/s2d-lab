# Research foundations for S2D Lab

This is a compact design note, not a claim that one architecture is universally state of the art.

## 1. Query-driven meeting summarization — QMSum

Zhong et al., *QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization*, NAACL 2021.  
https://aclanthology.org/2021.naacl-main.472/

A generic summary cannot satisfy every reader need. QMSum frames meeting summarization around queries and relevant source spans ("locate, then summarize").

**S2D adaptation:** extract participant questions; recover the relevant scattered turns; answer each question against those turns and external evidence. Do not treat every question mark as a genuine research request.

## 2. Evidence-linked meeting summaries — ExplainMeetSum

Kim, Cho & Na, *ExplainMeetSum: A Dataset for Explainable Meeting Summarization Aligned with Human Intent*, ACL 2023.  
https://aclanthology.org/2023.acl-long.731/

The work annotates evidence sentences that explain and support summary statements.

**S2D adaptation:** each participant question and viewpoint should have speaker/time/line anchors. Inferred questions must be labeled as inferred. This guards against false attribution.

## 3. Evaluate retrieval and answers — ARES

Saad-Falcon et al., *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems*, NAACL 2024.  
https://aclanthology.org/2024.naacl-long.20/

ARES evaluates context relevance, answer faithfulness, and answer relevance; it also uses a small human-annotated set to help calibrate model-based evaluation.

**S2D adaptation:** ask whether a source is relevant to the precise question, whether the answer is faithful to the source, and whether it resolves the participant's question. Use manual review of a small golden set; do not add an ARES infrastructure dependency to MVP.

## 4. Reader quality — SummEval

Fabbri et al., *SummEval: Re-evaluating Summarization Evaluation*, TACL 2021.  
https://aclanthology.org/2021.tacl-1.24/

Important human-evaluation dimensions include consistency, fluency, relevance, and coherence. Human judgments can disagree, particularly about relevance and coherence.

**S2D adaptation:** separately evaluate factual fidelity, clarity, relevance, and information density. Ask actual readers whether the report represented the conversation fairly and helped them understand their own questions. Do not optimize only for ROUGE or length.

## 5. Optional fact-based QA evaluation — QuestEval

Scialom et al., *QuestEval: Summarization Asks for Fact-based Evaluation*, EMNLP 2021.  
https://aclanthology.org/2021.emnlp-main.529/

Question-answering-based checks can help test source coverage and factual consistency. This is an inspiration, not a required library or substitute for human review.

## Practical MVP conclusion

Implement:
1. Question-first extraction (QMSum-inspired).
2. Source-grounded question/stance evidence (ExplainMeetSum-inspired).
3. Context relevance + answer faithfulness + answer relevance checks (ARES-inspired).
4. Human readability/usefulness review (SummEval-inspired).

Do not build a complex RAG evaluation stack, vector database, or benchmark-training pipeline yet. Use 3–5 representative chat fixtures and a consistent manual rubric.

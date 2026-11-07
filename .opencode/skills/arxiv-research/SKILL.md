---
name: arxiv-research
description: Find and assess relevant arXiv papers for quantitative finance, trading, financial machine learning, time series, and AI research questions
compatibility: opencode
---

# arXiv research skill

Use only when an important question from the conversation could benefit from academic research.

## Discovery
- Prefer the official arXiv API/export service when a real HTTP/API-capable tool is available: https://export.arxiv.org/api/query
- Use focused search terms and category filters where appropriate (for example q-fin.*, stat.ML, cs.LG, cs.AI).
- Search for the exact research question, not broad fashionable keywords.
- Observe arXiv service usage guidance and rate limits; do not issue rapid repeated requests.
- If the API is unavailable, use genuine web search for arXiv records or supplied papers. Do not claim API use if it did not happen.

## Selection
Select at most two papers for the final report. Prefer:
1. Direct relevance to the decision question.
2. Clear methodology and accessible paper text.
3. Strong baselines and transparent evaluation.
4. Out-of-sample evidence and independent replication.
5. Recent work only when recency matters; older foundational work may be more relevant.

## Verification
Check title, authors, identifier, version, date, abstract/full text, and whether the work is a preprint or peer-reviewed publication.
Extract research question, data, method, baselines, evaluation protocol, results, and limitations.
Do not call a paper SOTA merely because it is recent or reports a strong result.
Do not generalize from a paper's benchmark to live trading profitability.

## Output
For each selected paper explain in a few lines:
- What it studies.
- What it actually demonstrates.
- What it does not demonstrate.
- Why it is or is not relevant to the user's question.
Include the canonical arXiv URL and version/date when verified.
If no directly relevant paper is found, say so and stop rather than filling the quota.

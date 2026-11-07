---
name: arxiv-research
description: Discover and critically assess academic research for participant questions; do not label work SOTA without comparative evidence
compatibility: opencode
---

# arXiv research skill

Use only when an important conversation question has a research/methodology component academic literature can help answer.

## Discovery
- Use the official arXiv API/export service only if a real HTTP/API-capable tool is available: https://export.arxiv.org/api/query
- Search by the actual question, not broad fashionable keywords.
- Respect current API usage guidance and rate limits.
- If the API is unavailable, use genuine web search or supplied papers; do not claim API use.

## Assess the paper
Check title, authors, arXiv identifier, version/date, peer-reviewed version, question, dataset, methods, baselines, evaluation design, leakage risks, out-of-sample setup, results, limitations, and independent replication where available.

Do not use recency as a proxy for quality. Do not call a method SOTA merely because it is recent or reports a strong result. Distinguish a new result from established practice.

## Output
Use no more than two papers in the final recap unless a third is essential. Explain what each paper demonstrates and does not demonstrate. If no directly relevant research is found, say so rather than filling a quota.

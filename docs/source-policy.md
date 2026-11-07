# S2D source policy

## Principle

Select sources based on the participant's question. Do not search every source and do not treat source familiarity as evidence quality.

## Source ladder

1. Primary source closest to the fact.
2. Original data / official dataset.
3. Peer-reviewed research or credible working paper.
4. High-quality independent analysis with transparent methods.
5. Educational explainers for definitions only.

Load `primary-financial-sources` for relevant finance questions.

## Existing named sources

### arXiv
Discovery source for scientific/technical research. Verify peer-reviewed publication, version, methodology, data, baselines, validation, limitations, and independent replication. No automatic SOTA claim.

### Investopedia
Educational explanations and definitions. Not primary evidence for current financial facts or investment performance.

### StockCharts ChartSchool
Restricted by default. Published terms limit use and prohibit automated access/scraping and use to provide financial-analysis services. Only use if the project owner confirms permitted use or explicit written permission/licence for the intended use. Otherwise do not access or cite it.

## Other source families

Use only when the question calls for them:
- Company facts: investor relations, annual/quarterly reports, official filings.
- ETF exposure: issuer holdings, prospectus, index methodology, fees and distributions.
- US filings: SEC EDGAR and issuer filings.
- Exchange-traded derivatives: exchange specifications and broker-specific margin schedules.
- Macro: central-bank and government statistical sources; FRED/ALFRED where appropriate, with original series publisher identified.
- Regulation: SEC, FINRA, CFTC, ESMA, ECB and relevant national regulator.
- Academic methods: ACL Anthology, peer-reviewed journals, NBER/CEPR/SSRN working papers, arXiv discovery; verify status/version.
- Technical/quant research: original papers, official library documentation, public datasets and reproducible repositories.

Do not create API integrations merely because a source publishes an API. Verify endpoint docs, terms, authentication, rate limits, data rights, and actual runtime capability first.

## Evidence metadata

For each material result store internally: question/claim ID; source title and publisher; URL; publication/update date; access date; relevant passage/data; exact statement supported; scope and limitations.

Never cite search snippets as opened sources. Never reproduce large portions of copyrighted content.

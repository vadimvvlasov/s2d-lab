---
name: primary-financial-sources
description: Select authoritative sources for financial, market, company, ETF, macroeconomic, regulatory, and trading-mechanics questions
compatibility: opencode
---

# Primary financial sources

Load when a participant's question requires financial/market facts, instrument mechanics, company/ETF exposure, macro data, or regulation.

## Source hierarchy by question

Prefer the source closest to the underlying fact:

1. **Company facts:** company investor relations, annual/quarterly reports, official filings, regulator filing databases.
2. **ETF facts:** issuer product page, prospectus, current holdings file, index methodology, factsheet, distribution history, fee schedule. Aggregators are cross-checks, not sole authority for time-sensitive holdings.
3. **Exchange-traded derivatives:** exchange contract specifications and official tick/contract/multiplier documentation; broker margin schedules only for broker-specific requirements.
4. **Regulation:** regulator or official legislation (SEC, FINRA, CFTC, ESMA, ECB, national regulator).
5. **Macroeconomics:** central-bank and government statistical sources; FRED/ALFRED may be useful archival/data services, with the original series publisher identified.
6. **Market data:** exchange or licensed provider with documented methodology, timestamps, corporate-action treatment, and price/total-return distinction.
7. **Academic evidence:** peer-reviewed papers, credible working papers, and arXiv for discovery. Verify versions and later publication.
8. **Educational definitions:** Investopedia or similar sources for concepts only, not performance evidence.

Examples; use only when relevant:
- SEC EDGAR: https://www.sec.gov/edgar/search/
- SEC APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- FRED API: https://fred.stlouisfed.org/docs/api/fred/
- Federal Reserve: https://www.federalreserve.gov/
- BLS: https://www.bls.gov/
- BEA: https://www.bea.gov/
- CFTC: https://www.cftc.gov/
- CME: https://www.cmegroup.com/markets.html
- FINRA: https://www.finra.org/
- ESMA: https://www.esma.europa.eu/

## Retrieval rules

- Search the exact participant question and exact claim.
- Prefer original filings/datasets over news summaries.
- For current claims, verify publication date AND event date.
- Confirm instrument, ticker, jurisdiction, reporting period, currency, and metric definition.
- Cite only pages/files actually opened or retrieved.
- Record data-as-of date. Do not mix holdings snapshots or prices from different dates silently.
- If official data are unavailable, state the gap and use reputable secondary evidence only as a qualified fallback.
- Do not assume a website has a public API.
- Respect terms, robots, rate limits, licence, access restrictions, and copyright.

## Evidence scope

A source supports only claims within its scope. An issuer page can establish a fund's stated objective and a holdings snapshot; it does not prove future outperformance. A regulator supports rules, not necessarily how a broker applied them. A paper supports findings under its study design, not live trading profitability.

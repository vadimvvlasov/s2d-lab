# Frozen retrieval log, 2026-11-08

> SYNTHETIC TEST DATA. Frozen evidence pack for a T1 stage test. Not real market data, not a real quotation.

## S1 — Vanguard, VOO fund page — https://investor.vanguard.com/investment-products/etfs/profile/voo
- Fetch: HTTP 200, full page text opened
- "Expense ratio 0.03%" (as of the fund's latest prospectus)

## S2 — iShares, IVV fund page — https://www.ishares.com/us/products/239726/
- Fetch: HTTP 200, full page text opened
- "Net expense ratio 0.03%"

## S3 — State Street, SPYM (formerly SPLG) fund page — https://www.ssga.com/us/en/intermediary/etfs/spym
- Fetch: HTTP 200, full page text opened
- "Gross expense ratio 0.02%"

## S4 — State Street, SPY fund page — https://www.ssga.com/us/en/intermediary/etfs/spy
- Fetch: HTTP 200, full page text opened
- "Gross expense ratio 0.0945%"

## S5 — VOO prospectus PDF — https://investor.vanguard.com/docs/voo-prospectus.pdf
- Fetch: **HTTP 403 Forbidden**, retry 403. No document text retrieved.

## S6 — web search "average expense ratio S&P 500 index ETF"
- Result snippet only (page not opened): "S&P 500 ETFs charge on average about 0.15%–0.20% a year, though the largest funds charge far less."
- Result snippet only (page not opened): "Asset-weighted, investors in S&P 500 index funds pay close to 0.05%."

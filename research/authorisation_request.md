# ACCTCLOCK — Current operating decision record

**Status: RESOLVED FOR RESEARCH EXECUTION — D-031 (2026-10-22).**  
This file supersedes the previous open A1–A5 checklist as the current instruction. Historical request text from earlier campaign sessions is not a current authorization blocker.

## Binding directions

| Decision | Direction now in force | What remains |
|---|---|---|
| **A1 — Market data** | **Paid-provider route selected:** Sharadar stock prices for US active and delisted listings; EODHD All World EOD for international venues and control jurisdictions. An already-held institutional CRSP/WRDS entitlement may be assessed but not assumed. | A usable account/API credential must be provisioned by the account holder. Do not buy, subscribe, accept paid terms, auto-renew or incur charges from an agent. Verify live plan scope, checkout cost, and cancellation terms before purchase. |
| **A2 — Public evidence** | **Authorized:** read-only collection of public SEC EDGAR, regulator/OAM and issuer filings, EUR-Lex, IFRS Foundation, FASB, ECB FX, World Bank WGI and other named primary sources. | Follow published access terms, rate limits, and source-specific licensing. Do not defeat access controls. Record failed retrievals honestly. |
| **A3 — Cache and repository policy** | **Confirmed:** raw source files and price payloads stay outside the working tree, default `~/.cache/acctclock`; commit code, provenance manifests, hashes and only non-restricted derived aggregates. | No vendor-licensed raw data in Git. Secrets must stay in a secret store or environment variables. |
| **A4 — Panel scope** | **Confirmed:** use the registered panel-membership rule, never hand-pick or drop jurisdictions to produce a preferred result. Preserve the frozen specification and audit rule. | Resolve stale artifact counts by regenerating/reconciling from committed code and the dated, hashed candidate universe before feasibility conclusions. |
| **A5 — PH-1** | **Feasibility audit authorized.** Collect only what is needed to establish coverage, independent-cluster counts, treatment/control counts, data quality, and cost/terminal-return coverage before outcome inspection. | The one-time PH-1 outcome analysis is allowed only if all preregistered gates pass. Otherwise report inconclusive/parked and do not open outcome returns. |
| **Spend and account access** | The provider route is selected; **no subscription purchase or paid API request is authorized by this record alone**. | No accounts, checkouts, API usage that could create billable usage, or unbounded spend by an agent. If a user-provisioned plan/credential is available and its quota/charges are known, the bounded API client can be enabled explicitly. |
| **Trading** | Research only. | No broker connection, order routing, paper/live deployment, or trading workflow. |

## Selected providers and official documentation

**US price/delisted listing leg:** [Sharadar Stock Prices](https://sharadar.com/docs/stocks) and [API authentication](https://sharadar.com/docs/auth). The provider's documentation describes daily OHLCV for active and delisted US public stocks and a history back to December 1997. This does not itself prove CRSP-style terminal/delisting-return completeness; that field must be checked.

**International and matched-control price leg:** [EODHD All World plans](https://eodhd.com/pricing) and [historical EOD API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes). The current public plan page lists All World EOD at US$19.99/month (personal use); the actual exchange/symbol coverage, delisted history, usage terms and required fields must be verified on the subscribed plan. Older delisted records may have EOD-only coverage.

The campaign's older estimate of roughly US$30/month for Sharadar plus US$19.99/month for EODHD is **provisional**, not a current verified Sharadar quote or a spending limit. Before any checkout, the account holder must verify the actual current price, required coverage, renewal, cancellation and licence terms. The agent must never upgrade to a higher tier or annual plan silently.

## Credentials and bounded use

- `SHARADAR_API_KEY` — provider credential for Sharadar.
- `EODHD_API_TOKEN` — provider credential for EODHD.
- `ACCTCLOCK_ENABLE_PAID_DATA=1` — required explicit opt-in for the repository's paid API adapter.
- Never paste API secrets into ChatGPT, issues, commits, manifests or logs. Provision them directly in the execution environment or its secret store.
- Raw downloads are cached outside the repo and manifests must redact secrets.
- Smoke-test one US symbol and one international symbol, manually verify schema and adjustments, then measure coverage on delisted securities and matched controls before considering bulk acquisition.
- If the selected feed lacks required terminal/delisting returns, do not impute zero or silently drop the issuer. Record the missingness; test a documented permitted reconstruction or stop the primary test.

## Scientific gates remain binding

The user has selected a paid-provider route and authorized a feasibility audit; that does **not** waive the frozen thresholds. The primary campaign's minimum of 12 independent adoption/jurisdiction clusters and 200 treatment firms remains in force. A firm count cannot substitute for independent clusters. The latest registered PH-1 assessment expects roughly 4–8 clusters, below the 12-cluster minimum, so the arm is likely to be inconclusive unless a strictly pre-outcome feasibility audit demonstrates otherwise. Do not lower thresholds, peek at returns, treat EU member states as independent cohorts, or amend the frozen preregistration in place.

## Current status

- Paid provider direction: **selected**.
- Public primary-source harvesting: **authorized** within access terms/rate limits.
- Raw-cache policy and registered panel rule: **confirmed**.
- PH-1 feasibility audit: **authorized**.
- Provider subscription / credentials: **not provisioned or confirmed here**.
- Paid API request, bulk filing harvest, return analysis, backtest and trading: **not performed by this update**.
- Strategy status: **PARKED — not validated, not rejected**.

# ACCTCLOCK — Paid-data route and operational decisions

**Decision:** D-031, 2026-10-22  
**Status:** Provider route selected; implementation committed; acquisition not yet run.  
**Scope:** This document supersedes the earlier request for A1–A5 decisions as the current operating instruction. It does not edit any frozen hypothesis, specification, preregistration, panel rule, threshold, or result.

## 1. Direction from the maintainer

The instruction “Remove all the bottlenecks and direct against paid services” is interpreted as permission to route this research workflow toward paid market-data services and to resolve repository-level decisions in favour of execution. This is **not** authority to create accounts, sign a contract, buy a subscription, incur a charge, or spend an unspecified amount. No purchase or paid API call occurred as part of this repository update.

Effective decisions:

| Decision | Current direction |
|---|---|
| A1 — market prices | Use the paid-provider route in §2. Do not use a survivor-only free feed as the primary price source. |
| A2 — public evidence | Read-only collection from public regulator, issuer and standard-setter sources is authorised for this research, subject to published access rules and reasonable rate limits. |
| A3 — raw-data policy | Confirmed: cache raw files outside the repository; commit code, hashes, manifests, and non-restricted derived aggregates only. |
| A4 — panel scope | Confirmed: use the already registered panel-membership rule; do not hand-pick jurisdictions or narrow the panel to force a preferred count. |
| A5 — PH-1 | The prospectively registered PH-1 may undergo a **feasibility audit**. Its one-time outcome analysis is permitted only if every preregistered gate is passed before any outcome is opened. |
| Spend | No charge, subscription, auto-renewal, annual commitment, or purchase is made by an agent. The vendor route is selected; any actual checkout must be done by the account holder after verifying the current price and terms. |
| Live trading | Prohibited; research-only. No broker connection, order routing, paper/live deployment, or trading workflow is authorised. |

The agent must record this direction as D-031 and must not continue asking the user to re-answer A1–A5. Operational access is now the task; it is not a reason to repeat the decision request.

## 2. Provider route

### 2.1 Preferred split

1. **United States, active and delisted listings:** Sharadar direct stock-prices table (stocks / SEP) for daily OHLCV, corporate actions, ticker changes and delisted securities. Documentation: [Stock prices](https://sharadar.com/docs/stocks), [API authentication](https://sharadar.com/docs/auth).
2. **Non-US venues and matched control jurisdictions:** EODHD All World historical EOD API and its exchange symbol lists, requesting active and delisted listings as separate coverage groups. Documentation: [EOD historical data](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes), [delisted-symbol workflow](https://eodhd.com/financial-apis/delisted-stock-companies-data-2), [plans](https://eodhd.com/).
3. **Existing institutional entitlement:** If a CRSP/WRDS entitlement is already available in the authorised execution environment, assess it as a candidate for the price/delisting leg without creating a new account or purchase. Never assume an entitlement exists. Do not block public-filing work while checking it.

The purpose of this split is not to assume that the sources are complete. It is to obtain auditable candidate data, then measure whether the coverage and terminal-return information actually satisfy the frozen requirements. A provider’s marketing description is not a successful coverage audit.

### 2.2 Price and cost facts to verify at checkout

- The public EODHD plan page currently advertises **All World from US$19.99/month** with historical EOD access; its delisted-data page says older delistings may have EOD history only. The exact fields and history must be checked per exchange and instrument.
- The earlier campaign estimate for Sharadar was approximately **US$30/month**, but the current direct subscription price has not been confirmed from a public price table in this session. Treat it as a planning estimate, not a verified quote.
- The old combined estimate of approximately **US$50/month** is therefore provisional. Verify the current checkout price, scope, renewal and cancellation terms before any purchase. The agent must not silently switch to a higher tier, annual plan or extra product.
- Vendors' personal-use terms do not permit unrestricted redistribution. Raw price history must stay outside the public repository. Publish only code, schemas, hashes, source URLs, retrieval facts and non-restricted aggregates.

### 2.3 Acceptance tests for each provider (before bulk use)

For each exchange and for both treated and matched-control jurisdictions, establish all of the following from a small bounded pilot:

1. The listing universe includes inactive/delisted securities, ticker changes, class changes and the historical identifiers needed to link to issuer filings.
2. Historical price dates span the frozen event windows; count observations and gaps by event, security, year, venue and liquidity bucket.
3. OHLCV, adjustment factors, splits, dividends, spin-offs, cash acquisitions, bankruptcies and final tradable/terminal observations are sufficiently represented to calculate the required event returns.
4. **Explicit delisting-return gap:** neither an “adjusted close” field nor the existence of a delisted ticker automatically proves that a vendor supplies a CRSP-style delisting return. Identify what the plan actually includes. Where the exit/terminal value is unavailable, reconstruct it only from a documented, permissible primary source and a predeclared rule; otherwise record it missing and fail the registered R1 gate. Do not impute a zero return or drop the security silently.
5. The terms allow the intended personal research use and local caching, and no restricted raw payload is committed.
6. Request quotas, throttling, retry behaviour, history limits and identifier mapping are recorded. Never expose an API key in a log, URL manifest, commit, issue, or report.

If the selected plans cannot satisfy the registered price/delisting-return requirement, record the failure and stop the primary test. Do not call a partially covered panel “survivorship-clean” merely because paid access was used.

## 3. Credentials and bounded execution

The repository now has scripts/price_provider_client.py and offline tests in tests/test_price_provider_client.py.

- Sharadar credential: environment variable SHARADAR_API_KEY.
- EODHD credential: environment variable EODHD_API_TOKEN.
- The client also requires ACCTCLOCK_ENABLE_PAID_DATA=1. It is disabled by default.
- Raw payloads are written under $ACCTCLOCK_CACHE/raw/prices/ (default ~/.cache/acctclock) and hashes/redacted URLs are appended to $ACCTCLOCK_CACHE/manifests/prices.jsonl.
- Credentials are redacted from manifest URLs. Never ask the user to paste secrets into chat or commit them to the repository.
- Smoke-test one already-active US symbol and one symbol in an international venue, then validate returned rows manually against the vendor's documented schema before any panel-scale collection. The first pass is bounded, cancellable and read-only. No API call should be initiated unless the API credentials exist, the paid-data flag is set, and the account's quota/charges are understood.
- The adapter is not a subscription-management tool. It cannot create an account, accept terms, enter payment details, or purchase a plan.

## 4. Public filing and control-data work proceeds in parallel

Do not make paid price access a reason to delay tasks that need only public sources. Use the implemented SEC EDGAR acquirer for US filings and the registered primary-source route for issuer/regulator filings, legal instruments, IFRS Foundation profiles, EUR-Lex, FASB, FX and World Bank WGI.

Record source URL, retrieval timestamp, HTTP status, bytes and SHA-256. Honour each source's access policy and rate limits. Preserve original filings and restated comparatives as separate vintages. Do not use normalised current fundamentals as a substitute for originally published accounting items.

## 5. Frozen statistical gates remain binding

This change resolves operating choices; it does **not** remove a scientific limitation by wording.

- The frozen primary design stops before outcome calculations if it has fewer than **12 independent adoption/jurisdiction clusters** or fewer than **200 treatment firms**, as specified by the registered protocol.
- A firm count is not a substitute for independent clusters when treatment is assigned at jurisdiction/standard level.
- The current PH-1 notes report six primary-verified day-level T-A jurisdictions and an expected cluster count of roughly **4–8**, below the registered threshold. PH-1 therefore cannot proceed to outcome analysis unless a pre-outcome feasibility audit, under the same frozen rules, genuinely demonstrates that all preregistered gates are satisfied. It must not be “fixed” by looking at returns, lowering the threshold, treating the EU's 27 states as 27 independent adoption cohorts, or making post-hoc panel choices.
- If a gate fails, report **inconclusive/parked before outcomes**. This is a useful feasibility result, not evidence that the hypothesis is true or false.
- Do not amend the frozen v1.0/v1.1/v1.2/v1.3 artefacts in place. Any substantive alternate design must be a new, dated, preregistered version created before its outcome data are inspected.

## 6. Exact next sequence

1. Reconcile the latest campaign-state, handoff and panel row counts; do not trust stale duplicated counts.
2. Verify subscription plan scope, price and terminal-return semantics from current vendor documentation. No purchase is performed by the agent.
3. Implement/test any missing adapter coverage; keep all credentials out of code and logs.
4. Once valid user-provisioned credentials exist, run the two-symbol smoke test and record the manifest.
5. Continue the public filing/calendar work independently, with rate limits and source manifests.
6. Build the per-venue/per-event coverage matrix and publish the feasibility audit **before computing any return**.
7. Compute the registered outcome only if the frozen data-quality and sample gates pass. The PH-1 arm remains once-only and must be voided if an outcome is peeked early.
8. End with an evidence-backed result, blockers that are genuinely external or statistical, and the single highest-value next action. Never claim that a route selection or adapter implementation is a completed backtest.


## 7. Latest environment smoke check (2026-10-22)

Two bounded requests were attempted using only provider-published public sample/demo credentials and non-strategy AAPL date ranges: one Sharadar stocks-table query and one EODHD AAPL.US query. Both failed before an HTTP response with the local execution environment error **DNS resolution failed** ([Errno -3] Temporary failure in name resolution). The failure manifest is research/manifests/price_provider_smoke_attempts.jsonl; ledger entry E-025 records the attempt.

Interpretation: this is **not** evidence of vendor rejection, invalid sample credentials, or an API outage. No payload was received, no price data was inspected, and no paid API request or charge occurred. Do not repeat the same calls in this environment; retry from a network-enabled repository runner. The repository adapter's offline tests also remain unexecuted in this session because a working local repository clone is not available. Keep those validation items explicitly pending.

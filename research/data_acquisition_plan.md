# ACCTCLOCK — Data Acquisition Plan

Written: 2026-10-22
Author: Worker session 4 of the ACCTCLOCK loop.
Governing design: `research/specification_v1.1.md` (v1.1),
`research/preregistration_v1.1.md` (v1.1).
Companion: `research/data_route_assessment.md` (route comparison and D-031 current decision).

Status: **D-031 route selected; acquisition not yet executed.** The repo now contains a guarded paid-provider client and offline tests. No paid data was purchased or fetched; no public filing archive was harvested; no workflow run started; no outcome-period return has been computed or inspected.

**Current instruction:** public read-only harvesting is authorized subject to source terms/rate limits, and the selected paid route is Sharadar for US stocks plus EODHD All World for international venues. This supersedes the earlier requirement to wait for separate A1–A5 user responses. A paid request still requires user-provisioned credentials, an explicit adapter flag and known quota/charges; an agent must not buy a subscription or spend money. Keep raw files outside the repository. See research/paid_data_route_execution.md and research/authorisation_request.md.

---

## 1. What this document is, and what it is not

The v1.1 registration made the research design executable in principle. This document specifies source routes, cache layout, hashes/manifests, rate limits and validation requirements. D-031 has resolved the earlier A1–A5 operating decisions: read-only public collection is authorized, and the paid-provider route is selected. Remaining gates are operational (provisioned price-data access/credentials, source/coverage validation) and scientific (the frozen feasibility thresholds), not repeated authorization questions.

This remains an acquisition plan, not evidence that data have been acquired or the hypothesis tested. Section 8 is the current bounded execution sequence.

## 2. What the v1.1 design requires, mapped to data

| Design element | Data needed | Why it is not optional |
|---|---|---|
| **T-R** (first full report under the standard) | Filing **acceptance timestamp in UTC** | The primary exit timestamp and the end of the transition window. A fiscal-period end is not a public timestamp and cannot be traded against. |
| **T-RI** (first interim report under the standard) | Filing acceptance timestamp in UTC | The **pre-emption window** — a kill signal, not a null. |
| **T-A / T-E** (adoption announcement, effective date) | The jurisdiction's legal instrument | The primary entry timestamp and the start of the transition window. Already partly satisfied by `research/event_calendar.csv`. |
| **Affected-firm list knowable ex ante** | The instrument's scope definition + a point-in-time security master | V-009 ambiguity 6: the binding data constraint. |
| **Pre-adoption information quality** | The firm's **last annual report published before T-A**, as originally filed | The primary state. A normalised vendor feed substitutes the latest restated figure, which is look-ahead. |
| **Mechanical accounting-change magnitude** | The **restated comparatives** inside the firm's own first report under the standard | The CH-2 test; must be quantified on every primary statement the standard changes. |
| **Transition-window abnormal return** | Daily prices **with delisted securities retained** | A survivorship-filtered panel biases the estimate *against* the hypothesis: the firms the hypothesis predicts the effect in (low information quality, small, illiquid) are exactly the names a survivors-only panel drops. Kill condition 9 fires. |
| **Mandatory controls** | Enforcement quality (WGI) and the linguistic-distance measure | V-009 Cycle-52 item 2 and Cycle-113 item 1: mandatory, and not claimable as the campaign's own. |
| **Matched control jurisdictions** | Prices, filings and identifiers for not-yet-treated jurisdictions | The DDD's counterfactual. |

## 3. Caching and repository policy (default position)

**Default: cache everything outside the repository. Commit only code, manifests and
hashes.** This is the safe default because licence and terms differ per source and
redistribution rights differ per vendor.

```
$ACCTCLOCK_CACHE/                     # default: ~/.cache/acctclock  (outside the repo)
  raw/                                # immutable, write-once
    sec_edgar/                        # submissions, filing index, raw SGML headers
    oam/<jurisdiction>/               # per-OAM raw pulls
    ifrs_calendar/                   # IFRS Foundation jurisdiction profiles, snapshots
    eurlex/                           # OJ instruments (PDF/HTML)
    prices/<vendor>/                  # vendor extracts
    fx/                               # ECB reference rates
    wgi/                              # World Bank WGI extracts
    linguistic/                       # official-language status sources
  derived/                            # reproducible transforms of raw/
    filings/                          # parsed acceptance timestamps, XBRL facts
    panel_v1.1.csv                    # the registered panel, with T-A / T-E per event
    prices_panel/                     # point-in-time price panel
    identifiers/                      # firm <-> security <-> venue crosswalk
  manifests/                          # JSON manifests + hashes (see §5)
```

**What may be committed to the repository:**

| Artefact | Committed? | Notes |
|---|---|---|
| Acquisition and parsing **code** | **Yes** | `scripts/` — deterministic, reviewable, no data. |
| **Manifests** (source, URL, retrieval time, HTTP status, bytes, SHA-256) | **Yes** | `research/manifests/` — this is the provenance record. |
| **Hashes** of every raw file | **Yes** | in the manifest; the file itself stays in the cache. |
| **Derived aggregates** (the panel file, coverage counts, filing counts per event) | **Yes, if they contain no vendor-licensed content** | e.g. `research/panel_v1.1.csv` — event ids, dates, counts. |
| **Raw vendor price extracts, raw filings, identifier masters** | **No (default)** | Only with an explicit maintainer ruling that redistribution is permitted. |
| **Any file containing vendor-restricted content** | **No** | No exception. |

**Trigger for revisiting the default:** a maintainer ruling recorded in
`research/decision_log.md` as a new decision (D-0xx), stating that a specific named
source may be committed. The ruling is per-source and never blanket.

## 4. File layout and record schemas

### 4.1 Raw-file naming (deterministic, re-derivable)

```
raw/sec_edgar/<cik>/<accession-nodashes>/<form>.txt        # complete submission text file
raw/sec_edgar/<cik>/<accession-nodashes>/index.json        # filing index (acceptance date-time, form type, period)
raw/sec_edgar/<cik>/submissions.json                       # submissions JSON (CIK history; NOT used for the acceptance time)
raw/oam/<jurisdiction>/<yyyy>/<filing-id>/<original-document>   # original as published
raw/eurlex/celex-<celex>.html
raw/prices/<vendor>/<instrument>-daily-<yyyy>.csv
```

### 4.2 Derived record schemas

**Filing table** (`derived/filings/filings.csv`):

| Column | Type | Rule |
|---|---|---|
| `filing_id` | str | Source-native identifier (accession number / OAM id) |
| `jurisdiction` | str | ISO-ish code; `US`, `UK`, `EU`, `TR`, … |
| `cik_or_local_id` | str | Firm identifier in the source's namespace |
| `firm_id_internal` | str | Crosswalk key assigned by this pipeline (see §4.3) |
| `form_type` | str | 10-K / 10-Q / 20-F / annual report / interim report … |
| `period_end` | date | Fiscal period end. **Never used as a trading timestamp.** |
| `acceptance_datetime_utc` | ISO-8601 | **The only usable timestamp.** |
| `acceptance_datetime_source` | str | `sgml_header` \| `oam_field` — provenance of the parse |
| `is_first_full_under_standard` | bool | Derived; recorded with the derivation rule id |
| `is_first_interim_under_standard` | bool | Derived |
| `standard_id` | str | `IFRS15`, `IFRS16`, `IFRS9`, `ASC606`, `ASC842`, `ASU201601` |
| `source_url` | str | Exact URL fetched |
| `retrieved_utc` | ISO-8601 | Retrieval timestamp |
| `content_sha256` | hex | SHA-256 of the raw document bytes |

**Panel table** (`derived/panel_v1.1.csv`) — the registered panel of
`research/specification_v1.1.md` §1.1, one row per (standard, jurisdiction):

| Column | Rule |
|---|---|
| `event_id` | `EV-*`, matching `research/event_calendar.csv` |
| `standard_id`, `jurisdiction`, `stratum` | Stratum ∈ {A, B} per the specification |
| `T_A`, `T_E` | Adoption announcement and effective dates, primary-sourced |
| `T_A_source_url`, `T_E_source_url` | Primary source of each date |
| `date_conflict` | Free text; empty if none. **A conflict is recorded, never silently resolved** (D-011) |
| `affected_firm_scope_rule` | How the affected-firm list is determined ex ante |
| `filing_route` | Which OAM/regulator route, and whether it publishes a **time** |
| `price_venue_set` | Venues expected to be covered |
| `in_registered_panel` | bool — set **before** the feasibility audit and never changed afterwards |
| `coverage_notes` | Post-audit notes |

**Price table** (`derived/prices_panel/prices.csv`): date, internal security id, venue,
close, volume, currency, `is_delisted_last_observation`, `delisting_return_vendor`,
`corporate_action_adjusted` (bool), source.

**Identifier crosswalk** (`derived/identifiers/crosswalk.csv`): internal firm id,
security id, venue, cik/local id, valid-from, valid-to, name history.

### 4.3 Identifier discipline

- The internal `firm_id` is assigned by the pipeline, never taken from a vendor's
  "permanent" id without a validity interval.
- Every security carries a **valid-from / valid-to** interval so that a name change or
  a merger does not silently split a firm.
- Clustering is at the **firm** level; multiple share classes are separate securities
  but one firm (as in v1.0 §5).

## 5. Manifest and hashing scheme

Every fetched artefact produces one manifest entry:

```json
{
  "source_id": "SEC_EDGAR_SUBMISSION",
  "url": "https://www.sec.gov/Archives/edgar/data/.../0000320193-18-000123.txt",
  "method": "GET",
  "http_status": 200,
  "content_type": "text/plain",
  "bytes": 8123456,
  "sha256": "<hex>",
  "retrieved_utc": "2026-10-22T00:00:00Z",
  "user_agent": "acctclock-research <contact> (contact required by SEC policy)",
  "local_path": "raw/sec_edgar/320193/000032019318000123/10-K.txt",
  "parser_version": "sec_acceptance_parser@1.0.0",
  "notes": "acceptance datetime parsed from the SGML header ACCEPTANCE-DATETIME field"
}
```

Rules:

1. **SHA-256 over the raw bytes as received**, before any transformation. The hash is
   of the *file*, not of the parsed rows.
2. Manifests are append-only JSONL, one file per source, committed to the repository.
3. A fetch that fails is recorded as a **failed retrieval** with the HTTP status and
   the exception text — never as an absence.
4. Parsers are versioned; a parser change invalidates the derived layer and requires a
   re-run, which is recorded.
5. The **availability lag** measurement (the SEC states there is no timestamp for when
   content first becomes available on sec.gov — S-31) is produced by the pipeline as a
   coverage report: the distribution of (first observed retrieval time − acceptance
   time) for re-fetched documents. The lag is **measured, never assumed**.

## 6. Source-by-source acquisition specifications

### 6.1 SEC EDGAR (United States) — `data.sec.gov` and `www.sec.gov/Archives`

- **Current direction (D-031):** read-only acquisition is authorized under SEC access policies; no bulk harvest before a bounded smoke check.
- **Compliance:** SEC requires a **declared User-Agent** identifying the requester and
  a contact address, and caps traffic at **10 requests per second**. The pipeline uses
  **≤ 2 requests/second** with a token bucket, and honours `Retry-After`.
- **Acceptance timestamp:** parsed from the **raw SGML header**
  (`ACCEPTANCE-DATETIME`, `HHMMSS` **Eastern**), converted to UTC using the US
  daylight-saving offset for that date. The `data.sec.gov` submissions JSON field is
  **not** used for the acceptance time, because it has been documented to mix UTC and
  Eastern clock (S-41).
- **What to fetch:** the submissions JSON per CIK (identifier history), the filing index
  for each periodic report, and the complete submission text file for the reports that
  define T-R, T-RI, the state variables, and the restated comparatives.
- **Scope control:** fetch by CIK for the identified universe, not by full-index
  scanning. The universe itself comes from the panel's affected-firm rule, so the
  EDGAR work does not require an unbounded crawl.

### 6.2 FCA National Storage Mechanism / RNS (United Kingdom)

- **Current direction (D-031):** public-source acquisition is authorized subject to the route's access terms and timestamp/coverage checks.
- **What must be verified before use (an open gap, recorded in
  `research/event_calendar.csv` EV-201):** the day-level **UK endorsement instrument**
  date for IFRS 15 and IFRS 16 (the UK Endorsement Board approval and the FRC
  instrument), and whether the NSM/RNS route publishes a **filing time** and not only a
  date. A date without a time cannot produce T-R.
- **Note:** the UK is registered in Stratum A but its T-A values are **not yet
  primary-verified**. The panel file must carry `date_conflict` / an explicit
  unverified marker for those rows until the instrument is fetched.

### 6.3 National OAMs and regulators (Stratum B, and EU member-state routes)

- **Current direction (D-031):** public-source acquisition is authorized per route, subject to access terms, a pre-fetch timestamp/format/terms assessment, and rate limits.
- **Candidate routes named in `research/data_route_assessment.md` §6.1:** KAP (Türkiye),
  Saudi Exchange / CMA (Tadawul), SECP (Pakistan), the Croatian HANFA system, EGX
  (Egypt), and the ESMA ESEF filings via national OAMs for the EU member states.
- **Per-OAM verification pass required before any bulk fetch:** (a) does the route
  publish a **time** (not only a date); (b) what timezone is it in; (c) does it serve
  the **original** filing document or only a rendered version; (d) what the terms of use
  permit. A route failing (a) is recorded as **date-only** and its events are flagged;
  a date-only route cannot supply T-R and its events are excluded from the primary
  estimate with the exclusion counted.
- **Rate limits:** each OAM's own stated limit applies and is recorded in the manifest
  schema as `rate_limit_note`. Where no limit is published, the pipeline defaults to
  **1 request/second** and a descriptive User-Agent.

### 6.4 Standard-setter and legislative sources (calendar)

- IFRS Foundation jurisdiction profiles (S-47) — the **panel membership authority**.
  A **dated snapshot** of the profile pages is taken and committed with its hash,
  because the profiles are updated on an ongoing basis and the panel must be
  reproducible.
- EUR-Lex — the EU endorsement instruments (S-27, S-28, S-29) as the primary source
  for the EU T-A dates.
- FASB project pages / news releases / ASU index (S-33, S-34) for the US T-A dates.
  Note the recorded gap: `research/event_calendar.csv` EV-103 (ASU 2016-01) has an
  **unverified day-level issuance date** and must be fetched before that event is used.
- The **UK Endorsement Board / FRC** instruments for the UK (see §6.2).
- Each jurisdiction's own adoption instrument for Stratum B.

### 6.5 Prices — selected paid-provider route (D-031)

**Preferred split:**

- **US active and delisted stocks:** Sharadar stock-prices table / SEP, daily OHLCV with split-adjusted and split/dividend/spinoff-adjusted fields. Official docs: https://sharadar.com/docs/stocks and https://sharadar.com/docs/auth. The docs describe active and delisted US names back to December 1997.
- **International and matched-control venues:** EODHD All World historical EOD API; inventory active and delisted symbol lists by exchange, then request EOD history. Official docs: https://eodhd.com/financial-apis/api-for-historical-data-and-volumes, https://eodhd.com/financial-apis/delisted-stock-companies-data-2, and https://eodhd.com/pricing.
- **Existing CRSP/WRDS entitlement:** may be assessed if already provisioned, but do not assume access or create a new account solely for this possibility.

The current public EODHD price page lists **US$19.99/month** for All World EOD (personal use). The campaign's previous Sharadar estimate (~US$30/month) is not verified as a current quote. The earlier combined ~US$50/month figure is only a planning estimate. Verify checkout price, market/identifier coverage, data fields, licence, renewal and cancellation terms before any purchase; the agent may not buy or silently upgrade a plan.

**Required validation:** paid access does not itself prove the data panel is survivor-clean. Before bulk acquisition, audit exchanges, ticker history, inactive/delisted names, history depth, corporate actions, adjusted price definitions, delisting/terminal return treatment and coverage in both treated and not-yet-treated control jurisdictions. An adjusted close is not automatically a CRSP-style delisting return. Do not assume a missing terminal return is zero or silently drop the security; use a documented permitted reconstruction or fail the registered R1 gate.

The implementation is **scripts/price_provider_client.py**, with offline tests in **tests/test_price_provider_client.py**. It is disabled by default; requires **ACCTCLOCK_ENABLE_PAID_DATA=1** plus **SHARADAR_API_KEY** or **EODHD_API_TOKEN**, which must be provisioned directly in the execution environment/secret store, never in chat or Git. Raw files and manifests remain under the external cache, and credential values must never appear in logs or manifest URLs. No purchase or paid request has been made by this update.

### 6.6 FX, enforcement and linguistic distance

| Item | Source | Cost | Notes |
|---|---|---|---|
| Daily FX | ECB reference rates (frankfurter / ECB SDW) | Free | Same-day; the conservative column adds 10 bps. |
| Enforcement quality | World Bank **Worldwide Governance Indicators** | Free | Annual; **revised**, not vintage. The revision caveat is stated in every report; a sensitivity to ±1-year variants is pre-registered. |
| Linguistic distance | The published measure in **S-44**; fallback = an ordinal distance-from-English scale from UN/ISO 639 official-language status, English-official at 0 | Free | The fallback is registered in `research/specification_v1.1.md` §3.5 so the design is executable if the published index cannot be reproduced from its source. **Which source is used must be recorded before the holdout is opened.** |

### 6.7 Analyst data

**Treated as unavailable** (S-25). The v1.1 design is executable without it: analyst
coverage enters only as a matching variable and as a pre-registered secondary proxy,
both conditional on licence availability.

## 7. Verification and integrity checks (run before the feasibility audit)

1. **Hash verification:** every raw file's SHA-256 is re-verified against the manifest
   on each run; a mismatch aborts the pipeline.
2. **Timestamp sanity:** acceptance datetimes must be (a) after the issuer's period
   end, (b) within a plausible filing-lag distribution for the jurisdiction and form
   type, (c) not in the future relative to the retrieval time. Violations are quarantined
   and counted, not silently fixed.
3. **Future-leak scan:** for every field used as a pre-event variable, assert that its
   source filing's acceptance time is **< the decision timestamp** of the event in
   which it is used. This is the automated form of the point-in-time rule.
4. **Restatement isolation:** each accounting value is stored with the acceptance time
   of the filing it came from, so the point-in-time vintage is selectable and later
   restatements remain available as separate vintages.
5. **Delisting retention:** assert that every firm in the pre-event universe either has
   price data through the end of its event window **or** a vendor delisting return.
   A firm with neither is counted as a **coverage failure**, and the count is reported.
6. **Coverage matrix:** counts by event, jurisdiction, year, treatment leg, liquidity
   bucket and split — the input to the preregistration's feasibility audit (§5).

## 8. Current execution decision (D-031) — replaces the old A1–A5 wait

The earlier A1–A5 question list is historical; do not use it as a reason to wait for another user answer. The maintainer's current direction is recorded in research/authorisation_request.md and research/decision_log.md.

| Item | Current decision | Execution boundary |
|---|---|---|
| A1 — prices | Select Sharadar for US active/delisted prices and EODHD All World EOD for international/control venues. | Subscription purchase and payment remain with the account holder; an agent does not create accounts, accept paid terms or incur charges. API calls require user-provisioned credentials, explicit enable flag and known plan quota/charges. |
| A2 — public data | Read-only harvesting is authorized for SEC EDGAR and public regulator/issuer/standard-setter sources listed in §6. | Apply source access terms, rates, declared User-Agent and retry rules; cache outside repo and log failed retrievals. |
| A3 — raw data | Use external cache; commit code, hashes, provenance manifests and non-restricted aggregate outputs only. | No raw vendor-licensed payload in Git. |
| A4 — panel | Apply the already registered panel rule. | Do not hand-pick, trim or add jurisdictions after the feasibility audit starts to change counts. Reconcile stale panel counts from code/source manifests first. |
| A5 — PH-1 | Feasibility audit is authorized. | Outcome returns are inspected only if the data-quality and preregistered sample gates pass; preserve the once-only PH-1 rule. |

### 8.1 Bounded trigger sequence

1. Record D-031 and verify all frozen preregistration files remain unchanged.
2. Reconcile the panel file and state/handoff counts using the committed builder and manifest; record each pending membership condition explicitly.
3. Run the offline suite in the actual repository environment and report the observed test count. Do not infer that a test passes simply because test files were committed.
4. Continue public-source collection within permitted rate limits without waiting for vendor access.
5. If user-provisioned vendor credentials are available, verify that quota and charges are understood; enable the adapter explicitly for a small US and an international symbol, validate schema and secret redaction, then review results before any bulk request.
6. Build and publish the feasibility audit: independent clusters, treatment and control counts, coverage, missingness, survivorship/delisting-return semantics and licensing. **No outcome-period returns before this report.**
7. Stop before the outcome if the frozen minimum of **12 independent clusters** or **200 treatment firms** fails, or if the primary price/terminal-return requirement cannot be satisfied. Report the result as inconclusive/parked, not as a null and not as a validated strategy.

### 8.2 Explicitly not done or authorized

- No subscription purchase, auto-renewal or unspecified spend by an agent.
- No paid API request until credentials have been provisioned and quota/charges are understood.
- No bulk filing harvest until bounded smoke checks succeed and source rate limits are verified.
- No GitHub Actions run, workflow change, broker connection, trading action or deployment.
- No outcome-period return has been computed or inspected.

## 9. Historical free-data fallback (superseded as the selected route by D-031)

This is a historical fallback, not the current selected route. If paid credentials cannot be provisioned, the panel would collapse to **US (EDGAR) + UK (FCA
NSM) + EU-27 (national OAMs, treated as one application cohort)**, and the registered
Stratum B is unavailable because free survivorship-clean price coverage does not exist
for those venues.

| Quantity | Fallback value | Consequence |
|---|---|---|
| Independent clusters | ≈ **8** (EU IFRS 15/9/16 as one cohort per standard, UK IFRS 15/16, US ASC 606/842/ASU 2016-01) | **Below the ≥12 pre-registered minimum** → the primary estimand is **inconclusive by construction** (preregistration §5.3). |
| Treatment firms | likely ≥ 200 in the EU/US legs | Firm count does **not** substitute for cluster count: treatment is assigned at jurisdiction level, so the EU's single application date is one cluster. |
| Price panel | survivorship-filtered | **Kill condition 9 fires by construction**, and the bias is *against* the hypothesis (the low-information-quality arm is disproportionately dropped). |
| Conclusions that remain reachable | the descriptive event-study path; the **announcement/anticipation check** (CH-1); the **pre-emption window** (W-PRE, kill signal); the **H-C / PEAD** secondary; a direction-and-magnitude replication of the published conflict between **S-35** (K-IFRS reduced PEAD in Korea) and **S-36** (IFRS increased PEAD in Greece) | These are reported and explicitly not claimed as validation. |
| Conclusions that do **not** remain reachable | any promotion claim; any statement that the effect exists or does not exist; any portfolio-level net-return claim | A survivor-filtered cost estimate is not an institutional cost estimate. |

**The fallback is registered as a decision, not chosen silently by a data accident.** If
it is used, the primary result is reported as **inconclusive by construction**, with the
count of 8 clusters and the survivorship bias stated in every table.

## 10. Cost and effort summary

| Item | Cost | Effort | Blocking? |
|---|---|---|---|
| SEC EDGAR acquirer + SGML acceptance parser | free | 1–2 days | **Yes — the primary spine** |
| OAM acquirers (per jurisdiction) | free | 1 day each | Yes for Stratum B |
| UK endorsement instrument verification + NSM time verification | free | 0.5 day | Yes for the UK rows |
| Price subscription | EODHD currently lists US$19.99/month for All World EOD; Sharadar quote unverified (old ~US$30/month estimate) | account-holder checkout + bounded adapter test | Selected route; purchase not made by agent |
| IFRS Foundation profile snapshot | free | 0.5 day | Yes for the panel |
| EUR-Lex / FASB primary-date verification | free | 0.5 day | Yes for T-A |
| WGI + FX + linguistic distance | free | 0.5 day | Yes for the mandatory controls |
| Identifier crosswalk | free | 2–3 days | Yes |

## 11. Reproducibility

Every artefact in `derived/` must be reproducible from `raw/` plus the committed code,
by re-running the pipeline with the same parser versions. The pipeline must be
re-runnable **offline** from the cache: no step may require a live network call unless
it is the acquisition step itself. The pipeline's own output must be deterministic
given the same cache, so that an independent reviewer can re-derive the panel, the
coverage matrix and the feasibility-audit counts without a single re-fetch.

# Pre-outcome feasibility audit notes (session work)

## Current state
- Verified condition-2 jurisdictions (10): Brazil, EU, Hong Kong SAR, Indonesia, Malaysia, New Zealand, Philippines, Saudi Arabia, Singapore, UK
- Panel v1.2: 141 rows total, 10 with verified T-A in 10 distinct timing cohorts, 131 pending with empty T_A
- All rows pending (conditions 3, 4, 5 unverified)

## Gates (frozen)
- >= 12 independent timing cohorts
- >= 200 treatment firms
- Valid terminal/delisting returns required

## Observations
- Current verified cohorts: 10 distinct T-A dates spanning 2024-05-10 to 2026-02-13
- Gap to >=12: need +2 more cohorts minimum
- EU member states (27) could add 1 cohort if cleared (join 2026-02-13) - but carve-out check outstanding
- Other jurisdictions (local-equivalent) could add cohorts if verified
- Thailand excluded from arm on T-E ground (applies 2028-01-01)
- No outcome-period return computed or inspected

## Blockers
- **B1 (lawful free source inventory):** In progress. See `research/free_source_inventory/inventory.md`.
- **B2 (delisted securities and terminal returns coverage):** Unverified for free sources. Not established (FAIL, D-042/E-047).
- **B3 (network/DNS):** **SUPERSEDED 2026-11-05 (Session 1585).** The previously recorded "DNS resolution issues; external network requests may fail before HTTP" is stale. Outbound HTTPS is live: DNS resolves for sec.gov, github.com, yahoo.com, worldbank.org, stooq.com; `https://www.sec.gov/Archives/edgar/data/<CIK>/<accession>/<accession>.txt` returns HTTP 200 with a real `<ACCEPTANCE-DATETIME>` SGML stamp; `https://efts.sec.gov/LATEST/search-index` returns real hits. B3 no longer blocks any route. (Residual: `api.stooq.com` and `data.sec.gov/submissions/CIK*.json` 404; `data.fca.org.uk/rns/search` 403; `tadawul.com.sa` does not resolve from this environment.)
- **B4 (conditions 3,4,5 unverified for all rows):** Unchanged.

## Session 1593 (2026-11-05) - non-US A2 route re-probe, jurisdiction by jurisdiction

**CVM EDGAR (Brazil) — NEW finding, route RETIRED.** `www.cvm.gov.br/edgar/` and every
`/edgar/BuscaDeArquivo*.do` variant now answer **HTTP 410 Gone** (verified 2026-11-05:
`BuscaDeArquivos.do`, `BuscaDeArquivo.do`, `/edgar/` root, with and without `?view=1`).
This is a hard retirement, not a transient block, and it is a *new* finding: prior sessions
had not probed the CVM EDGAR filing-search route at all. Brazil's A2 remains **pending**;
no acceptance TIMESTAMP is obtainable from this source.

**DART / OpenDART (Korea FSS electronic disclosure) — reachable but not free-terms.**
`opendart.fss.or.kr` and `dart.fss.or.kr` resolve and answer HTTP 200, but the API surface
rejects every unauthenticated path with `{"message":"잘못된 URL입니다. 확인해주세요(/...)", "status":"101"}` and the public notice list (`/api/list.json`, `/api/document.xml`,
`/api/v1/notice`, `/api/noticeList.json`) returns only the OpenDART HTML shell, not a
machine-readable filing list. An acceptance TIMESTAMP requires an OpenDART API key, which
is a registration/credential route, **not** a free terms-permitting route under D-032.
Korea's A2 therefore remains **pending**.

**Re-confirmed negative (all 2026-11-05):** FCA RNS `data.fca.org.uk/rns/search` and
`/rns` HTTP 403 (F-003 stays `not_retrieved`, D-098 closed); FCA NSM page 404; Bursa
Malaysia `/en/announcements/search` 403; IDX `/en/announcements/search` 403; PSE
`/stockMarket/announcements/search` 403; NZX `/api/announcements/search` 404 and
`api.nzx.com` 403; KRX English page 404; ESMA `/financial-reporting-en` and
`/esma-activities/financial-reporting-and-interpretation-group` 404; EUR-Lex deep links
empty body. HKEXnews still 403; Tadawul still unresolvable.

**Does NOT advance the gate.** Admitted-firm count still 0 < 200 FAIL; cohort count
unchanged (12 ≥ 12 MET); no `panel_v1.1.csv` or `panel_v1.2.csv` row modified; all 141
PH-1 rows remain `filing_route` = PENDING A2 and `price_venue_set` = PENDING A1; no
outcome-period return computed or inspected; no paid services; no credentials requested;
`.github/workflows/main.yml` unmodified.

## Session 1585 (2026-11-05) - A2 route re-probe
- **A2 (filing route with acceptance timestamp) is LIVE for US rows.** SEC EDGAR SGML route confirmed returning real acceptance timestamps:
  - Qualcomm FY2018 10-K (CIK 804328, 0001728949-18-000095): ACCEPTANCE-DATETIME `20181107161548` ET -> **2018-11-07T21:15:48Z**
  - JPMorgan Chase FY2018 10-K (CIK 19617, 0000019617-19-000054): ACCEPTANCE-DATETIME `20190226165725` ET -> **2019-02-26T21:57:25Z**
  - Both FY2018 10-Ks are the first annual reports under ASC 606 (EV-101, T_E 2018-01-01), i.e. the registered panel's own T-R rows.
- Raw artefacts cached to `$ACCTCLOCK_CACHE` (external), never the repository. Manifests (source, URL, status, bytes, SHA-256) appended to `research/manifests/sec_edgar.jsonl` per D-015.
- **Does NOT advance the gate.** A2 is a per-filing route, not a firm-admission list. It supplies the timestamp mechanism for US rows but does not by itself admit firms to the treatment class, does not change the admitted-firm count (still 0 < 200 FAIL), and does not change the cohort count (still 12 >= 12 MET). No panel row was modified; no outcome-period return computed or inspected.
- **Non-US A2 routes still not established:** FCA RNS `data.fca.org.uk/rns/search` HTTP 403 (AccessDenied); `tadawul.com.sa` does not resolve from this environment; ESMA ESEF filing portal URLs 404. UK/EU/Saudi rows remain A2-pending.
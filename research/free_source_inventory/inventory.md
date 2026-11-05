# Free-source inventory for ACCTCLOCK (D-032 route)

This inventory is prepared under D-032 (free and lawful public sources only).
No paid vendors, subscriptions, payment-linked trials, paid API calls or credential requests are to be made.

## Session 1585 re-probe (2026-11-05)

**Network is live.** The previously recorded B3 "environment has DNS resolution issues;
external network requests may fail before HTTP" is **stale and superseded**. Verified
this session (plain `urllib`, declared User-Agent, no proxy):

| Host | Result |
|---|---|
| `www.sec.gov` | HTTP 200; `/Archives/edgar/data/<CIK>/<accession>/<accession>.txt` returns the real SGML header with `<ACCEPTANCE-DATETIME>` |
| `efts.sec.gov/LATEST/search-index` | HTTP 200 with real hits (joinable on `adsh`/`ciks`/`file_date`, not on ticker) |
| `www.ifrs.org` | HTTP 200 |
| `query1.finance.yahoo.com/v8/finance/chart/AAPL` | HTTP 200 with real meta |
| `api.worldbank.org` | HTTP 200 |
| `stooq.com` (root) | HTTP 200, but `/s/d/l/...` HTTP 404 and `api.stooq.com` does not resolve |
| `data.fca.org.uk/rns/search` | HTTP 403 AccessDenied |
| `tadawul.com.sa` | does not resolve from this environment |
| `eur-lex.europa.eu` | HTTP 200 (empty body for the `/eli/.../oj` deep links tried) |
| `www.esma.europa.eu` | HTTP 200; ESEF filing-portal deep links 404 |

**A2 (filing route that publishes an acceptance TIMESTAMP) is LIVE for US rows.**
Real acceptance timestamps were extracted from EDGAR SGML headers for two FY2018
10-Ks, which are the first annual reports under ASC 606 (EV-101, T_E 2018-01-01):

- Qualcomm FY2018 10-K (CIK 804328, accession 0001728949-18-000095):
  ACCEPTANCE-DATETIME `20181107161548` ET -> **2018-11-07T21:15:48Z**
- JPMorgan Chase FY2018 10-K (CIK 19617, accession 0000019617-19-000054):
  ACCEPTANCE-DATETIME `20190226165725` ET -> **2019-02-26T21:57:25Z**

Raw artefacts are cached outside the repository (`$ACCTCLOCK_CACHE`, default
`~/.cache/acctclock`); provenance manifests are appended to
`research/manifests/sec_edgar.jsonl` per D-015. This is a route demonstration, **not**
a gate advance: it supplies the timestamp mechanism for US rows but does not admit
firms to the treatment class, does not change the admitted-firm count, and does not
change the cohort count.

**Non-US A2 routes remain unestablished** (FCA RNS 403; Tadawul unresolvable; ESMA
ESEF portal 404). UK/EU/Saudi panel rows stay A2-pending.

**B2 (delisted/terminal-return price coverage) remains not established (FAIL,
D-042/E-047).** Stooq's price endpoints 404 in this environment and Yahoo's
delisted-ticker endpoints 404; the pre-2017 Wayback Yahoo route (D-148) does not reach
the PH-1 outcome window. No free source produces a survivorship-clean
delisted/terminal-return series here.

## Session 1593 re-probe (2026-11-05) — non-US A2 routes, jurisdiction by jurisdiction

| Host / route | Result |
|---|---|
| `www.cvm.gov.br/edgar/` and `/edgar/BuscaDeArquivo*.do` | **HTTP 410 Gone** — the CVM EDGAR filing-search route is *retired*, not merely unreachable. New finding this session (prior sessions never probed it). Brazil A2 stays pending. |
| `opendart.fss.or.kr`, `dart.fss.or.kr` | HTTP 200, but every unauthenticated API path returns `{"message":"잘못된 URL입니다.","status":"101"}` and the public notice list returns only the OpenDART HTML shell. An acceptance TIMESTAMP requires an API key (registration/credential route, not free terms-permitting under D-032). Korea A2 stays pending. |
| `data.fca.org.uk/rns/search`, `/rns` | HTTP 403 (F-003 stays `not_retrieved`, D-098 closed) |
| `www.fca.org.uk/firms/fca-national-storage-mechanism` | HTTP 404 |
| `www.bursamalaysia.com/en/announcements/search` | HTTP 403 |
| `www.idx.co.id/en/announcements/search` | HTTP 403 |
| `www.pse.com.ph/stockMarket/announcements/search` | HTTP 403 |
| `www.nzx.com/api/announcements/search` | HTTP 404; `api.nzx.com` HTTP 403 |
| `www.krx.co.kr/eng/...` | HTTP 404 |
| `www.esma.europa.eu/financial-reporting-en` | HTTP 404 |
| `eur-lex.europa.eu` deep links | HTTP 200 but empty body |
| `www.hkexnews.hk` | HTTP 403 (unchanged) |
| `tadawul.com.sa` | does not resolve (unchanged) |

**Does NOT advance the gate.** Admitted-firm count still 0 < 200 FAIL; cohort count
unchanged; no panel row modified; no outcome-period return computed or inspected; no
paid services; no credentials requested; `.github/workflows/main.yml` unmodified.
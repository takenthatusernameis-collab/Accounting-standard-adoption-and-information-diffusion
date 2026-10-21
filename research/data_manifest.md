# ACCTCLOCK — Data Manifest and Availability

Last updated: 2026-10-21
Status: **No data acquired. The primary test is blocked on data access.**

## 1. What is in this repository today

| Path | Content | Usable as research data? |
|---|---|---|
| `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` | Protocol v1.0 | No — protocol |
| `research/hypothesis.md`, `specification_v1.md`, `preregistration.md` | Frozen claim and test design | No — design |
| `research/source_ledger.csv` | Literature audit (25 sources) | No — citations |
| `research_state/workflow_run_diagnostics.jsonl` | Workflow run diagnostics written by the collector | No — operational |
| `scripts/`, `tests/` | Controller progress accounting, serialization, campaign resume, and their tests | No — infrastructure |

**There is no market data, no filing archive, no standardised accounting
extract, and no identifier file in this repository.** No claim in
`research/results.md` rests on data, because no data has been analysed.

## 2. Data required by the frozen specification

| # | Dataset | Fields needed | Point-in-time requirement | Frequency of updates |
|---|---|---|---|---|
| D1 | Daily equity prices and volumes | close, volume, bid-ask or quoted spread proxy, delisting return, share class, venue, currency | as-traded; delisted securities retained | daily |
| D2 | Filing acceptance timestamps | report type, filing time (UTC), fiscal period end, publication date | original acceptance time; no restated timestamps | per filing |
| D3 | Standardised accounting items as published | revenue, leases (ROU asset/liability), financial-instrument classification, total assets, working capital, accrual components, at least 8 quarters of history | as originally published, with later restatements kept separately | per filing |
| D4 | Identifier history | firm ↔ security ↔ venue over time, name changes, mergers, delistings | full history including inactive securities | continuous |
| D5 | Corporate actions | splits, dividends, rights issues, spin-offs | as announced | daily |
| D6 | FX | daily spot and forward rates for venue currencies | same-day | daily |
| D7 | Standard/event calendar | per standard and jurisdiction: issuance, endorsement, legal adoption, effective dates, first affected fiscal year | verified against the standard setter's own publication | event-driven |
| D8 | Standard-setting documents | the issued standard and its effective date | primary source | event-driven |
| D9 | Analyst forecasts and coverage (secondary only) | consensus EPS, dispersion, number of analysts | vintages with issue dates | daily/periodic |
| D10 | Enforcement proxies (secondary only) | jurisdiction-level enforcement indices | as of the event | annual |

## 3. Access status

| Route | Status | Notes |
|---|---|---|
| CRSP/Compustat/Worldscope/I/B/E/S | **Unavailable** | Subscription licensed (see `research/source_ledger.csv` S-25). No credentials, no licence, and no local copy. |
| Repository-committed data files | **None** | Verified by inventory on 2026-10-21; the repository contains 3 non-infrastructure files. |
| Public company filings (issuer/regulator sites) | **Partially available, not yet harvested** | Read-only retrieval is possible for issuer filings; a systematic, timestamped harvest of D2/D3 is not built. |
| Open transition data (lead) | **Identified, not retrieved** | Slovak IFRS 16 first-time-adopter filings and a linked dataset (S-24) are a public route to first-time-adopter accounting-change magnitudes for one jurisdiction. |
| Hypothesis-factory dossier | **Unavailable** | The canonical ACCTCLOCK dossier referenced by the protocol was not reachable from this environment; no commit SHA, retrieval date, or source path can be recorded for it. |

## 4. Integrity controls to implement when data arrives

1. Every dataset gets a **source manifest** entry: vendor, product, query or
   extract, version/date, timezone convention, identifier basis, corporate
   action treatment, and a file hash where feasible.
2. Every timestamp is stored in **UTC** with the original venue timezone
   recorded separately; fiscal-period end and publication time are distinct
   fields and are never conflated.
3. **Restatements are retained** as separate vintages; the point-in-time
   vintage is the one used for any pre-event variable.
4. **Delisted and failed firms are preserved**; no survivorship filter is
   applied at any stage, and the delisting return from the vendor is used
   unchanged.
5. Duplicate firm-event observations and overlapping windows are removed
   explicitly and the count of removals is reported.
6. Event dates are validated against **primary sources** (standard setter and
   issuer). Conflicts are recorded; the date that maximises returns is never
   selected.
7. Coverage is reported by event, country, year, treatment group, and liquidity
   bucket; critical timestamps are never imputed without a documented
   justification.

## 5. If licensed data cannot be obtained

The fallback route, to be attempted only if the licensed route is refused, is a
**narrowed, open-data test** built on public regulator/issuer filings for a
small number of jurisdictions, with:

- a much smaller event panel (and therefore an explicit **inconclusive-by-
  construction** conclusion if fewer than 12 independent clusters exist);
- returns reconstructed from public price histories for the same securities,
  with a documented delisting treatment;
- the same frozen specification, unchanged, with the reduced power stated in
  every result.

A reduced-power test is acceptable as *evidence*; a reduced-power test is not
acceptable as a basis for promotion. That distinction must be preserved in
`research/results.md`.

## 6. Blocker statement

> Essential data and permission are unavailable in this environment. Phase 3
> (data integrity) and Phase 4 (estimation) therefore cannot start. The work
> that *can* be done without data — repository audit, literature audit,
> hypothesis freezing, specification and preregistration, and the infrastructure
> that the controller needs to credit future sessions — has been completed and
> is recorded in this repository.
>
> This is a documented blocker, not a result. It is not evidence for or
> against the hypothesis, and it is not a reason to claim completion.

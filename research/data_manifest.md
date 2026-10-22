# ACCTCLOCK — Data Manifest and Availability

Last updated: 2026-10-22
Status: **No data acquired. The primary test is blocked on data access and on
maintainer authorisation, not on the design.** The executable design is registered as
**v1.1** (`research/hypothesis_v1.1.md`, `research/specification_v1.1.md`,
`research/preregistration_v1.1.md`).

## 1. What is in this repository today

| Path | Content | Usable as research data? |
|---|---|---|
| `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` | Protocol v1.0 | No — protocol |
| `research/hypothesis.md`, `specification_v1.md`, `preregistration.md` | Frozen claim and test design **v1.0** (immutable) | No — design |
| `research/hypothesis_v1.1.md`, `specification_v1.1.md`, `preregistration_v1.1.md` | Registered design **v1.1** (executable; replaces v1.0's empty treatment group) | No — design |
| `research/source_ledger.csv` | Literature audit (54 sources) | No — citations |
| `research/event_calendar.csv` | Primary-verified adoption dates for the registered panel | No — input to the test, not a result |
| `research/data_route_assessment.md`, `research/data_acquisition_plan.md` | Data route comparison and the concrete acquisition and authorisation plan | No — plan |
| `research_state/workflow_run_diagnostics.jsonl` | Workflow run diagnostics written by the collector | No — operational |
| `scripts/`, `tests/` | Controller progress accounting, serialization, campaign resume, and their tests | No — infrastructure |

**There is no market data, no filing archive, no standardised accounting
extract, and no identifier file in this repository.** No claim in
`research/results.md` rests on data, because no data has been analysed.

## 2. Data required by the registered specification (v1.1)

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
| D10 | **Enforcement quality (mandatory control under v1.1)** | jurisdiction-level enforcement index (World Bank WGI Regulatory Quality and Quality of Regulatory Framework) | jurisdiction-year of T-A; **revised, not vintage** — the caveat is stated in every report and a ±1-year sensitivity is pre-registered | annual |
| D11 | **Linguistic distance (mandatory control under v1.1)** | country-level distance from English: the published measure in **S-44**, or the registered ordinal fallback scale | jurisdiction-constant; the choice of source must be recorded **before the holdout is opened** | annual / one-off |
| D12 | Restated comparatives in the first report under each standard | the pre-change and post-change figures, per primary statement the standard changes | the filing that carries them, at its own acceptance time | per filing |

## 3. Access status

| Route | Status | Notes |
|---|---|---|
| CRSP/Compustat/Worldscope/I/B/E/S | **Unavailable** | Subscription licensed (see `research/source_ledger.csv` S-25). No credentials, no licence, and no local copy. A maintained institutional (WRDS) seat would be the best outcome and needs no purchase. |
| Repository-committed data files | **None** | Verified by inventory on 2026-10-22; the repository contains research artefacts and infrastructure only. |
| Public company filings (issuer/regulator sites) | **Reachable, not yet harvested** | Read-only retrieval is possible. The **SEC EDGAR** route is verified (acceptance timestamp in the raw SGML header, Eastern Time, converted to UTC — S-31, S-32, S-41). The **UK NSM/RNS** and the **national OAMs** require a per-route verification pass on whether a *time* (not only a date) is published. **Harvesting is not yet authorised** (`research/data_acquisition_plan.md` §8, item A2). |
| Price data | **Unavailable without authorisation** | Free sources are survivorship-filtered (measured: ~41% of a delisted cohort missing on free stooq — S-38), which fires kill condition 9 by construction and biases the estimate *against* the hypothesis. The cheapest survivorship-clean sources are ~$50/month at retail tiers; a CRSP/WRDS seat is free if the maintainer has one. |
| Open transition data (lead) | **Identified, not retrieved** | Slovak IFRS 16 first-time-adopter filings and a linked dataset (S-24) remain a public route to first-time-adopter accounting-change magnitudes for one jurisdiction. |
| Hypothesis-factory dossier | **Reachable and retrieved** | `takenthatusernameis-collab/QUANTITATIVE-HYPOTHESIS-FACTORY` at commit `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff`, retrieved read-only on 2026-10-22 and re-verified in the v1.1 registration session. Source paths and the binding amendments are recorded in `research/source_ledger.csv` S-37 and in `research/decision_log.md` D-008, D-012 – D-016. **The upstream repository was not modified.** |
| Enforcement series (WGI) | **Free, not yet assembled** | Annual and **revised**, not point-in-time; the revision caveat must be stated in every report and a ±1-year sensitivity is pre-registered. |
| Linguistic-distance measure | **Free, source to be pinned** | The published measure (S-44) is the primary control; an ordinal fallback scale is registered in `research/specification_v1.1.md` §3.5. |
| Analyst forecasts | **Treated as unavailable** | S-25. The v1.1 design is executable without it. |

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
**narrowed, open-data test** built on public regulator/issuer filings for a small number
of jurisdictions, with:

- a much smaller event panel (and therefore an explicit **inconclusive-by-
  construction** conclusion if fewer than 12 independent clusters exist);
- returns reconstructed from public price histories for the same securities,
  with a documented delisting treatment;
- the same frozen specification, unchanged, with the reduced power stated in
  every result.

Under the v1.1 design the fallback is scoped precisely in
`research/data_acquisition_plan.md` §9: **US (EDGAR) + UK (FCA NSM) + EU-27 (national
OAMs, one application cohort per standard)** — approximately **8 independent
clusters**, below the ≥12 pre-registered minimum, so the primary estimand is
**inconclusive by construction** (preregistration v1.1 §5.3). Stratum B (the
first-time-framework-adopter jurisdictions) is unavailable under the fallback because
survivorship-clean free price coverage does not exist for those venues. What remains
reachable under the fallback is the descriptive event-study path, the announcement
anticipation check, the pre-emption window, the H-C / PEAD secondary, and a
direction-and-magnitude replication of the published conflict between S-35 and S-36.

A reduced-power test is acceptable as *evidence*; a reduced-power test is not
acceptable as a basis for promotion. That distinction must be preserved in
`research/results.md`.

## 6. Source-identifier namespaces (read this before citing a source)

Two numbering schemes are in use in `research/`, and they must not be confused:

| Namespace | Range | Where it lives | How a reference looks |
|---|---|---|---|
| **Local ledger** | `S-01` … `S-54` | `research/source_ledger.csv` | `S-43` |
| **Canonical dossier ledger** | `S-001` … `S-457` | `takenthatusernameis-collab/QUANTITATIVE-HYPOTHESIS-FACTORY` at commit `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff`, `research/source_ledger.md` | `S-221` |

**Documents written before the v1.1 registration (2026-10-22) cite the dossier's
identifiers** — for example `S-179` (Song & Woo, Korea PEAD) and `S-188` (Forbes &
Giannopoulos, Greece PEAD) in `research/data_route_assessment.md` and
`research/decision_log.md`. **Documents written in or after the v1.1 registration cite
the local identifiers.** Every dossier source that v1.1 relies on was added to the
local ledger, so the two namespaces overlap. The mapping for the overlapping entries:

| Dossier ID | Local ID | Source |
|---|---|---|
| S-179 | S-35 | Song & Woo (2015) — K-IFRS adoption reduced PEAD in Korea |
| S-188 | S-36 | Forbes & Giannopoulos (2015) — IFRS adoption increased PEAD in Greece |
| S-221 | S-43 | Christensen, Hail & Leuz (2013) — enforcement |
| S-252 | S-44 | Guan, Shafron, Ye & Zhuang (2025) — linguistic distance |
| S-253 | S-42 | Pirveli & Zimmermann (2026) — systematic review |
| S-254 | S-47 | IFRS Foundation jurisdiction profiles |
| S-267 | S-49 | ESMA Public Statement on IFRS 18 |
| S-271, S-268, S-269, S-270 | S-54 | The single-package convergence (four primary instruments) |
| S-294 | S-45 | Neel (2017) — comparability |
| S-295 | S-46 | Jiao et al. (2012) — analysts' forecasts |
| S-407 | S-52 | De Melo Gaspar Neto (2025) — enforcement mediation |
| S-435 | S-48 | EY transition calendar |
| S-437 | S-53 | flatexDEGIRO early-adopter restated comparative |
| S-452 | S-50 | DRSC DAX 40 survey |
| S-453 | S-51 | Norwegian FSA thematic review |

**Rule.** New documents use the local identifiers. When a document must cite a dossier
entry that has no local counterpart, write the identifier with the qualifier
**"(dossier)"** and record the local counterpart in this table if one is later added.

## 7. Blocker statement

> Essential data and **permission** are unavailable in this environment. Phase 3
> (data integrity) and Phase 4 (estimation) therefore cannot start.
>
> **The design is no longer the blocker.** It was, and it was repaired: v1.1 of the
> hypothesis, specification and preregistration is registered and executable in
> principle (`research/decision_log.md` D-012 – D-016). What remains is a **data and
> authorisation** blocker with a named decision list:
> `research/data_acquisition_plan.md` §8.1 (A1 market data, A2 public harvesting,
> A3 repository policy, A4 panel scope, A5 prospective holdout).
>
> The work that *can* be done without data — repository audit, literature audit,
> hypothesis freezing, the specification and preregistration (v1.0 **and** v1.1), the
> event calendar, the data route assessment, the acquisition plan, and the
> infrastructure that the controller needs to credit future sessions — has been
> completed and is recorded in this repository.
>
> This is a documented blocker, not a result. It is not evidence for or
> against the hypothesis, and it is not a reason to claim completion.

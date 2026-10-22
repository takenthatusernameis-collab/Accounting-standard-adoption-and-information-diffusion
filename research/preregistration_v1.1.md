# ACCTCLOCK — Preregistration v1.1

Registered: 2026-10-22
Supersedes: `research/preregistration.md` v1.0 (2026-10-21). **v1.0 is immutable and is
retained unchanged in the repository.** This file is a *new* registered version, created
before any outcome-period return was computed or inspected, and recorded in
`research/prompt_changelog.md` (Iteration 8).

Companion documents: `research/hypothesis_v1.1.md` (v1.1),
`research/specification_v1.1.md` (v1.1).

---

## 1. Primary outcome

> **The transition-window state contrast** (τ), pooled across events:
>
> **τ = mean over events (standard × jurisdiction) of { [ BHAR_low − BHAR_high ] in the
> treated jurisdiction − [ BHAR_low − BHAR_high ] in the matched not-yet-treated
> control jurisdictions over the same calendar window } ,**
>
> where **BHAR(f)** is the buy-and-hold market-model abnormal return of firm `f` over
> its transition window **[T-A, T-R(f)]**; `low` and `high` are the
> pre-adoption-information-quality legs split at the **within-jurisdiction median**;
> and the estimation is **within jurisdiction**, with the mandatory enforcement-quality
> and linguistic-distance controls imposed per `research/specification_v1.1.md` §3.5–3.6.

**Two-sided.** No sign is selected ex ante. The reported quantity is the low-minus-high
spread with its confidence interval, p-value and economic units (percentage points and
basis points).

The **post-transition window [T-R, T-R+20]** (v1.0's H-B) is a **descriptive control**,
not the primary (V-009 Cycle-58 amendment item 2).

## 2. Estimand

A treatment-effect contrast on the abnormal-return path of firms around the first full
report prepared under a new accounting standard, with **firm-level pre-adoption
information quality** as the pre-registered moderator, identified **within
jurisdiction**, with the country-level conditioners (enforcement quality, linguistic
distance) imposed as mandatory controls and **not claimed as this campaign's own**.

## 3. Pre-registered claim about the published reading (V-009 Cycle-52 item 3)

The systematic review (S-42) finds that IFRS adoption's market effects are real but
that "accounting quality and comparability do not mediate the market effects",
attributing positive findings instead to **IFRS' mandatory nature and pre-IFRS
differences compared to local standards** — the *discontinuity at adoption*.

> **v1.1 claims the discontinuity-at-adoption reading.** The comparability-as-driver
> reading is reported as a **descriptive control only** (SEC-4, steady-state
> comparability).
>
> **A null obtained under the claimed reading is not a kill of the other reading**, and
> the report must say so explicitly.

## 4. Splits (chronological, never random)

Splitting is by **T-A**, the decision timestamp at which the position is taken.

| Split | Definition (by T-A) | Use |
|---|---|---|
| **Development** | T-A before **2016-01-01** | Specification sanity checks, code debugging, placebo construction, power estimation. **No acceptance decision.** Development-split returns are never reported as evidence of the hypothesis. |
| **Validation** | T-A in **[2016-01-01, 2019-01-01]** | Full primary and secondary tests, with all frozen robustness checks. |
| **Untouched holdout** | T-A on/after **2019-01-01** | Opened **once**, after the validation decision is recorded. Never used to select anything. |
| **PH-1 (prospective holdout arm)** | IFRS 18 first-application events (the **2027 interim reporting season**, periods ending 30 June 2027, published July–August 2027, per the dated transition calendar in S-48) | A genuinely forward holdout: the outcome lies in the future and cannot be inspected before it occurs. Registered here; **requires a separate v1.2 registration filed before the first IFRS 18 report is published** (V-009 Cycle-56 amendment item 4). |

### 4.1 The retrospective panel has no post-2019 T-A — declared in advance

Every registered retrospective event has T-A ≤ 2017-10-31 (the latest verified
adoption-announcement date in `research/event_calendar.csv`). **The untouched-holdout
split is therefore expected to be EMPTY.**

This is registered now, before any data is acquired, and its consequence is fixed:

1. **Acceptance criterion 3** (`research/specification_v1.1.md` §10.1: net-of-cost
   portfolio return positive on the chronological holdout) is **expected to be
   unevaluable** on the retrospective panel.
2. The retrospective panel **cannot by itself satisfy protocol promotion gate 4**
   ("results survive pre-registered out-of-sample and placebo tests"). The campaign's
   **promotion gates cannot be met on the retrospective panel**, and the report must
   state this rather than presenting a validation-only result as a pass.
3. The retrospective panel's **registered role is evidential**: it answers *does the
   transition-window state contrast exist, at what size, and does it survive the
   mandatory controls?* Its result feeds the prospective holdout.

### 4.2 Why a chronological split of the retrospective panel is nonetheless a genuine holdout

Because **no outcome-period return has ever been computed in this repository**, the
entire panel is currently un-returned. The chronological ordering is therefore a real
ordering of *information* for the validator, not a formality: the development split's
returns are computed first and are visible before the holdout is opened, and the
holdout is opened **once**. This does **not** upgrade the retrospective panel to a
promotable design — it establishes only that the holdout is uncontaminated.

## 5. Feasibility audit and power (computed **before** the primary model is estimated)

### 5.1 The audit (test order step 1)

The audit enumerates, per event: independent-cluster count; treatment and control firm
counts; coverage by event, jurisdiction, year, split and liquidity bucket; coverage of
the filing timestamps; missingness; and the count of firms whose transition window
length differs materially from the control window length.

### 5.2 Expected cluster counts (a prediction, not a result)

| Stratum | Expected clusters (standard × jurisdiction × application year) | Comment |
|---|---|---|
| A — content change (EU, UK, US) | ≈ **8** | EU IFRS 15 / 9 / 16 (3); UK IFRS 15 / 16 (2, dates to be verified); US ASC 606 / ASC 842 / ASU 2016-01 (3). **All EU events share one application date**, so the EU contributes one timing cohort, not 27 independent ones — this is stated in advance so it cannot be discovered later as a power surprise. |
| B — framework change (first-time IFRS adopters) | ≈ **20–40** | One cluster per (jurisdiction, standard) with a distinct application date; membership governed by the frozen rule in `research/specification_v1.1.md` §1.1, not by which jurisdictions happen to have prices. |
| **Total** | **≈ 28–48** | Above the ≥12 minimum **if Stratum B realises**; **≈ 8 — below the minimum — if Stratum B fails coverage.** |

### 5.3 The rule that binds if the audit falls short (frozen)

> If the realised independent-cluster count is **< 12** or the treatment-firm count is
> **< 200**, the **primary estimand is inconclusive by construction** — by the same
> precedent this document already used for a small holdout in v1.0 §4 and by
> `research/data_route_assessment.md` §6.4 for the 9-event fallback panel. The
> descriptive results (the event-study path, the announcement/anticipation check, the
> pre-emption arm, the H-C secondary, and the direction-and-magnitude replication of the
> published conflict between S-35 and S-36) are still produced **for the record**, and
> the decision is **park** or **inconclusive** — never "pass".
>
> **The rule is fixed here so that a short panel cannot later be used as a reason to
> change the panel, the window, or the thresholds.**

### 5.4 Minimum detectable effect

Unchanged from v1.0 §6: with 12 independent clusters the design is powered (80%) only
for an effect of roughly **0.5–0.7% per event**. If the observed effect is smaller, the
correct conclusion is **inconclusive**, not "no effect". The power calculation is
computed and reported **before** the primary model is estimated.

## 6. Test order (frozen; each step is recorded before the next begins)

1. **Feasibility and event-count audit** (§5). Report and **stop** if the counts fall
   below the pre-registered minimums.
2. **Descriptive event study.** Pre/post abnormal-return, volume and coverage paths from
   [T-A−60, T-R+60td], with the event-time monthly path from month −24 to +3 relative to
   T-R(f), pre-trend inspection, and the coverage profile. **Descriptive only**; may not
   change the specification.
3. **Primary test.** The estimand of §1 with cluster-robust inference, wild-cluster
   bootstrap and the jurisdiction-level randomisation test.
4. **Conditional and secondary tests.** Announcement/anticipation windows (CH-1),
   pre-emption window (CH-9 kill signal), post-transition residual (SEC-1), H-C (SEC-2),
   competing conditioners, alternative information-quality proxies, alternative factor
   benchmarks, matched-pair and regression specifications, **the mandated ablations
   (a), (b), (c)**, and the enforcement / linguistic-distance strata.
5. **Portfolio simulation.** The frozen rule with point-in-time holdings, conservative
   fills, costs, exposures, borrow availability and capacity limits.
6. **Out-of-sample.** The untouched holdout, opened **once** (and PH-1 when it exists).
7. **Robustness and red-team.** Placebo dates, placebo standards, false event
   assignments, leave-one-event-out, outlier exclusion, pre-/post-2010 subperiod,
   regime slices, alternative windows, and the pre-registered multiple-comparison
   adjustment.

**Stopping rule (frozen).** If step 3 fails any acceptance criterion, the remaining
steps are still executed **for the record** so that negative results are preserved, but
the decision is **park** or **reject**. The search stops: no alternative window,
threshold, proxy, universe or panel is tried afterwards to obtain a pass.

## 7. Statistical procedure (frozen)

- Standard errors clustered at the **(standard × jurisdiction × application year)** level
  with a **wild-cluster bootstrap** (Rademacher, 9,999 draws).
- Primary inference also reported as a **randomisation test**: permute the
  information-quality label within event clusters (10,000 permutations).
- **Multiple comparisons:** the three pre-registered secondary outcome families
  (announcement/anticipation SEC-3, transition window [primary], H-C SEC-2) are tested
  with **Holm–Bonferroni at the family level**. All other secondary analyses are
  labelled **exploratory** and reported with unadjusted statistics and an explicit
  "exploratory" tag.
- **Power is computed and reported before the primary model is estimated.**
- **Anti-peeking count (V-009 Cycle-52 item 5, Cycle-58 item 5):** an explicit count
  of every **(state definition × exit rule × jurisdiction × sub-sample)** combination
  examined is maintained and reported, including every country-level control arm
  examined, and every rule change is logged with a date and a reason.

## 8. Data requirements (all point-in-time)

- Daily prices and volumes, **delisted securities retained**, with corporate-action
  adjustments and a vendor delisting return.
- **Filing acceptance timestamps in UTC** for every periodic report, so T-R and T-RI are
  exact and public.
- Standardised financial statement items **as originally published**, including the first
  report under each standard and the restated comparatives needed for the mechanical
  magnitude (§4.4 of the specification).
- Identifier history: firm ↔ security ↔ venue, including delistings, name changes and
  mergers.
- Currency and FX reference rates.
- Jurisdiction-level enforcement quality (WGI) and the linguistic-distance measure, with
  their revision caveats stated.
- Secondary only: analyst forecasts and coverage counts (design is executable without).

The acquisition route, the file layout, the hashing and caching policy and the
authorisation checklist are in `research/data_acquisition_plan.md`.

## 9. Costs and thresholds (frozen, unchanged from v1.0)

- Cost assumptions: `research/specification_v1.1.md` §9 (primary and conservative
  columns).
- The **break-even one-way cost** is reported for every portfolio result.
- Capacity: positions capped at 5% of portfolio notional per name; a capacity statement
  is required at the 1%, 5% and 10% participation rates of 20-day ADV.
- The v1.0 acceptance thresholds (|mean| ≥ 0.5% per event; ≥12 independent events;
  ≥200 treatment firms; break-even ≥ 2× the conservative cost; leave-one-event-out
  changes the point estimate by <50%) are **carried forward unchanged**, plus
  acceptance criterion 8 of the specification (the within-jurisdiction estimate exists
  and survives the mandatory country-level controls).

## 10. Reporting commitments (frozen)

- Report the **full event-outcome distribution**, not just the mean.
- Report the **number of variants tried** at every stage and the split each variant was
  evaluated on.
- Report **every** pre-registered test, including the ones that failed.
- Report all negative and null results in `research/results.md` and
  `research/experiment_ledger.csv`.
- Report the **within-jurisdiction estimate separately from the pooled one**, and the
  estimate **with and without** the mandatory country-level controls.
- Report the enforcement and linguistic-distance strata separately, with the
  interaction test.
- Report the **pre-emption window** result explicitly as a **kill signal**, whether or
  not it is significant.
- Report the **comparator's own power** and the reason it was not run in the published
  literature (V-009 Cycle-58 item 3): the first-time-versus-second-time-adopter
  comparison **on drift** is unrun by the field, so a null in this design is a
  **contribution, not a replication**.
- **No promotion on Sharpe or CAGR alone**; no small-sample annualisation.

## 11. Status

**Registered, not executed.** No outcome-period return has been computed or inspected.
Execution is blocked by data availability and authorisation
(`research/data_acquisition_plan.md`, `research/data_route_assessment.md` §6.5), not by
the design. This document must not be edited after execution begins except by
registering a new version.

## 12. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Frozen outcome, estimand, splits (by T-R), test order, thresholds, costs. |
| **v1.1** | **2026-10-22** | Primary outcome redefined as the transition-window state contrast (the v1.0 post-first-report window demoted to a descriptive control); splits re-anchored on the decision timestamp T-A; the retrospective panel's empty holdout **declared in advance** with its consequence fixed; the prospective holdout arm PH-1 registered; feasibility, cluster-count and power rules fixed so a short panel cannot later justify a design change; the claimed published reading pre-registered; the mandatory country-level controls and their imposition registered; the pre-emption window registered as a kill signal. Registered **before** any outcome-period return was computed. |

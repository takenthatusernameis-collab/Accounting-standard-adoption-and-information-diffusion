# ACCTCLOCK — Preregistration v1.0

Frozen: 2026-10-21, before any outcome-period return was computed. No outcome data
exists in this repository, so nothing in this document can have been tuned on
results.

Companion documents: `research/hypothesis.md` v1.0, `research/specification_v1.md` v1.0.

## 1. Primary outcome

Mean buy-and-hold abnormal return over **[T-R, T-R+20] trading days**, market-model
adjusted, for low-information-quality first-time adopters minus
high-information-quality first-time adopters, within
(standard × jurisdiction × adoption-year) event clusters.

Two-sided test. No sign is selected ex ante; the reported quantity is the
low-minus-high spread with its confidence interval.

## 2. Estimand

A treatment-effect contrast on the abnormal-return path of first-time adopters
around the first report published under a new accounting standard, with
pre-event information quality as the pre-registered moderator.

## 3. Data requirements (all point-in-time)

- Daily prices and volumes, delisted securities included, with corporate-action
  adjustments and a vendor delisting return.
- Filing acceptance timestamps (UTC) for every periodic report, so T-R and
  T-E1 are exact and public.
- Standardised financial statement items as originally published, including
  the first report under each standard.
- Identifier history: firm ↔ security ↔ venue, including delistings, name
  changes, and mergers.
- Currency and FX reference rates.
- Where available (secondary only): analyst forecasts and coverage counts.

## 4. Splits (chronological, never random)

| Split | Definition | Use |
|---|---|---|
| **Development** | Events with T-R before 2019-01-01 | Specification sanity checks, code debugging, placebo construction. No acceptance decision. |
| **Validation** | Events with T-R in [2019-01-01, 2021-12-31] | Full primary and secondary tests, with all frozen robustness checks. |
| **Untouched holdout** | Events with T-R on/after 2022-01-01 | Opened **once**, after the validation decision is recorded. Never used to select anything. |

If the holdout contains fewer than 4 independent events, the holdout result is
reported as **inconclusive by construction** and the promotion gates in the
protocol cannot be met on that split. Development-split returns are never
reported as evidence of the hypothesis.

## 5. Test order (frozen; each step must be recorded before the next begins)

1. **Feasibility audit** — enumerate independent events, treatment/control
   counts, coverage by event/country/year/split/liquidity bucket. Report and
   stop if the counts fall below the pre-registered minimums.
2. **Descriptive event study** — average and median abnormal return paths from
   [T-A−30, T-R+60], pre-trend inspection, volume and coverage profiles. This
   step is descriptive only and may not change the specification.
3. **Primary test** — the pre-registered estimand with cluster-robust
   inference and a jurisdiction-level randomisation test.
4. **Conditional/secondary tests** — H-A and H-C windows, competing
   conditioners, alternative information-quality proxies, alternative factor
   benchmarks, matched-pair and regression specifications.
5. **Portfolio simulation** — the frozen rule with point-in-time holdings,
   conservative fills, costs, exposures, and capacity limits.
6. **Out-of-sample** — the untouched holdout, opened once.
7. **Robustness and red-team** — placebo dates, placebo standards, false event
   assignments, leave-one-event-out, outlier exclusion, subperiod/regime splits,
   alternative windows, and the pre-registered multiple-comparison adjustment.

**Stopping rule:** if step 3 fails any acceptance criterion, the remaining steps
are still executed for the *record* (so negative results are preserved) but the
decision is **park** or **reject**. The search stops; no alternative window,
threshold, proxy, or universe is tried afterwards to obtain a pass.

## 6. Statistical procedure

- Standard errors clustered at the (standard × jurisdiction × adoption-year)
  level, with wild-cluster bootstrap (Rademacher, 9999 draws) because the
  cluster count will be small.
- Primary inference also reported as a **randomisation test**: permute the
  information-quality label within event clusters (10,000 permutations).
- Multiple comparisons: the three pre-registered secondary outcome families
  (H-A, H-B, H-C) are tested with Holm–Bonferroni at the family level; all other
  secondary analyses are labelled exploratory and are reported with their
  unadjusted statistics and an explicit "exploratory" tag.
- Minimum detectable effect: with 12 independent clusters, the design is
  powered (80%) only for an effect of roughly 0.5–0.7% per event. If the
  observed effect is smaller than that, the correct conclusion is
  **inconclusive**, not "no effect".
- Power is computed and reported *before* the primary model is estimated.

## 7. Costs and thresholds (frozen)

- Cost assumptions: see `research/specification_v1.md` §9 (primary and
  conservative columns).
- Break-even one-way cost is reported for every portfolio result.
- Capacity: positions are capped at 5% of portfolio notional per name; a
  capacity statement is required at the 1%, 5%, and 10% participation rates of
  20-day ADV.

## 8. Reporting commitments

- Report the full event-outcome distribution, not just the mean.
- Report the number of variants tried at every stage, and the split each
  variant was evaluated on.
- Report every pre-registered test, including the ones that failed.
- Report all negative and null results in `research/results.md` and
  `research/experiment_ledger.csv`.
- No promotion on Sharpe or CAGR alone; no small-sample annualisation.

## 9. Status

**Registered, not executed.** Execution is blocked by data availability
(`research/data_manifest.md`). This document is the artefact that must exist
before the first outcome-period return is computed; it must not be edited
afterwards except by registering a new version.

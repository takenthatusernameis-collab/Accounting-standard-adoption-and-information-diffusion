# ACCTCLOCK — Results

**Status: no test has been run. There are no results.**

Last updated: 2026-10-21

This file is where effect sizes, uncertainty, costs, out-of-sample performance,
and negative evidence will be reported. It is intentionally short because the
campaign has not reached Phase 4.

## What has NOT been done

- No security has been priced, screened, or held.
- No event has been dated from a primary source.
- No abnormal return, factor model, portfolio simulation, or turnover figure
  has been computed.
- No acceptance criterion has been evaluated, because the test has not started.

## What this file will contain when the test runs

1. Event and independent-cluster counts, treatment/control coverage, balance,
   missingness, effective sample size, and the power calculation performed
   before estimation.
2. Pre-trend plots, descriptive event-study paths, and coverage by event,
   country, year, treatment group, and liquidity bucket.
3. The primary estimand with confidence intervals, p-values, and economic units,
   plus every pre-registered secondary and competing-conditioner result.
4. Gross and net cumulative return under both cost columns, break-even cost,
   turnover, hit rate, average win/loss, tail loss, factor attribution, and
   capacity at 1%, 5%, and 10% ADV participation.
5. Out-of-sample versus in-sample performance, the number of variants tried, and
   the split each was evaluated on.
6. Every placebo, leave-one-event-out, false-event-assignment, and outlier
   exclusion result, including the ones that fail.
7. Reproducibility status: commit, data/config hashes, independent rerun status.
8. The decision: continue, narrow, park, or reject, with reasons.

## Evidence that already exists and must be carried into any conclusion

The literature audit (`research/source_ledger.csv`) found published support for
the mechanism and published counter-evidence against the trading proposition:

- **Support:** IFRS adoption events move prices and the reaction is stronger
  for low pre-adoption information quality and weaker under weak enforcement
  (S-01); mandatory adoption improves comparability (S-02, S-03); mandatory
  disclosure changes produce measurable slow-diffusion effects (S-21); investor
  processing capacity governs how fast earnings news is incorporated (S-17).
- **Counter:** the drift family has decayed and has been argued to be
  non-existent for large caps since about 2006 (S-09, S-10, S-11); transaction
  costs explain most of it (S-12); it partly disappears under disaggregation
  (S-13); and a structurally similar announcement premium (index inclusion)
  fell from roughly 7.6% in the 1990s to roughly 0.8% in the past decade
  (S-20). Anticipation of scheduled reforms absorbs most of their effect
  (S-18, S-19).

These are priors, not results, and they must be reported alongside whatever the
test produces — including a null.

## Reproducibility status of the work so far

- Frozen artefacts are content-addressed by the repository commit; the commit
  that introduces them is recorded in `research/experiment_ledger.csv`.
- The infrastructure is covered by 67 automated tests
  (`tests/test_controller_progress_accounting.py`,
  `tests/test_workflow_diagnostics_scanner.py`,
  `tests/test_nonfinite_result_serialization.py`,
  `tests/test_campaign_resume.py`) and can be rerun with
  `python3 -m pytest -q tests/`.
- No independent reviewer has reproduced anything, because no result exists.

# ACCTCLOCK — Results

**Status: no test has been run. There are no results.**

Last updated: 2026-10-22

This file is where effect sizes, uncertainty, costs, out-of-sample performance,
and negative evidence will be reported. It is intentionally short because the
campaign has not reached Phase 4.

## What has NOT been done

- No security has been priced, screened, or held.
- No event has been dated from a primary source *for a return computation* — the
  event calendar (`research/event_calendar.csv`) now holds primary-source-verified
  **adoption dates**, which is an input to the test, not a result from it. No
  filing acceptance timestamp has been collected, so no T-R has been fixed.
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

### Two priors added in the 2026-10-22 session

- **The effect of IFRS adoption on drift is published and it points both ways.**
  Song & Woo (2015) find K-IFRS adoption *reduced* post-earnings-announcement
  drift in Korea (S-35); Forbes & Giannopoulos (2015) find IFRS adoption
  *increased* PEAD in Greece (S-36). The first-adoption case in the candidate's
  direction is attributed by its own authors to a disclosure shock, and the other
  first-adoption case runs the opposite way. So **first adoption does not predict
  the sign**, and the sign of the H-B effect is genuinely open.
- **The comparator the design rests on is unrun by the field.** The canonical
  hypothesis-factory dossier (S-37, retrieved read-only at commit
  `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff`) records, after three search
  cycles, that no published study compares post-earnings-announcement drift
  between first-time and second-time adopters of a common accounting standard,
  and that the field's largest comparability study is first-adopter *by
  construction* without covering drift. A null in that design is therefore a
  **contribution, not a replication** — and a null in any *other* design is not
  evidence that the mechanism is absent.

## A design finding that must be reported with any result

The frozen specification v1.0's treatment group — "firms whose reporting framework
changed at the event" — is **empty** across the frozen universe, and the canonical
dossier has independently rejected the only within-jurisdiction substitute. This was
recorded as D-009 and is why no result could be reported until a v1.1 registration
existed.

**v1.1 now exists** (`research/hypothesis_v1.1.md`, `research/specification_v1.1.md`,
`research/preregistration_v1.1.md`, registered 2026-10-22, before any outcome-period
return was computed). The design is executable in principle: the treatment is a
jurisdiction-level standard-application event, the state is firm-level pre-adoption
information quality estimated **within jurisdiction**, the control group is a matched
**not-yet-treated** jurisdiction set, and enforcement quality and linguistic distance
are **mandatory controls** rather than optional conditioners.

**Three consequences must travel with every result produced under v1.1:**

1. **The retrospective panel cannot satisfy protocol promotion gate 4 on its own.** Every
   registered retrospective event has T-A ≤ 2017-10-31, so the chronological holdout
   split is **empty**. This was declared in advance (D-014), together with its
   consequence: the retrospective panel's role is **evidential**, and the promotable
   test is the prospective holdout arm **PH-1** (the IFRS 18 first-application window),
   which requires a separate v1.2 registration before the first IFRS 18 report is
   published.
2. **A null in this design is a contribution, not a replication.** The
   first-time-versus-second-time-adopter comparison **on drift** is unrun by the field
   (S-37 / V-009 G-21). The comparator's own power and the reason it was not run must
   be reported with the result.
3. **A survivorship-filtered price panel fires kill condition 9 by construction**, and
   its bias is *against* the hypothesis, because the firms the hypothesis predicts the
   effect in are the small, illiquid, low-information-quality names a survivors-only
   panel drops.

## Reproducibility status of the work so far

- Frozen artefacts are content-addressed by the repository commit; the commit
  that introduces them is recorded in `research/experiment_ledger.csv`.
- The infrastructure is covered by 67 automated tests
  (`tests/test_controller_progress_accounting.py`,
  `tests/test_workflow_diagnostics_scanner.py`,
  `tests/test_nonfinite_result_serialization.py`,
  `tests/test_campaign_resume.py`) and can be rerun with
  `python3 -m pytest -q tests/`. The 2026-10-22 session re-ran the workflow's
  exact invocation and confirmed 67 passing cases.
- The event calendar is reproducible from the recorded primary-source URLs and
  retrieval timestamps in `research/event_calendar.csv`.
- The v1.1 design registration is reproducible from the retrieved canonical dossier at
  commit `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` and from the local source ledger
  rows **S-42 … S-54**.
- No independent reviewer has reproduced anything, because no result exists.

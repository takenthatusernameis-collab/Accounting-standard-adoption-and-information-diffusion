# ACCTCLOCK — Frozen Hypothesis v1.0

Frozen: 2026-10-21
Status: **Pre-registered, untested.** No outcome-period return has been computed in this
repository. Nothing in this file is evidence that an edge exists.

Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`
(v1.0, 2026-10-21). This file is the immutable claim record required by Phase 0 of
that protocol. Any change to the claim, universe, event clock, sample, entry/exit
rules, filters, costs, or acceptance criteria requires a new numbered version
(v1.1, v2.0, …) registered in `research/prompt_changelog.md`; v1.0 is never
overwritten.

## 1. The claim (one sentence)

Around a pre-announced accounting-standard adoption or implementation, firms with
**lower pre-event information quality** exhibit a **different post-event
abnormal-return path** than comparable firms with **higher pre-event information
quality**, and this difference is large enough, persistent enough, and distinct
enough from costs to survive a point-in-time, out-of-sample test.

The claim is deliberately two-sided about sign until a pre-registered economic
mechanism fixes one. No sign may be selected after inspecting returns.

## 2. Why the claim is not yet a strategy

Three separate things are often conflated. They are not interchangeable and the
research must name which one it tests.

| Outcome family | Description | Tradeable at a public timestamp? |
|---|---|---|
| **H-A** Announcement repricing | Price reaction to the standard's issuance, endorsement, or legal adoption | Only with anticipation/look-ahead; the reaction itself happens at the public event |
| **H-B** Transition-window repricing | Price reaction when the first report *prepared under* the new standard is published | Yes — entry after a public, dated report |
| **H-C** Post-earnings-announcement drift | Slower incorporation of the earnings surprise in reports written under the new standard | Yes — entry after a public earnings announcement |

**Primary hypothesis under test: H-B** (transition-window repricing), because it is the
only family that is both publicly timestamped and tradeable without look-ahead.
H-A is retained as a *mechanism and anticipation check* (it is where the published
evidence lives, and if the market reacts at announcement, the H-B premium is
already gone). H-C is retained as a pre-registered secondary.

## 3. Mechanism (why it might exist)

1. A new accounting standard changes reported numbers (revenue timing, lease
   capitalisation, financial-instrument classification). The change is larger when
   the firm's prior framework was less comparable to the new standard.
2. When a firm's pre-event information quality is low, the market has less
   pre-existing private or public knowledge with which to interpret the new
   numbers, so the revision of beliefs about the firm is larger and slower.
3. If the market prices the standard's *existence* at announcement but prices the
   *realised* accounting change only when the first report appears, the residual
   is a slow-information-diffusion premium concentrated in low-information-quality
   firms, and it should be visible in the transition window around the first
   report.

## 4. Competing and counter hypotheses (pre-registered)

- **CH-1 (anticipation).** The information is fully priced at H-A; the H-B window
  contains no residual. *Kill condition.*
- **CH-2 (mechanical accounting change).** The transition-window return is a
  mechanical consequence of balance-sheet or earnings re-measurement (e.g. lease
  capitalisation) and not a slow-information-diffusion effect. Test: control for
  the mechanical size of the accounting change and for accounting-based factors.
- **CH-3 (reversal).** The transition-window return is a reversal of the
  announcement-window reaction, not diffusion. Test: the H-B effect must be
  opposite in sign to the contemporaneous H-A effect for the same firms, and
  vanish when H-A abnormal returns are controlled for.
- **CH-4 (generic small-firm/liquidity/momentum exposure).** The "low information
  quality" proxy is a proxy for size, illiquidity, low analyst coverage, or
  momentum. Test: matched controls and factor controls.
- **CH-5 (concurrent events).** The window overlaps earnings announcements,
  index changes, or other reforms; the effect is not specific to the standard.
  Test: exclude windows with concurrent events; placebo dates.
- **CH-6 (anomaly decay).** The effect existed historically but has been
  arbitraged away or never existed in large caps, where the published drift
  literature shows the strongest decay (see `research/source_ledger.csv`,
  `S-09`, `S-10`, `S-21`).
- **CH-7 (non-specific to standards).** Any large accounting change produces the
  same path, with no special role for *standard* adoption. Test: unaffected
  standards / placebo adoption events.

## 5. Pre-registered predictions

- **P1** The low-minus-high pre-event information-quality difference in
  buy-and-hold abnormal return over the primary window is non-zero at the
  event-cluster level, with the two-sided 95% confidence interval excluding zero.
- **P2** The effect is concentrated in firms with the largest accounting change
  (first-time adopters of the standard) and is absent or materially smaller in
  repeat adopters and in placebo-standard firms.
- **P3** The effect survives controls for size, industry, liquidity, momentum,
  profitability, investment, analyst coverage, and the mechanical size of the
  accounting change.
- **P4** The net-of-cost return is positive in the economically justified
  direction on the subset of the sample where the gross effect is largest, and
  the break-even cost is above a conservative institutional estimate.
- **P5** Placebo adoption dates, unaffected standards, and unaffected
  information-quality splits produce no comparable effect.
- **P6** The effect is not driven by a single jurisdiction, standard, firm, or
  outlier, and the independent-event count supports cluster-robust inference.

## 6. Kill conditions (any one is sufficient to park or reject)

1. The H-A announcement window absorbs the entire effect (anticipation).
2. The information-quality interaction is absent, unstable across
   pre-registered windows, or flips sign under any pre-registered specification.
3. The effect disappears after controlling for size, liquidity, industry,
   momentum, or concurrent reforms.
4. Placebo dates, placebo standards, or untreated groups show comparable
   magnitudes.
5. One jurisdiction, standard, event, firm, or outlier explains the result.
6. The independent-event count is too small for informative cluster-robust
   inference (fewer than 12 independent jurisdiction-standard events, or fewer
   than 200 treatment firms).
7. Estimates are not robust to plausible event windows or benchmark models.
8. Gross returns are erased by conservative spreads, impact, turnover, borrow,
   and financing costs.
9. A point-in-time sample with delisted firms cannot be constructed, so the
   result cannot be replicated without look-ahead.
10. Any threshold, sign, universe, or exit rule was selected after inspecting
    holdout returns.

## 7. Evidence status of this hypothesis

- **Published mechanism evidence (A):** adoption events move prices, and the
  reaction is stronger for low pre-adoption information quality and weaker in
  weak-enforcement regimes — Armstrong, Barth, Jagolinzer and Riedl (2010).
- **Published comparability evidence (A):** mandatory adoption improves
  cross-country comparability (Yip & Young 2012) and reduces insiders' private
  information advantage (Brochet, Jagolinzer and Riedl 2013).
- **Published diffusion evidence (A):** information is incorporated into prices
  slowly and imperfectly around mandatory disclosure changes
  (Chen & Yu 2022 on mandatory monthly revenue reporting; Hirshleifer & Sheng
  2021 on processing capacity and drift).
- **Published counter-evidence (A):** the drift family has decayed sharply and
  has been argued to be non-existent for large caps since ~2006 (Martineau
  2021), is explained away by transaction costs (Ng, Rusticus & Verdi 2008), and
  is partly an artefact of portfolio aggregation (Katz, McCubbins & McMullin
  2018). Announcement premia of the same structural type (index inclusion) fell
  from ~7.6% in the 1990s to ~0.8% in the past decade
  ("The Disappearing Index Effect", NBER WP 30748).
- **Candidate-specific evidence (B):** none. No ACCTCLOCK-specific event study,
  portfolio simulation, or backtest has been run.
- **Strategy evidence (C):** none.
- **Assumptions (D):** the "lower information quality implies slower diffusion"
  link is a conjecture drawn from the general slow-diffusion literature. It has
  not been verified for accounting-standard adoption.

**Net assessment: the mechanism is plausible and published; the trading
specification is untested; the anomaly-decay evidence is a serious prior against
the hypothesis. The test below is designed to reject quickly.**

## 8. Immediate data blocker (documented, not a conclusion)

No market or accounting data is present in this repository, and no licensed
vendor access (CRSP, Compustat, Worldscope, I/B/E/S) exists in this
environment. Without point-in-time data the primary test cannot be executed.
See `research/data_manifest.md` for the exact required inputs, the cheapest
viable data route, and the open data lead identified (Slovak IFRS 16 transition
filings). This blocker is a *data* limitation, not evidence for or against the
hypothesis.

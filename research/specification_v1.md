# ACCTCLOCK — Frozen Strategy Specification v1.0

Frozen: 2026-10-21 (before any outcome-period return was computed; no outcome data
exists in this repository)
Governing hypothesis: `research/hypothesis.md` v1.0
Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` v1.0

This file freezes the ten elements required by Phase 2 of the protocol. Any change
after a return is observed requires a new version (v1.1+) recorded in
`research/prompt_changelog.md`; the primary test is never rewritten to rescue a
result.

---

## 1. Target events

**Standards in scope (primary panel).** Standards that (a) changed reported
numbers materially for a large set of listed firms, and (b) were adopted
jurisdiction-by-jurisdiction so that a first-time/repeat-adopter contrast exists
inside at least some jurisdictions.

| ID | Standard | EU endorsement | First mandatory application | First affected fiscal year | Typical first report |
|----|----------|----------------|-----------------------------|--------------------------|----------------------|
| E1 | IFRS 15 Revenue from Contracts with Customers | 2015 (EU) | annual periods beginning on/after 2018-01-01 (IFRS jurisdictions); 2018-01-01 for ASC 606 filers | FY2018 | Q1–Q2 2018 interim, FY2018 annual from early 2018 |
| E2 | IFRS 16 Leases | 2017 (EU) | annual periods beginning on/after 2019-01-01 | FY2019 | Q1 2019 interim, FY2019 annual |
| E3 | IFRS 9 Financial Instruments | 2015 (EU) | annual periods beginning on/after 2018-01-01 | FY2018 | Q1 2018 interim, FY2018 annual |

**Secondary panel (clearly labelled, never merged into the primary result).**
US GAAP first-time application of ASC 606 / ASC 842 / ASU 2016-01.

**Every event needs a verified date record** per jurisdiction: issuance/publication
date, endorsement or legal adoption date, effective date, first affected fiscal
year start, and the timestamp of the first report published under the new
standard. Dates come from the standard-setter's own publications and the issuer's
own filing index — never from a secondary summary. Where the standard-setter
publication is dated, that date is used for H-A; the issuer's filing timestamp
(venue timezone, normalised to UTC) is used for H-B.

## 2. Event clock (four distinct timestamps, never conflated)

| Clock | Definition | Used for |
|---|---|---|
| T-A | Standard published / endorsed / legally adopted (public timestamp) | H-A announcement window; anticipation check |
| T-E | First fiscal year beginning under the new standard | Alignment/filtering only; never a trading date |
| T-R | Timestamp of the **first report published under the new standard** (filings-system acceptance time, UTC) | **H-B primary entry timestamp** |
| T-E1 | Timestamp of the first **earnings announcement** published under the new standard | H-C secondary entry timestamp |

Only T-A, T-R, and T-E1 are usable trading timestamps, and each is used only from
the moment it is public. Any pipeline step that needs a later piece of
information (for example the exact content of the report) must be evaluated
*after* T-R, never before.

## 3. Treatment and controls

**Treatment.** *First-time adopters of the standard*: firms whose reporting
framework changed at the event (local GAAP → IFRS 15/16/9, or US GAAP → ASC
606/842). The economic shock is the change in reported numbers; the treatment
intensity is measured by the size of that change.

**Control.** Matched non-adopters in the same jurisdiction-year: firms that did
not change reporting framework at the event (repeat adopters of the standard
content, or firms whose framework already contained it), matched 1:k (k ≤ 5) on
size, industry, liquidity, prior-12-month momentum, market-to-book, and
pre-event analyst coverage. Matching uses only information available before T-A.

**Pre-registered information-quality split (the moderator).** Primary proxy:
**absolute discretionary accruals** computed with the cross-sectional Jones model
on the **last annual report published before T-A**, scaled by lagged total assets,
ranked cross-sectionally *within jurisdiction-year*, and split at the median.
Higher absolute value = lower information quality. Rationale: computable
point-in-time from a single filing, widely used, contains no return data, and is
not mechanically a size or liquidity proxy (size and liquidity are matched
away and enter as controls).

**Pre-registered secondary proxies (all computed pre-event, all reported
separately):** restatement or revision frequency over the prior 3 years;
earnings persistence (earnings-to-price ratio slope over 8 quarters);
disagreement among analyst forecasts (if licensed analyst data is available);
disclosure-quality indices (if a licensed index is available).

**Competing conditioners entered as interactions, never as substitutes:**
enforcement quality (jurisdiction-level, pre-registered proxy), analyst
following, the mechanical size of the accounting change, and whether the standard
was mandatory or voluntarily early-adopted.

**Data vintage.** Every pre-event input uses the report *as published at the
time* (point-in-time), never the latest restated version.

## 4. Signal (exact rule)

Primary rule (two-sided; no sign is chosen ex ante):

> At T-R (close of the first report published under the new standard), rank
> first-time adopters within jurisdiction-year by pre-event information quality.
> Form a **long-low-quality / short-high-quality** portfolio (the direction of
> the *difference* is estimated two-sided; the pair is always long the
> information-poor adopter and short the information-rich adopter, and the
> reported estimand is the sign of the spread, not a chosen side).
> Rebalance once at T-R. Exit at the close of the 20th trading day after T-R
> (T-R+20), or at the next earnings announcement under the new standard, whichever
> comes first.

Rules for the mechanical details:

- Entry price: the **closing price of T-R** if the filing was accepted before the
  venue close; otherwise the closing price of the next trading day. The choice
  is made by a rule fixed in advance, not by looking at returns.
- Position sizing: equal notional per name, long leg and short leg each
  beta-neutralised to the market; maximum 5% of portfolio notional per name.
- Exit: T-R+20 as above; no stop-loss, no discretionary override, no
  re-entry.
- Overlapping events: if a firm has two qualifying events within 20 trading
  days, only the first is traded and the second is excluded (no double
  counting).

**Secondary rule (pre-registered, reported separately).** The same construction
entered at T-E1 (first earnings announcement under the new standard) and held 60
trading days (H-C / PEAD-style), with the earnings surprise sign used to
orient the trade in the pre-registered PEAD direction (long positive surprise,
short negative surprise, within the same information-quality split).

## 5. Universe

- Venue: primary — EU regulated markets, UK (LSE), and EEA-equivalent listings
  plus US listings for the secondary panel.
- Security types: common shares only. Excluded: funds, ETFs, REITs, SPACs,
  shell companies, ADRs of non-primary listings (except where the ADR is the
  only listed line for a firm with a first-time adoption event), preference
  shares, warrants, and debt.
- Listing screen: listed on the venue on or before T-A − 250 trading days.
- Liquidity screen: median daily traded value over the 60 trading days ending
  T-A − 1 ≥ 1× the venue-specific screen (default 1,000,000 currency units;
  screen fixed before the event panel is priced, and reported per venue).
- Price screen: closing price ≥ 1.0 currency unit on T-A − 1.
- Point-in-time membership: a firm is in the universe at T-A only if it was
  listed and not already delisted, suspended, or in bankruptcy proceedings on
  T-A − 1.
- Delisted and failed firms are **retained** in the event study and in the
  portfolio simulation (with the actual delisting return and a documented
  delisting loss assumption). No survivorship filter.
- Multiple share classes: each class is a separate security, but the firm is
  matched and clustered at the firm level.
- Foreign listings and non-UTC venues: daily prices converted with the venue's
  official close and the same-day FX rate; reporting currency is not converted
  into USD for accounting variables.

## 6. Entry and exit

- Entry: close of T-R (or the next trading day's close, per the fixed rule).
- Permissible delay after disclosure: **at most 1 additional trading day**,
  chosen by the pre-registered rule, never by return inspection.
- Maximum holding period: 20 trading days (primary); 60 trading days (secondary).
- Exit triggers: fixed horizon, or the first subsequent earnings announcement
  under the new standard, whichever comes first.
- No intra-period trading, no rebalancing inside the window, no compounding
  across events.

## 7. Benchmark and estimand

- **Benchmark:** market model on daily returns, estimated on
  **[T-A−300, T-A−46]** relative to T-R trading days (i.e. ending 45 trading
  days before T-R), with a minimum of 150 non-missing estimation days and a
  20-day buffer for corporate actions.
- **Abnormal return:** AR = r − (α̂ + β̂·r_market). Market model is the primary
  benchmark; **FF5 (5 factors + momentum) and DGTW characteristic-adjusted**
  returns are pre-registered robustness benchmarks, not the primary.
- **Primary estimand:** the **difference in mean buy-and-hold abnormal return
  over [T-R, T-R+20] between the low-information-quality and
  high-information-quality treatment groups**, within jurisdiction-standard
  event clusters, net of nothing (gross). Reported with the two-sided 95%
  confidence interval, p-value, and economic units (percentage points and
  basis points), clustered at the (standard × jurisdiction × adoption year)
  level with a small-sample correction, plus a jurisdiction-level randomisation
  test as the primary robustness to few-cluster inference.
- **Secondary estimands:** [T-R, T-R+5], [T-R+6, T-R+20], H-A window
  [T-A−1, T-A+1] and [T-A−5, T-A+5] (anticipation), H-C window
  [T-E1+2, T-E1+60], and the sign of the H-B effect conditional on the
  contemporaneous H-A effect (CH-3).
- The estimand is a **conditional drift / treatment-effect contrast**, not a raw
  portfolio return. Portfolio net return is a downstream output (step 9/10),
  never the primary test.

## 8. Risk controls

Estimated and reported: market, country, industry, size, value, momentum,
profitability, investment, liquidity, and analyst coverage. Event-cluster
membership is a fixed effect. The information-quality proxy is orthogonalised
against size, liquidity, and coverage. Post-strategy factor attribution
(FF5 and DGTW) is reported in full; an apparent premium that is fully
attributable to a known factor is reported as such and is a kill condition if
the sign flips when the factor is controlled.

## 9. Costs (conservative, and the break-even is reported)

| Cost | Primary assumption | Conservative assumption |
|---|---|---|
| Commission | 1.0 bp per side | 2.0 bp per side |
| Half-spread | 5 bps | 10 bps |
| Market impact | 10 bps (per side, size-scaled) | 25 bps |
| Borrow fee (short leg) | 50 bps/year prorated | 200 bps/year prorated |
| Financing (gross exposure) | cash rate + 0 bps | cash rate + 50 bps |
| Taxes | 0% (research; stated assumption) | 0% with explicit caveat |
| FX | venue close, same-day FX | same-day FX plus 10 bps |
| Delisting / bankruptcy | actual return, floored at −100% | −100% on failure events |

Turnover is computed from the frozen rule. **The break-even one-way cost is
reported** (the per-side cost at which net return equals zero). Promotion
requires a positive net return under the *conservative* column.

## 10. Acceptance and kill criteria

**Acceptance (all must hold; otherwise the result is park/inconclusive, not a
pass):**

1. Primary estimand: 95% CI excludes zero under the two-sided test, and the
   point estimate is economically meaningful (|mean| ≥ 0.5% per event).
2. The sign is stable across all pre-registered windows and at least 2 of 3
   pre-registered benchmarks.
3. Net-of-conservative-cost portfolio return is positive in the pre-registered
   direction on the primary sample and on the chronological holdout.
4. The effect survives the pre-registered placebo set (placebo dates, unaffected
   standards, unaffected split).
5. The result is not driven by a single event, jurisdiction, firm, or outlier
   (leave-one-event-out changes the point estimate by less than 50%).
6. Independent-event count ≥ 12 and treatment-firm count ≥ 200.
7. Net-of-cost break-even cost exceeds the conservative cost assumption by at
   least 2×.

**Kill criteria:** the ten conditions in `research/hypothesis.md` §6.

**Frozen before the holdout is opened** — see `research/preregistration.md` for
the split, the test order, and the multiple-comparison adjustment.

# ACCTCLOCK — Strategy Specification v1.1

Registered: 2026-10-22
Supersedes: `research/specification_v1.md` v1.0 (2026-10-21). **v1.0 is immutable and
is retained unchanged in the repository.** This file is a *new* registered version,
created before any outcome-period return was computed or inspected, and recorded in
`research/prompt_changelog.md` (Iteration 8).

Governing hypothesis: `research/hypothesis_v1.1.md` (v1.1)
Governing preregistration: `research/preregistration_v1.1.md` (v1.1)
Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` v1.0
Binding design constraints: hypothesis-factory dossier V-009 (S-37) and its binding
amendments — Cycle-52, Cycle-56, Cycle-58, Cycle-111 correction notice, Cycle-113,
Cycle-114, Cycle-123, Cycle-126.

---

## 0. The defect this version repairs

v1.0 §3 defined treatment as "firms whose reporting framework changed at the event
(local GAAP → IFRS 15/16/9, or US GAAP → ASC 606/842)". Applied to the v1.0 universe
(EU, UK, US) this yields **zero firms**, so the v1.0 primary estimand is undefined
(D-009, ledger E-010). This version replaces the treatment definition with an
implementable one that is compliant with every binding dossier amendment, and it
registers the two pre-registrations the dossier requires (Cycle-52 item 3: which
published reading is claimed; Cycle-58 items 1 and 2: the transition-window claim and
the presentation-surface attribution).

**Nothing in this file was selected by looking at a return.** No outcome-period return
exists in this repository.

---

## 1. Target events and the registered jurisdiction panel

### 1.1 Panel membership rule (frozen, evaluated before any return is computed)

An event **(standard s, jurisdiction j)** is in the registered panel iff **all** of:

1. `s` ∈ {**IFRS 15**, **IFRS 9**, **IFRS 16**, **ASC 606**, **ASC 842**,
   **ASU 2016-01**};
2. jurisdiction `j`'s regulator has published a **legal instrument** making `s`
   mandatory for a class of listed firms, and that instrument has a public publication
   date (**T-A**) and a stated effective date (**T-E**);
3. the **affected-firm list is knowable ex ante** from `j`'s own published scope
   definition or from the IFRS Foundation jurisdiction profiles (S-47);
4. `j` is not a jurisdiction whose instrument creates a **voluntary early-adoption
   cohort** — such jurisdictions are excluded from the treatment (an *identification*
   exclusion, per V-009 Cycle-56 amendment item 3, not a data exclusion) and may be
   retained only as a pre-registered placebo stratum;
5. `j` has a public filing route that publishes a **filing acceptance time** (a date
   alone is insufficient — T-R must be a timestamp), verified per `j`.

**Membership is decided from the sources below and written to `research/panel_v1.1.csv`
before the feasibility audit.** No event may be added to or removed from the panel after
the feasibility audit begins. If the realised cluster count falls below the
pre-registered minimum of 12, the primary estimand is **inconclusive by construction**
and this is reported, not worked around.

### 1.2 The registered panel (as registered on 2026-10-22)

**Stratum A — content-change events.** The jurisdiction's reporting framework does not
change; the *content* of the framework does. These are the best-documented events and
carry the largest firm counts.

| Event | Standard | Jurisdiction | T-A (adoption announcement) | T-E (effective) | Source of record |
|---|---|---|---|---|---|
| EV-001 | IFRS 15 | EU (IAS Regulation) | 2016-09-22 | FY beginning on/after 2018-01-01 | Reg (EU) 2016/1905, OJ L 295, 29.10.2016 (S-27) |
| EV-002 | IFRS 9 | EU (IAS Regulation) | 2016-11-22 | FY beginning on/after 2018-01-01 | Reg (EU) 2016/2067, OJ L 323, 29.11.2016 (S-28) |
| EV-003 | IFRS 16 | EU (IAS Regulation) | 2017-10-31 | FY beginning on/after 2019-01-01 | Reg (EU) 2017/1986, OJ L 291, 09.11.2017 (S-29) |
| EV-201 | IFRS 15 | United Kingdom | **to be verified** (day-level UK endorsement instrument not yet fetched) | periods beginning on/after 2016-01-01 | FRC / UK Endorsement Board (S-26 jurisdiction profile; instrument pending) |
| EV-202 | IFRS 16 | United Kingdom | **to be verified** | periods beginning on/after 2019-01-01 | as above |
| EV-101 | ASC 606 | United States | 2014-05-28 | FY beginning after 2017-12-15 (PBE) | FASB ASU 2014-09 (S-33) |
| EV-102 | ASC 842 | United States | 2016-02-25 | FY beginning after 2018-12-15 (PBE) | FASB ASU 2016-02 (S-34) |
| EV-103 | ASU 2016-01 | United States | 2016-01 (**day-level unverified**) | FY beginning after 2018-12-15 (PBE) | FASB ASU index (S-26/S-33 family) — **date verification required before use** |

**Stratum B — framework-change events.** The jurisdiction applies IFRS for the first
time; the standard arrives as part of the initial IFRS package. This is where the
*discontinuity-at-adoption* reading (the reading v1.1 claims) is strongest, because
pre-IFRS differences from local standards are largest.

Jurisdictions are **admitted by rule, not by hand-picking**: every jurisdiction that
the IFRS Foundation's jurisdiction profiles (S-47) mark as *"IFRS Standards are
required for domestic public companies"* and that has (a) a published legal instrument
with a publication date, (b) a filing route publishing acceptance times, and (c) price
coverage, enters the panel. The candidate jurisdictions identified in the v1.0
assessment are Turkey, Saudi Arabia, Pakistan, Croatia and Egypt; the panel is **not**
limited to them, and it is **not** limited to countries where IFRS adoption happened in
the IFRS 15/16/9 era — the rule governs.

**Registered sub-strata (pre-registered, reported separately, never merged silently):**

| Stratum | Definition | Role |
|---|---|---|
| **A — content change, already IFRS** | EU, UK (IFRS 15/9/16); US (ASC 606/842, ASU 2016-01 — the US framework does not change because ASC 606/842 are *inside* US GAAP) | Primary panel |
| **B — framework change, first-time IFRS** | first-time IFRS adopters applying the standard as part of the package | Secondary panel; the strongest test of the claimed reading |
| **C — placebo** | placebo standards, placebo jurisdictions, random-date calendars matched by jurisdiction and sector, and unaffected information-quality splits | Robustness (kill conditions 4, 5) |
| **D — excluded** | jurisdictions with a voluntary early-adoption cohort (e.g. the UK IFRS 15 early-adopter cohort), excluded from treatment per V-009 Cycle-56 amendment item 3 | Not an identification; may be used only as a placebo stratum |

### 1.3 Rationale for the panel

- **The EU/UK/US events are the best-verified and the best-covered** (filing route with
  acceptance timestamps, price coverage, identifier history). They carry the largest
  firm counts and the strongest point-in-time accounting data. They are the primary
  panel.
- **The first-time-adopter jurisdictions are included as a registered secondary panel**,
  not as the primary, because (i) their price and filing coverage is materially weaker
  and therefore their realised cluster count is uncertain, (ii) the cohort is small,
  and (iii) the *discontinuity* they embody is the strongest version of the claimed
  reading. The panel is registered **before** coverage is known, precisely so that
  choosing it later on the basis of which jurisdictions happen to have prices is
  impossible.
- **The panel is a staggered-adoption panel, not a binary partition.** Jurisdictions are
  treated at their own application dates; the design never splits firms into
  "first-time adopters" and "second-time adopters" (V-009 Cycle-56 amendment item 1;
  Cycle-111 correction notice).

---

## 2. Event clock (four usable timestamps; never conflated)

| Clock | Definition | Usable as a trading timestamp? | v1.1 use |
|---|---|---|---|
| **T-A** | Adoption announcement — the jurisdiction's legal adoption instrument publication date; where no separate endorsement instrument exists, the standard-setter's issuance date of the instrument that makes it mandatory | Yes | **Primary entry.** Start of the transition window. |
| **T-A1** | Standard-setter issuance date of the standard | Yes | Pre-registered secondary anticipation window; fixes the announcement-clock choice in advance. |
| **T-E** | Effective date (first financial year beginning under the standard) | No | Alignment, filtering, and the `T-E`-based assignment of which fiscal years are affected. |
| **T-R** | Acceptance timestamp (UTC) of the firm's **first full report published under the standard** | Yes | **Primary exit.** End of the transition window. |
| **T-RI** | Acceptance timestamp (UTC) of the firm's **first interim report published under the standard** | Yes | **Pre-emption window** (kill signal). |
| **T-E1** | Acceptance timestamp of the firm's first earnings announcement under the standard | Yes | H-C secondary entry. |

**Timestamp discipline.** For the US, the acceptance datetime is parsed from the **raw
SGML header** of the complete submission text file, not from the `data.sec.gov`
submissions JSON, because that JSON field has been documented to mix UTC and Eastern
clock time (S-41). The SEC's `Accepted` field is Eastern Time and is converted to UTC
using the date's US daylight-saving offset (S-31, S-32). The SEC states plainly that
there is no timestamp for when filing content is first available on sec.gov (S-31), so
**acceptance time is a proxy for availability, and the availability lag must be
measured, not assumed** — the measurement is a pre-registered coverage report.

**Date-conflict rule (pre-registered).** Where two primary sources disagree on a date,
the date stated in the **jurisdiction's own adoption instrument** governs T-A; the
conflict is recorded in the panel file and in `research/event_calendar.csv` and is
never silently resolved. The date that maximises a return is never selected (D-011).

---

## 3. Treatment and controls — the executable definition

### 3.1 Treatment (frozen)

A firm `f` is **treated** for event `(s, j)` if and only if:

1. `f` was listed on a regulated market of jurisdiction `j` on `T-A − 250` trading days
   and was still listed, not suspended and not in bankruptcy proceedings on `T-A − 1`;
2. `f` falls within the scope of `j`'s adoption instrument, so that `f`'s first full
   reporting period beginning under `s` starts on or after `T-E`;
3. `f` filed a first full report under `s` (T-R(f)) on or before `T-A + 900` calendar
   days.

Treatment is therefore **continuous in timing and constant in status within an event**.
**There is no firm-level binary adopter partition anywhere in this design.**

### 3.2 Control group (frozen)

For event `(s, j)`, the control group is the set of firms in **not-yet-treated
jurisdictions** `k` such that:

- `k` has no application of `s` on or before `T-A(s,j)` and none during the event
  window `[T-A, T-R + 20td]` (the *not-yet-treated* restriction is what permits
  staggered-timing inference without assuming parallel trends for already-treated
  units);
- `k` has price coverage and a filing route for the same data requirements;
- `k`'s firms pass the **same screens**, computed as of `T-A(s,j)`.

Control firms are matched 1:k to treated firms (k ≤ 5) on **size, industry, liquidity,
prior-12-month momentum, market-to-book, pre-event analyst coverage and
fiscal-period-end proximity**, using only information available before T-A. The
**fiscal-period-end proximity** match is what makes the control transition window the
same length as the treated one, so the buy-and-hold comparison is like-for-like.

### 3.3 The candidate's own state (frozen) — firm-level pre-adoption information quality

**Primary proxy (unchanged from v1.0 §3):** absolute discretionary accruals computed
with the cross-sectional Jones model on the **last annual report published before
T-A**, scaled by lagged total assets, ranked cross-sectionally **within jurisdiction ×
adoption year**, and split at the within-jurisdiction median. Higher absolute value =
lower information quality. Rationale: computable point-in-time from a single filing,
widely used, contains no return data, and is not mechanically a size or liquidity proxy
(size and liquidity are matched away and enter as controls).

The state is **orthogonalised against size, liquidity and analyst coverage** before
use.

**Pre-registered secondary proxies (all computed pre-event, reported separately):**
restatement or revision frequency over the prior 3 years; earnings persistence
(earnings-to-price slope over 8 quarters); analyst forecast disagreement (only if a
licensed analyst feed is authorised — the design is executable without it).

**Competing conditioners entered as interactions, never as substitutes:** the
mechanical size of the accounting change (CH-2) and analyst following.

### 3.4 The identifying requirement (frozen) — within-jurisdiction

The state contrast is identified **within jurisdiction**. Two requirements follow, and
both are pre-registered:

1. The **primary estimate** is computed with jurisdiction fixed effects and
   jurisdiction-specific linear time trends, so every country-level characteristic —
   enforcement quality and linguistic distance included — is absorbed and **cannot**
   drive the estimate.
2. The **pooled jurisdiction-level estimate** is a **secondary** result, reported (a)
   with the mandatory country-level controls imposed and (b) without them, as the
   mandated ablation (b). Per V-009, a pooled result that exists **only** when the
   country-level controls are omitted is a **fail** (kill condition 11), not a
   secondary.

### 3.5 Mandatory country-level controls (frozen) — Cycle-52 item 2, Cycle-113 item 1

**Enforcement quality** and **linguistic distance** are **mandatory conditioning
controls**, fixed ex ante and applied to every arm. They are *published conditioners*
(S-43, S-44, S-52) and **may not be claimed as this campaign's own effect**. The
pre-registered ablation "replace the enforcement regime with trade invoicing share or
another country characteristic" is **withdrawn** (V-009 Cycle-52 amendment item 2): it
is now the control, not the ablation.

| Control | Primary measure | Pre-registered fallback | Point-in-time treatment |
|---|---|---|---|
| **Institutional enforcement quality** | World Bank Worldwide Governance Indicators, **Regulatory Quality** and **Quality of Regulatory Framework**, jurisdiction-year of T-A (World Bank WGI series) | — | WGI is **revised**, not vintage; the revision caveat is stated in every report, and a sensitivity to the ±1-year variants is pre-registered. |
| **Linguistic distance** | the country-level "distance between a country's official language and English" measure published in S-44 | **Ordinal distance-from-English scale** built from the official-language status published by the UN/ISO 639, with English-official jurisdictions at 0 — registered here so the design is executable if the published index cannot be reproduced exactly from its source | Jurisdiction-constant; see §3.6 |

### 3.6 How the mandatory controls are *imposed* (frozen)

Because both controls are jurisdiction-constant, they are **absorbed** by the
within-jurisdiction specification (§3.4). To make the imposition operative rather than
merely absorptive, v1.1 additionally requires:

1. The **within-jurisdiction primary estimate is reported within pre-registered
   strata**: enforcement quality split at the panel median, and linguistic distance
   split at the panel median (high vs low distance). Each stratum's estimate is
   reported with its own cluster-robust inference, plus a pre-registered interaction
   test of state × stratum.
2. **Acceptance of the primary estimate requires that no single stratum carries the
   whole effect** (consistent with kill condition 5). A state effect that appears in
   one enforcement stratum and not the others is reported as a stratum-specific
   result and is **not** a pass.
3. The pooled estimate with and without the controls is reported side by side, so a
   reader can see whether the country-level controls are doing the work.

### 3.7 What v1.1 explicitly does *not* build

- **No group A / group B partition** (first-time vs second-time adopters), and none is
  presented as pre-registered — V-009 Cycle-56 amendment item 1; Cycle-111 correction
  notice. First-time adopters apply IFRS as a single package, so the contrast would
  degenerate into the historical first-time-versus-second-time comparison the literature
  has already populated (S-35, S-36).
- **No UK early-adopter cohort as an identification** — V-009 Cycle-56 amendment item 3
  (voluntary, self-selected, small effective sample, no window for the diffusion
  clock to run). The cohort is excluded from treatment (§1.1 rule 4).
- **No published firm-level repeat-adopter flag is assumed to exist** — V-009
  Cycle-110 resolution (R-058). Any firm-level first-application indicator used is
  **constructed from the firm's own prior-year basis-of-preparation note** and is
  pre-registered as a construction. In v1.1 such an indicator is used only as a
  pre-registered **secondary** analysis (a moderation of the mechanical accounting
  change), never as the treatment.
- **No IFRS 18 prospective arm A.** Its state cannot be constructed for this panel
  (the retrospective standards carried no mandated pre-adoption impact disclosure),
  and its G-33 dependency is unmet (2026 quantification rate **0 of 13** on a
  convenience sample; the ESMA-supervised population rate **not yet published** —
  S-50, S-51). The retrospective analogue is registered instead (§4.3).

---

## 4. Signal (exact rule) and the windows

### 4.1 Primary rule (transition window; two-sided; no sign chosen ex ante)

> At **T-A** (close of the adoption-announcement trading day; if the instrument was
> published after the venue close, the close of the next trading day), and within each
> event `(s, j)`, rank treated firms by pre-adoption information quality (low /
> high, at the within-jurisdiction median) and form two equal-notional legs:
> **long the low-information-quality leg, short the high-information-quality leg.**
> The direction of the *difference* is estimated two-sided: the pair is always long the
> information-poor adopter and short the information-rich adopter, and the reported
> estimand is the **sign of the spread**, not a chosen side.
> The **matched control-jurisdiction legs are traded identically** (same direction,
> same entry rule, same exit rule, matched on the same variables), so the reported
> portfolio return is the **differenced** return.
> Each position is exited at the close of **that firm's own T-R** (its first full
> report under the new standard). Exits are therefore staggered.
> No stop-loss, no discretionary override, no rebalancing inside the window, no
> compounding across events; if a firm has two qualifying events within 20 trading
> days, only the first is traded and the second is excluded (no double counting).

### 4.2 Pre-registered secondary rules (reported separately, never merged)

| Rule | Construction | Purpose |
|---|---|---|
| **SEC-1 (post-transition residual)** | Enter at **T-R**, exit at the close of **T-R + 20 trading days** or at the next earnings announcement under the new standard, whichever comes first. Same legs. | This is the **v1.0 H-B window**. It is the **post-transition** window and is demoted to a descriptive control by V-009 Cycle-58 item 2. Retained because it is the v1.0-frozen rule and because the decomposition is informative. |
| **SEC-2 (H-C / PEAD)** | Enter at **T-E1**, hold 60 trading days, with the earnings-surprise sign orienting the trade in the pre-registered PEAD direction, within the same information-quality split. | Pre-registered secondary outcome family (Holm–Bonferroni across H-A/H-B/H-C). |
| **SEC-3 (announcement/anticipation)** | The announcement window **[T-A−1, T-A+1]** and **[T-A−5, T-A+5]**, reported as the anticipation check (CH-1). | Mandatory reporting; the CH-1 kill condition is evaluated on it. |
| **SEC-4 (steady-state comparability)** | Post-transition information-quality and comparability measures (earnings quality, analyst forecast accuracy/agreement, liquidity) at T-R + 4 quarters and later. | **Descriptive control only.** May never be presented as support for the claim (V-009 Cycle-58 item 2; S-45 and S-46 are first-time-adopter-by-construction designs). |
| **SEC-5 (mechanical magnitude moderation)** | The firm's accounting-change magnitude, constructed from the **restated comparatives in the firm's own first report under the standard**, normalised as specified in §4.4. | CH-2 test. |

### 4.3 Pre-emption arm (kill signal, not a null) — Cycle-113, Cycle-114

> **W-PRE = [T-RI − 5 trading days, T-RI + 5 trading days]** — the window around the
> **first disclosure of the accounting break** (the firm's first interim report under
> the new standard).
>
> **A significant pre-event drift in W-PRE is reported as evidence that the
> slow-diffusion premise has already been consumed — a KILL SIGNAL for the candidate,
> not a null on the effect.** W-PRE sits inside the transition window, so the
> transition window is decomposed into W-PRE and the remainder; the decomposition is
> reported whether or not W-PRE is significant.
>
> **Note on the retrospective instance.** For the retrospective panel the standards
> carried **no mandated pre-adoption impact disclosure** (the IAS 8 ¶¶30–31 mandate
> that the dossier's IFRS 18 instance relies on did not exist in 2014–2019). The
> accounting break was therefore **not** disclosed in advance in a form that let the
> market anticipate its size. This is a structural difference between the retrospective
> instance and the IFRS 18 instance, and it is registered so that the pre-emption
> arm is evaluated on its own merits rather than assumed to have fired.

### 4.4 Mechanical accounting-change magnitude (frozen; CH-2)

For the standard in question, the magnitude of the change is quantified on **every
primary statement the standard changes**, never inferred from the statement of profit
or loss alone (V-009 Cycle-58 amendment item 1 requires the break to be quantified
wherever it is measured). Specifically:

| Standard | Statements changed | Pre-registered magnitude measure |
|---|---|---|
| IFRS 15 / ASC 606 | statement of profit or loss; statement of cash flows (working-capital movements) | \|change in reported revenue\| and \|change in reported profit from operations\|, each scaled by lagged total assets, from the restated comparatives in the firm's own first report |
| IFRS 16 / ASC 842 | statement of financial position (ROU asset and lease liability); statement of profit or loss (lease depreciation and interest); statement of cash flows (operating lease payments reclassified to financing) | \|change in total assets\|, \|change in reported EBITDA\|, and \|change in operating cash flow\|, each scaled by lagged total assets |
| IFRS 9 / ASU 2016-01 | statement of financial position (financial-asset classification and credit-loss allowance) | \|change in total assets\| and \|change in reported profit before tax\|, each scaled by lagged total assets |

Where a firm does not disclose the required comparatives, the magnitude is recorded as
**not constructible** and the firm is excluded from SEC-5 only (never from the
primary). The **count** of non-constructible magnitudes is reported.

---

## 5. Universe

Carried forward from v1.0 §5, widened to the registered panel.

- **Venues:** regulated markets in each registered jurisdiction (EU regulated markets,
  LSE and other UK regulated markets, US registered exchanges and OTC markets, and the
  venues of the registered Stratum-B jurisdictions), plus the venues of the matched
  control jurisdictions.
- **Security types:** common shares only. Excluded: funds, ETFs, REITs, SPACs, shell
  companies, preference shares, warrants, debt, and ADRs of non-primary listings
  (except where the ADR is the only listed line for a firm with a qualifying event).
- **Listing screen:** listed on the venue on or before `T-A − 250` trading days.
- **Liquidity screen (primary, unchanged from v1.0):** median daily traded value over
  the 60 trading days ending `T-A − 1` ≥ 1× the venue-specific screen (default
  1,000,000 currency units), with the screen fixed before the event panel is priced and
  reported per venue. **Pre-registered robustness:** the V-009 top-quintile-by-volume
  screen required by the V-009 target universe is reported as a pre-registered sub-sample.
- **Price screen:** closing price ≥ 1.0 currency unit on `T-A − 1`.
- **Point-in-time membership:** a firm is in the universe at T-A only if it was listed
  and not already delisted, suspended, or in bankruptcy proceedings on `T-A − 1`.
- **Delisted and failed firms are retained** in the event study and the portfolio
  simulation, with the actual delisting return and a documented delisting-loss
  assumption. **No survivorship filter** (kill condition 9).
- **Multiple share classes:** each class is a separate security; the firm is matched
  and clustered at the firm level.
- **Foreign listings and non-UTC venues:** daily prices converted using the venue's
  official close and the same-day FX rate; reporting currency is **not** converted to
  USD for accounting variables.
- **Exclusion of concurrent fundamental news (V-009 frozen rule):** a firm with a
  **scheduled** earnings announcement inside the event window `[T-A, T-R]` is excluded
  from the treated legs (scheduled reporting dates are knowable ex ante; unscheduled
  M&A and regulatory events are handled by the concurrent-event robustness, not by an
  ex-ante exclusion that cannot be applied honestly). The count of excluded firms and
  the reason is reported.

---

## 6. Entry and exit

- **Entry:** close of T-A, or the close of the next trading day if the instrument was
  published after the venue close (fixed rule, never by return inspection).
- **Permissible delay after disclosure:** at most 1 additional trading day, chosen by
  the fixed rule above.
- **Exit:** the close of that firm's own T-R (first full report under the standard).
  Staggered exits; positions are not rebalanced inside the window.
- **Maximum holding period:** 24 months from T-A (a bound, not a target; the realised
  hold is `T-R − T-A`).
- **Overlapping events:** only the first qualifying event for a firm within 20 trading
  days is traded; the second is excluded and the exclusion count is reported.
- **No intra-period trading, no compounding across events.**

---

## 7. Benchmark and estimand

### 7.1 Benchmark

**Market model** on daily returns, estimated on trading days **[T-A − 300, T-A − 46]**
— i.e. ending 45 trading days **before** the adoption announcement — with a minimum of
150 non-missing estimation days and a 20-trading-day buffer for corporate actions.

> **Clarification of a v1.0 wording defect.** v1.0 §7 wrote the estimation window as
> "[T-A−300, T-A−46] relative to T-R trading days (i.e. ending 45 trading days before
> T-R)", which is internally inconsistent. The v1.0 file is **not** edited; v1.1 pins
> the window unambiguously and anchors it on **T-A**, because in v1.1 the outcome window
> begins at T-A and an estimation window ending before T-R would overlap the outcome
> window.

**Abnormal return:** AR = r − (α̂ + β̂·r_market). The market model is the primary
benchmark; **FF5** (5 factors + momentum) and **DGTW characteristic-adjusted** returns
are pre-registered robustness benchmarks, never the primary.

### 7.2 Primary estimand (frozen)

> **τ** = the **difference-in-differences of state contrasts**, pooled across events:
>
> **τ = mean over events (s, j) of { [ BHAR_low − BHAR_high ] in treated
> jurisdiction j − [ BHAR_low − BHAR_high ] in the matched not-yet-treated control
> jurisdictions over the same calendar window } ,**
>
> where **BHAR(f)** is the buy-and-hold market-model abnormal return of firm `f` over
> its **transition window [T-A, T-R(f)]**, and BHAR_low / BHAR_high are the means over
> the low- and high-information-quality legs of the respective jurisdiction.

The transition window is inherently variable in length because firms have different
fiscal year ends. Three pre-registered devices make the comparison like-for-like:

1. **Fiscal-period-end proximity matching** of control firms (§3.2), so the control
   window has the same length as the treated window;
2. the **event-time monthly path** from event month −24 to +3 relative to T-R(f) is
   reported **in full** for every leg, so the reader sees the whole path rather than
   one number;
3. a **length-standardised secondary estimand**: the average monthly abnormal return
   over the transition window, reported alongside.

The **primary** estimand is the cumulative (buy-and-hold) form. The estimand is a
**conditional drift / treatment-effect contrast**, not a raw portfolio return; portfolio
net return is a downstream output (§9), never the primary test.

### 7.3 Inference (frozen)

- Standard errors clustered at the **(standard × jurisdiction × application year)** level,
  with a **wild-cluster bootstrap (Rademacher, 9,999 draws)** because the cluster count
  is small.
- Primary inference is also reported as a **randomisation test**: permute the
  information-quality label within event clusters (10,000 permutations).
- **Two-sided.** No sign is selected ex ante.

### 7.4 Secondary estimands (all pre-registered, reported separately)

| Window | Measure |
|---|---|
| SEC-1 | [T-R, T-R+20] (post-transition residual) — the v1.0 H-B window, descriptive |
| SEC-1a | [T-R, T-R+5] and [T-R+6, T-R+20] |
| SEC-3 | [T-A−1, T-A+1] and [T-A−5, T-A+5] (announcement / anticipation) |
| W-PRE | [T-RI−5, T-RI+5] (pre-emption — kill signal) |
| SEC-2 | [T-E1+2, T-E1+60] (H-C / PEAD) |
| CH-3 | the sign of the transition-window effect conditional on the contemporaneous announcement-window effect |
| CH-2 | the transition-window effect conditional on the mechanical accounting-change magnitude (§4.4) |

---

## 8. Risk controls

Estimated and reported: market, country, industry, size, value, momentum,
profitability, investment, liquidity, and analyst coverage. Event-cluster membership
is a fixed effect. The information-quality proxy is orthogonalised against size,
liquidity and coverage. The two **mandatory** country-level controls (enforcement
quality, linguistic distance) are imposed per §3.5–3.6.

Post-strategy factor attribution (FF5 and DGTW) is reported in full; an apparent
premium that is fully attributable to a known factor is reported as such and is a kill
condition if the sign flips when the factor is controlled.

**Pre-registered regime slices (reported, never used to select):** crisis vs calm;
high vs low market-wide volatility; **pre- vs post-2010** (mandatory per V-009,
because disclosure regimes changed); strong vs weak enforcement strata; high vs low
linguistic-distance strata; quarters containing macro shocks.

**Pre-registered ablations (reported, never used to select):**

| # | Ablation | Source |
|---|---|---|
| (a) | **Drop the state conditioning** and take the unconditional long position on affected firms. If the state adds nothing, the candidate is dead. | V-009 |
| (b) | Use information quality **alone**, without the country-level controls. Reported as the mandated companion to §3.4. | V-009 |
| (c) | Remove the concurrent-macro-shock exclusion, to quantify the confounder. | V-009 |
| (d) | **WITHDRAWN** — replace the enforcement regime with trade invoicing share or another country characteristic. | V-009 Cycle-52 item 2 (it is now the control, not the ablation) |

---

## 9. Costs (unchanged from v1.0 §9)

| Cost | Primary assumption | Conservative assumption |
|---|---|---|
| Commission | 1.0 bp per side | 2.0 bp per side |
| Half-spread | 5 bps | 10 bps |
| Market impact | 10 bps (per side, size-scaled) | 25 bps |
| Borrow fee (short leg) | 50 bps/year prorated over the holding period | 200 bps/year prorated |
| Financing (gross exposure) | cash rate + 0 bps | cash rate + 50 bps |
| Taxes | 0% (research; stated assumption) | 0% with explicit caveat |
| FX | venue close, same-day FX | same-day FX plus 10 bps |
| Delisting / bankruptcy | actual return, floored at −100% | −100% on failure events |

Because the v1.1 holding period is **quarters** rather than weeks, the following are
added as pre-registered requirements of the portfolio simulation: **borrow
availability and borrow fee for the short leg must be sourced or conservatively
assumed** (V-009: borrow can be scarce in small-cap names), and the position must be
sized as **a small fraction of the firm's typical daily volume** (V-009), with market
impact computed relative to the firm's own depth.

Turnover is computed from the frozen rule. **The break-even one-way cost is reported.**
Promotion requires a positive net return under the *conservative* column.

---

## 10. Acceptance and kill criteria

### 10.1 Acceptance (all must hold; otherwise the result is park/inconclusive, not a pass)

1. **Primary estimand:** the two-sided 95% confidence interval on τ excludes zero, and
   the point estimate is economically meaningful (|mean| ≥ 0.5% per event).
2. The sign is stable across all pre-registered windows and at least 2 of 3
   pre-registered benchmarks.
3. **Net-of-conservative-cost portfolio return** is positive in the pre-registered
   direction on the primary sample **and** on the chronological holdout.
4. The effect survives the pre-registered placebo set (placebo dates, placebo
   standards, placebo jurisdictions, unaffected split).
5. The result is **not driven by a single event, jurisdiction, firm, outlier or
   control stratum** (leave-one-event-out changes the point estimate by less than 50%;
   no single enforcement or linguistic-distance stratum carries the effect).
6. **Independent-event count ≥ 12** (standard × jurisdiction × application-year
   clusters) and **treatment-firm count ≥ 200**.
7. **Net-of-cost break-even cost exceeds the conservative cost assumption by at least
   2×.**
8. **The within-jurisdiction estimate exists and survives the mandatory
   country-level controls.** A result that appears only when the enforcement and
   linguistic-distance controls are omitted is a **fail**.

### 10.2 Kill criteria

The ten kill conditions of `research/hypothesis.md` v1.0 §6, carried forward unchanged,
plus the three added in `research/hypothesis_v1.1.md` §7 (kill conditions 11–13):
country-level artefact, pre-emption consumed, and the state conditioning adding
nothing after costs.

**Kill condition 9 (point-in-time replication impossible) is live for this campaign**:
with a survivorship-filtered price panel it fires by construction, which is why
`research/data_route_assessment.md` §6.3 records the fallback as a systematic erosion
of the treatment arm rather than a neutral loss of power.

---

## 11. Anti-peeking and change control (frozen)

- The **transition-window pre-registration** (this file, §4.1–4.3) and the
  **presentation-surface attribution** (§4.4) are fixed **before the holdout is opened**,
  and any change to them is logged with a date and a reason (V-009 Cycle-52 item 5,
  Cycle-58 item 5).
- An explicit **count of every (state definition × exit rule × jurisdiction ×
  sub-sample) combination examined** is maintained and reported, and every rule change
  is logged with a date and a reason.
- No threshold, sign, universe, window, or exit rule is selected after inspecting
  holdout returns. The v1.0 file is never edited; a change means a **new registered
  version** recorded in `research/prompt_changelog.md`.

## 12. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Frozen ten elements. Treatment definition produced an empty treatment group across the frozen universe (D-009). |
| **v1.1** | **2026-10-22** | Executable treatment (jurisdiction-level standard application with a within-jurisdiction firm-level state), staggered-timing panel with a registered membership rule and two strata, mandatory enforcement and linguistic-distance controls with a three-part imposition, transition-window primary rule with announcement and first-report exits, pre-emption kill-signal arm, mechanical-magnitude attribution across all three primary statements, disambiguation of the benchmark estimation window. Registered **before** any outcome-period return was computed. |

# ACCTCLOCK — Strategy Specification v1.2 (prospective holdout arm PH-1)

Registered: 2026-10-22
Supersedes: nothing. `research/specification_v1.1.md` (2026-10-22) remains **in
force** for the retrospective panel. This file specifies **one added arm**, PH-1,
and changes **no** element of v1.1. Recorded in `research/prompt_changelog.md`
(Iteration 9).

Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`
(v1.0, 2026-10-21).
Binding design constraints: the canonical hypothesis-factory dossier, specification
**V-009 (IDEA-011 ACCTCLOCK)**, in particular Cycle-56 amendment item 4 (a
prospective holdout must be registered before the outcome can occur), Cycle-113
amendment item 2 (a pre-adoption disclosure window is a **kill signal**), and
Cycle-114 amendment item 2.

Status: **Pre-registered, untested.** No outcome-period return has been computed or
inspected in this repository, for the retrospective panel or for PH-1.

**Reading note.** Sections numbered §1–§12 exist here **only** where PH-1 needs
them. Where PH-1 inherits a v1.1 rule unchanged, this file says so **by reference**
rather than restating it, because a restatement is a copy that can drift. The
governing text for every inherited rule is `research/specification_v1.1.md`.

---

## 0. What this version adds, and what it does not touch

**Adds.** One arm: **PH-1**, the IFRS 18 first-application window (the 2027 interim
reporting season, periods ending 30 June 2027, reports published July–August 2027).

**Does not touch.** The retrospective panel, its membership rule (§1.1 of v1.1), its
event clock, its treatment, state and control definitions, its windows, its
benchmark and estimand, its costs, its thresholds and its acceptance criteria.

**What is new in substance, and why it matters.** The retrospective panel could only
register a *retrospective analogue* of the pre-emption arm, because the retrospective
standards carried no mandated pre-adoption impact disclosure. IFRS 18 carries one:
ESMA's public statement requires issuers to disclose the nature and, where known or
reasonably estimable, the impact of the impending accounting change under IAS 8
paragraphs 30 and 31 (S-49). PH-1 therefore has a **real, dated, mandated
pre-disclosure window**, and the pre-emption kill signal becomes a first-class
test rather than an analogue.

**What is deliberately absent.** No adopter-type contrast, no pooling of the four
IFRS 18 population statistics, and no claim that the retrospective panel's result
transfers.

## 1. PH-1 target events and the PH-1 panel

### 1.1 PH-1 panel membership rule (frozen, evaluated before any return is computed)

**Inherits v1.1 §1.1 by reference, with two changes that follow from IFRS 18's own
facts.**

An event (standard s, jurisdiction j) is in the PH-1 panel if and only if **all
five** of the following hold. They are checked in order, and each check is recorded.

1. **s = IFRS 18.** One standard. No other standard enters PH-1.
2. **j's regulator has published a legal instrument making IFRS 18 mandatory for a
   class of listed firms**, with a **day-level publication date**. IFRS 18 is in
   force in the EU (Commission Regulation (EU) 2026/338), the UK (UK Endorsement
   Board) and Saudi Arabia (CMA announcement CMA_N_4083), and the instrument dates
   are recorded in `research/hypothesis_v1.2.md` §5.
3. **The affected-firm list is knowable ex ante** from the IFRS Foundation
   jurisdiction profiles (S-47, S-58) or from j's own published scope definition.
4. **j has a public filing route that publishes a filing acceptance time** — a
   *timestamp*, not only a date. **Unchanged from v1.1; not one single UK or EU
   route has yet been confirmed to satisfy this, and it is the single most
   important open item for PH-1.**
5. **Point-in-time price coverage** exists for j's listed firms, including firms
   subsequently delisted.

**Changes from v1.1 §1.1, and why each is forced rather than chosen.**

- **The first-time-framework-adopter question is settled in advance, in the negative,
  for IFRS 18.** v1.1 §1.2 admitted Stratum B by rule and left the *event type*
  open. For IFRS 18 it is not open: the IFRS 18 endorsement instruments converge on
  a single application date, and jurisdictions that adopt IFRS for the first time in
  the IFRS 18 era apply the IFRSs "all at once" (S-54). A first-time-versus-
  second-time contrast therefore **degenerates** and is **not built**. The PH-1
  panel is **Stratum A only in event type** (a content change inside an existing
  framework), with the framework-change reading explicitly unavailable.
  *Consequence, stated plainly:* this removes the design's strongest claim
  (v1.1 §3 hypothesis, P2) from PH-1. PH-1 is a **weaker, narrower** test. It is
  registered anyway, because a narrower honest test is better than a broad
  unregistered one, and because the pre-emption channel is *stronger* here.
- **The jurisdiction universe is not frozen at the EU/UK/US.** v1.1's universe
  cannot be carried over (it was **not executable** — D-009), and IFRS 18's
  adoption extends beyond it. The universe is therefore the **panel rule applied
  to the jurisdictions the IFRS 18 instruments reach**, with conditions 3–5 checked
  per jurisdiction.

### 1.2 The PH-1 panel, as registered

**Not yet enumerated.** The PH-1 panel file is `research/panel_v1.2.csv`, and it
**must be written before the PH-1 feasibility audit begins** and before the arm is
run. It will contain one row per (IFRS 18, jurisdiction) admitted by the rule
above, with the same schema as `research/panel_v1.1.csv` and the same three-state
`in_registered_panel` discipline (**true** / **false** / **pending**).

The rows that are known at registration time, with their day-level anchors, are:

| Jurisdiction | Instrument | T-A | T-E | Panel status |
|---|---|---|---|---|
| European Union | Commission Regulation (EU) 2026/338 | 2026-02-13 (OJ 2026-02-16) | periods beginning on/after 2027-01-01 | pending conditions 3–5 |
| United Kingdom | UK Endorsement Board adoption of IFRS 18 | **day-level decision date to be pinned from the UKEB's own decision record** | periods beginning on/after 2027-01-01 | pending conditions 3–5 |
| Saudi Arabia | Saudi CMA announcement CMA_N_4083 | 2026-06-30 | periods beginning on/after 2027-01-01 | pending conditions 3–5 |

**The UK T-A is the first concrete task of the next phase** and is recorded in
`research/authorisation_request.md` and in the handoff.

### 1.3 Rationale for the PH-1 panel

Unchanged in form from v1.1 §1.3 (the affected population must be knowable ex ante;
the event must be a *legal* change with a *published* instrument; the route must
publish a timestamp). The additional reason specific to PH-1: a prospective holdout
is only untamable if the panel membership is fixed **before** the first report is
published, and that is now possible because the instruments are already dated.

## 2. Event clock for PH-1

**Inherits v1.1 §2 and §5 by reference, unchanged.** The same four usable
timestamps, the same pre-registered announcement-clock rule (T-A is the
jurisdictional legal-adoption date; T-A1 is the standard-setter issuance date,
**9 April 2024** for IFRS 18; both recorded and reported; conflicts recorded, never
silently resolved — D-011), and the same prohibition on selecting the date that
maximises any return.

**One addition.** For PH-1 the **pre-emption window** has a *mandated* disclosure
with its own date. It is:

> **T-PRE** = the filing acceptance time of the firm's **first disclosure of the
> nature and, where known or reasonably estimable, the impact of the impending
> IFRS 18 accounting change**, made under IAS 8 paragraphs 30 and 31 and required
> of issuers by ESMA's public statement (S-49).

T-PRE is the pre-emption window's anchor. It is computed from the filing route's
acceptance timestamp exactly as T-R is, and it is **a kill signal, not a null**
(v1.1 §4.3; kill condition 12).

**T-RI for PH-1** is the first interim report published under IFRS 18, i.e. the
report for the period ending 30 June 2027, published July–August 2027.

## 3. Treatment, state and controls for PH-1

**Inherits v1.1 §3 by reference, unchanged, in every particular:**

- **§3.1 treatment** — jurisdiction-level standard application, with the
  not-yet-treated matched control group;
- **§3.2 control group** — matched on fiscal-period-end proximity, as in v1.1;
- **§3.3 state** — firm-level pre-adoption information quality, constructed from
  the firm's **own** prior-year basis-of-preparation note and pre-registered as a
  construction, never treated as published;
- **§3.4 identifying requirement** — within jurisdiction;
- **§3.5 and §3.6 mandatory controls** — enforcement quality and linguistic
  distance, imposed in three parts;
- **§3.7 what is not built** — no adopter-type partition, no UK early-adopter
  cohort as an identification, no published firm-level repeat-adopter flag.

**Two PH-1 specifics, both mechanical.**

1. **The state's construction window.** The pre-adoption state is measured on the
   **last report published before T-A**, which for IFRS 18 is the FY2025 or FY2026
   report depending on the jurisdiction's reporting calendar. If the state window
   and the pre-disclosure window overlap, the overlap is **declared** in the
   write-up, because a firm that discloses its expected IFRS 18 impact and is
   then measured on information quality drawn from that same disclosure is
   mechanically different.
2. **The linguistic-distance measure.** The published measure (S-44) is used **if it
   can be reproduced exactly from its source**; otherwise the registered fallback
   ordinal scale is used. **The choice must be recorded before the holdout is
   opened**, i.e. before the first IFRS 18 report is published. It is currently
   **unresolved** and is an open item carried from v1.1.

## 4. Signal and windows for PH-1

**Inherits v1.1 §4 by reference, unchanged, with the pre-emption arm re-anchored.**

- **§4.1 primary rule** — the transition window [T-A, T-R], two-sided, no sign
  chosen ex ante, computed on the v1.1 benchmark and estimand;
- **§4.2 secondary rules** — reported separately, never merged;
- **§4.3 pre-emption arm** — for PH-1 the pre-emption window is [T-A, T-PRE]
  where T-PRE is defined in §2 above, and a significant drift in it is a **kill
  signal**;
- **§4.4 mechanical accounting-change magnitude** — unchanged, and quantified on
  all three primary statements where IFRS 18 changes them.

**PH-1 additions to the reported decomposition.**

- **D1. Pre-disclosure versus post-disclosure decomposition.** The transition
  window is split at T-PRE and both parts are reported, for the treated firms and
  for the matched controls. This is **mandatory** in the write-up whatever the
  result (v1.2 hypothesis P7, CH-10).
- **D2. Disclosure-quality split.** Because the population statistics show the
  mandated disclosure is frequently non-specific and rarely quantified (S-50, S-51),
  the treated set is **also** split by the *specificity* of the firm's own
  pre-disclosure (company-specific quantified impact / company-specific unquantified
  / standardised or absent). This split is **descriptive and pre-registered**, not a
  second identification, and it is reported with the three groups named in advance.
  It is **not** pooled with the four population statistics the arm-A non-pooling
  rule forbids pooling.

## 5. Universe for PH-1

**Inherits v1.1 §5 by reference, with the panel replaced by the PH-1 panel of §1.2.**
The liquidity screen, the price screen, the delisting treatment and the point-in-time
price construction are unchanged.

**One PH-1 addition.** The pre-disclosure document (IAS 8.30/.31) is a **filing**
and therefore enters the manifest and the hash chain exactly as a financial report
does. It is an input to D1 and D2 and must be retrievable and verifiable after the
fact.

## 6. Entry and exit for PH-1

**Inherits v1.1 §6 by reference, unchanged:** enter at T-A, exit at the firm's own
first full post-adoption report (T-R), with the v1.0 rule retained as the
pre-registered secondary rule. For PH-1, T-R is the FY2027 annual report for
December-year-end filers and the corresponding annual report for other calendars,
and T-RI is the interim report for the period ending 30 June 2027.

## 7. Benchmark and estimand for PH-1

**Inherits v1.1 §7 by reference, unchanged, in every particular:** the same market
model, the same estimation windows, the same primary estimand (the within-jurisdiction
difference in transition-window buy-and-hold abnormal return between low- and
high-information-quality firms, differenced against the same contrast in matched
control jurisdictions over the same calendar windows), the same cluster-robust
inference, and the same secondary estimands.

**One PH-1 addition.** The primary estimand is reported **alongside** D1, and the
report must state which of the two readings the data supports:
(i) a **slow-diffusion** reading (the response follows the first full report under
the new standard) or (ii) a **disclosure** reading (the response is concentrated in
or before the mandated pre-disclosure). The report **may not** choose a reading
after seeing which one is larger; it reports both, with the decomposition, and
states the conclusion the decomposition supports.

## 8. Risk controls for PH-1

**Inherits v1.1 §8 by reference, unchanged.**

## 9. Costs for PH-1

**Inherits v1.1 §9 by reference, unchanged.** No cost was tuned; no return exists.

## 10. Acceptance and kill criteria for PH-1

**Inherits v1.1 §10 by reference, unchanged, with two additions.**

- **Addition 1 (the holdout discipline).** The PH-1 result is reported **once**.
  Nothing about the PH-1 outcome may be inspected, computed, or reported before the
  analysis is run under the registered order in `research/preregistration_v1.2.md`.
  A single peek voids the arm, and a voided arm is reported as void, not as a null.
- **Addition 2 (arm-specific minimums).** The PH-1 feasibility audit must report at
  least **12 clusters** and at least **200 treatment firms**, exactly as for the
  retrospective panel. Below those minima the PH-1 primary estimand is
  **inconclusive by construction**, and the report says so instead of reporting a
  noisy estimate. This is frozen in advance so that a short arm cannot later be
  used to justify a design change.

**Kill condition 12 (pre-emption consumed)** applies to PH-1 with its **real**
disclosure anchor T-PRE, and a significant pre-disclosure drift is a kill signal.

## 11. Anti-peeking and change control for PH-1

**Inherits v1.1 §11 by reference, unchanged.** The panel, the window, the
thresholds, the exit rules, the cost table and the acceptance criteria are frozen;
a change means a **new registered version** in `research/prompt_changelog.md`,
never an edit in place. v1.0 and v1.1 are immutable and are not edited by this
file.

**The deadline that makes PH-1 a holdout.** This file, `research/hypothesis_v1.2.md`
and `research/preregistration_v1.2.md` are registered on **2026-10-22**, before any
IFRS 18 report can be published (the first is the interim report for the period
ending 30 June 2027, published July–August 2027). **After the first IFRS 18 report
is published, no element of the PH-1 design may be changed in place**; a change
would be a new registered version and would be reported as a post-hoc amendment.

## 12. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Original frozen specification; empty treatment group (D-009). |
| v1.1 | 2026-10-22 | Executable design: registered panel rule, within-jurisdiction identification, mandatory controls, transition-window signal, pre-emption arm. |
| **v1.2** | **2026-10-22** | Adds the **PH-1 prospective holdout arm** for IFRS 18: a **mandated** pre-disclosure anchor **T-PRE** from the IAS 8.30/.31 impact disclosure (S-49), the mandatory pre-/post-disclosure decomposition, the disclosure-specificity descriptive split, the slow-diffusion-versus-disclosure reading rule, the once-only reporting discipline, and the arm-specific ≥12-cluster / ≥200-firm minima. Settles the IFRS 18 adopter-type contrast in advance, in the negative (S-54). **No element of v1.1 is changed.** |

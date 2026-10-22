# ACCTCLOCK — Hypothesis v1.1

Registered: 2026-10-22
Supersedes: `research/hypothesis.md` v1.0 (2026-10-21). **v1.0 is immutable and remains
in force as the historical record.** This file is a *new* registered version, created
before any outcome-period return was computed or inspected in this repository, and
recorded in `research/prompt_changelog.md` (Iteration 8).

Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`
(v1.0, 2026-10-21).
Binding design constraints: the canonical hypothesis-factory dossier, specification
**V-009 (IDEA-011 ACCTCLOCK)**, retrieved read-only at commit
`1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` on 2026-10-22 — amendments Cycle-52,
Cycle-56, Cycle-58, the Cycle-111 correction notice, Cycle-113, Cycle-114, Cycle-123
and Cycle-126. Local ledger reference: `research/source_ledger.csv` **S-37**; the
underlying sources are now recorded locally as **S-42 … S-54**.

Status: **Pre-registered, untested.** No outcome-period return has been computed in
this repository. Nothing in this file is evidence that an edge exists.

---

## 0. Why v1.1 exists (the defect it repairs)

`research/specification_v1.md` v1.0 §3 defines treatment as *first-time adopters of the
standard: firms whose reporting framework changed at the event*. Applied to the frozen
universe of v1.0 §5 (EU, UK, US) this yields **zero firms**: the EU and the UK were
already on IFRS when IFRS 15/9/16 took effect, and ASC 606/842 are *inside* US GAAP.
The v1.0 primary estimand is therefore undefined (decision **D-009**, ledger row
**E-010**). v1.1 replaces the treatment definition with an implementable one; it does
**not** weaken the claim, and it does **not** touch any threshold, window, cost, or
acceptance criterion that is carried forward from v1.0.

## 1. The claim (one sentence)

**Around the application of a new accounting standard in a jurisdiction, the market
incorporates the standard's consequences over the transition window — from the public
adoption announcement to the firm's first full report prepared under the new standard
— and firms with lower pre-event information quality exhibit a different
transition-window abnormal-return path than comparable firms with higher pre-event
information quality, *within jurisdiction*, after mandatory enforcement and
linguistic-distance controls; and this difference is large enough, persistent enough and
distinct enough from costs to survive a point-in-time, out-of-sample test.**

The claim remains **two-sided**. No sign is selected before the holdout is opened.

## 2. What changed relative to v1.0, and what did not

| Element | v1.0 | v1.1 | Reason |
|---|---|---|---|
| Primary outcome family | H-B, defined as the post-first-report window [T-R, T-R+20] | **H-B′**, defined as the **transition window** [T-A, T-R] — the drift between the adoption announcement and the first full post-adoption report | V-009 Cycle-58 amendment item 2: the hypothesis under test **must** be pre-registered as a transition-window effect. The v1.0 [T-R, T-R+20] window is the *post-transition* window and is demoted to a **descriptive control**. |
| Treatment definition | "firms whose reporting framework changed at the event" | **Jurisdiction-level standard application**, with the firm-level state = pre-adoption information quality, estimated **within jurisdiction** | v1.0 treatment is empty (D-009). V-009 Cycle-52 amendment item 1 requires a **firm-level** state with identifying power *within* jurisdiction. |
| Enforcement quality | optional *competing conditioner* interacted with the state | **mandatory control** imposed on every arm; the state contrast must survive it | V-009 Cycle-52 amendment item 2; Cycle-113 amendment item 1 (S-52). The candidate **may not claim** the enforcement effect as its own. |
| Linguistic distance | absent | **mandatory control** | V-009 Cycle-52 amendment item 2 (S-44). |
| Which published reading is claimed | not stated | **discontinuity-at-adoption** reading claimed; comparability-as-driver reading reported as a descriptive control | V-009 Cycle-52 amendment item 3 (S-42). |
| Steady-state comparability | not distinguished | **descriptive control only**, never support for the claim | V-009 Cycle-58 amendment item 2 (S-45, S-46). |
| Pre-emption / hard-stop arm | absent | **registered**: event-window returns around the first disclosure of the accounting break are a **kill signal**, not a null | V-009 Cycle-113 amendment items 2 and 4; Cycle-114 amendment item 2. |
| UK early-adopter cohort | the only in-universe contrast | **rejected as an identification**; not used | V-009 Cycle-56 amendment item 3. |
| Group A / group B first-time-vs-second-time partition | implicit in "first-time adopters" | **not built, and not presented as pre-registered** | V-009 Cycle-56 amendment item 1; Cycle-111 correction notice. |
| Firm-level repeat-adopter flag | treated as if published | **not treated as published**; any such flag must be constructed from the firm's own prior-year basis-of-preparation note and pre-registered as a construction | V-009 Cycle-110 resolution (R-058). |
| Information-quality proxy | absolute discretionary accruals (Jones), median split within jurisdiction-year | **unchanged** | Carried forward from v1.0 §3. |
| Event clock (T-A, T-E, T-R, T-E1) | four timestamps, never conflated | **unchanged**; the *announcement* clock is pinned by a pre-registered rule (see §5) | v1.0 §2 was already correct. |
| Entry/exit rule | enter at T-R, exit T-R+20 or next earnings | **changed**: enter at the adoption announcement (T-A), exit at the firm's own first full post-adoption report (T-R) — with the v1.0 rule retained as the pre-registered secondary rule | V-009 frozen conceptual rules (position and exit). |
| Universe, liquidity/price screens, delisting treatment | as v1.0 §5 | **unchanged**, widened to the registered jurisdiction panel | v1.0 §5 was not the defect. |
| Benchmark (market model) and estimation windows | as v1.0 §7 | **unchanged in form**, re-anchored on the transition window | — |
| Risk controls | as v1.0 §8 | **unchanged**, plus the two mandatory country-level controls | V-009. |
| Costs | as v1.0 §9 | **unchanged** | No cost was tuned; no return exists. |
| Acceptance criteria | as v1.0 §10 and `research/preregistration.md` §4–7 | **unchanged in substance**, restated in `research/preregistration_v1.1.md`; the ≥12-cluster and ≥200-firm minima are retained | Tightening, never loosening. |

## 3. Mechanism (why it might exist)

1. A new accounting standard changes reported numbers (revenue timing under IFRS 15 /
   ASC 606, lease capitalisation under IFRS 16 / ASC 842, financial-instrument
   classification and credit-loss measurement under IFRS 9 / ASU 2016-01). The change
   is larger the less comparable the firm's prior framework was to the new standard.
2. Where the market's pre-existing knowledge is thinner — lower pre-event information
   quality — the revision of beliefs required to interpret the new numbers is larger
   and is incorporated more slowly.
3. If the market prices the standard's *existence* at announcement but prices the
   *realised* accounting change only as it is reported, the residual is a
   slow-information-diffusion premium concentrated in low-information-quality firms and
   visible in the **transition window** running from the adoption announcement to the
   first full post-adoption report.

## 4. Competing and counter hypotheses (carried forward and extended)

- **CH-1 (anticipation).** The information is fully priced at the announcement (T-A).
  *Kill condition.* Decomposition required: announcement window vs the remainder of the
  transition window.
- **CH-2 (mechanical accounting change).** The transition-window return is a mechanical
  consequence of re-measurement (e.g. lease capitalisation) rather than slow diffusion.
  *Test:* control for the mechanical size of the accounting change, measured on **all
  three primary statements** where the standard changes them (Cycle-58 amendment item 1:
  the break must be quantified where it is measured, never inferred from the statement
  of profit or loss alone).
- **CH-3 (reversal).** The transition-window return is a reversal of the announcement
  reaction rather than diffusion. *Test:* the transition-window effect must be opposite
  in sign to the contemporaneous announcement effect for the same firms, and must vanish
  when announcement-window abnormal returns are controlled for.
- **CH-4 (generic small-firm / liquidity / momentum exposure).** The information-quality
  proxy proxies for size, illiquidity, low coverage or momentum. *Test:* matched controls
  and factor controls; the estimate is differenced against a matched control-jurisdiction
  calendar.
- **CH-5 (concurrent events).** The window overlaps earnings announcements, index
  changes or other reforms. *Test:* exclude windows with concurrent fundamental news
  (the V-009 frozen rule) and run placebo dates.
- **CH-6 (anomaly decay).** The effect existed historically but has been arbitraged away
  and never existed in large caps (S-09, S-10, S-21).
- **CH-7 (non-specific to standards).** Any large accounting change produces the same
  path. *Test:* placebo standards and placebo adoption events.
- **CH-8 (country-level artefact).** The apparent effect is produced by cross-jurisdiction
  differences in enforcement or language rather than by the firm-level state.
  *Kill condition.* V-009 Cycle-52 pass/fail additions: a result that survives **only**
  when the mandatory country-level controls are omitted is a **fail**; the
  within-jurisdiction estimate must be reported separately from the pooled one.
- **CH-9 (pre-emption).** The accounting break was disclosed in advance in a form that
  let the market anticipate it. *Kill signal, not a null* (Cycle-113 amendment items 2
  and 4): a significant pre-event drift in the pre-emption window is reported as
  evidence that the slow-diffusion premise has already been consumed.

## 5. Event clock (unchanged in structure; the announcement clock is pinned here)

| Clock | Definition | v1.1 use |
|---|---|---|
| **T-A** | **Adoption announcement** = the date the jurisdiction's legal adoption instrument for the standard was published (for a jurisdiction that applies the standard without a separate endorsement instrument, the standard-setter's issuance date of the instrument that makes it mandatory). | Primary entry timestamp; start of the transition window. |
| **T-A1** | **Standard issuance** = the date the standard setter issued the standard. | Pre-registered secondary anticipation window and the pre-registration of the announcement-clock choice. |
| **T-E** | Effective date (first fiscal year beginning under the standard). | Alignment/filtering only; never a trading date. |
| **T-R** | **First full report published under the new standard** (filing-system acceptance time, UTC). | Primary exit timestamp; end of the transition window. |
| **T-RI** | **First interim report published under the new standard** (acceptance time, UTC). | Pre-emption / first-disclosure-of-the-break window (kill signal). |
| **T-E1** | First earnings announcement under the new standard. | H-C secondary entry timestamp. |

**Pre-registered announcement-clock rule (resolves V-009 ambiguity 1 and the recorded
date conflicts).** T-A is the **jurisdictional legal-adoption** date. T-A1 is the
**standard-setter issuance** date. Both are recorded for every event and both are
reported. Where the two primary sources disagree (e.g. IFRS 9 issuance recorded as
24 July 2014 in the EU Regulation recital and 25 July 2014 elsewhere), the date stated
in the **jurisdiction's own adoption instrument** is used for T-A, and the conflict is
recorded, never silently resolved. The date that maximises any return is never selected
(decision **D-011**).

**Justification for choosing T-A over T-A1.** The affected-firm list must be knowable
ex ante (V-009 ambiguity 6, the binding data constraint). The jurisdiction's adoption
instrument is what makes the obligation and the affected population public; the
standard-setter's issuance date is prior to that and does not identify the affected
jurisdiction. T-A1 is reported as a pre-registered anticipation window.

## 6. Pre-registered predictions

- **P1** The within-jurisdiction difference in transition-window buy-and-hold abnormal
  return (low minus high pre-adoption information quality), differenced against the
  same contrast measured in matched control jurisdictions over the same calendar
  windows, is non-zero at the event-cluster level, with the two-sided 95% confidence
  interval excluding zero.
- **P2** The effect is materially larger in the **framework-change** stratum
  (jurisdictions applying IFRS for the first time, where pre-IFRS differences are
  largest) than in the **content-change** stratum (already-IFRS jurisdictions applying
  a new standard), and is absent or materially smaller in placebo-standard events.
- **P3** The effect survives controls for size, industry, liquidity, momentum,
  profitability, investment, analyst coverage, the mechanical size of the accounting
  change, and the **mandatory** enforcement-quality and linguistic-distance controls.
- **P4** The net-of-cost return is positive in the economically justified direction on
  the subset where the gross effect is largest, and the break-even cost is above a
  conservative institutional estimate.
- **P5** Placebo adoption dates, placebo standards, placebo jurisdictions and
  unaffected information-quality splits produce no comparable effect.
- **P6** The effect is not driven by a single jurisdiction, standard, firm or outlier,
  and the independent-event count supports cluster-robust inference.

## 7. Kill conditions (any one is sufficient to park or reject)

Carried forward unchanged from v1.0 §6 (all ten), **plus**:

11. **The within-jurisdiction estimate does not exist or is not identified once the
    mandatory enforcement-quality and linguistic-distance controls are imposed** — i.e.
    the result survives only because the country-level controls are omitted
    (V-009 Cycle-52 pass/fail additions; CH-8).
12. **A significant pre-event drift in the pre-emption window** (the first disclosure of
    the accounting break, T-RI) shows the slow-diffusion premise was already consumed
    before the transition window opened (V-009 Cycle-113 hard-stop condition 3;
    Cycle-114 amendment item 2). This is a **kill signal, not a null**.
13. **The state conditioning adds nothing after costs** — the ablation in which the
    state is dropped and the unconditional affected-firm position is taken shows the
    same result (V-009 ablation (a); V-009 kill criteria).

## 8. What v1.1 does **not** claim, and why

- **No group A (first-time adopters) / group B (second-time adopters) partition is
  built**, and none is presented as pre-registered. V-009 Cycle-56 amendment item 1 and
  the Cycle-111 correction notice: first-time adopters apply IFRS as a single package,
  so the contrast degenerates into the historical first-time-versus-second-time IFRS
  comparison the literature has already populated (S-35, S-36). The v1.1 design
  identifies the effect from **staggered application timing** and a **within-jurisdiction
  firm-level state contrast**, never from a binary adopter partition.
- **The UK early-adopter cohort is not used as an identification.** V-009 Cycle-56
  amendment item 3: the treatment arm is voluntary and self-selected, the effective
  sample is the number of early adopters, and the early arm announces its statements
  together with their effect, so the diffusion clock has no window to run.
- **No published firm-level repeat-adopter flag is treated as available.** V-009
  Cycle-110 resolution (R-058): the IASB's 2005 early-adopter list could not be
  located. Any firm-level first-application indicator used in v1.1 is **constructed
  from the firm's own prior-year basis-of-preparation note** and is pre-registered as a
  construction.
- **The IFRS 18 prospective arm A is not used.** It is scoped to IFRS 18; its G-33
  dependency is unmet (the 2026 season's quantification rate is **0 of 13** on a
  convenience sample, and the ESMA-supervised population rate is **not yet published**,
  per S-50, S-51, S-49); and the retrospective standards in the v1.1 panel were **not**
  subject to a mandated pre-adoption impact disclosure, so the arm's state cannot be
  constructed for this panel at all. The **retrospective analogue** of the pre-emption
  arm — the first disclosure of the accounting break at T-RI — is registered instead.
- **Enforcement quality and linguistic distance are not claimed as this campaign's
  effect.** They are published conditioners (S-43, S-44, S-52); the campaign's claim
  is the firm-level, within-jurisdiction residual after they are imposed.

## 9. Evidence status of this hypothesis

Unchanged from v1.0 §7 and restated here because it governs interpretation:

- **Published mechanism evidence (A):** adoption events move prices, and the reaction
  is stronger for low pre-adoption information quality and weaker in weak-enforcement
  regimes — Armstrong, Barth, Jagolinzer and Riedl (2010), S-01. Mandatory adoption
  improves cross-country comparability (S-02, S-03). Mandatory disclosure changes
  produce measurable slow-diffusion effects (S-21).
- **Published counter-evidence (A):** the drift family has decayed sharply and has
  been argued to be non-existent for large caps since ~2006 (S-09, S-10, S-11); it is
  explained away by transaction costs (S-12); it is partly an artefact of portfolio
  aggregation (S-13); a structurally similar announcement premium fell from ~7.6% in
  the 1990s to ~0.8% in the past decade (S-20).
- **Published confounders that are now mandatory controls (A):** enforcement quality
  moderates the effect (S-43, and S-52 at 65% mediation / 73% larger in
  high-enforcement jurisdictions); linguistic distance flips the sign in severe
  language-barrier jurisdictions (S-44).
- **Published systematic prior (A):** IFRS adoption's market effects are real but
  "accounting quality and comparability do not mediate the market effects", with the
  positive findings attributed to IFRS' mandatory nature and pre-IFRS differences
  compared to local standards — the *discontinuity at adoption* reading (S-42).
- **Published nulls / reversals in the family (A):** K-IFRS adoption **reduced** PEAD
  in Korea (S-35); IFRS adoption **increased** PEAD in Greece (S-36). First adoption
  does not predict the sign.
- **The comparator the design rests on is unrun by the field (A):** the
  first-time-versus-second-time-adopter comparison **on drift** has not been run
  (S-37 / V-009 G-21). A null in this design is a **contribution, not a replication**.
- **Candidate-specific evidence (B):** none. No ACCTCLOCK event study, portfolio
  simulation or backtest has been run.
- **Strategy evidence (C):** none.
- **Assumptions (D):** the "lower information quality implies slower diffusion" link
  remains a conjecture drawn from the general slow-diffusion literature. It has not
  been verified for accounting-standard adoption.

## 10. Current blocker (documented, not a conclusion)

The design in this file is executable **in principle**. It is **not yet executable in
this environment**, for reasons that are *not* defects of the design:

1. **No market data with delisted securities.** Prices for the registered jurisdictions
   (including the framework-change jurisdictions outside the EU/UK/US) are not available
   without an authorised paid subscription. See `research/data_route_assessment.md` §6.5
   and `research/data_acquisition_plan.md`.
2. **No filing harvest.** T-R and T-RI (filing-system acceptance times in UTC) and the
   as-published accounting items have not been collected; read-only harvesting of SEC
   EDGAR and the national OAMs is not yet authorised.
3. **Enforcement and linguistic-distance series are not yet assembled** at the required
   vintage and granularity.

These are **data and authorisation limitations, not evidence for or against the
hypothesis**, and they do not license any result. The campaign status remains
**PARKED — not validated, not rejected.**

## 11. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Original frozen claim. Treatment definition produced an **empty** treatment group across the frozen universe (D-009); the outcome was defined as the post-first-report window rather than the transition window. |
| **v1.1** | **2026-10-22** | Executable, dossier-compliant treatment definition; transition-window claim; mandatory enforcement and linguistic-distance controls; discontinuity-at-adoption reading claimed; pre-emption kill-signal arm registered; UK early-adopter cohort and the group A/B partition both rejected as identifications; entry/exit rule moved to the announcement → first-full-report transition window. Registered **before** any outcome-period return was computed. |

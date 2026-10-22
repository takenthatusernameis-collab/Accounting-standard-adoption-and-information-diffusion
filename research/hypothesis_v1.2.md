# ACCTCLOCK — Hypothesis v1.2 (prospective holdout arm PH-1)

Registered: 2026-10-22
Supersedes: nothing. `research/hypothesis_v1.1.md` (2026-10-22) remains **in force**
for the retrospective panel; this file is a **new registered version** that adds one
arm, **PH-1**, and changes **no** element of v1.1. Recorded in
`research/prompt_changelog.md` (Iteration 9).

Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`
(v1.0, 2026-10-21).
Binding design constraints: the canonical hypothesis-factory dossier, specification
**V-009 (IDEA-011 ACCTCLOCK)**, amendments Cycle-52, Cycle-56, Cycle-58, Cycle-110,
Cycle-111, Cycle-113, Cycle-114, Cycle-123 and Cycle-126, in particular
**Cycle-56 amendment item 4** (a prospective holdout must be registered before the
outcome can occur).

Status: **Pre-registered, untested.** No outcome-period return has been computed or
inspected in this repository, for the retrospective panel or for PH-1. Nothing in
this file is evidence that an edge exists.

---

## 0. Why v1.2 exists

`research/preregistration_v1.1.md` §4.1 declares, in advance, that the retrospective
panel has **no** event with T-A on or after 2019-01-01, so its chronological holdout
is **EMPTY** and the retrospective panel cannot satisfy the protocol's promotion
gate on its own (decision **D-014**). Its registered role is **evidential**: does
the transition-window state contrast exist, at what size, and does it survive the
mandatory controls.

The promotable test is therefore **prospective**. The only genuinely prospective,
untamable holdout available to this campaign is the **IFRS 18 first-application
window**: the 2027 interim reporting season, periods ending 30 June 2027, reports
published July–August 2027 (S-48; S-54).

**This file is registered on 2026-10-22, before the first IFRS 18 report can be
published.** That is the point of it. A holdout registered after the outcome is
inspectable is not a holdout.

## 1. The claim (one sentence)

**Around the first application of IFRS 18 in a jurisdiction, the market incorporates
the standard's consequences over the transition window — from the public adoption
announcement to the firm's first full report prepared under IFRS 18 — and firms with
lower pre-event information quality exhibit a different transition-window
abnormal-return path than comparable firms with higher pre-event information
quality, *within jurisdiction*, after mandatory enforcement and linguistic-distance
controls; and this difference is large enough, persistent enough and distinct enough
from costs to survive a point-in-time, out-of-sample test.**

The claim is the v1.1 claim, restricted to one standard and one future window. It
remains **two-sided**. No sign is selected before the holdout is opened.

## 2. What changed relative to v1.1, and what did not

| Element | v1.1 | v1.2 | Reason |
|---|---|---|---|
| Panel | Retrospective panel: IFRS 15 / IFRS 9 / IFRS 16 / ASC 606 / ASC 842 / ASU 2016-01, Stratum A + Stratum B by rule | **Unchanged.** v1.2 adds an arm; it does not touch the retrospective panel. | The retrospective panel is registered and its holdout is declared empty (D-014). |
| Arm | One (retrospective) | **Two:** the retrospective panel (evidential) and **PH-1** (promotable, prospective) | D-014; V-009 Cycle-56 amendment item 4. |
| Standard in the promotable arm | six standards | **IFRS 18 only** | IFRS 18 is the only standard whose first-application window is still in the future. |
| **Pre-emption arm** | registered as a **retrospective analogue** (T-RI, the first interim report under the new standard) | **upgraded to the real thing**: IFRS 18 has a **mandated pre-adoption impact disclosure** under IAS 8 paragraphs 30 and 31, required of issuers by ESMA's public statement (S-49) | The retrospective standards had **no** mandated pre-adoption impact disclosure, so the retrospective arm could only register an analogue. Here the disclosure itself is the pre-emption channel. |
| State (firm-level pre-adoption information quality) | mandatory | **Unchanged**, but constructed on the **pre-IFRS-18** basis of preparation, which for IFRS 18 means the FY2025 or FY2026 report, whichever is the last report published before T-A | Same construction rule as v1.1, applied to a later event. |
| Enforcement-quality control | mandatory | **Unchanged.** IFRS 18 adoption is an EU-wide event, so the control is *within* the EU and *between* the EU and the UK/other IFRS-18 jurisdictions. | V-009 Cycle-52 amendment item 2. |
| Linguistic-distance control | mandatory | **Unchanged.** | V-009 Cycle-52 amendment item 2 (S-44). |
| Adopter-type contrast (first-time vs second-time IFRS adopters) | not built | **not built, and it must not be built** for IFRS 18 | The IFRS 18 endorsement instruments converge on one application date and jurisdictions that adopt IFRS for the first time apply the IFRSs "all at once" (S-54), so the contrast degenerates. This is the same prohibition as v1.1 §8. |
| Event clock | T-A, T-A1, T-E, T-R, T-RI, T-E1 | **Unchanged in structure.** For PH-1, T-A is the day-level publication date of the jurisdiction's IFRS 18 adoption instrument. | Same clock, same pre-registered announcement-clock rule. |
| Entry/exit rule | enter at T-A, exit at the firm's own first full post-adoption report (T-R) | **Unchanged** | Same rule. |
| Thresholds, costs, acceptance criteria | frozen in v1.1 | **Unchanged.** | Tightening, never loosening. |
| Language-distance measure | published measure if exactly reproducible, else the registered fallback ordinal scale, chosen **before** the holdout is opened | **Unchanged**, and the choice must be recorded before the holdout is opened | Carried forward. |

## 3. Mechanism (why it might exist)

Identical to v1.1 §3, with IFRS 18's own content in place of the earlier standards'
content. IFRS 18 changes how performance and cash flows are presented and what
disclosures accompany them; the change is larger the less comparable the firm's
prior presentation was to the new one; and where the market's pre-existing knowledge
is thinner the revision of beliefs needed to read the new numbers is larger and is
incorporated more slowly.

**The one genuinely new feature of PH-1.** IFRS 18 comes with a **mandated
pre-adoption impact disclosure** (S-49, ESMA's public statement requiring issuers to
disclose the nature and, where known or reasonably estimable, the impact of the
impending accounting change under IAS 8.30 and .31). That creates a *measurable,
dated pre-emption window* that did not exist for the retrospective panel. It is
therefore a **kill signal with teeth**: if the market's response is concentrated in
the pre-disclosure window rather than after it, the slow-diffusion premise has
already been consumed and the hypothesis is dead, cleanly and for a reason that was
registered in advance.

**The corresponding risk, registered in advance.** The mandated disclosure is also
a mechanism that could *create* the drift rather than merely pre-empt it: a
disclosure of a material change can make the market's information set better and
faster, not slower. If PH-1 returns a *null* transition-window effect, the
pre-emption arm is the first thing to examine, and the report must state whether the
pre-disclosure window carried the response. A null here is a **contribution, not a
replication** (S-37 / V-009 G-21), and the pre-emption decomposition is mandatory
in the write-up, not optional.

## 4. Competing and counter hypotheses

Carried forward unchanged from v1.1 §4 (CH-1 … CH-9), with one addition:

- **CH-10 (disclosure-induced faster diffusion).** The mandated IAS 8 pre-adoption
  impact disclosure compresses the diffusion of IFRS 18's consequences, so the
  transition-window effect is smaller or absent for IFRS 18 than it would be
  otherwise, and what remains is a *disclosure* event rather than a
  *slow-diffusion* event. *Test:* compare the pre-disclosure and post-disclosure
  sub-windows; report the transition-window estimate with and without the
  pre-disclosure window; state explicitly whether the arm is a slow-diffusion test
  or a disclosure test on the evidence of the decomposition.

## 5. Event clock for PH-1

Identical in structure to v1.1 §5, and the same pre-registered announcement-clock
rule applies: T-A is the **jurisdictional legal-adoption** date, T-A1 is the
**standard-setter issuance** date (IFRS 18 was issued on 9 April 2024), both are
recorded and reported, and a conflict between primary sources is **recorded, never
silently resolved** (D-011). The date that maximises any return is never selected.

**Known T-A anchors for PH-1** (all primary, all dated, recorded now so that the
adoption instrument is pinned before the outcome exists):

| Jurisdiction | Instrument | Adoption date | Application date | Source |
|---|---|---|---|---|
| European Union | Commission Regulation (EU) 2026/338 | 2026-02-13 (OJ publication 2026-02-16) | periods beginning on or after 2027-01-01 | S-54, EFRAG Endorsement Status Report |
| United Kingdom | UK Endorsement Board adoption of IFRS 18 | 2022-05 (UKEB adopts IFRS 18) — the UK-adoption date for the instrument must be pinned to the **day** from the UKEB's own decision record before the arm is run | periods beginning on or after 2027-01-01 | S-54 |
| Saudi Arabia | Saudi CMA announcement CMA_N_4083 | 2026-06-30 | periods beginning on or after 2027-01-01 | S-54 |

**Open before the arm is run:** the day-level UK Endorsement Board decision date,
and the day-level T-A for every other IFRS 18 jurisdiction the panel rule admits.
These are the **same** A2/A4 items as for the retrospective panel and are listed in
`research/authorisation_request.md`.

## 6. Pre-registered predictions

Identical in form to v1.1 §6 (P1 … P6), evaluated on PH-1, with one addition:

- **P7** The transition-window effect, if it exists, is **not** concentrated in the
  mandated pre-adoption disclosure window; and the decomposition of the
  transition window into its pre-disclosure and post-disclosure parts is reported
  whatever the result.

## 7. Kill conditions

The thirteen kill conditions of v1.1 §7 are carried forward **unchanged** and apply
to PH-1 in full. Two are singled out as the most likely to bind here:

- **Kill condition 12 (pre-emption consumed).** A significant pre-event drift in the
  pre-disclosure window is a **kill signal, not a null**.
- **Kill condition 14 (no promotable test).** If the feasibility audit for the PH-1
  panel reports fewer than **12 clusters** or fewer than **200 treatment firms**, the
  PH-1 arm is **inconclusive by construction** and is reported as such, exactly as
  the retrospective panel would be.

## 8. What v1.2 does **not** claim, and why

- **No adopter-type contrast.** IFRS 18's instruments converge on one application
  date and first-time IFRS adopters apply the IFRSs "all at once" (S-54), so a
  first-time-versus-second-time contrast degenerates into a comparison the
  literature has already populated.
- **No pooling of the four IFRS 18 population statistics.** The expected-impact
  distribution (S-50), the disclosure-incidence and timeliness statistics (S-51) and
  the ESMA quantification statistics (S-49) are the four statistics the arm-A
  non-pooling rule forbids pooling; they are reported as context and never combined
  into a single measure.
- **No claim that the retrospective panel's result transfers.** PH-1 is a separate
  arm with its own estimand and its own acceptance decision.
- **No claim on enforcement quality or linguistic distance.** They remain published
  conditioners and mandatory controls, never this campaign's effect.

## 9. Evidence status

Unchanged from v1.1 §9, plus the IFRS 18 arm's own evidence:

- **Published mechanism evidence (A):** as in v1.1 §9.
- **Published counter-evidence (A):** as in v1.1 §9.
- **Published nulls / reversals in the family (A):** as in v1.1 §9.
- **The comparator the design rests on is unrun by the field (A):** as in v1.1 §9.
- **IFRS 18 arm-specific evidence (A):** the pre-adoption impact disclosure is
  mandated and its population statistics are known to be thin — more than half of
  the 2025 annual reports of a random sample of 50 Norwegian listed companies gave
  no company-specific information or only standardised disclosures, and only 8% had
  updated the information in the 2026 half-year reports (S-51); 61% of the 28 DAX 40
  respondents expect minor effects (S-50); the ESMA-supervised population
  quantification rate is **0 of 13** on a convenience sample and is **not yet
  published** for the population (S-49).
- **Candidate-specific evidence (B):** none. No ACCTCLOCK event study, portfolio
  simulation or backtest has been run for IFRS 18 or for anything else.
- **Strategy evidence (C):** none.
- **Assumptions (D):** as in v1.1 §9, and now with the additional assumption that
  the mandated pre-adoption disclosure does not by itself resolve the information
  asymmetry the design is about.

## 10. Current blocker (documented, not a conclusion)

The PH-1 arm is **registered** and therefore is *not* tampered with. It is blocked on
exactly the same items as the retrospective panel, and on one more:

1. **A1 and A2 are outstanding** (see `research/authorisation_request.md`). Without
   price coverage there is no outcome; without read-only harvesting there is no
   T-R, no T-RI, no state variable and no restated comparative.
2. **The day-level IFRS 18 T-A for each admitted jurisdiction is not yet pinned**,
   and the UK Endorsement Board's IFRS 18 decision date in particular must be read
   from the UKEB's own decision record.
3. **The PH-1 feasibility audit has not been run**, so the ≥12-cluster and
   ≥200-firm minima are untested for this arm.

These are **data and authorisation limitations, not evidence for or against the
hypothesis**. The campaign status remains **PARKED — not validated, not rejected.**

## 11. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Original frozen claim; empty treatment group (D-009). |
| v1.1 | 2026-10-22 | Executable, dossier-compliant design; transition-window claim; mandatory controls; pre-emption kill-signal arm; retrospective panel's empty holdout declared in advance. |
| **v1.2** | **2026-10-22** | Adds the **PH-1 prospective holdout arm** on the IFRS 18 first-application window (2027 interim reporting season), with the mandated IAS 8 pre-adoption impact disclosure as the real pre-emption channel, the counter-hypothesis that the disclosure *compresses* diffusion (CH-10), and the prediction that the effect is not concentrated in the pre-disclosure window (P7). Registered **before the first IFRS 18 report can be published**. No element of v1.1 is changed. |

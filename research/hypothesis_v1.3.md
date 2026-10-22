# ACCTCLOCK — Hypothesis v1.3 (amendment to the PH-1 arm)

Registered: 2026-10-22
Supersedes: nothing. `research/hypothesis_v1.1.md` (2026-10-22) remains **in force**
for the retrospective panel, and `research/hypothesis_v1.2.md` (2026-10-22) remains
**in force for PH-1 except where this file expressly amends it**. This file
amends **four** elements of v1.2 and changes **nothing** in v1.1. Recorded in
`research/prompt_changelog.md` (Iteration 10).

Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`
(v1.0, 2026-10-21).

Binding design constraints: the canonical hypothesis-factory dossier, specification
**V-009 (IDEA-011 ACCTCLOCK)**, amendments Cycle-52, Cycle-56, Cycle-58, Cycle-110,
Cycle-111, Cycle-113, Cycle-114, Cycle-123 and Cycle-126, in particular
**Cycle-56 amendment item 4** (a prospective holdout must be registered before the
outcome can occur).

Status: **Pre-registered, untested.** No outcome-period return has been computed or
inspected in this repository, for the retrospective panel or for PH-1. Nothing in
this file is evidence that an edge exists. The campaign remains **PARKED — not
validated, not rejected.**

---

## 0. Why v1.3 exists, and what it buys

v1.2 registered PH-1 on 2026-10-22 with three items deliberately left open, to be
closed **before** the holdout is opened and **without** looking at an outcome:

1. the **Saudi T-PRE question** — whether the Saudi row enters PH-1 at all, given
   that Saudi Arabia's mandated pre-adoption impact disclosure falls inside its
   transition window;
2. the **linguistic-distance control** — the choice between the published measure
   and the registered fallback ordinal scale, and the fallback's category
   boundaries;
3. the **day-level T-A anchors** — the UK Endorsement Board decision date and the
   day-level T-A for every other IFRS 18 jurisdiction the panel rule admits.

All three are now closed, in advance, from primary sources. v1.3 also records one
**correction of a v1.2 statement** that the new evidence falsifies, and one
**scope observation** that the maintainer, not this file, must rule on.

The value of this file is the same as v1.2's: it is fixed before the outcome
exists. The first IFRS 18 reports are the 2027 interim reporting season, published
July–August 2027 (S-48). Nothing here may be changed in place after that.

## 1. The claim (one sentence)

**Unchanged from v1.2 §1, by reference.** Around the first application of IFRS 18
in a jurisdiction, the market incorporates the standard's consequences over the
transition window — from the public adoption announcement to the firm's first full
report prepared under IFRS 18 — and firms with lower pre-event information quality
exhibit a different transition-window abnormal-return path than comparable firms
with higher pre-event information quality, *within jurisdiction*, after mandatory
enforcement and linguistic-distance controls; and this difference is large enough,
persistent enough and distinct enough from costs to survive a point-in-time,
out-of-sample test.

It remains **two-sided**. No sign is selected before the holdout is opened.

## 2. What changed relative to v1.2, and what did not

| Element | v1.2 | v1.3 | Reason |
|---|---|---|---|
| Claim | The PH-1 claim | **Unchanged** | No evidence was inspected. |
| Panel | PH-1 panel by the five-condition rule of `research/specification_v1.1.md` §1.1 | **Unchanged.** The rule is not edited. The candidate universe is now **141** jurisdictions, because the snapshot parser had admitted one boilerplate paragraph as a jurisdiction; the artefact is removed and the removal is recorded as decision **D-025**. | A parsing artefact is a data-quality defect, not a panel-scope change. The panel is not narrowed or widened by rule; the feasibility audit has not begun. |
| Condition 2 (a dated instrument making IFRS 18 mandatory) | verified for 3 jurisdictions | **verified for 5**: European Union, United Kingdom, Saudi Arabia, **Singapore (2024-10-04)**, **Brazil (2025-12-23)** | Two further primary instruments were located and verified (source ledger S-76, S-77). **Hong Kong and South Africa were attempted and are recorded as not verified** — an unverified date is never filled in. |
| **Pre-disclosure anchor T-PRE** | "the filing acceptance timestamp of the firm's first pre-adoption disclosure of the expected impact of IFRS 18 … the disclosure must precede T-A for the pre-emption window to be well defined; if the disclosure does not precede T-A, the pre-emption arm is not available for that jurisdiction" | **Amended.** T-PRE is the acceptance timestamp of the firm's **first disclosure of the expected IFRS 18 impact** under the regime that applies to it. The pre-disclosure window **[T-A, T-PRE]** is well defined if and only if **T-A < T-PRE < T-R**; otherwise the pre-emption arm is **not applicable** for that jurisdiction and is reported as not applicable. | The v1.2 sentence contradicted v1.1 §4.3, which defines the pre-emption window as **[T-A, T-PRE]** — an interval that is non-empty precisely when T-PRE is *after* T-A. v1.3 replaces the inconsistent precondition with the interval condition, and it applies uniformly to every jurisdiction. |
| **Saudi Arabia** | open: "exclude the Saudi row on the T-PRE ground, or admit it with a separately specified T-PRE rule" | **Admitted, with the rule above.** Saudi Arabia's mandated disclosure falls inside its transition window, which makes its pre-disclosure window **[2024-12-26, the acceptance timestamp of the firm's first CMA-mandated impact disclosure]** — a non-empty interval — and therefore usable. | The primary estimand does not depend on the pre-disclosure anchor. Excluding Saudi would remove the only cohort outside the EU/UK for no methodological gain, at a moment when the arm is already short of its cluster minimum. The pre-emption **kill signal** for Saudi is evaluated on the interval above, and if a jurisdiction has no disclosure before T-R, its pre-emption arm is reported as **not applicable**, never as a null. |
| Linguistic-distance control | "unchanged": published measure if exactly reproducible, otherwise the registered fallback ordinal scale, chosen before the holdout opens | **Unchanged in principle, closed in practice.** The **registered fallback ordinal scale** is selected, with its construction rule, its official-language inputs, its five ordinal categories (LD-0 … LD-4) and their boundaries fixed in `research/specification_v1.3.md` §3, and validated against the published measure (Spearman **0.9776** over the published measure's 84-country sample; **0.9704** restricted to panel jurisdictions). | Decision **D-023** required the fallback's category boundaries to be enumerated by dated decision before the holdout opens. They are now enumerated, and the fallback is implemented, tested and validated from open, dated, hashed inputs. |
| **Convergence of IFRS 18 application dates** | "the IFRS 18 instruments converge on one application date and first-time adopters apply the IFRSs 'all at once' (S-54)" | **Corrected.** The instruments do **not** converge on one date: five primary-verified T-A dates now span seventeen months — Singapore 2024-10-04, Saudi Arabia 2024-12-26, the United Kingdom 2025-12-10, Brazil 2025-12-23, the European Union 2026-02-13 — while the **application** date is common (2027-01-01). The v1.2 statement is false as written and is replaced by the dated statement. | The statement is a *design input* for the feasibility audit and the cluster arithmetic. Leaving a falsified statement in a registered document would corrupt the audit. The correction is made now, before any outcome, and it does not change the rule. |
| Adopter-type contrast | not built | **Unchanged** | Stratum B remains settled in the negative (v1.2 §5.2), and the correction above does not reopen it: first-time IFRS adopters still apply the IFRSs "all at once". |
| Event clock | T-A, T-A1, T-E, T-R, T-RI, T-E1 | **Unchanged in structure**; the anchor table is corrected and extended (§5 below) | v1.2 §5 carried two wrong dates (the UK and Saudi Arabia), which D-022 had already resolved in the panel file but not in the hypothesis text. v1.3 restates the table correctly. |
| Entry/exit rule | enter at T-A, exit at the firm's own first full post-adoption report (T-R) | **Unchanged** | Same rule. |
| Thresholds, costs, acceptance criteria | frozen in v1.1 | **Unchanged** | Tightening, never loosening. |
| Kill conditions | thirteen, carried forward | **Unchanged**, with one clarification in §7 | Kill condition 12 is evaluated on the jurisdictions for which a pre-disclosure window exists; the others are named as not applicable. |

## 3. Mechanism (why it might exist)

**Unchanged from v1.2 §3.** IFRS 18 changes how performance and cash flows are
presented and what disclosures accompany them; the change is larger the less
comparable the firm's prior presentation was to the new one; and where the
market's pre-existing knowledge is thinner the revision of beliefs needed to read
the new numbers is larger and is incorporated more slowly.

**The one feature that is now pinned.** PH-1's pre-emption channel is a real
mandated pre-adoption impact disclosure (S-49, ESMA's public statement under IAS
8.30 and .31) in the EU and the United Kingdom, and a **CMA-mandated preliminary
assessment** of the expected impact of initial application in Saudi Arabia, in
approved financial statements for periods beginning on or after 2026-04-01
(CMA_N_4083). Under the v1.3 rule, both are located in time, and both yield a
pre-disclosure window that lies **inside** the transition window. That is the
mechanism, and it is a **kill signal with teeth**: if the response is concentrated
in the pre-disclosure window, the slow-diffusion premise has already been consumed.

## 4. Competing and counter hypotheses

**Unchanged from v1.2 §4:** CH-1 … CH-10, with CH-10 (disclosure-induced faster
diffusion) unchanged in substance. v1.3 adds no new counter-hypothesis, because it
changes no mechanism and no outcome definition; it fixes the **measurement** of the
pre-disclosure window so that CH-10 can be tested.

## 5. Event clock for PH-1 — the corrected anchor table

The announcement-clock rule is unchanged: T-A is the **jurisdictional
legal-adoption date**, T-A1 is the **standard-setter issuance date** (IFRS 18 was
issued on 9 April 2024), both are recorded, and a conflict between primary sources
is **recorded, never silently resolved** (D-011).

| Jurisdiction | Instrument | **T-A** (legal adoption) | Application | Source |
|---|---|---|---|---|
| Singapore | SFRS(I) 18, issued by the Accounting Standards Committee of ACRA | **2024-10-04** | periods beginning on or after 2027-01-01 | S-76 |
| Saudi Arabia | SOCPA adoption of IFRS 18 (Accounting Standards Council resolution 25/06/1446H) | **2024-12-26** | periods beginning on or after 2027-01-01 | S-61 |
| United Kingdom | UK Endorsement Board adoption of IFRS 18 for use in the UK | **2025-12-10** | annual reporting periods beginning on or after 2027-01-01 | S-63, S-69 |
| Brazil | Resolução CVM nº 237, de 23 de dezembro de 2025 (CPC 51, aligned to IFRS 18) | **2025-12-23** | financial years beginning on or after 2027-01-01 | S-77 |
| European Union | Commission Regulation (EU) 2026/338 | **2026-02-13** (OJ publication 2026-02-16) | periods beginning on or after 2027-01-01 | S-54, S-60 |

**Recorded date conflicts, never resolved silently.** The European Union has two
primary dates (endorsement 2026-02-13; Official Journal publication 2026-02-16);
the United Kingdom has two (adoption decision 2025-12-10; publication of the
adopted text and Adoption Statement 2025-12-12); Saudi Arabia has two different
*kinds* of instrument (the SOCPA adoption of 2024-12-26, and the CMA's
early-adoption decision CMA_N_4083 of 2026-06-30, which is a separate event and
not T-A). All six dates are written into the panel rows' own `date_conflict` field.

**Attempted and not verified, recorded as such.** Hong Kong SAR: the HKICPA's own
HKFRS 18 page states the effective date (financial periods beginning on or after
1 January 2027) but the retrieved page does not carry the **issuance** date, so
T-A is left empty rather than inferred. South Africa: the route is incorporation
by reference — the Companies Act Regulations refer directly to "IFRS as issued
from time to time by the IASB" — so there is **no dated local instrument** and
T-A is left empty. Both attempts are recorded in `research/decision_log.md`
(D-026). A missing date is a fact to be reported, not a number to be guessed.

**Still open before the arm is run:** the day-level T-A for every further IFRS 18
jurisdiction the panel rule admits, and the four conditions that remain unverified
for every jurisdiction.

## 6. Pre-registered predictions

**Unchanged from v1.2 §6:** P1 … P7, evaluated on PH-1. P7 is restated in the
v1.3 terms because the pre-disclosure window's definition is amended:

- **P7** The transition-window effect, if it exists, is **not** concentrated in the
  mandated pre-adoption disclosure window; and the decomposition of the transition
  window into its pre-disclosure and post-disclosure parts is reported whatever
  the result, **for every jurisdiction in which a pre-disclosure window exists**,
  with the jurisdictions in which it does not exist named in the report.

## 7. Kill conditions

The thirteen kill conditions of v1.1 §7 are carried forward **unchanged** and apply
to PH-1 in full. One clarification, and no change:

- **Kill condition 12 (pre-emption consumed).** A significant pre-event drift in
  the pre-disclosure window is a **kill signal, not a null**. It is evaluated on
  the jurisdictions whose pre-disclosure window exists. A jurisdiction with no such
  window — because it has no mandated pre-adoption disclosure before T-R — is
  reported as **not applicable** for this condition, and **never** as a null or a
  pass.
- **Kill condition 14 (no promotable test).** Unchanged: if the feasibility audit
  reports fewer than 12 clusters or fewer than 200 treatment firms, the PH-1 arm
  is **inconclusive by construction**.

## 8. What v1.3 does **not** claim, and why

- **No adopter-type contrast.** Unchanged (v1.2 §8): the IFRS 18 instruments
  converge on one **application** date and first-time adopters apply the IFRSs
  "all at once" (S-54), so a first-time-versus-second-time contrast degenerates.
- **No pooling of the four IFRS 18 population statistics.** Unchanged (S-49, S-50,
  S-51).
- **No claim that the retrospective panel's result transfers.**
- **No claim on enforcement quality or linguistic distance.** They remain published
  conditioners and mandatory controls, never this campaign's own effect. The
  fallback's concordance with the published measure is a validation of a
  **control**, reported as such and not as an outcome.
- **No claim about jurisdictions outside the registered candidate universe.**
  Jurisdictions such as **Australia** and **Japan** mandate IFRS 18 through their
  own local equivalents (AASB 18; the ASBJ statement) and are therefore genuine
  IFRS 18 application events, but the registered candidate universe is derived
  from the IFRS Foundation's list of jurisdictions that apply IFRS as issued by the
  IASB, and those jurisdictions are not on it. Adding them would be a **panel-scope
  change**, which is the maintainer's ruling under **A4** and requires a further
  registered version. It is raised as a dated recommendation in
  `research/decision_log.md` (D-026) and is **not** done silently here.
- **No claim that five verified instruments are five independent clusters.** Five
  jurisdictions with five distinct T-A dates are five **timing cohorts**; the number
  of *independent* clusters is a feasibility-audit question, and the expected
  answer remains below the ≥12 minimum.

## 9. Evidence status

Unchanged from v1.2 §9, plus three additions that are **control or measurement**
evidence, not outcome evidence:

- **The published linguistic-distance measure is reproducible at the language
  level.** Its operationalisation (S-44 §3.3: compare each official language's 192
  WALS characteristics with their English equivalents, 0 if shared and 1 if not,
  averaged over a country's official languages) was read from the **typeset,
  open-access** article, which was unreachable in the previous session and is
  reachable now (S-83). Recomputing it from **WALS 2020.6** (S-80) reproduces the
  published per-language values to within about 0.01 — Bengali 0.583 against a
  published 0.583, Japanese 0.597 against 0.590, Korean 0.507 against 0.507,
  Spanish 0.342 against 0.342, Russian 0.308 against 0.308. The residual
  non-reproducibility is **not** in the index but in the **jurisdiction-level
  official-language lists**, which come from a licensed database. This is the
  finding that makes the fallback both necessary and buildable.
- **The fallback scale is implemented, tested and validated.** Construction rule,
  ordinal categories and boundaries in `research/specification_v1.3.md` §3;
  per-jurisdiction table in `research/linguistic_distance_v1.csv`; validation in
  `research/linguistic_concordance.md`; 18 unit tests in
  `tests/test_linguistic_distance.py`.
- **Five IFRS 18 adoption instruments are now primary-verified**, and two more
  jurisdictions were attempted and recorded as not verified (Hong Kong SAR, South
  Africa).

No candidate-specific evidence (B), strategy evidence (C) or outcome evidence of
any kind exists. Nothing in this file is evidence that an edge exists.

## 10. Current blocker (documented, not a conclusion)

1. **A1 and A2 are outstanding** (`research/authorisation_request.md`). Without
   price coverage there is no outcome; without read-only harvesting there is no
   T-R, no T-RI, no state variable and no restated comparative.
2. **The day-level IFRS 18 T-A is still not pinned for most admitted
   jurisdictions.** Five are pinned; the remaining 136 candidate jurisdictions
   have an empty T-A, which is recorded rather than filled in.
3. **The PH-1 feasibility audit has not been run**, so the ≥12-cluster and
   ≥200-firm minima are untested for this arm.
4. **One verification could not be completed in this session**: the FCA National
   Storage Mechanism's *live* search response was unreachable (every API path
   returns HTTP 403), so the NSM's time-of-day behaviour is evidenced from the
   FCA's own served application code, not from a live response (D-027).

These are **data and authorisation limitations, not evidence for or against the
hypothesis**. The campaign status remains **PARKED — not validated, not rejected.**

## 11. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Original frozen claim; empty treatment group (D-009). |
| v1.1 | 2026-10-22 | Executable, dossier-compliant design; transition-window claim; mandatory controls; pre-emption kill-signal arm; retrospective panel's empty holdout declared in advance. |
| v1.2 | 2026-10-22 | Adds the **PH-1 prospective holdout arm** on the IFRS 18 first-application window, with the mandated IAS 8.30/.31 pre-adoption impact disclosure as the pre-emption channel, CH-10 and P7. Registered **before the first IFRS 18 report can be published**. |
| **v1.3** | **2026-10-22** | **Amends v1.2 in four places and nothing in v1.1.** (i) **Saudi Arabia is admitted** to PH-1 and the pre-disclosure window is defined by the interval condition **T-A < T-PRE < T-R**, which replaces v1.2's inconsistent "the disclosure must precede T-A" precondition and which resolves the open Saudi question in favour of admission; (ii) the **linguistic-distance control is closed**: the registered fallback ordinal scale is selected, its construction rule and its five ordinal categories with their boundaries are fixed, and it is validated against the published measure (Spearman 0.9776); (iii) the **anchor table is corrected** (the UK is 2025-12-10 and Saudi Arabia is 2024-12-26, not the dates v1.2 §5 carried) and **extended** to five primary-verified instruments with two attempts recorded as not verified; (iv) the statement that the IFRS 18 instruments **converge on one application date** is **corrected** — their T-A dates span seventeen months while the application date is common. Registered **before the first IFRS 18 report can be published**. |

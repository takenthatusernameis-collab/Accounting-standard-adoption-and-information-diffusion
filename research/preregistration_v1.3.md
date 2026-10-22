# ACCTCLOCK — Preregistration v1.3 (amendment to the PH-1 arm)

Registered: 2026-10-22
Supersedes: nothing. `research/preregistration_v1.1.md` (2026-10-22) remains **in
force** for the retrospective panel; `research/preregistration_v1.2.md` (2026-10-22)
remains **in force for PH-1 except where this file expressly amends it**. This
file amends **three** elements of v1.2 and changes **nothing** in v1.1. Recorded in
`research/prompt_changelog.md` (Iteration 10).

Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`
(v1.0, 2026-10-21).

Status: **Pre-registered, untested.** No outcome-period return has been computed or
inspected in this repository, for the retrospective panel or for PH-1.

**Reading note.** Where PH-1 inherits a v1.1 or v1.2 rule unchanged, this file says
so **by reference**. A restated rule is a copy that can drift; a reference cannot.

---

## 0. Why this file exists

Three items that `research/preregistration_v1.2.md` §8 left open are closed here,
**before** the holdout can be opened and without inspecting any outcome:

1. the **pre-disclosure window's definition** — v1.2 carried a precondition that
   contradicted the v1.1 §4.3 window, and it left the Saudi question unanswered;
2. the **day-level IFRS 18 adoption instrument date** for every admitted
   jurisdiction — five are now pinned from primary sources, two jurisdictions are
   recorded as attempted and not verified, and the rest remain **empty**;
3. the **linguistic-distance choice** — v1.2 §8 required it to be "recorded before
   the holdout is opened"; it is now recorded, with the fallback's construction
   rule, its ordinal categories and their boundaries, and its validation against
   the published measure.

One further item is corrected: v1.2 §5.2 stated that the IFRS 18 instruments
"converge on one application date". Their **T-A** dates span seventeen months; the
**application** date is common. The cluster arithmetic is restated accordingly.

## 1. Primary outcome (unchanged)

**Inherits v1.1 §1 by reference, unchanged.** The primary outcome family is
**H-B′**: the transition-window abnormal return on **[T-A, T-R]**, with the
**firm-level pre-adoption information quality** as the state, estimated **within
jurisdiction**, **two-sided**. For PH-1 the same quantity is computed for the
IFRS 18 event, using the IFRS 18 event clock (T-A, T-R) and the same benchmark and
estimand. The v1.0 [T-R, T-R+20] window remains a **descriptive control**.

## 2. Estimand (unchanged)

**Inherits v1.1 §2 by reference, unchanged**, including the PH-1 addition: the
PH-1 estimand is reported **alongside** the pre-/post-disclosure decomposition, and
the report must state which of two readings the decomposition supports — a
**slow-diffusion** reading or a **disclosure** reading — **without** choosing after
seeing which is larger.

## 3. Pre-registered claim about the published reading (unchanged)

**Inherits v1.1 §3 by reference, unchanged**, including the PH-1 caveat that IFRS 18
is a **weaker test of the same claim** than the retrospective panel, because IFRS 18
changes presentation and disclosure rather than measurement and because the
sharpest part of the discontinuity is not available.

## 4. Splits (unchanged)

**Inherits v1.1 §4 by reference, unchanged**, with the holdout for PH-1 being the
whole of PH-1 itself.

| Split | Rule | Status for PH-1 |
|---|---|---|
| Development | T-A before 2016-01-01 | Unchanged; **not** used for PH-1. |
| Validation | T-A in [2016-01-01, 2019-01-01] | Unchanged; **not** used for PH-1. |
| Untouched holdout (retrospective) | T-A on/after 2019-01-01 | **EMPTY** — declared in advance (D-014). |
| **PH-1 (prospective holdout arm)** | IFRS 18 first-application events: the **2027 interim reporting season**, periods ending 30 June 2027, published July–August 2027 | **Registered**, before the first IFRS 18 report exists. Opened **once**, under the test order in §6, after the PH-1 feasibility audit in §5 is published. |

**The once-only rule** is unchanged and is not weakened by this file: the PH-1
result is computed and reported **once**; no intermediate PH-1 quantity — not a
cluster count above the minimum, not a partial window, not a single firm's path —
may be computed, inspected or reported before the analysis in §6 is run. A peek
voids the arm; a voided arm is reported as **void**, never as a null.

## 5. Feasibility audit and power for PH-1

### 5.1 The audit (unchanged)

**Inherits v1.1 §5.1 by reference, unchanged**, applied to the PH-1 panel: per
event, the independent-cluster count; treatment and control firm counts; coverage
by event, jurisdiction, year and liquidity bucket; **coverage of the filing
timestamps** (including the T-PRE pre-disclosure documents); missingness; and the
count of firms whose transition window length differs materially from the control
window length.

### 5.2 Expected cluster counts (a prediction, not a result) — **restated**

| Stratum | Expected clusters for PH-1 | Comment |
|---|---|---|
| A — content change (IFRS 18 in an existing framework) | **≈ 4–8** | One cluster per admitted jurisdiction with a verified condition-2 instrument, on the rule in `research/specification_v1.3.md` §1. **Five** instruments are primary-verified today, with **five distinct T-A dates** spanning 2024-10-04 to 2026-02-13: Singapore, Saudi Arabia, the United Kingdom, Brazil, the European Union. The EU is a **single** timing cohort, not 27 independent ones. The upper end of the range allows for further jurisdictions whose instruments are verified before the audit; the **lower** end assumes none are. |
| B — framework change (first-time IFRS adopters) | **0** | Settled in advance, in the negative: first-time IFRS adopters apply the IFRSs "all at once", so the contrast degenerates and is not built. |
| **Total** | **≈ 4–8** | **Below the ≥12 minimum.** Stated in advance, and it is the reason PH-1 is registered as a **narrower and weaker** test than the retrospective panel rather than a stronger one. |

**Correction to v1.2 §5.2, recorded now.** v1.2 stated that "the IFRS 18
instruments converge on one application date". That is true of the **application**
date (2027-01-01, for every verified jurisdiction) and false of the **adoption**
dates, which now span seventeen months. The correction is made **before** the
audit and before any outcome, and it does not change the rule, the panel, the
window or the thresholds. It matters because the spread of T-A dates is what gives
PH-1 any timing variation at all: the arm's variation is in the *announcement
clock*, not in the *application clock*.

**A scope question this file does not decide.** Jurisdictions such as **Australia**
and **Japan** mandate IFRS 18 through their own local equivalents and are not on
the IFRS Foundation's list of IFRS jurisdictions, which is what the registered
candidate universe is derived from. Adding them would be a **panel-scope change**:
it requires the maintainer's ruling under **A4** and a further registered version.
It is **not** done here. It is raised as a dated recommendation in
`research/decision_log.md` (D-026).

### 5.3 The rule that binds if the audit falls short (frozen)

> If the realised independent-cluster count for PH-1 is **< 12** or the treatment-
> firm count is **< 200**, the **PH-1 primary estimand is inconclusive by
> construction** — the same rule, and the same precedent, that
> `research/preregistration_v1.1.md` §5.3 already froze for the retrospective
> panel. The descriptive results are still produced for the record, and the
> decision is **park** or **inconclusive** — never "pass".
>
> **The rule is fixed here so that a short arm cannot later be used as a reason to
> change the panel, the window, or the thresholds.**

### 5.4 Minimum detectable effect (unchanged)

**Inherits v1.1 §5.4 by reference, unchanged.** The power calculation is computed
and reported **before** the primary model is estimated, for each arm separately.

## 6. Test order for PH-1 (frozen)

**Inherits v1.1 §6 by reference, unchanged, applied to PH-1**, with the pre-emption
step anchored on the **real** mandated disclosure:

1. **Feasibility and event-count audit** (§5). Report and **stop** if the counts
   fall below the pre-registered minimums.
2. **Descriptive event study** — pre/post abnormal-return, volume and coverage paths
   from [T-A−60, T-R+60td]; descriptive only; may not change the specification.
3. **Primary test** — the estimand of §2 with cluster-robust inference, wild-cluster
   bootstrap and the jurisdiction-level randomisation test.
4. **Conditional and secondary tests** — announcement/anticipation windows (CH-1),
   the **pre-disclosure window** [T-A, T-PRE] (CH-9 / CH-10 **kill signal**),
   post-transition residual, H-C, and the direction-and-magnitude replication of the
   published conflict between S-35 and S-36.
5. **Portfolio simulation** — the frozen rule with point-in-time holdings,
   conservative fills, costs, exposures, borrow availability and capacity limits.
6. **Out-of-sample** — the untouched holdout, opened **once**. For PH-1, PH-1 *is*
   that out-of-sample step, and it is opened only after the retrospective
   validation decision is recorded.
7. **Robustness and red-team** — placebo dates, placebo standards, false event
   assignments, leave-one-event-out, outlier exclusion, pre-/post-2010 subperiod,
   regime slices, alternative windows, and the pre-registered multiple-comparison
   adjustment.

### 6a. The pre-/post-disclosure decomposition (mandatory, whatever the result) — **amended**

The transition window is split at **T-PRE**; both parts are reported for the
treated firms and for the matched controls. This is the decomposition that decides
between the slow-diffusion reading and the disclosure reading (v1.2 hypothesis P7,
CH-10).

**Amendment.** The pre-disclosure window is defined by the interval condition
**T-A < T-PRE < T-R** (`research/specification_v1.3.md` §2.2). Where a jurisdiction
has no mandated pre-adoption disclosure before T-R, the decomposition is reported
for it as **not applicable**, and the jurisdiction is **named in the report**. It
is **never** reported as a null, a pass or a zero, and the set of jurisdictions for
which the decomposition was computed is stated in the same table.

**Saudi Arabia is in scope.** Its CMA-mandated preliminary assessment of the
expected impact of initial application (CMA_N_4083, approved financial statements
for periods beginning on or after 2026-04-01) falls inside its transition window,
so its pre-disclosure window is **[2024-12-26, that acceptance timestamp]**, and
the decomposition is computed for it.

### 6b. The disclosure-specificity split (descriptive, pre-registered, not pooled)

**Unchanged from v1.2.** Treated firms are split into **company-specific quantified
impact** / **company-specific unquantified impact** / **standardised or absent**
pre-disclosure. The three groups are named in advance. This split is **not** pooled
with the four IFRS 18 population statistics that the arm-A non-pooling rule
forbids pooling (S-49, S-50, S-51).

## 7. Statistical procedure (unchanged)

**Inherits v1.1 §7 by reference, unchanged.** With one modification, forced by §5.2
rather than chosen: because PH-1 is expected to have a **small** number of
independent clusters, the **jurisdiction-level randomisation test** and the
**wild-cluster bootstrap** are reported as the **primary** inference for PH-1, with
the cluster-robust standard error reported alongside, and the report states the
**number of independent clusters** in the abstract and in the conclusion. No
inference method may be switched after the result is seen.

## 8. Data requirements for PH-1 — **the open items are closed**

**Inherits v1.1 §8 by reference, unchanged**, plus:

- the **IAS 8.30/.31 pre-adoption impact disclosure** for every treated firm, with
  its own filing acceptance timestamp (T-PRE), hashed in the manifest chain exactly
  like a financial report, so that the disclosure-specificity classification in §6b
  is auditable after the fact;
- the **day-level IFRS 18 adoption instrument date** for every admitted
  jurisdiction — **now pinned for five**: Singapore 2024-10-04, Saudi Arabia
  2024-12-26, United Kingdom 2025-12-10, Brazil 2025-12-23, European Union
  2026-02-13 (OJ publication 2026-02-16), with Hong Kong SAR and South Africa
  recorded as attempted and not verified, and every other jurisdiction's date
  **empty** rather than inferred;
- the **linguistic-distance choice** — **now recorded, before the holdout is
  opened**: the **registered fallback ordinal scale**, with the construction rule,
  the two official-language inputs, the five ordinal categories **LD-0 … LD-4** and
  their fixed boundaries set out in `research/specification_v1.3.md` §3.2, the
  per-jurisdiction table in `research/linguistic_distance_v1.csv`, and the
  validation against the published measure in `research/linguistic_concordance.md`
  (Spearman **0.9776** over the published sample; **0.9704** restricted to panel
  jurisdictions). The published measure (S-44) is the **external validation** of
  the fallback's ordering and is never combined with it.

## 9. Costs and thresholds for PH-1 (unchanged)

**Inherits v1.1 §9 by reference, unchanged.** No cost was tuned; no return exists.

## 10. Reporting commitments for PH-1

**Inherits v1.1 §10 by reference, unchanged**, and for PH-1 specifically:

- the PH-1 result is reported **once**;
- the report states the **number of independent clusters** and whether the ≥12
  minimum was met;
- the report states whether the **pre-disclosure window** carried the response, and
  **names** the jurisdictions for which the pre-disclosure window does not exist
  and is therefore reported as not applicable;
- the report states which of the two readings — slow-diffusion or disclosure — the
  decomposition supports, and does not present the more favourable one;
- a **void** (a peek) is reported as void;
- the report states the **number of jurisdictions excluded from the
  linguistic-distance stratification** and names them;
- the campaign's own status line — **PARKED, not validated, not rejected** — is
  carried into the PH-1 write-up unchanged, and a null in this design is reported
  as a **contribution, not a replication** (S-37 / V-009 G-21).

## 11. Status

PH-1 is **registered and untested**. It is blocked on the same authorisation items
as the retrospective panel (**A1** market data, **A2** read-only public harvesting,
**A4** panel scope) and on one item of its own: the **day-level IFRS 18 adoption
instrument date** for the jurisdictions that are not yet verified, and the
verification of conditions 3 to 5.

Registering v1.3 does **not** unblock anything, and it does not license any
result. It fixes the test **before** the outcome exists, which is the only thing it
can do at this point. The campaign remains **PARKED — not validated, not rejected.**

## 12. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Frozen outcome, estimand, splits (by T-R), test order, thresholds, costs. |
| v1.1 | 2026-10-22 | Transition-window state contrast; splits re-anchored on T-A; retrospective holdout **empty**, declared in advance; feasibility, cluster-count and power rules fixed; published reading pre-registered; pre-emption window registered as a kill signal. |
| v1.2 | 2026-10-22 | **PH-1 registered as the prospective holdout arm**: the once-only reporting rule; the real mandated pre-disclosure anchor T-PRE; the mandatory pre-/post-disclosure decomposition; the disclosure-specificity descriptive split; the expected sub-minimum cluster count stated in advance with the consequence fixed; inference fixed in advance to the jurisdiction-level randomisation test and the wild-cluster bootstrap as primary. |
| **v1.3** | **2026-10-22** | **Amends v1.2 in three places and nothing in v1.1.** (i) The **pre-disclosure window** is defined by the interval condition **T-A < T-PRE < T-R**, replacing v1.2's precondition that contradicted the v1.1 §4.3 window; **Saudi Arabia is admitted** to PH-1 and its decomposition is computed on [2024-12-26, the CMA-mandated disclosure acceptance timestamp], while a jurisdiction with no such disclosure before T-R is reported as **not applicable** and named. (ii) The **cluster arithmetic is restated** (≈ 4–8) and the statement that the IFRS 18 instruments converge on one date is **corrected**: the T-A dates span seventeen months, the application date is common. (iii) The three open data requirements of v1.2 §8 are **closed or explicitly left empty**: five day-level T-A dates are pinned from primary sources, two jurisdictions are recorded as attempted and not verified, and the **linguistic-distance choice is recorded** — the registered fallback ordinal scale with its construction rule, its categories LD-0 … LD-4 and their boundaries, and its concordance with the published measure (Spearman 0.9776). Registered **before the first IFRS 18 report can be published**. |

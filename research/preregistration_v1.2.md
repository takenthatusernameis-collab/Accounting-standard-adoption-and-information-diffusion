# ACCTCLOCK — Preregistration v1.2 (prospective holdout arm PH-1)

Registered: 2026-10-22
Supersedes: nothing. `research/preregistration_v1.1.md` (2026-10-22) remains **in
force** for the retrospective panel. This file pre-registers **one added arm**,
**PH-1**, and changes **no** element of v1.1. Recorded in
`research/prompt_changelog.md` (Iteration 9).

Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`
(v1.0, 2026-10-21).
Binding design constraints: the canonical hypothesis-factory dossier, specification
**V-009 (IDEA-011 ACCTCLOCK)**, in particular Cycle-56 amendment item 4 (a
prospective holdout must be registered before the outcome can occur).

Status: **Pre-registered, untested.** No outcome-period return has been computed or
inspected in this repository, for the retrospective panel or for PH-1.

**Reading note.** Where PH-1 inherits a v1.1 rule unchanged, this file says so **by
reference**. The governing text is `research/preregistration_v1.1.md`. A restated
rule is a copy that can drift; a reference cannot.

---

## 0. Why PH-1 is pre-registered now, and what that buys

The retrospective panel's chronological holdout is **EMPTY** — every registered
retrospective event has T-A ≤ 2017-10-31 — and that was declared in advance
(`research/preregistration_v1.1.md` §4.1; decision **D-014**). The retrospective
panel's registered role is therefore **evidential**.

The promotable test is **PH-1**: the IFRS 18 first-application window. IFRS 18 was
issued on 9 April 2024; it is mandatory in the EU for periods beginning on or after
1 January 2027, in the UK on the same date, and in Saudi Arabia on the same date
(S-54). The first IFRS 18 reports will be the **2027 interim reporting season**,
periods ending 30 June 2027, published July–August 2027 (S-48).

**This file is registered on 2026-10-22, before any of that can be published.** The
entire value of a prospective holdout is that it was fixed before the outcome
existed. After the first IFRS 18 report is published, nothing here may be changed
in place.

## 1. Primary outcome for PH-1

**Inherits v1.1 §1 by reference, unchanged.** The primary outcome family is
**H-B′**: the transition-window abnormal return, defined on the interval
**[T-A, T-R]** — the drift between the adoption announcement and the firm's first
full report prepared under the new standard — with the **firm-level pre-adoption
information quality** as the state, estimated **within jurisdiction**, **two-sided**.
No sign is selected before the holdout is opened.

**For PH-1 specifically:** the primary outcome is the same quantity computed for the
IFRS 18 event, using the IFRS 18 event clock (T-A, T-R) and the same benchmark and
estimand. The v1.0 [T-R, T-R+20] window remains a **descriptive control**.

## 2. Estimand for PH-1

**Inherits v1.1 §2 by reference, unchanged:** the within-jurisdiction difference in
transition-window buy-and-hold abnormal return between low- and high-information-
quality firms, differenced against the same contrast measured in matched control
jurisdictions over the same calendar windows, with cluster-robust inference.

**One PH-1 addition, registered as an estimate, not as a choice.** The PH-1
estimand is reported **alongside** the pre-/post-disclosure decomposition, and the
report must state which of two readings the decomposition supports: a
**slow-diffusion** reading or a **disclosure** reading. The report **may not**
choose a reading after seeing which is larger; it reports both, with the
decomposition, and states what the decomposition supports.

## 3. Pre-registered claim about the published reading

**Inherits v1.1 §3 by reference, unchanged:** the **discontinuity-at-adoption**
reading is claimed; the comparability-as-driver reading is reported as a descriptive
control; steady-state comparability is a descriptive control only.

**PH-1 caveat, registered in advance.** For IFRS 18 the discontinuity-at-adoption
reading is **much weaker than for the retrospective panel**, because IFRS 18 changes
*presentation and disclosure* rather than measurement, and because jurisdictions
that adopt IFRS for the first time in the IFRS 18 era apply the IFRSs "all at once"
(S-54), so the sharpest part of the discontinuity is not available. PH-1 is a
**weaker test of the same claim**, and the write-up must say so rather than present
PH-1 as a like-for-like replication.

## 4. Splits for PH-1

**Inherits v1.1 §4 by reference** (development / validation / untouched holdout
anchored on T-A), **with the holdout for PH-1 being the whole of PH-1 itself.**

| Split | Rule | Status for PH-1 |
|---|---|---|
| Development | T-A before 2016-01-01 | Unchanged; **not** used for PH-1 (IFRS 18's T-A is in 2026). |
| Validation | T-A in [2016-01-01, 2019-01-01] | Unchanged; **not** used for PH-1. |
| Untouched holdout (retrospective) | T-A on/after 2019-01-01 | **EMPTY** — declared in advance (D-014). |
| **PH-1 (prospective holdout arm)** | IFRS 18 first-application events: the **2027 interim reporting season**, periods ending 30 June 2027, published July–August 2027 | **Registered here, in advance, before the first IFRS 18 report exists.** Opened **once**, under the test order in §6, after the PH-1 feasibility audit in §5 has been published. |

**The once-only rule.** The PH-1 result is computed and reported **once**. No
intermediate PH-1 quantity — not a cluster count above the minimum, not a partial
window, not a single firm's path — may be computed, inspected or reported before the
analysis in §6 is run. A peek voids the arm; a voided arm is reported as **void**,
never as a null.

## 5. Feasibility audit and power for PH-1

### 5.1 The audit

**Inherits v1.1 §5.1 by reference, unchanged**, applied to the PH-1 panel: per
event, the independent-cluster count; treatment and control firm counts; coverage by
event, jurisdiction, year and liquidity bucket; **coverage of the filing timestamps**
(including the T-PRE pre-disclosure documents); missingness; and the count of firms
whose transition window length differs materially from the control window length.

### 5.2 Expected cluster counts (a prediction, not a result)

| Stratum | Expected clusters for PH-1 | Comment |
|---|---|---|
| A — content change (IFRS 18 in an existing framework) | **≈ 3–10** | One cluster per jurisdiction that adopts IFRS 18 with a distinct application date, on the rule in `research/specification_v1.2.md` §1.1. The EU is a **single** timing cohort, not 27 independent ones, and this is stated now so it cannot be discovered later as a power surprise. Saudi Arabia is a second cohort with its own date. |
| B — framework change (first-time IFRS adopters) | **0** | Settled in advance, in the negative: the IFRS 18 instruments converge on one application date and first-time adopters apply the IFRSs "all at once" (S-54). The contrast degenerates and is not built. |
| **Total** | **≈ 3–10** | **Below the ≥12 minimum.** This is stated in advance, and it is the reason the PH-1 arm is registered as a **narrower and weaker** test than the retrospective panel rather than as a stronger one. |

### 5.3 The rule that binds if the audit falls short (frozen)

> If the realised independent-cluster count for PH-1 is **< 12** or the treatment-firm
> count is **< 200**, the **PH-1 primary estimand is inconclusive by construction** —
> the same rule, and the same precedent, that `research/preregistration_v1.1.md` §5.3
> already froze for the retrospective panel. The descriptive results are still produced
> for the record, and the decision is **park** or **inconclusive** — never "pass".
>
> **The rule is fixed here so that a short arm cannot later be used as a reason to
> change the panel, the window, or the thresholds.**

**Consequence, stated plainly and in advance.** On the cluster arithmetic in §5.2,
PH-1 is **expected** to fall below the ≥12 minimum. If it does, the honest outcome
is that the campaign has an **evidential** retrospective panel and **no promotable
test**, and the report must say exactly that. **The number of clusters does not get
repaired by widening the panel after the fact**, and the panel rule in
`research/specification_v1.2.md` §1.1 is frozen before the audit begins.

### 5.4 Minimum detectable effect

**Inherits v1.1 §5.4 by reference, unchanged.** With 12 independent clusters the
design is powered (80%) only for an effect of roughly 0.5–0.7% per event. If the
observed effect is smaller, the correct conclusion is **inconclusive**, not "no
effect". The power calculation is computed and reported **before** the primary model
is estimated, for each arm separately.

## 6. Test order for PH-1 (frozen)

**Inherits v1.1 §6 by reference, unchanged, applied to PH-1**, with the pre-emption
step anchored on the **real** mandated disclosure rather than on an analogue:

1. **Feasibility and event-count audit** (§5). Report and **stop** if the counts fall
   below the pre-registered minimums.
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
   that out-of-sample step, and it is opened only after the retrospective validation
   decision is recorded.
7. **Robustness and red-team** — placebo dates, placebo standards, false event
   assignments, leave-one-event-out, outlier exclusion, pre-/post-2010 subperiod,
   regime slices, alternative windows, and the pre-registered multiple-comparison
   adjustment.

**The PH-1 additions, in the same order.**

- **6a. The pre-/post-disclosure decomposition (mandatory, whatever the result).**
  The transition window is split at T-PRE; both parts are reported for the treated
  firms and for the matched controls. This is the decomposition that decides between
  the slow-diffusion reading and the disclosure reading (v1.2 hypothesis P7, CH-10).
- **6b. The disclosure-specificity split (descriptive, pre-registered, not pooled).**
  Treated firms are split into **company-specific quantified impact** /
  **company-specific unquantified impact** / **standardised or absent** pre-disclosure.
  The three groups are named in advance. This split is **not** pooled with the four
  IFRS 18 population statistics that the arm-A non-pooling rule forbids pooling
  (S-49, S-50, S-51 and the ESMA quantification series).

## 7. Statistical procedure for PH-1

**Inherits v1.1 §7 by reference, unchanged.** With **one** modification, forced by
§5.2 rather than chosen: because PH-1 is expected to have a **small** number of
independent clusters, the **jurisdiction-level randomisation test** and the
**wild-cluster bootstrap** are reported as the **primary** inference for PH-1, with
the cluster-robust standard error reported alongside, and the report states the
**number of independent clusters** in the abstract and in the conclusion. No
inference method may be switched after the result is seen.

## 8. Data requirements for PH-1

**Inherits v1.1 §8 by reference, unchanged**, plus:

- **The IAS 8.30/.31 pre-adoption impact disclosure** for every treated firm, with
  its own filing acceptance timestamp (T-PRE), hashed in the manifest chain exactly
  like a financial report, so that the disclosure-specificity classification in §6b
  is auditable after the fact;
- the **day-level IFRS 18 adoption instrument date** for every admitted
  jurisdiction, with the UK Endorsement Board decision date still **to be pinned**
  (the first concrete task of the next phase);
- **the linguistic-distance choice** (published measure if exactly reproducible,
  otherwise the registered fallback ordinal scale), recorded **before the holdout is
  opened**.

## 9. Costs and thresholds for PH-1

**Inherits v1.1 §9 by reference, unchanged.** No cost was tuned; no return exists.

## 10. Reporting commitments for PH-1

**Inherits v1.1 §10 by reference, unchanged**, and for PH-1 specifically:

- the PH-1 result is reported **once**;
- the report states the **number of independent clusters** and whether the ≥12
  minimum was met;
- the report states whether the **pre-disclosure window** carried the response;
- the report states which of the two readings — slow-diffusion or disclosure — the
  decomposition supports, and does not present the more favourable one;
- a **void** (a peek) is reported as void;
- the campaign's own status line — **PARKED, not validated, not rejected** — is
  carried into the PH-1 write-up unchanged, and a null in this design is reported
  as a **contribution, not a replication** (S-37 / V-009 G-21).

## 11. Status

PH-1 is **registered and untested**. It is blocked on the same authorisation items
as the retrospective panel (**A1** market data, **A2** read-only public harvesting,
**A4** panel scope) and on one item of its own: the **day-level IFRS 18 adoption
instrument date** per admitted jurisdiction, beginning with the UK Endorsement
Board's IFRS 18 decision record.

Registering PH-1 does **not** unblock anything, and it does not license any result.
It fixes the test **before** the outcome exists, which is the only thing it can do
at this point. The campaign remains **PARKED — not validated, not rejected.**

## 12. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Frozen outcome, estimand, splits (by T-R), test order, thresholds, costs. |
| v1.1 | 2026-10-22 | Transition-window state contrast; splits re-anchored on T-A; retrospective holdout **empty**, declared in advance; feasibility, cluster-count and power rules fixed; published reading pre-registered; pre-emption window registered as a kill signal. |
| **v1.2** | **2026-10-22** | **PH-1 registered as the prospective holdout arm** on the IFRS 18 first-application window: the once-only reporting rule; the **real** mandated pre-disclosure anchor T-PRE; the mandatory pre-/post-disclosure decomposition; the disclosure-specificity descriptive split and the arm-A non-pooling rule; the slow-diffusion-versus-disclosure reading rule; the **expected** sub-minimum cluster count stated in advance with the consequence fixed (inconclusive by construction, never "pass"); inference fixed in advance to the jurisdiction-level randomisation test and the wild-cluster bootstrap as primary. Registered **before the first IFRS 18 report can be published**. |

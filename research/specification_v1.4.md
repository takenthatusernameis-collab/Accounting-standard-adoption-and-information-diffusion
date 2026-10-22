# ACCTCLOCK — Specification v1.4 (amendment to the PH-1 arm)

**Status: registered 2026-10-22, before the holdout was opened and before any
outcome-period return was computed or inspected in this repository.**

This file **amends `research/specification_v1.2.md` and
`research/specification_v1.3.md` in the places named in §0 below, and changes
nothing else.** Every part of v1.2 and v1.3 that is not named in §0 remains in
force verbatim. The **hypothesis is not amended**: `research/hypothesis_v1.3.md`
remains in force, because no claim, acceptance criterion or kill condition
changes here — only the *evidence* about the panel and a *stale expectation* are
corrected, which is the reasoning of **D-029**.

---

## 0. What this file changes, and why it is allowed to change it

| § | Element | Change | Authority |
|---|---|---|---|
| 1.2 | PH-1 condition-2 anchors | **Extended from five instruments to ten**, and corrected to include the five that D-026/D-030 had added to the panel without amending the registered table: Philippines 2024-05-10, Malaysia 2024-06-14, Hong Kong SAR 2024-07-09, Indonesia 2025-05-28, New Zealand 2024-05-23. | decisions **D-033**, **D-030**, **D-026**; source ledger S-91, S-92, S-93, S-94, S-98, S-72. |
| 1.3 | PH-1 panel, route evidence | **Two additive evidence columns** (`profile_route_hint`, `timing_cohort`) are carried in `research/panel_v1.2.csv`. **No membership condition is added, changed or removed.** | decision **D-034**; `scripts/build_panel.py::classify_profile_route`. |
| 1.4 | PH-1 panel, the EU cohort | **The member-state carve-out check is named and declared outstanding.** The 27 member states are recorded as joining the EU cohort on the *route*, with **T-A left empty** until the check is done. | decision **D-034**; source ledger S-54, S-60. |
| 2.3 | PH-1 event clock, T-E | **A jurisdiction whose IFRS 18 application date is not 2027-01-01 is outside the arm.** Thailand is recorded as failing the T-E condition on a primary-verified application date of 2028-01-01. | decision **D-034**; source ledger S-96. |
| 5 | Cluster arithmetic | **Restated from ≈ 4–8 to ≈ 10–13**, against an **unchanged ≥ 12 minimum**. | decision **D-034**. |

**Why amendment is permitted.** The registered arm's **panel, window, thresholds,
exit rules, cost table and acceptance criteria are frozen**; a change to any of
them requires a further registered version. What is amended here is (i) a table
of *primary-verified anchors* and (ii) a *stated expectation* about a quantity
that has moved because more instruments were verified — both **design inputs to
the feasibility audit**. The ≥ 12 threshold, the treatment definition, the
estimand, the test order, the split rules and the reporting commitments are
**untouched**, and the frozen rule that binds if the audit falls short
(`research/preregistration_v1.2.md` §5.3) is untouched.

---

## 1. The PH-1 panel

### 1.1 The membership rule (unchanged)

The five conditions of `research/specification_v1.1.md` §4.2 are unchanged, the
candidate universe is unchanged at **141 jurisdictions**, and no jurisdiction has
been added or removed by hand. The panel is still built by rule from the dated
IFRS Foundation profile snapshot of 2026-10-22 (S-58) and every row still carries
`in_registered_panel = pending`.

### 1.2 Condition 2: the primary-verified instruments — **extended to ten**

Every T-A below is a **day-level** date carried by a **primary source that was
read directly and hashed** in this campaign; the retrieval record for each is in
`research/manifests/source_ledger_verification.jsonl`. Where two primary dates
exist for one jurisdiction, both are recorded in the panel row's `date_conflict`
field and the conflict is left open (D-011, D-016).

| Jurisdiction | Instrument | T-A | Application | Source |
|---|---|---|---|---|
| Philippines | PFRS 18, adopted by the Financial and Sustainability Reporting Standards Council | **2024-05-10** | annual periods beginning on or after 2027-01-01 | S-94 |
| New Zealand | NZ IFRS 18, issued by the NZ Accounting Standards Board under s. 12(a) of the Financial Reporting Act 2013 | **2024-05-23** | annual periods beginning on or after 2027-01-01 | S-72 |
| Malaysia | MFRS 18, notice of issuance by the Malaysian Accounting Standards Board under s. 7(1) of the Financial Reporting Act 1997 | **2024-06-14** | annual reporting periods beginning on or after 2027-01-01 | S-91, S-98 |
| Hong Kong SAR | HKFRS 18, issued by the HKICPA's Financial Reporting Standards Committee | **2024-07-09** | financial periods beginning on or after 2027-01-01 | S-92 |
| Singapore | SFRS(I) 18, issued by the Accounting Standards Committee of ACRA | **2024-10-04** | annual reporting periods beginning on or after 2027-01-01 | S-76 |
| Saudi Arabia | SOCPA adoption of IFRS 18 (Accounting Standards Council resolution 25/06/1446H) | **2024-12-26** | periods beginning on or after 2027-01-01 | S-61 |
| Indonesia | PSAK 118, ratified by the Indonesian Accounting Standards Board (DSAK IAI) | **2025-05-28** | periods beginning on or after 2027-01-01 | S-93 |
| United Kingdom | UK Endorsement Board adoption of IFRS 18 for use in the UK | **2025-12-10** | periods beginning on or after 2027-01-01 | S-63, S-69 |
| Brazil | Resolução CVM nº 237, de 23 de dezembro de 2025 (approves CPC 51, aligned to IFRS 18; Article 1 makes it mandatory for the listed companies; Article 3 brings it into force on 2027-01-01) | **2025-12-23** | financial years beginning on or after 2027-01-01 | S-77 |
| European Union | Commission Regulation (EU) 2026/338 | **2026-02-13** (OJ publication 2026-02-16) | periods beginning on or after 2027-01-01 | S-54, S-60 |

**The ten T-A dates span twenty-one months** (2024-05-10 → 2026-02-13) and are
**ten distinct dates**.

**Recorded as attempted and NOT verified** — their T-A stays empty and their rows
stay `pending` (D-011): **Hong Kong SAR** was verified in this round and no
longer belongs here; the rows in this state are **South Africa** (incorporation
by reference, no dated local instrument), **South Korea** (K-IFRS No. 1118,
announced December 2025, no day-level date), **Pakistan** (SECP S.R.O. 2444(I)/2025
— every path on `secp.gov.pk` answered HTTP 403, S-99), **Sri Lanka** (SLFRS 18
listed for 2025, no day-level date) and **Thailand** (T-E ground, §2.3 below).

### 1.3 The route columns are triage, not membership — **new**

`research/panel_v1.2.csv` carries two **additive evidence columns** on top of the
retrospective panel's schema: `profile_route_hint` and `timing_cohort`. The
retrospective file `research/panel_v1.1.csv` is **unchanged**.

`profile_route_hint` reads the *reporting framework* that the dated jurisdiction
profile records, by a fixed deterministic rule (`classify_profile_route` in
`scripts/build_panel.py`):

| Class | Count | Meaning |
|---|---|---|
| `eu_member_state` | 27 | The profile records the IFRS Accounting Standards **as adopted by the EU**. |
| `eea_efta_own_instrument` | 3 | Norway, Iceland and Liechtenstein — **identical profile text** to the member states', but their route to the EU-endorsed IFRS runs through their **own** incorporation instrument. |
| `national_equivalent_profile` | 9 | The profile names a **national equivalent** framework (Hong Kong SAR, Indonesia, Malaysia, Myanmar, Nepal, New Zealand, the Philippines, Chinese Taipei, Thailand). |
| `standing_reference_profile` | 98 | The profile records adoption by **standing reference** to the IASB's standards. |
| `no_profile_status_text` | 4 | The profile carries no status text (the European Union, Nicaragua, Sri Lanka, Switzerland). |

**This classification never excludes a jurisdiction**, and the panel's own data
contains the counterexamples that prove it: **Brazil's** profile says only
*"Required."* and **Saudi Arabia's** records the IFRS Accounting Standards, yet
both carry dated national instruments (CVM Resolution 237; the SOCPA
resolution), and **South Korea's** profile records *"adopted IFRS Accounting
Standards"* while the KASB issued K-IFRS 1118. A standing-reference profile is a
**triage prior** — it says where to look for an instrument, and it is where the
remaining condition-2 effort is aimed.

### 1.4 The EU cohort and the outstanding carve-out check — **new**

The 27 member states apply the EU-endorsed standard through Commission
Regulation (EU) 2026/338, so they join the **2026-02-13** cohort and are **one**
cluster, not twenty-seven — the rule already fixed in the v1.1 pre-registration.
But a member state with a **permanent derogation** from particular endorsed
standards (Poland's bank and insurer derogations from IFRS 9 and IFRS 15 are the
known case) is not simply in the cohort. **Condition 2 is therefore not yet
verified for the member-state rows, and their T-A is left empty** rather than
inherited silently; their `timing_cohort` carries the EU date as the route, not
as a verified anchor.

The three EEA/EFTA states reach the EU-endorsed IFRS through their **own**
incorporation instruments, so their T-A is a separate question and is also empty.

**The carve-out check is named, queued and outstanding.** It is read-only work
and needs no authorisation.

---

## 2. The PH-1 event clock

### 2.1 T-A, T-A1, T-E (unchanged in structure)

Unchanged from v1.1 and v1.3: **T-A** is the jurisdictional legal-adoption date;
**T-A1** is the IASB issuance date (2024-04-09) and is *not* the event clock;
**T-E** is the first-application date (2027-01-01) for every jurisdiction in the
arm. The pre-disclosure window is **[T-A, T-PRE]** with the interval condition
**T-A < T-PRE < T-R** (v1.3 §2.2), and the Saudi row is admitted on that basis.

### 2.2 T-PRE and the pre-disclosure window (unchanged)

Unchanged from v1.3.

### 2.3 A jurisdiction whose application date is not 2027-01-01 is outside the arm — **new**

PH-1 is the **IFRS 18 first-application window**: T-E is 2027-01-01 for every
jurisdiction in the arm, because IFRS 18 applies to annual periods beginning on
or after that date. A jurisdiction that adopts IFRS 18 **a year later** has a
different transition window and cannot share the arm's.

**Thailand** is the case in point, and it is decided on a **primary-verified**
application date: the Thai Accounting Professions Council's own register records
that TFRS 18 has effect for accounting periods beginning on or after
**1 January B.E. 2571 = 1 January 2028** (S-96). Thailand therefore fails the
arm's **T-E condition**, whatever its T-A turns out to be, and its row stays
`pending` with an empty T-A. The ground is recorded **now**, before the holdout
opens, so that it is not later settled in the light of an outcome. (Thailand's
T-A is separately not verified at day level — S-96, S-97.)

---

## 3. Mandatory country-level controls (unchanged)

Unchanged from v1.3: the enforcement-quality and linguistic-distance controls,
the LD-0 … LD-4 categories and their boundaries, and the validation result
(Spearman 0.9776) all remain in force.

---

## 4. Everything else (unchanged)

The panel, the window, the thresholds, the exit rules, the cost table and the
acceptance criteria are **unchanged**. The campaign remains **PARKED — not
validated, not rejected** — and the arms remain blocked on **A1** and **A2**.

---

## 5. The cluster arithmetic — **restated**

| Quantity | Value |
|---|---|
| Distinct T-A dates verified today | **10** (2024-05-10, 2024-05-23, 2024-06-14, 2024-07-09, 2024-10-04, 2024-12-26, 2025-05-28, 2025-12-10, 2025-12-23, 2026-02-13) |
| Jurisdictions admitted to those cohorts | 10 anchor jurisdictions + the 27 member states, which join the EU cohort on the route and remain `pending` until the carve-out check is done |
| Independent timing cohorts if every anchor is admitted and no further instrument is found | **10** |
| Plausible range once the outstanding checks are done | **≈ 10–13** |
| Pre-registered minimum | **≥ 12** (unchanged) |

**The arm is no longer *certainly* inconclusive, and it is not yet shown to be
feasible.** The decisive quantity is **identified and bounded**: it is the number
of jurisdictions that issue their **own dated IFRS 18 instrument**, and that is a
handful, not a hundred. Two named tasks dominate it, both read-only and both
needing no authorisation: (i) the remaining local-equivalent jurisdictions —
South Korea, Pakistan, Sri Lanka, Myanmar, Nepal, Chinese Taipei, Mongolia,
Bhutan, Israel; and (ii) the EU member-state carve-out check.

**The ≥ 12 threshold is not moved.** A short arm binds the conclusion, and the
rule that binds if the audit falls short is frozen in
`research/preregistration_v1.2.md` §5.3 and is restated, unchanged, in
`research/preregistration_v1.4.md` §5.3.

---

## 6. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Frozen ten elements; the treatment definition produced an empty treatment group (D-009). |
| v1.1 | 2026-10-22 | Executable treatment, staggered-timing panel with a registered membership rule, mandatory controls with a three-part imposition, transition-window primary rule, pre-emption kill-signal arm, mechanical-magnitude attribution. Registered before any outcome-period return was computed. |
| v1.2 | 2026-10-22 | Adds the **PH-1** prospective arm: the panel membership rule with its five conditions, the IFRS 18 event clock, the once-only reporting rule, the pre-/post-disclosure decomposition, the disclosure-specificity split, the expected sub-minimum cluster count stated in advance. |
| v1.3 | 2026-10-22 | Amends v1.2 in four places and nothing in v1.1: the candidate universe corrected to 141; the T-A anchor table corrected and extended to five; the pre-disclosure window defined by the interval condition T-A < T-PRE < T-R, resolving the Saudi question in favour of admission; the linguistic-distance control closed. |
| **v1.4** | **2026-10-22** | **Amends v1.3 in five places and nothing in v1.1 or v1.2.** (i) The **T-A anchor table is extended to ten** primary-verified instruments, which are ten distinct dates spanning twenty-one months (D-033); (ii) **two additive route-evidence columns** are carried in the PH-1 panel, and the route class is declared to be **triage, never a determination** (D-034); (iii) the **EU member-state carve-out check is named and outstanding**, and the member states' T-A stays empty until it is done (D-034); (iv) a **T-E ground for exclusion** is registered, and Thailand is excluded from the arm on a primary-verified 2028-01-01 application date (D-034); (v) the **cluster arithmetic is restated as ≈ 10–13** against an **unchanged ≥ 12 minimum** (D-034). The hypothesis is **not** amended. |

---

**Boundary.** Nothing in this file licenses a result. The campaign remains
**PARKED — not validated, not rejected**; the arms remain blocked on **A1** and
**A2**; and no outcome-period return has been computed or inspected in this
repository at any point.

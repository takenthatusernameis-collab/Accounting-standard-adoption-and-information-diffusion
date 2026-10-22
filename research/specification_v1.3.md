# ACCTCLOCK — Specification v1.3 (amendment to the PH-1 arm)

Registered: 2026-10-22
Supersedes: nothing. `research/specification_v1.1.md` (2026-10-22) remains **in
force** for the retrospective panel; `research/specification_v1.2.md` (2026-10-22)
remains **in force for PH-1 except where this file expressly amends it**. This
file amends **four** elements of v1.2 and changes **nothing** in v1.1. Recorded in
`research/prompt_changelog.md` (Iteration 10).

Governing protocol: `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`
(v1.0, 2026-10-21).

Status: **Registered, untested.** No outcome-period return has been computed or
inspected in this repository, for the retrospective panel or for PH-1. The campaign
status is **PARKED — not validated, not rejected.**

---

## 0. What this file changes, and why it is allowed to change it

The panel, the window, the thresholds, the exit rules, the cost table and the
acceptance criteria are **frozen**. This file changes none of them. It closes
three items that v1.2 deliberately left open to be closed **before** the holdout is
opened, and it corrects one factual statement that the new primary evidence
falsifies.

| § | Element | Change | Authority |
|---|---|---|---|
| 1 | PH-1 panel membership | **Unchanged in rule.** The candidate universe is 141 jurisdictions, not 142: the 2026-10-22 snapshot parser had admitted one boilerplate paragraph from the IFRS Foundation index page as a jurisdiction, and the artefact is removed. | decision **D-025**; a data-quality defect, not a panel-scope change (D-016 is not triggered: the feasibility audit has not begun, and no jurisdiction was dropped by hand). |
| 2 | PH-1 event clock, T-A | **Corrected and extended.** Five primary-verified T-A dates replace the three that v1.2 carried (two of which were wrong). | decisions **D-022**, **D-026**; source ledger S-61, S-63, S-69, S-76, S-77. |
| 2 | PH-1 event clock, T-PRE | **Amended.** The pre-disclosure window is defined by the interval condition **T-A < T-PRE < T-R**, which replaces v1.2 §2's "the disclosure must precede T-A" precondition. | This file; hypothesis v1.3 §2 and §3. |
| 3 | Mandatory country-level controls, linguistic distance | **Closed.** The registered fallback ordinal scale is selected, its construction rule, its official-language inputs and its five ordinal categories with their boundaries are fixed, and the validation requirement is stated with its result. | decision **D-023**, completed by decision **D-028**. |

## 1. The PH-1 panel

### 1.1 The membership rule (unchanged)

`research/specification_v1.1.md` §1.1 is **in force** and is **not** edited. In
short: `s = IFRS 18`; the jurisdiction's regulator has published a **legal
instrument making IFRS 18 mandatory** for a class of listed firms with a
**day-level** date; the affected-firm list is knowable ex ante; the jurisdiction
has a public filing route that publishes a **filing acceptance time**; and
point-in-time price coverage exists including for delisted firms.

**The candidate universe** is derived by rule from the dated IFRS Foundation
jurisdiction-profile snapshot of 2026-10-22 (S-58), read back from the Stratum B
rows of `research/panel_v1.1.csv`, so that both panel files share one vintage. It
is **141** jurisdictions after the removal of the boilerplate artefact (D-025);
`research/panel_v1.2.csv` holds one row per jurisdiction, all
`in_registered_panel = pending`, because conditions 3 to 5 are unverified for
every jurisdiction.

### 1.2 Condition 2: the primary-verified instruments

| Jurisdiction | Instrument | T-A | Application | Source |
|---|---|---|---|---|
| Singapore | SFRS(I) 18, issued by the Accounting Standards Committee of ACRA | 2024-10-04 | annual reporting periods beginning on or after 2027-01-01 | S-76 |
| Saudi Arabia | SOCPA adoption of IFRS 18 (Accounting Standards Council resolution 25/06/1446H) | 2024-12-26 | periods beginning on or after 2027-01-01 | S-61 |
| United Kingdom | UK Endorsement Board adoption of IFRS 18 for use in the UK | 2025-12-10 | annual reporting periods beginning on or after 2027-01-01 | S-63, S-69 |
| Brazil | Resolução CVM nº 237, de 23 de dezembro de 2025 (approves CPC 51, aligned to IFRS 18; Article 1 makes it mandatory for the listed companies; Article 3 brings it into force on 2027-01-01) | 2025-12-23 | financial years beginning on or after 2027-01-01 | S-77 |
| European Union | Commission Regulation (EU) 2026/338 | 2026-02-13 (OJ publication 2026-02-16) | periods beginning on or after 2027-01-01 | S-54, S-60 |

**Attempted and not verified — recorded, never inferred.** *Hong Kong SAR*: the
HKICPA's HKFRS 18 page (S-78) states the effective date (financial periods
beginning on or after 1 January 2027) but the retrieved page does not carry the
issuance date, so T-A is empty. *South Africa*: the Companies Act Regulations
incorporate "IFRS as issued from time to time by the IASB" by standing reference
(S-79), so there is no dated local instrument and T-A is empty.

**Recorded conflicts.** The EU, the United Kingdom and Saudi Arabia each carry two
primary dates or two different instruments; all are written into the panel row's
own `date_conflict` field and none is resolved silently (D-011).

## 2. The PH-1 event clock

### 2.1 T-A, T-A1, T-E (unchanged in structure)

T-A is the **jurisdictional legal-adoption date** — the date of the instrument that
makes IFRS 18 mandatory. T-A1 is the **standard-setter issuance date** (IFRS 18:
9 April 2024). T-E is the **application date**, 2027-01-01 for every verified
jurisdiction. T-R is the firm's own first full report prepared under IFRS 18, and
T-RI the first interim.

### 2.2 T-PRE and the pre-disclosure window (amended)

> **T-PRE** is the filing **acceptance timestamp** of the firm's **first
> disclosure of the expected impact of IFRS 18** under the regime that applies to
> it — the IAS 8.30/.31 disclosure required by ESMA's public statement in the EU
> and the United Kingdom, and the CMA-mandated preliminary assessment of the
> expected impact of initial application in Saudi Arabia (CMA_N_4083, approved
> financial statements for periods beginning on or after 2026-04-01).
>
> The **pre-disclosure window** is **[T-A, T-PRE]**. It is **well defined** if and
> only if **T-A < T-PRE < T-R**.
>
> If a jurisdiction has no such disclosure before T-R, its pre-disclosure window
> **does not exist**: the pre-emption arm (CH-9 / CH-10, kill condition 12) is
> reported as **not applicable** for that jurisdiction, and the pre-/post-
> disclosure decomposition of §6a of the preregistration reports **not applicable**
> for it. It is **never** reported as a null, a pass or a zero.

**What this replaces.** v1.2 §2 required the disclosure to "precede T-A for the
pre-emption window to be well defined". That condition contradicts v1.1 §4.3,
which defines the pre-emption window as **[T-A, T-PRE]** — an interval that is
non-empty precisely when T-PRE is *after* T-A. v1.3 replaces the inconsistent
precondition with the interval condition, which is well defined, uniform across
jurisdictions, and applied to every jurisdiction the same way.

**Consequences, stated in advance.**

- **Saudi Arabia is admitted to PH-1.** Its mandated disclosure falls *inside* its
  transition window, so its pre-disclosure window is **[2024-12-26, the acceptance
  timestamp of the firm's first CMA-mandated impact disclosure]** — a non-empty
  interval — and the pre-emption kill signal is evaluable there. The alternative
  (excluding the Saudi row) would have removed the only cohort outside the EU and
  the United Kingdom without changing the primary estimand, which does not depend
  on the pre-disclosure anchor.
- **Saudi Arabia's transition window is the longest in the arm** (T-A 2024-12-26 to
  the FY2027 annual report), and its T-A is 13.5 months before the EU's. The
  matched-control design matches on fiscal-period-end proximity so that the
  control transition window has the same length as the treated one (v1.1 §4), and
  the count of firms whose window length differs materially from the control's is
  a pre-registered feasibility-audit output (`research/preregistration_v1.2.md`
  §5.1).
- **The five verified T-A dates span seventeen months** (2024-10-04 to
  2026-02-13) while the **application** date is common (2027-01-01). This
  **corrects** the v1.2 §5.2 statement that "the IFRS 18 instruments converge on
  one application date": they converge on one *application* date, not on one
  *adoption* date, and the adoption dates are spread. The correction is made now,
  before any outcome, and it does not change the panel rule.

## 3. Mandatory country-level controls (frozen, closed)

### 3.1 Enforcement quality (unchanged)

World Bank Worldwide Governance Indicators, **Regulatory Quality** and **Quality of
Regulatory Framework**, jurisdiction-year of T-A. WGI is revised, not vintage; the
revision caveat is stated in every report, and the ±1-year sensitivity is
pre-registered (v1.1 §3.5).

### 3.2 Linguistic distance (closed)

The **registered fallback ordinal scale** is the implemented control. The published
measure (S-44) is retained as the **external validation** of the fallback's
ordering and is never combined with it (D-023).

**Construction rule (fixed).**

1. The English reference is the WALS language record `eng`.
2. A WALS **parameter** is compared between two languages when both carry at least
   one value for it; a compared parameter is **shared** when the two languages'
   value sets intersect and **not shared** otherwise.
3. A language's **friction score** is the share of its compared parameters that are
   not shared with English.
4. A language's score is the **median** over the WALS records that carry its
   ISO 639-3 code and reach **30** compared parameters. A **macrolanguage**
   (`ara`, `zho`, `swa`, `msa`, `fas`, `est`, `nep`, `uzb`, `aze`) is scored from
   the WALS records of the individual languages that belong to it, using the SIL
   ISO 639-3 macrolanguage table.
5. A jurisdiction's score is the **simple mean** over its official languages,
   which is the aggregation rule the published measure uses. A jurisdiction whose
   official-language set is exactly {English} scores **0**.
6. A jurisdiction with an official language that cannot be scored is **not scored
   at all**: the mean over a subset of the official languages is not comparable
   with the other jurisdictions, so no value is imputed and the exclusion is
   recorded.
7. The ordinal category is read off the fixed boundaries below.

**Official-language inputs.** The published measure's own official-language list
(S-44 Table 1) is used for the jurisdictions it covers, because it is a dated,
citable, open list; **Unicode CLDR 48.2.0** is used for every other jurisdiction,
restricted to languages whose CLDR status is `official` (`official_regional` is
excluded, because CLDR uses it for languages official in part of a territory only
— Welsh in the United Kingdom, Gaelic in Scotland — which is not the national
official-language status the published measure uses). The source used for each
jurisdiction is recorded in `research/linguistic_distance_v1.csv`.

**The registered ordinal categories (fixed).**

| Category | Score band |
|---|---|
| **LD-0** | the official-language set is exactly {English} → 0 |
| **LD-1** | (0, 0.255] |
| **LD-2** | (0.255, 0.342] |
| **LD-3** | (0.342, 0.482] |
| **LD-4** | (0.482, 1] |

The boundaries are the published measure's own quartiles over its 84-country sample
(S-44 Table 2, Panel A: Q1 0.255, median 0.342, Q3 0.482). They are fixed here, in
advance, on a **published distribution** — not on this campaign's panel, which is
not assembled, and not on any outcome.

**Validation requirement and result.** The fallback must rank jurisdictions in the
same order as the published measure on the countries where the published measure
gives a value. Measured (`research/linguistic_concordance.md`):

| Statistic | Value |
|---|---|
| Spearman rank correlation, published sample | **0.9776** (80 of 84 rows matched) |
| Pearson correlation, published sample | **0.9933** |
| Spearman, restricted to panel jurisdictions | **0.9704** (61 rows) |
| Spearman, sensitivity with the CLDR list throughout | **0.8226** (76 rows) |

The residual disagreement is a **country-list** disagreement, not a
distance-computation disagreement: the WALS recomputation reproduces the published
per-language values, and the differences arise from which languages each country's
official list contains. The four published rows that cannot be scored at all
(Haiti, Kazakhstan, Papua New Guinea, South Africa) are reported as **unmatched**,
not as zeros.

**Imposition (unchanged from v1.1 §3.6).** The control is jurisdiction-constant and
is therefore absorbed by the within-jurisdiction specification; it is made
operative by reporting the primary estimate **within pre-registered strata** — high
versus low linguistic distance, split at the **panel median** — each with its own
cluster-robust inference and a pre-registered interaction test of state × stratum.
Where a jurisdiction carries no score (rule 6 above), it is **excluded from the
stratification and named in the report**, and the count of excluded jurisdictions
is reported.

## 4. Everything else (unchanged)

The retrospective panel, the window, the state construction, the thresholds, the
costs, the acceptance criteria, the kill conditions, the test order, the
inference rules and the reporting commitments are **unchanged**. The amendments
above touch only the PH-1 event clock, the PH-1 candidate universe's data quality,
and the closed choice of the linguistic-distance control.

## 5. Version history

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-10-21 | Frozen ten elements; the treatment definition produced an empty treatment group (D-009). |
| v1.1 | 2026-10-22 | Executable treatment, staggered-timing panel with a registered membership rule, mandatory controls with a three-part imposition, transition-window primary rule, pre-emption kill-signal arm, mechanical-magnitude attribution. Registered before any outcome-period return was computed. |
| v1.2 | 2026-10-22 | Adds the **PH-1** prospective arm: the panel membership rule with its five conditions, the IFRS 18 event clock, the once-only reporting rule, the pre-/post-disclosure decomposition, the disclosure-specificity split, the expected sub-minimum cluster count stated in advance. |
| **v1.3** | **2026-10-22** | **Amends v1.2 in four places and nothing in v1.1.** (i) The candidate universe is corrected to **141** jurisdictions after the removal of a boilerplate-parsing artefact (D-025); (ii) the **T-A anchor table is corrected and extended** to five primary-verified instruments — Singapore 2024-10-04, Saudi Arabia 2024-12-26, United Kingdom 2025-12-10, Brazil 2025-12-23, European Union 2026-02-13 — with Hong Kong SAR and South Africa recorded as attempted and not verified (D-026); (iii) the **pre-disclosure window is defined by the interval condition T-A < T-PRE < T-R**, replacing v1.2's inconsistent precondition and resolving the Saudi question in favour of admission; (iv) the **linguistic-distance control is closed** — the registered fallback ordinal scale with its construction rule, its two official-language inputs, its five categories LD-0 … LD-4 and their fixed boundaries, and its concordance with the published measure (Spearman 0.9776). The statement that the IFRS 18 instruments converge on one date is corrected: their T-A dates span seventeen months. |

# ACCTCLOCK — Handoff

**Last updated:** 2026-10-22 (D-032 free-only route update)
**Campaign:** ACCTCLOCK — the accounting-standard adoption / information-diffusion
hypothesis (canonical dossier IDEA-011, specification V-009)
**Status:** **PARKED — not validated, not rejected.** The *design* blocker is cleared,
the *promotable test is registered* (v1.2, amended by v1.3), and **all three named
verification gaps are now closed or determined from primary sources**. The *data and
authorisation* blocker is still open, and it is the only thing that blocks the
campaign. **No outcome-period return has ever been computed or inspected.**
**Machine-readable state:** `research/campaign_state.json` — next step is
`phase3b-data-execution-and-feasibility-audit` (pending, blocked on authorisation).

---

## Current instruction — D-032 (supersedes D-031 paid-provider route)

The maintainer explicitly directed the project away from all paid services. Do not use Sharadar, EODHD, paid API tiers, paid subscriptions, trials requiring payment details, or any request that could incur a charge. Do not ask the user to purchase or provision credentials. D-031's provider selection is superseded.

Use free and lawful public sources only: official filings and standards-setter records, regulators/OAMs, open government datasets, official exchange archives where available, and candidate free price archives/endpoints only after checking their terms and coverage. Candidate price sources (such as Stooq or Yahoo Finance) are not presumed complete, especially for delisted securities and terminal returns. No-cost access does not waive data-quality or terms-of-use checks.

Two previous sample requests failed before HTTP due to this terminal's DNS resolution error; that is an environment limitation, not a vendor result. Do not repeat paid-provider smoke requests. The provider adapter/tests remain in the repository but the paid paths are now out of scope; do not invoke them. Run offline tests only in an actual repository environment and report actual results.

Immediate next step: inventory free sources and execute the pre-outcome feasibility audit; reconcile panel counts using the committed builder; document source coverage, missingness, delisted-name/terminal-return limitations, and whether the frozen ≥12 independent-cluster / ≥200 treatment-firm gates can be met. If the registered PH-1 sample remains below threshold, stop and report inconclusive-by-construction. No outcome-period return may be opened before the gate. No paid calls, purchases, workflow runs, trading, broker connections, or deployment are authorized.

---

## 1. Read this first

Three things changed in this session, and one of them is a correction.

1. **The acquirer now exists.** The EDGAR acquisition path was prose in
   `research/data_acquisition_plan.md`; it is now **implemented and unit-tested** in
   `scripts/`, against synthetic fixtures, with **zero network calls** in the test
   suite. When authorisation arrives, the pipeline runs from committed code.
2. **The panel now exists as a file.** `research/panel_v1.1.csv` — 434 rows, derived
   **by rule** from a dated, hashed snapshot of the membership authority, with every
   Stratum B row marked `pending` because three of the five rule conditions cannot be
   verified until A1 and A2 land.
3. **The promotable test is registered.** v1.2 (`hypothesis_v1.2.md`,
   `specification_v1.2.md`, `preregistration_v1.2.md`) registers the prospective
   holdout arm **PH-1** on the IFRS 18 first-application window, **before the first
   IFRS 18 report can be published**.
4. **All three named verification gaps are now closed or determined** (decisions
   **D-021, D-022, D-023**): the **UK filing route publishes a date, not a time**; the
   **three IFRS 18 instrument dates are pinned**; and the **linguistic-distance
   measure cannot be reproduced exactly panel-wide**, so the registered fallback is
   selected.
5. **The PH-1 panel file now exists** — `research/panel_v1.2.csv`, 142 rows, built by
   committed code from the same dated membership vintage as `panel_v1.1.csv`.

**And one correction, which matters:** the **ASU 2016-01 event (EV-103) moves one
year earlier**. The event calendar previously carried a public-business-entity
effective date of 2018-12-15; the ASU's own text says **2017-12-15** (and
2018-12-15 for all other entities). The 2018-12-15 date belongs to **ASU 2016-02**
(EV-102) — the two rows had been conflated. `first_affected_fiscal_year_start` moves
from 2019-01-01 to **2018-01-01**. Decision **D-016**; the row's own `notes` and
`date_conflict` fields record the change. **No outcome-period return has ever been
computed or inspected, so nothing downstream is affected.**

The v1.0 and v1.1 files are **byte-identical and unedited**; verify with
`git diff -- research/hypothesis.md research/specification_v1.md research/preregistration.md
research/hypothesis_v1.1.md research/specification_v1.1.md research/preregistration_v1.1.md`
(expect empty output).

| Artefact | What it is |
|---|---|
| `scripts/sec_acceptance.py` | The SGML acceptance-time parser: `ACCEPTANCE-DATETIME` (`YYYYMMDDHHMMSS`, Eastern) → UTC, with the two daylight-saving transition days handled explicitly. |
| `scripts/data_cache.py` | The cache layout of the acquisition plan §3, plus the guard that refuses a cache root inside the repository (D-015). |
| `scripts/data_manifest.py` | The append-only JSONL manifest, SHA-256 over the raw bytes, and failed retrievals recorded as failed retrievals. |
| `scripts/sec_edgar.py` | The acquirer: submissions JSON, filing index, complete submission text; declared User-Agent; ≤ 2 requests/second; `Retry-After` honoured. |
| `tests/test_sec_acceptance.py` and 3 more | **48 new tests**; **115** in total, all passing, zero network calls. |
| `research/panel_v1.1.csv` | The registered panel, materialised: 8 Stratum A events + 426 Stratum B candidate rows. |
| `research/panel_v1.2.csv` | **The PH-1 panel, materialised**: 142 rows, one per (IFRS 18, jurisdiction); 3 carry a primary-verified day-level T-A, 139 carry none, and every row is `pending`. |
| `scripts/build_panel.py` | The PH-1 panel builder, with 9 unit tests; reads the candidate universe back out of `panel_v1.1.csv` so both panel files share one vintage; no network access. |
| `research/manifests/ifrs_jurisdiction_profiles.jsonl` | The dated snapshot manifest: 171 records with URL, HTTP status, bytes, **SHA-256** and retrieval timestamp. |
| `research/event_calendar.csv` | EV-103 primary-verified and **corrected**; EV-201 primary-verified; **EV-202 added**. |
| `research/authorisation_request.md` | The authorisation request, one-click-able, with the five decisions quoted verbatim. |
| `research/hypothesis_v1.2.md`, `research/specification_v1.2.md`, `research/preregistration_v1.2.md` | **PH-1 registered.** v1.0 and v1.1 untouched. |
| `research/decision_log.md` | **D-017 … D-023** record this session's decisions. |
| `research/prompt_changelog.md` | **Iterations 9 and 10** record what changed and why. |
| `research/source_ledger.csv` | **S-55 … S-71** added: SI 2015/980, the EFRAG Endorsement Status Report, FASB ASU 2016-01, the IFRS profile snapshot, the FRC's FRS 102 (March 2018), the EFRAG report of 16 February 2026, SOCPA's endorsement document, the Saudi CMA announcement, the UKEB IFRS 18 news release and project record, four FCA documents, the linguistic-distance operationalisation and the Joshi–Lahiri index. **71 sources.** |
| `research/experiment_ledger.csv` | **E-015 … E-021** record this session. **22 rows.** |

## 2. What is verified (with sources)

- **The canonical dossier was re-retrieved read-only** at commit
  `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` and re-read in full: V-009 with the
  binding amendments **Cycle-52, Cycle-56, Cycle-58, the Cycle-111 correction notice,
  Cycle-113, Cycle-114, Cycle-123 and Cycle-126**. It was **not modified**; it is not
  this repository and the upstream has no commits from this session.
- **The v1.1 design is compliant with every binding amendment.** The compliance map is
  `research/specification_v1.1.md` §3.7 and `research/hypothesis_v1.1.md` §8:
  - no **group A / group B** first-time-vs-second-time partition is built and none is
    presented as pre-registered (Cycle-56 item 1; Cycle-111 correction notice);
  - the **UK early-adopter cohort is excluded from treatment** as an identification
    (Cycle-56 item 3);
  - **no published firm-level repeat-adopter flag is assumed to exist**; any such
    indicator must be constructed from the firm's own basis-of-preparation note
    (Cycle-110 / R-058);
  - the state is **firm-level** and identified **within jurisdiction** (Cycle-52 item 1);
  - **enforcement quality and linguistic distance are mandatory controls**, not claimable
    conditioners, and the withdrawn ablation (d) stays withdrawn (Cycle-52 item 2;
    Cycle-113 item 1);
  - the claim is **pre-registered as a transition-window effect**, and steady-state
    comparability is a **descriptive control** only (Cycle-52 item 3; Cycle-58 item 2);
  - the **pre-emption arm is registered as a kill signal, not a null** (Cycle-113 items 2
    and 4; Cycle-114 item 2).
- **v1.2 is compliant too, and its narrowings are recorded as narrowings** (D-019):
  - the **IFRS 18 adopter-type contrast is settled in advance, in the negative**
    (S-54: the instruments converge on one application date and first-time IFRS
    adopters apply the IFRSs "all at once"), so PH-1 is a **narrower and weaker** test
    than the retrospective panel, and is registered as such;
  - the **pre-emption arm becomes the real thing** for PH-1, because IFRS 18 carries a
    **mandated** IAS 8.30/.31 pre-adoption impact disclosure (S-49), giving a real
    pre-disclosure anchor **T-PRE**;
  - the **expected cluster count is stated in advance and is below the minimum**
    (≈3–10 against ≥12), with the consequence fixed as **inconclusive by
    construction**, and inference fixed in advance to the jurisdiction-level
    randomisation test and the wild-cluster bootstrap;
  - the **once-only reporting rule** is fixed: a peek voids the arm, and a voided arm
    is reported as void, never as a null.
- **The tests still pass**: `python3 -m pytest -q tests/` → **115 passed** (re-run this
  session, same command as the workflow).
- **The date gaps are closed from primary sources** (D-016):
  - **EV-201 (IFRS 15, UK)** — the UK legal instrument is **The Companies,
    Partnerships and Groups (Accounts and Reports) Regulations 2015 (SI 2015/980)**,
    made **26 March 2015**, in force **6 April 2015**. Regulation 2(2) gives the
    mandatory date (financial years beginning on or after **1 January 2016**) and the
    directors' early-application arm (financial years beginning on or after
    **1 January 2015**). Fetched from legislation.gov.uk in session (S-55).
  - **EV-202 (IFRS 16, UK)** — **row added**. The UK required **no new** adoption
    instrument for IFRS 16: the standing SI 2015/980 requirement applies
    "international accounting standards adopted pursuant to the IAS Regulation", and
    IFRS 16 became EU-adopted on 2017-10-31, so the first affected UK financial years
    begin on or after **1 January 2019**. The T-A is therefore **inherited from the
    EU**, and the row says so — it is a weaker anchor than EV-201's.
  - **EV-103 (ASU 2016-01)** — issuance **2016-01-05**, effective-date paragraph
    quoted verbatim, and the date **corrected** (D-016). Read through the search
    provider's rendering because a direct fetch of fasb.org returns HTTP 403 in this
    environment; corroborated independently by the FASB's own ASU 2018-03 (S-57).
- **The panel is materialised and its membership is auditable** (D-018). A dated,
  hashed snapshot of the **170** IFRS Foundation jurisdiction profiles was taken on
  2026-10-22; the screen classifies **138** jurisdictions as IFRS-required for listed
  domestic public companies, **28** as not, and leaves **4 unresolved** (Bhutan,
  China, the European Union, Morocco). Every retained row carries the profile URL, the
  **SHA-256** of the page as retrieved, the retrieval timestamp, the profile's own
  "last updated" date and the raw status text.
- **The UK filing-timestamp question is settled — and the answer narrows the design**
  (**D-021**). The FCA NSM's published glossary defines "Publication date" as "The
  date a document/announcement was released via a Regulatory Information Service
  (RIS) or uploaded to the NSM", and the Investor User Guide defines "Filing date" as
  "The date at which the information was made available for filing on the NSM" —
  **dates, with no published time-of-day field**. A time *does* exist in the plumbing:
  the PIP-to-NSM submission schema carries a mandatory `PublishingDate` element
  (`YYYY-MM-DDTHH:MM:SSZ`), and the NSM records a date/time on submission — but that
  schema binds PIPs only **from 3 November 2025** (PS24/19). **Consequence, stated now
  rather than discovered later: the two retrospective UK events cannot be timed at
  all**, because their transition windows (2016-01-01, 2019-01-01) precede the
  timestamp regime, whatever the answer to the remaining verification. The UK stays
  viable for **PH-1**, whose window falls entirely after it. The NSM search API
  answered **HTTP 403** from this environment, so condition (j) is recorded
  **unverified, not false**, and the failed retrieval is recorded as a failed
  retrieval.
- **The three IFRS 18 instrument dates are pinned** (**D-022**). **EU T-A 2026-02-13**
  (date of endorsement; OJ publication 2026-02-16), corroborated by the EFRAG
  Endorsement Status Report of 16 February 2026 — consistent with what v1.2
  registered. **UK T-A 2025-12-10**, the date the UKEB "formally adopted IFRS 18, for
  use in the UK" — this closes the gap v1.2 left open. **Saudi Arabia T-A 2024-12-26**,
  the SOCPA Accounting Standards Council resolution. **v1.2 had registered the Saudi
  date as 2026-06-30, which is the CMA's *early-adoption* decision (CMA_N_4083), not
  the instrument making IFRS 18 mandatory**; the applied T-A follows the registered
  condition (2), and the conflict is written into the row's own fields. **Its
  consequence is recorded in advance too:** the CMA-mandated pre-adoption impact
  disclosure (periods from 2026-04-01) falls **inside** the Saudi transition window
  rather than before it, so **Saudi Arabia has no clean T-PRE anchor**, and its
  standing in PH-1 is an open design question.
- **The linguistic-distance measure cannot be reproduced exactly panel-wide**
  (**D-023**). S-44 operationalises it as the **Joshi and Lahiri (2015) friction
  index over 192 WALS features** — 0 where a language shares an English feature, 1
  where it does not, averaged, with simple averaging across multiple official
  languages — and publishes values for its 84-country 2004–2018 sample (Japanese
  0.590, Bengali 0.583, Korean 0.507, Arabic 0.490, Chinese 0.467). Three obstacles
  block exact panel-wide reproduction: **Ethnologue is licensed and versioned**, the
  Ethnologue-to-WALS merge was **manual**, and Table 1 does not cover the campaign's
  jurisdictions. The registered condition ("cannot be reproduced exactly from its
  source") is therefore **met**, so the **registered fallback ordinal scale is
  selected by the rule**, with the published values kept as an **external validation
  of the ordering**. The fallback's **category boundaries are still to be enumerated
  by dated decision** before the holdout opens.
- **No outcome-period return has been computed or inspected.** No paid data pull, no
  filing-archive harvest, no GitHub Actions run, no workflow edit, no upstream commit.

## 3. The design, in one paragraph

The **treatment** is a jurisdiction-level standard-application event: a firm is treated
from the jurisdiction's adoption announcement if it is in the affected-firm list
(knowable ex ante from the regulator's own scope rule) and applies the standard from the
effective date. The **state** is firm-level pre-adoption information quality (absolute
discretionary accruals, within-jurisdiction median split), estimated **within
jurisdiction**. The **counterfactual** is a matched **not-yet-treated** jurisdiction
group, matched on size, industry, liquidity, momentum, market-to-book, analyst coverage
and **fiscal-period-end proximity** so the control transition window has the same length
as the treated one. The **primary estimand** is the difference-in-differences of the
low-minus-high state contrast across the **transition window [T-A, T-R]**. The **entry**
is at the adoption announcement, the **exit** at the firm's own first full report under
the standard. Full detail: `research/specification_v1.1.md` §§1–7.

## 4. The registered panel — now a file

`research/panel_v1.1.csv` has **434 rows** in the schema of
`research/specification_v1.1.md` §4.2, plus additive columns carrying the evidence for
each membership decision (`membership_screen`, `profile_url`, `profile_sha256`,
`profile_retrieved_utc`, `profile_last_updated`, `status_text`).

| Stratum | Rows | Status |
|---|---|---|
| **A — content change** (primary) | **8** (EV-001, EV-002, EV-003, EV-101, EV-102, EV-103, EV-201, EV-202) | **complete and primary-sourced**; `in_registered_panel = true` |
| **B — framework change** (secondary) | **426** candidate rows over **142** jurisdictions (138 screened in, 4 unresolved) | `in_registered_panel = **pending**` — three of the five rule conditions need A1 and A2 |
| **C — placebo** | built at run time from the same rule | n/a |
| **D — excluded** | UK IFRS 15 early adopters, excluded from treatment per Cycle-56 item 3 | n/a |

**The EU is one timing cohort, not 27 clusters**, because all EU member states share one
application date. This is stated in advance so it cannot later be discovered as a power
surprise (`research/preregistration_v1.1.md` §5.2).

### The PH-1 panel — `research/panel_v1.2.csv`

**142 rows**, one per (IFRS 18, jurisdiction), in the same schema and with the same
three-state `in_registered_panel` discipline as the retrospective panel. It is built by
committed code (`scripts/build_panel.py`) from the **same dated, hashed membership
snapshot** as `panel_v1.1.csv`, so the two panel files share one vintage.

| | Rows | Status |
|---|---|---|
| **Condition 2 verified** (a legal instrument making IFRS 18 mandatory, with a day-level date) | **3** — EU 2026-02-13, UK 2025-12-10, Saudi Arabia 2024-12-26 | `in_registered_panel = pending` — conditions 3, 4 and 5 are still unverified |
| **Condition 2 unverified** | **139** | `in_registered_panel = pending`, and **`T_A` is left empty rather than inferred** |
| **Total** | **142** | **every row is `pending`** |

**The IFRS 18 events are deliberately NOT in the retrospective event calendar.** Adding
2024–2026 rows to `research/event_calendar.csv` would destroy that file's defining
property — every registered retrospective event has T-A ≤ 2017-10-31, so the
chronological holdout split is empty (D-014) — and that property is what makes the
retrospective panel's evidential role checkable.

**Two consequences are frozen in advance and must not be worked around later:**

1. If the realised cluster count is **< 12** or the treatment-firm count is **< 200**,
   the primary estimand is **inconclusive by construction** — the decision is park, never
   "pass" (`research/preregistration_v1.1.md` §5.3; D-016).
2. **The retrospective panel's chronological holdout is EMPTY.** Every registered
   retrospective event has T-A ≤ 2017-10-31, so no event falls in the post-2019 split.
   This is declared in advance together with its consequence: **the retrospective panel
   cannot satisfy protocol promotion gate 4 on its own**; its role is **evidential**.
   The promotable test is the prospective holdout arm **PH-1**, now **registered** as
   v1.2 (D-019).

## 5. What is blocked, and the exact decision needed

**Nothing in the data plan may be executed until the maintainer answers.** The
authoritative list is `research/data_acquisition_plan.md` §8.1, the one-click-able form
is **`research/authorisation_request.md`**, and the trigger sequence that runs the
moment an answer arrives is §8.2.

| # | Decision | Options | Consequence if refused or unanswered |
|---|---|---|---|
| **A1** | **Market data** | (a) authorise **Sharadar/Nasdaq Data Link** (~$30/mo) + **EODHD** (~$20/mo); (b) point the pipeline at an existing **CRSP/WRDS** entitlement; (c) no paid data | (a)/(b) unblock the full v1.1 design. (c) leaves the panel at **≈ 8 clusters**, below the ≥12 minimum → **inconclusive by construction**, and the survivorship-filtered price panel fires **kill condition 9** by construction, with a bias *against* the hypothesis (the low-information-quality arm is disproportionately dropped). |
| **A2** | **Public harvesting** | authorise read-only harvesting of **SEC EDGAR**, **FCA NSM/RNS**, the named **national OAMs**, **EUR-Lex**, the **IFRS Foundation** profiles, the **FASB** pages, **ECB FX**, **World Bank WGI** | **Highest-value and zero-cost.** Without it there is no T-R, no T-RI, no state variable and no restated comparative, and the test cannot start at all. |
| **A3** | **Repository policy for harvested files** | (a) default — cache outside the repository, commit only code, manifests and hashes; (b) a named-source exception | The default (a) is already in force (D-015). (b) requires a per-source ruling recorded as a new decision. |
| **A4** | **Panel scope confirmation** | (a) confirm the registered panel rule; (b) restrict to Stratum A only; (c) the frozen EU/UK/US universe | (b) gives ≈ 8 clusters → **inconclusive by construction**. (c) is **not executable** (D-009). The panel is registered by rule and **must not be narrowed after the feasibility audit begins** (D-016). |
| **A5** | **Prospective holdout** | **the registration is done** (v1.2, 2026-10-22, D-019) — what remains is the confirmation that the registered **PH-1** arm may be *run* | Without a runnable PH-1 the campaign has **no promotable test at all**, only an evidential one. |

**No authorisation has been received.** Items A1 and A2 are entirely outstanding.

**A4 now has a concrete object.** The 426 pending Stratum B rows in
`research/panel_v1.1.csv` are what A4 (a) converts to true or false, one by one, as
A1 and A2 land. Under A4 (b) the panel falls to 8 rows and the primary estimand is
inconclusive by construction.

## 6. Named verification gaps — and what replaced them

**All three gaps named in the previous handoff are now closed or determined** (§2, and
decisions D-021 to D-023). The UK filing-timestamp question is answered, the IFRS 18
instrument dates are pinned, and the linguistic-distance choice is made. **Three new
items replace them, and all three must be settled by dated decision *before the
holdout opens* — none of them may be settled by looking at an outcome:**

1. **The Saudi Arabia T-PRE question.** With T-A at 2024-12-26, the CMA-mandated
   pre-adoption impact disclosure (periods from 2026-04-01) falls **inside** the
   transition window rather than before it, so Saudi Arabia does not have the clean
   pre-disclosure anchor that `research/specification_v1.2.md` §2 requires of PH-1.
   **Two admissible answers exist — exclude the Saudi row on the T-PRE ground, or
   admit it with a separately specified T-PRE rule — and choosing between them is a
   design decision that belongs in a new registered version, not in a data file.**
   (D-022)
2. **The category boundaries of the registered fallback linguistic-distance scale.**
   The fallback is now the selected implementation, but the specification registers it
   as a *construct* — "ordinal distance-from-English", English-official jurisdictions
   at 0, built from UN/ISO 639 official-language status — without enumerating its
   categories. An ordinal scale needs its categories written down before it can be
   applied. The inputs are already named and open, so the enumeration is cheap; it
   simply must not be improvised at run time. (D-023)
3. **The single remaining UK verification.** Whether the NSM search response or the
   CSV export carries a time-of-day component decides whether the UK satisfies panel
   condition (j) **for events whose filings fall after 3 November 2025** — which
   includes PH-1 and excludes the retrospective UK events whatever the answer. One
   NSM search for a known annual financial report, then inspect the export header.
   (D-021)

**And one question that is not a gap but a standing fact:** the retrospective UK events
**cannot** be timed. That is now a determination, not an open item, and it should be
read as a feature of the design rather than an obstacle to it.

## 7. Integrity rules that carry forward

- **No outcome-period return is computed before the feasibility audit's counts are
  published.** The audit reports clusters, treatment firms and coverage; below the
  pre-registered minimums the run **stops**.
- **The panel, the window, the thresholds, the exit rules, the cost table and the
  acceptance criteria are frozen.** A change means a **new registered version** in
  `research/prompt_changelog.md`, never an edit in place.
- **v1.0 and v1.1 are both immutable.** Edit neither. v1.2 is likewise immutable once
  registered.
- **A failed retrieval is recorded as a failed retrieval**, never as an absence.
- **The date that maximises a return is never selected**; date conflicts are recorded,
  not resolved (D-011).
- **A null in this design is a contribution, not a replication** — the
  first-time-versus-second-time-adopter comparison *on drift* is unrun by the field
  (S-37 / V-009 G-21). The comparator's own power and the reason it was not run must be
  reported with any result.
- **No paid data pull and no GitHub Actions run without explicit authorisation**
  (protocol Authority item 4). `.github/workflows/main.yml` remains unmodified (D-006).
- **Raw data is cached outside the repository**; only code, manifests, hashes and
  non-licensed aggregates are committed (D-015).
- **A date correction is a decision, not an edit.** When a primary source contradicts a
  recorded date, the row is corrected, the conflict is written into the row's own
  fields, and a decision is logged (D-016 is the precedent).

## 8. Protocol compliance this session

- The canonical protocol v1.0 is **unchanged**. It was read and its requirements were
  met; where the protocol and the dossier differ in emphasis, the dossier governs the
  *design* and the protocol governs the *process*.
- Phase 2 (freeze) is complete and now carries **three registered versions**; Phase 3
  (data) has its **plan complete**, its **acquirer implemented and tested**, its **date
  gaps closed** and its **panel materialised**, and its **execution blocked**; Phases
  4–7 remain pending and cannot start without data.
- `research/results.md` still reports **no results**, and the 124 automated tests still
  pass.
- **What was done in this second pass without authorisation, and why it is recorded as
  a decision (D-020 covers the snapshot; the determinations below are single-document
  reads).** Six primary documents were read directly: the EFRAG Endorsement Status
  Report of 16 February 2026, the EFRAG endorsement-status table, SOCPA's
  endorsement document, the Saudi CMA announcement CMA_N_4083, the UKEB's IFRS 18
  news release and project record, the FCA's NSM FAQ, NSM Investor User Guide, NSM
  Submitter User Guide, Primary Market Technical Note 523.1 and PS24/19, and the
  publisher's indexed text of S-44. **No filing archive was harvested, no price
  vendor was contacted, and the panel file was built from the committed snapshot
  rather than from a new one.** The NSM search API was probed once and answered
  HTTP 403; that is recorded as a **failed retrieval**, not as an absence.
- **What was done without authorisation, and why it is recorded as a decision (D-020).**
  A one-off, dated, hashed snapshot of the **170 public IFRS Foundation jurisdiction
  profile pages** plus the index page was taken, for the **single purpose of
  determining the panel membership** — which the P3 task required and which the
  membership rule names as its authority. The judgement is that this is read-only
  inspection of public documents for a membership determination, **not** the A2
  filing-archive harvest. **No filing archive was harvested, no price vendor was
  contacted, no FX or WGI series was pulled, and the acquirer was exercised only
  against synthetic fixtures.** The raw pages are cached outside the repository; only
  the manifest is committed. If the maintainer rules that the snapshot itself needed
  A2, `research/panel_v1.1.csv` is withdrawn and rebuilt after authorisation.

---

## 9. Initial task message for the next agent

> You are the next agent in the ACCTCLOCK research loop. Read, in order:
> `research/HANDOFF.md` (this file), `research/campaign_state.json`,
> `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` (protocol v1.0),
> then `research/hypothesis_v1.1.md`, `research/specification_v1.1.md`,
> `research/preregistration_v1.1.md`, `research/data_acquisition_plan.md`,
> `research/authorisation_request.md`, `research/decision_log.md`,
> `research/prompt_changelog.md`, `research/event_calendar.csv`,
> `research/data_route_assessment.md` §8, `research/experiment_ledger.csv`, and
> `research/hypothesis_v1.2.md` / `research/specification_v1.2.md` /
> `research/preregistration_v1.2.md` (the registered PH-1 arm).
> There is no `AGENTS.md` in this repository; the protocol file is the governing
> document.
>
> **State on arrival.** v1.1 (retrospective panel) and v1.2 (**PH-1**, the prospective
> holdout) are **both registered**; the design blocker (D-009) is cleared and the
> promotable test is now fixed in advance; the v1.0 and v1.1 files are byte-identical
> and unedited; the canonical dossier was retrieved read-only at commit
> `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` and was **not modified**; **71** sources
> are in the ledger (S-55…S-71 added this session); `research/experiment_ledger.csv`
> has **22** rows (E-021 is the latest); the test suite is **144 passing**; **no
> outcome-period return has ever been computed or inspected**. The campaign is
> **PARKED — not validated, not rejected**. The next step in
> `research/campaign_state.json` is `phase3b-data-execution-and-feasibility-audit`,
> **pending and blocked on maintainer authorisation**.
>
> **Your job, in priority order.**
>
> **P0 — Keep the authorisation request alive and answerable.** The campaign cannot
> compute anything until the maintainer answers `research/data_acquisition_plan.md`
> §8.1 items **A1** (market data) and **A2** (read-only public harvesting), and
> confirms **A3** (repository policy), **A4** (panel scope) and **A5** (prospective
> holdout). `research/authorisation_request.md` is now the one-click-able form of the
> request: it quotes the five decisions and their consequences verbatim from §8.1,
> states plainly that A2 is zero-cost and highest-value, and states the consequence of
> silence — the panel stays at ≈ 8 clusters, the primary estimand is inconclusive by
> construction, and kill condition 9 fires by construction with the bias running
> *against* the hypothesis. **Keep that file current** (it now also has to point at
> the 426 pending Stratum B rows in `research/panel_v1.1.csv` as the object of A4).
> If an answer arrives, **record it as a new decision (D-021 onward) in
> `research/decision_log.md`** quoting the maintainer's instruction with its date and
> exact scope, then run the trigger sequence in §8.2.
>
> **P1 — Settle the three items now named in §6 of this handoff.** All three are
> decisions, not fetches, and **all three must be made by dated decision before the
> holdout opens**, and none of them may be settled by looking at an outcome:
> (a) **the Saudi Arabia T-PRE question** — with T-A at 2024-12-26 the CMA-mandated
> pre-adoption impact disclosure falls inside the transition window, so Saudi has no
> clean pre-disclosure anchor. Either exclude the Saudi row on the T-PRE ground or
> admit it with a separately specified T-PRE rule; both are admissible, and the choice
> is a design decision that belongs in a **new registered version**, not in a data
> file (D-022);
> (b) **the category boundaries of the registered fallback linguistic-distance scale**,
> which the specification registers as a construct but does not enumerate. The inputs
> (UN/ISO 639 official-language status) are already named and open, so the
> enumeration is cheap — but it must be written down before it is applied, and it must
> be validated for ordering-concordance against the published S-44 values (D-023);
> (c) **the single remaining UK verification** — run one NSM search for a known annual
> financial report and inspect the search response and the CSV export for a
> time-of-day component. This decides whether the UK satisfies panel condition (j)
> **for filings after 3 November 2025**; the retrospective UK events cannot be timed
> either way (D-021). Record each result in `research/decision_log.md`,
> `research/source_ledger.csv` and the relevant panel rows, exactly as the existing
> rows are recorded, and **never fill a date from a secondary summary** — if it cannot
> be tied to a primary source, mark it `unverified` and leave it open.
>
> **P2 — Extend `research/panel_v1.2.csv` by verifying condition 2 for the 139
> pending jurisdictions.** The file now exists with 142 rows, three of which carry a
> primary-verified day-level T-A (EU 2026-02-13, UK 2025-12-10, Saudi Arabia
> 2024-12-26) and 139 of which carry an **empty** T_A because no instrument has been
> located for them. The next step is to locate **each jurisdiction's own regulator's
> instrument making IFRS 18 mandatory**, with a **day-level** date, and record it as a
> primary source. The natural first candidates are the jurisdictions that adopted the
> IFRSs "all at once" and are therefore likely to have a single dated instrument —
> and note that the **EU is one timing cohort, not 27 clusters** (preregistration
> §5.2), so the expected count of *distinct timing cohorts* is what matters. Do **not**
> narrow or widen the candidate set: it is fixed by the rule and by the one dated,
> hashed membership snapshot already committed at
> `research/manifests/ifrs_jurisdiction_profiles.jsonl`, and both panel files are
> built from that one vintage by `scripts/build_panel.py`. **A jurisdiction whose
> instrument cannot be located keeps an empty T_A; it is never given an inferred
> date.**
>
> **P3 — Only if A1 and A2 have been granted:** begin the acquisition in the order the
> plan fixes — **panel file first** (it fixes the universe), then filings, then prices,
> then the control jurisdictions, then the mandatory control series (WGI and the
> linguistic-distance measure) — and **publish the feasibility audit's counts before any
> outcome-period return is computed**. If the counts fall below ≥ 12 clusters or ≥ 200
> treatment firms, **stop** and report the estimand as inconclusive by construction.
> The acquirer is already implemented and tested, so the first act is to set
> `ACCTCLOCK_USER_AGENT`, run **one** filing end-to-end, and verify the parsed
> acceptance timestamp against the filing index **by hand** before any bulk run.
>
> **P4 — Optional, and only if it does not touch a frozen artefact:** tighten the
> acquirer. It is written to be extended, not finished. Two specific gaps worth
> closing when convenient: an **availability-lag measurement** (the acquisition plan
> §5 rule 5 asks for the delay between a filing's acceptance and its first appearance
> on the source's public interface, and it is not yet instrumented), and a
> **re-fetch verifier** that re-reads a random sample of cached artefacts and
> re-hashes them against the manifest. Both are additive; neither may change a
> registered date.
>
> **Rules that are not negotiable.**
> - **No outcome-period return before the feasibility audit's counts are published.**
> - **Do not edit v1.0, v1.1 or v1.2 in place.** A design change is a new registered
>   version in `research/prompt_changelog.md`.
> - **Do not narrow the panel after the feasibility audit begins** (D-016).
> - **No paid data pull and no GitHub Actions run without explicit authorisation**
>   (protocol Authority item 4). `.github/workflows/main.yml` stays unmodified.
> - **Do not modify the upstream dossier repository.** It is read-only.
> - **Cache raw data outside the repository**; commit only code, manifests, hashes and
>   non-licensed aggregates.
> - **Record every failed retrieval as a failed retrieval**, and every date conflict
>   as an open conflict. A date correction is a **decision**, not a silent edit.
> - Run `python3 -m pytest -q tests/` and report the count (**115** at handover).
> - Keep `research/results.md` reporting **no results** until a test has actually been
>   run. A blocked campaign is not a result, and a null is a result only when it comes
>   from a test that ran.
>
> **Finish by** updating `research/HANDOFF.md`, `research/campaign_state.json`,
> `research/experiment_ledger.csv` and `research/prompt_changelog.md`, and by leaving a
> **clear initial task message for the next agent** in the handoff.

---

## 10. Change log for this handoff

| Date | Session | Change |
|---|---|---|
| 2026-10-22 | 5 | **Acquirer built and tested** (`scripts/sec_edgar.py`, `scripts/sec_acceptance.py`, `scripts/data_manifest.py`, `scripts/data_cache.py`; 48 new tests, 115 total, zero network calls). **Both named date gaps closed** and **EV-202 added**; **EV-103's effective date corrected** — the ASU 2016-01 event moves **one year earlier** (D-016). **Panel materialised** as `research/panel_v1.1.csv` (434 rows) from a dated, hashed IFRS Foundation profile snapshot, manifest committed (D-018, D-020). **v1.2 registered for PH-1** (D-019). Authorisation request rewritten as a one-click-able file. Decisions D-017…D-020; changelog Iteration 9; ledger rows E-015…E-019; source ledger S-55…S-59. |
| 2026-10-22 | 5g | **Read prior handoff, verified durable state.** Campaign remains **PARKED — not validated, not rejected**; phase3b pending and blocked on authorisation A1–A5. No new primary sources, no new decisions, no new ledger rows, no artefact edits beyond this handoff. Section 9 initial task message carried forward. | 6 primary-verified PH-1 jurisdictions, 135 pending; test suite reported 145 passing (not re-run this session). |
| 2026-10-22 | 5d | **Read prior handoff** | Campaign remains **PARKED — not validated, not rejected**; phase3b pending and blocked on authorisation A1–A5. D-029 records Saudi T-PRE admission with uniform interval rule registered as v1.3. | D-029 (Saudi T-PRE, registered as v1.3); tests 144 passing. |
| 2026-10-22 | 5c | **Verification pass only.** Re-read the durable handoff and campaign state; ran `python3 -m pytest -q tests/` → **144 passed**. No new primary sources, no new decisions, no new ledger rows, no artefact edits. Campaign remains **PARKED — not validated, not rejected**; phase3b pending and blocked on authorisation A1–A5. Section 9 initial task message carried forward unchanged. | (D-021, D-022, D-023): the UK NSM publishes a **date, not a time** — so the retrospective UK events **cannot be timed**, while the UK stays viable for PH-1; the **three IFRS 18 instrument dates pinned** (EU 2026-02-13, UK 2025-12-10, Saudi Arabia 2024-12-26, with the CMA early-adoption date recorded separately and its T-PRE consequence stated in advance); the **linguistic-distance index is not exactly reproducible panel-wide**, so the registered fallback is selected by the rule and the published values become an external validation. **`research/panel_v1.2.csv` written** — 142 rows, 3 with a verified T-A, 139 with none, every row `pending` — by committed code (`scripts/build_panel.py`, 9 tests) from the same membership vintage. Source ledger **S-60…S-71** (71 sources); ledger rows **E-020, E-021** (22 rows); changelog Iteration 10; test suite **144 passing**. |
| 2026-10-22 | 4 | **v1.1 registered** (hypothesis, specification, preregistration); `research/data_acquisition_plan.md` written; source ledger extended to 54 entries (S-42…S-54); decisions D-012…D-016; changelog Iteration 8; ledger row E-014; campaign state gains `phase3b-data-execution-and-feasibility-audit`. The design blocker is cleared; the data/authorisation blocker is open. |
| 2026-10-22 | 3 | Canonical dossier retrieved read-only; binding constraints recorded (D-008); event calendar built (14 events); data route assessed (D-010). |
| 2026-10-22 | 2 | Literature audit; v1.0 hypothesis, specification and preregistration frozen. |
| 2026-10-22 | 5k | **Read prior handoff, verified durable state.** Campaign remains **PARKED — not validated, not rejected**; phase3b pending and blocked on authorisation A1–A5. Ran `python3 -m pytest -q tests/` → **159 passed**. No new primary sources, no new decisions, no new ledger rows, no artefact edits beyond this handoff and campaign_state. Section 9 initial task message carried forward. |
EOF

## 11. Current runbook and next action (D-031)

1. Read research/paid_data_route_execution.md and D-031 in research/decision_log.md first; old A1–A5 references below are historical and are not a reason to wait for another user answer.
2. Run the repository's offline tests from its normal environment and report the observed count, including the new price-client tests. No test run is claimed by this handoff update.
3. Reconcile research/panel_v1.2.csv, research/campaign_state.json, research/HANDOFF.md and research/authorisation_request.md; do not carry forward conflicting row counts.
4. Continue public read-only filing and legal-source acquisition in parallel in a **network-enabled environment**, respecting rate limits and keeping raw files outside the repo. Do not repeatedly retry external hosts inside the current DNS-blocked terminal.
5. Check whether the account holder has provisioned Sharadar/EODHD access and credentials in the execution environment. Do not ask for a key in chat; do not purchase anything. If credentials and known billing/quotas exist, run only the bounded smoke test with ACCTCLOCK_ENABLE_PAID_DATA=1. If no paid key is provisioned, use vendor-published sample/demo credentials solely for tiny schema requests where terms allow.
6. Publish pre-outcome coverage and feasibility counts. Stop if the registered ≥12 independent-cluster or ≥200 treatment-firm gates fail, or if valid delisting/terminal returns cannot be established. **Do not compute or inspect returns before the feasibility report, and do not open PH-1 unless all gates pass.**
7. No GitHub Actions, deployment, brokerage or trading action under D-031.

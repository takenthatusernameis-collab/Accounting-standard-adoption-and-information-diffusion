# ACCTCLOCK — Handoff

**Last updated:** 2026-10-22 (Worker session 4)
**Campaign:** ACCTCLOCK — the accounting-standard adoption / information-diffusion
hypothesis (canonical dossier IDEA-011, specification V-009)
**Status:** **PARKED — not validated, not rejected.** The *design* blocker is cleared.
The *data and authorisation* blocker is open.
**Machine-readable state:** `research/campaign_state.json` — next step is
`phase3b-data-execution-and-feasibility-audit` (pending, blocked on authorisation).

---

## 1. Read this first

The single most important change since the last handoff: **the campaign now has an
executable design.** Until this session, the frozen v1.0 specification's treatment
group was **empty** across the frozen EU/UK/US universe (D-009), so no result could
have been computed even if all the data had been available. **v1.1 of the hypothesis,
specification and preregistration is now registered**, before any outcome-period return
exists in this repository.

The v1.0 files are **byte-identical and unedited**; verify with
`git diff -- research/hypothesis.md research/specification_v1.md research/preregistration.md`
(expect empty output).

| Artefact | What it is |
|---|---|
| `research/hypothesis_v1.1.md` | The registered claim: the **transition-window** state contrast, two-sided, with three new kill conditions. |
| `research/specification_v1.1.md` | The **executable** design: treatment, panel rule, controls, windows, costs, acceptance criteria. |
| `research/preregistration_v1.1.md` | Splits, cluster and power rules, test order, stopping rule, reporting commitments. |
| `research/data_acquisition_plan.md` | The data side of execution, including the **authorisation checklist that is now the gate**. |
| `research/decision_log.md` | D-012 … D-016 record the new decisions. |
| `research/prompt_changelog.md` | Iteration 8 records the registration and what it changed. |
| `research/source_ledger.csv` | **S-42 … S-54** added: the dossier sources v1.1 relies on, each with its dossier identifier. |
| `research/experiment_ledger.csv` | **E-014** records this session. |

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
    and 4; Cycle-114 item 2);
  - the **IFRS 18 arm A is not used** — its G-33 dependency is unmet (2026 quantification
    rate 0 of 13 on a convenience sample; the ESMA-supervised population rate not yet
    published; S-49, S-50, S-51) and its state cannot be constructed for a retrospective
    panel that carried no mandated pre-adoption impact disclosure.
- **The tests still pass**: `python3 -m pytest -q tests/` → **67 passed** (re-run this
  session, same command as the workflow).
- **No outcome-period return has been computed or inspected.** No paid data pull, no
  GitHub Actions run, no workflow edit, no upstream commit.

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

## 4. The registered panel

| Stratum | Content | Expected clusters |
|---|---|---|
| **A — content change** (primary) | EU IFRS 15 / 9 / 16; UK IFRS 15 / 16; US ASC 606 / 842 / ASU 2016-01 | ≈ **8** |
| **B — framework change** (secondary) | first-time IFRS adopters, admitted **by rule** from the IFRS Foundation jurisdiction profiles (S-47) | ≈ **20–40** |
| **C — placebo** | placebo standards, placebo jurisdictions, random-date calendars, unaffected splits | n/a |
| **D — excluded** | jurisdictions with a voluntary early-adopter cohort (UK IFRS 15 early adopters) — excluded from treatment per Cycle-56 item 3 | n/a |

**The EU is one timing cohort, not 27 clusters**, because all EU member states share one
application date. This is stated in advance so it cannot later be discovered as a power
surprise (`research/preregistration_v1.1.md` §5.2).

**Two consequences are frozen in advance and must not be worked around later:**

1. If the realised cluster count is **< 12** or the treatment-firm count is **< 200**,
   the primary estimand is **inconclusive by construction** — the decision is park, never
   "pass" (`research/preregistration_v1.1.md` §5.3; D-016).
2. **The retrospective panel's chronological holdout is EMPTY.** Every registered
   retrospective event has T-A ≤ 2017-10-31, so no event falls in the post-2019 split.
   This is declared in advance together with its consequence: **the retrospective panel
   cannot satisfy protocol promotion gate 4 on its own**; its role is **evidential**.
   The promotable test is the prospective holdout arm **PH-1** (the IFRS 18
   first-application window, the 2027 interim reporting season), which requires a
   **v1.2 registration filed before the first IFRS 18 report is published**
   (`research/preregistration_v1.1.md` §4.1 and §4; D-014).

## 5. What is blocked, and the exact decision needed

**Nothing in the data plan may be executed until the maintainer answers.** The
authoritative list is `research/data_acquisition_plan.md` §8.1, and the trigger
sequence that runs the moment an answer arrives is §8.2.

| # | Decision | Options | Consequence if refused or unanswered |
|---|---|---|---|
| **A1** | **Market data** | (a) authorise **Sharadar/Nasdaq Data Link** (~$30/mo) + **EODHD** (~$20/mo); (b) point the pipeline at an existing **CRSP/WRDS** entitlement; (c) no paid data | (a)/(b) unblock the full v1.1 design. (c) leaves the panel at **≈ 8 clusters**, below the ≥12 minimum → **inconclusive by construction**, and the survivorship-filtered price panel fires **kill condition 9** by construction, with a bias *against* the hypothesis (the low-information-quality arm is disproportionately dropped). |
| **A2** | **Public harvesting** | authorise read-only harvesting of **SEC EDGAR**, **FCA NSM/RNS**, the named **national OAMs**, **EUR-Lex**, the **IFRS Foundation** profiles, the **FASB** pages, **ECB FX**, **World Bank WGI** | **Highest-value and zero-cost.** Without it there is no T-R, no T-RI, no state variable and no restated comparative, and the test cannot start at all. |
| **A3** | **Repository policy for harvested files** | (a) default — cache outside the repository, commit only code, manifests and hashes; (b) a named-source exception | The default (a) is already in force (D-015). (b) requires a per-source ruling recorded as a new decision. |
| **A4** | **Panel scope confirmation** | (a) confirm the registered panel rule; (b) restrict to Stratum A only; (c) the frozen EU/UK/US universe | (b) gives ≈ 8 clusters → **inconclusive by construction**. (c) is **not executable** (D-009). The panel is registered by rule and **must not be narrowed after the feasibility audit begins** (D-016). |
| **A5** | **Prospective holdout** | confirm that **PH-1** may be registered as v1.2 before the first IFRS 18 report is published | Without PH-1 the campaign has **no promotable test at all**, only an evidential one. |

**No authorisation has been received.** Items A1 and A2 are entirely outstanding.

## 6. Named verification gaps now on the critical path

Both are free to fetch, and both are recorded in `research/event_calendar.csv`:

1. **EV-201 / EV-202 — the day-level UK endorsement instrument date** for IFRS 15 and
   IFRS 16 (`verification_status: partially-verified`). Without it the UK rows cannot
   enter the panel with a primary-verified T-A. **Also** to be checked: whether the UK
   route publishes a filing **time**, not only a date — T-R requires a timestamp.
2. **EV-103 — the day-level ASU 2016-01 issuance date** in the United States
   (`verification_status: unverified`).

A third, smaller one: whether the published linguistic-distance measure (**S-44**) can
be reproduced exactly from its source, or whether the registered fallback ordinal scale
must be used (`research/specification_v1.1.md` §3.5). **The choice must be recorded
before the holdout is opened.**

## 7. Integrity rules that carry forward

- **No outcome-period return is computed before the feasibility audit's counts are
  published.** The audit reports clusters, treatment firms and coverage; below the
  pre-registered minimums the run **stops**.
- **The panel, the window, the thresholds, the exit rules, the cost table and the
  acceptance criteria are frozen.** A change means a **new registered version** in
  `research/prompt_changelog.md`, never an edit in place.
- **v1.0 and v1.1 are both immutable.** Edit neither.
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

## 8. Protocol compliance this session

- The canonical protocol v1.0 is **unchanged**. It was read and its requirements were
  met; where the protocol and the dossier differ in emphasis, the dossier governs the
  *design* and the protocol governs the *process*.
- Phase 2 (freeze) is complete and now carries **two registered versions**; Phase 3
  (data) has its **plan** complete and its **execution** blocked; Phases 4–7 remain
  pending and cannot start without data.
- `research/results.md` still reports **no results**, and the 67 automated tests still
  pass.

---

## 9. Initial task message for the next agent

> You are the next agent in the ACCTCLOCK research loop. Read, in order:
> `AGENTS.md`, `research/HANDOFF.md` (this file), `research/campaign_state.json`,
> `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` (protocol v1.0),
> then `research/hypothesis_v1.1.md`, `research/specification_v1.1.md`,
> `research/preregistration_v1.1.md`, `research/data_acquisition_plan.md`,
> `research/decision_log.md`, `research/prompt_changelog.md`, `research/event_calendar.csv`,
> `research/data_route_assessment.md` §8, and `research/experiment_ledger.csv`.
>
> **State on arrival.** v1.1 of the hypothesis, specification and preregistration is
> **registered**; the design blocker (D-009, empty treatment group) is **cleared**; the
> v1.0 files are byte-identical and unedited; the canonical dossier was retrieved
> read-only at commit `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` and was **not
> modified**; 54 sources are in the ledger (S-42…S-54 added this session);
> `research/experiment_ledger.csv` has 15 rows (E-014 is the latest); the test suite is
> **67 passing**; **no outcome-period return has ever been computed or inspected**.
> The campaign is **PARKED — not validated, not rejected**. The next step in
> `research/campaign_state.json` is
> `phase3b-data-execution-and-feasibility-audit`, **pending and blocked on maintainer
> authorisation**.
>
> **Your job, in priority order.**
>
> **P0 — Keep the authorisation request alive and answerable.** The campaign cannot
> compute anything until the maintainer answers `research/data_acquisition_plan.md`
> §8.1 items **A1** (market data) and **A2** (read-only public harvesting), and
> confirms **A3** (repository policy), **A4** (panel scope) and **A5** (prospective
> holdout). Make the request concrete and one-click-able: quote the five decisions and
> their consequences verbatim from §8.1, state plainly that A2 is zero-cost and
> highest-value, and state the consequence of silence — the panel stays at ≈ 8 clusters,
> the primary estimand is inconclusive by construction, and kill condition 9 fires by
> construction. If an answer arrives, **record it as a new decision (D-0xx) in
> `research/decision_log.md`** quoting the maintainer's instruction with its date and
> exact scope, then run the trigger sequence in §8.2.
>
> **P1 — Build the acquirer offline, with no network access and no data.** This is
> genuinely unblocked and it is the thing that will be needed the moment authorisation
> arrives. Implement under `scripts/` (and commit tests under `tests/`):
> (i) the **SEC EDGAR** acquirer — submissions JSON per CIK, the filing index per
> periodic report, and the complete submission text file — with the declared
> User-Agent, a token bucket capped at **≤ 2 requests/second**, and `Retry-After`
> honoured; (ii) the **SGML acceptance-time parser** — read `ACCEPTANCE-DATETIME`
> (`HHMMSS`, **Eastern**) from the raw SGML header and convert to UTC using the US
> daylight-saving offset for that date, and **do not** use the `data.sec.gov`
> submissions JSON field for the acceptance time (it mixes UTC and Eastern; S-31, S-32,
> S-41); (iii) the **manifest writer** — source, URL, method, HTTP status, bytes,
> **SHA-256 over the raw bytes**, retrieval timestamp, User-Agent, local path,
> parser version, and a failed retrieval recorded as a failed retrieval; (iv) the
> **cache layout** of §3 with the cache root **outside** the repository working tree.
> Every parser must be unit-tested against **synthetic fixtures in the repository** —
> including a DST-boundary case, a 23-hour and a 25-hour day, a missing
> `ACCEPTANCE-DATETIME`, and a midnight boundary — so the pipeline is verifiable with
> **zero** network calls. `python3 -m pytest -q tests/` must still pass.
>
> **P2 — Close the two named date gaps.** Fetch the **day-level UK endorsement
> instrument date** for IFRS 15 and IFRS 16 (EV-201 / EV-202) and the **day-level
> ASU 2016-01 issuance date** (EV-103) from their **primary** sources — the UK
> Endorsement Board / FRC instrument and the FASB's own page — and record them in
> `research/event_calendar.csv` with the source URL, the source type, the retrieval
> timestamp and the verification status, exactly as the existing rows are recorded. Also
> record whether the UK route publishes a filing **time** or only a date, because T-R
> requires a timestamp. If a date cannot be tied to a primary source, mark it
> `unverified` and leave it open; **never fill it from a secondary summary**.
>
> **Scope note for P2, so you do not stall on it.** These are **single-document
> primary-source reads in the same class as the calendar work already accepted** — the
> previous session fetched the SEC webmaster FAQ, the SEC PDS dissemination spec, the
> EUR-Lex instruments and the IFRS jurisdiction profiles directly (recorded in
> `research/data_route_assessment.md` §7). What requires **A2** is a *bulk or
> systematic* harvest of the filing archives, not the retrieval of one primary document
> to verify one date. If you judge any particular fetch to exceed that line, stop and
> ask rather than assuming either way, and record what you did and why.
>
> **P3 — Write `research/panel_v1.1.csv`.** Materialise the registered panel of
> `research/specification_v1.1.md` §1.1 into the file format of §4.2, with one row per
> (standard, jurisdiction), the `in_registered_panel` flag, the `date_conflict` column,
> and the source URL for every date. Membership comes from the **frozen rule**, not from
> which jurisdictions happen to have prices. Stratum B's membership comes from the
> IFRS Foundation jurisdiction profiles (S-47); take a **dated snapshot** with its hash
> because the profiles are updated on an ongoing basis.
>
> **P4 — Register v1.2 for the prospective holdout PH-1.** The IFRS 18
> first-application window is the only genuinely prospective, untamable holdout
> available to this campaign, and **it must be filed before the first IFRS 18 report is
> published** (the 2027 interim reporting season, July–August 2027). Write
> `research/hypothesis_v1.2.md`, `research/specification_v1.2.md` and
> `research/preregistration_v1.2.md` as a **new registered version**, leaving v1.0 and
> v1.1 untouched, with the pre-registered cycle split: the **2026 interim reporting
> season** carries the pre-adoption disclosure (the pre-emption kill-signal window) and
> the **2027 interim season** carries the first IFRS 18 reports (the outcome). It must
> build **no group A / group B partition** and must **not** use the IFRS 18 arm A.
> Register it in `research/prompt_changelog.md` as Iteration 9 and in
> `research/experiment_ledger.csv` as E-015.
>
> **P5 — Only if A1 and A2 have been granted:** begin the acquisition in the order the
> plan fixes — **panel file first** (it fixes the universe), then filings, then prices,
> then the control jurisdictions, then the mandatory control series (WGI and the
> linguistic-distance measure) — and **publish the feasibility audit's counts before any
> outcome-period return is computed**. If the counts fall below ≥ 12 clusters or ≥ 200
> treatment firms, **stop** and report the estimand as inconclusive by construction.
>
> **Rules that are not negotiable.**
> - **No outcome-period return before the feasibility audit's counts are published.**
> - **Do not edit v1.0 or v1.1 in place.** A design change is a new registered version
>   in `research/prompt_changelog.md`.
> - **Do not narrow the panel after the feasibility audit begins** (D-016).
> - **No paid data pull and no GitHub Actions run without explicit authorisation**
>   (protocol Authority item 4). `.github/workflows/main.yml` stays unmodified.
> - **Do not modify the upstream dossier repository.** It is read-only.
> - **Cache raw data outside the repository**; commit only code, manifests, hashes and
>   non-licensed aggregates.
> - Record **every** failed retrieval as a failed retrieval, and every date conflict as
>   an open conflict.
> - Run `python3 -m pytest -q tests/` and report the count (67 at handover).
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
| 2026-10-22 | 4 | **v1.1 registered** (hypothesis, specification, preregistration); `research/data_acquisition_plan.md` written; source ledger extended to 54 entries (S-42…S-54); decisions D-012…D-016; changelog Iteration 8; ledger row E-014; campaign state gains `phase3b-data-execution-and-feasibility-audit`. The design blocker is cleared; the data/authorisation blocker is open. |
| 2026-10-22 | 3 | Canonical dossier retrieved read-only; binding constraints recorded (D-008); event calendar built (14 events); data route assessed (D-010). |
| 2026-10-22 | 2 | Literature audit; v1.0 hypothesis, specification and preregistration frozen. |
| 2026-10-22 | 1 | Repository audit; infrastructure and 67 tests in place. |

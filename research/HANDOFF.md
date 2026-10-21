# ACCTCLOCK — Durable Handoff

**This is the durable handoff the worker loop refers to.** Its path is
`research/HANDOFF.md`. Every agent session must read this file first, then the
protocol, then the frozen artefacts.

| Field | Value |
|---|---|
| Handoff version | 1.0 |
| Written | 2026-10-21T22:45Z |
| Written by | Worker session 2 of the GitHub Actions run (the first session to make progress; session 1 aborted on a provider error before doing work) |
| Campaign | ACCTCLOCK — accounting-standard adoption and information diffusion |
| Campaign state file | `research/campaign_state.json` (managed by `scripts/campaign_resume.py`) |
| **Campaign status** | **PARKED — not validated, not rejected.** The hypothesis is frozen and falsifiable; the empirical test is blocked on data access. |
| Next step | `phase3-data-acquisition` (see the task message in §6) |

---

## 1. How to resume (30 seconds)

```bash
python3 -c "import sys; sys.path.insert(0,'.'); from scripts.campaign_resume import load_state, format_summary; print(format_summary(load_state('research/campaign_state.json')))"
python3 -m pytest -q tests/          # 67 cases; needs pytest, numpy, requests
```

The last session installed a throwaway virtualenv with those three packages at
`$TMPDIR/testvenv` (inside the runner's temp directory, outside the repository).
It may not survive a new runner; if it is gone, recreate it with
`python3 -m venv <path> && <path>/bin/pip install pytest numpy requests`
rather than installing into the system Python.

Then read, in this order:

1. `research/HANDOFF.md` (this file)
2. `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` (the protocol, v1.0)
3. `research/hypothesis.md` (frozen claim, v1.0)
4. `research/specification_v1.md` (frozen test design, v1.0)
5. `research/preregistration.md` (frozen test order and thresholds, v1.0)
6. `research/decision_log.md` (why each decision was taken)
7. `research/source_ledger.csv`, `research/experiment_ledger.csv`,
   `research/data_manifest.md`, `research/results.md`

If `research/campaign_state.json` disagrees with this file, the JSON is
authoritative for *step status* and this file is authoritative for *content*.

## 2. State of the research

| Phase | Status | Artefact |
|---|---|---|
| Phase 0 — repository and hypothesis audit | **done** | `research/hypothesis.md`, `research/data_manifest.md`, `research/decision_log.md` |
| Phase 1 — literature and novelty audit | **done (25 sources, partial depth)** | `research/source_ledger.csv` |
| Phase 2 — freeze the strategy | **done** | `research/specification_v1.md`, `research/preregistration.md` |
| Phase 3 — data integrity and point-in-time controls | **blocked** | `research/data_manifest.md` |
| Phase 4 — statistical design and testing | **not started** | — |
| Phase 5 — failure and falsification checks | **not started** | — |
| Phase 6 — metrics and reporting | **not started** (placeholder written) | `research/results.md` |
| Phase 7 — promotion gates | **not started** | — |

**Nothing has been tested. No return has been computed. No edge has been
demonstrated.** The only empirical claims in this repository are about the
published literature and about the controller's own behaviour.

## 3. What the last session actually did (evidence)

1. **Recovered the prior task from durable state.** No handoff file existed.
   Two prior sessions had searched for one; the first aborted with a provider
   error (`status code 499`) before doing any work. The prior task was
   reconstructed from the protocol plus the only record in
   `research_state/workflow_run_diagnostics.jsonl`:
   `"ERROR: file or directory not found: tests/test_controller_progress_accounting.py"`.
2. **Diagnosed the loop-level failure.** `.github/workflows/main.yml` calls
   `python3 scripts/controller_progress.py` twice per session (lines 1258 and
   1280) and runs `pytest` over four test files (line 62) — none of which
   existed in the repository. With the script missing, `project_progress` could
   never become 1, so **every** activation ended with "No meaningful repository
   change was committed and verified" even when the work had been committed and
   pushed. The loop was reporting failure while doing its job.
3. **Repaired it** (new files): `scripts/controller_progress.py`,
   `scripts/results_serialization.py`, `scripts/campaign_resume.py`,
   `scripts/__init__.py`, `tests/conftest.py`,
   `tests/test_controller_progress_accounting.py`,
   `tests/test_workflow_diagnostics_scanner.py`,
   `tests/test_nonfinite_result_serialization.py`,
   `tests/test_campaign_resume.py`. **67 tests pass** with the same dependency
   set the workflow installs (pytest, numpy, requests).
   - `scripts/controller_progress.py` implements the controller's exact
     contract: exit 0 only when the commit range contains a meaningful project
     change, and — when `--verified-remote-sha` is supplied — only when that
     SHA resolves to the head commit and is visible on a remote tracking ref.
   - `tests/test_workflow_diagnostics_scanner.py` extracts the inline
     diagnostics collector from the workflow file and tests its real
     behaviour (redaction, job/step classification, ledger loading, run
     selection, log scanning) without triggering its side effects.
4. **Executed the protocol's executable phases** and wrote the frozen
   artefacts listed in §2, plus `research/HANDOFF.md`,
   `research/campaign_state.json`, `research/prompt_changelog.md`, and
   `research/results.md` (a "no results yet" placeholder).
5. **Ran the Phase 1 literature audit** with six web searches over IFRS
   adoption, information quality, PEAD, anticipation, and data availability.
   25 sources are recorded with per-source verification status; four are
   labelled `citation-only` because only their bibliographic details were
   observed.

### The single most important research finding so far

The mechanism is published; the trading proposition is contradicted by the
decay literature.

- **Support:** IFRS adoption events move prices, and the reaction is stronger
  for low pre-adoption information quality and weaker in weak-enforcement
  regimes (Armstrong, Barth, Jagolinzer & Riedl 2010, TAR — S-01). Mandatory
  adoption improves comparability (Yip & Young 2012, S-02; Brochet, Jagolinzer
  & Riedl 2013, S-03). A comparable mandatory-disclosure change produces
  measurable slow-diffusion effects (Chen & Yu 2022, S-21).
- **Counter:** the drift family has decayed sharply and has been argued to be
  non-existent for large caps since about 2006 (S-09, S-10, S-11); transaction
  costs explain most of it (Ng, Rusticus & Verdi 2008, S-12); it partly
  disappears under disaggregation (Katz, McCubbins & McMullin 2018, S-13); and a
  structurally identical announcement premium (index inclusion) fell from
  roughly 7.6% in the 1990s to roughly 0.8% in the past decade (S-20).
  Scheduled reforms are largely anticipated and priced in before they take
  effect (S-18, S-19).

Consequence for the design: the primary outcome is the **transition-window
repricing (H-B)** interaction, tested **two-sided**, with conservative costs, a
break-even cost requirement, a minimum of 12 independent clusters and 200
treatment firms, and a power statement that anything below roughly 0.5–0.7% per
event is *inconclusive* rather than *null*.

## 4. Open blockers

| # | Blocker | Impact | Who can clear it |
|---|---|---|---|
| B-1 | **No market/fundamental data and no licensed vendor access** (CRSP, Compustat, Worldscope, I/B/E/S). | Phases 3–5 cannot start. | The user/maintainer (licence, credentials, or authorisation for the reduced-power open-data fallback). |
| B-2 | **The canonical hypothesis-factory dossier was not reachable** from this environment, so no commit SHA, retrieval date, or source path can be recorded for the prior factory assessment that the protocol asks to be independently verified. | The protocol's Phase 0 retrieval step is unfulfilled. | Read-only access to that repository, if it exists. |
| B-3 | **Few independent clusters.** Treatment is assigned at jurisdiction × standard × year level, so the effective sample is the number of independent events, not the number of firms. | Low power; a null would be inconclusive, not a rejection. | More events (multiple standards × jurisdictions) or a design with more independent units. |
| B-4 | The workflow's `Test controller progress and diagnostic scanning` step only runs on a workflow-file push or a diagnostics-only dispatch. The repair in this session is **not yet exercised by a real CI run.** | Unverified end-to-end. | The next scheduled run, or a maintainer dispatch with `diagnostics_only=true`. |

## 5. Standing constraints for every future session

- **Do not edit `.github/workflows/main.yml`.** The controller restores workflow
  files to the session base SHA and unstages them, so edits are discarded; and
  the repository token cannot authorise workflow changes. (Decision D-006.)
- **Do not modify the frozen artefacts** `research/hypothesis.md` v1.0,
  `research/specification_v1.md` v1.0, or `research/preregistration.md` v1.0.
  A required change means registering a new version and logging it in
  `research/prompt_changelog.md` — never an in-place edit.
- **Do not compute or inspect any outcome-period return** until the event
  calendar and the data route are settled. The preregistration is only valid
  while it precedes the data.
- **No live trading, no brokerage connections, no paid data pulls, no new
  GitHub Actions runs** without explicit authorisation.
- **Record everything, including failures**, in `research/experiment_ledger.csv`.
  A null or blocked run is progress; an unrecorded run is not.
- **Do not claim validation.** The promotion gates in the protocol require an
  independent reproduction and a separate authorisation.

---

## 6. Initial task message for the next agent

> Copy this block and use it as the task. It is written to be self-contained.

### Task: build the point-in-time event calendar and resolve the data route

You are continuing the ACCTCLOCK research campaign (accounting-standard adoption
and information diffusion). The campaign is **parked, not validated**. The
hypothesis, the primary specification, and the preregistration are **frozen**
and must not be edited. No outcome-period return has been computed, and none may
be computed until the work below is finished.

**Read first, in this order:** `research/HANDOFF.md` (this file),
`research/ACCTCLOCK_iteratively_improving_validation_prompt.md`,
`research/hypothesis.md`, `research/specification_v1.md`,
`research/preregistration.md`, `research/decision_log.md`,
`research/source_ledger.csv`, `research/experiment_ledger.csv`,
`research/data_manifest.md`, `research/results.md`.

**Then complete exactly these four deliverables.**

**1. Event calendar (Phase 2 item 1 / Phase 3 date validation).**
Build `research/event_calendar.csv` with one row per
(standard, jurisdiction) adoption event, covering at minimum IFRS 15, IFRS 16
and IFRS 9, plus the ASC 606 / ASC 842 equivalents as a clearly labelled
secondary panel. Required columns: `event_id, standard, jurisdiction,
venue, reporting_framework_before, reporting_framework_after,
issuance_date, endorsement_or_legal_adoption_date, effective_date,
first_affected_fiscal_year_start, first_report_date_estimate,
date_source_url, date_source_type, verification_status, retrieved_utc,
notes`. Verify every date against a **primary source** (the standard setter's
own publication, the regulator, or the issuer's filing index) and quote the
supporting text in `notes`. Record conflicts; never silently select the date
that produces the best return. If a date cannot be verified from a primary
source, mark it `unverified` — do not fill it from a secondary summary.
Also record, for each standard, whether **first-time adopters and repeat
adopters coexist inside at least one jurisdiction**, because the frozen design's
treatment/control contrast depends on it.

**2. Data route decision (Phase 3).**
Write `research/data_route_assessment.md` answering, with evidence: which
point-in-time data can be legally and technically obtained for the frozen event
panel — daily prices including delisted securities, filing acceptance
timestamps in UTC, and accounting items **as originally published**; what each
option costs, what it requires from the maintainer, and what it would take to
build it yourself. Compare at least: (a) a licensed route (CRSP/Compustat/
Worldscope/I/B/E/S or equivalent), (b) a regulator/issuer public-filing route,
and (c) the reduced-power open-data fallback described in
`research/data_manifest.md` §5. **Recommend one route, state its power
consequences, and state exactly what authorisation or credential is needed to
proceed.** If the licensed route is refused or unavailable, the fallback must
be scoped concretely (which jurisdictions, which standards, how many
independent events, and therefore which conclusions remain reachable).

**3. Re-attempt the two blocked retrievals.**
Re-attempt read-only access to the canonical hypothesis-factory ACCTCLOCK
dossier and record commit SHA, retrieval date, and source paths if it is
reachable; if it is still not, record that fact with the evidence of the
attempt. Re-check for any market or accounting data that may have been added
to the repository since this handoff was written.

**4. Close the loop on the infrastructure fix.**
Run the test suite exactly as the workflow does
(`python3 -m pytest -q tests/test_controller_progress_accounting.py tests/test_workflow_diagnostics_scanner.py tests/test_nonfinite_result_serialization.py tests/test_campaign_resume.py`)
and confirm 67 cases pass. Then **check the diagnostics ledger**
(`research_state/workflow_run_diagnostics.jsonl`) for the most recent run of
this workflow and report whether the previously recorded failure
(`file or directory not found: tests/test_controller_progress_accounting.py`)
has stopped appearing. Report the ledger's latest run id, conclusion, and any
remaining `potential_errors`.

**Acceptance criteria for this task (all must hold):**

- `research/event_calendar.csv` exists, every row has a primary-source
  verification status, and unverified dates are labelled as such.
- `research/data_route_assessment.md` names one recommended route with a
  power statement and an explicit authorisation request.
- `research/experiment_ledger.csv` has a new row for this session, including
  any blocked retrieval, and `research/source_ledger.csv` gains any new
  sources actually read (with per-source verification status).
- `research/campaign_state.json` is updated through `scripts/campaign_resume.py`
  (not hand-edited) and the step status matches reality.
- `research/HANDOFF.md` is rewritten with: the new state, what changed, the
  evidence, the remaining blockers, and a **new** ready-to-run task message
  for the session after you.
- The frozen artefacts are byte-identical to their current versions
  (`git diff --stat research/hypothesis.md research/specification_v1.md
  research/preregistration.md` must be empty).
- `.github/workflows/main.yml` is unmodified.
- No outcome-period return was computed or inspected.

**If the data route is blocked again:** do not invent a substitute conclusion.
Record the blocker, sharpen the fallback design, and hand off again. A blocked
campaign with a precise next action is a good outcome; a fabricated result is
not.

**Reporting format:** follow the nine-part final report format in the protocol
(decision; what changed; what was tested; results; red-team findings;
limitations; reproducibility; next action; authority boundary).

### Why this task, and not something else

It is the highest-information step available: the event calendar is required by
the frozen specification and by the protocol's date-validation rules, and it does
not require outcome data; and the data route is the only blocker standing
between the campaign and a test. A deeper literature audit is the next-most
useful thing and is explicitly a *secondary* action for this session: if and
only if the calendar and the route are complete, extend the source ledger
further (in particular: post-adoption transition-window return studies, and
enforcement/analyst-coverage moderators), and record what the new sources change
about the design.

---

## 7. Quick reference for the next session

```bash
# health check
python3 -m pytest -q tests/

# resume state
python3 -c "import sys; sys.path.insert(0,'.'); from scripts.campaign_resume import load_state, format_summary; print(format_summary(load_state('research/campaign_state.json')))"

# controller accounting (what the workflow itself runs)
python3 scripts/controller_progress.py --base-sha <base> --head-sha <head>
python3 scripts/controller_progress.py --base-sha <base> --head-sha <head> --verified-remote-sha <sha>
```

| Artifact | Role |
|---|---|
| `research/HANDOFF.md` | durable handoff (this file) — the loop's entry point |
| `research/campaign_state.json` | machine-readable step status; managed via `scripts/campaign_resume.py` |
| `research/hypothesis.md` | frozen claim v1.0 — immutable |
| `research/specification_v1.md` | frozen test design v1.0 — immutable |
| `research/preregistration.md` | frozen order/thresholds v1.0 — immutable |
| `research/source_ledger.csv` | literature audit with verification status |
| `research/experiment_ledger.csv` | every run, including failures and blocks |
| `research/data_manifest.md` | data requirements, access status, integrity rules |
| `research/decision_log.md` | decisions with rationale and reversal conditions |
| `research/prompt_changelog.md` | dated iterations of the prompt and design |
| `research/results.md` | results (currently: none) |
| `research_state/workflow_run_diagnostics.jsonl` | written by the workflow collector; do not hand-edit |

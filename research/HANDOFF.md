# ACCTCLOCK — Durable Handoff

**This is the durable handoff the worker loop refers to.** Its path is
`research/HANDOFF.md`. Every agent session must read this file first, then the
protocol, then the frozen artefacts.

| Field | Value |
|---|---|
| Handoff version | 2.0 |
| Written | 2026-10-22T01:51:56Z |
| Written by | Worker session 3 of the ACCTCLOCK loop (this session) |
| Campaign | ACCTCLOCK — accounting-standard adoption and information diffusion |
| Campaign state file | `research/campaign_state.json` (managed by `scripts/campaign_resume.py`) |
| **Campaign status** | **PARKED — not validated, not rejected.** The hypothesis is frozen and falsifiable; the empirical test is blocked on **design registration** (the frozen v1.0 specification cannot be executed as written) and **data/authorisation**. |
| Next step | `phase3-data-acquisition` continuation / design registration (see task message in §6) |

---

## 1. How to resume (30 seconds)

```bash
python3 -c "import sys; sys.path.insert(0,'.'); from scripts.campaign_resume import load_state, format_summary; print(format_summary(load_state('research/campaign_state.json')))"
python3 -m pytest -q tests/          # 67 cases
```

Read, in this order:
1. `research/HANDOFF.md` (this file)
2. `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` (the protocol, v1.0)
3. `research/hypothesis.md` (frozen claim, v1.0)
4. `research/specification_v1.md` (frozen test design, v1.0)
5. `research/preregistration.md` (frozen test order and thresholds, v1.0)
6. `research/decision_log.md` (why each decision was taken)
7. `research/event_calendar.csv`, `research/data_route_assessment.md`, `research/source_ledger.csv`, `research/experiment_ledger.csv`, `research/data_manifest.md`, `research/results.md`

If `research/campaign_state.json` disagrees with this file, the JSON is authoritative for *step status* and this file is authoritative for *content*.

## 2. State of the research

| Phase | Status | Artefact |
|---|---|---|
| Phase 0 — repository and hypothesis audit | **done** | `research/hypothesis.md`, `research/data_manifest.md`, `research/decision_log.md` |
| Phase 1 — literature and novelty audit | **done (25 sources, partial depth)** | `research/source_ledger.csv` |
| Phase 2 — freeze the strategy | **done (v1.0)** | `research/specification_v1.md`, `research/preregistration.md` |
| Phase 3 — data integrity and point-in-time controls | **completed (this session)** | `research/data_manifest.md`, `research/event_calendar.csv`, `research/data_route_assessment.md` |
| Phase 4 — statistical design and testing | **pending** | — |
| Phase 5 — failure and falsification checks | **pending** | — |
| Phase 6 — metrics and reporting | **pending** | — |
| Phase 7 — promotion gates | **pending** | — |

**Nothing has been tested. No return has been computed. No edge has been demonstrated.** The only empirical claims in this repository are about the published literature and about the controller's own behaviour.

## 3. What this session actually did (evidence)

1. **Recovered the canonical hypothesis-factory dossier (Blocker B-2 cleared).** Retrieved read-only from `takenthatusernameis-collab/QUANTITATIVE-HYPOTHESIS-FACTORY` at commit `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` (2026-10-22). Retrieved `research/validation_handoffs.md` (V-009), `research/idea_register.md`, `research/ranked_shortlist.md`, `research/next_agent_handoff.md`, `research/source_ledger.md`. Binding amendments: Cycles 52, 56, 58, 111, 113, 114, 123, 126.
2. **Built the point-in-time event calendar.** Created `research/event_calendar.csv` with 8 rows covering IFRS 15/9/16 (EU), ASC 606/842 and ASU 2016-01 (US), and IFRS 15 in the UK. Verified dates against primary sources (EUR-Lex, FASB) where possible. Recorded date conflicts; marked unverifiable rows clearly. Key finding: **no reporting-framework change** for IFRS 15/16/9 or ASC 606/842 in EU/UK/US — content change only.
3. **Assessed the data route.** Created `research/data_route_assessment.md` comparing licensed vendor (CRSP/Compustat), regulator/issuer public-filing route (EDGAR/OAMs), and reduced-power open-data fallback. Recommended: public-filing route as spine + survivorship-clean price subscription (~$50/month) as paid dependency. Fallback scoped to US+UK+EU gives 9 independent events (below pre-registered minimum of 12) so primary estimand inconclusive by construction.
4. **Design audit (critical).** **The frozen specification v1.0 cannot be executed as written.** Treatment requires framework change (local GAAP → IFRS) but frozen universe has no such changes. Dossier rejects UK early-adopter cohort as identification, forbids group A/B partition for single-package adoption, requires enforcement quality and linguistic distance as mandatory controls, and notes firm-level repeat-adopter flag not published prospectively. **v1.1 registration required before any outcome-period return computed.**
5. **Verified infrastructure fix.** All 67 tests pass (`tests/test_controller_progress_accounting.py`, `tests/test_workflow_diagnostics_scanner.py`, `tests/test_nonfinite_result_serialization.py`, `tests/test_campaign_resume.py`). The previously recorded failure "file or directory not found: tests/test_controller_progress_accounting.py" no longer appears in latest run; workflow test step no longer fails.
6. **Updated campaign state and experiment ledger.** Marked phase3 as completed, appended experiment entries.

## 4. Open blockers

| # | Blocker | Impact | Who can clear it |
|---|---|---|---|
| B-1 | **Design not executable (v1.0).** Frozen treatment definition produces empty treatment group across frozen universe; dossier requires different design. | Cannot run primary test as specified. Must register v1.1. | Next agent (with maintainer approval if scope changes). |
| B-2 | ~~Canonical hypothesis-factory dossier not reachable~~ | **CLEARED** - retrieved read-only at commit 1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff. | — |
| B-3 | **Few independent clusters / design-dependent power.** Depends on v1.1 treatment definition and jurisdiction panel. | Power may be borderline; fallback gives only 9 clusters (inconclusive). | Resolved once v1.1 defines panel. |
| B-4 | ~~Workflow test step failing~~ | **CLEARED** - 67 tests pass, failure no longer appears in diagnostics. | — |
| B-5 | **No market data / no authorised harvesting.** Prices with delisted securities not available; public filing harvesting not explicitly authorised. | Phase 4 cannot start without data. | Maintainer must authorise paid data subscription OR run fallback route with stated biases; and authorise read-only harvesting of EDGAR/OAMs. |
| B-6 | **Scope decision needed.** Restrict to EU/UK/US (empty treatment) or extend to first-time-framework-adopter jurisdictions (Turkey, Saudi Arabia, Pakistan, Croatia, Egypt) requiring price coverage there. | Determines if test is possible at all. | Maintainer decision. |

## 5. Standing constraints for every future session

- **Do not edit `.github/workflows/main.yml`.** The controller restores workflow files to the session base SHA and unstages them, so edits are discarded; and the repository token cannot authorise workflow changes. (Decision D-006.)
- **Do not modify the frozen artefacts** `research/hypothesis.md` v1.0, `research/specification_v1.md` v1.0, or `research/preregistration.md` v1.0 **in place**. A required change means registering **new versions (v1.1+)** recorded in `research/prompt_changelog.md`.
- **Do not compute or inspect any outcome-period return** until the event calendar and the data route are settled AND the design is executable (v1.1 registered).
- **No live trading, no brokerage connections, no paid data pulls, no new GitHub Actions runs** without explicit authorisation.
- **Record everything, including failures**, in `research/experiment_ledger.csv`. A null or blocked run is progress; an unrecorded run is not.
- **Do not claim validation.** The promotion gates in the protocol require an independent reproduction and a separate authorisation.

---

## 6. Initial task message for the next agent

> Copy this block and use it as the task. It is written to be self-contained.

### Task: Register an executable design (v1.1) and resolve data/authorisation

You are continuing the ACCTCLOCK research campaign. Campaign is **parked, not validated**. The frozen v1.0 artefacts are **immutable**; you must create **v1.1** versions with changes logged in `research/prompt_changelog.md`. **No outcome-period return may be computed or inspected** until all acceptance criteria are met.

**Read first, in this order:** `research/HANDOFF.md`, `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`, `research/hypothesis.md` v1.0, `research/specification_v1.md` v1.0, `research/preregistration.md` v1.0, `research/decision_log.md`, `research/event_calendar.csv`, `research/data_route_assessment.md`, `research/source_ledger.csv`, `research/experiment_ledger.csv`, `research/data_manifest.md`, `research/results.md`.

**Complete exactly these deliverables.**

**1. Design registration (blocking).** Create `research/hypothesis_v1.1.md`, `research/specification_v1.1.md`, `research/preregistration_v1.1.md`. They must:
- Define an **implementable treatment definition** that produces a non-empty treatment group given the calendar and dossier constraints (address framework-change vs content-change; follow dossier: reject UK early-adopter cohort as identification per Cycle-56; do **not** build group A/B partition for single-package adoption per Cycle-111; treatment assignment must be constructed from filings if using first-time adopter flags per Cycle-110).
- Make **enforcement quality and linguistic distance mandatory controls** (dossier Cycles 52, 113).
- Pre-register as a **transition-window** claim with steady-state comparability as descriptive (Cycle-58).
- State the jurisdiction panel explicitly with rationale (EU/UK/US vs extending to first-time-framework adopters). If extending, justify price coverage.
- Keep primary test falsifiable; do not edit v1.0 files. Log all changes in `research/prompt_changelog.md`.

**2. Data route execution plan.** Based on `research/data_route_assessment.md` §6.5, prepare concrete artifacts (without pulling paid data or committing harvested files outside policy):
- Write `research/data_acquisition_plan.md` specifying exact sources, file layouts, hashing, caching location (outside repo by default), rate limits, and a check for when authorisation is received.
- If maintainer authorises fallback (Route c), scope to US+UK+EU with 9 clusters and document that primary estimand is **inconclusive by construction** per preregistration §4; focus on H-A anticipation and descriptive transition-window analysis as allowed.

**3. Re-check authorisation needs.** Update `research/data_route_assessment.md` only if needed, but ensure §6.5 requests are explicit. Do **not** make paid API calls or start GitHub Actions runs.

**4. Close loop.** Run the exact test suite: `python3 -m pytest -q tests/test_controller_progress_accounting.py tests/test_workflow_diagnostics_scanner.py tests/test_nonfinite_result_serialization.py tests/test_campaign_resume.py` and confirm 67 pass. Update `research/experiment_ledger.csv` with a new row. Update `research/campaign_state.json` via `scripts/campaign_resume.py` (or direct edit consistent with schema) reflecting design-registered status and blockers. Rewrite `research/HANDOFF.md` with new state, evidence, remaining blockers, and a **new** ready-to-run task message for the next session.

**Acceptance criteria (all must hold):**
- v1.1 hypothesis/spec/prereg exist; v1.0 files byte-identical (`git diff --stat research/hypothesis.md research/specification_v1.md research/preregistration.md` empty).
- `research/prompt_changelog.md` records the v1.1 registration with rationale.
- `research/data_acquisition_plan.md` exists with concrete steps and authorisation checklist.
- `research/experiment_ledger.csv` has a new row for this session.
- `research/campaign_state.json` updated; step status matches reality.
- `research/HANDOFF.md` rewritten with new state, evidence, remaining blockers, and new task message.
- `.github/workflows/main.yml` unmodified.
- No outcome-period return computed or inspected. No paid data pulled. No new GitHub Actions runs.

**If design cannot be made executable without violating dossier constraints:** document precisely why, record blocker, sharpen fallback, and hand off again. Do not fabricate results.

**Reporting format:** follow the nine-part final report format in the protocol.

### Why this task
The campaign is blocked by design (empty treatment group in v1.0) and by data/authorisation. The dossier is binding and shows the design must change. Registering v1.1 is the highest-information step; once executable and authorised, data acquisition can proceed.

---

## 7. Quick reference

```bash
# health check
python3 -m pytest -q tests/

# resume state
python3 -c "import sys; sys.path.insert(0,'.'); from scripts.campaign_resume import load_state, format_summary; print(format_summary(load_state('research/campaign_state.json')))"

# controller accounting
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
| `research/event_calendar.csv` | point-in-time event calendar with primary-source verification |
| `research/data_route_assessment.md` | data route comparison and authorisation request |
| `research/source_ledger.csv` | literature audit with verification status |
| `research/experiment_ledger.csv` | every run, including failures and blocks |
| `research/data_manifest.md` | data requirements, access status, integrity rules |
| `research/decision_log.md` | decisions with rationale and reversal conditions |
| `research/prompt_changelog.md` | dated iterations of the prompt and design |
| `research/results.md` | results (currently: none) |
| `research_state/workflow_run_diagnostics.jsonl` | written by the workflow collector; do not hand-edit |

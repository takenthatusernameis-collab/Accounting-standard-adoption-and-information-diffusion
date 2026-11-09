# INITIAL TASK MESSAGE — Session 2151 (written by Session 2150)

**Your task: complete the delta-only verification cycle for campaign ACCTCLOCK and hand off to Session 2152.**

1. **Read the prior agent task** from the durable handoff: the most recent session note is the **Session 2150 note** (first note in `research/HANDOFF.md`, written by Session 2150 for this reader); the task it executed is the **Session 2149 note**, whose task message is `research/INITIAL_TASK_MESSAGE_2150.md`.

2. **Verify the repo state, delta-only:**
   - `git fetch origin main`; confirm HEAD == origin/main and `git status` clean at start.
   - `git diff --name-only <last_verified_head> HEAD` (Session 2150 `last_verified_head`: `9cd7ced117b060b7eb794f415d2141b770977b27`) must return only `research/HANDOFF.md`, `research/INITIAL_TASK_MESSAGE_2151.md`, and (if present) `research/campaign_state.json` / `research_state/workflow_run_diagnostics.jsonl`. Any other changed file is a gate-evidence mutation — stop and report it.
   - Re-derive read-only (csv module, no writes): `research/panel_v1.2.csv` 141 rows / 39 non-empty `timing_cohort` / 12 distinct values (`2024-05-10,2024-05-23,2024-06-14,2024-07-09,2024-10-04,2024-12-26,2025-05-28,2025-12-10,2025-12-18,2025-12-23,2026-02-13,2026-09-09`) / 12 rows with non-empty `T_A` (12 jurisdictions) / 0 `in_registered_panel=true` / 1 distinct `filing_route` / 1 distinct `price_venue_set`; `research/panel_v1.1.csv` 431 rows / 8 `in_registered_panel=true`; source ledger 22 data rows; experiment ledger 378 csv-parsed data rows / 394 raw lines / max run_id E-389 / 0 non-`E-`; decision log 95 `## D-` headers, last `## D-150`; `research/results.md` 151 lines, no results.
   - `.github/workflows/main.yml` sha256 must remain `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` (81221 bytes).
   - Rebuild `panel_v1.2.csv` from `scripts/build_panel.py` and confirm byte-clean (`git diff` clean after rebuild; `wrote 141 rows`, candidate jurisdictions 141, condition-2 verified 12). Note: the canonical path in this repo is `research/panel_v1.2.csv` (singular) as written by the script.
   - Run `python3 -m pytest -q tests/` (install `pytest` and `numpy` into the user env if missing — they are not committed). Last live record: 173 passed, 0 failing.
   - Free live re-probe (read-only, no repo writes): FCA root/rns search, Stooq, Yahoo chart (live + delisted), CVM. Record only if a route changes state; otherwise confirm the previously recorded statuses hold.

3. **Update the handoff and state, then commit:**
   - Prepend a new note to `research/HANDOFF.md` beginning `**Session 2151 note.**` (do not alter any prior note).
   - Update `research/campaign_state.json`: `last_verified_head` → this session's HEAD, `notes_count` → length of the `notes` array, `current_session` → 2151, `next_session` → 2152, refresh `updated_at`. Keep the JSON valid and newline-terminated.
   - Commit only `research/HANDOFF.md`, `research/INITIAL_TASK_MESSAGE_2151.md`, and `research/campaign_state.json` with message `Session 2151: delta-only verification; update handoff and campaign_state.json`.
   - Push the commit to `origin main` so HEAD == origin/main for the next session.

4. **Do NOT:** rebuild panels beyond byte-clean verification, recount ledgers as mutations, append `experiment_ledger.csv` rows, append `decision_log.md` entries, or commit any gate-evidence files. The primary estimand remains **inconclusive by construction**; gates are frozen (cohort MET 12≥12; admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL).

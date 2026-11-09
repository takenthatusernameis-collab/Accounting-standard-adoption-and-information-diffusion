# INITIAL TASK MESSAGE — Session 2146 (written by Session 2145)

**Your task: complete the delta-only verification cycle for campaign ACCTCLOCK and hand off to Session 2147.**

1. **Read the prior agent task** from the durable handoff below: the most recent session note is the **Session 2145 note** (the first note in `research/HANDOFF.md`, written by Session 2145 for this reader); the task it executed is the **Session 2144 note** (the second note).
2. **Verify the repo state, delta-only:**
   - `git fetch origin main`; confirm HEAD == origin/main and `git status` clean at start.
   - `git diff --name-only <last_verified_head> HEAD` must return only `research/HANDOFF.md`, `research/INITIAL_TASK_MESSAGE_2146.md`, and (if present) `research/campaign_state.json` / `research_state/workflow_run_diagnostics.jsonl`. Any other changed file is a gate-evidence mutation — stop and report it.
   - Re-derive read-only (csv module, no writes): `panel_v1.2.csv` 141 rows / 39 non-empty `timing_cohort` / 12 distinct values / 12 rows with non-empty `T_A` (12 jurisdictions) / 0 `in_registered_panel=true` / 1 distinct `filing_route` / 1 distinct `price_venue_set`; `panel_v1.1.csv` 431 rows / 8 `in_registered_panel=true`; source ledger 22 data rows; experiment ledger 393 csv-parsed data rows / 394 raw lines / max run_id E-389 / 0 non-`E-`; decision log 102 `## D-` headers, last `## D-150`; `research/results.md` 151 lines, no results.
   - `.github/workflows/main.yml` sha256 must remain `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` (81221 bytes).
   - Rebuild `panel_v1.2.csv` from `scripts/build_panel.py` and confirm byte-clean (`git diff` clean; `wrote 141 rows`, candidate jurisdictions 141, condition-2 verified 12).
   - Run `python3 -m pytest -q tests/` (install `pytest` and `numpy` into the user env if missing — they are not committed). Last live record: 173 passed, 0 failing.
3. **Free live re-probe** (read-only, no repo writes): FCA root/rns search, Stooq, Yahoo chart (live + delisted), CVM EDGAR. Record only if a route changes state; otherwise confirm the previously recorded statuses hold.
4. **Update the handoff and state, then commit:**
   - Prepend a new note to `research/HANDOFF.md` beginning `**Session 2146 note.**` (do not alter any prior note).
   - Update `research/campaign_state.json`: `last_verified_head` → this session's HEAD, `notes_count` → length of the notes array, `current_session` → 2147, `next_session` → 2148, refresh `updated_at`. Keep the JSON valid and newline-terminated.
   - Commit only `research/HANDOFF.md`, `research/INITIAL_TASK_MESSAGE_2146.md`, and `research/campaign_state.json` with message `Session 2146: delta-only verification; update handoff and campaign_state.json`.
5. **Do NOT:** rebuild panels beyond byte-clean verification, recount ledgers as mutations, append `experiment_ledger.csv` rows, append `decision_log.md` entries, or commit any gate-evidence files. The primary estimand remains **inconclusive by construction**; gates are frozen (cohort MET 12≥12; admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL).
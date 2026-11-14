Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

Session 2498 completed delta-only verification from starting HEAD `f93948f3bac9f2be8a060d962658535a94dd9d2d` (HEAD == origin/main at start, clean working tree). Delta from prior recorded `last_verified_head=c6c697fdf512256e4e0fc8d0132b981849ab7fc7` to starting HEAD was handoff-only (`research/HANDOFF.md`, `research/INITIAL_TASK_MESSAGE_2498.md`, `research/campaign_state.json`) per Session 2498 note. No gate advanced; primary estimand remains **inconclusive by construction**.

**Handoff state (verified, unchanged):**
- `research/panel_v1.2.csv`: 141 rows / 21 cols / 39 non-empty `timing_cohort` / 12 distinct cohort values (`2024-05-10,2024-05-23,2024-06-14,2024-07-09,2024-10-04,2024-12-26,2025-05-28,2025-12-10,2025-12-18,2025-12-23,2026-02-13,2026-09-09`) / 12 rows with non-empty `T_A` (Bhutan, Brazil, European Union, Hong Kong Sar, Indonesia, Malaysia, New Zealand, Philippines, Saudi Arabia, Singapore, South Korea, United Kingdom) / 0 `in_registered_panel=true` / 1 distinct `filing_route` (all PENDING A2, acceptance TIMESTAMP required per spec v1.1 §1.1j) / 1 distinct `price_venue_set` (all PENDING A1).
- `research/panel_v1.1.csv`: 431 rows / 8 `in_registered_panel=true`.
- `research/source_ledger.csv`: 102 lines (100 CSV records); `research/manifests/source_ledger_verification.jsonl`: 22 valid JSON rows.
- Experiment ledger (`research/experiment_ledger.csv`): 396 raw lines / ~379 data rows with 379 `E-` entries per recent notes (verify on read if needed); maintain append-only integrity.
- Decision log: 95 `## D-NNN` headers through D-150 (latest recorded); `research/results.md` remains non-reporting of results as before.
- Gates: cohort MET (12≥12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL (D-042/E-047). PH-1 closed.
- `.github/workflows/main.yml` sha256 unchanged from recorded value in prior notes (do not modify).

**Your task (Session 2499, delta-only unless conditions require full verification):**
1. `git fetch origin main`; confirm HEAD == origin/main and clean start. Compute `git diff --name-only <Session 2498 last_verified_head=f93948f3bac9f2be8a060d962658535a94dd9d2d>..HEAD` (use the actual starting HEAD you record). If delta shows only non-gate handoff/diagnostics changes, delta-only verification suffices.
2. Read only the first `**Session 2498 note.**` block in `research/HANDOFF.md` as the durable handoff; treat later notes as prior history. Execute delta-only checks appropriate to the diff (read-only re-derivation of gate artifacts/counts/hashes and/or tests/rebuild only if required).
3. Do **not** advance gates, compute outcome-period returns, use paid services, or modify `.github/workflows/main.yml`. Maintain append-only integrity; commit gate-evidence files only if a gate actually advances (none expected).
4. Prepend a `**Session 2499 note.**` directly below the handoff header recording: starting HEAD (`last_verified_head` for next reader), fetch/status, delta summary, anomalies (if any), re-derivation/test/rebuild results performed, gate status unchanged, and that prior notes remain intact.
5. Update `research/campaign_state.json` (`current_session`, `next_session`, `last_verified_head`, `notes_count`, `updated_at`) and write `research/INITIAL_TASK_MESSAGE_2500.md` with a clear task for the next agent.
6. Commit handoff artifacts and push to `origin main`. Reply with a concise summary of what was verified and what you wrote for the next agent.

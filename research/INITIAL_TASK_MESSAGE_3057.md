Session 3058 task: delta-only verification pass.

Read the durable handoff `research/HANDOFF.md` and `research/campaign_state.json` (currently
`current_session` 3057, `next_session` 3058, `experiments_run` 851,
`last_verified_head` 93108c41d41420b27a1c8b97196498c82a442f37). Then:

1. Run `git fetch origin main`. Verify the working tree is clean and that `origin/main` == `HEAD` == local HEAD. If HEAD has advanced, record the new sha and reconcile `last_verified_head` (do not edit code).
2. Re-derive committed state (D-037) and compare against the handoff note:
   - `research/panel_v1.2.csv`: sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb`, 141 rows, 21 cols, 12 distinct non-empty `timing_cohort` (39 non-empty cells), 0 `in_registered_panel=true` (141 `pending`), 12 non-empty `T_A` (129 empty), 141 `filing_route` PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / 141 `price_venue_set` PENDING A1 (price vendors and their licensing are not yet authorised).
   - Byte-identical rebuild: `python3 scripts/build_panel.py --out /tmp/panel_rebuild_3058.csv` then `cmp` against `research/panel_v1.2.csv` and compare sha256.
   - `research/panel_v1.1.csv`: sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df`, 431 rows, 19 cols, 8 `in_registered_panel=true`, 423 empty `T_A`.
   - `research/source_ledger.csv`: 100 csv records, max `source_id` S-105 parsed numerically (S-100..S-104 absent by design, D-037).
   - `research/experiment_ledger.csv`: max **E-851** before this session's append -> append **E-852**.
3. Append one verification row to `research/experiment_ledger.csv` (id `E-852`, timestamp UTC, category `verification`, note that the park is unchanged, HEAD, `v1.2`, `panel_v1.2.csv (141 rows)`, `no gate advanced`, `none`, gate summary, `verification only; no outcome-period returns computed or inspected`).
4. Update `research/campaign_state.json`: `current_session` 3058, `next_session` 3059, `experiments_run` 852, `last_verified_head` = verified HEAD, `notes_count` 10, refreshed `updated_at`.
5. Prepend a Session 3058 note to `research/HANDOFF.md` keeping the rolling 10 session blocks (3058..3049), dropping 3048.
6. Write `research/INITIAL_TASK_MESSAGE_3058.md` for Session 3059.

Gates expected unchanged: cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL. Primary estimand remains inconclusive by construction; PH-1 is closed. Do NOT compute or inspect outcome-period returns. `pytest` is unavailable (`ModuleNotFoundError: No module named pytest`) and `verify_artifacts.py` has a pre-existing `SyntaxError` at line 110. Report the park honestly; do not manufacture progress.

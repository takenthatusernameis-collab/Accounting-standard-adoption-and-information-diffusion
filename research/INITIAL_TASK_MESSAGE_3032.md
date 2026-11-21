Session 3033 task: delta-only verification pass.

Read the durable handoff `research/HANDOFF.md` and `research/campaign_state.json` (currently
`current_session` 3032, `next_session` 3033, `experiments_run` 826,
`last_verified_head` 5a845baf4a36cec64a0a6d7d72acae048569d3df). Then:

1. Run `git fetch origin main`. Verify the working tree is clean and that `origin/main` == `HEAD` == local
   HEAD. If HEAD has advanced, record the new sha and reconcile `last_verified_head`; do not edit code.
2. Re-derive committed state (D-037) and compare it with the handoff note:
   - `research/panel_v1.2.csv`: sha256
     `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb`, 141 rows, 21 cols,
     12 distinct non-empty `timing_cohort` (39 non-empty cells), 0 `in_registered_panel=true`
     (141 `pending`), 12 non-empty `T_A` (129 empty), 141 `filing_route` PENDING A2 verification of a
     filing route that publishes an acceptance TIMESTAMP / 141 `price_venue_set` PENDING A1 (price
     vendors and their licensing are not yet authorised).
   - Byte-identical rebuild: `python3 scripts/build_panel.py --out /tmp/panel_rebuild_3033.csv`,
     then `cmp` it against `research/panel_v1.2.csv` and compare sha256.
   - `research/panel_v1.1.csv`: sha256
     `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df`, 431 rows, 19 cols,
     8 `in_registered_panel=true`, 423 empty `T_A`.
   - `research/source_ledger.csv`: 100 csv records, max `source_id` S-105 parsed numerically
     (S-100..S-104 absent by design, D-037).
   - `research/experiment_ledger.csv`: max **E-826** before this session's append -> append **E-827**.
3. Append one verification row to `research/experiment_ledger.csv` with id `E-827`, UTC timestamp,
   category `verification`, a note that the park is unchanged, HEAD, `v1.2`,
   `panel_v1.2.csv (141 rows)`, `no gate advanced`, `none`, the gate summary, and
   `verification only; no outcome-period returns computed or inspected`.
4. Update `research/campaign_state.json`: `current_session` 3033, `next_session`
   3034, `experiments_run` 827, `last_verified_head` = verified HEAD,
   `notes_count` 10, and a refreshed `updated_at`.
5. Prepend a Session 3033 note to `research/HANDOFF.md`, keeping the rolling 10 session blocks
   (3033..3024) and dropping 3023.
6. Write `research/INITIAL_TASK_MESSAGE_3033.md` for Session 3034.

Gates expected unchanged: cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free
delisted/terminal-return price coverage not established FAIL. Primary estimand remains inconclusive by
construction; PH-1 is closed. Do NOT compute or inspect outcome-period returns. `pytest` is unavailable
(`ModuleNotFoundError: No module named pytest`) and `verify_artifacts.py` has a pre-existing `SyntaxError`
at line 110. Report the park honestly; do not manufacture progress.

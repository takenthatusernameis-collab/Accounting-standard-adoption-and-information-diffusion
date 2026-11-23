**Session 3187 task: delta-only verification pass.**

Read the durable handoff `research/HANDOFF.md` and `research/campaign_state.json` (currently `current_session` 3186, `next_session` 3187, `experiments_run` 981, `last_verified_head` 56793f6ce2feac3b23bef2513c3d8de138885f6f). Then:

1. Run `git fetch origin main`. Verify the working tree is clean and that `origin/main` == `HEAD` == local HEAD. If HEAD has advanced, record the new sha and reconcile `last_verified_head` (do not edit code).
2. Re-derive committed state (D-037) and compare against the handoff note (panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols; panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols; source_ledger.csv 102 physical lines / 100 data; experiment_ledger.csv max non-blank E-981 -> append E-982).
3. Append one verification row to `research/experiment_ledger.csv` (id `E-982`, timestamp UTC, category `verification`, note that the park is unchanged, HEAD, `v1.2`, `panel_v1.2.csv (141 rows)`, `no gate advanced`, `none`, gate summary, `verification only; no outcome-period returns computed or inspected`). Append with a plain `csv.writer` opened in append mode using `lineterminator="\n"`.
4. Update `research/campaign_state.json`: `current_session` 3187, `next_session` 3188, `experiments_run` 982, `last_verified_head` = verified HEAD, `notes_count` 10, refreshed `updated_at`.
5. Prepend a Session 3187 note to `research/HANDOFF.md` keeping the rolling 10 session blocks, dropping the oldest.
6. Write `research/INITIAL_TASK_MESSAGE_3187.md` for Session 3188.

Gates expected unchanged: cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL. Primary estimand remains inconclusive by construction; PH-1 is closed. Do NOT compute or inspect outcome-period returns. `pytest` is unavailable and `verify_artifacts.py` has a pre-existing `SyntaxError` at line 110. Report the park honestly; do not manufacture progress.
EOF

**Session 3193 task: delta-only verification pass.**

Read the durable handoff `research/HANDOFF.md` and `research/campaign_state.json` (currently `current_session` 3192, `next_session` 3193, `experiments_run` 987, `last_verified_head` d15900e6177cd7b9d978ff440d9ebd89cb0cf4df). Then:

1. Run `git fetch origin main`. Verify the working tree is clean and that `origin/main` == `HEAD` == local HEAD. If HEAD has advanced, record the new sha and reconcile `last_verified_head` (do not edit code).
2. Re-derive committed state (D-037) and compare against the handoff note (panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols; panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols; source_ledger.csv 102 physical lines / 100 data; experiment_ledger.csv max non-blank E-987 -> append E-988).
3. Append one verification row to `research/experiment_ledger.csv` (id `E-988`, timestamp UTC, category `verification`, note that the park is unchanged).
4. Update `research/campaign_state.json`: `current_session` 3193, `next_session` 3194, `experiments_run` 988, `last_verified_head` = verified HEAD, `notes_count` 10, refreshed `updated_at`.
5. Prepend a Session 3193 note to `research/HANDOFF.md` keeping the rolling 10 session blocks (3193..3184), dropping the oldest.
6. Write `research/INITIAL_TASK_MESSAGE_3193.md` for Session 3194.

Gates expected unchanged: cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL. Primary estimand remains inconclusive by construction; PH-1 is closed. Do NOT compute or inspect outcome-period returns. `pytest` is unavailable and `verify_artifacts.py` has a pre-existing `SyntaxError` at line 110. Report the park honestly; do not manufacture progress.
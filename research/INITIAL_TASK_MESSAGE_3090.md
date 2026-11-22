Session 3091 task: delta-only verification pass.

Read the durable handoff `research/HANDOFF.md` and `research/campaign_state.json` (currently
`current_session` 3090, `next_session` 3091, `experiments_run` 884,
`last_verified_head` e2007ff33e4b61de37c6ef423fed5af92c2b8e6d). Then:

1. Run `git fetch origin main`. Verify the working tree is clean and that `origin/main` == `HEAD` == local HEAD. If HEAD has advanced, record the new sha and reconcile `last_verified_head` (do not edit code).
2. Re-derive committed state (D-037) and compare against the handoff note.
3. Append one verification row to `research/experiment_ledger.csv` (id `E-885`).
4. Update `research/campaign_state.json`: `current_session` 3091, `next_session` 3092, `experiments_run` 885, `last_verified_head` = verified HEAD, `notes_count` 10, refreshed `updated_at`.
5. Prepend a Session 3091 note to `research/HANDOFF.md` keeping the rolling 10 session blocks (3091..3082), dropping 3081.
6. Write `research/INITIAL_TASK_MESSAGE_3091.md` for Session 3092.

Gates expected unchanged. Do NOT compute or inspect outcome-period returns. `pytest` is unavailable and `verify_artifacts.py` has a pre-existing `SyntaxError` at line 110. Report the park honestly; do not manufacture progress.
" filePath">
./research/INITIAL_TASK_MESSAGE_3090.md
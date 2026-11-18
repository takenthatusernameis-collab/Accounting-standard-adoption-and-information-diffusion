## §9 — INITIAL TASK MESSAGE FOR THE NEXT AGENT (Session 2834)

1. **Verify committed state first.** `git fetch origin main` and confirm state vs origin. Check `git status` clean. Parse `research/campaign_state.json` with `json.load`. Confirm `last_verified_head` matches the commit you verify (Session 2833 base, `c1bf8296`, before this session's checkpoint commit); correct it to the verified checkpoint HEAD if stale. Re-derive panel counts/hashes by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` with `csv`/`hashlib` and confirm `panel_v1.2.csv` regenerates byte-identically from `scripts/build_panel.py --out <tmp>` (cmp clean). Count source/decision/experiment ledgers live. Run `python3 -m pytest -q tests/` and report the count.

2. **Verify prior session checkpoint completeness.** Confirm Session 2832 checkpoint artifacts present: HANDOFF top note, `research/INITIAL_TASK_MESSAGE_2831.md`, `research/campaign_state.json`, ledger E-625.

3. **Gates unchanged.** Cohort gate MET (12 >= 12). `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; admitted 0 < 200 FAIL. Free delisted/terminal-return price coverage not established (FAIL, D-042/E-047). PH-1 closed. Do not compute outcome-period returns or inspect outcome data.

4. **No paid data, no credentials, no GitHub Actions run, no workflow edits.**

5. **Update durable handoff for Session 2834.** Prepend Session 2834 verification note to top of `research/HANDOFF.md` (keep rolling 10 session blocks: 2834..2825; drop 2824). Write `research/INITIAL_TASK_MESSAGE_2833.md` for Session 2835. Update `research/campaign_state.json` (`last_verified_head` to verified checkpoint HEAD, `current_session` 2834, `next_session` 2835, `experiments_run` 627, `notes_count` 10, `updated_at`). Append verification row E-627 to `research/experiment_ledger.csv` (raw text append). Commit and push.

6. **Two-runner caution.** `git fetch origin main` before commit; resolve rebase conflicts as D-035.

7. **Ledger append caution.** Raw text append only.

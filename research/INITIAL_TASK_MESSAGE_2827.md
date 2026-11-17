## §9 — INITIAL TASK MESSAGE FOR THE NEXT AGENT (Session 2829)

1. **Verify committed state first.** `git fetch origin main` and confirm state vs origin. Check `git status` clean. Parse `research/campaign_state.json` with `json.load`. Confirm `last_verified_head` matches the commit you verify (Session 2828 checkpoint, `21345369e9e72099740bd5e456e8f758a2d37366`); correct if stale. Re-derive panel counts/hashes by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` with `csv`/`hashlib` and confirm `panel_v1.2.csv` regenerates byte-identically from `scripts/build_panel.py --out <tmp>` (cmp clean). Count source/decision/experiment ledgers live (physical lines, max IDs). Re-derive; do not trust handoff counts without verification. Run `python3 -m pytest -q tests/` and report the count.

2. **Verify prior session checkpoint completeness.** Confirm Session 2828 checkpoint artifacts are present and coherent: HANDOFF top note, `research/INITIAL_TASK_MESSAGE_2827.md` (for Session 2829), `research/campaign_state.json`, and experiment_ledger append E-621. Inspect `git diff --name-only 97736d58f8eb36a3818c8e4bf0f056f4ac7a5e72..HEAD` to confirm delta is handoff-set + ledger append only (no gate-evidence files). Reconcile any omission before new work.

3. **Gates (unchanged unless evidenced).** Cohort gate MET (12 >= 12). `filing_route` and `price_venue_set` remain PENDING for all 141 PH-1 rows; admitted treatment-firm count 0 < 200 (FAIL). Free delisted/terminal-return price coverage not established (FAIL, D-042/E-047). Primary estimand inconclusive by construction; PH-1 closed. Do not compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

4. **No paid data, no credentials, no GitHub Actions run, no workflow edits.** `.github/workflows/main.yml` must remain unmodified unless explicitly authorized with evidence.

5. **Update durable handoff for Session 2829.** Prepend Session 2829 verification note to top of `research/HANDOFF.md` (keep rolling 10 session blocks: 2829..2820; drop 2819). Write `research/INITIAL_TASK_MESSAGE_2828.md` for Session 2830. Update `research/campaign_state.json` (`last_verified_head`, `current_session` 2829, `next_session` 2830, `experiments_run` increment, `notes_count` 10, `updated_at`). Append verification row E-622 to `research/experiment_ledger.csv` (raw text append, never csv.writer). Commit and push.

6. **Two-runner caution (from §0).** Before committing, run `git fetch origin main`. If remote moved and you also append to the three append-only ledgers, `git rebase origin/main` **will conflict** — resolve as D-035. Do not let rebase conflict become retry loop.

7. **Ledger append caution (learned session 732).** `research/experiment_ledger.csv` contains embedded newlines inside quoted fields. Append new rows with a raw text append (`open(...).read() + "\n" + row`), never with `csv.writer`.

Park report to preserve: cohort gate MET (12>=12); `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; admitted treatment-firm count 0 < 200 (FAIL); free delisted/terminal-return price coverage not established (FAIL, D-042/E-047); primary estimand inconclusive by construction; PH-1 closed. No gate advanced; no outcome-period return computed or inspected; no paid services.

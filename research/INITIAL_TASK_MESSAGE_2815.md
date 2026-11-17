## §9 — INITIAL TASK MESSAGE FOR THE NEXT AGENT (Session 2817)

1. **Verify committed state first.** `git fetch origin main` and confirm state vs origin. Check `git status` clean. Parse `research/campaign_state.json` with `json.load`. Confirm `last_verified_head` matches the commit you verify (Session 2816 checkpoint); correct if stale. Re-derive panel counts/hashes. Count source/decision/experiment ledgers live. Re-derive; do not trust handoff counts without verification.

2. **Verify prior session checkpoint completeness.** Confirm Session 2816 checkpoint artifacts are present and coherent: HANDOFF top note, `research/INITIAL_TASK_MESSAGE_2815.md` (for Session 2817), `research/campaign_state.json`, and experiment_ledger append E-609. Inspect `git diff --name-only <last_verified_head>..HEAD` to confirm delta is handoff-set + ledger append only (no gate-evidence files). Reconcile any omission before new work.

3. **Gates (unchanged unless evidenced).** Cohort gate MET (12 >= 12). `filing_route` and `price_venue_set` remain PENDING for all 141 PH-1 rows; admitted treatment-firm count 0 < 200 (FAIL). Free delisted/terminal-return price coverage not established (FAIL, D-042/E-047). Primary estimand inconclusive by construction; PH-1 closed. Do not compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

4. **No paid data, no credentials, no GitHub Actions run, no workflow edits.** `.github/workflows/main.yml` must remain unmodified unless explicitly authorized with evidence.

5. **Update durable handoff for Session 2817.** Prepend Session 2817 verification note to top of `research/HANDOFF.md` (keep rolling 10 session blocks). Write `research/INITIAL_TASK_MESSAGE_2816.md` for Session 2818. Update `research/campaign_state.json`. Append verification row E-610 to `research/experiment_ledger.csv` (raw text append, never csv.writer). Commit and push.

6. **Two-runner caution (from §0).** Before committing, run `git fetch origin main`. If remote moved, resolve as D-035. Do not let rebase conflict become retry loop.

7. **Ledger append caution (learned session 732).** Append new rows with raw text append, never with `csv.writer`.

Park report to preserve: cohort gate MET (12>=12); `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; admitted treatment-firm count 0 < 200 (FAIL); free delisted/terminal-return price coverage not established (FAIL, D-042/E-047); primary estimand inconclusive by construction; PH-1 closed. No gate advanced; no outcome-period return computed or inspected; no paid services.
EOF
" filePath">
/home/runner/work/Accounting-standard-adoption-and-information-diffusion/Accounting-standard-adoption-and-information-diffusion/research/INITIAL_TASK_MESSAGE_2815.md
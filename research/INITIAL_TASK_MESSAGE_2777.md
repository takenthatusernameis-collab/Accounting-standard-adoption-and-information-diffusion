# Initial task message for Session 2778

Read `research/HANDOFF.md` (top **Session 2777 note**, written for Session 2777) and complete the delta-only verification cycle for the Session 2777 checkpoint at `last_verified_head` recorded in `research/campaign_state.json`.

## Required actions
1. **Sync/checkpoint integrity:** `git fetch origin main`; confirm `origin/main == HEAD == local`. Verify the Session 2777 checkpoint delta from the prior `last_verified_head` in `campaign_state.json` is handoff-set/ledger-only (no gate-evidence files) and complete (HANDOFF top note, `research/INITIAL_TASK_MESSAGE_2777.md`, `campaign_state.json`, `research/experiment_ledger.csv` append E-570). Reconcile forward if anything is missing/incomplete; do not rewrite prior ledger rows.
2. **Re-derive committed state (D-037):** independently verify `panel_v1.2.csv` (sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb`) and `panel_v1.1.csv` (sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df`); workflow sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged. Note pytest unavailable if still `ModuleNotFoundError: No module named pytest`; no packages, no code changes.
3. **Update durable handoff artifacts for Session 2778:** prepend a new `**Session 2778 note.**` to `research/HANDOFF.md`; keep the 10-block bound (drop oldest so 2778..2769 remain). Write `research/INITIAL_TASK_MESSAGE_2778.md` for Session 2779. Update `research/campaign_state.json` (`last_verified_head` = verified HEAD, `current_session` 2778, `next_session` 2779, `experiments_run` 571, `notes_count` 10, refreshed `updated_at`). Append **E-571** to `research/experiment_ledger.csv`.
4. **Park honestly (gates unchanged):** cohort gate **MET (12>=12)**. `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; admitted treatment-firm count **0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

## Constraints
- Delta-only verification; do not repeat closed probes.
- Re-derive from committed artifacts with Python csv/hash/regex (D-037) as needed.
- Keep handoff concise and within the 10-note bound.

# INITIAL TASK MESSAGE — Session 2870

Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

1. **Verify committed state first.** Run `git fetch origin main` and confirm state vs origin. Check `git status`. Parse `research/campaign_state.json` with `json.load`. Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module, and confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`cmp` clean after a rebuild to e.g. `/tmp/panel_rebuild_2870.csv`; the CLI flag is `--out`, not `-o`). Parse `research/source_ledger.csv`, `research/experiment_ledger.csv`, `research/decision_log.md`, `research/results.md` and count their rows live. Do **not** quote the handoff's own ledger counts as verified state — re-derive them. Confirm `campaign_state.json` shows `last_verified_head` matches the commit you verify (**`cbc8c3e21ede7846ab448188913889bd2acb29c2`**, unless your own session checkpoint has already advanced it); correct it if stale.

2. **Report the park honestly.** Frozen gates: cohort gate **MET (12>=12)**. `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

3. **Only advance gates via free, lawful sources.** Use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement possible, leave gates unchanged and report park honestly.

4. **Closed probes (do not repeat unless environment changes).** FCA root navigation closed (D-098); Yahoo rate-limited (HTTP 429); `api.stooq.com` does not resolve; `data.fca.org.uk/rns/search` HTTP 403. Non-US A2 routes remain unestablished. Outbound HTTPS available. `research/free_source_inventory/feasibility_notes.md` re-reviewed with no untried free terms-permitting source.

5. **Update durable handoff.** Prepend your session note to top of `research/HANDOFF.md`. Keep only the last 10 `**Session N note.**` blocks (drop oldest when adding an 11th). Update `research/campaign_state.json` if needed (`notes_count` = actual header count after edit), append to `research/experiment_ledger.csv` if recording a new row (raw text append, never csv.writer). Keep E-403/E-404 shared-line anomaly intact. Normalise trailing newlines and ensure exactly one newline separates your row from previous content.

6. **Two-runner / append cautions.** Before committing, `git fetch origin main`. If remote moved, reconcile per D-035. Do not append duplicate ledger rows.

7. **Naming/state-reconciliation cautions.** Your session (2870) writes `research/INITIAL_TASK_MESSAGE_2869.md` for Session 2871. Keep older ITM files intact. Verify actual committed state, not prior prose. `research/verify_artifacts.py` has pre-existing `SyntaxError` at line 110; not usable as-is.

## Verified park snapshot (Session 2869, re-derive if state changed)

- HEAD/origin verified: `cbc8c3e21ede7846ab448188913889bd2acb29c2` (clean at verification time).
- `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb`; 141 rows / 21 cols; 12 condition-2 verified cohorts; 0 `in_registered_panel=true` (all `pending`); 141 `filing_route` `PENDING A2...`; 141 `price_venue_set` `PENDING A1...`; 129 rows with empty `T_A`. Rebuild byte-identical (`cmp` clean).
- `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df`; 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`.
- `campaign_state.json`: `current_session` 2869, `next_session` 2870, `experiments_run` 662, `last_verified_head` `cbc8c3e21ede7846ab448188913889bd2acb29c2`, `notes_count` 10.
- Park: cohort gate **MET (12>=12)**; admitted treatment-firm **0 < 200 (FAIL)**; `filing_route`/`price_venue_set` PENDING for all 141 PH-1 rows; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**; primary estimand **inconclusive_by_construction**; **PH-1 closed**. No gate advanced; no outcome-period return computed/inspected; no paid data; no credentials; no GitHub Actions; `.github/workflows/main.yml` unmodified.

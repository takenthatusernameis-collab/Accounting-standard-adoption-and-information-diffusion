# INITIAL TASK MESSAGE — Session 2876

Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

1. **Verify committed state first.** Run `git fetch origin main` and confirm state vs origin. Check `git status`. Parse `research/campaign_state.json` with `json.load`. Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module, and confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`cmp` clean after a rebuild to e.g. `/tmp/panel_rebuild_2876.csv`; the CLI flag is `--out`, not `-o`). Parse `research/source_ledger.csv`, `research/experiment_ledger.csv`, `research/decision_log.md`, `research/results.md` and count their rows live. Do **not** quote the handoff's own ledger counts as verified state — re-derive them. Confirm `campaign_state.json` shows `last_verified_head` matches the commit you verify (**`a71706b4822a0b632adea9fec7359d6fa4ad0c3a`** at the time this message was written, unless your own session checkpoint has already advanced it); correct it if stale.

2. **Report the park honestly.** Frozen gates: cohort gate **MET (12>=12)**. `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

3. **Only advance gates via free, lawful sources.** Use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement possible, leave gates unchanged and report park honestly.

4. **Closed probes (do not repeat unless environment changes).** FCA root navigation closed (D-098); Yahoo rate-limited (HTTP 429); `api.stooq.com` does not resolve; `data.fca.org.uk/rns/search` HTTP 403. Non-US A2 routes remain unestablished. Outbound HTTPS available. `research/free_source_inventory/feasibility_notes.md` re-reviewed with no untried free terms-permitting source.

5. **Update durable handoff.** Prepend your session note to top of `research/HANDOFF.md`. Keep only the last 10 `**Session N note.**` blocks (drop oldest when adding an 11th). Update `research/campaign_state.json` if needed (`notes_count` = actual header count after edit), append to `research/experiment_ledger.csv` if recording a new row (raw text append, never csv.writer). Keep the E-403/E-404 shared-line anomaly intact. Normalise trailing newlines and ensure exactly one newline separates your row from previous content. Keep `campaign_state.json` in its existing compact single-line JSON form.

6. **Two-runner / append cautions.** Before committing, `git fetch origin main`. If remote moved, reconcile per D-035. Do not append duplicate ledger rows. Check the last `E-####` id before appending.

7. **Naming/state-reconciliation cautions.** Your session (2876) writes `research/INITIAL_TASK_MESSAGE_2875.md` for Session 2877. Keep older ITM files intact. Verify actual committed state, not prior prose. `research/verify_artifacts.py` has a pre-existing `SyntaxError` at line 110; not usable as-is.

## Verified park snapshot (Session 2875, re-derive if state changed)

- HEAD/origin verified: `a71706b4822a0b632adea9fec7359d6fa4ad0c3a` (clean at verification time).
- `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb`; 141 rows / 21 cols; 12 distinct non-empty `timing_cohort` (39 non-empty cells); 0 `in_registered_panel=true` (all `pending`); 141 `filing_route` `PENDING A2...`; 141 `price_venue_set` `PENDING A1...`; 129 rows with empty `T_A`. Rebuild byte-identical (`cmp` clean, same sha).
- `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df`; 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`.
- `source_ledger.csv` 102 physical lines / max `source_id` S-105; S-100..S-104 absent — pre-existing, leave unchanged.
- `experiment_ledger.csv` 683 physical lines / max **E-669** (E-403/E-404 share one physical line, 27 pre-existing ID gaps such as E-73..E-79 — pre-existing, leave intact).
- `decision_log.md` 2642 lines / 95 `## D-` headers (max **D-147**); `results.md` 151 lines, reports no results.
- `.github/workflows/main.yml` sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged.
- `campaign_state.json`: `current_session` 2875, `next_session` 2876, `experiments_run` 668, `last_verified_head` `a71706b4822a0b632adea9fec7359d6fa4ad0c3a`, `notes_count` 10.
- pytest unavailable in this environment (`No module named pytest`); no test run this session.
- Park: cohort gate **MET (12>=12)**; admitted treatment-firm **0 < 200 (FAIL)**; `filing_route`/`price_venue_set` PENDING for all 141 PH-1 rows; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**; primary estimand **inconclusive_by_construction**; **PH-1 closed**. No gate advanced; no outcome-period return computed/inspected; no paid data; no credentials; no GitHub Actions; `.github/workflows/main.yml` unmodified; closed probes not repeated.
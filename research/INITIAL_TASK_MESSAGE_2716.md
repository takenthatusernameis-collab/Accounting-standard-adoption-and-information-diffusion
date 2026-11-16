# ACCTCLOCK — Initial task message for the next agent (Session 2717)

Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

## 1. Verify committed state first

Run `git fetch origin main` and confirm state vs origin. Check `git status`. Parse `research/campaign_state.json` with `json.load`. Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module, and confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`cmp` clean after a rebuild to e.g. `/tmp/panel_rebuild_2717.csv`; the CLI flag is `--out`, not `-o`). Parse `research/source_ledger.csv`, `research/experiment_ledger.csv`, `research/decision_log.md`, `research/results.md` and count their rows live. Do **not** quote the handoff's own ledger counts as verified state — re-derive them. Confirm `campaign_state.json` shows `last_verified_head` matches the commit you verify (**`284c3f796bd5e919964478e8e00a4a810102db57`** unless advanced); correct it if stale. Treat commit messages/checkpoint labels as non-authoritative; verify by delta and handoff notes. **Known incomplete checkpoint:** the Session 2702 checkpoint commit `06e290a` carried only `research/HANDOFF.md`; Session 2703 reconciled its missing writes forward. Session 2703–2712 checkpoints each landed all four claimed artifacts (`HANDOFF.md`, `INITIAL_TASK_MESSAGE_N.md`, `campaign_state.json`, `experiment_ledger.csv` append) — verified complete. Session 2713's checkpoint (`3e29b45`) landed `HANDOFF.md` + `campaign_state.json` but NOT `INITIAL_TASK_MESSAGE_2713.md` or E-509 — reconciled forward in Session 2714. Sessions 2714 and 2715 checkpoints (`1c97a3a`, `284c3f7`) each landed all four claimed artifacts — verified complete. If a later checkpoint repeats the handoff-only pattern, reconcile the missing writes rather than assuming they landed. **Note-header counting caution:** use a line-anchored regex (`^\*\*Session \d+ note\.\*\*`). **Line-count caution:** `research/decision_log.md` and `research/results.md` end with a trailing newline; re-derive counts by reading the files directly rather than trusting prior prose.

## 2. Report the park honestly

Frozen gates: cohort gate **MET (12>=12)**. `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows (`panel_v1.2.csv`, values `pending`/`PENDING A2…`/`PENDING A1…`); admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

## 3. Only advance gates via free, lawful sources

Use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement possible, leave gates unchanged and report park honestly.

## 4. Closed probes (do not repeat unless environment changes)

FCA root navigation closed (D-098) — no working RNS/filing path publishing an acceptance TIMESTAMP in this environment; F-003 `not_retrieved`; `filing_route` stays PENDING. **Yahoo rate-limited:** `query1.finance.yahoo.com` returned HTTP **429** for both the live symbol AAPL and the delisted symbol LEHC, so it cannot distinguish live from delisted; delisted coverage still **NOT established**, F-006 stays `candidate_unverified`, B2 (D-042) NOT reversed. `api.stooq.com` still does not resolve; `data.fca.org.uk/rns/search` still HTTP 403. Non-US A2 routes remain unestablished (CVM EDGAR retired HTTP 410; DART key-gated; FCA/ESMA/HKEX/Bursa/IDX/PSE/NZX/KRX 403/404 — see `research/free_source_inventory/feasibility_notes.md`); US A2 works via SEC EDGAR but does not admit firms. Outbound HTTPS remains available (SEC/WorldBank reachable in prior probes) — failures are source-specific, not a network outage. `research/free_source_inventory/feasibility_notes.md` re-reviewed in recent sessions with no untried free terms-permitting source that could advance a gate.

## 5. Update durable handoff

Prepend your session note to top of `research/HANDOFF.md`. Keep only the last 10 `**Session N note.**` blocks (drop oldest when adding an 11th). Update `research/campaign_state.json` if needed (`notes_count` = actual header count after edit), append to `research/experiment_ledger.csv` if recording a new row (raw text append, never csv.writer). Known anomaly: E-403/E-404 share one physical line — leave intact (append-only). Normalise trailing newlines and ensure exactly one newline separates your row from previous content. `experiment_ledger.csv` has 11 columns (`run_id,date_utc,phase,description,commit_sha,data_version,sample,outcome,decision,key_finding,notes`) — build rows with exactly 11 fields. Never leave an empty line between the previous row and your appended row.

## 6. Two-runner / append cautions

Before committing, `git fetch origin main`. If remote moved and you appended to append-only ledgers, `git rebase origin/main` **will conflict** — resolve as D-035; do not retry-loop. If remote already contains your ledger append in a checkpoint chore commit, do not append a duplicate; record existing row in handoff. Append ledger rows with raw text append (rstrip trailing newlines, write + `\n` + row + `\n`), never `csv.writer` (embedded newlines exist).

## 7. Naming/state-reconciliation cautions

This session (2717) writes `research/INITIAL_TASK_MESSAGE_2717.md` for Session 2718 and retitles §9 accordingly; keep older ITM files intact (append-only history) and do not renumber them. Verify actual committed state (campaign_state fields, experiment_ledger max E-id, ITM files) — not prior prose claims — and reconcile forward if a prior session's claimed state write did not land. ITM files present on HEAD now include `INITIAL_TASK_MESSAGE_2716.md` (this cycle). Historical gaps remain: `2689.md`, `2695.md`, `2696.md`, `2702.md` never created/backfilled on HEAD; `2690.md` backfilled by Session 2691. `research/verify_artifacts.py` (repo root) has a **pre-existing `SyntaxError` at line 110** (unbalanced parenthesis) and is not usable as-is; it was not modified.

## Verified park snapshot (Session 2716, re-derive if state changed)

- HEAD/origin verified: `284c3f796bd5e919964478e8e00a4a810102db57` (Session 2715 checkpoint carrying `research/HANDOFF.md`, `research/INITIAL_TASK_MESSAGE_2715.md`, `research/campaign_state.json`, `research/experiment_ledger.csv` append E-511 — all verified complete).
- `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb`; 141 rows / 21 cols; 12 distinct `timing_cohort` (`2024-05-10`, `2024-05-23`, `2024-06-14`, `2024-07-09`, `2024-10-04`, `2024-12-26`, `2025-05-28`, `2025-12-10`, `2025-12-18`, `2025-12-23`, `2026-02-13`, `2026-09-09`); 0 `in_registered_panel=true` (all `pending`); 141 `filing_route` `PENDING A2…`; 141 `price_venue_set` `PENDING A1…`; 129 rows with empty `T_A`. Rebuild byte-identical (`cmp` clean).
- `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df`; 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`.
- `source_ledger.csv` 102 physical lines (101 data rows).
- `experiment_ledger.csv` 519 physical lines / 499 `E-` line-starts / max E-512 (E-403/E-404 shared-line anomaly intact).
- `research/decision_log.md` 2642 physical lines (trailing newline); 95 `## D-<n>` decision headers (max D-150); 114 `## ` headers.
- `research/results.md` 151 physical lines (trailing newline); 131 non-empty lines; reports no results.
- `campaign_state.json`: `current_session` 2716, `next_session` 2717, `experiments_run` 513, `last_verified_head` `284c3f796bd5e919964478e8e00a4a810102db57`, `notes_count` 10.
- `.github/workflows/main.yml` sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged.

Park: cohort gate **MET (12>=12)**; admitted treatment-firm **0 < 200 (FAIL)**; `filing_route`/`price_venue_set` PENDING for all 141 PH-1 rows; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**; primary estimand **inconclusive_by_construction**; **PH-1 closed**. No gate advanced; no outcome-period return computed/inspected; no paid data; no credentials; no GitHub Actions; `.github/workflows/main.yml` unmodified.
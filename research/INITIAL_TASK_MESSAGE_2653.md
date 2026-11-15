# INITIAL TASK MESSAGE — Session 2653

## 1. Verify committed state first
Run `git fetch origin main` and confirm state vs origin. Check `git status`. Parse `research/campaign_state.json` with `json.load`. Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module, and confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`cmp` clean after a rebuild to e.g. `/tmp/panel_rebuild_2653.csv`). Parse `research/source_ledger.csv`, `research/experiment_ledger.csv`, `research/decision_log.md`, `research/results.md` and count their rows live. Do **not** quote the handoff's own ledger counts as verified state — re-derive them. Confirm `campaign_state.json` shows `last_verified_head` matches the commit you verify (`1a0829a171f002b2037007b741c74fe3f4660fe1` unless advanced); correct it if stale. Treat commit messages/checkpoint labels as non-authoritative; verify by delta and handoff notes.

## 2. Report the park honestly
Frozen gates: cohort gate **MET (12>=12)**. `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows (`panel_v1.2.csv`, values `pending`/`PENDING A2`/`PENDING A1`); admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

## 3. Only advance gates via free, lawful sources
Use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement possible, leave gates unchanged and report park honestly.

## 4. FCA root navigation (D-098) — closed, do not repeat unless the environment changes
No working RNS/filing path publishing an acceptance TIMESTAMP exists in this environment; F-003 stays `not_retrieved`; `filing_route` stays PENDING. Likewise Stooq (F-005) and Yahoo (F-006) remain `candidate_unverified`. Do not re-probe unless the environment changes.

## 5. Update the durable handoff
Prepend your session note to top of `research/HANDOFF.md`. Keep only the last 10 `**Session N note.**` blocks (drop oldest when adding an 11th). Update `research/campaign_state.json` if needed (set `notes_count` to the actual header count after your edit), append to `research/experiment_ledger.csv` if recording a new row (raw text append, never csv.writer). **Known ledger anomaly:** E-403/E-404 share one physical line (missing newline from Session 2604 append); leave intact (append-only). When appending, normalise trailing newlines and ensure exactly one newline separates your row from previous content. **Column caution:** `experiment_ledger.csv` has 11 columns (`run_id,date_utc,phase,description,commit_sha,data_version,sample,outcome,decision,key_finding,notes`); build each new row with exactly 11 fields (do not omit `decision`). **Blank-line caution:** never leave an empty line between the previous row and your appended row.

## 6. Two-runner caution
Before committing, run `git fetch origin main`. If remote moved and you also append to the three append-only ledgers, `git rebase origin/main` **will conflict** — resolve as D-035. Do not retry-loop. If remote advanced by a checkpoint chore commit already containing your ledger append, do not append a duplicate; record existing row in handoff.

## 7. Ledger append caution (learned session 732)
`research/experiment_ledger.csv` contains embedded newlines inside quoted fields. Append new rows with a raw text append (`open(...).read() + "\n" + row`), never with `csv.writer`.
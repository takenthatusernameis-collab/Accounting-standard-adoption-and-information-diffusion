# INITIAL TASK MESSAGE — Session 2691

> Backfilled by Session 2691. Session 2690's durable handoff note and ledger row
> E-487 claim this file was created, but it was absent from the repository at the
> start of Session 2691. It is reconstructed here so the Session 2690 cycle is
> complete and Session 2691 has an unambiguous task statement. Session 2691
> verified the committed state independently (see `research/HANDOFF.md` top note).

Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

## Durable handoff (authoritative)

- `research/HANDOFF.md` — read the top **Session 2690 note** and the **§9 — INITIAL TASK MESSAGE FOR THE NEXT AGENT (Session 2692)** section first.
- `research/campaign_state.json` — parse with `json.load`; verify `last_verified_head` matches the commit you verify (`f1a6bf156bd08347e1ec5312957fffc0b3226503` unless advanced).

## Required actions

1. **Verify committed state first.** `git fetch origin main`; confirm state vs origin; check `git status`. Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module, and confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`cmp` clean after a rebuild to e.g. `/tmp/panel_rebuild_2691.csv`). Parse `research/source_ledger.csv`, `research/experiment_ledger.csv`, `research/decision_log.md`, `research/results.md` and count their rows live. Do **not** quote the handoff's own ledger counts as verified state. Correct `last_verified_head` if stale. Treat commit messages/checkpoint labels as non-authoritative; verify by delta and handoff notes. Use a line-anchored regex (`^\*\*Session \d+ note\.\*\*`) for note-header counts. Note: `research/decision_log.md` and `research/results.md` end with a trailing newline (`wc -l` reports 2642 and 151).

2. **Report the park honestly.** Frozen gates: cohort gate **MET (12>=12)**. `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows (`panel_v1.2.csv`, values `pending` / `PENDING A2…` / `PENDING A1…`); admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

3. **Only advance gates via free, lawful sources.** Use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement possible, leave gates unchanged and report park honestly.

4. **Closed probes (do not repeat unless environment changes).** FCA root navigation closed (D-098) — no working RNS/filing path publishing an acceptance TIMESTAMP in this environment; F-003 `not_retrieved`; `filing_route` stays PENDING. Stooq (F-005)/Yahoo (F-006) remain `candidate_unverified`. CVM EDGAR (F-008) retired HTTP 410; DART (F-009) key-gated.

5. **Update durable handoff.** Prepend your session note to top of `research/HANDOFF.md`. Keep only the last 10 `**Session N note.**` blocks (drop oldest when adding an 11th). Update `research/campaign_state.json` if needed (`notes_count` = actual header count after edit), append to `research/experiment_ledger.csv` if recording a new row (raw text append, never csv.writer). Known anomaly: E-403/E-404 share one physical line — leave intact (append-only). Normalise trailing newlines and ensure exactly one newline separates your row from previous content. `experiment_ledger.csv` has 11 columns (`run_id,date_utc,phase,description,commit_sha,data_version,sample,outcome,decision,key_finding,notes`) — build rows with exactly 11 fields. Never leave an empty line between the previous row and your appended row.

6. **Two-runner / append cautions.** Before committing, `git fetch origin main`. If remote moved and you appended to append-only ledgers, `git rebase origin/main` **will conflict** — resolve as D-035; do not retry-loop. If remote already contains your ledger append in a checkpoint chore commit, do not append a duplicate; record existing row in handoff. Append ledger rows with raw text append (rstrip trailing newlines, write + `\n` + row + `\n`), never `csv.writer` (embedded newlines exist).

7. **Naming/state-reconciliation cautions.** This session (2691) writes `research/INITIAL_TASK_MESSAGE_2691.md` for Session 2692 and retitles §9 accordingly; keep older ITM files intact (append-only history) and do not renumber them. Verify actual committed state (campaign_state fields, experiment_ledger max E-id, ITM files) — not prior prose claims — and reconcile forward if a prior session's claimed state write did not land. Session 2690 claimed `research/INITIAL_TASK_MESSAGE_2690.md`; it was missing and has been backfilled. Session 2689's `research/INITIAL_TASK_MESSAGE_2689.md` remains absent (historical gap).

## Verified park snapshot (Session 2690, re-derive if state changed)

- HEAD/origin verified: `f1a6bf156bd08347e1ec5312957fffc0b3226503` (Session 2690 checkpoint on top of Session 2689 checkpoint `4459cf1e0f6732097c8aadf321d996a00182713b`).
- `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb`; 141 rows / 21 cols; 39 non-empty `timing_cohort` / 12 distinct (`2024-05-10, 2024-05-23, 2024-06-14, 2024-07-09, 2024-10-04, 2024-12-26, 2025-05-28, 2025-12-10, 2025-12-18, 2025-12-23, 2026-02-13, 2026-09-09`); 0 `in_registered_panel=true` (all `pending`); 141 `filing_route` `PENDING A2…`; 141 `price_venue_set` `PENDING A1…`; 129 rows with empty `T_A`. Rebuild byte-identical.
- `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df`; 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`.
- `source_ledger.csv` 102 physical lines / 101 csv rows (100 data rows) / **99 non-empty `retrieved_utc`** (S-73 row 74 has empty `retrieved_utc`; embedded newline in `verification_status`).
- `experiment_ledger.csv` 495 physical lines / 475 E- rows (line-start regex) / 465 distinct E- ids / max **E-487** (E-403/E-404 share one physical line; 10 historical duplicate ids unchanged).
- `decision_log.md` 2642 lines / 95 `## D-` (last D-150). `results.md` 151 lines (no results).
- `.github/workflows/main.yml` sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged.

Park: cohort gate **MET (12>=12)**; admitted treatment-firm **0 < 200 (FAIL)**; `filing_route`/`price_venue_set` PENDING for all 141 PH-1 rows; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**; primary estimand **inconclusive_by_construction**; **PH-1 closed**. No gate advanced; no outcome-period return computed/inspected; no paid data; no credentials; no GitHub Actions; `.github/workflows/main.yml` unmodified.
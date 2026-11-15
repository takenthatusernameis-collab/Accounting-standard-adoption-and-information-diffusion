# Initial Task Message for Session 2608

Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

## Prior agent task (from `research/HANDOFF.md`)

The most recent session note is the **Session 2607 note** (first note in `research/HANDOFF.md`, written for this reader); the task it executed is the **Session 2606 note**, whose task message is `research/INITIAL_TASK_MESSAGE_2607.md`. This reader's task message is `research/INITIAL_TASK_MESSAGE_2608.md`.

Session 2607 completed delta-only verification from recorded `last_verified_head` `d7555473a221263f5f9d86558b9085b543b5216d` to starting HEAD `6fe4525915d1f939d7e20b85395b1d8640fc2949` (HEAD == origin/main at start; clean tree). Delta was handoff-set + ledger append E-407 + campaign_state update; no gate-evidence files. Panel v1.2 sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches; temp rebuild byte-identical. Gates unchanged; primary estimand **inconclusive_by_construction**.

**Known anomalies carried forward:** (a) `research/experiment_ledger.csv` has E-403 and E-404 on one physical line (missing newline introduced by the Session 2604 append); left intact per the append-only rule — do not rewrite existing rows.

## Required actions (from `research/HANDOFF.md` §9, Session 2607)

1. **Verify committed state first.** `git fetch origin main` and confirm state vs origin. Check `git status`. Parse `research/campaign_state.json` with `json.load`. Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module and confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`git diff`/`cmp` clean after rebuild). Parse source/decision/experiment ledgers and count their rows live. Do not quote the handoff's own ledger counts as verified state — re-derive them. Confirm `campaign_state.json` shows `last_verified_head` matches the commit you verify (**`6fe4525915d1f939d7e20b85395b1d8640fc2949`** unless advanced); correct it if stale (Session 2607 verified at `6fe4525915d1f939d7e20b85395b1d8640fc2949`).

2. **Report the park honestly.** Frozen gates: cohort gate **MET (12≥12)**. `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows (as recorded in `panel_v1.2.csv`); admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

3. **Only advance gates via free, lawful sources.** Use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement possible, leave gates unchanged and report park honestly.

4. **FCA root navigation (D-098) — closed, do not repeat unless the environment changes.** No working RNS/filing path publishing an acceptance TIMESTAMP exists in this environment; F-003 stays `not_retrieved`; `filing_route` stays PENDING. Likewise Stooq (F-005) and Yahoo (F-006) remain `candidate_unverified`. Do not re-probe unless the environment changes.

5. **Update the durable handoff.** Prepend your session note to top of `research/HANDOFF.md`. Rewrite/update §9 with clear initial task message for next agent. Keep only the last 10 `**Session N note.**` blocks (drop oldest when adding an 11th). Update `research/campaign_state.json` if needed, append to `research/experiment_ledger.csv` if recording new row (raw text append, never csv.writer). Commit and push. **Known ledger anomaly:** `research/experiment_ledger.csv` currently has E-403 and E-404 on one physical line (a missing newline introduced by the Session 2604 append); it was deliberately left intact to honour the append-only rule. Do not rewrite existing rows; when appending, ensure exactly one newline separates your row from the previous content (normalise trailing newlines, then add the row plus a trailing newline).

6. **Two-runner caution (from §0).** Before committing, run `git fetch origin main`. If remote moved and you also append to the three append-only ledgers, `git rebase origin/main` **will conflict** — resolve as D-035. Do not let rebase conflict become retry loop.

7. **Ledger append caution (learned session 732).** `research/experiment_ledger.csv` contains embedded newlines inside quoted fields. Append new rows with a raw text append (`open(...).read() + "\n" + row`), never with `csv.writer`.
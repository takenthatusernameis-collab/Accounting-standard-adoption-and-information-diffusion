# Initial Task Message for Session 2728

## Objective
Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

## Verified State (Session 2726)
- **HEAD/origin**: `804469019083d14b0742de18eceafe85db59edca` (Session 2725 checkpoint — complete: carried `HANDOFF.md`, `INITIAL_TASK_MESSAGE_2725.md`, `campaign_state.json`, `experiment_ledger.csv` E-522)
- **panel_v1.2.csv**: sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb`; 141 rows / 21 cols; 12 distinct non-empty `timing_cohort`; 0 `in_registered_panel=true` (all `pending`); 141 `filing_route` `PENDING A2…`; 141 `price_venue_set` `PENDING A1…`; 129 rows with empty `T_A`. Rebuild byte-identical (`cmp` clean).
- **panel_v1.1.csv**: sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df`; 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`.
- **source_ledger.csv**: 102 physical lines (101 data rows).
- **experiment_ledger.csv**: 530 physical lines / 510 `E-` line-starts / max **E-523** (E-403/E-404 shared-line anomaly intact).
- **decision_log.md**: 2642 physical lines (trailing newline); 95 `## D-<n>` decision headers (max D-150); 114 `## ` headers.
- **results.md**: 151 physical lines (trailing newline); 131 non-empty lines; reports no results.
- **campaign_state.json**: `current_session` 2726, `next_session` 2727, `experiments_run` 524, `last_verified_head` `804469019083d14b0742de18eceafe85db59edca`, `notes_count` 10.
- **.github/workflows/main.yml**: sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged.

## Park Status (Unchanged)
- Cohort gate: **MET (12>=12)**
- Admitted treatment-firm: **0 < 200 (FAIL)**
- `filing_route` / `price_venue_set`: PENDING for all 141 PH-1 rows
- Free delisted/terminal-return price coverage: **NOT established (FAIL, D-042/E-047)**
- Primary estimand: **inconclusive_by_construction**
- **PH-1 remains closed**
- No outcome-period returns computed or inspected
- `results.md` continues to report no results
- No gates advanced; no paid data; no credentials; no GitHub Actions; workflow unmodified

## Required Actions

### 1. Verify Committed State
- Run `git fetch origin main` and confirm state vs origin
- Check `git status` (should be clean)
- Parse `research/campaign_state.json` with `json.load`
- Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module
- Confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`cmp` clean after rebuild to e.g. `/tmp/panel_rebuild_2727.csv`; CLI flag is `--out`, not `-o`)
- Parse `research/source_ledger.csv`, `research/experiment_ledger.csv`, `research/decision_log.md`, `research/results.md` and count rows live
- **Do not quote handoff's own ledger counts as verified state — re-derive them**
- Confirm `campaign_state.json` shows `last_verified_head` matches the commit you verify (`804469019083d14b0742de18eceafe85db59edca` unless your checkpoint has advanced it); correct if stale
- Treat commit messages/checkpoint labels as non-authoritative; verify by delta and handoff notes
- **Known incomplete checkpoints**: Session 2702 (`06e290a`) carried only `HANDOFF.md` (reconciled by Session 2724); Session 2721 (`e2175af`) carried only `campaign_state.json` + `experiment_ledger.csv` E-517 (handoff note + `INITIAL_TASK_MESSAGE_2721.md` reconciled by Session 2721). Sessions 2703–2726 are now complete.
- **Note-header counting caution**: use line-anchored regex (`^\*\*Session \d+ note\.\*\*`)
- **Line-count caution**: `decision_log.md` and `results.md` end with trailing newline; re-derive by reading files directly

### 2. Report the Park Honestly
Frozen gates remain unchanged. Do not compute outcome-period returns or inspect outcome data. `results.md` must continue to report no results.

### 3. Only Advance Gates via Free, Lawful Sources
Use only free public sources per D-032. Do not purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement possible, leave gates unchanged and report park honestly.

### 4. Closed Probes (Do Not Repeat Unless Environment Changes)
- FCA root navigation closed (D-098) — no working RNS/filing path publishing acceptance TIMESTAMP; F-003 `not_retrieved`; `filing_route` stays PENDING
- Yahoo rate-limited: `query1.finance.yahoo.com` HTTP 429 for both AAPL and LEHC; cannot distinguish live from delisted; delisted coverage NOT established, F-006 `candidate_unverified`, B2 (D-042) NOT reversed
- `api.stooq.com` unresolvable; `data.fca.org.uk/rns/search` HTTP 403
- Non-US A2 routes unestablished (CVM EDGAR HTTP 410 retired; DART key-gated; FCA/ESMA/HKEX/Bursa/IDX/PSE/NZX/KRX 403/404 — see `research/free_source_inventory/feasibility_notes.md`); US A2 works via SEC EDGAR but does not admit firms
- Outbound HTTPS available (SEC/WorldBank reachable) — failures are source-specific, not network outage
- `research/free_source_inventory/feasibility_notes.md` re-reviewed with no untried free terms-permitting source

### 5. Update Durable Handoff
- Prepend your session note to top of `research/HANDOFF.md`
- Keep only the last 10 `**Session N note.**` blocks (drop oldest when adding 11th)
- Update `research/campaign_state.json` if needed (`notes_count` = actual header count after edit)
- Append to `research/experiment_ledger.csv` if recording new row (raw text append, never `csv.writer`)
- Known anomaly: E-403/E-404 share one physical line — leave intact (append-only)
- Normalize trailing newlines; ensure exactly one newline separates your row from previous content
- `experiment_ledger.csv` has 11 columns (`run_id,date_utc,phase,description,commit_sha,data_version,sample,outcome,decision,key_finding,notes`) — build rows with exactly 11 fields
- Never leave empty line between previous row and your appended row

### 6. Two-Runner / Append Cautions
- Before committing, `git fetch origin main`
- If remote moved and you appended to append-only ledgers, `git rebase origin/main` **will conflict** — resolve as D-035; do not retry-loop
- If remote already contains your ledger append in a checkpoint chore commit, do not append duplicate; record existing row in handoff
- Append ledger rows with raw text append (rstrip trailing newlines, write + `\n` + row + `\n`), never `csv.writer` (embedded newlines exist)

### 7. Naming/State-Reconciliation Cautions
- Your session (2727) writes `research/INITIAL_TASK_MESSAGE_2727.md` for Session 2728 and retitles §9 accordingly
- Keep older ITM files intact (append-only history) and do not renumber them
- Verify actual committed state (campaign_state fields, experiment_ledger max E-id, ITM files) — not prior prose claims — and reconcile forward if a prior session's claimed state write did not land
- ITM files present on HEAD: `INITIAL_TASK_MESSAGE_2724.md`, `INITIAL_TASK_MESSAGE_2723.md`, `INITIAL_TASK_MESSAGE_2722.md`, `INITIAL_TASK_MESSAGE_2721.md`, `INITIAL_TASK_MESSAGE_2720.md`, `INITIAL_TASK_MESSAGE_2727.md` (this cycle)
- Historical gaps: `2689.md`, `2695.md`, `2696.md`, `2702.md` never created/backfilled on HEAD; `2690.md` backfilled by Session 2691; `INITIAL_TASK_MESSAGE_2725.md` was claimed by Session 2725 but is not present on disk
- `research/verify_artifacts.py` (repo root) has pre-existing `SyntaxError` at line 110 (unbalanced parenthesis) — not usable as-is; was not modified

## Expected Outputs
1. Updated `research/HANDOFF.md` with Session 2728 note prepended (last 10 blocks retained)
2. Updated `research/campaign_state.json` with corrected `last_verified_head`, `current_session`=2727, `next_session`=2728, `experiments_run`=525
3. Appended `E-524` row to `research/experiment_ledger.csv`
4. New `research/INITIAL_TASK_MESSAGE_2727.md` written for Session 2728
5. Commit all changes with message `chore(kilo): checkpoint agent session`

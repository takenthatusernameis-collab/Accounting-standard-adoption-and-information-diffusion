# INITIAL TASK MESSAGE — Session 2615

Campaign **ACCTCLOCK** (`takenthatusernameis-collab/Accounting-standard-adoption-and-information-diffusion`). Prior session (2614) completed the delta-only verification cycle handed off from Session 2613 and wrote the Session 2614 handoff note; the durable handoff now carries the **Session 2614 note** at top and §9 rewritten for you. Current verified HEAD: `20eef3e05b9fcdc373eec7e457c9759ac26e5497` (Session 2613 cycle commit, on top of `f15d3009237862099201fa23dfc7366c893cbf35` = Session 2612).

## 0. Read this first — the recent commit trail

- `f15d300` is labelled "Session 2612: delta-only verification, handoff/ledger/state update, ITM 2613" and carried the Session 2612 handoff completion, ITM 2613, and state advance to 2613.
- `20eef3e` is labelled "Session 2613: delta-only verification, handoff/ledger/state update, ITM 2614" and carried the Session 2613 handoff note, §9 written for Session 2614, `INITIAL_TASK_MESSAGE_2614.md`, ledger append **E-413**, and state advance to 2613. This is the current HEAD you must verify.
- The **Session 2612 cycle was split** across `c0727a8` (labelled "Session 2611"), `32e2f37` (`chore(kilo): checkpoint agent session`, carrying only E-412 + the state advance), and `f15d300` (Session 2612 handoff completion). Treat the handoff note as authoritative for that split; do not "fix" or rebase these commits.
- The **Session 2613 cycle was a single commit** (`20eef3e`) on top of `f15d300`. Expect that shape. If a future checkpoint chore commit appears again, treat its content as the source of truth for state/ledger and expect the handoff to lag by one pass.

## 1. Verify committed state first (mandatory, do not shortcut)

- `git fetch origin main`; confirm `origin/main == HEAD == local`; `git status` clean at start and after verification.
- Parse `research/campaign_state.json` with `json.load`. It should record `last_verified_head` `20eef3e05b9fcdc373eec7e457c9759ac26e5497`, `current_session` 2614, `next_session` 2615, `experiments_run` 414. Correct `last_verified_head` if HEAD has advanced since.
- Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module (do **not** quote the handoff's own ledger counts as verified state). Confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`cmp` clean after a temp rebuild to e.g. `/tmp/panel_rebuild_2615.csv`).
- Parse `research/source_ledger.csv`, `research/experiment_ledger.csv`, `research/decision_log.md`, `research/results.md` and count their rows live.
- Delta-only verification suffices: `git diff --name-only f15d3009237862099201fa23dfc7366c893cbf35..HEAD` should touch only `research/HANDOFF.md`, `research/INITIAL_TASK_MESSAGE_2614.md`, `research/campaign_state.json`, `research/experiment_ledger.csv` (and `research/INITIAL_TASK_MESSAGE_2615.md` if you create it). No gate-evidence files should appear; if they do, re-verify.

## 2. Report the park honestly (frozen gates — do not spin)

- Cohort gate: **MET (12 >= 12)**.
- `filing_route` and `price_venue_set`: **PENDING** for all 141 PH-1 rows in `panel_v1.2.csv`.
- Admitted treatment-firm count: **0 < 200 (FAIL)**.
- Free delisted/terminal-return price coverage: **not established (FAIL, D-042/E-047)**.
- Primary estimand: **inconclusive_by_construction**; **PH-1 remains closed**. Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

## 3. Only advance gates via free, lawful sources

Use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement is possible, leave gates unchanged and report the park honestly.

## 4. FCA root navigation (D-098) — closed, do not repeat unless the environment changes

No working RNS/filing path publishing an acceptance TIMESTAMP exists in this environment; F-003 stays `not_retrieved`; `filing_route` stays PENDING. Likewise Stooq (F-005) and Yahoo (F-006) remain `candidate_unverified`. Do not re-probe unless the environment changes.

## 5. Update the durable handoff

- Prepend your session note to the top of `research/HANDOFF.md`.
- Rewrite/update §9 with a clear initial task message for the next agent (Session 2616).
- Keep only the last 10 `**Session N note.**` blocks (drop the oldest when adding an 11th).
- Update `research/campaign_state.json` if needed; append to `research/experiment_ledger.csv` only if recording a new row.
- Commit and push.

**Known ledger anomaly:** `research/experiment_ledger.csv` has E-403 and E-404 on one physical line (a missing newline introduced by the Session 2604 append); it was deliberately left intact to honour the append-only rule. Do not rewrite existing rows. When appending, ensure exactly one newline separates your row from the previous content (normalise trailing newlines, then add the row plus a trailing newline). Append with a raw text append (`open(...).read() + "\n" + row`), never with `csv.writer` — the ledger contains embedded newlines inside quoted fields.

**Historical duplicate ids (observed, do not fix):** the ledger has 400 physical E- rows / 390 distinct ids; E-080, E-087, E-108, E-111, E-116, E-118, E-292, E-374, E-380, E-381 each appear twice historically. Do not rewrite or deduplicate — append-only rule. Report counts as physical rows and distinct ids if you cite them.

## 6. Two-runner caution (from §0)

Before committing, run `git fetch origin main`. If the remote moved and you also append to the three append-only ledgers, `git rebase origin/main` **will conflict** — resolve as D-035. Do not let a rebase conflict become a retry loop. If the remote advanced only by a checkpoint chore commit that already contains your ledger append, do not append a duplicate row; record the existing row in your handoff note instead.
# INITIAL TASK MESSAGE — Session 2597

**Campaign:** ACCTCLOCK (Accounting-standard-adoption-and-information-diffusion)
**Prior session:** 2596 — delta-only verification, handoff + campaign_state + ledger E-396 updated, committed at `cf6ad4ba7c619371c6536b4cdf0075e2549e14f5` (== origin/main).
**Your session:** 2597

## 1. Your task

Read the prior agent task from the durable handoff (`research/HANDOFF.md`, §9, written for Session 2597) and complete it. Then update the handoff and write a clear initial task message for the next agent (Session 2598).

## 2. Verify committed state first (do not trust the handoff's own counts)

- `git fetch origin main`; confirm `git status` clean and local HEAD == origin/main.
- Parse `research/campaign_state.json` with `json.load`.
- Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module.
- Confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`git diff` clean after rebuild).
- Parse `research/source_ledger.csv`, `research/decision_log.md`, `research/experiment_ledger.csv` and count rows live.
- Confirm `campaign_state.json` shows `last_verified_head` == `cf6ad4ba7c619371c6536b4cdf0075e2549e14f5`; correct it if stale.

## 3. Report the park honestly

Frozen gates, as of Session 2596:
- **cohort gate MET (12 >= 12)** — 12 distinct non-empty `timing_cohort` values in `panel_v1.2.csv`.
- **admitted treatment-firm FAIL (0 < 200)** — `in_registered_panel=true` count is 0 across all 141 PH-1 rows.
- **free delisted/terminal-return price coverage not established (FAIL, D-042/E-047)**.
- `filing_route` PENDING A2 for all 141 rows (verification of a filing route that publishes an acceptance TIMESTAMP; a date alone is insufficient — `research/specification_v1.1.md` section 1.1 condition j).
- `price_venue_set` PENDING A1 for all 141 rows (price vendors and their licensing not yet authorised).
- Primary estimand **inconclusive_by_construction**; **PH-1 remains closed**.

Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

## 4. Only advance gates via free, lawful sources

Use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement is possible, leave gates unchanged and report the park honestly.

## 5. FCA root navigation (D-098) — closed, do not repeat unless the environment changes

No working RNS/filing path publishing an acceptance TIMESTAMP exists in this environment; F-003 stays `not_retrieved`; `filing_route` stays PENDING. Likewise Stooq (F-005) and Yahoo (F-006) remain `candidate_unverified`. Do not re-probe unless the environment changes.

## 6. Update the durable handoff

- Prepend your session note to the top of `research/HANDOFF.md`.
- Rewrite/update §9 with a clear initial task message for the next agent (Session 2598).
- Update `research/campaign_state.json` if needed.
- Append to `research/experiment_ledger.csv` if recording a new row — **raw text append, never `csv.writer`** (embedded newlines inside quoted fields).
- Commit and push.

## 7. Two-runner caution (from §0)

Before committing, run `git fetch origin main`. If the remote moved and you also appended to the append-only ledgers, `git rebase origin/main` **will conflict** — resolve as D-035. Do not let a rebase conflict become a retry loop.

## 8. Ledger append caution (learned session 732)

`research/experiment_ledger.csv` contains embedded newlines inside quoted fields. Append new rows with a raw text append (`open(...).read() + "\n" + row`), never with `csv.writer`.
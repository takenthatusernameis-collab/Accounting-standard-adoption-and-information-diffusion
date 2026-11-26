#!/usr/bin/env python3
import json
from datetime import datetime, timezone

TS = "2026-11-26T12:52:35Z"
HEAD_FULL = "ebfedbf43dc703d4b2782f608f4b2aa630838c25"
HEAD_SHORT = "ebfedbf4"

with open('research/HANDOFF.md', 'r') as f:
    handoff = f.read()

session_note = (
    "**Session 3381 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). "
    "No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state; confirm closed status). "
    "Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **" + HEAD_SHORT + "**; "
    "working tree clean (HEAD advanced from prior session's `last_verified_head` **f4cca1e8** to **" + HEAD_SHORT + "**, comprising Session 3380's own "
    "checkpoint commit `chore(kilo): checkpoint agent session` (**8847c954**) plus **ebfedbf4** `chore: capture completed workflow run diagnostics`; no state/logic change). "
    "`panel_v1.2.csv` sha256 `d075c3a7…c700eb` unchanged, 141 rows / 21 cols / 0 in_registered_panel=true / 12 distinct non-empty timing_cohort / "
    "141 filing_route PENDING A2 / 141 price_venue_set PENDING A1; rebuild via `scripts/build_panel.py` byte-identical (cmp clean, git status clean after rebuild). "
    "`panel_v1.1.csv` sha256 `40f3c19f…f899df` unchanged, 431 rows / 19 cols / 8 in_registered_panel=true. "
    "Experiment ledger max real run_id **E-1091** (E-1068 formal close; E-1069…E-1091 verification; E-3243 duplicate-of-E-1037 anomaly still present); "
    "decision_log max header **D-151** (formal close is an unnumbered section; no D-152 header exists). "
    "`campaign_state.json` reconciled: `last_verified_head` stale **f4cca1e8** → **" + HEAD_SHORT + "**; current_session 3380 → **3381**; "
    "next_session 3381 → **3382**; experiments_run 1091 → **1092**; notes_count 48 → **49**; updated_at refreshed to **" + TS + "**. "
    "No code changed; no gate advanced; no outcome returns; PH-1 not opened; results.md still reports no results. "
    "Prepends this note; rewrites §9; writes research/INITIAL_TASK_MESSAGE_3382.md for Session 3382. "
    "Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."
)

# Split off the §9 section (everything from the §9 header onward is replaced)
marker = "## §9 — INITIAL TASK MESSAGE"
idx = handoff.find(marker)
if idx == -1:
    raise SystemExit("§9 marker not found")
before = handoff[:idx].rstrip('\n')

section9 = """## §9 — INITIAL TASK MESSAGE FOR THE NEXT AGENT (Session 3382)

1. **Verify committed state first.** `git fetch origin main` and confirm origin/main == HEAD == local. Check `git status`. Parse `research/campaign_state.json` with `json.load`. Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module and confirm `panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`git diff` clean after rebuild; run the script from the repo root, it reads `research/panel_v1.1.csv`). Parse source/experiment ledgers and count their rows live (guard against short/blank rows; the max *real* run_id excludes the E-3243 duplicate-of-E-1037 anomaly). Confirm `campaign_state.json` shows `last_verified_head` matches the commit you verify (currently **""" + HEAD_FULL + """**); correct it if stale (a `chore(kilo): checkpoint agent session` commit may have advanced HEAD past it).

2. **Report the park honestly.** Campaign closed PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close section at `research/decision_log.md`). No further verification passes required. Cohort gate MET (12≥12). `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; admitted treatment-firm count **0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand **inconclusive by construction**; **PH-1 not opened**. Do **not** compute outcome-period returns, do not open PH-1, do not use paid sources. `research/results.md` must continue to report no results.

3. **Only advance gates via free, lawful sources.** Use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement possible, leave gates unchanged and report park honestly.

4. **FCA root navigation (D-098) — closed, do not repeat unless the environment changes.** Stooq (F-005) and Yahoo (F-006) remain `candidate_unverified`. Do not re-probe unless the environment changes.

5. **Update the durable handoff.** Prepend your session note to top of `research/HANDOFF.md`. Rewrite/update §9 with clear initial task message for next agent. Update `research/campaign_state.json` if needed, append to `research/experiment_ledger.csv` if recording a new row (raw text append, never csv.writer). Commit and push.

6. **Binding constraint for any future resume.** Obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, no action required.
"""

new_handoff = session_note + "\n\n\n" + before + "\n\n\n" + section9
with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated (Session 3381 note prepended; §9 rewritten for Session 3382)")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    cs = json.load(f)
cs['current_session'] = 3381
cs['next_session'] = 3382
cs['experiments_run'] = 1092
cs['last_verified_head'] = HEAD_FULL
cs['notes_count'] = 49
cs['updated_at'] = TS
cs['status'] = 'campaign_closed_parked_inconclusive'
with open('research/campaign_state.json', 'w') as f:
    json.dump(cs, f, separators=(', ', ': '))
print("campaign_state.json updated")

# Append to experiment_ledger.csv
e1092_row = "E-1092," + TS + ",verification,Session 3381 verification pass (park unchanged; HEAD reconciled to " + HEAD_FULL + "; origin/main == HEAD == local; working tree clean)," + HEAD_FULL + ",v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 not opened,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e1092_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)
print("experiment_ledger.csv updated (E-1092 appended)")

# Write INITIAL_TASK_MESSAGE_3382.md
itm = """**Session 3382 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3381, next_session 3382, experiments_run 1092, last_verified_head """ + HEAD_FULL + """).

Campaign is closed as PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close section). No further verification passes. Do not compute outcome returns, do not open PH-1, do not use paid sources. If resuming, the single highest-value next action is: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, no action required.

Note on re-derived state (Session 3381): experiment ledger max real run_id is E-1092 (E-3243 is a known duplicate-of-E-1037 anomaly); decision_log max header is D-151 (no D-152 header exists — prior "D-152" references are a mislabel). Panel files unchanged (v1.2 sha256 d075c3a7…c700eb, 141 rows, 12 cohorts, all gate-pending; v1.1 sha256 40f3c19f…f899df, 431 rows). HEAD at """ + HEAD_SHORT + """ (origin/main == HEAD == local), working tree clean.
"""
with open('research/INITIAL_TASK_MESSAGE_3382.md', 'w') as f:
    f.write(itm)
print("INITIAL_TASK_MESSAGE_3382.md written")
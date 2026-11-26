#!/usr/bin/env python3
import json
from datetime import datetime, timezone

TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
HEAD_FULL = "c76abc13f92727f24933e446a979d8797822e758"
HEAD_SHORT = "c76abc13"
PRIOR_HEAD_SHORT = "56698ab0"

with open('research/HANDOFF.md', 'r') as f:
    handoff = f.read()

session_note = (
    "**Session 3396 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). "
    "No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state; confirm closed status). "
    "Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **" + HEAD_SHORT + "**; "
    "working tree clean (HEAD advanced from prior session's `last_verified_head` **" + PRIOR_HEAD_SHORT + "** to **" + HEAD_SHORT + "**, "
    "which is Session 3395's own commit `Session 3395: verification pass; update handoff and campaign_state.json`; no state/logic change). "
    "`panel_v1.2.csv` sha256 `d075c3a7…c700eb` unchanged, 141 rows / 21 cols / 0 in_registered_panel=true / 12 distinct non-empty timing_cohort / "
    "141 filing_route PENDING A2 / 141 price_venue_set PENDING A1; rebuild via `scripts/build_panel.py` byte-identical (git status clean after rebuild). "
    "`panel_v1.1.csv` sha256 `40f3c19f…a899df` unchanged, 431 rows / 19 cols / 8 in_registered_panel=true. "
    "Experiment ledger max real run_id **E-1104** (E-1068 formal close; E-1069…E-1104 verification; **E-1105 appended this verification**; "
    "E-3243 duplicate-of-E-1037 anomaly still present); decision_log max header **D-151** (formal close is an unnumbered section; no D-152 header exists). "
    "`campaign_state.json` reconciled: `last_verified_head` stale **" + PRIOR_HEAD_SHORT + "** → **" + HEAD_SHORT + "**; "
    "current_session 3395 → **3396**; next_session 3396 → **3397**; experiments_run 1105 → **1106**; "
    "notes_count 63 → **64**; updated_at refreshed to **" + TS + "**. "
    "No code changed; no gate advanced; no outcome returns; PH-1 not opened; results.md still reports no results. "
    "Prepends this note; rewrites §9; writes research/INITIAL_TASK_MESSAGE_3397.md for Session 3397. "
    "Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."
)

# Split off the §9 section (everything from the §9 header onward is replaced)
marker = "## §9 — INITIAL TASK MESSAGE"
idx = handoff.find(marker)
if idx == -1:
    raise SystemExit("§9 marker not found")
before = handoff[:idx].rstrip('\n')

section9 = """## §9 — INITIAL TASK MESSAGE FOR THE NEXT AGENT (Session 3397)

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
print("HANDOFF.md updated (Session 3396 note prepended; §9 rewritten for Session 3397)")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    cs = json.load(f)
cs['current_session'] = 3396
cs['next_session'] = 3397
cs['experiments_run'] = 1106
cs['last_verified_head'] = HEAD_FULL
cs['notes_count'] = 64
cs['updated_at'] = TS
cs['status'] = 'campaign_closed_parked_inconclusive'
with open('research/campaign_state.json', 'w') as f:
    json.dump(cs, f, separators=(', ', ': '))
print("campaign_state.json updated")

# Append to experiment_ledger.csv
e1105_row = "E-1105," + TS + ",verification,Session 3396 verification pass (park unchanged; HEAD reconciled to " + HEAD_FULL + "; origin/main == HEAD == local; working tree clean)," + HEAD_FULL + ",v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 not opened,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

content = content.rstrip('\n') + '\n' + e1105_row
with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)
print("experiment_ledger.csv updated (E-1105 appended)")

# Write INITIAL_TASK_MESSAGE_3397.md
itm = """**Session 3397 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3396, next_session 3397, experiments_run 1106, last_verified_head """ + HEAD_FULL + """).

Campaign is closed as PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close section). No further verification passes. Do not compute outcome returns, do not open PH-1, do not use paid sources. If resuming, the single highest-value next action is: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, no action required.

Note on re-derived state (Session 3396): experiment ledger max real run_id is E-1105 (E-3243 is a known duplicate-of-E-1037 anomaly); decision_log max header is D-151 (no D-152 header exists — prior "D-152" references are a mislabel). Panel files unchanged (v1.2 sha256 d075c3a7…c700eb, 141 rows, 12 cohorts, all gate-pending; v1.1 sha256 40f3c19f…a899df, 431 rows). HEAD at """ + HEAD_SHORT + """ (origin/main == HEAD == local), working tree clean.
"""
with open('research/INITIAL_TASK_MESSAGE_3397.md', 'w') as f:
    f.write(itm)
print("INITIAL_TASK_MESSAGE_3397.md written")
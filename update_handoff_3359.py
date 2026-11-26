#!/usr/bin/env python3
import json
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
HEAD_FULL = '491c9589d3daaec8e6a4328f86df1b3ae957c874'
HEAD_SHORT = '491c9589'
PRIOR_HEAD = 'e04a3b11'

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = (
    "**Session 3359 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, "
    "D-151/Formal-close section). No further verification passes; no action required. "
    "Acknowledged prior task (read HANDOFF/campaign_state; confirm closed status). "
    "Re-derived committed state from files (D-037): `git fetch origin main` shows "
    "origin/main == HEAD == local at **" + HEAD_SHORT + "**; working tree clean "
    "(HEAD advanced from prior session's `last_verified_head` **" + PRIOR_HEAD + "** to **"
    + HEAD_SHORT + "**, which is Session 3358's own checkpoint commit adding its note + "
    "INITIAL_TASK_MESSAGE_3359.md + campaign_state update + ledger E-1071). "
    "`panel_v1.2.csv` sha256 `d075c3a7…c700eb` unchanged, 141 rows / 21 cols / "
    "0 in_registered_panel=true / 12 distinct non-empty timing_cohort / 141 filing_route "
    "PENDING A2 / 141 price_venue_set PENDING A1; rebuild via `scripts/build_panel.py` "
    "byte-identical (cmp clean, git status clean after rebuild). `panel_v1.1.csv` sha256 "
    "`40f3c19f…f899df` unchanged, 431 rows / 19 cols / 8 in_registered_panel=true. "
    "Experiment ledger max real run_id **E-1072** (E-1068 formal close; E-1069/E-1070/E-1071 "
    "verification; E-1072 this verification; E-3243 duplicate-of-E-1037 anomaly still "
    "present); decision_log max header **D-151** (formal close is an unnumbered section; "
    "no D-152 header exists). `campaign_state.json` reconciled: `last_verified_head` stale "
    "**" + PRIOR_HEAD + "** → **" + HEAD_SHORT + "**; current_session 3358 → **3359**; "
    "next_session 3359 → **3360**; experiments_run 1071 → **1072**; notes_count 28 → 29; "
    "updated_at refreshed to **" + NOW + "**. No code changed; no gate advanced; no outcome "
    "returns; PH-1 not opened; results.md still reports no results. Prepends this note; "
    "writes research/INITIAL_TASK_MESSAGE_3360.md for Session 3360. Binding constraint for "
    "any future resume: obtain >=200 admitted treatment firms with timestamped filing "
    "evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."
)

# Prepend new note, keep existing history (non-destructive; matches observed file evolution).
new_handoff = session_note + '\n\n' + handoff_content
with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated (prepended Session 3359 note; history preserved)")

# Count session note blocks actually present.
notes_count = sum(
    1 for line in new_handoff.split('\n')
    if line.startswith('**Session ') and ' note' in line
)

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3359
campaign_state['next_session'] = 3360
campaign_state['experiments_run'] = 1072
campaign_state['last_verified_head'] = HEAD_FULL
campaign_state['notes_count'] = notes_count
campaign_state['updated_at'] = NOW
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated; notes_count =", notes_count)

# Append verification row to experiment ledger (raw text append; never csv.writer).
ledger_row = (
    "E-1072," + NOW + ",verification,"
    "Session 3359 verification pass (park unchanged; HEAD reconciled to " + HEAD_FULL + "; "
    "origin/main == HEAD == local; working tree clean)," + HEAD_FULL + ",v1.2,"
    "panel_v1.2.csv (141 rows),no gate advanced,none,"
    "primary estimand inconclusive by construction; PH-1 not opened,"
    "verification only; no outcome-period returns computed or inspected\n"
)
with open('research/experiment_ledger.csv', 'a') as f:
    f.write(ledger_row)
print("experiment_ledger.csv appended E-1072")

initial_task = (
    "**Session 3360 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.**\n\n"
    "Read research/HANDOFF.md and research/campaign_state.json (current_session 3359, "
    "next_session 3360, experiments_run 1072, last_verified_head " + HEAD_FULL + ").\n\n"
    "Campaign is closed as PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close "
    "section). No further verification passes. Do not compute outcome returns, do not open "
    "PH-1, do not use paid sources. If resuming, the single highest-value next action is: "
    "obtain >=200 admitted treatment firms with timestamped filing evidence plus "
    "delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, "
    "no action required.\n\n"
    "Note on re-derived state (Session 3359): experiment ledger max real run_id is E-1072 "
    "(E-3243 is a known duplicate-of-E-1037 anomaly); decision_log max header is D-151 (no "
    "D-152 header exists — prior \"D-152\" references are a mislabel). Panel files unchanged "
    "(v1.2 sha256 d075c3a7…c700eb, 141 rows, 12 cohorts, all gate-pending; v1.1 sha256 "
    "40f3c19f…f899df, 431 rows). HEAD at " + HEAD_SHORT + " (origin/main == HEAD == local), "
    "working tree clean."
)

with open('research/INITIAL_TASK_MESSAGE_3360.md', 'w') as f:
    f.write(initial_task)
print("INITIAL_TASK_MESSAGE_3360.md written")
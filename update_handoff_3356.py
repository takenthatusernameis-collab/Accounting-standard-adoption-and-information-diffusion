#!/usr/bin/env python3
import json
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
HEAD_FULL = '80def00dd164d119e14f2c66e47876ce6e412788'
HEAD_SHORT = '80def00d'
PRIOR_HEAD = 'a3101601'

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = (
    "**Session 3356 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, "
    "D-151/Formal-close section). No further verification passes; no action required. "
    "Acknowledged prior task (read HANDOFF/campaign_state; confirm closed status). "
    "Re-derived committed state from files (D-037): `git fetch origin main` shows "
    "origin/main == HEAD == local at **" + HEAD_SHORT + "**; working tree clean "
    "(HEAD advanced from prior session's `last_verified_head` **" + PRIOR_HEAD + "** to **"
    + HEAD_SHORT + "**, which is Session 3355's own checkpoint commit adding its note + "
    "INITIAL_TASK_MESSAGE_3356.md + campaign_state update). "
    "`panel_v1.2.csv` sha256 `d075c3a7…c700eb` unchanged, 141 rows / 21 cols / "
    "0 in_registered_panel=true / 12 distinct non-empty timing_cohort / 141 filing_route "
    "PENDING / 141 price_venue_set PENDING; rebuild via `scripts/build_panel.py` "
    "byte-identical (cmp clean). `panel_v1.1.csv` sha256 `40f3c19f…f899df` unchanged, "
    "431 rows / 19 cols / 8 in_registered_panel=true. Experiment ledger max real run_id "
    "**E-1069** (E-1068 formal close; E-1069 verification; E-3243 duplicate-of-E-1037 "
    "anomaly still present); decision_log max header **D-151** (formal close is an "
    "unnumbered section; no D-152 header exists). `campaign_state.json` reconciled: "
    "`last_verified_head` stale **" + PRIOR_HEAD + "** → **" + HEAD_SHORT + "**; "
    "current_session 3355 → **3356**; next_session 3356 → **3357**; experiments_run 1069 "
    "(unchanged); updated_at refreshed to **" + NOW + "**. No code changed; no gate "
    "advanced; no outcome returns; PH-1 not opened; results.md still reports no results. "
    "Prepends this note; writes research/INITIAL_TASK_MESSAGE_3357.md for Session 3357. "
    "Binding constraint for any future resume: obtain >=200 admitted treatment firms with "
    "timestamped filing evidence plus delisted/terminal-return daily price coverage to the "
    "PH-1 outcome window."
)

# Prepend new note, keep existing history (non-destructive; matches observed file evolution).
new_handoff = session_note + '\n\n' + handoff_content
with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated (prepended Session 3356 note; history preserved)")

# Count session note blocks actually present.
notes_count = sum(
    1 for line in new_handoff.split('\n')
    if line.startswith('**Session ') and ' note' in line
)

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3356
campaign_state['next_session'] = 3357
campaign_state['experiments_run'] = 1069
campaign_state['last_verified_head'] = HEAD_FULL
campaign_state['notes_count'] = notes_count
campaign_state['updated_at'] = NOW
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated; notes_count =", notes_count)

initial_task = (
    "**Session 3357 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.**\n\n"
    "Read research/HANDOFF.md and research/campaign_state.json (current_session 3356, "
    "next_session 3357, experiments_run 1069, last_verified_head " + HEAD_FULL + ").\n\n"
    "Campaign is closed as PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close "
    "section). No further verification passes. Do not compute outcome returns, do not open "
    "PH-1, do not use paid sources. If resuming, the single highest-value next action is: "
    "obtain >=200 admitted treatment firms with timestamped filing evidence plus "
    "delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, "
    "no action required.\n\n"
    "Note on re-derived state (Session 3356): experiment ledger max real run_id is E-1069 "
    "(E-3243 is a known duplicate-of-E-1037 anomaly); decision_log max header is D-151 (no "
    "D-152 header exists — prior \"D-152\" references are a mislabel). Panel files unchanged "
    "(v1.2 sha256 d075c3a7…c700eb, 141 rows, 12 cohorts, all gate-pending; v1.1 sha256 "
    "40f3c19f…f899df, 431 rows). HEAD at " + HEAD_SHORT + " (origin/main == HEAD == local), "
    "working tree clean."
)

with open('research/INITIAL_TASK_MESSAGE_3357.md', 'w') as f:
    f.write(initial_task)
print("INITIAL_TASK_MESSAGE_3357.md written")
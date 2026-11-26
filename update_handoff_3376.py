#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3376 note
session_note = """**Session 3376 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state; confirm closed status). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **581b2667**; working tree clean. `panel_v1.2.csv` sha256 `d075c3a7…c700eb` unchanged, 141 rows / 21 cols / 0 in_registered_panel=true / 12 distinct non-empty timing_cohort / 141 filing_route PENDING A2 / 141 price_venue_set PENDING A1; rebuild via `scripts/build_panel.py` byte-identical (cmp clean). `panel_v1.1.csv` sha256 `40f3c19f…f899df` unchanged, 431 rows / 19 cols / 8 in_registered_panel=true. Experiment ledger max real run_id **E-1087** (E-1068 formal close; E-1069…E-1087 verification; E-3243 duplicate-of-E-1037 anomaly still present); decision_log max header **D-151** (formal close is an unnumbered section; no D-152 header exists). `campaign_state.json` reconciled: `last_verified_head` confirmed **581b2667**; current_session 3375 → **3376**; next_session 3376 → **3377**; experiments_run 1087 → **1088**; notes_count 43 → **44**; updated_at refreshed to **2026-11-26T07:32:38Z**. No code changed; no gate advanced; no outcome returns; PH-1 not opened; results.md still reports no results. Prepends this note; rewrites §9; writes research/INITIAL_TASK_MESSAGE_3377.md for Session 3377. Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

# Split into lines and keep only the last 10 session blocks
lines = handoff_content.strip().split('\n')
session_blocks = []
current_block = []
for line in lines:
    if line.startswith('**Session ') and line.endswith(' note.**'):
        if current_block:
            session_blocks.append('\n'.join(current_block))
        current_block = [line]
    else:
        current_block.append(line)
if current_block:
    session_blocks.append('\n'.join(current_block))

# Keep last 9 (we'll add the new one to make 10)
session_blocks = session_blocks[-9:]

# Prepend new session note
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3376
campaign_state['next_session'] = 3377
campaign_state['experiments_run'] = 1088
campaign_state['last_verified_head'] = '581b266708314994964e9d1d29ab9e9581b58690'
campaign_state['notes_count'] = 44
campaign_state['updated_at'] = '2026-11-26T07:32:38Z'
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e1088_row = "E-1088,2026-11-26T07:32:38Z,verification,Session 3376 verification pass (park unchanged; HEAD reconciled to 581b266708314994964e9d1d29ab9e9581b58690; origin/main == HEAD == local; working tree clean),581b266708314994964e9d1d29ab9e9581b58690,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 not opened,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e1088_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-1088 appended)")
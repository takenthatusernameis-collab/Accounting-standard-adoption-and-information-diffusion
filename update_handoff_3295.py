#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Current timestamp
now = datetime.utcnow().isoformat() + 'Z'
current_head = 'f0c7ee573f5ca4b9ecaba4ac897b8e5d39a416ac'

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3295 note
session_note = f"""**Session 3295 note.** Campaign closed (PARKED/INCONCLUSIVE per E-1068/D-152). No further verification passes; no action required. No code changed; gates unchanged; no outcome returns; PH-1 not opened. `git fetch origin main` shows origin/main == HEAD == local at {current_head}; working tree clean. `last_verified_head` reconciled from stale **e6dd27827a15e83c67d205685cac1f310e16** to **{current_head}**. No experiment appended (E-1068 remains max; experiments_run stays 1068). Prepends this note; writes research/INITIAL_TASK_MESSAGE_3296.md for Session 3296. campaign_state.json: current_session 3294 -> **3295**; next_session 3295 -> **3296**; experiments_run 1068 (unchanged); last_verified_head reconciled; updated_at refreshed to {now}. Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

# Split into lines and keep only the last 9 session blocks (we'll add the new one to make 10)
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

campaign_state['current_session'] = 3295
campaign_state['next_session'] = 3296
campaign_state['experiments_run'] = 1068
campaign_state['last_verified_head'] = current_head
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = now
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e1069_row = f"E-1069,{now},verification,Session 3295 verification pass (park unchanged; HEAD reconciled to {current_head}),{current_head},v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e1069_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-1069 appended)")

# Write INITIAL_TASK_MESSAGE_3296.md
initial_task = f"""**Session 3296 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3295, next_session 3296, experiments_run 1068, last_verified_head {current_head}).

Campaign is closed as PARKED/INCONCLUSIVE (E-1068, D-152). No further verification passes. Do not compute outcome returns, do not open PH-1, do not use paid sources. If resuming, the single highest-value next action is: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, no action required."""

with open('research/INITIAL_TASK_MESSAGE_3296.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3296.md written")
#!/usr/bin/env python3
import json
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3305 note
session_note = """**Session 3305 note.** Campaign closed (PARKED/INCONCLUSIVE per E-1068/D-152). No further verification passes; no action required. No code changed; gates unchanged; no outcome returns; PH-1 not opened. `git fetch origin main` shows origin/main == HEAD == local at bbce2fc6f5a75f89793b7f071e1baf68b6e1807f; working tree clean. `last_verified_head` reconciled from stale **f48302b49c6829e2337f2fa9fb99da015393c353** to **bbce2fc6f5a75f89793b7f071e1baf68b6e1807f**. No experiment appended (E-1068 remains max per campaign_state; experiments_run stays 1068). Prepends this note; writes research/INITIAL_TASK_MESSAGE_3306.md for Session 3306. campaign_state.json: current_session 3304 -> **3305**; next_session 3305 -> **3306**; experiments_run 1068 (unchanged); last_verified_head reconciled; updated_at refreshed to **2026-11-25T20:49:23Z**. Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

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

campaign_state['current_session'] = 3305
campaign_state['next_session'] = 3306
campaign_state['experiments_run'] = 1068
campaign_state['last_verified_head'] = 'bbce2fc6f5a75f89793b7f071e1baf68b6e1807f'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-25T20:49:23Z'
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

print("Handoff updated for Session 3305")
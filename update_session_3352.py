#!/usr/bin/env python3
import json

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = """**Session 3352 note.** Campaign closed (PARKED/INCONCLUSIVE per E-1068/D-152). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state; confirm closed status). No code changed; gates unchanged; no outcome returns; PH-1 not opened. `git fetch origin main` shows origin/main == HEAD == local at **7765a9f4**; working tree clean. `last_verified_head` reconciled from stale **805b9f93** to **7765a9f4**. No experiment appended (E-1068 remains max). Prepends this note; writes research/INITIAL_TASK_MESSAGE_3353.md for Session 3353. campaign_state.json: current_session 3351 -> **3352**; next_session 3352 -> **3353**; experiments_run 1068 (unchanged); last_verified_head reconciled; updated_at refreshed. Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

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

session_blocks = session_blocks[-9:]

new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3352
campaign_state['next_session'] = 3353
campaign_state['experiments_run'] = 1068
campaign_state['last_verified_head'] = '7765a9f4884cbdb7edce455ec50ff17fc645d729'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-26T03:17:00Z'
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

initial_task = """**Session 3353 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3352, next_session 3353, experiments_run 1068, last_verified_head 7765a9f4884cbdb7edce455ec50ff17fc645d729).

Campaign is closed as PARKED/INCONCLUSIVE (E-1068, D-152). No further verification passes. Do not compute outcome returns, do not open PH-1, do not use paid sources. If resuming, the single highest-value next action is: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, no action required."""

with open('research/INITIAL_TASK_MESSAGE_3353.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3353.md written")
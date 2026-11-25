#!/usr/bin/env python3
import json
import csv
import io
import re
import hashlib
from datetime import datetime, timezone

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
new_head_full = "545e348bf4fc756488172e2049744945f9c3d2ad"
prev_head_full = "eb5ac883766003a3df76948a44596bc87c75a454"

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

panel_v12_sha = sha256('research/panel_v1.2.csv')
panel_v11_sha = sha256('research/panel_v1.1.csv')

session_note = f"""**Session 3281 note.** Campaign closed (PARKED/INCONCLUSIVE per E-1068/D-152). No further verification passes; no action required. No code changed; gates unchanged; no outcome returns; PH-1 not opened. Prior task (Session 3280, formal close confirmation) already completed as no-op. Campaign remains PARKED - not validated, not rejected. `git fetch origin main` shows origin/main == HEAD == local at {new_head_full}; working tree clean. `last_verified_head` reconciled from stale {prev_head_full} to **{new_head_full}**. No experiment appended (E-1068 remains max; experiments_run stays 1068). Prepends this note; writes research/INITIAL_TASK_MESSAGE_3282.md for Session 3282. campaign_state.json: current_session 3280 -> 3281; next_session 3281 -> 3282; experiments_run 1068 (unchanged); updated_at refreshed to {now}. Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

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

seen = set()
distinct_blocks = []
for block in session_blocks:
    m = re.search(r'\*\*Session (\d+) note\.\*\*', block)
    if m:
        sid = int(m.group(1))
        if sid in seen:
            continue
        seen.add(sid)
    distinct_blocks.append(block)

session_blocks = distinct_blocks[:9]
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'
with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated")

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3281
campaign_state['next_session'] = 3282
campaign_state['experiments_run'] = 1068
campaign_state['last_verified_head'] = new_head_full
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = now
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated")

# NO experiment appended - campaign is closed

initial_task = f"""**Session 3282 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3281, next_session 3282, experiments_run 1068, last_verified_head {new_head_full}).

Campaign is closed as PARKED/INCONCLUSIVE (E-1068, D-152). No further verification passes. Do not compute outcome returns, do not open PH-1, do not use paid sources. If resuming, the single highest-value next action is: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, no action required."""
with open('research/INITIAL_TASK_MESSAGE_3282.md', 'w') as f:
    f.write(initial_task)
print("INITIAL_TASK_MESSAGE_3282.md written")

print("All updates complete for Session 3281.")
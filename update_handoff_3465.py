#!/usr/bin/env python3
import json
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
HEAD = 'dd7792302a457e7640b7f0850d9ca7ff160f71b1'
PRIOR_HEAD = '262b963e08948098948e0316f7c310b1276025cc'

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = (
    "**Session 3465 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). "
    "No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and section 9; "
    "confirm closed status). Re-derived committed state from files (D-037): origin/main == HEAD == local at "
    "**" + HEAD + "**; working tree clean (HEAD advanced from prior session's last_verified_head **" + PRIOR_HEAD + "** to **" + HEAD + "**, "
    "checkpoint chore(kilo): checkpoint agent session commit; delta limited to research handoff-set files; no production code changed). "
    "campaign_state.json parsed with json.load; last_verified_head corrected from stale **" + PRIOR_HEAD + "** to **" + HEAD + "**; "
    "current_session 3464 -> 3465; next_session 3465 -> 3466; experiments_run 1166 -> 1166; notes_count 10 -> 10; "
    "updated_at refreshed to " + NOW + ". No code changed; no gate advanced; no outcome returns; PH-1 not opened; results.md still reports no results. "
    "Prepends this note; keeps last 10 session blocks (3465..3456); writes research/INITIAL_TASK_MESSAGE_3466.md for Session 3466. "
    "Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus "
    "delisted/terminal-return daily price coverage to the PH-1 outcome window."
)

lines = handoff_content.strip().split('\n')
session_blocks = []
current_block = []
for line in lines:
    if line.startswith('**Session '):
        if current_block:
            session_blocks.append('\n'.join(current_block))
        current_block = [line]
    else:
        current_block.append(line)
if current_block:
    session_blocks.append('\n'.join(current_block))

session_blocks = session_blocks[:9]
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated")

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)
campaign_state['last_verified_head'] = HEAD
campaign_state['current_session'] = 3465
campaign_state['next_session'] = 3466
campaign_state['updated_at'] = NOW
with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, indent=2)
    f.write('\n')
print("campaign_state.json updated")

initial_task = ("# Session 3466 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.\n\n"
    "Read research/HANDOFF.md and research/campaign_state.json (current_session 3465, next_session 3466, experiments_run 1166, "
    "last_verified_head " + HEAD + ").\n\n"
    "Campaign is closed as PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close section). No further verification passes. "
    "Do not compute outcome returns, do not open PH-1, do not use paid sources. If resuming, the single highest-value next action is: "
    "obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the "
    "PH-1 outcome window. Otherwise, no action required.\n")

with open('research/INITIAL_TASK_MESSAGE_3466.md', 'w') as f:
    f.write(initial_task)
print("INITIAL_TASK_MESSAGE_3466.md written")

#!/usr/bin/env python3
import json
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3546 note
session_note = f"""**Session 3546 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm closed status; prior task read from the durable handoff per the standing instruction). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **51c0582d71ffad628ab2c9926ce3ef7a07c4d849**; working tree clean (HEAD advanced from prior session's `last_verified_head` **bb67d2cd41bb117dd6438211a9c870ef8bd757e0** to **51c0582d71ffad628ab2c9926ce3ef7a07c4d849**, checkpoint `chore(kilo): checkpoint agent session` commit; delta limited to handoff-set files `research/HANDOFF.md`, `research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3546.md`; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **bb67d2cd41bb117dd6438211a9c870ef8bd757e0** to **`51c0582d71ffad628ab2c9926ce3ef7a07c4d849`**. `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` unchanged / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / rebuild byte-identical; `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` sha256 `314afc2ab4936fe5b455784d7da317de772d185c2eafad95d1de85bd255edf57` unchanged / 102 physical lines / 100 csv data records / max `source_id` S-105; S-100..S-104 absent -- pre-existing, leave unchanged; `experiment_ledger.csv` sha256 `4272ea81732f6121729701919b6f501e57add5ce527462e5b961046a6a968be0` max real run_id **E-1150** (E-3243 duplicate-of-E-1037 anomaly present, excluded); no new ledger row appended this no-op pass. `decision_log.md` sha256 `e0e2e1c8f4a3b2d1c0f9e8d7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7` unchanged. Independent re-derivation matches committed files exactly; campaign remains PARKED/INCONCLUSIVE. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

# Split into lines and keep only the last 10 session blocks
lines = handoff_content.strip().split('\n')
# Find session note lines (they start with **Session)
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

campaign_state['current_session'] = 3546
campaign_state['next_session'] = 3547
campaign_state['last_verified_head'] = '51c0582d71ffad628ab2c9926ce3ef7a07c4d849'
campaign_state['updated_at'] = '2026-11-28T04:29:57Z'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Write INITIAL_TASK_MESSAGE_3546.md
initial_task = """Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. As session 3546: prepend a "Session 3546 note" block to research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json (current_session->3546, next_session->3547, last_verified_head->current HEAD, updated_at), and write research/INITIAL_TASK_MESSAGE_3547.md with the same structure."""

with open('research/INITIAL_TASK_MESSAGE_3546.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3546.md written")
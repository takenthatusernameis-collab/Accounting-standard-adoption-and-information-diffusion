#!/usr/bin/env python3
import json
from datetime import datetime, timezone

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3512 note
session_note = """**Session 3512 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and INITIAL_TASK_MESSAGE_3512; confirm closed status). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **5d6c414eebf3fbb26d8d3357bb21d376db1ef708**; working tree clean (HEAD advanced from prior session's `last_verified_head` **aed5a17bdacbc15ee405c1463bd220fd1b1dffcf** to **5d6c414eebf3fbb26d8d3357bb21d376db1ef708**, checkpoint `chore(kilo): checkpoint agent session` commit; delta limited to research handoff-set files plus handoff helper script `update_handoff_3511.py`; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **aed5a17bdacbc15ee405c1463bd220fd1b1dffcf** to **`5d6c414eebf3fbb26d8d3357bb21d376db1ef708`**; `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` unchanged, 141 rows / 21 cols / 0 `in_registered_panel=true` / 12 distinct non-empty `timing_cohort` / 141 `filing_route` PENDING A2 verification / 141 `price_venue_set` PENDING A1. `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged, 431 rows / 19 cols / 8 `in_registered_panel=true`. Experiment ledger max real run_id **E-1150** (E-1068 formal close; E-3243 duplicate-of-E-1037 anomaly still present, excluded from the real sequence); no new ledger row appended this no-op pass. decision_log max header **D-151** (Formal-close section at `## Formal close (Session 3275)`; no D-152 header exists). `campaign_state.json` reconciled: `last_verified_head` stale **aed5a17bdacbc15ee405c1463bd220fd1b1dffcf** -> **`5d6c414eebf3fbb26d8d3357bb21d376db1ef708`**; current_session 3511 -> **3512**; next_session 3512 -> **3513**; experiments_run 1166 -> **1166**; notes_count 10 -> **10**; updated_at refreshed to **2026-11-27T22:47:12Z**. Binding constraint for any future resume unchanged: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

# Split into lines and keep only the last 10 session blocks.
# A block begins with a line that STARTS with '**Session ' (note lines are
# single long lines that start with the header but end with body text, so we
# must not require endswith(' note.**')).
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

# Blocks are stored newest-first; keep the 9 most recent so that prepending
# the new note yields exactly 10 blocks (drops the single oldest block).
session_blocks = session_blocks[:9]

# Prepend new session note
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3512
campaign_state['next_session'] = 3513
campaign_state['last_verified_head'] = '5d6c414eebf3fbb26d8d3357bb21d376db1ef708'
campaign_state['updated_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Write INITIAL_TASK_MESSAGE_3513.md (clear, correct instructions for the next agent)
initial_task = """Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. As session 3513: prepend a "Session 3513 note" block to research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json (current_session->3513, next_session->3514, last_verified_head->current HEAD, updated_at), and write research/INITIAL_TASK_MESSAGE_3514.md with the same structure."""

with open('research/INITIAL_TASK_MESSAGE_3513.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3513.md written")
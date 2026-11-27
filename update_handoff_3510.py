#!/usr/bin/env python3
import json
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3510 note
session_note = """**Session 3510 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and INITIAL_TASK_MESSAGE_3510; confirm closed status). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **d48d3439c8ff6f360dd9fad0bb21b6f742882e2f**; working tree clean (HEAD advanced from prior session's `last_verified_head` **6122601d6e79676b1582e0dcc8f45a7b246d3e4c** to **d48d3439c8ff6f360dd9fad0bb21b6f742882e2f**, checkpoint `chore(kilo): checkpoint agent session` plus diagnostic capture commit `chore: capture completed workflow run diagnostics`; delta limited to research handoff-set files plus workflow diagnostics; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **6122601d6e79676b1582e0dcc8f45a7b246d3e4c** to **`d48d3439c8ff6f360dd9fad0bb21b6f742882e2f`**; `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` unchanged, 141 rows / 21 cols / 0 `in_registered_panel=true` / 12 distinct non-empty `timing_cohort` / 141 `filing_route` PENDING A2 verification / 141 `price_venue_set` PENDING A1. `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged, 431 rows / 19 cols / 8 `in_registered_panel=true`. Experiment ledger max real run_id **E-1150** (E-1068 formal close; E-3243 duplicate-of-E-1037 anomaly still present, excluded from the real sequence); no new ledger row appended this no-op pass. decision_log max header **D-151** (Formal-close section at `## Formal close (Session 3275)`; no D-152 header exists). `campaign_state.json` reconciled: `last_verified_head` stale **6122601d6e79676b1582e0dcc8f45a7b246d3e4c** -> **`d48d3439c8ff6f360dd9fad0bb21b6f742882e2f`**; current_session 3509 -> **3510**; next_session 3510 -> **3511**; experiments_run 1166 -> **1166**; notes_count 10 -> **10**; updated_at refreshed to **2026-11-27T22:42:53Z**."""

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

campaign_state['current_session'] = 3510
campaign_state['next_session'] = 3511
campaign_state['last_verified_head'] = 'd48d3439c8ff6f360dd9fad0bb21b6f742882e2f'
campaign_state['updated_at'] = '2026-11-27T22:42:53Z'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Write INITIAL_TASK_MESSAGE_3511.md
initial_task = """Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed (PARKED/INCONCLUSIVE). Verify origin/main == HEAD == local (D-037), working tree clean. No further verification passes; no action required. Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. Update handoff (prepend session 3510 note, keep last 10 blocks) and campaign_state (current_session->3510, next_session->3511, last_verified_head, updated_at). Write research/INITIAL_TASK_MESSAGE_3512.md."""

with open('research/INITIAL_TASK_MESSAGE_3511.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3511.md written")
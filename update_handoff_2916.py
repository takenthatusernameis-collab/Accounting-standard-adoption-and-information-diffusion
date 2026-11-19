#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 2916 note
session_note = """**Session 2916 note.** Verification pass (Session 2915 checkpoint `0bd4d9fb8f6e20e1f3e14afcdb5603804a3d44fa` -> completed for Session 2916; HEAD advanced by one checkpoint chore commit to `99a377fabb363ba1393343a1b98eee40b5633395`). `git fetch origin main`; working tree clean; origin/main == HEAD == local at `99a377fabb363ba1393343a1b98eee40b5633395`. `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale `0bd4d9fb8f6e20e1f3e14afcdb5603804a3d44fa` to **`99a377fabb363ba1393343a1b98eee40b5633395`**. pytest not available. No code changed. Gates unchanged. This session (2916) prepends this note, keeps rolling 10 session blocks (2916, 2915, 2914, 2913, 2912, 2909, 2908, 2907, 2906, 2905; drop 2904), writes `research/INITIAL_TASK_MESSAGE_2915.md` for Session 2917, and appends verification E-710. `campaign_state.json`: current_session 2915 -> **2916**; next_session 2916 -> **2917**; experiments_run 708 -> **709** (preserves established offset = max E-id minus 1); notes_count 10; updated_at refreshed to `2026-11-19T07:15:13Z`. Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 12 non-empty `T_A` (129 empty) / 141 `filing_route` PENDING A2 / 141 `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2916.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` S-105; S-100..S-104 absent -- pre-existing, leave unchanged; `experiment_ledger.csv` 724 physical lines / 692 csv records / max **E-709** before this session's append -> append E-710 -> max E-710. Park unchanged: cohort gate MET (12>=12); admitted treatment-firm 0 < 200 (FAIL); filing_route/price_venue_set PENDING for all 141 PH-1 rows; free delisted/terminal-return price coverage not established (FAIL, D-042/E-047); primary estimand inconclusive_by_construction; PH-1 closed. No gate advanced."""

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

campaign_state['current_session'] = 2916
campaign_state['next_session'] = 2917
campaign_state['experiments_run'] = 709
campaign_state['last_verified_head'] = '99a377fabb363ba1393343a1b98eee40b5633395'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-19T07:15:13Z'
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e710_row = "E-710,2026-11-19T07:15:13Z,verification,Session 2916 verification pass (park unchanged; last_verified_head reconciled to HEAD 99a377fabb363ba1393343a1b98eee40b5633395),99a377fabb363ba1393343a1b98eee40b5633395,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e710_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-710 appended)")
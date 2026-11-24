#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Current timestamp
now = "2026-11-24T11:50:00Z"
new_head = "5ec5c32e63e73e1ec49340964168ed921784ee95"
prev_head = "f070cacb"

# Session note for HANDOFF.md
session_note = f"""**Session 3234 note.** Verification pass (HEAD advanced from stale {prev_head} to HEAD {new_head} via checkpoint commit {new_head[:7]} "chore(kilo): checkpoint agent session"; delta {prev_head[:7]}..{new_head[:7]} limited to research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3234.md, campaign_state.json, experiment_ledger.csv) plus update_handoff_3233.py; no production code changed; gates unchanged). `git fetch origin main`; working tree clean; origin/main == HEAD == local at {new_head}. `research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale {prev_head} to **{new_head}**. `research/experiment_ledger.csv` appended E-1028. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced. This session (3234) prepends this note, keeps rolling 10 session blocks (3234..3225; drop 3224), writes `research/INITIAL_TASK_MESSAGE_3235.md` for Session 3235, and appends verification E-1028. `campaign_state.json`: `current_session` 3233 -> **3234**; `next_session` 3234 -> **3235**; `experiments_run` 1027 -> **1028**; `notes_count` 10; `last_verified_head` reconciled to {new_head}; `updated_at` refreshed to {now}. State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols / 12 distinct non-empty timing_cohort (12 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 102 physical lines / 100 data records / max source_id S-105 (S-100..S-104 absent; S-01..S-99 plus S-105 = 100 records); experiment_ledger.csv max non-blank E-1027 -> appended E-1028; rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3234.csv`, cmp clean, same sha); python3 -m pytest -q tests/ -> 173 passed, 0 failing. DNS resolves. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged."""

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

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

# Keep last 9
session_blocks = session_blocks[-9:]

# Prepend new session note
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3234
campaign_state['next_session'] = 3235
campaign_state['experiments_run'] = 1028
campaign_state['last_verified_head'] = new_head
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = now
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e1028_row = f"E-1028,{now},verification,\"Session 3234 verification pass (park unchanged; HEAD advanced from stale {prev_head} to HEAD {new_head} via checkpoint commit {new_head[:7]} \\\"chore(kilo): checkpoint agent session\\\"; delta {prev_head[:7]}..{new_head[:7]} limited to research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3234.md, campaign_state.json, experiment_ledger.csv) plus update_handoff_3233.py; no production code changed; gates unchanged). State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols / 12 distinct non-empty timing_cohort (12 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 102 physical lines / 100 data records / max source_id S-105 (S-100..S-104 absent; S-01..S-99 plus S-105 = 100 records); experiment_ledger.csv max non-blank E-1027 -> appended E-1028; rebuild byte-identical (\\`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3234.csv\\`, cmp clean, same sha); python3 -m pytest -q tests/ -> 173 passed, 0 failing. DNS resolves. \\`verify_artifacts.py\\` (repo root) still raises \\`SyntaxError\\` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced.\",{new_head},v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL (D-042/E-047); primary estimand inconclusive_by_construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e1028_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-1028 appended)")

# Write INITIAL_TASK_MESSAGE_3235.md
initial_task = f"""**Session 3235 task: delta-only verification pass.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3234, next_session 3235, experiments_run 1028, last_verified_head {new_head}). Then perform verification pass: fetch, reconcile HEAD, re-derive state, append E-1029, update campaign_state, prepend HANDOFF note, write INITIAL_TASK_MESSAGE_3236.md. Gates unchanged. Do not compute outcome returns.
"""

with open('research/INITIAL_TASK_MESSAGE_3235.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3235.md written")

print("All updates complete.")
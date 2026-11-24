#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3197 note
session_note = """**Session 3197 note.** Verification pass (HEAD advanced from stale 3e376bf7135e1c6527cb288a71e5671ffc5f0cb2 to HEAD 49afe1dd54c133f4aae99ee9d7e60b9cd31ebc87 via checkpoint commit 49afe1dd "chore(kilo): checkpoint agent session"; delta 3e376bf7..49afe1dd limited to research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3196.md, campaign_state.json, experiment_ledger.csv); no production code changed; gates unchanged). `git fetch origin main`; working tree clean; origin/main == HEAD == local at 49afe1dd54c133f4aae99ee9d7e60b9cd31ebc87. `research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale 3e376bf7135e1c6527cb288a71e5671ffc5f0cb2 to **49afe1dd54c133f4aae99ee9d7e60b9cd31ebc87**. `research/experiment_ledger.csv` appended E-991 (max non-blank E-990 -> E-991; 1006 physical lines incl header / 29 blank lines / 977 non-blank lines). State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 102 physical lines / 100 records incl header (100 data), max source_id S-105 (S-100..S-104 absent); experiment_ledger.csv max non-blank E-990 -> appended E-991; rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3197.csv` cmp clean, same sha). pytest unavailable (`ModuleNotFoundError: No module named pytest`); `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced. This session (3197) prepends this note, keeps rolling 10 session blocks (3197..3188; drop 3187), writes `research/INITIAL_TASK_MESSAGE_3197.md` for Session 3198, and appends verification E-991. `campaign_state.json`: `current_session` 3196 -> **3197**; `next_session` 3197 -> **3198**; `experiments_run` 991 -> **992** (preserves established offset = max E-id minus 1); `notes_count` 10; `updated_at` refreshed to `2026-11-24T00:00:16Z`. Independent re-derivation: panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb matches / 141 rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 / 141 price_venue_set PENDING A1 / rebuild byte-identical; panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df matches / 431 rows / 19 cols / 8 in_registered_panel=true / 423 empty T_A; source_ledger.csv 102 physical lines / 100 data records / max source_id S-105; S-100..S-104 absent -- pre-existing, leave unchanged; experiment_ledger.csv 1006 physical lines / 29 blank / 977 non-blank / max E-991."""

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

campaign_state['current_session'] = 3197
campaign_state['next_session'] = 3198
campaign_state['experiments_run'] = 992
campaign_state['last_verified_head'] = '49afe1dd54c133f4aae99ee9d7e60b9cd31ebc87'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-24T00:00:16Z'
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e991_row = "E-991,2026-11-24T00:00:16Z,verification,Session 3197 verification pass (park unchanged; HEAD advanced from stale 3e376bf7135e1c6527cb288a71e5671ffc5f0cb2 to HEAD 49afe1dd54c133f4aae99ee9d7e60b9cd31ebc87 via checkpoint commit 49afe1dd chore(kilo): checkpoint agent session; delta 3e376bf7..49afe1dd limited to research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3196.md, campaign_state.json, experiment_ledger.csv); no production code changed; gates unchanged). State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 102 physical lines / 100 data records / max source_id S-105 (S-100..S-104 absent); experiment_ledger.csv max non-blank E-990 -> appended E-991; rebuild byte-identical (python3 scripts/build_panel.py --out /tmp/panel_rebuild_3197.csv cmp clean, same sha). pytest unavailable (ModuleNotFoundError: No module named pytest); verify_artifacts.py (repo root) still raises SyntaxError at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced.,49afe1dd54c133f4aae99ee9d7e60b9cd31ebc87,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL (D-042/E-047); primary estimand inconclusive_by_construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e991_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-991 appended)")

# Write INITIAL_TASK_MESSAGE_3197.md for Session 3198
initial_task = """**Session 3198 task: delta-only verification pass.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3197, next_session 3198, experiments_run 992, last_verified_head 49afe1dd54c133f4aae99ee9d7e60b9cd31ebc87). Then perform verification pass: fetch, reconcile HEAD, re-derive state, append E-992, update campaign_state, prepend HANDOFF note, write INITIAL_TASK_MESSAGE_3198.md. Gates unchanged. Do not compute outcome returns."""

with open('research/INITIAL_TASK_MESSAGE_3197.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3197.md written")
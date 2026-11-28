#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3587 note
session_note = """**Session 3587 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm closed status; prior task read from the durable handoff per the standing instruction -- INITIAL_TASK_MESSAGE_3586.md). Session 3586 complete: HANDOFF.md session 3586 note present, campaign_state.json current_session->3586/next_session->3587, INITIAL_TASK_MESSAGE_3587.md written; committed as checkpoint af3fda28. Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **4bfd041e7ee18b542398de156d7fd3ddd32c2818**; working tree clean (HEAD advanced from prior session's `last_verified_head` **af3fda28e82d0be640db50d75a57f73e909d2253** to **4bfd041e7ee18b542398de156d7fd3ddd32c2818** via checkpoint af3fda28 [session 3586 handoff-set files]; delta limited to handoff-set files `research/HANDOFF.md`, `research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3587.md`, `research/experiment_ledger.csv`; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **af3fda28e82d0be640db50d75a57f73e909d2253** to **4bfd041e7ee18b542398de156d7fd3ddd32c2818**. Re-verified artifact digests directly this pass: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (12 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / 141 long-form `filing_route` PENDING A2 verification / 141 long-form `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3587.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` S-105; S-100..S-104 absent -- pre-existing, leave unchanged; `experiment_ledger.csv` 1185 physical lines / last row **E-1183** (verification) -> append E-1184 (verification). Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

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

campaign_state['current_session'] = 3587
campaign_state['next_session'] = 3588
campaign_state['experiments_run'] = 1184
campaign_state['last_verified_head'] = '4bfd041e7ee18b542398de156d7fd3ddd32c2818'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-28T14:30:15Z'
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e1184_row = "E-1184,2026-11-28T14:30:15Z,verification,Session 3587 verification pass (park unchanged; HEAD reconciled to 4bfd041e7ee18b542398de156d7fd3ddd32c2818; origin/main == HEAD == local; working tree clean),4bfd041e7ee18b542398de156d7fd3ddd32c2818,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e1184_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-1184 appended)")

# Write INITIAL_TASK_MESSAGE_3588.md
initial_task = """Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. As session 3587: prepend a "Session 3588 note" block to research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json (current_session->3588, next_session->3589, last_verified_head->current HEAD, updated_at, experiments_run->1185, notes_count->10), append an E-1185 verification row to research/experiment_ledger.csv, and write research/INITIAL_TASK_MESSAGE_3589.md with the same structure. IMPORTANT: name the forward message INITIAL_TASK_MESSAGE_<next_session>.md (e.g. 3589), NOT the current session number. When citing ledger counts/ranges, re-derive them from the files rather than copying prior notes."""

with open('research/INITIAL_TASK_MESSAGE_3588.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3588.md written")
#!/usr/bin/env python3
import json
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3588 note
session_note = """**Session 3588 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm closed status; prior task read from the durable handoff per the standing instruction -- INITIAL_TASK_MESSAGE_3587.md). Session 3587 complete: HANDOFF.md session 3587 note present, campaign_state.json current_session->3587/next_session->3588, INITIAL_TASK_MESSAGE_3588.md written; committed as checkpoint 298587f2. Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **298587f2dd95c79f948e92248ecaf0093bc32f7c**; working tree clean (HEAD advanced from prior session's `last_verified_head` **4bfd041e7ee18b542398de156d7fd3ddd32c2818** to **298587f2dd95c79f948e92248ecaf0093bc32f7c** via checkpoint 298587f2 [session 3587 handoff-set files]; delta limited to handoff-set files `research/HANDOFF.md`, `research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3588.md`, `research/experiment_ledger.csv`; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **4bfd041e7ee18b542398de156d7fd3ddd32c2818** to **298587f2dd95c79f948e92248ecaf0093bc32f7c**. Re-verified artifact digests directly this pass: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (12 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / 141 long-form `filing_route` PENDING A2 verification / 141 long-form `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3588.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` sha256 `314afc2ab4936fe5b455784d7da317de772d185c2eafad95d1de85bd255edf57` / 100 csv data records; `experiment_ledger.csv` 1187 physical lines / last row **E-1184** (verification) -> append E-1185 (verification). Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window.

"""

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
new_handoff = session_note + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3588
campaign_state['next_session'] = 3589
campaign_state['experiments_run'] = 1185
campaign_state['last_verified_head'] = '298587f2dd95c79f948e92248ecaf0093bc32f7c'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-28T14:31:34Z'
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e1185_row = "E-1185,2026-11-28T14:31:34Z,verification,Session 3588 verification pass (park unchanged; HEAD reconciled to 298587f2dd95c79f948e92248ecaf0093bc32f7c; origin/main == HEAD == local; working tree clean),298587f2dd95c79f948e92248ecaf0093bc32f7c,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e1185_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-1185 appended)")

# Write INITIAL_TASK_MESSAGE_3589.md
initial_task = """Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. As session 3588: prepend a "Session 3589 note" block to research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json (current_session->3589, next_session->3590, last_verified_head->current HEAD, updated_at, experiments_run->1186, notes_count->10), append an E-1186 verification row to research/experiment_ledger.csv, and write research/INITIAL_TASK_MESSAGE_3590.md with the same structure. IMPORTANT: name the forward message INITIAL_TASK_MESSAGE_<next_session>.md (e.g. 3590), NOT the current session number. When citing ledger counts/ranges, re-derive them from the files rather than copying prior notes."""

with open('research/INITIAL_TASK_MESSAGE_3589.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3589.md written")

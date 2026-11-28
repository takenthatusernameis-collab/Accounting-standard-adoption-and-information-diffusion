#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3570 note
session_note = """**Session 3570 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm closed status; prior task read from the durable handoff per the standing instruction). Session 3569 complete: HANDOFF.md session 3569 note present, campaign_state.json current_session->3569/next_session->3570, INITIAL_TASK_MESSAGE_3570.md written; committed as checkpoint d8eb04ec. Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **d8eb04ecbfb0be6743dbb0e2aee544fb356f3591**; working tree clean (HEAD advanced from prior session's `last_verified_head` **60252d2fbfb0be6743dbb0e2aee544fb356f3591** to **d8eb04ecbfb0be6743dbb0e2aee544fb356f3591**, checkpoint `chore(kilo): checkpoint agent session` commit; delta limited to handoff-set files `research/HANDOFF.md`, `research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3570.md`; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **60252d2fbfb0be6743dbb0e2aee544fb356f3591** to **d8eb04ecbfb0be6743dbb0e2aee544fb356f3591**. Re-verified artifact digests directly this pass: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / 141 long-form `filing_route` PENDING A2 / 141 long-form `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3570.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` sha256 `314afc2ab4936fe5b455784d7da317de772d185c2eafad95d1de85bd255edf57` / 100 csv data records / max `source_id` S-99; `experiment_ledger.csv` 1168 physical lines / 1167 csv records / max **E-1166** before this session's append -> append **E-1167** (this session). Gates: `cohort` MET (12>=12), `admitted_treatment_firm` 0<200 FAIL, `free_delisted_terminal_return_price_coverage` not established FAIL. Primary estimand inconclusive_by_construction; PH-1 closed. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

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

campaign_state['current_session'] = 3570
campaign_state['next_session'] = 3571
campaign_state['experiments_run'] = 1167
campaign_state['last_verified_head'] = 'd8eb04ecbfb0be6743dbb0e2aee544fb356f3591'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = datetime.utcnow().isoformat() + 'Z'
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e1167_row = "E-1167,2026-11-28T08:31:50Z,verification,Session 3570 verification pass (park unchanged; HEAD reconciled to d8eb04ecbfb0be6743dbb0e2aee544fb356f3591; origin/main == HEAD == local; working tree clean),d8eb04ecbfb0be6743dbb0e2aee544fb356f3591,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e1167_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-1167 appended)")
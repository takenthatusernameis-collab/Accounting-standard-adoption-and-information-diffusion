#!/usr/bin/env python3
import json
import re
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 2921 note
session_note = """**Session 2921 note.** Verification pass (HEAD `32f67563f56d75c3ec03689b38caeb58b00dc777` verified for Session 2921; git fetch origin main; working tree clean; origin/main == HEAD == local at `32f67563f56d75c3ec03689b38caeb58b00dc777`). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale `71223ae29a321ac23fa4a621e7cd4f6bd00d19ef` to **`32f67563f56d75c3ec03689b38caeb58b00dc777`** (one checkpoint chore commit advanced HEAD since Session 2920; no code changed, gates unchanged). pytest not available in this shell (`No module named pytest`); prior sessions reported 173 passed, 0 failing. No code changed. Gates unchanged. This session (2921) prepends this note, keeps rolling 10 session blocks (2921, 2920, 2919, 2918, 2917, 2916, 2915, 2914, 2913, 2912; drop 2909), writes `research/INITIAL_TASK_MESSAGE_2920.md` for Session 2922, and appends verification E-715. `campaign_state.json`: `current_session` 2920 -> **2921**; `next_session` 2921 -> **2922**; `experiments_run` 713 -> **713** (preserves established offset = max E-id minus 1; max E-id remains 714); `notes_count` 10; `updated_at` refreshed to `2026-11-19T09:07:17Z`. Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 12 non-empty `T_A` (129 empty) / 141 `filing_route` PENDING A2 / 141 `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2921.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` S-99 (S-100..S-104 absent -- pre-existing, leave unchanged); `experiment_ledger.csv` 729 physical lines / 727 csv records / max **E-714** before this session's append -> append E-715 -> max **E-715** (E-403/E-404 shared-line anomaly intact, E-680 ragged row intact); `research/decision_log.md` 2642 physical lines / 95 `## D-<n>` headers (max D-147); `results.md` 151 physical lines / 131 non-empty lines / reports no results. Park unchanged: cohort gate **MET (12>=12)**; admitted treatment-firm **0 < 200 (FAIL)**; `filing_route`/`price_venue_set` PENDING for all 141 PH-1 rows; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**; primary estimand **inconclusive_by_construction**; **PH-1 closed**. No gate advanced; no outcome-period return computed/inspected; no paid data; no credentials; no GitHub Actions; `.github/workflows/main.yml` unmodified; closed probes not repeated."""

# Split into lines and keep only the first 9 session blocks (we'll add the new one to make 10)
lines = handoff_content.strip().split('\n')
session_blocks = []
current_block = []
for line in lines:
    if line.startswith('**Session ') and ' note.**' in line:
        if current_block:
            session_blocks.append('\n'.join(current_block))
        current_block = [line]
    else:
        current_block.append(line)
if current_block:
    session_blocks.append('\n'.join(current_block))

# Keep first 9 (newest 9), drop oldest (we'll add the new one to make 10)
session_blocks = session_blocks[:9]

# Prepend new session note
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 2921
campaign_state['next_session'] = 2922
campaign_state['experiments_run'] = 713
campaign_state['last_verified_head'] = '32f67563f56d75c3ec03689b38caeb58b00dc777'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-19T09:07:17Z'
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e715_row = "E-715,2026-11-19T09:07:17Z,verification,Session 2921 verification pass (park unchanged; last_verified_head reconciled to HEAD 32f67563f56d75c3ec03689b38caeb58b00dc777),32f67563f56d75c3ec03689b38caeb58b00dc777,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e715_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-715 appended)")
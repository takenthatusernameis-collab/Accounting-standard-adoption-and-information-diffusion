#!/usr/bin/env python3
import json
import csv
import re
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 2902 note
session_note = """**Session 2902 note.** Verification pass (Session 2901 checkpoint `18f4241894a5d478b0eddef893c86cecaf63bddb` -> completed for Session 2902; HEAD advanced by one checkpoint chore commit to `7423574a392d0d802a0c2eb2b9a7a102caf5a1f5`). `git fetch origin main`; working tree clean; origin/main == HEAD == local at `7423574a392d0d802a0c2eb2b9a7a102caf5a1f5`. `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale `18f4241894a5d478b0eddef893c86cecaf63bddb` to **`7423574a392d0d802a0c2eb2b9a7a102caf5a1f5`**. pytest not available in this shell (`No module named pytest`); prior sessions reported 173 passed, 0 failing. No code changed. Gates unchanged. This session (2902) prepends this note, keeps rolling 10 session blocks (2902..2891; drop 2890), writes `research/INITIAL_TASK_MESSAGE_2901.md` for Session 2903, and appends verification E-696. `campaign_state.json`: `current_session` 2901 -> **2902**; `next_session` 2902 -> **2903**; `experiments_run` 694 -> **695** (preserves established offset = max E-id minus 1; appended E-696 so max E-id 696); `notes_count` 10; `updated_at` refreshed to `2026-11-19T03:16:11Z`. Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / 141 long-form `filing_route` PENDING A2 / 141 long-form `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2902.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` S-99; S-100..S-104 absent -- pre-existing, leave unchanged; `experiment_ledger.csv` 710 physical lines / 678 csv DictReader records (embedded newlines; ragged rows incl. E-403/E-404 shared-line anomaly, E-680 ragged) / max **E-695** before this session's append -> appended **E-696**; `decision_log.md` 2642 physical lines / 95 `## D-<n>` headers (max D-150) / no trailing newline; `results.md` 151 physical lines / 131 non-empty / reports no results; `verify_artifacts.py` (repo root) pre-existing `SyntaxError` at line 110; `.github/workflows/main.yml` sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged."""

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

campaign_state['current_session'] = 2902
campaign_state['next_session'] = 2903
campaign_state['experiments_run'] = 695
campaign_state['last_verified_head'] = '7423574a392d0d802a0c2eb2b9a7a102caf5a1f5'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-19T03:16:11Z'
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e696_row = "E-696,2026-11-19T03:16:11Z,verification,Session 2902 verification pass (park unchanged),7423574a392d0d802a0c2eb2b9a7a102caf5a1f5,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e696_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-696 appended)")
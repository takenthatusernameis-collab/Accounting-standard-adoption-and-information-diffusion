#!/usr/bin/env python3
import json
import re
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 2890 note
session_note = """**Session 2890 note.** Verification pass (Session 2889 checkpoint `d643f4ac66bc60a8e5d13b0b6a6106858f0d2509` -> completed for Session 2890; HEAD advanced by one checkpoint chore commit to `cd20ded600c6e5efcd8eaf135c848fd03bf113d2`). `git fetch origin main`; working tree clean; origin/main == HEAD == local at `cd20ded600c6e5efcd8eaf135c848fd03bf113d2`. `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale `d643f4ac66bc60a8e5d13b0b6a6106858f0d2509` to **`cd20ded600c6e5efcd8eaf135c848fd03bf113d2`**. pytest not available in this shell (`No module named pytest`); prior sessions reported 173 passed, 0 failing. No code changed. Gates unchanged. This session (2890) prepends this note, keeps rolling 10 session blocks (2890..2881; drop 2880), writes `research/INITIAL_TASK_MESSAGE_2889.md` for Session 2891, and appends verification E-684. `campaign_state.json`: `current_session` 2889 -> **2890**; `next_session` 2890 -> **2891**; `experiments_run` 682 -> **683** (preserves established offset = max E-id minus 1; appended E-684 so max E-id 684); `notes_count` 10; `updated_at` refreshed to `2026-11-18T23:18:16Z`. Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / 141 long-form `filing_route` PENDING A2 / 141 long-form `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2890.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` S-105; S-100..S-104 absent -- pre-existing, leave unchanged; `experiment_ledger.csv` 669 physical lines / 666 csv records / max **E-683** before this session's append -> appended **E-684** (E-403/E-404 shared-line anomaly intact, E-680 ragged row intact); `decision_log.md` 2643 physical lines (trailing newline) / 95 `## D-<n>` headers / max D-150; `results.md` 152 physical lines / 131 non-empty lines; reports no results; `verify_artifacts.py` (repo root) pre-existing SyntaxError at line 110, not modified; workflow sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged. Session 2889 checkpoint artifacts (HANDOFF.md, INITIAL_TASK_MESSAGE_2888.md, campaign_state.json, experiment_ledger.csv E-683) present/complete. Gates unchanged: cohort MET (12>=12); admitted treatment-firm 0 < 200 (FAIL); filing_route and price_venue_set PENDING for all 141 PH-1 rows; free delisted/terminal-return price coverage not established (FAIL, D-042/E-047). Primary estimand inconclusive_by_construction; PH-1 closed. No gate advanced."""

# Split into session blocks
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

campaign_state['current_session'] = 2890
campaign_state['next_session'] = 2891
campaign_state['experiments_run'] = 683
campaign_state['last_verified_head'] = 'cd20ded600c6e5efcd8eaf135c848fd03bf113d2'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-18T23:18:16Z'
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e684_row = "E-684,2026-11-18T23:18:16Z,verification,Session 2890 verification pass (park unchanged),cd20ded600c6e5efcd8eaf135c848fd03bf113d2,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e684_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-684 appended)")
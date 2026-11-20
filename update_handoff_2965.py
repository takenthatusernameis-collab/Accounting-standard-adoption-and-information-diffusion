#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Current timestamp
now = "2026-11-20T03:49:05Z"
current_head = "2863788a81d3f4f091929a966b408f82a1d9fdac"

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 2965 note
session_note = f"""**Session 2965 note.** Verification pass (HEAD {current_head} verified for Session 2965; `git fetch origin main`; working tree clean; origin/main == HEAD == local at `{current_head}`). `research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale `88ab8a2d0c251e17dca755c09b4c83cf857613c9` to **`{current_head}`** (HEAD advanced since Session 2964 via checkpoint chore commit; no code changed, gates unchanged). pytest not available (`ModuleNotFoundError: No module named pytest`); prior sessions reported 173 passed, 0 failing. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. This session (2965) prepends this note, keeps rolling 10 session blocks (2965..2956; drop 2955), writes `research/INITIAL_TASK_MESSAGE_2965.md` for Session 2966, and appends verification E-759. `campaign_state.json`: `current_session` **2965**; `next_session` **2966**; `experiments_run` **758**; `notes_count` 10; `updated_at` refreshed to `{now}`. Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 12 non-empty `T_A` (129 empty) / 141 `filing_route` PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / 141 `price_venue_set` PENDING A1 (price vendors and their licensing are not yet authorised) / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2965.csv`, `cmp` clean); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` **S-105** (S-100..S-104 absent -- per D-037); `experiment_ledger.csv` 774 physical lines / max **E-758** before this session's append -> **E-759** after. Park unchanged: cohort gate MET (12>=12); admitted treatment-firm 0 < 200 (FAIL); `filing_route`/`price_venue_set` PENDING for all 141 PH-1 rows; primary estimand inconclusive by construction."""

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

campaign_state['current_session'] = 2965
campaign_state['next_session'] = 2966
campaign_state['experiments_run'] = 758
campaign_state['last_verified_head'] = current_head
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = now
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e759_row = f"E-759,{now},verification,Session 2965 verification pass (park unchanged; last_verified_head reconciled from stale 88ab8a2d0c251e17dca755c09b4c83cf857613c9 to HEAD {current_head}; checkpoint chore commit only; no code changed; gates unchanged),{current_head},v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed; only cohort gate passes (12>=12); treatment-firm gate 0<200 FAIL; free delisted/terminal-return coverage not established FAIL,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e759_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-759 appended)")

# Write INITIAL_TASK_MESSAGE_2965.md
initial_task = f"""Session 2966 task: delta-only verification pass.

Read durable handoff `research/HANDOFF.md` and `research/campaign_state.json`. Run `git fetch origin main`; verify working tree clean and origin/main == HEAD == local. Parse campaign_state.json with `json.load`; reconcile `last_verified_head` if stale (currently `{current_head}`). Re-derive committed state (D-037). Append verification E-760. Update campaign_state. Prepend Session 2966 note. Write `research/INITIAL_TASK_MESSAGE_2966.md` for Session 2967. Gates unchanged expected. Do not compute outcome-period returns. pytest unavailable. Report park honestly."""

with open('research/INITIAL_TASK_MESSAGE_2965.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_2965.md written")
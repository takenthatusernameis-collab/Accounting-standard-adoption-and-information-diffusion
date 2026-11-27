#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3446 note
session_note = """**Session 3446 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and §9; confirm closed status). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **4612eb05**; working tree clean (HEAD advanced from prior session's `last_verified_head` **db394738a26b4e3332c9bce805e578d58440c8cb** to **4612eb05a21209a84cf7d383409f5ecc0cd5594e**, which is a `chore(kilo): checkpoint agent session` commit; no state/logic change). `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` unchanged, 141 rows / 21 cols / 0 `in_registered_panel=true` / 12 distinct non-empty `timing_cohort` / 141 `filing_route` PENDING A2 verification / 141 `price_venue_set` PENDING A1; rebuild via `scripts/build_panel.py` byte-identical (post-rebuild sha256 unchanged, git status clean, git diff empty). `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged, 431 rows / 19 cols / 8 `in_registered_panel=true`. Experiment ledger max real run_id **E-1139** (E-1068 formal close; E-1069…E-1139 verification; E-3243 duplicate-of-E-1037 anomaly still present, excluded by numeric run_id comparison); decision_log max header **D-151** (96 D-headers; Formal-close section at `## Formal close (Session 3275)`; no D-152 header exists). `campaign_state.json` reconciled: `last_verified_head` stale **db394738a26b4e3332c9bce805e578d58440c8cb** → **4612eb05a21209a84cf7d383409f5ecc0cd5594e**; current_session 3445 → **3446**; next_session 3446 → **3447**; experiments_run 1154 → **1155**; notes_count 112 → **113**; updated_at refreshed to **2026-11-27T04:25:43Z**. No code changed; no gate advanced; no outcome returns; PH-1 not opened; results.md still reports no results. Prepends this note; rewrites §9; writes research/INITIAL_TASK_MESSAGE_3447.md for Session 3447. Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

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

campaign_state['current_session'] = 3446
campaign_state['next_session'] = 3447
campaign_state['experiments_run'] = 1155
campaign_state['last_verified_head'] = '4612eb05a21209a84cf7d383409f5ecc0cd5594e'
campaign_state['notes_count'] = 113
campaign_state['updated_at'] = '2026-11-27T04:25:43Z'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e1140_row = "E-1140,2026-11-27T04:25:43Z,verification,Session 3446 verification pass (park unchanged; HEAD reconciled to 4612eb05a21209a84cf7d383409f5ecc0cd5594e; origin/main == HEAD == local; working tree clean),4612eb05a21209a84cf7d383409f5ecc0cd5594e,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 not opened,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e1140_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-1140 appended)")

# Write INITIAL_TASK_MESSAGE_3447.md
initial_task = """**Session 3447 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3446, next_session 3447, experiments_run 1155, last_verified_head 4612eb05a21209a84cf7d383409f5ecc0cd5594e).

Campaign is closed as PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close section). No further verification passes. Do not compute outcome returns, do not open PH-1, do not use paid sources. If resuming, the single highest-value next action is: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, no action required.

Note on re-derived state (Session 3446): experiment ledger max real run_id is E-1139 (E-3243 is a known duplicate-of-E-1037 anomaly; compare run_ids numerically, not as strings); decision_log max header is D-151 (no D-152 header exists — prior "D-152" references are a mislabel). Panel files unchanged (v1.2 sha256 d075c3a7…c700eb, 141 rows, 12 cohorts, all gate-pending, rebuild byte-identical; v1.1 sha256 40f3c19f…a899df, 431 rows). HEAD at 4612eb05 (origin/main == HEAD == local), working tree clean. last_verified_head reconciled from stale db394738 to 4612eb05a21209a84cf7d383409f5ecc0cd5594e."""

with open('research/INITIAL_TASK_MESSAGE_3447.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3447.md written")
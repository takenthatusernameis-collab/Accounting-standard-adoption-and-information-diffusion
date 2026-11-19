#!/usr/bin/env python3
import json
from datetime import datetime, timezone

now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
head = '9fb701c51af11e34ea31520693fcb0c52ef9bdfa'

# Get original HANDOFF.md from git (HEAD already has session 2892 committed)
import subprocess
original = subprocess.run(['git', 'show', 'HEAD:research/HANDOFF.md'], capture_output=True, text=True).stdout

# Split into session blocks: each block starts with a line beginning with '**Session '
lines = original.strip().split('\n')
blocks = []
cur = []
for line in lines:
    if line.startswith('**Session '):
        if cur:
            blocks.append('\n'.join(cur))
        cur = [line]
    else:
        cur.append(line)
if cur:
    blocks.append('\n'.join(cur))

print('Original blocks:', len(blocks))
for b in blocks:
    print(' ', b.split('\n')[0][:80])

# Session 2893 note
session_note = """**Session 2893 note.** Verification pass (Session 2892 checkpoint `703714894fb7fb86d9b0cb222fc273acf5684bd8` -> completed for Session 2893; HEAD is one checkpoint chore commit ahead at """ + head + """). `git fetch origin main`; working tree clean; origin/main == HEAD == local at """ + head + """. `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale `703714894fb7fb86d9b0cb222fc273acf5684bd8` to **""" + head + """**. pytest not available in this shell (`No module named pytest`); prior sessions reported 173 passed, 0 failing. No code changed. Gates unchanged. This session (2893) prepends this note, keeps rolling 10 session blocks (2893..2884; drop 2883), writes `research/INITIAL_TASK_MESSAGE_2892.md` for Session 2894, and appends verification E-687. `campaign_state.json`: `current_session` 2892 -> **2893**; `next_session` 2893 -> **2894**; `experiments_run` 685 -> **686** (preserves established offset = max E-id minus 1; appended E-687 so max E-id 687); `notes_count` 10; `updated_at` refreshed to """ + now + """. Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / 141 long-form `filing_route` PENDING A2 / 141 long-form `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2893.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` S-105; S-100..S-104 absent -- pre-existing, leave unchanged; `experiment_ledger.csv` 701 physical lines / 671 csv records / max **E-686** before this session's append -> appended **E-687**; `decision_log.md` 2642 physical lines / 95 `## D-<n>` headers (max D-150); `results.md` 151 physical lines / 131 non-empty lines; reports no results. Park unchanged: cohort MET (12>=12); admitted treatment-firm 0 < 200 (FAIL); filing_route/price_venue_set PENDING for all 141 PH-1 rows; free delisted/terminal-return price coverage not established (FAIL, D-042/E-047). Primary estimand inconclusive_by_construction; PH-1 closed."""

# Keep last 9 existing blocks (drop oldest 2883), prepend new one
blocks = blocks[-9:]
new_handoff = session_note + '\n\n' + '\n\n'.join(blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print('HANDOFF.md updated with', 1 + len(blocks), 'session blocks')

# Verify block count
with open('research/HANDOFF.md') as f:
    content = f.read()
lines2 = content.strip().split('\n')
count = sum(1 for l in lines2 if l.startswith('**Session '))
print('Verified HANDOFF.md session blocks:', count)

# Update campaign_state.json
with open('research/campaign_state.json') as f:
    cs = json.load(f)

cs['current_session'] = 2893
cs['next_session'] = 2894
cs['experiments_run'] = 686
cs['last_verified_head'] = head
cs['notes_count'] = 10
cs['updated_at'] = now
cs['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(cs, f, separators=(', ', ': '))
print('campaign_state.json updated')

# experiment_ledger.csv already has E-687 from previous partial run - verify
with open('research/experiment_ledger.csv') as f:
    lines3 = f.readlines()
e_ids = [l.split(',')[0] for l in lines3 if l.startswith('E-')]
print('experiment_ledger.csv max E-id:', max(e_ids) if e_ids else 'N/A')

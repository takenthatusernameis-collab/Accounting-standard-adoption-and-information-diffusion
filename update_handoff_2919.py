#!/usr/bin/env python3
import json
import re
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 2919 note
session_note = """**Session 2919 note.** Verification pass (HEAD `1558ead4a6e6400bc4875ba73fbab49f534429f1` verified for Session 2919; git fetch origin main; working tree clean; origin/main == HEAD == local at `1558ead4a6e6400bc4875ba73fbab49f534429f1`). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale `793c5b14d66684eb37b560b1b12ba66d77dd8277` to **`1558ead4a6e6400bc4875ba73fbab49f534429f1`** (three checkpoint chore commits advanced HEAD since Session 2918; no code changed, gates unchanged). pytest not available in this shell (`No module named pytest`); prior sessions reported 173 passed, 0 failing. No code changed. Gates unchanged. This session (2919) prepends this note, keeps rolling 10 session blocks (2919, 2918, 2917, 2916, 2915, 2914, 2913, 2912, 2909, 2908; drop 2907), writes `research/INITIAL_TASK_MESSAGE_2918.md` for Session 2920, and appends verification E-713. `campaign_state.json`: `current_session` 2918 -> **2919**; `next_session` 2919 -> **2920**; `experiments_run` 711 -> **711** (preserves established offset = max E-id minus 1; max E-id remains 712); `notes_count` 10; `updated_at` refreshed to `2026-11-19T08:17:23Z`. Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 12 non-empty `T_A` (129 empty) / 141 `filing_route` PENDING A2 / 141 `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2919.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` S-99 (S-100..S-104 absent -- pre-existing, leave unchanged); `experiment_ledger.csv` 727 physical lines / 695 csv records / max **E-712** before this session's append -> append E-713 -> max E-713 (E-403/E-404 shared-line anomaly intact, E-680 ragged row intact); `research/decision_log.md` 2642 physical lines (ends with trailing newline) / 95 `## D-<n>` decision headers (max D-147); `research/results.md` 151 physical lines / 131 non-empty lines / reports no results; `research/HANDOFF.md` 10 `**Session N note.**` blocks after edit; `.github/workflows/main.yml` sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged; `verify_artifacts.py` (repo root) pre-existing `SyntaxError` at line 110 (unbalanced parenthesis; confirmed again this session via `ast.parse`) and is not usable as-is; not modified. Park unchanged: cohort gate **MET (12>=12)**; admitted treatment-firm **0 < 200 (FAIL)**; `filing_route`/`price_venue_set` PENDING for all 141 PH-1 rows; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**; primary estimand **inconclusive_by_construction**; **PH-1 closed**. No gate advanced; no outcome-period return computed/inspected; no paid data; no credentials; no GitHub Actions; `.github/workflows/main.yml` unmodified; closed probes not repeated."""

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

campaign_state['current_session'] = 2919
campaign_state['next_session'] = 2920
campaign_state['experiments_run'] = 711
campaign_state['last_verified_head'] = '1558ead4a6e6400bc4875ba73fbab49f534429f1'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-19T08:17:23Z'
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e713_row = "E-713,2026-11-19T08:17:23Z,verification,Session 2919 verification pass (park unchanged),1558ead4a6e6400bc4875ba73fbab49f534429f1,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e713_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-713 appended)")
#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3189 note
session_note = """**Session 3189 note.** Verification pass (HEAD `b47562a740b6ceb82659250e9b05ce52ae921a57` verified for Session 3189; `git fetch origin main`; working tree clean; origin/main == HEAD == local at `b47562a740b6ceb82659250e9b05ce52ae921a57`). `research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale `fba080e968a8605f1a3335b2e86497a89b489d82` to **`b47562a740b6ceb82659250e9b05ce52ae921a57`** (HEAD advanced since Session 3188's E-983 append via checkpoint commit `b47562a7` "chore(kilo): checkpoint agent session"; delta `fba080e9..b47562a7` limited to research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3188.md, campaign_state.json, experiment_ledger.csv); no production code changed, gates unchanged). `research/experiment_ledger.csv` appended E-984 (max non-blank E-983 -> E-984; 997 physical lines incl header / 29 blank lines / 968 non-blank lines). State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true / 423 empty T_A; source_ledger.csv 101 physical lines / 100 records incl header (100 data), max source_id S-99 (S-100..S-104 absent); experiment_ledger.csv max non-blank E-983 -> appended E-984; rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3189.csv`, cmp clean, same sha). pytest unavailable (`ModuleNotFoundError: No module named pytest`); prior sessions reported 173 passed, 0 failing. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. This session (3189) prepends this note, keeps rolling 10 session blocks (3189..3180), dropping 3179, writes `research/INITIAL_TASK_MESSAGE_3189.md` for Session 3190, and appends verification E-984. `campaign_state.json`: current_session 3188 -> **3189**; next_session 3189 -> **3190**; experiments_run 983 -> **984**; notes_count 10; updated_at refreshed to `2026-11-23T16:04:39Z`. Independent re-derivation: panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb matches / 141 rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 / 141 price_venue_set PENDING A1 / rebuild byte-identical; panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df matches / 431 rows / 19 cols / 8 in_registered_panel=true / 423 empty T_A; source_ledger.csv 101 lines / 100 data / max source_id S-99 (S-100..S-104 absent) / experiment_ledger.csv max non-blank E-983 -> E-984."""

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

campaign_state['current_session'] = 3189
campaign_state['next_session'] = 3190
campaign_state['experiments_run'] = 984
campaign_state['last_verified_head'] = 'b47562a740b6ceb82659250e9b05ce52ae921a57'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-23T16:04:39Z'
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append to experiment_ledger.csv
e984_row = "E-984,2026-11-23T16:04:39Z,verification,Session 3189 verification pass (park unchanged; HEAD advanced from stale fba080e968a8605f1a3335b2e86497a89b489d82 to HEAD b47562a740b6ceb82659250e9b05ce52ae921a57; checkpoint commit b47562a7 touched only research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3188.md, campaign_state.json, experiment_ledger.csv); no production code changed; gates unchanged). State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 101 physical lines / 100 records incl header (100 data), max source_id S-99 (S-100..S-104 absent); experiment_ledger.csv max non-blank E-983 -> appended E-984; rebuild byte-identical (cmp clean, same sha). pytest unavailable (ModuleNotFoundError: No module named pytest); verify_artifacts.py (repo root) still raises SyntaxError at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced.,b47562a740b6ceb82659250e9b05ce52ae921a57,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL (D-042/E-047); primary estimand inconclusive_by_construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Ensure exactly one newline before append
content = content.rstrip('\n') + '\n' + e984_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-984 appended)")

# Write INITIAL_TASK_MESSAGE_3189.md
initial_task = """**Session 3190 task: delta-only verification pass.**

Read the durable handoff `research/HANDOFF.md` and `research/campaign_state.json` (currently `current_session` 3189, `next_session` 3190, `experiments_run` 984, `last_verified_head` b47562a740b6ceb82659250e9b05ce52ae921a57). Then:

1. Run `git fetch origin main`. Verify the working tree is clean and that `origin/main` == `HEAD` == local HEAD. If HEAD has advanced, record the new sha and reconcile `last_verified_head` (do not edit code).
2. Re-derive committed state (D-037) and compare against the handoff note (panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols; panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols; source_ledger.csv 101 physical lines / 100 data; experiment_ledger.csv max non-blank E-984 -> append E-985).
3. Append one verification row to `research/experiment_ledger.csv` (id `E-985`, timestamp UTC, category `verification`, note that the park is unchanged, HEAD, `v1.2`, `panel_v1.2.csv (141 rows)`, `no gate advanced`, `none`, gate summary, `verification only; no outcome-period returns computed or inspected`). Append with a plain `csv.writer` opened in append mode using `lineterminator="\\n"`.
4. Update `research/campaign_state.json`: `current_session` 3190, `next_session` 3191, `experiments_run` 985, `last_verified_head` = verified HEAD, `notes_count` 10, refreshed `updated_at`.
5. Prepend a Session 3190 note to `research/HANDOFF.md` keeping the rolling 10 session blocks (3190..3181), dropping the oldest.
6. Write `research/INITIAL_TASK_MESSAGE_3190.md` for Session 3191.

Gates expected unchanged: cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL. Primary estimand remains inconclusive by construction; PH-1 is closed. Do NOT compute or inspect outcome-period returns. `pytest` is unavailable and `verify_artifacts.py` has a pre-existing `SyntaxError` at line 110. Report the park honestly; do not manufacture progress."""

with open('research/INITIAL_TASK_MESSAGE_3189.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3189.md written")

print("Session 3189 complete")
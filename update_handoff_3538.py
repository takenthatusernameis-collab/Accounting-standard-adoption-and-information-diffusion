#!/usr/bin/env python3
import json
import csv
from datetime import datetime

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3538 note
session_note = """**Session 3538 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm closed status; prior task read from the durable handoff per the standing instruction). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **ae98d605874979bac2f6c0ec3a1fecabb57b83db**; working tree clean (HEAD advanced from prior session's `last_verified_head` **08826571f2d4a8565d7d2bb1721d8e16e7c1b208** to **ae98d605874979bac2f6c0ec3a1fecabb57b83db**, checkpoint `chore(kilo): checkpoint agent session` commit; delta limited to handoff-set files `research/HANDOFF.md`, `research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3538.md`; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **08826571f2d4a8565d7d2bb1721d8e16e7c1b208** to **`ae98d605874979bac2f6c0ec3a1fecabb57b83db`**. `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` unchanged / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / 141 long-form `filing_route` PENDING A2 / 141 long-form `price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3538.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` S-105; S-100..S-104 absent -- pre-existing, leave unchanged; `experiment_ledger.csv` sha256 `4272ea81732f6121729701919b6f501e57add5ce527462e5b961046a6a968be0` max real run_id **E-1150** (E-3243 duplicate-of-E-1037 anomaly present, excluded); no new ledger row appended this no-op pass. `decision_log.md` sha256 `a9f2a6242417de61eb877f416d72eb34e69c6c415b64e5523fd5541b1ba20cd6` max header **D-151**; no D-152. `results.md` sha256 `94077e1c24ae9e54d3b47ea309f530d73c4beafea931f363014815da78066e18` 151 lines, no results. Workflow `.github/workflows/main.yml` sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged. `campaign_state.json` reconciled: `last_verified_head` stale **08826571f2d4a8565d7d2bb1721d8e16e7c1b208** -> **`ae98d605874979bac2f6c0ec3a1fecabb57b83db`**; `current_session` 3537 -> **3538**; `next_session` 3538 -> **3539**; `experiments_run` 1166; `notes_count` 10; `updated_at` refreshed to `2026-11-28T02:49:49Z`. Independent re-derivation matches committed files exactly; campaign remains PARKED/INCONCLUSIVE. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

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

campaign_state['current_session'] = 3538
campaign_state['next_session'] = 3539
campaign_state['last_verified_head'] = 'ae98d605874979bac2f6c0ec3a1fecabb57b83db'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-28T02:49:49Z'
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Create INITIAL_TASK_MESSAGE_3539.md
initial_task = """Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. As session 3539: prepend a "Session 3539 note" block to research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json (current_session->3539, next_session->3540, last_verified_head->current HEAD, updated_at), and write research/INITIAL_TASK_MESSAGE_3540.md with the same structure."""

with open('research/INITIAL_TASK_MESSAGE_3539.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3539.md created")
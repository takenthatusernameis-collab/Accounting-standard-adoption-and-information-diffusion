#!/usr/bin/env python3
import json
from datetime import datetime, timezone

HANDOFF = 'research/HANDOFF.md'
STATE = 'research/campaign_state.json'

HEAD = 'fcd089e5e80d04ab329825f88e5862756bb1f223'
PRIOR_HEAD = '51c0582d71ffad628ab2c9926ce3ef7a07c4d849'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

session_note = (
    "**Session 3547 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, "
    "D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification "
    "passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm "
    "closed status; prior task read from the durable handoff per the standing instruction). "
    "Prior session 3546 completed its handoff/state updates but its `update_handoff_3546.py` wrote "
    "`research/INITIAL_TASK_MESSAGE_3546.md` instead of the required `INITIAL_TASK_MESSAGE_3547.md` "
    "(off-by-one); this pass backfills `INITIAL_TASK_MESSAGE_3547.md` to complete that dropped "
    "deliverable and writes `INITIAL_TASK_MESSAGE_3548.md` for the next agent. "
    "Re-derived committed state from files (D-037): `git fetch origin main` shows "
    "origin/main == HEAD == local at **" + HEAD + "**; working tree clean (HEAD advanced from prior "
    "session's `last_verified_head` **" + PRIOR_HEAD + "** to **" + HEAD + "**, checkpoint "
    "`chore(kilo): checkpoint agent session` commit; delta limited to handoff-set files "
    "`research/HANDOFF.md`, `research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3546.md`, "
    "plus `update_handoff_3546.py`; no production code changed). `campaign_state.json` parsed with "
    "`json.load`; `last_verified_head` corrected from stale **" + PRIOR_HEAD + "** to **`" + HEAD + "`**`. "
    "`panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` "
    "unchanged / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / "
    "0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / 141 long-form `filing_route` "
    "PENDING A2 / 141 long-form `price_venue_set` PENDING A1 / rebuild byte-identical "
    "(`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3547.csv` cmp clean, same sha); "
    "`panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` "
    "unchanged / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; "
    "`source_ledger.csv` sha256 `314afc2ab4936fe5b455784d7da317de772d185c2eafad95d1de85bd255edf57` "
    "unchanged / 102 physical lines / 100 csv data records / max `source_id` S-105; S-100..S-104 "
    "absent -- pre-existing, leave unchanged; `experiment_ledger.csv` sha256 "
    "`4272ea81732f6121729701919b6f501e57add5ce527462e5b961046a6a968be0` unchanged / 1134 data records / "
    "max real run_id **E-1150** (E-3243 duplicate-of-E-1037 anomaly present, excluded; E-1068 present); "
    "no new ledger row appended this no-op pass. `decision_log.md` sha256 "
    "`a9f2a6242417de61eb877f416d72eb34e69c6c415b64e5523fd5541b1ba20cd6` unchanged; Formal-close "
    "marker and D-151 present. Independent re-derivation matches committed files exactly; campaign "
    "remains PARKED/INCONCLUSIVE. Binding constraint for any future resume (unchanged): obtain >=200 "
    "admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily "
    "price coverage to the PH-1 outcome window."
)

with open(HANDOFF, 'r') as f:
    handoff_content = f.read()

lines = handoff_content.strip().split('\n')
session_blocks = []
current_block = []
for line in lines:
    if line.startswith('**Session '):
        if current_block:
            session_blocks.append('\n'.join(current_block))
        current_block = [line]
    else:
        if current_block:
            current_block.append(line)
if current_block:
    session_blocks.append('\n'.join(current_block))

# Keep the 9 newest prior blocks (file is newest-first); prepend the new one -> 10 total.
session_blocks = session_blocks[:9]
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open(HANDOFF, 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated; blocks now:", 1 + len(session_blocks))

with open(STATE, 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3547
campaign_state['next_session'] = 3548
campaign_state['last_verified_head'] = HEAD
campaign_state['updated_at'] = NOW
campaign_state['notes_count'] = 10

with open(STATE, 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated")

# Backfill the prior session's dropped deliverable (task for session 3547).
initial_task_3547 = (
    "Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed "
    "(PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify "
    "origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; "
    "no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted "
    "treatment firms with timestamped filing evidence plus delisted/terminal-return daily price "
    "coverage to the PH-1 outcome window. As session 3547: prepend a \"Session 3547 note\" block to "
    "research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json "
    "(current_session->3547, next_session->3548, last_verified_head->current HEAD, updated_at), and "
    "write research/INITIAL_TASK_MESSAGE_3548.md with the same structure. (This file backfills the "
    "deliverable that session 3546's update_handoff_3546.py dropped due to an off-by-one filename.)"
)
with open('research/INITIAL_TASK_MESSAGE_3547.md', 'w') as f:
    f.write(initial_task_3547)
print("INITIAL_TASK_MESSAGE_3547.md written (backfill)")

# Forward task for the next agent (session 3548).
initial_task_3548 = (
    "Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed "
    "(PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify "
    "origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; "
    "no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted "
    "treatment firms with timestamped filing evidence plus delisted/terminal-return daily price "
    "coverage to the PH-1 outcome window. As session 3548: prepend a \"Session 3548 note\" block to "
    "research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json "
    "(current_session->3548, next_session->3549, last_verified_head->current HEAD, updated_at), and "
    "write research/INITIAL_TASK_MESSAGE_3549.md with the same structure. IMPORTANT: name the "
    "forward message INITIAL_TASK_MESSAGE_<next_session>.md (e.g. 3549), NOT the current session "
    "number, to avoid the off-by-one that dropped INITIAL_TASK_MESSAGE_3547.md."
)
with open('research/INITIAL_TASK_MESSAGE_3548.md', 'w') as f:
    f.write(initial_task_3548)
print("INITIAL_TASK_MESSAGE_3548.md written")
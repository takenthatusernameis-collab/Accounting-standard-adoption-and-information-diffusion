#!/usr/bin/env python3
import json
from datetime import datetime, timezone

HANDOFF = 'research/HANDOFF.md'
STATE = 'research/campaign_state.json'

HEAD = '1c9059c497f5d01dbe6c7da7067153cc4226bc57'
PRIOR_HEAD = '66ef37b7e4e3e2fe7b59bbb26180f44b8e4bdf7d'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

session_note = (
    "**Session 3556 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, "
    "D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification "
    "passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm "
    "closed status; prior task read from the durable handoff per the standing instruction). "
    "Re-derived committed state from files (D-037): `git fetch origin main` shows "
    "origin/main == HEAD == local at **" + HEAD + "**; working tree clean (HEAD advanced from prior "
    "session's `last_verified_head` **" + PRIOR_HEAD + "** to **" + HEAD + "**, checkpoint "
    "`chore(kilo): checkpoint agent session` commit; delta limited to handoff-set files "
    "`research/HANDOFF.md`, `research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3556.md`, "
    "`update_handoff_3555.py`; no production code changed). `campaign_state.json` parsed with "
    "`json.load`; `last_verified_head` corrected from stale **" + PRIOR_HEAD + "** to **`" + HEAD + "`**`. "
    "`panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` "
    "unchanged / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / "
    "0 `in_registered_panel=true` (141 `pending`) / 129 empty `T_A` / rebuild byte-identical; "
    "`panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` "
    "unchanged / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; "
    "`source_ledger.csv` sha256 `314afc2ab4936fe5b455784d7da317de772d185c2eafad95d1de85bd255edf57` "
    "unchanged / 100 csv data records / max `source_id` S-105; S-100..S-104 absent -- pre-existing, "
    "leave unchanged; `experiment_ledger.csv` sha256 "
    "`4272ea81732f6121729701919b6f501e57add5ce527462e5b961046a6a968be0` unchanged / 1165 data records / "
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

campaign_state['current_session'] = 3556
campaign_state['next_session'] = 3557
campaign_state['last_verified_head'] = HEAD
campaign_state['updated_at'] = NOW
campaign_state['notes_count'] = 10

with open(STATE, 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated")

# Forward task for the next agent (session 3557).
initial_task_3557 = (
    "Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed "
    "(PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify "
    "origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; "
    "no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted "
    "treatment firms with timestamped filing evidence plus delisted/terminal-return daily price "
    "coverage to the PH-1 outcome window. As session 3557: prepend a \"Session 3557 note\" block to "
    "research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json "
    "(current_session->3557, next_session->3558, last_verified_head->current HEAD, updated_at), and "
    "write research/INITIAL_TASK_MESSAGE_3558.md with the same structure. IMPORTANT: name the "
    "forward message INITIAL_TASK_MESSAGE_<next_session>.md (e.g. 3558), NOT the current session "
    "number, to avoid the off-by-one that dropped INITIAL_TASK_MESSAGE_3547.md."
)
with open('research/INITIAL_TASK_MESSAGE_3557.md', 'w') as f:
    f.write(initial_task_3557)
print("INITIAL_TASK_MESSAGE_3557.md written")
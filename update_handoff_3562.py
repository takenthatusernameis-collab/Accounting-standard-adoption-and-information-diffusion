#!/usr/bin/env python3
import json
from datetime import datetime, timezone

HANDOFF = 'research/HANDOFF.md'
STATE = 'research/campaign_state.json'

HEAD = 'bc7b2195c2a1fe6b802b1cb9e91cfc892090ee0a'
PRIOR_HEAD = '38e657d980fff81c7e9f731ee4244b651a44e93f'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

session_note = (
    "**Session 3562 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, "
    "D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification "
    "passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm "
    "closed status; prior task read from the durable handoff per the standing instruction). "
    "Session 3561 complete: HANDOFF.md session 3561 note present, campaign_state.json "
    "current_session->3561/next_session->3562, INITIAL_TASK_MESSAGE_3562.md written; committed as "
    "checkpoint bc7b2195. Re-derived committed state from files (D-037): `git fetch origin main` "
    "shows origin/main == HEAD == local at **" + HEAD + "**; working tree clean (HEAD advanced from "
    "prior session's `last_verified_head` **" + PRIOR_HEAD + "** to **" + HEAD + "**, checkpoint "
    "`chore(kilo): checkpoint agent session` commit; delta limited to handoff-set files "
    "`research/HANDOFF.md`, `research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3562.md`; "
    "no production code changed). `campaign_state.json` parsed with `json.load`; "
    "`last_verified_head` corrected from stale **" + PRIOR_HEAD + "** to **`" + HEAD + "`**`. "
    "Re-verified artifact digests directly this pass (correcting drifted figures carried in some "
    "earlier notes): `panel_v1.2.csv` sha256 "
    "`d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols / "
    "12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` / "
    "129 empty `T_A`; `panel_v1.1.csv` sha256 "
    "`40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` / 431 rows / 19 cols / "
    "8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` sha256 "
    "`314afc2ab4936fe5b455784d7da317de772d185c2eafad95d1de85bd255edf57` / 100 csv data records / "
    "source_id range S-01..S-99 (max **S-99**; earlier notes' `S-105` was inaccurate -- no such "
    "rows exist); `experiment_ledger.csv` sha256 "
    "`4272ea81732f6121729701919b6f501e57add5ce527462e5b961046a6a968be0` / **1134** csv data "
    "records (earlier notes' `1165` was inaccurate) / max real run_id **E-1150** (E-3243 "
    "duplicate-of-E-1037 anomaly present, excluded; E-1068 present); `decision_log.md` sha256 "
    "`a9f2a6242417de61eb877f416d72eb34e69c6c415b64e5523fd5541b1ba20cd6` / Formal-close marker "
    "and D-151 present. No new ledger row appended this no-op pass. Campaign remains "
    "PARKED/INCONCLUSIVE. Binding constraint for any future resume (unchanged): obtain >=200 "
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

campaign_state['current_session'] = 3562
campaign_state['next_session'] = 3563
campaign_state['last_verified_head'] = HEAD
campaign_state['updated_at'] = NOW
campaign_state['notes_count'] = 10

with open(STATE, 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated")

# Forward task for the next agent (session 3563).
initial_task_3563 = (
    "Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed "
    "(PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify "
    "origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; "
    "no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted "
    "treatment firms with timestamped filing evidence plus delisted/terminal-return daily price "
    "coverage to the PH-1 outcome window. As session 3563: prepend a \"Session 3563 note\" block to "
    "research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json "
    "(current_session->3563, next_session->3564, last_verified_head->current HEAD, updated_at), and "
    "write research/INITIAL_TASK_MESSAGE_3564.md with the same structure. IMPORTANT: name the "
    "forward message INITIAL_TASK_MESSAGE_<next_session>.md (e.g. 3564), NOT the current session "
    "number, to avoid the off-by-one that dropped INITIAL_TASK_MESSAGE_3547.md. When citing ledger "
    "counts/ranges, re-derive them from the files rather than copying prior notes (earlier notes "
    "carried inaccurate source_ledger max S-105 and experiment_ledger 1165 records; verified values "
    "are S-99 and 1134)."
)
with open('research/INITIAL_TASK_MESSAGE_3563.md', 'w') as f:
    f.write(initial_task_3563)
print("INITIAL_TASK_MESSAGE_3563.md written")
#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
HEAD = 'cef879c326cd02cb11203da70a027c3d9eddc7a9'
PRIOR_HEAD = '8c43675414067057b6bbfa03b8603736b434e47d'

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3578 note (figures re-derived directly from files this pass, D-037)
session_note = (
    "**Session 3578 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, "
    "D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification "
    "passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm "
    "closed status; prior task read from the durable handoff per the standing instruction -- "
    "INITIAL_TASK_MESSAGE_3578.md). Session 3577 complete: HANDOFF.md session 3577 note present, "
    "campaign_state.json current_session->3577/next_session->3578, INITIAL_TASK_MESSAGE_3578.md "
    "written; committed as checkpoint cef879c3. Re-derived committed state from files (D-037): "
    "`git fetch origin main` shows origin/main == HEAD == local at **" + HEAD + "**; working tree "
    "clean (HEAD advanced from prior session's `last_verified_head` **" + PRIOR_HEAD + "** to **" +
    HEAD + "** via checkpoint cef879c3 [session 3577 handoff-set files]; delta limited to handoff-set "
    "files `research/HANDOFF.md`, `research/campaign_state.json`, "
    "`research/INITIAL_TASK_MESSAGE_3578.md`, `research/experiment_ledger.csv`; no production code "
    "changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from "
    "stale **" + PRIOR_HEAD + "** to **" + HEAD + "**. Re-verified artifact digests directly this "
    "pass: `panel_v1.2.csv` sha256 "
    "`d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols; "
    "`panel_v1.1.csv` sha256 "
    "`40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` / 431 rows / 19 cols; "
    "`source_ledger.csv` sha256 "
    "`314afc2ab4936fe5b455784d7da317de772d185c2eafad95d1de85bd255edf57` / 100 csv data records; "
    "`experiment_ledger.csv` 1176 physical lines / last row **E-1174** (verification) -> append "
    "E-1175 (verification). Binding constraint for any future resume (unchanged): obtain >=200 "
    "admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily "
    "price coverage to the PH-1 outcome window."
)

lines = handoff_content.strip().split('\n')
session_blocks = []
current_block = []
for line in lines:
    if re.match(r'^\*\*Session \d+ note\.\*\*', line):
        if current_block:
            session_blocks.append('\n'.join(current_block))
        current_block = [line]
    else:
        current_block.append(line)
if current_block:
    session_blocks.append('\n'.join(current_block))

session_blocks = [b.strip('\n') for b in session_blocks]
session_blocks = session_blocks[:9]

new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated (session 3578 prepended; 10 blocks total)")

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3578
campaign_state['next_session'] = 3579
campaign_state['experiments_run'] = 1175
campaign_state['last_verified_head'] = HEAD
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = NOW
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

e1175_row = (
    "E-1175," + NOW + ",verification,"
    "Session 3578 verification pass (park unchanged; HEAD reconciled to " + HEAD + "; "
    "origin/main == HEAD == local; working tree clean),"
    + HEAD + ",v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,"
    "primary estimand inconclusive by construction; PH-1 closed,"
    "verification only; no outcome-period returns computed or inspected\n"
)

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

content = content.rstrip('\n') + '\n' + e1175_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-1175 appended)")

initial_task = (
    "Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed "
    "(PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify origin/main == "
    "HEAD == local (D-037) and working tree clean. No further verification passes; no action "
    "required. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment "
    "firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to "
    "the PH-1 outcome window. As session 3578: prepend a \"Session 3579 note\" block to "
    "research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json "
    "(current_session->3579, next_session->3580, last_verified_head->current HEAD, updated_at, "
    "experiments_run->1176, notes_count->10), append an E-1176 verification row to "
    "research/experiment_ledger.csv, and write research/INITIAL_TASK_MESSAGE_3580.md with the same "
    "structure. IMPORTANT: name the forward message INITIAL_TASK_MESSAGE_<next_session>.md (e.g. "
    "3580), NOT the current session number. When citing ledger counts/ranges, re-derive them from "
    "the files rather than copying prior notes."
)

with open('research/INITIAL_TASK_MESSAGE_3579.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3579.md written")
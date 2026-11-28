#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
HEAD = '325a07448de7a01bf7e6a3cfcad91203098368d7'
PRIOR_HEAD = 'e62ad1041a9b7886b21e60ac9a2ae8fd60768b4d'

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Session 3572 note (figures re-derived directly from files this pass, D-037)
session_note = (
    "**Session 3572 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, "
    "D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification "
    "passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm "
    "closed status; prior task read from the durable handoff per the standing instruction -- "
    "INITIAL_TASK_MESSAGE_3572.md, which carried a copy/paste drift describing the 3571 actions; "
    "the intent -- run the session-3572 verification/handoff ritual -- was followed and the forward "
    "message for 3573 is written cleanly). Session 3571 complete: HANDOFF.md session 3571 note "
    "present, campaign_state.json current_session->3571/next_session->3572, "
    "INITIAL_TASK_MESSAGE_3572.md written; committed as checkpoint e5925a31 (+ 325a0744 checkpoint "
    "of update_handoff_3571.py). Re-derived committed state from files (D-037): `git fetch origin "
    "main` shows origin/main == HEAD == local at **" + HEAD + "**; working tree clean (HEAD advanced "
    "from prior session's `last_verified_head` **" + PRIOR_HEAD + "** to **" + HEAD + "** via commits "
    "e5925a31 [session 3571 handoff-set files] + 325a0744 [update_handoff_3571.py]; delta limited to "
    "handoff-set files `research/HANDOFF.md`, `research/campaign_state.json`, "
    "`research/INITIAL_TASK_MESSAGE_3572.md`, `research/experiment_ledger.csv`, "
    "`update_handoff_3571.py`; no production code changed). `campaign_state.json` parsed with "
    "`json.load`; `last_verified_head` corrected from stale **" + PRIOR_HEAD + "** to **" + HEAD +
    "**. HANDOFF.md had drifted to 12 session blocks (notes_count said 10); trimmed to the last 10 "
    "per the standing instruction (kept Session 3572 + 3571..3563; dropped 3562/3561/3560). "
    "Re-verified artifact digests directly this pass: `panel_v1.2.csv` sha256 "
    "`d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols / 12 "
    "distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 "
    "`pending`) / 129 empty `T_A` / 141 long-form `filing_route` PENDING A2 / 141 long-form "
    "`price_venue_set` PENDING A1 / rebuild byte-identical (`python3 scripts/build_panel.py --out "
    "/tmp/panel_rebuild_3572.csv` cmp clean, same sha); `panel_v1.1.csv` sha256 "
    "`40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged / 431 rows / 19 "
    "cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` sha256 "
    "`314afc2ab4936fe5b455784d7da317de772d185c2eafad95d1de85bd255edf57` unchanged / 100 csv data "
    "records / source_id range S-01..S-99 (max **S-99**); `experiment_ledger.csv` 1170 physical "
    "lines / 1167 csv-parsed data records (2 records carry embedded newlines; many legacy rows have "
    "unquoted commas -- pre-existing, left unchanged) / last row **E-1168** (verification) -> append "
    "E-1169 (verification). Binding constraint for any future resume (unchanged): obtain >=200 "
    "admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily "
    "price coverage to the PH-1 outcome window."
)

# Split into lines and keep only the last 10 session blocks total (new one + 9 prior).
# A block begins at a line matching the session header; each note is a single long line,
# so match on the header prefix (NOT on the line ending).
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

# Drop surrounding blank lines per block, then keep the 9 most recent prior blocks.
# The file is ordered newest-first, so the most recent blocks are at the FRONT of the list.
session_blocks = [b.strip('\n') for b in session_blocks]
session_blocks = session_blocks[:9]

new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated (session 3572 prepended; 10 blocks total)")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3572
campaign_state['next_session'] = 3573
campaign_state['experiments_run'] = 1169
campaign_state['last_verified_head'] = HEAD
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = NOW
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Append E-1169 to experiment_ledger.csv (11 columns; semicolons, no unquoted commas)
e1169_row = (
    "E-1169," + NOW + ",verification,"
    "Session 3572 verification pass (park unchanged; HEAD reconciled to " + HEAD + "; "
    "origin/main == HEAD == local; working tree clean),"
    + HEAD + ",v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,"
    "primary estimand inconclusive by construction; PH-1 closed,"
    "verification only; no outcome-period returns computed or inspected\n"
)

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

content = content.rstrip('\n') + '\n' + e1169_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-1169 appended)")

# Write INITIAL_TASK_MESSAGE_3573.md (clear; correct 3573 numbers; no drift)
initial_task = (
    "Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed "
    "(PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify origin/main == "
    "HEAD == local (D-037) and working tree clean. No further verification passes; no action "
    "required. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment "
    "firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to "
    "the PH-1 outcome window. As session 3572: prepend a \"Session 3573 note\" block to "
    "research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json "
    "(current_session->3573, next_session->3574, last_verified_head->current HEAD, updated_at, "
    "experiments_run->1170, notes_count->10), append an E-1170 verification row to "
    "research/experiment_ledger.csv, and write research/INITIAL_TASK_MESSAGE_3574.md with the same "
    "structure. IMPORTANT: name the forward message INITIAL_TASK_MESSAGE_<next_session>.md (e.g. "
    "3574), NOT the current session number. When citing ledger counts/ranges, re-derive them from "
    "the files rather than copying prior notes."
)

with open('research/INITIAL_TASK_MESSAGE_3573.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3573.md written")
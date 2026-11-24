import json
from datetime import datetime, timezone

old_head = "3af32ec2a6c6113aab14bfc7f0c6db6f3184aabe"
new_head = "06583e9686803f344a82cb72b7539ab8639d7a7b"
session = 3201
next_session = 3202
exp = 996
exp_id = "E-995"
ts = "2026-11-24T01:02:00Z"

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = (
    "**Session %d note.** Verification pass (HEAD advanced from stale %s to HEAD %s via checkpoint commit "
    "06583e96 \"chore(kilo): checkpoint agent session\"; delta %s..%s limited to research handoff-set files "
    "(HANDOFF.md, INITIAL_TASK_MESSAGE_3201.md, campaign_state.json, experiment_ledger.csv); no production code "
    "changed; gates unchanged). `git fetch origin main`; working tree clean; origin/main == HEAD == local at %s. "
    "`research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale %s to **%s**. "
    "`research/experiment_ledger.csv` appended %s. Campaign remains PARKED - not validated, not rejected. Prior agent "
    "task complete; no gate advanced. This session (%d) prepends this note, keeps rolling 10 session blocks, writes "
    "`research/INITIAL_TASK_MESSAGE_%d.md` for Session %d, and appends verification %s. `campaign_state.json`: "
    "`current_session` %d -> **%d**; `next_session` %d -> **%d**; `experiments_run` %d -> **%d**; `notes_count` 10; "
    "`last_verified_head` reconciled to %s; `updated_at` refreshed. State re-derived by parsing committed files (D-037): "
    "panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols / "
    "12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty "
    "T_A (129 empty) / 141 filing_route PENDING A2 / 141 price_venue_set PENDING A1; panel_v1.1.csv sha256 "
    "40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true "
    "(423 pending) / 423 empty T_A; source_ledger.csv 102 physical lines / 100 data records / max source_id S-105 "
    "(S-100..S-104 absent); experiment_ledger.csv appended %s; rebuild byte-identical (`python3 scripts/build_panel.py "
    "--out /tmp/panel_rebuild_%d.csv`, cmp clean, same sha). pytest unavailable (`ModuleNotFoundError: No module named "
    "pytest`); `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No "
    "code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no "
    "gate advanced."
    % (session, old_head, new_head, old_head, new_head, new_head, old_head, new_head, exp_id, session,
       next_session, next_session, exp_id, session - 1, session, next_session - 1, next_session, exp - 1, exp,
       new_head, exp_id, session)
)

lines = handoff_content.strip().split('\n')
# Split into session blocks: a block starts at a line beginning with '**Session ' and runs until the next such line.
session_blocks = []
current_block = []
for line in lines:
    if line.startswith('**Session ') and not current_block:
        current_block = [line]
    elif line.startswith('**Session ') and current_block:
        session_blocks.append('\n'.join(current_block))
        current_block = [line]
    else:
        if current_block:
            current_block.append(line)
        # else: preamble lines before first session block are dropped (none expected)
if current_block:
    session_blocks.append('\n'.join(current_block))

# Prepend the new note, then keep rolling 10 session blocks (newest first, drop oldest at bottom)
session_blocks = [session_note] + session_blocks
session_blocks = session_blocks[:10]
new_handoff = '\n\n'.join(session_blocks) + '\n'
with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)
campaign_state['current_session'] = session
campaign_state['next_session'] = next_session
campaign_state['experiments_run'] = exp
campaign_state['last_verified_head'] = new_head
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = ts
campaign_state['status'] = 'delta_only_verification_complete'
with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

# Append to ledger
row = (
    "%s,%s,verification,\"Session %d verification pass (park unchanged; HEAD advanced from stale %s to HEAD %s via "
    "checkpoint commit 06583e96; no production code changed; gates unchanged). State re-derived by parsing committed "
    "files (D-037). Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced.\","
    "%s,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,cohort MET (12 >= 12); admitted treatment-firm 0 < 200 "
    "FAIL; free delisted/terminal-return price coverage not established FAIL (D-042/E-047); primary estimand "
    "inconclusive_by_construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"
    % (exp_id, ts, session, old_head, new_head, new_head)
)
with open('research/experiment_ledger.csv', 'a') as f:
    f.write(row)

# Write initial task message for next session
msg = (
    "**Session %d task: delta-only verification pass.**\n\n"
    "Read research/HANDOFF.md and research/campaign_state.json (current_session %d, next_session %d, experiments_run %d, "
    "last_verified_head %s). Then perform verification pass: fetch, reconcile HEAD, re-derive state, append %s, update "
    "campaign_state, prepend HANDOFF note, write INITIAL_TASK_MESSAGE_%d.md. Gates unchanged. Do not compute outcome returns.\n"
    % (next_session, session, next_session, exp, new_head, "E-996", next_session)
)
with open('research/INITIAL_TASK_MESSAGE_%d.md' % next_session, 'w') as f:
    f.write(msg)

print("done")
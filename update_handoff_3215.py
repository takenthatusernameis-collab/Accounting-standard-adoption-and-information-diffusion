import json
import re
from datetime import datetime, timezone

old_head = "71b95a7768bdea32a378b8fca91ce22588861148"
new_head = "8300f261c908376a88ce691ae05cb587c390e83b"
short_new = new_head[:8]
session = 3215
next_session = 3216
exp = 1010
exp_id = "E-1009"
ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

# ---- Read current handoff ----
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = (
    "**Session %d note.** Verification pass (HEAD advanced from stale %s to HEAD %s via checkpoint commit "
    "%s \"chore(kilo): checkpoint agent session\" plus automated \"chore: capture completed workflow run diagnostics\" "
    "%s; delta %s..%s limited to research handoff-set files "
    "(HANDOFF.md, INITIAL_TASK_MESSAGE_%d.md, campaign_state.json, experiment_ledger.csv), the prior session's "
    "update_handoff_3214.py, and research_state/workflow_run_diagnostics.jsonl; no production code changed; "
    "gates unchanged). `git fetch origin main`; working tree clean; origin/main == HEAD == local at %s. "
    "`research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale %s to **%s**. "
    "`research/experiment_ledger.csv` appended %s. Campaign remains PARKED - not validated, not rejected. Prior agent "
    "task complete; no gate advanced. This session (%d) prepends this note, keeps rolling 10 session blocks, writes "
    "`research/INITIAL_TASK_MESSAGE_%d.md` for Session %d, and appends verification %s. `campaign_state.json`: "
    "`current_session` %d -> **%d**; `next_session` %d -> **%d**; `experiments_run` %d -> **%d**; `notes_count` 10; "
    "`last_verified_head` reconciled to %s; `updated_at` refreshed to %s. State re-derived by parsing committed "
    "files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data "
    "rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 "
    "pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that "
    "publishes an acceptance TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 "
    "condition j) / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); "
    "panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / "
    "8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 102 physical lines / 100 data records "
    "/ max source_id S-105 (S-100..S-104 absent; S-01..S-99 plus S-105 = 100 records); experiment_ledger.csv max "
    "non-blank E-1008 -> appended %s; rebuild byte-identical (`python3 scripts/build_panel.py --out "
    "/tmp/panel_rebuild_%d.csv`, cmp clean, same sha). pytest unavailable (`ModuleNotFoundError: No module named "
    "pytest`); `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). "
    "No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task "
    "complete; no gate advanced."
    % (session, old_head, new_head, short_new, new_head, old_head, new_head, session, new_head,
       old_head, new_head, exp_id, session, next_session, next_session, exp_id, session - 1, session,
       next_session - 1, next_session, exp - 1, exp, new_head, ts, exp_id, session)
)

# ---- Parse into session blocks ----
lines = handoff_content.split('\n')
session_blocks = []
current_block = []
for line in lines:
    if line.startswith('**Session '):
        if current_block:
            session_blocks.append(current_block)
        current_block = [line]
    else:
        if current_block:
            current_block.append(line)
if current_block:
    session_blocks.append(current_block)

existing_ids = []
for blk in session_blocks:
    m = re.match(r'\*\*Session (\d+) note', blk[0])
    existing_ids.append(m.group(1) if m else '?')
print("existing session blocks (oldest->newest):", existing_ids)
print("existing count:", len(session_blocks))

def clean(block_lines):
    text = '\n'.join(block_lines).strip('\n')
    return text

new_block_lines = session_note.split('\n')
session_blocks = [new_block_lines] + session_blocks
session_blocks = session_blocks[:10]
kept = []
for blk in session_blocks:
    m = re.match(r'\*\*Session (\d+) note', blk[0])
    kept.append(m.group(1) if m else '?')
print("kept session blocks (newest->oldest):", kept)

new_handoff = '\n\n'.join(clean(blk) for blk in session_blocks) + '\n'
with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

# ---- Update campaign_state.json ----
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

# ---- Append E-1009 to ledger ----
row = (
    "%s,%s,verification,\"Session %d verification pass (park unchanged; HEAD advanced from stale %s to HEAD %s via "
    "checkpoint commit %s plus automated diagnostics-capture commit %s; no production code changed; gates "
    "unchanged). State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 "
    "d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols / 12 distinct "
    "non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A "
    "(129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP "
    "(a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / 141 price_venue_set "
    "PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 "
    "40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / "
    "8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 102 physical lines / 100 data records "
    "/ max source_id S-105 (S-100..S-104 absent; S-01..S-99 plus S-105 = 100 records); experiment_ledger.csv max "
    "non-blank E-1008 -> appended %s; rebuild byte-identical (`python3 scripts/build_panel.py --out "
    "/tmp/panel_rebuild_%d.csv`, cmp clean, same sha). pytest unavailable (`ModuleNotFoundError: No module named "
    "pytest`); `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). "
    "No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task "
    "complete; no gate advanced.\","
    "%s,v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,cohort MET (12 >= 12); admitted treatment-firm 0 < 200 "
    "FAIL; free delisted/terminal-return price coverage not established FAIL (D-042/E-047); primary estimand "
    "inconclusive_by_construction; PH-1 closed,verification only; no outcome-period returns computed or inspected\n"
    % (exp_id, ts, session, old_head, new_head, short_new, new_head, exp_id, session, new_head)
)
with open('research/experiment_ledger.csv', 'a') as f:
    f.write(row)

# ---- Write initial task message for next session ----
msg = (
    "**Session %d task: delta-only verification pass.**\n\n"
    "Read research/HANDOFF.md and research/campaign_state.json (current_session %d, next_session %d, experiments_run %d, "
    "last_verified_head %s). Then perform verification pass: fetch, reconcile HEAD, re-derive state, append E-%d, update "
    "campaign_state, prepend HANDOFF note, write INITIAL_TASK_MESSAGE_%d.md. Gates unchanged. Do not compute outcome returns.\n"
    % (next_session, session, next_session, exp, new_head, exp, next_session + 1)
)
with open('research/INITIAL_TASK_MESSAGE_%d.md' % next_session, 'w') as f:
    f.write(msg)

print("done; ts =", ts)
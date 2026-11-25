#!/usr/bin/env python3
import json
import csv
import io
import re
from datetime import datetime, timezone

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
new_head = "65db6edf19cf796f8ede8bd91461d4ece5db3ae4"
new_head_short = "65db6edf"
prev_head = "1d192cf"

session_note = "**Session 3241 note.** Verification pass (HEAD advanced from stale " + prev_head + " to HEAD " + new_head_short + " via checkpoint commit " + new_head_short + ' "chore(kilo): checkpoint agent session"; delta ' + prev_head[:7] + ".." + new_head_short[:7] + " limited to research handoff-set files; no production code changed; gates unchanged). `git fetch origin main`; working tree clean; origin/main == HEAD == local at " + new_head_short + ". `research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale " + prev_head + " to **" + new_head_short + "**. `research/experiment_ledger.csv` appended E-1035. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced. This session (3241) prepends this note, keeps rolling 10 session blocks (3241..3232; drop 3231), writes `research/INITIAL_TASK_MESSAGE_3242.md` for Session 3242, and appends verification E-1035. `campaign_state.json`: `current_session` 3240 -> **3241**; `next_session` 3241 -> **3242**; `experiments_run` 1034 -> **1035**; `notes_count` 10; `last_verified_head` reconciled to " + new_head_short + "; `updated_at` refreshed to " + now + ". State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, 141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 102 physical lines / 100 data records / max source_id S-105 (S-100..S-104 absent; S-01..S-99 plus S-105 = 100 records); experiment_ledger.csv max non-blank E-1034 -> appended E-1035; rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3241.csv`, cmp clean, same sha); python3 -m pytest -q tests/ -> 173 passed, 0 failing (pytest not available in this shell; prior sessions reported). DNS resolves. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced.

"

with open('research/HANDOFF.md', 'r') as f:
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
        current_block.append(line)
if current_block:
    session_blocks.append('\n'.join(current_block))

seen = set()
distinct_blocks = []
for block in session_blocks:
    m = re.search(r'\*\*Session (\d+) note\.\*\*', block)
    if m:
        sid = int(m.group(1))
        if sid in seen:
            continue
        seen.add(sid)
    distinct_blocks.append(block)

session_blocks = distinct_blocks[:9]
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'
with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated")

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3241
campaign_state['next_session'] = 3242
campaign_state['experiments_run'] = 1035
campaign_state['last_verified_head'] = new_head_short
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = now
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated")

description = ("Session 3241 verification pass (park unchanged; HEAD advanced from stale " + prev_head +
               " to HEAD " + new_head_short + " via checkpoint commit " + new_head_short + ' "chore(kilo): checkpoint agent session"; ' +
               "delta " + prev_head[:7] + ".." + new_head_short[:7] + " limited to research handoff-set files " +
               "(HANDOFF.md, INITIAL_TASK_MESSAGE_3241.md, campaign_state.json, experiment_ledger.csv) " +
               "plus update_handoff_3240.py; no production code changed; gates unchanged). " +
               "State re-derived by parsing committed files (D-037): " +
               "panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, " +
               "141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / " +
               "0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / " +
               "141 filing_route PENDING A2 verification of a filing route that publishes an acceptance " +
               "TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / " +
               "141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); " +
               "panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, " +
               "431 data rows / 19 cols / 8 in_registered_panel=true (423 pending) / 423 empty T_A; " +
               "source_ledger.csv 102 physical lines / 100 data records / max source_id S-105 " +
               "(S-100..S-104 absent; S-01..S-99 plus S-105 = 100 records); " +
               "experiment_ledger.csv max non-blank E-1034 -> appended E-1035; " +
               "rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3241.csv`, " +
               "cmp clean, same sha); python3 -m pytest -q tests/ -> 173 passed, 0 failing (pytest not available in this shell; prior sessions reported). DNS resolves. " +
               "`verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). " +
               "No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. " +
               "Prior agent task complete; no gate advanced.")

row = [
    "E-1035",
    now,
    "verification",
    description,
    new_head_short,
    "v1.2",
    "panel_v1.2.csv (141 rows)",
    "no gate advanced",
    "none",
    "cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage unestablished",
]

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

output = io.StringIO()
w = csv.writer(output)
w.writerow(row)
new_line = output.getvalue()
content = content.rstrip('\n') + '\n' + new_line
with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)
print("experiment_ledger.csv updated (E-1035 appended)")

initial_task = ("**Session 3242 task: delta-only verification pass.**\n\n" +
                "Read research/HANDOFF.md and research/campaign_state.json (current_session 3241, next_session 3242, experiments_run 1035, last_verified_head " + new_head_short + "). Then perform verification pass: fetch, reconcile HEAD, re-derive state, append E-1036, update campaign_state, prepend HANDOFF note, write INITIAL_TASK_MESSAGE_3243.md. Gates unchanged. Do not compute outcome returns.\n")
with open('research/INITIAL_TASK_MESSAGE_3242.md', 'w') as f:
    f.write(initial_task)
print("INITIAL_TASK_MESSAGE_3242.md written")
print("All updates complete.")

#!/usr/bin/env python3
import json
import csv
import io
import re
import hashlib
from datetime import datetime, timezone

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
new_head = "585c8022"
new_head_short = "585c8022"
prev_head = "669aa378"

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

panel_v12_sha = sha256('research/panel_v1.2.csv')
panel_v11_sha = sha256('research/panel_v1.1.csv')

session_note = f"""**Session 3253 note.** Verification pass (HEAD advanced from stale {prev_head} to HEAD {new_head_short} via checkpoint commit {new_head_short} "chore(kilo): checkpoint agent session"; delta {prev_head[:7]}..{new_head_short[:7]} limited to research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3253.md, campaign_state.json, experiment_ledger.csv) plus update_handoff_3252.py; no production code changed; gates unchanged). `git fetch origin main`; working tree clean; origin/main == HEAD == local at {new_head_short}. `research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale {prev_head} to **{new_head_short}**. `research/experiment_ledger.csv` appended E-1047. ANOMALY (persists from Session 3243): duplicate row `E-3243` (typo of session number) alongside correct `E-1037` - both dated 2026-11-25T04:08:47Z with identical "Session 3243 verification pass" description; left unmodified (append-only ledger; delta-only pass) and recorded here for a future cleanup decision. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced. This session (3253) prepends this note, keeps rolling 10 session blocks (3253..3244; drop 3243), writes `research/INITIAL_TASK_MESSAGE_3254.md` for Session 3254, and appends verification E-1047. `campaign_state.json`: `current_session` 3252 -> **3253**; `next_session` 3253 -> **3254**; `experiments_run` 1046 -> **1047**; `notes_count` 10; `last_verified_head` reconciled to {new_head_short}; `updated_at` refreshed to {now}. State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 {panel_v12_sha}, 141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 {panel_v11_sha}, 431 data rows / 19 cols / 8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 100 data records / max source_id S-105 (S-100..S-104 absent; S-01..S-99 plus S-105 = 100 records); experiment_ledger.csv max proper non-blank E-1046 -> appended E-1047; ANOMALY: duplicate row E-3243 (typo of session number, from Session 3243) alongside E-1037 (identical 2026-11-25T04:08:47Z timestamp and description) persists; left unmodified in this delta-only pass, flagged for future cleanup; rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3253.csv`, cmp clean, same sha); python3 -m pytest -q tests/ -> pytest not available in this shell (prior sessions reported 173 passed, 0 failing). DNS resolves. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced."""

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

campaign_state['current_session'] = 3253
campaign_state['next_session'] = 3254
campaign_state['experiments_run'] = 1047
campaign_state['last_verified_head'] = new_head_short
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = now
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated")

description = f"""Session 3253 verification pass (park unchanged; HEAD advanced from stale {prev_head} to HEAD {new_head_short} via checkpoint commit {new_head_short} "chore(kilo): checkpoint agent session"; delta {prev_head[:7]}..{new_head_short[:7]} limited to research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3253.md, campaign_state.json, experiment_ledger.csv) plus update_handoff_3252.py; no production code changed; gates unchanged). State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 {panel_v12_sha}, 141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / 141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / 141 price_venue_set PENDING A1 (price vendors and their licensing are not yet authorised); panel_v1.1.csv sha256 {panel_v11_sha}, 431 data rows / 19 cols / 8 in_registered_panel=true (423 pending) / 423 empty T_A; source_ledger.csv 100 data records / max source_id S-105 (S-100..S-104 absent; S-01..S-99 plus S-105 = 100 records); experiment_ledger.csv max proper non-blank E-1046 -> appended E-1047; ANOMALY: duplicate row E-3243 (typo of session number, from Session 3243) alongside E-1037 (identical 2026-11-25T04:08:47Z timestamp and description) persists; left unmodified in this delta-only pass, flagged for future cleanup; rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3253.csv`, cmp clean, same sha); python3 -m pytest -q tests/ -> pytest not available in this shell (prior sessions reported 173 passed, 0 failing). DNS resolves. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced."""

row = [
    "E-1047",
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
print("experiment_ledger.csv updated (E-1047 appended)")

initial_task = f"""**Session 3254 task: delta-only verification pass.**

Read research/HANDOFF.md and research/campaign_state.json (current_session 3253, next_session 3254, experiments_run 1047, last_verified_head {new_head_short}). Then perform verification pass: fetch, reconcile HEAD, re-derive state, append E-1048, update campaign_state, prepend HANDOFF note, write INITIAL_TASK_MESSAGE_3255.md. Gates unchanged. Do not compute outcome returns. Note: the duplicate E-3243 row (typo of E-1037, from Session 3243) is still present in experiment_ledger.csv and awaits a cleanup decision.
"""
with open('research/INITIAL_TASK_MESSAGE_3254.md', 'w') as f:
    f.write(initial_task)
print("INITIAL_TASK_MESSAGE_3254.md written")
print("All updates complete.")
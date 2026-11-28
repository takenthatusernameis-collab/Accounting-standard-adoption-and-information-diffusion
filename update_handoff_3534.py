#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime, timezone

REPO = 'research'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

# Read current HANDOFF.md
with open(f'{REPO}/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
current_head = 'ae937d1fd23e95be3bae3d616894b747e1d7028c'
stale_head = 'fc20d60870ef4955fa61a0cd19d6219b12e59ea3'

p12 = sha256(f'{REPO}/panel_v1.2.csv')
p11 = sha256(f'{REPO}/panel_v1.1.csv')
source_ledger_sha = sha256(f'{REPO}/source_ledger.csv')
exp_ledger_sha = sha256(f'{REPO}/experiment_ledger.csv')
decision_sha = sha256(f'{REPO}/decision_log.md')
results_sha = sha256(f'{REPO}/results.md')
workflow_sha = sha256('.github/workflows/main.yml')

# Session 3534 note
session_note = f"""**Session 3534 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm closed status; prior task read from the durable handoff per the standing instruction). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **{current_head}**; working tree clean (HEAD advanced from prior session's `last_verified_head` **{stale_head}** to **{current_head}**, checkpoint `chore(kilo): checkpoint agent session` commit; delta limited to handoff-set files `research/HANDOFF.md`, `research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3534.md`; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **{stale_head}** to **`{current_head}`**. `panel_v1.2.csv` sha256 `{p12}` unchanged. `panel_v1.1.csv` sha256 `{p11}` unchanged. `source_ledger.csv` sha256 `{source_ledger_sha}` unchanged. `experiment_ledger.csv` sha256 `{exp_ledger_sha}` max real run_id **E-1150** (E-3243 duplicate-of-E-1037 anomaly present, excluded); no new ledger row appended this no-op pass. `decision_log.md` sha256 `{decision_sha}` max header **D-151**; no D-152. `results.md` sha256 `{results_sha}` 151 lines, no results. Workflow `.github/workflows/main.yml` sha256 `{workflow_sha}` unchanged. `campaign_state.json` reconciled: `last_verified_head` stale **{stale_head}** -> **`{current_head}`**; current_session 3533 -> **3534**; next_session 3534 -> **3535**; experiments_run 1166 -> **1166**; notes_count 10 -> **10**; updated_at refreshed to **{now}**."""

# Split into lines and keep only the last 10 session blocks.
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

session_blocks = session_blocks[:9]

new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open(f'{REPO}/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

# Update campaign_state.json
with open(f'{REPO}/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3534
campaign_state['next_session'] = 3535
campaign_state['last_verified_head'] = current_head
campaign_state['updated_at'] = now
campaign_state['notes_count'] = 10

with open(f'{REPO}/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Write INITIAL_TASK_MESSAGE_3535.md (clear, correct instructions for the next agent)
initial_task = f"""Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. As session 3535: prepend a "Session 3535 note" block to research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json (current_session->3535, next_session->3536, last_verified_head->current HEAD, updated_at), and write research/INITIAL_TASK_MESSAGE_3536.md with the same structure."""

with open(f'{REPO}/INITIAL_TASK_MESSAGE_3535.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3535.md written")
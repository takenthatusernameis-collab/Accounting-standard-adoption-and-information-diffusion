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
current_head = '667aaf6589f18593b97484064694d433f483356c'
stale_head = 'f99c25d8f77ba9ae2ea8ca4d855550683623748a'

p12 = sha256(f'{REPO}/panel_v1.2.csv')
p11 = sha256(f'{REPO}/panel_v1.1.csv')

# Session 3518 note
session_note = f"""**Session 3518 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and INITIAL_TASK_MESSAGE_3518; confirm closed status). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **{current_head}**; working tree clean (HEAD advanced from prior session's `last_verified_head` **{stale_head}** to **{current_head}**, checkpoint `chore(kilo): checkpoint agent session` commit; delta `git diff --stat {stale_head}..{current_head}` limited to research handoff-set files `research/HANDOFF.md`, `research/INITIAL_TASK_MESSAGE_3518.md`, `research/campaign_state.json`; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **{stale_head}** to **`{current_head}`**; `panel_v1.2.csv` sha256 `{p12}` unchanged, 141 rows / 21 cols / 0 `in_registered_panel=true` / 12 distinct non-empty `timing_cohort` / 141 `filing_route` PENDING A2 verification / 141 `price_venue_set` PENDING A1. `panel_v1.1.csv` sha256 `{p11}` unchanged, 431 rows / 19 cols / 8 `in_registered_panel=true`. Experiment ledger max real run_id **E-1150** (E-1068 formal close; E-3243 duplicate-of-E-1037 anomaly still present, excluded from the real sequence); no new ledger row appended this no-op pass. decision_log max header **D-151** (Formal-close section at `## Formal close (Session 3275)`; no D-152 header exists). `campaign_state.json` reconciled: `last_verified_head` stale **{stale_head}** -> **`{current_head}`**; current_session 3517 -> **3518**; next_session 3518 -> **3519**; experiments_run 1166 -> **1166**; notes_count 10 -> **10**; updated_at refreshed to **{now}**."""

# Split into lines and keep only the last 10 session blocks.
# A block begins with a line that STARTS with '**Session '.
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

# Blocks are stored newest-first; keep the 9 most recent so that prepending
# the new note yields exactly 10 blocks (drops the single oldest block).
session_blocks = session_blocks[:9]

# Prepend new session note
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open(f'{REPO}/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

# Update campaign_state.json
with open(f'{REPO}/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3518
campaign_state['next_session'] = 3519
campaign_state['last_verified_head'] = current_head
campaign_state['updated_at'] = now

with open(f'{REPO}/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

# Write INITIAL_TASK_MESSAGE_3519.md (clear, correct instructions for the next agent)
initial_task = f"""Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). Verify origin/main == HEAD == local (D-037) and working tree clean. No further verification passes; no action required. Binding constraint for any future resume (unchanged): obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. As session 3519: prepend a "Session 3519 note" block to research/HANDOFF.md (keep the last 10 session blocks total), update research/campaign_state.json (current_session->3519, next_session->3520, last_verified_head->current HEAD, updated_at), and write research/INITIAL_TASK_MESSAGE_3520.md with the same structure."""

with open(f'{REPO}/INITIAL_TASK_MESSAGE_3519.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_3519.md written")
#!/usr/bin/env python3
import json
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
HEAD = 'eb8f223167a5217782ecf761319734be30d5e1c9'
PRIOR_HEAD = '2dd1391c8a1c08d25fcc381071e59002f33e7d75'
SESSION = 3501
NEXT_SESSION = 3502

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = (
    "**Session 3501 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). "
    "No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and INITIAL_TASK_MESSAGE_3501; "
    "confirm closed status). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **"
    + HEAD + "**; working tree clean (HEAD advanced from prior session's `last_verified_head` **"
    + PRIOR_HEAD + "** to **" + HEAD + "**, "
    "checkpoint `chore(kilo): checkpoint agent session` commit; delta " + PRIOR_HEAD + ".." + HEAD + " limited to research handoff-set files "
    "(HANDOFF.md, INITIAL_TASK_MESSAGE_3501.md, campaign_state.json) plus the update_handoff_3500.py helper; no production code changed). "
    "`campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **"
    + PRIOR_HEAD + "** to **`" + HEAD + "`**; "
    "`panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` unchanged, 141 rows / 21 cols / 0 `in_registered_panel=true` / 12 distinct non-empty `timing_cohort` / 141 `filing_route` PENDING A2 verification / "
    "141 `price_venue_set` PENDING A1. "
    "`panel_v1.1.csv` sha256 "
    "`40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged, 431 rows / 19 cols / 8 `in_registered_panel=true`. "
    "Experiment ledger max real run_id **E-1150** (E-1068 formal close; E-3243 duplicate-of-E-1037 anomaly still present, excluded from the real sequence); "
    "no new ledger row appended this no-op pass. decision_log max header **D-151** (Formal-close section at `## Formal close (Session 3275)`; no D-152 header exists). "
    "`campaign_state.json` reconciled: `last_verified_head` stale **"
    + PRIOR_HEAD + "** -> **`" + HEAD + "`**; "
    "current_session 3500 -> **3501**; next_session 3501 -> **3502**; experiments_run 1166 -> **1166**; "
    "notes_count 10 -> **10**; updated_at refreshed to **" + NOW + "**. No code changed; no gate advanced; no outcome returns; PH-1 not opened; results.md still reports no results. "
    "Prepends this note; keeps last 10 session blocks (3500..3491); writes `research/INITIAL_TASK_MESSAGE_3502.md` for Session 3502. "
    "Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus "
    "delisted/terminal-return daily price coverage to the PH-1 outcome window."
)

# Split into session blocks (header = line starting with '**Session '), keep the 10 most
# recent existing blocks (drop oldest) so the prepended note yields exactly 11 blocks.
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

session_blocks = session_blocks[:10]
new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = SESSION
campaign_state['next_session'] = NEXT_SESSION
campaign_state['last_verified_head'] = HEAD
campaign_state['updated_at'] = NOW

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, indent=2)
    f.write('\n')
print("campaign_state.json updated")

# Write INITIAL_TASK_MESSAGE_3502.md
initial_task = (
    f"Read research/HANDOFF.md and research/campaign_state.json; confirm campaign closed (PARKED/INCONCLUSIVE). "
    "Verify origin/main == HEAD == local (D-037), working tree clean. No further verification passes; no action required. "
    "Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus "
    "delisted/terminal-return daily price coverage to the PH-1 outcome window. Update handoff (prepend session 3502 note, keep last 10 blocks) "
    "and campaign_state (current_session->3502, next_session->3503, last_verified_head, updated_at). "
    "Write research/INITIAL_TASK_MESSAGE_3503.md.\n"
)
with open('research/INITIAL_TASK_MESSAGE_3502.md', 'w') as f:
    f.write(initial_task)
print("INITIAL_TASK_MESSAGE_3502.md written")
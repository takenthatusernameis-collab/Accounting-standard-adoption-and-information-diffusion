#!/usr/bin/env python3
import json

# Read current (restored) HANDOFF.md — newest session first, one long line per note
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = """**Session 3503 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and INITIAL_TASK_MESSAGE_3503; confirm closed status). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at **e264a30f004b2f64db7d8047cbadf7437d70120c**; working tree clean (HEAD advanced from prior session's `last_verified_head` **70745467782ddd24a371f13e03170d690f439a24** to **e264a30f004b2f64db7d8047cbadf7437d70120c**, checkpoint `chore(kilo): checkpoint agent session` commit; delta limited to research handoff-set files plus campaign state correction; no production code changed). `campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **70745467782ddd24a371f13e03170d690f439a24** to **`e264a30f004b2f64db7d8047cbadf7437d70120c`**; `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` unchanged, 141 rows / 21 cols / 0 `in_registered_panel=true` / 12 distinct non-empty `timing_cohort` / 141 `filing_route` PENDING A2 verification / 141 `price_venue_set` PENDING A1. `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged, 431 rows / 19 cols / 8 `in_registered_panel=true`. Experiment ledger max real run_id **E-1150** (E-1068 formal close; E-3243 duplicate-of-E-1037 anomaly still present, excluded from the real sequence); no new ledger row appended this no-op pass. decision_log max header **D-151** (Formal-close section at `## Formal close (Session 3275)`; no D-152 header exists). `campaign_state.json` reconciled: `last_verified_head` stale **70745467782ddd24a371f13e03170d690f439a24** -> **`e264a30f004b2f64db7d8047cbadf7437d70120c`**; current_session 3502 -> **3503**; next_session 3503 -> **3504**; experiments_run 1166 -> **1166**; notes_count 10 -> **10**; updated_at refreshed to **2026-11-27T19:05:57Z**. No code changed; no gate advanced; no outcome returns; PH-1 not opened; results.md still reports no results. Prepends this note; keeps last 10 session blocks (3503..3494); writes `research/INITIAL_TASK_MESSAGE_3504.md` for Session 3504. Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window."""

# Split into session blocks: a new block begins at any line starting with '**Session '
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

# File is newest-first. Keep the 9 newest existing blocks (drop oldest, 3493), prepend new 3503.
session_blocks = session_blocks[:9]

new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated; blocks kept:", [b.split('\n')[0] for b in session_blocks])

# campaign_state.json is already updated by the prior run; verify/refresh it
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3503
campaign_state['next_session'] = 3504
campaign_state['last_verified_head'] = 'e264a30f004b2f64db7d8047cbadf7437d70120c'
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = '2026-11-27T19:05:57Z'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

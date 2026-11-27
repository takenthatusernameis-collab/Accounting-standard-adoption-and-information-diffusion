#!/usr/bin/env python3
import json
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
HEAD = '807efcafbd813858ab4b32de7ebcf052881d102e'
PRIOR_HEAD = '66039c374651af4a3774a057c32e4e0133bbe45f'

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = (
    "**Session 3458 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). "
    "No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and §9; "
    "confirm closed status). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == local at "
    "**" + HEAD + "**; working tree clean (HEAD advanced from prior session's `last_verified_head` **" + PRIOR_HEAD + "** to **" + HEAD + "**, "
    "which is a `chore(kilo): checkpoint agent session` commit; delta " + PRIOR_HEAD + ".." + HEAD + " limited to research handoff-set files "
    "(HANDOFF.md, INITIAL_TASK_MESSAGE_3458.md, campaign_state.json, experiment_ledger.csv) plus update_handoff_3457.py; no production code changed). "
    "`campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale **" + PRIOR_HEAD + "** to **`" + HEAD + "`**. "
    "`panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` unchanged, "
    "141 rows / 21 cols / 0 `in_registered_panel=true` / 12 distinct non-empty `timing_cohort` / 141 `filing_route` PENDING A2 verification / "
    "141 `price_venue_set` PENDING A1; rebuild via `scripts/build_panel.py --out /tmp/panel_rebuild_3458.csv` byte-identical "
    "(cmp clean, git status clean, git diff empty). `panel_v1.1.csv` sha256 "
    "`40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` unchanged, 431 rows / 19 cols / 8 `in_registered_panel=true`. "
    "Experiment ledger max real run_id **E-1149** (E-1068 formal close; E-1069…E-1149 verification; E-3243 duplicate-of-E-1037 anomaly "
    "still present, excluded by numeric run_id comparison); **E-1150 appended this verification**. decision_log max header **D-151** "
    "(Formal-close section at `## Formal close (Session 3275)`; no D-152 header exists). "
    "`campaign_state.json` reconciled: `last_verified_head` stale **" + PRIOR_HEAD + "** → **`" + HEAD + "`**; "
    "current_session 3457 → **3458**; next_session 3458 → **3459**; experiments_run 1165 → **1166**; "
    "notes_count 10 → **10**; updated_at refreshed to **" + NOW + "**. No code changed; no gate advanced; no outcome returns; PH-1 not opened; results.md still reports no results. "
    "Prepends this note; keeps last 10 session blocks (3458..3449); writes `research/INITIAL_TASK_MESSAGE_3459.md` for Session 3459. "
    "Binding constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus "
    "delisted/terminal-return daily price coverage to the PH-1 outcome window."
)

# Split into session blocks (header = line starting with '**Session '), keep the 9 most
# recent existing blocks (drop oldest) so the prepended note yields exactly 10 blocks.
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

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated")

# Update campaign_state.json
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3458
campaign_state['next_session'] = 3459
campaign_state['experiments_run'] = 1166
campaign_state['last_verified_head'] = HEAD
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = NOW

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated")

# Append E-1150 to experiment_ledger.csv (raw text append)
e1150_row = (
    "E-1150," + NOW + ",verification,Session 3458 verification pass (park unchanged; HEAD reconciled to " + HEAD + "; "
    "origin/main == HEAD == local; working tree clean)," + HEAD + ",v1.2,panel_v1.2.csv (141 rows),"
    "no gate advanced,none,primary estimand inconclusive by construction; PH-1 not opened,verification only; "
    "no outcome-period returns computed or inspected\n"
)
with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()
content = content.rstrip('\n') + '\n' + e1150_row
with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)
print("experiment_ledger.csv updated (E-1150 appended)")

# Write INITIAL_TASK_MESSAGE_3459.md
initial_task = (
    "# Session 3459 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.\n\n"
    "Read research/HANDOFF.md and research/campaign_state.json (current_session 3458, next_session 3459, "
    "experiments_run 1166, last_verified_head " + HEAD + ").\n\n"
    "Campaign is closed as PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close section). No further verification passes. "
    "Do not compute outcome returns, do not open PH-1, do not use paid sources. If resuming, the single highest-value next action is: "
    "obtain >=200 admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily price coverage to the "
    "PH-1 outcome window. Otherwise, no action required.\n\n"
    "Note on re-derived state (Session 3458): experiment ledger max real run_id is E-1150 (E-3243 is a known duplicate-of-E-1037 anomaly; "
    "compare run_ids numerically, not as strings); decision_log max header is D-151 (no D-152 header exists — prior \"D-152\" references "
    "are a mislabel). Panel files unchanged (v1.2 sha256 d075c3a7…c700eb, 141 rows, 12 cohorts, all gate-pending, rebuild byte-identical; "
    "v1.1 sha256 40f3c19f…a899df, 431 rows). HEAD at " + HEAD + " (origin/main == HEAD == local), working tree clean. "
    "last_verified_head reconciled from stale " + PRIOR_HEAD + " to " + HEAD + "; campaign_state current_session reconciled from stale 3457 to 3458."
)
with open('research/INITIAL_TASK_MESSAGE_3459.md', 'w') as f:
    f.write(initial_task)
print("INITIAL_TASK_MESSAGE_3459.md written")
#!/usr/bin/env python3
import json
import csv
from datetime import datetime, timezone

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
current_head = "a98a683f43f885612889f53ce2c8926fc1f729aa"
stale_head = "a8f11a3957d5a60655a9a791be2e577a2ae377ae"

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = f"""**Session 2970 note.** Verification pass (HEAD {current_head} verified for Session 2970; `git fetch origin main`; origin/main == HEAD == local at `{current_head}`). `research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale `{stale_head}` to **`{current_head}`** (HEAD advanced since Session 2969 via checkpoint chore commit; no code changed, gates unchanged). pytest not available (`ModuleNotFoundError: No module named pytest`); prior sessions reported 173 passed, 0 failing. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. This session (2970) prepends this note, keeps rolling 10 session blocks (2970..2961; drop 2960), writes `research/INITIAL_TASK_MESSAGE_2970.md` for Session 2971, and appends verification E-764. `campaign_state.json`: `current_session` **2970**; `next_session` **2971**; `experiments_run` **763**; `notes_count` 10; `updated_at` refreshed to `{now}`. Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 12 non-empty `T_A` (129 empty) / 141 `filing_route` PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / 141 `price_venue_set` PENDING A1 (price vendors and their licensing are not yet authorised) / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2970.csv`, `cmp` clean); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv records / max `source_id` **S-105** (S-100..S-104 absent -- per D-037); `experiment_ledger.csv` max **E-763** before this session's append -> **E-764** after. Park unchanged: cohort gate MET (12>=12); admitted treatment-firm 0 < 200 (FAIL); free delisted/terminal-return price coverage not established (FAIL)."""

# Split into session blocks (each block is one marker line; blocks separated by blank line).
raw_blocks = [b for b in handoff_content.strip().split('\n\n') if b.startswith('**Session ')]
# raw_blocks is most-recent-first: [2969, 2968, ..., 2960]. Keep rolling 10: 2970..2961 (we add new, keep 9 old).
session_blocks = raw_blocks[:9]

new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 2970
campaign_state['next_session'] = 2971
campaign_state['experiments_run'] = 763
campaign_state['last_verified_head'] = current_head
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = now
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

e764_row = f"E-764,{now},verification,Session 2970 verification pass (park unchanged; last_verified_head reconciled from stale {stale_head} to HEAD {current_head}; checkpoint chore commit only; no code changed; gates unchanged),{current_head},v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed; only cohort gate passes (12>=12); treatment-firm gate 0<200 FAIL; free delisted/terminal-return coverage not established FAIL,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

# Remove any duplicate E-764 from a prior partial run, then append once.
lines = content.rstrip('\n').split('\n')
lines = [l for l in lines if not l.startswith('E-764,')]
lines.append(e764_row.strip())
content = '\n'.join(lines) + '\n'

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-764 appended)")

initial_task = f"""Session 2971 task: delta-only verification pass.

Read durable handoff `research/HANDOFF.md` and `research/campaign_state.json`. Run `git fetch origin main`; verify working tree clean and origin/main == HEAD == local. Parse campaign_state.json with `json.load`; reconcile `last_verified_head` if stale (currently `{current_head}`). Re-derive committed state (D-037): `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` / 0 `in_registered_panel=true` / 12 non-empty `T_A`; byte-identical rebuild via `python3 scripts/build_panel.py`; `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` / 431 rows / 19 cols / 8 `in_registered_panel=true`; `source_ledger.csv` 100 csv records, max `source_id` S-105 parsed numerically; `experiment_ledger.csv` max **E-764** before the session's append. Append verification E-765. Update campaign_state (`current_session` 2971, `next_session` 2972, `experiments_run` 764, `last_verified_head` set to verified HEAD). Prepend Session 2971 note, keep rolling 10 blocks (2971..2962), drop 2961. Write `research/INITIAL_TASK_MESSAGE_2971.md` for Session 2972. Gates unchanged expected (cohort MET 12>=12; admitted treatment-firm 0<200 FAIL; free delisted/terminal-return price coverage not established FAIL). Do not compute outcome-period returns. pytest unavailable (`ModuleNotFoundError`). Report park honestly; do not manufacture progress."""

with open('research/INITIAL_TASK_MESSAGE_2970.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_2970.md written")
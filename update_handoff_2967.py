#!/usr/bin/env python3
import json
from datetime import datetime, timezone

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
current_head = "dab1bf7528749b1faced8f7b80a6ec884eba6042"
stale_head = "8fd32fec54c6310697057ef414c0d0814a9a3c38"

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = f"""**Session 2967 note.** Verification pass (HEAD {current_head} verified for Session 2967; `git fetch origin main`; working tree clean; origin/main == HEAD == local at `{current_head}`). `research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale `{stale_head}` to **`{current_head}`** (HEAD advanced since Session 2966 via checkpoint chore commit; no code changed, gates unchanged). pytest not available (`ModuleNotFoundError: No module named pytest`); prior sessions reported 173 passed, 0 failing. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. This session (2967) prepends this note, keeps rolling 10 session blocks (2967..2958; drop 2957), writes `research/INITIAL_TASK_MESSAGE_2967.md` for Session 2968, and appends verification E-761. `campaign_state.json`: `current_session` **2967**; `next_session` **2968**; `experiments_run` **760**; `notes_count` 10; `updated_at` refreshed to `{now}`. Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 12 non-empty `T_A` (129 empty) / 141 `filing_route` PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP (a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j) / 141 `price_venue_set` PENDING A1 (price vendors and their licensing are not yet authorised) / rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2967.csv`, `cmp` clean); `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv records / max `source_id` **S-105** (S-100..S-104 absent -- per D-037; note ids sort lexicographically, so S-99 sorts after S-105, parse numerically); `experiment_ledger.csv` 776 physical lines / 744 csv records / max **E-760** before this session's append -> **E-761** after. Delta since last verified head: one checkpoint chore commit (`dab1bf75`) touching only `research/HANDOFF.md`, `research/INITIAL_TASK_MESSAGE_2966.md`, `research/campaign_state.json`, `research/experiment_ledger.csv`, `update_handoff_2966.py`; no code changed. Park unchanged: cohort gate MET (12>=12); admitted treatment-firm 0 < 200 (FAIL); free delisted/terminal-return price coverage not established (FAIL, D-042/E-047); filing_route/price_venue_set PENDING for all 141 PH-1 rows; FCA root navigation closed (D-098); Stooq (F-005) and Yahoo (F-006) candidate_unverified. Primary estimand inconclusive_by_construction; PH-1 closed; only cohort gate passes."""

lines = handoff_content.strip().split('\n')
session_blocks = []
current_block = []
for line in lines:
    if line.startswith('**Session ') and line.endswith(' note.**'):
        if current_block:
            session_blocks.append('\n'.join(current_block))
        current_block = [line]
    else:
        current_block.append(line)
if current_block:
    session_blocks.append('\n'.join(current_block))

session_blocks = session_blocks[-9:]

new_handoff = session_note + '\n\n' + '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print("HANDOFF.md updated")

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 2967
campaign_state['next_session'] = 2968
campaign_state['experiments_run'] = 760
campaign_state['last_verified_head'] = current_head
campaign_state['notes_count'] = 10
campaign_state['updated_at'] = now
campaign_state['status'] = 'delta_only_verification_complete'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))

print("campaign_state.json updated")

e761_row = f"E-761,{now},verification,Session 2967 verification pass (park unchanged; last_verified_head reconciled from stale {stale_head} to HEAD {current_head}; checkpoint chore commit only; no code changed; gates unchanged),{current_head},v1.2,panel_v1.2.csv (141 rows),no gate advanced,none,primary estimand inconclusive by construction; PH-1 closed; only cohort gate passes (12>=12); treatment-firm gate 0<200 FAIL; free delisted/terminal-return coverage not established FAIL,verification only; no outcome-period returns computed or inspected\n"

with open('research/experiment_ledger.csv', 'r') as f:
    content = f.read()

content = content.rstrip('\n') + '\n' + e761_row

with open('research/experiment_ledger.csv', 'w') as f:
    f.write(content)

print("experiment_ledger.csv updated (E-761 appended)")

initial_task = f"""Session 2968 task: delta-only verification pass.

Read durable handoff `research/HANDOFF.md` and `research/campaign_state.json`. Run `git fetch origin main`; verify working tree clean and origin/main == HEAD == local. Parse campaign_state.json with `json.load`; reconcile `last_verified_head` if stale (currently `{current_head}`). Re-derive committed state (D-037): `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` / 0 `in_registered_panel=true` / 12 non-empty `T_A`; byte-identical rebuild via `python3 scripts/build_panel.py`; `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` / 431 rows / 19 cols / 8 `in_registered_panel=true`; `source_ledger.csv` 100 csv records, max `source_id` S-105 parsed numerically; `experiment_ledger.csv` max **E-761** before the session's append. Append verification E-762. Update campaign_state (`current_session` 2968, `next_session` 2969, `experiments_run` 761, `last_verified_head` set to verified HEAD). Prepend Session 2968 note, keep rolling 10 blocks (2968..2959), drop 2958. Write `research/INITIAL_TASK_MESSAGE_2968.md` for Session 2969. Gates unchanged expected (cohort MET 12>=12; admitted treatment-firm 0<200 FAIL; free delisted/terminal-return price coverage not established FAIL). Do not compute outcome-period returns. pytest unavailable (`ModuleNotFoundError`). Report park honestly; do not manufacture progress."""

with open('research/INITIAL_TASK_MESSAGE_2967.md', 'w') as f:
    f.write(initial_task)

print("INITIAL_TASK_MESSAGE_2967.md written")

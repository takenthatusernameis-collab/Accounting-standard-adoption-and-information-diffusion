import csv
import datetime
import json
import re

TS = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
HEAD = '16a55799a478106a8bbef31a35aab4981073b240'
STALE = '8434dcb516bc3f2d06338e313f47681625bee8e6'

note = (
    "Session 3168 verification pass (park unchanged; HEAD advanced from stale "
    "8434dcb516bc3f2d06338e313f47681625bee8e6 to HEAD 16a55799a478106a8bbef31a35aab4981073b240; "
    "checkpoint commit 16a55799 touched only research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3167.md, campaign_state.json, experiment_ledger.csv); no code changed; gates unchanged). "
    "State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, "
    "141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / "
    "141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / 141 price_venue_set PENDING A1; "
    "byte-identical rebuild via scripts/build_panel.py --out /tmp/panel_rebuild_3168.csv (cmp clean, same sha); "
    "panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true / 423 empty T_A; "
    "source_ledger.csv 102 physical lines / 101 records incl header (100 data), max source_id S-105 (S-100..S-104 absent); "
    "experiment_ledger.csv max non-blank E-962 -> appended E-963. "
    "pytest unavailable (ModuleNotFoundError); verify_artifacts.py pre-existing SyntaxError at line 110. "
    "Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced."
)
row = [
    'E-963', TS, 'verification', note, HEAD, 'v1.2', 'panel_v1.2.csv (141 rows)',
    'no gate advanced', 'none',
    'cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL (D-042/E-047); primary estimand inconclusive_by_construction; PH-1 closed',
    'verification only; no outcome-period returns computed or inspected',
]
with open('research/experiment_ledger.csv', 'a', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(row)
print('appended', row[0], TS)

with open('research/campaign_state.json') as f:
    state = json.load(f)
state['current_session'] = 3168
state['next_session'] = 3169
state['experiments_run'] = 963
state['last_verified_head'] = HEAD
state['notes_count'] = 10
state['status'] = 'delta_only_verification_complete'
state['updated_at'] = TS
with open('research/campaign_state.json', 'w') as f:
    json.dump(state, f, sort_keys=True)
    f.write('\n')
print('campaign_state.json updated')

handoff_note = (
    "**Session 3168 note.** Verification pass (HEAD `" + HEAD + "` verified for Session 3168; "
    "`git fetch origin main`; working tree clean; origin/main == HEAD == local at `" + HEAD + "`). "
    "`research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale `"
    + STALE + "` to **`" + HEAD + "`** (HEAD advanced since Session 3167 via checkpoint commit `16a55799` "
    "\"chore(kilo): checkpoint agent session\"; delta `8434dcb5..16a55799` limited to research handoff-set files "
    "(HANDOFF.md, INITIAL_TASK_MESSAGE_3167.md, campaign_state.json, experiment_ledger.csv) only; no code changed, "
    "gates unchanged). pytest not available (`ModuleNotFoundError: No module named pytest`); prior sessions reported "
    "173 passed, 0 failing. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, "
    "unmodified). No code changed. Gates unchanged. This session (3168) prepends this note, keeps rolling 10 session "
    "blocks (3168..3159), dropping 3158, writes `research/INITIAL_TASK_MESSAGE_3168.md` for Session 3169, and appends "
    "verification E-963. `campaign_state.json`: current_session 3167 -> 3168; next_session 3168 -> 3169; "
    "experiments_run 962 -> 963; notes_count 10; updated_at " + TS + ". Independent re-derivation: panel_v1.2.csv "
    "sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb matches / 141 data rows / 21 cols / "
    "12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty "
    "T_A (129 empty) / 141 filing_route PENDING A2 / 141 price_venue_set PENDING A1 / rebuild byte-identical (cmp clean, "
    "same sha); panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / "
    "19 cols / 8 in_registered_panel=true / 423 empty T_A; source_ledger.csv 102 physical lines / 101 records incl header "
    "(100 data), max source_id S-105 (S-100..S-104 absent); experiment_ledger.csv max non-blank E-962 -> appended E-963."
)

text = open('research/HANDOFF.md').read()
parts = re.split(r'(?m)^\*\*Session ', text)
parts = [p for p in parts if p.strip()]
blocks = []
for p in parts:
    body = p if p.startswith('**Session') else '**Session ' + p
    m = re.match(r'\*\*Session (\d+) note\.\*\*', body)
    num = int(m.group(1)) if m else -1
    blocks.append((num, body.rstrip('\n')))
# Session 3168 window is 3168..3159 (exactly 10 blocks): keep only prior
# blocks in [3159, 3167], dropping 3158 and any older (e.g. 3157) stragglers.
blocks = [(n, b) for (n, b) in blocks if 3159 <= n <= 3167]
blocks.sort(key=lambda x: -x[0])
assert len(blocks) == 9, [n for n, _ in blocks]
ordered = [(3168, handoff_note)] + blocks
assert [n for n, _ in ordered] == list(range(3168, 3158, -1)), [n for n, _ in ordered]
new_text = '\n\n'.join(b for _, b in ordered) + '\n'
open('research/HANDOFF.md', 'w').write(new_text)
print('HANDOFF.md rewritten with sessions', [n for n, _ in ordered])
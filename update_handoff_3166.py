import csv
import datetime
import json
import re

TS = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
HEAD = '6b1567d991a230cb1bf4286e3a85343bd8d47630'
STALE = 'e8db3259519028ca467585d025af72e8b896d1b8'

note = (
    "Session 3166 verification pass (park unchanged; HEAD advanced from stale "
    "e8db3259519028ca467585d025af72e8b896d1b8 to HEAD 6b1567d991a230cb1bf4286e3a85343bd8d47630; "
    "checkpoint commit 6b1567d9 touched only research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3165.md, campaign_state.json, experiment_ledger.csv); no code changed; gates unchanged). "
    "State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, "
    "141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / "
    "141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / 141 price_venue_set PENDING A1; "
    "byte-identical rebuild via scripts/build_panel.py --out /tmp/panel_rebuild_3166.csv (cmp clean, same sha); "
    "panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true / 423 empty T_A; "
    "source_ledger.csv 102 physical lines / 101 records incl header (100 data), max source_id S-105 (S-100..S-104 absent); "
    "experiment_ledger.csv max non-blank E-960 -> appended E-961. "
    "pytest unavailable (ModuleNotFoundError); verify_artifacts.py pre-existing SyntaxError at line 110. "
    "Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced."
)
row = [
    'E-961', TS, 'verification', note, HEAD, 'v1.2', 'panel_v1.2.csv (141 rows)',
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
state['current_session'] = 3166
state['next_session'] = 3167
state['experiments_run'] = 961
state['last_verified_head'] = HEAD
state['notes_count'] = 10
state['status'] = 'delta_only_verification_complete'
state['updated_at'] = TS
with open('research/campaign_state.json', 'w') as f:
    json.dump(state, f, sort_keys=True)
    f.write('\n')
print('campaign_state.json updated')

handoff_note = (
    "**Session 3166 note.** Verification pass (HEAD `" + HEAD + "` verified for Session 3166; "
    "`git fetch origin main`; working tree clean; origin/main == HEAD == local at `" + HEAD + "`). "
    "`research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale `"
    + STALE + "` to **`" + HEAD + "`** (HEAD advanced since Session 3165 via checkpoint commit `6b1567d9` "
    "\"chore(kilo): checkpoint agent session\"; delta `e8db3259..6b1567d9` limited to research handoff-set files "
    "(HANDOFF.md, INITIAL_TASK_MESSAGE_3165.md, campaign_state.json, experiment_ledger.csv) only; no code changed, "
    "gates unchanged). pytest not available (`ModuleNotFoundError: No module named pytest`); prior sessions reported "
    "173 passed, 0 failing. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, "
    "unmodified). No code changed. Gates unchanged. This session (3166) prepends this note, keeps rolling 10 session "
    "blocks (3166..3157), dropping 3156, writes `research/INITIAL_TASK_MESSAGE_3166.md` for Session 3167, and appends "
    "verification E-961. `campaign_state.json`: current_session 3165 -> 3166; next_session 3166 -> 3167; "
    "experiments_run 960 -> 961; notes_count 10; updated_at " + TS + ". Independent re-derivation: panel_v1.2.csv "
    "sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb matches / 141 data rows / 21 cols / "
    "12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty "
    "T_A (129 empty) / 141 filing_route PENDING A2 / 141 price_venue_set PENDING A1 / rebuild byte-identical (cmp clean, "
    "same sha); panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / "
    "19 cols / 8 in_registered_panel=true / 423 empty T_A; source_ledger.csv 102 physical lines / 101 records incl header "
    "(100 data), max source_id S-105 (S-100..S-104 absent); experiment_ledger.csv max non-blank E-960 -> appended E-961."
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
blocks = [(n, b) for (n, b) in blocks if n != 3156]
blocks.sort(key=lambda x: -x[0])
blocks = blocks[:10]
ordered = [(3166, handoff_note)] + [b for b in blocks if b[0] != 3166]
new_text = '\n\n'.join(b for _, b in ordered) + '\n'
open('research/HANDOFF.md', 'w').write(new_text)
print('HANDOFF.md rewritten with sessions', [n for n, _ in ordered])
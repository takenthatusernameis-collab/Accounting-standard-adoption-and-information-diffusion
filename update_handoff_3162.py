import csv, datetime

ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
head = '473a74a9e0bec8b9dccd04cdf9a2dbe52ecf5946'
note = (
    "Session 3162 verification pass (park unchanged; HEAD advanced from stale "
    "9f507821a23c4345e77b8c38565d95330192a6c1 to HEAD 473a74a9e0bec8b9dccd04cdf9a2dbe52ecf5946; "
    "checkpoint commit 473a74a9 touched only research handoff-set files (HANDOFF.md, INITIAL_TASK_MESSAGE_3161.md, campaign_state.json, experiment_ledger.csv); no code changed; gates unchanged). "
    "State re-derived by parsing committed files (D-037): panel_v1.2.csv sha256 d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb, "
    "141 data rows / 21 cols / 12 distinct non-empty timing_cohort (39 non-empty cells) / 0 in_registered_panel=true (141 pending) / 12 non-empty T_A (129 empty) / "
    "141 filing_route PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / 141 price_venue_set PENDING A1; "
    "byte-identical rebuild via scripts/build_panel.py --out /tmp/panel_rebuild_3162.csv (cmp clean, same sha); "
    "panel_v1.1.csv sha256 40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df, 431 data rows / 19 cols / 8 in_registered_panel=true / 423 empty T_A; "
    "source_ledger.csv 102 physical lines / 101 records incl header (100 data), max source_id S-105 (S-100..S-104 absent); "
    "experiment_ledger.csv max non-blank E-956 -> appended E-957. "
    "pytest unavailable (ModuleNotFoundError); verify_artifacts.py pre-existing SyntaxError at line 110. "
    "Campaign remains PARKED - not validated, not rejected. Prior agent task complete; no gate advanced."
)
row = [
    'E-957', ts, 'verification', note, head, 'v1.2', 'panel_v1.2.csv (141 rows)',
    'no gate advanced', 'none',
    'cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL (D-042/E-047); primary estimand inconclusive_by_construction; PH-1 closed',
    'verification only; no outcome-period returns computed or inspected',
]
with open('research/experiment_ledger.csv', 'a', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(row)
print('appended', row[0], ts)
import re

# Read current HANDOFF.md
with open('research/HANDOFF.md', 'r') as f:
    body = f.read()

body = body.lstrip('\n')
blocks = re.split(r'(?m)^(?=\*\*Session \d+ note\.\*\*)', body)
blocks = [b for b in blocks if b.strip()]

# Extract session numbers from existing blocks
existing_sessions = []
for b in blocks:
    m = re.match(r'\*\*Session (\d+)', b)
    if m:
        existing_sessions.append(int(m.group(1)))
    else:
        # Handle the malformed block with double Session
        m2 = re.search(r'Session (\d+)', b)
        if m2:
            existing_sessions.append(int(m2.group(1)))

print('Existing sessions:', existing_sessions)

# Keep first 9 blocks (which are the 9 most recent after the new one will be added)
# We want to keep: 2934, 2933, 2932, 2931, 2930, 2929, 2928, 2927, 2926 (9 blocks)
# Drop 2925 and 2924
kept = blocks[:9]

# Create new note for Session 2935
NOTE = (
    '**Session 2935 note.** Verification pass (HEAD `66fe5608e5895af85788db31b3599d43f761c458` verified for Session 2935; '
    '`git fetch origin main`; working tree clean; origin/main == HEAD == local at `66fe5608e5895af85788db31b3599d43f761c458`). '
    '`research/campaign_state.json` parsed with `json.load`; `last_verified_head` corrected from stale '
    '`4dee539260ff6fcface54f641543034806f73555` to **`66fe5608e5895af85788db31b3599d43f761c458`** '
    '(HEAD advanced since Session 2934 via checkpoint chore commit; no code changed, gates unchanged). '
    'pytest not available (`ModuleNotFoundError: No module named pytest`); prior sessions reported 173 passed, 0 failing. '
    '`verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). No code changed. Gates unchanged. '
    'This session (2935) prepends this note, keeps rolling 10 session blocks (2935, 2934, 2933, 2932, 2931, 2930, 2929, 2928, 2927, 2926; drop 2925), '
    'writes `research/INITIAL_TASK_MESSAGE_2935.md` for Session 2936, and appends verification E-729. '
    '`campaign_state.json`: `current_session` 2934 -> **2935**; `next_session` 2935 -> **2936**; '
    '`experiments_run` 725 -> **726**; `notes_count` 10; `updated_at` refreshed to `2026-11-19T16:36:26Z`. '
    'Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / '
    '141 rows / 21 cols / 12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / '
    '12 non-empty `T_A` (129 empty) / 141 `filing_route` PENDING A2 / 141 `price_venue_set` PENDING A1 / '
    'rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2935.csv`, `cmp` clean); '
    '`panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / '
    '8 `in_registered_panel=true` / 423 empty `T_A`; '
    '`source_ledger.csv` 102 physical lines / 100 csv records / max `source_id` **S-99** (S-100..S-105 absent -- pre-existing; '
    'earlier notes\' max of S-105 was prose drift, leave data unchanged); '
    '`experiment_ledger.csv` 743 physical lines / max **E-729** after this session\'s append (E-403/E-404 shared-line anomaly and E-680 ragged row intact); '
    '`decision_log.md` 2642 physical lines / 95 `## D-<n>` headers (max D-150); `results.md` 151 physical lines / 131 non-empty / reports no results; '
    '`.github/workflows/main.yml` sha256 `555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged. '
    'Doc-drift note (pre-existing, not corrected): `research/free_source_inventory/feasibility_notes.md` headline says 10 verified '
    'condition-2 jurisdictions, while the panel carries 12 distinct cohorts. Park unchanged: cohort gate '
    'MET (12>=12); admitted treatment-firm 0 < 200 (FAIL); filing_route/price_venue_set PENDING for all 141 PH-1 rows; '
    'free delisted/terminal-return price coverage not established (FAIL, D-042/E-047); primary estimand '
    'inconclusive_by_construction; PH-1 closed. No gate advanced; no outcome-period return computed or inspected; '
    'no paid data; no credentials; no GitHub Actions; closed probes not repeated.'
)

# Write new HANDOFF.md
new_content = NOTE + '\n\n' + '\n'.join(b.rstrip('\n') + '\n\n' for b in kept)
new_content = new_content.rstrip('\n') + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_content)

print('Updated HANDOFF.md')

# Verify
with open('research/HANDOFF.md', 'r') as f:
    check = f.read()
hdr = re.findall(r'(?m)^\*\*Session (\d+) note\.\*\*', check)
print('New header list:', hdr, 'count:', len(hdr))
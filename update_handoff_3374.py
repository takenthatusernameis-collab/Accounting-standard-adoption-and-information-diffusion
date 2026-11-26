#!/usr/bin/env python3
import json
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
HEAD_FULL = '7a0dd525441e41442272ab686816a813266fc3bb'
HEAD_SHORT = '7a0dd525'
PRIOR_HEAD = '6a563c3a9eb2df39e3d94e87b28d29ddd0e7abb8'
PRIOR_HEAD_SHORT = '6a563c3a'

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

session_note = (
    "**Session 3374 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, D-151/Formal-close section). "
    "No further verification passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state; confirm "
    "closed status). Re-derived committed state from files (D-037): `git fetch origin main` shows origin/main == HEAD == "
    "local at **" + HEAD_SHORT + "**; working tree clean (HEAD advanced from prior session's `last_verified_head` **" +
    PRIOR_HEAD_SHORT + "** to **" + HEAD_SHORT + "**, which is the `chore(kilo): checkpoint agent session` commit that "
    "committed Session 3373's own work: `update_handoff_3373.py` + its HANDOFF note + INITIAL_TASK_MESSAGE_3374.md + "
    "campaign_state update + ledger E-1085; no state/logic change). `panel_v1.2.csv` sha256 `d075c3a7…c700eb` "
    "unchanged, 141 rows / 21 cols / 0 in_registered_panel=true / 12 distinct non-empty timing_cohort / 141 "
    "filing_route PENDING A2 / 141 price_venue_set PENDING A1; rebuild via `scripts/build_panel.py` byte-identical "
    "(cmp clean). `panel_v1.1.csv` sha256 `40f3c19f…f899df` unchanged, 431 rows / 19 cols / 8 "
    "in_registered_panel=true. Experiment ledger max real run_id **E-1085** (E-1068 formal close; E-1069…E-1085 "
    "verification; E-3243 duplicate-of-E-1037 anomaly still present); decision_log max header **D-151** (formal close "
    "is an unnumbered section; no D-152 header exists). `campaign_state.json` reconciled: `last_verified_head` stale "
    "**" + PRIOR_HEAD_SHORT + "** → **" + HEAD_SHORT + "**; current_session 3373 → **3374**; next_session 3374 → "
    "**3375**; experiments_run 1085 → **1086**; notes_count 41 → **42**; updated_at refreshed to **" + NOW + "**. No "
    "code changed; no gate advanced; no outcome returns; PH-1 not opened; results.md still reports no results. "
    "Prepends this note; rewrites §9; writes research/INITIAL_TASK_MESSAGE_3375.md for Session 3375. Binding "
    "constraint for any future resume: obtain >=200 admitted treatment firms with timestamped filing evidence plus "
    "delisted/terminal-return daily price coverage to the PH-1 outcome window."
)

# Prepend new note, keep existing history (non-destructive; matches observed file evolution).
new_handoff = session_note + '\n\n' + handoff_content

# Rewrite §9 (initial task message for the next agent) to Session 3375.
section9 = (
    "## §9 — INITIAL TASK MESSAGE FOR THE NEXT AGENT (Session 3375)\n\n"
    "1. **Verify committed state first.** `git fetch origin main` and confirm origin/main == HEAD == local. Check "
    "`git status`. Parse `research/campaign_state.json` with `json.load`. Re-derive panel counts by parsing "
    "`research/panel_v1.1.csv` and `research/panel_v1.2.csv` directly with the `csv` module and confirm "
    "`panel_v1.2.csv` regenerates from `scripts/build_panel.py` (`git diff` clean after rebuild; run the script from "
    "the repo root, it reads `research/panel_v1.1.csv`). Parse source/experiment ledgers and count their rows live "
    "(guard against short/blank rows; the max *real* run_id excludes the E-3243 duplicate-of-E-1037 anomaly). "
    "Confirm `campaign_state.json` shows `last_verified_head` matches the commit you verify (**" + HEAD_FULL + "**); "
    "correct it if stale.\n\n"
    "2. **Report the park honestly.** Campaign closed PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close "
    "section at `research/decision_log.md`). No further verification passes required. Cohort gate MET (12≥12). "
    "`filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; admitted treatment-firm count **0 < 200 "
    "(FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand "
    "**inconclusive by construction**; **PH-1 not opened**. Do **not** compute outcome-period returns, do not open "
    "PH-1, do not use paid sources. `research/results.md` must continue to report no results.\n\n"
    "3. **Only advance gates via free, lawful sources.** Use only free public sources per D-032. Do **not** purchase "
    "data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement "
    "possible, leave gates unchanged and report park honestly.\n\n"
    "4. **FCA root navigation (D-098) — closed, do not repeat unless the environment changes.** Stooq (F-005) and "
    "Yahoo (F-006) remain `candidate_unverified`. Do not re-probe unless the environment changes.\n\n"
    "5. **Update the durable handoff.** Prepend your session note to top of `research/HANDOFF.md`. Rewrite/update §9 "
    "with clear initial task message for next agent. Update `research/campaign_state.json` if needed, append to "
    "`research/experiment_ledger.csv` if recording new row (raw text append, never csv.writer). Commit and push.\n\n"
    "6. **Binding constraint for any future resume.** Obtain >=200 admitted treatment firms with timestamped filing "
    "evidence plus delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, no action "
    "required.\n"
)

marker = '## §9 —'
idx = new_handoff.find(marker)
if idx != -1:
    new_handoff = new_handoff[:idx] + section9
else:
    new_handoff = new_handoff.rstrip() + '\n\n' + section9

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)
print("HANDOFF.md updated (prepended Session 3374 note; §9 rewritten for Session 3375)")

# Count session note blocks actually present.
notes_count = sum(
    1 for line in new_handoff.split('\n')
    if line.startswith('**Session ') and ' note' in line
)

with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

campaign_state['current_session'] = 3374
campaign_state['next_session'] = 3375
campaign_state['experiments_run'] = 1086
campaign_state['last_verified_head'] = HEAD_FULL
campaign_state['notes_count'] = notes_count
campaign_state['updated_at'] = NOW
campaign_state['status'] = 'campaign_closed_parked_inconclusive'

with open('research/campaign_state.json', 'w') as f:
    json.dump(campaign_state, f, separators=(', ', ': '))
print("campaign_state.json updated; notes_count =", notes_count)

# Append verification row to experiment ledger (raw text append; never csv.writer).
ledger_row = (
    "E-1086," + NOW + ",verification,"
    "Session 3374 verification pass (park unchanged; HEAD reconciled to " + HEAD_FULL + "; "
    "origin/main == HEAD == local; working tree clean)," + HEAD_FULL + ",v1.2,"
    "panel_v1.2.csv (141 rows),no gate advanced,none,"
    "primary estimand inconclusive by construction; PH-1 not opened,"
    "verification only; no outcome-period returns computed or inspected\n"
)
with open('research/experiment_ledger.csv', 'a') as f:
    f.write(ledger_row)
print("experiment_ledger.csv appended E-1086")

initial_task = (
    "**Session 3375 task: Campaign closed (PARKED/INCONCLUSIVE). No further action.**\n\n"
    "Read research/HANDOFF.md and research/campaign_state.json (current_session 3374, "
    "next_session 3375, experiments_run 1086, last_verified_head " + HEAD_FULL + ").\n\n"
    "Campaign is closed as PARKED/INCONCLUSIVE (E-1068 formal close; D-151 / Formal-close "
    "section). No further verification passes. Do not compute outcome returns, do not open "
    "PH-1, do not use paid sources. If resuming, the single highest-value next action is: "
    "obtain >=200 admitted treatment firms with timestamped filing evidence plus "
    "delisted/terminal-return daily price coverage to the PH-1 outcome window. Otherwise, "
    "no action required.\n\n"
    "Note on re-derived state (Session 3374): experiment ledger max real run_id is E-1086 "
    "(E-3243 is a known duplicate-of-E-1037 anomaly); decision_log max header is D-151 (no "
    "D-152 header exists — prior \"D-152\" references are a mislabel). Panel files unchanged "
    "(v1.2 sha256 d075c3a7…c700eb, 141 rows, 12 cohorts, all gate-pending; v1.1 sha256 "
    "40f3c19f…f899df, 431 rows). HEAD at " + HEAD_SHORT + " (origin/main == HEAD == local), "
    "working tree clean."
)

with open('research/INITIAL_TASK_MESSAGE_3375.md', 'w') as f:
    f.write(initial_task)
print("INITIAL_TASK_MESSAGE_3375.md written")
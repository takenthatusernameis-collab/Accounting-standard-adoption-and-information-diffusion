import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/home/runner/work/Accounting-standard-adoption-and-information-diffusion/Accounting-standard-adoption-and-information-diffusion")
RESEARCH = ROOT / "research"
HANDOFF = RESEARCH / "HANDOFF.md"
STATE = RESEARCH / "campaign_state.json"
LEDGER = RESEARCH / "experiment_ledger.csv"

SESSION = 3071
NEXT_SESSION = 3072
HEAD = "fe5d335094fc48dd5dd438d16efdb66b3a56954e"
STALE_HEAD = "dc2dda7f5c6f8633105e19e3cea01097a3215c8e"
EXPERIMENTS_RUN = 865

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

note = (
    f"**Session {SESSION} note.** Verification pass (HEAD `{HEAD}` verified for Session {SESSION}; "
    "`git fetch origin main`; working tree clean; origin/main == HEAD == local at `" + HEAD + "`). "
    "`research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale "
    f"`{STALE_HEAD}` to **`{HEAD}`** (HEAD advanced since Session 3070 via checkpoint commit `{HEAD[:8]}` "
    "\"chore(kilo): checkpoint agent session\"; changes limited to research files only; no code changed, gates unchanged). "
    "pytest not available (`ModuleNotFoundError: No module named pytest`); prior sessions reported 173 passed, 0 failing. "
    "`verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). "
    "No code changed. Gates unchanged. This session (3071) prepends this note, keeps rolling 10 session blocks "
    "(3071..3062; drop 3061), writes `research/INITIAL_TASK_MESSAGE_3071.md` for Session 3072, and appends verification E-865. "
    f"`campaign_state.json`: `current_session` **3070 -> 3071**; `next_session` **3071 -> 3072**; "
    f"`experiments_run` **864 -> 865** (max E-id now E-865; experiments_run tracks the highest appended E-id); "
    f"`notes_count` 10; `updated_at` refreshed to `{now}`. "
    "Independent re-derivation: `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / "
    "12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / "
    "12 non-empty `T_A` (129 empty) / "
    "141 `filing_route` PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / "
    "141 `price_venue_set` PENDING A1 (price vendors and their licensing are not yet authorised) / "
    "rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_3071.csv`, `cmp` clean, same sha); "
    "`panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / "
    "8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv data records / max `source_id` **S-105** parsed numerically (S-100..S-104 absent -- pre-existing, leave unchanged); "
    "`experiment_ledger.csv` max **E-865** after this session's append. "
    "Park unchanged: cohort gate MET (12>=12); admitted treatment-firm 0 < 200 (FAIL); free delisted/terminal-return price coverage not established (FAIL). "
    "Primary estimand remains inconclusive by construction; PH-1 closed. No outcome-period returns computed or inspected."
)

text = HANDOFF.read_text()
blocks = re.split(r"(?=^\*\*Session \d+ note\.\*\*)", text, flags=re.M)
blocks = [b.strip() for b in blocks if b.strip()]
blocks = [b for b in blocks if not b.startswith(f"**Session {SESSION} note.**")]

kept = []
for b in blocks:
    m = re.match(r"\*\*Session (\d+) note\.\*\*", b)
    if m and int(m.group(1)) <= SESSION - 10:
        continue
    kept.append(b)
kept = [note] + kept
kept = kept[:10]
HANDOFF.write_text("\n\n".join(kept) + "\n")

state = json.loads(STATE.read_text())
state["current_session"] = SESSION
state["next_session"] = NEXT_SESSION
state["experiments_run"] = EXPERIMENTS_RUN
state["last_verified_head"] = HEAD
state["notes_count"] = 10
state["updated_at"] = now
state["status"] = "delta_only_verification_complete"
STATE.write_text(json.dumps(state, sort_keys=True) + "\n")

with LEDGER.open("a", newline="") as fh:
    w = csv.writer(fh)
    w.writerow([
        f"E-{EXPERIMENTS_RUN}",
        now,
        "verification",
        f"Session {SESSION} verification pass (park unchanged; last_verified_head reconciled from stale {STALE_HEAD} to HEAD {HEAD}; commit {HEAD[:8]} \"chore(kilo): checkpoint agent session\" only (research files only); no code changed; gates unchanged)",
        HEAD,
        "v1.2",
        "panel_v1.2.csv (141 rows)",
        "no gate advanced",
        "none",
        "cohort MET (12>=12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL; primary estimand inconclusive_by_construction; PH-1 closed",
        "verification only; no outcome-period returns computed or inspected",
    ])

tm = RESEARCH / f"INITIAL_TASK_MESSAGE_{SESSION}.md"
tm.write_text(f"""Session {NEXT_SESSION} task: delta-only verification pass.

Read the durable handoff `research/HANDOFF.md` and `research/campaign_state.json` (currently
`current_session` {SESSION}, `next_session` {NEXT_SESSION}, `experiments_run` {EXPERIMENTS_RUN},
`last_verified_head` {HEAD}). Then:

1. Run `git fetch origin main`. Verify the working tree is clean and that `origin/main` == `HEAD` == local HEAD. If HEAD has advanced, record the new sha and reconcile `last_verified_head` (do not edit code).
2. Re-derive committed state (D-037) and compare against the handoff note:
   - `research/panel_v1.2.csv`: sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb`, 141 rows, 21 cols, 12 distinct non-empty `timing_cohort` (39 non-empty cells), 0 `in_registered_panel=true` (141 `pending`), 12 non-empty `T_A` (129 empty), 141 `filing_route` PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP / 141 `price_venue_set` PENDING A1 (price vendors and their licensing are not yet authorised).
   - Byte-identical rebuild: `python3 scripts/build_panel.py --out /tmp/panel_rebuild_{NEXT_SESSION}.csv` then `cmp` against `research/panel_v1.2.csv` and compare sha256.
   - `research/panel_v1.1.csv`: sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df`, 431 rows, 19 cols, 8 `in_registered_panel=true`, 423 empty `T_A`.
   - `research/source_ledger.csv`: 102 physical lines / 100 csv data records, max `source_id` S-105 parsed numerically (S-100..S-104 absent by design, D-037).
   - `research/experiment_ledger.csv`: max **E-{EXPERIMENTS_RUN}** before this session's append -> append **E-{EXPERIMENTS_RUN + 1}**.
3. Append one verification row to `research/experiment_ledger.csv` (id `E-{EXPERIMENTS_RUN + 1}`, timestamp UTC, category `verification`, note that the park is unchanged, HEAD, `v1.2`, `panel_v1.2.csv (141 rows)`, `no gate advanced`, `none`, gate summary, `verification only; no outcome-period returns computed or inspected`).
4. Update `research/campaign_state.json`: `current_session` {NEXT_SESSION}, `next_session` {NEXT_SESSION + 1}, `experiments_run` {EXPERIMENTS_RUN + 1}, `last_verified_head` = verified HEAD, `notes_count` 10, refreshed `updated_at`.
5. Prepend a Session {NEXT_SESSION} note to `research/HANDOFF.md` keeping the rolling 10 session blocks ({NEXT_SESSION}..{NEXT_SESSION - 9}), dropping {NEXT_SESSION - 10}.
6. Write `research/INITIAL_TASK_MESSAGE_{NEXT_SESSION}.md` for Session {NEXT_SESSION + 1}.

Gates expected unchanged: cohort MET (12 >= 12); admitted treatment-firm 0 < 200 FAIL; free delisted/terminal-return price coverage not established FAIL. Primary estimand remains inconclusive by construction; PH-1 is closed. Do NOT compute or inspect outcome-period returns. `pytest` is unavailable (`ModuleNotFoundError: No module named pytest`) and `verify_artifacts.py` has a pre-existing `SyntaxError` at line 110. Report the park honestly; do not manufacture progress.
""")

print("updated", HANDOFF, STATE, LEDGER, tm.name, "at", now)

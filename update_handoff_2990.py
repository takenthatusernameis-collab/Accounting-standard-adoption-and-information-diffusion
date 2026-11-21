import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT / "research"
HANDOFF = RESEARCH / "HANDOFF.md"
STATE = RESEARCH / "campaign_state.json"
LEDGER = RESEARCH / "experiment_ledger.csv"

SESSION = 2990
NEXT_SESSION = 2991
HEAD = "b8db9e677229d13c9f540accacbf2665b1f2b3a6"
STALE_HEAD = "b6ae2974d7c7162f5865dcdd63071396de41107c"
EXPERIMENTS_RUN = 783

note = (
    f"**Session {SESSION} note.** Verification pass (HEAD {HEAD} verified for Session {SESSION}; "
    "`git fetch origin main`; working tree clean; origin/main == HEAD == local at `b8db9e677229d13c9f540accacbf2665b1f2b3a6`). "
    "`research/campaign_state.json` parsed with `json.load`; `last_verified_head` reconciled from stale "
    f"`{STALE_HEAD}` to **`{HEAD}`** (HEAD advanced since Session 2989 via checkpoint chore commit b8db9e67; no code changed, gates unchanged). "
    "pytest not available (`ModuleNotFoundError: No module named pytest`); prior sessions reported 173 passed, 0 failing. "
    "`verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 (pre-existing, unmodified). "
    "No code changed. Gates unchanged. This session (2990) prepends this note, keeps rolling 10 session blocks "
    "(2990..2981; drop 2980), writes `research/INITIAL_TASK_MESSAGE_2990.md` for Session 2991, and appends verification E-784. "
    f"`campaign_state.json`: `current_session` **{SESSION}**; `next_session` **{NEXT_SESSION}**; `experiments_run` **{EXPERIMENTS_RUN}**; "
    "`notes_count` 10; `updated_at` refreshed. Independent re-derivation: "
    "`panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / "
    "12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / 12 non-empty `T_A` (129 empty) / "
    "141 `filing_route` PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP (a date alone is insufficient; "
    "research/specification_v1.1.md section 1.1 condition j) / 141 `price_venue_set` PENDING A1 (price vendors and their licensing are not yet authorised) / "
    "rebuild byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2990.csv`, `cmp` clean); "
    "`panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / 19 cols / "
    "8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 100 csv records / max `source_id` **S-105** "
    "(S-100..S-104 absent -- per D-037); `experiment_ledger.csv` 798 physical lines / 767 `E-` line-starts / max **E-783** before this session's append -> **E-784** after. "
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
    if m and int(m.group(1)) <= 2980:
        continue
    kept.append(b)
kept = [note] + kept
kept = kept[:10]
HANDOFF.write_text("\n\n".join(kept) + "\n")

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
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
        "E-784",
        now,
        "verification",
        f"Session {SESSION} verification pass (park unchanged; last_verified_head reconciled from stale {STALE_HEAD} to HEAD {HEAD}; checkpoint chore commit b8db9e67 only; no code changed; gates unchanged)",
        HEAD,
        "v1.2",
        "panel_v1.2.csv (141 rows)",
        "no gate advanced",
        "none",
        "primary estimand inconclusive by construction; PH-1 closed; only cohort gate passes (12>=12); treatment-firm gate 0<200 FAIL; free delisted/terminal-return coverage not established FAIL",
        "verification only; no outcome-period returns computed or inspected",
    ])

tm = RESEARCH / f"INITIAL_TASK_MESSAGE_{SESSION}.md"
tm.write_text(f"""Session {NEXT_SESSION} task: delta-only verification pass.

Read durable handoff `research/HANDOFF.md` and `research/campaign_state.json`. Run `git fetch origin main`; verify working tree clean and origin/main == HEAD == local. Parse campaign_state.json with `json.load`; reconcile `last_verified_head` if stale (currently `{HEAD}`). Re-derive committed state (D-037): `panel_v1.2.csv` sha256 `d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols / 12 distinct non-empty `timing_cohort` / 0 `in_registered_panel=true` / 12 non-empty `T_A`; byte-identical rebuild via `python3 scripts/build_panel.py`; `panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` / 431 rows / 19 cols / 8 `in_registered_panel=true`; `source_ledger.csv` 100 csv records, max `source_id` S-105 parsed numerically; `experiment_ledger.csv` max **E-784** before the session's append. Append verification E-785. Update campaign_state (`current_session` {NEXT_SESSION}, `next_session` {NEXT_SESSION + 1}, `experiments_run` {EXPERIMENTS_RUN + 1}, `last_verified_head` set to verified HEAD). Prepend Session {NEXT_SESSION} note, keep rolling 10 blocks ({NEXT_SESSION}..{SESSION - 8}), drop {SESSION - 9}. Write `research/INITIAL_TASK_MESSAGE_{NEXT_SESSION}.md` for Session {NEXT_SESSION + 1}. Gates unchanged expected (cohort MET 12>=12; admitted treatment-firm 0<200 FAIL; free delisted/terminal-return price coverage not established FAIL). Do not compute outcome-period returns. pytest unavailable (`ModuleNotFoundError`). Report park honestly; do not manufacture progress.
""")

print("updated", HANDOFF, STATE, LEDGER, tm.name, "at", now)

import json, re, os

NOTE = (
    "**Session 2924 note.** Verification pass (HEAD `2ffb93d96ac0cae59d2a8a8d7c265002f9bda789` verified for "
    "Session 2924; `git fetch origin main`; working tree clean; origin/main == HEAD == local at "
    "`2ffb93d96ac0cae59d2a8a8d7c265002f9bda789`). `research/campaign_state.json` parsed with `json.load`; "
    "`last_verified_head` corrected from stale `cce288bf14532919d2fcd8d014c1e2f4079d3414` to "
    "**`2ffb93d96ac0cae59d2a8a8d7c265002f9bda789`** (one checkpoint chore commit advanced HEAD since Session 2923; "
    "no code changed, gates unchanged). pytest not available in this shell (`No module named pytest`); prior "
    "sessions reported 173 passed, 0 failing. `verify_artifacts.py` (repo root) still raises `SyntaxError` at line 110 "
    "(pre-existing, unmodified). No code changed. Gates unchanged. This session (2924) prepends this note, keeps "
    "rolling 10 session blocks (2924, 2923, 2922, 2921, 2920, 2919, 2918, 2917, 2916, 2915; drop 2914), writes "
    "`research/INITIAL_TASK_MESSAGE_2923.md` for Session 2925, and appends verification E-718. "
    "`campaign_state.json`: `current_session` 2923 -> **2924**; `next_session` 2924 -> **2925**; "
    "`experiments_run` 715 -> **716** (established actual offset is max E-id minus 2; prior notes mis-stated it as "
    "minus 1; max E-id now 718); `notes_count` 10; `updated_at` refreshed to `2026-11-19T10:14:31Z`. "
    "Independent re-derivation: `panel_v1.2.csv` sha256 "
    "`d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` matches / 141 rows / 21 cols / "
    "12 distinct non-empty `timing_cohort` (39 non-empty cells) / 0 `in_registered_panel=true` (141 `pending`) / "
    "12 non-empty `T_A` (129 empty) / 141 `filing_route` PENDING / 141 `price_venue_set` PENDING / rebuild "
    "byte-identical (`python3 scripts/build_panel.py --out /tmp/panel_rebuild_2924.csv`, `cmp` clean); "
    "`panel_v1.1.csv` sha256 `40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` matches / 431 rows / "
    "19 cols / 8 `in_registered_panel=true` / 423 empty `T_A`; `source_ledger.csv` 102 physical lines / 100 csv "
    "records / max `source_id` **S-99** (S-100..S-105 absent -- pre-existing; earlier notes' max of S-105 was "
    "prose drift, leave data unchanged); `experiment_ledger.csv` 733 physical lines / 730 csv records / max "
    "**E-718** after this session's append (E-403/E-404 shared-line anomaly and E-680 ragged row intact); "
    "`research/decision_log.md` 2642 physical lines / 95 `## D-<n>` headers (max D-150); `research/results.md` "
    "151 physical lines / 131 non-empty / reports no results; `.github/workflows/main.yml` sha256 "
    "`555f5fbaa2844c965712434b2fe199dfb508f99a1a781d66d86f4b07ddee00aa` unchanged. Doc-drift note (pre-existing, "
    "not corrected): `research/free_source_inventory/feasibility_notes.md` headline says 10 verified "
    "condition-2 jurisdictions, while the panel carries 12 distinct cohorts. Park unchanged: cohort gate "
    "MET (12>=12); admitted treatment-firm 0 < 200 (FAIL); filing_route/price_venue_set PENDING for all 141 PH-1 "
    "rows; free delisted/terminal-return price coverage not established (FAIL, D-042/E-047); primary estimand "
    "inconclusive_by_construction; PH-1 closed. No gate advanced; no outcome-period return computed or inspected; "
    "no paid data; no credentials; no GitHub Actions; closed probes not repeated."
)

path = "research/HANDOFF.md"
with open(path, encoding="utf-8") as fh:
    body = fh.read()

body = body.lstrip("\n")
blocks = re.split(r"(?m)^(?=\*\*Session \d+ note\.\*\*)", body)
blocks = [b for b in blocks if b.strip()]
print("existing blocks:", len(blocks), [re.match(r"\*\*Session (\d+)", b).group(1) for b in blocks])
kept = blocks[:9]
new = NOTE + "\n\n" + "\n".join(b.rstrip("\n") + "\n\n" for b in kept)
new = new.rstrip("\n") + "\n"
with open(path, "w", encoding="utf-8") as fh:
    fh.write(new)

with open(path, encoding="utf-8") as fh:
    check = fh.read()
hdr = re.findall(r"(?m)^\*\*Session (\d+) note\.\*\*", check)
print("new header list:", hdr, "count:", len(hdr))
print("bytes:", os.path.getsize(path))

state = json.load(open("research/campaign_state.json"))
state["current_session"] = 2924
state["next_session"] = 2925
state["experiments_run"] = 716
state["notes_count"] = len(hdr)
state["last_verified_head"] = "2ffb93d96ac0cae59d2a8a8d7c265002f9bda789"
state["updated_at"] = "2026-11-19T10:14:31Z"
keys = ["campaign", "current_session", "experiments_run", "gates", "last_verified_head", "next_session",
        "notes_count", "primary_estimand", "repo", "status", "updated_at"]
line = "{"
parts = []
for k in sorted(keys):
    parts.append(json.dumps(k) + ": " + json.dumps(state[k], separators=(",", ":")))
line += ", ".join(parts) + "}"
json.loads(line)
with open("research/campaign_state.json", "w", encoding="utf-8") as fh:
    fh.write(line + "\n")
print(line)

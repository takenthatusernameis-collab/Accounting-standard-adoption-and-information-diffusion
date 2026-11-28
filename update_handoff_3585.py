import io

PATH = "research/HANDOFF.md"

note = (
    "**Session 3585 note.** Campaign closed (PARKED/INCONCLUSIVE; E-1068 formal close, "
    "D-151/Formal-close section at `## Formal close (Session 3275)`). No further verification "
    "passes; no action required. Acknowledged prior task (read HANDOFF/campaign_state and confirm "
    "closed status; prior task read from the durable handoff per the standing instruction -- "
    "INITIAL_TASK_MESSAGE_3584.md). Session 3584 complete: HANDOFF.md session 3584 note present, "
    "campaign_state.json current_session->3584/next_session->3585, INITIAL_TASK_MESSAGE_3585.md "
    "written; committed as checkpoint f14299f6. Re-derived committed state from files (D-037): "
    "`git fetch origin main` shows origin/main == HEAD == local at "
    "**f14299f6f213f8f3c2292ec416664883378a9e2a**; working tree clean (HEAD advanced from prior "
    "session's `last_verified_head` **bbe928c6da65b2500c3971d085c0f6cae2d6cf24** to "
    "**f14299f6f213f8f3c2292ec416664883378a9e2a** via checkpoint f14299f6 [session 3584 "
    "handoff-set files]; delta limited to handoff-set files `research/HANDOFF.md`, "
    "`research/campaign_state.json`, `research/INITIAL_TASK_MESSAGE_3585.md`, "
    "`research/experiment_ledger.csv`; no production code changed). `campaign_state.json` parsed "
    "with `json.load`; `last_verified_head` corrected from stale "
    "**bbe928c6da65b2500c3971d085c0f6cae2d6cf24** to "
    "**f14299f6f213f8f3c2292ec416664883378a9e2a**. Re-verified artifact digests directly this "
    "pass: `panel_v1.2.csv` sha256 "
    "`d075c3a77f7dac79f9aa82023d0b5a53252d5095a88a7761abeb471153c700eb` / 141 rows / 21 cols; "
    "`panel_v1.1.csv` sha256 "
    "`40f3c19f38c70810fe8984e36d18f9ddc4e973e68c537106d2d72b13efa899df` / 431 rows / 19 cols; "
    "`source_ledger.csv` sha256 "
    "`314afc2ab4936fe5b455784d7da317de772d185c2eafad95d1de85bd255edf57` / 100 csv data records; "
    "`experiment_ledger.csv` 1184 physical lines / last row **E-1181** (verification) -> append "
    "E-1182 (verification). Binding constraint for any future resume (unchanged): obtain >=200 "
    "admitted treatment firms with timestamped filing evidence plus delisted/terminal-return daily "
    "price coverage to the PH-1 outcome window."
)

with io.open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Split into non-empty session blocks (each note is one physical line).
blocks = [ln.strip() for ln in content.splitlines() if ln.strip()]
assert blocks, "no blocks found"
assert blocks[0].startswith("**Session 3584 note.**"), blocks[0][:40]

# Prepend the new note and keep the most recent 10 blocks.
new_blocks = [note] + blocks
new_blocks = new_blocks[:10]

out = "\n\n".join(new_blocks) + "\n"
with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(out)

print("blocks now:", len(new_blocks))
print("first:", new_blocks[0][:40])
print("last:", new_blocks[-1][:40])
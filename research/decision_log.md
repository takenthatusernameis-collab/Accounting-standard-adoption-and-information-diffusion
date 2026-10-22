# ACCTCLOCK — Decision Log

Every decision is recorded with its date, the evidence it rested on, and what
would reverse it. Decisions are never silently revised; a reversal is a new
entry.

---

## D-001 — 2026-10-21 — Accept the durable state as the prior agent task, and repair the loop first

**Context.** The worker loop's task message says to read the prior agent task
from the durable handoff. No handoff file existed. The durable state consisted
of the protocol (`research/ACCTCLOCK_..._prompt.md`), the diagnostics ledger
(`research_state/workflow_run_diagnostics.jsonl`), and the workflow definition.
The ledger's only record is a failed run whose logged error was
`file or directory not found: tests/test_controller_progress_accounting.py`.

**Decision.** Treat (a) the recorded failure and (b) the protocol's Phase 0–2
work as the prior task. Repair the controller-crediting path first, then perform
the protocol phases that are executable without data.

**Rationale.** The workflow's own test step referenced four test files and
`scripts/controller_progress.py` that did not exist. With the script missing,
`project_progress` could never be set, so every activation ended with "No
meaningful repository change was committed and verified" even when work had
been committed and pushed. Nothing else in the campaign could be persisted
reliably until that was fixed.

**Reverses if.** The controller's contract is shown to differ from the
implementation in `scripts/controller_progress.py`.

---

## D-002 — 2026-10-21 — Freeze H-B (transition-window repricing) as the primary outcome, two-sided

**Context.** The protocol requires reconciling four non-interchangeable
outcomes: announcement-to-report drift, post-earnings-announcement drift,
transition-window repricing, or a combination. The starting prompt was
ambiguous.

**Decision.** Primary = transition-window repricing (H-B) around the first
report published under the new standard, tested two-sided. H-A (announcement)
is retained as the mechanism and anticipation check; H-C (PEAD) is retained as
a pre-registered secondary.

**Rationale.** H-A is where the published evidence lives (S-01) but the reaction
happens at a public announcement and is not tradeable without look-ahead. H-B
and H-C are publicly timestamped and tradeable. No economically justified sign
exists for H-B, so the test is two-sided by construction (protocol Phase 2.4).

**Reverses if.** A mechanism argument fixes a sign, or if the data show the
announcement window absorbs the entire effect (which is a kill condition, not a
reason to switch the primary outcome).

---

## D-003 — 2026-10-21 — Park the empirical test at Phase 3 on a documented data blocker

**Decision.** Do not claim any validation, any result, or any completion. Record
the blocker in `research/data_manifest.md` and leave the campaign parked with a
precise next action.

**Rationale.** No market data, no filing archive, no licensed vendor access, and
no reachable hypothesis-factory dossier exist in this environment. The protocol
(Authority item 6) requires stopping at a clear handoff in exactly this case,
and forbids claiming completion based on a plan.

**Reverses if.** A data route is authorised or becomes available.

---

## D-004 — 2026-10-21 — Create the durable handoff and the machine-readable campaign state

**Decision.** Establish `research/HANDOFF.md` (human-readable, includes the
ready-to-run task message for the next agent) and `research/campaign_state.json`
(machine-readable, managed by `scripts/campaign_resume.py`).

**Rationale.** The loop's own task message presumes a durable handoff exists.
Two prior sessions searched for one and found nothing, which wasted an
activation and ended one session with a provider error. The handoff must be
discoverable without guesswork, and the campaign state must let a session
resume mid-cycle rather than restart.

**Reverses if.** The controller is changed to inject the prior task directly
into the worker prompt (a workflow change, which this repository's token
cannot authorise).

---

## D-005 — 2026-10-21 — Treat the anomaly-decay literature as a prior against the hypothesis, not as a verdict

**Decision.** Record PEAD decay (S-09, S-10, S-11), the transaction-cost
explanation (S-12), the aggregation critique (S-13), and the structural
analogy of the disappearing index effect (S-20) as strong counter-evidence that
must shape the test's power and cost assumptions — and that must be reported in
`research/results.md` whatever the outcome.

**Rationale.** The candidate's edge would be a form of slow information
diffusion, and that family is documented to be weak or absent in large caps
since roughly 2006. Designing a test that ignores this would be an invitation
to a false positive.

**Reverses if.** The primary test is run and returns a robust, cost-surviving
effect.

---

## D-006 — 2026-10-21 — Do not modify the workflow file

**Decision.** Leave `.github/workflows/main.yml` untouched.

**Rationale.** The controller's checkpoint explicitly restores workflow
definitions to the session base SHA and unstages them, so any edit would be
discarded at checkpoint time; and the repository token cannot authorise
workflow-file changes in any case. The failure recorded in the ledger was
caused by *missing repository files*, not by a defective workflow, so the
repair belongs in `tests/` and `scripts/`.

**Reverses if.** A maintainer with workflow-write authority asks for a change
and the controller's staging rule is changed to allow it.

---

## D-007 — 2026-10-21 — Declare the campaign status: **PARKED (not rejected)**

**Decision.** Status is *parked*: the hypothesis is testable in principle, the
design is frozen and falsifiable, but execution is blocked by data access.
This is explicitly not "rejected" (no credible evidence contradicts the claim)
and explicitly not "validated" (no test has been run).

**Reverses if.** Data arrives (→ continue) or a decisive test runs against the
hypothesis (→ reject).

---

## D-008 — 2026-10-22 — Retrieve the canonical hypothesis-factory dossier read-only, and treat it as binding on the design

**Context.** Blocker B-2 in the previous handoff recorded that the canonical
ACCTCLOCK dossier could not be reached. The protocol (Phase 0) requires it:
"Recover the canonical ACCTCLOCK dossier and current validation handoff from the
hypothesis factory using read-only access. Record commit SHA, retrieval date, and
source paths."

**Decision.** The dossier was retrieved read-only in this session and **is
reachable**: repository `takenthatusernameis-collab/QUANTITATIVE-HYPOTHESIS-FACTORY`,
commit `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff`, commit date 2026-10-22T00:49:21Z,
retrieved 2026-10-22. Source paths: `research/validation_handoffs.md` (specification
**V-009**, IDEA-011 ACCTCLOCK), `research/idea_register.md` (IDEA-011 dossier),
`research/ranked_shortlist.md` (active ranking), `research/next_agent_handoff.md`
(Cycle 132 state), `research/source_ledger.md` (437 verified sources, S-001…S-457).
No upstream file was edited; no upstream work was performed; the repository was
read through the GitHub API only.

**Rationale.** The dossier is binding on this campaign's *design* even though this
repository owns its own frozen artefacts. It records, at the retrieved commit, four
constraints that the frozen artefacts in this repository do not currently satisfy:
(a) the within-jurisdiction early-versus-mandatory contrast is **rejected as an
identification** (V-009 Cycle-56, item 3); (b) a group A (first-time adopters) /
group B (second-time adopters) partition **must not be built** for a
single-package IFRS adoption (V-009 Cycle-56, item 1; Cycle-111 correction
notice); (c) **enforcement quality and linguistic distance are mandatory
controls**, not candidate states and not optional slices (V-009 Cycle-52, item 2;
Cycle-113, item 1); and (d) the firm-level "repeat adopter" flag is **not
published prospectively** (Cycle-110 resolution, R-058) and must be derived from
each firm's own prior-year basis-of-preparation note and pre-registered as a
construction. It also records a fact that *raises* the campaign's value: the
first-time-versus-second-time-adopter **drift** comparison is **unrun by the
field** (G-21), so a null in that design is a contribution, not a replication
(V-009 Cycle-58, item 3).

**Reverses if.** The dossier is superseded, or a maintainer of the factory
repository states that V-009 is not binding on validator repositories.

---

## D-009 — 2026-10-22 — The frozen specification's treatment group is empty; do not execute v1.0

**Context.** `research/specification_v1.md` §3 defines treatment as "firms whose
reporting framework changed at the event (local GAAP → IFRS 15/16/9, or US GAAP →
ASC 606/842)". Applied to the frozen universe of §5 (EU, UK, US) this yields
**zero** firms: the EU and the UK were already on IFRS when IFRS 15/9/16 took
effect, so those are content changes; ASC 606 and ASC 842 are *inside* US GAAP, so
the US framework did not change either. The frozen primary estimand is therefore
undefined. The same conclusion is reached, from the opposite direction, by the
canonical dossier (D-008), which rejects the within-jurisdiction early-versus-
mandatory route outright.

**Decision.** The frozen specification v1.0 **must not be executed as written**, and
it must not be edited in place. A v1.1 (and a matching hypothesis v1.1 and
preregistration v1.1) must be registered through `research/prompt_changelog.md`
**before any outcome-period return is computed**. No data is to be purchased
against a design that cannot be executed.

**Rationale.** This is a defect in the frozen artefact, not a data limitation. It
is invisible until the event calendar is built, which is why the calendar was
built first. Executing v1.0 would have produced either an empty treatment group
(a null that means nothing) or an unregistered, post-hoc treatment definition
(the exact failure mode the protocol's Authority item 5 forbids).

**Reverses if.** A registered v1.1 supplies a non-empty, identified treatment
group.

---

## D-010 — 2026-10-22 — Adopt the regulator/issuer filing route as the data spine, with a paid price subscription as its one paid dependency

**Context.** The previous handoff required a comparison of a licensed route, a
regulator/issuer route, and a reduced-power open-data fallback, with one
recommended route and a power statement.

**Decision.** Recommend **route (b), the regulator/issuer public-filing route, as
the spine**, with the one paid component being a survivorship-clean daily price
source (Sharadar/Nasdaq Data Link ≈ $30/month and/or EODHD ≈ $20/month at retail
tiers, or CRSP Global if an institutional seat exists). Rationale: the licensed
route supplies prices but **not** the EDGAR acceptance timestamp (T-R, the frozen
primary entry timestamp) and not the filing as originally published, so a licence
alone does not unblock the test; the public route supplies T-R, the filing as
published, and the event calendar, but not prices. The fallback (route c) is
scoped to US + UK + EU-27 only, giving **9 independent events — below the
pre-registered minimum of 12** — and is therefore **inconclusive by construction**
for the primary estimand; it can still deliver the H-A anticipation check, the H-C
secondary, and a directional replication of the published conflict between S-179
(Korea, PEAD falls) and S-188 (Greece, PEAD rises).

**Rationale.** A licensed price feed without T-R cannot execute the frozen
design; a free price feed with a survivors-only universe triggers hypothesis kill
condition 9 *and* biases the estimate against the hypothesis, because the firms the
hypothesis predicts the effect in (low information quality, small, illiquid) are
exactly the names a survivor-filtered panel drops.

**Reverses if.** A maintained institutional licence is offered, in which case the
price component is upgraded and the spine is unchanged.

---

## D-011 — 2026-10-22 — Event-calendar dating policy: primary source or `unverified`, conflicts recorded, never resolved by return

**Decision.** `research/event_calendar.csv` records, for every (standard,
jurisdiction) event, the issuance date, the endorsement or legal adoption date,
the effective date, the first affected fiscal-year start and an estimated first
report date, each with its own source URL, source type, and verification status.
A date that cannot be tied to a primary source (the standard setter, the
regulator, the EU Official Journal, or the issuer's own filing index) is marked
`unverified` and is never filled from a secondary summary. **Where two primary
sources disagree, both readings are recorded in `notes` and the conflict is left
open.** The date that maximises any return is never selected.

**Rationale.** The protocol (Phase 3) requires exactly this, and the handoff
repeats it. It is a discipline, not a formatting rule: the calendar is the input
to the H-A announcement window, so a silently resolved date conflict is a
look-ahead channel.

**Reverses if.** Never. This is a permanent integrity rule.

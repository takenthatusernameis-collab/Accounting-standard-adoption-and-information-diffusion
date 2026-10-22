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

---

## D-012 — 2026-10-22 — Register v1.1 with a jurisdiction-level treatment and a within-jurisdiction firm-level state; build **no** adopter partition

**Context.** D-009 established that the v1.0 treatment definition yields an empty
treatment group. Two candidate repairs existed: (a) a **firm-level binary partition** of
first-time adopters against second-time adopters, and (b) a **jurisdiction-level
application event** with staggered timing and a firm-level state estimated *within*
jurisdiction. The canonical dossier (D-008) forbids (a): V-009 Cycle-56 amendment
item 1 and the Cycle-111 correction notice state that first-time adopters apply IFRS as
a single package, so the partition "degenerates into the historical first-time-versus-
second-time IFRS comparison the literature has already populated" (S-35, S-36), and
Cycle-56 item 3 rejects the within-jurisdiction early-versus-mandatory contrast because
the treatment arm is voluntary and self-selected and the diffusion clock has no window
to run. Option (b) is consistent with the dossier's own frozen conceptual rules
("Event universe: adoption events of new accounting standards … covering affected firms
in the adopting jurisdiction"; "Position: long affected firms with low pre-adoption
information quality … from the announcement date to the first full post-adoption
reporting date") and with V-009 Cycle-52 amendment item 1, which requires the
candidate's state to be firm-level and to "retain identifying power **within** a
jurisdiction".

**Decision.** Register **v1.1** of the hypothesis, specification and preregistration
(`research/hypothesis_v1.1.md`, `research/specification_v1.1.md`,
`research/preregistration_v1.1.md`) in which:

- the **treatment** is a jurisdiction-level standard-application event — a firm is
  treated from the jurisdiction's adoption announcement if it is in the affected-firm
  list (knowable ex ante) and applies the standard from the effective date;
- the **state** is firm-level pre-adoption information quality (absolute discretionary
  accruals, within-jurisdiction median split), estimated **within jurisdiction**;
- the **counterfactual** is a matched **not-yet-treated** jurisdiction group, matched
  on size, industry, liquidity, momentum, market-to-book, analyst coverage and
  **fiscal-period-end proximity** (so the control transition window has the same length
  as the treated one);
- **no group A / group B partition is built** and none is presented as pre-registered;
  the **UK early-adopter cohort is excluded from treatment**; and **no published
  firm-level repeat-adopter flag is treated as available** (V-009 Cycle-110, R-058).

The v1.0 files are **not edited**; the change is registered as a new version in
`research/prompt_changelog.md` (Iteration 8).

**Rationale.** (a) is the design the dossier has closed, for a stated reason that
applies to the retrospective instance exactly as it does to the IFRS 18 instance.
(b) satisfies every binding amendment: firm-level state with within-jurisdiction
identifying power (Cycle-52 item 1), a non-empty and ex-ante-knowable affected-firm
list (V-009 ambiguity 6), a transition-window claim (Cycle-58 item 2), and a design
that identifies from **timing**, not from a partition. It also avoids the power trap
the v1.0 universe created: treatment assigned at jurisdiction level means firm count
is not a substitute for cluster count.

**Reverses if.** The feasibility audit shows the registered panel cannot reach the
≥12-cluster minimum **and** a pre-registered, dossier-compliant alternative treatment
definition is registered as v1.2 with the same reasoning recorded. It does not reverse
by returning to a group A / group B partition.

---

## D-013 — 2026-10-22 — Enforcement quality and linguistic distance are mandatory controls, imposed in three parts; the campaign claims only the within-jurisdiction residual

**Context.** v1.0 §3 treated enforcement quality as an *optional competing conditioner*
to be interacted with the state. V-009 Cycle-52 amendment item 2 makes enforcement and
linguistic distance **mandatory conditioning controls** ("fixed ex ante, applied to every
arm"), and states that the candidate's claim becomes "the **within-jurisdiction,
firm-level residual** after those controls are imposed"; the candidate "may not claim"
the enforcement effect as its own, because it is published (S-43, S-44, S-52). Cycle-113
amendment item 1 promotes institutional enforcement quality from "available" to
"mandatory" and makes the enforcement-conditioned comparator a **control requirement
and not a falsification**. The Cycle-52 pass/fail additions are: a result that
survives only because the country-level controls are omitted is a **fail**, and the
within-jurisdiction estimate must be shown separately from the pooled one.

**Decision.** v1.1 makes both controls mandatory and imposes them in three registered
parts:

1. the **primary** within-jurisdiction estimate uses jurisdiction fixed effects and
   jurisdiction-specific linear time trends, so both controls are absorbed and cannot
   drive the estimate;
2. the **pooled** jurisdiction-level estimate is reported **with** the controls imposed
   and **without** them, the latter as the mandated ablation (b) — and a pooled result
   that exists only without the controls is a **fail** (kill condition 11);
3. the within-jurisdiction estimate is **reported within pre-registered enforcement-
   quality and linguistic-distance strata**, with an interaction test, and acceptance
   requires that **no single stratum carries the whole effect**.

The withdrawn ablation (d) ("replace the enforcement regime with trade invoicing share
or another country characteristic") is **not reinstated**: it is now the control, and
replacing it with a further country characteristic would test nothing.

**Rationale.** The controls are jurisdiction-constant, so in a within-jurisdiction
specification they are absorbed rather than estimated. Part 3 exists precisely so that
the imposition is operative and visible rather than an artefact of the fixed effects:
without it, "the controls are imposed" would be unverifiable from the output. Part 2
implements the dossier's fail rule directly.

**Reverses if.** A maintainer of the factory repository states that V-009 is not
binding on validator repositories, or amends the Cycle-52 / Cycle-113 controls.

---

## D-014 — 2026-10-22 — Declare the retrospective panel's holdout empty in advance, and register a prospective holdout arm

**Context.** v1.0's chronological split was defined on T-R. In v1.1 the decision
timestamp is T-A, and **every registered retrospective event has T-A ≤ 2017-10-31**
(`research/event_calendar.csv`). There is therefore **no event with T-A on or after
2019-01-01**, and the "untouched holdout" split would be empty. The protocol's Phase 7
gate 4 requires results to survive a pre-registered out-of-sample test, and v1.0's
preregistration §4 already set the precedent that a small holdout is "inconclusive by
construction".

**Decision.**

1. The splits are re-anchored on **T-A** (Development: T-A < 2016-01-01; Validation:
   T-A ∈ [2016-01-01, 2019-01-01]; Untouched holdout: T-A ≥ 2019-01-01).
2. The **emptiness of the retrospective holdout is declared in advance**, together with
   its consequence: acceptance criterion 3 is expected to be **unevaluable**, and
   **the retrospective panel cannot by itself satisfy protocol promotion gate 4**. The
   retrospective panel's registered role is **evidential** — does the transition-window
   state contrast exist, at what size, and does it survive the mandatory controls.
3. **PH-1**, a prospective holdout arm on the **IFRS 18 first-application window** (the
   2027 interim reporting season, periods ending 30 June 2027), is registered in
   `research/preregistration_v1.1.md`. Its outcome lies in the future and cannot be
   inspected before it occurs. It **requires a separate v1.2 registration filed before
   the first IFRS 18 report is published** (V-009 Cycle-56 amendment item 4), and it
   is registered here with the pre-registered cycle split: the 2026 interim reporting
   season carries the pre-adoption disclosure (the pre-emption kill-signal window) and
   the 2027 interim season carries the first IFRS 18 reports (the outcome).
4. The retrospective panel is nevertheless a **genuine** holdout in the operational
   sense, because **no outcome-period return has ever been computed in this
   repository**; the chronological ordering is a real ordering of information for the
   validator. This does not upgrade the retrospective panel to a promotable design.

**Rationale.** Discovering an empty holdout after the specification was frozen and the
data bought would be a look-ahead channel of exactly the kind the protocol forbids.
Declaring it now forces the honest conclusion — the retrospective panel is evidential,
and the promotable test is prospective — and makes PH-1 a concrete, dated commitment
rather than a hope.

**Reverses if.** A registered panel event with T-A on or after 2019-01-01 is added
under the panel membership rule before the feasibility audit begins.

---

## D-015 — 2026-10-22 — Cache raw data outside the repository by default; commit only code, manifests and hashes

**Context.** The data route is a regulator/issuer filing spine plus one paid price
subscription. Licence and terms of use differ per source, and redistribution rights
differ per vendor, so committing raw harvests or vendor extracts to the repository is
a per-source legal question that the campaign cannot answer for itself.

**Decision.** The default is: **raw files live in a cache outside the repository
working tree** (`$ACCTCLOCK_CACHE`, default `~/.cache/acctclock`); the repository
receives **code**, **manifests** (source, URL, method, HTTP status, bytes, SHA-256,
retrieval timestamp, parser version), **hashes**, and **derived aggregates that carry
no vendor-licensed content** (the panel file, coverage counts). A per-source exception
requires an explicit maintainer ruling recorded as a new decision in this log. The
acquisition plan (`research/data_acquisition_plan.md` §3, §5) fixes the naming, the
schemas and the manifest format, and requires that a failed retrieval be recorded as a
failed retrieval rather than as an absence.

**Rationale.** This is the same discipline as D-011 applied to data instead of dates:
the provenance record must be complete and committed, while the material stays where
the licence puts it. It also keeps the repository small enough for the controller to
checkpoint, and makes the pipeline re-runnable offline from the cache.

**Reverses if.** A maintainer rules that a specific named source may be committed to
the repository.

---

## D-016 — 2026-10-22 — The panel membership rule is frozen before the feasibility audit and must not be narrowed afterwards

**Context.** The v1.1 panel has two strata: Stratum A (content-change events in the EU,
UK and US) and Stratum B (framework-change events, i.e. first-time IFRS adopters,
admitted **by rule**). The realised size of Stratum B depends on price and filing
coverage, which are unknown until the data is acquired. Preregistration §5.2 predicts
≈8 clusters for Stratum A and ≈20–40 for Stratum B, with the total above the ≥12
minimum only if Stratum B realises.

**Decision.** The panel membership rule (`research/specification_v1.1.md` §1.1) and the
stratum split are **frozen at registration**. The feasibility audit **reports** the
realised counts and **stops** if the counts fall below the pre-registered minimums
(≥12 clusters, ≥200 treatment firms), in which case the primary estimand is
**inconclusive by construction**. **The panel may not be narrowed, widened or
re-weighted after the feasibility audit begins** in order to reach the minimums; a
different panel requires a new registered version.

**Rationale.** A panel that is adjusted until it reaches a power threshold is a panel
selected on the outcome. The rule fixes the selection criterion in advance — including
the part of it (Stratum B) that may turn out to be unobtainable — and the honest
consequence (inconclusive) is pre-registered alongside it.

**Reverses if.** The maintainer changes the panel scope **before** the feasibility
audit begins, under authorisation item A4 of `research/data_acquisition_plan.md` §8.1.

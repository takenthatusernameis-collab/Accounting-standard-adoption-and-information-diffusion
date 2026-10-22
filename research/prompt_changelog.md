# ACCTCLOCK — Prompt Changelog

Dated iterations of the research prompt and the frozen artefacts it governs.
Each entry states what changed, why, and whether the change altered the
hypothesis or the acceptance criteria (which would require a new version).

---

## 2026-10-21 — v1.0 baseline (protocol created)

- Protocol created at `research/ACCTCLOCK_iteratively_improving_validation_prompt.md`
  (v1.0). It defines the mission, authority limits, the Phase 0–7 structure, the
  required artefacts, and the final report format.
- Status at creation: guidance only. No test had run; no edge was claimed.

## 2026-10-21 — Iteration 1: hypothesis and outcome ambiguity resolved

**Problem.** The starting hypothesis did not name which of four
non-interchangeable outcomes it referred to ("post-announcement or
post-reporting abnormal-return path"). Protocol Phase 0 requires the ambiguity
to be resolved, or competing hypotheses to be defined, *before* any returns are
seen.

**Change.** `research/hypothesis.md` v1.0 created with three named outcome
families (H-A announcement, H-B transition window, H-C post-earnings-announcement
drift), H-B pre-selected as primary because it is the only publicly timestamped
and tradeable family, seven counter-hypotheses, six pre-registered predictions,
and ten kill conditions. The primary test is two-sided because no economically
justified sign exists.

**Hypothesis or acceptance criteria altered?** No — this is the first
registration of the hypothesis, made before any return was computed.

## 2026-10-21 — Iteration 2: specification and preregistration frozen

**Change.** `research/specification_v1.md` and `research/preregistration.md`
created. They fix the event clock (four distinct timestamps, only three of
which are tradeable), the treatment/control design, the information-quality
proxy (absolute discretionary accruals, median split within jurisdiction-year),
the entry/exit rule, the benchmark and estimand, the risk controls, the cost
assumptions, the acceptance criteria, the chronological development /
validation / holdout split, the test order, the stopping rule, and the
multi-comparison adjustment.

**Hypothesis or acceptance criteria altered?** No — both are frozen
pre-data.

**Known weakness carried forward.** The design has few independent clusters
(jurisdiction × standard × year). The preregistration therefore requires a
jurisdiction-level randomisation test, a wild-cluster bootstrap, and an
explicit statement that an effect below roughly 0.5–0.7% per event is
*inconclusive* rather than *null*.

## 2026-10-21 — Iteration 3: literature audit folded into the design

**Change.** 25 sources recorded in `research/source_ledger.csv` with a
per-source verification status (`abstract read`, `working paper read`,
`citation-only`). Four sources are labelled citation-only because only their
bibliographic details were observed.

**Design consequences adopted (see D-002, D-005).**

- The primary outcome was moved to the transition window and the announcement
  window was demoted to an anticipation check, because the published evidence
  (S-01) is an announcement-window reaction that is not tradeable without
  look-ahead.
- Cost assumptions were set conservatively and a break-even cost is required,
  because transaction costs are a documented explanation for the drift family
  (S-12) and spreads widen after announcements (S-14).
- A minimum of 12 independent events and 200 treatment firms is required, and
  the result must survive exclusion of the largest winners, because the drift
  family has decayed sharply and may be an aggregation artefact
  (S-09, S-10, S-13).

**Hypothesis or acceptance criteria altered?** The acceptance criteria were
tightened (minimum event/firm counts, break-even cost, no-single-outlier rule)
before any data existed. This is a legitimate tightening of a pre-registration,
not a rescue of a failing result; it is recorded here for audit.

## 2026-10-21 — Iteration 4: infrastructure repair (no change to the research design)

**Change.** The controller's progress-accounting script and the four test files
required by the workflow's pytest step were created, and the campaign-state and
serialization helpers were added. 67 test cases pass.

**Hypothesis or acceptance criteria altered?** No — the infrastructure change
touches no research artefact, and the frozen specification, preregistration, and
hypothesis are untouched.

## 2026-10-21 — Iteration 5: handoff and campaign state established

**Change.** `research/HANDOFF.md` (durable handoff with the next agent's task
message) and `research/campaign_state.json` (machine-readable resume state)
created, with `scripts/campaign_resume.py` as the manager for the latter.

**Hypothesis or acceptance criteria altered?** No.

## 2026-10-22 — Iteration 6: event calendar, data route, and the canonical dossier recovered

**Change.** Three artefacts were added and no frozen artefact was touched:
`research/event_calendar.csv` (primary-source-verified adoption dates for the
IFRS 15/16/9 primary panel and the ASC 606/842 secondary panel, with per-row
verification status, recorded date conflicts, and an explicit
first-time/repeat-adopter coexistence assessment per standard),
`research/data_route_assessment.md` (three routes compared, one route recommended
with a power statement and an explicit authorisation request, and the
reduced-power fallback scoped concretely), and the retrieval record for the
canonical hypothesis-factory dossier, which is now reachable at commit
`1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` (see D-008). The infrastructure fix
from the previous session was re-verified: the workflow's exact pytest invocation
passes 67 cases, and the previously recorded failure
(`file or directory not found: tests/test_controller_progress_accounting.py`) no
longer appears in the diagnostics ledger.

**Hypothesis or acceptance criteria altered?** No. `research/hypothesis.md` v1.0,
`research/specification_v1.md` v1.0 and `research/preregistration.md` v1.0 are
byte-identical to their previous versions. What changed is the *knowledge about*
the frozen design, which is recorded as decisions D-008 to D-011.

**Known weakness carried forward, now sharpened.** The event calendar exposed a
defect in the frozen specification rather than confirming it: the treatment group
defined in `research/specification_v1.md` §3 ("firms whose reporting framework
changed at the event") is **empty** across the frozen universe of §5, because the
EU and the UK were already on IFRS when IFRS 15/16/9 took effect and ASC 606/842
are inside US GAAP. The canonical dossier reaches the same conclusion from the
other side and is more restrictive: it rejects the within-jurisdiction
early-versus-mandatory contrast outright (V-009 Cycle-56, item 3), forbids a
group A / group B partition for a single-package IFRS adoption (Cycle-56 item 1;
Cycle-111 correction notice), and requires enforcement quality and linguistic
distance as **mandatory controls** rather than optional interacting conditioners
(Cycle-52 item 2; Cycle-113 item 1). See D-009.

## 2026-10-22 — Iteration 7: the design revision is pre-registered as the next action, not performed here

**Change.** No design was changed in this session, because no outcome-period
return exists and a design change made without the calendar and the dossier
would have been speculative. Instead, the required revision was specified
precisely enough for the next session to execute it as a *registered* v1.1:
a non-empty, identified treatment definition; the mandatory enforcement and
linguistic-distance controls; the pre-registered transition-window claim with
steady-state comparability results demoted to a descriptive control; the
construction rule for the firm-level repeat-adopter flag (derived from each
firm's own prior-year basis-of-preparation note, per the dossier's R-058);
the jurisdiction panel; and the revised split and cluster counts.

**Hypothesis or acceptance criteria altered?** Not yet, and deliberately so. The
next session must register `research/hypothesis.md` v1.1,
`research/specification_v1.md` v1.1 and `research/preregistration.md` v1.1 through
this changelog **before** any return is computed. v1.0 is never overwritten
(`research/specification_v1.md`, preamble).

## 2026-10-22 — Iteration 8: the design revision is **registered** as v1.1

**Problem.** The frozen v1.0 design could not be executed: its treatment definition
("firms whose reporting framework changed at the event") produced an **empty** treatment
group across the frozen EU/UK/US universe, so the primary estimand was undefined
(D-009, ledger E-010). The canonical dossier independently rejected the only
within-universe substitute — the UK early-adopter cohort — as an identification, and
forbade a group A / group B first-time-vs-second-time partition for a single-package
IFRS adoption. The campaign therefore had no executable estimand, and no amount of
data acquisition could change that.

**Change.** **v1.1 of the hypothesis, the specification and the preregistration is
registered**, in new files. `research/hypothesis.md`, `research/specification_v1.md` and
`research/preregistration.md` v1.0 are **byte-identical to their previous versions** and
are not edited in place.

| New artefact | What it registers |
|---|---|
| `research/hypothesis_v1.1.md` | The **transition-window** claim: the drift between the adoption announcement and the firm's first full report under the new standard, with the firm-level pre-adoption information quality as the state, identified **within jurisdiction**, two-sided. Three kill conditions added (country-level artefact; pre-emption consumed; state adds nothing after costs). |
| `research/specification_v1.1.md` | The **executable treatment**: a jurisdiction-level standard-application event with a registered panel membership rule, a not-yet-treated matched control group matched on fiscal-period-end proximity, the mandatory country-level controls and the three-part way they are *imposed*, the announcement → first-full-report entry/exit rule, the pre-emption kill-signal window, the mechanical-magnitude attribution across all three primary statements, and the clarification of the v1.0 benchmark-window wording defect. |
| `research/preregistration_v1.1.md` | Splits re-anchored on the decision timestamp **T-A**; the **retrospective panel's empty holdout declared in advance** with its consequence fixed (the retrospective panel cannot satisfy protocol gate 4 on its own); the **prospective holdout arm PH-1** registered; the feasibility, cluster-count, power and stopping rules frozen so that a short panel cannot later justify a design change; the claimed published reading pre-registered. |
| `research/data_acquisition_plan.md` | The data side of execution: sources, file layout, record schemas, manifest and SHA-256 scheme, cache location **outside** the repository, rate limits, per-OAM verification pass, and the explicit authorisation checklist with a trigger sequence. |
| `research/source_ledger.csv` | 13 new rows, **S-42 … S-54**: the dossier sources that v1.1 relies on, each carrying its dossier identifier and an honest verification status. |

**Design choices and their grounds (all recorded in `research/decision_log.md`):**

1. **Treatment = jurisdiction-level standard application, not a firm-level adopter
   partition.** A binary first-time-vs-second-time partition is what V-009's
   Cycle-56 item 1 and the Cycle-111 correction notice forbid, because a single-package
   adoption collapses it into the historical comparison the literature has already
   populated (S-35, S-36). The design identifies the effect from **staggered
   application timing** and a **within-jurisdiction firm-level state contrast** instead.
2. **The state contrast is the campaign's own claim; the country-level effects are
   not.** Enforcement quality (S-43, S-52) and linguistic distance (S-44) are
   **published conditioners** and enter as mandatory controls, with the rule that a
   result surviving only when they are omitted is a **fail** (V-009 Cycle-52 item 2;
   Cycle-113 item 1).
3. **The claimed reading is the discontinuity-at-adoption reading** (S-42); the
   comparability-as-driver reading is a descriptive control, and a null under the
   claimed reading is not a kill of the other (V-009 Cycle-52 item 3).
4. **The transition window is the primary window; the v1.0 post-first-report window
   is demoted to a descriptive control** (V-009 Cycle-58 item 2).
5. **The pre-emption window is registered as a kill signal, not a null** (V-009
   Cycle-113 items 2 and 4; Cycle-114 item 2), in its retrospective analogue: the
   first disclosure of the accounting break at the firm's first interim report.
6. **The IFRS 18 prospective arm A is not used.** Its state cannot be constructed for
   the retrospective panel (those standards carried no mandated pre-adoption impact
   disclosure), and its G-33 dependency is unmet (2026 quantification rate 0 of 13 on a
   convenience sample; the ESMA-supervised population rate not yet published —
   S-50, S-51, S-49).

**Hypothesis or acceptance criteria altered?** **Yes — this is a new registered version,
and it is registered BEFORE any outcome-period return exists.** No threshold, cost,
window length, acceptance criterion or kill condition was loosened. The acceptance
criteria are carried forward unchanged and two are added: acceptance criterion 8 (the
within-jurisdiction estimate exists and survives the mandatory country-level controls)
and the explicit declaration that the retrospective panel has an **empty** holdout.
The v1.0 acceptance thresholds (|mean| ≥ 0.5% per event, ≥12 independent events, ≥200
treatment firms, break-even ≥ 2× the conservative cost, leave-one-event-out <50%) are
unchanged.

**Known weaknesses carried forward, now sharpened.**

- The **EU contributes one timing cohort**, not 27 independent clusters, because all
  EU member states share one application date. This is stated in advance so it cannot
  later be discovered as a power surprise.
- The expected cluster count (≈28–48) depends on Stratum B's **coverage**, which
  depends on the price and filing routes for the first-time-adopter jurisdictions. If
  Stratum B does not realise, the count falls to ≈8 and the primary estimand is
  **inconclusive by construction**. The rule is frozen in advance.
- The retrospective panel **cannot satisfy protocol promotion gate 4 on its own**; the
  genuinely prospective holdout is **PH-1** (the IFRS 18 first-application window),
  which requires a separate v1.2 registration before the first IFRS 18 report is
  published.

## Next iteration (reserved)

The next prompt improvement must address the highest-value unresolved question.
As of this entry, the **design** question is resolved: v1.1 is registered, executable in
principle, and compliant with every binding dossier amendment. The highest-value
unresolved question is now the **data and authorisation** question: the v1.1 panel
cannot be assembled until the maintainer answers the authorisation checklist in
`research/data_acquisition_plan.md` §8 (A1 market data, A2 public harvesting, A3
repository policy, A4 panel scope, A5 prospective holdout).

Two secondary questions are also now open and are **named** so they are not lost:
(i) the **day-level UK endorsement instrument date** and whether the UK route publishes a
filing **time** (T-R needs a time), and (ii) the **day-level ASU 2016-01 issuance
date**, both recorded as verification gaps in `research/event_calendar.csv`; and (iii)
whether the published linguistic-distance measure (S-44) can be reproduced exactly from
its source, or whether the registered fallback scale must be used.

A prompt iteration that merely rewords the hypothesis without resolving one of those
questions is not progress.

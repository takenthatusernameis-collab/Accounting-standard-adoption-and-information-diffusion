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

## Next iteration (reserved)

The next prompt improvement must address the highest-value unresolved question.
As of this entry, that question is **no longer the data route** — the data route
is now assessed, a route is recommended and an authorisation request is on the
table (`research/data_route_assessment.md` §6.5). The highest-value unresolved
question is the **registered design revision (v1.1)** described in Iteration 7,
because until it exists the campaign has no executable estimand, and no amount of
data acquisition changes that. A prompt iteration that merely rewords the
hypothesis without resolving that decision is not progress.

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

## Next iteration (reserved)

The next prompt improvement must address the highest-value unresolved question.
As of this entry, that question is the **data route**: which point-in-time
market and filing data can be legally and technically obtained for the frozen
event panel, and what the reduced-power fallback looks like if the licensed
route is unavailable (`research/data_manifest.md` §5). A prompt iteration that
merely rewords the hypothesis without resolving a decision is not progress.

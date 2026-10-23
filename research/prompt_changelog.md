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

## 2026-10-22 — Iteration 9: the acquirer is built, the named date gaps are closed, the panel is materialised, and v1.2 is registered

**Problem.** Three things stood between the campaign and an executable data phase.
(i) The EDGAR acquirer existed only as prose in `research/data_acquisition_plan.md`;
nothing was implemented, so the moment authorisation arrived the pipeline would have
had to be written from scratch and the acceptance-time parse would have been
unverified. (ii) Two named verification gaps sat on the critical path — the day-level
UK endorsement instrument date for IFRS 15 and IFRS 16, and the day-level ASU 2016-01
issuance date — and a registered event (EV-202) had no row in the calendar at all.
(iii) The registered panel of `research/specification_v1.1.md` §1.1 existed as a *rule*
but not as a *file*, so the panel's membership could not be frozen, audited or handed
to an acquirer. Separately, the campaign's only promotable test — the prospective
holdout arm PH-1 — had no registered version, and the protocol requires it to be
registered before the first IFRS 18 report can be published.

**Change.** All four are now done. No frozen artefact was edited in place.

| Artefact | What it registers |
|---|---|
| `scripts/sec_acceptance.py` | The SGML acceptance-time parser. `ACCEPTANCE-DATETIME` (`YYYYMMDDHHMMSS`, Eastern) read from the raw SGML header and converted to UTC with the US daylight-saving offset **in effect at that local wall time**. The spring-forward **23-hour** day and the fall-back **25-hour** day are handled explicitly: a nonexistent local time is quarantined, an ambiguous local time is quarantined **with both candidate UTC readings recorded**, and neither is ever silently resolved or defaulted. The submissions-JSON `acceptanceDateTime` field is refused as a source (S-41). |
| `scripts/data_cache.py` | The cache layout and the repository-policy guard (D-015): raw data is cached **outside** the working tree, and a cache root inside the repository is refused before any write. |
| `scripts/data_manifest.py` | The append-only JSONL retrieval manifest, the SHA-256 over the **raw bytes as received**, and the rule that a failed retrieval is recorded **as a failed retrieval** with its HTTP status and exception text, never as an absence. |
| `scripts/sec_edgar.py` | The EDGAR acquirer: the submissions JSON per CIK (identifier history only), the filing index per periodic report, and the complete submission text file; a declared User-Agent that the acquirer **refuses to run without**; a rate limiter capped at **2 requests per second**; `Retry-After` honoured with a bounded retry budget; every retrieval, successful or not, written to the manifest. |
| `tests/test_sec_acceptance.py`, `tests/test_data_cache.py`, `tests/test_data_manifest.py`, `tests/test_sec_edgar.py` | **48 new tests** against synthetic fixtures, including the DST spring-forward and fall-back cases, the 23-hour and 25-hour days, a missing `ACCEPTANCE-DATETIME`, a malformed value, a midnight boundary, a rate-limiter assertion, a `Retry-After` assertion and a failed-retrieval assertion. The suite makes **zero network calls**. Total: **115 passing** (67 before). |
| `research/event_calendar.csv` | **Two gaps closed and one row added.** EV-103 (ASU 2016-01) is now primary-verified with the day-level issuance date **2016-01-05** and the ASU's own effective-date sentence — and its effective date is **corrected**: it previously carried 2018-12-15 for public business entities and 2019-12-15 for all other entities, both one year late, and `first_affected_fiscal_year_start` was 2019-01-01; the ASU's own text gives 2017-12-15 and 2018-12-15 respectively, and the 2018-12-15 date previously recorded belongs to ASU 2016-02 (EV-102). **The ASU 2016-01 event therefore moves one year earlier.** EV-201 (IFRS 15, UK) is now primary-verified with the day-level UK legal instrument — **SI 2015/980, made 26 March 2015, in force 6 April 2015**, regulation 2(2) giving the 1 January 2016 mandatory date and the 1 January 2015 early-application arm. **EV-202 (IFRS 16, UK) is added as a row**, with the note that the UK needed no new instrument for IFRS 16 and that its T-A is therefore *inherited* from the EU endorsement. |
| `research/panel_v1.1.csv` | The registered panel **materialised**: 434 rows — 8 complete Stratum A events and 426 Stratum B candidate rows derived **by rule** from a dated, hashed snapshot of the 170 IFRS Foundation jurisdiction profiles. The Stratum B rows carry `in_registered_panel = pending` because three of the five rule conditions cannot be verified until A1 and A2 land. |
| `research/manifests/ifrs_jurisdiction_profiles.jsonl` | The snapshot manifest: 171 records with the URL, HTTP status, byte count, **SHA-256** and retrieval timestamp of every page. The profiles are updated on an ongoing basis, which is exactly why the snapshot is dated and hashed. |
| `research/authorisation_request.md` | The authorisation request in one-click-able form: the five decisions and their consequences quoted verbatim from `research/data_acquisition_plan.md` §8.1, the statement that A2 is zero-cost and highest-value, and the consequence of silence stated plainly. |
| `research/hypothesis_v1.2.md`, `research/specification_v1.2.md`, `research/preregistration_v1.2.md` | **PH-1 registered** as the prospective holdout arm on the IFRS 18 first-application window, **before the first IFRS 18 report can be published**. The retrospective panel is untouched. |
| `research/source_ledger.csv` | 5 new rows, **S-55 … S-59**: SI 2015/980, the EFRAG Endorsement Status Report, FASB ASU 2016-01, the IFRS Foundation profile snapshot and the FRC's FRS 102 (March 2018). |

**Design choices and their grounds (all recorded in `research/decision_log.md`):**

1. **The acceptance time is parsed from the raw SGML header, never from the
   submissions JSON.** The registered design pins it there, and the submissions field
   has been documented to mix UTC and Eastern clock readings (S-41).
2. **A daylight-saving transition stamp is quarantined, not resolved.** A local time
   that does not exist cannot be converted; a local time that happens twice has two
   correct answers and the header does not say which. Both are recorded and counted,
   per `research/data_acquisition_plan.md` §7 rule 2.
3. **The filing index is the SEC's `index-headers.json` payload**, cached at the
   plan's path `raw/sec_edgar/<cik>/<accession-nodashes>/index.json`; the manifest
   records the exact URL that produced it, and the index's acceptance stamp is used
   only as a **cross-check** against the SGML header, with the header authoritative.
4. **The Stratum B panel is derived by rule from the membership authority, and the
   residual uncertainty is recorded rather than decided.** The screen classifies 138
   jurisdictions as IFRS-required for listed domestic public companies, 28 as not, and
   **4 as unresolved** (Bhutan, China, the European Union, Morocco); the 4 are carried
   in the panel with the screen labelled `review-required` and `in_registered_panel =
   pending`, because a rule that cannot decide a case must not guess one.
5. **PH-1 settles the IFRS 18 adopter-type contrast in advance, in the negative.**
   The IFRS 18 instruments converge on one application date and first-time IFRS
   adopters apply the IFRSs "all at once" (S-54), so the contrast degenerates. PH-1
   is therefore a **narrower and weaker** test than the retrospective panel, and is
   registered as such. It is registered anyway because a narrower honest test fixed in
   advance is worth more than a broader one fixed afterwards.
6. **PH-1's expected cluster count is stated in advance, below the minimum.**
   ≈3–10 clusters against a ≥12 minimum, so the PH-1 primary estimand is expected to
   be **inconclusive by construction**. The rule is frozen so that a short arm cannot
   later be used to justify a design change, and the honest consequence — an
   evidential retrospective panel and **no promotable test** — is recorded now rather
   than discovered later.

**Hypothesis or acceptance criteria altered?** **Yes — this is a new registered
version (v1.2), and it is registered BEFORE any outcome-period return exists, and
before the first IFRS 18 report can be published.** No threshold, cost, window length,
acceptance criterion or kill condition was loosened; the thirteen v1.1 kill conditions
are carried forward unchanged and two are added (the once-only reporting rule and the
arm-specific ≥12-cluster / ≥200-firm minima). The v1.0 and v1.1 files are
**byte-identical to their previous versions** and are not edited in place.

**Known weaknesses carried forward, now sharpened.**

- **The ASU 2016-01 event moved one year earlier** (decision D-016). Any statement
  made before this entry that placed the event in 2019 is superseded by the event
  calendar. No return has ever been computed, so nothing downstream is affected.
- **The UK IFRS 16 T-A is inherited, not national.** The UK required no new adoption
  instrument for IFRS 16, so the "UK adoption instrument date" is the EU endorsement
  date. It is a weaker anchor than EV-201's and is flagged as such in the calendar.
- **Whether the UK filing route publishes a filing *time* is still open.** The FCA
  National Storage Mechanism API host answered HTTP 403 to every request from this
  environment, so the published field list could not be read here. T-R needs a
  timestamp, so this must be settled before any UK firm can be timed.
- **The PH-1 panel is not yet enumerated** (`research/panel_v1.2.csv` does not exist)
  and the day-level IFRS 18 adoption instrument date per jurisdiction is not pinned;
  the UK Endorsement Board's IFRS 18 decision date is the first concrete task.
- **The linguistic-distance choice (published measure vs the registered fallback
  ordinal scale) is still unresolved** and must be recorded before the holdout opens.


---

## 2026-10-22 — Iteration 10: the three named verification gaps are closed, the PH-1 panel is materialised, and two date conflicts are recorded rather than resolved

**Problem.** Iteration 9 left three named verification gaps on the critical path and one
required file missing. The gaps were: (i) whether the UK filing route publishes a filing
**time** (T-R needs a timestamp, and the FCA NSM host had answered HTTP 403 from this
environment, so the published field list could not be read); (ii) the **day-level IFRS 18
adoption instrument date** per admitted jurisdiction, the UK Endorsement Board's decision
date first; and (iii) the **linguistic-distance choice**, which the frozen specification
requires to be recorded before the holdout opens. The file was
`research/panel_v1.2.csv` — required by `research/specification_v1.2.md` §1.2 to exist
**before** the PH-1 feasibility audit begins, and absent.

**Change.** All three gaps are now closed or determined, and the file exists. **No frozen
artefact was edited in place**; three new decisions (D-021, D-022, D-023) carry the changes,
and `research/specification_v1.2.md` is untouched.

| Artefact | What it registers |
|---|---|
| `research/panel_v1.2.csv` | The PH-1 panel: **142 rows**, one per (IFRS 18, jurisdiction), in the schema of `research/specification_v1.1.md` §4.2 and with the same three-state `in_registered_panel` discipline. **All 142 rows are `pending`**: conditions 3, 4 and 5 are unverified for every jurisdiction, and condition 2 is verified for three. **Three rows carry a primary-verified day-level T_A** — European Union **2026-02-13**, United Kingdom **2025-12-10**, Saudi Arabia **2024-12-26** — each with a `date_conflict` field recording the competing dates. The other 139 carry an **empty** T_A rather than an inferred one. |
| `scripts/build_panel.py`, `tests/test_build_panel.py` | The builder and its 9 unit tests. The candidate universe is **read back from the Stratum B rows of `research/panel_v1.1.csv`**, so both panel files are built from **one dated, hashed membership vintage** and no new snapshot was taken. No network access. |
| `research/event_calendar.csv` | EV-201 and EV-202 carry the UK filing-timestamp determination. The **retrospective calendar is deliberately not extended** with the IFRS 18 events: adding 2024–2026 rows would destroy its defining property (every registered retrospective event has T-A ≤ 2017-10-31, so the chronological holdout split is empty — D-014). The IFRS 18 events live in `research/panel_v1.2.csv`. |
| `research/decision_log.md` | **D-021** (the UK route publishes a date, not a time), **D-022** (the three IFRS 18 instrument dates pinned; the Saudi conflict recorded), **D-023** (the linguistic-distance measure cannot be reproduced exactly panel-wide, so the registered fallback is selected). |
| `research/source_ledger.csv` | **S-60 … S-71** — twelve primary sources: the EFRAG Endorsement Status Report of 16 February 2026, SOCPA's endorsement document, the Saudi CMA announcement CMA_N_4083, the UKEB IFRS 18 news release and project record, four FCA documents (the NSM FAQ, Technical Note 523.1, the Investor User Guide, the Submitter User Guide, plus PS24/19), the operationalisation detail for S-44, and the Joshi and Lahiri index. **71 sources** in all. |

**The three determinations, in brief.**

1. **The UK NSM publishes a date, not a time.** Its glossary defines "Publication date" as
   "The date a document/announcement was released via a Regulatory Information Service
   (RIS) or uploaded to the NSM"; the Investor User Guide defines "Filing date" as "The date
   at which the information was made available for filing on the NSM". A time *does* exist in
   the plumbing — the PIP-to-NSM schema carries a mandatory `PublishingDate` element
   (`YYYY-MM-DDTHH:MM:SSZ`) — but that schema binds PIPs only **from 3 November 2025** under
   PS24/19. **Consequence, stated now rather than discovered later: the two retrospective UK
   events cannot be timed at all**, because their transition windows (2016-01-01, 2019-01-01)
   precede the timestamp regime, whatever the answer to the remaining verification. The UK
   stays viable for **PH-1**, whose window falls entirely after it. The NSM search API
   answered HTTP 403, so the condition is recorded **unverified, not false**, and the failed
   retrieval is recorded as a failed retrieval.
2. **The IFRS 18 instruments are pinned.** EU **2026-02-13** (endorsement) with OJ publication
   **2026-02-16**; UK **2025-12-10** (UKEB formal adoption — this closes the gap v1.2 left
   open); Saudi Arabia **2024-12-26** (SOCPA adoption). **v1.2 had registered the Saudi date
   2026-06-30, which is the CMA's *early-adoption* decision, not the instrument making IFRS 18
   mandatory.** The applied T-A follows the registered condition (2), and the conflict is written
   into the row's own fields. **Its consequence is recorded too:** the CMA-mandated pre-adoption
   impact disclosure (periods from 2026-04-01) falls **inside** the Saudi transition window
   rather than before it, so Saudi Arabia has **no clean T-PRE anchor**, and whether it enters
   PH-1 at all is an open design question to be settled **before the holdout opens** and never
   by looking at outcomes.
3. **The published linguistic-distance index cannot be reproduced exactly panel-wide.** S-44
   operationalises it as the Joshi and Lahiri (2015) friction index over 192 WALS features,
   averaged, with simple averaging for multi-language countries, and publishes values for its
   84-country 2004–2018 sample. Three obstacles block exact panel-wide reproduction: Ethnologue
   is **licensed and versioned**, the Ethnologue-to-WALS merge was **manual**, and Table 1 does
   not cover the campaign's jurisdictions. The registered condition ("cannot be reproduced
   exactly from its source") is therefore **met**, and the **registered fallback ordinal scale
   is selected by the rule**, with the published values kept as an **external validation of the
   ordering**. The fallback's **category boundaries are still not enumerated**, and that
   enumeration must be added by dated decision before the holdout opens.

**What is still true, and stated so it is not lost.** The campaign is **PARKED — not
validated, not rejected**. The highest-value unresolved question is unchanged: the **data and
authorisation** question. A1, A2 and A3 are entirely outstanding, and A4 now has a concrete
object (the 426 pending Stratum B rows) and A5 a concrete ask (confirmation that the
registered PH-1 arm may be **run**). **No outcome-period return has ever been computed or
inspected.** The test suite is **124 passing** (115 before).

## Next iteration (reserved)

The next prompt improvement must address the highest-value unresolved question.
As of this entry, the **design** question is resolved and so are the three named
verification gaps that sat behind it. v1.1 is registered and compliant with every
binding dossier amendment; v1.2 is registered for the prospective holdout arm; the
retrospective panel and the PH-1 panel are both materialised as files; the acquirer is
implemented and tested; and every event-calendar date is primary-verified.

The highest-value unresolved question is therefore **unchanged** and is the **data and
authorisation** question: neither panel can be assembled into data until the maintainer
answers the authorisation checklist in `research/data_acquisition_plan.md` §8 —
**A1** (market data), **A2** (read-only public harvesting, zero-cost and highest
value), **A3** (repository policy), **A4** (panel scope, which now has a concrete
object in the 426 pending Stratum B rows of `research/panel_v1.1.csv`), and **A5**
(confirmation that the registered PH-1 arm may be **run**). One-click-able form:
`research/authorisation_request.md`.

Three further items are now open and are **named** so they are not lost, all of them
requiring a **dated decision before the holdout opens** and none of them permitting a
look at any outcome:

(i) the **Saudi Arabia T-PRE question** — with T-A at 2024-12-26, the CMA-mandated
pre-adoption impact disclosure falls inside the transition window rather than before
it, so Saudi Arabia has no clean pre-disclosure anchor and its standing in PH-1 must be
settled (exclude, or admit with a separately specified T-PRE rule) — D-022;
(ii) the **category boundaries of the registered fallback linguistic-distance scale**,
which must be enumerated by dated decision now that the fallback is the selected
implementation — D-023;
(iii) the **single remaining UK verification** — whether the NSM search response or
CSV export carries a time-of-day component, which decides whether the UK satisfies
panel condition (j) for events after 3 November 2025 — D-021.

A prompt iteration that merely rewords the hypothesis without resolving one of those
questions is not progress.


## Iteration 11 (2026-10-22, session 5d)

**What changed.** D-029 settled the Saudi Arabia T-PRE question by admitting the Saudi row with a uniform interval rule: the pre-disclosure window [T-A, T-PRE] is well defined if and only if T-A < T-PRE < T-R, where T-PRE is the acceptance timestamp of the firm's first disclosure of the expected IFRS 18 impact under the applicable regime; if no such disclosure exists before T-R, the pre-emption arm is reported as not applicable (named), never null/pass/zero. The decision was registered as v1.3. The preregistration_v1.2.md statement that "the IFRS 18 instruments converge on one application date" was corrected (application dates converge to 2027-01-01 but T-A dates span 17 months: Singapore 2024-10-04, Saudi Arabia 2024-12-26, UK 2025-12-10, Brazil 2025-12-23, EU 2026-02-13), restating cluster arithmetic as ~4-8 (still below ≥12). All fixes made before first IFRS 18 report; no outcome data inspected.

**Why.** Resolved the remaining named design question without looking at outcomes, in accordance with preregistration discipline.


## Iteration 12 (2026-10-22, session 5e)

**What changed.** One more jurisdiction's condition 2 was verified from a primary source read directly in this session (New Zealand, T-A 2024-05-23, S-72) and one more was recorded as attempted and not verified at day level (South Korea, S-73). `research/panel_v1.2.csv` was rebuilt from committed code and now carries **six** primary-verified day-level T-A values instead of five; `scripts/build_panel.py`, `tests/test_build_panel.py` and `research/source_ledger.csv` (now **73** sources) were updated accordingly, and the test suite went from 144 to **145** passing.

**Why.** The prior handoff's **P2** asked for condition 2 to be verified for the jurisdictions whose T-A was empty. New Zealand is a genuine addition: its instrument is a dated statutory instrument with a day-level issuance date, and the XRB page is reachable from this environment. South Korea is the honest negative: K-IFRS 1118 is real and mandatory from 2027-01-01, but no source carries a day, so under D-011 the date stays empty rather than being inferred from the month.

**Hypothesis or acceptance criteria altered?** No. No registered version was edited in place; `research/panel_v1.2.csv` is regenerated by `scripts/build_panel.py` from the same dated, hashed membership vintage, so the panel rule, the thresholds, the ≥12-cluster / ≥200-firm minima and the inconclusive-by-construction consequence fixed in v1.2 and v1.3 are unchanged. The verified cohort count moves from five to six, still below the minimum.

**Still true.** The campaign is **PARKED — not validated, not rejected**. A1 and A2 remain entirely outstanding, and **no outcome-period return has ever been computed or inspected**. The PH-1 panel's 135 remaining rows stay `pending` with empty T_A; condition 2 is not the binding constraint on any of them, conditions 3, 4 and 5 are, and those are exactly the A2 and A1 authorisations.


## Iteration 13 — 2026-10-22 — Paid-provider route and stale authorization blockers resolved (D-031)

**What changed.** The current operating decision now selects Sharadar Stock Prices / SEP for the US price/delisted-name leg and EODHD All World EOD for international and matched-control venues. Read-only public-source harvesting and a PH-1 pre-outcome feasibility audit are authorized under source terms and rate limits. The old A1–A5 request has been superseded as a current decision blocker. Added scripts/price_provider_client.py, offline tests in tests/test_price_provider_client.py, and research/paid_data_route_execution.md.

**Boundaries preserved.** The agent cannot buy subscriptions, open accounts, accept paid terms, or incur unspecified charges. Paid requests require a user-provisioned credential and explicit ACCTCLOCK_ENABLE_PAID_DATA=1. Credentials are not allowed in chat/Git/logs; raw price data remains outside the repository. No provider call, paid pull, bulk filing harvest, Actions run, or return computation was performed by this update.

**Hypothesis and acceptance criteria altered?** No. Frozen v1.0–v1.3 research specifications and their thresholds remain unchanged. The pre-outcome feasibility report still needs to show ≥12 independent clusters, ≥200 treatment firms, acceptable coverage, point-in-time integrity and a valid terminal/delisting-return rule. The expected PH-1 count (~4–8 clusters) remains a material feasibility risk; the test must stop as inconclusive if gates fail.

**Still open.** Actual account access/API credentials; empirical verification of selected plans' exchange-level coverage and terminal-return semantics; actual execution of offline tests in the repo; public filing-acquisition coverage; reconciliation of state/handoff/panel counts; the frozen statistical feasibility gate. The campaign remains **PARKED — not validated, not rejected**.


## Iteration 14 — 2026-10-22 — Harden provider response handling and record network-environment failure

**What changed.** Removed the request's gzip/deflate Accept-Encoding header because the urllib client does not currently implement response decompression; the client now requests parseable JSON/CSV content, and its offline test source asserts the request headers. Two minimal sample-key smoke attempts (Sharadar public test key and EODHD demo pattern) were tried on tiny AAPL date ranges; both failed before HTTP with this terminal's DNS resolution error. The failed retrievals are documented in research/manifests/price_provider_smoke_attempts.jsonl and experiment entry E-025.

**Why.** Do not let a compressed payload reach a parser that assumes uncompressed JSON/CSV, and do not misclassify a local DNS failure as a vendor/API rejection. Use a network-enabled execution environment for the next bounded test.

**Hypothesis or acceptance criteria altered?** No. The price client is still untested in a live-capable environment; new offline tests have not been run in this session. No vendor response was received, no market data were inspected, no paid API request or purchase occurred, and no outcome-period return was computed or inspected. The ≥12 independent-cluster / ≥200 treatment-firm gates and PH-1 once-only discipline remain unchanged. The campaign remains **PARKED — not validated, not rejected**.


## 2026-10-22 — Iteration 7: D-032 free-only route and bottleneck removal

**Change.** Prompt advanced to v1.2. D-032 supersedes D-031's paid-provider direction. All active instructions now prohibit paid vendors, subscriptions, payment-linked trials, paid API calls, purchases, and asking the user to provision paid credentials. The next agent should immediately inventory lawful free sources, reconcile panel counts, run offline tests only where an actual repository environment exists, and execute a pre-outcome feasibility audit. Legacy paid-route documentation is explicitly marked superseded.

**Bottlenecks removed.** No repeated A1–A5 questions, no waiting for paid credentials, and no vendor checkout decision. Independent public-source discovery and code/test audit can proceed immediately.

**Safeguards unchanged.** Frozen hypotheses and preregistrations, ≥12 independent clusters, ≥200 treatment firms, the no-outcome-peeking gate, source terms/rate limits, delisted-security/terminal-return checks, and research-only/no-live-trading boundaries remain binding. Free-source insufficiency must be reported honestly; it does not justify lowering gates or fabricating completeness.

**Hypothesis or acceptance criteria altered?** No. Only the data-access route and operating instructions changed; no outcome data were opened and no performance claim is made.


## Iteration 15 — 2026-10-22 — Four more jurisdictions verified at day level, the cohort gate restated, and v1.4 registered

**What changed.** Condition 2 of the PH-1 membership rule was verified for **four further jurisdictions**, each from a standard-setter or regulator document read directly in session and hashed in `research/manifests/source_ledger_verification.jsonl`: **Philippines** T-A 2024-05-10 (the FSRSC's own register, S-94), **Malaysia** T-A 2024-06-14 (the MASB's statutory notice of issuance, S-91, corroborated by the MASB's own standards list, S-98), **Hong Kong SAR** T-A 2024-07-09 (the HKICPA Financial Reporting Standards Committee's own minutes and their post-meeting issuance note, S-92, which closes the gap D-026 left open), and **Indonesia** T-A 2025-05-28 (the DSAK IAI's own bulletin, S-93). **Pakistan, Sri Lanka and Thailand are recorded as attempted and not verified** and keep an **empty** T_A rather than an inferred one; the Philippine Board of Accountancy resolution failed to retrieve and is recorded as a conflict, not as a date. `research/panel_v1.2.csv` was rebuilt from committed code and now carries **ten** primary-verified day-level T_A values in **ten distinct timing cohorts**, spanning twenty-one months. The panel gains two additive evidence columns, `profile_route_hint` and `timing_cohort`, read from the dated membership snapshot by a fixed deterministic rule in `scripts/build_panel.py`. **v1.4 is registered**: `research/specification_v1.4.md` and `research/preregistration_v1.4.md`.

**Why.** The prior handoff's **P2** asked for condition 2 to be verified for the jurisdictions whose T-A was empty. The decisive quantity turned out to be the number of jurisdictions that issue their own **dated** IFRS 18 instrument, and that is a handful, not a hundred — so the registered expectation had to be restated before the holdout opens rather than discovered afterwards. v1.3 carried an expectation of ≈ 4–8 cohorts; ten are now verified, so the expectation becomes **≈ 10–13 against the unchanged ≥ 12 minimum**. The arm is therefore **no longer certainly inconclusive, and not yet shown to be feasible either**. Two further determinations were fixed in advance: the **profile route is a triage prior and never excludes a jurisdiction** (Brazil, Saudi Arabia and South Korea are the counterexamples carried in the panel's own data), and **Thailand is outside the arm on a T-E ground**, because TFRS 18 applies to periods beginning on or after 1 January 2028, a year after the arm's 2027-01-01 window.

**Hypothesis or acceptance criteria altered?** **No.** The hypothesis is **not** amended: `research/hypothesis_v1.3.md` remains in force, and v1.4 is a specification and pre-registration amendment only. The **≥ 12 independent timing cohorts** minimum, the **≥ 200 treatment firms** minimum, the acceptance criteria, the test order, the split and the exit rules are **unchanged**; v1.2 §5.3's binding rule is restated verbatim in v1.4 §5.3. The registered **once-only** discipline and the no-peeking gate are unchanged. No registered version was edited in place, and no registered date was edited in place.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The 131 pending rows keep an **empty** T_A. The **EU member-state carve-out check** — whether any of the 27 member states holds a permanent derogation from particular endorsed standards, which decides whether the member-state rows can join the 2026-02-13 EU cohort — is **named and outstanding**. **No outcome-period return has been computed or inspected**, no filing archive was harvested, no paid data was pulled, and no workflow was run.


## Iteration 16 — 2026-10-22 — Two concurrently committed lines reconciled by hand; the upstream identifiers keep their numbers

**What changed.** The previous worker session ended with a **bounded remote checkpoint-persistence failure**. The cause was **not** a network, credential or permission fault: two research lines had been committed to this repository **concurrently, from two different runners**, and both had appended to the same three append-only ledgers — the upstream line with **D-031** (paid-provider route), **D-032** (free-only route), **E-023 … E-025** and **S-86 … S-90**, and the session-96 line with its own **D-031**, **D-032**, **E-023** and **S-86 … S-94**. The controller reconciles by fetching and running `git rebase --autostash origin/main`; the rebase stopped on those three ledgers at every attempt, the controller aborted and retried the identical rebase, and the retry budget was consumed. **The conflict was in the content, so no amount of retrying could clear it.**

The reconciliation is by hand and is recorded as **D-035**: the **upstream identifiers keep their numbers**, because they are published, are referenced from the upstream handoff, the protocol file and `research/campaign_state.json`, and record two explicit maintainer instructions; the **local line's identifiers move to the next free numbers** — `D-031 → D-033`, `D-032 → D-034`, `E-023 → E-026`, `S-86 … S-94 → S-91 … S-99`, a uniform shift of five — **with every cross-reference moved with them**, so the decision log, the experiment ledger, the source ledger, the retrieval manifest, the panel builder, the panel file, `research/specification_v1.4.md` and `research/preregistration_v1.4.md` all cite the same number. **Both lines' content is retained in full** and no ledger carries a duplicate identifier. `research/panel_v1.2.csv` regenerates **byte-identically** from committed code, which is the check that the renumbering broke nothing. One **pre-existing upstream** test defect was repaired (**D-036**): the paid-provider redaction test asserted the literal marker against a **percent-encoded** query value — the redaction itself was always correct and the credential never reached the manifest, only the assertion was wrong.

**Nothing was reset or discarded.** The original commit `9093ba4da2bc7488bb5204b758447ef8e1df4e91` is retained at the branch `backup/session-96-local-ahead` and the tag `backup/session-96-local-ahead-9093ba4`, and the pre-reconciliation recovery bundle verifies. The reconciliation is a **rebase, not a history rewrite**: the upstream commits are byte-identical and `origin/main` is an ancestor of the reconciled tip, so the push is a fast-forward.

**Hypothesis or acceptance criteria altered?** **No.** No registered version was edited in place, no threshold, acceptance criterion, panel rule or registered date was moved, no outcome-period return was computed or inspected, no paid provider was contacted and `.github/workflows/main.yml` remains unmodified. The paid-provider adapter stays **inert and out of scope** under D-032.

**A known cosmetic defect, recorded rather than corrected.** The upstream's D-032 entry is filed in this changelog under a **second** heading reading "Iteration 7", which duplicates the original Iteration 7. The numbering in this file is therefore **not unique**. It is recorded here and left as it stands, because renumbering a published entry would break any citation of it; the D-032 entry is unambiguous because its decision ID is given in its own heading.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The data route is **free and lawful public sources only**, per D-032. The test suite is **173 passing, 0 failing**.

## Iteration 17 — 2026-10-22 — Pre-outcome feasibility audit (P3) executed; frozen gates fail, estimand inconclusive by construction

**What changed.** Executed P3 (pre-outcome feasibility audit) under D-032 (free-only route). The EDGAR acquirer was run end-to-end against one live filing (AAPL 10-K 0000320193-25-000079): submissions JSON and the complete submission text were retrieved (HTTP 200), cached outside the repository under `ACCTCLOCK_CACHE`, and SHA-256 hashed in the `sec_edgar` manifest; the SGML `ACCEPTANCE-DATETIME` 20251031060126 (Eastern) parsed DST-correctly to `2025-10-31T10:01:26Z`. The filing-index cross-check source `index-headers.json` returned HTTP 404 and was recorded as a `failed_retrieval`, so the SGML header remains the authoritative acceptance timestamp per the design. The free price source Stooq returns a JavaScript anti-bot challenge and no CSV data; Yahoo Finance is terms-prohibited/unreliable, so delisted/terminal-return coverage is not established (B2 open). Network/DNS (B3) is resolved in this runner. From the committed panel files (authoritative per D-037): `research/panel_v1.2.csv` has 141 rows with 10 verified T-A in 10 distinct timing cohorts (2024-05-10 to 2026-02-13), all rows `pending`; `research/panel_v1.1.csv` has 431 rows (8 Stratum A `true`, 423 Stratum B `pending`). Against the frozen gates — ≥ 12 independent timing cohorts and ≥ 200 treatment firms — the audit publishes 10 cohorts (< 12) and 0 admitted treatment firms (< 200), and cannot establish terminal/delisting returns from free sources. Both gates fail, so the primary estimand is reported as **inconclusive by construction**: no outcome-period return was computed or inspected, PH-1 was not opened, and no registered artefact was edited in place. Recorded as experiment ledger row E-029. Test suite: 173 passing, 0 failing.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule, or registered date was moved. No v1.0–v1.4 file was edited in place.

**Still true.** The campaign is **PARKED — not validated, not rejected**. P0 (free-source inventory, E-028) and P1 (EU member-state carve-out, D-038) are complete; P2 (remaining local-equivalent jurisdictions) is complete with 10 cohorts verified; P3 (feasibility audit) has run and the frozen ≥12 cohort / ≥200 treatment-firm gates fail. No outcome-period return has been computed or inspected; no paid provider was contacted; `.github/workflows/main.yml` remains unmodified; raw data is cached outside the repository.

## Iteration 18 — 2026-10-22 — Park reported honestly; frozen gates fail, next agent tasked

**What changed.** The prior agent task (research/HANDOFF.md §9) is complete: P0–P3 are all finished, and the campaign is reported as parked rather than advanced. The frozen gates fail — **10 verified timing cohorts < 12 required**, **0 admitted treatment firms < 200 required** — and free delisted/terminal-return price coverage is not established (Stooq returns a JavaScript anti-bot challenge; Yahoo Finance is terms-prohibited/unreliable). Even reaching 12 cohorts would not satisfy the ≥200 treatment-firm gate, which requires firm-level data that has not been acquired. **No outcome-period return has been computed or inspected**, and **PH-1 has not been opened**. Recorded as experiment ledger row E-030. Test suite: 173 passing, 0 failing.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4).

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule, or registered date was moved. No v1.0–v1.4 file was edited in place.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task is either to verify +2 more condition-2 jurisdictions (day-level IFRS 18 instruments, each from its own regulator, hashed, empty T_A if unverifiable per D-011) to reach 12 cohorts AND establish ≥200 treatment firms AND terminal/delisting returns from free sources, or to report the park honestly again. No outcome-period return may be computed or inspected before the gate; PH-1 may not be opened unless all gates pass.

## Iteration 19 — 2026-10-23 — Verification pass; park remains correctly reported; handoff rewritten for next agent

**What changed.** Session 121 re-verified the committed state against the durable handoff: `git fetch origin main` shows `origin/main` at `2c34075` (advanced from `0020852` at session 120; remote == HEAD); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. DNS resolves. P0–P3 all complete; campaign remains **PARKED — not validated, not rejected**; frozen gates still fail (11 verified timing cohorts < 12 required; 0 admitted treatment firms < 200 required); free delisted/terminal-return price coverage not established (Stooq JS anti-bot challenge, Yahoo terms-prohibited/unreliable). No new primary source read, no filing archive harvested, no paid provider contacted, no outcome-period return computed or inspected, no GitHub Actions run. Prior agent task (report the park honestly, E-030/E-032, Iteration 18) remains complete. §9 initial task message rewritten for the next agent. Experiment ledger row E-033 recorded; `research/campaign_state.json` updated; `research/HANDOFF.md` header, §1-2 notes, §9 and §10 updated.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4).

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule, or registered date was moved. No v1.0–v1.4 file was edited in place.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task is either to verify +1 more condition-2 jurisdiction to reach 12 cohorts AND establish ≥200 treatment firms AND terminal/delisting returns from free sources, or to report the park honestly again. No outcome-period return may be computed or inspected before the gate; PH-1 may not be opened unless all gates pass.

## Iteration 20 — 2026-10-23 — Verification pass; park remains correctly reported; handoff updated for next agent

**What changed.** Session 131 re-verified the committed state against the durable handoff: `git fetch origin main` shows `origin/main` at `e75972a` (remote == HEAD); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. DNS resolves. P0–P3 all complete; campaign remains **PARKED — not validated, not rejected**; frozen gates still fail (11 verified timing cohorts < 12 required; 0 admitted treatment firms < 200 required); free delisted/terminal-return price coverage not established. No new primary source read, no filing archive harvested, no paid provider contacted, no outcome-period return computed or inspected, no GitHub Actions run. Prior agent task (report the park honestly, E-035) complete. Experiment ledger row E-036 recorded; `research/campaign_state.json` updated; `research/HANDOFF.md` header, session notes and §10 updated. §9 initial task message carried forward for the next agent.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4).

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule, or registered date was moved. No v1.0–v1.4 file was edited in place.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task is either to verify +1 more condition-2 jurisdiction to reach 12 cohorts AND establish ≥200 treatment firms AND terminal/delisting returns from free sources, or to report the park honestly again. No outcome-period return may be computed or inspected before the gate; PH-1 may not be opened unless all gates pass.

## Iteration 21 — 2026-10-23 — Verification pass; park remains correctly reported; handoff updated for next agent

**What changed.** Session 132 re-verified the committed state against the durable handoff: `git fetch origin main` shows `origin/main` at `2efe2a3` (remote == HEAD); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. DNS resolves (172.66.147.243). P0–P3 all complete; campaign remains **PARKED — not validated, not rejected**; frozen gates still fail (11 verified timing cohorts < 12 required; 0 admitted treatment firms < 200 required); free delisted/terminal-return price coverage not established. No new primary source read, no filing archive harvested, no paid provider contacted, no outcome-period return computed or inspected, no GitHub Actions run. Prior agent task (report the park honestly, E-036) complete. Experiment ledger row E-037 recorded; `research/campaign_state.json` updated; `research/HANDOFF.md` header, §9 and §10 updated. §9 initial task message carried forward for the next agent.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4).

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule, or registered date was moved. No v1.0–v1.4 file was edited in place.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task is either to verify +1 more condition-2 jurisdiction to reach 12 cohorts AND establish ≥200 treatment firms AND terminal/delisting returns from free sources, or to report the park honestly again. No outcome-period return may be computed or inspected before the gate; PH-1 may not be opened unless all gates pass.

## Iteration 22 — 2026-10-23 — Condition-2 verification pass; the frozen ≥ 12 timing-cohort gate is satisfied for the first time

**What changed.** Session 137 verified condition 2 of the PH-1 membership rule for **South Korea** from the Korean Accounting Standards Board's **own instrument register** (`https://www.kasb.or.kr/front/board/accountingAllList.do`, source ledger **S-105**, read directly and hashed), which lists **K-IFRS No. 1118** with the day-level date **2025-12-18**. This closes the D-030 finding that no source consulted carried a day-level issuance date. The verified set is now **twelve** instruments in **twelve distinct timing cohorts** (2024-05-10 Philippines, 2024-05-23 New Zealand, 2024-06-14 Malaysia, 2024-07-09 Hong Kong SAR, 2024-10-04 Singapore, 2024-12-26 Saudi Arabia, 2025-05-28 Indonesia, 2025-12-10 United Kingdom, **2025-12-18 South Korea**, 2025-12-23 Brazil, 2026-02-13 European Union, 2026-09-09 Bhutan), spanning twenty-seven months.

`scripts/build_panel.py` gained the South Korea instrument entry; `tests/test_build_panel.py` was updated to assert twelve verified jurisdictions, a day-level T-A of 2025-12-18 for South Korea, and a distinct timing-cohort count of **12** (`test_distinct_timing_cohort_count_is_twelve`). `research/panel_v1.2.csv` regenerates from committed code at **141 rows / 12 verified T-A / 12 distinct cohorts**. `research/source_ledger.csv` now holds **105** sources (S-105 added) and `research/manifests/source_ledger_verification.jsonl` carries the hashed retrieval. Decision **D-039** and experiment ledger row **E-039** record the pass. The experiment ledger was also repaired: row **E-031** (the session-115 test-fix pass) was missing from the committed CSV although referenced from the durable handoff and `research/campaign_state.json`, a gap left by the checkpoint-persistence failure of session 96; it is restored at its proper sequence number, verbatim from that durable record, so the ledger now runs **E-000 … E-039** with no gap and no duplicate. `python3 -m pytest -q tests/` → **173 passed, 0 failing**.

**Why.** The frozen feasibility gate requires **≥ 12 independent timing cohorts**; the handover state had eleven. This was the single remaining condition-2 verification that could move the count, and it was executed under D-032's free-only route against the standard setter's own public register, with no paid service, no filing-archive harvest and no GitHub Actions run.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule or registered date was moved, and no v1.0–v1.4 file was edited in place. The **≥ 12** minimum was **satisfied by adding a verified cohort, not by lowering the number**.

**Still true, and now sharper.** The campaign is **PARKED — not validated, not rejected**. One of the three frozen gates now passes; the other two still fail, and they are the hard ones:

| Gate | Required | Achieved | Status |
|---|---|---|---|
| Independent timing cohorts | ≥ 12 | **12** | **MET** |
| Admitted treatment firms | ≥ 200 | **0** | **FAIL** |
| Free delisted/terminal-return price coverage | established | not established (Stooq JS anti-bot challenge; Yahoo terms-prohibited/unreliable) | **FAIL** |

The treatment-firm gate needs firm-level data that has not been acquired (conditions 3, 4 and 5 are unverified for all 141 PH-1 rows), and the terminal-return gate needs empirical coverage evidence from a free source. Under `research/preregistration_v1.4.md` §5.3 the primary estimand is **inconclusive by construction** until **all three** gates pass, so PH-1 stays closed and **no outcome-period return may be computed or inspected**.

**Reverses if.** A primary source from the KASB or the FSS carrying a different day-level date for K-IFRS No. 1118 (the conflict is then written into the row's own `date_conflict` field per D-011 and a new decision is logged); or the instrument text proves the register's date to be a metadata artefact rather than the establishment date (the PDF itself was not directly retrievable, which is recorded as a limitation in D-039 and S-105, not hidden).

## Iteration 23 — 2026-10-23 — Verification pass; the handoff is reconciled to the committed state

**What changed.** Session 138 re-verified the committed state against the handoff: `git fetch origin main` shows `origin/main` at `29c6e07` (remote == HEAD), `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. DNS resolves. The durable handoff was found to be **stale** — its header, §2, §4, §9 and §10 still quoted **11** verified timing cohorts, although the committed `research/campaign_state.json`, `research/decision_log.md` (D-039), `research/prompt_changelog.md` (Iteration 22) and `research/experiment_ledger.csv` (E-039) had already recorded the session-137 South Korea pass at **12**. `research/HANDOFF.md` was brought into line with the committed files; `research/campaign_state.json` gained a session-138 note; experiment ledger row **E-040** was appended. `research/panel_v1.2.csv` was regenerated from committed code and compared byte-identically with `cmp` (141 rows / 12 verified T-A / 12 distinct cohorts). No registered artefact was edited in place, and no v1.0–v1.4 file was touched.

**Why.** A handoff that contradicts the committed state is a hazard for the next agent (it would task them with verifying a 13th cohort to reach 12). The committed files are authoritative (D-037); the prose is corrected to match them, exactly as D-037 did the first time.

**Hypothesis or acceptance criteria altered?** **No.** No threshold, acceptance criterion, test order, split, panel rule or registered date was moved. No v1.0–v1.4 file was edited in place. The **≥ 12** minimum was met by adding a verified cohort (D-039), not by lowering the number, and that is what the reconciled handoff now records.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The cohort gate passes (12 ≥ 12); the treatment-firm gate (0 < 200) and the terminal-return gate both still fail, so the primary estimand remains **inconclusive by construction** and PH-1 stays closed. No outcome-period return has been computed or inspected.

## Iteration 25 — 2026-10-23 — Verification pass; one pre-existing JSON defect repaired; handoff and §9 rewritten for the next agent

**What changed.** Session 150 re-verified the committed state against the durable handoff: `git fetch origin main` → `origin/main` at `fb9c790` (remote == local HEAD), `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**; DNS resolves. Panel counts were re-derived by **parsing the committed files** (D-037): `panel_v1.1.csv` 431 rows (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` 141 rows with **12** non-empty T-A values in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all 141 rows `pending`, and the file regenerates **byte-identically** from committed code. Source ledger holds **100** records (S-01…S-99 plus S-105; S-100…S-104 exist only in `research/manifests/p1_carveout_check.jsonl` and were never appended to the ledger — parse the file, do not trust a quoted count); decision log D-001…D-040; experiment ledger E-000…E-043.

**One repair, recorded as a decision.** Loading `research/campaign_state.json` with `json.load` **failed**: `Expecting value: line 39 column 3`. The cause is a **trailing comma** after the last element of the `"notes"` array (`...next agent.",\n  ],`). The defect is **pre-existing** — it is present at the prior handoff tip `ca251b1` and at every earlier tip back to at least `29c6e07`, so it was introduced by an earlier session's edit, not this one. The comma was removed (**D-040**); `git diff` shows a single one-line change (one insertion, one deletion) and the file now parses with all **35** notes intact and no other byte changed. This is recorded because a machine-readable state file that cannot be parsed is not a state file, and because every prior "verification pass" from sessions 133–149 that reloaded this file would have hit the same error — those passes were reporting a check that had not actually been run.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4). The cohort gate is satisfied and cannot be un-met without a primary-source contradiction (D-011); the treatment-firm gate requires firm-level data that has not been acquired, and the terminal-return gate requires empirical coverage evidence from a free source — neither can be advanced under current constraints.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule or registered date was moved. No v1.0–v1.4 file was edited in place. The only file edited outside the ledgers is `research/campaign_state.json`, and only one character of it — a syntax repair, not a content change.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task: do not compute outcome returns or open PH-1; the binding constraint is ≥200 admitted treatment firms (conditions 3–5 unverified for all 141 PH-1 rows) plus free delisted/terminal-return coverage. Report the park honestly if gates cannot be advanced. Keep `research/results.md` reporting no results; run `python3 -m pytest -q tests/` and report the count.

## Iteration 28 — 2026-10-23 — Verification pass; the free price-source gate re-audited live and still fails (D-042)

**What changed.** Session 160 re-verified the committed state against the durable handoff: `git fetch origin main` → `origin/main` at `ce5753c` (remote == HEAD); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**; DNS resolves for all 12 candidate hosts; `research/campaign_state.json` loads with `json.load` and parses (the D-040 repair holds). The prior agent task (park reported honestly, E-039…E-046, Iterations 22–28) remains complete. Panel counts re-derived by **parsing the committed files** (D-037): `panel_v1.1.csv` 431 rows (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` 141 rows with **12** non-empty T-A in **12** distinct timing cohorts (2024-05-10, 2024-05-23, 2024-06-14, 2024-07-09, 2024-10-04, 2024-12-26, 2025-05-28, 2025-12-10, 2025-12-18, 2025-12-23, 2026-02-13, 2026-09-09), all 141 rows `pending`, and the file regenerates **byte-identically** from committed code (re-built and compared with `cmp`). Source ledger holds **100** records (S-01…S-99 plus S-105; S-100…S-104 exist only in `research/manifests/p1_carveout_check.jsonl` and were never appended to the ledger — parse the file, do not trust a quoted count); decision log D-001…D-042; experiment ledger E-000…E-047.

The session then re-audited the **free price-source gate (B2)** live rather than carrying the prior session's findings forward on trust, because that audit predates this environment's DNS recovery. Twelve candidate hosts resolve; nine free price sources were probed over HTTP. **Stooq** returns a JavaScript anti-bot challenge with no CSV data (confirms the prior finding); **Yahoo Finance** returns HTTP 429 on every host for live and delisted tickers alike across a 90-second cooldown, and its terms prohibit automated harvesting; **Alpha Vantage**'s demo key returns a registration message, not data; **IEX Cloud** and the **Nasdaq API** time out; **Barchart** returns live quotes only; **Investing.com** returns HTTP 403; **Marketbeat** and **Tradingview** return HTML marketing pages. **No free candidate delivers a daily price series for a delisted security**, so free delisted/terminal-return coverage is **not established**. Recorded as decision **D-042** and experiment-ledger row **E-047**.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4). The cohort gate is satisfied and cannot be un-met without a primary-source contradiction (D-011); the treatment-firm gate requires firm-level data that has not been acquired, and the terminal-return gate requires empirical coverage evidence from a free source. This session's audit supplies the missing empirical evidence, and the evidence is negative: B2 stays open, and under D-032's own caveat that does not justify lowering the gate or asserting completeness.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule or registered date was moved. No v1.0–v1.4 file was edited in place. The only files edited outside the ledgers are `research/decision_log.md` (D-042), `research/experiment_ledger.csv` (E-047), `research/campaign_state.json` (one prepended note and `updated_at`) and `research/prompt_changelog.md` (this iteration).

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task: do not compute outcome returns or open PH-1; the binding constraint is ≥200 admitted treatment firms (conditions 3–5 unverified for all 141 PH-1 rows) plus free delisted/terminal-return coverage. Report the park honestly if gates cannot be advanced. Keep `research/results.md` reporting no results; run `python3 -m pytest -q tests/` and report the count.

## Iteration 27 — 2026-10-23 — Verification pass; EDGAR acquirer repaired end-to-end against a live filing (D-041)

**What changed.** Session 156 re-verified the committed state against the durable handoff: `git fetch origin main` → `origin/main` at `29c18d7` (remote == HEAD); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing** (the suite gained four new tests for the repaired paths and lost none); DNS resolves; `research/campaign_state.json` loads with `json.load` and parses. The prior agent task (park reported honestly, E-039…E-044, Iterations 22–27) remains complete. Rather than re-verify the EDGAR acquirer only against its own fixtures, the acquirer was re-run end-to-end against a live filing (AAPL 10-K `0000320193-25-000079`) and it **failed at the first parse**, which is how three transport defects were found and repaired (D-041): (1) EDGAR serves the complete submission text gzip-compressed though the URL ends in `.txt`; (2) `index-headers.json` is no longer served by EDGAR (HTTP 404 after the 2025-10-31 re-format), so the acquirer now fetches `index.json` and `<accession>-index-headers.html`; (3) `iter_header_fields` skipped every line beginning with `<`, silently dropping the tag-form header fields. After the repair all four artefacts retrieve HTTP 200, `ACCEPTANCE-DATETIME 20251031060126` (Eastern) parses to **2025-10-31T10:01:26Z**, the SGML-header stamp agrees with the per-filing header block, and all four manifest records re-hash against the cached files. The four artefacts are cached outside the repository under `ACCTCLOCK_CACHE` and are not committed. Panel counts re-derived by parsing the committed files (D-037): `panel_v1.1.csv` 431 rows (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` 141 rows with **12** non-empty T-A in **12** distinct timing cohorts, all 141 rows `pending`, regenerates byte-identically from committed code. Source ledger holds **100** records (S-01…S-99 plus S-105); decision log D-001…D-041; experiment ledger E-000…E-045.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4). The cohort gate is satisfied and cannot be un-met without a primary-source contradiction (D-011); the treatment-firm gate requires firm-level data that has not been acquired, and the terminal-return gate requires empirical coverage evidence from a free source — neither can be advanced under current constraints. The acquirer repair removes the last mechanical blocker on the filing side of the free route but does not by itself advance any gate.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule or registered date was moved. No v1.0–v1.4 file was edited in place. The only files edited outside the ledgers are `scripts/sec_edgar.py`, `scripts/sec_acceptance.py`, `scripts/data_cache.py`, two new fixtures and their tests, plus `research/campaign_state.json` (one prepended note and `updated_at`).

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task: do not compute outcome returns or open PH-1; the binding constraint is ≥200 admitted treatment firms (conditions 3–5 unverified for all 141 PH-1 rows) plus free delisted/terminal-return coverage. Report the park honestly if gates cannot be advanced. Keep `research/results.md` reporting no results; run `python3 -m pytest -q tests/` and report the count.

## Iteration 26 — 2026-10-23 — Verification pass; handoff, campaign state and §9 rewritten for the next agent

**What changed.** Session 153 re-verified the committed state against the durable handoff: `git fetch origin main` → `origin/main` at `4cc0858` (remote == HEAD); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**; DNS resolves. The remote had advanced past the prior tip `f6019ca` by two checkpoint commits (`7550d6f`, `4cc0858`), but the only content change was a "session 152" verification note appended to `research/HANDOFF.md` §12 — no ledger, panel, code or registered artefact moved. The prior agent task (park reported honestly, E-039…E-043, Iterations 22–25) remains complete. Panel counts were re-derived by **parsing the committed files** (D-037): `panel_v1.1.csv` 431 rows (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` 141 rows with **12** non-empty T-A values in **12** distinct timing cohorts (2024-05-10, 2024-05-23, 2024-06-14, 2024-07-09, 2024-10-04, 2024-12-26, 2025-05-28, 2025-12-10, 2025-12-18, 2025-12-23, 2026-02-13, 2026-09-09), all 141 rows `pending`, and the file regenerates **byte-identically** from committed code. Source ledger holds **100** records (S-01…S-99 plus S-105; S-100…S-104 exist only in `research/manifests/p1_carveout_check.jsonl` and were never appended to the ledger — parse the file, do not trust a quoted count); decision log D-001…D-040; experiment ledger E-000…E-044. `research/campaign_state.json` was loaded with `json.load` and **parses** (the D-040 repair holds), and gained a session-153 note as its new first element (now **37**), with `updated_at` set to the session-153 timestamp and no other byte changed.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4). The cohort gate is satisfied and cannot be un-met without a primary-source contradiction (D-011); the treatment-firm gate requires firm-level data that has not been acquired, and the terminal-return gate requires empirical coverage evidence from a free source — neither can be advanced under current constraints.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule or registered date was moved. No v1.0–v1.4 file was edited in place. The only files edited outside the ledgers are `research/campaign_state.json` (one prepended note and `updated_at`) and `research/HANDOFF.md` (this session's note, the header, §9 and §10).

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task: do not compute outcome returns or open PH-1; the binding constraint is ≥200 admitted treatment firms (conditions 3–5 unverified for all 141 PH-1 rows) plus free delisted/terminal-return coverage. Report the park honestly if gates cannot be advanced. Keep `research/results.md` reporting no results; run `python3 -m pytest -q tests/` and report the count.

## Iteration 24 — 2026-10-23 — Verification pass; park remains correctly reported; handoff carried forward for next agent

**What changed.** Session 145 re-verified the committed state against the durable handoff: `git fetch origin main` → origin/main at `ca89c5b` (remote == HEAD); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. DNS resolves. P0–P3 all complete; campaign remains **PARKED — not validated, not rejected**; frozen gates: **12 verified timing cohorts ≥ 12 (MET)**, **0 admitted treatment firms < 200 (FAIL)**, free delisted/terminal-return price coverage not established (FAIL). No new primary source read, no filing archive harvested, no paid provider contacted, no outcome-period return computed or inspected, no GitHub Actions run. Prior agent task (park reported honestly, E-039/E-040, Iterations 22-23) remains complete. `research/HANDOFF.md` (header, §9, §10, session notes), `research/campaign_state.json` (session-145 note, `updated_at`, `execution_status`), `research/experiment_ledger.csv` (row E-041) and `research/prompt_changelog.md` (this iteration) updated. §9 initial task message carried forward for the next agent.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4). The cohort gate is satisfied and cannot be un-met without a primary-source contradiction (D-011); the treatment-firm gate requires firm-level data that has not been acquired, and the terminal-return gate requires empirical coverage evidence from a free source — neither can be advanced under current constraints.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule, or registered date was moved. No v1.0–v1.4 file was edited in place.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task: do not compute outcome returns or open PH-1; the binding constraint is ≥200 admitted treatment firms (conditions 3–5 unverified for all 141 PH-1 rows) plus free delisted/terminal-return coverage. Report the park honestly if gates cannot be advanced. Keep `research/results.md` reporting no results; run `python3 -m pytest -q tests/` and report the count.

---

## Iteration 29 — 2026-10-23 — Verification pass (session 162); the remote had advanced by a checkpoint commit and no rebase was needed

**What changed.** Session 162 re-verified the committed state against the durable handoff: `git fetch origin main` → `origin/main` at **`5088681`** (remote == HEAD), advanced from the prior tip `ce5753c` by one checkpoint commit (`5088681 chore(kilo): checkpoint agent session`, 1 file changed, 76 insertions / 123 deletions, `research/HANDOFF.md` only); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing** (1.23 s). DNS resolves. Because the remote's advance touched only the handoff and **not** the three append-only ledgers, the D-035 reconciliation precondition did not arise — no rebase was attempted and no conflict occurred. Panel counts were re-derived by **parsing the committed files** (D-037): `panel_v1.1.csv` 431 rows (8 `in_registered_panel=true`, 423 pending; 8 non-empty T-A in 7 distinct retrospective cohorts, all ≤ 2017-10-31); `panel_v1.2.csv` 141 rows with **12** non-empty T-A in **12** distinct timing cohorts (2024-05-10, 2024-05-23, 2024-06-14, 2024-07-09, 2024-10-04, 2024-12-26, 2025-05-28, 2025-12-10, 2025-12-18, 2025-12-23, 2026-02-13, 2026-09-09), all 141 rows `pending`, and the file regenerates **byte-identically** from committed code (rebuilt; working tree clean). Source ledger holds **100** records (S-01…S-99 plus S-105; S-100…S-104 exist only in `research/manifests/p1_carveout_check.jsonl` and were never appended to the ledger — parse the file, do not trust a quoted count); decision log D-001…D-043; experiment ledger E-000…E-048. `research/campaign_state.json` loaded with `json.load` and **parses** (the D-040 repair holds); it gained a session-162 note as its new first element (now **44**), `updated_at` set to the session-162 timestamp, and no other byte changed beyond that note.

**Why.** The park is a determination, not a result: no test has run, so no null or effect can be claimed. The gates are frozen and may not be lowered; the panel may not be narrowed after the feasibility audit (D-016); no paid service may be used (D-032); no GitHub Actions run may be started (protocol Authority item 4). The cohort gate is satisfied and cannot be un-met without a primary-source contradiction (D-011); the treatment-firm gate requires firm-level data that has not been acquired, and the terminal-return gate requires empirical coverage evidence from a free source — neither can be advanced under current constraints.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule or registered date was moved. No v1.0–v1.4 file was edited in place. The only files edited outside the ledgers are `research/campaign_state.json` (one prepended note and `updated_at`) and `research/HANDOFF.md` (this session's note, the header, §9 and §10).

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task: do not compute outcome returns or open PH-1; the binding constraint is ≥200 admitted treatment firms (conditions 3–5 unverified for all 141 PH-1 rows) plus free delisted/terminal-return coverage. Report the park honestly if gates cannot be advanced. Keep `research/results.md` reporting no results; run `python3 -m pytest -q tests/` and report the count.

---

## Iteration 30 — 2026-10-23 — Verification pass; the park is reported honestly; no gate advanced

**What changed.** This session re-verified the committed state against the durable handoff: `git fetch origin main` → `origin/main` at **`92cc7fb`** (remote == HEAD); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**; DNS resolves. Panel counts re-derived by **parsing the committed files** (D-037): `panel_v1.1.csv` 431 rows (8 `in_registered_panel=true`, 423 pending; 8 non-empty T-A in 7 distinct retrospective cohorts, all ≤ 2017-10-31); `panel_v1.2.csv` 141 rows with **12** non-empty T-A in **12** distinct timing cohorts (2024-05-10, 2024-05-23, 2024-06-14, 2024-07-09, 2024-10-04, 2024-12-26, 2025-05-28, 2025-12-10, 2025-12-18, 2025-12-23, 2026-02-13, 2026-09-09), all 141 rows `pending`, regenerates byte-identically from committed code. Source ledger holds **100** records (S-01…S-99 plus S-105; S-100…S-104 exist only in `research/manifests/p1_carveout_check.jsonl` and were never appended — parse the file, do not trust a quoted count); decision log D-001…D-043; experiment ledger E-000…E-049 (row E-049 records this session). `research/campaign_state.json` loaded with `json.load` and **parses** (the D-040 repair holds); it gained a session note as its new first element (now **45**), `updated_at` set to the session timestamp, and no other byte changed. No rebase was needed (the remote's advance touched only the handoff, not the three append-only ledgers), so no D-035 reconciliation was triggered.

**Why.** No gate can be advanced under current constraints: the timing-cohort gate is MET (12 ≥ 12, session 137, D-039) and must not be chased for a 13th cohort (D-011); the treatment-firm gate (0 < 200) requires firm-level data that has not been acquired and conditions 3–5 remain unverified for all 141 PH-1 rows; the free delisted/terminal-return price coverage was re-audited live (session 160, D-042) and remains not established, so those exact probes are not repeated. The primary estimand is therefore **inconclusive_by_construction** on two of the three gates. No new primary source was read, no filing archive harvested, no paid provider contacted, no outcome-period return computed or inspected, no GitHub Actions run, PH-1 not opened, no registered artefact edited in place.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule or registered date was moved. No v1.0–v1.4 file was edited in place.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task: do not compute outcome returns or open PH-1; the binding constraint is ≥200 admitted treatment firms plus free delisted/terminal-return coverage. Report the park honestly if gates cannot be advanced. Keep `research/results.md` reporting no results; run `python3 -m pytest -q tests/` and report the count; before committing, run `git fetch origin main` and reconcile per D-035 if the remote has advanced and your work appends to the three append-only ledgers.

## Iteration 31 — 2026-10-23 — Verification pass; the park is reported honestly; no gate advanced

**What changed.** This session re-verified the committed state against the durable handoff: `git fetch origin main` → `origin/main` at **`1ddd6b7`** (remote == HEAD); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**; DNS resolves. Panel counts re-derived by **parsing the committed files** (D-037): `panel_v1.1.csv` 431 rows (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` 141 rows with **12** non-empty T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all 141 rows `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger holds **100** records (S-01…S-99 plus S-105; S-100…S-104 exist only in `research/manifests/p1_carveout_check.jsonl` and were never appended to the ledger — parse the file, do not trust a quoted count); decision log D-001…D-043; experiment ledger E-000…E-050 (row E-050 records this session). `research/campaign_state.json` loaded with `json.load` and **parses**; gained a session note as its new first element, `updated_at` set to the session timestamp. No rebase was needed (the remote's advance touched only handoff/checkpoint content).

**Why.** No gate can be advanced under current constraints: the timing-cohort gate is MET (12 ≥ 12, session 137, D-039) and must not be chased for a 13th cohort (D-011); the treatment-firm gate (0 < 200) requires firm-level data that has not been acquired and conditions 3–5 remain unverified for all 141 PH-1 rows; the free delisted/terminal-return price coverage was re-audited live (session 160, D-042) and remains not established. The primary estimand is therefore **inconclusive_by_construction** on two of the three gates. No new primary source was read, no filing archive harvested, no paid provider contacted, no outcome-period return computed or inspected, no GitHub Actions run, PH-1 not opened, no registered artefact edited in place.

**Hypothesis or acceptance criteria altered?** **No.** `research/hypothesis_v1.3.md` remains in force; v1.4 does not amend the hypothesis. No threshold, acceptance criterion, test order, split, panel rule or registered date was moved. No v1.0–v1.4 file was edited in place.

**Still true.** The campaign is **PARKED — not validated, not rejected**. The next agent's task: do not compute outcome returns or open PH-1; the binding constraint is ≥200 admitted treatment firms plus free delisted/terminal-return coverage. Report the park honestly if gates cannot be advanced. Keep `research/results.md` reporting no results; run `python3 -m pytest -q tests/` and report the count; before committing, run `git fetch origin main` and reconcile per D-035 if the remote has advanced and your work appends to the three append-only ledgers.

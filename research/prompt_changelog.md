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

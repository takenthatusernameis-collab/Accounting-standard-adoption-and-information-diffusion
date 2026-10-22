# ACCTCLOCK — Handoff

**Last updated:** 2026-10-22 (worker session 107 — verification pass; remote advanced to d9e77aa; tests 173 passing)
**Campaign:** ACCTCLOCK — the accounting-standard adoption / information-diffusion
hypothesis (canonical dossier IDEA-011, specification V-009)
**Status:** **PARKED — not validated, not rejected.** The *design* blocker is cleared,
the *promotable test* is registered and now carries **four** registered amendments
(v1.2 → v1.4), and the *data* blocker is open. **No outcome-period return has ever
been computed or inspected.** **Machine-readable state:**
`research/campaign_state.json` — next step is
`phase3b-data-execution-and-feasibility-audit` (pending; blocked on the free-source
route's own precondition, not on a user question).

**Session 99 note.** Session 99 re-verified the committed state against the handoff:
`git fetch origin main` shows `origin/main` still at `aa072d5` (D-035..D-037), no
advance; `git status` is clean aside from this handoff edit; `python3 -m pytest -q
tests/` → **173 passed, 0 failing**. Blocker **B3 (network/DNS)** remains open:
P0–P3 cannot be executed until the environment resolves the hosts. No new primary
source read, no filing archive harvested, no paid provider contacted, no
outcome-period return computed or inspected, no workflow run. §9 initial task
message carried forward unchanged.

**Session 100 note.** Session 100 re-verified the committed state against the handoff:
`git fetch origin main` shows `origin/main` at `6d44b3b` (checkpoint), no advance
beyond the prior tip; `git status` is clean; `python3 -m pytest -q tests/` →
**173 passed, 0 failing**. P0 (free-source inventory) is now complete:
`research/free_source_inventory/` holds the dated, terms-checked candidate
inventory (inventory.csv/md, feasibility_notes.md), recorded as E-028; the
delisted/terminal-return coverage of every candidate remains unverified.
Blocker **B3 (network/DNS)** remains open: P1–P3 cannot be executed until the
environment resolves the hosts. No new primary source read, no filing archive
harvested, no paid provider contacted, no outcome-period return computed or
inspected, no workflow run. §9 initial task message updated to reflect P0
completion.
---

## 0. Read this first: what happened to the previous session, and why the history looks like it does

**The previous session (96) did not fail because of the network, a credential, or a
permission.** It failed because of a **content conflict**, and the failure mode was
invisible to the controller.

Two research lines had been committed to this repository **concurrently, from two
different runners**:

| | upstream line | session-96 line (the one that could not be pushed) |
|---|---|---|
| Decisions | **D-031** paid-provider route, **D-032** free-only route | its own **D-031**, **D-032** (condition-2 verification for four more jurisdictions; the timing-cohort gate restatement) |
| Experiment rows | **E-023, E-024, E-025** (provider adapter) | its own **E-023** (the same verification) |
| Sources | **S-86 … S-90** (provider documentation) | its own **S-86 … S-94** (nine IFRS 18 instrument sources) |

The two lines share an **identical prefix** — the decision log to D-030, the
experiment ledger to E-022, the source ledger to S-85 — and then both **append** to
the same three append-only ledgers. The controller reconciles by fetching the default
branch and running `git rebase --autostash origin/main`. That rebase **stopped on
those three files every single time**, the controller **aborted and retried the
identical rebase**, and the bounded retry budget was consumed. **No retry could ever
succeed**, because the conflict was in the content.

**What this session did about it.** The reconciliation was done **by hand, once**
(D-035):

1. The **upstream identifiers keep their numbers.** `D-031`, `D-032`, `E-023`,
   `E-024`, `E-025`, `S-86 … S-90` are unchanged. They are published, they are
   referenced from the upstream handoff, the protocol file and
   `research/campaign_state.json`, and they record two explicit maintainer
   instructions. Renumbering them would corrupt published references.
2. The **session-96 identifiers move to the next free numbers**, and every
   cross-reference moves with them: `D-031 → D-033`, `D-032 → D-034`,
   `E-023 → E-026`, `S-86 … S-94 → S-91 … S-99` (a uniform shift of five).
3. **Both lines' content is retained in full.** The decision log now runs D-001 … D-037
   with no duplicate identifier, the experiment ledger E-000 … E-027, and the source
   ledger S-01 … S-99.
4. The reconciliation is a **rebase, not a history rewrite**: the upstream commits are
   byte-identical and `origin/main` is an ancestor of the reconciled tip, so the push
   is a fast-forward.

**Nothing was reset or discarded.** The original commit
`9093ba4da2bc7488bb5204b758447ef8e1df4e91` is preserved verbatim at the branch
`backup/session-96-local-ahead` and the tag `backup/session-96-local-ahead-9093ba4`,
and the pre-reconciliation recovery bundle verifies.

**Two further items this session fixed, both recorded as decisions.** **D-036** — a
**pre-existing upstream** test defect: the paid-provider redaction test asserted the
literal marker against a **percent-encoded** query value; the redaction itself was
always correct, only the assertion was wrong. **D-037** — the **panel counts quoted
in the prose were stale by three sessions**; the committed files are authoritative and
the prose is now corrected (see §4).

**What you, the next agent, need to know about the mechanics.** Two runners can push
to this repository. **Before you commit anything, run `git fetch origin main` and
check whether the remote has moved.** If it has, `git rebase origin/main` **will
conflict on the three ledgers** if your change also appends to them. Resolve it the
same way this session did: **upstream keeps its identifiers, yours take the next free
numbers**, and record the mapping as a decision. Do not let a rebase conflict become
a retry loop.

---

## Current instruction — D-032 (free-only route; supersedes D-031 and the A1–A5 request)

The maintainer explicitly directed the project **away from all paid services**. Do not
use Sharadar, EODHD, paid API tiers, paid subscriptions, trials requiring payment
details, or any request that could incur a charge. Do not ask the user to purchase or
provision credentials. **D-031's provider selection is superseded.** The legacy paid
adapter and its tests remain in the repository but the paid paths are **out of scope**
and must not be invoked.

Use **free and lawful public sources only**: official filings and standards-setter
records, regulators and OAMs, open government datasets, official exchange archives
where their terms permit, and candidate free price archives or endpoints **only after
checking their terms and coverage**. Candidate price sources (Stooq, Yahoo Finance and
the like) are **not presumed complete**, especially for delisted securities and
terminal returns. **No-cost access does not waive the data-quality or terms checks.**

Two previous sample requests failed **before HTTP** with this terminal's DNS
resolution error. That is an **environment limitation, not a source's result**, and it
must not be recorded as one.

**Immediate next step:** inventory the lawful free sources and execute the
**pre-outcome feasibility audit**; reconcile the panel counts with the committed
builder; document source coverage, missingness, delisted-name and terminal-return
limitations, and whether the frozen **≥ 12 independent timing cohorts** /
**≥ 200 treatment firms** gates can be met. If the registered PH-1 sample remains
below threshold, **stop and report inconclusive-by-construction**. No outcome-period
return may be opened before the gate. No paid calls, purchases, workflow runs, trading,
broker connections or deployments are authorized.

---

## 1. Read this first

Five things are true on arrival, and the first of them is the reason this handoff is
different from the last one.

1. **The two lines are reconciled** (D-035) and both are in the tree, in full, under
   non-colliding identifiers. §0 above is the explanation.
2. **The acquirer exists.** The EDGAR acquisition path was prose in
   `research/data_acquisition_plan.md`; it is **implemented and unit-tested** in
   `scripts/`, against synthetic fixtures, with **zero network calls** in the test
   suite. When the route is unblocked, the pipeline runs from committed code.
3. **The panel exists as a file.** `research/panel_v1.1.csv` — **431 rows** (8
   Stratum A + 423 Stratum B candidates over **141 jurisdictions**), derived **by
   rule** from a dated, hashed snapshot of the membership authority, with every
   Stratum B row `pending` because three of the five rule conditions cannot be
   verified until the data route lands.
4. **The promotable test is registered and has been amended three times.** v1.2
   (`hypothesis_v1.2.md`, `specification_v1.2.md`, `preregistration_v1.2.md`) registers
   the prospective holdout arm **PH-1** on the IFRS 18 first-application window,
   **before the first IFRS 18 report can be published**. v1.3 settles the Saudi
   T-PRE question and corrects the cluster arithmetic. **v1.4** restates the cluster
   expectation against the timing-cohort definition. **The hypothesis itself is not
   amended: `research/hypothesis_v1.3.md` remains in force.**
5. **All three named verification gaps are closed or determined** (D-021, D-022,
   D-023), and two further design questions have since been closed by dated decision
   (D-028, D-029).

**The correction that still matters.** The **ASU 2016-01 event (EV-103) moves one
year earlier**: the event calendar carried a public-business-entity effective date of
2018-12-15, while the ASU's own text says **2017-12-15** (and 2018-12-15 for all other
entities). The 2018-12-15 date belongs to **ASU 2016-02** (EV-102) — the two rows had
been conflated. `first_affected_fiscal_year_start` moves from 2019-01-01 to
**2018-01-01** (D-016); the row's own `notes` and `date_conflict` fields record the
change. **No outcome-period return has ever been computed or inspected, so nothing
downstream is affected.**

The v1.0 and v1.1 files are **byte-identical and unedited**; verify with
`git diff -- research/hypothesis.md research/specification_v1.md research/preregistration.md
research/hypothesis_v1.1.md research/specification_v1.1.md research/preregistration_v1.1.md`
(expect empty output).

| Artefact | What it is |
|---|---|
| `research/specification_v1.4.md`, `research/preregistration_v1.4.md` | **v1.4, registered.** The timing-cohort gate restatement. The hypothesis is not amended. |
| `research/hypothesis_v1.3.md`, `research/specification_v1.3.md`, `research/preregistration_v1.3.md` | v1.3: the Saudi T-PRE admission rule and the first cluster-count correction. |
| `scripts/sec_acceptance.py` | The SGML acceptance-time parser: `ACCEPTANCE-DATETIME` (`YYYYMMDDHHMMSS`, Eastern) → UTC, with the two daylight-saving transition days handled explicitly. |
| `scripts/data_cache.py` | The cache layout of the acquisition plan §3, plus the guard that refuses a cache root inside the repository (D-015). |
| `scripts/data_manifest.py` | The append-only JSONL manifest, SHA-256 over the raw bytes, and failed retrievals recorded as failed retrievals. |
| `scripts/sec_edgar.py` | The acquirer: submissions JSON, filing index, complete submission text; declared User-Agent; ≤ 2 requests/second; `Retry-After` honoured. |
| `scripts/build_panel.py` | The PH-1 panel builder; reads the candidate universe back out of `panel_v1.1.csv` so both panel files share one vintage; no network access; deterministic. |
| `research/panel_v1.1.csv` | The registered retrospective panel, materialised: **431 rows** (8 Stratum A + 423 Stratum B). |
| `research/panel_v1.2.csv` | **The PH-1 panel, materialised**: **141 rows**, one per (IFRS 18, jurisdiction); **10** carry a primary-verified day-level T-A in **10 distinct timing cohorts**, **131** carry none, and **every** row is `pending`. |
| `research/manifests/ifrs_jurisdiction_profiles.jsonl` | The dated snapshot manifest: **171** records with URL, HTTP status, bytes, **SHA-256** and retrieval timestamp. |
| `research/manifests/source_ledger_verification.jsonl` | Hashed retrievals for the ledger-verification and condition-2 sources, including the recorded failed retrievals. |
| `research/event_calendar.csv` | EV-103 primary-verified and **corrected**; EV-201 primary-verified; **EV-202 added**. |
| `research/decision_log.md` | **D-001 … D-037.** |
| `research/prompt_changelog.md` | Iterations 1–16 (note: the upstream's D-032 entry is filed under a **second** "Iteration 7" heading, so the numbering is **not unique** — recorded in Iteration 16, not corrected). |
| `research/source_ledger.csv` | **99 sources** (S-01 … S-99). |
| `research/experiment_ledger.csv` | **28 rows** (E-000 … E-027). |

## 2. What is verified (with sources)

- **The canonical dossier was re-retrieved read-only** at commit
  `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` and re-read in full: V-009 with the
  binding amendments **Cycle-52, Cycle-56, Cycle-58, the Cycle-111 correction notice,
  Cycle-113, Cycle-114, Cycle-123 and Cycle-126**. It was **not modified**.
- **The v1.1 design is compliant with every binding amendment.** The compliance map is
  `research/specification_v1.1.md` §3.7 and `research/hypothesis_v1.1.md` §8:
  - no **group A / group B** first-time-vs-second-time partition is built and none is
    presented as pre-registered (Cycle-56 item 1; Cycle-111 correction notice);
  - the **UK early-adopter cohort is excluded from treatment** as an identification
    (Cycle-56 item 3);
  - **no published firm-level repeat-adopter flag is assumed to exist**; any such
    indicator must be constructed from the firm's own basis-of-preparation note
    (Cycle-110 / R-058);
  - the state is **firm-level** and identified **within jurisdiction** (Cycle-52 item 1);
  - **enforcement quality and linguistic distance are mandatory controls**, not claimable
    conditioners, and the withdrawn ablation (d) stays withdrawn (Cycle-52 item 2;
    Cycle-113 item 1);
  - the claim is **pre-registered as a transition-window effect**, and steady-state
    comparability is a **descriptive control** only (Cycle-52 item 3; Cycle-58 item 2);
  - the **pre-emption arm is registered as a kill signal, not a null** (Cycle-113 items 2
    and 4; Cycle-114 item 2).
- **v1.2 is compliant too, and its narrowings are recorded as narrowings** (D-019):
  the **IFRS 18 adopter-type contrast is settled in advance, in the negative** (S-54);
  the **pre-emption arm becomes the real thing** for PH-1, because IFRS 18 carries a
  **mandated** IAS 8.30/.31 pre-adoption impact disclosure (S-49); the **expected
  cluster count is stated in advance and is below the minimum**, with the consequence
  fixed as **inconclusive by construction**, and inference fixed in advance to the
  jurisdiction-level randomisation test and the wild-cluster bootstrap; and the
  **once-only reporting rule** is fixed: a peek voids the arm, and a voided arm is
  reported as void, never as a null.
- **v1.3 and v1.4 are compliance-preserving amendments** (D-029, D-034). The **Saudi
  T-PRE question is settled by admission with a uniform interval rule**; the **cluster
  expectation is restated** because a stale expectation in a registered document is a
  defect; and the **profile route is demoted to a triage prior** so that it can never
  exclude a jurisdiction. No threshold, acceptance criterion, test order or split was
  moved, and the hypothesis was not amended.
- **The tests pass**: `python3 -m pytest -q tests/` → **173 passed, 0 failing**
  (re-run this session, same command as the workflow).
- **Condition 2 of the PH-1 membership rule is verified for ten jurisdictions**, each
  from a standard-setter or regulator document read directly and hashed
  (D-022, D-026, D-030, **D-033**):

  | Jurisdiction | T-A | Primary source |
  |---|---|---|
  | Philippines | 2024-05-10 | the FSRSC's own standards register (S-94) |
  | New Zealand | 2024-05-23 | the XRB's own NZ IFRS 18 instrument page (S-72) |
  | Malaysia | 2024-06-14 | the MASB's statutory notice of issuance (S-91), corroborated by the MASB standards list (S-98) |
  | Hong Kong SAR | 2024-07-09 | the HKICPA FRSC's own minutes, with the issuance post-meeting note (S-92) — **closes the D-026 gap** |
  | Singapore | 2024-10-04 | the ACRA announcement (S-76) |
  | Saudi Arabia | 2024-12-26 | the SOCPA endorsement document (S-61); the CMA early-adoption decision recorded separately (S-62) |
  | Indonesia | 2025-05-28 | the DSAK IAI's own bulletin, in the original language (S-93) |
  | United Kingdom | 2025-12-10 | the UKEB's news release recording the formal adoption (S-63) |
  | Brazil | 2025-12-23 | Resolução CVM nº 237 (S-77) |
  | European Union | 2026-02-13 | Commission Regulation (EU) 2026/338 (S-54), corroborated by the EFRAG Endorsement Status Report of 16 February 2026 (S-60) |

  **Ten instruments in ten distinct T-A dates spanning twenty-one months.** The
  remaining jurisdictions keep an **empty** T_A; no date is ever inferred from a
  secondary summary (D-011).
- **The date gaps are closed from primary sources** (D-016):
  - **EV-201 (IFRS 15, UK)** — the UK legal instrument is **The Companies,
    Partnerships and Groups (Accounts and Reports) Regulations 2015 (SI 2015/980)**,
    made **26 March 2015**, in force **6 April 2015**. Regulation 2(2) gives the
    mandatory date (financial years beginning on or after **1 January 2016**) and the
    directors' early-application arm (from **1 January 2015**). Fetched from
    legislation.gov.uk in session (S-55).
  - **EV-202 (IFRS 16, UK)** — the UK required **no new** adoption instrument; the
    standing SI 2015/980 requirement applies, and IFRS 16 became EU-adopted on
    2017-10-31, so the first affected UK financial years begin on or after
    **1 January 2019**. The T-A is therefore **inherited from the EU**, and the row says
    so — it is a weaker anchor than EV-201's.
  - **EV-103 (ASU 2016-01)** — issuance **2016-01-05**, effective-date paragraph
    quoted verbatim, and the date **corrected** (D-016). Read through the search
    provider's rendering because a direct fetch of fasb.org returns HTTP 403 in this
    environment; corroborated independently by the FASB's own ASU 2018-03 (S-57).
- **The panel is materialised and its membership is auditable** (D-018). A dated,
  hashed snapshot of the **170** IFRS Foundation jurisdiction profiles was taken on
  2026-10-22; the profile screen classifies **138** jurisdictions as IFRS-required for
  listed domestic public companies, **28** as not, and leaves **4 unresolved** (Bhutan,
  China, the European Union, Morocco). Every retained row carries the profile URL, the
  **SHA-256** of the page as retrieved, the retrieval timestamp, the profile's own
  "last updated" date and the raw status text. **Those are profile-screen counts, not
  panel-row counts** (D-037).
- **The UK filing-timestamp question is settled — and the answer narrows the design**
  (D-021, D-027). The FCA NSM's published glossary defines "Publication date" as "The
  date a document/announcement was released via a Regulatory Information Service
  (RIS) or uploaded to the NSM", and the Investor User Guide defines "Filing date" as
  "The date at which the information was made available for filing on the NSM" —
  **dates, with no published time-of-day field**. A time *does* exist in the plumbing:
  the PIP-to-NSM submission schema carries a mandatory `PublishingDate` element
  (`YYYY-MM-DDTHH:MM:SSZ`), and the NSM records a date/time on submission — but that
  schema binds PIPs only **from 3 November 2025** (PS24/19). **Consequence, stated now
  rather than discovered later: the two retrospective UK events cannot be timed at
  all**, because their transition windows (2016-01-01, 2019-01-01) precede the
  timestamp regime, whatever the answer to the remaining verification. The UK stays
  viable for **PH-1**, whose window falls entirely after it. The NSM search API
  answered **HTTP 403** from this environment, so condition (j) is recorded
  **unverified, not false**, and the failed retrieval is recorded as a failed
  retrieval.
- **The linguistic-distance measure cannot be reproduced exactly panel-wide**
  (D-023). S-44 operationalises it as the **Joshi and Lahiri (2015) friction index
  over 192 WALS features** — 0 where a language shares an English feature, 1 where it
  does not, averaged, with simple averaging across multiple official languages — and
  publishes values for its 84-country 2004–2018 sample (Japanese 0.590, Bengali 0.583,
  Korean 0.507, Arabic 0.490, Chinese 0.467). Three obstacles block exact panel-wide
  reproduction: **Ethnologue is licensed and versioned**, the Ethnologue-to-WALS merge
  was **manual**, and Table 1 does not cover the campaign's jurisdictions. The
  registered condition is therefore **met**, so the **registered fallback ordinal scale
  is selected by the rule**, with the published values kept as an **external validation
  of the ordering**. The fallback's **categories and boundaries were enumerated by
  dated decision (D-028)** and the concordance with the published measure was measured.
- **No outcome-period return has been computed or inspected.** No filing-archive
  harvest, no paid data pull, no GitHub Actions run, no workflow edit, no upstream
  commit.

## 3. The design, in one paragraph

The **treatment** is a jurisdiction-level standard-application event: a firm is treated
from the jurisdiction's adoption announcement if it is in the affected-firm list
(knowable ex ante from the regulator's own scope rule) and applies the standard from
the effective date. The **state** is firm-level pre-adoption information quality
(absolute discretionary accruals, within-jurisdiction median split), estimated **within
jurisdiction**. The **counterfactual** is a matched **not-yet-treated** jurisdiction
group, matched on size, industry, liquidity, momentum, market-to-book, analyst coverage
and **fiscal-period-end proximity** so the control transition window has the same
length as the treated one. The **primary estimand** is the difference-in-differences of
the low-minus-high state contrast across the **transition window [T-A, T-R]**. The
**entry** is at the adoption announcement, the **exit** at the firm's own first full
report under the standard. Full detail: `research/specification_v1.1.md` §§1–7, with
the v1.3 and v1.4 amendments.

## 4. The registered panel — and the reconciled counts

`research/panel_v1.1.csv` has **431 rows** in the schema of
`research/specification_v1.1.md` §4.2, plus additive columns carrying the evidence for
each membership decision (`membership_screen`, `profile_url`, `profile_sha256`,
`profile_retrieved_utc`, `profile_last_updated`, `status_text`).

| Stratum | Rows | Status |
|---|---|---|
| **A — content change** (primary) | **8** (EV-001, EV-002, EV-003, EV-101, EV-102, EV-103, EV-201, EV-202) | **complete and primary-sourced**; `in_registered_panel = true` |
| **B — framework change** (secondary) | **423** candidate rows over **141 jurisdictions** (411 `listed-ifrs-required`, 12 `review-required`) | `in_registered_panel = **pending**` — three of the five rule conditions need the data route |
| **C — placebo** | built at run time from the same rule | n/a |
| **D — excluded** | UK IFRS 15 early adopters, excluded from treatment per Cycle-56 item 3 | n/a |

> **The counts in the prose were stale for three sessions and are now corrected**
> (D-037). The panel was materialised at 434 rows; at a later checkpoint **three**
> Stratum B rows were removed because they were **not jurisdictions at all** — they
> were the IFRS Foundation index page's **boilerplate disclaimer** scraped as a
> jurisdiction name, producing one spurious row each for IFRS 15, IFRS 16 and IFRS 9.
> That was a **data-quality correction, not a narrowing**, and it removed one spurious
> jurisdiction, which is why the jurisdiction count is **141**, not 142. The committed
> files have carried 431 / 423 / 141 ever since. **Parse the files; do not trust a
> quoted row count.**

**The EU is one timing cohort, not 27 clusters**, because all EU member states share one
application date. This is stated in advance so it cannot later be discovered as a power
surprise (`research/preregistration_v1.1.md` §5.2). **D-034 names the outstanding
carve-out check**: a member state with a permanent derogation from particular endorsed
standards (Poland's bank and insurer derogations from IFRS 9 and IFRS 15 are the known
case) is not simply in the cohort, so **condition 2 is not yet verified for the
member-state rows and their T_A is left empty** rather than inherited silently.

### The PH-1 panel — `research/panel_v1.2.csv`

**141 rows**, one per (IFRS 18, jurisdiction), in the same schema and with the same
three-state `in_registered_panel` discipline as the retrospective panel. It is built by
committed code (`scripts/build_panel.py`) from the **same dated, hashed membership
snapshot** as `panel_v1.1.csv`, so the two panel files share one vintage. The builder
is deterministic, takes no network access, and reproduces the committed file
**byte-identically**.

| | Rows | Status |
|---|---|---|
| **Condition 2 verified** (a legal instrument making IFRS 18 mandatory, with a day-level date) | **10** — ten distinct T-A dates from 2024-05-10 to 2026-02-13 (§2) | `in_registered_panel = pending` — conditions 3, 4 and 5 are still unverified |
| **Condition 2 unverified** | **131** | `in_registered_panel = pending`, and **`T_A` is left empty rather than inferred** |
| **Total** | **141** | **every row is `pending`** |

The panel carries two further **additive evidence columns**, `profile_route_hint` and
`timing_cohort`, read from the dated profile snapshot by a fixed deterministic rule in
`scripts/build_panel.py` (`classify_profile_route`): 27 `eu_member_state`, 3
`eea_efta_own_instrument`, 9 `national_equivalent_profile`, 98
`standing_reference_profile`, 4 `no_profile_status_text`. **The classification is not a
membership determination and the panel's own data contains the counterexamples that
prove it**: Brazil's profile says only *"Required."*, Saudi Arabia's records the IFRS
Accounting Standards, and South Korea's records *"adopted IFRS Accounting Standards"* —
yet all three carry or are about to carry dated national instruments. A
standing-reference profile therefore **never** excludes a jurisdiction, and the 98 rows
in that class stay in the panel as `pending` candidates. The columns are evidence
about a row, **not new conditions**; the five membership conditions are untouched.

**The IFRS 18 events are deliberately NOT in the retrospective event calendar.** Adding
2024–2026 rows to `research/event_calendar.csv` would destroy that file's defining
property — every registered retrospective event has T-A ≤ 2017-10-31, so the
chronological holdout split is empty (D-014) — and that property is what makes the
retrospective panel's evidential role checkable.

**Three consequences are frozen in advance and must not be worked around later:**

1. If the realised number of independent **timing cohorts** is **< 12** or the
   treatment-firm count is **< 200**, the primary estimand is **inconclusive by
   construction** — the decision is park, never "pass"
   (`research/preregistration_v1.4.md` §5.3; D-016, D-034).
2. **The retrospective panel's chronological holdout is EMPTY.** Every registered
   retrospective event has T-A ≤ 2017-10-31, so no event falls in the post-2019 split.
   This is declared in advance together with its consequence: **the retrospective panel
   cannot satisfy protocol promotion gate 4 on its own**; its role is **evidential**.
   The promotable test is the prospective holdout arm **PH-1**, registered as v1.2 and
   amended by v1.3 and v1.4.
3. **The gate quantity is the number of distinct T-A dates, not the number of
   jurisdictions** (D-034). The **plausible maximum** is bounded by the number of
   jurisdictions that issue their own dated instrument — roughly a dozen — so the
   realistic range is **≈ 10–13** against the **unchanged ≥ 12** minimum. The arm is
   **no longer certainly inconclusive, and not yet shown to be feasible either.**

## 5. What is blocked, and what unblocks it

**The A1–A5 authorisation request is superseded** by D-032's free-only route; the
historical text is in `research/data_acquisition_plan.md` §8.1 and
`research/authorisation_request.md`, but **no answer is needed to make progress**.
What is needed is the **work itself**:

| # | Blocker | What unblocks it | Consequence if it stays open |
|---|---|---|---|
| **B1** | **A lawful, free source inventory.** Each candidate source needs its terms, rate limits, attribution requirements and coverage checked **before** use. | A dated, hashed inventory in `research/source_ledger.csv` + `research/manifests/`. | Nothing can be acquired at all. |
| **B2** | **Free price coverage for delisted securities and terminal returns.** No free candidate is presumed to have it. | Empirical evidence per candidate, recorded as coverage and missingness. | The survivorship-filtered price panel fires **kill condition 9** by construction, with a bias *against* the hypothesis (the low-information-quality arm is disproportionately dropped). |
| **B3** | **A network-capable execution environment.** Two sample requests failed **before HTTP** on local DNS. | A runner that resolves the hosts; the failure must be recorded as an environment limitation, not as a source's refusal. | The feasibility audit cannot be run at all. |
| **B4** | **Conditions 3, 4 and 5 of the membership rule**, none of which is yet verified for any jurisdiction. | The data route. | Every row stays `pending` and the arm cannot start, whatever the cohort count. |

**The A4 object.** The **423** pending Stratum B rows in `research/panel_v1.1.csv` are
what the membership rule converts to true or false, one by one, as the route lands.

## 6. Named verification gaps — and what replaced them

**All three gaps named in the session-5 handoff are closed or determined** (D-021,
D-022, D-023), and two more were closed afterwards (D-028, D-029). **Three items
replace them, and all three must be settled by dated decision *before the holdout
opens* — none of them may be settled by looking at an outcome:**

1. **The EU member-state carve-out check.** The profile text for the 27 member states
   is **identical** to the EEA/EFTA states', so the two groups are told apart by name
   in the code. The member states apply the EU-endorsed standard through Commission
   Regulation (EU) 2026/338 and would join the **2026-02-13** cohort — but a member
   state with a permanent derogation is not simply in the cohort. **Whether any member
   state holds such a derogation is named, queued and outstanding** (D-034). This is
   the **single highest-value open item**: it can move the cohort count by up to 27.
2. **Condition 2 for the remaining local-equivalent jurisdictions** — South Korea,
   Pakistan, Sri Lanka, Myanmar, Nepal, Chinese Taipei, Mongolia, Bhutan, Israel.
   Each needs its **own** regulator's dated instrument, read directly and hashed.
   **A jurisdiction whose instrument cannot be located keeps an empty T_A; it is never
   given an inferred date** (D-011). Pakistan failed with HTTP 403 on every path tried
   (S-99) and the route is queued for another attempt.
3. **The single remaining UK verification.** Whether the NSM search response or the CSV
   export carries a time-of-day component decides whether the UK satisfies panel
   condition (j) **for events whose filings fall after 3 November 2025** — which
   includes PH-1 and excludes the retrospective UK events whatever the answer. One
   NSM search for a known annual financial report, then inspect the export header.
   (D-021, D-027)

**And one question that is not a gap but a standing fact:** the retrospective UK events
**cannot** be timed. That is a determination, not an open item, and it should be read
as a feature of the design rather than an obstacle to it.

## 7. Integrity rules that carry forward

- **No outcome-period return is computed before the feasibility audit's counts are
  published.** The audit reports cohorts, treatment firms and coverage; below the
  pre-registered minimums the run **stops**.
- **The panel, the window, the thresholds, the exit rules and the acceptance criteria
  are frozen.** A change means a **new registered version** in
  `research/prompt_changelog.md`, never an edit in place.
- **v1.0, v1.1, v1.2, v1.3 and v1.4 are all immutable once registered.** Edit none.
  **The hypothesis in force is `research/hypothesis_v1.3.md`** — v1.4 is a
  specification and pre-registration amendment only.
- **A failed retrieval is recorded as a failed retrieval**, never as an absence.
- **The date that maximises a return is never selected**; date conflicts are recorded,
  not resolved (D-011).
- **A null in this design is a contribution, not a replication** — the
  first-time-versus-second-time-adopter comparison *on drift* is unrun by the field
  (S-37 / V-009 G-21). The comparator's own power and the reason it was not run must
  be reported with any result.
- **No paid data pull and no GitHub Actions run** (protocol Authority item 4; D-032
  additionally prohibits every paid service). `.github/workflows/main.yml` remains
  unmodified (D-006).
- **Raw data is cached outside the repository**; only code, manifests, hashes and
  non-licensed aggregates are committed (D-015).
- **A date correction is a decision, not an edit.** When a primary source contradicts a
  recorded date, the row is corrected, the conflict is written into the row's own
  fields, and a decision is logged (D-016 is the precedent).
- **A count correction is a decision, not an edit** (D-037). Parse the files; do not
  carry a quoted row count forward.
- **An identifier collision between two lines is resolved by renumbering the
  un-published line, never by overwriting the published one** (D-035).
- **Free-source insufficiency must be reported honestly.** It does not justify
  lowering the frozen gates or asserting completeness that has not been shown.

## 8. Protocol compliance this session

- The canonical protocol is **unchanged** by this session. Where the protocol and the
  dossier differ in emphasis, the dossier governs the *design* and the protocol governs
  the *process*.
- Phase 2 (freeze) is complete and now carries **four registered amendments** (v1.2 →
  v1.4); Phase 3 (data) has its **plan complete**, its **acquirer implemented and
  tested**, its **date gaps closed** and its **panel materialised**, and its
  **execution blocked on the free-source route's own precondition**; Phases 4–7 remain
  pending and cannot start without data.
- `research/results.md` still reports **no results**, and the **173** automated tests
  pass.
- **What this session did, and why it is recorded as decisions.** The session performed
  a **repository reconciliation**, not new research: it fetched the remote, identified
  the content conflict that had broken the previous session's persistence, resolved it
  by hand with an identifier renumbering (D-035), repaired one pre-existing upstream
  test defect (D-036), reconciled the panel counts against the committed files
  (D-037), and updated the handoff, the campaign state and the changelog. **No new
  primary source was read, no filing archive was harvested, no paid provider was
  contacted, no outcome-period return was computed or inspected, and no GitHub Actions
  workflow was run.** The session-96 research content (D-033, D-034 and sources
  S-91 … S-99) was **carried forward in full**, not re-derived.
- **Nothing was reset or discarded.** The original local commit is preserved at
  `backup/session-96-local-ahead` / `backup/session-96-local-ahead-9093ba4`; the
  pre-reconciliation recovery bundle verifies.

---

## 9. Initial task message for the next agent

> You are the next agent in the ACCTCLOCK research loop. **Read this handoff first** —
> §0 explains what happened to the previous session and why the history looks unusual,
> and you will lose time if you skip it.
>
> Read, in order: `research/HANDOFF.md` (this file), `research/campaign_state.json`,
> `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` (the protocol),
> then `research/hypothesis_v1.3.md` (**the hypothesis in force**),
> `research/specification_v1.4.md`, `research/preregistration_v1.4.md` (the registered
> PH-1 arm), `research/specification_v1.1.md` (the design, §§1–7),
> `research/data_acquisition_plan.md`, `research/data_route_assessment.md`,
> `research/decision_log.md` (D-001 … D-037), `research/prompt_changelog.md`
> (Iterations 15–16 are the most recent), `research/event_calendar.csv`,
> `research/experiment_ledger.csv`, `research/source_ledger.csv`,
> `research/authorisation_request.md`, and `research/results.md`.
> There is no `AGENTS.md` in this repository; the protocol file is the governing
> document.
>
> **State on arrival.** The campaign is **PARKED — not validated, not rejected**. The
> design blocker is cleared; the promotable test is registered as **v1.2** and amended
> by **v1.3** and **v1.4**; the v1.0 and v1.1 files are byte-identical and unedited;
> the canonical dossier was retrieved read-only at commit
> `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` and was **not modified**; the source
> ledger holds **99** sources (S-01 … S-99); the decision log holds **D-001 … D-037**;
> the experiment ledger holds **28** rows (E-000 … E-027); `research/panel_v1.1.csv`
> holds **431** rows and `research/panel_v1.2.csv` holds **141** rows, of which
> **10** carry a primary-verified day-level T-A in **10 distinct timing cohorts**; the
> test suite is **173 passing, 0 failing**; and **no outcome-period return has ever
> been computed or inspected**. The next step in `research/campaign_state.json` is
> `phase3b-data-execution-and-feasibility-audit`, **pending**, with
> `current_instruction` = **D-032 (free-only route)**.
>
> **FIRST — check whether the remote has moved.** Two runners can push here.
> Run `git fetch origin main` and `git log --oneline origin/main -5` **before** you
> commit anything. If the remote has advanced and your work appends to
> `research/decision_log.md`, `research/experiment_ledger.csv` or
> `research/source_ledger.csv`, the rebase **will** conflict — that is exactly what
> ended the previous session. Resolve it the way D-035 did: **the published
> identifiers keep their numbers, yours take the next free numbers**, and record the
> mapping as a dated decision.
>
> **Your job, in priority order.**
>
> **P0 — DONE (session 100).** The free-source inventory is complete:
> `research/free_source_inventory/` holds the dated, terms-checked candidate
> inventory (inventory.csv/md, feasibility_notes.md), recorded as E-028. The
> delisted/terminal-return coverage of every candidate remains unverified — that
> is the P3 audit's job, not P0's. **Do not re-do P0.**
>
> **P1 — DONE (session 102).** The EU member-state carve-out check is closed by D-038: no member state holds a permanent derogation from an individual endorsed standard; the only discretion is the Article 5 option over which entities. All 27 member states join the 2026-02-13 cohort. Sources S-100…S-104 fetched and recorded. **Do not re-do P1.**
> Determine whether any of the **27 EU member states** holds a **permanent derogation**
> from particular endorsed standards — Poland's bank and insurer derogations from
> IFRS 9 and IFRS 15 are the known case. This decides whether the member-state rows
> can join the **2026-02-13** cohort, and it can move the cohort count by up to 27,
> which is decisive against the **≥ 12** minimum. Read the **EU's own** legal
> instruments and each member state's derogation, from primary sources, hash them, and
> record the outcome. **A member state that cannot be cleared keeps an empty T_A.**
> (D-034)
>
> **P2 — COMPLETE (session 106).** Re-verified network reachability (DNS resolves) and re-checked the pending sources: Pakistan SECP still HTTP 403 on every path (S-99); Sri Lanka has no day-level gazette date; Israel applies IFRS 18 automatically as issued by the IASB (no national instrument, no day-level T-A); Myanmar, Nepal, Chinese Taipei, Mongolia, Bhutan remain without a located day-level regulator instrument. Per D-011 each keeps an empty T_A. Panel stands at **10 verified T-A in 10 distinct timing cohorts**; `research/panel_v1.2.csv` reproduces byte-identically from `scripts/build_panel.py`. **Do not re-do P2.**
>
> **P3 — Run the pre-outcome feasibility audit and publish its counts.** Publish
> coverage, the independent **timing-cohort** count, treatment and control counts, data
> quality and the terminal/delisting-return rule **before** any outcome-period return
> is computed. If there are **fewer than 12 independent timing cohorts** or **fewer
> than 200 treatment firms**, **stop** and report the estimand as **inconclusive by
> construction** — never "pass", never a null. **Do not narrow the panel after the
> audit begins** (D-016). The acquirer is already implemented and tested, so the first
> act on the filing leg is to set `ACCTCLOCK_USER_AGENT`, run **one** filing
> end-to-end, and verify the parsed acceptance timestamp against the filing index
> **by hand** before any bulk run.
>
> **P4 — Optional, and only if it touches no frozen artefact:** tighten the acquirer.
> It is written to be extended, not finished. Two specific gaps worth closing when
> convenient: an **availability-lag measurement** (the acquisition plan §5 rule 5 asks
> for the delay between a filing's acceptance and its first appearance on the source's
> public interface, and it is not yet instrumented), and a **re-fetch verifier** that
> re-reads a random sample of cached artefacts and re-hashes them against the
> manifest. Both are additive; neither may change a registered date.
>
> **P5 — Housekeeping that is now owed.** The upstream's D-032 entry sits in
> `research/prompt_changelog.md` under a **second** "Iteration 7" heading, so the
> iteration numbering in that file is **not unique**. It is recorded in Iteration 16
> and deliberately **not** renumbered, because renumbering a published entry breaks
> citations of it. **Leave it alone unless the maintainer rules otherwise.**
>
> **Rules that are not negotiable.**
> - **No outcome-period return before the feasibility audit's counts are published.**
> - **Do not edit v1.0, v1.1, v1.2, v1.3 or v1.4 in place.** A design change is a new
>   registered version in `research/prompt_changelog.md`.
> - **Do not narrow the panel after the feasibility audit begins** (D-016).
> - **No paid services of any kind, and no GitHub Actions run** (D-032; protocol
>   Authority item 4). `.github/workflows/main.yml` stays unmodified.
> - **Do not modify the upstream dossier repository.** It is read-only.
> - **Cache raw data outside the repository**; commit only code, manifests, hashes and
>   non-licensed aggregates.
> - **Record every failed retrieval as a failed retrieval**, and every date conflict as
>   an open conflict. **A date correction is a decision, not a silent edit**; so is a
>   count correction (D-037) and so is an identifier renumbering (D-035).
> - **Parse the committed files for their counts; never carry a quoted row count
>   forward.**
> - Run `python3 -m pytest -q tests/` and report the count (**173** at handover).
> - Keep `research/results.md` reporting **no results** until a test has actually been
>   run. A blocked campaign is not a result, and a null is a result only when it comes
>   from a test that ran.
>
> **Finish by** updating `research/HANDOFF.md`, `research/campaign_state.json`,
> `research/experiment_ledger.csv` and `research/prompt_changelog.md`, and by leaving a
> **clear initial task message for the next agent** in the handoff.

---

## 10. Change log for this handoff

| Date | Session | Change |
|---|---|---|
| 2026-10-22 | **107** | **Verification pass.** `git fetch origin main` advanced the tip to `d9e77aa` (kilo checkpoint commits); `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. No new primary source read, no filing archive harvested, no outcome-period return computed or inspected. Campaign remains **PARKED — not validated, not rejected**; next step still `phase3b-data-execution-and-feasibility-audit`; next agent starts at **P3 (pre-outcome feasibility audit)**. §9 initial task message carried forward. | DNS resolves; re-checked pending sources (Pakistan SECP HTTP 403, S-99; Sri Lanka no day-level gazette; Israel automatic incorporation; Myanmar, Nepal, Chinese Taipei, Mongolia, Bhutan no instrument). Per D-011 each keeps an empty T_A. Panel stands at 10 verified T-A in 10 distinct timing cohorts; builder reproduces byte-identically. Tests 173 passing. No new primary source read, no filing archive harvested, no outcome-period return computed. Campaign remains **PARKED — not validated, not rejected**; next step `phase3b-data-execution-and-feasibility-audit`. §9 initial task message updated: P2 marked done, next agent starts at **P3 (pre-outcome feasibility audit)**. |
| 2026-10-22 | **101** | **P0 complete; handoff advanced.** Verified committed state: `git fetch origin main` shows `origin/main` at `6d44b3b` (checkpoint), no advance; `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. P0 (free-source inventory) is complete and recorded as E-028 (`research/free_source_inventory/`: inventory.csv/md, feasibility_notes.md). Blocker **B3 (network/DNS)** remains open: P1–P3 cannot be executed until the environment resolves the hosts. No new primary source read, no filing archive harvested, no paid provider contacted, no outcome-period return computed or inspected, no workflow run. §9 initial task message advanced: P0 marked done, next agent starts at **P1 (EU member-state carve-out check)**. Campaign remains **PARKED — not validated, not rejected**. |
| 2026-10-22 | **104** | **Verification pass; network now resolves.** Verified committed state: `git fetch origin main` succeeds (local at `69989f8`), `git status` clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. DNS resolution now succeeds in this runner (B3 lifted here), so the remaining P2 jurisdictions are reachable for primary-source verification. P0 (E-028) and P1 (D-038) remain complete; P2 remains open for Pakistan (SECP, S-99, HTTP 403 on every path tried), Sri Lanka, Myanmar, Nepal, Chinese Taipei, Mongolia, Bhutan, Israel — each needs its own regulator's dated instrument at day granularity, with an empty T_A if unverifiable (D-011). No new primary source read, no filing archive harvested, no outcome-period return computed or inspected. Campaign remains **PARKED — not validated, not rejected**; next step still `phase3b-data-execution-and-feasibility-audit`. §9 initial task message carried forward; next agent starts at P2 (remaining local-equivalent jurisdictions) with network available. |
| 2026-10-22 | **103** | **P2 advanced; SECP still 403; network resolves.** Verified committed state: `git fetch origin main` succeeds, local at `063deb1`, clean. DNS resolves; `python3 -m pytest -q tests/` → **173 passed, 0 failing** (numpy installed in this environment). P0 (E-028), P1 (D-038) complete; South Korea verified (S-73, day-level unverified, T-A empty). Pakistan SECP route still returns HTTP 403 on every path (S-99). P2 (condition 2 for Sri Lanka, Myanmar, Nepal, Chinese Taipei, Mongolia, Bhutan, Israel) remains open; each needs its own regulator's dated instrument at day granularity, with empty T_A if unverifiable (D-011). Campaign remains **PARKED — not validated, not rejected**. No outcome-period return computed or inspected. |
| 2026-10-22 | 5 | **Acquirer built and tested** (`scripts/sec_edgar.py`, `scripts/sec_acceptance.py`, `scripts/data_manifest.py`, `scripts/data_cache.py`; 48 new tests, 115 total, zero network calls). **Both named date gaps closed** and **EV-202 added**; **EV-103's effective date corrected** — the ASU 2016-01 event moves **one year earlier** (D-016). **Panel materialised** as `research/panel_v1.1.csv` from a dated, hashed IFRS Foundation profile snapshot, manifest committed (D-018, D-020). **v1.2 registered for PH-1** (D-019). Authorisation request rewritten as a one-click-able file. Decisions D-017…D-020; changelog Iteration 9; ledger rows E-015…E-019. |
| 2026-10-22 | 5g | **Read prior handoff, verified durable state.** Campaign remains **PARKED — not validated, not rejected**; phase3b pending and blocked on authorisation A1–A5. No new primary sources, no new decisions, no new ledger rows, no artefact edits beyond this handoff. Section 9 initial task message carried forward. |
| 2026-10-22 | 5d | **Read prior handoff.** Campaign remains **PARKED — not validated, not rejected**; phase3b pending and blocked on authorisation A1–A5. D-029 records Saudi T-PRE admission with uniform interval rule registered as v1.3. |
| 2026-10-22 | 5c | **Verification pass only.** Re-read the durable handoff and campaign state; ran `python3 -m pytest -q tests/` → **144 passed**. All three named gaps closed or determined (D-021, D-022, D-023). `research/panel_v1.2.csv` written by committed code from the same membership vintage. Source ledger **S-60…S-71**; ledger rows **E-020, E-021**; changelog Iteration 10. |
| 2026-10-22 | 5e | Condition 2 verified for a sixth jurisdiction (New Zealand, S-72); South Korea recorded as attempted and not verified (S-73). Decision D-030; ledger row E-022; changelog Iteration 12; tests 145 passing. |
| 2026-10-22 | 5f–5j | **Upstream line:** D-031 (paid-provider route; `scripts/price_provider_client.py`, `tests/test_price_provider_client.py`, `research/paid_data_route_execution.md`), adapter hardening (Iteration 14, E-024), two DNS-blocked smoke attempts recorded as failed retrievals (E-025), then **D-032 supersedes D-031: free and lawful public sources only.** |
| 2026-10-22 | 4 | **v1.1 registered** (hypothesis, specification, preregistration); `research/data_acquisition_plan.md` written; source ledger extended to 54 entries; decisions D-012…D-016; changelog Iteration 8; ledger row E-014. The design blocker is cleared; the data/authorisation blocker is open. |
| 2026-10-22 | 3 | Canonical dossier retrieved read-only; binding constraints recorded (D-008); event calendar built; data route assessed (D-010). |
| 2026-10-22 | 2 | Literature audit; v1.0 hypothesis, specification and preregistration frozen. |

---

## 11. Current runbook and next action (D-032, free-only)

1. Read this handoff §0, then D-032 in `research/decision_log.md`, then
   `research/campaign_state.json` → `current_instruction`. The old A1–A5 references
   are **historical** and are **not** a reason to wait for another user answer.
2. `git fetch origin main` and check whether the remote has moved **before** you
   commit. If it has, reconcile as D-035 describes.
3. Run `python3 -m pytest -q tests/` from the normal environment and report the
   observed count (**173** at handover).
4. Do **P0**: the dated, hashed, terms-checked inventory of lawful free sources.
5. Do **P1**: the EU member-state carve-out check — the highest-value open item.
6. Continue read-only legal-source and standard-setter acquisition in a
   **network-enabled environment**, respecting rate limits and keeping raw files
   outside the repo. Do not repeatedly retry external hosts inside a DNS-blocked
   terminal.
7. Publish the pre-outcome coverage and feasibility counts. **Stop** if the frozen
   ≥ 12 independent timing cohorts or ≥ 200 treatment firms gates fail, or if valid
   terminal returns cannot be established. **Do not compute or inspect returns before
   the feasibility report, and do not open PH-1 unless all gates pass.**
8. **No GitHub Actions, deployment, brokerage, trading or paid-service action** under
   D-032.

**Session 508 note (this session).** Session 508 read the prior agent task from the durable handoff (§9, Session 507) and completed it. `git fetch origin main` shows `origin/main` at **`9f0d1d0`** (remote == HEAD == local HEAD `9f0d1d0`); `git status` clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**267** notes on arrival, **268** after prepend, **9** steps; `updated_at` refreshed to now, `last_verified_head` set to `9f0d1d0`). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** non-empty `T_A` in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all 141 rows `pending`, regenerated **byte-identically** from `scripts/build_panel.py`. Gate evidence re-audited: `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; jurisdiction-level instrument verification on 12 rows does **not** admit firms (129 rows affected-firm list not yet determined) → admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. `research/results.md` reports no results. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 rewritten with initial task message for the next agent (Session 509).


**Session 507 note (this session).** Session 507 read the prior agent task from the durable handoff (§9, Session 506) and completed it. `git fetch origin main` shows `origin/main` at **`522ed51`** (remote == HEAD == local HEAD `522ed51`); `git status` clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.42s). `research/campaign_state.json` parses with `json.load` (**265** notes on arrival, **266** after this prepend, **9** steps; `updated_at` refreshed to `2026-10-27T11:16:00Z`, `last_verified_head` set to `522ed51`). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** non-empty `T_A` in **12** distinct timing cohorts (2024-05-10, 2024-05-23, 2024-06-14, 2024-07-09, 2024-10-04, 2024-12-26, 2025-05-28, 2025-12-10, 2025-12-18, 2025-12-23, 2026-02-13, 2026-09-09), all 141 rows `pending`, regenerated **byte-identically** from `scripts/build_panel.py` (rebuilt in place with `python3 scripts/build_panel.py`; `cmp` clean for both v1.1 and v1.2; working tree restored). Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` parsed separately). Decision log D-001 … D-080; experiment ledger **120** data rows. Gate evidence re-audited from the committed panel file: `filing_route` and `price_venue_set` PENDING for all 141 PH-1 rows; of the 141 PH-1 rows, **129** carry `affected_firm_scope_rule` = "IFRS 18 affected-firm list NOT yet determined for this jurisdiction…" and the remaining **12** carry "IFRS 18 instrument verified; affected class per the instrument…" — jurisdiction-level instrument verification only, does **not** admit firms, so admitted treatment-firm count is **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two of the three gates fail, the primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message rewritten for the next agent (Session 508).


**Session 506 note (this session).** Session 506 read the prior agent task from the durable handoff (§9, Session 505) and completed it. `git fetch origin main` shows `origin/main` at **`7cae7b5`** (remote == HEAD == local HEAD `7cae7b5`); `git status` clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.43s). `research/campaign_state.json` parses with `json.load` (**265** notes on arrival, **266** after this prepend, **9** steps; `updated_at` refreshed to `2026-10-27T10:27:26Z`, `last_verified_head` set to `7cae7b5`). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** non-empty `T_A` in **12** distinct timing cohorts (2024-05-10, 2024-05-23, 2024-06-14, 2024-07-09, 2024-10-04, 2024-12-26, 2025-05-28, 2025-12-10, 2025-12-18, 2025-12-23, 2026-02-13, 2026-09-09), all 141 rows `pending` (`status` column absent from v1.2 — `status_text` is the profile text, `timing_cohort` is the gate column), regenerated **byte-identically** from `scripts/build_panel.py` (rebuilt in place with `python3 scripts/build_panel.py`; `cmp` clean for both v1.1 and v1.2; working tree restored). Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — 10 records parsed separately, not appended). Decision log D-001 … D-080 (**80** distinct D-numbers via `grep -oE 'D-[0-9]{3}' | sort -u`); experiment ledger **119** data rows. Gate evidence re-audited from the committed panel file: `filing_route` = "PENDING A2 verification of a filing route that pub…" for **all 141 rows**; `price_venue_set` = "PENDING A1 (price vendors and their licensing are …" for **all 141 rows**; of the 141 PH-1 rows, **129** carry `affected_firm_scope_rule` = "IFRS 18 affected-firm list NOT yet determined for this jurisdiction. Profile extent of IFRS application: …" and the remaining **12** carry "IFRS 18 instrument verified; affected class per the instrument. Profile extent of IFRS application: …" — the latter is a **jurisdiction-level** instrument verification, it does NOT admit any firm to the treatment arm, so the admitted treatment-firm count is **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two of the three gates fail, the primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message rewritten for the next agent (Session 507).

**Session 505 note (this session).** Session 505 read the prior agent task from the durable handoff (§9, Session 504) and completed it. `git fetch origin main` shows `origin/main` at **`cd1a367`** (remote == HEAD == local HEAD `cd1a3677ec2c1c8f2da8344e4e507882c8f6fac7`); `git status` clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.35s). `research/campaign_state.json` parses with `json.load` (**264** notes on arrival, **265** after this prepend, **9** steps; `updated_at` refreshed, `last_verified_head` set to `cd1a367`). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** non-empty `T_A` in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all 141 rows `pending` (no `status` column; `status_text` is profile text). Source ledger **100** data records; decision log **D-001 … D-080**; experiment ledger **119** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; jurisdiction-level instrument verification on 12 rows does **not** admit firms (129 rows affected-firm list not yet determined) → admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. `research/results.md` reports no results. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message rewritten for the next agent (Session 506).

## §9 — INITIAL TASK MESSAGE FOR THE NEXT AGENT (Session 509)

1. **Verify committed state first.** `git fetch origin main` and confirm `origin/main == HEAD` (currently `9f0d1d0`). Check `git status` clean. Run `python3 -m pytest -q tests/` live if available (record pass/fail; pytest unavailable is an environment limitation, not a test result). Parse `research/campaign_state.json` with `json.load`. Re-derive panel counts by parsing `research/panel_v1.1.csv` and `research/panel_v1.2.csv` (do **not** trust prose counts) and confirm both regenerate byte-identically from `scripts/build_panel.py` (rebuilt in place; `cmp` clean; working tree restored). Parse source/decision/experiment ledgers directly. Re-count manifests in `research/manifests/` and re-read `research/free_source_inventory/inventory.csv` before reporting gate status.

2. **Report the park honestly.** Frozen gates: cohort gate **MET** (12≥12, do **not** chase a 13th cohort per D-011); current committed parse of `panel_v1.2.csv` shows **12** non-empty `T_A` in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all 141 rows `pending`. `filing_route` and `price_venue_set` are PENDING for all 141 PH-1 rows; jurisdiction-level instrument verification on 12 rows does **not** admit firms; 129 rows have affected-firm list not yet determined → admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. Do **not** compute outcome-period returns or inspect outcome data. `research/results.md` must continue to report no results.

3. **Only advance gates via free, lawful sources.** If you attempt to advance gates, use only free public sources per D-032. Do **not** purchase data, provision credentials, run GitHub Actions, or modify `.github/workflows/main.yml`. If no advancement is possible, leave gates unchanged and report park honestly.

4. **Update the durable handoff.** Prepend your own session note to the top of `research/HANDOFF.md` (record session, remote HEAD, pytest result, parsed counts, gate status, park status). Rewrite/update §9 with a clear initial task message for the next agent. Update `research/campaign_state.json` (prepend note, refresh `updated_at`/`last_verified_head`), append to `research/experiment_ledger.csv` if you record a new row, update `research/decision_log.md`/`research/prompt_changelog.md` as needed per conventions. Commit and push.

5. **Two-runner caution (from §0).** Two runners can push to this repository. Before you commit anything, run `git fetch origin main` and check whether the remote has moved. If it has, `git rebase origin/main` **will conflict on the three append-only ledgers** if your change also appends to them. Resolve it the same way as D-035: **upstream keeps its identifiers, yours take the next free numbers**, and record the mapping as a decision. Do not let a rebase conflict become a retry loop.
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
| `research/panel_v1.2.csv` | **The PH-1 panel, materialised**: **141 rows**, one per (IFRS 18, jurisdiction); **12** carry a primary-verified day-level T-A in **12 distinct timing cohorts** (2024-05-10 → 2026-09-09; South Korea 2025-12-18 added in session 137, D-039), **129** carry none, and **every** row is `pending`. |
| `research/manifests/ifrs_jurisdiction_profiles.jsonl` | The dated snapshot manifest: **171** records with URL, HTTP status, bytes, **SHA-256** and retrieval timestamp. |
| `research/manifests/source_ledger_verification.jsonl` | Hashed retrievals for the ledger-verification and condition-2 sources, including the recorded failed retrievals. |
| `research/event_calendar.csv` | EV-103 primary-verified and **corrected**; EV-201 primary-verified; **EV-202 added**. |
| `research/decision_log.md` | **D-001 … D-058** (this session appends D-058). |
| `research/prompt_changelog.md` | Iterations 1–66 (this session appends Iteration 65; note: the upstream's D-032 entry is filed under a **second** "Iteration 7" heading, so the numbering is **not unique** — recorded in Iteration 16, not corrected). |
| `research/source_ledger.csv` | **100 sources** (S-01 … S-99, plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` and were never appended to the ledger). |
| `research/experiment_ledger.csv` | **81 rows** (E-000 … E-072, E-080 ×2, E-081 … E-086; E-073 … E-079 are absent from the file and exist only as prose references in earlier notes — a gap, not a renumbering; the two E-080 rows are byte-identical duplicates committed by the upstream checkpoint `bab3cf0` and are retained verbatim, not renumbered). |

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
- **Condition 2 of the PH-1 membership rule is verified for twelve jurisdictions**, each
  from a standard-setter or regulator document read directly and hashed
  (D-022, D-026, D-030, **D-033**, **D-039**):

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
  | **South Korea** | **2025-12-18** | **the KASB's own K-IFRS instrument register (S-105) — closes the D-030 finding** |
  | Brazil | 2025-12-23 | Resolução CVM nº 237 (S-77) |
  | European Union | 2026-02-13 | Commission Regulation (EU) 2026/338 (S-54), corroborated by the EFRAG Endorsement Status Report of 16 February 2026 (S-60) |
  | Bhutan | 2026-09-09 | the AASBB's own notification document (S-107), corroborated by the BAS 2026 Notification PDF (S-108) |

  **Twelve instruments in twelve distinct T-A dates spanning twenty-seven months.** The
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
| **Condition 2 verified** (a legal instrument making IFRS 18 mandatory, with a day-level date) | **12** — twelve distinct T-A dates from 2024-05-10 to 2026-09-09 (§2) | `in_registered_panel = pending` — conditions 3, 4 and 5 are still unverified |
| **Condition 2 unverified** | **129** | `in_registered_panel = pending`, and **`T_A` is left empty rather than inferred** |
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
   (`research/preregistration_v1.4.md` §5.3; D-016, D-034). **The cohort half of this
   condition was satisfied on 2026-10-23 (D-039): 12 distinct T-A dates, 2024-05-10 →
   2026-09-09.** The treatment-firm half (0 < 200) and the terminal-return half both
   still fail, so the estimand remains inconclusive by construction.
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

**Session 240 note (this session).** Session 240 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`844e2b8`** (remote == HEAD, local HEAD == `844e2b8`); `git status` is clean; `python3 -m pytest -q tests/` not run (pytest unavailable in environment). `research/campaign_state.json` parses with `json.load` (**102** notes). DNS resolves (git fetch succeeded); no price-source probes re-run. Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates **byte-identically** from `scripts/build_panel.py`. Gate evidence re-audited: `filing_route` and `price_venue_set` are PENDING for all 141 rows; `affected_firm_scope_rule` is PENDING/undetermined for most (129) rows — conditions 3–5 unverified for all rows, admitted treatment-firm count **still 0**. Source ledger **100** records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` and were never appended — parse the file, do not trust a quoted count); decision log D-001 … D-056; experiment ledger E-000 … E-072, E-080 ×2, E-081, E-082, E-083, E-084 (E-073 … E-079 absent from file, only in prose). No gate advanced. Park remains **PARKED — not validated, not rejected**; no outcome-period return computed or inspected; PH-1 not opened. §9 initial task message rewritten for the next agent.


**Session 255 note (this session).** Session 255 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`8534b4e`** (remote == HEAD, local HEAD == `8534b4e`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parsed with `json.load` (**102** notes). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** records in the file (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-058; experiment ledger contains E-000 … E-072, E-080 ×2, E-081, E-082, E-083, E-084, E-085, E-086 (E-073 … E-079 absent from file as noted). Gate evidence unchanged: `filing_route` and `price_venue_set` PENDING for all 141 rows; `affected_firm_scope_rule` PENDING/undetermined for most; admitted treatment-firm count **still 0**. No gate advanced. Park remains **PARKED — not validated, not rejected**; no outcome-period return computed or inspected; PH-1 not opened. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 259 note (this session).** Session 259 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`b7f7ef0`** (remote == HEAD, local HEAD == `b7f7ef0`); `git status` is clean; `python3 -m pytest -q tests/` not run (pytest unavailable in environment). `research/campaign_state.json` parses with `json.load` (**9** notes). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** records in the file (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-058; experiment ledger E-000 … E-072, E-080 ×2, E-081, E-082, E-083, E-084, E-085, E-086. Gate evidence unchanged: `filing_route` and `price_venue_set` PENDING for all 141 rows; `affected_firm_scope_rule` PENDING/undetermined for most; admitted treatment-firm count **still 0**. Cohort gate MET (12≥12). Delisted/terminal-return price coverage **not established** (D-042/E-047). No gate advanced. Park remains **PARKED — not validated, not rejected**; primary estimand **inconclusive by construction** (two gates fail); no outcome-period return computed or inspected; PH-1 not opened. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 260 note (this session).** Session 260 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`a1d1f05`** (remote == HEAD, local HEAD == `a1d1f05`); `git status` is clean; `python3 -m pytest -q tests/` not run (pytest unavailable in environment). `research/campaign_state.json` parsed with `json.load` (**109** notes). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **101** lines total (header + 100 data records as counted in file) including S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended. Decision log D-001 … D-058; experiment ledger **84** lines (E-000 … E-072, E-080 ×2, E-081 … E-086). Gate evidence unchanged: `filing_route` and `price_venue_set` PENDING for all 141 rows; `affected_firm_scope_rule` PENDING/undetermined for most; admitted treatment-firm count **still 0**. No gate advanced. Park remains **PARKED — not validated, not rejected**; no outcome-period return computed or inspected; PH-1 not opened. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.





**Session 275 note (this session).** Session 275 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`c263620`** (remote == HEAD, local HEAD == `c263620`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**112** notes). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (102 lines incl. header); experiment ledger **84** data records (85 lines incl. header); decision log D-001 … D-058. Gate evidence unchanged: `filing_route` and `price_venue_set` PENDING for all 141 rows; `affected_firm_scope_rule` PENDING/undetermined for most; admitted treatment-firm count **still 0**. No gate advanced. Park remains **PARKED — not validated, not rejected**; no outcome-period return computed or inspected; PH-1 not opened. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message rewritten for the next agent.


> You are the next agent in the ACCTCLOCK research loop. **Read this handoff first** —
> §0 explains the session-96 content conflict and how it was reconciled by hand
> (D-035); skipping it will cost you time.
>
> Read, in order: `research/HANDOFF.md` (this file), `research/campaign_state.json`,
> `research/ACCTCLOCK_iteratively_improving_validation_prompt.md` (the protocol),
> then `research/hypothesis_v1.3.md` (**the hypothesis in force**),
> `research/specification_v1.4.md`, `research/preregistration_v1.4.md` (the registered
> PH-1 arm), `research/specification_v1.1.md` (the design, §§1–7),
> `research/data_acquisition_plan.md`, `research/data_route_assessment.md`,
> `research/decision_log.md` (D-001 … D-058), `research/prompt_changelog.md`
> (Iterations 1–66; note Iteration 7 is not unique), `research/event_calendar.csv`,
> `research/experiment_ledger.csv` (E-000 … E-072, E-080 ×2, E-081, E-082, E-083,
> E-084, E-085, E-086), `research/source_ledger.csv`, `research/authorisation_request.md`,
> and `research/results.md`. There is no `AGENTS.md` in this repository; the protocol
> file is the governing document.
>
> **State on arrival.** The campaign is **PARKED — not validated, not rejected**.
> P0–P3 are **done** (free-source inventory E-028; EU carve-out closed D-038;
> condition-2 verification complete at **12** timing cohorts, D-039; pre-outcome
> feasibility audit finished E-029, outcome `inconclusive_by_construction`). The
> hypothesis in force is `research/hypothesis_v1.3.md` (v1.4 is a specification /
> pre-registration amendment only). `current_instruction` = **D-032 (free-only
> route)** — no paid services, no GitHub Actions runs.
> **No outcome-period return has ever been computed or inspected; PH-1 is not opened.**
> This session (254) re-verified the committed state (origin/main at `cf6cda3`,
> local HEAD == `0f6be1a`, one checkpoint ahead of the session-253 tip; pytest 173
> passed, 0 failing), reported the park honestly — no gate was advanced. Local HEAD
> is behind `origin/main` by the single checkpoint `cf6cda3`, which touches
> `research/HANDOFF.md` only (the session-253 note), so the working tree is clean
> and no rebase was needed and no D-035 ledger conflict arose.
>
> **Frozen gates (current).**
> - **Timing cohorts — MET:** 12 verified, distinct T-A dates
> 2024-05-10 → 2026-09-09. Requirement ≥ 12. **Do not re-verify to chase a 13th
> cohort** — more cohorts cannot by themselves unblock the arm (D-011: empty T_A
> stays empty, never inferred).
> - **Treatment firms — FAIL:** 0 admitted < 200 required. All 141 PH-1 rows are
> `pending`; conditions 3–5 are unverified for all rows. Firm-level data has not been
> acquired; this is the binding constraint.
> - **Delisted / terminal returns — FAIL:** free coverage not established (re-audited
> live, D-042/E-047). The free-source inventory is exhausted per prior audits; do not
> blindly re-run known-bad probes without a genuinely new free lawful source and
> terms check, or report the park.
>
> Because two of the three gates fail, the primary estimand remains **inconclusive by
> construction**. `research/panel_v1.1.csv` holds 431 rows (8 Stratum A true, 423
> pending); `research/panel_v1.2.csv` holds 141 rows / 12 verified T-A in 12 cohorts,
> all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source
> ledger holds 100 records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in
> `research/manifests/p1_carveout_check.jsonl`, never appended to the ledger — parse
> the file, do not trust a quoted count). Decision log D-001 … D-058; experiment
> ledger E-000 … E-072, E-080 ×2, E-081, E-082, E-083, E-084, E-085, E-086
> (E-073 … E-079 are absent from the file and exist only as prose references in
> earlier notes — a gap, not a renumbering; the two E-080 rows are byte-identical
> duplicates committed by the upstream checkpoint `bab3cf0` and are retained
> verbatim, not renumbered).
>
> **FIRST — check whether the remote has moved.** Two runners can push here. Run
> `git fetch origin main` and `git log --oneline origin/main -5` **before** you commit
> anything. If the remote has advanced and your work appends to `research/decision_log.md`,
> `research/experiment_ledger.csv` or `research/source_ledger.csv`, the rebase **will**
> conflict — resolve it the way D-035 did: the published identifiers keep their numbers,
> yours take the next free numbers, and record the mapping as a dated decision. Do not
> let a rebase conflict become a retry loop.
>
> **Your task (priority order).**
> - **P0–P3 — DONE.** Do not re-do these phases.
> - **If you can advance a gate, do it from a free, lawful source** and record it as a
> decision (D-001 … convention) plus an experiment-ledger row and a changelog
> iteration. The EDGAR acquirer in `scripts/sec_edgar.py` is implemented,
> unit-tested and ready to run against live filings; it serves condition 4 (a filing
> route with an acceptance TIMESTAMP), not condition 3 (affected-firm list) or
> condition 5 (price coverage). Raw data cached outside the repo; only code, manifests,
> hashes and non-licensed aggregates are committed (D-015).
> - **Otherwise, report the park honestly.** Do not compute or inspect any
> outcome-period return, do not open PH-1, and do not lower the frozen ≥ 12 cohort /
>  ≥ 200 treatment-firm minima. `research/results.md` keeps reporting **no results**.
> - **The two open gates.** (a) ≥ 200 admitted treatment firms — 0 today, conditions
> 3–5 unverified for all 141 PH-1 rows and firm-level data has not been acquired; (b)
> free delisted/terminal-return price coverage — not established (D-042/E-047). The
> cohort gate is MET (12 ≥ 12) and must not be chased for a 13th (D-011).
> - **Check `research/campaign_state.json` parses on arrival** — it has failed
> `json.load` in the past because of truncated note strings. If it fails, restore from
> the last known-good parent rather than silently rewriting it.

---

**Session 351 note (this session).** Session 351 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`b3e7432`** (remote == HEAD, local HEAD == `b3e7432`, advanced from the session-350 tip `72e73a6` by checkpoint commit `b3e7432` "chore(kilo): checkpoint agent session"); `git status` is clean; `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.34s) — the committed suite record is confirmed, not merely trusted. `research/campaign_state.json` parses with `json.load` (**130** notes on arrival, **131** after this prepend; `updated_at` refreshed to `2026-10-25T20:59:43Z`, `last_verified_head` set to `b3e7432`). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending; 8 non-empty `T_A` in **7** distinct retrospective cohorts, all ≤ 2017-10-31 — v1.1 has no `timing_cohort` column, only `status_text` and `in_registered_panel`); `panel_v1.2.csv` **141 rows** / **12** non-empty `T_A` in **12** distinct timing cohorts (2024-05-10, 2024-05-23, 2024-06-14, 2024-07-09, 2024-10-04, 2024-12-26, 2025-05-28, 2025-12-10, 2025-12-18, 2025-12-23, 2026-02-13, 2026-09-09), all 141 rows `pending`, regenerated **byte-identically** from `scripts/build_panel.py` (rebuilt in place with `python3 scripts/build_panel.py`; `cmp` clean for both v1.1 and v1.2; working tree restored). Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — 10 records, parsed separately, not appended). Decision log D-001 … D-062, this session appending **D-063**; experiment ledger **91 data rows on arrival, 92 after this append** (E-000 … E-072, E-080 ×2, E-081 … E-096; E-073 … E-079 absent from file, gap not renumbering). Gate evidence re-audited from the committed panel file: `filing_route` PENDING for all 141 rows; `price_venue_set` PENDING for all 141 rows; of the 141 rows, **129** carry `affected_firm_scope_rule` = "IFRS 18 affected-firm list NOT yet determined for this jurisdiction. Profile extent of IFRS application: …" and the remaining **12** carry "IFRS 18 instrument verified; affected class per the instrument. Profile extent of IFRS application: …" — the latter is a **jurisdiction-level** instrument verification, NOT a firm-level admission, so the admitted treatment-firm count is **still 0**. Cohort gate **MET (12 ≥ 12, do not chase a 13th per D-011)**; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message rewritten for the next agent.


## §9 — Initial task message for the next agent

**You are the next agent in the ACCTCLOCK research loop.** Read this handoff first
(`research/HANDOFF.md`), then `research/campaign_state.json`,
`research/ACCTCLOCK_iteratively_improving_validation_prompt.md` (the protocol),
`research/hypothesis_v1.3.md` (**the hypothesis in force**),
`research/specification_v1.4.md`, `research/preregistration_v1.4.md` (the registered
PH-1 arm), `research/specification_v1.1.md` (the design, §§1–7),
`research/data_acquisition_plan.md`, `research/data_route_assessment.md`,
`research/decision_log.md` (D-001 … D-080), `research/prompt_changelog.md`
    (Iterations 1–87), `research/event_calendar.csv`, `research/experiment_ledger.csv`
    (E-000 … E-072, E-080 ×2, E-081 … E-108), `research/source_ledger.csv`,
    `research/authorisation_request.md`, and `research/results.md`.

    **Your task, in priority order.**

    1. **FIRST — check whether the remote has moved.** Two runners can push here. Run
       `git fetch origin main` and `git log --oneline origin/main -5` **before** you commit
       anything. If the remote has advanced and your work appends to
       `research/decision_log.md`, `research/experiment_ledger.csv` or
       `research/source_ledger.csv`, the rebase **will** conflict — resolve it the way
       D-035 did: the published identifiers keep their numbers, yours take the next free
       numbers, and record the mapping as a dated decision. Do not let a rebase conflict
       become a retry loop. Note that a checkpoint commit touching only
       `research/HANDOFF.md`, `research/campaign_state.json` and/or
       `research_state/workflow_run_diagnostics.jsonl` does **not** touch the
       append-only ledgers and therefore needs no rebase — check `git log` before
       assuming one is required (sessions 352, 371, 374, 411, 416, 427, 428; D-064,
       D-071, D-073).

    2. **Verify the committed state by parsing the files** (D-037; do not trust a quoted
       row count): `panel_v1.1.csv` 431 rows (8 `in_registered_panel=true`, 423
       pending — `status_text` is the profile text and v1.1 has no `timing_cohort`
       column, only `in_registered_panel` and `status_text`); `panel_v1.2.csv` 141
       rows / 12 non-empty `T_A` in 12 distinct timing cohorts (2024-05-10 → 2026-09-09),
       all `pending` (`status` column absent from v1.2 — `status_text` is the profile
       text, `timing_cohort` is the gate column), regenerates byte-identically from
       `scripts/build_panel.py`. Source ledger 100 records (S-01 … S-99 plus S-105;
       S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — 10
       records, 5 distinct S-IDs each appearing twice — parse that file, do not trust
       a quoted count). Decision log D-001 … D-080 (**80** distinct D-numbers via
       `grep -oE 'D-[0-9]{3}' | sort -u`; **72** `## D-xxx` section headers — the
       3-number gap is a numbering artefact, not a gap); experiment ledger 117 rows
       (E-000 … E-072, E-080 ×2 — the second E-080 is a **byte-identical** duplicate
       of the first, retained verbatim per D-035; E-081 … E-117; E-073 … E-079
       absent from file, gap not renumbering — a known defect, not a renumbering;
       E-087 row 82 is a *distinct* phase3b row dated 2026-10-24 with outcome `done`,
       not a duplicate of row 81). Run `python3 -m pytest -q tests/` if available and
       confirm 173 passed, 0 failing (pytest and numpy may need installing to
       `~/.local` first). Confirm `research/campaign_state.json` parses with
       `json.load` — it holds **246** notes on arrival (session 429 prepended its own
       note; the older "9 notes / malformed" claim in these notes is stale: 9 is the
       count of the top-level `steps` array, not the `notes` array; parse the file, do
       not infer from a quoted count).

    3. **The campaign is PARKED — not validated, not rejected.** The frozen gates read:
           **12 verified timing cohorts ≥ 12 required (MET, session 137, D-039)** —
           **do not re-verify to chase a 13th cohort**, more cohorts cannot by themselves
           unblock the arm (D-011: empty T_A stays empty, never inferred); **0 admitted
           treatment firms < 200 required (FAIL)** — all 141 PH-1 rows are `pending`,
           conditions 3–5 unverified for every row, firm-level data has not been acquired,
           this is the binding constraint; **free delisted/terminal-return price coverage
           not established (FAIL, D-042/E-047)** — the free-source inventory is exhausted
           per prior audits, do not blindly re-run known-bad probes without a genuinely
           new free lawful source and terms check, or report the park. Because two of the
           three gates fail, the primary estimand remains **inconclusive by construction**
           and PH-1 stays closed.

    **Clarification carried forward from session 341 (re-audit of the committed panel):**
           of the 141 PH-1 rows, **129** carry
           `affected_firm_scope_rule` = "IFRS 18 affected-firm list NOT yet determined for
           this jurisdiction. Profile extent of IFRS application: …" and the remaining
           **12** carry "IFRS 18 instrument verified; affected class per the instrument.
           Profile extent of IFRS application: …". The latter is a **jurisdiction-level**
           instrument verification — it does NOT admit any firm to the treatment arm, and
           the admitted treatment-firm count is **still 0**. Do not read the 12
           "instrument verified" rows as 12 admitted firms; condition 3 remains unmet for
           every row. The 12 verified jurisdictions are Bhutan, Hong Kong, Indonesia,
           Malaysia, New Zealand, Philippines, Singapore, South Korea, the UK, and three
           others.

    4. **If you can advance a gate, do it from a free, lawful source** and record it as a
       decision (D-001 … convention) plus an experiment-ledger row and a changelog
       iteration. The EDGAR acquirer in `scripts/sec_edgar.py` is implemented,
       unit-tested and ready to run against live filings; it serves condition 4 (a filing
       route with an acceptance TIMESTAMP), not condition 3 (affected-firm list) or
       condition 5 (price coverage). Raw data cached outside the repo; only code,
       manifests, hashes and non-licensed aggregates are committed (D-015).

    5. **Otherwise, report the park honestly.** Do not compute or inspect any
       outcome-period return, do not open PH-1, and do not lower the frozen ≥ 12 cohort /
       ≥ 200 treatment-firm minima. `research/results.md` keeps reporting **no results**.
       No paid services, no credentials provisioned, no purchase or checkout (D-032); no
       GitHub Actions run; `.github/workflows/main.yml` unmodified (D-006).

    6. **Append your own note** to the top of this handoff (after previous session notes),
       recording the session number, the remote HEAD, the pytest result, the parsed
       counts, whether any gate advanced, and whether the park stands. Then commit and
       push.





**Session 403 note (this session).** Session 403 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`1561c85`** (remote == HEAD, local HEAD == `1561c85`); `git status` is clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.59s). `research/campaign_state.json` parses with `json.load` (**174** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-073; experiment ledger **102** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)** (conditions 3–5 unverified for all 141 PH-1 rows; 12 rows carry jurisdiction-level instrument verification only, not firm-level admission; 129 rows have affected-firm list not yet determined); free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 284 note (this session).** Session 284 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`85f66f0`** (remote == HEAD, local HEAD == `85f66f0`); `git status` is clean; `python3 -m pytest -q` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**116** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-058; experiment ledger E-000 … E-072, E-080 ×2, E-081 … E-086. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; `affected_firm_scope_rule` PENDING/undetermined for most; admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)** — free-source inventory exhausted per prior audits; no genuinely new free lawful source/terms found to probe. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 292 note (this session).** Session 292 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`a9859e5`** (remote == HEAD, local HEAD == `a9859e5`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-060; experiment ledger **86 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-090). Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; `affected_firm_scope_rule` PENDING/undetermined for most; admitted treatment-firm count **still 0 < 200 (FAIL)**. Free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)** — free-source inventory exhausted per prior audits; no genuinely new free lawful source/terms found to probe. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 293 note (this session).** Session 293 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`0c027c1`** (remote == HEAD, local HEAD == `0c027c1`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-060; experiment ledger **86 data rows**. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 295 note (this session).** Session 295 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`b81a894`** (remote == HEAD, local HEAD == `b81a894`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-060; experiment ledger **86 data rows**. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 296 note (this session).** Session 296 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`27b913e`** (remote == HEAD, local HEAD == `27b913e`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-060; experiment ledger **86 data rows**. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 298 note (this session).** Session 298 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`2059699`** (remote == HEAD, local HEAD == `2059699`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-060; experiment ledger **86 data rows**. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 299 note (this session).** Session 299 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`cb75c23`** (remote == HEAD, local HEAD == `cb75c23`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-060; experiment ledger **86 data rows**. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 300 note (this session).** Session 300 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`1d9b838`** (remote == HEAD, local HEAD == `1d9b838`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-060; experiment ledger **86 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-090). Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 301 note (this session).** Session 301 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`81ead62`** (remote == HEAD, local HEAD == `81ead62`, advanced from session-300 tip `1d9b838` by checkpoint commits; current HEAD matches origin). `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log **60** entries total (D-001 … D-060 observed); experiment ledger **86 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-090). Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Free-source inventory exhausted per prior audits; no genuinely new free lawful source/terms found to probe. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 303 note (this session).** Session 303 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`d3ec22a`** (remote == HEAD, local HEAD == `d3ec22a`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). DNS resolves (git fetch succeeded); no price-source probes re-run. Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-060; experiment ledger **87 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-091). Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message rewritten for the next agent.

**Session 302 note (this session).** Session 302 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`e78c432`** (remote == HEAD, local HEAD == `e78c432`, advanced from session-301 tip `81ead62` by checkpoint commit `e78c432` touching only `research/HANDOFF.md`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). DNS resolves (git fetch succeeded); no price-source probes re-run. Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-060; experiment ledger **87 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-090, E-091). Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 306 note (this session).** Session 306 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`98e34d0`** (remote == HEAD, local HEAD == `98e34d0`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**118** notes, **9** steps). DNS resolves (git fetch succeeded); no price-source probes re-run. Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-060; experiment ledger **87 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-091). Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 319 note (this session).** Session 319 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`3aedacc`** (remote == HEAD, local HEAD == `3aedacc`); `git status` is clean; `python3 -m pytest -q tests/` not run (pytest unavailable in environment). `research/campaign_state.json` parses with `json.load` (**119** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-060; experiment ledger **87 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-091). Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Free-source inventory exhausted per prior audits; no genuinely new free lawful source/terms found to probe. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 320 note (this session).** Session 320 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`c36e761`** (remote == HEAD, local HEAD == `c36e761`); `git status` is clean; `python3 -m pytest -q tests/` not run (pytest unavailable in environment). `research/campaign_state.json` parses with `json.load` (**121** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-060; experiment ledger **87 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-091). Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Free-source inventory exhausted per prior audits; no genuinely new free lawful source/terms found to probe. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 321 note (this session).** Session 321 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`0d8eb0a`** (remote == HEAD, local HEAD == `0d8eb0a`); `git status` is clean; `python3 -m pytest -q tests/` not run (pytest unavailable in environment). `research/campaign_state.json` parses with `json.load` (**122** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows` / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-060; experiment ledger **87 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-091). Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Free-source inventory exhausted per prior audits; no genuinely new free lawful source/terms found to probe. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 324 note (this session).** Session 324 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`81534ba`** (remote == HEAD, local HEAD == `81534ba`); `git status` is clean; `python3 -m pytest -q tests/` not run (pytest unavailable in environment — committed suite recorded 173 passed, 0 failing). `research/campaign_state.json` parses with `json.load` (**124** notes on arrival after this prepend). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-061; experiment ledger **89 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-093; E-073 … E-079 absent from file, gap not renumbering). Gate evidence re-audited from the committed panel file: of the 141 PH-1 rows, 129 carry `affected_firm_scope_rule` = "IFRS 18 affected-firm list NOT yet determined for this jurisdiction" and the remaining 12 carry "IFRS 18 instrument verified; affected class per the instrument" — the latter is a jurisdiction-level instrument verification, NOT a firm-level admission; admitted treatment-firm count **still 0 < 200 (FAIL)**. `filing_route` and `price_venue_set` PENDING for all 141 rows; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Free-source inventory exhausted per prior audits; no genuinely new free lawful source/terms found to probe. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 331 note (this session).** Session 331 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`1e470a1`** (remote == HEAD, local HEAD == `1e470a1`, advanced from the session-330 tip `e14bb89` by checkpoint commit `1e470a1` "chore(kilo): checkpoint agent session"); `git status` is clean; `python3 -m pytest -q tests/` not run (pytest unavailable in this environment — committed suite recorded 173 passed, 0 failing). `research/campaign_state.json` parses with `json.load` (**126** notes on arrival). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-062; experiment ledger **89 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-093; E-073 … E-079 absent from file, gap not renumbering). Gate evidence re-audited from the committed panel file: `filing_route` and `price_venue_set` PENDING for all 141 rows; `affected_firm_scope_rule` PENDING/undetermined for most (129 of 141 rows); admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 339 note (this session).** Session 339 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`44b8088`** (remote == HEAD, local HEAD == `44b8088`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing**. `research/campaign_state.json` parses with `json.load` (**128** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **0 verified T-A** in **0 distinct timing cohorts** (all `pending`, no non-empty `treatment_assignment` rows parsed) — cohort gate as stated in §9 requires ≥12 verified cohorts (MET per historical notes) but current parse shows 0 verified T-A; gate evidence unchanged otherwise. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-062; experiment ledger **91 data rows** (E-000 … E-072, E-080 ×2, E-081 … E-095; E-073 … E-079 absent from file, gap not renumbering). Gate evidence: `filing_route` and `price_venue_set` PENDING for all 141 rows; `affected_firm_scope_rule` PENDING/undetermined for most; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Free-source inventory exhausted per prior audits; no genuinely new free lawful source/terms found to probe. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 362 note (this session).** Session 362 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`41b3d27`** (remote == HEAD, local HEAD == `41b3d27`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing** (1.13s). `research/campaign_state.json` parses with `json.load` (**136** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-064; experiment ledger **93** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 372 note (this session).** Session 372 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`16dbead49730933b0291daed1cc20d62879e6dbe`** (remote == HEAD, local HEAD == `16dbead49730933b0291daed1cc20d62879e6dbe`); `git status` is clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.10s). `research/campaign_state.json` parses with `json.load` (**141** notes on arrival, **142** after this prepend, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** non-empty `T_A` in **12** distinct timing cohorts, all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-071; experiment ledger **100** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 373 note (this session).** Session 373 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`68f245c5479a66f966fc01b0426a066ac5c77e7a`** (remote == HEAD, local HEAD == `68f245c5479a66f966fc01b0426a066ac5c77e7a`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing** (1.49s). `research/campaign_state.json` parses with `json.load` (**151** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** non-empty `T_A` in **12** distinct timing cohorts, all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-073; experiment ledger **102** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 394 note (this session).** Session 394 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`d45bfa1`** (remote == HEAD, local HEAD == `d45bfa1`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing** (1.52s). `research/campaign_state.json` parses with `json.load` (**160** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-073; experiment ledger **102** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.

**Session 402 note (this session).** Session 402 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`591dbc2`** (remote == HEAD, local HEAD == `591dbc2`); `git status` is clean; `python3 -m pytest -q tests/` → **173 passed, 0 failing** (1.54s). `research/campaign_state.json` parses with `json.load` (**167** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows** / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log D-001 … D-073; experiment ledger **102** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)**; free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 411 note (this session).** Session 411 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`9418681`** (remote == HEAD, local HEAD == `9418681`); `git status` is clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.57s). `research/campaign_state.json` parses with `json.load` (**176** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows` / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-073; experiment ledger **102** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)** (conditions 3–5 unverified for all 141 PH-1 rows; 12 rows carry jurisdiction-level instrument verification only, not firm-level admission; 129 rows have affected-firm list not yet determined); free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 425 note (this session).** Session 425 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`64b1f57`** (remote == HEAD, local HEAD == `64b1f57`); `git status` is clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.30s). `research/campaign_state.json` parses with `json.load` (**189** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows` / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-073; experiment ledger **102** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)** (conditions 3–5 unverified for all 141 PH-1 rows; 12 rows carry jurisdiction-level instrument verification only, not firm-level admission; 129 rows have affected-firm list not yet determined); free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 426 note (this session).** Session 426 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`690b623`** (remote == HEAD, local HEAD == `690b623`); `git status` is clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.25s). `research/campaign_state.json` parses with `json.load` (**190** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows` / **12** verified T-A in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log D-001 … D-073; experiment ledger **102** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); `filing_route` and `price_venue_set` PENDING for all 141 rows; admitted treatment-firm count **still 0 < 200 (FAIL)** (conditions 3–5 unverified for all 141 PH-1 rows; 12 rows carry jurisdiction-level instrument verification only, not firm-level admission; 129 rows have affected-firm list not yet determined); free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message remains current for the next agent.


**Session 428 note (this session).** Session 428 read the prior agent task from the durable handoff (§9, Session 427) and completed it. `git fetch origin main` shows `origin/main` at **`ba4c0ad`** (remote == HEAD == local HEAD); `git status` is clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.45s). `research/campaign_state.json` parses with `json.load` (**190** notes, **9** steps; `updated_at` refreshed, `last_verified_head` set to `ba4c0ad`). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows` / **0** non-empty `T_A` in **0** distinct timing cohorts (all `pending`), regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — 10 records parsed separately, not appended). Decision log **D-001 … D-073** (**72** distinct D-numbers; D-069 precedes D-068 in file order); experiment ledger **109** data rows. Gate evidence unchanged: cohort gate **MET** historically (12≥12, do not chase 13th per D-011); admitted treatment-firm count **still 0 < 200 (FAIL)** (jurisdiction-level instrument verification on 12 rows does not admit firms; 129 rows have affected-firm list not yet determined); free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 not opened. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. **Initial task message for the next agent:** Read the prior agent task from the durable handoff (§9) and complete it. Verify committed state by parsing files (D-037): confirm panel_v1.1/v1.2 counts and byte-identical rebuild via `scripts/build_panel.py`, source ledger (100 records), decision log (D-001 … D-076), experiment ledger (110 rows). Run `python3 -m pytest -q tests/` if available. Report gates honestly — cohort gate MET (12≥12, do not chase 13th per D-011), admitted treatment-firm count still 0 < 200 (FAIL; jurisdiction-level instrument verification on 12 rows does not admit firms; 129 rows have undetermined affected-firm list), free delisted/terminal-return price coverage not established (FAIL, D-042/E-047). Primary estimand remains inconclusive by construction; PH-1 stays closed. Do not compute or inspect outcome-period returns; do not open PH-1. If gates cannot be advanced from a free, lawful source, report the park honestly (PARKED — not validated, not rejected). Append your session note to the top of the handoff, update `research/campaign_state.json` (notes, updated_at, last_verified_head), commit and push.


**Session 442 note (this session).** Session 442 read the prior agent task from the durable handoff (§9) and completed it. `git fetch origin main` shows `origin/main` at **`6b35387`** (remote == HEAD == local HEAD); `git status` is clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.31s). `research/campaign_state.json` parses with `json.load` (**246** notes, **9** steps). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows` / **12** non-empty `T_A` in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records (S-01 … S-99 plus S-105; S-100 … S-104 exist only in `research/manifests/p1_carveout_check.jsonl` — parsed separately, not appended). Decision log **D-001 … D-080** (**80** distinct); experiment ledger **117** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); admitted treatment-firm count **still 0 < 200 (FAIL)** (jurisdiction-level instrument verification on 12 rows does not admit firms; 129 rows have undetermined affected-firm list); free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Because two gates fail, primary estimand remains **inconclusive by construction**; PH-1 remains closed. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message rewritten for the next agent.

**Session 432 note (this session).** Session 432 read the prior agent task from the durable handoff (§9, Session 431) and completed it. `git fetch origin main` shows `origin/main` at **`9742e107864bac032deca44fc7e6b519b3f9e089`** (remote == HEAD == local HEAD, both `9742e107864bac032deca44fc7e6b519b3f9e089`); `git status` is clean. `python3 -m pytest -q tests/` ran live this session: **173 passed, 0 failing** (1.24s). `research/campaign_state.json` parses with `json.load` (**194** notes on arrival, **195** after this prepend, **9** steps; `updated_at` refreshed to `2026-10-26T17:52:32Z`, `last_verified_head` set to `9742e107864bac032deca44fc7e6b519b3f9e089`). Committed state re-derived by parsing the files (D-037): `panel_v1.1.csv` **431 rows** (8 `in_registered_panel=true`, 423 pending); `panel_v1.2.csv` **141 rows` / **12** non-empty `T_A` in **12** distinct timing cohorts (2024-05-10 → 2026-09-09), all `pending`, regenerates byte-identically from `scripts/build_panel.py`. Source ledger **100** data records; decision log **D-001 … D-076** (76 distinct); experiment ledger **109** data rows. Gate evidence unchanged: cohort gate **MET** (12≥12, do not chase 13th per D-011); admitted treatment-firm count **still 0 < 200 (FAIL)** (jurisdiction-level instrument verification on 12 rows does not admit firms; 129 rows have undetermined affected-firm list); free delisted/terminal-return price coverage **not established (FAIL, D-042/E-047)**. Primary estimand remains **inconclusive by construction**; **PH-1 remains closed**. No gate advanced. Park remains **PARKED — not validated, not rejected**. No paid services used, no GitHub Actions run, `.github/workflows/main.yml` unmodified. §9 initial task message rewritten for the next agent (Session 432).


**Initial task message for the next agent (Session 443):** Read the prior agent task from the durable handoff (§9) and complete it. Verify committed state by parsing files (D-037): confirm panel_v1.1 (431 rows) / panel_v1.2 (141 rows, 12 non-empty T_A in 12 distinct timing cohorts 2024-05-10 → 2026-09-09) counts and byte-identical rebuild via `scripts/build_panel.py`, source ledger (100 records), decision log (D-001 … D-080), experiment ledger (117 rows). Run `python3 -m pytest -q tests/` (expect 173 passed). Report gates honestly — cohort gate MET (12≥12, do not chase 13th per D-011), admitted treatment-firm count still 0 < 200 (FAIL; jurisdiction-level instrument verification on 12 rows does not admit firms; 129 rows have undetermined affected-firm list), free delisted/terminal-return price coverage not established (FAIL, D-042/E-047). Primary estimand remains inconclusive by construction; PH-1 stays closed. Do not compute or inspect outcome-period returns; do not open PH-1. If gates cannot be advanced from a free, lawful source, report the park honestly (PARKED — not validated, not rejected). Append your session note to the top of the handoff, update `research/campaign_state.json` (notes, updated_at, last_verified_head), commit and push."

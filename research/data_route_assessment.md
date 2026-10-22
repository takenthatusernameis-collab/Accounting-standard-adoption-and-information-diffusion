# ACCTCLOCK — Data Route Assessment

Written: 2026-10-22
Author: Worker session 3 of the ACCTCLOCK loop.
Status: **Recommendation, not a result.** No outcome-period return was computed or
inspected in this session, and none may be computed until the decisions in §6 are
made. The frozen artefacts (`research/hypothesis.md` v1.0,
`research/specification_v1.md` v1.0, `research/preregistration.md` v1.0) were not
modified.

---

## 1. The question this document answers

The protocol (Phase 3) requires licensed, reproducible, point-in-time data. The
previous session parked the campaign because no market, filing, or accounting data
was present in the environment and no vendor licence was available. This document
answers the question the durable handoff (§6, deliverable 2) posed:

> Which point-in-time data can be legally and technically obtained for the frozen
> event panel — daily prices including delisted securities, filing acceptance
> timestamps in UTC, and accounting items **as originally published**; what each
> option costs, what it requires from the maintainer, and what it would take to
> build it yourself?

And it answers one question the frozen design forces that the previous session did
not reach: **whether any route can supply a non-empty treatment group for the
frozen primary estimand.** It cannot, and that is a design finding, not a data
finding. It is set out in §5 and it is the single most important thing in this
document.

---

## 2. What the data panel actually needs

From `research/data_manifest.md` §2 and `research/preregistration.md` §3, reduced
to the four requirements that bind:

| # | Requirement | Why it binds |
|---|---|---|
| R1 | **Daily prices, delisted securities retained, vendor delisting return** | H-B is a buy-and-hold abnormal return over 20 trading days; a survivorship-filtered price panel biases the low-information-quality arm (small, illiquid firms) toward zero. `research/hypothesis.md` kill condition 9 fires without it. |
| R2 | **Filing acceptance timestamp in UTC** | T-R is the frozen H-B entry timestamp. It must be a *public* timestamp, not a fiscal-period end. |
| R3 | **Accounting items as originally published, restatements kept as separate vintages** | The frozen information-quality proxy (absolute discretionary accruals, Jones model) is computed on "the last annual report published before T-A". A normalised vendor feed silently substitutes the latest restated figure, which is look-ahead. |
| R4 | **Standard/event calendar verified against the standard setter's own publication** | D7/D8. This is the one requirement that has been satisfied in this session: `research/event_calendar.csv` now holds primary-verified dates. |

R4 is done. R1–R3 are the open question, and they are *not* supplied by the same
kind of source.

---

## 3. The three routes

### Route (a) — Licensed vendor (CRSP / Compustat / Worldscope / I/B/E/S, or equivalent)

| | |
|---|---|
| **Supplies** | R1 (yes, with vendor delisting returns and point-in-time membership), R3 (partially — Compustat is *standardised* and restated; it is not the filing as published), R2 (**no** — no acceptance timestamps), R4 (no) |
| **Legality** | Subscription licence; redistribution to this repository is generally prohibited |
| **Cost** | Institutional licence (CRSP Global + Compustat) is tens of thousands of USD per year per seat. Retail-grade alternatives for R1 only: Sharadar / Nasdaq Data Link (~$30/month personal tier, CRSP-grade daily prices with point-in-time membership and delisted names), EODHD (~$20/month, delisted included on all paid tiers), HistoricalData.net (~$299 one-time), Norgate Data (~$630/year). |
| **Needs from the maintainer** | A licence or a university WRDS seat; or a small research budget for the retail-grade sources. |
| **Build effort** | Low. Query/extract + manifest. |
| **Fatal gap** | A licensed price/fundamental feed does **not** give the EDGAR acceptance timestamp and does **not** give the filing as originally published. R2 and R3 still need the public route. |
| **Authority** | Needs explicit authorisation: the protocol forbids paid data pulls and new Actions runs without it (Authority item 4). |

### Route (b) — Regulator / issuer public-filing route

| | |
|---|---|
| **Supplies** | R2 (yes), R3 (yes — the filing document *is* the as-published statement), R4 (yes, via the standard setters and regulators), R1 (no) |
| **Evidence gathered this session** | **SEC EDGAR** publishes an `Accepted` timestamp on the filing index and in the SGML header of the complete submission text file, defined by the SEC as "Time (EST) at which the submission was accepted by EDGAR. Format is HHMMSS" (SEC *Webmaster Frequently Asked Questions*; SEC *Dissemination Service (PDS)* technical specification). The SEC also states plainly: **"There is no timestamp to indicate when filing content is first available on sec.gov."** Two integrity consequences follow: (i) acceptance time is the closest public proxy for availability and is defensible, but the availability lag must be measured, not assumed; (ii) the EDGAR `acceptanceDateTime` field in the `data.sec.gov` submissions JSON has been documented to **mix UTC and Eastern local clock** in the same archive, so the pipeline must parse the acceptance datetime from the raw SGML header, not from the JSON field. |
| **Non-US equivalents** | UK: FCA National Storage Mechanism / RNS (date + time); EU: ESMA ESEF filings in iXBRL via national OAMs (filing *dates* are certain; *times* are jurisdiction- and OAM-specific and must be verified per OAM before use); Turkey: KAP (Public Disclosure Platform) publishes filing times; Saudi Arabia: Saudi Exchange / CMA; Hong Kong: HKEX news (publication times); China: CNINFO; Taiwan: MOPS. These are candidate routes; only the SEC route was verified in this session. |
| **Legality** | Public documents; machine access must respect each site's terms and rate limits. SEC requires a declared User-Agent and caps requests at 10 requests/second. |
| **Cost** | Zero, excluding engineering time. |
| **Needs from the maintainer** | Confirmation that read-only harvesting of these public endpoints is authorised for this repository, and a decision on whether the harvest may be committed to the repository or must be cached outside it (licence/terms checks differ per OAM; the safest default is *cache outside the repository, commit only code + derived manifests with hashes*). |
| **Build effort** | High but bounded: an EDGAR harvester is a few hundred lines; a multi-jurisdiction OAM harvester is a few thousand and needs per-OAM parsing work. |
| **Fatal gap** | No prices. |

### Route (c) — Reduced-power open-data fallback

This is `research/data_manifest.md` §5 plus the price evidence gathered this
session.

| | |
|---|---|
| **Free price sources** | Stooq (free bulk ASCII daily, US 517 MB / UK 160 MB / world 185 MB; also carries FX and macro), Yahoo Finance (unofficial, unstable), Tiingo and Alpha Vantage (free tiers, rate-capped, non-redistributable terms). |
| **Measured survivorship gap** | An independent survey of these sources (checked 2026-07-18) found **no fully-free API is survivorship-free**: Yahoo and Alpaca serve no delisted names at all; **stooq free bulk covered only ~41% of a delisted cohort** (survivors 100%, but JCPenney, Heinz, Dean Foods, Big Lots, Avon, Safeway, Windstream and Molex were absent); Tiingo's free tier is partial from 2013 and misses Lehman/Enron/WorldCom. The same survey records that "clean delisted prices live only behind paid/gated products". |
| **Cheapest survivorship-clean alternative** | Sharadar / Nasdaq Data Link (~$30/month personal, CRSP-grade, point-in-time membership bundled), EODHD (~$20/month, delisted on all paid tiers, history from 1972 for Ford), HistoricalData.net (~$299 one-time, 50k+ delisted, 2003+), FMP (~$22–149/month, delisted API), MarketParquet ($79 one-time, US daily from 2000 with delisted symbols). CRSP/WRDS is institutional-only but free through a university seat. |
| **Free non-price data** | IFRS Foundation jurisdiction profiles (170 jurisdictions, with per-standard adoption status, "required for domestic public companies" vs "permitted but not required", and a separate IFRS filing-profile project giving filing timetables and taxonomy use) — this is the authoritative D7/D8 calendar and it is free. ECB reference rates for FX (D6). World Bank Worldwide Governance Indicators for enforcement (D10), with the caveat that WGI is annual and subject to revision, so it is a *revised* rather than strictly point-in-time series. |
| **Fatal gap** | With free prices only, the sample is survivorship-filtered, and hypothesis kill condition 9 fires by construction. |

---

## 4. Why the three routes cannot be chosen by picking one

R1 (prices with delisted names) and R2/R3 (acceptance timestamps and the filing
as published) are supplied by **different classes of source**. The licensed route
supplies R1 well and R3 badly and not at all R2. The public route supplies R2, R3
and R4 and not R1. This is a structural fact, not a preference, and it is why the
recommendation below names a spine and one paid dependency rather than a single
vendor.

It also explains why the previous session's blocker was not solvable by "getting
CRSP": a CRSP licence alone would still leave T-R — the frozen primary entry
timestamp — undefined, and the frozen specification's benchmark window is
anchored on T-R.

---

## 5. The finding that outranks the data route: the frozen design has an empty treatment group

This must be stated before any data is bought, because it changes what the data
would be bought *for*.

`research/specification_v1.md` §3 defines the treatment group as:

> **Treatment.** *First-time adopters of the standard*: firms whose reporting
> framework changed at the event (local GAAP → IFRS 15/16/9, or US GAAP →
> ASC 606/842).

Applied to the frozen universe in §5 of the same file ("EU regulated markets, UK
(LSE), and EEA-equivalent listings plus US listings for the secondary panel"):

| Panel | Framework before → after | Framework change? |
|---|---|---|
| EU, IFRS 15 (2018), IFRS 9 (2018), IFRS 16 (2019) | IFRS (adopted by the EU since 2005) → IFRS | **No.** Content change only. |
| UK, IFRS 15 (2016), IFRS 9 (2018), IFRS 16 (2019) | UK-adopted IFRS → UK-adopted IFRS | **No.** Content change only. |
| US, ASC 606 (FY2018), ASC 842 (FY2019) | US GAAP → US GAAP | **No.** ASC 606 and ASC 842 are *inside* US GAAP; the framework did not change. |

So the frozen treatment group has **zero firms** across the entire frozen
universe, and the frozen primary estimand ("difference in mean buy-and-hold
abnormal return over [T-R, T-R+20] between the low-information-quality and
high-information-quality **treatment groups**") is undefined. No data route can
repair this: it is a definitional collision inside the frozen artefacts, not an
acquisition problem.

The two readings that are *not* the parenthetical both have their own problems:

1. **"First-time adopter of the standard content"** (a firm whose *first* report
   under IFRS 15 is the transition report). This is non-empty, but then in the
   EU and the UK essentially *every* filer is a first-time adopter of IFRS 15 in
   FY2018, and the control group ("repeat adopters of the standard content")
   is empty. The only documented within-jurisdiction coexistence in the frozen
   universe is the **UK early-adoption cohort** (early application of IFRS 15 for
   periods beginning on/after 1 January 2015 and IFRS 16 for periods beginning
   on/after 1 January 2018, against mandatory application a year later). That
   cohort is small, voluntary, self-selected, and mechanically correlated with
   the firm-level information-quality state the design wants to condition on.
2. **A first-time *framework* adopter** (local GAAP → IFRS in the IFRS 15/16
   era). This is non-empty only in jurisdictions that moved to IFRS *after*
   2014 — Turkey, Saudi Arabia, Pakistan, Croatia, Egypt, and similar — and those
   jurisdictions are (a) outside the frozen universe, and (b) all-firm switches,
   which removes the within-jurisdiction control by construction.

**This is not a new finding invented here.** The canonical hypothesis-factory
dossier, retrieved read-only in this session at commit
`1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff` (see §7), reaches the same place from
the other direction and is *more* restrictive than this document:

- V-009 **Cycle-56 amendment**, item 3: the within-jurisdiction early-versus-
  mandatory contrast is **rejected as an identification** — the treatment arm is
  voluntary and self-selected, the effective sample is the number of early
  adopters, and the early arm announces its statements together with their
  effect, so "the diffusion clock has no window to run".
- V-009 **Cycle-56 amendment**, item 1, and the **Cycle-111 correction notice**:
  the group A (first-time adopters) / group B (second-time adopters) partition
  **must not be built**, because the published endorsement instruments converge
  on one mandatory application date and "first-time adopters apply IFRS as a
  single package" — the contrast degenerates into the historical first-time-
  versus-second-time comparison the literature has already populated.
- The **Cycle-110 resolution (R-058)**: the firm-level "repeat adopter" flag is
  **not published prospectively** (the IASB's 2005 early-adopter list could not be
  located); it remains derivable only from each firm's own prior-year basis-of-
  preparation note. So the treatment assignment must be constructed from filings,
  and it must be **pre-registered** as a construction.

**Consequence.** The frozen specification must not be executed as written, and it
must not be edited in place. The protocol requires a new registered version
(`research/prompt_changelog.md`; `research/specification_v1.md` v1.0 is immutable).
This is a mandatory stop condition, not a preference, and it is the next
session's first task. Any data purchased before that registration is bought
against a design that cannot be executed.

**What the factory dossier does say is available, and what it changes here:**

- The G-21 comparator — first-time versus second-time adopter drift — is
  **unrun by the field** after three search cycles, and the field's largest
  comparability study is first-adopter *by construction* without covering drift.
  A null in that design is a **contribution, not a replication** (V-009 Cycle-58
  amendment, item 3). This is the strongest reason the campaign is worth
  continuing at all, and it is *more* favourable to the campaign than this
  repository's own prior assessment recorded.
- **Enforcement quality and linguistic distance are mandatory controls** (V-009
  Cycle-52 amendment, item 2; Cycle-113 amendment, item 1). The frozen
  specification currently treats enforcement quality as an *optional competing
  conditioner* to be interacted with (`research/specification_v1.md` §3), which
  would present a published effect as the campaign's own. That is a divergence
  that a v1.1 registration must close.
- The claim must be pre-registered as a **transition-window** effect, with
  steady-state comparability results reported as a descriptive control (V-009
  Cycle-58 amendment, item 2). The frozen specification is already a
  transition-window design, so this is consistent — but it should be stated
  explicitly in v1.1.
- The canonical dossier has **moved to the IFRS 18 window** (mandatory for
  annual periods beginning on or after 1 January 2027) and has *closed* the
  IFRS 18 instance of the G-21 comparator, retaining only a "prospective arm A"
  built on the IAS 8 paragraphs 30–31 pre-adoption impact disclosure — whose
  measured quantification rate is **0 of 13** in the filed 2026 sample, and which
  the dossier therefore judges **not runnable on current evidence**. This
  repository's frozen panel (IFRS 15/16/9 and ASC 606/842) is *historical* and
  is not the instance the factory closed, but the closing logic (a single
  package, one mandatory date) applies to the retrospective instance as well and
  must be confronted in v1.1.

---

## 6. Recommendation

### 6.1 The recommended route

**Recommended: Route (b) — the regulator/issuer public-filing route — as the
spine, with a survivorship-clean market-data subscription for prices (R1) as its
one paid dependency.**

Concretely, the route is:

| Need | Source | Access |
|---|---|---|
| D7/D8 event calendar (R4) | IFRS Foundation jurisdiction profiles (170 jurisdictions, per-standard adoption status) + EUR-Lex Commission Regulations + EFRAG endorsement status reports + FASB ASU pages + national regulators | Free, public, primary. **Already started**: `research/event_calendar.csv`. |
| D2 filing acceptance timestamps (R2) | SEC EDGAR (`Accepted`, ET → UTC, parsed from the SGML header); FCA NSM/RNS for the UK; national OAMs (KAP, Tadawul/CMA, HKEX, CNINFO, MOPS) for the rest of the panel | Free, public. Requires a per-OAM verification pass on whether a *time* (not just a date) is published and on its timezone. |
| D3 accounting items as originally published (R3) | EDGAR complete submission text files and XBRL; ESEF iXBRL filings via national OAMs | Free, public. Archive the original filing; never substitute a normalised restated series. |
| D1 daily prices with delisted securities (R1) | **Sharadar / Nasdaq Data Link** (~$30/month) for US, plus **EODHD** (~$20/month) for UK and selected EU venues; or CRSP Global + Compustat if a university/institutional seat exists | **Paid — requires authorisation.** |
| D4 identifier history | Derived from the same sources plus exchange/security-master crosswalks | Free |
| D5 corporate actions | Vendor (with the price source) or exchange announcements | Paid / free per venue |
| D6 FX | ECB reference rates (frankfurter / ECB SDW) | Free |
| D9 analyst forecasts | I/B/E/S or equivalent | **Licensed — treat as unavailable**; the frozen specification already marks analyst-coverage matching and analyst disagreement as conditional on licence availability (`research/specification_v1.md` §3), so the design must be executable without them. |
| D10 enforcement proxies | World Bank WGI regulatory-quality series (annual; revision caveat) | Free |

### 6.2 Why this route and not the others

- It is the only route that can supply **T-R**, which the frozen benchmark window
  and the whole H-B design are anchored on. Buying a price feed without it does
  not unblock the test.
- It is the only route that supplies the **filing as published**, which the
  frozen information-quality proxy requires and which a normalised vendor feed
  silently violates.
- It is the route that makes the **affected-firm list knowable ex ante**, which
  the canonical dossier names as "the binding data constraint" (V-009, Ambiguity
  item 6).
- Its only paid component is small and specific (~$50/month at retail tiers) and
  is aimed at the one requirement that cannot be met for free.

### 6.3 Power consequences of the recommended route

These are stated **before** any estimation, as `research/preregistration.md` §6
requires, and they are stated against a v1.1-registered design, because the frozen
v1.0 design has no treatment group to power (§5 above).

| Quantity | Value under the recommended route |
|---|---|
| Independent clusters (standard × jurisdiction × adoption year) | ≈ 20–30 across IFRS 15/9/16 in the EU, UK, Turkey, Saudi Arabia, Pakistan, Croatia, Egypt, Hong Kong, Australia, Singapore, Canada, plus ASC 606/842 in the US. **Meets the ≥12 pre-registered minimum.** |
| Treatment firms | The first-time-framework-adopter jurisdictions alone (Turkey ~500 listed, Pakistan ~550, Saudi Arabia ~250, Croatia ~90) plausibly clear the ≥200 pre-registered minimum — but only if the v1.1 design puts them in scope, and only if prices for those venues are obtainable. |
| Minimum detectable effect | Unchanged from the preregistration: with 12 clusters the design is powered (80%) only for ≈0.5–0.7% per event. Below that, the honest conclusion is **inconclusive**, not null. |
| Effect of a survivorship-biased price panel | **Biases the estimate against the hypothesis.** The firms the hypothesis predicts the effect in are the low-information-quality, small, illiquid ones — precisely the names most likely to be missing from a survivors-only price panel (measured gap: 41% of a delisted cohort missing on stooq free). The fallback is therefore *not* a neutral reduction in power; it is a systematic erosion of the treatment arm. |

### 6.4 The fallback, if the paid price source is refused (Route (c) scoping)

Scoped concretely, as `research/data_manifest.md` §5 requires:

- **Jurisdictions:** US (EDGAR, free) + UK (FCA NSM, free) + EU-27 treated as a
  single cluster per standard (national OAMs, free). No non-US/UK venue prices
  are available for free without survivorship bias.
- **Standards:** ASC 606 (first affected FY beginning after 15 December 2017),
  ASC 842 (FY beginning after 15 December 2018), IFRS 15 (1 January 2018), IFRS 9
  (1 January 2018), IFRS 16 (1 January 2019).
- **Independent events:** 3 (US) + 3 (UK) + 3 (EU) = **9**, which is **below the
  pre-registered minimum of 12**. The primary estimand is therefore
  **inconclusive by construction** — the preregistration's own precedent
  (`research/preregistration.md` §4: a holdout with fewer than 4 independent
  events is inconclusive by construction) extends to the primary panel here.
- **Conclusions that remain reachable:** (i) a *descriptive* transition-window
  abnormal-return path, reported and explicitly not claimed; (ii) the **H-A
  anticipation check**, which is the highest-value reachable result and needs
  prices only for a survivor-filtered sample, with the bias stated;
  (iii) the **H-C / PEAD** secondary; and (iv) a **direction-and-magnitude
  replication** of the published conflict in this family — S-179 (Song & Woo
  2015, K-IFRS adoption *reduced* PEAD in Korea) versus S-188 (Forbes &
  Giannopoulos 2015, IFRS adoption *increased* PEAD in Greece) — extended to
  the transition-window outcome the field has not tested. This last item is a
  genuine contribution at reduced power and is the most defensible thing the
  fallback can deliver.
- **Conclusions that do NOT remain reachable:** any promotion claim (protocol
  gate 2 requires point-in-time data lineage, gate 7 requires an independent
  reproduction, and kill condition 9 fires); any statement that the effect exists
  or does not exist; any portfolio-level net return claim (a survivor-filtered
  cost estimate is not an institutional cost estimate).

### 6.5 Exact authorisation requested

> **Status as of 2026-10-22 (re-checked in the v1.1 registration session):** item **3**
> (design registration) has been **carried out** — v1.1 exists and is registered — but
> it remains an item on the list because a maintainer confirmation is still required
> for any **scope** change to the registered panel. Item **4** (scope ruling) has been
> **superseded by the registered panel rule** in `research/specification_v1.1.md` §1.1
> and is now reduced to a confirmation (authorisation item A4). Items **1** and **2** are
> **still entirely outstanding**. The full, operational form of this list, with the
> trigger sequence that runs once an answer is received, is
> **`research/data_acquisition_plan.md` §8**.

From the maintainer, one of the following, plus two design decisions:

1. **Market data (preferred):** authorisation to subscribe to **Sharadar / Nasdaq
   Data Link** (~$30/month) and **EODHD** (~$20/month) for daily prices including
   delisted securities, **or** a CRSP Global + Compustat / WRDS institutional
   seat if the maintainer has one. Budget: ~$50/month retail, or an existing
   institutional entitlement. Explicitly: this is a paid data pull and therefore
   needs the protocol's Authority item 4 authorisation. Alternative, no cost:
   a written instruction to run Route (c) with the §6.4 scope and its stated
   biases.
2. **Public harvesting:** confirmation that read-only harvesting of SEC EDGAR,
   the FCA National Storage Mechanism, ESMA ESEF filings and the national OAMs
   named in §6.1 is authorised for this repository, and a ruling on whether
   harvested files may be committed to the repository (default: **no** — cache
   outside the repository, commit only code, manifests and hashes).
3. **Design registration (blocking, no cost):** authorisation to register
   `research/specification_v1.md` **v1.1** and `research/hypothesis.md` **v1.1**
   with (a) an implementable treatment definition, (b) the mandatory enforcement
   and linguistic-distance controls, (c) the pre-registered transition-window
   claim, and (d) the jurisdiction panel — and to open `research/preregistration.md`
   **v1.1** with the revised split and cluster counts. This must happen *before*
   any outcome-period return is computed, and it is the only way the campaign
   proceeds without falsifying its own pre-registration.
4. **Scope ruling (blocking, no cost):** a decision on whether the panel is
   restricted to the frozen universe (EU/UK/US) — in which case the treatment
   group is empty under reading (1) and the design must use a different
   treatment definition — or extended to the first-time-framework-adopter
   jurisdictions (Turkey, Saudi Arabia, Pakistan, Croatia, Egypt), which requires
   price coverage for those venues and therefore decision 1.

---

## 7. Provenance of the sources used in this assessment

| Source | Type | Retrieved | Used for |
|---|---|---|---|
| `https://www.sec.gov/about/webmaster-frequently-asked-questions` | Regulator (primary) | 2026-10-22 | EDGAR `Accepted` definition, EST, and the explicit "no public-availability timestamp" caveat |
| `https://www.sec.gov/files/edgar/pds_dissemination_spec.pdf` | Regulator technical specification (primary) | 2026-10-22 | Acceptance Date / Acceptance Time (EST) field definitions |
| `https://api.crossref.org/...` (not used) | — | — | — |
| `https://www.ifrs.org/use-around-the-world/use-of-ifrs-standards-by-jurisdiction/` | Standard setter (primary) | 2026-10-22 | Jurisdiction profiles, 170 jurisdictions, per-standard adoption status, filing-profile project |
| `https://stooq.com/db/h/` | Data vendor (primary, own catalogue) | 2026-10-22 | Free bulk coverage by market (US/UK/world daily, FX, macro) |
| `https://unisona.ai/repo/docs/research/2026-07-18-market-data-vendors-survivorship.md` | Third-party research note (**secondary**, independent) | 2026-10-22 | Measured survivorship gaps in free price sources; price of the survivorship-clean retail tiers |
| `https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/free-equity-apis.html` | Third-party teaching note (**secondary**) | 2026-10-22 | Free price source coverage and licence caveats; adjustment quirks |
| `https://iangow.github.io/sec_submissions/timestamps/` | Third-party analysis (**secondary**) | 2026-10-22 | Evidence that the EDGAR submissions JSON mixes UTC and Eastern acceptance times |
| `https://eur-lex.europa.eu/...` CELEX 32016R1905, 32016R2067, 32017R1986 | EU Official Journal (primary) | 2026-10-22 | IFRS 15/9/16 endorsement dates, effective dates, OJ publication and entry into force |
| Hypothesis-factory dossier `takenthatusernameis-collab/QUANTITATIVE-HYPOTHESIS-FACTORY` @ `1f9bd09cc96c1953f67ffc1f9892f7e60b6a71ff`, `research/validation_handoffs.md` (V-009) | Canonical dossier (primary for this campaign) | 2026-10-22 | Binding constraints and amendments quoted in §5 |

Nothing in this document is a result about the hypothesis. No outcome-period
return was computed, inspected, or simulated in this session.

---

## 8. Re-check after the v1.1 registration (2026-10-22)

This section records what changed in the data route as a consequence of the v1.1
registration, and what did not.

### 8.1 What the v1.1 design changed in the data requirements

| v1.0 requirement | v1.1 requirement | Effect on the route |
|---|---|---|
| Prices for the EU/UK/US universe only | Prices for the **registered panel**, including the Stratum B first-time-framework-adopter venues, **and** for the matched **not-yet-treated control jurisdictions** | The price source must cover **control** jurisdictions as well as treated ones. A source that covers only the treated venues is not sufficient. This widens the requirement stated in §6.1 without changing its price. |
| T-R as the entry timestamp | **T-A** as the entry timestamp, **T-R** as the exit, and **T-RI** as the pre-emption timestamp | **Unchanged in kind**: the public-filing route is still the only source of all three, and the paid price feed still does not supply any of them. The route recommendation of D-010 stands. |
| The affected-firm list for the EU/UK/US | The affected-firm list for the **registered panel**, plus each jurisdiction's own scope rule | The IFRS Foundation jurisdiction profiles (S-47) move from "a calendar source" to the **panel membership authority**. Still free and primary. |
| "Firms whose reporting framework changed" | Firms in the jurisdiction's affected-firm list applying the standard from T-E | The affected-firm list becomes **ex-ante knowable** for the first time in this campaign's history. This is the requirement that was previously unmet, and it is now met **by design**, not by data. |
| — | **Restated comparatives** inside the first report under the standard (the mechanical accounting-change magnitude, CH-2) | Still supplied by the public-filing route; it adds no new source requirement. |
| — | Enforcement quality (WGI) and the linguistic-distance measure | **Free**, non-blocking, but **mandatory**: the design is not executable without them. Their assembly is now on the critical path. |

### 8.2 What did not change

- **The route recommendation stands.** The regulator/issuer filing route remains the
  spine, and the survivorship-clean price subscription remains its one paid dependency
  (D-010). No new paid dependency was introduced by v1.1.
- **The fallback stands and is now precisely quantified.** Under the v1.1 design the
  fallback panel is **US + UK + EU-27**, giving **≈ 8 independent clusters** (the EU is
  one application cohort per standard because all member states share one application
  date), which is **below the ≥12 minimum**. The primary estimand is therefore
  **inconclusive by construction** — a rule now frozen in
  `research/preregistration_v1.1.md` §5.3 rather than asserted after the fact.
  The reachable results under the fallback are the descriptive event-study path, the
  announcement/anticipation check, the pre-emption window, the H-C / PEAD secondary, and
  the direction-and-magnitude replication of the published conflict between S-35 and
  S-36.
- **No authorisation has been received.** Items A1 (market data) and A2 (public
  harvesting) are entirely outstanding; A3 (repository policy), A4 (panel scope) and
  A5 (prospective holdout) await confirmation. The trigger sequence is in
  `research/data_acquisition_plan.md` §8.2.
- **No paid data pull, no GitHub Actions run and no workflow edit** occurred in this
  session.

### 8.3 One new, named verification dependency

v1.1 pins the **adoption announcement clock** to the jurisdiction's legal adoption
instrument, with the standard-setter issuance date as a secondary window. Two
verification gaps follow, both already recorded in `research/event_calendar.csv` and
both now **on the critical path** rather than incidental:

1. **EV-201 / EV-202 — the day-level UK endorsement instrument date** for IFRS 15 and
   IFRS 16. Without it the UK rows cannot enter the registered panel with a
   primary-verified T-A.
2. **EV-103 — the day-level ASU 2016-01 issuance date** in the United States.

Both are free to fetch and are part of the §6.4 acquisition specification.

### 8.4 A note on the dossier's own instance

The canonical dossier's live instance is **IFRS 18**, and its prospective arm A is
**not runnable on current evidence** (the 2026 season's quantification rate is 0 of 13
on a convenience sample; the ESMA-supervised population rate is not yet published —
S-49, S-50, S-51). v1.1 therefore **does not use arm A**, and instead registers its
retrospective analogue: the **pre-emption window** around the first disclosure of the
accounting break at the firm's first interim report under the standard
(`research/specification_v1.1.md` §4.3). The retrospective standards carried **no
mandated pre-adoption impact disclosure**, so the structural pre-emption channel that
dominates the IFRS 18 instance is **absent** from the v1.1 panel — a difference that is
registered so that the pre-emption arm is evaluated on its own merits rather than
assumed to have fired.


## 9. Current route decision D-031 (2026-10-22) — supersedes the old fallback recommendation

**Current direction:** paid providers are selected to address the price-history bottleneck. The earlier §6.5 recommendation and §8.2 free fallback remain as historical analysis, but do not cause the agent to ask for A1–A5 again.

- **US active/delisted daily prices:** Sharadar Stock Prices / SEP. The vendor documents active and delisted US stock coverage and history to December 1997: https://sharadar.com/docs/stocks. API access is described at https://sharadar.com/docs/auth.
- **International and controls:** EODHD All World historical EOD. Current public plan page lists US$19.99/month for the personal All World EOD plan; verify exact symbol/venue/delisted coverage and checkout terms before purchase: https://eodhd.com/pricing and https://eodhd.com/financial-apis/api-for-historical-data-and-volumes. EODHD's delisted endpoint documents its per-exchange delisted-symbol workflow: https://eodhd.com/financial-apis/delisted-stock-companies-data-2.
- **Existing institutional access:** test for an already-held CRSP/WRDS entitlement only where available; do not assume one or create new accounts to check it.
- **Spend boundary:** route selected is not a purchase authorization. No agent may enter payment details, start a subscription, accept contract terms, silently select an annual plan, or incur unspecified charges. The account holder must provision plan access and credentials. The prior ~$30/month Sharadar estimate is provisional; the combined ~$50/month estimate is not a current verified quote.
- **Implementation:** scripts/price_provider_client.py and tests/test_price_provider_client.py provide a guarded, offline-testable adapter. The paid fetch flag must be explicitly enabled and credentials must be injected from the execution environment, not chat/Git. Manifests redact credentials; raw data stays outside Git.
- **Acceptance, not assumption:** for both treated and not-yet-treated control jurisdictions, verify inactive/delisted securities, ticker changes, split/dividend adjustments, coverage, original dates, and terminal/delisting-return semantics. An adjusted-close series is not proof of a CRSP-style delisting return. If that gap cannot be solved under an auditable rule, fail the primary price gate rather than drop securities or impute zero.
- **Work in parallel:** public source/filing collection is authorized read-only under published terms and rate limits and should proceed without waiting for paid credentials.
- **Frozen inference:** the minimum of 12 independent adoption clusters and 200 treatment firms remains fixed. PH-1 is still expected at roughly 4–8 clusters, so it remains likely inconclusive unless the pre-outcome feasibility audit actually passes. No return analysis before the audit; no threshold lowering, no treating EU-27 as 27 independent cohorts, and no edits to frozen preregistration files.
- **Current state:** route selected and code added, but no provider credentials, paid request, purchase, bulk filing harvest, backtest or outcome-return inspection occurred in this update. Strategy remains **PARKED — not validated, not rejected**.

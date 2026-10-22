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

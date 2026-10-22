# ACCTCLOCK — maintainer authorisation request

**Status: OPEN. No authorisation has been received.**
Raised: 2026-10-22. Last touched: 2026-10-22 (session 5).
The authoritative list is `research/data_acquisition_plan.md` §8.1; this file is the
one-click-able form of that list. Every quote below is verbatim from §8.1.

**One line.** The campaign cannot compute anything until the maintainer answers
**A1** and **A2**. **A2 is zero-cost and highest-value.**

---

## A1 — Market data  *(entirely outstanding)*

> **Options.** (a) authorise **Sharadar/Nasdaq Data Link** (~$30/mo) + **EODHD**
> (~$20/mo); (b) point the pipeline at an existing **CRSP/WRDS** entitlement;
> (c) no paid data.
>
> **Consequence if refused or unanswered.** (a)/(b) unblock the full v1.1 design.
> (c) leaves the panel at **≈ 8 clusters**, below the ≥12 minimum → **inconclusive
> by construction**, and the survivorship-filtered price panel fires **kill
> condition 9** by construction, with a bias *against* the hypothesis (the
> low-information-quality arm is disproportionately dropped).

**Answer needed:** (a), (b) or (c). If (b), name the entitlement and its vintage
coverage; the panel's jurisdictions are outside the EU/UK/US and a US-only
entitlement does not cover them.

## A2 — Public harvesting  *(entirely outstanding)*

> **Options.** authorise read-only harvesting of **SEC EDGAR**, **FCA NSM/RNS**, the
> named **national OAMs**, **EUR-Lex**, the **IFRS Foundation** profiles, the
> **FASB** pages, **ECB FX**, **World Bank WGI**.
>
> **Consequence if refused or unanswered.** **Highest-value and zero-cost.** Without
> it there is no T-R, no T-RI, no state variable and no restated comparative, and
> the test cannot start at all.

**Answer needed:** yes / no, and if yes, whether it is unconditional or limited to a
named subset of the list.

## A3 — Repository policy for harvested files

> **Options.** (a) default — cache outside the repository, commit only code,
> manifests and hashes; (b) a named-source exception.
>
> **Consequence if refused or unanswered.** The default (a) is already in force
> (D-015). (b) requires a per-source ruling recorded as a new decision.

**Answer needed:** confirm (a), or name the source and the exception. Nothing is
waiting on this; (a) is the working default.

## A4 — Panel scope confirmation

> **Options.** (a) confirm the registered panel rule; (b) restrict to Stratum A
> only; (c) the frozen EU/UK/US universe.
>
> **Consequence if refused or unanswered.** (b) gives ≈ 8 clusters → **inconclusive
> by construction**. (c) is **not executable** (D-009). The panel is registered by
> rule and **must not be narrowed after the feasibility audit begins** (D-016).

**Answer needed:** (a), (b) or (c).
**Note.** `research/panel_v1.1.csv` now exists: 434 rows — 8 complete Stratum A
events and 426 Stratum B candidate rows derived by rule from the dated IFRS
Foundation profile snapshot of 2026-10-22. The Stratum B rows carry
`in_registered_panel = pending`, because three of the five conditions of the rule
(a day-level legal instrument, a filing route publishing an acceptance *timestamp*,
and price coverage) cannot be verified until A1 and A2 land. **A4 (a) is needed to
convert those rows to true or false before the feasibility audit begins**, which is
the point at which the rule becomes binding.

## A5 — Prospective holdout

> **Options.** confirm that **PH-1** may be registered as v1.2 before the first
> IFRS 18 report is published.
>
> **Consequence if refused or unanswered.** Without PH-1 the campaign has **no
> promotable test at all**, only an evidential one.

**Answer needed:** yes / no.
**Note.** `research/hypothesis_v1.2.md`, `research/specification_v1.2.md` and
`research/preregistration_v1.2.md` are now **written and registered** (2026-10-22),
ahead of the first IFRS 18 report in the 2027 interim reporting season. The
registration is in place; the confirmation is still required for the arm to be
*run* under the protocol's promotion gate. A further **v1.3** was registered the
same day (D-029), which admits Saudi Arabia on a uniform T-PRE interval rule and
restates the cluster arithmetic as **≈ 4–8** cohorts — still below the ≥12
minimum, so the arm is expected to be inconclusive by construction whatever A1
and A2 return.

---

## The consequence of silence, stated plainly

1. The panel stays at **≈ 8 clusters** (Stratum A only), **below the ≥12 minimum**,
   and the primary estimand is **inconclusive by construction** — not "no effect",
   but "cannot be estimated".
2. **Kill condition 9 fires by construction**, because the survivorship-filtered
   price panel drops the low-information-quality arm disproportionately. The bias
   runs **against** the hypothesis, so a parked campaign under A1(c) is not a
   neutral outcome.
3. The campaign remains **PARKED — not validated, not rejected**, with **no
   outcome-period return ever computed or inspected**.

## What has *already* been done without authorisation

So that the request is honest about the state of the repository, everything below
was built and verified **offline**, with **no paid data pull**, **no filing-archive
harvest**, and **no GitHub Actions run**:

- the SEC EDGAR acquirer, the SGML acceptance-time parser, the manifest writer and
  the cache layout are **implemented and unit-tested** (`scripts/sec_edgar.py`,
  `scripts/sec_acceptance.py`, `scripts/data_manifest.py`, `scripts/data_cache.py`;
  48 new tests, 115 in total, all passing);
- the two named date gaps are **closed** from primary sources (EV-103, EV-201,
  and the missing EV-202 row added);
- `research/panel_v1.1.csv` is **materialised**;
- v1.2 is **registered** for PH-1.

## When an answer arrives

Record it as a new decision (**D-017** onward) in `research/decision_log.md`,
quoting the maintainer's instruction with its date and its exact scope, then run
the trigger sequence in `research/data_acquisition_plan.md` §8.2.

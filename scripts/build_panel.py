"""Builder for the PH-1 panel file, ``research/panel_v1.2.csv``.

The PH-1 arm is the prospective holdout on the IFRS 18 first-application window
(``research/specification_v1.2.md`` §1). Its panel membership rule has five
conditions, checked in order, and every check is recorded:

1. ``s = IFRS 18``;
2. the jurisdiction's regulator has published a **legal instrument making IFRS 18
   mandatory** for a class of listed firms, with a **day-level** date;
3. the affected-firm list is knowable **ex ante** from the IFRS Foundation
   jurisdiction profiles or the jurisdiction's own published scope rule;
4. the jurisdiction has a public filing route that publishes a **filing
   acceptance time** (a timestamp, not only a date);
5. point-in-time price coverage exists, including for delisted firms.

**Conditions 3 to 5 are unverified for every jurisdiction**, because condition 3
depends on the membership snapshot, condition 4 on the A2 authorisation and
condition 5 on the A1 authorisation. **Condition 2 is verified for ten
jurisdictions** (European Union, United Kingdom, Saudi Arabia, Singapore,
Brazil, New Zealand, Malaysia, Hong Kong SAR, Indonesia, Philippines). Every row
therefore carries ``in_registered_panel = pending``, which is the three-state
discipline of ``research/specification_v1.1.md`` §4.2: ``true`` / ``false`` /
``pending``.

The candidate universe is taken from the **same dated, hashed membership
snapshot** that produced ``research/panel_v1.1.csv`` — the Stratum B rows of that
file, which are themselves derived from
``research/manifests/ifrs_jurisdiction_profiles.jsonl`` (S-58). Both panel files
are therefore built from **one vintage**, as the handoff requires.

The verified instruments are **primary sources**, quoted in
``research/decision_log.md`` (D-022 and D-026):

* **European Union** — Commission Regulation (EU) 2026/338; date of endorsement
  **2026-02-13**, date of publication in the Official Journal **2026-02-16**;
  application for financial years beginning on or after 2027-01-01.
* **United Kingdom** — the UK Endorsement Board formally adopted IFRS 18 for use
  in the UK on **2025-12-10**; the adopted text and the Adoption Statement were
  published on 2025-12-12; application for annual reporting periods beginning on
  or after 2027-01-01.
* **Saudi Arabia** — the Saudi Organization for Chartered and Professional
  Accountants (SOCPA) adopted IFRS 18 for application in the Kingdom on
  **2024-12-26** (Accounting Standards Council resolution 25/06/1446H). The
  Capital Market Authority announcement CMA_N_4083 of **2026-06-30** is the
  Board's decision on **early adoption** during 2026, not the instrument making
  IFRS 18 mandatory. Both dates are recorded and the conflict is written into the
  row's own ``date_conflict`` field; it is never silently resolved (D-011).
* **Singapore** — the Accounting Standards Committee of ACRA issued **SFRS(I) 18**
  on **2024-10-04**, applying to annual reporting periods beginning on or after
  2027-01-01; listed issuers apply SFRS(I) under the SGX Mainboard Rulebook.
* **Brazil** — **Resolucao CVM no 237, de 23 de dezembro de 2025**, whose Article 1
  makes CPC 51 (aligned to IFRS 18) mandatory for the listed companies and whose
  Article 3 brings it into force on 2027-01-01.
* **New Zealand** — **NZ IFRS 18**, issued on **2024-05-23** by the NZ Accounting
  Standards Board under section 12(a) of the Financial Reporting Act 2013;
  mandatory date 2027-01-01.
* **Philippines** — **PFRS 18**, adopted by the Financial and Sustainability
  Reporting Standards Council on **2024-05-10**; the Philippine Accounting
  Standards are prescribed for listed companies by the Securities and Exchange
  Commission under SRC Rule 68.
* **Malaysia** — **MFRS 18**, issued on **2024-06-14** by notice of the Malaysian
  Accounting Standards Board under subsection 7(1) of the Financial Reporting Act
  1997 and regulation 3 of the Financial Reporting (Publication of Approved
  Accounting Standards) Regulations 1999; mandatory date 2027-01-01.
* **Hong Kong SAR** — **HKFRS 18**, issued on **2024-07-09** by the HKICPA's
  Financial Reporting Standards Committee; mandatory date 2027-01-01.
* **Indonesia** — **PSAK 118**, ratified on **2025-05-28** by the Indonesian
  Accounting Standards Board (DSAK IAI) as the Indonesian equivalent of IFRS 18;
  mandatory date 2027-01-01.

**Pakistan, Sri Lanka and Thailand are recorded as *attempted and not verified*,
not as verified.** Pakistan's SECP issued S.R.O. 2444(I)/2025 of 2025-12-12
notifying IFRS 18, but every path on ``secp.gov.pk`` answers **HTTP 403** from
this environment, so the instrument itself could not be read and the date is not
tied to a primary source at day level; it therefore stays empty under D-011.
Sri Lanka's Institute of Chartered Accountants lists SLFRS 18 among its 2025
standards, but no day-level issuance date was located. Thailand's TFAC page is
primary-verified for the *effective date* — TFRS 18 applies to periods beginning
on or after **1 January B.E. 2571 (1 January 2028)** — but its announcement
column is empty in the retrieved rendering and the Thai text of the standard
itself is not machine-extractable here, so no day-level T-A was pinned; the
distinct application date is recorded because it puts Thailand **outside** the
arm's 2027-01-01 first-application window.

**The route columns are triage, not membership.** ``profile_route_hint`` reads the
*reporting framework* recorded in the IFRS Foundation jurisdiction profile and
``timing_cohort`` records the cohort a row would join if it is admitted. Neither
is a determination, and the panel's own data contains the counterexample that
proves it: Brazil's profile says only "Required." yet the CVM issued a dated
IFRS 18 resolution; Saudi Arabia's profile records the IFRS Accounting Standards
yet SOCPA issued a dated adoption resolution; South Korea's profile records
"adopted IFRS Accounting Standards" yet the KASB issued K-IFRS 1118. A
standing-reference profile therefore does **not** exclude a jurisdiction from
having its own dated instrument, and no jurisdiction is excluded on this basis.

**South Africa and South Korea are recorded as *attempted and not verified*, not
as verified.** South Africa's route is incorporation by reference ("IFRS as issued
from time to time by the IASB"), which has no dated local instrument, so T-A is
left empty. South Korea's K-IFRS No. 1118 was established and announced in
December 2025, but no source consulted carries a day-level issuance date, so T-A
is left empty rather than inferred from the month. Both attempts are recorded in
``research/decision_log.md`` (D-026 and D-030) and in
``research/source_ledger.csv`` (S-73).

The builder is deterministic and takes no network access.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable

PANEL_COLUMNS: tuple[str, ...] = (
    "event_id",
    "standard_id",
    "jurisdiction",
    "stratum",
    "T_A",
    "T_E",
    "in_registered_panel",
    "date_conflict",
    "source_url",
    "filing_route",
    "affected_firm_scope_rule",
    "price_venue_set",
    "coverage_notes",
    "membership_screen",
    "profile_url",
    "profile_sha256",
    "profile_retrieved_utc",
    "profile_last_updated",
    "status_text",
)

#: The PH-1 panel file carries two **additive** evidence columns on top of the
#: retrospective panel's schema (``research/specification_v1.1.md`` §4.2). They
#: are evidence about the row, not new membership conditions:
#:
#: * ``profile_route_hint`` — the *reporting framework* the dated IFRS Foundation
#:   jurisdiction profile records for the jurisdiction, read by the fixed rule in
#:   :func:`classify_profile_route`. It is a **triage prior**: it says where to
#:   look for an IFRS 18 instrument, and it is **not** a determination of
#:   membership. The panel's own data carries the counterexamples that prove it
#:   (Brazil, Saudi Arabia and South Korea each have a dated national instrument
#:   although their profiles do not name a national equivalent).
#: * ``timing_cohort`` — the cohort the row would join if it were admitted: the
#:   verified T-A date, the EU cohort date for the member states that apply the
#:   EU-endorsed IFRS directly, or empty where no cohort is known yet.
PH1_EXTRA_COLUMNS: tuple[str, ...] = ("profile_route_hint", "timing_cohort")

PH1_COLUMNS: tuple[str, ...] = PANEL_COLUMNS + PH1_EXTRA_COLUMNS

#: The 27 member states of the European Union, as they are named in the dated
#: IFRS Foundation membership snapshot (S-58). The profile text is **identical**
#: for the 27 member states and for the three EEA/EFTA states that apply the
#: EU-endorsed IFRS (Norway, Iceland, Liechtenstein), so the two groups cannot be
#: told apart from the profile text and are told apart here, by name.
EU_MEMBER_STATES: frozenset[str] = frozenset(
    {
        "Austria",
        "Belgium",
        "Bulgaria",
        "Croatia",
        "Cyprus",
        "Czechia",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Germany",
        "Greece",
        "Hungary",
        "Ireland",
        "Italy",
        "Latvia",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Netherlands",
        "Poland",
        "Portugal",
        "Romania",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
    }
)

#: The EEA/EFTA states whose profile text is identical to the member states'
#: but whose route to the EU-endorsed IFRS runs through their **own**
#: incorporation instrument, so their T-A is a separate question.
EEA_EFTA_STATES: frozenset[str] = frozenset({"Iceland", "Liechtenstein", "Norway"})

#: The EU cohort's T-A: the date of endorsement of Commission Regulation (EU)
#: 2026/338 (S-60). Every member state applies the endorsed standard through it.
EU_COHORT_T_A = "2026-02-13"

#: Profile markers for a jurisdiction whose framework is a **national
#: equivalent** of the IFRS Accounting Standards rather than the IFRS Accounting
#: Standards as issued by the IASB. These are the jurisdictions that issue their
#: own dated standard-setter instrument and can therefore carry their own T-A.
NATIONAL_EQUIVALENT_MARKERS: tuple[str, ...] = (
    "mfrs",
    "pfrs",
    "tfrs",
    "sak indonesia",
    "psak",
    "hkfrs",
    "nz ifrs",
    "k-ifrs",
    "nfrs",
    "slfrs",
    "myanmar financial reporting standards",
    "thai financial reporting standards",
    "ifrs accounting standards as endorsed by the fsc",
)

#: Profile markers for a jurisdiction whose framework is the IFRS Accounting
#: Standards **as adopted by the European Union**.
EU_ADOPTED_MARKERS: tuple[str, ...] = ("as adopted by the eu",)

ROUTE_EU_MEMBER = "eu_member_state"
ROUTE_EEA_EFTA = "eea_efta_own_instrument"
ROUTE_NATIONAL_EQUIVALENT = "national_equivalent_profile"
ROUTE_STANDING_REFERENCE = "standing_reference_profile"
ROUTE_NO_STATUS_TEXT = "no_profile_status_text"

STANDARD_ID = "IFRS 18"
STRATUM = "A"
APPLICATION_DATE = "2027-01-01"

#: Jurisdictions whose condition 2 is verified from a primary instrument.
IFRS18_INSTRUMENTS: dict[str, dict[str, str]] = {
    "European Union": {
        "t_a": "2026-02-13",
        "date_conflict": (
            "Two EU dates, both primary-verified and both recorded, never conflated: the date of "
            "endorsement is 2026-02-13 and the date of publication in the Official Journal is "
            "2026-02-16 (EFRAG Endorsement Status Report, 16 February 2026; Commission Regulation "
            "(EU) 2026/338). T-A is the date of endorsement, 2026-02-13, because the v1.1 event "
            "clock defines T-A as the jurisdictional legal-adoption date, not the OJ publication "
            "date. The two differ by three days and the difference is material to a 60-day "
            "pre-adoption window."
        ),
        "source_url": "https://eur-lex.europa.eu/eli/reg/2026/338/oj",
        "coverage_notes": (
            "Condition 2 VERIFIED. Commission Regulation (EU) 2026/338 endorsing IFRS 18 "
            "Presentation and Disclosure in Financial Statements. Date of endorsement 2026-02-13; "
            "date of publication in the Official Journal 2026-02-16 (EFRAG Endorsement Status "
            "Report, 16 February 2026, and the EFRAG endorsement-status table; source ledger S-60). EU effective date "
            "2027-01-01. The EU is ONE timing cohort, not 27 independent clusters; that is stated "
            "in advance in research/preregistration_v1.2.md section 5.2 so it cannot be discovered "
            "later as a power surprise. Source ledger S-60. Conditions 3, 4 and 5 remain unverified."
        ),
    },
    "United Kingdom": {
        "t_a": "2025-12-10",
        "date_conflict": (
            "Two UK dates, both primary-verified and both recorded: the date the UK Endorsement "
            "Board formally adopted IFRS 18 for use in the UK is 2025-12-10, and the date the "
            "adopted text and the Adoption Statement were published is 2025-12-12. T-A is the "
            "adoption decision date, 2025-12-10, per the v1.1 event clock (T-A is the "
            "jurisdictional legal-adoption date)."
        ),
        "source_url": (
            "https://www.endorsement-board.uk/news-events/news/"
            "ukeb-adopts-ifrs-18-presentation-and-disclosure-in-financial-statements/"
        ),
        "coverage_notes": (
            "Condition 2 VERIFIED. The UK Endorsement Board formally adopted IFRS 18 for use in "
            "the UK on 2025-12-10 and published the standard and the Adoption Statement on "
            "2025-12-12; the UKEB project record shows Project Closure 2026-01-30 and an "
            "effective date of 2027-01-01. THIS CLOSES THE GAP LEFT OPEN AT REGISTRATION: "
            "research/specification_v1.2.md section 1.2 recorded the UK T-A as 'day-level decision "
            "date to be pinned from the UKEB's own decision record', and it is now pinned to "
            "2025-12-10 from that record. v1.2 is not edited in place; the pinned date is applied "
            "here and the change is logged as decision D-022 (source ledger S-63, S-69). Conditions 3, 4 and 5 remain "
            "unverified, and condition 4 is the open one for the UK: the FCA National Storage "
            "Mechanism publishes a filing DATE, not a time (decision D-021)."
        ),
    },
    "Singapore": {
        "t_a": "2024-10-04",
        "date_conflict": (
            "Two Singapore dates, both primary-verified and both recorded: the Accounting "
            "Standards Committee (ASC) of ACRA issued SFRS(I) 18 on 2024-10-04, and the standard "
            "applies to annual reporting periods beginning on or after 2027-01-01. T-A is the "
            "issuance date, 2024-10-04, because the v1.1 event clock defines T-A as the "
            "jurisdictional legal-adoption date. The ASC issued FRS 118 in the same announcement "
            "for entities that do not apply SFRS(I); the listed-company instrument is SFRS(I) 18, "
            "because the SGX Mainboard Rulebook requires listed issuers to apply SFRS(I)."
        ),
        "source_url": "https://www.acra.gov.sg/news-events/news-announcements/833/",
        "coverage_notes": (
            "Condition 2 VERIFIED. ACRA announcement of 2024-10-04: the Accounting Standards "
            "Committee issued SFRS(I) 18 Presentation and Disclosure in Financial Statements, "
            "applying to annual reporting periods beginning on or after 2027-01-01. Mandatory "
            "character: a standard-setter issuance given legal force by the Companies Act (Cap. 50) "
            "and the SGX Mainboard Rulebook, which require listed issuers to apply SFRS(I). "
            "Source ledger S-76. Conditions 3, 4 and 5 remain unverified: the SGX filing route's "
            "publication of an acceptance TIMESTAMP is not yet checked."
        ),
    },
    "Brazil": {
        "t_a": "2025-12-23",
        "date_conflict": (
            "Two Brazil dates, both primary-verified and both recorded: Resolucao CVM no 237 is "
            "dated 23 December 2025, and the Resolution enters into force on 1 January 2027, "
            "applying to financial years beginning on or after that date. T-A is the publication "
            "date of the instrument, 2025-12-23. The earlier date of the CPC pronouncement itself "
            "(the Comite de Pronunciamentos Contabeis, a non-governmental body) is not T-A, because "
            "the Resolution is the instrument that makes it mandatory for listed companies."
        ),
        "source_url": (
            "https://conteudo.cvm.gov.br/legislacao/resolucoes/anexos/200/resol237.htm"
        ),
        "coverage_notes": (
            "Condition 2 VERIFIED. Resolucao CVM no 237, de 23 de dezembro de 2025, approves the "
            "Comite de Pronunciamentos Contabeis pronouncement CPC 51 (Presentation and Disclosure "
            "in Financial Statements, aligned to IFRS 18) and its Article 1 makes it mandatory for "
            "the 'companhias abertas' (listed companies); Article 3 brings it into force on 1 "
            "January 2027 for financial years beginning on or after that date. Mandatory "
            "character: a direct legal instrument of the securities regulator (CVM) under Lei "
            "6.404/1976 art. 177 and Lei 6.385/1976 art. 22. Source ledger S-77. Conditions 3, 4 "
            "and 5 remain unverified."
        ),
    },
    "New Zealand": {
        "t_a": "2024-05-23",
        "date_conflict": (
            "Two New Zealand dates, both primary-verified and both recorded: the NZ Accounting "
            "Standards Board of the External Reporting Board issued NZ IFRS 18 on 23 May 2024, "
            "and the instrument took effect (was gazetted as secondary legislation) on 20 June "
            "2024. T-A is the issuance date, 2024-05-23, because the v1.1 event clock defines "
            "T-A as the jurisdictional legal-adoption date. The XRB's own instrument page carries "
            "the month-level label 'May 2024'; the day comes from the standard's own text, which "
            "states that it was issued on 23 May 2024 pursuant to section 12(a) of the Financial "
            "Reporting Act 2013."
        ),
        "source_url": "https://www.xrb.govt.nz/standards/accounting-standards/for-profit-entities/nz-ifrs-18",
        "coverage_notes": (
            "Condition 2 VERIFIED. NZ IFRS 18, the New Zealand Equivalent to IFRS 18 "
            "Presentation and Disclosure in Financial Statements, was issued on 2024-05-23 by the "
            "NZ Accounting Standards Board of the External Reporting Board, pursuant to section "
            "12(a) of the Financial Reporting Act 2013; it is secondary legislation, gazetted on "
            "2024-05-23 and taking effect on 20 June 2024. Mandatory date 1 January 2027 for Tier 1 "
            "and Tier 2 for-profit entities; Tier 1 entities complying with NZ IFRS 18 are "
            "simultaneously in compliance with IFRS 18 as issued by the IASB, so the mandatory "
            "character is statutory rather than merely a rulebook election. Source ledger S-72. "
            "Conditions 3, 4 and 5 remain unverified: the NZX filing route's publication of an "
            "acceptance TIMESTAMP is not yet checked."
        ),
    },
    "Philippines": {
        "t_a": "2024-05-10",
        "date_conflict": (
            "Two Philippine dates, both recorded rather than merged: the Financial and "
            "Sustainability Reporting Standards Council (FSRSC) adopted PFRS 18 "
            "Presentation and Disclosure in Financial Statements on 2024-05-10, and the "
            "Professional Regulatory Board of Accountancy adopted it into the Philippine "
            "Accounting Standards by Resolution No. 38, series of 2024, dated 2024-05-29. "
            "T-A is the FSRSC adoption date, 2024-05-10, because the FSRSC is the standard "
            "setter and its adoption is the instrument that makes the standard part of the "
            "Philippine reporting framework, the same rule that was applied to Singapore's "
            "SFRS(I) 18 and Malaysia's MFRS 18. The Board of Accountancy resolution's own "
            "PDF could not be retrieved in this session (the request failed, and is recorded "
            "as a failed retrieval), so 2024-05-29 rests on a secondary rendering and is "
            "recorded as a conflict rather than used as T-A (D-011)."
        ),
        "source_url": "http://www.pfsrsc.org/government-organization-our-standards",
        "coverage_notes": (
            "Condition 2 VERIFIED. The Financial and Sustainability Reporting Standards "
            "Council's own standards page records PFRS 18 Presentation and Disclosure in "
            "Financial Statements with 'Date adopted by FSRSC: May 10, 2024' and an effective "
            "date of January 1, 2027. Mandatory character: the Securities and Exchange "
            "Commission prescribes the financial reporting framework for corporations under "
            "the Revised Securities Regulation Code Rule 68, and the Philippine Accounting "
            "Standards are issued by the Professional Regulatory Board of Accountancy under "
            "the Accountancy Act. "
            "Source ledger S-94. Conditions 3, 4 and 5 remain unverified: the SEC filing "
            "route's publication of an acceptance TIMESTAMP is not yet checked."
        ),
    },
    "Malaysia": {
        "t_a": "2024-06-14",
        "date_conflict": (
            "Two Malaysian dates are recorded rather than merged: the Malaysian Accounting "
            "Standards Board gave notice of the issuance of MFRS 18 on 2024-06-14 (the notice "
            "is signed by the Chairman and dated 14 June 2024), and MFRS 18 applies to annual "
            "reporting periods beginning on or after 1 January 2027. T-A is the notice date, "
            "2024-06-14, because the v1.1 event clock defines T-A as the jurisdictional "
            "legal-adoption date and the notice is the instrument. The MASB's own standards "
            "list records the same issue date, 14 June 2024, for MFRS 18 and 1 January 2027 "
            "as its applicable date; the two primary sources agree."
        ),
        "source_url": (
            "https://www.masb.org.my/pdf.php?file_path=pdf_file&pdf=20240614_Notice+ENG_Clean.pdf"
        ),
        "coverage_notes": (
            "Condition 2 VERIFIED. The Malaysian Accounting Standards Board's NOTICE - "
            "ISSUANCE OF MASB APPROVED ACCOUNTING STANDARD, issued under subsection 7(1) of "
            "the Financial Reporting Act 1997 (Act 558) and regulation 3 of the Financial "
            "Reporting (Publication of Approved Accounting Standards) Regulations 1999, gives "
            "notice of MFRS 18 Presentation and Disclosure in Financial Statements, applies "
            "it to financial statements required to be prepared or lodged under any law "
            "administered by the Securities Commission Malaysia, and is dated 14 June 2024. "
            "MFRS 18 applies for annual reporting periods beginning on or after 1 January "
            "2027. Source ledger S-91 (notice) and S-98 (the MASB standards list). "
            "Conditions 3, 4 and 5 remain unverified: the Bursa Malaysia filing route's "
            "publication of an acceptance TIMESTAMP is not yet checked."
        ),
    },
    "Hong Kong Sar": {
        "t_a": "2024-07-09",
        "date_conflict": (
            "Two Hong Kong dates are recorded rather than merged: the HKICPA's Financial "
            "Reporting Standards Committee approved the issuance of HKFRS 18 at its meeting "
            "of 31 May 2024, and the committee's own minutes carry the post-meeting note "
            "'HKFRS 18 together with the consequential amendments to other HKFRSs and the "
            "updated HK-Int 5 were issued on 9 July 2024'. T-A is the issuance date, "
            "2024-07-09, because the v1.1 event clock defines T-A as the jurisdictional "
            "legal-adoption date and the issuance is that event; the approval meeting of "
            "31 May 2024 is recorded as the earlier step in the same process. The earlier "
            "attempt on this jurisdiction (D-026, source S-78) had read only the HKICPA's "
            "HKFRS 18 web page, which states the effective date but not the issuance date, "
            "and left T-A empty; the committee's own minutes now carry the day."
        ),
        "source_url": (
            "https://www.hkicpa.org.hk/-/media/HKICPA-Website/New-HKICPA/Standards-and-"
            "regulation/SSD/03_Our-views/Minutes-and-Meeting-Summaries/FRSC/20240531283.pdf"
        ),
        "coverage_notes": (
            "Condition 2 VERIFIED. The minutes of the 283rd meeting of the HKICPA's Financial "
            "Reporting Standards Committee, held on 31 May 2024 and signed by the Chairman on "
            "9 July 2024, record the Committee's approval of the issuance of HKFRS 18 and the "
            "post-meeting note that HKFRS 18 was issued on 9 July 2024. HKFRS 18 applies to "
            "financial periods beginning on or after 1 January 2027. Mandatory character: the "
            "HKICPA issues HKFRS for the purposes of the Companies Ordinance (Cap. 622) and "
            "the HKEX Listing Rules require issuers to prepare financial statements that "
            "comply with HKFRS. Source ledger S-92. Conditions 3, 4 and 5 remain unverified: "
            "the HKEX filing route's publication of an acceptance TIMESTAMP is not yet checked."
        ),
    },
    "Indonesia": {
        "t_a": "2025-05-28",
        "date_conflict": (
            "Two Indonesian dates are recorded rather than merged: the Indonesian Accounting "
            "Standards Board (DSAK IAI) ratified PSAK 118 Presentation and Disclosure in "
            "Financial Statements on 28 May 2025, and the exposure draft that preceded it "
            "(DE PSAK 118) was approved on 26 November 2024. T-A is the ratification date, "
            "2025-05-28, because the v1.1 event clock defines T-A as the jurisdictional "
            "legal-adoption date and the ratified standard is the instrument that makes "
            "IFRS 18 mandatory for Indonesian reporting entities; 2024-11-26 is the "
            "exposure draft and is recorded as an earlier step, not as the adoption."
        ),
        "source_url": (
            "https://web.iaiglobal.or.id/assets/files/file_sak/DSAK%20Terkini%20Volume%207%202025.pdf"
        ),
        "coverage_notes": (
            "Condition 2 VERIFIED. The DSAK IAI's own summary bulletin, DSAK Terkini Volume "
            "07/XII/2025, records that on 28 May 2025 DSAK IAI ratified PSAK 118 Presentation "
            "and Disclosure in Financial Statements, which refers to IFRS 18 Presentation and "
            "Disclosure in Financial Statements and takes effect on 1 January 2027. Mandatory "
            "character: Indonesian national accounting standards (SAK Indonesia) bind the "
            "listed companies supervised by the Financial Services Authority (OJK), whose "
            "financial statements must be prepared in accordance with SAK Indonesia. Source "
            "ledger S-93. Conditions 3, 4 and 5 remain unverified: the IDX filing route's "
            "publication of an acceptance TIMESTAMP is not yet checked."
        ),
    },
    "Saudi Arabia": {
        "t_a": "2024-12-26",
        "date_conflict": (
            "OPEN CONFLICT, RECORDED AND NOT RESOLVED. Two Saudi instruments bear on IFRS 18 and "
            "they are NOT the same kind of instrument. (a) The Saudi Organization for Chartered "
            "and Professional Accountants (SOCPA) adopted IFRS 18 for application in the Kingdom "
            "on 2024-12-26 (Accounting Standards Council resolution 25/06/1446H), which is the "
            "local adoption instrument. (b) The Capital Market Authority announcement CMA_N_4083 "
            "of 2026-06-30 is the Board's decision on EARLY ADOPTION during 2026; it states that "
            "mandatory application commences for financial reporting periods beginning on or "
            "after 2027-01-01. research/specification_v1.2.md section 1.2 recorded T-A as "
            "2026-06-30, which is date (b), an early-adoption decision, not the instrument that "
            "makes IFRS 18 mandatory. The registered rule (condition 2) asks for the instrument "
            "MAKING IFRS 18 MANDATORY, so T-A is 2024-12-26 and date (b) is recorded as a "
            "separate event. CONSEQUENCE THAT MUST NOT BE DISCOVERED LATE: CMA_N_4083 also requires "
            "a preliminary assessment of the expected impact of initial application in approved "
            "financial statements for periods beginning on or after 2026-04-01. With T-A at "
            "2024-12-26 that mandated pre-adoption disclosure falls INSIDE the transition window "
            "rather than before it, so Saudi Arabia does not have the clean pre-disclosure anchor "
            "T-PRE that research/specification_v1.2.md section 2 requires of PH-1. Whether the "
            "Saudi row enters PH-1 at all, and on what footing, is a decision that must be made "
            "BEFORE the holdout is opened and must not be settled by looking at outcomes."
        ),
        "source_url": "https://cma.gov.sa/en/MediaCenter/NEWS/Pages/CMA_N_4083.aspx",
        "coverage_notes": (
            "Condition 2 VERIFIED for the local adoption instrument (SOCPA, 2024-12-26). The CMA "
            "announcement CMA_N_4083 of 2026-06-30 is the early-adoption decision and is recorded "
            "as a separate event, not as T-A. Application for financial reporting periods beginning "
            "on or after 2027-01-01. Source ledger S-61 (SOCPA) and S-62 (CMA). Conditions 3, 4 and 5 remain unverified, and the T-PRE "
            "consequence in the date_conflict field is unresolved by design."
        ),
    },
}

#: Jurisdictions whose condition 2 has NOT been verified. Their T-A stays empty
#: and the row stays ``pending``: an unverified date is never filled in.
UNVERIFIED_FILING_ROUTE = (
    "PENDING A2 verification of a filing route that publishes an acceptance TIMESTAMP "
    "(a date alone is insufficient; research/specification_v1.1.md section 1.1 condition j)"
)
UNVERIFIED_PRICE = "PENDING A1 (price vendors and their licensing are not yet authorised)"


def _strip(text: str) -> str:
    return " ".join((text or "").split())


#: A jurisdiction name is a place name. The longest name in the candidate
#: universe is "St Vincent And The Grenadines" (five words); the IFRS
#: Foundation index page also carries a boilerplate disclaimer paragraph, and the
#: 2026-10-22 snapshot parsed that paragraph as if it were a jurisdiction
#: (decision D-025). The filter below rejects any name that is not a place name,
#: so the artefact cannot recur.
MAX_JURISDICTION_WORDS = 8
MAX_JURISDICTION_CHARS = 60


def is_plausible_jurisdiction(name: str) -> bool:
    """True when a candidate name can be a jurisdiction and not page boilerplate."""
    text = _strip(name)
    if not text:
        return False
    if len(text.split()) > MAX_JURISDICTION_WORDS:
        return False
    if len(text) > MAX_JURISDICTION_CHARS:
        return False
    return True


def classify_profile_route(jurisdiction: str, status_text: str) -> str:
    """Classify the reporting framework the dated jurisdiction profile records.

    The rule is fixed and deterministic:

    1. no status text in the profile → ``no_profile_status_text``;
    2. the text says the IFRS Accounting Standards **as adopted by the EU** →
       ``eu_member_state`` for the 27 member states, and
       ``eea_efta_own_instrument`` for the EEA/EFTA states, whose route runs
       through their own incorporation instrument;
    3. the text names a **national equivalent** framework → ``national_equivalent_profile``;
    4. anything else → ``standing_reference_profile``.

    This is a **triage prior, not a determination**. The panel's own data
    contains the counterexamples: Brazil's profile says only "Required." and
    Saudi Arabia's records the IFRS Accounting Standards, yet both have dated
    national instruments (CVM Resolution 237; the SOCPA resolution). A
    standing-reference profile therefore never excludes a jurisdiction.
    """
    text = _strip(status_text).lower()
    if not text:
        return ROUTE_NO_STATUS_TEXT
    if any(marker in text for marker in EU_ADOPTED_MARKERS):
        if jurisdiction in EEA_EFTA_STATES:
            return ROUTE_EEA_EFTA
        return ROUTE_EU_MEMBER
    if any(marker in text for marker in NATIONAL_EQUIVALENT_MARKERS):
        return ROUTE_NATIONAL_EQUIVALENT
    return ROUTE_STANDING_REFERENCE


def load_candidate_jurisdictions(panel_v1_1_path: Path) -> list[dict[str, str]]:
    """Read the candidate universe from the Stratum B rows of ``panel_v1.1.csv``.

    The Stratum B rows of the retrospective panel are one row per
    (jurisdiction, standard) and were themselves derived by rule from the dated
    IFRS Foundation profile snapshot. Reading them back here keeps the two panel
    files on **one vintage** and avoids a second snapshot.

    Returns one record per jurisdiction, in file order.
    """
    seen: dict[str, dict[str, str]] = {}
    with Path(panel_v1_1_path).open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("stratum") != "B":
                continue
            jurisdiction = _strip(row.get("jurisdiction", ""))
            if not jurisdiction or jurisdiction in seen:
                continue
            if not is_plausible_jurisdiction(jurisdiction):
                continue
            seen[jurisdiction] = {
                "jurisdiction": jurisdiction,
                "membership_screen": _strip(row.get("membership_screen", "")),
                "profile_url": _strip(row.get("profile_url", "")),
                "profile_sha256": _strip(row.get("profile_sha256", "")),
                "profile_retrieved_utc": _strip(row.get("profile_retrieved_utc", "")),
                "profile_last_updated": _strip(row.get("profile_last_updated", "")),
                "status_text": _strip(row.get("status_text", "")),
            }
    return list(seen.values())


def build_row(
    index: int,
    candidate: dict[str, str],
    instrument: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build one PH-1 panel row.

    ``instrument`` is ``None`` for a jurisdiction whose condition 2 is not yet
    verified; such a row keeps an empty ``T_A`` and stays ``pending``.
    """
    jurisdiction = candidate["jurisdiction"]
    instrument = instrument or {}
    t_a = _strip(instrument.get("t_a", ""))
    scope = candidate.get("status_text", "")
    verified = bool(instrument)
    route = classify_profile_route(jurisdiction, scope)

    if verified:
        coverage = instrument.get("coverage_notes", "")
        date_conflict = instrument.get("date_conflict", "")
        source_url = instrument.get("source_url", "")
        scope_rule = (
            f"IFRS 18 instrument verified; affected class per the instrument. "
            f"Profile extent of IFRS application: {scope}"
        )
        cohort = t_a
    elif route == ROUTE_EU_MEMBER:
        coverage = (
            "PH-1 CANDIDATE, RULE-DERIVED, NOT YET ADMITTED. The profile records the IFRS "
            "Accounting Standards as adopted by the EU, so this jurisdiction is in the EU "
            "TIMING COHORT and would join the cohort dated 2026-02-13 (Commission Regulation "
            "(EU) 2026/338). Condition 2 is NOT yet verified for this row: the member-state "
            "carve-out check is OUTSTANDING (member states with a permanent derogation from "
            "particular endorsed standards), so T_A is left EMPTY rather than inherited "
            "silently. Conditions 4 and 5 are unverified pending A2 and A1."
        )
        date_conflict = ""
        source_url = candidate.get("profile_url", "")
        scope_rule = (
            f"IFRS 18 affected-firm list NOT yet determined for this jurisdiction. "
            f"Profile extent of IFRS application: {scope}"
        )
        cohort = EU_COHORT_T_A
    elif route == ROUTE_EEA_EFTA:
        coverage = (
            "PH-1 CANDIDATE, RULE-DERIVED, NOT YET ADMITTED. The profile text is identical "
            "to the EU member states' ('as adopted by the EU'), but this jurisdiction reaches "
            "the EU-endorsed IFRS through its OWN incorporation instrument, so its T-A is a "
            "separate question from the EU's and has not been located. Condition 2 is NOT "
            "verified: T_A is left EMPTY rather than inherited from the EU. Conditions 4 and "
            "5 are unverified pending A2 and A1."
        )
        date_conflict = ""
        source_url = candidate.get("profile_url", "")
        scope_rule = (
            f"IFRS 18 affected-firm list NOT yet determined for this jurisdiction. "
            f"Profile extent of IFRS application: {scope}"
        )
        cohort = ""
    else:
        coverage = (
            "PH-1 CANDIDATE, RULE-DERIVED, NOT YET ADMITTED. Condition 2 (a legal instrument "
            "making IFRS 18 mandatory, with a day-level date) is NOT verified for this "
            "jurisdiction: no instrument has been located, so T_A is left EMPTY rather than "
            "inferred. Condition 3 rests on the dated IFRS Foundation jurisdiction profile "
            "snapshot of 2026-10-22 (S-58). Conditions 4 and 5 are unverified pending A2 and A1."
        )
        date_conflict = ""
        source_url = candidate.get("profile_url", "")
        scope_rule = (
            f"IFRS 18 affected-firm list NOT yet determined for this jurisdiction. "
            f"Profile extent of IFRS application: {scope}"
        )
        cohort = ""

    return {
        "event_id": f"EV-{300 + index:03d}",
        "standard_id": STANDARD_ID,
        "jurisdiction": jurisdiction,
        "stratum": STRATUM,
        "T_A": t_a,
        "T_E": APPLICATION_DATE,
        "in_registered_panel": "pending",
        "date_conflict": date_conflict,
        "source_url": source_url,
        "filing_route": UNVERIFIED_FILING_ROUTE,
        "affected_firm_scope_rule": scope_rule,
        "price_venue_set": UNVERIFIED_PRICE,
        "coverage_notes": coverage,
        "membership_screen": candidate.get("membership_screen", ""),
        "profile_url": candidate.get("profile_url", ""),
        "profile_sha256": candidate.get("profile_sha256", ""),
        "profile_retrieved_utc": candidate.get("profile_retrieved_utc", ""),
        "profile_last_updated": candidate.get("profile_last_updated", ""),
        "status_text": scope,
        "profile_route_hint": route,
        "timing_cohort": cohort,
    }


def build_rows(candidates: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Build every PH-1 panel row, in candidate order."""
    rows: list[dict[str, str]] = []
    for index, candidate in enumerate(candidates, start=1):
        jurisdiction = candidate["jurisdiction"]
        rows.append(build_row(index, candidate, IFRS18_INSTRUMENTS.get(jurisdiction)))
    return rows


def write_panel(rows: Iterable[dict[str, str]], path: Path) -> int:
    """Write the PH-1 panel file with the retrospective panel's schema."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(PH1_COLUMNS), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in PH1_COLUMNS})
            count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    """Rebuild the PH-1 panel file from the registered candidate universe."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--panel-v1-1",
        default="research/panel_v1.1.csv",
        help="the retrospective panel file whose Stratum B rows define the universe",
    )
    parser.add_argument(
        "--out", default="research/panel_v1.2.csv", help="the PH-1 panel file to write"
    )
    args = parser.parse_args(argv)
    candidates = load_candidate_jurisdictions(Path(args.panel_v1_1))
    rows = build_rows(candidates)
    count = write_panel(rows, Path(args.out))
    verified = sum(1 for row in rows if row["T_A"])
    print(f"wrote {count} rows to {args.out}")
    print(f"candidate jurisdictions: {len(candidates)}; condition-2 verified: {verified}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

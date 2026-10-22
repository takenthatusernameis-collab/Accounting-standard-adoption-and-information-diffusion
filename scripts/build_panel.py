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
condition 5 on the A1 authorisation. **Condition 2 is verified for five
jurisdictions only** (European Union, United Kingdom, Saudi Arabia, Singapore,
Brazil). Every row therefore carries
``in_registered_panel = pending``, which is the three-state discipline of
``research/specification_v1.1.md`` §4.2: ``true`` / ``false`` / ``pending``.

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

**Hong Kong and South Africa are recorded as *attempted and not verified*, not as
verified.** Hong Kong's HKICPA page states the effective date (financial periods
beginning on or after 2027-01-01) but the retrieved page does not carry the
issuance date, so T-A is left empty. South Africa's route is incorporation by
reference ("IFRS as issued from time to time by the IASB"), which has no dated
local instrument, so T-A is left empty. Both attempts are recorded in
``research/decision_log.md`` (D-026).

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
    "Saudi Arabia": {
        "t_a": "2024-12-26",        "date_conflict": (
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

    if verified:
        coverage = instrument.get("coverage_notes", "")
        date_conflict = instrument.get("date_conflict", "")
        source_url = instrument.get("source_url", "")
        scope_rule = (
            f"IFRS 18 instrument verified; affected class per the instrument. "
            f"Profile extent of IFRS application: {scope}"
        )
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
        writer = csv.DictWriter(handle, fieldnames=list(PANEL_COLUMNS), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in PANEL_COLUMNS})
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

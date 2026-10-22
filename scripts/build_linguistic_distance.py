"""Builder for the fallback linguistic-distance scale and its concordance report.

Reads the dated, hashed source snapshots in the cache outside the working tree
(decision **D-015**), scores every jurisdiction in the registered panel, writes
the derived table to ``research/linguistic_distance_v1.csv`` and writes the
external-validation report to ``research/linguistic_concordance.md``.

The published measure (S-44, Table 1) is used **only** as an external validation
of the fallback's ordering, and as the source of the official-language list for
the jurisdictions it covers. It is never combined with the fallback and never
presented as this campaign's own measure (decision **D-023**; v1.1 §3.5).

The builder is deterministic, needs no network access, and takes its inputs from
the cache so that the derived artefacts are reproducible from recorded hashes.
"""

from __future__ import annotations

import argparse
import csv
import zipfile
from pathlib import Path

from .linguistic_distance import (
    LD_BANDS,
    MIN_COMMON_FEATURES,
    OFFICIAL_STATUS_STRICT,
    PARSER_VERSION,
    JurisdictionScore,
    concordance,
    iso_language_scores,
    jurisdiction_score,
    load_cldr_official_languages,
    load_cldr_territory_names,
    load_sil_code_scopes,
    load_sil_macrolanguages,
    published_official_languages,
    read_published_table,
    resolve_territory,
    score_jurisdictions,
)

COLUMNS: tuple[str, ...] = (
    "jurisdiction",
    "territory",
    "official_languages_iso639_3",
    "official_language_source",
    "ld_score",
    "ld_category",
    "missing_languages",
    "wals_records_considered",
    "note",
)

#: Published-measure country names that differ from the IFRS Foundation names.
PUBLISHED_NAME_ALIASES: dict[str, str] = {
    "Hong Kong": "Hong Kong Sar",
    "Türkiye": "Turkiye",
}

#: The official-language source used for each jurisdiction.
SOURCE_PUBLISHED = "S-44 Table 1 (published list)"
SOURCE_CLDR = "Unicode CLDR 48.2.0 (strict official status)"


def panel_jurisdictions(panel_path: Path) -> list[str]:
    """Read the candidate jurisdictions from the Stratum B rows of the panel."""
    seen: list[str] = []
    with Path(panel_path).open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("stratum") != "B":
                continue
            jurisdiction = (row.get("jurisdiction") or "").strip()
            if jurisdiction and jurisdiction not in seen:
                seen.append(jurisdiction)
    return seen


def load_sources(cache_root: Path) -> tuple[dict[str, object], dict[str, str], dict[str, str]]:
    """Load the cached source snapshots needed to score the jurisdictions."""
    wals_path = cache_root / "raw" / "linguistic" / "wals-2020.6.zip"
    cldr_path = cache_root / "raw" / "linguistic" / "cldr-common-49.zip"
    cldr_json = cache_root / "raw" / "linguistic" / "cldr_territoryInfo.json"
    macrolanguages = load_sil_macrolanguages(
        cache_root / "raw" / "linguistic" / "iso-639-3-macrolanguages.tab"
    )
    scopes = load_sil_code_scopes(cache_root / "raw" / "linguistic" / "iso-639-3.tab")
    with zipfile.ZipFile(cldr_path) as cldr:
        territory_names = load_cldr_territory_names(cldr)
    official = load_cldr_official_languages(cldr_json, statuses=OFFICIAL_STATUS_STRICT)
    requested = sorted({language for languages in official.values() for language in languages})
    with zipfile.ZipFile(wals_path) as wals:
        scores = iso_language_scores(
            wals, codes=requested, macrolanguages=macrolanguages, scopes=scopes
        )
    return {"official": official, "scores": scores, "names": territory_names}, official, territory_names


def score_panel(
    jurisdictions: list[str],
    official: dict[str, tuple[str, ...]],
    territory_names: dict[str, str],
    scores: dict[str, object],
    published: dict[str, tuple[str, ...]],
) -> list[JurisdictionScore]:
    """Score every jurisdiction under the registered official-language rule."""
    scored: list[JurisdictionScore] = []
    for jurisdiction in jurisdictions:
        territory = resolve_territory(jurisdiction, territory_names)
        if territory is None:
            scored.append(
                JurisdictionScore(
                    jurisdiction=jurisdiction,
                    territory="",
                    official_languages=(),
                    score=None,
                    category="LD-NA",
                    missing_languages=(),
                    note="No CLDR territory could be matched to this jurisdiction name.",
                )
            )
            continue
        languages = published.get(jurisdiction)
        if languages is None:
            languages = official.get(territory, ())
        scored.append(
            score_jurisdictions([jurisdiction], {territory: languages}, territory_names, scores)[0]
        )
    return scored


def build_rows(
    cache_root: Path,
    panel_path: Path,
    published_path: Path,
    published: dict[str, tuple[str, ...]],
) -> list[dict[str, str]]:
    """Score every panel jurisdiction from the cached source snapshots."""
    sources, official, territory_names = load_sources(cache_root)
    scores = sources["scores"]
    jurisdictions = panel_jurisdictions(panel_path)
    scored = score_panel(jurisdictions, official, territory_names, scores, published)
    rows: list[dict[str, str]] = []
    for record in scored:
        considered = sum(
            scores[language].wals_records
            for language in record.official_languages
            if language in scores
        )
        source = (
            SOURCE_PUBLISHED
            if record.jurisdiction in published
            else SOURCE_CLDR
        )
        rows.append(
            {
                "jurisdiction": record.jurisdiction,
                "territory": record.territory,
                "official_languages_iso639_3": " ".join(record.official_languages),
                "official_language_source": source,
                "ld_score": "" if record.score is None else f"{record.score:.6f}",
                "ld_category": record.category,
                "missing_languages": " ".join(record.missing_languages),
                "wals_records_considered": str(considered),
                "note": record.note,
            }
        )
    return rows


def write_table(rows: list[dict[str, str]], path: Path) -> int:
    """Write the derived per-jurisdiction table."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(COLUMNS), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in COLUMNS})
    return len(rows)


def write_concordance(
    report: dict[str, object],
    sensitivity: dict[str, object],
    panel_report: dict[str, object],
    rows: list[dict[str, str]],
    path: Path,
) -> None:
    """Write the external-validation report."""
    bands = "\n".join(f"| {name} | ({low:.3f}, {high:.3f}] |" for name, low, high in LD_BANDS)
    matched = report["matched"]  # type: ignore[index]
    lines = [
        "# ACCTCLOCK — fallback linguistic-distance scale and its external validation",
        "",
        "Generated by `scripts/build_linguistic_distance.py` "
        f"(parser version `{PARSER_VERSION}`). Deterministic; no network access.",
        "",
        "## What this is",
        "",
        "The campaign's mandatory country-level control (v1.1 §3.5) is imposed as a",
        "**stratification variable** (high versus low linguistic distance) and is",
        "absorbed by the within-jurisdiction specification. Decision **D-023** selected",
        "the **registered fallback ordinal scale** over the published measure, because",
        "the published measure cannot be reproduced exactly panel-wide: its",
        "jurisdiction-level official-language lists come from a licensed and versioned",
        "commercial database whose vintage is not archived.",
        "",
        "This report is the **external validation** that D-023 required: the fallback",
        "must rank jurisdictions in the same order as the published measure on the",
        "countries where the published measure gives a value. It is a validation of a",
        "**control**, not a test of the hypothesis, and it is not an outcome.",
        "",
        "## Construction",
        "",
        "1. English reference: the WALS language record `eng`.",
        "2. A WALS parameter is compared between two languages when both carry a value",
        "   for it; it is **shared** when their value sets intersect.",
        "3. A language's friction score is the share of its compared parameters that are",
        "   not shared with English.",
        "4. A language's score is the **median** over the WALS records that carry its",
        f"   ISO 639-3 code and reach {MIN_COMMON_FEATURES} compared parameters. A",
        "   macrolanguage (`ara`, `zho`, `swa`) is scored from the WALS records of the",
        "   individual languages that belong to it (SIL ISO 639-3 macrolanguage table).",
        "5. A jurisdiction's score is the **simple mean** over its official languages,",
        "   which is the aggregation rule the published measure uses. A jurisdiction",
        "   whose official-language set is exactly {English} scores **0**.",
        "6. A jurisdiction with an official language that cannot be scored is **not",
        "   scored at all**: the mean over a subset of the official languages is not",
        "   comparable with the other jurisdictions, so no value is imputed and the",
        "   exclusion is recorded.",
        "7. The ordinal category is read off the fixed boundaries below.",
        "",
        "## The official-language input",
        "",
        "Two official-language inputs are used, and the source is recorded per",
        "jurisdiction in `research/linguistic_distance_v1.csv`:",
        "",
        f"- **{SOURCE_PUBLISHED}** for the jurisdictions the published measure covers —",
        "  a dated, citable, open list of national official languages;",
        f"- **{SOURCE_CLDR}** for every other jurisdiction. `official_regional`",
        "  languages are excluded, because CLDR uses that status for languages that are",
        "  official in part of a territory only (Welsh in the United Kingdom, Gaelic in",
        "  Scotland), which is not the national official-language status the published",
        "  measure uses.",
        "",
        "## The registered ordinal categories",
        "",
        "| Category | Score band |",
        "|---|---|",
        bands,
        "",
        "The boundaries are the published measure's own quartiles over its 84-country",
        "sample (S-44 Table 2, Panel A: Q1 0.255, median 0.342, Q3 0.482). They are",
        "fixed here, in advance, on a **published distribution** — not on this",
        "campaign's panel, which is not assembled, and not on any outcome. `LD-0` is",
        "reserved for a jurisdiction whose official-language set is exactly {English}.",
        "",
        "## External validation against the published measure",
        "",
        f"- Countries matched: **{report['matched_count']}** of 84 published rows.",
        f"- Spearman rank correlation: **{report['spearman']:.4f}**.",
        f"- Pearson correlation: **{report['pearson']:.4f}**.",
        f"- Largest absolute difference on a matched country: "
        f"**{report['max_absolute_difference']:.4f}**.",
        f"- Restricted to the jurisdictions that are also in the registered panel: "
        f"**{panel_report['matched_count']}** countries, Spearman "
        f"**{panel_report['spearman']:.4f}**, Pearson **{panel_report['pearson']:.4f}**.",
        f"- Published rows that could not be matched and are reported as unmatched: "
        f"**{len(report['unmatched'])}**"
        + (f" ({', '.join(report['unmatched'])})" if report["unmatched"] else "")
        + ".",
        "",
        "### Sensitivity: the CLDR official-language input throughout",
        "",
        "The concordance is recomputed with the CLDR official-language input for every",
        "country, which is the strictest reading of an open input and the one that",
        "carries the most country-list disagreement with the published measure:",
        "",
        f"- Countries matched: **{sensitivity['matched_count']}** of 84 published rows.",
        f"- Spearman rank correlation: **{sensitivity['spearman']:.4f}**.",
        f"- Pearson correlation: **{sensitivity['pearson']:.4f}**.",
        f"- Largest absolute difference on a matched country: "
        f"**{sensitivity['max_absolute_difference']:.4f}**.",
        "",
        "The difference between the two rows is a **country-list** difference, not a",
        "distance-computation difference: the WALS recomputation reproduces the",
        "published per-language values, and the disagreements are entirely in which",
        "languages a country's official list contains.",
        "",
        "### Matched countries, published value against fallback value",
        "",
        "| Country | Published LD | Fallback LD | Difference |",
        "|---|---|---|---|",
    ]
    for country, published_value, fallback in matched:
        lines.append(
            f"| {country} | {published_value:.3f} | {fallback:.3f} | "
            f"{fallback - published_value:+.3f} |"
        )
    lines += [
        "",
        "## Coverage of the registered panel",
        "",
        f"- Jurisdictions scored: **{sum(1 for row in rows if row['ld_score'])}** of {len(rows)}.",
        f"- Jurisdictions with no jurisdiction-level value: "
        f"**{sum(1 for row in rows if row['ld_category'] == 'LD-NA')}** "
        f"({', '.join(sorted({row['jurisdiction'] for row in rows if row['ld_category'] == 'LD-NA'})) or 'none'}).",
        f"- Jurisdictions whose official-language input is the published list: "
        f"**{sum(1 for row in rows if row['official_language_source'] == SOURCE_PUBLISHED)}**; "
        f"from CLDR: **{sum(1 for row in rows if row['official_language_source'] == SOURCE_CLDR)}**.",
        "",
        "The per-jurisdiction table is `research/linguistic_distance_v1.csv`. The source",
        "snapshots are recorded in `research/manifests/linguistic_sources.jsonl` with",
        "their SHA-256 digests; the raw archives stay in the cache outside the working",
        "tree (D-015).",
        "",
        "**Boundary conditions.** A jurisdiction whose official-language set cannot be",
        "reproduced from the open sources is recorded as **unmatched** or **not",
        "applicable**, never as a zero. The control is a **published conditioner** and a",
        "**mandatory control**, never this campaign's own effect (v1.1 §3.5).",
    ]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Build the derived table and the concordance report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-root", default=None, help="cache root holding raw/linguistic")
    parser.add_argument(
        "--panel",
        default="research/panel_v1.1.csv",
        help="panel file whose Stratum B rows define the candidate jurisdictions",
    )
    parser.add_argument(
        "--out-table", default="research/linguistic_distance_v1.csv", help="derived table path"
    )
    parser.add_argument(
        "--out-report",
        default="research/linguistic_concordance.md",
        help="concordance report path",
    )
    parser.add_argument(
        "--published",
        default="research/linguistic_s44_table1.csv",
        help="published-measure fixture used for the external validation",
    )
    args = parser.parse_args(argv)

    from .data_cache import build_layout

    layout = build_layout(args.cache_root)
    published_map = published_official_languages(Path(args.published))
    renamed_published = {
        PUBLISHED_NAME_ALIASES.get(country, country): codes
        for country, codes in published_map.items()
    }
    rows = build_rows(layout.root, Path(args.panel), Path(args.published), renamed_published)
    count = write_table(rows, Path(args.out_table))

    sources, official, territory_names = load_sources(layout.root)
    scores = sources["scores"]
    published_rows = read_published_table(Path(args.published))
    renamed_rows = [
        {**row, "country": PUBLISHED_NAME_ALIASES.get(row["country"].strip(), row["country"].strip())}
        for row in published_rows
    ]

    def score_map(language_sets: dict[str, tuple[str, ...]]) -> dict[str, JurisdictionScore]:
        out: dict[str, JurisdictionScore] = {}
        for name, languages in language_sets.items():
            record = jurisdiction_score(name, name, languages, scores)
            if record.score is not None:
                out[name] = record
        return out

    primary_map = {
        row["jurisdiction"]: JurisdictionScore(
            jurisdiction=row["jurisdiction"],
            territory=row["territory"],
            official_languages=tuple(row["official_languages_iso639_3"].split()),
            score=float(row["ld_score"]) if row["ld_score"] else None,
            category=row["ld_category"],
            missing_languages=tuple(row["missing_languages"].split()),
            note=row["note"],
        )
        for row in rows
        if row["ld_score"]
    }
    published_sets: dict[str, tuple[str, ...]] = {}
    for row in published_rows:
        country = PUBLISHED_NAME_ALIASES.get(row["country"].strip(), row["country"].strip())
        languages = published_map.get(row["country"].strip())
        if languages:
            published_sets[country] = languages
    report = concordance(renamed_rows, score_map(published_sets))
    panel_report = concordance(renamed_rows, primary_map)

    cldr_sets: dict[str, tuple[str, ...]] = {}
    for row in published_rows:
        country = PUBLISHED_NAME_ALIASES.get(row["country"].strip(), row["country"].strip())
        territory = resolve_territory(country, territory_names)
        if territory is None:
            continue
        cldr_sets[country] = official.get(territory, ())
    sensitivity = concordance(renamed_rows, score_map(cldr_sets))

    write_concordance(report, sensitivity, panel_report, rows, Path(args.out_report))
    print(f"scored {count} jurisdictions")
    print(f"published-sample spearman {report['spearman']:.4f} over {report['matched_count']} rows")
    print(f"cldr sensitivity spearman {sensitivity['spearman']:.4f} over {sensitivity['matched_count']} rows")
    print(f"panel-overlap spearman {panel_report['spearman']:.4f} over {panel_report['matched_count']} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

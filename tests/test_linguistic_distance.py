"""Unit tests for the fallback linguistic-distance scale.

The tests use small synthetic fixtures so that the whole rule — the feature
comparison, the macrolanguage expansion, the jurisdiction mean, the ordinal
bands and the concordance statistics — is verifiable with **zero** network calls
and without the multi-megabyte source archives.
"""

from __future__ import annotations

import csv
import io
import zipfile

import pytest

from scripts.linguistic_distance import (
    ENGLISH_ISO,
    LD_BANDS,
    OFFICIAL_STATUS_STRICT,
    PUBLISHED_LANGUAGE_CODES,
    LanguageScore,
    band,
    concordance,
    iso_language_scores,
    language_candidates,
    language_friction,
    normalise_language_code,
    pearson,
    ranks,
    resolve_territory,
    score_jurisdictions,
    spearman,
)

VALUES = """ID,Language_ID,Parameter_ID,Value
1,eng,1A,1
2,eng,2A,1
3,eng,3A,2
4,spa,1A,1
5,spa,2A,2
6,spa,3A,2
7,fra,1A,2
8,fra,2A,1
9,fra,3A,2
10,jpn,1A,2
11,jpn,2A,2
12,jpn,3A,2
"""

LANGUAGES = """ID,Name,ISO639P3code,ISO_codes
eng,English,eng,eng
spa,Spanish,spa,spa
fra,French,fra,fra
jpn,Japanese,jpn,jpn
"""

MACROLANGUAGES = """M_Id\tI_Id\tI_Status
zho\tcmn\tA
"""


def build_archive(values: str = VALUES, languages: str = LANGUAGES) -> zipfile.ZipFile:
    """Build an in-memory zip carrying the WALS-shaped CLDF members."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("wals/cldf/values.csv", values)
        archive.writestr("wals/cldf/languages.csv", languages)
    buffer.seek(0)
    return zipfile.ZipFile(buffer)


def test_friction_counts_features_that_are_not_shared() -> None:
    archive = build_archive()
    values = {
        "eng": {"1A": {"1"}, "2A": {"1"}, "3A": {"2"}},
        "spa": {"1A": {"1"}, "2A": {"2"}, "3A": {"2"}},
    }
    score, compared = language_friction(values, "spa")
    assert compared == 3
    assert score == pytest.approx(1 / 3)


def test_features_absent_from_one_language_are_excluded_not_counted_as_unshared() -> None:
    values = {
        "eng": {"1A": {"1"}},
        "spa": {"1A": {"1"}, "9Z": {"7"}},
    }
    score, compared = language_friction(values, "spa")
    assert compared == 1
    assert score == 0.0


def test_iso_scores_are_the_median_over_the_wals_records_that_carry_the_code() -> None:
    archive = build_archive()
    scores = iso_language_scores(archive, codes=["spa", "jpn"], min_common_features=1)
    assert scores["spa"].score == pytest.approx(1 / 3)
    assert scores["jpn"].score == pytest.approx(2 / 3)
    assert scores["spa"].wals_records == 1


def test_macrolanguage_is_scored_from_the_individuals_that_belong_to_it() -> None:
    archive = build_archive()
    candidates = language_candidates("zho", {"zho": ("cmn",)}, {})
    assert "cmn" in candidates
    assert candidates == ("cmn", "zho")


def test_declared_equivalence_is_available_for_filipino() -> None:
    candidates = language_candidates("fil", {}, {})
    assert "tgl" in candidates


def test_iso_two_letter_codes_are_expanded_and_script_subtags_dropped() -> None:
    assert normalise_language_code("en") == "eng"
    assert normalise_language_code("zh_Hant") == "zho"
    assert normalise_language_code("fil") == "fil"
    assert normalise_language_code("") is None


def test_english_only_jurisdiction_scores_zero_and_is_band_ld0() -> None:
    scores = {ENGLISH_ISO: LanguageScore("eng", 0.0, 100, 1)}
    record = score_jurisdictions(
        ["Anguilla"], {"AI": ("eng",)}, {"AI": "Anguilla"}, scores
    )[0]
    assert record.score == 0.0
    assert record.category == "LD-0"


def test_jurisdiction_score_is_the_mean_over_its_official_languages() -> None:
    scores = {
        "eng": LanguageScore("eng", 0.0, 100, 1),
        "spa": LanguageScore("spa", 0.3, 100, 1),
        "fra": LanguageScore("fra", 0.5, 100, 1),
    }
    record = score_jurisdictions(
        ["Canada"], {"CA": ("eng", "fra")}, {"CA": "Canada"}, scores
    )[0]
    assert record.score == pytest.approx(0.25)
    assert record.category == "LD-1"


def test_a_jurisdiction_with_an_unscorable_language_is_not_scored_at_all() -> None:
    scores = {"eng": LanguageScore("eng", 0.0, 100, 1)}
    record = score_jurisdictions(
        ["Philippines"], {"PH": ("eng", "fil")}, {"PH": "Philippines"}, scores
    )[0]
    assert record.score is None
    assert record.category == "LD-NA"
    assert record.missing_languages == ("fil",)
    assert "no value is imputed" in record.note


def test_band_boundaries_are_the_published_measure_quartiles() -> None:
    assert LD_BANDS[1][1:] == (0.0, 0.255)
    assert LD_BANDS[2][1:] == (0.255, 0.342)
    assert LD_BANDS[3][1:] == (0.342, 0.482)
    assert LD_BANDS[4][1:] == (0.482, 1.0)
    assert band(0.0, english_only=True) == "LD-0"
    assert band(0.2) == "LD-1"
    assert band(0.3) == "LD-2"
    assert band(0.4) == "LD-3"
    assert band(0.6) == "LD-4"


def test_supranational_bloc_carries_no_value_rather_than_a_zero() -> None:
    record = score_jurisdictions(
        ["European Union"], {}, {"European Union": "European Union"}, {}
    )[0]
    assert record.score is None
    assert record.category == "LD-NA"


def test_territory_resolution_uses_the_alias_table_for_irfs_names() -> None:
    names = {"GB": "United Kingdom", "TW": "Taiwan", "HK": "Hong Kong"}
    assert resolve_territory("United Kingdom", names) == "GB"
    assert resolve_territory("Chinese Taipei", names) == "TW"
    assert resolve_territory("Hong Kong Sar", names) == "HK"
    assert resolve_territory("Nowhere", names) is None


def test_ranks_average_ties() -> None:
    assert ranks([10.0, 20.0, 20.0, 30.0]) == [1.0, 2.5, 2.5, 4.0]


def test_spearman_is_one_for_a_monotone_transform() -> None:
    assert spearman([1.0, 2.0, 3.0, 4.0], [10.0, 20.0, 30.0, 40.0]) == pytest.approx(1.0)
    assert spearman([1.0, 2.0, 3.0, 4.0], [40.0, 30.0, 20.0, 10.0]) == pytest.approx(-1.0)


def test_pearson_matches_the_closed_form() -> None:
    assert pearson([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == pytest.approx(1.0)


def test_concordance_reports_unmatched_countries_rather_than_dropping_them() -> None:
    published = [
        {"country": "Argentina", "official_language": "Spanish", "published_ld": "0.342"},
        {"country": "Japan", "official_language": "Japanese", "published_ld": "0.590"},
        {"country": "Nowhere", "official_language": "Spanish", "published_ld": "0.342"},
    ]
    fallback = {
        "Argentina": score_jurisdictions(
            ["Argentina"], {"AR": ("spa",)}, {"AR": "Argentina"},
            {"spa": LanguageScore("spa", 0.34, 100, 1)},
        )[0],
        "Japan": score_jurisdictions(
            ["Japan"], {"JP": ("jpn",)}, {"JP": "Japan"},
            {"jpn": LanguageScore("jpn", 0.59, 100, 1)},
        )[0],
    }
    report = concordance(published, fallback)
    assert report["matched_count"] == 2
    assert report["unmatched"] == ["Nowhere"]
    assert report["spearman"] == pytest.approx(1.0)


def test_published_language_names_all_map_to_iso_codes() -> None:
    assert PUBLISHED_LANGUAGE_CODES["English"] == "eng"
    assert PUBLISHED_LANGUAGE_CODES["Paraguayan Guaraní"] == "grn"
    assert set(PUBLISHED_LANGUAGE_CODES.values()) <= set(PUBLISHED_LANGUAGE_CODES.values())


def test_strict_status_filter_excludes_regional_official_languages() -> None:
    assert "official" in OFFICIAL_STATUS_STRICT
    assert "official_regional" not in OFFICIAL_STATUS_STRICT


def test_registered_cldr_vintages_are_declared_in_both_places() -> None:
    """The official-language and territory-name CLDR vintages must be stated.

    Decision D-028 registers CLDR 48.2.0 for the official-language statuses
    (source ledger S-81). The territory-name list comes from the CLDR 49 common
    bundle (S-82) because the `latest` URL serves that release. The two vintages
    differ, and the difference must stay visible in the code that produced the
    registered numbers rather than collapsing into a single version claim.
    """
    from scripts import build_linguistic_distance, linguistic_distance

    assert "48.2.0" in build_linguistic_distance.SOURCE_CLDR
    module_doc = linguistic_distance.__doc__ or ""
    assert "CLDR 48.2.0" in module_doc
    assert "CLDR **49**" in module_doc

"""Tests for the PH-1 panel builder.

No network access: the builder reads committed files only.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.build_panel import (  # noqa: E402
    IFRS18_INSTRUMENTS,
    PANEL_COLUMNS,
    build_rows,
    is_plausible_jurisdiction,
    load_candidate_jurisdictions,
    write_panel,
)

PANEL_V1_1 = REPO / "research" / "panel_v1.1.csv"


def _candidates():
    return load_candidate_jurisdictions(PANEL_V1_1)


def test_candidate_universe_is_one_row_per_jurisdiction():
    candidates = _candidates()
    names = [c["jurisdiction"] for c in candidates]
    assert len(names) == len(set(names)), "duplicate jurisdictions in the candidate universe"
    assert len(names) == 141


def test_page_boilerplate_is_not_a_jurisdiction():
    boilerplate = (
        "The information in these profiles is for general guidance only and may change from time "
        "to time. You should not act on the information in the profiles, and you should obtain "
        "specific professional advice to before making any decisions or taking any action."
    )
    assert is_plausible_jurisdiction(boilerplate) is False
    assert is_plausible_jurisdiction("Saudi Arabia") is True
    assert is_plausible_jurisdiction("St Vincent And The Grenadines") is True
    assert is_plausible_jurisdiction("") is False


def test_verified_instruments_are_the_six_primary_verified_jurisdictions():
    assert set(IFRS18_INSTRUMENTS) == {
        "European Union",
        "United Kingdom",
        "Saudi Arabia",
        "Singapore",
        "Brazil",
        "New Zealand",
    }


def test_panel_v1_2_schema_matches_panel_v1_1():
    with PANEL_V1_1.open("r", encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle))
    assert header == list(PANEL_COLUMNS)


def test_every_row_is_pending():
    rows = build_rows(_candidates())
    assert rows
    assert all(row["in_registered_panel"] == "pending" for row in rows)


def test_verified_instruments_carry_day_level_dates():
    rows = {row["jurisdiction"]: row for row in build_rows(_candidates())}
    assert rows["European Union"]["T_A"] == "2026-02-13"
    assert rows["United Kingdom"]["T_A"] == "2025-12-10"
    assert rows["Saudi Arabia"]["T_A"] == "2024-12-26"
    assert rows["Singapore"]["T_A"] == "2024-10-04"
    assert rows["Brazil"]["T_A"] == "2025-12-23"
    assert rows["New Zealand"]["T_A"] == "2024-05-23"
    for jurisdiction in IFRS18_INSTRUMENTS:
        assert rows[jurisdiction]["T_E"] == "2027-01-01"


def test_attempted_but_unverified_jurisdictions_carry_no_date():
    """Hong Kong, South Africa and South Korea were attempted and could not be
    verified at day level; their T-A stays empty rather than inferred."""
    rows = {row["jurisdiction"]: row for row in build_rows(_candidates())}
    for jurisdiction in ("Hong Kong Sar", "South Africa", "South Korea"):
        assert jurisdiction in rows, f"{jurisdiction} must be in the candidate universe"
        assert rows[jurisdiction]["T_A"] == "", (
            f"{jurisdiction} was attempted and not verified, so T_A must stay empty"
        )


def test_unverified_rows_have_no_date():
    rows = build_rows(_candidates())
    unverified = [r for r in rows if r["jurisdiction"] not in IFRS18_INSTRUMENTS]
    assert unverified
    assert all(row["T_A"] == "" for row in unverified)


def test_date_conflicts_are_recorded_not_resolved():
    rows = {row["jurisdiction"]: row for row in build_rows(_candidates())}
    for jurisdiction in IFRS18_INSTRUMENTS:
        assert rows[jurisdiction]["date_conflict"], f"{jurisdiction} must record its date conflict"
    assert "2026-06-30" in rows["Saudi Arabia"]["date_conflict"]
    assert "2025-12-12" in rows["United Kingdom"]["date_conflict"]
    assert "2026-02-16" in rows["European Union"]["date_conflict"]


def test_event_ids_are_unique_and_sequential():
    rows = build_rows(_candidates())
    ids = [row["event_id"] for row in rows]
    assert len(ids) == len(set(ids))
    assert ids[0] == "EV-301"


def test_candidate_rows_carry_the_snapshot_evidence():
    rows = build_rows(_candidates())
    for row in rows:
        assert row["profile_sha256"], row["jurisdiction"]
        assert row["profile_retrieved_utc"].startswith("2026-10-22")


def test_write_panel_round_trips(tmp_path):
    rows = build_rows(_candidates())
    out = tmp_path / "panel_v1.2.csv"
    count = write_panel(rows, out)
    assert count == len(rows)
    with out.open("r", encoding="utf-8", newline="") as handle:
        read_back = list(csv.DictReader(handle))
    assert len(read_back) == count
    assert read_back[0]["standard_id"] == "IFRS 18"

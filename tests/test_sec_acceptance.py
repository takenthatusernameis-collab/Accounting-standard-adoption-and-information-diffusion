"""Unit tests for the EDGAR SGML acceptance-timestamp parser.

Every case runs against a synthetic fixture in ``tests/fixtures/sec_edgar`` so
the whole acceptance-time path is verifiable with **zero** network calls
(``research/data_acquisition_plan.md`` §11).
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest

from scripts.sec_acceptance import (
    AcceptanceParseError,
    find_acceptance_field,
    format_utc,
    iter_header_fields,
    parse_acceptance_timestamp,
    parse_acceptance_timestamp_or_reason,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "sec_edgar"


def read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_standard_winter_stamp_uses_the_standard_time_offset() -> None:
    parsed = parse_acceptance_timestamp(read("submission_header_standard.txt"))
    assert parsed.ok
    assert parsed.raw_value == "20240116163025"
    # 16:30:25 Eastern Standard Time is 21:30:25 UTC.
    assert parsed.utc_datetime == dt.datetime(2024, 1, 16, 21, 30, 25, tzinfo=dt.timezone.utc)
    assert parsed.eastern_offset == dt.timedelta(hours=-5)
    assert not parsed.ambiguous
    assert not parsed.nonexistent


def test_summer_stamp_uses_the_daylight_time_offset() -> None:
    text = read("submission_header_standard.txt").replace("20240116163025", "20240716163025")
    parsed = parse_acceptance_timestamp(text)
    assert parsed.ok
    # 16:30:25 Eastern Daylight Time is 20:30:25 UTC.
    assert parsed.utc_datetime == dt.datetime(2024, 7, 16, 20, 30, 25, tzinfo=dt.timezone.utc)
    assert parsed.eastern_offset == dt.timedelta(hours=-4)


def test_spring_forward_nonexistent_local_time_is_quarantined() -> None:
    """The 23-hour day: 02:00-02:59 local does not exist on 2024-03-10."""
    parsed = parse_acceptance_timestamp(read("submission_header_dst_spring_forward.txt"))
    assert not parsed.ok
    assert parsed.nonexistent
    assert not parsed.ambiguous
    assert parsed.utc_datetime is None
    assert parsed.quarantine_reason == "nonexistent_local_time"
    assert parsed.local_date == dt.date(2024, 3, 10)
    assert parsed.local_time == dt.time(2, 30)


def test_fall_back_ambiguous_local_time_is_quarantined_with_both_candidates() -> None:
    """The 25-hour day: 01:00-01:59 local happens twice on 2024-11-03."""
    parsed = parse_acceptance_timestamp(read("submission_header_dst_fall_back.txt"))
    assert not parsed.ok
    assert parsed.ambiguous
    assert not parsed.nonexistent
    assert parsed.quarantine_reason == "ambiguous_local_time"
    # Both readings are recorded; neither is silently chosen.
    assert len(parsed.candidate_utc_datetimes) == 2
    assert dt.datetime(2024, 11, 3, 5, 30, tzinfo=dt.timezone.utc) in parsed.candidate_utc_datetimes
    assert dt.datetime(2024, 11, 3, 6, 30, tzinfo=dt.timezone.utc) in parsed.candidate_utc_datetimes
    assert parsed.candidate_utc_datetimes[0] < parsed.candidate_utc_datetimes[1]


def test_transition_days_have_23_and_25_local_hours() -> None:
    """The offset really does switch on the two transition dates."""
    spring = parse_acceptance_timestamp(read("submission_header_dst_spring_forward.txt"))
    assert spring.eastern_offset == dt.timedelta(hours=-5)
    fall = parse_acceptance_timestamp(read("submission_header_dst_fall_back.txt"))
    assert fall.eastern_offset == dt.timedelta(hours=-4)


def test_missing_acceptance_datetime_is_a_recorded_failure() -> None:
    with pytest.raises(AcceptanceParseError) as excinfo:
        parse_acceptance_timestamp(read("submission_header_missing_acceptance.txt"))
    assert excinfo.value.reason == "missing_acceptance_datetime"


def test_malformed_acceptance_datetime_is_a_recorded_failure() -> None:
    with pytest.raises(AcceptanceParseError) as excinfo:
        parse_acceptance_timestamp(read("submission_header_malformed.txt"))
    assert excinfo.value.reason == "malformed_acceptance_datetime"


def test_non_existing_date_is_rejected() -> None:
    text = read("submission_header_standard.txt").replace("20240116163025", "20240230163025")
    with pytest.raises(AcceptanceParseError) as excinfo:
        parse_acceptance_timestamp(text)
    assert excinfo.value.reason == "malformed_acceptance_datetime"


def test_midnight_boundary_stamp_converts_to_the_previous_or_same_utc_day() -> None:
    parsed = parse_acceptance_timestamp(read("submission_header_midnight_boundary.txt"))
    assert parsed.ok
    assert parsed.local_time == dt.time(0, 0, 0)
    # 00:00:00 Eastern Standard Time on 2024-02-29 is 05:00:00 UTC the same day.
    assert parsed.utc_datetime == dt.datetime(2024, 2, 29, 5, 0, tzinfo=dt.timezone.utc)


def test_midnight_boundary_exactly_at_local_midnight_is_not_shifted_a_day() -> None:
    text = read("submission_header_standard.txt").replace("20240116163025", "20240116000000")
    parsed = parse_acceptance_timestamp(text)
    assert parsed.utc_datetime == dt.datetime(2024, 1, 16, 5, 0, tzinfo=dt.timezone.utc)
    assert parsed.local_date == dt.date(2024, 1, 16)


def test_last_second_of_the_local_day_converts_forward() -> None:
    text = read("submission_header_standard.txt").replace("20240116163025", "20240116235959")
    parsed = parse_acceptance_timestamp(text)
    assert parsed.utc_datetime == dt.datetime(2024, 1, 17, 4, 59, 59, tzinfo=dt.timezone.utc)


def test_header_pair_form_is_accepted() -> None:
    text = "ACCEPTANCE-DATETIME: 20180630163025\nFILER:\n"
    assert find_acceptance_field(text) == "20180630163025"
    parsed = parse_acceptance_timestamp(text)
    assert parsed.utc_datetime == dt.datetime(2018, 6, 30, 20, 30, 25, tzinfo=dt.timezone.utc)


def test_submissions_json_acceptance_field_is_not_used_as_a_source() -> None:
    """The submissions JSON acceptance field is not an admissible acceptance source.

    It has been documented to mix UTC and Eastern clock readings (S-41), so the
    parser must refuse it rather than silently accept a clock it cannot vouch for.
    """
    payload = '{"acceptanceDateTime": "2018-06-30T16:30:25.000Z", "cik": "0000000000"}'
    assert find_acceptance_field(payload) is None
    with pytest.raises(AcceptanceParseError) as excinfo:
        parse_acceptance_timestamp(payload)
    assert excinfo.value.reason == "missing_acceptance_datetime"


def test_safe_wrapper_reports_the_reason_without_raising() -> None:
    parsed, reason = parse_acceptance_timestamp_or_reason(read("submission_header_missing_acceptance.txt"))
    assert parsed is None
    assert reason == "missing_acceptance_datetime"


def test_header_fields_are_readable_for_form_type_and_period() -> None:
    fields = dict(iter_header_fields(read("submission_header_standard.txt")))
    assert fields["CONFORMED SUBMISSION TYPE"] == "10-K"
    assert fields["CONFORMED PERIOD OF REPORT"] == "20231231"
    assert fields["FORM TYPE"] == "10-K"


def test_format_utc_is_stable_and_rejects_naive_values() -> None:
    assert format_utc(dt.datetime(2024, 1, 16, 21, 30, 25, tzinfo=dt.timezone.utc)) == "2024-01-16T21:30:25Z"
    with pytest.raises(ValueError):
        format_utc(dt.datetime(2024, 1, 16, 21, 30, 25))

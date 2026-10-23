"""Unit tests for the read-only EDGAR acquirer.

Every case runs against an injected transport, so the test suite makes **zero**
network calls while still exercising the rate limit, the ``Retry-After``
handling, the declared User-Agent, the cache layout and the manifest writes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.data_cache import CacheLayout
from scripts.data_manifest import ManifestWriter
from scripts.sec_edgar import (
    MAX_REQUESTS_PER_SECOND,
    EdgarClient,
    EdgarConfigurationError,
    FilingIndex,
    RateLimiter,
    Response,
    build_user_agent,
    cross_check_acceptance,
    parse_filing_index,
    resolve_user_agent,
)
from scripts.sec_acceptance import parse_acceptance_timestamp

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "sec_edgar"
USER_AGENT = "AcctClock Research contact@example.org"


class FakeClock:
    """A monotonic clock that only advances when something sleeps."""

    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def time(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def make_opener(responses: dict[str, Response], calls: list[tuple[str, dict[str, str]]]):
    def opener(url: str, headers: dict[str, str]) -> Response:
        calls.append((url, headers))
        return responses.get(url, Response(status=404, body=b"not found", headers={}))

    return opener


def make_client(tmp_path: Path, responses=None, calls=None, clock=None):
    clock = clock or FakeClock()
    calls = calls if calls is not None else []
    layout = CacheLayout(root=tmp_path / "acctclock")
    layout.ensure()
    client = EdgarClient(
        layout=layout,
        user_agent=USER_AGENT,
        manifest=ManifestWriter(tmp_path / "manifests" / "sec_edgar.jsonl"),
        limiter=RateLimiter(MAX_REQUESTS_PER_SECOND, clock=clock.time, sleeper=clock.sleep),
        opener=make_opener(responses or {}, calls),
        sleeper=clock.sleep,
        clock=clock.time,
        max_retries=2,
    )
    return client, layout, calls, clock


def test_rate_limiter_caps_the_request_rate_at_two_per_second() -> None:
    clock = FakeClock()
    limiter = RateLimiter(2.0, clock=clock.time, sleeper=clock.sleep)
    stamps = [limiter.acquire() for _ in range(5)]
    assert limiter.acquisitions == 5
    # Consecutive requests are at least half a second apart, so no one-second
    # window can contain more than two requests.
    for earlier, later in zip(stamps, stamps[1:]):
        assert later - earlier >= 0.5
    assert clock.now >= 2.0


def test_rate_limiter_rejects_a_non_positive_rate() -> None:
    with pytest.raises(ValueError):
        RateLimiter(0)


def test_declared_user_agent_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ACCTCLOCK_USER_AGENT", raising=False)
    with pytest.raises(EdgarConfigurationError):
        resolve_user_agent()
    monkeypatch.setenv("ACCTCLOCK_USER_AGENT", USER_AGENT)
    assert resolve_user_agent() == USER_AGENT


def test_user_agent_builder_requires_an_organisation_and_a_contact() -> None:
    assert build_user_agent("AcctClock Research", "contact@example.org") == USER_AGENT
    with pytest.raises(EdgarConfigurationError):
        build_user_agent("", "contact@example.org")
    with pytest.raises(EdgarConfigurationError):
        build_user_agent("AcctClock Research", "")


def test_client_refuses_an_empty_user_agent(tmp_path: Path) -> None:
    with pytest.raises(EdgarConfigurationError):
        EdgarClient(layout=CacheLayout(root=tmp_path / "acctclock"), user_agent="  ")


def test_fetch_writes_the_raw_file_and_a_manifest_entry(tmp_path: Path) -> None:
    payload = (FIXTURES / "submission_header_standard.txt").read_bytes()
    url = (
        "https://www.sec.gov/Archives/edgar/data/0000000001/"
        "000000000124000001/0000000001-24-000001.txt"
    )
    client, layout, calls, _ = make_client(tmp_path, {url: Response(200, payload, {"content-type": "text/plain"})})
    target, error = client.fetch_submission_text(1, "0000000001-24-000001", "10-K")
    assert error is None
    assert target is not None
    assert target.read_bytes() == payload
    assert target.parent == layout.raw / "sec_edgar" / "0000000001" / "000000000124000001"
    assert target.name == "10-K.txt"

    records = ManifestWriter(tmp_path / "manifests" / "sec_edgar.jsonl").records()
    assert len(records) == 1
    assert records[0]["outcome"] == "success"
    assert records[0]["http_status"] == 200
    assert records[0]["sha256"]
    assert records[0]["local_path"].startswith("raw/sec_edgar/")
    assert calls[0][1]["User-Agent"] == USER_AGENT


def test_a_failed_retrieval_is_recorded_as_a_failed_retrieval(tmp_path: Path) -> None:
    url = "https://data.sec.gov/submissions/CIK0000000001.json"
    client, _layout, _calls, _clock = make_client(
        tmp_path, {url: Response(500, b"server error", {})}
    )
    target, error = client.fetch_submissions(1)
    assert target is None
    assert error == "HTTP 500"
    records = ManifestWriter(tmp_path / "manifests" / "sec_edgar.jsonl").records()
    assert records[0]["outcome"] == "failed_retrieval"
    assert records[0]["http_status"] == 500


def test_retry_after_is_honoured(tmp_path: Path) -> None:
    url = (
        "https://www.sec.gov/Archives/edgar/data/0000000001/"
        "000000000124000001/0000000001-24-000001.txt"
    )
    payload = b"<SEC-HEADER>ok</SEC-HEADER>"
    calls: list[tuple[str, dict[str, str]]] = []

    def opener(request_url: str, headers: dict[str, str]) -> Response:
        calls.append((request_url, headers))
        if len(calls) == 1:
            return Response(429, b"slow down", {"retry-after": "3"})
        return Response(200, payload, {})

    clock = FakeClock()
    layout = CacheLayout(root=tmp_path / "acctclock")
    layout.ensure()
    client = EdgarClient(
        layout=layout,
        user_agent=USER_AGENT,
        manifest=ManifestWriter(tmp_path / "manifests" / "sec_edgar.jsonl"),
        limiter=RateLimiter(MAX_REQUESTS_PER_SECOND, clock=clock.time, sleeper=clock.sleep),
        opener=opener,
        sleeper=clock.sleep,
        clock=clock.time,
        max_retries=2,
    )
    target, error = client.fetch_submission_text(1, "0000000001-24-000001", "10-K")
    assert error is None
    assert target is not None and target.read_bytes() == payload
    # The first response was throttled with Retry-After: 3, so the client waited.
    assert 3.0 in clock.sleeps
    assert len(calls) == 2


def test_retries_are_bounded(tmp_path: Path) -> None:
    url = (
        "https://www.sec.gov/Archives/edgar/data/0000000001/"
        "000000000124000001/0000000001-24-000001.txt"
    )
    client, _layout, calls, _clock = make_client(
        tmp_path, {url: Response(503, b"unavailable", {"retry-after": "1"})}
    )
    target, error = client.fetch_submission_text(1, "0000000001-24-000001", "10-K")
    assert target is None
    assert error == "HTTP 503"
    # One initial attempt plus the bounded retry budget.
    assert len(calls) == 3


def test_filing_index_is_parsed_into_the_fields_the_design_needs() -> None:
    """The directory listing carries the accession directory name."""
    payload = json.loads((FIXTURES / "filing_index_directory.json").read_text(encoding="utf-8"))
    index = parse_filing_index(payload)
    assert index.accession_number is None
    assert index.form_type is None
    assert index.period_of_report is None
    assert index.filing_date is None
    assert index.acceptance_datetime_eastern is None
    assert index.raw["directory"]["name"] == "0000000000-24-000001"


def test_filing_index_headers_html_is_parsed_into_the_fields_the_design_needs(tmp_path: Path) -> None:
    """The per-filing header block carries the fields the design needs."""
    client, _layout, _calls, _clock = make_client(Path("/tmp"))
    html = (FIXTURES / "filing_index_headers.html").read_text(encoding="utf-8")
    target = tmp_path / "index-headers.html"
    target.write_text(html, encoding="utf-8")
    index = client.parse_filing_index_headers(target)
    assert index.accession_number == "0000000000-24-000001"
    assert index.form_type == "10-K"
    assert index.period_of_report == "20231231"
    assert index.filing_date == "2024-01-16"
    assert index.acceptance_datetime_eastern == "20240116163025"


def test_acceptance_cross_check_compares_the_two_eastern_stamps(tmp_path: Path) -> None:
    text = (FIXTURES / "submission_header_standard.txt").read_text(encoding="utf-8")
    timestamp = parse_acceptance_timestamp(text)
    client, _layout, _calls, _clock = make_client(Path("/tmp"))
    html = (FIXTURES / "filing_index_headers.html").read_text(encoding="utf-8")
    header_path = tmp_path / "index-headers.html"
    header_path.write_text(html, encoding="utf-8")
    index = client.parse_filing_index_headers(header_path)
    check = cross_check_acceptance(timestamp, index)
    assert check.agree is True

    index2 = FilingIndex(
        accession_number=index.accession_number,
        form_type=index.form_type,
        period_of_report=index.period_of_report,
        filing_date=index.filing_date,
        acceptance_datetime_eastern="20240116163026",
        raw=index.raw,
    )
    mismatch = cross_check_acceptance(timestamp, index2)
    assert mismatch.agree is False
    assert mismatch.sgml_value == "20240116163025"
    assert mismatch.index_value == "20240116163026"


def test_gzip_encoded_submission_text_is_decompressed_before_parsing(tmp_path: Path) -> None:
    """EDGAR serves the complete submission text file gzip-compressed.

    The cached file is stored as received and its manifest digest is over the
    compressed bytes; only the in-memory copy used for parsing is
    decompressed, so the acceptance stamp is legible.
    """
    import gzip

    text = (FIXTURES / "submission_header_standard.txt").read_text(encoding="utf-8")
    payload = gzip.compress(text.encode("utf-8"))
    url = (
        "https://www.sec.gov/Archives/edgar/data/0000000001/"
        "000000000124000001/0000000001-24-000001.txt"
    )
    client, _layout, _calls, _clock = make_client(
        tmp_path, {url: Response(200, payload, {"content-type": "text/plain", "content-encoding": "gzip"})}
    )
    target, error = client.fetch_submission_text(1, "0000000001-24-000001", "10-K")
    assert error is None and target is not None
    # The file on disk is the compressed bytes, not the decompressed text.
    assert target.read_bytes() == payload
    timestamp, reason = client.parse_acceptance(target)
    assert reason is None
    assert timestamp is not None and timestamp.ok
    assert timestamp.utc_datetime is not None
    assert timestamp.utc_datetime.hour == 21


def test_urls_are_built_on_the_registered_hosts() -> None:
    client, _layout, _calls, _clock = make_client(Path("/tmp"))
    assert client.submissions_url(320193) == "https://data.sec.gov/submissions/CIK0000320193.json"
    assert client.filing_index_url(320193, "0000320193-18-000123") == (
        "https://www.sec.gov/Archives/edgar/data/0000320193/000032019318000123/index.json"
    )
    assert client.filing_index_headers_url(320193, "0000320193-18-000123") == (
        "https://www.sec.gov/Archives/edgar/data/0000320193/000032019318000123/"
        "0000320193-18-000123-index-headers.html"
    )
    assert client.submission_text_url(320193, "0000320193-18-000123") == (
        "https://www.sec.gov/Archives/edgar/data/0000320193/000032019318000123/"
        "0000320193-18-000123.txt"
    )

"""Unit tests for the source-document fetcher.

Every test runs with an **injected transport**: the suite makes no network
call, so it is deterministic and offline (the campaign's standing rule for the
acquisition code, D-015 and the acquisition plan §6).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.data_cache import CachePolicyError, build_layout
from scripts.data_manifest import ManifestWriter
from scripts.sec_edgar import RateLimiter, Response
from scripts.source_fetch import (
    SourceConfigurationError,
    build_user_agent,
    cache_filename,
    read_ledger_rows,
    retrieve_source,
    select_rows,
    source_cache_path,
)


def make_layout(tmp_path: Path):
    return build_layout(tmp_path / "cache").ensure()


class FakeTransport:
    """Records calls and replays a scripted list of responses."""

    def __init__(self, responses: list[Response]) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[str, dict[str, str], float]] = []

    def __call__(self, url: str, headers: dict[str, str], timeout: float) -> Response:
        self.calls.append((url, headers, timeout))
        if not self.responses:
            raise AssertionError("transport called more times than scripted")
        return self.responses.pop(0)


def ok(body: bytes = b"payload", status: int = 200, headers: dict[str, str] | None = None) -> Response:
    return Response(status=status, body=body, headers=headers or {})


def test_user_agent_is_required():
    with pytest.raises(SourceConfigurationError):
        build_user_agent("", "contact@example.org")
    with pytest.raises(SourceConfigurationError):
        build_user_agent("AcctClock Research", "")


def test_user_agent_carries_organisation_and_contact():
    agent = build_user_agent("AcctClock Research", "contact@example.org")
    assert "AcctClock Research" in agent
    assert "contact@example.org" in agent


def test_retrieve_writes_raw_payload_outside_the_repository_and_hashes_it(tmp_path):
    layout = make_layout(tmp_path)
    manifest = ManifestWriter(tmp_path / "manifest.jsonl")
    transport = FakeTransport([ok(b"hello world")])

    outcome = retrieve_source(
        "S-99",
        "https://example.org/documents/standard.pdf",
        layout=layout,
        manifest=manifest,
        user_agent="AcctClock Research (research contact: contact@example.org)",
        transport=transport,
    )

    assert outcome.ok
    assert outcome.record.http_status == 200
    assert outcome.record.bytes == len(b"hello world")
    assert outcome.record.sha256 is not None
    assert len(outcome.record.sha256) == 64
    raw = layout.raw_source("sources") / "S-99" / "standard.pdf"
    assert raw.read_bytes() == b"hello world"
    assert transport.calls[0][1]["User-Agent"].startswith("AcctClock Research")


def test_manifest_record_is_append_only_jsonl(tmp_path):
    layout = make_layout(tmp_path)
    manifest = ManifestWriter(tmp_path / "manifest.jsonl")
    transport = FakeTransport([ok(b"one"), ok(b"two")])

    for index in (1, 2):
        retrieve_source(
            f"S-9{index}",
            f"https://example.org/{index}",
            layout=layout,
            manifest=manifest,
            user_agent="AcctClock Research (research contact: contact@example.org)",
            transport=transport,
        )

    lines = (tmp_path / "manifest.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    first = json.loads(lines[0])
    assert first["source_id"] == "S-91"
    assert first["outcome"] == "success"


def test_failed_retrieval_is_recorded_as_a_failed_retrieval(tmp_path):
    layout = make_layout(tmp_path)
    manifest = ManifestWriter(tmp_path / "manifest.jsonl")
    transport = FakeTransport([ok(b"nope", status=403)])

    outcome = retrieve_source(
        "S-98",
        "https://example.org/forbidden",
        layout=layout,
        manifest=manifest,
        user_agent="AcctClock Research (research contact: contact@example.org)",
        transport=transport,
    )

    assert not outcome.ok
    assert outcome.record.outcome == "failed_retrieval"
    assert outcome.record.http_status == 403
    assert outcome.record.sha256 is None
    assert "failed retrieval" in outcome.record.notes


def test_retryable_status_is_retried_and_retry_after_is_honoured(tmp_path):
    layout = make_layout(tmp_path)
    manifest = ManifestWriter(tmp_path / "manifest.jsonl")
    waited: list[float] = []
    transport = FakeTransport(
        [
            ok(b"", status=429, headers={"retry-after": "7"}),
            ok(b"second try"),
        ]
    )

    limiter = RateLimiter(1000.0, clock=lambda: 0.0, sleeper=lambda seconds: waited.append(seconds))

    outcome = retrieve_source(
        "S-97",
        "https://example.org/throttled",
        layout=layout,
        manifest=manifest,
        user_agent="AcctClock Research (research contact: contact@example.org)",
        transport=transport,
        limiter=limiter,
    )

    assert outcome.ok
    assert outcome.attempts == 2
    assert len(transport.calls) == 2
    assert waited and waited[0] == pytest.approx(7.0)


def test_retry_budget_is_bounded(tmp_path):
    layout = make_layout(tmp_path)
    manifest = ManifestWriter(tmp_path / "manifest.jsonl")
    transport = FakeTransport(
        [
            ok(b"", status=503, headers={"retry-after": "1"}),
            ok(b"", status=503, headers={"retry-after": "1"}),
            ok(b"", status=503, headers={"retry-after": "1"}),
        ]
    )
    limiter = RateLimiter(1000.0, clock=lambda: 0.0, sleeper=lambda seconds: None)

    outcome = retrieve_source(
        "S-96",
        "https://example.org/unavailable",
        layout=layout,
        manifest=manifest,
        user_agent="AcctClock Research (research contact: contact@example.org)",
        transport=transport,
        limiter=limiter,
    )

    assert not outcome.ok
    assert len(transport.calls) == 3
    assert outcome.record.http_status == 503


def test_missing_url_is_refused(tmp_path):
    layout = make_layout(tmp_path)
    manifest = ManifestWriter(tmp_path / "manifest.jsonl")
    with pytest.raises(SourceConfigurationError):
        retrieve_source(
            "S-95",
            "   ",
            layout=layout,
            manifest=manifest,
            user_agent="AcctClock Research (research contact: contact@example.org)",
            transport=FakeTransport([]),
        )


def test_cache_root_inside_the_repository_is_refused(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])
    with pytest.raises(CachePolicyError):
        build_layout(Path(__file__).resolve().parents[1] / "cache-inside-repo")


def test_cache_filename_is_deterministic_and_safe():
    assert cache_filename("https://example.org/a/b/doc.pdf") == "doc.pdf"
    assert cache_filename("https://example.org/a/b/doc.pdf?x=1") == "doc.pdf"
    assert "/" not in cache_filename("https://example.org/weird name")


def test_source_cache_path_is_per_source(tmp_path):
    layout = make_layout(tmp_path)
    path = source_cache_path(layout, "S-76", "https://example.org/x.html")
    assert path.parent.name == "S-76"
    assert path.name == "x.html"


def test_ledger_selection_by_id():
    rows = [
        {"source_id": "S-1", "doi_or_url": "https://example.org/1"},
        {"source_id": "S-2", "doi_or_url": "https://example.org/2"},
    ]
    assert [row["source_id"] for row in select_rows(rows, ["S-2"])] == ["S-2"]
    assert [row["source_id"] for row in select_rows(rows, [])] == ["S-1", "S-2"]


def test_read_ledger_rows_returns_every_row():
    ledger = Path(__file__).resolve().parents[1] / "research" / "source_ledger.csv"
    rows = read_ledger_rows(ledger)
    assert len(rows) > 0
    assert "source_id" in rows[0]
    assert "doi_or_url" in rows[0]

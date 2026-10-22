"""Unit tests for the append-only retrieval manifest and content hashing."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.data_manifest import (
    ManifestWriter,
    sha256_bytes,
    sha256_file,
    utc_now_iso,
    verify_against_manifest,
)


def test_success_record_carries_the_sha256_of_the_raw_bytes(tmp_path: Path) -> None:
    writer = ManifestWriter(tmp_path / "sec_edgar.jsonl")
    payload = b"<SEC-HEADER>...raw bytes...\n"
    record = writer.record_success(
        source_id="SEC_EDGAR_SUBMISSION",
        url="https://www.sec.gov/Archives/edgar/data/1/0000000001-24-000001.txt",
        http_status=200,
        payload=payload,
        local_path="raw/sec_edgar/0000000001/000000000124000001/10-K.txt",
        user_agent="AcctClock Research contact@example.org",
        content_type="text/plain",
        parser_version="sec_acceptance_parser@1.0.0",
    )
    assert record.sha256 == hashlib.sha256(payload).hexdigest()
    assert record.bytes == len(payload)
    assert record.outcome == "success"

    written = writer.records()
    assert len(written) == 1
    assert written[0]["sha256"] == record.sha256
    assert written[0]["source_id"] == "SEC_EDGAR_SUBMISSION"
    assert written[0]["retrieved_utc"].endswith("Z")


def test_failed_retrieval_is_recorded_as_a_failed_retrieval(tmp_path: Path) -> None:
    writer = ManifestWriter(tmp_path / "sec_edgar.jsonl")
    writer.record_failure(
        source_id="SEC_EDGAR_SUBMISSION",
        url="https://www.sec.gov/Archives/edgar/data/1/missing.txt",
        http_status=404,
        error="HTTP 404",
        user_agent="AcctClock Research contact@example.org",
    )
    written = writer.records()
    assert written[0]["outcome"] == "failed_retrieval"
    assert written[0]["http_status"] == 404
    assert written[0]["sha256"] is None
    assert "failed retrieval" in written[0]["notes"]


def test_a_transport_error_is_recorded_with_its_exception_text(tmp_path: Path) -> None:
    writer = ManifestWriter(tmp_path / "sec_edgar.jsonl")
    writer.record_failure(
        source_id="SEC_EDGAR_SUBMISSIONS",
        url="https://data.sec.gov/submissions/CIK0000000001.json",
        http_status=None,
        error="TimeoutError: timed out",
    )
    written = writer.records()
    assert written[0]["outcome"] == "failed_retrieval"
    assert "TimeoutError" in written[0]["notes"]


def test_manifest_is_append_only(tmp_path: Path) -> None:
    path = tmp_path / "sec_edgar.jsonl"
    writer = ManifestWriter(path)
    writer.record_failure(
        source_id="X", url="https://example.org/1", http_status=500, error="HTTP 500"
    )
    first = path.read_text(encoding="utf-8")
    writer.record_success(
        source_id="X",
        url="https://example.org/2",
        http_status=200,
        payload=b"body",
        local_path="raw/x",
    )
    second = path.read_text(encoding="utf-8")
    assert second.startswith(first)
    assert len(writer.records()) == 2
    for line in second.splitlines():
        json.loads(line)


def test_verify_against_manifest_detects_a_mismatch(tmp_path: Path) -> None:
    payload = b"original bytes"
    target = tmp_path / "raw" / "file.bin"
    target.parent.mkdir(parents=True)
    target.write_bytes(payload)
    writer = ManifestWriter(tmp_path / "m.jsonl")
    writer.record_success(
        source_id="X",
        url="https://example.org/f",
        http_status=200,
        payload=payload,
        local_path=str(target),
    )
    record = writer.records()[0]
    assert verify_against_manifest(record) is True

    target.write_bytes(b"tampered bytes")
    assert verify_against_manifest(record) is False


def test_verify_against_manifest_requires_both_digest_and_path(tmp_path: Path) -> None:
    assert verify_against_manifest({"sha256": None, "local_path": None}) is False
    assert verify_against_manifest({"sha256": "abc", "local_path": None}) is False


def test_sha256_file_matches_sha256_bytes(tmp_path: Path) -> None:
    payload = b"a" * (1 << 20) + b"tail"
    target = tmp_path / "blob.bin"
    target.write_bytes(payload)
    assert sha256_file(target) == sha256_bytes(payload)


def test_utc_now_iso_is_stable() -> None:
    stamp = utc_now_iso()
    assert stamp.endswith("Z")
    assert "T" in stamp

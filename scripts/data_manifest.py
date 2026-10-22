"""Append-only retrieval manifests and content hashing for the ACCTCLOCK pipeline.

The manifest scheme is fixed by ``research/data_acquisition_plan.md`` §5 and by
decision **D-015**: the repository receives the provenance record (source, URL,
method, HTTP status, bytes, SHA-256, retrieval timestamp, user agent, local path,
parser version) while the raw payload stays in the cache outside the working tree.

Rules implemented here:

1. the SHA-256 is computed over the **raw bytes as received**, before any
   transformation, so the hash is of the file and not of the parsed rows;
2. manifests are **append-only JSONL**, one file per source;
3. a failed retrieval is recorded as a **failed retrieval** carrying the HTTP
   status and the exception text — never as an absence;
4. parsers are versioned, so a parser change is visible in the manifest.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

MANIFEST_VERSION = 1

#: Field order of a manifest record, matching the example in the acquisition plan.
FIELD_ORDER = (
    "source_id",
    "url",
    "method",
    "http_status",
    "content_type",
    "bytes",
    "sha256",
    "retrieved_utc",
    "user_agent",
    "local_path",
    "parser_version",
    "outcome",
    "notes",
)


def utc_now_iso() -> str:
    """Current UTC time in the ISO-8601 form used across the campaign."""
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(payload: bytes) -> str:
    """SHA-256 over the raw bytes as received."""
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    """SHA-256 over a file on disk, read in chunks."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass
class ManifestRecord:
    """One retrieval, successful or failed."""

    source_id: str
    url: str
    method: str = "GET"
    http_status: int | None = None
    content_type: str | None = None
    bytes: int | None = None
    sha256: str | None = None
    retrieved_utc: str = field(default_factory=utc_now_iso)
    user_agent: str | None = None
    local_path: str | None = None
    parser_version: str | None = None
    outcome: str = "success"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return {key: data[key] for key in FIELD_ORDER if key in data}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=False)


class ManifestWriter:
    """Append-only JSONL manifest writer."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def append(self, record: ManifestRecord) -> ManifestRecord:
        """Append one record, creating the parent directory when needed."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = record.to_json()
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return record

    def record_success(
        self,
        *,
        source_id: str,
        url: str,
        http_status: int,
        payload: bytes,
        local_path: str | None,
        user_agent: str | None = None,
        content_type: str | None = None,
        method: str = "GET",
        parser_version: str | None = None,
        notes: str = "",
        retrieved_utc: str | None = None,
    ) -> ManifestRecord:
        """Record a successful retrieval and its SHA-256 over the raw bytes."""
        record = ManifestRecord(
            source_id=source_id,
            url=url,
            method=method,
            http_status=http_status,
            content_type=content_type,
            bytes=len(payload),
            sha256=sha256_bytes(payload),
            retrieved_utc=retrieved_utc or utc_now_iso(),
            user_agent=user_agent,
            local_path=local_path,
            parser_version=parser_version,
            outcome="success",
            notes=notes,
        )
        return self.append(record)

    def record_failure(
        self,
        *,
        source_id: str,
        url: str,
        http_status: int | None,
        error: str,
        user_agent: str | None = None,
        method: str = "GET",
        parser_version: str | None = None,
        notes: str = "",
        retrieved_utc: str | None = None,
    ) -> ManifestRecord:
        """Record a failed retrieval.

        A failure is a **failed retrieval**, not an absence: it carries the HTTP
        status and the exception text so that the coverage report can count it.
        """
        record = ManifestRecord(
            source_id=source_id,
            url=url,
            method=method,
            http_status=http_status,
            content_type=None,
            bytes=None,
            sha256=None,
            retrieved_utc=retrieved_utc or utc_now_iso(),
            user_agent=user_agent,
            local_path=None,
            parser_version=parser_version,
            outcome="failed_retrieval",
            notes=f"failed retrieval: {error}" if not notes else f"{notes}; failed retrieval: {error}",
        )
        return self.append(record)

    def records(self) -> list[dict[str, Any]]:
        """Read every record back, in write order."""
        if not self.path.exists():
            return []
        out: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{self.path}:{number} is not valid JSON: {exc}") from exc
        return out


def verify_against_manifest(record: dict[str, Any], layout_root: Path | None = None) -> bool:
    """Re-hash a recorded artefact and compare it with the manifest digest.

    ``research/data_acquisition_plan.md`` §7 rule 1: a mismatch aborts the
    pipeline. The function returns ``True`` only when the digest matches.
    """
    digest = record.get("sha256")
    local_path = record.get("local_path")
    if not digest or not local_path:
        return False
    target = Path(local_path)
    if layout_root is not None and not target.is_absolute():
        target = Path(layout_root) / target
    if not target.exists():
        return False
    return sha256_file(target) == digest

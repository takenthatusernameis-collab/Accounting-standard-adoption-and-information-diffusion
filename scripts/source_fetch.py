"""Read-only source-document fetcher for the ACCTCLOCK source ledger.

The source ledger (``research/source_ledger.csv``) is the campaign's provenance
record: every claim about the world that the registered design relies on is
tied to a row there. A row is only as good as its evidence, and the strongest
evidence the campaign has is a **hashed retrieval record**: the URL, the HTTP
status, the byte count, the SHA-256 of the raw bytes as received and the
retrieval timestamp (decision **D-015**).

This module re-fetches the documents the ledger cites so that a cited row can
carry a fresh, verifiable retrieval record instead of an assertion. It is the
same discipline the EDGAR acquirer (``scripts/sec_edgar.py``) follows, applied
to source documents rather than to filings:

* a **declared User-Agent** identifying the requester and a contact address;
  the fetcher refuses to run without one;
* a request rate capped at **2 requests per second**;
* ``Retry-After`` honoured on a throttled or unavailable response, with a
  bounded number of retries and a bounded wait;
* every retrieval — successful or not — is written to an append-only manifest
  with the SHA-256 of the raw bytes as received;
* the **raw payload stays in the cache outside the repository working tree**
  (D-015); only the manifest is committed.

The transport is injectable and nothing here performs a network call at import
time, so the module is unit-testable with **zero network calls**.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

from .data_cache import CacheLayout, build_layout, relative_to_root
from .data_manifest import ManifestRecord, ManifestWriter
from .sec_edgar import RateLimiter, Response

#: The campaign-wide ceiling for any public web route.
MAX_REQUESTS_PER_SECOND = 2.0

#: Status codes worth retrying when the server asks us to back off.
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})

#: Upper bound on how long a single ``Retry-After`` wait may last.
MAX_RETRY_AFTER_SECONDS = 120.0

#: Bounded retry budget for a single source.
MAX_ATTEMPTS = 3

#: Cache sub-directory for source documents.
SOURCE_DIR = "sources"

#: Ledger column holding the URL of the document.
LEDGER_URL_COLUMN = "doi_or_url"

#: Ledger column holding the source identifier.
LEDGER_ID_COLUMN = "source_id"

_SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


class SourceConfigurationError(RuntimeError):
    """Raised when the fetcher is not configured in a policy-compliant way."""


class SourceRequestError(RuntimeError):
    """Raised when a retrieval fails after the bounded retry budget."""


def build_user_agent(organisation: str, contact: str) -> str:
    """Build the declared User-Agent string.

    Public web routes ask a requester to identify themselves. The campaign
    declares an organisation and a contact address; the fetcher refuses to run
    without both.
    """
    organisation = organisation.strip()
    contact = contact.strip()
    if not organisation or not contact:
        raise SourceConfigurationError(
            "A declared User-Agent with an organisation and a contact address is required; "
            "set ACCTCLOCK_USER_AGENT to e.g. 'AcctClock Research contact@example.org'."
        )
    return f"{organisation} (research contact: {contact})"


def default_transport(url: str, headers: dict[str, str], timeout: float) -> Response:
    """Perform one HTTP GET and return the response, including error statuses.

    An HTTP error status is returned as a response, not raised: a 403 or a 404
    is a **failed retrieval** that must be recorded as such, not an absence.
    """
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            return Response(
                status=int(response.status),
                body=body,
                headers={str(key).lower(): str(value) for key, value in response.headers.items()},
            )
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read()
        except Exception:  # pragma: no cover - defensive; some handlers have no body
            body = b""
        headers_map = {}
        if exc.headers is not None:
            headers_map = {str(key).lower(): str(value) for key, value in exc.headers.items()}
        return Response(status=int(exc.code), body=body, headers=headers_map)


@dataclass
class FetchOutcome:
    """The result of one source retrieval."""

    source_id: str
    url: str
    record: ManifestRecord
    payload: bytes | None
    attempts: int

    @property
    def ok(self) -> bool:
        return self.record.outcome == "success"


def cache_filename(url: str) -> str:
    """Deterministic local file name for a source document."""
    tail = url.split("://", 1)[-1]
    tail = tail.split("?", 1)[0].split("#", 1)[0]
    tail = tail.rstrip("/").rsplit("/", 1)[-1]
    safe = _SAFE_NAME.sub("_", tail).strip("_") or "document"
    return safe[:120]


def source_cache_path(layout: CacheLayout, source_id: str, url: str) -> Path:
    """The raw cache path for one source document."""
    safe_id = _SAFE_NAME.sub("_", source_id).strip("_") or "source"
    return layout.raw_source(SOURCE_DIR) / safe_id / cache_filename(url)


def _retry_after_seconds(headers: dict[str, str]) -> float | None:
    raw = headers.get("retry-after") if headers else None
    if raw is None:
        return None
    try:
        return float(str(raw).strip())
    except ValueError:
        return None


def retrieve_source(
    source_id: str,
    url: str,
    *,
    layout: CacheLayout,
    manifest: ManifestWriter,
    user_agent: str,
    transport: Callable[[str, dict[str, str], float], Response] = default_transport,
    limiter: RateLimiter | None = None,
    timeout: float = 60.0,
    parser_version: str | None = None,
    notes: str = "",
) -> FetchOutcome:
    """Fetch one source document and record the retrieval in the manifest.

    A successful retrieval writes the raw bytes to the cache (outside the
    repository) and appends a manifest record carrying the SHA-256 of those
    bytes. An unsuccessful retrieval appends a **failed retrieval** record and
    returns ``ok = False``; it is never silently dropped.
    """
    if not url.strip():
        raise SourceConfigurationError(f"{source_id}: no URL to fetch")
    if not user_agent.strip():
        raise SourceConfigurationError(f"{source_id}: a declared User-Agent is required")

    rate_limiter = limiter if limiter is not None else RateLimiter(MAX_REQUESTS_PER_SECOND)
    headers = {"User-Agent": user_agent, "Accept": "*/*"}
    last_status: int | None = None
    last_error = ""

    for attempt in range(1, MAX_ATTEMPTS + 1):
        rate_limiter.acquire()
        try:
            response = transport(url, headers, timeout)
        except Exception as exc:  # network-level failure: recorded, never raised away
            last_status = None
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt == MAX_ATTEMPTS:
                break
            continue

        last_status = response.status
        if response.status == 200:
            path = source_cache_path(layout, source_id, url)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(response.body)
            record = manifest.record_success(
                source_id=source_id,
                url=url,
                http_status=response.status,
                payload=response.body,
                local_path=relative_to_root(layout, path),
                user_agent=user_agent,
                content_type=response.headers.get("content-type"),
                parser_version=parser_version,
                notes=notes,
            )
            return FetchOutcome(
                source_id=source_id,
                url=url,
                record=record,
                payload=response.body,
                attempts=attempt,
            )

        last_error = f"HTTP {response.status}"
        if response.status not in RETRYABLE_STATUS or attempt == MAX_ATTEMPTS:
            break

        wait = _retry_after_seconds(response.headers)
        if wait is None:
            wait = float(2 ** (attempt - 1))
        wait = min(max(wait, 0.0), MAX_RETRY_AFTER_SECONDS)
        limiter_wait = getattr(rate_limiter, "_sleeper", None)
        if callable(limiter_wait):
            limiter_wait(wait)

    record = manifest.record_failure(
        source_id=source_id,
        url=url,
        http_status=last_status,
        error=last_error or "no response",
        user_agent=user_agent,
        parser_version=parser_version,
        notes=notes,
    )
    return FetchOutcome(
        source_id=source_id,
        url=url,
        record=record,
        payload=None,
        attempts=MAX_ATTEMPTS,
    )


def read_ledger_rows(path: Path) -> list[dict[str, str]]:
    """Read the source ledger into dictionaries, preserving the column order."""
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def select_rows(rows: Iterable[dict[str, str]], ids: Sequence[str] | None) -> list[dict[str, str]]:
    """Select ledger rows by source id, or all of them when ``ids`` is empty."""
    if not ids:
        return list(rows)
    wanted = {value.strip() for value in ids if value.strip()}
    return [row for row in rows if row.get(LEDGER_ID_COLUMN, "").strip() in wanted]


def _slug(url: str) -> str:
    return _SAFE_NAME.sub("_", url.split("://", 1)[-1])[:80]


def main(argv: list[str] | None = None) -> int:
    """Re-fetch cited source documents and write the retrieval manifest."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ledger",
        default="research/source_ledger.csv",
        help="the source ledger whose rows are fetched",
    )
    parser.add_argument(
        "--ids",
        default="",
        help="comma-separated source ids to fetch; empty means every row",
    )
    parser.add_argument(
        "--manifest",
        default="research/manifests/source_ledger_verification.jsonl",
        help="append-only manifest path for the retrieval records",
    )
    parser.add_argument(
        "--cache-root",
        default=None,
        help="cache root for the raw payloads; must be outside the repository (D-015)",
    )
    parser.add_argument(
        "--user-agent",
        default=None,
        help="declared User-Agent; defaults to $ACCTCLOCK_USER_AGENT",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="free-text note recorded on every manifest record",
    )
    args = parser.parse_args(argv)

    raw_agent = args.user_agent or os.environ.get("ACCTCLOCK_USER_AGENT", "")
    if ":" in raw_agent and "(" in raw_agent:
        user_agent = raw_agent
    else:
        organisation, _, contact = raw_agent.partition(" ")
        user_agent = build_user_agent(organisation, contact)

    rows = select_rows(read_ledger_rows(Path(args.ledger)), args.ids.split(",") if args.ids else [])
    if not rows:
        print("no ledger rows selected")
        return 1

    layout = build_layout(args.cache_root).ensure()
    manifest = ManifestWriter(Path(args.manifest))
    outcomes: list[FetchOutcome] = []
    for row in rows:
        source_id = (row.get(LEDGER_ID_COLUMN) or "").strip()
        url = (row.get(LEDGER_URL_COLUMN) or "").strip()
        if not source_id or not url:
            print(f"skipping row without an id or url: {source_id!r}")
            continue
        outcome = retrieve_source(
            source_id,
            url,
            layout=layout,
            manifest=manifest,
            user_agent=user_agent,
            notes=args.notes or f"source-ledger re-verification of {_slug(url)}",
        )
        outcomes.append(outcome)
        print(
            f"{source_id} {outcome.record.outcome} "
            f"status={outcome.record.http_status} bytes={outcome.record.bytes} "
            f"sha256={outcome.record.sha256} {url}"
        )

    failures = [outcome for outcome in outcomes if not outcome.ok]
    print(f"retrieved {len(outcomes) - len(failures)} of {len(outcomes)} sources")
    return 0 if not failures else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

"""Read-only EDGAR acquirer for the ACCTCLOCK campaign.

This module is the spine of the data plan
(``research/data_acquisition_plan.md`` §6.1). It is written so that the whole
acquisition path is **verifiable offline**: the transport is injectable, the
rate limiter is deterministic under an injected clock, and nothing in this file
performs a network call at import time.

What it fetches, per the registered plan:

* ``data.sec.gov/submissions/CIK##########.json`` — the submissions JSON, used
  **only** for identifier history. Its ``acceptanceDateTime`` field is
  deliberately **not** used for the acceptance time: it has been documented to
  mix UTC and Eastern clock readings (S-41), and the registered design pins the
  parse to the raw SGML header (``research/specification_v1.1.md`` §2).
* ``www.sec.gov/Archives/edgar/data/<cik>/<accession>/index.json`` — the filing
  index, a directory listing of every file in the accession; it is cached at
  the plan's path ``raw/sec_edgar/<cik>/<accession-nodashes>/index.json`` and
  the manifest records the exact URL that produced it.
* ``www.sec.gov/Archives/edgar/data/<cik>/<accession>/<accession>-index-headers.html``
  — the per-filing header block, carrying the form type, the period of report
  and the acceptance stamp in Eastern clock. The legacy ``index-headers.json``
  document is no longer served by EDGAR.
* ``www.sec.gov/Archives/edgar/data/<cik>/<accession>/<accession>.txt`` — the
  complete submission text file, whose SGML header is the authoritative source
  of the acceptance timestamp.

Compliance rules implemented here:

* a **declared User-Agent** identifying the requester and a contact address,
  which the SEC requires. The acquirer refuses to run without one.
* a request rate capped at **2 requests per second**, well inside the SEC's
  stated ceiling of 10, with a deterministic spacing limiter.
* ``Retry-After`` is honoured on a throttled or unavailable response, with a
  bounded number of retries and a bounded wait.
* every retrieval — successful or not — is written to an append-only manifest
  with the SHA-256 of the raw bytes as received.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .data_cache import CacheLayout, relative_to_root, sec_edgar_paths
from .data_manifest import ManifestWriter, utc_now_iso
from .sec_acceptance import (
    AcceptanceParseError,
    AcceptanceTimestamp,
    format_utc,
    iter_header_fields,
    parse_acceptance_timestamp,
)

SEC_ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data"
DATA_SEC_BASE = "https://data.sec.gov"

#: The SEC's ceiling is 10 requests per second; the plan caps the pipeline at 2.
MAX_REQUESTS_PER_SECOND = 2.0

#: Status codes that are worth retrying when the server asks us to back off.
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})

#: Upper bound on how long a single ``Retry-After`` wait may last.
MAX_RETRY_AFTER_SECONDS = 120.0

FILING_INDEX_SOURCE = "index.json"

#: The header block for one filing now lives in a separate HTML file named
#: ``<accession>-index-headers.html`` inside the accession directory. The
#: legacy ``index-headers.json`` document is no longer served by EDGAR (it
#: returns HTTP 404 after the 2025-10-31 re-format), so the acquirer reads
#: the header fields from this file and the directory listing from
#: :data:`FILING_INDEX_SOURCE` below.
FILING_INDEX_HEADERS_HTML = "index-headers.html"


def _decompress_text(payload: bytes) -> str:
    """Return the payload as text, transparently handling EDGAR's gzip encoding.

    EDGAR serves the complete submission text file with ``Content-Encoding:
    gzip`` even though the URL ends in ``.txt``. The raw bytes are hashed and
    cached as received; only the in-memory copy used for parsing is
    decompressed, so the manifest digest always matches the file on disk.
    """
    if payload[:2] == b"\x1f\x8b":
        import gzip

        try:
            payload = gzip.decompress(payload)
        except OSError:
            pass
    return payload.decode("utf-8", errors="replace")


class EdgarConfigurationError(RuntimeError):
    """Raised when the acquirer is not configured in a policy-compliant way."""


class EdgarRequestError(RuntimeError):
    """Raised when a retrieval fails after the bounded retry budget."""


@dataclass
class Response:
    """A minimal transport response."""

    status: int
    body: bytes
    headers: dict[str, str]
    decompressed: bytes | None = None


class RateLimiter:
    """Strict spacing rate limiter.

    Requests are spaced at least ``1 / max_rate_per_second`` seconds apart, so
    the achieved rate can never exceed the configured ceiling. The clock and the
    sleep function are injectable so the behaviour is unit-testable without
    waiting in real time.
    """

    def __init__(
        self,
        max_rate_per_second: float = MAX_REQUESTS_PER_SECOND,
        clock: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        if max_rate_per_second <= 0:
            raise ValueError("max_rate_per_second must be positive")
        self.max_rate_per_second = float(max_rate_per_second)
        self.interval = 1.0 / self.max_rate_per_second
        self._clock = clock
        self._sleeper = sleeper
        self._next_allowed: float | None = None
        self.acquisitions = 0
        self.total_wait = 0.0

    def acquire(self) -> float:
        """Block until the next request may be issued. Returns the timestamp."""
        now = self._clock()
        if self._next_allowed is None:
            self._next_allowed = now
        if now < self._next_allowed:
            wait = self._next_allowed - now
            self.total_wait += wait
            self._sleeper(wait)
            now = self._next_allowed
        self._next_allowed = now + self.interval
        self.acquisitions += 1
        return now


def build_user_agent(organisation: str, contact: str) -> str:
    """Build the SEC-compliant declared User-Agent string.

    The SEC asks for an organisation name and a contact address, for example
    ``"AcctClock Research contact@example.org"``.
    """
    organisation = organisation.strip()
    contact = contact.strip()
    if not organisation or not contact:
        raise EdgarConfigurationError(
            "A declared User-Agent with an organisation and a contact address is required "
            "by SEC policy; set ACCTCLOCK_USER_AGENT to e.g. "
            "'AcctClock Research contact@example.org'."
        )
    return f"{organisation} {contact}"


def resolve_user_agent(env: dict[str, str] | None = None) -> str:
    """Read the declared User-Agent from the environment.

    The acquirer refuses to run without one rather than sending an anonymous
    request to a regulator's server.
    """
    import os

    environ = os.environ if env is None else env
    value = (environ.get("ACCTCLOCK_USER_AGENT") or "").strip()
    if not value:
        raise EdgarConfigurationError(
            "ACCTCLOCK_USER_AGENT is not set. SEC policy requires a declared User-Agent "
            "identifying the requester and a contact address."
        )
    return value


@dataclass(frozen=True)
class FilingIndex:
    """The filing-index fields the design needs."""

    accession_number: str | None
    form_type: str | None
    period_of_report: str | None
    filing_date: str | None
    acceptance_datetime_eastern: str | None
    raw: dict[str, Any]


def parse_filing_index(payload: dict[str, Any]) -> FilingIndex:
    """Read the filing-index fields out of an ``index-headers.json`` payload."""
    headers = payload.get("headers") or {}
    if not isinstance(headers, dict):
        headers = {}
    return FilingIndex(
        accession_number=headers.get("accession-number"),
        form_type=headers.get("form") or headers.get("type"),
        period_of_report=headers.get("period"),
        filing_date=headers.get("filing-date"),
        acceptance_datetime_eastern=headers.get("acceptance-datetime"),
        raw=payload,
    )


@dataclass(frozen=True)
class AcceptanceCrossCheck:
    """Comparison of the SGML-header stamp with the filing-index stamp."""

    agree: bool
    sgml_value: str | None
    index_value: str | None


def cross_check_acceptance(
    timestamp: AcceptanceTimestamp | None, index: FilingIndex | None
) -> AcceptanceCrossCheck:
    """Compare the two Eastern-clock stamps available for one filing.

    Both sources are Eastern clock. A disagreement is recorded as a data-quality
    finding; the SGML header stays authoritative because the registered design
    pins the parse to it.
    """
    sgml_value = timestamp.raw_value if timestamp is not None else None
    index_value = index.acceptance_datetime_eastern if index is not None else None
    if sgml_value is None or index_value is None:
        return AcceptanceCrossCheck(agree=False, sgml_value=sgml_value, index_value=index_value)
    return AcceptanceCrossCheck(
        agree=sgml_value == index_value, sgml_value=sgml_value, index_value=index_value
    )


class EdgarClient:
    """A read-only EDGAR client that records everything it retrieves."""

    def __init__(
        self,
        layout: CacheLayout,
        user_agent: str,
        manifest: ManifestWriter | None = None,
        limiter: RateLimiter | None = None,
        opener: Callable[[str, dict[str, str]], Response] | None = None,
        sleeper: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        max_retries: int = 3,
    ) -> None:
        if not user_agent.strip():
            raise EdgarConfigurationError("A declared User-Agent is required.")
        self.layout = layout
        self.user_agent = user_agent
        self.manifest = manifest or ManifestWriter(layout.manifest_path("sec_edgar"))
        self.limiter = limiter or RateLimiter(MAX_REQUESTS_PER_SECOND, clock=clock, sleeper=sleeper)
        self._opener = opener or self._default_opener
        self._sleeper = sleeper
        self.max_retries = max(0, int(max_retries))
        self.requests = 0

    # -- transport ---------------------------------------------------------

    @staticmethod
    def _decompress(body: bytes, headers: dict[str, str]) -> bytes:
        """Return the payload in a form the parsers can read.

        EDGAR serves the complete submission text file with ``Content-Encoding:
        gzip`` even though the URL ends in ``.txt``, and the SGML header is only
        legible after decompression. The raw bytes are hashed and cached as
        received; only the in-memory copy used for parsing is decompressed.
        """
        encoding = (headers.get("content-encoding") or "").lower()
        if encoding != "gzip":
            return body
        try:
            return gzip.decompress(body)
        except OSError:
            return body

    @staticmethod
    def _default_opener(url: str, headers: dict[str, str]) -> Response:
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read()
                norm_headers = {k.lower(): v for k, v in response.headers.items()}
                return Response(
                    status=response.status,
                    body=body,
                    headers=norm_headers,
                )
        except urllib.error.HTTPError as exc:
            return Response(
                status=exc.code,
                body=exc.read() if exc.fp is not None else b"",
                headers={k.lower(): v for k, v in (exc.headers or {}).items()},
            )

    def _request(self, url: str) -> Response:
        """Issue one request, honouring the rate limit and ``Retry-After``."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept-Encoding": "gzip, deflate",
        }
        attempt = 0
        while True:
            self.limiter.acquire()
            self.requests += 1
            response = self._opener(url, headers)
            response.decompressed = self._decompress(response.body, response.headers)
            if response.status not in RETRYABLE_STATUS:
                return response
            if attempt >= self.max_retries:
                return response
            wait = self._retry_after_seconds(response, attempt)
            attempt += 1
            self._sleeper(wait)

    @staticmethod
    def _retry_after_seconds(response: Response, attempt: int) -> float:
        """Honour ``Retry-After``; fall back to a bounded exponential back-off."""
        raw = response.headers.get("retry-after")
        if raw:
            try:
                return min(MAX_RETRY_AFTER_SECONDS, max(0.0, float(raw)))
            except ValueError:
                pass
        return min(MAX_RETRY_AFTER_SECONDS, float(2**attempt))

    # -- retrieval ---------------------------------------------------------

    def _store(
        self,
        *,
        source_id: str,
        url: str,
        target: Path,
        parser_version: str | None = None,
        notes: str = "",
    ) -> tuple[Response | None, str | None]:
        """Fetch one artefact, cache it and record the manifest entry."""
        try:
            response = self._request(url)
        except Exception as exc:  # noqa: BLE001 - recorded as a failed retrieval
            self.manifest.record_failure(
                source_id=source_id,
                url=url,
                http_status=None,
                error=f"{type(exc).__name__}: {exc}",
                user_agent=self.user_agent,
                parser_version=parser_version,
                notes=notes,
            )
            return None, f"{type(exc).__name__}: {exc}"

        if response.status != 200:
            error = f"HTTP {response.status}"
            self.manifest.record_failure(
                source_id=source_id,
                url=url,
                http_status=response.status,
                error=error,
                user_agent=self.user_agent,
                parser_version=parser_version,
                notes=notes,
            )
            return response, error

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(response.body)
        self.manifest.record_success(
            source_id=source_id,
            url=url,
            http_status=response.status,
            payload=response.body,
            local_path=relative_to_root(self.layout, target),
            user_agent=self.user_agent,
            content_type=response.headers.get("content-type"),
            parser_version=parser_version,
            notes=notes,
        )
        return response, None

    # -- public API --------------------------------------------------------

    def submissions_url(self, cik: int | str) -> str:
        return f"{DATA_SEC_BASE}/submissions/CIK{int(cik):010d}.json"

    def filing_index_url(self, cik: int | str, accession: str) -> str:
        return (
            f"{SEC_ARCHIVES_BASE}/{int(cik):010d}/"
            f"{accession.replace('-', '')}/{FILING_INDEX_SOURCE}"
        )

    def filing_index_headers_url(self, cik: int | str, accession: str) -> str:
        return (
            f"{SEC_ARCHIVES_BASE}/{int(cik):010d}/"
            f"{accession.replace('-', '')}/{accession}-index-headers.html"
        )

    def submission_text_url(self, cik: int | str, accession: str) -> str:
        return (
            f"{SEC_ARCHIVES_BASE}/{int(cik):010d}/"
            f"{accession.replace('-', '')}/{accession}.txt"
        )

    def fetch_submissions(self, cik: int | str) -> tuple[Path | None, str | None]:
        """Fetch the submissions JSON (identifier history only)."""
        paths = sec_edgar_paths(self.layout, cik, "0")
        url = self.submissions_url(cik)
        _, error = self._store(
            source_id="SEC_EDGAR_SUBMISSIONS",
            url=url,
            target=paths["submissions"],
            parser_version="sec_acceptance_parser@1.0.0",
            notes=(
                "identifier history only; the acceptanceDateTime field of this payload is "
                "not used for the acceptance time (S-41)"
            ),
        )
        if error:
            return None, error
        return paths["submissions"], None

    def fetch_filing_index(self, cik: int | str, accession: str) -> tuple[Path | None, str | None]:
        """Fetch the accession directory listing (``index.json``).

        This is the directory manifest for one filing: it lists every file in
        the accession directory, including the ``<accession>-index-headers.html``
        file that carries the form type, period of report and acceptance stamp.
        The legacy ``index-headers.json`` document is no longer served by EDGAR,
        so the header fields themselves come from :meth:`fetch_filing_index_headers`.
        """
        paths = sec_edgar_paths(self.layout, cik, accession)
        url = self.filing_index_url(cik, accession)
        _, error = self._store(
            source_id="SEC_EDGAR_FILING_INDEX",
            url=url,
            target=paths["index"],
            parser_version="sec_acceptance_parser@1.0.0",
            notes=(
                f"filing index payload is the SEC {FILING_INDEX_SOURCE} directory listing: "
                "the file inventory for one accession, including the header HTML"
            ),
        )
        if error:
            return None, error
        return paths["index"], None

    def fetch_filing_index_headers(self, cik: int | str, accession: str) -> tuple[Path | None, str | None]:
        """Fetch the per-filing header block (``<accession>-index-headers.html``).

        The header block carries the form type, the period of report, the filing
        date and the acceptance stamp in Eastern clock, and it is the same block
        that the complete submission text file's SGML header duplicates. The
        acquirer reads it from this file rather than from the submissions JSON,
        whose ``acceptanceDateTime`` field mixes UTC and Eastern clock (S-41).
        """
        paths = sec_edgar_paths(self.layout, cik, accession)
        url = self.filing_index_headers_url(cik, accession)
        _, error = self._store(
            source_id="SEC_EDGAR_FILING_INDEX_HEADERS",
            url=url,
            target=paths["index_headers"],
            parser_version="sec_acceptance_parser@1.0.0",
            notes=(
                "the SEC per-filing header block: form type, period of report, filing date "
                "and the acceptance stamp in Eastern clock"
            ),
        )
        if error:
            return None, error
        return paths["index_headers"], None

    def parse_filing_index_headers(self, html_path: Path) -> FilingIndex:
        """Read the header fields out of a cached ``<accession>-index-headers.html`` file.

        The file wraps the SGML header block in an HTML comment. EDGAR serves it
        gzip-compressed even though the URL ends in ``.html``, so the cached raw
        bytes are decompressed for parsing while the manifest digest stays over
        the compressed bytes. The fields are the same ``NAME: value`` pairs
        that :func:`scripts.sec_acceptance.iter_header_fields` reads from the
        submission text header, so the two sources stay in lock-step.
        """
        text = _decompress_text(Path(html_path).read_bytes())
        start = text.find("<SEC-HEADER>")
        end = text.find("</SEC-HEADER>")
        if start == -1 or end == -1:
            raise EdgarConfigurationError(
                f"{html_path} does not contain a <SEC-HEADER> block"
            )
        block = text[start + len("<SEC-HEADER>"):end]
        fields = dict(iter_header_fields(block))
        return FilingIndex(
            accession_number=fields.get("ACCESSION-NUMBER"),
            form_type=fields.get("TYPE") or fields.get("FORM-TYPE"),
            period_of_report=fields.get("PERIOD"),
            filing_date=fields.get("FILING-DATE"),
            acceptance_datetime_eastern=fields.get("ACCEPTANCE-DATETIME"),
            raw=fields,
        )

    def fetch_submission_text(self, cik: int | str, accession: str, form: str) -> tuple[Path | None, str | None]:
        """Fetch the complete submission text file for one accession."""
        paths = sec_edgar_paths(self.layout, cik, accession)
        target = paths["submission_text"].with_name(f"{form}.txt")
        url = self.submission_text_url(cik, accession)
        _, error = self._store(
            source_id="SEC_EDGAR_SUBMISSION",
            url=url,
            target=target,
            parser_version="sec_acceptance_parser@1.0.0",
            notes="complete submission text file; the SGML header carries ACCEPTANCE-DATETIME",
        )
        if error:
            return None, error
        return target, None

    def parse_acceptance(self, submission_text_path: Path) -> tuple[AcceptanceTimestamp | None, str | None]:
        """Parse the acceptance stamp out of a cached complete submission text file.

        The cached file is stored as received, which for EDGAR means gzip
        compressed; the parser reads the decompressed text so that the SGML
        header is legible.
        """
        raw = Path(submission_text_path).read_bytes()
        text = _decompress_text(raw)
        try:
            return parse_acceptance_timestamp(text), None
        except AcceptanceParseError as exc:
            return None, exc.reason


def utc_now() -> str:
    """Current UTC time in ISO-8601 (``Z``) form."""
    return utc_now_iso()


def describe_timestamp(timestamp: AcceptanceTimestamp) -> str:
    """Render a parsed acceptance timestamp for a manifest note."""
    if timestamp.utc_datetime is not None:
        return format_utc(timestamp.utc_datetime)
    if timestamp.ambiguous:
        candidates = ", ".join(format_utc(value) for value in timestamp.candidate_utc_datetimes)
        return f"ambiguous local time {timestamp.local_date} {timestamp.local_time} [{candidates}]"
    return f"nonexistent local time {timestamp.local_date} {timestamp.local_time}"


def load_json(path: Path) -> dict[str, Any]:
    """Read a cached JSON artefact.

    EDGAR serves the accession directory listing with ``Content-Encoding:
    gzip``, so a cached ``index.json`` may be compressed on disk. The raw bytes
    are hashed as received; this reader decompresses only for parsing.
    """
    payload = Path(path).read_bytes()
    if payload[:2] == b"\x1f\x8b":
        import gzip

        try:
            payload = gzip.decompress(payload)
        except OSError:
            pass
    return json.loads(payload.decode("utf-8", errors="replace"))


def utc_date_stamp(moment: dt.datetime | None = None) -> str:
    """``YYYY-MM-DD`` stamp for the manifest notes."""
    moment = moment or dt.datetime.now(dt.timezone.utc)
    return moment.date().isoformat()

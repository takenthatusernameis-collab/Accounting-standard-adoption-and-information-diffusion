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
* ``www.sec.gov/Archives/edgar/data/<cik>/<accession>/index-headers.json`` — the
  filing index. Its payload carries the form type, the period of report and the
  acceptance stamp in Eastern clock; it is cached at the plan's path
  ``raw/sec_edgar/<cik>/<accession-nodashes>/index.json`` and the manifest
  records the exact URL that produced it.
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

FILING_INDEX_SOURCE = "index-headers.json"


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
    def _default_opener(url: str, headers: dict[str, str]) -> Response:
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return Response(
                    status=response.status,
                    body=response.read(),
                    headers={k.lower(): v for k, v in response.headers.items()},
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
        """Fetch the filing index for one accession."""
        paths = sec_edgar_paths(self.layout, cik, accession)
        url = self.filing_index_url(cik, accession)
        _, error = self._store(
            source_id="SEC_EDGAR_FILING_INDEX",
            url=url,
            target=paths["index"],
            parser_version="sec_acceptance_parser@1.0.0",
            notes=(
                f"filing index payload is the SEC {FILING_INDEX_SOURCE} document: form type, "
                "period of report and the acceptance stamp in Eastern clock"
            ),
        )
        if error:
            return None, error
        return paths["index"], None

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
        """Parse the acceptance stamp out of a cached complete submission text file."""
        text = Path(submission_text_path).read_text(encoding="utf-8", errors="replace")
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
    """Read a cached JSON artefact."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def utc_date_stamp(moment: dt.datetime | None = None) -> str:
    """``YYYY-MM-DD`` stamp for the manifest notes."""
    moment = moment or dt.datetime.now(dt.timezone.utc)
    return moment.date().isoformat()

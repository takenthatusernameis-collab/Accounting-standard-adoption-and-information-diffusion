"""Parse the SEC EDGAR acceptance timestamp out of a raw SGML submission header.

Why this module exists
----------------------
The ACCTCLOCK design needs a **public, exact, UTC** filing timestamp for two events:
``T-R`` (the firm's first full report published under a standard, the primary exit)
and ``T-RI`` (the first interim report under the standard, the pre-emption window).
A fiscal-period end is not a timestamp and cannot be traded against, so the
acceptance timestamp is the only admissible source.

The EDGAR ``data.sec.gov`` submissions JSON carries an ``acceptanceDateTime``
field that has been documented to mix UTC and Eastern clock readings (S-41). The
registered design therefore pins the parse to the **raw SGML header** of the
complete submission text file, where ``ACCEPTANCE-DATETIME`` is a fixed-width
``YYYYMMDDHHMMSS`` value in **Eastern Time**
(``research/specification_v1.1.md`` §2; ``research/data_acquisition_plan.md`` §6.1).

Eastern Time is not a fixed offset. The conversion below resolves the offset that
is in effect at the *local* wall time of the acceptance stamp, which means the two
annual transitions have to be handled explicitly:

* **Spring forward** — the local hour 02:00-02:59 does not exist on the
  transition date. A stamp inside that hour is **nonexistent** and is quarantined.
* **Fall back** — the local hour 01:00-01:59 happens twice on the transition date.
  A stamp inside that hour is **ambiguous** and is quarantined with *both* candidate
  UTC readings recorded, because the EDGAR header does not disambiguate them.

A quarantined stamp is never silently resolved and never defaulted to an assumed
offset; it is recorded, counted, and reported
(``research/data_acquisition_plan.md`` §7 rule 2).

This module performs **no network access** and has no third-party dependencies.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from typing import Iterable
from zoneinfo import ZoneInfo

PARSER_VERSION = "sec_acceptance_parser@1.0.0"

EASTERN = ZoneInfo("America/New_York")
UTC = dt.timezone.utc

ACCEPTANCE_FIELD = "ACCEPTANCE-DATETIME"

#: The field is a single fixed-width stamp inside the SGML header block. EDGAR
#: writes it as an opening tag with the value on the same line and no closing
#: tag, for example ``<ACCEPTANCE-DATETIME>20240116163025``.
_ANY_TAG_RE = re.compile(r"<" + ACCEPTANCE_FIELD + r">\s*([^\s<]*)")


class AcceptanceParseError(ValueError):
    """Raised when the acceptance timestamp cannot be read at all.

    ``reason`` is a stable machine-readable code so that failures are counted by
    category rather than collapsed into one bucket.
    """

    def __init__(self, reason: str, message: str) -> None:
        super().__init__(message)
        self.reason = reason


@dataclass(frozen=True)
class AcceptanceTimestamp:
    """The result of reading one EDGAR acceptance stamp.

    ``utc_datetime`` is ``None`` when the local wall time does not exist or is
    ambiguous on the US daylight-saving transition date. The candidate readings
    are always populated in that case so the quarantine is auditable.
    """

    raw_value: str
    local_date: dt.date
    local_time: dt.time
    eastern_offset: dt.timedelta | None
    utc_datetime: dt.datetime | None
    ambiguous: bool = False
    nonexistent: bool = False
    candidate_utc_datetimes: tuple[dt.datetime, ...] = field(default_factory=tuple)
    source: str = "sgml_header"

    @property
    def ok(self) -> bool:
        """True when a single UTC reading could be determined."""
        return self.utc_datetime is not None

    @property
    def quarantine_reason(self) -> str | None:
        if self.nonexistent:
            return "nonexistent_local_time"
        if self.ambiguous:
            return "ambiguous_local_time"
        return None


def find_acceptance_field(text: str) -> str | None:
    """Return the raw ``ACCEPTANCE-DATETIME`` value, or ``None`` when absent.

    Both spellings are accepted because the complete submission text file uses the
    tag form ``<ACCEPTANCE-DATETIME>...`` while a header rendered on its own uses
    the ``ACCEPTANCE-DATETIME: ...`` pair form. The value is returned verbatim so
    that a malformed stamp is distinguishable from an absent field.
    """
    match = _ANY_TAG_RE.search(text)
    if match and match.group(1):
        return match.group(1)
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith(ACCEPTANCE_FIELD + ":"):
            value = stripped.split(":", 1)[1].strip()
            if value:
                return value
    return None


def _local_to_utc_candidates(local: dt.datetime) -> tuple[tuple[dt.datetime, ...], bool]:
    """Return the UTC readings for a local Eastern wall time.

    The second element of the return value is ``True`` when the local wall time
    is ambiguous (it occurs twice on a fall-back date).
    """
    first = local.replace(tzinfo=EASTERN, fold=0)
    second = local.replace(tzinfo=EASTERN, fold=1)
    if first.utcoffset() == second.utcoffset():
        return (first.astimezone(UTC),), False
    return (first.astimezone(UTC), second.astimezone(UTC)), True


def _is_nonexistent(local: dt.datetime) -> bool:
    """True when the local wall time falls in the spring-forward gap."""
    first = local.replace(tzinfo=EASTERN, fold=0)
    # A nonexistent local time round-trips to a different wall clock time.
    return first.astimezone(UTC).astimezone(EASTERN).replace(tzinfo=None) != local


def parse_acceptance_timestamp(text: str) -> AcceptanceTimestamp:
    """Parse the acceptance stamp from a complete submission text file.

    Raises
    ------
    AcceptanceParseError
        With ``reason`` ``"missing_acceptance_datetime"`` when the header does not
        carry the field, and ``"malformed_acceptance_datetime"`` when the value is
        not a 14-digit ``YYYYMMDDHHMMSS`` stamp or is not a real date and time.
    """
    raw = find_acceptance_field(text)
    if raw is None:
        raise AcceptanceParseError(
            "missing_acceptance_datetime",
            f"No <{ACCEPTANCE_FIELD}> field found in the SGML header.",
        )
    if len(raw) != 14 or not raw.isdigit():
        raise AcceptanceParseError(
            "malformed_acceptance_datetime",
            f"{ACCEPTANCE_FIELD} value {raw!r} is not a 14-digit YYYYMMDDHHMMSS stamp.",
        )
    try:
        naive = dt.datetime.strptime(raw, "%Y%m%d%H%M%S")
    except ValueError as exc:
        raise AcceptanceParseError(
            "malformed_acceptance_datetime",
            f"{ACCEPTANCE_FIELD} value {raw!r} is not a valid date and time: {exc}",
        ) from exc

    if _is_nonexistent(naive):
        # The wall time does not exist on this date; the header cannot be trusted.
        offset = naive.replace(tzinfo=EASTERN, fold=0).utcoffset()
        return AcceptanceTimestamp(
            raw_value=raw,
            local_date=naive.date(),
            local_time=naive.time(),
            eastern_offset=offset,
            utc_datetime=None,
            ambiguous=False,
            nonexistent=True,
            candidate_utc_datetimes=(),
        )

    candidates, ambiguous = _local_to_utc_candidates(naive)
    if ambiguous:
        offset = naive.replace(tzinfo=EASTERN, fold=0).utcoffset()
        return AcceptanceTimestamp(
            raw_value=raw,
            local_date=naive.date(),
            local_time=naive.time(),
            eastern_offset=offset,
            utc_datetime=None,
            ambiguous=True,
            nonexistent=False,
            candidate_utc_datetimes=candidates,
        )

    return AcceptanceTimestamp(
        raw_value=raw,
        local_date=naive.date(),
        local_time=naive.time(),
        eastern_offset=naive.replace(tzinfo=EASTERN).utcoffset(),
        utc_datetime=candidates[0],
        ambiguous=False,
        nonexistent=False,
        candidate_utc_datetimes=candidates,
    )


def format_utc(value: dt.datetime) -> str:
    """Render a UTC timestamp in the ISO-8601 form used across the campaign."""
    if value.tzinfo is None:
        raise ValueError("naive datetimes are not accepted; timestamps are UTC")
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_acceptance_timestamp_or_reason(text: str) -> tuple[AcceptanceTimestamp | None, str | None]:
    """Non-raising wrapper: return ``(timestamp, error_reason)``."""
    try:
        return parse_acceptance_timestamp(text), None
    except AcceptanceParseError as exc:
        return None, exc.reason


def iter_header_fields(text: str) -> Iterable[tuple[str, str]]:
    """Yield the ``NAME: value`` pairs of an EDGAR SGML header block.

    Used by the acquirer to read the form type, the period of report and the
    filer identity from the same header that carries the acceptance stamp, so
    that every filing attribute comes from one authoritative block.
    """
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("<"):
            continue
        if ":" not in stripped:
            continue
        name, _, value = stripped.partition(":")
        name = name.strip()
        if not name or len(name) > 60:
            continue
        if not all(character.isalnum() or character in " -/" for character in name):
            continue
        yield name, value.strip()

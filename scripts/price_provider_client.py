"""Paid price-provider adapters for ACCTCLOCK.

The client is read-only and disabled by default. It supports Sharadar's stock
price table for US active/delisted securities and EODHD historical EOD prices
for international coverage. API keys are read only from environment variables;
never commit them, print them, or write them to manifests.

No network calls occur at import time. A real request requires
ACCTCLOCK_ENABLE_PAID_DATA=1 plus the relevant provider credential. Raw
responses are written outside the repository through the registered cache and
manifest policy before parsing, so malformed responses remain auditable.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from .data_cache import CacheLayout, build_layout, relative_to_root
from .data_manifest import ManifestWriter, sha256_bytes

PARSER_VERSION = "price_provider_parser@1.0.0"
USER_AGENT = "ACCTCLOCK research (read-only historical price acquisition)"
DEFAULT_TIMEOUT_SECONDS = 30
MAX_RESPONSE_BYTES = 100 * 1024 * 1024


class PriceProviderConfigurationError(RuntimeError):
    """Raised when a paid request was not explicitly enabled or configured."""


class PriceProviderRequestError(RuntimeError):
    """Raised when a provider request fails; the secret is never included."""


class PriceProviderDataError(ValueError):
    """Raised when a price response is malformed or fails integrity checks."""


@dataclass(frozen=True)
class PriceBar:
    ticker: str
    date: dt.date
    open: float | None
    high: float | None
    low: float | None
    close: float
    adjusted_close: float | None
    volume: float | None
    provider: str


def _iso_date(value: str, field: str) -> str:
    try:
        parsed = dt.date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be YYYY-MM-DD") from exc
    if parsed.isoformat() != value:
        raise ValueError(f"{field} must be YYYY-MM-DD")
    return value


def _number(value: Any, field: str, *, required: bool = False) -> float | None:
    if value is None or str(value).strip() in {"", "None", "null", "NA", "N/A"}:
        if required:
            raise PriceProviderDataError(f"missing required numeric field {field}")
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise PriceProviderDataError(f"invalid numeric field {field}") from exc
    if not math.isfinite(parsed):
        raise PriceProviderDataError(f"non-finite numeric field {field}")
    return parsed


def parse_eodhd_prices(payload: bytes, requested_symbol: str) -> list[PriceBar]:
    """Parse EODHD's JSON EOD response into a stable provider-neutral schema."""
    try:
        rows = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PriceProviderDataError("EODHD returned invalid JSON") from exc
    if isinstance(rows, dict):
        # Provider errors commonly arrive as JSON objects rather than price rows.
        raise PriceProviderDataError("EODHD returned an error object, not price rows")
    if not isinstance(rows, list):
        raise PriceProviderDataError("EODHD response must be a JSON array")
    bars: list[PriceBar] = []
    for row in rows:
        if not isinstance(row, dict):
            raise PriceProviderDataError("EODHD row must be an object")
        try:
            day_text = _iso_date(str(row["date"]), "date")
            day = dt.date.fromisoformat(day_text)
            close = _number(row.get("close"), "close", required=True)
            adjusted = _number(
                row.get("adjusted_close", row.get("adjustedClose")),
                "adjusted_close",
            )
        except KeyError as exc:
            raise PriceProviderDataError(f"EODHD row missing field {exc.args[0]}") from exc
        assert close is not None
        bars.append(
            PriceBar(
                ticker=str(row.get("code") or row.get("symbol") or requested_symbol),
                date=day,
                open=_number(row.get("open"), "open"),
                high=_number(row.get("high"), "high"),
                low=_number(row.get("low"), "low"),
                close=close,
                adjusted_close=adjusted,
                volume=_number(row.get("volume"), "volume"),
                provider="eodhd",
            )
        )
    return _validate_bars(bars, requested_symbol)


def parse_sharadar_prices(payload: bytes, requested_symbol: str) -> list[PriceBar]:
    """Parse Sharadar's CSV stock table (closeadj is split/dividend/spinoff adjusted)."""
    try:
        text = payload.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        fields = set(reader.fieldnames or [])
        required = {"date", "close", "ticker"}
        if not required.issubset(fields):
            raise PriceProviderDataError("Sharadar CSV lacks required ticker/date/close columns")
        bars: list[PriceBar] = []
        for row in reader:
            day_text = _iso_date(str(row.get("date", "")), "date")
            close = _number(row.get("close"), "close", required=True)
            assert close is not None
            bars.append(
                PriceBar(
                    ticker=str(row.get("ticker") or requested_symbol),
                    date=dt.date.fromisoformat(day_text),
                    open=_number(row.get("open"), "open"),
                    high=_number(row.get("high"), "high"),
                    low=_number(row.get("low"), "low"),
                    close=close,
                    adjusted_close=_number(row.get("closeadj"), "closeadj"),
                    volume=_number(row.get("volume"), "volume"),
                    provider="sharadar",
                )
            )
    except UnicodeDecodeError as exc:
        raise PriceProviderDataError("Sharadar returned non-UTF-8 CSV") from exc
    return _validate_bars(bars, requested_symbol)


def _validate_bars(bars: list[PriceBar], requested_symbol: str) -> list[PriceBar]:
    """Reject duplicate, unsorted, invalid or non-positive closing-price observations."""
    dates = [bar.date for bar in bars]
    if len(dates) != len(set(dates)):
        raise PriceProviderDataError(f"duplicate daily observations for {requested_symbol}")
    for bar in bars:
        if bar.close <= 0:
            raise PriceProviderDataError(f"non-positive closing price for {requested_symbol}")
        if bar.adjusted_close is not None and bar.adjusted_close <= 0:
            raise PriceProviderDataError(f"non-positive adjusted close for {requested_symbol}")
        if all(v is not None for v in (bar.low, bar.high)):
            if bar.low > bar.high:
                raise PriceProviderDataError(f"low exceeds high for {requested_symbol}")
    return sorted(bars, key=lambda bar: bar.date)


def _provider_request_url(
    provider: str,
    symbol: str,
    start: str,
    end: str,
    credential: str,
) -> tuple[str, str]:
    """Return (actual URL, redacted URL) for a bounded per-symbol date-range query."""
    start = _iso_date(start, "start")
    end = _iso_date(end, "end")
    if start > end:
        raise ValueError("start must be on or before end")
    if not symbol.strip():
        raise ValueError("symbol cannot be blank")
    if provider == "eodhd":
        base = "https://eodhd.com/api/eod/" + urllib.parse.quote(symbol.strip(), safe="")
        common = {"from": start, "to": end, "fmt": "json"}
        actual = urllib.parse.urlencode({**common, "api_token": credential})
        redacted = urllib.parse.urlencode({**common, "api_token": "[REDACTED]"})
    elif provider == "sharadar":
        base = "https://api.sharadar.com/v1.0/data/stocks"
        common = {
            "format": "csv",
            "ticker": symbol.strip(),
            "from": start,
            "to": end,
            "fields": "ticker,date,open,high,low,close,closeadj,closeunadj,volume,lastupdated",
            "limit": "10000",
            "skip": "0",
        }
        actual = urllib.parse.urlencode({**common, "api_key": credential})
        redacted = urllib.parse.urlencode({**common, "api_key": "[REDACTED]"})
    else:
        raise ValueError("provider must be 'eodhd' or 'sharadar'")
    return f"{base}?{actual}", f"{base}?{redacted}"


def _safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return slug[:100] or "unknown"


def _record_failure(
    layout: CacheLayout,
    *,
    provider: str,
    redacted_url: str,
    status: int | None,
    message: str,
) -> None:
    ManifestWriter(layout.manifest_path("prices")).record_failure(
        source_id=f"{provider.upper()}_PRICE_HISTORY",
        url=redacted_url,
        http_status=status,
        error=message,
        user_agent=USER_AGENT,
        parser_version=PARSER_VERSION,
        notes="Credential values are redacted; failure is not treated as missing data.",
    )


def acquire_price_history(
    provider: str,
    symbol: str,
    start: str,
    end: str,
    *,
    cache_root: str | os.PathLike[str] | None = None,
    repository_root: str | os.PathLike[str] | None = None,
    environ: Mapping[str, str] | None = None,
    opener: Callable[..., Any] = urllib.request.urlopen,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> tuple[list[PriceBar], Path]:
    """Fetch and cache one symbol's daily history; disabled unless explicitly enabled.

    Required environment variables:
      * ACCTCLOCK_ENABLE_PAID_DATA=1
      * SHARADAR_API_KEY for provider='sharadar', or EODHD_API_TOKEN for 'eodhd'

    The raw response and a redacted URL/hash manifest are saved outside the repository.
    This method performs a paid data request only when the environment explicitly enables
    it. It never purchases a plan, and it does not compute returns or alter a preregistration.
    """
    env = os.environ if environ is None else environ
    provider = provider.strip().lower()
    if provider not in {"eodhd", "sharadar"}:
        raise ValueError("provider must be 'eodhd' or 'sharadar'")
    if env.get("ACCTCLOCK_ENABLE_PAID_DATA") != "1":
        raise PriceProviderConfigurationError(
            "Paid price requests are disabled; set ACCTCLOCK_ENABLE_PAID_DATA=1 explicitly."
        )
    credential_name = "EODHD_API_TOKEN" if provider == "eodhd" else "SHARADAR_API_KEY"
    credential = env.get(credential_name, "").strip()
    if not credential:
        raise PriceProviderConfigurationError(
            f"Missing {credential_name}; configure it in the environment or secret store."
        )

    actual_url, redacted_url = _provider_request_url(provider, symbol, start, end, credential)
    kwargs: dict[str, Any] = {"explicit": cache_root, "env": dict(env)}
    if repository_root is not None:
        kwargs["repo"] = Path(repository_root)
    layout = build_layout(**kwargs).ensure()
    request = urllib.request.Request(
        actual_url,
        headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"},
        method="GET",
    )

    try:
        response = opener(request, timeout=timeout)
        try:
            status = int(getattr(response, "status", response.getcode()))
            headers = getattr(response, "headers", {})
            content_type = headers.get("Content-Type") if hasattr(headers, "get") else None
            payload = response.read(MAX_RESPONSE_BYTES + 1)
        finally:
            close = getattr(response, "close", None)
            if callable(close):
                close()
    except urllib.error.HTTPError as exc:
        message = f"HTTP {exc.code} from {provider}; credential redacted"
        _record_failure(layout, provider=provider, redacted_url=redacted_url, status=exc.code, message=message)
        raise PriceProviderRequestError(message) from None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        message = f"transport failure from {provider}: {type(exc).__name__}; credential redacted"
        _record_failure(layout, provider=provider, redacted_url=redacted_url, status=None, message=message)
        raise PriceProviderRequestError(message) from None

    if len(payload) > MAX_RESPONSE_BYTES:
        _record_failure(
            layout, provider=provider, redacted_url=redacted_url, status=status,
            message=f"response exceeded {MAX_RESPONSE_BYTES} bytes; credential redacted",
        )
        raise PriceProviderRequestError("Price response exceeded the configured size limit.")
    if status < 200 or status >= 300:
        message = f"HTTP {status} from {provider}; credential redacted"
        _record_failure(layout, provider=provider, redacted_url=redacted_url, status=status, message=message)
        raise PriceProviderRequestError(message)
    if not payload:
        message = f"empty response from {provider}; credential redacted"
        _record_failure(layout, provider=provider, redacted_url=redacted_url, status=status, message=message)
        raise PriceProviderRequestError(message)

    extension = "json" if provider == "eodhd" else "csv"
    digest = sha256_bytes(payload)
    filename = (
        f"{_safe_slug(symbol)}-{start}-{end}-{digest[:16]}.{extension}"
    )
    raw_path = layout.raw_source("prices") / provider / filename
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if raw_path.exists() and raw_path.read_bytes() != payload:
        raise PriceProviderDataError("cache hash collision: refusing to overwrite an existing raw payload")
    if not raw_path.exists():
        raw_path.write_bytes(payload)
    ManifestWriter(layout.manifest_path("prices")).record_success(
        source_id=f"{provider.upper()}_PRICE_HISTORY",
        url=redacted_url,
        http_status=status,
        payload=payload,
        local_path=relative_to_root(layout, raw_path),
        user_agent=USER_AGENT,
        content_type=content_type,
        parser_version=PARSER_VERSION,
        notes=f"symbol={symbol}; start={start}; end={end}; API credential redacted from manifest URL",
    )

    if provider == "eodhd":
        bars = parse_eodhd_prices(payload, symbol)
    else:
        bars = parse_sharadar_prices(payload, symbol)
    filtered = [bar for bar in bars if start <= bar.date.isoformat() <= end]
    if len(filtered) != len(bars):
        raise PriceProviderDataError("provider returned rows outside the requested date range")
    return filtered, raw_path

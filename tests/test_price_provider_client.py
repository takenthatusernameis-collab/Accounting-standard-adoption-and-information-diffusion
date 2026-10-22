"""Offline tests for paid price-provider adapters; no live API or subscription used."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from scripts.price_provider_client import (
    PriceProviderConfigurationError,
    PriceProviderDataError,
    _provider_request_url,
    acquire_price_history,
    parse_eodhd_prices,
    parse_sharadar_prices,
)


class FakeResponse:
    def __init__(self, payload: bytes, status: int = 200, content_type: str = "application/json"):
        self.payload = payload
        self.status = status
        self.headers = {"Content-Type": content_type}
        self.closed = False

    def getcode(self):
        return self.status

    def read(self, size=-1):
        return self.payload[:size]

    def close(self):
        self.closed = True


def test_provider_urls_redact_credentials_in_manifest_form():
    actual, redacted = _provider_request_url("eodhd", "AAPL.US", "2024-01-01", "2024-01-31", "secret-value")
    assert "secret-value" in actual
    assert "secret-value" not in redacted
    assert parse_qs(urlparse(redacted).query)["api_token"] == ["[REDACTED]"]

    actual, redacted = _provider_request_url("sharadar", "AAPL", "2024-01-01", "2024-01-31", "secret-value")
    assert "secret-value" in actual
    assert "secret-value" not in redacted
    assert parse_qs(urlparse(redacted).query)["api_key"] == ["[REDACTED]"]


def test_rejects_bad_date_range_and_provider():
    with pytest.raises(ValueError):
        _provider_request_url("eodhd", "AAPL.US", "2024-02-01", "2024-01-01", "x")
    with pytest.raises(ValueError):
        _provider_request_url("unknown", "AAPL", "2024-01-01", "2024-01-31", "x")


def test_paid_request_is_disabled_by_default():
    with pytest.raises(PriceProviderConfigurationError, match="disabled"):
        acquire_price_history(
            "eodhd", "AAPL.US", "2024-01-01", "2024-01-31",
            environ={},
            opener=lambda *args, **kwargs: pytest.fail("network must not be called"),
        )


def test_missing_credentials_fail_before_network():
    with pytest.raises(PriceProviderConfigurationError, match="EODHD_API_TOKEN"):
        acquire_price_history(
            "eodhd", "AAPL.US", "2024-01-01", "2024-01-31",
            environ={"ACCTCLOCK_ENABLE_PAID_DATA": "1"},
            opener=lambda *args, **kwargs: pytest.fail("network must not be called"),
        )


def test_parse_eodhd_daily_bars():
    payload = json.dumps([
        {"date": "2024-01-02", "open": 10, "high": 12, "low": 9, "close": 11,
         "adjusted_close": 10.5, "volume": 1000},
        {"date": "2024-01-03", "open": 11, "high": 13, "low": 10, "close": 12,
         "adjusted_close": 11.4, "volume": 1200},
    ]).encode()
    bars = parse_eodhd_prices(payload, "AAPL.US")
    assert len(bars) == 2
    assert bars[0].date == dt.date(2024, 1, 2)
    assert bars[0].ticker == "AAPL.US"
    assert bars[0].adjusted_close == 10.5
    assert bars[0].provider == "eodhd"


def test_parse_sharadar_uses_closeadj_as_adjusted_close():
    payload = (
        "ticker,date,open,high,low,close,closeadj,closeunadj,volume,lastupdated\n"
        "AAPL,2024-01-02,10,12,9,11,10.5,11,1000,2024-01-03\n"
    ).encode()
    bars = parse_sharadar_prices(payload, "AAPL")
    assert len(bars) == 1
    assert bars[0].ticker == "AAPL"
    assert bars[0].adjusted_close == 10.5
    assert bars[0].provider == "sharadar"


def test_parse_rejects_duplicates_malformed_rows_and_invalid_prices():
    duplicate = json.dumps([
        {"date": "2024-01-02", "close": 11},
        {"date": "2024-01-02", "close": 12},
    ]).encode()
    with pytest.raises(PriceProviderDataError, match="duplicate"):
        parse_eodhd_prices(duplicate, "AAPL.US")

    invalid = json.dumps([{"date": "2024-01-02", "close": 0}]).encode()
    with pytest.raises(PriceProviderDataError, match="non-positive"):
        parse_eodhd_prices(invalid, "AAPL.US")

    with pytest.raises(PriceProviderDataError):
        parse_eodhd_prices(b"not-json", "AAPL.US")

    with pytest.raises(PriceProviderDataError, match="required"):
        parse_sharadar_prices(b"ticker,date,open\nAAPL,2024-01-02,1\n", "AAPL")


def test_end_to_end_cache_and_manifest_use_redacted_url(tmp_path: Path):
    payload = json.dumps([
        {"date": "2024-01-02", "open": 10, "high": 12, "low": 9, "close": 11,
         "adjusted_close": 10.5, "volume": 1000}
    ]).encode()
    observed = {}

    def fake_open(request, timeout=30):
        observed["url"] = request.full_url
        observed["timeout"] = timeout
        return FakeResponse(payload)

    repo = tmp_path / "repo"
    (repo / "research").mkdir(parents=True)
    (repo / "scripts").mkdir(parents=True)
    cache = tmp_path / "outside-cache"
    bars, path = acquire_price_history(
        "eodhd", "AAPL.US", "2024-01-01", "2024-01-31",
        cache_root=cache,
        repository_root=repo,
        environ={"ACCTCLOCK_ENABLE_PAID_DATA": "1", "EODHD_API_TOKEN": "do-not-log-me"},
        opener=fake_open,
    )
    assert len(bars) == 1
    assert path.is_file()
    assert path.is_relative_to(cache)
    assert not path.is_relative_to(repo)
    manifest_text = (cache / "manifests" / "prices.jsonl").read_text()
    assert "[REDACTED]" in manifest_text
    assert "do-not-log-me" not in manifest_text
    assert "do-not-log-me" in observed["url"]
    assert observed["timeout"] == 30


def test_cache_guard_rejects_raw_prices_inside_repository(tmp_path: Path):
    payload = json.dumps([{"date":"2024-01-02", "close":10}]).encode()
    repo = tmp_path / "repo"
    (repo / "research").mkdir(parents=True)
    (repo / "scripts").mkdir(parents=True)

    def fake_open(request, timeout=30):
        return FakeResponse(payload)

    with pytest.raises(Exception, match="inside the repository"):
        acquire_price_history(
            "eodhd", "AAPL.US", "2024-01-01", "2024-01-31",
            cache_root=repo / "cache",
            repository_root=repo,
            environ={"ACCTCLOCK_ENABLE_PAID_DATA": "1", "EODHD_API_TOKEN": "x"},
            opener=fake_open,
        )

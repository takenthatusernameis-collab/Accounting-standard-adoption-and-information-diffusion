"""Regression tests for strict JSON serialization of research results.

Research outputs legitimately contain NaN and infinity: an empty sample yields
a NaN standard error, a zero-variance series yields an infinite Sharpe ratio,
and an empty denominator yields an infinite break-even cost. ``json.dumps``
writes those as bare ``NaN``/``Infinity`` tokens, which are not valid JSON and
break strict readers. The serializer must replace them with ``null`` and must
never emit a non-finite token.
"""

from __future__ import annotations

import base64
import dataclasses
import datetime as dt
import json
import math
from pathlib import Path

import numpy as np
import pytest

from scripts.results_serialization import (
    dumps,
    is_non_finite,
    read_json,
    to_jsonable,
    write_json,
)


def test_nan_and_infinity_become_null() -> None:
    assert to_jsonable(float("nan")) is None
    assert to_jsonable(float("inf")) is None
    assert to_jsonable(float("-inf")) is None
    assert to_jsonable(1.5) == 1.5
    assert to_jsonable(0) == 0
    assert to_jsonable(True) is True
    assert to_jsonable("nan") == "nan"


def test_is_non_finite_classification() -> None:
    assert is_non_finite(float("nan")) is True
    assert is_non_finite(float("inf")) is True
    assert is_non_finite(3.0) is False
    assert is_non_finite("nan") is False
    assert is_non_finite(None) is False
    assert is_non_finite(True) is False


def test_numpy_scalars_and_arrays_are_converted() -> None:
    assert to_jsonable(np.float64("nan")) is None
    assert to_jsonable(np.float32("inf")) is None
    assert to_jsonable(np.float32(2.5)) == pytest.approx(2.5)
    assert to_jsonable(np.int64(7)) == 7
    assert to_jsonable(np.array([1.0, np.nan, 3.0])) == [1.0, None, 3.0]


def test_nested_structures_are_converted_recursively() -> None:
    payload = {
        "se": float("nan"),
        "sharpe": float("inf"),
        "nested": [{"value": np.float32("nan")}, {"ok": 1.0}],
        "matrix": np.array([[1.0, np.nan], [3.0, 4.0]]),
    }
    converted = to_jsonable(payload)
    assert converted["se"] is None
    assert converted["sharpe"] is None
    assert converted["nested"][0]["value"] is None
    assert converted["matrix"][0][1] is None


def test_dumps_never_emits_non_finite_tokens() -> None:
    text = dumps({"se": float("nan"), "sharpe": float("-inf"), "n": 1})
    assert "NaN" not in text
    assert "Infinity" not in text
    assert json.loads(text) == {"se": None, "sharpe": None, "n": 1}


def test_dumps_is_strict_json() -> None:
    text = dumps({"value": float("nan")})

    def reject(constant: str) -> object:
        raise ValueError(f"non-finite constant {constant}")

    assert json.loads(text, parse_constant=reject) == {"value": None}


def test_non_string_keys_are_stringified() -> None:
    assert to_jsonable({1: "a", ("x", "y"): "b"}) == {"1": "a", "('x', 'y')": "b"}


def test_sets_dataclasses_and_paths_are_converted() -> None:
    @dataclasses.dataclass
    class Result:
        value: float
        label: str

    assert to_jsonable({"b", "a"}) == ["a", "b"]
    assert to_jsonable(Result(float("nan"), "x")) == {"value": None, "label": "x"}
    assert to_jsonable(Path("/tmp/example")) == "/tmp/example"
    assert to_jsonable(dt.datetime(2026, 10, 21, 12, 0, 0)) == "2026-10-21T12:00:00"


def test_bytes_are_base64_encoded() -> None:
    assert to_jsonable(b"\x00\x01") == base64.b64encode(b"\x00\x01").decode("ascii")


def test_write_json_round_trip(tmp_path: Path) -> None:
    target = tmp_path / "results" / "metrics.json"
    write_json(target, {"se": float("nan"), "n": 3, "tags": ["a", "b"]})
    assert target.exists()
    assert read_json(target) == {"se": None, "n": 3, "tags": ["a", "b"]}
    assert "NaN" not in target.read_text(encoding="utf-8")


def test_write_json_leaves_no_temporary_file(tmp_path: Path) -> None:
    target = tmp_path / "metrics.json"
    write_json(target, {"ok": True})
    assert [item.name for item in tmp_path.iterdir()] == ["metrics.json"]


def test_unknown_objects_fall_back_to_repr() -> None:
    class Opaque:
        def __repr__(self) -> str:
            return "<opaque>"

    assert to_jsonable(Opaque()) == "<opaque>"


def test_non_finite_values_survive_a_full_result_payload() -> None:
    payload = {
        "event_count": 0,
        "mean_abnormal_return": math.nan,
        "t_stat": math.inf,
        "by_jurisdiction": {"DE": {"car": math.nan}, "FR": {"car": 0.01}},
    }
    text = dumps(payload)
    assert "NaN" not in text and "Infinity" not in text
    restored = json.loads(text)
    assert restored["mean_abnormal_return"] is None
    assert restored["by_jurisdiction"]["DE"]["car"] is None
    assert restored["by_jurisdiction"]["FR"]["car"] == 0.01

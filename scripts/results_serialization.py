#!/usr/bin/env python3
"""JSON serialization helpers that never emit non-finite numbers.

Research result payloads routinely contain NaN and +/-Infinity: an empty
sample produces a NaN standard error, a zero-variance series produces an
infinite Sharpe ratio, and a division by an empty denominator produces an
infinite break-even cost. ``json.dumps`` happily writes those tokens, but
``NaN``/``Infinity`` are not valid JSON, so downstream readers (and strict
parsers) reject the file. This module converts non-finite values to ``null``
and then serializes with ``allow_nan=False`` so a non-finite value can never
silently corrupt a result file.
"""

from __future__ import annotations

import base64
import dataclasses
import datetime as dt
import json
import math
import os
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

#: Sentinel recorded in place of a non-finite number.
NON_FINITE_NULL = None


def is_non_finite(value: Any) -> bool:
    """Return True for NaN/Infinity numbers, including numpy floating scalars."""
    if isinstance(value, bool):
        return False
    if isinstance(value, float):
        return not math.isfinite(value)
    # numpy scalars and 0-d arrays expose the float protocol without being
    # instances of ``float``; convert defensively.
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    if isinstance(value, (int, str, bytes)):
        return False
    return not math.isfinite(number)


def to_jsonable(value: Any) -> Any:
    """Recursively convert ``value`` into a JSON-serializable structure.

    Non-finite floats become ``None``. Numpy scalars and arrays are converted
    to native Python values. Mappings, sequences, sets, dataclasses,
    datetimes, paths, and bytes are handled explicitly; anything else falls
    back to its ``repr`` so serialization never fails mid-run.
    """
    if value is None or isinstance(value, (bool, int, str)):
        return value

    if isinstance(value, float):
        return value if math.isfinite(value) else NON_FINITE_NULL

    if isinstance(value, (bytes, bytearray, memoryview)):
        return base64.b64encode(bytes(value)).decode("ascii")

    if isinstance(value, dt.datetime):
        return value.isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, dt.time):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)

    # numpy scalars (np.float64, np.int64, np.bool_) expose ``item()``.
    item = getattr(value, "item", None)
    if callable(item) and getattr(value, "shape", None) == ():
        return to_jsonable(item())

    # numpy arrays and pandas objects expose ``tolist()``.
    tolist = getattr(value, "tolist", None)
    if callable(tolist):
        return to_jsonable(tolist())

    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return to_jsonable(dataclasses.asdict(value))

    if isinstance(value, Mapping):
        return {str(key): to_jsonable(item) for key, item in value.items()}

    if isinstance(value, (set, frozenset)):
        return [to_jsonable(item) for item in sorted(value, key=repr)]

    if isinstance(value, Sequence):
        return [to_jsonable(item) for item in value]

    if hasattr(value, "to_dict") and callable(value.to_dict):
        return to_jsonable(value.to_dict())

    return repr(value)


def dumps(payload: Any, *, indent: int | None = 2, sort_keys: bool = True) -> str:
    """Serialize ``payload`` to a JSON string with non-finite values removed."""
    return json.dumps(
        to_jsonable(payload),
        allow_nan=False,
        indent=indent,
        sort_keys=sort_keys,
        ensure_ascii=False,
    )


def write_json(path: str | os.PathLike[str], payload: Any, *, indent: int | None = 2) -> Path:
    """Write ``payload`` to ``path`` atomically as strict JSON."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    text = dumps(payload, indent=indent) + "\n"
    temporary = target.with_name(target.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)
    return target


def read_json(path: str | os.PathLike[str]) -> Any:
    """Read a JSON document written by :func:`write_json`."""
    return json.loads(Path(path).read_text(encoding="utf-8"))

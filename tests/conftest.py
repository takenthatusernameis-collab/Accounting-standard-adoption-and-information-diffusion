"""Shared pytest configuration for the ACCTCLOCK repository test suite.

The repository root is placed on ``sys.path`` so the tests can import the
``scripts`` package regardless of how pytest is invoked.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

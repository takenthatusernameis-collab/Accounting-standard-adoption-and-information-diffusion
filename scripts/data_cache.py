"""Cache layout and repository-policy guard for the ACCTCLOCK data pipeline.

The registered caching policy is decision **D-015** and is written out in
``research/data_acquisition_plan.md`` §3:

* raw data is cached **outside** the repository working tree, under
  ``$ACCTCLOCK_CACHE`` (default ``~/.cache/acctclock``);
* the repository receives **code**, **manifests**, **hashes** and non-licensed
  derived aggregates only;
* a per-source exception requires an explicit maintainer ruling recorded as a
  new decision.

This module owns the cache root resolution, the deterministic directory layout
and the guard that refuses to write a raw artefact inside the repository.
It performs no network access and has no third-party dependencies.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

CACHE_ENV_VAR = "ACCTCLOCK_CACHE"
DEFAULT_CACHE_ROOT = Path.home() / ".cache" / "acctclock"

#: Top-level directories of the registered layout.
RAW_DIR = "raw"
DERIVED_DIR = "derived"
MANIFEST_DIR = "manifests"

#: Per-source raw sub-directories, fixed by ``research/data_acquisition_plan.md`` §3.
SOURCE_DIRS = (
    "sec_edgar",
    "oam",
    "ifrs_calendar",
    "eurlex",
    "prices",
    "fx",
    "wgi",
    "linguistic",
    "sources",
)

#: Per-source manifest file names, one JSONL file per source.
MANIFEST_NAMES = {
    "sec_edgar": "sec_edgar.jsonl",
    "ifrs_calendar": "ifrs_calendar.jsonl",
    "eurlex": "eurlex.jsonl",
    "prices": "prices.jsonl",
    "fx": "fx.jsonl",
    "wgi": "wgi.jsonl",
    "linguistic": "linguistic.jsonl",
    "oam": "oam.jsonl",
    "sources": "sources.jsonl",
}


class CachePolicyError(RuntimeError):
    """Raised when the cache root would place raw data inside the repository."""


def cache_root(explicit: str | os.PathLike[str] | None = None, env: dict[str, str] | None = None) -> Path:
    """Resolve the cache root.

    Precedence: an explicit argument, then ``$ACCTCLOCK_CACHE``, then
    ``~/.cache/acctclock``.
    """
    if explicit is not None:
        return Path(explicit).expanduser()
    environ = os.environ if env is None else env
    value = environ.get(CACHE_ENV_VAR)
    if value:
        return Path(value).expanduser()
    return DEFAULT_CACHE_ROOT


def repository_root(start: Path | None = None) -> Path:
    """Locate the repository working tree that contains this package."""
    base = Path(start) if start is not None else Path(__file__).resolve().parent
    for candidate in [base, *base.parents]:
        if (candidate / "research").is_dir() and (candidate / "scripts").is_dir():
            return candidate
    return base


def is_inside(child: Path, parent: Path) -> bool:
    """True when ``child`` is ``parent`` or lives beneath it."""
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def ensure_outside_repository(root: Path, repo: Path | None = None) -> Path:
    """Fail loudly when the cache root sits inside the repository working tree.

    Raw data must never be committed (D-015). The check runs before any write,
    so a misconfigured environment cannot leak raw artefacts into a commit.
    """
    repository = repo if repo is not None else repository_root()
    root = Path(root).expanduser()
    if is_inside(root, repository):
        raise CachePolicyError(
            f"Cache root {root} is inside the repository working tree {repository}. "
            "Raw data must be cached outside the repository (decision D-015); "
            f"set {CACHE_ENV_VAR} to a path outside the working tree."
        )
    return root


@dataclass(frozen=True)
class CacheLayout:
    """Resolved locations of the registered cache layout."""

    root: Path

    @property
    def raw(self) -> Path:
        return self.root / RAW_DIR

    @property
    def derived(self) -> Path:
        return self.root / DERIVED_DIR

    @property
    def manifests(self) -> Path:
        return self.root / MANIFEST_DIR

    def raw_source(self, source: str) -> Path:
        if source not in SOURCE_DIRS:
            raise KeyError(f"unknown source directory {source!r}")
        return self.raw / source

    def manifest_path(self, source: str) -> Path:
        if source not in MANIFEST_NAMES:
            raise KeyError(f"unknown manifest source {source!r}")
        return self.manifests / MANIFEST_NAMES[source]

    def ensure(self) -> "CacheLayout":
        """Create the directory skeleton. Returns ``self`` for chaining."""
        self.raw.mkdir(parents=True, exist_ok=True)
        self.derived.mkdir(parents=True, exist_ok=True)
        self.manifests.mkdir(parents=True, exist_ok=True)
        for name in SOURCE_DIRS:
            (self.raw / name).mkdir(parents=True, exist_ok=True)
        return self


def build_layout(
    explicit: str | os.PathLike[str] | None = None,
    repo: Path | None = None,
    env: dict[str, str] | None = None,
) -> CacheLayout:
    """Resolve, guard and construct the cache layout without creating anything."""
    root = cache_root(explicit, env=env)
    ensure_outside_repository(root, repo=repo)
    return CacheLayout(root=root)


def sec_edgar_paths(layout: CacheLayout, cik: int | str, accession: str) -> dict[str, Path]:
    """Deterministic raw paths for one EDGAR filing.

    Follows ``research/data_acquisition_plan.md`` §4.1:

    * ``raw/sec_edgar/<cik>/<accession-nodashes>/<form>.txt`` — complete submission
      text file;
    * ``raw/sec_edgar/<cik>/<accession-nodashes>/index.json`` — filing index;
    * ``raw/sec_edgar/<cik>/submissions.json`` — submissions JSON (identifier
      history only; **never** the acceptance time).
    """
    cik_text = f"{int(cik):010d}" if str(cik).strip().isdigit() else str(cik)
    accession_nodashes = accession.replace("-", "")
    base = layout.raw_source("sec_edgar") / cik_text / accession_nodashes
    return {
        "cik": Path(cik_text),
        "accession_nodashes": Path(accession_nodashes),
        "submission_text": base / "submission.txt",
        "index": base / "index.json",
        "submissions": layout.raw_source("sec_edgar") / cik_text / "submissions.json",
    }


def relative_to_root(layout: CacheLayout, path: Path) -> str:
    """Render a path relative to the cache root for manifest ``local_path`` fields."""
    try:
        return str(Path(path).resolve().relative_to(layout.root.resolve()))
    except ValueError:
        return str(path)

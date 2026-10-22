"""Unit tests for the cache layout and the repository-policy guard.

The caching policy is decision D-015: raw data lives outside the repository
working tree, and the repository receives code, manifests, hashes and
non-licensed derived aggregates only.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.data_cache import (
    CACHE_ENV_VAR,
    CacheLayout,
    CachePolicyError,
    build_layout,
    cache_root,
    ensure_outside_repository,
    relative_to_root,
    repository_root,
    sec_edgar_paths,
)


def test_cache_root_precedence(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(CACHE_ENV_VAR, "/tmp/from-env")
    assert cache_root() == Path("/tmp/from-env")
    assert cache_root("/tmp/explicit") == Path("/tmp/explicit")
    monkeypatch.delenv(CACHE_ENV_VAR)
    assert cache_root().name == "acctclock"


def test_cache_root_honours_an_injected_environment() -> None:
    assert cache_root(env={CACHE_ENV_VAR: "/tmp/injected"}) == Path("/tmp/injected")


def test_cache_root_inside_the_repository_is_refused(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "research").mkdir(parents=True)
    (repo / "scripts").mkdir(parents=True)
    with pytest.raises(CachePolicyError) as excinfo:
        ensure_outside_repository(repo / "cache", repo=repo)
    assert "D-015" in str(excinfo.value)


def test_cache_root_outside_the_repository_is_accepted(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "research").mkdir(parents=True)
    (repo / "scripts").mkdir(parents=True)
    root = tmp_path / "elsewhere" / "acctclock"
    assert ensure_outside_repository(root, repo=repo) == root


def test_build_layout_refuses_an_inside_repository_root(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "research").mkdir(parents=True)
    (repo / "scripts").mkdir(parents=True)
    with pytest.raises(CachePolicyError):
        build_layout(repo / "raw-cache", repo=repo)


def test_layout_has_the_registered_directories(tmp_path: Path) -> None:
    layout = CacheLayout(root=tmp_path / "acctclock")
    assert layout.raw.name == "raw"
    assert layout.derived.name == "derived"
    assert layout.manifests.name == "manifests"
    assert layout.raw_source("sec_edgar").name == "sec_edgar"
    assert layout.raw_source("prices").name == "prices"
    assert layout.manifest_path("sec_edgar").name == "sec_edgar.jsonl"
    with pytest.raises(KeyError):
        layout.raw_source("not-a-source")


def test_ensure_creates_the_skeleton(tmp_path: Path) -> None:
    layout = CacheLayout(root=tmp_path / "acctclock")
    layout.ensure()
    assert layout.raw_source("sec_edgar").is_dir()
    assert layout.derived.is_dir()
    assert layout.manifests.is_dir()


def test_sec_edgar_paths_follow_the_registered_naming(tmp_path: Path) -> None:
    layout = CacheLayout(root=tmp_path / "acctclock")
    paths = sec_edgar_paths(layout, 320193, "0000320193-18-000123")
    assert paths["submissions"] == layout.raw / "sec_edgar" / "0000320193" / "submissions.json"
    assert paths["index"] == (
        layout.raw / "sec_edgar" / "0000320193" / "000032019318000123" / "index.json"
    )
    assert paths["submission_text"] == (
        layout.raw / "sec_edgar" / "0000320193" / "000032019318000123" / "submission.txt"
    )


def test_relative_to_root_is_the_manifest_local_path(tmp_path: Path) -> None:
    layout = CacheLayout(root=tmp_path / "acctclock")
    target = layout.raw / "sec_edgar" / "0000000001" / "submissions.json"
    assert relative_to_root(layout, target) == "raw/sec_edgar/0000000001/submissions.json"


def test_repository_root_finds_the_working_tree() -> None:
    root = repository_root()
    assert (root / "research").is_dir()
    assert (root / "scripts").is_dir()

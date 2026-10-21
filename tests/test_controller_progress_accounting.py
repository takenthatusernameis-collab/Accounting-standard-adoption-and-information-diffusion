"""Regression tests for the controller's progress accounting.

These tests pin the contract that `.github/workflows/main.yml` relies on:

    python3 scripts/controller_progress.py --base-sha <base> --head-sha <head>
    python3 scripts/controller_progress.py --base-sha <base> --head-sha <head> \
        --verified-remote-sha <sha>

The first call must exit 0 only when the commit range contains a meaningful
project change. The second must exit 0 only when the change is also visible on
a remote. A regression here silently breaks the worker loop: the controller
then reports "No meaningful repository change was committed and verified" for
sessions that did in fact persist work.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.controller_progress import (
    EXCLUDED_PATH_PATTERNS,
    ControllerProgressError,
    changed_paths,
    evaluate,
    is_excluded_path,
    meaningful_paths,
    remote_visibility,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "controller_progress.py"


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """Create a working repository with a bare origin remote."""
    remote = tmp_path / "remote.git"
    subprocess.run(
        ["git", "init", "--quiet", "--bare", str(remote)],
        check=True,
        capture_output=True,
    )
    work = tmp_path / "work"
    work.mkdir()
    subprocess.run(["git", "init", "--quiet", str(work)], check=True, capture_output=True)
    _git(work, "symbolic-ref", "HEAD", "refs/heads/main")
    _git(work, "config", "user.email", "test@example.com")
    _git(work, "config", "user.name", "Test")
    _git(work, "remote", "add", "origin", str(remote))
    (work / "README.md").write_text("initial\n", encoding="utf-8")
    _git(work, "add", "README.md")
    _git(work, "commit", "-q", "-m", "initial")
    _git(work, "push", "-q", "-u", "origin", "main")
    return work


def _commit(repo: Path, relative_path: str, content: str, message: str) -> str:
    target = repo / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _run_script(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )


# --------------------------------------------------------------------------
# Path classification
# --------------------------------------------------------------------------


def test_workflow_definitions_are_not_project_progress() -> None:
    assert is_excluded_path(".github/workflows/main.yml")
    assert not is_excluded_path("research/HANDOFF.md")
    assert not is_excluded_path("scripts/controller_progress.py")
    assert not is_excluded_path("tests/test_controller_progress_accounting.py")


def test_build_and_runtime_artifacts_are_excluded() -> None:
    for path in (
        "tests/__pycache__/test_controller_progress_accounting.cpython-312.pyc",
        ".pytest_cache/CACHEDIR.TAG",
        "node_modules/kilo/index.js",
        ".venv/lib/python3.12/site-packages/pkg.py",
        ".env",
        "data.sqlite3",
        "kilo-session-3.log",
        "research/output.tmp",
    ):
        assert is_excluded_path(path), path
        assert path not in meaningful_paths([path])


def test_meaningful_paths_keeps_real_work() -> None:
    paths = [
        "research/HANDOFF.md",
        "research/source_ledger.csv",
        "scripts/controller_progress.py",
        ".github/workflows/main.yml",
        "tests/__pycache__/x.pyc",
    ]
    assert meaningful_paths(paths) == [
        "research/HANDOFF.md",
        "research/source_ledger.csv",
        "scripts/controller_progress.py",
    ]


def test_excluded_patterns_cover_workflow_and_cache_directories() -> None:
    assert ".github/workflows/*" in EXCLUDED_PATH_PATTERNS
    assert "__pycache__/*" in EXCLUDED_PATH_PATTERNS


# --------------------------------------------------------------------------
# Commit range accounting
# --------------------------------------------------------------------------


def test_no_commits_yet_means_no_progress(repo: Path) -> None:
    head = _git(repo, "rev-parse", "HEAD")
    assert changed_paths(repo, head, head) == []
    report = evaluate(repo, head, head)
    assert report["has_meaningful_progress"] is False
    assert report["reason"] == "no_meaningful_project_changes"


def test_project_change_is_meaningful_progress(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    head = _commit(repo, "research/HANDOFF.md", "handoff\n", "add handoff")

    report = evaluate(repo, base, head)
    assert report["has_meaningful_progress"] is True
    assert report["meaningful_paths"] == ["research/HANDOFF.md"]

    result = _run_script(repo, "--base-sha", base, "--head-sha", head)
    assert result.returncode == 0, result.stdout
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["has_meaningful_progress"] is True


def test_workflow_only_change_is_not_meaningful_progress(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    head = _commit(repo, ".github/workflows/main.yml", "name: test\n", "touch workflow")

    report = evaluate(repo, base, head)
    assert report["has_meaningful_progress"] is False
    assert report["excluded_paths"] == [".github/workflows/main.yml"]

    result = _run_script(repo, "--base-sha", base, "--head-sha", head)
    assert result.returncode == 1


def test_artifact_only_change_is_not_meaningful_progress(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    head = _commit(repo, "tests/__pycache__/x.pyc", "junk\n", "add cache artifact")

    result = _run_script(repo, "--base-sha", base, "--head-sha", head)
    assert result.returncode == 1


def test_unknown_base_commit_is_reported_as_an_error(repo: Path) -> None:
    head = _git(repo, "rev-parse", "HEAD")
    result = _run_script(repo, "--base-sha", "0" * 40, "--head-sha", head)
    assert result.returncode == 2
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert "error" in payload


def test_non_repository_path_is_reported_as_an_error(tmp_path: Path) -> None:
    result = _run_script(tmp_path, "--base-sha", "a" * 40, "--head-sha", "b" * 40)
    assert result.returncode == 2
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["error"] == "not_a_git_repository"


# --------------------------------------------------------------------------
# Remote verification
# --------------------------------------------------------------------------


def test_pushed_commit_is_verified_on_the_remote_tracking_ref(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    head = _commit(repo, "research/results.md", "results\n", "add results")
    _git(repo, "push", "-q", "origin", "HEAD:main")

    visibility = remote_visibility(repo, head, head)
    assert visibility["status"] == "visible_on_remote_tracking_ref"

    report = evaluate(repo, base, head, head)
    assert report["remote_verified"] is True

    result = _run_script(repo, "--base-sha", base, "--head-sha", head, "--verified-remote-sha", head)
    assert result.returncode == 0, result.stdout


def test_unpushed_commit_is_not_credited(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    head = _commit(repo, "research/results.md", "results\n", "add results")

    visibility = remote_visibility(repo, head, head)
    assert visibility["status"] == "not_visible_on_any_remote_ref"

    result = _run_script(repo, "--base-sha", base, "--head-sha", head, "--verified-remote-sha", head)
    assert result.returncode == 1
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["remote_verified"] is False
    assert "remote_not_verified" in payload["reason"]


def test_remote_sha_that_is_not_the_head_commit_is_rejected(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    older = base
    head = _commit(repo, "research/results.md", "results\n", "add results")
    _git(repo, "push", "-q", "origin", "HEAD:main")

    result = _run_script(
        repo, "--base-sha", base, "--head-sha", head, "--verified-remote-sha", older
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["remote_visibility"]["status"] == "remote_sha_does_not_match_head"


def test_missing_remote_sha_cannot_credit_progress(repo: Path) -> None:
    base = _git(repo, "rev-parse", "HEAD")
    head = _commit(repo, "research/results.md", "results\n", "add results")
    _git(repo, "push", "-q", "origin", "HEAD:main")

    result = _run_script(
        repo, "--base-sha", base, "--head-sha", head, "--verified-remote-sha", "f" * 40
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["remote_visibility"]["status"] == "remote_commit_missing"


def test_evaluate_raises_for_missing_commits(repo: Path) -> None:
    head = _git(repo, "rev-parse", "HEAD")
    with pytest.raises(ControllerProgressError):
        changed_paths(repo, "0" * 40, head)

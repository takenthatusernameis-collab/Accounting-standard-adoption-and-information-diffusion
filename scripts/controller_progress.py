#!/usr/bin/env python3
"""Controller progress accounting for the Kilo general-agent loop.

The workflow controller decides whether a worker session produced meaningful,
remotely persisted repository progress. It calls this script twice per session:

1. ``--base-sha <base> --head-sha <head>``
   Exit 0 when the commit range ``base..head`` contains at least one meaningful
   project change. Workflow definitions, caches, and build/runtime artifacts do
   not count as progress.

2. ``--base-sha <base> --head-sha <head> --verified-remote-sha <sha>``
   Exit 0 only when the range contains meaningful project changes *and* the
   supplied SHA resolves to the head commit *and* that commit is visible on a
   remote tracking ref. This is the single path that credits a session with
   project progress.

Exit codes
    0   progress credited
    1   no meaningful progress (or remote visibility could not be confirmed)
    2   usage error or unusable repository state

The controller only inspects the exit status. Every diagnostic detail is
printed to stdout as a single JSON object so a human reading the workflow log
can reconstruct the accounting decision.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

SCHEMA_VERSION = 1

#: Paths that never constitute meaningful project progress. The controller's
#: staging step already excludes these from its checkpoint commits; this list
#: mirrors that behaviour so the accounting decision matches what was committed.
EXCLUDED_PATH_PATTERNS: tuple[str, ...] = (
    ".github/workflows/*",
    "*/.github/workflows/*",
    ".venv/*",
    "*/.venv/*",
    "venv/*",
    "*/venv/*",
    "node_modules/*",
    "*/node_modules/*",
    "__pycache__/*",
    "*/__pycache__/*",
    ".pytest_cache/*",
    "*/.pytest_cache/*",
    ".mypy_cache/*",
    "*/.mypy_cache/*",
    ".ruff_cache/*",
    "*/.ruff_cache/*",
    ".tox/*",
    "*/.tox/*",
    ".env",
    ".env.*",
    "*/.env",
    "*/.env.*",
    "*.pyc",
    "*.pyo",
    "*.sqlite",
    "*.sqlite3",
    "*.db",
    "*.sqlite-wal",
    "*.sqlite-shm",
    "*.sqlite3-wal",
    "*.sqlite3-shm",
    "*.db-wal",
    "*.db-shm",
    "*.tmp",
    "coverage.xml",
    "*/coverage.xml",
    ".coverage",
    "*/.coverage",
    "kilo-session-*.log",
    "*/kilo-session-*.log",
    "kilo-progress-*.log",
    "*/kilo-progress-*.log",
)


class ControllerProgressError(RuntimeError):
    """Raised when the repository cannot be inspected for progress."""


def _git(repo: Path, *args: str) -> str:
    """Run a git command inside ``repo`` and return stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip().replace("\n", " ")[:300]
        raise ControllerProgressError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout


def _git_ok(repo: Path, *args: str) -> bool:
    """Return True when a git command exits successfully."""
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def is_excluded_path(path: str) -> bool:
    """Return True when ``path`` is an excluded artifact rather than work."""
    normalized = path.strip().replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    for pattern in EXCLUDED_PATH_PATTERNS:
        if fnmatch.fnmatch(normalized, pattern):
            return True
    return False


def meaningful_paths(paths: Iterable[str]) -> list[str]:
    """Filter ``paths`` down to the ones that count as project progress."""
    return [path for path in paths if not is_excluded_path(path)]


def changed_paths(repo: Path, base_sha: str, head_sha: str) -> list[str]:
    """Return the paths that differ between ``base_sha`` and ``head_sha``."""
    if not base_sha or not head_sha:
        return []
    if base_sha == head_sha:
        return []
    if not _git_ok(repo, "cat-file", "-e", f"{base_sha}^{{commit}}"):
        raise ControllerProgressError(f"base commit {base_sha} is not available in the repository")
    if not _git_ok(repo, "cat-file", "-e", f"{head_sha}^{{commit}}"):
        raise ControllerProgressError(f"head commit {head_sha} is not available in the repository")
    output = _git(repo, "diff", "--name-only", "--no-renames", base_sha, head_sha)
    return [line for line in output.splitlines() if line.strip()]


def _remote_tracking_refs(repo: Path) -> list[tuple[str, str]]:
    """Return ``(refname, objectname)`` pairs for every remote tracking ref."""
    output = _git(repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/remotes")
    refs: list[tuple[str, str]] = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) == 2:
            refs.append((parts[0], parts[1]))
    return refs


def _fetch_head_shas(repo: Path) -> list[str]:
    """Return the SHAs recorded in FETCH_HEAD, if the file exists."""
    fetch_head = repo / ".git" / "FETCH_HEAD"
    try:
        text = fetch_head.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    shas: list[str] = []
    for line in text.splitlines():
        parts = line.split()
        if parts and len(parts[0]) >= 7:
            shas.append(parts[0])
    return shas


def remote_visibility(repo: Path, remote_sha: str, head_sha: str) -> dict[str, object]:
    """Describe whether ``remote_sha`` is a remotely visible copy of ``head_sha``."""
    detail: dict[str, object] = {
        "verified_remote_sha": remote_sha,
        "head_sha": head_sha,
    }

    if not _git_ok(repo, "cat-file", "-e", f"{remote_sha}^{{commit}}"):
        detail["status"] = "remote_commit_missing"
        return detail

    resolved_remote = _git(repo, "rev-parse", f"{remote_sha}^{{commit}}").strip()
    resolved_head = _git(repo, "rev-parse", f"{head_sha}^{{commit}}").strip()
    detail["resolved_remote_sha"] = resolved_remote
    detail["resolved_head_sha"] = resolved_head

    if resolved_remote != resolved_head:
        detail["status"] = "remote_sha_does_not_match_head"
        return detail

    refs = _remote_tracking_refs(repo)
    fetch_shas = _fetch_head_shas(repo)
    detail["remote_tracking_refs"] = len(refs)

    for refname, _objectname in refs:
        if _git_ok(repo, "merge-base", "--is-ancestor", resolved_remote, refname):
            detail["status"] = "visible_on_remote_tracking_ref"
            detail["refname"] = refname
            return detail

    for sha in fetch_shas:
        if sha == resolved_remote or _git_ok(repo, "merge-base", "--is-ancestor", resolved_remote, sha):
            detail["status"] = "visible_on_fetch_head"
            return detail

    if not refs and not fetch_shas:
        detail["status"] = "remote_visibility_unverifiable_no_remote_refs"
        return detail

    detail["status"] = "not_visible_on_any_remote_ref"
    return detail


def evaluate(
    repo: Path,
    base_sha: str,
    head_sha: str,
    verified_remote_sha: str | None = None,
) -> dict[str, object]:
    """Evaluate the progress accounting decision for a session."""
    paths = changed_paths(repo, base_sha, head_sha)
    kept = meaningful_paths(paths)
    report: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "repo": str(repo),
        "base_sha": base_sha,
        "head_sha": head_sha,
        "changed_path_count": len(paths),
        "meaningful_path_count": len(kept),
        "meaningful_paths": kept,
        "excluded_paths": [path for path in paths if path not in kept],
    }

    if not kept:
        report["has_meaningful_progress"] = False
        report["reason"] = "no_meaningful_project_changes"
        return report

    report["has_meaningful_progress"] = True

    if verified_remote_sha:
        visibility = remote_visibility(repo, verified_remote_sha, head_sha)
        report["remote_visibility"] = visibility
        report["remote_verified"] = visibility.get("status") in (
            "visible_on_remote_tracking_ref",
            "visible_on_fetch_head",
        )
        if not report["remote_verified"]:
            report["reason"] = f"remote_not_verified:{visibility.get('status')}"
            return report

    report["reason"] = "meaningful_project_changes_present"
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report whether a session produced meaningful, remotely visible progress."
    )
    parser.add_argument("--base-sha", required=True, help="Session base commit.")
    parser.add_argument("--head-sha", required=True, help="Session head commit.")
    parser.add_argument(
        "--verified-remote-sha",
        default=None,
        help="SHA that the controller verified on the remote. Required for the crediting path.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository root to inspect (defaults to the current directory).",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists():
        print(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "error": "not_a_git_repository",
                    "repo": str(repo),
                },
                sort_keys=True,
            )
        )
        return 2

    try:
        report = evaluate(repo, args.base_sha, args.head_sha, args.verified_remote_sha)
    except ControllerProgressError as exc:
        print(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "error": str(exc),
                    "repo": str(repo),
                },
                sort_keys=True,
            )
        )
        return 2

    print(json.dumps(report, sort_keys=True))
    return 0 if report.get("has_meaningful_progress") and (
        not args.verified_remote_sha or report.get("remote_verified")
    ) else 1


if __name__ == "__main__":
    sys.exit(main())

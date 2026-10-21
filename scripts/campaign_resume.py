#!/usr/bin/env python3
"""Resumable state for a multi-cycle research campaign.

The ACCTCLOCK campaign is executed by an autonomous worker loop in which each
session may be interrupted, restarted, or handed to a different agent. A
durable, machine-readable state file makes resumption deterministic: every
session records which campaign steps are complete, which one was in flight
when it stopped, and what the next agent must do.

The state file is intentionally plain JSON so it can be inspected, diffed, and
merged by hand. ``research/HANDOFF.md`` remains the human-readable handoff;
this module is the structured counterpart.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Iterable, Sequence

try:
    from scripts.results_serialization import write_json
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.results_serialization import write_json

SCHEMA_VERSION = 1

#: Allowed lifecycle states for a campaign step.
STEP_STATUSES: frozenset[str] = frozenset(
    {"pending", "in_progress", "completed", "failed", "skipped"}
)

#: Statuses that mean the step still needs to run.
UNFINISHED_STATUSES: frozenset[str] = frozenset({"pending", "in_progress", "failed"})


class CampaignStateError(RuntimeError):
    """Raised when campaign state is missing, malformed, or contradictory."""


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class Step:
    """A single unit of campaign work."""

    id: str
    status: str = "pending"
    attempts: int = 0
    started_at: str | None = None
    finished_at: str | None = None
    result: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "attempts": self.attempts,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "result": self.result,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Step":
        if not isinstance(payload, dict) or not payload.get("id"):
            raise CampaignStateError("campaign step entries require an 'id'")
        status = payload.get("status", "pending")
        if status not in STEP_STATUSES:
            raise CampaignStateError(f"unknown campaign step status: {status!r}")
        return cls(
            id=str(payload["id"]),
            status=status,
            attempts=int(payload.get("attempts", 0) or 0),
            started_at=payload.get("started_at"),
            finished_at=payload.get("finished_at"),
            result=dict(payload.get("result") or {}),
            error=payload.get("error"),
        )


@dataclass(frozen=True)
class CampaignState:
    """The durable state of a research campaign."""

    campaign_id: str
    steps: tuple[Step, ...] = ()
    notes: tuple[str, ...] = ()
    updated_at: str = ""
    remote_source: str | None = None
    conflicts: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "campaign_id": self.campaign_id,
            "updated_at": self.updated_at,
            "remote_source": self.remote_source,
            "conflicts": list(self.conflicts),
            "notes": list(self.notes),
            "steps": [step.to_dict() for step in self.steps],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CampaignState":
        if not isinstance(payload, dict):
            raise CampaignStateError("campaign state must be a JSON object")
        campaign_id = payload.get("campaign_id")
        if not campaign_id:
            raise CampaignStateError("campaign state requires a 'campaign_id'")
        raw_steps = payload.get("steps") or []
        if not isinstance(raw_steps, list):
            raise CampaignStateError("campaign state 'steps' must be a list")
        return cls(
            campaign_id=str(campaign_id),
            steps=tuple(Step.from_dict(entry) for entry in raw_steps),
            notes=tuple(str(note) for note in payload.get("notes") or []),
            updated_at=str(payload.get("updated_at") or ""),
            remote_source=payload.get("remote_source"),
            conflicts=tuple(str(item) for item in payload.get("conflicts") or []),
        )

    def step(self, step_id: str) -> Step | None:
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def pending_steps(self) -> tuple[Step, ...]:
        """Return unfinished steps, with an interrupted step first."""
        interrupted = tuple(step for step in self.steps if step.status == "in_progress")
        waiting = tuple(step for step in self.steps if step.status in ("pending", "failed"))
        return interrupted + waiting


def new_state(campaign_id: str, step_ids: Iterable[str]) -> CampaignState:
    """Create a fresh campaign state whose steps all start as ``pending``."""
    steps = tuple(Step(id=str(step_id)) for step_id in step_ids)
    return CampaignState(campaign_id=campaign_id, steps=steps, updated_at=_utc_now())


def load_state(path: str | Path) -> CampaignState:
    """Load a campaign state file.

    Raises :class:`CampaignStateError` when the file is absent or malformed so
    a corrupted state can never silently become "everything is done".
    """
    target = Path(path)
    if not target.exists():
        raise CampaignStateError(f"campaign state file not found: {target}")
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CampaignStateError(f"campaign state file is unreadable: {target}: {exc}") from exc
    return CampaignState.from_dict(payload)


def save_state(path: str | Path, state: CampaignState) -> Path:
    """Persist ``state`` atomically."""
    updated = replace(state, updated_at=_utc_now())
    return write_json(path, updated.to_dict())


def mark_step(
    state: CampaignState,
    step_id: str,
    status: str,
    *,
    result: dict[str, Any] | None = None,
    error: str | None = None,
) -> CampaignState:
    """Return a copy of ``state`` with ``step_id`` moved to ``status``."""
    if status not in STEP_STATUSES:
        raise CampaignStateError(f"unknown campaign step status: {status!r}")
    steps: list[Step] = []
    found = False
    for step in state.steps:
        if step.id != step_id:
            steps.append(step)
            continue
        found = True
        if status == "in_progress":
            steps.append(
                replace(
                    step,
                    status=status,
                    attempts=step.attempts + 1,
                    started_at=_utc_now(),
                    finished_at=None,
                    error=None,
                )
            )
        elif status in ("completed", "skipped"):
            steps.append(
                replace(
                    step,
                    status=status,
                    finished_at=_utc_now(),
                    result=dict(result or step.result),
                    error=None,
                )
            )
        else:  # failed or pending
            steps.append(
                replace(
                    step,
                    status=status,
                    finished_at=_utc_now(),
                    result=dict(result or step.result),
                    error=error,
                )
            )
    if not found:
        raise CampaignStateError(f"unknown campaign step: {step_id!r}")
    return replace(state, steps=tuple(steps), updated_at=_utc_now())


def resume_plan(state: CampaignState) -> list[str]:
    """Return the ordered IDs of the steps a resumed session should run."""
    return [step.id for step in state.pending_steps()]


def apply_remote_state(local: CampaignState, remote: CampaignState) -> CampaignState:
    """Merge a remote campaign dossier into the local state.

    A remote step that is already complete locally is never overwritten; a
    local step that the remote marks complete is adopted. Divergences are
    recorded as conflicts instead of being resolved silently.
    """
    conflicts: list[str] = list(local.conflicts)
    merged: list[Step] = []

    for step in local.steps:
        remote_step = remote.step(step.id)
        if remote_step is None:
            merged.append(step)
            continue
        if remote_step.status == step.status:
            merged.append(step)
            continue
        if step.status in ("completed", "skipped"):
            conflicts.append(
                f"{step.id}: local status '{step.status}' differs from remote '{remote_step.status}'"
            )
            merged.append(step)
            continue
        if remote_step.status in ("completed", "skipped"):
            merged.append(replace(step, status=remote_step.status, result=dict(remote_step.result)))
            continue
        conflicts.append(
            f"{step.id}: local status '{step.status}' differs from remote '{remote_step.status}'"
        )
        merged.append(step)

    for remote_step in remote.steps:
        if local.step(remote_step.id) is None:
            merged.append(remote_step)

    return replace(
        local,
        steps=tuple(merged),
        conflicts=tuple(conflicts),
        remote_source=remote.remote_source,
        updated_at=_utc_now(),
    )


def fetch_remote_state(
    url: str,
    *,
    session: Any | None = None,
    timeout: float = 30.0,
) -> CampaignState:
    """Fetch a remote campaign dossier over HTTP (read-only).

    ``requests`` is imported lazily so that the controller and the test suite
    can import this module without the dependency being installed.
    """
    try:
        import requests
    except ImportError as exc:  # pragma: no cover - dependency is in the workflow venv
        raise CampaignStateError("the 'requests' package is required to fetch remote state") from exc

    http = session or requests
    try:
        response = http.get(url, timeout=timeout)
    except Exception as exc:  # network failures are campaign blockers, not evidence
        raise CampaignStateError(f"remote campaign state request failed: {exc}") from exc

    status_code = getattr(response, "status_code", 200)
    if status_code != 200:
        raise CampaignStateError(f"remote campaign state request returned HTTP {status_code}")

    try:
        payload = response.json()
    except Exception as exc:
        raise CampaignStateError(f"remote campaign state is not valid JSON: {exc}") from exc

    state = CampaignState.from_dict(payload)
    return replace(state, remote_source=url)


def build_resume_state(
    local_path: str | Path,
    *,
    remote_url: str | None = None,
    session: Any | None = None,
) -> tuple[CampaignState, list[str]]:
    """Load local state, optionally merge a remote dossier, and plan the resume."""
    state = load_state(local_path)
    if remote_url:
        state = apply_remote_state(state, fetch_remote_state(remote_url, session=session))
    return state, resume_plan(state)


def state_summary(state: CampaignState) -> dict[str, Any]:
    """Return a compact, JSON-safe summary of a campaign state."""
    counts: dict[str, int] = {status: 0 for status in sorted(STEP_STATUSES)}
    for step in state.steps:
        counts[step.status] = counts.get(step.status, 0) + 1
    return {
        "campaign_id": state.campaign_id,
        "updated_at": state.updated_at,
        "step_count": len(state.steps),
        "status_counts": counts,
        "next_steps": resume_plan(state),
        "conflicts": list(state.conflicts),
    }


def format_summary(state: CampaignState) -> str:
    """Render a human-readable one-block summary of a campaign state."""
    summary = state_summary(state)
    lines: Sequence[str] = (
        f"campaign: {summary['campaign_id']}",
        f"updated_at: {summary['updated_at']}",
        f"steps: {summary['step_count']} "
        f"({', '.join(f'{key}={value}' for key, value in summary['status_counts'].items() if value)})",
        f"next: {', '.join(summary['next_steps']) or '(none)'}",
    )
    if summary["conflicts"]:
        lines.append(f"conflicts: {len(summary['conflicts'])}")
    return "\n".join(lines)

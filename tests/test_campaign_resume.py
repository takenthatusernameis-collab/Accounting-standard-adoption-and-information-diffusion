"""Regression tests for resumable research-campaign state.

The worker loop can be interrupted between any two cycles, and the next agent
must be able to resume from durable state instead of re-running finished work
or, worse, treating a corrupted state file as "everything is complete". These
tests pin the resume contract used by `research/HANDOFF.md` and
`research/campaign_state.json`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.campaign_resume import (
    STEP_STATUSES,
    CampaignState,
    CampaignStateError,
    apply_remote_state,
    build_resume_state,
    fetch_remote_state,
    format_summary,
    load_state,
    mark_step,
    new_state,
    resume_plan,
    save_state,
    state_summary,
)


def test_new_state_creates_pending_steps() -> None:
    state = new_state("ACCTCLOCK", ["phase0", "phase1", "phase2"])
    assert state.campaign_id == "ACCTCLOCK"
    assert [step.status for step in state.steps] == ["pending", "pending", "pending"]
    assert resume_plan(state) == ["phase0", "phase1", "phase2"]


def test_completed_steps_leave_the_resume_plan() -> None:
    state = new_state("ACCTCLOCK", ["phase0", "phase1", "phase2"])
    state = mark_step(state, "phase0", "completed", result={"files": 3})
    assert resume_plan(state) == ["phase1", "phase2"]


def test_interrupted_step_is_resumed_first() -> None:
    state = new_state("ACCTCLOCK", ["phase0", "phase1", "phase2"])
    state = mark_step(state, "phase0", "completed")
    state = mark_step(state, "phase1", "in_progress")
    state = mark_step(state, "phase2", "in_progress")
    assert resume_plan(state) == ["phase1", "phase2"]


def test_failed_steps_are_retried_on_resume() -> None:
    state = new_state("ACCTCLOCK", ["phase0", "phase1"])
    state = mark_step(state, "phase0", "failed", error="missing data")
    assert resume_plan(state) == ["phase0", "phase1"]
    assert state.pending_steps()[0].id == "phase0"


def test_marking_a_step_in_progress_counts_the_attempt() -> None:
    state = new_state("ACCTCLOCK", ["phase0"])
    state = mark_step(state, "phase0", "in_progress")
    state = mark_step(state, "phase0", "failed", error="boom")
    state = mark_step(state, "phase0", "in_progress")
    step = state.step("phase0")
    assert step is not None
    assert step.attempts == 2
    assert step.status == "in_progress"


def test_completion_records_the_result_and_clears_the_error() -> None:
    state = new_state("ACCTCLOCK", ["phase0"])
    state = mark_step(state, "phase0", "failed", error="boom")
    state = mark_step(state, "phase0", "completed", result={"ok": True})
    step = state.step("phase0")
    assert step is not None
    assert step.result == {"ok": True}
    assert step.error is None
    assert step.finished_at is not None


def test_unknown_step_and_status_are_rejected() -> None:
    state = new_state("ACCTCLOCK", ["phase0"])
    with pytest.raises(CampaignStateError):
        mark_step(state, "missing", "completed")
    with pytest.raises(CampaignStateError):
        mark_step(state, "phase0", "almost_done")
    assert "completed" in STEP_STATUSES


def test_state_round_trips_through_disk(tmp_path: Path) -> None:
    state = new_state("ACCTCLOCK", ["phase0", "phase1"])
    state = mark_step(state, "phase0", "completed", result={"n": 2})
    path = save_state(tmp_path / "campaign_state.json", state)

    restored = load_state(path)
    assert restored.campaign_id == "ACCTCLOCK"
    assert restored.step("phase0") is not None
    assert restored.step("phase0").result == {"n": 2}
    assert resume_plan(restored) == ["phase1"]


def test_saved_state_is_plain_json(tmp_path: Path) -> None:
    state = new_state("ACCTCLOCK", ["phase0"])
    path = save_state(tmp_path / "campaign_state.json", state)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["steps"][0]["id"] == "phase0"


def test_missing_state_file_raises(tmp_path: Path) -> None:
    with pytest.raises(CampaignStateError):
        load_state(tmp_path / "absent.json")


def test_corrupt_state_file_raises(tmp_path: Path) -> None:
    path = tmp_path / "campaign_state.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(CampaignStateError):
        load_state(path)


def test_state_without_campaign_id_raises(tmp_path: Path) -> None:
    path = tmp_path / "campaign_state.json"
    path.write_text('{"steps": []}', encoding="utf-8")
    with pytest.raises(CampaignStateError):
        load_state(path)


def test_remote_state_is_merged_only_where_local_is_incomplete() -> None:
    local = new_state("ACCTCLOCK", ["phase0", "phase1"])
    local = mark_step(local, "phase0", "completed", result={"local": True})
    local = mark_step(local, "phase1", "pending")

    remote = new_state("ACCTCLOCK", ["phase0", "phase1"])
    remote = mark_step(remote, "phase0", "completed", result={"remote": True})
    remote = mark_step(remote, "phase1", "completed", result={"remote": True})

    merged = apply_remote_state(local, remote)
    assert merged.step("phase0").result == {"local": True}
    assert merged.step("phase1").status == "completed"
    assert merged.step("phase1").result == {"remote": True}


def test_remote_merge_records_conflicts_instead_of_choosing_silently() -> None:
    local = new_state("ACCTCLOCK", ["phase0"])
    local = mark_step(local, "phase0", "completed", result={"local": True})
    remote = new_state("ACCTCLOCK", ["phase0"])
    remote = mark_step(remote, "phase0", "failed", error="remote failure")

    merged = apply_remote_state(local, remote)
    assert merged.step("phase0").status == "completed"
    assert merged.conflicts
    assert "phase0" in merged.conflicts[0]


def test_fetch_remote_state_uses_the_provided_session() -> None:
    class FakeResponse:
        status_code = 200

        @staticmethod
        def json() -> dict:
            return {
                "campaign_id": "ACCTCLOCK",
                "steps": [{"id": "phase0", "status": "completed"}],
            }

    class FakeSession:
        def __init__(self) -> None:
            self.requested: list[str] = []

        def get(self, url: str, timeout: float = 30.0) -> FakeResponse:
            self.requested.append(url)
            return FakeResponse()

    session = FakeSession()
    state = fetch_remote_state("https://example.invalid/dossier.json", session=session)
    assert session.requested == ["https://example.invalid/dossier.json"]
    assert state.step("phase0").status == "completed"
    assert state.remote_source == "https://example.invalid/dossier.json"


def test_fetch_remote_state_reports_http_failures() -> None:
    class FakeResponse:
        status_code = 404

    class FakeSession:
        def get(self, url: str, timeout: float = 30.0) -> FakeResponse:
            return FakeResponse()

    with pytest.raises(CampaignStateError):
        fetch_remote_state("https://example.invalid/missing.json", session=FakeSession())


def test_fetch_remote_state_reports_network_failures() -> None:
    class FakeSession:
        def get(self, url: str, timeout: float = 30.0) -> object:
            raise OSError("network unreachable")

    with pytest.raises(CampaignStateError):
        fetch_remote_state("https://example.invalid/dossier.json", session=FakeSession())


def test_build_resume_state_merges_and_plans(tmp_path: Path) -> None:
    path = tmp_path / "campaign_state.json"
    save_state(path, new_state("ACCTCLOCK", ["phase0", "phase1"]))

    class FakeResponse:
        status_code = 200

        @staticmethod
        def json() -> dict:
            return {
                "campaign_id": "ACCTCLOCK",
                "steps": [
                    {"id": "phase0", "status": "completed"},
                    {"id": "phase1", "status": "pending"},
                ],
            }

    class FakeSession:
        def get(self, url: str, timeout: float = 30.0) -> FakeResponse:
            return FakeResponse()

    state, plan = build_resume_state(
        path, remote_url="https://example.invalid/dossier.json", session=FakeSession()
    )
    assert isinstance(state, CampaignState)
    assert state.step("phase0").status == "completed"
    assert plan == ["phase1"]


def test_summary_reports_counts_and_next_steps() -> None:
    state = new_state("ACCTCLOCK", ["phase0", "phase1"])
    state = mark_step(state, "phase0", "completed")
    summary = state_summary(state)
    assert summary["campaign_id"] == "ACCTCLOCK"
    assert summary["step_count"] == 2
    assert summary["status_counts"]["completed"] == 1
    assert summary["next_steps"] == ["phase1"]
    assert "phase1" in format_summary(state)

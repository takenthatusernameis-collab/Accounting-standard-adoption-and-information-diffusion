"""Regression tests for the workflow's inline diagnostics collector.

The collector that classifies completed workflow runs lives inside
`.github/workflows/main.yml` as an inline heredoc. It is the only durable
writer of `research_state/workflow_run_diagnostics.jsonl`, and a silent
regression there would hide exactly the failures this repository depends on
(the previous recorded run failed because a required test file was missing).

The tests extract the inline module from the workflow file, execute only its
helper definitions (never the collector's top-level side effects), and assert
the behaviour the ledger depends on.
"""

from __future__ import annotations

import io
import textwrap
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "main.yml"

#: Marker for the start of the collector's top-level side effects. Everything
#: before it is safe to execute in isolation.
COLLECTOR_ENTRY_MARKER = "LEDGER.parent.mkdir("


def _heredoc_blocks(text: str) -> list[list[str]]:
    lines = text.splitlines()
    blocks: list[list[str]] = []
    index = 0
    while index < len(lines):
        if "<<'PYTHON'" in lines[index]:
            start = index + 1
            end = start
            while end < len(lines) and lines[end].strip() != "PYTHON":
                end += 1
            blocks.append(lines[start:end])
            index = end + 1
            continue
        index += 1
    return blocks


def _collector_source() -> str:
    text = WORKFLOW.read_text(encoding="utf-8")
    candidates = [
        block for block in _heredoc_blocks(text) if any("def redact(" in line for line in block)
    ]
    assert candidates, "the diagnostics collector block was not found in the workflow file"
    source = textwrap.dedent("\n".join(candidates[0]))
    entry = source.index(COLLECTOR_ENTRY_MARKER)
    return source[:entry]


@pytest.fixture(scope="module")
def scanner() -> dict:
    """Execute the collector's helper definitions without its side effects."""
    namespace: dict = {"__name__": "workflow_diagnostics_scanner"}
    with pytest.MonkeyPatch.context() as environment:
        # The collector reads these at import time; the helpers never use them.
        environment.setenv("REPOSITORY", "example/repository")
        environment.setenv("GITHUB_TOKEN", "test-token")
        exec(compile(_collector_source(), str(WORKFLOW), "exec"), namespace)
    assert "redact" in namespace
    return namespace


def test_collector_source_is_extracted(scanner: dict) -> None:
    for name in (
        "redact",
        "classify_jobs",
        "run_key",
        "load_ledger",
        "select_runs_for_processing",
        "preserve_additional_fields",
        "scan_log_archive",
    ):
        assert name in scanner


# --------------------------------------------------------------------------
# Secret redaction
# --------------------------------------------------------------------------


def test_redact_removes_bearer_tokens(scanner: dict) -> None:
    redacted = scanner["redact"]("Authorization: Bearer abcdef0123456789abcdefghijklmnop")
    assert "abcdef0123456789" not in redacted
    assert "REDACTED" in redacted


def test_redact_removes_github_tokens(scanner: dict) -> None:
    token = "ghp_" + "a" * 36
    redacted = scanner["redact"](f"token={token} rest")
    assert token not in redacted
    assert "REDACTED" in redacted


def test_redact_removes_jwt(scanner: dict) -> None:
    jwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dBjftJeZ4CVPmB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    redacted = scanner["redact"](f"authorization: {jwt}")
    assert jwt not in redacted
    assert "REDACTED" in redacted


def test_redact_removes_secret_assignments(scanner: dict) -> None:
    redacted = scanner["redact"]("api_key=super-secret-value")
    assert "super-secret-value" not in redacted
    assert "REDACTED" in redacted


def test_redact_removes_signed_url_secrets(scanner: dict) -> None:
    redacted = scanner["redact"]("https://example.com/logs?X-Amz-Signature=deadbeefcafe&x=1")
    assert "deadbeefcafe" not in redacted
    assert "X-Amz-Signature=[REDACTED]" in redacted


def test_redact_truncates_long_values(scanner: dict) -> None:
    redacted = scanner["redact"]("payload " + "A" * 400)
    assert len(redacted) <= scanner["MAX_EXCERPT_CHARS"]
    assert "REDACTED_LONG_VALUE" in redacted


# --------------------------------------------------------------------------
# Job and step classification
# --------------------------------------------------------------------------


def test_classify_jobs_accepts_successful_jobs(scanner: dict) -> None:
    jobs = [
        {
            "id": 1,
            "name": "kilo",
            "conclusion": "success",
            "html_url": "https://example.invalid/job/1",
            "steps": [
                {"number": 1, "name": "checkout", "outcome": "success", "conclusion": "success"},
                {"number": 2, "name": "run", "outcome": "skipped", "conclusion": "skipped"},
            ],
        }
    ]
    assert scanner["classify_jobs"](jobs) == []


def test_classify_jobs_flags_failed_job_and_step(scanner: dict) -> None:
    jobs = [
        {
            "id": 7,
            "name": "kilo",
            "conclusion": "failure",
            "html_url": "https://example.invalid/job/7",
            "steps": [
                {
                    "number": 3,
                    "name": "Test controller progress and diagnostic scanning",
                    "outcome": "failure",
                    "conclusion": "failure",
                }
            ],
        }
    ]
    errors = scanner["classify_jobs"](jobs)
    kinds = {error["type"] for error in errors}
    assert "job_conclusion" in kinds
    assert "step_outcome_or_conclusion" in kinds


def test_classify_jobs_preserves_continue_on_error_outcomes(scanner: dict) -> None:
    jobs = [
        {
            "id": 9,
            "name": "kilo",
            "conclusion": "success",
            "steps": [
                {"number": 4, "name": "collect", "outcome": "failure", "conclusion": "success"}
            ],
        }
    ]
    errors = scanner["classify_jobs"](jobs)
    assert errors == [
        {
            "type": "step_outcome_or_conclusion",
            "job_id": 9,
            "job_name": "kilo",
            "step_number": 4,
            "step_name": "collect",
            "outcome": "failure",
            "conclusion": "success",
        }
    ]


# --------------------------------------------------------------------------
# Ledger handling
# --------------------------------------------------------------------------


def test_run_key_combines_id_and_attempt(scanner: dict) -> None:
    assert scanner["run_key"]({"id": 42, "run_attempt": 2}) == "42:2"
    assert scanner["run_key"]({"run_id": 42}) == "42:1"
    assert scanner["run_key"]({}) is None


def test_load_ledger_reads_records_and_ignores_blank_lines(
    scanner: dict, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ledger = tmp_path / "workflow_run_diagnostics.jsonl"
    ledger.write_text(
        '{"run_id": 1, "run_attempt": 1}\n\n{"run_id": 2, "run_attempt": 1}\n',
        encoding="utf-8",
    )
    monkeypatch.setitem(scanner, "LEDGER", ledger)
    records = scanner["load_ledger"]()
    assert set(records) == {"1:1", "2:1"}


def test_load_ledger_refuses_to_discard_invalid_records(
    scanner: dict, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ledger = tmp_path / "workflow_run_diagnostics.jsonl"
    ledger.write_text('{"run_id": 1, "run_attempt": 1}\nnot-json\n', encoding="utf-8")
    monkeypatch.setitem(scanner, "LEDGER", ledger)
    with pytest.raises(RuntimeError):
        scanner["load_ledger"]()


def test_select_runs_for_processing_picks_new_and_stale_records(scanner: dict) -> None:
    runs = [
        {"id": 1, "run_attempt": 1, "updated_at": "2026-10-21T19:00:00Z"},
        {"id": 2, "run_attempt": 1, "updated_at": "2026-10-21T20:00:00Z"},
        {"id": 3, "run_attempt": 1, "updated_at": "2026-10-21T18:00:00Z"},
    ]
    records = {
        "1:1": {
            "run_id": 1,
            "run_attempt": 1,
            "status": "completed",
            "conclusion": "failure",
            "run_completed_at": "2026-10-21T19:00:00Z",
            "capture_status": "complete",
        },
        "2:1": {
            "run_id": 2,
            "run_attempt": 1,
            "status": "in_progress",
            "conclusion": None,
            "run_completed_at": None,
            "capture_status": "complete",
        },
    }
    selected = scanner["select_runs_for_processing"](runs, records)
    selected_ids = [run["id"] for run, _existing in selected]
    assert selected_ids == [2, 3]


def test_select_runs_for_processing_caps_the_batch(scanner: dict) -> None:
    runs = [
        {"id": index, "run_attempt": 1, "updated_at": f"2026-10-21T{index:02d}:00:00Z"}
        for index in range(1, 60)
    ]
    selected = scanner["select_runs_for_processing"](runs, {})
    assert len(selected) == scanner["MAX_NEW_RUNS_PER_INVOCATION"]


def test_preserve_additional_fields_keeps_repository_metadata(scanner: dict) -> None:
    previous = {"run_id": 5, "local_note": "kept"}
    record = {"run_id": 5, "status": "completed"}
    merged = scanner["preserve_additional_fields"](record, previous)
    assert merged["local_note"] == "kept"
    assert merged["status"] == "completed"


# --------------------------------------------------------------------------
# Log scanning
# --------------------------------------------------------------------------


def _log_archive(files: dict[str, str]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return buffer.getvalue()


def test_scan_log_archive_surfaces_real_errors(
    scanner: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive = _log_archive(
        {
            "0_kilo.txt": (
                "2026-10-21T19:16:08.8049804Z ERROR: file or directory not found: "
                "tests/test_controller_progress_accounting.py\n"
                "2026-10-21T19:16:11.9702218Z   TEST_OUTCOME: failure\n"
            )
        }
    )
    monkeypatch.setitem(scanner, "download_log_archive", lambda run: (archive, False))
    signals, status = scanner["scan_log_archive"]({"id": 1})
    assert status == "scanned"
    assert any("file or directory not found" in signal["excerpt"] for signal in signals)


def test_scan_log_archive_ignores_echoed_workflow_source(
    scanner: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    echo = "\x1b[36;1m          if [[ \"$TEST_OUTCOME\" != \"success\" ]]; then failed=1; fi\x1b[0m\n"
    archive = _log_archive({"0_kilo.txt": echo})
    monkeypatch.setitem(scanner, "download_log_archive", lambda run: (archive, False))
    signals, status = scanner["scan_log_archive"]({"id": 1})
    assert status == "scanned"
    assert signals == []


def test_scan_log_archive_prioritizes_the_kilo_abort_signal(
    scanner: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive = _log_archive(
        {
            "0_kilo.txt": (
                "Traceback (most recent call last):\n"
                "Kilo stopped after 3 consecutive invalid argument failures for the 'edit' tool\n"
            )
        }
    )
    monkeypatch.setitem(scanner, "download_log_archive", lambda run: (archive, False))
    signals, _status = scanner["scan_log_archive"]({"id": 1})
    assert signals
    assert signals[0]["signal_kind"] == "kilo_invalid_argument_turn_abort"


def test_scan_log_archive_reports_unreadable_archives(
    scanner: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setitem(scanner, "download_log_archive", lambda run: (b"not-a-zip", False))
    signals, status = scanner["scan_log_archive"]({"id": 1})
    assert signals == []
    assert status == "archive_not_readable_as_zip"

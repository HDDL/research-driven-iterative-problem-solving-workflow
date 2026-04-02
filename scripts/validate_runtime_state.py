#!/usr/bin/env python3
"""Validate ARPS v0.7 runtime state and evidence logs.

Usage:
  python scripts/validate_runtime_state.py STATE.json
  python scripts/validate_runtime_state.py STATE.json evidence_log.jsonl
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


STAGES = {
    "inventory",
    "orient",
    "reframe",
    "model",
    "review",
    "options",
    "evaluate",
    "act",
    "reflect",
    "synthesize",
}

CONFIDENCE_LEVELS = {"very_low", "low", "medium", "high", "very_high"}
TERMINAL_CONDITIONS = {
    "solved",
    "bounded_recommendation_ready",
    "blocked_waiting_for_external_input",
    "budget_exhausted",
    "unsafe_to_continue",
}
PROGRESS_MARKERS = {
    "new_independent_evidence_changes_hypothesis_status",
    "new_external_signal_received",
    "dominant_uncertainty_reduced_or_resolved",
    "option_or_work_item_rejected_with_evidence_backed_reason",
    "blocker_removed",
    "hard_check_or_guard_newly_passes",
    "confidence_ceiling_increases_from_new_independent_evidence",
}


class ValidationError(Exception):
    pass


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise ValidationError(f"duplicate key {key!r}")
        obj[key] = value
    return obj


def _load_json(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValidationError(f"{path}: file not found") from exc
    except OSError as exc:
        raise ValidationError(f"{path}: could not read file: {exc}") from exc

    try:
        return json.loads(text, object_pairs_hook=_pairs_no_duplicates)
    except ValidationError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def _expect_mapping(value: Any, path: str, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object, got {type(value).__name__}")
        return None
    return value


def _expect_list(value: Any, path: str, errors: list[str]) -> list[Any] | None:
    if not isinstance(value, list):
        errors.append(f"{path}: expected array, got {type(value).__name__}")
        return None
    return value


def _expect_string(value: Any, path: str, errors: list[str], *, nonempty: bool = True) -> str | None:
    if not isinstance(value, str):
        errors.append(f"{path}: expected string, got {type(value).__name__}")
        return None
    if nonempty and not value:
        errors.append(f"{path}: expected non-empty string")
        return None
    return value


def _expect_bool(value: Any, path: str, errors: list[str]) -> bool | None:
    if not isinstance(value, bool):
        errors.append(f"{path}: expected boolean, got {type(value).__name__}")
        return None
    return value


def _expect_int(value: Any, path: str, errors: list[str], *, minimum: int | None = None) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"{path}: expected integer, got {type(value).__name__}")
        return None
    if minimum is not None and value < minimum:
        errors.append(f"{path}: expected integer >= {minimum}, got {value}")
        return None
    return value


def _expect_string_list(value: Any, path: str, errors: list[str]) -> list[str] | None:
    items = _expect_list(value, path, errors)
    if items is None:
        return None
    out: list[str] = []
    for index, item in enumerate(items):
        s = _expect_string(item, f"{path}[{index}]", errors)
        if s is not None:
            out.append(s)
    return out


def _expect_unique_strings(value: Any, path: str, errors: list[str]) -> list[str] | None:
    items = _expect_string_list(value, path, errors)
    if items is None:
        return None
    seen: set[str] = set()
    for item in items:
        if item in seen:
            errors.append(f"{path}: duplicate value {item!r}")
        seen.add(item)
    return items


def _expect_iso_datetime(value: Any, path: str, errors: list[str]) -> str | None:
    s = _expect_string(value, path, errors)
    if s is None:
        return None
    try:
        parsed = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path}: expected ISO 8601 datetime, got {s!r}")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{path}: expected timezone-aware ISO 8601 datetime, got {s!r}")
        return None
    return s


def validate_state(state: Any, path: Path, errors: list[str]) -> tuple[set[str], set[str]]:
    obj = _expect_mapping(state, str(path), errors)
    if obj is None:
        return set(), set()

    required_fields = [
        "run_id",
        "current_stage",
        "capabilities",
        "active_work_item",
        "pending_work_items",
        "completed_work_items",
        "rejected_options",
        "last_completed_action",
        "last_checkpoint_at",
        "last_external_signal_at",
        "confidence",
        "confidence_ceiling",
        "evidence_log",
        "evidence_sources",
        "last_evaluated_hypotheses",
        "decision_log",
        "progress_log",
        "blockers",
        "waiting_on",
        "waiting_on_external",
        "budgets",
        "counters",
        "terminal_condition",
        "resume_pointer",
        "resume_instructions",
    ]
    for field in required_fields:
        if field not in obj:
            errors.append(f"{path}: missing required field {field!r}")

    _expect_string(obj.get("run_id"), f"{path}.run_id", errors)

    current_stage = _expect_string(obj.get("current_stage"), f"{path}.current_stage", errors)
    if current_stage is not None and current_stage not in STAGES:
        errors.append(
            f"{path}.current_stage: expected one of {sorted(STAGES)}, got {current_stage!r}"
        )

    capabilities = _expect_mapping(obj.get("capabilities"), f"{path}.capabilities", errors)
    if capabilities is not None:
        for field in [
            "can_run_code",
            "can_search_web",
            "can_read_files",
            "can_write_files",
            "can_call_apis",
            "can_ask_human",
        ]:
            if field not in capabilities:
                errors.append(f"{path}.capabilities: missing required field {field!r}")
            else:
                _expect_bool(capabilities[field], f"{path}.capabilities.{field}", errors)
        _expect_unique_strings(capabilities.get("available_tools"), f"{path}.capabilities.available_tools", errors)
        _expect_unique_strings(capabilities.get("hard_limits"), f"{path}.capabilities.hard_limits", errors)

    active_work_item = _expect_string(obj.get("active_work_item"), f"{path}.active_work_item", errors)
    pending_work_items = _expect_unique_strings(
        obj.get("pending_work_items"), f"{path}.pending_work_items", errors
    )
    completed_work_items = _expect_unique_strings(
        obj.get("completed_work_items"), f"{path}.completed_work_items", errors
    )

    state_evidence_ids: set[str] = set()
    referenced_evidence_ids: set[str] = set()
    evidence_source_ids: set[str] = set()
    rejected_options = _expect_list(obj.get("rejected_options"), f"{path}.rejected_options", errors)
    rejected_option_ids: set[str] = set()
    if rejected_options is not None:
        for index, item in enumerate(rejected_options):
            entry = _expect_mapping(item, f"{path}.rejected_options[{index}]", errors)
            if entry is None:
                continue
            rejected_id = _expect_string(entry.get("id"), f"{path}.rejected_options[{index}].id", errors)
            _expect_string(entry.get("reason"), f"{path}.rejected_options[{index}].reason", errors)
            if rejected_id is not None:
                rejected_option_ids.add(rejected_id)
            if "evidence_ids" in entry:
                refs = _expect_unique_strings(
                    entry.get("evidence_ids"), f"{path}.rejected_options[{index}].evidence_ids", errors
                )
                if refs is not None:
                    referenced_evidence_ids.update(refs)

    _expect_string(obj.get("last_completed_action"), f"{path}.last_completed_action", errors)
    _expect_iso_datetime(obj.get("last_checkpoint_at"), f"{path}.last_checkpoint_at", errors)
    _expect_iso_datetime(obj.get("last_external_signal_at"), f"{path}.last_external_signal_at", errors)

    confidence = _expect_string(obj.get("confidence"), f"{path}.confidence", errors)
    if confidence is not None and confidence not in CONFIDENCE_LEVELS:
        errors.append(
            f"{path}.confidence: expected one of {sorted(CONFIDENCE_LEVELS)}, got {confidence!r}"
        )
    confidence_ceiling = _expect_string(
        obj.get("confidence_ceiling"), f"{path}.confidence_ceiling", errors
    )
    if confidence_ceiling is not None and confidence_ceiling not in CONFIDENCE_LEVELS:
        errors.append(
            f"{path}.confidence_ceiling: expected one of {sorted(CONFIDENCE_LEVELS)}, got {confidence_ceiling!r}"
        )

    evidence_log = _expect_list(obj.get("evidence_log"), f"{path}.evidence_log", errors)
    if evidence_log is not None:
        seen: set[str] = set()
        for index, item in enumerate(evidence_log):
            entry = _expect_mapping(item, f"{path}.evidence_log[{index}]", errors)
            if entry is None:
                continue
            evidence_id = _expect_string(entry.get("id"), f"{path}.evidence_log[{index}].id", errors)
            _expect_string(entry.get("kind"), f"{path}.evidence_log[{index}].kind", errors)
            _expect_string(entry.get("summary"), f"{path}.evidence_log[{index}].summary", errors)
            _expect_string(
                entry.get("effect_on_confidence"),
                f"{path}.evidence_log[{index}].effect_on_confidence",
                errors,
            )
            if evidence_id is not None:
                if evidence_id in seen:
                    errors.append(f"{path}.evidence_log: duplicate evidence id {evidence_id!r}")
                seen.add(evidence_id)
                state_evidence_ids.add(evidence_id)
            provenance = None
            if "provenance" in entry:
                provenance = _expect_string(
                    entry.get("provenance"), f"{path}.evidence_log[{index}].provenance", errors
                )
            source_ids = None
            if "source_ids" in entry:
                source_ids = _expect_unique_strings(
                    entry.get("source_ids"), f"{path}.evidence_log[{index}].source_ids", errors
                )
            if provenance is None and not source_ids:
                errors.append(
                    f"{path}.evidence_log[{index}]: expected provenance or source_ids to preserve the evidence trail"
                )

    evidence_sources = _expect_list(obj.get("evidence_sources"), f"{path}.evidence_sources", errors)
    if evidence_sources is not None:
        seen: set[str] = set()
        for index, item in enumerate(evidence_sources):
            entry = _expect_mapping(item, f"{path}.evidence_sources[{index}]", errors)
            if entry is None:
                continue
            source_id = _expect_string(entry.get("id"), f"{path}.evidence_sources[{index}].id", errors)
            _expect_string(entry.get("kind"), f"{path}.evidence_sources[{index}].kind", errors)
            _expect_string(
                entry.get("provenance"), f"{path}.evidence_sources[{index}].provenance", errors
            )
            if source_id is not None:
                if source_id in seen:
                    errors.append(f"{path}.evidence_sources: duplicate source id {source_id!r}")
                seen.add(source_id)
                evidence_source_ids.add(source_id)

    if evidence_log is not None and evidence_source_ids:
        for index, item in enumerate(evidence_log):
            entry = _expect_mapping(item, f"{path}.evidence_log[{index}]", errors)
            if entry is None or "source_ids" not in entry:
                continue
            source_ids = _expect_unique_strings(
                entry.get("source_ids"), f"{path}.evidence_log[{index}].source_ids", errors
            )
            if source_ids is None:
                continue
            missing = sorted(set(source_ids) - evidence_source_ids)
            if missing:
                errors.append(
                    f"{path}.evidence_log[{index}].source_ids: unknown evidence source ids: {', '.join(missing)}"
                )

    last_evaluated_hypotheses = _expect_list(
        obj.get("last_evaluated_hypotheses"), f"{path}.last_evaluated_hypotheses", errors
    )
    if last_evaluated_hypotheses is not None:
        for index, item in enumerate(last_evaluated_hypotheses):
            entry = _expect_mapping(item, f"{path}.last_evaluated_hypotheses[{index}]", errors)
            if entry is None:
                continue
            _expect_string(entry.get("id"), f"{path}.last_evaluated_hypotheses[{index}].id", errors)
            _expect_string(
                entry.get("status"), f"{path}.last_evaluated_hypotheses[{index}].status", errors
            )
            if "supported_by" in entry:
                refs = _expect_unique_strings(
                    entry.get("supported_by"),
                    f"{path}.last_evaluated_hypotheses[{index}].supported_by",
                    errors,
                )
                if refs is not None:
                    referenced_evidence_ids.update(refs)

    decision_log = _expect_list(obj.get("decision_log"), f"{path}.decision_log", errors)
    if decision_log is not None:
        for index, item in enumerate(decision_log):
            entry = _expect_mapping(item, f"{path}.decision_log[{index}]", errors)
            if entry is None:
                continue
            _expect_iso_datetime(entry.get("at"), f"{path}.decision_log[{index}].at", errors)
            _expect_string(entry.get("decision"), f"{path}.decision_log[{index}].decision", errors)
            _expect_string(entry.get("because"), f"{path}.decision_log[{index}].because", errors)
            if "evidence_ids" in entry:
                refs = _expect_unique_strings(
                    entry.get("evidence_ids"), f"{path}.decision_log[{index}].evidence_ids", errors
                )
                if refs is not None:
                    referenced_evidence_ids.update(refs)

    progress_log = _expect_list(obj.get("progress_log"), f"{path}.progress_log", errors)
    if progress_log is not None:
        seen_cycles: set[int] = set()
        last_cycle = -1
        for index, item in enumerate(progress_log):
            entry = _expect_mapping(item, f"{path}.progress_log[{index}]", errors)
            if entry is None:
                continue
            cycle = _expect_int(entry.get("cycle"), f"{path}.progress_log[{index}].cycle", errors, minimum=1)
            if cycle is not None:
                if cycle in seen_cycles:
                    errors.append(f"{path}.progress_log: duplicate cycle {cycle}")
                if cycle <= last_cycle:
                    errors.append(f"{path}.progress_log: cycles must be strictly increasing")
                seen_cycles.add(cycle)
                last_cycle = cycle
            markers = _expect_unique_strings(entry.get("markers"), f"{path}.progress_log[{index}].markers", errors)
            if markers is not None:
                invalid_markers = sorted(set(markers) - PROGRESS_MARKERS)
                if invalid_markers:
                    errors.append(
                        f"{path}.progress_log[{index}].markers: expected only {sorted(PROGRESS_MARKERS)}, got invalid values: {', '.join(invalid_markers)}"
                    )
            refs = None
            if "evidence_ids" in entry:
                refs = _expect_unique_strings(
                    entry.get("evidence_ids"), f"{path}.progress_log[{index}].evidence_ids", errors
                )
                if refs is not None:
                    referenced_evidence_ids.update(refs)
            if markers is not None and markers and not refs:
                errors.append(
                    f"{path}.progress_log[{index}]: non-empty markers require evidence_ids"
                )

    _expect_unique_strings(obj.get("blockers"), f"{path}.blockers", errors)
    waiting_on = _expect_unique_strings(obj.get("waiting_on"), f"{path}.waiting_on", errors)
    waiting_on_external = _expect_unique_strings(
        obj.get("waiting_on_external"), f"{path}.waiting_on_external", errors
    )
    if waiting_on is not None and waiting_on_external is not None:
        missing = sorted(set(waiting_on_external) - set(waiting_on))
        if missing:
            errors.append(
                f"{path}.waiting_on_external: values must also appear in waiting_on: {', '.join(missing)}"
            )

    budgets = _expect_mapping(obj.get("budgets"), f"{path}.budgets", errors)
    if budgets is not None:
        for field in [
            "iterations_remaining",
            "no_progress_cycles_remaining",
            "external_signal_cycles_remaining",
        ]:
            if field not in budgets:
                errors.append(f"{path}.budgets: missing required field {field!r}")
            else:
                _expect_int(budgets[field], f"{path}.budgets.{field}", errors, minimum=0)

    counters = _expect_mapping(obj.get("counters"), f"{path}.counters", errors)
    if counters is not None:
        for field in [
            "consecutive_no_progress",
            "consecutive_discards",
            "repeated_failure_type_count",
        ]:
            if field not in counters:
                errors.append(f"{path}.counters: missing required field {field!r}")
            else:
                _expect_int(counters[field], f"{path}.counters.{field}", errors, minimum=0)
        if progress_log is not None and "consecutive_no_progress" in counters:
            consecutive_no_progress = _expect_int(
                counters.get("consecutive_no_progress"),
                f"{path}.counters.consecutive_no_progress",
                errors,
                minimum=0,
            )
            if consecutive_no_progress is not None:
                observed = 0
                for item in reversed(progress_log):
                    entry = _expect_mapping(item, "<internal>", [])
                    if entry is None:
                        break
                    markers = entry.get("markers")
                    if isinstance(markers, list) and len(markers) == 0:
                        observed += 1
                    else:
                        break
                if consecutive_no_progress != observed:
                    errors.append(
                        f"{path}.counters.consecutive_no_progress: expected {observed} based on trailing empty progress markers, got {consecutive_no_progress}"
                    )

    terminal_condition = _expect_string(obj.get("terminal_condition"), f"{path}.terminal_condition", errors)
    if terminal_condition is not None and terminal_condition not in TERMINAL_CONDITIONS:
        errors.append(
            f"{path}.terminal_condition: expected one of {sorted(TERMINAL_CONDITIONS)}, got {terminal_condition!r}"
        )

    resume_pointer = _expect_mapping(obj.get("resume_pointer"), f"{path}.resume_pointer", errors)
    if resume_pointer is not None:
        work_item_id = _expect_string(
            resume_pointer.get("work_item_id"), f"{path}.resume_pointer.work_item_id", errors
        )
        _expect_string(resume_pointer.get("attempt_id"), f"{path}.resume_pointer.attempt_id", errors)
        stage = _expect_string(resume_pointer.get("stage"), f"{path}.resume_pointer.stage", errors)
        if stage is not None and stage not in STAGES:
            errors.append(
                f"{path}.resume_pointer.stage: expected one of {sorted(STAGES)}, got {stage!r}"
            )
        checkpoint_namespace = _expect_string(
            resume_pointer.get("checkpoint_namespace"),
            f"{path}.resume_pointer.checkpoint_namespace",
            errors,
        )
        _expect_string(resume_pointer.get("next_step"), f"{path}.resume_pointer.next_step", errors)
        resumable_items: set[str] = set()
        if active_work_item is not None:
            resumable_items.add(active_work_item)
        if pending_work_items is not None:
            resumable_items.update(pending_work_items)
        if work_item_id is not None and not resumable_items:
            errors.append(
                f"{path}.resume_pointer.work_item_id: no active or pending work items are available to resume"
            )
        if work_item_id is not None and resumable_items and work_item_id not in resumable_items:
            errors.append(
                f"{path}.resume_pointer.work_item_id: expected one of the active or pending work items {sorted(resumable_items)}, got {work_item_id!r}"
            )
        if completed_work_items is not None and work_item_id is not None and work_item_id in completed_work_items:
            errors.append(
                f"{path}.resume_pointer.work_item_id: completed work items cannot be resume targets without an explicit invalidation record"
            )
        if work_item_id is not None and work_item_id in rejected_option_ids:
            errors.append(
                f"{path}.resume_pointer.work_item_id: rejected work items cannot be resume targets"
            )
        if (
            current_stage is not None
            and stage is not None
            and current_stage != stage
        ):
            errors.append(
                f"{path}.resume_pointer.stage: expected to match current_stage {current_stage!r}, got {stage!r}"
            )
        if (
            work_item_id is not None
            and checkpoint_namespace is not None
            and work_item_id != checkpoint_namespace
        ):
            errors.append(
                f"{path}.resume_pointer.checkpoint_namespace: expected {work_item_id!r} to match the resumed work item id"
            )

    _expect_string(obj.get("resume_instructions"), f"{path}.resume_instructions", errors)

    if budgets is not None and waiting_on_external is not None and terminal_condition is not None:
        remaining = budgets.get("external_signal_cycles_remaining")
        if (
            isinstance(remaining, int)
            and remaining == 0
            and waiting_on_external
            and terminal_condition != "blocked_waiting_for_external_input"
        ):
            errors.append(
                f"{path}: external_signal_cycles_remaining is 0 while waiting_on_external is non-empty; terminal_condition should be 'blocked_waiting_for_external_input'"
            )

    return state_evidence_ids, referenced_evidence_ids


def validate_evidence_log(path: Path, errors: list[str]) -> set[str]:
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise ValidationError(f"{path}: file not found") from exc
    except OSError as exc:
        raise ValidationError(f"{path}: could not read file: {exc}") from exc

    evidence_ids: set[str] = set()
    seen: set[str] = set()
    for line_no, raw_line in enumerate(raw_lines, start=1):
        if not raw_line.strip():
            errors.append(f"{path}:{line_no}: blank line is not valid JSONL")
            continue
        try:
            record = json.loads(raw_line, object_pairs_hook=_pairs_no_duplicates)
        except ValidationError as exc:
            errors.append(f"{path}:{line_no}: invalid JSON: {exc}")
            continue
        except json.JSONDecodeError as exc:
            errors.append(
                f"{path}:{line_no}: invalid JSON at column {exc.colno}: {exc.msg}"
            )
            continue

        entry = _expect_mapping(record, f"{path}:{line_no}", errors)
        if entry is None:
            continue
        evidence_id = _expect_string(entry.get("id"), f"{path}:{line_no}.id", errors)
        _expect_string(entry.get("kind"), f"{path}:{line_no}.kind", errors)
        _expect_string(entry.get("summary"), f"{path}:{line_no}.summary", errors)
        _expect_string(entry.get("effect_on_confidence"), f"{path}:{line_no}.effect_on_confidence", errors)
        provenance = None
        if "provenance" in entry:
            provenance = _expect_string(entry.get("provenance"), f"{path}:{line_no}.provenance", errors)
        source_ids = None
        if "source_ids" in entry:
            source_ids = _expect_unique_strings(entry.get("source_ids"), f"{path}:{line_no}.source_ids", errors)
        if provenance is None and not source_ids:
            errors.append(f"{path}:{line_no}: expected provenance or source_ids")
        if "timestamp" in entry:
            _expect_iso_datetime(entry.get("timestamp"), f"{path}:{line_no}.timestamp", errors)

        if evidence_id is not None:
            if evidence_id in seen:
                errors.append(f"{path}:{line_no}: duplicate evidence id {evidence_id!r}")
            seen.add(evidence_id)
            evidence_ids.add(evidence_id)

    return evidence_ids


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print(
            "Usage: python scripts/validate_runtime_state.py STATE.json [evidence_log.jsonl]",
            file=sys.stderr,
        )
        return 2

    state_path = Path(argv[1])
    evidence_path = Path(argv[2]) if len(argv) == 3 else None

    errors: list[str] = []

    state_evidence_ids: set[str] = set()
    referenced_evidence_ids: set[str] = set()
    state_ok = False
    try:
        state = _load_json(state_path)
        state_evidence_ids, referenced_evidence_ids = validate_state(state, state_path, errors)
        state_ok = True
    except ValidationError as exc:
        errors.append(str(exc))

    evidence_log_ids: set[str] = set()
    evidence_ok = False
    if evidence_path is not None:
        try:
            evidence_log_ids = validate_evidence_log(evidence_path, errors)
            evidence_ok = True
        except ValidationError as exc:
            errors.append(str(exc))

    if state_ok:
        known_evidence_ids = set(state_evidence_ids)
        if evidence_path is not None:
            if evidence_ok:
                known_evidence_ids |= evidence_log_ids
            else:
                known_evidence_ids = set()

        if evidence_path is None or evidence_ok:
            missing_refs = sorted(referenced_evidence_ids - known_evidence_ids)
            if missing_refs:
                errors.append(
                    f"{state_path}: evidence references not found in the available evidence records: {', '.join(missing_refs)}"
                )

    if state_ok and evidence_ok and evidence_path is not None:
        missing = sorted(state_evidence_ids - evidence_log_ids)
        if missing:
            errors.append(
                f"{state_path}: evidence_log ids not found in {evidence_path}: {', '.join(missing)}"
            )

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if evidence_path is None:
        print(f"OK: {state_path}")
    else:
        print(f"OK: {state_path} and {evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

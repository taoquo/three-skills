#!/usr/bin/env python3
"""Validate shader-port route fixtures."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SHADER_PORT_SCRIPTS_DIR = REPO_ROOT / "skills" / "shader-port" / "scripts"
if str(SHADER_PORT_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SHADER_PORT_SCRIPTS_DIR))

from fixture_schema import (
    fixture_option_lists,
    fixture_report_lists,
    primary_contract_to_backend_promises_map,
    route_to_status_map,
)

FIXTURES_ROOT = REPO_ROOT / "skills" / "shader-port" / "fixtures"
REPORT_TEMPLATE_PATH = REPO_ROOT / "skills" / "shader-port" / "assets" / "report-template.md"
FIXTURE_INDEX_PATH = FIXTURES_ROOT / "README.md"
REQUIRED_CASE_FILES = ("README.md", "REPORT.md", "fixture.json")
REQUIRED_RUNNABLE_FILES = ("index.html", "main.js")
OPTION_LISTS = fixture_option_lists()
REPORT_LISTS = fixture_report_lists()
SUMMARY_FIELD_LABELS = tuple(REPORT_LISTS["required_summary_fields"])
VALID_CLASSIFICATIONS = set(OPTION_LISTS["classifications"])
VALID_AUTHORING_ROUTES = set(OPTION_LISTS["authoring_routes"])
VALID_STATUS_LABELS = set(OPTION_LISTS["status_labels"])
VALID_PRIMARY_RENDERER_CONTRACTS = set(OPTION_LISTS["primary_renderer_contracts"])
VALID_FALLBACK_CONTRACTS = set(OPTION_LISTS["fallback_contracts"])
VALID_VERIFIED_PATHS = set(OPTION_LISTS["verified_paths"])
BACKEND_TABLE_PATHS = (
    "`WebGPU` via `WebGPURenderer`",
    "`WebGL2` backend via `WebGPURenderer`",
    "Raw `WebGLRenderer` path",
)
ROUTE_TO_STATUS = route_to_status_map()
PRIMARY_CONTRACT_TO_BACKEND_PROMISES = primary_contract_to_backend_promises_map()
PLACEHOLDER_PATTERNS = (
    "__FIXTURE_OR_TASK_NAME__",
    "`TODO`",
)


def collect_case_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return [path for path in sorted(root.iterdir()) if path.is_dir()]


def extract_h2_headings(text: str) -> list[str]:
    return re.findall(r"^## .+$", text, re.M)


def extract_section(text: str, heading: str) -> str | None:
    pattern = rf"^{re.escape(heading)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1).strip() if match else None


def extract_summary_field(text: str, label: str) -> str | None:
    pattern = rf"^- {re.escape(label)}:\s*`([^`]+)`\s*$"
    match = re.search(pattern, text, re.M)
    return match.group(1).strip() if match else None


def extract_summary_labels(text: str) -> list[str]:
    summary_section = extract_section(text, "## Summary")
    if summary_section is None:
        return []
    return re.findall(r"^- ([^:]+):\s*`[^`]+`\s*$", summary_section, re.M)


def extract_bullet_value(section_text: str, label: str) -> str | None:
    pattern = rf"^- {re.escape(label)}:\s*`([^`]+)`\s*$"
    match = re.search(pattern, section_text, re.M)
    return match.group(1).strip() if match else None


def parse_renderer_backend_contract(section_text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for raw_line in section_text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        match = re.match(r"^\|\s*(.+?)\s*\|\s*`?(yes|no)`?\s*\|", line)
        if not match:
            continue
        rows[match.group(1).strip()] = match.group(2).strip()
    return rows


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a top-level object")
    return data


def validate_fixture_index(case_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    if not FIXTURE_INDEX_PATH.exists():
        return [f"{FIXTURES_ROOT}: missing README.md"]

    text = FIXTURE_INDEX_PATH.read_text()
    for case_dir in case_dirs:
        expected_ref = f"[{case_dir.name}/README.md]({case_dir.name}/README.md)"
        if expected_ref not in text:
            errors.append(f"{FIXTURE_INDEX_PATH}: missing fixture index entry for {case_dir.name}")

    return errors


def validate_report(case_dir: Path, metadata: dict[str, object], expected_sections: list[str]) -> list[str]:
    errors: list[str] = []
    report_path = case_dir / "REPORT.md"
    text = report_path.read_text()

    report_sections = extract_h2_headings(text)
    if report_sections != expected_sections:
        errors.append(f"{case_dir}: REPORT.md section order must match the shader-port report template")

    for placeholder in PLACEHOLDER_PATTERNS:
        if placeholder in text:
            errors.append(f"{case_dir}: REPORT.md must not contain template placeholder {placeholder}")

    if "TODO" in text:
        errors.append(f"{case_dir}: REPORT.md must not contain TODO placeholders")

    for label in SUMMARY_FIELD_LABELS:
        if extract_summary_field(text, label) is None:
            errors.append(f"{case_dir}: REPORT.md Summary missing field {label}")

    expected_pairs = {
        "Classification": metadata["classification"],
        "Authoring route": metadata["authoring_route"],
        "Status label": metadata["status_label"],
        "Primary renderer contract": metadata["primary_renderer_contract"],
        "Fallback contract": metadata["fallback_contract"],
        "Runnable sample": "yes" if metadata["runnable"] else "no",
        "Verified paths": ", ".join(metadata["verified_paths"]) if metadata["verified_paths"] else "none",
    }
    for label, expected in expected_pairs.items():
        actual = extract_summary_field(text, label)
        if actual != expected:
            errors.append(f"{case_dir}: REPORT.md Summary field {label} must match fixture.json")

    classification_section = extract_section(text, "## Classification")
    if classification_section is None:
        errors.append(f"{case_dir}: REPORT.md missing Classification section")
    else:
        intake_classification = extract_bullet_value(classification_section, "Intake classification")
        if intake_classification != metadata["classification"]:
            errors.append(f"{case_dir}: Classification section must match fixture.json classification")

    route_section = extract_section(text, "## Chosen Authoring Route")
    if route_section is None:
        errors.append(f"{case_dir}: REPORT.md missing Chosen Authoring Route section")
    else:
        preferred_route = extract_bullet_value(route_section, "Preferred route")
        if preferred_route != metadata["authoring_route"]:
            errors.append(f"{case_dir}: Chosen Authoring Route section must match fixture.json authoring_route")

    status_section = extract_section(text, "## Status Label")
    if status_section is None:
        errors.append(f"{case_dir}: REPORT.md missing Status Label section")
    else:
        final_status_label = extract_bullet_value(status_section, "Final status label")
        if final_status_label != metadata["status_label"]:
            errors.append(f"{case_dir}: Status Label section must match fixture.json status_label")

    backend_section = extract_section(text, "## Renderer / Backend Contract")
    if backend_section is None:
        errors.append(f"{case_dir}: REPORT.md missing Renderer / Backend Contract section")
    else:
        actual_backend_promises = parse_renderer_backend_contract(backend_section)
        expected_backend_promises = PRIMARY_CONTRACT_TO_BACKEND_PROMISES[str(metadata["primary_renderer_contract"])]
        for path_label in BACKEND_TABLE_PATHS:
            actual = actual_backend_promises.get(path_label)
            expected = expected_backend_promises[path_label]
            if actual != expected:
                errors.append(
                    f"{case_dir}: Renderer / Backend Contract row {path_label} must be {expected!r}"
                )

    fallback_section = extract_section(text, "## Fallback Plan")
    if fallback_section is None:
        errors.append(f"{case_dir}: REPORT.md missing Fallback Plan section")
    else:
        primary_fallback = extract_bullet_value(fallback_section, "Primary fallback")
        if primary_fallback != metadata["fallback_contract"]:
            errors.append(f"{case_dir}: Fallback Plan must match fixture.json fallback_contract")

    verification_notes = extract_section(text, "## Verification Notes")
    if verification_notes is None:
        errors.append(f"{case_dir}: REPORT.md missing Verification Notes section")
    else:
        expected_verified_paths = ", ".join(metadata["verified_paths"]) if metadata["verified_paths"] else "none"
        verification_paths = extract_bullet_value(verification_notes, "Verified path(s)")
        if verification_paths != expected_verified_paths:
            errors.append(f"{case_dir}: Verification Notes must match fixture.json verified_paths")
        if metadata["authoring_route"] != "blocked" and not verification_notes.strip():
            errors.append(f"{case_dir}: non-blocked fixture must include Verification Notes")

    blocked_reason = str(metadata["blocked_reason"])
    if metadata["authoring_route"] == "blocked" and blocked_reason not in text:
        errors.append(f"{case_dir}: blocked_reason must appear in REPORT.md")

    return errors


def validate_fixture_json(case_dir: Path) -> tuple[dict[str, object] | None, list[str]]:
    errors: list[str] = []
    path = case_dir / "fixture.json"
    try:
        data = load_json(path)
    except (ValueError, json.JSONDecodeError) as exc:
        return None, [str(exc)]

    required_fields = (
        "fixture_id",
        "classification",
        "authoring_route",
        "status_label",
        "primary_renderer_contract",
        "fallback_contract",
        "verified_paths",
        "runnable",
        "blocked_reason",
    )
    for field in required_fields:
        if field not in data:
            errors.append(f"{path}: missing field {field}")

    if errors:
        return None, errors

    fixture_id = data["fixture_id"]
    if not isinstance(fixture_id, str) or fixture_id != case_dir.name:
        errors.append(f"{path}: fixture_id must match the directory name")

    classification = data["classification"]
    if classification not in VALID_CLASSIFICATIONS:
        errors.append(f"{path}: classification must be one of {sorted(VALID_CLASSIFICATIONS)}")

    authoring_route = data["authoring_route"]
    if authoring_route not in VALID_AUTHORING_ROUTES:
        errors.append(f"{path}: authoring_route must be one of {sorted(VALID_AUTHORING_ROUTES)}")

    status_label = data["status_label"]
    if status_label not in VALID_STATUS_LABELS:
        errors.append(f"{path}: status_label must be one of {sorted(VALID_STATUS_LABELS)}")
    elif authoring_route in ROUTE_TO_STATUS and status_label != ROUTE_TO_STATUS[authoring_route]:
        errors.append(f"{path}: status_label must match the default route mapping for {authoring_route}")

    primary_renderer_contract = data["primary_renderer_contract"]
    if primary_renderer_contract not in VALID_PRIMARY_RENDERER_CONTRACTS:
        errors.append(
            f"{path}: primary_renderer_contract must be one of {sorted(VALID_PRIMARY_RENDERER_CONTRACTS)}"
        )

    fallback_contract = data["fallback_contract"]
    if fallback_contract not in VALID_FALLBACK_CONTRACTS:
        errors.append(f"{path}: fallback_contract must be one of {sorted(VALID_FALLBACK_CONTRACTS)}")

    blocked_reason_value = data["blocked_reason"]
    if not isinstance(blocked_reason_value, str):
        errors.append(f"{path}: blocked_reason must be a string")

    verified_paths = data["verified_paths"]
    if not isinstance(verified_paths, list) or not all(isinstance(item, str) and item for item in verified_paths):
        errors.append(f"{path}: verified_paths must be a string list")
    elif any(item not in VALID_VERIFIED_PATHS for item in verified_paths):
        errors.append(f"{path}: verified_paths entries must be drawn from {sorted(VALID_VERIFIED_PATHS)}")
    elif len(set(verified_paths)) != len(verified_paths):
        errors.append(f"{path}: verified_paths must not contain duplicates")

    runnable = data["runnable"]
    if not isinstance(runnable, bool):
        errors.append(f"{path}: runnable must be a boolean")

    if not errors:
        blocked_reason = str(blocked_reason_value).strip()
        if authoring_route == "blocked":
            if not blocked_reason:
                errors.append(f"{path}: blocked fixture must provide blocked_reason")
            if verified_paths:
                errors.append(f"{path}: blocked fixture must not claim verified_paths")
            if primary_renderer_contract != "blocked":
                errors.append(f"{path}: blocked fixture must use primary_renderer_contract='blocked'")
            if fallback_contract != "blocked-pending-assets-or-decision":
                errors.append(
                    f"{path}: blocked fixture must use fallback_contract='blocked-pending-assets-or-decision'"
                )
        else:
            if blocked_reason:
                errors.append(f"{path}: non-blocked fixture must leave blocked_reason empty")
            if not verified_paths:
                errors.append(f"{path}: non-blocked fixture must provide at least one verified path")
            if "none" in verified_paths:
                errors.append(f"{path}: non-blocked fixture must not use 'none' inside verified_paths")

        if authoring_route == "legacy-webgl-raw":
            if primary_renderer_contract != "webgl-renderer-only":
                errors.append(
                    f"{path}: legacy-webgl-raw must use primary_renderer_contract='webgl-renderer-only'"
                )
            if fallback_contract not in {"none", "approximation"}:
                errors.append(
                    f"{path}: legacy-webgl-raw fallback_contract must be 'none' or 'approximation'"
                )

        if authoring_route == "tsl-webgpu-only":
            if primary_renderer_contract != "webgpu-only":
                errors.append(f"{path}: tsl-webgpu-only must use primary_renderer_contract='webgpu-only'")
            if fallback_contract not in {"approximation", "legacy-webgl-raw", "blocked-pending-assets-or-decision"}:
                errors.append(
                    f"{path}: tsl-webgpu-only fallback_contract must stay within the allowed fallback set"
                )

        if authoring_route in {"pure-tsl", "tsl-plus-interop"}:
            if primary_renderer_contract != "webgpu+webgl2-backend":
                errors.append(
                    f"{path}: {authoring_route} fixtures must use primary_renderer_contract='webgpu+webgl2-backend'"
                )

        if "documentation-only" in verified_paths and len(verified_paths) > 1:
            errors.append(f"{path}: documentation-only cannot be mixed with runtime verified_paths")

    return data, errors


def validate_runnable_case(case_dir: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if not metadata["runnable"]:
        return errors

    for filename in REQUIRED_RUNNABLE_FILES:
        if not (case_dir / filename).exists():
            errors.append(f"{case_dir}: runnable fixture missing {filename}")

    main_js_path = case_dir / "main.js"
    if main_js_path.exists():
        try:
            completed = subprocess.run(
                ["node", "--check", str(main_js_path)],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            errors.append(f"{main_js_path}: node is required for syntax validation")
        else:
            if completed.returncode != 0:
                message = completed.stderr.strip() or completed.stdout.strip() or "unknown syntax error"
                errors.append(f"{main_js_path}: node --check failed ({message})")

    return errors


def main() -> int:
    if not REPORT_TEMPLATE_PATH.exists():
        print("[ERROR] shader-port report template not found", file=sys.stderr)
        return 1

    case_dirs = collect_case_dirs(FIXTURES_ROOT)
    if not case_dirs:
        print("[ERROR] no shader-port fixture directories found", file=sys.stderr)
        return 1

    expected_sections = REPORT_LISTS["required_sections"]
    if not expected_sections:
        print("[ERROR] could not extract sections from shader-port report template", file=sys.stderr)
        return 1

    template_text = REPORT_TEMPLATE_PATH.read_text()
    template_sections = extract_h2_headings(template_text)
    if template_sections != expected_sections:
        print("[ERROR] shader-port report template sections do not match assets/fixture-schema.json", file=sys.stderr)
        return 1

    template_summary_labels = extract_summary_labels(template_text)
    if template_summary_labels != list(SUMMARY_FIELD_LABELS):
        print("[ERROR] shader-port report template Summary fields do not match assets/fixture-schema.json", file=sys.stderr)
        return 1

    errors: list[str] = []
    errors.extend(validate_fixture_index(case_dirs))

    seen_routes: set[str] = set()
    runnable_count = 0

    for case_dir in case_dirs:
        for relative_path in REQUIRED_CASE_FILES:
            if not (case_dir / relative_path).exists():
                errors.append(f"{case_dir}: missing {relative_path}")

        metadata, fixture_errors = validate_fixture_json(case_dir)
        errors.extend(fixture_errors)
        if metadata is None:
            continue

        seen_routes.add(str(metadata["authoring_route"]))
        if metadata["runnable"]:
            runnable_count += 1

        errors.extend(validate_report(case_dir, metadata, expected_sections))
        errors.extend(validate_runnable_case(case_dir, metadata))

    missing_routes = sorted(VALID_AUTHORING_ROUTES - seen_routes)
    if missing_routes:
        errors.append(f"{FIXTURES_ROOT}: fixture corpus must cover every authoring route; missing {missing_routes}")

    if runnable_count < 1:
        errors.append(f"{FIXTURES_ROOT}: fixture corpus must include at least one runnable fixture")

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(f"[OK] validated {len(case_dirs)} shader-port fixture(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

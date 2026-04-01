#!/usr/bin/env python3
"""Validate replicator public examples under effects/."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPLICATOR_SCRIPTS_DIR = REPO_ROOT / "skills" / "replicator" / "scripts"
if str(REPLICATOR_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(REPLICATOR_SCRIPTS_DIR))

from workflow_schema import workflow_list, workflow_option_lists

RUNTIME_VERSIONS_PATH = REPO_ROOT / "skills" / "replicator" / "assets" / "runtime-versions.json"
THREE_RUNTIME_VERSION = ""
LIL_GUI_RUNTIME_VERSION = ""
if RUNTIME_VERSIONS_PATH.exists():
    try:
        runtime_versions = json.loads(RUNTIME_VERSIONS_PATH.read_text())
        THREE_RUNTIME_VERSION = str(runtime_versions.get("three", "")).strip()
        LIL_GUI_RUNTIME_VERSION = str(runtime_versions.get("lil_gui", "")).strip()
    except json.JSONDecodeError:
        THREE_RUNTIME_VERSION = ""
        LIL_GUI_RUNTIME_VERSION = ""

WORKFLOW_OPTION_LISTS = workflow_option_lists()
STATUS_LABELS = WORKFLOW_OPTION_LISTS["status_labels"]
MODE_CONTRACTS = WORKFLOW_OPTION_LISTS["mode_contracts"]
REFERENCE_ACCESS_GATES = WORKFLOW_OPTION_LISTS["reference_access_gates"]
REVIEW_ARTIFACT_GATES = WORKFLOW_OPTION_LISTS["review_artifact_gates"]
REVIEW_ARTIFACT_TYPES = WORKFLOW_OPTION_LISTS["review_artifact_types"]
ACCEPTED_SOURCE_TYPES = WORKFLOW_OPTION_LISTS["accepted_source_types"]
SOURCE_ROLES = WORKFLOW_OPTION_LISTS["source_roles"]

API_COMPAT_RULES = {
    "0.180": [
        (r"new\s+THREE\.RenderPipeline\s*\(", "three@0.180.x uses THREE.PostProcessing, not THREE.RenderPipeline"),
        (r"\.setResolutionScale\s*\(", "three@0.180.x uses .setResolution(...), not .setResolutionScale(...)"),
        (r"\.getResolutionScale\s*\(", "three@0.180.x uses .getResolution(), not .getResolutionScale()"),
    ]
}

REQUIRED_REPORT_SECTIONS = tuple(workflow_list("report.required_sections"))

REQUIRED_FILES = (
    "REPORT.md",
    "index.html",
    "main.js",
    "research/summary.md",
    "research/sources.json",
    "review-artifacts/checklist.md",
)

REQUIRED_SOURCE_FIELDS = tuple(workflow_list("sources_json.required_fields"))
REQUIRED_SOURCE_ENTRY_FIELDS = tuple(workflow_list("sources_json.required_entry_fields"))
REQUIRED_MANIFEST_FIELDS = tuple(workflow_list("review_artifact_manifest.required_fields"))
REQUIRED_MANIFEST_ENTRY_FIELDS = tuple(workflow_list("review_artifact_manifest.required_entry_fields"))


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON ({exc})") from exc


def require_string_map(value: object) -> dict[str, object] | None:
    return value if isinstance(value, dict) else None


def validate_sources_json(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        data = load_json(path)
    except ValueError as exc:
        return [str(exc)]

    source_map = require_string_map(data)
    if source_map is None:
        return [f"{path}: expected a top-level object"]

    for field in REQUIRED_SOURCE_FIELDS:
        if field not in source_map:
            errors.append(f"{path}: missing field {field}")

    for field in REQUIRED_SOURCE_FIELDS[:-3]:
        value = source_map.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}: field {field} must be a non-empty string")

    for field in ("accepted_source_types", "source_roles"):
        value = source_map.get(field)
        if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
            errors.append(f"{path}: field {field} must be a non-empty string list")

    mode_contract = source_map.get("mode_contract")
    if mode_contract not in MODE_CONTRACTS:
        errors.append(f"{path}: mode_contract must be one of {MODE_CONTRACTS}")

    status_label = source_map.get("status_label")
    if status_label not in STATUS_LABELS:
        errors.append(f"{path}: status_label must be one of {STATUS_LABELS}")

    reference_access_gate = source_map.get("reference_access_gate")
    if reference_access_gate not in REFERENCE_ACCESS_GATES:
        errors.append(f"{path}: reference_access_gate must be one of {REFERENCE_ACCESS_GATES}")

    review_artifact_gate = source_map.get("review_artifact_gate")
    if review_artifact_gate not in REVIEW_ARTIFACT_GATES:
        errors.append(f"{path}: review_artifact_gate must be one of {REVIEW_ARTIFACT_GATES}")

    review_artifact_type = source_map.get("review_artifact_type")
    if review_artifact_type not in REVIEW_ARTIFACT_TYPES:
        errors.append(f"{path}: review_artifact_type must be one of {REVIEW_ARTIFACT_TYPES}")

    accepted_source_types = source_map.get("accepted_source_types")
    if accepted_source_types != ACCEPTED_SOURCE_TYPES:
        errors.append(f"{path}: accepted_source_types must match the workflow schema")

    source_roles = source_map.get("source_roles")
    if source_roles != SOURCE_ROLES:
        errors.append(f"{path}: source_roles must match the workflow schema")

    sources = source_map.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{path}: field sources must be a non-empty list")
        return errors

    for index, entry in enumerate(sources):
        entry_map = require_string_map(entry)
        if entry_map is None:
            errors.append(f"{path}: sources[{index}] must be an object")
            continue

        for field in REQUIRED_SOURCE_ENTRY_FIELDS:
            value = entry_map.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{path}: sources[{index}].{field} must be a non-empty string")

        entry_type = entry_map.get("type")
        if isinstance(entry_type, str) and entry_type not in ACCEPTED_SOURCE_TYPES:
            errors.append(f"{path}: sources[{index}].type must be one of {ACCEPTED_SOURCE_TYPES}")

        role = entry_map.get("role")
        if isinstance(role, str) and role not in SOURCE_ROLES:
            errors.append(f"{path}: sources[{index}].role must be one of {SOURCE_ROLES}")

    return errors


def validate_capture_manifest(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        data = load_json(path)
    except ValueError as exc:
        return [str(exc)]

    manifest = require_string_map(data)
    if manifest is None:
        return [f"{path}: expected a top-level object"]

    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in manifest:
            errors.append(f"{path}: missing field {field}")

    if manifest.get("artifacts_subdir") != "review-artifacts":
        errors.append(f"{path}: artifacts_subdir must be set to review-artifacts")

    for field in ("effect_slug",):
        value = manifest.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}: field {field} must be a non-empty string")

    for field in (
        "expected_ids",
        "missing_reference",
        "missing_current",
        "kind_mismatches",
        "image_dimension_mismatches",
        "unparsed_formats",
        "entries",
    ):
        value = manifest.get(field)
        if not isinstance(value, list):
            errors.append(f"{path}: field {field} must be a list")

    complete_pairs = manifest.get("complete_pairs")
    if not isinstance(complete_pairs, int) or complete_pairs < 0:
        errors.append(f"{path}: field complete_pairs must be a non-negative integer")

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return errors

    for index, entry in enumerate(entries):
        entry_map = require_string_map(entry)
        if entry_map is None:
            errors.append(f"{path}: entries[{index}] must be an object")
            continue

        for field in REQUIRED_MANIFEST_ENTRY_FIELDS:
            if field not in entry_map:
                errors.append(f"{path}: entries[{index}] missing field {field}")

        if not isinstance(entry_map.get("artifact_id"), str) or not entry_map["artifact_id"]:
            errors.append(f"{path}: entries[{index}].artifact_id must be a non-empty string")

        for field in ("reference_exists", "current_exists", "kind_match"):
            value = entry_map.get(field)
            if not isinstance(value, bool):
                errors.append(f"{path}: entries[{index}].{field} must be a boolean")

        dimension_match = entry_map.get("image_dimension_match")
        if dimension_match is not None and not isinstance(dimension_match, bool):
            errors.append(f"{path}: entries[{index}].image_dimension_match must be a boolean or null")

        for field in ("reference_path", "current_path", "reference_kind", "current_kind"):
            value = entry_map.get(field)
            if value is not None and not isinstance(value, str):
                errors.append(f"{path}: entries[{index}].{field} must be a string or null")

    return errors


def validate_main_js_syntax(path: Path) -> list[str]:
    try:
        completed = subprocess.run(
            ["node", "--check", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return [f"{path}: node is required for syntax validation"]

    if completed.returncode == 0:
        return []

    message = completed.stderr.strip() or completed.stdout.strip() or "unknown syntax error"
    return [f"{path}: node --check failed ({message})"]


def extract_import_map(index_text: str) -> dict[str, str] | None:
    match = re.search(r'<script\s+type="importmap">\s*(\{.*?\})\s*</script>', index_text, re.S)
    if not match:
        return None

    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None

    imports = payload.get("imports")
    return imports if isinstance(imports, dict) else None


def validate_effect_code_contract(artifact_dir: Path) -> list[str]:
    errors: list[str] = []
    index_path = artifact_dir / "index.html"
    main_js_path = artifact_dir / "main.js"

    if not index_path.exists() or not main_js_path.exists():
        return errors

    index_text = index_path.read_text()
    main_js_text = main_js_path.read_text()
    combined = f"{index_text}\n{main_js_text}"

    if 'id="app"' not in index_text:
        errors.append(f"{artifact_dir}: index.html must include canvas#app")

    import_map = extract_import_map(index_text)
    if 'type="importmap"' in index_text and import_map is None:
        errors.append(f"{artifact_dir}: index.html contains an invalid import map")

    if import_map is not None and "three" not in import_map:
        errors.append(f"{artifact_dir}: index.html import map must include a base three entry")

    if import_map is not None and THREE_RUNTIME_VERSION:
        for key in ("three", "three/webgpu", "three/tsl", "three/addons/"):
            value = import_map.get(key)
            if value is not None and f"three@{THREE_RUNTIME_VERSION}" not in value:
                errors.append(f"{artifact_dir}: import map entry {key} must target three@{THREE_RUNTIME_VERSION}")

    if import_map is not None and LIL_GUI_RUNTIME_VERSION:
        value = import_map.get("lil-gui")
        if value is not None and f"lil-gui@{LIL_GUI_RUNTIME_VERSION}" not in value:
            errors.append(f"{artifact_dir}: import map entry lil-gui must target lil-gui@{LIL_GUI_RUNTIME_VERSION}")

    if "./main.js" not in index_text and 'type="module"' not in index_text:
        errors.append(f"{artifact_dir}: index.html must load main.js or include a module entrypoint")

    if import_map is not None and "./main.js" in index_text and "main.js" not in {path.name for path in artifact_dir.iterdir() if path.is_file()}:
        errors.append(f"{artifact_dir}: index.html expects ./main.js but the file is missing")

    if "from 'three/webgpu'" in main_js_text or 'from "three/webgpu"' in main_js_text:
        if import_map is None or "three/webgpu" not in import_map:
            errors.append(f"{artifact_dir}: main.js imports three/webgpu but index.html does not map it")

    if "from 'three/tsl'" in main_js_text or 'from "three/tsl"' in main_js_text:
        if import_map is None or "three/tsl" not in import_map:
            errors.append(f"{artifact_dir}: main.js imports three/tsl but index.html does not map it")

    if "from 'three/addons/" in main_js_text or 'from "three/addons/' in main_js_text:
        if import_map is None or "three/addons/" not in import_map:
            errors.append(f"{artifact_dir}: main.js imports three/addons/* but index.html does not map it")

    relative_imports = re.findall(r"""from\s+['"](\.[^'"]+)['"]""", main_js_text)
    dynamic_relative_imports = re.findall(r"""import\(\s*['"](\.[^'"]+)['"]\s*\)""", main_js_text)
    for target in set(relative_imports + dynamic_relative_imports):
        resolved = (main_js_path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{artifact_dir}: main.js imports missing relative module {target}")

    if "new THREE.WebGPURenderer(" in combined and ".init(" not in combined:
        errors.append(f"{artifact_dir}: WebGPURenderer usage must call renderer.init()")

    if "forceWebGL" in combined and "new THREE.WebGPURenderer(" not in combined:
        errors.append(f"{artifact_dir}: forceWebGL must be attached to WebGPURenderer")

    if "new THREE.WebGLRenderer(" in combined and "from 'three/webgpu'" in main_js_text:
        errors.append(f"{artifact_dir}: WebGLRenderer path should import from three, not three/webgpu")

    if "new THREE.PostProcessing(" in combined and "three/webgpu" not in main_js_text:
        errors.append(f"{artifact_dir}: THREE.PostProcessing requires the WebGPU entrypoint import")

    if "pass(" in main_js_text and "three/tsl" not in main_js_text:
        errors.append(f"{artifact_dir}: pass(...) usage must import from three/tsl")

    if "requestAnimationFrame(" not in main_js_text and "setAnimationLoop(" not in main_js_text:
        errors.append(f"{artifact_dir}: main.js must define an explicit render loop")

    if THREE_RUNTIME_VERSION:
        rules = API_COMPAT_RULES.get(".".join(THREE_RUNTIME_VERSION.split(".")[:2]), [])
        for pattern, message in rules:
            if re.search(pattern, combined):
                errors.append(f"{artifact_dir}: {message}")

    return errors


def validate_artifact(artifact_dir: Path) -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_FILES:
        full_path = artifact_dir / relative_path
        if not full_path.exists():
            errors.append(f"{artifact_dir}: missing {relative_path}")

    report_path = artifact_dir / "REPORT.md"
    if report_path.exists():
        report_text = report_path.read_text()
        for section in REQUIRED_REPORT_SECTIONS:
            if section not in report_text:
                errors.append(f"{artifact_dir}: REPORT.md missing section {section}")

    sources_path = artifact_dir / "research" / "sources.json"
    if sources_path.exists():
        errors.extend(validate_sources_json(sources_path))

    manifest_path = artifact_dir / "review-artifacts" / "manifest.json"
    if manifest_path.exists():
        errors.extend(validate_capture_manifest(manifest_path))

    main_js_path = artifact_dir / "main.js"
    if main_js_path.exists():
        errors.extend(validate_main_js_syntax(main_js_path))

    errors.extend(validate_effect_code_contract(artifact_dir))

    return errors


def collect_artifact_dirs(root: Path) -> dict[str, Path]:
    if not root.exists():
        return {}
    return {
        path.name: path
        for path in sorted(root.iterdir())
        if path.is_dir()
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    effects_root = repo_root / "effects"

    effect_dirs = collect_artifact_dirs(effects_root)

    if not effect_dirs:
        print("[ERROR] no public effect directories found under effects/", file=sys.stderr)
        return 1

    errors: list[str] = []
    for artifact_dir in effect_dirs.values():
        errors.extend(validate_artifact(artifact_dir))

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(f"[OK] validated {len(effect_dirs)} public effect(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

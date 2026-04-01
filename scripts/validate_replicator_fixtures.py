#!/usr/bin/env python3
"""Validate replicator artifacts under test/ and effects/."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
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

API_COMPAT_RULES = {
    "0.180": [
        (r"new\s+THREE\.RenderPipeline\s*\(", "three@0.180.x uses THREE.PostProcessing, not THREE.RenderPipeline"),
        (r"\.setResolutionScale\s*\(", "three@0.180.x uses .setResolution(...), not .setResolutionScale(...)"),
        (r"\.getResolutionScale\s*\(", "three@0.180.x uses .getResolution(), not .getResolutionScale()"),
    ]
}

REQUIRED_REPORT_SECTIONS = (
    "## Reference Access Gate",
    "## Mode Contract",
    "## Archetype Route",
    "## Visual Evidence Table",
    "## Classic Graphics Baseline",
    "## Search Log",
    "## Evidence vs Inference",
    "## Shortest Convincing Path",
    "## First-Frame Review Gate",
    "## PostFX Decision",
    "## Performance Decision",
    "## Browser Validation Gate",
    "## Review Artifact Gate",
    "## Visual Acceptance",
    "## Fidelity Failure Protocol",
    "## Completion Rule",
)

REQUIRED_FILES = (
    "REPORT.md",
    "index.html",
    "main.js",
    "research/summary.md",
    "research/sources.json",
    "review-artifacts/checklist.md",
)

REQUIRED_SOURCE_FIELDS = (
    "effect_slug",
    "effect_title",
    "effect_archetype",
    "canonical_profile",
    "authoring_path",
    "runtime_renderer",
    "resource_model",
    "pass_topology",
    "compatibility_contract",
    "target_device_class",
    "performance_contract",
    "dominant_bottleneck",
    "post_pipeline_type",
    "render_target_layout",
    "history_requirement",
    "nearest_rejected_route",
    "target_environment",
    "performance_priority",
    "mode_contract",
    "status_label",
    "reference_access_gate",
    "primary_visual_artifact",
    "classic_graphics_baseline",
    "first_frame_gate",
    "browser_validation_gate",
    "review_artifact_gate",
    "review_artifact_type",
    "accepted_source_types",
    "source_roles",
    "sources",
)

REQUIRED_SOURCE_ENTRY_FIELDS = ("type", "value", "label", "role", "contribution")
REQUIRED_MANIFEST_FIELDS = (
    "effect_slug",
    "artifacts_subdir",
    "expected_ids",
    "complete_pairs",
    "missing_reference",
    "missing_current",
    "kind_mismatches",
    "image_dimension_mismatches",
    "unparsed_formats",
    "entries",
)
REQUIRED_MANIFEST_ENTRY_FIELDS = (
    "artifact_id",
    "reference_path",
    "current_path",
    "reference_exists",
    "current_exists",
    "reference_kind",
    "current_kind",
    "kind_match",
    "reference_size",
    "current_size",
    "image_dimension_match",
)
PAIRED_TEXT_FILES = (
    "REPORT.md",
    "index.html",
    "main.js",
    "research/summary.md",
    "review-artifacts/checklist.md",
)
PAIRED_JSON_FILES = (
    "research/sources.json",
)


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


def compare_artifact_pairs(effect_dirs: dict[str, Path], fixture_dirs: dict[str, Path]) -> list[str]:
    errors: list[str] = []

    missing_effects = sorted(set(fixture_dirs) - set(effect_dirs))
    missing_fixtures = sorted(set(effect_dirs) - set(fixture_dirs))

    for slug in missing_effects:
        errors.append(f"effects/: missing public example for fixture {slug}")
    for slug in missing_fixtures:
        errors.append(f"test/: missing fixture for public example {slug}")

    for slug in sorted(set(effect_dirs) & set(fixture_dirs)):
        effect_dir = effect_dirs[slug]
        fixture_dir = fixture_dirs[slug]

        for relative_path in PAIRED_TEXT_FILES:
            effect_path = effect_dir / relative_path
            fixture_path = fixture_dir / relative_path
            if not effect_path.exists() or not fixture_path.exists():
                continue
            effect_text = effect_path.read_text()
            fixture_text = fixture_path.read_text()
            if effect_text != fixture_text:
                errors.append(f"{slug}: {relative_path} differs between effects/ and test/")

        for relative_path in PAIRED_JSON_FILES:
            effect_path = effect_dir / relative_path
            fixture_path = fixture_dir / relative_path
            if not effect_path.exists() or not fixture_path.exists():
                continue
            effect_json = load_json(effect_path)
            fixture_json = load_json(fixture_path)
            if effect_json != fixture_json:
                errors.append(f"{slug}: {relative_path} differs between effects/ and test/")

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    test_root = repo_root / "test"
    effects_root = repo_root / "effects"

    fixture_dirs = collect_artifact_dirs(test_root)
    effect_dirs = collect_artifact_dirs(effects_root)

    if not fixture_dirs:
        print("[ERROR] no fixture directories found under test/", file=sys.stderr)
        return 1
    if not effect_dirs:
        print("[ERROR] no public effect directories found under effects/", file=sys.stderr)
        return 1

    errors: list[str] = []
    for artifact_dir in fixture_dirs.values():
        errors.extend(validate_artifact(artifact_dir))
    for artifact_dir in effect_dirs.values():
        errors.extend(validate_artifact(artifact_dir))
    errors.extend(compare_artifact_pairs(effect_dirs, fixture_dirs))

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(
        "[OK] validated "
        f"{len(fixture_dirs)} fixture(s), {len(effect_dirs)} public effect(s), "
        "and effect/fixture parity"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

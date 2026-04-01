#!/usr/bin/env python3
"""Validate replicator artifacts under test/ and effects/."""

from __future__ import annotations

import json
import sys
from pathlib import Path

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
    "captures/checklist.md",
    "captures/manifest.json",
    "captures/review.md",
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
    "side_by_side_review",
    "accepted_source_types",
    "source_roles",
    "sources",
)

REQUIRED_SOURCE_ENTRY_FIELDS = ("type", "value", "label", "role", "contribution")
REQUIRED_MANIFEST_FIELDS = (
    "effect_slug",
    "captures_subdir",
    "expected_slots",
    "complete_pairs",
    "missing_reference",
    "missing_current",
    "size_mismatches",
    "unsupported_formats",
    "entries",
)
REQUIRED_MANIFEST_ENTRY_FIELDS = (
    "slot",
    "reference_path",
    "current_path",
    "reference_exists",
    "current_exists",
    "reference_size",
    "current_size",
    "size_match",
)
PAIRED_TEXT_FILES = (
    "REPORT.md",
    "index.html",
    "main.js",
    "research/summary.md",
    "captures/checklist.md",
    "captures/review.md",
)
PAIRED_JSON_FILES = (
    "research/sources.json",
    "captures/manifest.json",
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

    if manifest.get("captures_subdir") != "captures":
        errors.append(f"{path}: captures_subdir must be set to captures")

    for field in ("effect_slug",):
        value = manifest.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}: field {field} must be a non-empty string")

    for field in ("expected_slots", "missing_reference", "missing_current", "size_mismatches", "unsupported_formats", "entries"):
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

        if not isinstance(entry_map.get("slot"), str) or not entry_map["slot"]:
            errors.append(f"{path}: entries[{index}].slot must be a non-empty string")

        for field in ("reference_exists", "current_exists", "size_match"):
            value = entry_map.get(field)
            if not isinstance(value, bool):
                errors.append(f"{path}: entries[{index}].{field} must be a boolean")

        for field in ("reference_path", "current_path"):
            value = entry_map.get(field)
            if value is not None and not isinstance(value, str):
                errors.append(f"{path}: entries[{index}].{field} must be a string or null")

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

    manifest_path = artifact_dir / "captures" / "manifest.json"
    if manifest_path.exists():
        errors.extend(validate_capture_manifest(manifest_path))

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

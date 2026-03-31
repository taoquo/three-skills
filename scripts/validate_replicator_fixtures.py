#!/usr/bin/env python3
"""Validate that replicator fixtures under test/ follow the v3 artifact shape."""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_REPORT_SECTIONS = (
    "## Archetype Route",
    "## Search Log",
    "## Evidence vs Inference",
    "## Shortest Convincing Path",
    "## PostFX Decision",
    "## Performance Decision",
    "## Visual Acceptance",
)

REQUIRED_FILES = (
    "REPORT.md",
    "research/summary.md",
    "research/sources.json",
    "captures/checklist.md",
    "captures/manifest.json",
    "captures/review.md",
)


def validate_fixture(fixture_dir: Path) -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_FILES:
        full_path = fixture_dir / relative_path
        if not full_path.exists():
            errors.append(f"{fixture_dir.name}: missing {relative_path}")

    report_path = fixture_dir / "REPORT.md"
    if report_path.exists():
        report_text = report_path.read_text()
        for section in REQUIRED_REPORT_SECTIONS:
            if section not in report_text:
                errors.append(f"{fixture_dir.name}: REPORT.md missing section {section}")

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    test_root = repo_root / "test"

    if not test_root.exists():
        print("[ERROR] test/ directory not found", file=sys.stderr)
        return 1

    fixture_dirs = sorted(path for path in test_root.iterdir() if path.is_dir())
    if not fixture_dirs:
        print("[ERROR] no fixture directories found under test/", file=sys.stderr)
        return 1

    errors: list[str] = []
    for fixture_dir in fixture_dirs:
        errors.extend(validate_fixture(fixture_dir))

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(f"[OK] validated {len(fixture_dirs)} replicator fixture(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

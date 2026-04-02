#!/usr/bin/env python3
"""Validate perf-doctor report-centric fixtures."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_ROOT = REPO_ROOT / "skills" / "perf-doctor" / "fixtures"
REPORT_TEMPLATE_PATH = REPO_ROOT / "skills" / "perf-doctor" / "assets" / "report-template.md"
FIXTURE_INDEX_PATH = FIXTURES_ROOT / "README.md"
REQUIRED_CASE_FILES = ("README.md", "report.md")
REQUIRED_CASE_HEADINGS = (
    "## Background",
    "## Known Symptoms",
    "## Expected Dominant Bottleneck",
    "## Recommended First Capture",
    "## Case Status",
    "## Report",
)
REQUIRED_FINAL_CALL_BULLETS = (
    "- Dominant bottleneck:",
    "- Secondary bottleneck:",
    "- First fix to ship:",
    "- First fallback tier to wire:",
    "- What not to change yet:",
)
VALID_STATUSES = {"diagnosed", "partially-diagnosed", "blocked"}
MIN_CASE_COUNT = 3


def extract_h2_headings(text: str) -> list[str]:
    return re.findall(r"^## .+$", text, re.M)


def extract_status(report_text: str) -> str | None:
    match = re.search(r"^- Status:\s*`([^`]+)`\s*$", report_text, re.M)
    return match.group(1).strip() if match else None


def extract_section(text: str, heading: str) -> str | None:
    pattern = rf"^{re.escape(heading)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1) if match else None


def count_table_data_rows(section_text: str) -> int:
    rows = 0
    for raw_line in section_text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if re.fullmatch(r"\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|?", line):
            continue
        if "Unknown" in line and "Why it matters" in line and "Next measurement or test" in line:
            continue
        rows += 1
    return rows


def validate_case_readme(case_dir: Path) -> list[str]:
    errors: list[str] = []
    readme_path = case_dir / "README.md"
    if not readme_path.exists():
        return errors

    text = readme_path.read_text()
    for heading in REQUIRED_CASE_HEADINGS:
        if heading not in text:
            errors.append(f"{case_dir}: README.md missing section {heading}")

    return errors


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


def validate_report(case_dir: Path, expected_sections: list[str]) -> list[str]:
    errors: list[str] = []
    report_path = case_dir / "report.md"
    if not report_path.exists():
        return errors

    text = report_path.read_text()
    report_sections = extract_h2_headings(text)

    if report_sections != expected_sections:
        errors.append(f"{case_dir}: report.md section order must match the perf-doctor report template")

    if "__PROJECT_OR_SCENE_NAME__" in text or "`TODO`" in text:
        errors.append(f"{case_dir}: report.md must not contain unfilled template placeholders")

    status = extract_status(text)
    if status is None:
        errors.append(f"{case_dir}: report.md missing Summary status")
    elif status not in VALID_STATUSES:
        errors.append(f"{case_dir}: report.md uses invalid status {status!r}")

    final_call = extract_section(text, "## Final Call")
    if final_call is None:
        errors.append(f"{case_dir}: report.md missing Final Call section")
    else:
        for bullet in REQUIRED_FINAL_CALL_BULLETS:
            if bullet not in final_call:
                errors.append(f"{case_dir}: report.md Final Call missing bullet {bullet}")

    if status == "partially-diagnosed":
        unknowns_section = extract_section(text, "## Unknowns and Next Capture")
        if unknowns_section is None:
            errors.append(f"{case_dir}: partially-diagnosed report must include Unknowns and Next Capture")
        elif count_table_data_rows(unknowns_section) < 1:
            errors.append(f"{case_dir}: partially-diagnosed report must include at least one unknown row")

    return errors


def collect_case_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return [path for path in sorted(root.iterdir()) if path.is_dir()]


def main() -> int:
    if not REPORT_TEMPLATE_PATH.exists():
        print("[ERROR] perf-doctor report template not found", file=sys.stderr)
        return 1

    case_dirs = collect_case_dirs(FIXTURES_ROOT)
    if not case_dirs:
        print("[ERROR] no perf-doctor fixture directories found", file=sys.stderr)
        return 1
    if len(case_dirs) < MIN_CASE_COUNT:
        print(
            f"[ERROR] perf-doctor fixture corpus must contain at least {MIN_CASE_COUNT} cases",
            file=sys.stderr,
        )
        return 1

    expected_sections = extract_h2_headings(REPORT_TEMPLATE_PATH.read_text())
    if not expected_sections:
        print("[ERROR] could not extract sections from perf-doctor report template", file=sys.stderr)
        return 1

    errors: list[str] = []
    errors.extend(validate_fixture_index(case_dirs))
    statuses: list[str] = []
    for case_dir in case_dirs:
        for relative_path in REQUIRED_CASE_FILES:
            if not (case_dir / relative_path).exists():
                errors.append(f"{case_dir}: missing {relative_path}")

        errors.extend(validate_case_readme(case_dir))
        errors.extend(validate_report(case_dir, expected_sections))
        report_path = case_dir / "report.md"
        if report_path.exists():
            status = extract_status(report_path.read_text())
            if status is not None:
                statuses.append(status)

    if "partially-diagnosed" not in statuses:
        errors.append(f"{FIXTURES_ROOT}: fixture corpus must include at least one partially-diagnosed case")

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(f"[OK] validated {len(case_dirs)} perf-doctor fixture(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

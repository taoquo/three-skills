#!/usr/bin/env python3
"""Validate material-lab route fixtures."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_ROOT = REPO_ROOT / "skills" / "material-lab" / "fixtures"
REPORT_TEMPLATE_PATH = REPO_ROOT / "skills" / "material-lab" / "assets" / "report-template.md"
FIXTURE_INDEX_PATH = FIXTURES_ROOT / "README.md"
REQUIRED_CASE_FILES = ("README.md", "REPORT.md", "index.html", "main.js")
REQUIRED_README_HEADINGS = (
    "## Why This Fixture Exists",
    "## Route Decision",
    "## Preview",
    "## What To Look For",
    "## Limits",
)
PLACEHOLDER_PATTERNS = (
    "__FIXTURE_OR_TASK_NAME__",
    "`TODO`",
    "TODO",
)


def collect_case_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return [path for path in sorted(root.iterdir()) if path.is_dir()]


def extract_h2_headings(text: str) -> list[str]:
    return re.findall(r"^## .+$", text, re.M)


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


def validate_case_readme(case_dir: Path) -> list[str]:
    errors: list[str] = []
    readme_path = case_dir / "README.md"
    if not readme_path.exists():
        return errors

    text = readme_path.read_text()
    for heading in REQUIRED_README_HEADINGS:
        if heading not in text:
            errors.append(f"{case_dir}: README.md missing section {heading}")

    if "http://localhost:" not in text:
        errors.append(f"{case_dir}: README.md must include an explicit localhost preview URL")

    if "Do not use `file://`" not in text:
        errors.append(f"{case_dir}: README.md must warn against file:// preview")

    return errors


def validate_report(case_dir: Path, expected_sections: list[str]) -> list[str]:
    errors: list[str] = []
    report_path = case_dir / "REPORT.md"
    if not report_path.exists():
        return errors

    text = report_path.read_text()
    report_sections = extract_h2_headings(text)
    if report_sections != expected_sections:
        errors.append(f"{case_dir}: REPORT.md section order must match the material-lab report template")

    for pattern in PLACEHOLDER_PATTERNS:
        if pattern in text:
            errors.append(f"{case_dir}: REPORT.md must not contain placeholder {pattern}")

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


def uses_specifier(main_js_text: str, specifier: str) -> bool:
    return f'"{specifier}"' in main_js_text or f"'{specifier}'" in main_js_text


def validate_runnable_contract(case_dir: Path) -> list[str]:
    errors: list[str] = []
    index_path = case_dir / "index.html"
    main_js_path = case_dir / "main.js"

    if not index_path.exists() or not main_js_path.exists():
        return errors

    index_text = index_path.read_text()
    main_js_text = main_js_path.read_text()

    if 'id="app"' not in index_text:
        errors.append(f"{case_dir}: index.html must include canvas#app")

    if "./main.js" not in index_text:
        errors.append(f"{case_dir}: index.html must load ./main.js")

    if "file:" not in index_text or "http://localhost/" not in index_text:
        errors.append(f"{case_dir}: index.html must gate file:// preview and point users to http://localhost/")

    import_map = extract_import_map(index_text)
    if 'type="importmap"' in index_text and import_map is None:
        errors.append(f"{case_dir}: index.html contains an invalid import map")

    if import_map is not None and "three" not in import_map:
        errors.append(f"{case_dir}: index.html import map must include a base three entry")

    required_mappings = {
        "three/addons/": any(
            token in main_js_text for token in ('from "three/addons/', "from 'three/addons/")
        ),
        "three/webgpu": uses_specifier(main_js_text, "three/webgpu"),
        "three/tsl": uses_specifier(main_js_text, "three/tsl"),
        "lil-gui": uses_specifier(main_js_text, "lil-gui"),
    }
    for key, required in required_mappings.items():
        if required and (import_map is None or key not in import_map):
            errors.append(f"{case_dir}: index.html import map must include {key}")

    relative_imports = re.findall(r"""from\s+['"](\.[^'"]+)['"]""", main_js_text)
    dynamic_relative_imports = re.findall(r"""import\(\s*['"](\.[^'"]+)['"]\s*\)""", main_js_text)
    for target in set(relative_imports + dynamic_relative_imports):
        resolved = (main_js_path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{case_dir}: main.js imports missing relative module {target}")

    if "requestAnimationFrame(" not in main_js_text and "setAnimationLoop(" not in main_js_text:
        errors.append(f"{case_dir}: main.js must define an explicit render loop")

    return errors


def main() -> int:
    if not REPORT_TEMPLATE_PATH.exists():
        print("[ERROR] material-lab report template not found", file=sys.stderr)
        return 1

    case_dirs = collect_case_dirs(FIXTURES_ROOT)
    if not case_dirs:
        print("[ERROR] no material-lab fixture directories found", file=sys.stderr)
        return 1

    expected_sections = extract_h2_headings(REPORT_TEMPLATE_PATH.read_text())
    if not expected_sections:
        print("[ERROR] could not extract sections from material-lab report template", file=sys.stderr)
        return 1

    errors: list[str] = []
    errors.extend(validate_fixture_index(case_dirs))
    for case_dir in case_dirs:
        for relative_path in REQUIRED_CASE_FILES:
            if not (case_dir / relative_path).exists():
                errors.append(f"{case_dir}: missing {relative_path}")

        errors.extend(validate_case_readme(case_dir))
        errors.extend(validate_report(case_dir, expected_sections))

        main_js_path = case_dir / "main.js"
        if main_js_path.exists():
            errors.extend(validate_main_js_syntax(main_js_path))

        errors.extend(validate_runnable_contract(case_dir))

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(f"[OK] validated {len(case_dirs)} material-lab fixture(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

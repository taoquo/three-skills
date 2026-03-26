#!/usr/bin/env python3
"""
Minimal validator for skills/*/SKILL.md files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_NAME_LENGTH = 64


def extract_frontmatter(text: str) -> str | None:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    return match.group(1)


def parse_scalar(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", frontmatter, re.M)
    if not match:
        return None
    return match.group(1).strip()


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    text = skill_md.read_text()
    frontmatter = extract_frontmatter(text)
    if frontmatter is None:
        return [f"{skill_dir.name}: missing or invalid YAML frontmatter block"]

    name = parse_scalar(frontmatter, "name")
    description = parse_scalar(frontmatter, "description")

    if not name:
        errors.append(f"{skill_dir.name}: missing frontmatter name")
    elif not re.fullmatch(r"[a-z0-9-]+", name):
        errors.append(f"{skill_dir.name}: name must be kebab-case")
    elif len(name) > MAX_NAME_LENGTH:
        errors.append(f"{skill_dir.name}: name exceeds {MAX_NAME_LENGTH} characters")
    elif name != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name must match folder name")

    if not description:
        errors.append(f"{skill_dir.name}: missing frontmatter description")
    elif "<" in description or ">" in description:
        errors.append(f"{skill_dir.name}: description contains angle brackets")

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    skills_root = repo_root / "skills"

    if not skills_root.exists():
        print("[ERROR] skills/ directory not found", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if not skill_dirs:
        print("[ERROR] no skill directories found under skills/", file=sys.stderr)
        return 1

    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(f"[OK] validated {len(skill_dirs)} skill(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

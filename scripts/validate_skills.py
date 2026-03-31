#!/usr/bin/env python3
"""Validator for the local skills repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_NAME_LENGTH = 64
REQUIRED_TOP_LEVEL_FIELDS = ("name", "description", "license")
REQUIRED_METADATA_FIELDS = ("version", "category", "render_backends", "shader_language")


def parse_bool(value: object, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1"}:
            return True
        if normalized in {"false", "no", "0"}:
            return False
    return default


def parse_frontmatter(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    current_key: str | None = None
    current_list_key: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue

        if re.match(r"^\s+-\s+", raw_line) and current_key == "metadata" and current_list_key:
            data.setdefault(f"metadata.{current_list_key}", [])
            casted = data[f"metadata.{current_list_key}"]
            if isinstance(casted, list):
                casted.append(re.sub(r"^\s+-\s+", "", raw_line).strip().strip('"'))
            continue

        top_match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw_line)
        if top_match and not raw_line.startswith("  "):
            key, value = top_match.groups()
            current_key = key
            current_list_key = None
            if value:
                data[key] = value.strip().strip('"')
            else:
                data[key] = {}
            continue

        meta_match = re.match(r"^  ([A-Za-z0-9_-]+):\s*(.*)$", raw_line)
        if meta_match and current_key == "metadata":
            key, value = meta_match.groups()
            if value:
                data[f"metadata.{key}"] = value.strip().strip('"')
                current_list_key = None
            else:
                data[f"metadata.{key}"] = []
                current_list_key = key
            continue

    return data


def extract_frontmatter(text: str) -> str | None:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    return match.group(1)


def find_markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def validate_markdown_links(markdown_path: Path) -> list[str]:
    errors: list[str] = []
    text = markdown_path.read_text()
    for target in find_markdown_links(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean_target = target.split("#", 1)[0]
        if not clean_target:
            continue
        resolved = (markdown_path.parent / clean_target).resolve()
        if not resolved.exists():
            errors.append(f"{markdown_path.relative_to(markdown_path.parents[2])}: missing linked path {target}")
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    text = skill_md.read_text()
    frontmatter = extract_frontmatter(text)
    if frontmatter is None:
        return [f"{skill_dir.name}: missing or invalid YAML frontmatter block"]

    data = parse_frontmatter(frontmatter)
    name = data.get("name") if isinstance(data.get("name"), str) else None
    description = data.get("description") if isinstance(data.get("description"), str) else None

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if not data.get(field):
            errors.append(f"{skill_dir.name}: missing frontmatter {field}")

    for field in REQUIRED_METADATA_FIELDS:
        if not data.get(f"metadata.{field}"):
            errors.append(f"{skill_dir.name}: missing metadata.{field}")

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

    if not (skill_dir / "references").exists():
        errors.append(f"{skill_dir.name}: missing references/ directory")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        errors.append(f"{skill_dir.name}: missing agents/openai.yaml")

    owns_templates = parse_bool(data.get("metadata.owns_templates"))
    if owns_templates:
        template_root = skill_dir / "assets" / "templates"
        if not template_root.exists():
            errors.append(f"{skill_dir.name}: missing assets/templates/ directory")
        elif skill_dir.name == "replicator":
            expected_templates = ("tsl-webgpu", "tsl-webgl2", "legacy-glsl")
            for template_name in expected_templates:
                template_dir = template_root / template_name
                if not template_dir.exists():
                    errors.append(f"{skill_dir.name}: missing template {template_name}")

    owns_scaffolder = parse_bool(data.get("metadata.owns_scaffolder"))
    if owns_scaffolder and not (skill_dir / "scripts").exists():
        errors.append(f"{skill_dir.name}: missing scripts/ directory")

    errors.extend(validate_markdown_links(skill_md))
    for doc in skill_dir.rglob("*.md"):
        if doc != skill_md:
            errors.extend(validate_markdown_links(doc))

    return errors


def validate_readme(repo_root: Path, skill_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    readme = repo_root / "README.md"
    if not readme.exists():
        return ["README.md: missing file"]

    text = readme.read_text()
    lines = text.splitlines()
    available_skill_names: list[str] = []
    in_available_skills = False

    for line in lines:
        if line.startswith("## "):
            if in_available_skills:
                break
            in_available_skills = line == "## Available Skills"
            continue

        if not in_available_skills:
            continue

        match = re.match(r"^\|\s*`([a-z0-9-]+)`\s*\|", line.strip())
        if match:
            available_skill_names.append(match.group(1))

    if not available_skill_names:
        errors.append("README.md: missing or invalid Available Skills table")
        return errors

    expected_names = sorted(skill_dir.name for skill_dir in skill_dirs)
    listed_names = sorted(set(available_skill_names))

    for skill_name in expected_names:
        if skill_name not in listed_names:
            errors.append(f"README.md: missing skill listing for {skill_name}")

    for skill_name in listed_names:
        if skill_name not in expected_names:
            errors.append(f"README.md: lists unknown skill {skill_name}")

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
    errors.extend(validate_readme(repo_root, skill_dirs))

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(f"[OK] validated {len(skill_dirs)} skill(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

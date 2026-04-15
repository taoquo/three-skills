#!/usr/bin/env python3
"""Validator for the local skills repository."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 500
REQUIRED_TOP_LEVEL_FIELDS = ("name", "description", "license")
REQUIRED_METADATA_FIELDS = ("category", "render_backends", "shader_language")
REQUIRED_HOST_MARKDOWN = (
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    ".claude/INSTALL.md",
    ".codex/INSTALL.md",
    ".cursor-plugin/INSTALL.md",
    ".opencode/INSTALL.md",
    ".github/pull_request_template.md",
)
REQUIRED_TOP_LEVEL_FILES = (
    "LICENSE",
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
)
REQUIRED_HOST_JSON_FIELDS = {
    ".claude-plugin/plugin.json": ("name", "description", "version", "author", "homepage", "repository", "license"),
    ".claude-plugin/marketplace.json": ("name", "description", "owner", "plugins"),
    ".cursor-plugin/plugin.json": (
        "name",
        "displayName",
        "description",
        "version",
        "author",
        "homepage",
        "repository",
        "license",
        "skills",
    ),
}
DESCRIPTION_WORKFLOW_PATTERNS = (
    re.compile(r"\bstep-by-step\b"),
    re.compile(r"\bworkflow\b.{0,40}\b(?:that|which|to)\b"),
    re.compile(
        r"\b(?:produce|produces|generate|generates|return|returns|deliver|delivers)\b.{0,50}\b(?:report\.md|artifact|artifacts|demo|demos|output|outputs|gui|controls)\b"
    ),
    re.compile(r"\bthen\b.{0,50}\b(?:produce|produces|generate|generates|return|returns|deliver|delivers)\b"),
    re.compile(r"\b(?:write|writes|update|updates|create|creates)\b.{0,50}\breport\.md\b"),
)


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


def validate_host_support(repo_root: Path) -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_TOP_LEVEL_FILES:
        path = repo_root / relative_path
        if not path.exists():
            errors.append(f"{relative_path}: missing file")

    for relative_path in REQUIRED_HOST_MARKDOWN:
        path = repo_root / relative_path
        if not path.exists():
            errors.append(f"{relative_path}: missing file")
            continue
        errors.extend(validate_markdown_links(path))

    for relative_path, required_fields in REQUIRED_HOST_JSON_FIELDS.items():
        path = repo_root / relative_path
        if not path.exists():
            errors.append(f"{relative_path}: missing file")
            continue

        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{relative_path}: invalid JSON ({exc})")
            continue

        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"{relative_path}: missing field {field}")

        if relative_path == ".claude-plugin/marketplace.json":
            plugins = data.get("plugins")
            if not isinstance(plugins, list) or not plugins:
                errors.append(f"{relative_path}: plugins must be a non-empty list")
            else:
                plugin = plugins[0]
                if not isinstance(plugin, dict):
                    errors.append(f"{relative_path}: first plugin entry must be an object")
                else:
                    for field in ("name", "description", "version", "source", "author"):
                        if field not in plugin or not plugin[field]:
                            errors.append(f"{relative_path}: first plugin entry missing field {field}")

        if relative_path == ".cursor-plugin/plugin.json":
            skills_path = data.get("skills")
            if skills_path != "./skills/":
                errors.append(f"{relative_path}: skills must be set to ./skills/")

    return errors


def validate_claude_mirrors(repo_root: Path, skill_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    claude_skills_root = repo_root / ".claude" / "skills"

    if not claude_skills_root.exists():
        return [".claude/skills: missing directory"]

    for skill_dir in skill_dirs:
        mirror_path = claude_skills_root / skill_dir.name
        if not mirror_path.exists():
            errors.append(f".claude/skills/{skill_dir.name}: missing mirror entry")
            continue

        if not mirror_path.is_symlink():
            errors.append(f".claude/skills/{skill_dir.name}: mirror entry must be a symlink")
            continue

        if mirror_path.resolve() != skill_dir.resolve():
            errors.append(f".claude/skills/{skill_dir.name}: mirror entry must point to skills/{skill_dir.name}")

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
    else:
        if not description.startswith("Use when "):
            errors.append(f"{skill_dir.name}: description must start with 'Use when '")
        if len(description) > MAX_DESCRIPTION_LENGTH:
            errors.append(f"{skill_dir.name}: description exceeds {MAX_DESCRIPTION_LENGTH} characters")
        if any(pattern.search(description.lower()) for pattern in DESCRIPTION_WORKFLOW_PATTERNS):
            errors.append(
                f"{skill_dir.name}: description should describe trigger conditions only, not workflow or outputs"
            )

    if not (skill_dir / "references").exists():
        errors.append(f"{skill_dir.name}: missing references/ directory")
    elif not (skill_dir / "references" / "README.md").exists():
        errors.append(f"{skill_dir.name}: missing references/README.md")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        errors.append(f"{skill_dir.name}: missing agents/openai.yaml")

    owns_templates = parse_bool(data.get("metadata.owns_templates"))
    if owns_templates:
        template_root = skill_dir / "assets" / "templates"
        if not template_root.exists():
            errors.append(f"{skill_dir.name}: missing assets/templates/ directory")
        elif skill_dir.name == "replicator":
            runtime_versions = skill_dir / "assets" / "runtime-versions.json"
            workflow_schema = skill_dir / "assets" / "workflow-schema.json"
            if not runtime_versions.exists():
                errors.append(f"{skill_dir.name}: missing assets/runtime-versions.json")
            if not workflow_schema.exists():
                errors.append(f"{skill_dir.name}: missing assets/workflow-schema.json")
            else:
                try:
                    schema = json.loads(workflow_schema.read_text())
                except json.JSONDecodeError as exc:
                    errors.append(f"{skill_dir.name}: invalid assets/workflow-schema.json ({exc})")
                else:
                    if not isinstance(schema, dict):
                        errors.append(f"{skill_dir.name}: assets/workflow-schema.json must contain a top-level object")
                    else:
                        for field in (
                            "defaults",
                            "option_lists",
                            "report",
                            "sources_json",
                            "review_artifact_manifest",
                        ):
                            if field not in schema:
                                errors.append(f"{skill_dir.name}: assets/workflow-schema.json missing field {field}")
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


def validate_version_consistency(repo_root: Path) -> list[str]:
    errors: list[str] = []
    versions: dict[str, str] = {}

    json_sources = {
        ".claude-plugin/plugin.json": "version",
        ".cursor-plugin/plugin.json": "version",
    }

    for relative_path, field in json_sources.items():
        path = repo_root / relative_path
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        version = data.get(field)
        if isinstance(version, str) and version:
            versions[relative_path] = version

    marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
    if marketplace_path.exists():
        data = json.loads(marketplace_path.read_text())
        plugins = data.get("plugins")
        if isinstance(plugins, list) and plugins:
            plugin = plugins[0]
            if isinstance(plugin, dict):
                version = plugin.get("version")
                if isinstance(version, str) and version:
                    versions[".claude-plugin/marketplace.json"] = version

    if not versions:
        return errors

    unique_versions = sorted(set(versions.values()))
    if len(unique_versions) > 1:
        joined = ", ".join(f"{path}={version}" for path, version in sorted(versions.items()))
        errors.append(f"version mismatch across public metadata: {joined}")

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
    errors.extend(validate_host_support(repo_root))
    errors.extend(validate_claude_mirrors(repo_root, skill_dirs))
    errors.extend(validate_version_consistency(repo_root))

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(f"[OK] validated {len(skill_dirs)} skill(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

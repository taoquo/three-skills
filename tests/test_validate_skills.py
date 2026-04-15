import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "validate_skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", MODULE_PATH)
assert SPEC and SPEC.loader
validate_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_skills)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def create_skill(
    repo_root: Path,
    *,
    name: str = "demo-skill",
    description: str,
    include_references_readme: bool = True,
) -> Path:
    skill_dir = repo_root / "skills" / name
    write_text(
        skill_dir / "SKILL.md",
        f"""---
name: {name}
license: MIT
description: {description}
metadata:
  category: threejs
  render_backends:
    - webgpu
    - webgl2
  shader_language: tsl
---

# Demo Skill

## Overview

Short overview.

## Workflow

1. Do the thing.

## Deliverables

- One artifact.
""",
    )
    write_text(
        skill_dir / "agents" / "openai.yaml",
        """interface:
  display_name: "Demo Skill"
  short_description: "Demo skill"
  default_prompt: "Use $demo-skill when the task matches the trigger."
""",
    )
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)
    if include_references_readme:
        write_text(
            skill_dir / "references" / "README.md",
            """# Demo References

## Suggested Order

1. None
""",
        )
    return skill_dir


class ValidateSkillsTests(unittest.TestCase):
    def test_description_must_start_with_use_when(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            skill_dir = create_skill(
                repo_root,
                description="Analyze references and recreate the effect in Three.js.",
            )

            errors = validate_skills.validate_skill(skill_dir)

            self.assertIn(
                "demo-skill: description must start with 'Use when '",
                errors,
            )

    def test_description_rejects_workflow_summary_language(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            skill_dir = create_skill(
                repo_root,
                description="Use when the task is to study a material, then produce a REPORT.md with outputs.",
            )

            errors = validate_skills.validate_skill(skill_dir)

            self.assertIn(
                "demo-skill: description should describe trigger conditions only, not workflow or outputs",
                errors,
            )

    def test_references_readme_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            skill_dir = create_skill(
                repo_root,
                description="Use when the task is to study a focused material treatment in isolation.",
                include_references_readme=False,
            )

            errors = validate_skills.validate_skill(skill_dir)

            self.assertIn(
                "demo-skill: missing references/README.md",
                errors,
            )

    def test_valid_skill_passes_new_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            skill_dir = create_skill(
                repo_root,
                description="Use when the task is to study a focused material treatment in isolation rather than recreate a full effect.",
            )

            errors = validate_skills.validate_skill(skill_dir)

            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

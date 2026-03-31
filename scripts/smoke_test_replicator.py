#!/usr/bin/env python3
"""Smoke-test the replicator scaffolder across its canonical archetype profiles."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


def load_init_effect_module(repo_root: Path):
    module_path = repo_root / "skills" / "replicator" / "scripts" / "init_effect.py"
    spec = importlib.util.spec_from_file_location("replicator_init_effect", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_contains(text: str, needle: str, context: str) -> None:
    if needle not in text:
        raise AssertionError(f"missing {needle!r} in {context}")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    module = load_init_effect_module(repo_root)
    canonical_profiles = sorted(module.PROFILE_PRESETS)

    with tempfile.TemporaryDirectory(prefix="replicator-smoke-") as tmp:
        tmp_root = Path(tmp)

        for profile in canonical_profiles:
            slug = f"smoke-{profile}"
            effect_dir = module.scaffold_effect(
                slug=slug,
                title=f"Smoke {profile}",
                output_root=tmp_root / profile,
                shader="auto",
                backend="auto",
                profile=profile,
            )

            report_path = effect_dir / "REPORT.md"
            summary_path = effect_dir / "research" / "summary.md"
            sources_path = effect_dir / "research" / "sources.json"
            checklist_path = effect_dir / "captures" / "checklist.md"
            index_path = effect_dir / "index.html"

            for path in (report_path, summary_path, sources_path, checklist_path, index_path):
                if not path.exists():
                    raise AssertionError(f"missing expected file: {path}")

            summary_text = summary_path.read_text()
            report_text = report_path.read_text()
            index_text = index_path.read_text()
            sources = json.loads(sources_path.read_text())

            expected = module.PROFILE_PRESETS[profile]
            assert_contains(summary_text, f"- Effect archetype: `{expected['effect_archetype']}`", str(summary_path))
            assert_contains(summary_text, f"- Starter profile: `{profile}`", str(summary_path))
            assert_contains(summary_text, "## Suggested Route", str(summary_path))
            assert_contains(summary_text, "## Suggested Modules", str(summary_path))
            assert_contains(summary_text, "## Suggested Quality Ladder", str(summary_path))
            assert_contains(summary_text, f"- Three.js version: `{module.THREE_VERSION}`", str(summary_path))
            assert_contains(summary_text, f"- lil-gui version: `{module.LIL_GUI_VERSION}`", str(summary_path))

            assert sources["profile"] == profile
            assert sources["effect_archetype"] == expected["effect_archetype"]
            assert sources["resource_model"] == expected["resource_model"]
            assert sources["pass_topology"] == expected["pass_topology"]
            assert sources["post_pipeline_type"] == expected["post_pipeline_type"]
            assert sources["render_target_layout"] == expected["render_target_layout"]
            assert sources["history_requirement"] == expected["history_requirement"]
            assert sources["three_version"] == module.THREE_VERSION
            assert sources["lil_gui_version"] == module.LIL_GUI_VERSION

            if "__THREE_VERSION__" in index_text or "__LIL_GUI_VERSION__" in index_text:
                raise AssertionError(f"runtime version token was not replaced in {index_path}")
            assert_contains(index_text, f"three@{module.THREE_VERSION}", str(index_path))
            assert_contains(index_text, f"lil-gui@{module.LIL_GUI_VERSION}", str(index_path))

            assert_contains(report_text, "## Archetype Route", str(report_path))
            assert_contains(report_text, "## Search Log", str(report_path))
            assert_contains(report_text, "## Evidence vs Inference", str(report_path))
            assert_contains(report_text, "## Shortest Convincing Path", str(report_path))
            assert_contains(report_text, "## Visual Acceptance", str(report_path))

    print(f"[OK] smoke-tested replicator scaffolds for {len(canonical_profiles)} canonical profile(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Scaffold an effect folder from the replicator template.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

TEXT_SUFFIXES = {
    ".css",
    ".frag",
    ".glsl",
    ".html",
    ".js",
    ".json",
    ".md",
    ".txt",
    ".vert",
}
BACKENDS = {"webgpu", "webgl2", "auto"}
SHADER_MODES = {"tsl", "legacy", "auto"}
PROFILES = {"basic", "post", "particles", "material"}
TEMPLATE_BY_KEY = {
    ("tsl", "webgpu"): "tsl-webgpu",
    ("tsl", "webgl2"): "tsl-webgl2",
    ("legacy", "webgl2"): "legacy-glsl",
}


def normalize_slug(raw: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", raw.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ValueError("effect slug is empty after normalization")
    return slug


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def replace_tokens(path: Path, replacements: dict[str, str]) -> None:
    if path.suffix not in TEXT_SUFFIXES and path.name not in {".gitignore", ".gitattributes"}:
        return
    text = path.read_text()
    for source, target in replacements.items():
        text = text.replace(source, target)
    path.write_text(text)


def resolve_generation_mode(shader: str, backend: str) -> tuple[str, str, str]:
    resolved_shader = "tsl" if shader == "auto" else shader
    resolved_backend = "webgpu" if backend == "auto" else backend

    if resolved_shader == "legacy" and resolved_backend == "webgpu":
        raise ValueError("legacy shader mode only supports the webgl2 backend")

    template_name = TEMPLATE_BY_KEY.get((resolved_shader, resolved_backend))
    if template_name is None:
        raise ValueError(
            f"no template available for shader={resolved_shader} backend={resolved_backend}"
        )

    return resolved_shader, resolved_backend, template_name


def write_supporting_files(
    effect_dir: Path,
    slug: str,
    title: str,
    shader: str,
    backend: str,
    profile: str,
) -> None:
    captures_dir = effect_dir / "captures"
    research_dir = effect_dir / "research"
    captures_dir.mkdir(exist_ok=True)
    research_dir.mkdir(exist_ok=True)
    (captures_dir / ".gitkeep").write_text("")

    summary = f"""# {title} Research Summary

- Effect slug: `{slug}`
- Shader authoring language: `{shader}`
- Runtime backend: `{backend}`
- Profile: `{profile}`
- Target environment: `desktop-first`
- Performance priority: `deferred until look is correct`
- Status: `todo`

## Notes

- Search canonical and mainstream graphics sources first, then engine references, then the Three.js landing path.
- Validate the final renderer and TSL decisions against the official Three.js docs before sign-off.
- Add the link tree, search terms, and implementation takeaways here.
- Mirror the final backend choice and fallback path in `../REPORT.md`.
"""
    (research_dir / "summary.md").write_text(summary)

    sources = {
        "effect_slug": slug,
        "effect_title": title,
        "shader_language": shader,
        "backend": backend,
        "profile": profile,
        "target_environment": "desktop-first",
        "performance_priority": "deferred until look is correct",
        "sources": [],
    }
    (research_dir / "sources.json").write_text(json.dumps(sources, indent=2) + "\n")


def scaffold_effect(
    slug: str,
    title: str,
    output_root: Path,
    shader: str,
    backend: str,
    profile: str,
) -> Path:
    skill_root = Path(__file__).resolve().parent.parent
    resolved_shader, resolved_backend, template_name = resolve_generation_mode(shader, backend)
    template_dir = skill_root / "assets" / "templates" / template_name
    report_template = skill_root / "assets" / "report-template.md"
    effect_dir = output_root / "effects" / slug

    if effect_dir.exists():
        raise FileExistsError(f"output directory already exists: {effect_dir}")

    effect_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template_dir, effect_dir)

    replacements = {
        "__EFFECT_SLUG__": slug,
        "__EFFECT_TITLE__": title,
        "__BACKEND__": resolved_backend,
        "__SHADER_LANGUAGE__": resolved_shader,
        "__PROFILE__": profile,
    }

    for path in effect_dir.rglob("*"):
        if path.is_file():
            replace_tokens(path, replacements)

    report_text = report_template.read_text()
    for source, target in replacements.items():
        report_text = report_text.replace(source, target)
    (effect_dir / "REPORT.md").write_text(report_text)
    write_supporting_files(effect_dir, slug, title, resolved_shader, resolved_backend, profile)

    return effect_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create effects/<slug>/ from the bundled template.",
    )
    parser.add_argument("effect_slug", help="Effect name or slug")
    parser.add_argument(
        "--title",
        help="Optional human-readable title. Defaults to a title-cased version of the slug.",
    )
    parser.add_argument(
        "--backend",
        default="auto",
        choices=sorted(BACKENDS),
        help="Runtime backend to scaffold. Defaults to auto, which currently prefers webgpu.",
    )
    parser.add_argument(
        "--shader",
        default="auto",
        choices=sorted(SHADER_MODES),
        help="Shader authoring mode. Defaults to auto, which currently resolves to tsl.",
    )
    parser.add_argument(
        "--profile",
        default="basic",
        choices=sorted(PROFILES),
        help="Starter profile label to record in the generated research files.",
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Project root where the effects/ directory should be created. Defaults to the current directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        slug = normalize_slug(args.effect_slug)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    title = args.title.strip() if args.title else title_from_slug(slug)
    output_root = Path(args.output).resolve()

    try:
        effect_dir = scaffold_effect(
            slug,
            title,
            output_root,
            args.shader,
            args.backend,
            args.profile,
        )
    except (FileExistsError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Created {effect_dir}")
    print("[OK] Update REPORT.md and research/summary.md first, then replace the inline starter scene in index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

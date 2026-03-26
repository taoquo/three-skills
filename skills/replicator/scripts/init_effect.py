#!/usr/bin/env python3
"""
Scaffold an effect folder from the replicator template.
"""

from __future__ import annotations

import argparse
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


def scaffold_effect(slug: str, title: str, output_root: Path) -> Path:
    skill_root = Path(__file__).resolve().parent.parent
    template_dir = skill_root / "assets" / "template"
    report_template = skill_root / "assets" / "report-template.md"
    effect_dir = output_root / "effects" / slug

    if effect_dir.exists():
        raise FileExistsError(f"output directory already exists: {effect_dir}")

    effect_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template_dir, effect_dir)

    replacements = {
        "__EFFECT_SLUG__": slug,
        "__EFFECT_TITLE__": title,
    }

    for path in effect_dir.rglob("*"):
        if path.is_file():
            replace_tokens(path, replacements)

    report_text = report_template.read_text()
    for source, target in replacements.items():
        report_text = report_text.replace(source, target)
    (effect_dir / "REPORT.md").write_text(report_text)

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
        effect_dir = scaffold_effect(slug, title, output_root)
    except FileExistsError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Created {effect_dir}")
    print("[OK] Update REPORT.md first, then replace the placeholder scene in main.js")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

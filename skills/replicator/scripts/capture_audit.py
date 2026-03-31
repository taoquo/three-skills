#!/usr/bin/env python3
"""Generate a manifest and lightweight review summary for replicator captures."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
DEFAULT_SLOTS = ("01", "02")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit captures/reference-*.png and captures/current-*.png for a replicator effect.",
    )
    parser.add_argument(
        "effect_dir",
        help="Effect directory that contains captures/, for example effects/my-effect or test/my-fixture.",
    )
    parser.add_argument(
        "--slots",
        default=",".join(DEFAULT_SLOTS),
        help="Comma-separated slot ids to expect by default. Defaults to 01,02.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any expected pair is missing.",
    )
    return parser.parse_args()


def read_png_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def read_jpeg_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        data = handle.read()
    if not data.startswith(b"\xff\xd8"):
        return None

    offset = 2
    length = len(data)
    while offset + 9 < length:
        if data[offset] != 0xFF:
            offset += 1
            continue
        marker = data[offset + 1]
        offset += 2
        if marker in {0xD8, 0xD9}:
            continue
        if offset + 2 > length:
            return None
        segment_length = int.from_bytes(data[offset : offset + 2], "big")
        if segment_length < 2 or offset + segment_length > length:
            return None
        if marker in {
            0xC0,
            0xC1,
            0xC2,
            0xC3,
            0xC5,
            0xC6,
            0xC7,
            0xC9,
            0xCA,
            0xCB,
            0xCD,
            0xCE,
            0xCF,
        }:
            if offset + 7 > length:
                return None
            height = int.from_bytes(data[offset + 3 : offset + 5], "big")
            width = int.from_bytes(data[offset + 5 : offset + 7], "big")
            return width, height
        offset += segment_length
    return None


def read_webp_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(30)
    if len(header) < 30 or header[:4] != b"RIFF" or header[8:12] != b"WEBP":
        return None
    chunk = header[12:16]
    if chunk == b"VP8X" and len(header) >= 30:
        width = 1 + int.from_bytes(header[24:27], "little")
        height = 1 + int.from_bytes(header[27:30], "little")
        return width, height
    return None


def read_image_size(path: Path) -> tuple[int, int] | None:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return read_png_size(path)
    if suffix in {".jpg", ".jpeg"}:
        return read_jpeg_size(path)
    if suffix == ".webp":
        return read_webp_size(path)
    return None


def collect_capture_slots(captures_dir: Path, default_slots: list[str]) -> list[str]:
    slots = set(default_slots)
    pattern = re.compile(r"^(reference|current)-([a-zA-Z0-9_-]+)\.[^.]+$")

    for path in captures_dir.iterdir():
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        match = pattern.match(path.name)
        if match:
            slots.add(match.group(2))

    return sorted(slots)


def resolve_capture_file(captures_dir: Path, prefix: str, slot: str) -> Path | None:
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        candidate = captures_dir / f"{prefix}-{slot}{ext}"
        if candidate.exists():
            return candidate
    return None


def build_manifest(effect_dir: Path, slots: list[str]) -> dict[str, object]:
    captures_dir = effect_dir / "captures"
    entries: list[dict[str, object]] = []

    for slot in slots:
        reference_path = resolve_capture_file(captures_dir, "reference", slot)
        current_path = resolve_capture_file(captures_dir, "current", slot)
        reference_size = read_image_size(reference_path) if reference_path else None
        current_size = read_image_size(current_path) if current_path else None

        entry = {
            "slot": slot,
            "reference_path": str(reference_path.relative_to(effect_dir)) if reference_path else None,
            "current_path": str(current_path.relative_to(effect_dir)) if current_path else None,
            "reference_exists": reference_path is not None,
            "current_exists": current_path is not None,
            "reference_size": list(reference_size) if reference_size else None,
            "current_size": list(current_size) if current_size else None,
            "size_match": bool(reference_size and current_size and reference_size == current_size),
        }
        entries.append(entry)

    complete_pairs = sum(1 for entry in entries if entry["reference_exists"] and entry["current_exists"])
    missing_reference = [entry["slot"] for entry in entries if not entry["reference_exists"]]
    missing_current = [entry["slot"] for entry in entries if not entry["current_exists"]]
    size_mismatches = [
        entry["slot"]
        for entry in entries
        if entry["reference_exists"] and entry["current_exists"] and not entry["size_match"]
    ]

    return {
        "effect_dir": str(effect_dir),
        "captures_dir": str(captures_dir),
        "expected_slots": slots,
        "complete_pairs": complete_pairs,
        "missing_reference": missing_reference,
        "missing_current": missing_current,
        "size_mismatches": size_mismatches,
        "entries": entries,
    }


def write_review(effect_dir: Path, manifest: dict[str, object]) -> None:
    captures_dir = effect_dir / "captures"
    entries = manifest["entries"]
    lines = [
        "# Capture Review",
        "",
        f"- Complete pairs: `{manifest['complete_pairs']}`",
        f"- Missing reference slots: `{', '.join(manifest['missing_reference']) or 'none'}`",
        f"- Missing current slots: `{', '.join(manifest['missing_current']) or 'none'}`",
        f"- Size mismatches: `{', '.join(manifest['size_mismatches']) or 'none'}`",
        "",
        "## Pair Coverage",
        "",
        "| Slot | Reference | Current | Size Match | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]

    for entry in entries:
        ref_label = entry["reference_path"] or "missing"
        cur_label = entry["current_path"] or "missing"
        size_match = "yes" if entry["size_match"] else ("n/a" if not entry["reference_exists"] or not entry["current_exists"] else "no")
        lines.append(f"| `{entry['slot']}` | `{ref_label}` | `{cur_label}` | `{size_match}` | `TODO` |")

    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "- Compare the paired captures using the fidelity rubric in `checklist.md`.",
            "- Focus first on silhouette, motion, density, palette, and finish gaps.",
            "- If a pair is missing, capture it before calling the effect done.",
            "",
        ]
    )
    (captures_dir / "review.md").write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    effect_dir = Path(args.effect_dir).resolve()
    captures_dir = effect_dir / "captures"

    if not effect_dir.exists():
        print(f"[ERROR] effect directory not found: {effect_dir}", file=sys.stderr)
        return 1
    if not captures_dir.exists():
        print(f"[ERROR] captures/ directory not found under: {effect_dir}", file=sys.stderr)
        return 1

    default_slots = [slot.strip() for slot in args.slots.split(",") if slot.strip()]
    slots = collect_capture_slots(captures_dir, default_slots)
    manifest = build_manifest(effect_dir, slots)

    (captures_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    write_review(effect_dir, manifest)

    print(f"[OK] wrote {captures_dir / 'manifest.json'}")
    print(f"[OK] wrote {captures_dir / 'review.md'}")

    if args.strict and (manifest["missing_reference"] or manifest["missing_current"]):
        print("[ERROR] capture pairs are incomplete", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

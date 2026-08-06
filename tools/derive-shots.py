#!/usr/bin/env python3
"""Derive the site's web images from the canonical studio captures.

This is asset preparation, not a site build step. The site itself is
plain static HTML/CSS with no build, no framework and no dependencies.
You run this by hand when captures change; the pages never need editing.

Requires: Pillow (pip install Pillow)

Usage
-----
    python tools/derive-shots.py --source "path/to/your/Shots"
    python tools/derive-shots.py --check      # report only, write nothing

To avoid retyping the path, put it in tools/source-path.txt, which is
untracked. This repository is public, so the capture folder location is
kept out of it deliberately.

How the healing works
---------------------
Each capture has ONE canonical source filename. When a shot is re-captured,
it overwrites that canonical file in the studio Shots folder. Re-running this
script re-derives the web set under stable web filenames, so the HTML pages
never change — they already point at the right names.

Shots still awaiting capture are reported as PENDING and skipped. The pages
carry a visible placeholder block for each until the file exists.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required:  pip install Pillow")

REPO = Path(__file__).resolve().parent.parent
SOURCE_CONFIG = REPO / "tools" / "source-path.txt"   # untracked; see .gitignore
OUT_DIR = REPO / "assets" / "shots"
OG_PATH = REPO / "assets" / "og-image.jpg"

WIDTH = 1920          # long edge of the web derivatives
WEBP_QUALITY = 90
JPEG_QUALITY = 90

OG_SIZE = (1200, 630)  # Open Graph / social card

# canonical source filename  ->  web filename stem
DERIVATIVES: dict[str, str] = {
    # Banked and usable today
    "Devlog1_B_Island_Hero.png":     "geomancer-island-hero",
    "Devlog1_C_Before_Plates.png":   "geomancer-range-plates-before",
    "Devlog1_D_Before_FarHalf.png":  "geomancer-range-farhalf-before",
    "Devlog1_E_After_Complete.png":  "geomancer-range-complete-after",
    # Awaiting the post-polish capture session. Capture to THESE filenames
    # and this script picks them up with no further changes.
    "Devlog1_A_Before_Template.png": "geomancer-template-before",
    "Devlog1_A_After_Template.png":  "geomancer-template-after",
    "Devlog1_F_Basin_Wetland.png":   "geomancer-basin-wetland",
}

# Source for the Open Graph card.
OG_SOURCE = "Devlog1_B_Island_Hero.png"

# Filled in as images are written, and reported at the end so the width and
# height attributes in the pages can be kept truthful. Cropping editor chrome
# changes an image's height, so these move when a shot is re-captured.
DIMENSIONS: dict[str, tuple[int, int]] = {}

# Internal review evidence and raw variants. These must never reach the site.
# Guarded here as well as by convention, because a mistake is public.
EXCLUDED_SUBSTRINGS = ("Evidence_Comparison", "_alt_", "_Raw")


def excluded(name: str) -> bool:
    return any(bit in name for bit in EXCLUDED_SUBSTRINGS)


def _row_mean(im: Image.Image, y: int, w: int) -> tuple[float, float, float]:
    px = [im.getpixel((x, y)) for x in range(0, w, max(1, w // 60))]
    return tuple(sum(p[i] for p in px) / len(px) for i in range(3))  # type: ignore[return-value]


def _band_depth(rows: list, edge: float, max_spread: float, margin: int) -> int:
    """Given row means ordered from an outer edge inward, return the depth of
    a uniform strip of editor chrome, or 0 if the edge is ordinary content."""
    cut = 0
    for i in range(1, len(rows)):
        if max(abs(a - b) for a, b in zip(rows[i], rows[i - 1])) > edge:
            cut = i
            break
    if cut == 0:
        return 0
    # Measure uniformity over the solid part of the band, skipping the
    # anti-aliased ramp at its inner edge.
    solid = rows[:max(1, int(cut * 0.6))]
    spread = max(max(r[c] for r in solid) - min(r[c] for r in solid)
                 for c in range(3))
    if spread > max_spread:              # a gradient, not a flat UI strip
        return 0
    return cut + margin


def detect_chrome(im: Image.Image, edge: float = 25.0, max_spread: float = 15.0,
                  cap_frac: float = 0.12, margin: int = 2) -> tuple[int, int]:
    """Depth in pixels of editor chrome along the top and bottom edges.

    Some banked captures include a strip of editor UI above and/or below the
    render — a light strip at the top, a dark toolbar at the bottom. These are
    found by measurement rather than hardcoded per file, so that when a shot
    is re-captured cleanly the crop becomes zero and no real image data is
    lost. That keeps canonical-filename healing intact: overwrite the source,
    re-run, done.

    A strip is not perfectly flat — it can drift a few levels across its
    depth — so it is identified by two things together: a sharp row-to-row
    transition where it ends, and near-uniformity across the strip itself.
    A sky gradient has the second property but not the first; a horizon has
    the first but not the second.

    Every crop is reported on stdout, so an unexpected one is visible rather
    than silent.
    """
    w, h = im.size
    cap = max(4, int(h * cap_frac))
    top_rows = [_row_mean(im, y, w) for y in range(cap)]
    bottom_rows = [_row_mean(im, h - 1 - y, w) for y in range(cap)]
    return (_band_depth(top_rows, edge, max_spread, margin),
            _band_depth(bottom_rows, edge, max_spread, margin))


def derive_one(src: Path, stem: str, check: bool) -> str:
    im = Image.open(src).convert("RGB")
    top, bottom = detect_chrome(im)
    if top or bottom:
        im = im.crop((0, top, im.size[0], im.size[1] - bottom))
    w, h = im.size
    height = round(h * WIDTH / w)
    bits = ([f"{top}px top"] if top else []) + ([f"{bottom}px bottom"] if bottom else [])
    note = f" (cropped {', '.join(bits)})" if bits else ""
    if check:
        return f"would write {stem}.webp / .jpg at {WIDTH}x{height}{note}"

    resized = im.resize((WIDTH, height), Image.LANCZOS)
    webp = OUT_DIR / f"{stem}.webp"
    jpeg = OUT_DIR / f"{stem}.jpg"
    resized.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)
    resized.save(jpeg, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    DIMENSIONS[stem] = (WIDTH, height)
    return (
        f"{WIDTH}x{height}{note}  "
        f"webp {webp.stat().st_size / 1024:.0f} KB  "
        f"jpg {jpeg.stat().st_size / 1024:.0f} KB"
    )


def derive_og(src: Path, check: bool) -> str:
    """Centre-crop to the Open Graph aspect, then resize."""
    im = Image.open(src).convert("RGB")
    top, bottom = detect_chrome(im)
    if top or bottom:
        im = im.crop((0, top, im.size[0], im.size[1] - bottom))
    w, h = im.size
    target = OG_SIZE[0] / OG_SIZE[1]
    if w / h > target:                      # too wide - trim the sides
        new_w = round(h * target)
        box = ((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h)
    else:                                   # too tall - trim top and bottom
        new_h = round(w / target)
        box = (0, (h - new_h) // 2, w, (h - new_h) // 2 + new_h)
    if check:
        return f"would write {OG_PATH.name} at {OG_SIZE[0]}x{OG_SIZE[1]}"
    im.crop(box).resize(OG_SIZE, Image.LANCZOS).save(
        OG_PATH, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True
    )
    return f"{OG_SIZE[0]}x{OG_SIZE[1]}  jpg {OG_PATH.stat().st_size / 1024:.0f} KB"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=None,
                        help="folder holding the canonical capture PNGs")
    parser.add_argument("--check", action="store_true",
                        help="report what would happen; write nothing")
    args = parser.parse_args()

    source: Path | None = args.source
    if source is None and SOURCE_CONFIG.is_file():
        text = SOURCE_CONFIG.read_text(encoding="utf-8").strip()
        if text:
            source = Path(text)
    if source is None:
        sys.exit(
            "No capture folder given.\n"
            "  Pass --source \"path/to/Shots\", or write that path into\n"
            f"  {SOURCE_CONFIG.relative_to(REPO)} (untracked)."
        )
    if not source.is_dir():
        sys.exit(f"Source folder not found: {source}")

    if not args.check:
        OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"source : {source}")
    print(f"output : {OUT_DIR}")
    print(f"quality: webp q{WEBP_QUALITY} / jpeg q{JPEG_QUALITY} at {WIDTH}px\n")

    pending: list[str] = []
    written = 0

    for filename, stem in DERIVATIVES.items():
        if excluded(filename):             # belt and braces
            print(f"  EXCLUDED  {filename}")
            continue
        src = source / filename
        if not src.is_file():
            pending.append(filename)
            print(f"  PENDING   {filename}  ->  {stem}.*  (not captured yet)")
            continue
        print(f"  OK        {filename}  ->  {derive_one(src, stem, args.check)}")
        written += 1

    og_src = source / OG_SOURCE
    if og_src.is_file():
        print(f"\n  OG CARD   {OG_SOURCE}  ->  {derive_og(og_src, args.check)}")
    else:
        print(f"\n  OG CARD   PENDING - {OG_SOURCE} missing")

    if DIMENSIONS and not args.check:
        print("\nSet these on the matching <img> tags so the browser reserves the")
        print("right space and the page does not jump as images load:")
        for stem, (w, h) in DIMENSIONS.items():
            print(f'  {stem:34} width="{w}" height="{h}"')

    print(f"\n{written} derived, {len(pending)} pending.")
    if pending:
        print("Pending shots keep their placeholder block on the page until captured:")
        for name in pending:
            print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

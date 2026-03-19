"""Core conversion logic for HOI4 flags."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence

from PIL import Image

logger = logging.getLogger(__name__)

# HOI4 flag dimensions (width x height)
FLAG_SIZES: dict[str, tuple[int, int]] = {
    "large": (82, 52),
    "medium": (41, 26),
    "small": (10, 7),
}

SUPPORTED_INPUT_EXTS: set[str] = {
    ".tga", ".png", ".ppm", ".jpeg", ".tiff", ".bmp", ".jpg",
}

OUTPUT_EXT = ".tga"


def _is_supported(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_INPUT_EXTS


def discover_flags(source_dir: Path) -> list[Path]:
    """Return sorted list of supported image files in *source_dir*."""
    flags = sorted(p for p in source_dir.iterdir() if p.is_file() and _is_supported(p))
    if not flags:
        logger.warning("No supported image files found in %s", source_dir)
    return flags


def convert_flag(
    src: Path,
    dest_dir: Path,
    size: tuple[int, int],
    output_ext: str = OUTPUT_EXT,
) -> Path:
    """Convert a single flag image: resize to *size* and save as *output_ext*.

    Returns the path of the written file.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_path = dest_dir / (src.stem + output_ext)

    with Image.open(src) as img:
        resized = img.resize(size, Image.LANCZOS)
        resized.save(out_path, compression=None)

    return out_path


def convert_flags(
    source_dir: Path,
    output_dir: Path,
    sizes: Sequence[str] | None = None,
    skip_large: bool = False,
) -> dict[str, list[Path]]:
    """Convert all flags in *source_dir* into HOI4-ready assets.

    Parameters
    ----------
    source_dir:
        Directory containing the source flag images.
    output_dir:
        Root output directory. Sub-folders per size are created here.
    sizes:
        Which sizes to generate. Defaults to all (large, medium, small).
    skip_large:
        If True, assumes source images are already 82×52 .tga and only
        generates medium + small variants.

    Returns
    -------
    dict mapping size name → list of written file paths.
    """
    if sizes is None:
        sizes = ["large", "medium", "small"] if not skip_large else ["medium", "small"]

    flags = discover_flags(source_dir)
    if not flags:
        return {}

    results: dict[str, list[Path]] = {}
    for size_name in sizes:
        dim = FLAG_SIZES[size_name]
        dest = output_dir / size_name
        written: list[Path] = []
        for flag in flags:
            out = convert_flag(flag, dest, dim)
            logger.info("[%s] %s → %s", size_name, flag.name, out)
            written.append(out)
        results[size_name] = written

    return results

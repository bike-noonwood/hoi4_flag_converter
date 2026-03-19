"""Command-line interface for hoi4-flag-converter."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .converter import FLAG_SIZES, SUPPORTED_INPUT_EXTS, convert_flags


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hoi4-flags",
        description=(
            "Convert images into Hearts of Iron IV flag assets.\n\n"
            "Reads flag images from a source directory, resizes them to the\n"
            "required HOI4 dimensions, and writes .tga files into per-size\n"
            "sub-folders (large/, medium/, small/) under the output directory."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  hoi4-flags ./my_flags\n"
            "  hoi4-flags ./my_flags -o ./converted --sizes medium small\n"
            "  hoi4-flags ./my_flags --skip-large -v\n"
            "\n"
            "supported input formats:\n"
            f"  {', '.join(sorted(SUPPORTED_INPUT_EXTS))}\n"
            "\n"
            "HOI4 flag dimensions:\n"
            f"  large  = {FLAG_SIZES['large'][0]}×{FLAG_SIZES['large'][1]}\n"
            f"  medium = {FLAG_SIZES['medium'][0]}×{FLAG_SIZES['medium'][1]}\n"
            f"  small  = {FLAG_SIZES['small'][0]}×{FLAG_SIZES['small'][1]}"
        ),
    )

    parser.add_argument(
        "source",
        type=Path,
        help="Directory containing source flag images.",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help=(
            "Root output directory. Sub-folders (large/, medium/, small/) are "
            "created here. Defaults to a 'converted' folder inside SOURCE."
        ),
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        choices=list(FLAG_SIZES.keys()),
        default=None,
        help="Which sizes to generate (default: all three).",
    )
    parser.add_argument(
        "--skip-large",
        action="store_true",
        help=(
            "Skip generating the large (82×52) size. Useful when your source "
            "images are already correctly sized .tga files and you only need "
            "the medium and small variants."
        ),
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed progress for each file.",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress all output except errors.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    # --- configure logging ---
    if args.quiet:
        level = logging.ERROR
    elif args.verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(
        format="%(message)s",
        level=level,
        stream=sys.stderr,
    )

    # --- validate source ---
    source: Path = args.source.resolve()
    if not source.is_dir():
        parser.error(f"source directory does not exist: {source}")

    # --- resolve output ---
    output: Path = (args.output or source / "converted").resolve()

    # --- resolve sizes ---
    sizes = args.sizes
    if sizes is None and args.skip_large:
        sizes = ["medium", "small"]

    # --- run conversion ---
    results = convert_flags(
        source_dir=source,
        output_dir=output,
        sizes=sizes,
        skip_large=args.skip_large,
    )

    if not results:
        print("No supported flag images found.", file=sys.stderr)
        return 1

    # --- summary ---
    if not args.quiet:
        total = sum(len(v) for v in results.values())
        print(f"Converted {total} flag(s) into {len(results)} size(s):")
        for size_name, paths in results.items():
            print(f"  {size_name:>6} ({FLAG_SIZES[size_name][0]}×{FLAG_SIZES[size_name][1]}): "
                  f"{len(paths)} file(s) → {paths[0].parent}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

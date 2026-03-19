# hoi4-flag-converter

A CLI tool that converts images into properly sized [Hearts of Iron IV](https://store.steampowered.com/app/394360/Hearts_of_Iron_IV/) flag assets (`.tga`).

HOI4 expects flags in three sizes:

| Size   | Dimensions |
|--------|-----------|
| Large  | 82 × 52   |
| Medium | 41 × 26   |
| Small  | 10 × 7    |

This tool takes a directory of flag images in any common format and outputs correctly sized `.tga` files organized into sub-folders.

## Installation

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

## Usage

```
hoi4-flags <source_directory> [options]
```

### Basic conversion

Convert all flags in `./my_flags`, writing output to `./my_flags/converted/`:

```bash
hoi4-flags ./my_flags
```

### Specify output directory

```bash
hoi4-flags ./my_flags -o ./output
```

### Generate only certain sizes

```bash
hoi4-flags ./my_flags --sizes medium small
```

### Skip large (source images are already 82×52)

If your images are already at the correct large resolution, skip regenerating them and only create the medium and small variants:

```bash
hoi4-flags ./my_flags --skip-large
```

### Verbose output

```bash
hoi4-flags ./my_flags -v
```

### Full help

```bash
hoi4-flags --help
```

## Supported input formats

`.bmp`, `.jpg`, `.jpeg`, `.png`, `.ppm`, `.tga`, `.tiff`

## Flag naming

Name your source images using the HOI4 tag format, e.g.:

- `AFG_communism.png`
- `JAP_fascism.png`
- `ZIM_democratic.png`

The converter preserves the filename stem and only changes the extension to `.tga`.

## License

MIT

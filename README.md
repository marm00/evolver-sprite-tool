# Evolver Sprite Tool: generating standardized assets for Evolver

This is a command line tool for opinionated image manipulation with type conversion, scaling, and chroma keying.

## Usage

### Directory Structure

- `in/`: Default folder for input images.
- `out/`: Default folder for output images.

### Examples

```sh
$ python main.py -i ./in/*.webp -o ./out
Processed 1 image(s) in 0.00 seconds. View ./out for details.
```

### Option Summary

The tool recognizes these options:

| Option | Description | Default |
| --- | --- | --- |
| `-i`, `--input` | The file(s) to process (file name, directory name, or regex pattern) | `./in` |
| `-f`, `--format` | The image format to convert to (e.g. PNG, JPEG, BMP) | `PNG` |

### Requirements

- Python 3.9 or higher *(determined with `vermin t=3.7- --backport argparse --eval-annotations --no-parse-comments`)*

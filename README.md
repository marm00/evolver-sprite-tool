# Evolver Sprite Tool

Transform images into standardized assets for [Evolver](https://github.com/marm00/evolver).

This is a command line tool for opinionated image manipulation with type conversion, scaling, and chroma keying.

## Usage

### Directories

- `in/`: Default folder for input images.
- `out/`: Default folder for output images.

### Examples

```console
$ python evolver.py
Processed 2/2 images in 0.5 seconds. View results in {absolute path}\out.

$ python evolver.py -i D:/images/old -o D:/images/new
Processed 2/2 images in 0.07 seconds. View results in D:\images\new.

$ python evolver.py -i ./in/**/*.png -o .\newfolder
Processed 9/9 images in 0.12 seconds. View results in {absolute path}\newfolder.

$ python evolver.py -i ./in/wolf/*grey*.jpeg --ignore txt .zip png
Processed 1/1 images in 0.04 seconds. View results in {absolute path}\out.

$ python evolver.py -f PNG -s 128x128
Processed 1/1 images in 0.05 seconds. View results in {absolute path}\out.

$ python evolver.py -m 255,0,0,50
Processed 1/1 images in 0.04 seconds. View results in {absolute path}\out.
```

### Option Summary

The tool recognizes these options:

| Option | Description | Default |
| --- | --- | :---: |
| `-i` or `--input` | The file(s) to process (file name, directory name, or [glob pattern](https://docs.python.org/3/library/glob.html)) | `./in` |
| `-o` or `--output` | The output folder for the processed images | `./out` |
| `--ignore` | File extensions to ignore (e.g., txt jpg .zip .png) | `gitkeep` |
| `-f` or `--format` | Override the inferred output image format, defaults to PNG if mask is used and the provided format does not support RGBA | `None` |
| `-s` or `--size` | The output image size in WIDTHxHEIGHT format (e.g. 64x64) | `64x64` |
| `-m` or `--mask` | Transparentize pixels matching this mask in RED,GREEN,BLUE,THRESHOLD format (e.g. 0,255,0,100). The transparent mask is applied to pixels with a [euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance) below the threshold. If mask is used and the final format does not support RGBA, the output format will be PNG | `(0,255,0,100)` |

### Requirements

- Python 3.9 or higher *(determined with [vermin](https://github.com/netromdk/vermin))*  
`vermin t=3.7- --backport argparse --eval-annotations --no-parse-comments .`

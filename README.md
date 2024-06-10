# Evolver Sprite Tool

Transform images into standardized assets for [Evolver](https://github.com/marm00/evolver).

This is a command line tool for opinionated image manipulation with [PIL](https://pillow.readthedocs.io/).

## Usage

### Directories

- `in/`: Default folder for input images.
- `out/`: Default folder for output images.

### Examples

```console
$ python evolver.py
Processed 2/2 images in 0.05 seconds. View results in {absolute path}\out.

$ python evolver.py --input D:/images/old --output D:/images/new
Processed 2/2 images in 0.07 seconds. View results in D:\images\new.

$ python evolver.py --input ./in/**/*.webp --output .\newfolder
Processed 9/9 images in 0.12 seconds. View results in {absolute path}\newfolder.

$ python evolver.py --input ./in/wolf/*grey*.jpeg --ignore txt .zip png
Processed 1/1 images in 0.04 seconds. View results in {absolute path}\out.

$ python evolver.py --format PNG -size 128x128 --center 0
Processed 4/4 images in 0.08 seconds. View results in {absolute path}\out.

$ python evolver.py --mask 255,0,0,50
Processed 1/1 images in 0.06 seconds. View results in {absolute path}\out.
```

### Option Summary

The tool recognizes these options:

| Option | Description | Default |
| --- | --- | :---: |
| `-i`, `--input` | The file(s) to process (file name, directory name, or [glob pattern](https://docs.python.org/3/library/glob.html)) | `./in` |
| `-o`, `--output`| The output folder for the processed images | `./out` |
| `--ignore` | File extensions to ignore (e.g., txt jpg .zip .png) | `gitkeep` |
| `-f`, `--format` | Override the inferred output image format *([note](#note))* | `None` |
| `-s`, `--size` | The output image size in WIDTHxHEIGHT format | `64x64` |
| `-m`, `--mask` | Turn pixels transparent if similar to the defined mask *([note](#note))* | `0,255,0,100` |
| `-c`, `--center` | Center the image, 0 or 1 (default). Match `--mask`! *([note](#note))* | `1` |

#### Note

Not all image formats support the **A**lpha channel in RGB**A**. This program changes the destination file extension to WEBP for transparentization when the file extension or `--format` is not one of PNG, TIFF, WEBP, or GIF.

For each image pixel, the [euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance) is calculated from its RGB values to the provided mask RGB (like full green at 0,255,0). If this distance is shorter than the provided threshold, the pixel is converted to 255,255,255,0.

For centering to work, a clear separation between the background and the foreground is required. This separation should be reflected in the `--mask` value.
For instance, if the foreground is black and the background is white, the `--mask` value should be `255,255,255,100`.

### Requirements

- Python 3.9 or higher *(determined with [vermin](https://github.com/netromdk/vermin))*  
`vermin t=3.7- --backport argparse --eval-annotations --no-parse-comments .`
- Install the packages listed in [requirements.txt](./requirements.txt)  
  `pip install -r requirements.txt`

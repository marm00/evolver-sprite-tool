# Evolver Sprite Tool

Transform images into standardized assets for [Evolver](https://github.com/marm00/evolver).

This is a command line tool for opinionated image manipulation with type conversion, scaling, and chroma keying.

## Usage

### Directory Structure

- `in/`: Default folder for input images.
- `out/`: Default folder for output images.

### Examples

```console
$ python evolver.py
Processed 2 image(s) in 0.00 seconds. View results in {absolute path}\out.

$ python evolver.py -i D:/images/old -o D:/images/new
Processed 2 image(s) in 0.00 seconds. View results in D:\images\new.

$ python evolver.py -i **/*.webp -o .\newfolder
Processed 1 image(s) in 0.00 seconds. View results in {absolute path}\newfolder.

$ python evolver.py -i ./in/wolf/*grey*.jpeg
Processed 1 image(s) in 0.00 seconds. View results in .\out.
```

### Option Summary

The tool recognizes these options:

| Option | Description | Default |
| --- | --- | --- |
| `-i`, `--input` | The file(s) to process (file name, directory name, or [glob pattern](https://docs.python.org/3/library/glob.html)) | `./in` |
| `-f`, `--format` | The image format to convert to (e.g. PNG, JPEG, BMP) | `PNG` |

### Requirements

- Python 3.9 or higher *(determined with [vermin](https://github.com/netromdk/vermin))*  
`vermin t=3.7- --backport argparse --eval-annotations --no-parse-comments .`

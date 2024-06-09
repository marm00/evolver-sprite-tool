<div align="center">
  Evolver Sprite Tool: generating standardized assets for Evolver.
</div>

---

This is a command line tool for opinionated image manipulation with type conversion, scaling, and chroma keying.

## Usage

### Directory Structure

- `in/`: Default folder for input images.
- `out/`: Default folder for output images.

### Basic Commands

```sh
python main.py -i ./in/*.webp -o ./out
```

### Option Summary

The tool recognizes these options:

| Option | Description | Default |
| --- | --- | --- |
| `--input`, `-i` | The file(s) to process (file name, directory name, or regex pattern) | `./in` |
| `--format`, `-f` | The image format to convert to (e.g. PNG, JPEG, BMP) | `PNG` |

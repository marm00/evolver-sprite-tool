# Evolver Sprite Tool

## Usage

This image manipulation tool supports type conversion, scaling, and chroma keying.

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
| `--input` or `i` | The file(s) to process (file name, directory name, or regex pattern) | `./in` |

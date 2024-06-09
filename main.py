import argparse
import glob
import os
from pathlib import Path
import re
from PIL import Image


def get_absolute_paths(input_string, ignore_extensions):
    if not os.path.isabs(input_string):
        input_string = os.path.abspath(input_string)

    matched_paths = glob.glob(input_string)
    all_files = set()

    for path in matched_paths:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.add(file_path)
        elif os.path.isfile(path):
            all_files.add(path)

    filtered_files = [
        file
        for file in all_files
        if not any(file.endswith(ext) for ext in ignore_extensions)
    ]

    absolute_paths = [os.path.abspath(file) for file in filtered_files]
    return absolute_paths


def collect_images(input_arg):
    # List to hold the collected file paths
    files = []

    # Check if the input path is a directory
    if os.path.isdir(input_arg):
        # Collect all files from the directory except .gitkeep
        files = [
            f
            for f in glob.glob(os.path.join(input_arg, "*"))
            if not f.endswith(".gitkeeep")
        ]

    # Check if the input path is a file
    elif os.path.isfile(input_arg):
        files = [input_arg]

    # If the input is neither a directory nor a file, treat it as a regex pattern
    else:
        # Get all files in the current directory and subdirectories
        all_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(".")
            for file in files
        ]
        # Filter files based on the regex pattern
        pattern = re.compile(input_arg)
        files = [
            file
            for file in all_files
            if pattern.search(file) and not file.endswith(".gitkeep")
        ]

    return files


def convert_image(input_arg, output_path, size, transparent_green):
    # Open an image file
    with Image.open(input_arg) as img:
        # Resize the image
        img = img.resize(size, Image.ANTIALIAS)

        # Convert green pixels to transparent
        if transparent_green:
            img = img.convert("RGBA")
            data = img.getdata()
            new_data = []
            for item in data:
                # Change all green (0, 255, 0) pixels to transparent
                if item[0] == 0 and item[1] == 255 and item[2] == 0:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)

        # Save the image
        img.save(output_path, "PNG")


def main():
    parser = argparse.ArgumentParser(
        description="Evolver CLI Tool for Image Standardization."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default="./in",
        help="The input string (file name, directory name, or pattern). Defaults to './in'.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="./out",
        help="Output image file path (in png format).",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=str,
        default="64x64",
        help="Output image size in WIDTHxHEIGHT format (default: 64x64).",
    )
    parser.add_argument(
        "-t",
        "--transparent-green",
        action="store_true",
        help="Convert green pixels (0,255,0) to transparent.",
    )
    parser.add_argument(
        "--ignore",
        type=str,
        nargs="*",
        default=["gitkeep"],
        help="File extensions to ignore (e.g., txt md). Defaults to ['gitkeep'].",
    )

    args = parser.parse_args()
    ignore_extensions = [
        ext if ext.startswith(".") else f".{ext}" for ext in args.ignore
    ]
    absolute_paths = get_absolute_paths(args.input, ignore_extensions)
    for path in absolute_paths:
        print(path)

    # Parse the size argument
    try:
        width, height = map(int, args.size.split("x"))
    except ValueError:
        parser.error("Size must be in WIDTHxHEIGHT format, e.g., 64x64")

    # Ensure the output directory exists
    # os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Convert the image
    # convert_image(args.input, args.output, (width, height), args.transparent_green)


if __name__ == "__main__":
    main()

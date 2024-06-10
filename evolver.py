import argparse
import glob
import os
import time
from PIL import Image


def get_absolute_paths(input: str, ignore: list[str]) -> list[str]:
    """
    Get absolute paths for files in a directory or matching a glob pattern.

    Args:
        input (str): The input string representing a file name, directory name, or glob pattern.
        ignore (list[str]): A list of file extensions to ignore. Extensions should include the period (e.g., ".txt").

    Returns:
        list[str]: A list of absolute paths for files that match the input, excluding those with ignored extensions.
    """
    input = os.path.abspath(input)
    matched_paths = glob.glob(input)
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
        file for file in all_files if not any(file.endswith(ext) for ext in ignore)
    ]

    absolute_paths = [os.path.abspath(file) for file in filtered_files]
    return absolute_paths


def convert_image(input_arg, output_path, size, transparent_green, format):
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
        img.save(output_path, format)


def setup_output_directory(output_path):
    if not os.path.isdir(output_path):
        try:
            os.makedirs(output_path, exist_ok=True)
        except OSError as e:
            raise Exception(f"Incorrect format for output path: {e}")
    return os.path.abspath(output_path)


def process_image(path) -> bool:
    error_message = ""

    def skip(message):
        formatted_error = f"WARNING: Skipping {path} because {message}"
        print(formatted_error)
        return formatted_error

    try:
        with Image.open(path) as img:
            print(img.size)
    except FileNotFoundError:
        error_message = skip(f"the file cannot be found.")
    except Image.UnidentifiedImageError:
        error_message = skip(f"the found file cannot be opened and identified.")
    except ValueError:
        error_message = skip(f"the 'mode' is not r, or a StringIO instance is used for 'fp'.")
    except TypeError:
        error_message = skip(f"'formats' is not None, a list or a tuple.")

    return False if error_message else True


def main():
    start_time = time.time()
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
        help="Directory for output images. Defaults to './out'.",
    )
    parser.add_argument(
        "--ignore",
        type=str,
        nargs="*",
        default=["gitkeep"],
        help="File extensions to ignore (e.g., txt md .zip .png). Defaults to ['gitkeep'].",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="PNG",
        help="Output image format (default: PNG). Make sure to capitalize the extension and exclude the period.",
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

    args = parser.parse_args()

    output_path = setup_output_directory(args.output)
    ignore_extensions = [f".{ext.lstrip('.')}" for ext in args.ignore]
    input_files = get_absolute_paths(args.input, ignore_extensions)

    success_count = sum(1 for success in input_files if process_image(success))

    print(
        f"Processed {success_count}/{len(input_files)} images in {time.time() - start_time:.2f} seconds. "
        f"{'View results in {output_path}.' if (success_count > 0) else 'No images were processed.'}"
    )

    # Parse the size argument
    # try:
    #     width, height = map(int, args.size.split("x"))
    # except ValueError:
    #     parser.error("Size must be in WIDTHxHEIGHT format, e.g., 64x64")

    # Ensure the output directory exists
    # os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Convert the image
    # convert_image(args.input, args.output, (width, height), args.transparent_green, args.format)


if __name__ == "__main__":
    main()
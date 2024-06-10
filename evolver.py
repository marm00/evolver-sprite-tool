import argparse
import glob
import os
import time
from PIL import Image


def get_absolute_paths(input: str, ignore: list[str]) -> list[str]:
    found_paths = glob.glob(os.path.abspath(input), recursive=True)
    found_files = set()

    def include_file(file_path: str) -> None:
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        if not (ignore and any(file_path.endswith(ext) for ext in ignore)):
            found_files.add(file_path)

    for path in found_paths:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    include_file(file_path)
        elif os.path.isfile(path):
            include_file(path)
        else:
            print(f"WARNING: Unexpected behavior for {path} - expected a directory or file.")

    return found_files

def setup_output_directory(output_path: str) -> str:
    if not os.path.isdir(output_path):
        try:
            os.makedirs(output_path, exist_ok=True)
        except OSError as e:
            raise Exception(f"Incorrect format for output path: {e}")
    return os.path.abspath(output_path)

def valid_output_file(output_directory: str, file_path: str, format: str) -> str | bool:
    new_path_file = os.path.join(output_directory, os.path.basename(file_path))
    temp_file_path = f"{new_path_file}.tmp"

    try:
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(b"")
    except Exception:
        return False
    finally:
        if os.path.exists(temp_file_path) and os.path.isfile(temp_file_path):
            os.remove(temp_file_path)
            
    if format:
        file_root, _ = os.path.splitext(new_path_file)
        new_path_file = f"{file_root}.{format.lower()}"

    return new_path_file

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

def process_image(
    file_path: str, output_directory: str, format: str, size: tuple[int, int]
) -> bool:
    def skip(message):
        formatted_error = f"WARNING: Skipping {file_path} because {message}"
        print(formatted_error)
        return formatted_error
    
    new_file_path = valid_output_file(output_directory, file_path, format)
    if not new_file_path:
        return skip("A temp file could not be created. Check the path, file type and permissions.")
    error_message = ""

    try:
        with Image.open(file_path) as img:
            print(f"Processing {file_path}")
            img = img.resize(size, Image.LANCZOS)
            try:
                img.save(new_file_path, format)
            except KeyError:
                error_message = skip(f"the format type {format} is not supported.") 
            except ValueError:
                error_message = skip(
                    "the output format could not be determined from the file name."
                )
            except OSError:
                error_message = skip("the output file could not be written (it still might be created!).")

    except FileNotFoundError:
        error_message = skip("the file cannot be found.")
    except Image.UnidentifiedImageError:
        error_message = skip("the found file cannot be opened and identified, inspect the image manually.")
    except ValueError:
        error_message = skip(
            "the 'mode' is not r, or a StringIO instance is used for 'fp'."
        )
    except TypeError:
        error_message = skip("'formats' is not None, a list or a tuple.")

    return False if error_message else True


def size_type(size: str) -> tuple[int, int]:
    try:
        width, height = map(int, size.split("x"))
        return (width, height)
    except ValueError:
        raise argparse.ArgumentTypeError("Size must be in WIDTHxHEIGHT format.")


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
        help="File extensions to ignore (e.g., txt jpg .zip .png). Defaults to ['gitkeep'].",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default=None,
        help="Override the inferred output image format (e.g., PNG, JPEG, BMP).",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=size_type,
        default=(64, 64),
        help="Output image size in WIDTHxHEIGHT format (default: 64x64).",
    )
    parser.add_argument(
        "-t",
        "--transparent-green",
        action="store_true",
        help="Convert green pixels (0,255,0) to transparent.",
    )

    args = parser.parse_args()

    output_directory = setup_output_directory(args.output)
    ignore_extensions = [f".{ext.lstrip('.')}" for ext in args.ignore]
    input_files = get_absolute_paths(args.input, ignore_extensions)
    print(args.size)

    success_count = sum(
        1
        for success in input_files
        if process_image(success, output_directory, args.format, args.size)
    )

    print(
        f"Processed {success_count}/{len(input_files)} images in {time.time() - start_time:.2f} seconds. "
        f"{f"View results in {output_directory}." if (success_count > 0) else 'No images were processed.'}"

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

import argparse
import glob
import math
import os
import subprocess
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

def valid_output_file(output_directory: str, file_path: str, format: str, mask_rgb: tuple[int, int, int]) -> str | bool:
    new_path_file = os.path.join(output_directory, os.path.basename(file_path))
    file_root, file_ext = os.path.splitext(new_path_file)
    temp_file_path = f"{new_path_file}.tmp"

    try:
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(b"")
    except Exception:
        return False
    finally:
        if os.path.exists(temp_file_path) and os.path.isfile(temp_file_path):
            os.remove(temp_file_path)

    if mask_rgb and not any((format == rgba_format or file_ext[1:].upper() == rgba_format) for rgba_format in ["PNG", "TIFF", "WEBP", "GIF"]):
        format = "WEBP"
            
    if format:
        new_path_file = f"{file_root}.{format.lower()}"

    return new_path_file

def process_image(
    file_path: str, output_directory: str, format: str, size: tuple[int, int], mask: tuple[tuple[int, int, int], int], center: bool) -> bool:
    def skip(message):
        formatted_error = f"WARNING: Skipping {file_path} because {message}"
        print(formatted_error)
        return formatted_error
    
    mask_rgb, mask_threshold = mask
    new_file_path = valid_output_file(output_directory, file_path, format, mask_rgb)
    if not new_file_path:
        return skip("A temp file could not be created. Check the path, file type and permissions.")
    error_message = ""

    try:
        with Image.open(file_path) as img:
            img = img.resize(size, Image.LANCZOS)
            if mask_rgb and mask_threshold:
                img = img.convert("RGBA")
                data = img.getdata()
                new_data = []
                for item in data:
                    euclidean_distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(item[:3], mask_rgb)))
                    if euclidean_distance < mask_threshold:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                img.putdata(new_data)
                
                if center:
                    bbox = img.getbbox()
                    if bbox:
                        cropped_img = img.crop(bbox)
                        canvas = Image.new("RGBA", size, (255, 255, 255, 0))
                        x = (size[0] - cropped_img.width) // 2
                        y = (size[1] - cropped_img.height) // 2
                        canvas.paste(cropped_img, (x, y))
                        img = canvas

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
    
def mask_type(mask: str) -> tuple[tuple[int, int, int], int]:
    try:
        red, green, blue, threshold = map(int, mask.split(","))
        return ((red, green, blue), threshold)
    except ValueError:
        raise argparse.ArgumentTypeError("Mask must be in RED,GREEN,BLUE,THRESHOLD format.")


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
        "-m",
        "--mask",
        type=mask_type,
        default=((0, 255, 0), 100),
        help="Transparentize pixels matching this mask (RED,GREEN,BLUE,THRESHOLD) (default: 0,255,0,100).",
    )
    parser.add_argument(
        "-c",
        "--center",
        type=int,
        choices=[0, 1],
        default=1,
        help="Center the image, 0 or 1 (default), ensure that --mask matches the background." 
    )
    parser.add_argument(
        "-p",
        "--pack",
        type=int,
        choices=[0, 1],
        default=1,
        help="Use TexturePacker to convert output into a single sprite sheet, 0 or 1 (default)."
    )

    args = parser.parse_args()

    output_directory = setup_output_directory(args.output)
    ignore_extensions = [f".{ext.lstrip('.')}" for ext in args.ignore]
    input_files = get_absolute_paths(args.input, ignore_extensions)

    success_count = sum(
        1
        for success in input_files
        if process_image(success, output_directory, args.format, args.size, args.mask, args.center)
    )

    print(
        f"Processed {success_count}/{len(input_files)} images in {time.time() - start_time:.2f} seconds. "
        f"{f"View results in {output_directory}." if (success_count > 0) else 'No images were processed.'}"
    )

    if args.pack:
        cmd = f"TexturePacker {output_directory} --sheet {time.time()} --texture-format webp --format json"
        # subprocess.run(cmd)

if __name__ == "__main__":
    main()

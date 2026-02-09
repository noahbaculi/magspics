# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pillow",
# ]
# ///

from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

from PIL import Image


# Responsive image widths for srcset generation.
#
# These widths provide good coverage across devices and pixel densities:
#   - 400w  : Small thumbnails, quarter-width images, low-DPI fallback
#   - 800w  : Half-width on tablets, full-width on mobile at 2x DPR
#   - 1500w : Full-width on ~1440px laptops at 2x DPR
#   - 2200w : Full-width on larger displays at 2x DPR
#
# The `sizes` attribute tells the browser the display size, and it
# picks the smallest srcset image that still looks sharp at that size
# multiplied by the device's pixel ratio.
DEFAULT_IMAGE_WIDTHS = sorted([400, 800, 1500, 2200])

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic"}


def round_down_to_nearest(value: int, multiple: int) -> int:
    """Round value down to the nearest multiple."""
    return (value // multiple) * multiple


def convert_img(
    file_path: Path, widths: list[int], exclude: list[str], include: list[str]
) -> str | None:
    """
    Generate resized WebP images for responsive srcset usage.

    Returns the file path string if conversion fails, None on success.
    """
    file_path_str = str(file_path)

    if include and not any(inc in file_path_str for inc in include):
        print(f"\tSkipping not included {file_path} with include list = {include}.")
        return None

    if any(exc in file_path_str for exc in exclude):
        print(f"\tSkipping excluded {file_path} with exclude list = {exclude}.")
        return None

    try:
        with Image.open(file_path) as img:
            if file_path.suffix.lower() == ".png":
                img = img.convert("RGBA")

            original_width, original_height = img.size

            num_existing_files = 0
            num_generated_files = 0

            for width in widths:
                is_final_width = width > original_width

                if is_final_width:
                    width = round_down_to_nearest(original_width, 100)

                output_path = file_path.with_name(f"{file_path.stem}_{width}_w.webp")

                if not output_path.exists():
                    size_ratio = width / original_width
                    new_size = (
                        round(original_width * size_ratio),
                        round(original_height * size_ratio),
                    )
                    new_img = img.resize(new_size, Image.Resampling.LANCZOS)
                    new_img.save(output_path, "webp")
                    num_generated_files += 1
                else:
                    num_existing_files += 1

                if is_final_width:
                    break

        if num_generated_files != 0:
            print(
                f"\tGenerated {num_generated_files} images and skipped {num_existing_files} images for '{file_path}'."
            )
        return None

    except Exception as e:
        print(f"\tFailed to process {file_path}: {e}")
        return file_path_str


def convert_folder(
    base_path: str,
    widths: list[int],
    exclude: list[str] | None = None,
    include: list[str] | None = None,
) -> None:
    """Convert all images in a directory to responsive WebP sizes."""

    base = Path(base_path)

    if not base.is_dir():
        raise ValueError(f"{base_path} is not a valid directory")

    exclude = exclude or []
    include = include or []

    image_files = [
        root / f
        for root, _, files in base.walk()
        for f in files
        if Path(f).suffix.lower() in IMAGE_EXTENSIONS and "_w." not in f
    ]

    print(f"Generating scaled images for {len(image_files)} files in '{base_path}'...")

    worker = partial(convert_img, widths=widths, exclude=exclude, include=include)
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(worker, image_files))

    invalid_files = {r for r in results if r is not None}
    if invalid_files:
        raise ValueError("Failed to convert:\n\t" + "\n\t".join(invalid_files))


if __name__ == "__main__":
    convert_folder("images/portfolio", DEFAULT_IMAGE_WIDTHS)
    convert_folder(
        "images/icons",
        [100],
        include=["instagram", "twitter"],
    )
    convert_folder("images/cover", [600, 1000, 2000])

    print("Done.")

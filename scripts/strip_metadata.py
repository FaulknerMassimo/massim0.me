"""
strip_metadata.py

Usage: python scripts/strip_metadata.py <path> [--inplace]

Examples:
    python scripts/strip_metadata.py images/cats/eclipse.jpg
    python scripts/strip_metadata.py images/racing/lap.mov
    python scripts/strip_metadata.py images/cats/
    python scripts/strip_metadata.py images/cats/ images/memes/ --inplace
"""

import sys
import shutil
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageOps

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif", ".webp"}
VIDEO_EXTENSIONS = {".mov"}
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

def strip_metadata(src_path: Path, inplace: bool = False) -> Path:
    if src_path.suffix.lower() in VIDEO_EXTENSIONS:
        return strip_video_metadata(src_path, inplace=inplace)

    with Image.open(src_path) as img:
        img = ImageOps.exif_transpose(img)
        clean = Image.new(img.mode, img.size)
        clean.putdata(list(img.getdata()))

    if inplace:
        dest_path = src_path
    else:
        dest_path = src_path.with_stem(src_path.stem + "_clean")

    clean.save(dest_path)
    return dest_path

def strip_video_metadata(src_path: Path, inplace: bool = False) -> Path:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to strip metadata from .mov files.")

    if inplace:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=src_path.suffix,
            dir=src_path.parent,
        ) as tmp:
            output_path = Path(tmp.name)
        dest_path = src_path
    else:
        output_path = src_path.with_stem(src_path.stem + "_clean")
        dest_path = output_path

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(src_path),
        "-map_metadata",
        "-1",
        "-c",
        "copy",
        str(output_path),
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "ffmpeg failed.")

        if inplace:
            output_path.replace(src_path)
        return dest_path
    except Exception:
        if inplace and output_path.exists():
            output_path.unlink(missing_ok=True)
        raise

def process(target: str, inplace: bool) -> None:
    target_path = Path(target)

    if target_path.is_file():
        paths = [target_path]
    elif target_path.is_dir():
        paths = [
            p for p in target_path.iterdir()
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
        if not paths:
            print(f"No supported media files found in '{target_path}'.")
            return
    else:
        print(f"Error: '{target}' is not a valid file or directory.")
        sys.exit(1)

    for src in paths:
        try:
            dest = strip_metadata(src, inplace=inplace)
            label = "overwritten" if inplace else f"saved as '{dest.name}'"
            print(f"  [OK] {src.name} -> {label}")
        except Exception as exc:
            print(f"  [FAIL] {src.name}: {exc}")

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    inplace = "--inplace" in args
    paths = [a for a in args if not a.startswith("--")]

    if not paths:
        print("Error: provide at least one file or directory path.")
        sys.exit(1)

    for path in paths:
        process(path, inplace)

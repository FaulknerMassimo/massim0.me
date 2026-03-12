import sys
import os
from pathlib import Path
from PIL import Image, ImageOps

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif", ".webp"}

def strip_metadata(src_path: Path, inplace: bool = False) -> Path:
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
            print(f"No supported image files found in '{target_path}'.")
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

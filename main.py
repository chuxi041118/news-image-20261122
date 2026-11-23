#!/usr/bin/env python3
"""Entrypoint for news-image-20261122. Stdlib only, no network.

Copies the pre-drawn entry.png (built by gen_image.py) to
$MAKEFUN_OUTPUT_DIR/entry.png, creating the directory if needed.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"copied {src} -> {dst}")


if __name__ == "__main__":
    sys.exit(main())

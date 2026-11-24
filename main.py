#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — entrypoint (Python 3.13, stdlib only).

The entry is the image beside this file: a chat-log meme composed by
compose.py (AI-generated rogue-robot illustration on top, every word
rendered sharp with PIL + DejaVu). This program copies it, byte for byte,
to the grader's output directory as entry.png, after checking it meets
the gate: a whole PNG, at most 1 MiB, at most 1024 by 1024 pixels.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def png_dimensions(path):
    """Read width/height from a PNG's IHDR chunk; raise if not a PNG."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk where expected")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")

    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the "
                         f"{MAX_BYTES} byte gate")
    width, height = png_dimensions(SOURCE)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"entry.png is {width}x{height}, over the "
                         f"{MAX_SIDE}x{MAX_SIDE} gate")

    shutil.copyfile(SOURCE, dest)
    copied = os.path.getsize(dest)
    if copied != size:
        raise ValueError(f"copy came out {copied} bytes, expected {size}")
    print(f"wrote {dest}  {width}x{height}  {size} bytes")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

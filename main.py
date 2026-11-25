#!/usr/bin/env python3
"""Entrypoint for the news-image-20261124 entry.

The grading sandbox runs this file with the standard library only, so it
does no drawing: the finished page was drawn at build time by
build_image.py and is committed as entry.png. This program simply copies
those exact bytes to /output/entry.png, identically on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(OUT_DIR, "entry.png"))


if __name__ == "__main__":
    main()

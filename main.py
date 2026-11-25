#!/usr/bin/env python3
"""one-day-press: one-day world news image for make.fun news-image-20261125.

The entry program. It hands in the pre-rendered entry.png — drawn by
render_news.py in this repo from public news digests of Wednesday 25
November 2026 — by copying it to the output directory. Standard library
only; deterministic: both runs write identical bytes.

Run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = output_dir()
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(os.path.join(here, "entry.png"), os.path.join(out, "entry.png"))
    print("wrote entry.png")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf==1.28.2"]
# ///
"""Render light/dark PDF sheets as PNG previews for the public README."""

from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/previews"


def build():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for sheet in ("omarchy-on-mac-keybindings", "herdr-keybindings-omarchy"):
        for theme in ("", "-dark"):
            name = sheet + theme
            with pymupdf.open(ROOT / "output/pdf" / f"{name}.pdf") as document:
                if len(document) != 1:
                    raise ValueError(f"{name}: README preview expects a one-page sheet")
                image = document[0].get_pixmap(matrix=pymupdf.Matrix(1.8, 1.8), alpha=False)
                destination = OUTPUT / f"{name}.png"
                image.save(destination)
                print(destination)


if __name__ == "__main__":
    build()

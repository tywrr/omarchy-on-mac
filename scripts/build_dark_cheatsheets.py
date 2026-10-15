#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdf==6.20.1"]
# ///
"""Create dark PDFs from both light sheets, preserving vector art and text.

Run after rebuilding the macOS sheet: uv run scripts/build_dark_cheatsheets.py.
The Herdr light PDF is the original reference supplied from Documents/cheat sheets.
"""

from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, FloatObject, NameObject

ROOT = Path(__file__).resolve().parents[1]
PDFS = ROOT / "output/pdf"

# Both original sheets share this light palette. Pastel accents keep dark text
# readable inside filled keycaps; the remaining labels use light text.
PALETTE = {
    "FFFFFF": "181923",  # Page, unfilled keycaps, and text on accent fills.
    "15140F": "E8E6E0",  # Main text.
    "55534A": "B5B7C5",  # Supporting text.
    "CBC5B6": "4D5065",  # Keycap borders and rules.
    "ECE9E1": "242633",  # Background grid.
    "FAF9F6": "222430",  # Card surfaces.
    "F5F3EE": "2A2C3A",  # Footer and secondary surfaces.
    "8839EF": "C4A1FF",  # Purple.
    "2AA198": "7DD7CC",  # Teal.
    "397E4D": "A6D69A",  # Green.
    "B8860B": "F2CA7A",  # Gold.
    "B74343": "F0939B",  # Red.
}


def recolor(source):
    reader = PdfReader(source)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    for page in writer.pages:
        for reference in page.get("/Resources", {}).get("/XObject", {}).values():
            image = reference.get_object()
            if (
                image.get("/Subtype") == "/Image"
                and image.get("/ColorSpace") == "/DeviceGray"
                and image.get("/BitsPerComponent") == 8
                and image.get("/SMask")
                and "/Decode" not in image
                and set(image.get_data()) == {0}
            ):
                # The Herdr logo is solid black with a separate alpha mask.
                # Decode it as white, preserving its original edges and mask.
                image[NameObject("/Decode")] = ArrayObject([FloatObject(1), FloatObject(0)])
            else:
                raise ValueError(f"{source.name}: nested artwork needs a palette review")
        stream = page.get_contents()
        operations = []
        for operands, operator in stream.operations:
            if operator in (b"rg", b"RG"):
                original = "".join(f"{round(float(value) * 255):02X}" for value in operands)
                if original not in PALETTE:
                    raise ValueError(f"{source.name}: unmapped color #{original}")
                replacement = PALETTE[original]
                operands = [
                    FloatObject(int(replacement[i:i + 2], 16) / 255)
                    for i in (0, 2, 4)
                ]
            elif operator in (b"g", b"G", b"k", b"K", b"cs", b"CS", b"scn", b"SCN"):
                raise ValueError(f"{source.name}: unsupported color operator {operator!r}")
            operations.append((operands, operator))
        stream.operations = operations
        page.replace_contents(stream)
        page.compress_content_streams()

    writer.add_metadata({"/Title": f"{reader.metadata.title} - Dark"})
    output = source.with_stem(source.stem + "-dark")
    with output.open("wb") as target:
        writer.write(target)

    verified = PdfReader(output)
    if len(reader.pages) != len(verified.pages):
        raise ValueError(f"{output.name}: page count changed")
    for original, dark in zip(reader.pages, verified.pages):
        if original.extract_text() != dark.extract_text() or original.mediabox != dark.mediabox:
            raise ValueError(f"{output.name}: text or page size changed")
    print(output)


if __name__ == "__main__":
    for filename in ("omarchy-on-mac-keybindings.pdf", "herdr-keybindings-omarchy.pdf"):
        recolor(PDFS / filename)

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["reportlab==5.0.1"]
# ///
"""Build the one-page wall sheet: uv run scripts/build_cheatsheet.py.

Uses the typography, landscape grid, and card palette of the local Herdr sheet.
Checks that every configured Fn chord is represented before creating the PDF.
"""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/omarchy-on-mac-keybindings.pdf"
INK, MUTED = HexColor("#15140F"), HexColor("#55534A")
BORDER, GRID = HexColor("#CBC5B6"), HexColor("#ECE9E1")
SURFACE, WHITE = HexColor("#FAF9F6"), HexColor("#FFFFFF")
PURPLE, TEAL = HexColor("#8839EF"), HexColor("#2AA198")
GREEN, GOLD, RED = map(HexColor, ("#397E4D", "#B8860B", "#B74343"))
DISPLAY, LABEL, SYMBOL, MONO = (
    "Archivo-SemiBold", "Inter-Regular", "Inter-SemiBold", "JetBrainsMono-Regular"
)

# The Fn modifier is supplied by the banner for every displayed chord.
CARDS = [
    ("TERMINAL + TOOLS", PURPLE, [
        ("RET", "New Ghostty window", "fn - return"),
        ("⌃ RET", "Herdr / new terminal", "fn + ctrl - return"),
        ("⇧ N", "Neovim / new terminal", "fn + shift - n"),
        ("⌃ Q", "Calculator", "fn + ctrl - q"),
    ], "HERDR PREFIX: CONTROL + SPACE"),
    ("DAILY APPS", TEAL, [
        ("⇧ C", "Apple Calendar", "fn + shift - c"),
        ("⇧ E", "Apple Mail", "fn + shift - e"),
        ("⇧ /", "1Password", "fn + shift - 0x2c"),
        ("⌃ V", "Clipboard history", "fn + ctrl - v"),
    ], "CLIPBOARD: PRESS AGAIN TO CLOSE"),
    ("BROWSER + FILES", GREEN, [
        ("⇧ RET", "Google Chrome", "fn + shift - return"),
        ("⇧⌥ B", "New incognito window", "fn + shift + alt - b"),
        ("⇧ F", "New Finder window", "fn + shift - f"),
        ("⌃ S", "Share / LocalSend", "fn + ctrl - s"),
    ], "FINDER: A NEW WINDOW EACH PRESS"),
    ("SYSTEM", GOLD, [
        ("W", "Quit app (Command+Q)", "fn - w"),
        ("ESC", "Apple system menu", "fn - escape"),
        ("⌃ L", "Lock Screen", "fn + ctrl - l"),
        ("⌃ E", "Emoji & Symbols", "fn + ctrl - e"),
    ], "CAPS LOCK IS REMAPPED TO ESCAPE"),
]
HIGHLIGHTS = [
    ("1-5", "SWITCH DESKTOP", "NATIVE MISSION CONTROL", PURPLE),
    ("⇧ 1-5", "MOVE + FOLLOW", "WHICHSPACE MOVES THE WINDOW", GOLD),
    ("⌥ F", "FILL / RESTORE", "TOGGLE PREVIOUS WINDOW SIZE", TEAL),
    ("F", "FULL SCREEN", "TOGGLE NATIVE FULL SCREEN", GREEN),
    ("SPACE", "SPOTLIGHT", "SEARCH APPS AND MORE", RED),
]


def verify_coverage():
    documented = {row[2] for _, _, rows, _ in CARDS for row in rows}
    documented |= {f"fn - {n}" for n in range(1, 6)}
    documented |= {f"fn + shift - {n}" for n in range(1, 6)}
    documented |= {"fn + alt - f", "fn - f", "fn - space"}
    configured = set()
    for line in (ROOT / "skhd/skhdrc").read_text().splitlines():
        if line.startswith("fn "):
            chord = line.split(" | ")[0].split(" : ")[0].strip()
            # Apple keyboards may produce keypad Enter for Fn+Return.
            configured.add(chord.replace("0x4c", "return"))
    if configured != documented:
        raise ValueError(f"Cheatsheet/config mismatch: {configured ^ documented}")


def runs(text, font, size):
    for char in text:
        modifier = char in "⌃⌥⇧⌘"
        scale = 1.45 if char == "⌃" else 1
        offset = size * (0.73 / 2 - (0.363 + 0.734) / 2 * scale) if char == "⌃" else 0
        actual_font = SYMBOL if modifier else font
        actual_size = size * scale
        yield char, actual_font, actual_size, offset, pdfmetrics.stringWidth(char, actual_font, actual_size)


def width(text, font, size):
    return sum(run[4] for run in runs(text, font, size))


def text(c, x, y, value, font=LABEL, size=10, color=INK, align="left"):
    if align == "center":
        x -= width(value, font, size) / 2
    elif align == "right":
        x -= width(value, font, size)
    c.setFillColor(color)
    for char, actual_font, actual_size, offset, advance in runs(value, font, size):
        c.setFont(actual_font, actual_size)
        c.drawString(x, y + offset, char)
        x += advance


def keycap(c, x, y, value, color=INK, filled=False, size=13, height=28, fixed_width=None):
    cap_width = fixed_width or max(25, width(value, MONO, size) + 13)
    c.setStrokeColor(color if filled else BORDER)
    c.setFillColor(color if filled else WHITE)
    c.setLineWidth(1)
    c.roundRect(x, y, cap_width, height, 2.5, stroke=1, fill=1)
    text(c, x + cap_width / 2, y + (height - .73 * size) / 2, value,
         MONO, size, WHITE if filled else INK, "center")
    return cap_width


def build():
    verify_coverage()
    for font in (DISPLAY, LABEL, SYMBOL, MONO):
        pdfmetrics.registerFont(TTFont(font, str(ROOT / "assets/fonts" / f"{font}.ttf")))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(792, 612), invariant=1)
    c.setTitle("Omarchy on Mac - Keyboard Wall Sheet")
    c.setAuthor("Omarchy on Mac")
    c.setFillColor(WHITE)
    c.rect(0, 0, 792, 612, stroke=0, fill=1)
    c.setStrokeColor(GRID)
    c.setLineWidth(.3)
    for x in range(24, 769, 72):
        c.line(x, 18, x, 594)
    for y in range(18, 595, 72):
        c.line(18, y, 774, y)

    text(c, 24, 574, "omarchy / mac", DISPLAY, 19)
    c.setStrokeColor(BORDER)
    c.line(177, 570, 177, 592)
    text(c, 191, 574, "KEYBOARD WALL SHEET", DISPLAY, 19)
    text(c, 768, 584, "FN / GLOBE AS SUPER", MONO, 7.5, MUTED, "right")
    text(c, 768, 572, "⌃ CONTROL  ⌥ OPTION  ⇧ SHIFT", MONO, 7.2, MUTED, "right")

    c.setFillColor(WHITE)
    c.setStrokeColor(INK)
    c.setLineWidth(1.2)
    c.rect(24, 500, 744, 56, stroke=1, fill=1)
    text(c, 42, 530, "> SUPER", MONO, 8, PURPLE)
    keycap(c, 107, 511, "Fn", PURPLE, True, 21, 34, 57)
    text(c, 184, 530, "HOLD FN / GLOBE, ADD THE KEYS BELOW", DISPLAY, 13.5)
    text(c, 184, 513, "Every card includes Super. Alt means Option. No prefix sequence.", MONO, 7.4, MUTED)
    text(c, 695, 525, "ACTIONS", MONO, 7.5, MUTED, "right")
    keycap(c, 708, 511, "21", PURPLE, True, 19, 34, 43)

    keycap(c, 24, 455, "5", PURPLE, True, 15, 28, 25)
    text(c, 60, 463, "DESKTOP + WINDOW ACTIONS", DISPLAY, 13.5)
    text(c, 768, 464, "NATIVE SPACES / NATIVE WINDOWS", MONO, 7.4, MUTED, "right")
    gap = 14
    card_width = (744 - 4 * gap) / 5
    for i, (chord, title, note, accent) in enumerate(HIGHLIGHTS):
        x = 24 + i * (card_width + gap)
        c.setStrokeColor(accent)
        c.setFillColor(SURFACE)
        c.setLineWidth(.9)
        c.roundRect(x, 337, card_width, 112, 4, stroke=1, fill=1)
        cap_width = max(41, width(chord, MONO, 20) + 18)
        keycap(c, x + (card_width - cap_width) / 2, 391, chord, accent, True, 20, 34, cap_width)
        text(c, x + card_width / 2, 365, title, DISPLAY, 11, INK, "center")
        text(c, x + card_width / 2, 348, note, MONO, 5.9, MUTED, "center")

    keycap(c, 24, 304, "Fn", PURPLE, True, 13, 26, 42)
    text(c, 78, 312, "LAUNCH APPS + SYSTEM ACTIONS", DISPLAY, 13.5)
    text(c, 768, 313, "HOLD FN WITH EVERY CHORD", MONO, 7.4, MUTED, "right")
    gap = 16
    card_width = (744 - 3 * gap) / 4
    for i, (title, accent, rows, note) in enumerate(CARDS):
        x = 24 + i * (card_width + gap)
        c.setStrokeColor(accent)
        c.setFillColor(SURFACE)
        c.setLineWidth(.9)
        c.roundRect(x, 91, card_width, 201, 4, stroke=1, fill=1)
        text(c, x + 12, 267, title, DISPLAY, 12)
        c.setStrokeColor(BORDER)
        c.setLineWidth(.5)
        c.line(x + 12, 255, x + card_width - 12, 255)
        for j, (chord, label, _) in enumerate(rows):
            y = 218 - 31 * j
            keycap(c, x + 11, y, chord, size=11, height=25, fixed_width=51)
            text(c, x + 70, y + 8, label, LABEL, 8.1)
        text(c, x + 11, 103, note, MONO, 5.9, MUTED)

    c.setStrokeColor(BORDER)
    c.setFillColor(HexColor("#F5F3EE"))
    c.roundRect(24, 39, 744, 45, 3, stroke=1, fill=1)
    text(c, 37, 70, "NATIVE MAC DESKTOPS + WHICHSPACE + SKHD.ZIG", MONO, 7.1, MUTED)
    text(c, 37, 58, "3-finger swipe left / right: switch desktops on both Omarchy and macOS.", LABEL, 8.1)
    text(c, 37, 47, "Fill restores the previous size. Full screen uses its own Space. Fn+W quits the whole app.", LABEL, 7.8)
    text(c, 755, 70, "⌘W: CLOSE ONE WINDOW", MONO, 7.1, MUTED, "right")
    text(c, 755, 47, "ESC: DISMISS THE APPLE MENU", MONO, 6.4, MUTED, "right")
    text(c, 24, 20, "github.com/tywrr/omarchy-on-mac", MONO, 7, MUTED)
    text(c, 396, 20, "LIVE CONFIG: ~/.config/skhd/skhdrc", MONO, 6.6, MUTED, "center")
    text(c, 768, 20, "2026-10-14  /  macOS 26", MONO, 7, MUTED, "right")
    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()

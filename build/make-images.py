#!/usr/bin/env python3
"""The og-image and the PNG favicons. Family tokens; the mark is the rising line.

Run: /opt/homebrew/bin/python3 build/make-images.py
Georgia stands in for Newsreader here: the web page loads the real face, and a PNG
only needs a warm serif at this size. Nothing is fetched.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PAPER, INK, MUTED, GOLD = "#fdfaf7", "#1a1a1a", "#6b6560", "#c8a96e"
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"


def rising_line(draw, box, width):
    """The favicon mark at any size: one line climbing, a gold dot where it lands."""
    x0, y0, x1, y1 = box
    pts = [(x0, y1), (x0 + (x1 - x0) * 0.33, y1 - (y1 - y0) * 0.30),
           (x0 + (x1 - x0) * 0.66, y1 - (y1 - y0) * 0.62), (x1, y0)]
    draw.line(pts, fill=INK, width=width, joint="curve")
    r = max(3, width)
    draw.ellipse((x1 - r, y0 - r, x1 + r, y0 + r), fill=GOLD)


# og-image: 1200x630, the wordmark and the promise, nothing else.
og = Image.new("RGB", (1200, 630), PAPER)
d = ImageDraw.Draw(og)
d.text((80, 150), "contrashittification", font=ImageFont.truetype(SERIF, 76), fill=INK)
d.text((84, 258), "the good news collection", font=ImageFont.truetype(SANS, 28), fill=MUTED)
d.text((80, 340), "Things that got better,", font=ImageFont.truetype(SERIF, 40), fill=INK)
d.text((80, 396), "and things that stayed good.", font=ImageFont.truetype(SERIF, 40), fill=INK)
rising_line(d, (840, 150, 1110, 270), 6)
og.save(ROOT / "og-image.png")

# Favicons from one drawing, downsampled so the line survives.
for size, name in ((32, "favicon-32x32.png"), (180, "apple-touch-icon.png")):
    big = Image.new("RGB", (size * 8, size * 8), PAPER)
    rising_line(ImageDraw.Draw(big), (size, size * 7, size * 7, size), max(4, size // 2))
    big.resize((size, size), Image.LANCZOS).save(ROOT / name)

print("og-image.png, favicon-32x32.png, apple-touch-icon.png written")

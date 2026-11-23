#!/usr/bin/env python3
"""Draw the news-image-20261122 entry: one 1024x1024 poster summing up
Sunday 22 November 2026 world news. Pillow only, no network."""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NAVY = (13, 27, 46)
PANEL = (19, 38, 62)
GOLD = (212, 175, 55)
WHITE = (245, 244, 238)
MUTED = (176, 190, 205)
RULE = (212, 175, 55)
ACCENTS = [(212, 175, 55), (86, 178, 214), (214, 110, 86), (120, 190, 130), (186, 130, 205)]

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


MASTHEAD = font("DejaVuSerif-Bold.ttf", 58)
DATE_FONT = font("DejaVuSans-Bold.ttf", 30)
HEAD_FONT = font("DejaVuSans-Bold.ttf", 31)
SUB_FONT = font("DejaVuSans.ttf", 23)
FOOT_FONT = font("DejaVuSans.ttf", 19)
NUM_FONT = font("DejaVuSans-Bold.ttf", 34)

STORIES = [
    ("CLIMATE TALKS COLLAPSE",
     "COP31 in Antalya ends with no deal as nations split over fossil fuels."),
    ("MYANMAR GUILTY OF ROHINGYA GENOCIDE",
     "World Court rules the 2017 crackdown was genocide, a first for a state."),
    ("RUSSIAN WARSHIP SUNK OFF LIBYA",
     "Suspected Ukrainian sea drones hit a vessel at Benghazi; Kyiv claims it."),
    ("IRAN-GULF TENSIONS FLARE",
     "Tankers struck near Hormuz; Trump warns Tehran over the US blockade."),
    ("MEXICO CAPTURES 'EL CHAPO ISIDRO'",
     "Cartel boss seized in a Sinaloa raid; 11 killed, including four soldiers."),
]


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width using the font's metrics."""
    lines = []
    for raw in text.split("\n"):
        words = raw.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=MASTHEAD)
    d.text(((W - tw) / 2, 34), title, font=MASTHEAD, fill=WHITE)
    d.rectangle([64, 118, W - 64, 121], fill=RULE)
    date = "SUNDAY  22  NOVEMBER  2026"
    dw = d.textlength(date, font=DATE_FONT)
    d.text(((W - dw) / 2, 138), date, font=DATE_FONT, fill=GOLD)
    d.rectangle([64, 186, W - 64, 189], fill=RULE)

    # Five story rows
    top = 210
    row_h = 146
    for i, (head, sub) in enumerate(STORIES):
        y = top + i * row_h
        accent = ACCENTS[i]
        # panel
        d.rounded_rectangle([48, y, W - 48, y + row_h - 18], radius=14, fill=PANEL)
        # number badge
        cx, cy, r = 108, y + (row_h - 18) // 2, 34
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
        num = str(i + 1)
        nw = d.textlength(num, font=NUM_FONT)
        d.text((cx - nw / 2, cy - 24), num, font=NUM_FONT, fill=NAVY)
        # headline + subline
        tx = 168
        max_w = W - 48 - tx - 28
        head_lines = wrap(d, head, HEAD_FONT, max_w)
        hy = y + 16
        for line in head_lines[:2]:
            d.text((tx, hy), line, font=HEAD_FONT, fill=WHITE)
            hy += 40
        sub_lines = wrap(d, sub, SUB_FONT, max_w)
        sy = hy + 4
        for line in sub_lines[:2]:
            d.text((tx, sy), line, font=SUB_FONT, fill=MUTED)
            sy += 30

    # Footer
    foot = "Five stories that defined the day  |  Sources: AP, Reuters, AFP, Al Jazeera"
    fw = d.textlength(foot, font=FOOT_FONT)
    d.text(((W - fw) / 2, H - 44), foot, font=FOOT_FONT, fill=MUTED)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()

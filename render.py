#!/usr/bin/env python3
"""Build-time renderer: draws the 26 Nov 2026 broadsheet with PIL + OFL fonts.

Writes page.png (1024x1024). Run: python3 render.py
Fonts are system Noto (OFL): Noto Serif Display Black for the masthead/date,
Noto Serif Bold for headlines, Noto Serif for body, Noto Serif Italic for
the subhead, Noto Sans Condensed for labels/tags.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C

W, H = 1024, 1024
MX = 18  # side margin
CREAM = (247, 242, 231)
PAPER2 = (238, 231, 214)
INK = (24, 24, 24)
RED = (176, 30, 36)
BLUE = (31, 78, 121)
SEA = (168, 196, 214)
LAND = (226, 214, 182)
GREY = (110, 105, 95)
GOLD = (176, 141, 42)
DARK = (38, 52, 74)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def F(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_BLACK = lambda s: F("NotoSerifDisplay-Black.ttf", s)
F_SERIF_B = lambda s: F("NotoSerif-Bold.ttf", s)
F_SERIF = lambda s: F("NotoSerif-Regular.ttf", s)
F_SERIF_I = lambda s: F("NotoSerif-Italic.ttf", s)
F_COND_B = lambda s: F("NotoSans-CondensedBold.ttf", s)
F_COND = lambda s: F("NotoSans-Condensed.ttf", s)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines (never splits a word)."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, font, color, leading=None, align="l",
               box_w=None):
    if leading is None:
        leading = font.size + 2
    for line in lines:
        lx = x
        if align == "c":
            lx = x + (box_w - draw.textlength(line, font=font)) // 2
        elif align == "r":
            lx = x + box_w - draw.textlength(line, font=font)
        draw.text((lx, y), line, font=font, fill=color)
        y += leading
    return y


def chip(draw, x, y, text, font):
    """Red figure chip, top-right anchored at (x, y) as its right edge."""
    w = int(draw.textlength(text, font=font)) + 12
    h = font.size + 8
    draw.rounded_rectangle([x - w, y, x, y + h], radius=3, fill=RED)
    draw.text((x - w + 6, y + 4), text, font=font, fill=CREAM)
    return w


# ---------------- illustrations (code-drawn, literal) ----------------

def ill_strait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.polygon([(x, y), (x + w * 0.42, y), (x + w * 0.52, y + h * 0.45),
               (x + w * 0.46, y + h), (x, y + h)], fill=LAND)
    d.polygon([(x + w, y), (x + w * 0.62, y), (x + w * 0.55, y + h * 0.4),
               (x + w * 0.60, y + h), (x + w, y + h)], fill=LAND)
    for sx in (0.30, 0.66):
        px, py = x + int(w * sx), y + int(h * 0.62)
        d.rectangle([px - 14, py - 6, px + 14, py + 2], fill=INK)
        d.rectangle([px - 4, py - 12, px + 2, py - 6], fill=INK)
    for mx, my in ((0.48, 0.55), (0.55, 0.72), (0.44, 0.80)):
        d.ellipse([x + w * mx - 3, y + h * my - 3, x + w * mx + 3,
                   y + h * my + 3], fill=RED)
    d.polygon([(x + w * 0.30, y + h * 0.55), (x + w * 0.26, y + h * 0.38),
               (x + w * 0.34, y + h * 0.38)], fill=(232, 110, 30))


def ill_night(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARK)
    for i, bh in enumerate((0.55, 0.75, 0.45, 0.65, 0.5)):
        bx = x + int(w * (0.06 + i * 0.19))
        d.rectangle([bx, y + h * (1 - bh), bx + int(w * 0.15),
                     y + h], fill=(12, 12, 18))
        for wy in range(3):
            d.rectangle([bx + 3, y + h * (1 - bh) + 6 + wy * 12, bx + 8,
                         y + h * (1 - bh) + 11 + wy * 12], fill=(240, 200, 90))
    cx, cy = x + int(w * 0.78), y + int(h * 0.30)
    for dx, dy in ((0, -14), (0, 14), (-14, 0), (14, 0), (-10, -10),
                   (10, -10), (-10, 10), (10, 10)):
        d.line([cx, cy, cx + dx, cy + dy], fill=(240, 140, 40), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(250, 180, 60))


def ill_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    d.polygon([(x, y + h), (x + int(w * 0.30), y + int(h * 0.55)),
               (x + int(w * 0.42), y + int(h * 0.62)),
               (x + int(w * 0.55), y + h)], fill=LAND)
    cx, cy = x + int(w * 0.62), y + int(h * 0.48)
    for r in (8, 16, 24, 32):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=BLUE, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for i in range(6):
        rx = x + int(w * (0.12 + i * 0.13))
        d.line([rx, y + int(h * 0.14), rx - 5, y + int(h * 0.30)],
               fill=BLUE, width=2)


def ill_congo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    d.polygon([(x + w * 0.30, y + h * 0.12), (x + w * 0.62, y + h * 0.10),
               (x + w * 0.78, y + h * 0.35), (x + w * 0.70, y + h * 0.70),
               (x + w * 0.55, y + h * 0.92), (x + w * 0.32, y + h * 0.85),
               (x + w * 0.20, y + h * 0.55), (x + w * 0.22, y + h * 0.30)],
              fill=LAND, outline=INK)
    for px, py, r in ((0.45, 0.35, 7), (0.58, 0.55, 9), (0.40, 0.62, 6),
                      (0.62, 0.30, 5), (0.50, 0.78, 5)):
        d.ellipse([x + w * px - r, y + h * py - r, x + w * px + r,
                   y + h * py + r], fill=RED)


def ill_bank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    for bx in (0.12, 0.58):
        px = x + int(w * bx)
        d.polygon([(px, y + h * 0.18), (px + int(w * 0.28), y + h * 0.18),
                   (px + int(w * 0.14), y + h * 0.05)], fill=INK)
        for i in range(3):
            cx0 = px + int(w * (0.03 + i * 0.09))
            d.rectangle([cx0, y + h * 0.22, cx0 + 5, y + h * 0.82], fill=INK)
        d.rectangle([px - 3, y + h * 0.82, px + int(w * 0.28) + 3,
                     y + h * 0.88], fill=INK)
    d.line([x + int(w * 0.44), y + int(h * 0.45), x + int(w * 0.56),
            y + int(h * 0.45)], fill=RED, width=3)
    d.polygon([(x + int(w * 0.56), y + int(h * 0.45)),
               (x + int(w * 0.50), y + int(h * 0.38)),
               (x + int(w * 0.50), y + int(h * 0.52))], fill=RED)


def ill_bars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    vals = (0.25, 0.35, 0.30, 0.55, 0.48, 0.72, 0.88)
    bw = w / (len(vals) + 1)
    for i, v in enumerate(vals):
        bx = x + int(bw * (i + 0.6))
        d.rectangle([bx, y + h - 8 - int(h * v * 0.8), bx + int(bw * 0.7),
                     y + h - 8], fill=BLUE if i < 6 else RED)
    d.line([x + 6, y + h - 8, x + w - 6, y + int(h * 0.12)], fill=RED, width=3)


def ill_centrifuge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 220, 226))
    for row in range(2):
        for i in range(6):
            cx0 = x + int(w * (0.08 + i * 0.15))
            cy0 = y + int(h * (0.20 + row * 0.38))
            d.rounded_rectangle([cx0, cy0, cx0 + 10, cy0 + int(h * 0.28)],
                                radius=4, fill=INK)
            d.rectangle([cx0 + 3, cy0 - 5, cx0 + 7, cy0], fill=INK)
    d.rectangle([x, y + h - 6, x + w, y + h], fill=GREY)


def ill_soldiers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    for i in range(4):
        cx0 = x + int(w * (0.10 + i * 0.22))
        d.ellipse([cx0, y + int(h * 0.18), cx0 + 16, y + int(h * 0.18) + 16],
                  fill=INK)
        d.rectangle([cx0 - 2, y + int(h * 0.18) + 14, cx0 + 18,
                     y + h - 4], fill=INK)
    d.rectangle([x + int(w * 0.72), y + int(h * 0.55), x + w - 4,
                 y + h - 6], fill=(255, 255, 255), outline=RED)
    d.line([x + int(w * 0.72), y + int(h * 0.55), x + int(w * 0.86),
            y + int(h * 0.72)], fill=RED, width=2)
    d.line([x + w - 4, y + int(h * 0.55), x + int(w * 0.86),
            y + int(h * 0.72)], fill=RED, width=2)


def ill_tariff(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    d.rectangle([x + int(w * 0.14), y + int(h * 0.12), x + int(w * 0.58),
                 y + int(h * 0.88)], fill=(255, 255, 255), outline=INK)
    for i in range(4):
        d.line([x + int(w * 0.20), y + int(h * (0.25 + i * 0.15)),
                x + int(w * 0.52), y + int(h * (0.25 + i * 0.15))],
               fill=GREY, width=2)
    cx, cy = x + int(w * 0.74), y + int(h * 0.42)
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=RED, width=3)


def ill_line(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    for i in range(4):
        yy = y + int(h * (0.2 + i * 0.2))
        d.line([x + 4, yy, x + w - 4, yy], fill=(210, 204, 190), width=1)
    pts = [(0.05, 0.72), (0.22, 0.66), (0.38, 0.70), (0.55, 0.45),
           (0.72, 0.38), (0.88, 0.18)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        d.line([x + w * ax, y + h * ay, x + w * bx, y + h * by],
               fill=RED, width=3)
    d.ellipse([x + w * 0.88 - 4, y + h * 0.18 - 4, x + w * 0.88 + 4,
               y + h * 0.18 + 4], fill=RED)


def ill_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.35], fill=(150, 190, 150))
    d.rectangle([x, y + h * 0.35, x + w, y + h], fill=(120, 90, 60))
    d.rectangle([x + int(w * 0.42), y + int(h * 0.35), x + int(w * 0.58),
                 y + h], fill=(40, 28, 18))
    d.line([x + int(w * 0.50), y + int(h * 0.05), x + int(w * 0.50),
            y + int(h * 0.75)], fill=(240, 200, 90), width=2)
    d.ellipse([x + int(w * 0.50) - 4, y + int(h * 0.75) - 4,
               x + int(w * 0.50) + 4, y + int(h * 0.75) + 4],
              fill=(240, 200, 90))
    for i in range(3):
        d.ellipse([x + int(w * (0.15 + i * 0.12)), y + int(h * 0.55),
                   x + int(w * (0.15 + i * 0.12)) + 6,
                   y + int(h * 0.55) + 6], fill=(240, 200, 90))


def ill_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    d.polygon([(x + int(w * 0.2), y + int(h * 0.15)),
               (x + int(w * 0.8), y + int(h * 0.15)),
               (x + int(w * 0.5), y + int(h * 0.02))], fill=INK)
    for i in range(4):
        cx0 = x + int(w * (0.22 + i * 0.15))
        d.rectangle([cx0, y + int(h * 0.20), cx0 + 6, y + int(h * 0.80)],
                    fill=INK)
    d.rectangle([x + int(w * 0.15), y + int(h * 0.80), x + int(w * 0.85),
                 y + int(h * 0.86)], fill=INK)
    d.line([x + int(w * 0.62), y + int(h * 0.55), x + int(w * 0.92),
            y + int(h * 0.40)], fill=RED, width=3)
    d.rectangle([x + int(w * 0.86), y + int(h * 0.34), x + int(w * 0.98),
                 y + int(h * 0.46)], fill=RED)


def ill_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    cx, cy = x + int(w * 0.5), y + int(h * 0.30)
    for i in range(12):
        import math
        a = math.radians(i * 30)
        d.ellipse([cx + 26 * math.cos(a) - 2, cy + 18 * math.sin(a) - 2,
                   cx + 26 * math.cos(a) + 2, cy + 18 * math.sin(a) + 2],
                  fill=GOLD)
    d.ellipse([x + int(w * 0.18), y + int(h * 0.55), x + int(w * 0.82),
               y + int(h * 0.78)], fill=INK)
    for i in range(3):
        fx = x + int(w * (0.30 + i * 0.20))
        d.line([fx, y + int(h * 0.30), fx, y + int(h * 0.55)], fill=INK,
               width=2)
        d.rectangle([fx, y + int(h * 0.30), fx + 12, y + int(h * 0.40)],
                    fill=RED if i != 1 else BLUE)


def ill_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    hx, hy = x + int(w * 0.12), y + int(h * 0.55)
    d.polygon([(hx, hy), (hx + int(w * 0.76), hy),
               (hx + int(w * 0.68), hy + int(h * 0.22)),
               (hx + int(w * 0.08), hy + int(h * 0.22))], fill=INK)
    cols = [RED, GOLD, BLUE, (40, 120, 70)]
    for r in range(2):
        for i in range(4):
            d.rectangle([hx + 8 + i * 16, hy - 10 - r * 11,
                         hx + 22 + i * 16, hy - 1 - r * 11],
                        fill=cols[(i + r) % 4])
    d.rectangle([hx + int(w * 0.70), hy - 22, hx + int(w * 0.76), hy],
                fill=(255, 255, 255), outline=INK)


def ill_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 140, 80))
    d.rectangle([x + int(w * 0.14), y + int(h * 0.12), x + int(w * 0.86),
                 y + int(h * 0.88)], fill=(90, 170, 100), outline=(255, 255, 255))
    d.line([x + int(w * 0.5), y + int(h * 0.12), x + int(w * 0.5),
            y + int(h * 0.88)], fill=(255, 255, 255), width=2)
    d.line([x + int(w * 0.14), y + int(h * 0.5), x + int(w * 0.86),
            y + int(h * 0.5)], fill=(255, 255, 255), width=2)
    d.ellipse([x + int(w * 0.68) - 7, y + int(h * 0.28) - 7,
               x + int(w * 0.68) + 7, y + int(h * 0.28) + 7],
              fill=(210, 230, 60), outline=INK)


def ill_submarine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.rectangle([x, y + int(h * 0.42), x + w, y + h], fill=(24, 60, 96))
    hx, hy = x + int(w * 0.16), y + int(h * 0.55)
    d.rounded_rectangle([hx, hy, hx + int(w * 0.68), hy + int(h * 0.22)],
                        radius=10, fill=INK)
    d.rectangle([hx + int(w * 0.30), hy - int(h * 0.16), hx + int(w * 0.42),
                 hy], fill=INK)
    d.line([hx + int(w * 0.36), hy - int(h * 0.30), hx + int(w * 0.36),
            hy - int(h * 0.16)], fill=INK, width=2)


ILLUSTRATIONS = {
    "strait": ill_strait, "night": ill_night, "storm": ill_storm,
    "congo": ill_congo, "bank": ill_bank, "bars": ill_bars,
    "centrifuge": ill_centrifuge, "soldiers": ill_soldiers,
    "tariff": ill_tariff, "line": ill_line, "mine": ill_mine,
    "court": ill_court, "summit": ill_summit, "ship": ill_ship,
    "tennis": ill_tennis, "submarine": ill_submarine,
}

# Simplified continent outlines (lon, lat) — stylised, recognisable.
N_AMERICA = [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-130, 54),
             (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
             (-105, 20), (-97, 16), (-90, 14), (-83, 9), (-79, 9), (-81, 13),
             (-87, 16), (-90, 21), (-96, 19), (-97, 26), (-93, 30),
             (-84, 30), (-81, 26), (-80, 32), (-76, 35), (-74, 39),
             (-70, 42), (-65, 44), (-60, 46), (-55, 47), (-60, 50),
             (-64, 58), (-72, 62), (-85, 66), (-95, 69), (-110, 68),
             (-125, 70), (-145, 70), (-158, 71), (-168, 66)]
S_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
             (-72, -18), (-70, -30), (-73, -44), (-70, -54), (-66, -55),
             (-62, -45), (-57, -34), (-52, -32), (-48, -28), (-41, -23),
             (-39, -17), (-35, -9), (-38, -4), (-44, -2), (-50, 0),
             (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-77, 8)]
AFRICA = [(-17, 15), (-16, 20), (-11, 27), (-5, 35), (0, 36), (10, 37),
          (19, 32), (25, 32), (30, 31), (34, 28), (37, 22), (39, 18),
          (43, 11), (51, 11), (51, 6), (42, -2), (40, -8), (40, -15),
          (36, -20), (32, -26), (28, -33), (20, -35), (15, -27),
          (12, -18), (13, -12), (9, -1), (9, 4), (-8, 4), (-13, 8),
          (-17, 12)]
EURASIA = [(-10, 36), (-9, 43), (-2, 44), (-4, 48), (-1, 49), (2, 51),
           (5, 53), (8, 57), (10, 59), (5, 62), (12, 65), (18, 69),
           (25, 71), (30, 70), (40, 68), (50, 69), (60, 69), (70, 72),
           (80, 73), (90, 75), (100, 76), (110, 74), (120, 73), (130, 72),
           (140, 72), (150, 70), (160, 70), (170, 67), (178, 65),
           (170, 60), (162, 56), (158, 52), (150, 59), (142, 55),
           (141, 50), (140, 45), (135, 43), (130, 42), (127, 40),
           (122, 38), (120, 35), (122, 32), (118, 25), (110, 21),
           (108, 18), (105, 10), (100, 8), (98, 10), (94, 17), (92, 21),
           (89, 22), (86, 20), (80, 15), (77, 8), (75, 12), (73, 16),
           (70, 20), (66, 25), (61, 25), (58, 26), (56, 27), (54, 26),
           (52, 25), (50, 29), (48, 30), (44, 29), (41, 28), (39, 24),
           (38, 21), (35, 20), (35, 16), (39, 13), (43, 12), (45, 13),
           (48, 14), (51, 16), (55, 17), (58, 20), (57, 24), (54, 24),
           (51, 26), (50, 29), (48, 30), (44, 29), (40, 31), (36, 36),
           (33, 36), (30, 36), (27, 37), (23, 36), (20, 39), (19, 42),
           (15, 44), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37),
           (-6, 36)]
AUSTRALIA = [(114, -22), (114, -30), (115, -33), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (140, -17), (136, -15),
             (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
             (118, -20)]

EUROPE_INSET = [(-10, 36), (-9, 43), (-2, 44), (-4, 48), (-1, 49), (2, 51),
                (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58),
                (28, 59), (30, 60), (30, 70), (25, 71), (18, 69), (12, 65),
                (5, 62), (5, 58), (8, 57), (10, 59), (5, 60), (5, 62),
                (12, 58), (18, 56), (21, 54), (19, 52), (14, 54), (12, 54),
                (8, 54), (3, 51), (-2, 50), (-5, 48), (-2, 47), (-1, 44),
                (3, 43), (7, 44), (12, 44), (14, 45), (19, 42), (19, 40),
                (16, 40), (16, 38), (12, 38), (8, 39), (3, 38), (-1, 37),
                (-6, 36), (-9, 37), (-9, 43), (-10, 36)]


def draw_map(d, x, y, w, h, polys, lon0, lon1, lat0, lat1):
    def px(lon, lat):
        return (x + (lon - lon0) / (lon1 - lon0) * w,
                y + (lat1 - lat) / (lat1 - lat0) * h)
    d.rectangle([x, y, x + w, y + h], fill=(216, 228, 236))
    for poly in polys:
        d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=(150, 140, 115))


def pin(d, px, py, num, label=None, dx=0, dy=0):
    cx, cy = px + dx, py + dy
    if dx or dy:
        d.line([px, py, cx, cy], fill=INK, width=1)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=INK)
    d.text((cx, cy - 6), str(num), font=F_COND_B(10), fill=CREAM,
           anchor="ma")
    if label:
        d.text((cx + 10, cy - 6), label, font=F_COND_B(9), fill=INK)


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)
    y = 10

    # masthead
    f = F_BLACK(30)
    d.text((W // 2, y), C.MASTHEAD, font=f, fill=INK, anchor="ma")
    y += 34
    d.line([MX, y, W - MX, y], fill=INK, width=2)
    y += 8
    # date — largest type on the page
    f = F_BLACK(40)
    d.text((W // 2, y), C.DATE_LINE, font=f, fill=INK, anchor="ma")
    y += 46
    # red italic subhead
    f = F_SERIF_I(15)
    d.text((W // 2, y), C.SUBHEAD, font=f, fill=RED, anchor="ma")
    y += 20
    # region line
    parts = [f"{C.TOTAL_STORIES} STORIES"]
    parts += [f"{name} {n}" for name, n in C.REGION_COUNTS]
    f = F_COND_B(12)
    d.text((W // 2, y), "  ·  ".join(parts), font=f, fill=INK, anchor="ma")
    y += 18
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    y += 7

    # ---- THE DAY IN NUMBERS ----
    f = F_COND_B(12)
    d.text((MX, y), "THE DAY IN NUMBERS", font=f, fill=RED)
    y += 15
    cell_w = (W - 2 * MX) // len(C.NUMBERS)
    f_num = F_SERIF_B(21)
    f_cap = F_COND(10)
    for i, (num, cap) in enumerate(C.NUMBERS):
        cx = MX + i * cell_w + cell_w // 2
        d.text((cx, y), num, font=f_num, fill=INK, anchor="ma")
        lines = wrap(d, cap, f_cap, cell_w - 10)
        assert len(lines) <= 2, f"numbers caption too long: {cap}"
        text_block(d, MX + i * cell_w + 5, y + 22, lines, f_cap, GREY,
                   leading=11, align="c", box_w=cell_w - 10)
        if i:
            d.line([MX + i * cell_w, y + 2, MX + i * cell_w, y + 38],
                   fill=GREY, width=1)
    y += 42
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    y += 7

    # ---- UTC TIMELINE ----
    f = F_COND_B(12)
    d.text((MX, y), "THE DAY IN TIME \u2014 ALL TIMES UTC", font=f, fill=RED)
    y += 15
    col_w = (W - 2 * MX) // 3
    f_t = F_COND_B(11)
    f_e = F_SERIF(11)
    for i, (t, ev) in enumerate(C.TIMELINE):
        x = MX + (i % 3) * col_w
        yy = y + (i // 3) * 12
        d.text((x, yy), t, font=f_t, fill=RED)
        tw = d.textlength(t, font=f_t)
        d.text((x + tw + 5, yy), ev, font=f_e, fill=INK)
    y += 36
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    y += 7

    # ---- LEADS ----
    lead_w = (W - 2 * MX - 16) // 3
    lead_h = 146
    ly = y
    f_head = F_SERIF_B(16)
    f_body = F_SERIF(11)
    f_tag = F_COND_B(10)
    for i, (num, region, cert, head, body, chip_text, kind, pin_xy) in enumerate(C.LEADS):
        x = MX + i * (lead_w + 8)
        d.rectangle([x, ly, x + lead_w, ly + lead_h], outline=INK, width=1)
        ix, iy, iw, ih = x + 4, ly + 4, lead_w - 8, 54
        ILLUSTRATIONS[kind](d, ix, iy, iw, ih)
        chip(d, ix + iw - 3, iy + 3, chip_text, F_COND_B(11))
        lines = wrap(d, head, f_head, lead_w - 12)
        assert len(lines) <= 2, f"lead headline too long: {head}"
        text_block(d, x + 6, ly + 62, lines, f_head, INK, leading=19)
        blines = wrap(d, body, f_body, lead_w - 12)
        assert len(blines) <= 2, f"lead body too long: {body}"
        text_block(d, x + 6, ly + 102, blines, f_body, INK, leading=13)
        d.text((x + 6, ly + lead_h - 14), f"{num}  ·  {cert}", font=f_tag,
               fill=RED)
        d.text((x + lead_w - 6, ly + lead_h - 14), region, font=f_tag,
               fill=GREY, anchor="ra")
    y = ly + lead_h + 7

    # ---- MIDDLE TIER: rows of 5, 4, 4 ----
    # row 1: headline-only cards; rows 2-3: headline + 2-line body.
    rows = [(C.MIDDLE[0:5], 72, True), (C.MIDDLE[5:9], 94, False),
            (C.MIDDLE[9:13], 94, False)]
    f_mhead = F_SERIF_B(13)
    f_mbody = F_SERIF(10)
    f_mcert = F_COND_B(8)
    for row, rh, headline_only in rows:
        n = len(row)
        mw = (W - 2 * MX - (n - 1) * 6) // n
        for i, (num, region, cert, head, body, chip_text, kind,
                pin_xy) in enumerate(row):
            x = MX + i * (mw + 6)
            d.rectangle([x, y, x + mw, y + rh], outline=INK, width=1)
            ix, iy, iw, ih = x + 3, y + 3, mw - 6, 34
            ILLUSTRATIONS[kind](d, ix, iy, iw, ih)
            chip(d, ix + iw - 3, iy + 3, chip_text, F_COND_B(9))
            # certainty strip along the bottom of the illustration
            d.rectangle([ix, iy + ih - 10, ix + iw, iy + ih], fill=INK)
            d.text((ix + 4, iy + ih - 9), cert, font=f_mcert, fill=CREAM)
            lines = wrap(d, head, f_mhead, mw - 26)
            assert len(lines) <= 2, f"middle headline too long: {head}"
            text_block(d, x + 4, y + 41, lines, f_mhead, INK, leading=15)
            if not headline_only:
                blines = wrap(d, body, f_mbody, mw - 8)
                assert len(blines) <= 2, f"middle body too long: {body}"
                text_block(d, x + 4, y + 71, blines, f_mbody, GREY,
                           leading=11)
            d.text((x + mw - 4, y + 41), str(num), font=F_COND_B(11),
                   fill=RED, anchor="ra")
        y += rh + 5

    # ---- MAP ----
    f = F_COND_B(12)
    d.text((MX, y), "WHERE IT HAPPENED \u2014 PIN NUMBERS MATCH STORY NUMBERS",
           font=f, fill=RED)
    y += 13
    map_y = y
    map_h = 70
    map_w = 640
    draw_map(d, MX, map_y, map_w, map_h,
             [N_AMERICA, S_AMERICA, AFRICA, EURASIA, AUSTRALIA],
             -170, 190, -55, 75)
    d.rectangle([MX, map_y, MX + map_w, map_y + map_h], outline=INK, width=1)
    f_oc = F_COND(9)
    d.text((MX + 8, map_y + map_h - 12), "PACIFIC", font=f_oc, fill=GREY)
    d.text((MX + 300, map_y + map_h - 12), "ATLANTIC", font=f_oc, fill=GREY)

    def map_px(lon, lat):
        return (MX + (lon + 170) / 360.0 * map_w,
                map_y + (75 - lat) / 130.0 * map_h)

    # pins: (num, lon, lat, dx, dy) — nudges for the Korea/Tokyo clusters
    pin_specs = []
    for item in C.LEADS + C.MIDDLE:
        pin_specs.append((item[0], item[7][0], item[7][1], 0, 0))
    nudges = {6: (0, 0), 7: (13, 9), 9: (0, 0), 10: (15, -10)}
    for num, lon, lat, dx, dy in pin_specs:
        if num in (5, 8, 13, 16):
            continue  # Europe inset
        px, py = map_px(lon, lat)
        ndx, ndy = nudges.get(num, (0, 0))
        pin(d, px, py, num, dx=ndx, dy=ndy)
    # Europe inset (draw map first, then label on top)
    ex, ew = MX + map_w + 8, W - MX - (MX + map_w + 8)
    draw_map(d, ex, map_y, ew, map_h, [EUROPE_INSET], -12, 32, 35, 62)
    d.rectangle([ex, map_y, ex + ew, map_y + map_h], outline=INK, width=1)
    d.rectangle([ex + 3, map_y + 3, ex + 92, map_y + 15], fill=CREAM)
    d.text((ex + 6, map_y + 4), "EUROPE \u2014 DETAIL", font=F_COND_B(10),
           fill=RED)
    for num, lon, lat in ((5, 8.7, 50.1), (8, -0.1, 51.5),
                          (13, 4.35, 50.85), (16, -4.15, 50.37)):
        px = ex + (lon + 12) / 44.0 * ew
        py = map_y + (62 - lat) / 27.0 * map_h
        pin(d, px, py, num)
    y = map_y + map_h + 7

    # ---- ALSO ----
    f = F_COND_B(12)
    d.text((MX, y), "ALSO ON THURSDAY 26 NOVEMBER", font=f, fill=RED)
    y += 13
    col_w = (W - 2 * MX) // 3
    f_a = F_COND_B(11)
    also_lines = {
        17: "SAUDI DEFENCES STOP TWO HOUTHI MISSILES AIMED AT RIYADH",
        18: "EUROPEAN STOCKS RALLY; STOXX 600 +1.4%",
        19: "DIESEL TANKER SINKS OFF IBIZA; ONE CREW MEMBER DIES",
        20: "SNOW BLANKETS VIENNA; BUSES STUCK IN MORNING RUSH",
        21: "GERMAN CONSUMER SENTIMENT EDGES UP TO \u221230.2",
        22: "ITALY ASKS GERMANY TO STOP A HENKEL FACTORY CLOSURE",
        23: "AIRBALTIC OFFERS CREW EXIT, DEMOTION OR PNG SECONDMENT",
        24: "EISENKOT RESUMES COALITION TALKS WITH THE DEMOCRATS",
        25: "KUSHNER: TRUMP KEEPS \u2018ALL OPTIONS ON TABLE\u2019 ON IRAN",
        26: "AUSTRALIA SET TO PASS AN LNG RESERVE LAW",
        27: "JAPAN OPPOSITION FILES CENSURE MOTION ON MINISTER",
        28: "HONG KONG MARKS A YEAR SINCE THE TAI PO FIRE KILLED 168",
        29: "INDIAN SHARES EXTEND GAINS ON RECORD FOREIGN INFLOWS",
        30: "DR CONGO SUMMONS UGANDA ENVOY (STATEMENT WED)",
        31: "KENYA COURT: EBOLA SITE BUILD BREACHED CHARTER",
        32: "RWANDA HIKES RATE 75BP TO 9.5%; INFLATION 19.5%",
        33: "FIRST GENERIC HIV-PREVENTION DRUGS REACH AFRICA",
        34: "TULLOW OIL TO BEAT ITS ANNUAL OUTPUT TARGET",
        35: "GOLD STEADIES AFTER HITTING A MORE-THAN-ONE-YEAR LOW",
        36: "TRUMP, NATO CHIEF: RUSSIA MUST NOT WIDEN WAR (WED)",
        37: "BRAZIL CALLS US TARIFF PLAN \u2018UNACCEPTABLE\u2019 (WED EVE)",
        38: "US MARKETS SHUT FOR THANKSGIVING",
        39: "JAPAN PROPERTY DRAWS GLOBAL MONEY",
        40: "APPLE PULLS MINIMAX\u2019S TALKIE CHATBOT",
    }
    for i, item in enumerate(C.ALSO):
        num = item[0]
        x = MX + (i % 3) * col_w
        yy = y + (i // 3) * 11
        txt = also_lines[num]
        w = d.textlength(txt, font=f_a)
        assert w <= col_w - 30, f"ALSO line too long: {txt}"
        d.text((x, yy), f"{num}.", font=f_a, fill=RED)
        d.text((x + 20, yy), txt, font=f_a, fill=INK)
    y += 8 * 11 + 4

    # ---- DATE CHECK ----
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    y += 5
    f = F_COND_B(12)
    d.text((MX, y), "DATE CHECK \u2014 EXCLUDED AS OTHER DAYS\u2019 NEWS, OR NOT YET",
           font=f, fill=RED)
    y += 13
    f_d = F_SERIF(10)
    f_dl = F_COND_B(10)
    for label, note in C.DATECHECK:
        d.text((MX, y), label, font=f_dl, fill=RED)
        lw = d.textlength(label, font=f_dl)
        lines = wrap(d, note, f_d, W - 2 * MX - lw - 8)
        assert len(lines) == 1, f"DATE CHECK line wraps: {note}"
        d.text((MX + lw + 8, y), lines[0], font=f_d, fill=INK)
        y += 11
    y += 2
    f_l = F_COND(10)
    d.text((MX, y), C.LEGEND, font=f_l, fill=GREY)
    y += 11
    d.text((MX, y), C.ILLU_NOTE, font=f_l, fill=GREY)
    y += 11

    assert y <= H - 4, f"page overflow: y={y}"
    return img


def main():
    img = render()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "page.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

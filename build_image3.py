#!/usr/bin/env python3
"""V3 builder for 'Sum up 24 November's world news in one image'.

The dense tabloid class Mas pointed at: a giant date title, region-count
tabs, a numbers strip, fifteen numbered tiles each with its own drawn
scene, verdict banner, region line and status chip, a numbered
also-on-Tuesday list, and a dot-matrix world map pinning tiles 1-15.
All stories are the edition's verified Tuesday 24 November 2026 spine.
Draws entry.png (1024x1024); main.py only copies it in the sandbox.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28

PAPER = (250, 246, 236)
INK = (24, 24, 40)
RED = (179, 32, 44)
NAVY = (22, 50, 79)
NAVY2 = (16, 38, 62)
GOLD = (201, 146, 14)
GOLDD = (146, 104, 10)
TEAL = (31, 84, 112)
GREEN = (46, 110, 60)
ORANGE = (196, 110, 24)
PURPLE = (110, 62, 140)
GREY = (96, 96, 110)
RULE = (60, 60, 80)
CREAM = (238, 231, 214)
SKY = (196, 220, 232)
SEA = (46, 111, 142)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, width, pitch, fill=INK, max_lines=None):
    lines = wrap(d, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += pitch
    return y


def chip(d, x, y, text, fill):
    f = F(SANSB, 8)
    w = d.textlength(text, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], 2, fill=fill)
    d.text((x + 5, y + 2.5), text, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- content

REGIONS = [
    ("EUROPE", NAVY, 7), ("MIDDLE EAST", RED, 5), ("AFRICA", ORANGE, 2),
    ("ASIA", TEAL, 2), ("AMERICAS", GREEN, 11), ("GLOBAL", NAVY2, 1),
]

NUMBERS = [
    ("7", "CONDITIONS TEHRAN SETS\nFOR ANY TALKS AT ALL"),
    ("7", "TANKERS STRUCK IN HORMUZ\nSINCE 16 NOVEMBER"),
    ("11", "INJURED AS A DRONE HITS\nRIYADH'S PIF TOWER"),
    ("$8BN", "RECOVERED IN THE LARGEST\nUS ANTI-SCAM SWEEP EVER"),
    ("6,500", "ROHINGYA MALAYSIA PLANS\nTO SEND BACK TO MYANMAR"),
]

# (region, region colour, status, status colour, banner, banner colour,
#  headline, body, scene key)
BIG_TILES = [
    ("MIDDLE EAST", RED, "REPORTED", GOLD, "NO TALKS UNTIL 7 CONDITIONS", RED,
     "Iran names its price for the strait",
     "No talks, no reopening of Hormuz until seven conditions are met: "
     "sanctions ended, blockade lifted, assets freed. Tehran claims "
     "three tankers mined. Reuters",
     "hormuz"),
    ("MIDDLE EAST", RED, "REPORTED", GOLD, "DRONE STRIKE", RED,
     "Drone hits Riyadh's PIF Tower; 11 hurt",
     "A Houthi drone struck the PIF Tower, injuring 11, civil defence "
     "said. The Houthis reported dozens killed by Saudi strikes in "
     "Yemen the same day. Al Jazeera",
     "riyadh"),
    ("AMERICAS", GREEN, "CONFIRMED", NAVY, "PARTY REVOLT", NAVY,
     "Trump faces down his own party over Huang",
     "Republicans broke with Trump over security fears after Nvidia "
     "reinstated Jensen Huang, ousted 12 days earlier. He testifies in "
     "secret on 1 December. CNN",
     "capitol"),
]

SMALL_TILES = [
    ("EUROPE", NAVY, "REPORTED", GOLD, "WORLD COURT", GOLDD,
     "14 countries back the ICJ on Rohingya",
     "Britain, Spain, Canada, Australia and ten more affirmed the ICJ's "
     "genocide ruling.",
     "scales"),
    ("AMERICAS", GREEN, "CONFIRMED", NAVY, "GUILTY", RED,
     "US jury finds Huawei guilty",
     "Guilty of stealing trade secrets; cleared of racketeering by a "
     "Brooklyn jury. BBC",
     "court"),
    ("GLOBAL", NAVY2, "CONFIRMED", NAVY, "ONE YEAR", TEAL,
     "UN chief: an AI-risk framework in a year",
     "Guterres urged states to build a multilateral AI-risk framework "
     "within a year. UN News",
     "globe"),
    ("AFRICA", ORANGE, "REPORTED", GOLD, "TEAMS TRAPPED", ORANGE,
     "Fighting traps Ebola teams in Ituri",
     "Fighting near a hospital forced Ebola response teams to shelter "
     "24 hours. WHO",
     "shield"),
    ("AMERICAS", GREEN, "CONFIRMED", NAVY, "14 DEAD", RED,
     "Measles toll climbs towards 6,000 cases",
     "Fourteen dead, cases near 6,000; nine of the deaths in "
     "Pennsylvania.",
     "spots"),
    ("MIDDLE EAST", RED, "REPORTED", GOLD, "SIX KILLED", RED,
     "Strikes kill six in Gaza, medics say",
     "Airstrikes killed six, including two police; Oxfam called Gaza "
     "a 'toxic land'.",
     "gaza"),
    ("EUROPE", NAVY, "CONFIRMED", NAVY, "FIRST ACCESS", NAVY,
     "Germany first to get Kyiv's Delta system",
     "Berlin won access to Ukraine's Delta battlefield system, the two "
     "ministries agreed.",
     "delta"),
    ("EUROPE", NAVY, "CONFIRMED", NAVY, "SPACE WARNING", PURPLE,
     "NATO vows defence against space threats",
     "Rutte spoke after reports of a Russian nuclear-armed satellite. "
     "BBC",
     "satellite"),
]

# (region code, region colour, text)
LIST_ITEMS = [
    ("EU", NAVY, "MOSCOW — Putin complains Ukraine keeps striking "
     "Russian oil refineries, vows retaliation."),
    ("AF", ORANGE, "LIBYA — Tripoli demands Kyiv explain Sunday's "
     "attacks on Russian ships at Benghazi."),
    ("EU", NAVY, "BELGIUM — a strike against austerity cancels "
     "flights and snarls transport nationwide."),
    ("EU", NAVY, "BRITAIN — the Timms review could strip disability "
     "payments from hundreds of thousands."),
    ("AM", GREEN, "IOWA — the Army orders explosive lead azide "
     "detonated; nearby residents evacuated."),
    ("ME", RED, "IRAN — singer Parastoo Ahmadi is given 74 lashes "
     "for defying the morality rules."),
    ("AM", GREEN, "WEATHER — record king tides flood Bay Area roads "
     "as a storm surge rides the full moon."),
    ("AM", GREEN, "WASHINGTON — Trump awards Rudy Giuliani the "
     "Presidential Medal of Freedom."),
    ("ME", RED, "IRAQ — Baghdad orders the federal oil ministry to "
     "run the Kurdish-region oilfields."),
    ("AM", GREEN, "MEXICO — 'El Chapo Isidro' will be tried at home "
     "despite a US extradition request."),
    ("AM", GREEN, "VENEZUELA — public debt put at $237.5 billion as "
     "restructuring talks advance."),
    ("AM", GREEN, "CUBA — the WHO chief visits a health system in "
     "visible deterioration."),
    ("EU", NAVY, "BRITAIN — the inmate who murdered Ian Huntley gets "
     "a second whole-life sentence."),
    ("AS", TEAL, "NEPAL — a magnitude-5.6 earthquake strikes Koshi "
     "province, near the China border."),
    ("AS", TEAL, "TIANGONG — Pakistan's Zeeshan Ali becomes the first "
     "foreign astronaut aboard."),
    ("AM", GREEN, "JUSTICE — $8 billion recovered, 800+ charged in "
     "the largest US anti-scam sweep ever."),
    ("AM", GREEN, "COLOMBIA — a car bomb in Villavicencio; gunmen "
     "take hostages in Cartagena."),
]

DATE_CHECK = (
    "DATE CHECK — Tuesday 24 November 2026 is day 328 of the year; 37 days "
    "remain. Every story on this page was first reported on Tuesday 24 "
    "November 2026 — wire copy, official statements, court filings. "
    "Not Tuesday: the Nvidia market explosion and COP31's collapse "
    "(both Monday 23 November, covered on yesterday's page)."
)


# ---------------------------------------------------------------- scenes

def _bg(d, x, y, w, h, top=SKY, bottom=(238, 233, 214)):
    for i in range(int(h)):
        t = i / max(h - 1, 1)
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        d.line([x, y + i, x + w, y + i], fill=col)


def sc_hormuz(d, x, y, w, h):
    _bg(d, x, y, w, h, top=SEA, bottom=SEADEEP if (SEADEEP := (31, 84, 112)) else SEA)
    d.polygon([(x, y), (x + w * 0.5, y), (x + w * 0.38, y + h * 0.34),
               (x, y + h * 0.42)], fill=(217, 178, 106))
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h * 0.6),
               (x + w * 0.55, y + h * 0.68), (x + w * 0.2, y + h * 0.8)],
              fill=(198, 156, 84))
    sx, sy = x + w * 0.28, y + h * 0.5
    d.line([sx - 8, sy + 9, sx + w * 0.3, sy + 9], fill=(255, 255, 255),
           width=2)
    d.polygon([(sx, sy), (sx + w * 0.26, sy), (sx + w * 0.22, sy + 8),
               (sx + w * 0.04, sy + 8)], fill=(30, 34, 46),
              outline=(255, 255, 255))
    d.rectangle([sx + w * 0.19, sy - 7, sx + w * 0.22, sy], fill=(30, 34, 46))
    d.rectangle([sx + w * 0.05, sy - 4, sx + w * 0.15, sy], fill=(150, 60, 50))
    for mx, my in ((0.62, 0.3), (0.68, 0.52)):
        cx, cy = x + w * mx, y + h * my
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
        for dx, dy in ((0, -5), (0, 5), (-5, 0), (5, 0)):
            d.line([cx, cy, cx + dx, cy + dy], fill=RED, width=1)


def sc_riyadh(d, x, y, w, h):
    _bg(d, x, y, w, h)
    cx = x + w * 0.42
    d.polygon([(cx - 18, y + h), (cx, y + h * 0.08), (cx + 18, y + h)],
              fill=NAVY)
    d.polygon([(cx - 18, y + h), (cx, y + h * 0.08), (cx + 3, y + h)],
              fill=NAVY2)
    for tx, th in ((0.14, 0.45), (0.68, 0.35)):
        d.rectangle([x + w * tx, y + h * (1 - th), x + w * tx + 12, y + h],
                    fill=(150, 148, 140))
    dx, dy = x + w * 0.72, y + h * 0.3
    d.line([dx - 12, dy, dx + 12, dy], fill=INK, width=2)
    d.line([dx, dy - 5, dx, dy + 5], fill=INK, width=2)
    d.ellipse([dx - 2.5, dy - 2.5, dx + 2.5, dy + 2.5], fill=INK)
    bx, by = x + w * 0.6, y + h * 0.52
    for dx2, dy2 in ((0, -7), (6, -4), (7, 3), (3, 7), (-5, 5), (-7, -2)):
        d.line([bx, by, bx + dx2, by + dy2], fill=RED, width=2)
    d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=RED)


def sc_capitol(d, x, y, w, h):
    _bg(d, x, y, w, h)
    cx = x + w / 2
    base = y + h
    fillc = (206, 212, 224)
    d.rectangle([cx - w * 0.32, base - 10, cx + w * 0.32, base], fill=fillc,
                outline=NAVY)
    d.rectangle([cx - w * 0.26, base - 24, cx + w * 0.26, base - 10],
                fill=fillc, outline=NAVY)
    for i in range(6):
        px = cx - w * 0.22 + i * w * 0.088
        d.line([px, base - 24, px, base - 10], fill=NAVY, width=2)
    d.pieslice([cx - w * 0.13, base - 56, cx + w * 0.13, base - 12],
               180, 360, fill=NAVY)
    d.line([cx, base - 56, cx, base - 66], fill=NAVY, width=3)
    d.polygon([(cx, base - 66), (cx + 13, base - 62), (cx, base - 58)],
              fill=RED)


def sc_scales(d, x, y, w, h):
    _bg(d, x, y, w, h)
    cx, top = x + w / 2, y + h * 0.16
    d.line([cx, top, cx, y + h * 0.88], fill=NAVY, width=3)
    d.line([cx - w * 0.2, top + 5, cx + w * 0.2, top + 5], fill=NAVY, width=3)
    d.rectangle([cx - 12, y + h * 0.88, cx + 12, y + h * 0.95], fill=NAVY)
    for sx in (-0.2, 0.2):
        px = cx + w * sx
        d.line([px, top + 5, px - 7, top + 22], fill=NAVY, width=1)
        d.line([px, top + 5, px + 7, top + 22], fill=NAVY, width=1)
        d.arc([px - 10, top + 16, px + 10, top + 30], 0, 180, fill=RED, width=2)


def sc_court(d, x, y, w, h):
    _bg(d, x, y, w, h)
    cx = x + w / 2
    d.polygon([(cx - w * 0.32, y + h * 0.3), (cx + w * 0.32, y + h * 0.3),
               (cx, y + h * 0.06)], fill=NAVY)
    d.rectangle([cx - w * 0.34, y + h * 0.32, cx + w * 0.34, y + h * 0.4],
                fill=NAVY)
    for i in range(5):
        px = cx - w * 0.26 + i * w * 0.13
        d.rectangle([px, y + h * 0.42, px + 5, y + h * 0.82], fill=(240, 236, 224))
    d.rectangle([cx - w * 0.34, y + h * 0.82, cx + w * 0.34, y + h * 0.9],
                fill=NAVY)


def sc_globe(d, x, y, w, h):
    _bg(d, x, y, w, h, top=NAVY2, bottom=TEAL)
    cx, cy, r = x + w / 2, y + h / 2, h * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 190, 150))
    d.ellipse([cx - r * 0.55, cy - r * 0.6, cx - r * 0.05, cy - r * 0.1],
              fill=(46, 110, 60))
    d.ellipse([cx + r * 0.1, cy + r * 0.05, cx + r * 0.6, cy + r * 0.55],
              fill=(46, 110, 60))
    for a in range(0, 360, 45):
        import math
        nx = cx + (r + 12) * math.cos(math.radians(a))
        ny = cy + (r + 9) * math.sin(math.radians(a))
        d.line([cx, cy, nx, ny], fill=(255, 214, 120), width=1)
        d.ellipse([nx - 2.5, ny - 2.5, nx + 2.5, ny + 2.5],
                  fill=(255, 214, 120))


def sc_shield(d, x, y, w, h):
    _bg(d, x, y, w, h, top=(170, 205, 160), bottom=(220, 226, 190))
    cx, cy = x + w / 2, y + h / 2
    d.polygon([(cx - 16, cy - h * 0.32), (cx + 16, cy - h * 0.32),
               (cx + 16, cy + 4), (cx, cy + h * 0.36), (cx - 16, cy + 4)],
              fill=(240, 240, 240), outline=RED)
    d.rectangle([cx - 3.5, cy - h * 0.2, cx + 3.5, cy + h * 0.14], fill=RED)
    d.rectangle([cx - 10, cy - h * 0.06, cx + 10, cy + 1], fill=RED)
    for lx in (x + 12, x + w - 18):
        d.arc([lx, y + h * 0.2, lx + 12, y + h * 0.8], 270, 90,
              fill=(46, 110, 60), width=3)


def sc_spots(d, x, y, w, h):
    _bg(d, x, y, w, h)
    cx, cy = x + w * 0.38, y + h / 2
    d.ellipse([cx - h * 0.3, cy - h * 0.32, cx + h * 0.3, cy + h * 0.32],
              fill=(238, 205, 170))
    import random
    rng = random.Random(7)
    for _ in range(16):
        px = cx + rng.uniform(-h * 0.26, h * 0.26)
        py = cy + rng.uniform(-h * 0.28, h * 0.28)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    vx = x + w * 0.72
    d.polygon([(vx, y + h * 0.25), (vx + 9, y + h * 0.25), (vx + 4.5,
               y + h * 0.45)], fill=TEAL)
    d.rectangle([vx + 1.5, y + h * 0.45, vx + 7.5, y + h * 0.72], fill=TEAL)


def sc_gaza(d, x, y, w, h):
    _bg(d, x, y, w, h, top=(214, 190, 160), bottom=(232, 220, 195))
    base = y + h
    for bx, bw, bh in ((0.06, 0.16, 0.5), (0.26, 0.13, 0.68), (0.43, 0.18, 0.42),
                       (0.65, 0.14, 0.6), (0.83, 0.12, 0.46)):
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + bw), base],
                    fill=(120, 112, 100))
    for sx, sy in ((0.32, 0.3), (0.7, 0.38)):
        cx, cy = x + w * sx, base - h * sy
        for r, col in ((13, (105, 100, 95)), (9, (130, 124, 116)),
                       (5.5, (155, 148, 138))):
            d.ellipse([cx - r, cy - r * 1.5, cx + r, cy + r * 0.6], fill=col)


def sc_delta(d, x, y, w, h):
    _bg(d, x, y, w, h, top=NAVY2, bottom=NAVY)
    d.rectangle([x + w * 0.14, y + h * 0.14, x + w * 0.86, y + h * 0.8],
                outline=(140, 220, 160), width=2)
    for i in range(1, 5):
        gx = x + w * 0.14 + i * w * 0.144
        d.line([gx, y + h * 0.14, gx, y + h * 0.8], fill=(70, 110, 90), width=1)
    for i in range(1, 3):
        gy = y + h * 0.14 + i * h * 0.22
        d.line([x + w * 0.14, gy, x + w * 0.86, gy], fill=(70, 110, 90), width=1)
    d.polygon([(x + w * 0.3, y + h * 0.6), (x + w * 0.52, y + h * 0.34),
               (x + w * 0.68, y + h * 0.52)], outline=(255, 214, 120), width=2)
    d.ellipse([x + w * 0.6, y + h * 0.24, x + w * 0.66, y + h * 0.34],
              fill=RED)


def sc_satellite(d, x, y, w, h):
    _bg(d, x, y, w, h, top=(10, 16, 34), bottom=NAVY2)
    import random
    rng = random.Random(3)
    for _ in range(26):
        px, py = rng.uniform(x + 3, x + w - 3), rng.uniform(y + 3, y + h - 3)
        d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255))
    cx, cy = x + w / 2, y + h / 2
    d.rectangle([cx - 8, cy - 7, cx + 8, cy + 7], fill=(200, 200, 210))
    for sx in (-1, 1):
        xa, xb = cx + sx * 10, cx + sx * 34
        d.rectangle([min(xa, xb), cy - 5, max(xa, xb), cy + 5],
                    fill=(70, 110, 190))
        for g in range(1, 4):
            gx = cx + sx * (10 + g * 8)
            d.line([gx, cy - 5, gx, cy + 5], fill=(40, 70, 130), width=1)
    d.arc([cx - 16, cy + 4, cx + 16, cy + 26], 20, 160, fill=GOLD, width=2)


def sc_mountains(d, x, y, w, h):
    _bg(d, x, y, w, h)
    base = y + h
    d.polygon([(x, base), (x + w * 0.3, y + h * 0.22), (x + w * 0.52, base)],
              fill=(130, 125, 140))
    d.polygon([(x + w * 0.38, base), (x + w * 0.68, y + h * 0.1),
               (x + w, base)], fill=(105, 100, 118))
    d.polygon([(x + w * 0.62, y + h * 0.24), (x + w * 0.68, y + h * 0.1),
               (x + w * 0.74, y + h * 0.24)], fill=(255, 255, 255))
    d.polygon([(x + w * 0.25, y + h * 0.32), (x + w * 0.3, y + h * 0.22),
               (x + w * 0.35, y + h * 0.32)], fill=(255, 255, 255))
    d.line([x + w * 0.47, y + h * 0.55, x + w * 0.53, y + h * 0.72,
            x + w * 0.5, y + h * 0.88], fill=RED, width=2)


def sc_station(d, x, y, w, h):
    _bg(d, x, y, w, h, top=(10, 16, 34), bottom=(30, 60, 100))
    cx, cy = x + w / 2, y + h * 0.44
    d.line([cx - w * 0.36, cy, cx + w * 0.36, cy], fill=(210, 210, 220), width=3)
    for sx in (-0.3, -0.18, 0.18, 0.3):
        d.rectangle([cx + w * sx - 7, cy - 8, cx + w * sx + 7, cy + 8],
                    fill=(70, 110, 190))
    d.rectangle([cx - 6, cy - 10, cx + 6, cy + 10], fill=(220, 220, 228))
    d.line([cx, cy - 10, cx, cy - 18], fill=(210, 210, 220), width=2)
    d.arc([x + w * 0.1, y + h * 0.62, x + w * 0.9, y + h * 1.25], 180, 360,
          fill=(120, 190, 150), width=5)


def sc_vault(d, x, y, w, h):
    _bg(d, x, y, w, h, top=(90, 95, 110), bottom=(60, 64, 78))
    cx, cy, r = x + w / 2, y + h / 2, h * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 175, 185),
              outline=(220, 220, 228), width=3)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
              outline=(220, 220, 228), width=3)
    for a in range(0, 360, 60):
        import math
        nx = cx + r * 0.68 * math.cos(math.radians(a))
        ny = cy + r * 0.68 * math.sin(math.radians(a))
        d.line([cx, cy, nx, ny], fill=(220, 220, 228), width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD)


def sc_rooftops(d, x, y, w, h):
    _bg(d, x, y, w, h, top=(232, 190, 140), bottom=(240, 220, 185))
    base = y + h
    for bx, bw, bh, col in ((0.04, 0.2, 0.52, (178, 120, 80)),
                            (0.27, 0.22, 0.66, (196, 140, 92)),
                            (0.52, 0.2, 0.46, (170, 112, 74)),
                            (0.75, 0.21, 0.58, (188, 130, 86))):
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + bw), base],
                    fill=col)
        d.polygon([(x + w * bx - 3, base - h * bh),
                   (x + w * (bx + bw) + 3, base - h * bh),
                   (x + w * (bx + bw * 0.5), base - h * (bh + 0.14))],
                  fill=(150, 60, 50))
    px = x + w * 0.9
    d.line([px, base, px, base - h * 0.5], fill=(46, 110, 60), width=2)
    for a in (-38, -14, 12, 36):
        import math
        ex = px + 13 * math.sin(math.radians(a))
        ey = base - h * 0.5 - 9 * math.cos(math.radians(a))
        d.line([px, base - h * 0.5, ex, ey], fill=(46, 110, 60), width=2)


SCENES = {
    "hormuz": sc_hormuz, "riyadh": sc_riyadh, "capitol": sc_capitol,
    "scales": sc_scales, "court": sc_court, "globe": sc_globe,
    "shield": sc_shield, "spots": sc_spots, "gaza": sc_gaza,
    "delta": sc_delta, "satellite": sc_satellite,
    "mountains": sc_mountains, "station": sc_station, "vault": sc_vault,
    "rooftops": sc_rooftops,
}


# ---------------------------------------------------------------- world map

CONTINENTS = [
    [(-165, 68), (-150, 70), (-135, 69), (-120, 71), (-105, 68), (-92, 66),
     (-85, 64), (-79, 62), (-76, 60), (-71, 57), (-66, 52), (-70, 46),
     (-73, 42), (-75, 38), (-76, 34), (-79, 33), (-81, 30), (-80, 25),
     (-82, 23), (-84, 20), (-87, 21), (-90, 20), (-91, 19), (-94, 17),
     (-97, 16), (-100, 17), (-105, 20), (-108, 23), (-110, 24), (-114, 29),
     (-117, 33), (-121, 34), (-124, 40), (-124, 46), (-127, 52), (-133, 57),
     (-147, 60), (-158, 58), (-165, 60)],
    [(-45, 60), (-30, 68), (-22, 70), (-20, 76), (-28, 80), (-45, 80),
     (-55, 76), (-55, 68)],
    [(-77, 7), (-70, 11), (-64, 10), (-60, 8), (-52, 5), (-50, 0), (-44, -3),
     (-38, -5), (-39, -13), (-41, -22), (-48, -28), (-52, -33), (-57, -38),
     (-62, -41), (-65, -45), (-67, -50), (-68, -54), (-71, -54), (-73, -50),
     (-73, -44), (-73, -37), (-71, -30), (-70, -22), (-70, -18), (-75, -15),
     (-79, -8), (-80, -4), (-78, 1)],
    [(-17, 15), (-10, 29), (-6, 33), (-2, 35), (10, 37), (11, 34), (20, 32),
     (30, 31), (34, 28), (35, 24), (38, 22), (40, 15), (43, 12), (48, 11),
     (51, 12), (46, 5), (42, -2), (40, -8), (39, -15), (37, -20), (35, -24),
     (32, -29), (27, -34), (20, -35), (17, -32), (14, -26), (12, -18),
     (13, -12), (12, -6), (9, -1), (9, 4), (6, 4), (-3, 5), (-8, 5),
     (-13, 8), (-17, 12)],
    [(-9, 37), (-9, 43), (-2, 44), (0, 46), (-4, 48), (-1, 50), (3, 51),
     (7, 54), (8, 57), (12, 55), (18, 56), (21, 59), (19, 61), (24, 65),
     (30, 70), (45, 68), (60, 69), (75, 72), (95, 76), (110, 74), (130, 72),
     (150, 70), (165, 69), (178, 66), (172, 62), (162, 58), (156, 51),
     (150, 49), (142, 51), (141, 46), (143, 42), (138, 36), (133, 34),
     (129, 33), (126, 38), (122, 37), (120, 32), (121, 27), (117, 24),
     (110, 20), (108, 14), (106, 8), (104, 3), (101, 6), (99, 10), (97, 15),
     (93, 17), (90, 22), (87, 21), (84, 19), (80, 14), (77, 8), (75, 13),
     (72, 19), (69, 22), (64, 25), (59, 25), (54, 26), (51, 28), (49, 30),
     (50, 25), (53, 24), (55, 25), (57, 22), (55, 17), (53, 15), (48, 13),
     (44, 12), (42, 15), (39, 20), (36, 24), (34, 28), (33, 29), (36, 36),
     (30, 36), (27, 37), (22, 37), (19, 40), (15, 38), (12, 38), (10, 37),
     (3, 37), (-2, 37)],
    [(-5, 50), (-3, 53), (-2, 55), (-4, 58), (-6, 58), (-8, 55), (-6, 52)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (140, 45), (138, 40), (135, 34), (131, 32)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -9),
     (125, -10), (131, -9), (136, -8), (141, -6), (147, -7), (150, -9),
     (146, -10), (140, -10), (134, -11), (128, -11), (122, -11), (116, -10),
     (110, -9), (104, -6), (99, -1), (95, 2)],
    [(109, 1), (113, 4), (117, 6), (119, 2), (117, -2), (113, -3), (110, -1)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (151, -24), (146, -19), (142, -11), (142, -15),
     (141, -17), (140, -20), (136, -15), (135, -12), (132, -11), (130, -12),
     (126, -14), (122, -17), (118, -20)],
]

MAP_PINS = [
    (1, 56, 26), (2, 47, 25), (3, -78, 38), (4, 4, 53), (5, -72, 43),
    (6, -70, 39), (7, 29, 1), (8, -81, 42), (9, 34, 31), (10, 31, 50),
    (11, 7, 50),
]
LON0, LON1, LAT0, LAT1 = -168, 192, 84, -60
MCOLS, MROWS, MCELL = 71, 18, 6


def _inside(px, py, poly):
    c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and \
                (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            c = not c
        j = i
    return c


def world_map(d, x, y):
    w, h = MCOLS * MCELL, MROWS * MCELL
    d.rectangle([x, y, x + w, y + h], fill=NAVY2)
    for r in range(MROWS):
        lat = LAT0 - (r + 0.5) * (LAT0 - LAT1) / MROWS
        for c in range(MCOLS):
            lon = LON0 + (c + 0.5) * (LON1 - LON0) / MCOLS
            cx, cy = x + c * MCELL, y + r * MCELL
            if any(_inside(lon, lat, p) for p in CONTINENTS):
                d.ellipse([cx + 1, cy + 1, cx + MCELL - 1, cy + MCELL - 1],
                          fill=(240, 230, 200))
            else:
                d.ellipse([cx + 2.5, cy + 2.5, cx + MCELL - 2.5,
                           cy + MCELL - 2.5], fill=(70, 120, 160))
    f_pin = F(SANSB, 7)
    for n, lon, lat in MAP_PINS:
        c = (lon - LON0) / (LON1 - LON0) * MCOLS
        r = (LAT0 - lat) / (LAT0 - LAT1) * MROWS
        px, py = x + c * MCELL, y + r * MCELL
        d.ellipse([px - 5.5, py - 5.5, px + 5.5, py + 5.5], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        d.text((px - d.textlength(t, font=f_pin) / 2, py - 3.5), t,
               font=f_pin, fill=(255, 255, 255))
    return h


# ---------------------------------------------------------------- layout

def header(d):
    f_kick = F(SANSB, 10)
    d.text((M, 8), "ONE DAY OF WORLD NEWS", font=f_kick, fill=RED)
    right = ("28 STORIES · 6 REGIONS · 11 ILLUSTRATED · EVERY ONE FROM "
             "TUESDAY 24 NOVEMBER 2026")
    d.text((W - M - d.textlength(right, font=f_kick), 8), right,
           font=f_kick, fill=INK)
    d.line([M, 22, W - M, 22], fill=INK, width=2)
    d.text((M, 27), "Tuesday 24 November 2026", font=F(SERIF, 45), fill=INK)
    brand = "THE WORLD IN ONE DAY"
    f_brand = F(SERIF, 13)
    bw = d.textlength(brand, font=f_brand) + 22
    d.rectangle([W - M - bw, 32, W - M, 58], fill=RED)
    d.text((W - M - bw + 11, 38), brand, font=f_brand, fill=(255, 255, 255))
    sub = ("Iran names its price for Hormuz · a drone finds Riyadh's "
           "tallest tower · a US jury finds Huawei guilty")
    d.text((M, 76), sub, font=F(SANS, 12.5), fill=GREY)
    d.line([M, 94, W - M, 94], fill=GOLD, width=2)
    return 98


def region_tabs(d, y):
    f_tab = F(SANSB, 10.5)
    gap = 6
    widths = []
    for name, _col, n in REGIONS:
        widths.append(d.textlength(f"{name} {n}", font=f_tab) + 20)
    total = sum(widths) + gap * (len(REGIONS) - 1)
    scale = (W - 2 * M) / total
    x = M
    for (name, col, n), w0 in zip(REGIONS, widths):
        w = w0 * scale
        d.rectangle([x, y, x + w, y + 20], fill=col)
        t = f"{name} {n}"
        d.text((x + (w - d.textlength(t, font=f_tab)) / 2, y + 4.5), t,
               font=f_tab, fill=(255, 255, 255))
        x += w + gap
    d.text((x + 2, y + 4.5), "= 28", font=F(SANSB, 10.5), fill=INK)
    return y + 23


def numbers_strip(d, y):
    d.rectangle([M, y, W - M, y + 46], fill=NAVY)
    d.rectangle([M, y, W - M, y + 3], fill=GOLD)
    f_num = F(SANSB, 21)
    f_lab = F(SANSB, 7.5)
    colw = (W - 2 * M) / 5
    for i, (num, lab) in enumerate(NUMBERS):
        x = M + i * colw + 12
        d.text((x, y + 4), num, font=f_num, fill=(255, 214, 120))
        ly = y + 27
        for ln in lab.split("\n"):
            d.text((x, ly), ln, font=f_lab, fill=(235, 240, 248))
            ly += 9.5
        if i:
            d.line([M + i * colw, y + 6, M + i * colw, y + 40],
                   fill=(90, 120, 155), width=1)
    d.text((M, y - 13), "IN NUMBERS", font=F(SANSB, 9), fill=RED)
    return y + 48


def tile(d, x, y, w, num, t, big):
    region, rcol, status, scol, banner, bcol, head, body, scene = t
    scene_h = 96 if big else 56
    SCENES[scene](d, x, y, w, scene_h)
    d.rectangle([x, y, x + w, y + scene_h], outline=RULE, width=1)
    f_num = F(SANSB, 12 if big else 10.5)
    r = 11 if big else 9.5
    d.ellipse([x + 5, y + 5, x + 5 + 2 * r, y + 5 + 2 * r], fill=GOLD,
              outline=(255, 255, 255), width=2)
    ns = str(num)
    d.text((x + 5 + r - d.textlength(ns, font=f_num) / 2, y + 5 + r - 7),
           ns, font=f_num, fill=INK)
    f_ban = F(SANSB, 9.5 if big else 8.5)
    d.rectangle([x, y + scene_h - 15, x + w, y + scene_h], fill=bcol)
    d.text((x + 7, y + scene_h - 12.5), banner, font=f_ban,
           fill=(255, 255, 255))
    ry = y + scene_h + 4
    d.text((x, ry), region, font=F(SANSB, 8.5), fill=rcol)
    f_st = F(SANSB, 8)
    sw = d.textlength(status, font=f_st) + 10
    d.rounded_rectangle([x + w - sw, ry - 2, x + w, ry + 11], 2, fill=scol)
    d.text((x + w - sw + 5, ry + 0.5), status, font=f_st,
           fill=(255, 255, 255))
    hy = para(d, x, ry + 14, head,
              F(SERIF, 16 if big else 12.5), w, 19 if big else 15,
              max_lines=2)
    para(d, x, hy + 1, body, F(SANS, 11.5 if big else 10), w,
         14 if big else 12.5, max_lines=4 if big else 2)
    return (scene_h + 4 + 14 + (38 if big else 30) +
            (57 if big else 26) + 2)


def bottom_band(d, y):
    d.rectangle([M, y, W - M, y + 16], fill=NAVY2)
    d.text((M + 10, y + 3), "ALSO ON TUESDAY — 17 MORE, BY REGION",
           font=F(SANSB, 10.5), fill=(255, 255, 255))
    map_title = "WHERE IT HAPPENED — PINS 1–11"
    d.text((W - M - d.textlength(map_title, font=F(SANSB, 10.5)), y + 3),
           map_title, font=F(SANSB, 10.5), fill=(255, 214, 120))
    y += 20
    list_w = W - 2 * M - 446
    colw = (list_w - 12) / 2
    f_txt = F(SANS, 9.5)
    f_num = F(SANSB, 9.5)
    ys = [y, y]
    half = (len(LIST_ITEMS) + 1) // 2
    for i, (code, col, text) in enumerate(LIST_ITEMS):
        c = 0 if i < half else 1
        x = M + c * (colw + 12)
        yy = ys[c]
        n = str(12 + i)
        d.text((x, yy), n, font=f_num, fill=RED)
        d.rectangle([x + 17, yy + 1, x + 37, yy + 12], fill=col)
        d.text((x + 20, yy + 2.5), code, font=F(SANSB, 7.5),
               fill=(255, 255, 255))
        yy = para(d, x + 42, yy, text, f_txt, colw - 42, 11.5, max_lines=3)
        ys[c] = yy + 3
    mx = W - M - MCOLS * MCELL
    mh = world_map(d, mx, y)
    f_leg = F(SANSB, 8.5)
    lx = mx
    ly = y + mh + 5
    for name, col, n in REGIONS:
        t = f"{name} {n}"
        tw = d.textlength(t, font=f_leg)
        if lx + tw + 14 > W - M:
            lx = mx
            ly += 13
        d.rectangle([lx, ly + 1, lx + 9, ly + 10], fill=col)
        d.text((lx + 12, ly), t, font=f_leg, fill=INK)
        lx += tw + 22
    ly += 20
    d.rectangle([mx, ly, W - M, ly + 56], fill=CREAM, outline=RED, width=2)
    para(d, mx + 8, ly + 4, DATE_CHECK, F(SANS, 9.5), MCOLS * MCELL - 16,
         11.5, max_lines=4)
    return max(max(ys), ly + 60)


def footer(d, y):
    d.rectangle([M, y, W - M, y + 30], fill=CREAM, outline=RED, width=2)
    para(d, M + 10, y + 4, DATE_CHECK, F(SANS, 10), W - 2 * M - 20, 12,
         max_lines=2)
    return y + 34


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = header(d)
    y = region_tabs(d, y + 2)
    y = numbers_strip(d, y + 14)
    gap = 10
    bw = (W - 2 * M - 2 * gap) / 3
    bh = 0
    for i, t in enumerate(BIG_TILES):
        bh = tile(d, M + i * (bw + gap), y, bw, i + 1, t, True)
    y += bh + 6
    gap2 = 9
    sw = (W - 2 * M - 3 * gap2) / 4
    for r in range(2):
        sh = 0
        for c in range(4):
            idx = r * 4 + c
            sh = tile(d, M + c * (sw + gap2), y, sw, 4 + idx,
                      SMALL_TILES[idx], False)
        y += sh + 7
    y = bottom_band(d, y + 2)
    img.save("entry.png", optimize=True)
    print("entry.png written, layout ends at y =", y)


if __name__ == "__main__":
    main()

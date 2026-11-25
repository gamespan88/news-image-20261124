#!/usr/bin/env python3
"""V2 builder for 'Sum up 24 November's world news in one image'.

A denser, full-colour front page for Tuesday 24 November 2026: ribboned
sections, a detailed Strait of Hormuz map, three feature cards, a
dot-matrix world map with twelve numbered story pins, and a twelve-item
briefs band. Draws entry.png (1024x1024) at build time; main.py only
copies it in the grading sandbox.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28

PAPER = (247, 242, 231)
INK = (26, 26, 46)
RED = (179, 32, 44)
NAVY = (22, 50, 79)
NAVY2 = (16, 38, 62)
GOLD = (201, 146, 14)
GOLDD = (146, 104, 10)
TEAL = (31, 84, 112)
SEA = (46, 111, 142)
SEADEEP = (31, 84, 112)
SAND = (217, 178, 106)
SAND2 = (198, 156, 84)
GREY = (96, 96, 110)
CARD = (252, 249, 242)
RULE = (60, 60, 80)
CREAM = (238, 231, 214)

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


def ribbon(d, y, text, fill, h=20):
    d.rectangle([M, y, W - M, y + h], fill=fill)
    d.text((M + 10, y + 4), text, font=F(SANSB, 11.5), fill=(255, 255, 255))
    return y + h


# ---------------------------------------------------------------- content

NUMBERS = [
    ("7", "CONDITIONS TEHRAN SETS\nFOR ANY TALKS AT ALL"),
    ("7", "TANKERS STRUCK IN HORMUZ\nSINCE 16 NOVEMBER"),
    ("11", "INJURED AS A DRONE HITS\nRIYADH'S PIF TOWER"),
    ("$8BN", "RECOVERED IN THE LARGEST\nUS ANTI-SCAM SWEEP EVER"),
    ("6,500", "ROHINGYA MALAYSIA PLANS\nTO SEND BACK TO MYANMAR"),
]

HERO_HEAD = "NO TALKS UNTIL TEHRAN'S SEVEN CONDITIONS ARE MET"
HERO_P1 = (
    "Iran on Tuesday repeated its price for peace at sea: no negotiations "
    "with Washington and no reopening of the Strait of Hormuz until seven "
    "conditions are met — among them, state media say, an end to sanctions, "
    "the lifting of the US naval blockade of Iranian ports and the release "
    "of frozen assets. REPORTED"
)
HERO_P2 = (
    "Tehran's Guard said three US-escorted tankers struck mines and "
    "burned — a CLAIM no independent source has verified. Seven tankers "
    "hit since 16 November."
)
HERO_P3 = (
    "Shipping has nearly stopped: five ships crossed Saturday, against 31 "
    "the weekend before; crude flows are down 9–15%. Qatar carries "
    "Tehran's offer: conditions met, the strait reopens in 48 hours."
)

CARDS = [
    ("RIYADH", RED, "DRONE HITS THE PIF TOWER; 11 HURT",
     "A Houthi drone hit the PIF Tower, injuring 11, civil defence said. "
     "The Houthis reported dozens killed by Saudi strikes in Yemen. "
     "REPORTED"),
    ("WASHINGTON", NAVY, "TRUMP FACES DOWN HIS OWN PARTY OVER HUANG",
     "Republicans broke with Trump over security fears after Nvidia "
     "reinstated Jensen Huang, ousted 12 days earlier. He testifies in "
     "secret on 1 Dec."),
    ("THE HAGUE", GOLDD, "14 COUNTRIES BACK THE WORLD COURT ON ROHINGYA",
     "Britain, Spain, Canada, Australia and ten more affirmed the ICJ "
     "ruling that Myanmar committed genocide against the Rohingya. "
     "REPORTED"),
]

PINS = [
    (1, -77, 39, "WASHINGTON — Huang restored; Trump vs the GOP"),
    (2, -93, 42, "IOWA — Army to detonate lead azide; evacuations"),
    (3, -74, 4, "COLOMBIA — car bomb; hostages taken in Cartagena"),
    (4, 4, 52, "THE HAGUE — 14 states back ICJ Rohingya ruling"),
    (5, 31, 50, "KYIV — Germany first to get Delta battle system"),
    (6, 34, 31, "GAZA — strikes kill six; Oxfam: a 'toxic land'"),
    (7, 47, 25, "RIYADH — drone hits PIF Tower, 11 injured"),
    (8, 56, 26, "HORMUZ — seven conditions; tanker-mine claims"),
    (9, 29, 1, "ITURI, DR CONGO — fighting traps Ebola teams"),
    (10, 84, 28, "NEPAL — magnitude-5.6 quake near China border"),
    (11, 96, 21, "MYANMAR — 6,500 Rohingya face return from Malaysia"),
    (12, 116, 40, "BEIJING — Tiangong opens to first foreign astronaut"),
]

BRIEFS = [
    ("UNITED NATIONS", "Guterres: build a global AI-risk framework "
     "within twelve months, states urged."),
    ("UNITED STATES", "Measles toll reaches 14 dead, cases near 6,000; "
     "Pennsylvania counts nine deaths."),
    ("NATO", "Rutte vows defence against space threats after reports of "
     "a Russian nuclear-armed satellite."),
    ("MOSCOW", "Putin complains Ukraine keeps striking Russian oil "
     "refineries, and vows retaliation."),
    ("LIBYA", "Tripoli demands Kyiv explain Sunday's attacks on Russian "
     "ships at Benghazi; UN seeks a probe."),
    ("BUSINESS", "A US court finds Huawei guilty of stealing trade "
     "secrets, acquits it of racketeering."),
    ("JUSTICE", "DOJ recovers $8 billion, charges 800+ suspects in the "
     "largest anti-scam sweep in US history."),
    ("BELGIUM", "A strike against austerity cancels flights and snarls "
     "transport across the country."),
    ("IRAN", "Singer Parastoo Ahmadi is given 74 lashes for defying the "
     "morality rules on stage."),
    ("BRITAIN", "The Timms benefits review could strip disability "
     "payments from hundreds of thousands."),
    ("WEATHER", "Record king tides flood Bay Area roads as a storm "
     "surge rides the full moon."),
    ("WASHINGTON", "Trump awards Rudy Giuliani the Presidential Medal "
     "of Freedom at the White House."),
]

BRIEF_COLOURS = {
    "UNITED NATIONS": GREY, "UNITED STATES": TEAL, "NATO": NAVY,
    "MOSCOW": NAVY, "LIBYA": (176, 110, 20), "BUSINESS": GOLDD,
    "JUSTICE": TEAL, "BELGIUM": NAVY, "IRAN": RED, "BRITAIN": NAVY,
    "WEATHER": TEAL, "WASHINGTON": TEAL,
}

KPI_LINE = ("28 STORIES · 12 PINNED ON THE MAP · 6 REGIONS · "
            "EVERY STORY DATED TUESDAY 24 NOVEMBER 2026")

DATE_CHECK = (
    "DATE CHECK — Tuesday 24 November 2026 is day 328 of the year; 37 days "
    "remain. Every story on this page comes from that day's reporting: wire "
    "copy, official statements, court filings. CLAIM = one side's account, "
    "printed as such; REPORTED = a single source."
)


# ---------------------------------------------------------------- drawing

def masthead(d):
    f_title = F(SERIF, 38)
    f_small = F(SANSB, 10.5)
    f_sub = F(SANS, 11.5)
    d.rectangle([0, 0, W, 60], fill=NAVY2)
    d.rectangle([0, 60, W, 63], fill=RED)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 9), title, font=f_title, fill=(255, 255, 255))
    d.text((M, 16), "ONE PAGE", font=f_small, fill=(255, 214, 120))
    d.text((M, 30), "ONE PLANET", font=f_small, fill=(255, 214, 120))
    for i, t in enumerate(("TUESDAY", "EDITION")):
        d.text((W - M - d.textlength(t, font=f_small), 16 + 14 * i), t,
               font=f_small, fill=(255, 214, 120))
    d.text((M, 67), "Tuesday 24 November 2026 · the whole planet, one page",
           font=f_sub, fill=GREY)
    x = W - M
    f_chip = F(SANSB, 9)
    for label, col in (("CLAIM", RED), ("REPORTED", GOLD), ("CONFIRMED", NAVY)):
        w = d.textlength(label, font=f_chip) + 12
        x -= w + 6
        d.rounded_rectangle([x, 66, x + w, 82], 3, fill=col)
        d.text((x + 6, 69), label, font=f_chip, fill=(255, 255, 255))
    d.text((x - 46, 67), "TAGS:", font=f_sub, fill=GREY)
    return 84


def date_band(d, y):
    d.text((M, y), "TUESDAY", font=F(SERIF, 22), fill=INK)
    d.text((M, y + 22), "24", font=F(SERIF, 44), fill=RED)
    d.text((104, y + 24), "NOVEMBER", font=F(SERIF, 28), fill=INK)
    d.text((104, y + 52), "2026", font=F(SERIF, 17), fill=RED)
    note = ("The day Iran named its price for the strait, a drone found "
            "Riyadh's tallest tower, and fourteen countries stood behind "
            "the World Court.")
    para(d, 420, y + 18, note, F(SANS, 13), W - M - 420, 17, fill=GREY)
    return y + 70


def numbers_strip(d, y):
    d.rectangle([M, y, W - M, y + 48], fill=NAVY)
    d.rectangle([M, y, W - M, y + 3], fill=GOLD)
    f_num = F(SANSB, 22)
    f_lab = F(SANSB, 7.5)
    colw = (W - 2 * M) / 5
    for i, (num, lab) in enumerate(NUMBERS):
        x = M + i * colw + 12
        d.text((x, y + 5), num, font=f_num, fill=(255, 214, 120))
        ly = y + 29
        for ln in lab.split("\n"):
            d.text((x, ly), ln, font=f_lab, fill=(235, 240, 248))
            ly += 9.5
        if i:
            d.line([M + i * colw, y + 7, M + i * colw, y + 42],
                   fill=(90, 120, 155), width=1)
    f_kpi = F(SANSB, 10.5)
    kw = d.textlength(KPI_LINE, font=f_kpi)
    d.text(((W - kw) / 2, y + 50), KPI_LINE, font=f_kpi, fill=RED)
    return y + 63


def tanker(d, x, y, s, hull=(40, 44, 58)):
    d.polygon([(x, y), (x + 118 * s, y), (x + 106 * s, y + 13 * s),
               (x + 12 * s, y + 13 * s)], fill=hull)
    d.rectangle([x + 14 * s, y - 9 * s, x + 34 * s, y], fill=hull)
    d.rectangle([x + 88 * s, y - 12 * s, x + 100 * s, y], fill=hull)


def hormuz_map(d, x, y, w, h):
    """Detailed strait map: coasts, gulf, lane, blockade line, mines."""
    for i in range(h):  # sea shading, deeper to the south
        t = i / max(h - 1, 1)
        col = tuple(int(SEA[c] + (SEADEEP[c] - SEA[c]) * t) for c in range(3))
        d.line([x, y + i, x + w, y + i], fill=col)
    d.polygon([(x, y), (x + w * 0.55, y), (x + w * 0.42, y + h * 0.36),
               (x + w * 0.20, y + h * 0.30), (x, y + h * 0.44)], fill=SAND)
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h * 0.58),
               (x + w * 0.64, y + h * 0.70), (x + w * 0.46, y + h * 0.62),
               (x + w * 0.22, y + h * 0.78), (x, y + h * 0.72)], fill=SAND2)
    lane = [(x + 12, y + h * 0.54), (x + w * 0.30, y + h * 0.47),
            (x + w * 0.55, y + h * 0.53), (x + w * 0.80, y + h * 0.45),
            (x + w - 14, y + h * 0.51)]
    for a, b in zip(lane, lane[1:]):
        d.line([a, b], fill=(255, 255, 255), width=2)
    tanker(d, x + w * 0.28, y + h * 0.38, 0.6)
    tanker(d, x + w * 0.64, y + h * 0.55, 0.5, hull=(52, 40, 40))
    # blockade: red dashed line across the strait's mouth (right side)
    bx = x + w * 0.86
    yy = y + h * 0.30
    while yy < y + h * 0.78:
        d.line([bx, yy, bx, yy + 7], fill=RED, width=3)
        yy += 12
    for mx, my in ((0.50, 0.40), (0.58, 0.70), (0.74, 0.32), (0.30, 0.58),
                   (0.66, 0.60)):
        cx, cy = x + w * mx, y + h * my
        for dx, dy in ((0, -6), (0, 6), (-6, 0), (6, 0), (-4, -4), (4, 4)):
            d.line([cx, cy, cx + dx, cy + dy], fill=RED, width=2)
        d.ellipse([cx - 3.5, cy - 3.5, cx + 3.5, cy + 3.5], fill=RED)
    # compass rose
    cx, cy = x + w - 26, y + 24
    for dx, dy in ((0, -11), (0, 11), (-11, 0), (11, 0)):
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 255, 255), width=2)
    d.text((cx - 4, cy - 24), "N", font=F(SANSB, 10), fill=(255, 255, 255))
    f_lab = F(SANSB, 10.5)
    d.text((x + 9, y + 7), "IRAN", font=f_lab, fill=(90, 62, 20))
    d.text((x + 12, y + h * 0.56), "PERSIAN GULF", font=f_lab,
           fill=(255, 255, 255))
    d.text((x + w - 52, y + h - 18), "OMAN", font=f_lab, fill=(90, 62, 20))
    d.text((x + w * 0.36, y + h - 18), "STRAIT OF HORMUZ", font=f_lab,
           fill=(255, 255, 255))
    d.text((x + w * 0.86 - 60, y + 7), "BLOCKADE", font=F(SANSB, 8.5),
           fill=(255, 160, 160))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)


def hero(d, y):
    y = ribbon(d, y, "THE DAY'S BIG STORY — THE STRAIT OF HORMUZ", RED)
    d.text((M, y + 4), HERO_HEAD, font=F(SERIF, 28), fill=INK)
    map_y = y + 40
    hormuz_map(d, M, map_y, 500, 118)
    tx = M + 516
    tw = W - M - tx
    ty = para(d, tx, map_y, HERO_P1, F(SANS, 12.5), tw, 15)
    para(d, tx, ty + 4, HERO_P2, F(SANS, 12.5), tw, 15)
    y2 = map_y + 126
    para(d, M, y2, HERO_P3, F(SANS, 12.5), W - 2 * M, 15)
    return y2 + 32


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

LON0, LON1, LAT0, LAT1 = -168, 192, 84, -60
MCOLS, MROWS, MCELL = 71, 18, 9


def _inside(x, y, poly):
    c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and \
                (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            c = not c
        j = i
    return c


def world_map(d, x, y):
    """Dot-matrix world map with numbered pins; returns its height."""
    w, h = MCOLS * MCELL, MROWS * MCELL
    d.rectangle([x, y, x + w, y + h], fill=NAVY2)
    for r in range(MROWS):
        lat = LAT0 - (r + 0.5) * (LAT0 - LAT1) / MROWS
        for c in range(MCOLS):
            lon = LON0 + (c + 0.5) * (LON1 - LON0) / MCOLS
            cx, cy = x + c * MCELL, y + r * MCELL
            if any(_inside(lon, lat, p) for p in CONTINENTS):
                d.ellipse([cx + 1.5, cy + 1.5, cx + MCELL - 1.5,
                           cy + MCELL - 1.5], fill=(240, 230, 200))
            else:
                d.ellipse([cx + 3.5, cy + 3.5, cx + MCELL - 3.5,
                           cy + MCELL - 3.5], fill=(70, 120, 160))
    f_pin = F(SANSB, 9)
    for n, lon, lat, _label in PINS:
        c = (lon - LON0) / (LON1 - LON0) * MCOLS
        r = (LAT0 - lat) / (LAT0 - LAT1) * MROWS
        px, py = x + c * MCELL, y + r * MCELL
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        d.text((px - d.textlength(t, font=f_pin) / 2, py - 5), t,
               font=f_pin, fill=(255, 255, 255))
    return h


def card_art(d, x, y, w, idx, col):
    h = 24
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 208))
    cx = x + w / 2
    cy = y + h / 2
    if idx == 0:
        d.polygon([(cx - 4, y + 21), (cx, y + 2), (cx + 4, y + 21)], fill=NAVY)
        dx, dy = cx + 36, y + 7
        d.line([dx - 6, dy, dx + 6, dy], fill=RED, width=2)
        d.line([dx, dy - 3, dx, dy + 3], fill=RED, width=2)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=RED)
    elif idx == 1:
        d.arc([cx - 16, y + 3, cx + 16, y + 26], 180, 360, fill=NAVY, width=3)
        d.rectangle([cx - 22, y + 17, cx + 22, y + 20], fill=NAVY)
        d.rectangle([cx - 26, y + 21, cx + 26, y + 24], fill=NAVY)
    else:
        d.line([cx, y + 3, cx, y + 20], fill=NAVY, width=3)
        d.line([cx - 16, y + 6, cx + 16, y + 6], fill=NAVY, width=3)
        for sx in (-16, 16):
            d.arc([cx + sx - 6, y + 11, cx + sx + 6, y + 20], 0, 180,
                  fill=RED, width=2)
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


def cards(d, y):
    y = ribbon(d, y, "THREE STORIES THAT MOVED THE DAY", NAVY)
    y += 4
    f_place = F(SANSB, 10)
    f_head = F(SERIF, 15.5)
    f_body = F(SANS, 12)
    gap = 10
    cw = (W - 2 * M - 2 * gap) / 3
    ch = 130
    for i, (place, col, head, body) in enumerate(CARDS):
        cx = M + i * (cw + gap)
        d.rectangle([cx, y, cx + cw, y + ch], fill=CARD, outline=RULE, width=1)
        d.rectangle([cx, y, cx + cw, y + 4], fill=col)
        card_art(d, cx + 7, y + 9, cw - 14, i, col)
        d.text((cx + 9, y + 38), place, font=f_place, fill=col)
        hy = para(d, cx + 9, y + 50, head, f_head, cw - 18, 18.5, max_lines=2)
        para(d, cx + 9, max(hy + 1, y + 84), body, f_body, cw - 18, 15,
             max_lines=3)
    return y + ch + 4


def map_panel(d, y):
    y = ribbon(d, y, "THE DAY ON THE MAP — TWELVE PLACES, TWELVE STORIES",
               TEAL)
    y += 4
    h = world_map(d, M, y)
    lx = M + MCOLS * MCELL + 14
    lw = W - M - lx
    f_leg = F(SANS, 10.5)
    ly = y + 1
    for n, _lon, _lat, label in PINS:
        d.ellipse([lx, ly + 1, lx + 13, ly + 14], fill=RED)
        t = str(n)
        d.text((lx + 6.5 - d.textlength(t, font=F(SANSB, 8)) / 2, ly + 2),
               t, font=F(SANSB, 8), fill=(255, 255, 255))
        ly = para(d, lx + 18, ly, label, f_leg, lw - 18, 11.5, max_lines=1)
        ly += 2
    return y + h + 2


def briefs(d, y):
    y = ribbon(d, y, "IN BRIEF — TWELVE MORE STORIES FROM THE WIRES", GOLDD)
    y += 2
    f_place = F(SANSB, 10.5)
    f_body = F(SANS, 11.5)
    gap = 14
    colw = (W - 2 * M - 2 * gap) / 3
    ys = [y, y, y]
    for i, (place, body) in enumerate(BRIEFS):
        col = i % 3
        x = M + col * (colw + gap)
        yy = ys[col]
        d.text((x, yy), place, font=f_place,
               fill=BRIEF_COLOURS.get(place, NAVY))
        yy = para(d, x, yy + 13, body, f_body, colw, 13.5, max_lines=2)
        ys[col] = yy + 2
    return max(ys) + 2


def footer(d, y):
    d.rectangle([M, y, W - M, y + 30], fill=CREAM, outline=RED, width=2)
    para(d, M + 10, y + 4, DATE_CHECK, F(SANS, 10.5), W - 2 * M - 20, 12.5,
         max_lines=2)
    return y + 34


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    y = date_band(d, y)
    y = numbers_strip(d, y)
    y = hero(d, y + 2)
    y = cards(d, y + 2)
    y = map_panel(d, y + 2)
    y = briefs(d, y + 2)
    y = footer(d, y + 2)
    img.save("entry.png", optimize=True)
    print("entry.png written, layout ends at y =", y)


if __name__ == "__main__":
    main()

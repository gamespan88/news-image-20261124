#!/usr/bin/env python3
"""Build the entry page for 'Sum up 24 November's world news in one image'.

Draws a complete one-page newspaper for Tuesday 24 November 2026 at
1024x1024 with Pillow and writes entry.png next to this file. The shipped
entrypoint (main.py) only copies the finished entry.png to /output; all
drawing happens here, at build time, because the grading sandbox has no
imaging library.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28  # page margin

PAPER = (247, 242, 231)
INK = (26, 26, 46)
RED = (179, 32, 44)
NAVY = (22, 50, 79)
GOLD = (201, 146, 14)
SEA = (46, 111, 142)
SAND = (217, 178, 106)
SAND2 = (198, 156, 84)
GREY = (96, 96, 110)
CARD = (252, 249, 242)
RULE = (60, 60, 80)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
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
    """Draw a wrapped paragraph; returns the y just below it."""
    lines = wrap(d, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += pitch
    return y


# ---------------------------------------------------------------- content

NUMBERS = [
    ("7", "CONDITIONS TEHRAN SETS\nFOR ANY TALKS AT ALL"),
    ("7", "TANKERS STRUCK IN HORMUZ\nSINCE 16 NOVEMBER"),
    ("11", "INJURED AS A DRONE HITS\nRIYADH'S PIF TOWER"),
    ("$8BN", "RECOVERED IN THE LARGEST\nUS ANTI-SCAM SWEEP EVER"),
    ("6,500", "ROHINGYA MALAYSIA PLANS\nTO SEND BACK TO MYANMAR"),
]

HERO_KICKER = "THE DAY'S BIG STORY — THE STRAIT OF HORMUZ"
HERO_HEAD = "NO TALKS UNTIL TEHRAN'S SEVEN CONDITIONS ARE MET"
HERO_P1 = (
    "Iran on Tuesday repeated its price for peace at sea: no negotiations "
    "with Washington and no reopening of the Strait of Hormuz until seven "
    "conditions are met — among them, state media say, an end to sanctions, "
    "the lifting of the US naval blockade of Iranian ports and the release "
    "of frozen assets. REPORTED"
)
HERO_P2 = (
    "Tehran's Revolutionary Guard said three US-escorted tankers struck "
    "mines and burned — a CLAIM no independent source has verified. Seven "
    "tankers hit since 16 November; the blockade was tightened Tuesday."
)
HERO_P3 = (
    "Shipping has nearly stopped: five ships crossed Saturday, against 31 "
    "the weekend before; crude flows are down 9–15%. Qatar carries "
    "Tehran's offer: conditions met, the strait reopens in 48 hours."
)

CARDS = [
    ("RIYADH", "DRONE HITS THE PIF TOWER; 11 HURT",
     "A Houthi drone hit Riyadh's PIF Tower on Tuesday, injuring 11, civil "
     "defence said. The Houthis reported dozens killed by Saudi strikes "
     "in Yemen. REPORTED"),
    ("WASHINGTON", "TRUMP FACES DOWN HIS OWN PARTY OVER HUANG",
     "Republicans broke with Trump over security fears after Nvidia "
     "reinstated Jensen Huang, ousted 12 days earlier. He testifies in "
     "secret on 1 Dec."),
    ("THE HAGUE", "14 COUNTRIES BACK THE WORLD COURT ON THE ROHINGYA",
     "Britain, Spain, Canada, Australia and ten more states affirmed the "
     "ICJ ruling that Myanmar committed genocide against the Rohingya. "
     "REPORTED"),
    ("UNITED NATIONS", "UN CHIEF: A GLOBAL AI FRAMEWORK WITHIN A YEAR",
     "Secretary-General António Guterres urged member states to build, "
     "within twelve months, a multilateral framework to govern the risks "
     "of AI. REPORTED"),
    ("DR CONGO", "FIGHTING TRAPS EBOLA TEAMS IN ITURI",
     "Heavy fighting near a hospital in Ituri province forced Ebola "
     "response teams to shelter for more than 24 hours, the WHO said."),
    ("UNITED STATES", "MEASLES: 14 DEAD, CASES NEAR 6,000",
     "America's measles epidemic reached 14 deaths, cases nearing 6,000. "
     "Pennsylvania counts nine deaths across 46 counties, from a disease "
     "eliminated in 2000."),
]

BRIEFS = [
    ("GAZA", "Israeli airstrikes killed at least six Palestinians, two of "
     "them police officers, medics said; Oxfam called Gaza a 'toxic land'."),
    ("LIBYA", "Tripoli demanded Kyiv explain Sunday's attacks on Russian "
     "ships at Benghazi; the UN urged an independent probe."),
    ("UKRAINE", "Germany becomes the first country granted access to "
     "Kyiv's Delta battlefield-management system, agreed in Berlin."),
    ("NATO", "Rutte vowed the alliance will defend against threats in "
     "space after reports of a Russian nuclear-armed satellite."),
    ("MOSCOW", "Putin complained Ukraine keeps striking Russian oil "
     "refineries despite Trump's request, and vowed retaliation."),
    ("BUSINESS", "A US court found Huawei guilty of stealing trade "
     "secrets — and acquitted the company of racketeering."),
    ("JUSTICE", "The DOJ recovered $8 billion and charged 800+ suspects "
     "in the largest anti-scam sweep in US history."),
    ("SPACE", "China opened its Tiangong station to a first foreign "
     "astronaut: Pakistan's Zeeshan Ali flies on Shenzhou-24."),
    ("NEPAL", "A magnitude-5.6 earthquake struck Koshi province near the "
     "Chinese border; no toll was confirmed by nightfall."),
    ("COLOMBIA", "A car bomb wrecked buildings in Villavicencio; in "
     "Cartagena, armed men took hostages in the tourist old town."),
    ("IRAN", "Singer Parastoo Ahmadi was given 74 lashes — the latest "
     "sentence against artists who defy the morality rules."),
    ("UNITED STATES", "The Army ordered explosive lead azide detonated in "
     "Iowa, neighbours evacuated; king tides flooded Bay Area roads."),
]

DATE_CHECK = (
    "DATE CHECK — Tuesday 24 November 2026 is day 328 of the year; 37 days "
    "remain. Every story on this page comes from that day's reporting: wire "
    "copy, official statements, court filings. CLAIM = one side's account, "
    "printed as such; REPORTED = a single source."
)

# ---------------------------------------------------------------- drawing

def masthead(d):
    f_title = F(SERIF, 44)
    f_small = F(SANSB, 10.5)
    f_sub = F(SANS, 12)
    d.line([M, 12, W - M, 12], fill=RULE, width=3)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 17), title, font=f_title, fill=INK)
    d.text((M, 30), "ONE PAGE", font=f_small, fill=RED)
    d.text((M, 44), "ONE PLANET", font=f_small, fill=RED)
    for i, t in enumerate(("TUESDAY", "EDITION")):
        d.text((W - M - d.textlength(t, font=f_small), 30 + 14 * i), t,
               font=f_small, fill=RED)
    d.line([M, 70, W - M, 70], fill=RULE, width=2)
    d.text((M, 75), "Tuesday 24 November 2026 · the whole planet, one page",
           font=f_sub, fill=GREY)
    x = W - M
    f_chip = F(SANSB, 9)
    for label, col in (("CLAIM", RED), ("REPORTED", GOLD), ("CONFIRMED", NAVY)):
        w = d.textlength(label, font=f_chip) + 12
        x -= w + 6
        d.rounded_rectangle([x, 74, x + w, 90], 3, fill=col)
        d.text((x + 6, 77), label, font=f_chip, fill=(255, 255, 255))
    d.text((x - 46, 75), "TAGS:", font=f_sub, fill=GREY)
    return 92


def date_band(d, y):
    d.text((M, y + 2), "TUESDAY", font=F(SERIF, 24), fill=INK)
    d.text((M, y + 26), "24", font=F(SERIF, 50), fill=RED)
    d.text((112, y + 30), "NOVEMBER", font=F(SERIF, 30), fill=INK)
    d.text((112, y + 62), "2026", font=F(SERIF, 20), fill=RED)
    note = ("The day Iran named its price for the strait, a drone found "
            "Riyadh's tallest tower, and fourteen countries stood behind "
            "the World Court.")
    para(d, 430, y + 26, note, F(SANS, 13.5), W - M - 430, 18, fill=GREY)
    d.line([M, y + 80, W - M, y + 80], fill=RULE, width=2)
    return y + 86


def numbers_strip(d, y):
    d.rectangle([M, y, W - M, y + 52], fill=NAVY)
    f_num = F(SANSB, 23)
    f_lab = F(SANSB, 8)
    colw = (W - 2 * M) / 5
    for i, (num, lab) in enumerate(NUMBERS):
        x = M + i * colw + 12
        d.text((x, y + 4), num, font=f_num, fill=(255, 214, 120))
        ly = y + 31
        for ln in lab.split("\n"):
            d.text((x, ly), ln, font=f_lab, fill=(235, 240, 248))
            ly += 10
        if i:
            d.line([M + i * colw, y + 6, M + i * colw, y + 46],
                   fill=(90, 120, 155), width=1)
    return y + 58


def tanker(d, x, y, s, hull=(40, 44, 58)):
    d.polygon([(x, y), (x + 118 * s, y), (x + 106 * s, y + 13 * s),
               (x + 12 * s, y + 13 * s)], fill=hull)
    d.rectangle([x + 14 * s, y - 9 * s, x + 34 * s, y], fill=hull)
    d.rectangle([x + 88 * s, y - 12 * s, x + 100 * s, y], fill=hull)


def hero_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.polygon([(x, y), (x + w * 0.52, y), (x + w * 0.40, y + h * 0.34),
               (x + w * 0.18, y + h * 0.30), (x, y + h * 0.42)], fill=SAND)
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h * 0.60),
               (x + w * 0.62, y + h * 0.70), (x + w * 0.44, y + h * 0.62),
               (x + w * 0.20, y + h * 0.78), (x, y + h * 0.72)], fill=SAND2)
    lane = [(x + 12, y + h * 0.52), (x + w * 0.30, y + h * 0.46),
            (x + w * 0.55, y + h * 0.52), (x + w * 0.80, y + h * 0.44),
            (x + w - 14, y + h * 0.50)]
    for a, b in zip(lane, lane[1:]):
        d.line([a, b], fill=(255, 255, 255), width=2)
    tanker(d, x + w * 0.30, y + h * 0.40, 0.55)
    tanker(d, x + w * 0.66, y + h * 0.52, 0.45, hull=(52, 40, 40))
    for mx, my in ((0.50, 0.30), (0.58, 0.68), (0.76, 0.30), (0.22, 0.62)):
        cx, cy = x + w * mx, y + h * my
        for dx, dy in ((0, -6), (0, 6), (-6, 0), (6, 0), (-4, -4), (4, 4)):
            d.line([cx, cy, cx + dx, cy + dy], fill=RED, width=2)
        d.ellipse([cx - 3.5, cy - 3.5, cx + 3.5, cy + 3.5], fill=RED)
    f_lab = F(SANSB, 10.5)
    d.text((x + 9, y + 7), "IRAN", font=f_lab, fill=(90, 62, 20))
    d.text((x + w - 52, y + h - 18), "OMAN", font=f_lab, fill=(90, 62, 20))
    d.text((x + w * 0.38, y + h - 18), "STRAIT OF HORMUZ", font=f_lab,
           fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)


def hero(d, y):
    d.text((M, y), HERO_KICKER, font=F(SANSB, 11.5), fill=RED)
    d.text((M, y + 16), HERO_HEAD, font=F(SERIF, 27), fill=INK)
    art_y = y + 56
    hero_art(d, M, art_y, 420, 76)
    para(d, M + 436, art_y + 2, HERO_P1, F(SANS, 12.5), W - M - (M + 436), 15)
    y2 = art_y + 84
    half = (W - 2 * M - 16) / 2
    para(d, M, y2, HERO_P2, F(SANS, 12.5), half, 15.5)
    para(d, M + half + 16, y2, HERO_P3, F(SANS, 12.5), half, 15.5)
    return y2 + 52


def card_art(d, x, y, w, idx):
    h = 30
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 208))
    cx = x + w / 2
    cy = y + h / 2
    if idx == 0:  # tower + drone
        d.polygon([(cx - 5, y + 27), (cx, y + 3), (cx + 5, y + 27)], fill=NAVY)
        for yy in (11, 17, 23):
            d.line([cx - 2, y + yy, cx + 2, y + yy], fill=(255, 214, 120), width=2)
        dx, dy = cx + 44, y + 9
        d.line([dx - 7, dy, dx + 7, dy], fill=RED, width=2)
        d.line([dx, dy - 4, dx, dy + 4], fill=RED, width=2)
        d.ellipse([dx - 2.5, dy - 2.5, dx + 2.5, dy + 2.5], fill=RED)
        for a in range(0, 360, 45):
            r = a * math.pi / 180
            d.line([cx + 15 + 5 * math.cos(r), cy + 5 * math.sin(r),
                    cx + 15 + 9 * math.cos(r), cy + 9 * math.sin(r)],
                   fill=GOLD, width=2)
    elif idx == 1:  # capitol dome
        d.arc([cx - 20, y + 5, cx + 20, y + 33], 180, 360, fill=NAVY, width=3)
        d.line([cx, y + 1, cx, y + 7], fill=NAVY, width=3)
        d.rectangle([cx - 27, y + 22, cx + 27, y + 25], fill=NAVY)
        d.rectangle([cx - 32, y + 26, cx + 32, y + 29], fill=NAVY)
    elif idx == 2:  # scales
        d.line([cx, y + 4, cx, y + 26], fill=NAVY, width=3)
        d.line([cx - 20, y + 8, cx + 20, y + 8], fill=NAVY, width=3)
        for sx in (-20, 20):
            d.line([cx + sx, y + 8, cx + sx - 5, y + 19], fill=NAVY, width=2)
            d.line([cx + sx, y + 8, cx + sx + 5, y + 19], fill=NAVY, width=2)
            d.arc([cx + sx - 7, y + 14, cx + sx + 7, y + 24], 0, 180,
                  fill=RED, width=3)
        d.rectangle([cx - 11, y + 26, cx + 11, y + 29], fill=NAVY)
    elif idx == 3:  # globe
        d.ellipse([cx - 13, y + 2, cx + 13, y + 28], outline=SEA, width=3)
        d.ellipse([cx - 5, y + 2, cx + 5, y + 28], outline=SEA, width=2)
        d.line([cx - 13, y + 10, cx + 13, y + 10], fill=SEA, width=2)
        d.line([cx - 13, y + 20, cx + 13, y + 20], fill=SEA, width=2)
    elif idx == 4:  # shield cross
        d.polygon([(cx, y + 2), (cx + 13, y + 6), (cx + 13, y + 16),
                   (cx, y + 28), (cx - 13, y + 16), (cx - 13, y + 6)],
                  outline=NAVY, width=3)
        d.rectangle([cx - 2, y + 8, cx + 2, y + 22], fill=RED)
        d.rectangle([cx - 7, y + 13, cx + 7, y + 17], fill=RED)
    else:  # measles spots
        for (ox, oy, r) in ((-24, 9, 5), (-6, 18, 4), (10, 7, 6),
                            (24, 19, 4), (0, 4, 3)):
            d.ellipse([cx + ox - r, y + oy - r, cx + ox + r, y + oy + r],
                      outline=RED, width=2)
            d.ellipse([cx + ox - 1, y + oy - 1, cx + ox + 1, y + oy + 1],
                      fill=RED)
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


def cards(d, y):
    f_place = F(SANSB, 10)
    f_head = F(SERIF, 14.5)
    f_body = F(SANS, 10.5)
    gap = 10
    cw = (W - 2 * M - 2 * gap) / 3
    ch = 120
    for i, (place, head, body) in enumerate(CARDS):
        cx = M + (i % 3) * (cw + gap)
        cy = y + (i // 3) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=RULE, width=1)
        card_art(d, cx + 7, cy + 6, cw - 14, i)
        d.text((cx + 9, cy + 39), place, font=f_place, fill=RED)
        hy = para(d, cx + 9, cy + 51, head, f_head, cw - 18, 16.5, max_lines=2)
        para(d, cx + 9, max(hy + 1, cy + 83), body, f_body, cw - 18, 12,
             max_lines=3)
    return y + 2 * ch + gap + 6


def briefs(d, y):
    d.line([M, y, W - M, y], fill=RULE, width=2)
    d.text((M, y + 4), "THE DAY IN BRIEF — TWELVE MORE STORIES",
           font=F(SANSB, 13), fill=INK)
    y += 24
    f_place = F(SANSB, 10.5)
    f_body = F(SANS, 11)
    colw = (W - 2 * M - 20) / 2
    ys = [y, y]
    for i, (place, body) in enumerate(BRIEFS):
        col = 0 if i < 6 else 1
        x = M + col * (colw + 20)
        yy = ys[col]
        d.text((x, yy), f"{i + 1:02d}", font=f_place, fill=RED)
        d.text((x + 28, yy), place, font=f_place, fill=NAVY)
        yy = para(d, x + 28, yy + 13, body, f_body, colw - 28, 13,
                  max_lines=2)
        ys[col] = yy + 4
    return max(ys) + 2


def footer(d, y):
    d.rectangle([M, y, W - M, y + 34], fill=(238, 231, 214), outline=RED, width=2)
    para(d, M + 10, y + 5, DATE_CHECK, F(SANS, 11), W - 2 * M - 20, 13)
    line = ("THE WORLD IN ONE DAY · one image, one day, the whole planet · "
            "drawn in code for Tuesday 24 November 2026")
    f_foot = F(SANSB, 10)
    tw = d.textlength(line, font=f_foot)
    d.text(((W - tw) / 2, y + 40), line, font=f_foot, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    y = date_band(d, y)
    y = numbers_strip(d, y)
    y = hero(d, y + 2)
    d.line([M, y, W - M, y], fill=RULE, width=2)
    y = cards(d, y + 6)
    y = briefs(d, y)
    footer(d, y)
    img.save("entry.png", optimize=True)
    print("entry.png written, layout ends at y =", y)


if __name__ == "__main__":
    main()

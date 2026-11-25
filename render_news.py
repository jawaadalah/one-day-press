#!/usr/bin/env python3
"""Render the Wednesday 25 November 2026 world-news collage, 1024x1024 PNG.

Original work for make.fun news-image-20261125: a dense dated front page —
masthead, one lead story, then a grid of dated stories from seven regions,
plus a footer strip. Stories are the events first reported on 25 November
2026, paraphrased here from public news digests (Reuters, BBC, UN News,
The Global Eye, Jagran Josh). No copied artwork; every pixel is drawn here.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (10, 25, 49)
ORANGE = (255, 122, 0)
PAPER = (250, 247, 240)
INK = (18, 18, 18)
GREY = (90, 90, 90)
REGION_COLORS = {
    "MIDDLE EAST": (178, 34, 34),
    "EUROPE": (25, 80, 160),
    "ASIA": (0, 128, 96),
    "AFRICA": (150, 90, 10),
    "AMERICAS": (90, 40, 140),
    "TECH": (10, 90, 140),
    "WORLD": (70, 70, 70),
}
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

LEAD_HEAD = "ZELENSKIY CONFIRMS BALTIC SHIP STRIKE"
LEAD_DEK = "Kyiv owns the Gulf of Finland drone hit; Moscow calls it terrorism, Norway urges caution"

STORIES = [
    ("EUROPE", "Zelenskiy confirms ship strike", "Ukraine hit a Russian cargo ship in the Gulf of Finland; Norway urges caution."),
    ("EUROPE", "Russia cries \u2018terrorism\u2019", "Moscow warns of severe consequences after drone strikes on ships in the Baltic and Libya."),
    ("MIDDLE EAST", "Houthis hit Riyadh tower", "Drone attack on the capital\u2019s tallest tower wounds 11, Saudi civil defence says."),
    ("MIDDLE EAST", "Tankers hit by mines in Hormuz", "Iran\u2019s Revolutionary Guard Navy says three oil tankers were struck by naval mines."),
    ("MIDDLE EAST", "Gaza death toll hits 74,746", "WAFA tally rises amid continuing Israeli attacks, UN warns of humanitarian strain."),
    ("MIDDLE EAST", "Iran accuses Bahrain, Kuwait", "Tehran tells the UN both states facilitated US aggression in the Gulf."),
    ("MIDDLE EAST", "Kurds reject oilfield takeover", "Erbil pushes back after Baghdad orders the ministry to run fields in four provinces."),
    ("EUROPE", "UK warns of Russian sabotage", "Defence alert tells Ukraine suppliers to harden against arson and physical threats."),
    ("EUROPE", "Sarkozy case goes to trial", "French officials order corruption trial for the ex-president and Carla Bruni."),
    ("EUROPE", "EU caps Chinese hybrid EVs", "Brussels sets new limits on hybrid imports amid trade tensions with Beijing."),
    ("EUROPE", "Hungary, Ukraine restore ties", "Neighbours agree to reopen links and talk minority rights."),
    ("EUROPE", "NATO plans AWACS for Poland", "Early-warning aircraft to deploy after missiles and a drone entered Polish airspace."),
    ("ASIA", "Huawei guilty of trade theft", "US jury convicts over Iran business; acquitted of racketeering."),
    ("ASIA", "China probes Shanghai chief", "Party leader Chen Jining under investigation, Beijing confirms."),
    ("ASIA", "BJP, Akali Dal reunite", "Punjab alliance returns after a six-year split, ahead of the 2027 polls."),
    ("ASIA", "Malaysia to return migrants", "Kuala Lumpur plans to send Myanmar migrants home."),
    ("AFRICA", "DRC military plane missing", "Aircraft vanishes amid rebel claims in the east, officials say."),
    ("AFRICA", "Libya rejects Ukraine deals", "Tripoli disowns any agreement over the Benghazi attack on a Russian corvette."),
    ("AFRICA", "266m face acute hunger", "WFP warns food insecurity is deepening across conflict zones."),
    ("AMERICAS", "Trump honours Giuliani", "Ex-mayor receives the Presidential Medal of Freedom at the White House."),
    ("AMERICAS", "Fort Hood shooter seeks stay", "Nidal Hasan asks a court to halt his execution, set for next week."),
    ("AMERICAS", "CIA, ODNI hit by breach", "Hackers take unclassified information from US intelligence agencies, source says."),
    ("AMERICAS", "US delays Patriot missiles", "Shipment of 60 missiles to Ukraine held back despite payment received."),
    ("AMERICAS", "Colombia car bomb wounds 25", "Blast in a city centre as armed violence surges."),
    ("AMERICAS", "Nvidia shares fall 7%", "Lawmakers demand answers over Trump\u2019s intervention in the AI chipmaker."),
    ("TECH", "Dell lifts AI forecasts", "Record quarter as AI server demand surges."),
    ("TECH", "US readies new tariffs", "Administration prepares to unveil duties on global trading partners."),
]

FOOTER_EXTRA = "Also 25 Nov: Ukraine seeks $125bn aid for 2027  \u00b7  England beat Australia in 2nd T20I  \u00b7  ~490,000 Russian troops lost, leaked data"
FOOTER_SOURCES = "Sources: Reuters, BBC, UN News, The Global Eye \u2014 25 November 2026"


def make_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, width):
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 96], fill=NAVY)
    draw.text((24, 14), "THE WORLD IN ONE DAY", font=make_font(BOLD, 40), fill=(255, 255, 255))
    draw.text((24, 62), "Wednesday 25 November 2026  \u00b7  27 stories, 7 regions, one day",
              font=make_font(REGULAR, 19), fill=(255, 200, 140))
    draw.rectangle([0, 96, W, 100], fill=ORANGE)


def draw_lead(draw):
    y = 112
    draw.text((24, y), LEAD_HEAD, font=make_font(SERIF_BOLD, 34), fill=INK)
    y += 46
    for line in wrap_text(draw, LEAD_DEK, make_font(REGULAR, 19), 976):
        draw.text((24, y), line, font=make_font(REGULAR, 19), fill=GREY)
        y += 26
    y += 8
    draw.line([24, y, 1000, y], fill=(200, 200, 200), width=2)
    return y + 12


def draw_card(draw, x, y, w, h, region, head, body):
    colour = REGION_COLORS[region]
    draw.rectangle([x, y + 2, x + 5, y + h - 12], fill=colour)
    draw.text((x + 12, y + 2), region, font=make_font(BOLD, 11), fill=colour)
    cy = y + 18
    for line in wrap_text(draw, head, make_font(BOLD, 15), w - 14)[:2]:
        draw.text((x + 12, cy), line, font=make_font(BOLD, 15), fill=INK)
        cy += 19
    for line in wrap_text(draw, body, make_font(REGULAR, 12), w - 14)[:2]:
        draw.text((x + 12, cy), line, font=make_font(REGULAR, 12), fill=GREY)
        cy += 16


def draw_grid(draw, top):
    # Nine rows of three cards; the last row holds the final stories.
    # Card height is whatever remains after the masthead, lead and footer.
    cols, gap = 3, 16
    cw = (W - 48 - gap * (cols - 1)) // cols
    rows = 9
    ch = (H - top - 64) // rows
    placed = 0
    for r in range(rows):
        for c in range(cols):
            if placed >= len(STORIES):
                break
            region, head, body = STORIES[placed]
            placed += 1
            draw_card(draw, 24 + c * (cw + gap), top + r * ch, cw, ch, region, head, body)
        if placed >= len(STORIES):
            break
    return placed


def draw_footer(draw):
    fy = H - 52
    draw.rectangle([0, fy, W, H], fill=NAVY)
    draw.text((24, fy + 8), FOOTER_EXTRA, font=make_font(REGULAR, 14), fill=(255, 255, 255))
    draw.text((24, fy + 30), FOOTER_SOURCES, font=make_font(REGULAR, 12), fill=(180, 190, 205))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    top = draw_lead(draw)
    placed = draw_grid(draw, top)
    draw_footer(draw)
    img.save("/home/hatch/workspace/makefun-evolving/work/news25/entry.png", optimize=True)
    import os
    print("bytes:", os.path.getsize("/home/hatch/workspace/makefun-evolving/work/news25/entry.png"))
    print("stories:", placed)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render Wednesday 25 November 2026 world-news collage, 1024x1024 PNG.
Original work for make.fun news-image-20261124. Stories sourced from
public news digests of 24 Nov 2026 (Just Security Early Edition, The
Global Eye, Horizon, IQMIA). No copied artwork; all text drawn here."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (10, 25, 49); ORANGE = (255, 122, 0); PAPER = (250, 247, 240)
INK = (18, 18, 18); GREY = (90, 90, 90); RED = (178, 34, 34)
REGION_COLORS = {
    "MIDDLE EAST": (178, 34, 34), "EUROPE": (25, 80, 160),
    "ASIA": (0, 128, 96), "AFRICA": (150, 90, 10),
    "AMERICAS": (90, 40, 140), "TECH": (10, 90, 140), "WORLD": (70, 70, 70),
}
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FBO = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 96], fill=NAVY)
d.text((24, 14), "THE WORLD IN ONE DAY", font=font(FB, 40), fill=(255, 255, 255))
d.text((24, 62), "Wednesday 25 November 2026  \u00b7  27 stories, 7 regions, one day",
       font=font(FR, 19), fill=(255, 200, 140))
d.rectangle([0, 96, W, 100], fill=ORANGE)

LEAD = ("ZELENSKIY CONFIRMS BALTIC SHIP STRIKE",
        "Kyiv owns the Gulf of Finland drone hit; Moscow calls it terrorism, Norway urges caution",
        "EUROPE")
# Lead block
y = 112
d.text((24, y), LEAD[0], font=font(FBO, 34), fill=INK)
y += 46
for ln in wrap(d, LEAD[1], font(FR, 19), 976):
    d.text((24, y), ln, font=font(FR, 19), fill=GREY); y += 26
y += 8
d.line([24, y, 1000, y], fill=(200, 200, 200), width=2)
y += 12

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

# Grid: 3 cols x 9 rows-ish; cards computed to fit remaining height
top = y
cols, gap = 3, 16
cw = (W - 48 - gap * (cols - 1)) // cols
rows = 9
ch = (H - top - 64) // rows  # leave footer strip
idx = 0
for r in range(rows):
    for c in range(cols):
        if idx >= len(STORIES): break
        region, head, body = STORIES[idx]; idx += 1
        x = 24 + c * (cw + gap); yy = top + r * ch
        col = REGION_COLORS[region]
        d.rectangle([x, yy + 2, x + 5, yy + ch - 12], fill=col)
        d.text((x + 12, yy + 2), region, font=font(FB, 11), fill=col)
        hy = yy + 18
        for ln in wrap(d, head, font(FB, 15), cw - 14)[:2]:
            d.text((x + 12, hy), ln, font=font(FB, 15), fill=INK); hy += 19
        for ln in wrap(d, body, font(FR, 12), cw - 14)[:2]:
            d.text((x + 12, hy), ln, font=font(FR, 12), fill=GREY); hy += 16
    if idx >= len(STORIES): break

# Footer
fy = H - 52
d.rectangle([0, fy, W, H], fill=NAVY)
d.text((24, fy + 8), "Also 25 Nov: Ukraine seeks $125bn aid for 2027  \u00b7  England beat Australia in 2nd T20I  \u00b7  ~490,000 Russian troops lost, leaked data",
       font=font(FR, 14), fill=(255, 255, 255))
d.text((24, fy + 30), "Sources: Reuters, BBC, UN News, The Global Eye \u2014 25 November 2026",
       font=font(FR, 12), fill=(180, 190, 205))

img.save("/home/hatch/workspace/makefun-evolving/work/news25/entry.png", optimize=True)
import os
print("bytes:", os.path.getsize("/home/hatch/workspace/makefun-evolving/work/news25/entry.png"))
print("stories:", idx)

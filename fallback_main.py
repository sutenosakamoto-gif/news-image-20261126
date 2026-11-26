#!/usr/bin/env python3
"""Fallback entry (Stage 1): standard-library-only broadsheet renderer.

Draws a complete, submittable 1024x1024 front page for Thursday 26 November
2026 using only the Python standard library (zlib for PNG encoding and a
small built-in 5x7 bitmap font). Deterministic: two runs write identical
bytes. This is the insurance version; the richer build-time render is
render.py / page.png, copied by main.py.
"""
import os
import struct
import zlib

W, H = 1024, 1024
CREAM = (247, 242, 231)
INK = (24, 24, 24)
RED = (176, 30, 36)
BLUE = (31, 78, 121)
GREY = (110, 105, 95)
LIGHT = (232, 226, 212)
GOLD = (176, 141, 42)

# 5x7 bitmap font: each glyph is 7 rows of 5 bits (MSB = left column).
FONT = {
    'A': (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'B': (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    'C': (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    'D': (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    'E': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    'F': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    'G': (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    'H': (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'I': (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    'J': (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    'K': (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    'L': (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    'M': (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    'N': (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    'O': (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'P': (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    'Q': (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    'R': (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    'S': (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    'T': (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    'U': (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'V': (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    'W': (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    'X': (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    'Y': (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    'Z': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    '0': (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    '1': (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    '2': (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F),
    '3': (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    '4': (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    '5': (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    '6': (0x0E, 0x10, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    '7': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    '8': (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    '9': (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x01, 0x0E),
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ',': (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    ':': (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ';': (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    '!': (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    '?': (0x0E, 0x11, 0x01, 0x02, 0x04, 0, 0x04),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    '-': (0, 0, 0, 0x1F, 0, 0, 0),
    '/': (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    '(': (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ')': (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    '%': (0x18, 0x19, 0x02, 0x04, 0x08, 0x13, 0x18),
    '+': (0, 0x04, 0x04, 0x1F, 0x04, 0x04, 0),
    '=': (0, 0, 0x1F, 0, 0x1F, 0, 0),
    '&': (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    '$': (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    '£': (0x07, 0x08, 0x08, 0x1E, 0x08, 0x08, 0x1F),
    '€': (0x0E, 0x11, 0x10, 0x1E, 0x10, 0x11, 0x0E),
    '"': (0x0A, 0x0A, 0x0A, 0, 0, 0, 0),
    '#': (0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A),
    '[': (0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E),
    ']': (0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E),
    '>': (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
    '<': (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
}


def glyph(ch):
    return FONT.get(ch.upper(), FONT.get(ch, (0,) * 7))


class Canvas:
    def __init__(self):
        self.px = bytearray(CREAM * (W * H))

    def set(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            base = (yy * W + x) * 3
            for xx in range(w):
                if 0 <= x + xx < W and 0 <= yy < H:
                    self.px[base + xx * 3: base + xx * 3 + 3] = bytes(c)

    def frame(self, x, y, w, h, c, t=1):
        self.rect(x, y, w, t, c)
        self.rect(x, y + h - t, w, t, c)
        self.rect(x, y, t, h, c)
        self.rect(x + w - t, y, t, h, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def text(self, x, y, s, scale, c, align='l'):
        s = s.upper()
        w = len(s) * 6 * scale - scale
        if align == 'c':
            x -= w // 2
        elif align == 'r':
            x -= w
        for ch in s:
            g = glyph(ch)
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.rect(x + col * scale, y + row * scale,
                                  scale, scale, c)
            x += 6 * scale
        return w

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def wrap(self, s, scale, maxw):
        words, lines, cur = s.upper().split(), [], ''
        for wd in words:
            trial = (cur + ' ' + wd).strip()
            if self.text_w(trial, scale) <= maxw or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


def chunk(typ, data):
    c = struct.pack('>I', len(data)) + typ + data
    return c + struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF)


def write_png(cv, path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += cv.px[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
           + chunk(b'IDAT', zlib.compress(bytes(raw), 6))
           + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)


# ---- content (compact; full sourcing in SOURCES.md) ----
LEADS = [
    ("1", "HORMUZ", "CLAIM",
     "IRAN SAYS MORE SHIPS HIT MINES IN HORMUZ",
     "TEHRAN REPORTS AN LNG CARRIER ON FIRE AND A CONTAINER SHIP MINED. "
     "IDENTITIES UNCONFIRMED. BRENT CLIMBS TO $94.71.", "$94.71"),
    ("2", "GAZA", "REPORTED",
     "ISRAEL KILLS NINE IN GAZA, THIRD NIGHT RUNNING",
     "MEDICS SAY THE DEAD INCLUDE THE HAMAS-APPOINTED DEPUTY EDUCATION "
     "MINISTER AND HIS WIFE, DESPITE THE CEASEFIRE.", "9 KILLED"),
    ("3", "USA", "CONFIRMED",
     "THANKSGIVING STORM SLAMS THE US EAST COAST",
     "ALERTS FOR 80M+ PEOPLE, GUSTS TO 70 MPH, FLOODING. THE 100TH MACY'S "
     "PARADE MOVES TO SATURDAY - A FIRST IN 100 YEARS.", "80M+ ALERTS"),
]
MIDDLE = [
    ("4", "AFRICA", "CONFIRMED", "CONGO EBOLA CASES PASS 12,000",
     "12,021 CASES, 5,904 DEATHS. OUTBREAK IN 8 OF 26 PROVINCES.", "12,021"),
    ("5", "EUROPE", "CONFIRMED", "UNICREDIT CLEARS LAST HURDLE FOR 41BN COMMERZBANK TAKEOVER",
     "POLAND'S REGULATOR GIVES FINAL APPROVAL; VOTE SOUGHT ON BOARD.", "41BN"),
    ("6", "ASIA", "OFFICIAL", "BANK OF KOREA HIKES TO 3.25%",
     "QUARTER-POINT RISE, HIGHEST SINCE NOV 2024, ON CHIP BOOM.", "3.25%"),
    ("7", "ASIA", "OFFICIAL", "KIM TOURS NUCLEAR SITES, URGES WIDER TACTICAL-NUKE USE",
     "KCNA REPORTS THE TOUR ON THURSDAY; THE VISIT WAS WEDNESDAY.", "KCNA"),
    ("8", "EUROPE", "CONFIRMED", "UK WRITES TO 100,000 STRATEGIC RESERVISTS",
     "FIRST SUCH LETTERS SINCE THE COLD WAR; NOT MOBILISATION.", "100,000"),
    ("9", "ASIA", "CONFIRMED", "JAPAN CALLS US TARIFF PLAN 'REGRETTABLE'",
     "TOKYO PROTESTS A PROPOSED 15% LEVY; SEOUL VOWS TALKS.", "15%"),
    ("10", "ASIA", "CONFIRMED", "ASIAN SHARES BOUNCE AFTER WALL STREET FIGHTBACK",
     "NIKKEI +1.6%, KOSPI +1.9% IN A THIN HOLIDAY SESSION.", "+1.6%"),
    ("11", "ASIA", "CONFIRMED", "INDONESIA MINE: 13 DEAD, 13 STILL TRAPPED",
     "SEARCH RESUMES IN THE FLOODED BOGOR GOLD MINE.", "13 + 13"),
    ("12", "ASIA", "CONFIRMED", "MYANMAR WILL NOT FULLY OBEY ICJ GENOCIDE ORDERS",
     "JUNTA REJECTS 'INAPPROPRIATE' PARTS OF LAST WEEK'S RULING.", "ICJ"),
    ("13", "EUROPE", "CONFIRMED", "EU LEADERS OPEN TWO-DAY SUMMIT ON 1.6TN BUDGET",
     "NO DEAL EXPECTED THIS WEEK; AIM IS 17-18 DECEMBER.", "1.6TN"),
    ("14", "LATAM", "CONFIRMED", "PACIFIC TRADE BLOC MEETS IN VIETNAM AFTER US TARIFF SALVO",
     "CPTPP, ASEAN AND EU TRADE CHIEF GATHER; CHILE, MEXICO, PERU IN.", "12 NATIONS"),
    ("15", "ASIA", "CONFIRMED", "SINNER RULED OUT OF THE AUSTRALIAN OPEN",
     "TWO-TIME CHAMPION, 25, MISSES JANUARY AFTER KNEE SURGERY.", "AO 2027"),
    ("16", "EUROPE", "CONFIRMED", "BABCOCK WINS RECORD 8.7BN SUBMARINE CONTRACT",
     "FIVE-YEAR UK DEFENCE DEAL; SHARES RISE 5.8%.", "8.7BN"),
]
ALSO = [
    "17 SAUDI DEFENCES STOP TWO HOUTHI MISSILES AT RIYADH",
    "18 EUROPEAN STOCKS RALLY; STOXX 600 +1.4%",
    "19 DIESEL TANKER SINKS OFF IBIZA; ONE CREW DIES",
    "20 SNOW BLANKETS VIENNA; BUSES STUCK IN RUSH HOUR",
    "21 GERMAN CONSUMER SENTIMENT EDGES UP TO -30.2",
    "22 ITALY ASKS GERMANY TO STOP HENKEL PLANT CLOSURE",
    "23 AIRBALTIC OFFERS CREW EXIT OR PNG SECONDMENT",
    "24 EISENKOT RESUMES COALITION TALKS WITH DEMOCRATS",
    "25 KUSHNER: TRUMP KEEPS 'ALL OPTIONS' OPEN ON IRAN",
    "26 AUSTRALIA SET TO PASS LNG RESERVE LAW FOR HOME USE",
    "27 JAPAN OPPOSITION FILES CENSURE MOTION ON MINISTER",
    "28 HONG KONG MARKS A YEAR SINCE TAI PO FIRE KILLED 168",
    "29 INDIAN SHARES EXTEND GAINS ON RECORD INFLOWS",
    "30 DR CONGO SUMMONS UGANDA ENVOY OVER REBEL POSTS",
    "31 KENYA COURT: EBOLA SITE BUILD BREACHED CHARTER",
    "32 RWANDA HIKES RATE 75BP TO 9.5%; INFLATION 19.5%",
    "33 FIRST GENERIC HIV-PREVENTION DRUGS REACH AFRICA",
    "34 TULLOW OIL TO BEAT OUTPUT TARGET ON GHANA WELLS",
    "35 GOLD STEADIES AFTER A MORE-THAN-ONE-YEAR LOW",
    "36 TRUMP, NATO CHIEF: RUSSIA MUST NOT WIDEN UKRAINE WAR",
    "37 BRAZIL CALLS US TARIFF PLAN 'UNACCEPTABLE'",
    "38 US MARKETS SHUT FOR THANKSGIVING; NASDAQ -2% WED",
    "39 JAPAN PROPERTY DRAWS MONEY; FUNDS RAISE $4.66BN",
    "40 APPLE PULLS MINIMAX TALKIE OVER CHILD SAFETY",
]
NUMBERS = [
    ("$94.71", "BRENT CRUDE, EARLY ASIAN TRADE"),
    ("12,021", "EBOLA CASES IN DR CONGO"),
    ("100,000", "UK RESERVISTS WRITTEN TO"),
    ("80M+", "PEOPLE UNDER US STORM ALERTS"),
    ("41BN", "UNICREDIT-COMMERZBANK DEAL"),
    ("+1.6%", "NIKKEI ON THURSDAY"),
    ("13", "DEAD IN INDONESIA MINE"),
]
TIMELINE = [
    ("OVERNIGHT", "ISRAELI STRIKES KILL NINE IN GAZA"),
    ("01:19", "KCNA REPORTS KIM'S NUCLEAR TOUR"),
    ("01:37", "BRENT $94.71 AS IRAN CLAIMS MINE STRIKES"),
    ("02:05", "MACY'S 100TH PARADE MOVED TO SATURDAY"),
    ("03:01", "SEOUL VOWS TALKS AFTER US TARIFF PLANS"),
    ("03:55", "INDONESIA MINE SEARCH RESUMES"),
    ("05:29", "CONGO EBOLA PASSES 12,000 CASES"),
    ("07:14", "BABCOCK WINS 8.7BN SUBMARINE DEAL"),
    ("07:28", "UNICREDIT CLEARS LAST COMMERZBANK HURDLE"),
]
DATECHECK = [
    "WED 25 NOV - SECTION 301 TARIFF ANNOUNCEMENT; US PCE +3.8%, GDP 4.3%. ONLY REACTIONS ARE THU.",
    "WED 25 NOV - SHENZHOU-24 LAUNCH; HOUTHI RAS TANURA CLAIMS; CAIRO TANKER FIRE, 31 DEAD.",
    "WED 25 NOV - UK ENERGY CAP +26%; AUSTRALIA-SOLOMON PACT; N KOREA EXPELS SWISS ENVOY.",
    "WED 25 NOV - SPACEX FCC STARMIND APPROVAL; MLB SUES PLAYERS' UNION; LUMA CONTRACT AXED.",
    "WED 25 NOV - TWO TANKERS HIT MINES IN HORMUZ; UKMTO DUBAI BLAST; KYIV MISSILES; SAVASLEYKA.",
    "TUE 24 NOV - SUDAN RSF STRIKES KILL 19; DURAN DURAN GUITARIST ANDY TAYLOR DIES, 65.",
    "WED EVENING - DECIDED WED, REPORTED THU: MACY'S MOVE; KIM TOUR; MYANMAR ICJ REFUSAL; MORE.",
    "NOT YET - SPAIN ELECTION 29 NOV; OPEC+ 29 NOV; ITLOS FALKLANDS RULING 28 NOV; EUROPA LEAGUE.",
]
REGION_LINE = ("40 STORIES - MIDDLE EAST 5 - EUROPE 11 - ASIA-PACIFIC 12 - "
               "AFRICA 6 - NORTH AMERICA 2 - LATIN AMERICA 2 - GLOBAL 2")


def motif(cv, x, y, w, h, kind, chip):
    """Simple geometric motif + figure chip for a lead/middle illustration."""
    cv.rect(x, y, w, h, LIGHT)
    cv.frame(x, y, w, h, INK)
    if kind == "HORMUZ":
        cv.rect(x + 8, y + h - 22, w - 16, 14, BLUE)
        cv.rect(x + w // 2 - 30, y + 8, 60, 10, INK)
        cv.disc(x + w // 2 - 40, y + h - 30, 4, RED)
        cv.disc(x + w // 2 + 40, y + h - 30, 4, RED)
    elif kind == "GAZA":
        cv.rect(x, y + h - 26, w, 26, INK)
        for i in range(5):
            cv.rect(x + 8 + i * (w // 5), y + h - 46 - (i % 3) * 8, 18, 46, INK)
        cv.disc(x + w - 24, y + 14, 8, RED)
    elif kind == "USA":
        for i in range(4):
            cv.line(x + 10 + i * 14, y + h - 10, x + 30 + i * 14, y + 12, BLUE)
        cv.disc(x + w - 30, y + 18, 12, GOLD)
    elif kind == "AFRICA":
        cv.disc(x + w // 2, y + h // 2, 16, RED)
        cv.disc(x + w // 2 - 22, y + h // 2 - 8, 7, RED)
        cv.disc(x + w // 2 + 24, y + h // 2 + 6, 6, RED)
    elif kind == "EUROPE":
        for i in range(3):
            cv.rect(x + 10 + i * 16, y + h - 24, 12, 24, INK)
    elif kind == "ASIA":
        for i in range(5):
            bh = 8 + i * 7
            cv.rect(x + 10 + i * 14, y + h - 8 - bh, 10, bh, BLUE)
        cv.line(x + 8, y + h - 8, x + w - 8, y + 10, RED)
    elif kind == "LATAM":
        cv.rect(x + w // 2 - 26, y + 10, 52, 14, BLUE)
        cv.rect(x + w // 2 - 20, y + 26, 40, 10, RED)
        cv.rect(x + w // 2 - 14, y + 38, 28, 8, GOLD)
    else:
        cv.disc(x + w // 2, y + h // 2, 14, BLUE)
    cw = cv.text_w(chip, 1) + 10
    cv.rect(x + w - cw - 4, y + 4, cw, 11, RED)
    cv.text(x + w - cw + 1, y + 6, chip, 1, CREAM)


def build():
    cv = Canvas()
    cv.frame(4, 4, W - 8, H - 8, INK, 2)
    y = 14
    cv.text(512, y, "THE WORLD IN ONE PAGE", 3, INK, 'c')
    y += 30
    cv.hline(18, y, W - 36, INK, 2)
    y += 8
    cv.text(512, y, "THURSDAY 26 NOVEMBER 2026", 4, INK, 'c')
    y += 42
    cv.text(512, y, "MINES IN HORMUZ LIFT OIL PAST $94 - GAZA STRIKES A THIRD NIGHT",
            1, RED, 'c')
    y += 12
    cv.text(512, y, "A THANKSGIVING STORM BATTERS THE EAST COAST", 1, RED, 'c')
    y += 16
    cv.text(512, y, REGION_LINE, 1, INK, 'c')
    y += 16
    cv.hline(18, y, W - 36, INK)
    y += 6
    cv.text(18, y, "THE DAY IN NUMBERS", 1, RED)
    y += 12
    cw = (W - 36) // 7
    for i, (num, cap) in enumerate(NUMBERS):
        x = 18 + i * cw
        cv.text(x + cw // 2, y, num, 2, INK, 'c')
        for j, ln in enumerate(cv.wrap(cap, 1, cw - 8)):
            cv.text(x + cw // 2, y + 18 + j * 9, ln, 1, GREY, 'c')
        if i:
            cv.vline(x, y - 2, 34, GREY)
    y += 40
    cv.hline(18, y, W - 36, INK)
    y += 6
    cv.text(18, y, "THE DAY IN TIME - ALL TIMES UTC", 1, RED)
    y += 12
    colw = (W - 36) // 3
    for i, (t, txt) in enumerate(TIMELINE):
        x = 18 + (i % 3) * colw
        yy = y + (i // 3) * 11
        cv.text(x, yy, t + "  " + txt, 1, INK)
    y += 36
    cv.hline(18, y, W - 36, INK)
    y += 6
    # leads
    lw = (W - 36 - 16) // 3
    ly = y
    for i, (num, kind, cert, head, body, chip) in enumerate(LEADS):
        x = 18 + i * (lw + 8)
        cv.frame(x, ly, lw, 158, INK)
        motif(cv, x + 4, ly + 4, lw - 8, 62, kind, chip)
        hh = cv.wrap(head, 2, lw - 12)
        yy = ly + 72
        for ln in hh[:2]:
            cv.text(x + 6, yy, ln, 2, INK)
            yy += 16
        for ln in cv.wrap(body, 1, lw - 12)[:2]:
            cv.text(x + 6, yy, ln, 1, INK)
            yy += 9
        cv.text(x + 6, ly + 158 - 12, num + "  " + cert, 1, RED)
    y = ly + 158 + 6
    # middle: rows of 5, 4, 4
    rows = [MIDDLE[0:5], MIDDLE[5:9], MIDDLE[9:13]]
    for row in rows:
        n = len(row)
        mw = (W - 36 - (n - 1) * 6) // n
        for i, (num, kind, cert, head, body, chip) in enumerate(row):
            x = 18 + i * (mw + 6)
            cv.frame(x, y, mw, 90, INK)
            motif(cv, x + 3, y + 3, mw - 6, 40, kind, chip)
            hh = cv.wrap(head, 1, mw - 26)
            yy = y + 47
            for ln in hh[:2]:
                cv.text(x + 4, yy, ln, 1, INK)
                yy += 9
            for ln in cv.wrap(body, 1, mw - 8)[:1]:
                cv.text(x + 4, yy, ln, 1, GREY)
            cv.text(x + mw - 4, y + 47, num, 1, RED, 'r')
        y += 96
    # map
    cv.text(18, y, "WHERE IT HAPPENED - PIN NUMBERS MATCH STORY NUMBERS", 1, RED)
    y += 12
    my = y
    cv.frame(18, my, 640, 76, INK)
    cv.text(24, my + 4, "WORLD MAP - PINS 1-16", 1, GREY)
    pins = [(56, 26, 1), (34, 31, 2), (-74, 41, 3), (23, -3, 4), (127, 38, 6),
            (126, 39, 7), (140, 36, 9), (107, -7, 11), (96, 20, 12),
            (106, 21, 14), (145, -38, 15)]
    for lon, lat, n in pins:
        px = 18 + int((lon + 170) / 360.0 * 640)
        py = my + int((75 - lat) / 130.0 * 76)
        cv.disc(px, py, 7, RED)
        cv.text(px, py - 3, str(n), 1, CREAM, 'c')
    cv.frame(666, my, 340, 76, INK)
    cv.text(672, my + 4, "EUROPE - DETAIL", 1, GREY)
    epins = [(-4, 50, 16), (0, 52, 8), (4, 51, 13), (9, 50, 5)]
    for lon, lat, n in epins:
        px = 666 + int((lon + 12) / 32.0 * 340)
        py = my + int((62 - lat) / 28.0 * 76)
        cv.disc(px, py, 7, RED)
        cv.text(px, py - 3, str(n), 1, CREAM, 'c')
    y = my + 76 + 6
    # ALSO
    cv.text(18, y, "ALSO ON THURSDAY 26 NOVEMBER", 1, RED)
    y += 12
    colw = (W - 36) // 3
    for i, item in enumerate(ALSO):
        x = 18 + (i % 3) * colw
        yy = y + (i // 3) * 11
        cv.text(x, yy, item, 1, INK)
    y += 8 * 11 + 6
    # DATE CHECK
    cv.hline(18, y, W - 36, INK)
    y += 5
    cv.text(18, y, "DATE CHECK - EXCLUDED AS OTHER DAYS' NEWS, OR NOT YET", 1, RED)
    y += 12
    for line in DATECHECK:
        cv.text(18, y, line, 1, INK)
        y += 11
    cv.text(18, y + 2,
            "CONFIRMED = 2+ OUTLETS - OFFICIAL = ON THE RECORD - REPORTED = ONE "
            "OUTLET - CLAIM = ONE SIDE'S ACCOUNT.", 1, GREY)
    cv.text(18, y + 12,
            "SCENES ARE DRAWN ILLUSTRATIONS, NOT PHOTOGRAPHS.", 1, GREY)
    return cv


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(outdir, exist_ok=True)
        out = os.path.join(outdir, "entry.png")
    except OSError:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "entry.png")
    size = write_png(build(), out)
    print("wrote", out, size, "bytes")


if __name__ == "__main__":
    main()

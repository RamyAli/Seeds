"""Option C: builds screens-c.html, option B's layout re-skinned with:

- Main colour #FF5002. Text-sized orange on white uses #C23D00 so it passes
  WCAG AA; #FF5002 is kept for fills, icons, bars and the hero.
- English type: IBM Plex Sans for headlines, titles and hero numbers, and
  Inter for body text.
- Arabic type: Tajawal throughout.

    python3 design/nestly/build_c.py
"""
from pathlib import Path

import build_b

OUT = Path(__file__).with_name("screens-c.html")

MAIN = "#FF5002"
MAIN_TEXT = "#C23D00"
INK = "#18120E"

# option B colours -> option C
RECOLOR = [
    # accent family
    ("#2F5BEA", MAIN), ("#1B3FC4", "#C93C00"), ("#1F48D6", MAIN_TEXT), ("#3D6BF5", "#FF6A1F"),
    ("rgba(47,91,234,", "rgba(255,80,2,"), ("rgba(120,160,255,", "rgba(255,170,110,"),
    ("rgba(20,40,160,", "rgba(140,30,0,"), ("rgba(160,185,245,", "rgba(255,180,140,"),
    ("rgba(31,72,214,", "rgba(194,61,0,"),
    ("#5B82F7", "#FF7A3D"), ("#1E43C8", "#D94300"), ("#A8BEFF", "#FFC2A3"),
    # tints
    ("#D6E2FF", "#FFE1D2"), ("#E6EDFF", "#FFEADF"), ("#EAF0FF", "#FFF0E8"), ("#F5F8FF", "#FFF8F4"),
    ("#DCE5FF", "#FFE0CF"), ("#EEF2FE", "#FFEFE6"), ("#E9EEF9", "#FFEFE6"),
    ("#F6F8FE", "#FFF9F5"), ("#E7EDFB", "#FCEADF"),
    # neutrals: cool blue-grey -> warm neutral
    ("#E8EEFB", "#FDEEE5"), ("#F1F4F9", "#F6F4F2"), ("#F4F6F9", "#F7F5F3"), ("#F3F5F9", "#F6F4F2"),
    ("#EEF1F6", "#F0EDEA"), ("#F5F7FB", "#F6F4F1"), ("#E4E9F2", "#EEE8E3"), ("#C9D2E3", "#DDD3CB"),
    ("#CBD3E1", "#DCD5CF"), ("#1B2440", "#2A1A10"),
    ("#0E1424", INK), ("#22201E", INK), ("#5B6478", "#6B635C"), ("#9AA2B4", "#A39A92"),
    ("rgba(14,20,36,", "rgba(24,18,14,"), ("rgba(20,40,90,", "rgba(70,35,10,"),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
         '&family=IBM+Plex+Sans:wght@400;500;600;700&family=Tajawal:wght@400;500;700;800'
         '&family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,wght@1,400;1,500&display=swap" rel="stylesheet">')

HEAD = '"IBM Plex Sans","Helvetica Neue",Arial,sans-serif'
ARABIC = '"Tajawal","IBM Plex Sans Arabic",sans-serif'

EXTRA_CSS = f"""
/* option C type: IBM Plex Sans for headlines and titles, Inter for body */
.title,.hello,.stitle,.stitle-b,.ctitle,.center-title,.hb-name,.hnum,.hcur,.gval,.bigamt,.dv,.sumv,
.ai-name,.btn,.prof .rtitle{{font-family:{HEAD}}}
.title{{font-weight:600;letter-spacing:-.6px}}
.hnum{{font-weight:600;letter-spacing:-1px}}
.gval,.bigamt,.dv,.sumv{{letter-spacing:-.4px}}
/* Arabic: Tajawal everywhere (it has no 600, so semibold maps to 700) */
[lang=ar],[lang=ar] *{{font-family:{ARABIC}}}
[lang=ar] .hello,[lang=ar] .ctitle,[lang=ar] .rtitle,[lang=ar] .hb-name,[lang=ar] .stitle-b,
[lang=ar] .link,[lang=ar] .count,[lang=ar] b,[lang=ar] .pill,[lang=ar] .chip,[lang=ar] .promo-btn,
[lang=ar] .hnum,[lang=ar] .gval,[lang=ar] .title{{font-weight:700}}
[lang=ar] .ra,[lang=ar] .meta,[lang=ar] .rsub,[lang=ar] .hb-sm{{font-weight:500}}
/* small orange text uses the AA-safe shade */
.chip.blue,.pill.on-blue{{color:{MAIN_TEXT}}}
.hb-sm{{color:rgba(255,255,255,.88)}}
"""


def main():
    html, n = build_b.render(title="Nestly screens, option C", fonts=FONTS, extra_css=EXTRA_CSS)
    for a, z in RECOLOR:
        html = html.replace(a, z)
    html = html.replace('data-name="B', 'data-name="C')
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html)//1024} KB, {n} screens)")


if __name__ == "__main__":
    main()

"""Builds screens.html: the Nestly app screens redesigned in a Grassfeld-like
layout with iOS 26 Liquid Glass surfaces and the Seed palette.

Each screen is a `.screen` element (393 x 852, iPhone 16 Pro), so the file can
be pushed to Figma with html_to_figma using cssSelector ".screen".

    python3 design/nestly/build.py
"""
import math
from pathlib import Path

OUT = Path(__file__).with_name("screens.html")

# ---------------------------------------------------------------- tokens
INK = "#22201E"
INK2 = "#6E675F"
INK3 = "#9C958B"
ORANGE = "#DE6538"
CLAY = "#A9441D"
POS = "#4F8A3C"
NEG = "#B8322A"
DRY = "#C9A04A"
WET = "#3D7A94"
CANOPY = "#2E4B33"
SHOOT = "#9DBF6A"
TRACK = "#EAE3D8"
HATCH = "#CFC3B1"
HATCH_ON = True  # hatched "left" part of progress bars

# ---------------------------------------------------------------- icons
ICONS = {
    "home": "M3.5 10.5 12 3.5l8.5 7V20a1 1 0 0 1-1 1H15v-6H9v6H4.5a1 1 0 0 1-1-1z",
    "activity": "M7 4 3.5 7.5 7 11M3.5 7.5H17M17 20l3.5-3.5L17 13M20.5 16.5H7",
    "insights": "M5 20v-8M12 20V5M19 20v-5",
    "goals": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 16.5a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9zM12 12.5a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z",
    "sparkle": "M12 3.5l1.9 5.1 5.1 1.9-5.1 1.9L12 17.5l-1.9-5.1L5 10.5l5.1-1.9zM18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z",
    "mic": "M12 3.5a3 3 0 0 0-3 3V12a3 3 0 0 0 6 0V6.5a3 3 0 0 0-3-3zM5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3",
    "scan": "M4 8.5V6a2 2 0 0 1 2-2h2.5M15.5 4H18a2 2 0 0 1 2 2v2.5M20 15.5V18a2 2 0 0 1-2 2h-2.5M8.5 20H6a2 2 0 0 1-2-2v-2.5M7.5 12h9",
    "pen": "M4 20h4L19.5 8.5l-4-4L4 16zM13.5 6.5l4 4",
    "bell": "M18 16v-5a6 6 0 0 0-12 0v5l-1.5 2h15zM10 21h4",
    "search": "M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM20 20l-4-4",
    "chev": "M9.5 6l6 6-6 6",
    "chevl": "M14.5 6l-6 6 6 6",
    "chevd": "M6 9.5l6 6 6-6",
    "close": "M6.5 6.5l11 11M17.5 6.5l-11 11",
    "plus": "M12 5v14M5 12h14",
    "check": "M5 12.5l4.5 4.5L19 7",
    "salary": "M4 8h16v11H4zM9 8V5.5h6V8M4 13h16",
    "cart": "M3 4.5h2l2.3 10.5h10.9L20.5 7.5H6.2M9 20a1 1 0 1 0 0-.01M17.5 20a1 1 0 1 0 0-.01",
    "bag": "M6 8.5h12l-1 11.5H7zM9 8.5V7a3 3 0 0 1 6 0v1.5",
    "car": "M4 16.5v-4l2.5-6h11l2.5 6v4zM4 16.5V19h3v-2.5M17 16.5V19h3v-2.5M7.5 13h.01M16.5 13h.01",
    "heart": "M12 20s-7.5-4.6-7.5-10.2A4.2 4.2 0 0 1 12 7.3a4.2 4.2 0 0 1 7.5 2.5C19.5 15.4 12 20 12 20z",
    "bolt": "M13 3 5.5 13.5h5.5L10 21l8-10.5h-5.5z",
    "cup": "M5 9h11v4.5a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5zM16 10h1.5a2.2 2.2 0 0 1 0 4.4H16M8.5 3.5v3M12.5 3.5v3",
    "send": "M4.5 12 20 4.5 14 20l-3-7z",
    "calendar": "M5 6h14v14H5zM5 10h14M9 3.5v4M15 3.5v4",
    "cheque": "M3 6.5h18v11H3zM6.5 10.5h6M6.5 13.5h4M15 13h3",
    "wallet": "M4 7.5h15a1 1 0 0 1 1 1V19H5a1 1 0 0 1-1-1zM4 7.5 15.5 4.5v3M16 13.5h.01",
    "shield": "M12 3.5 5 6.5V11c0 4.4 3 7.9 7 9.5 4-1.6 7-5.1 7-9.5V6.5z",
    "help": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM9.6 9.6a2.5 2.5 0 1 1 3.4 2.3c-.6.3-1 .8-1 1.5v.6M12 17h.01",
    "logout": "M14.5 4h4.5v16h-4.5M10 8l-4 4 4 4M6 12h10",
    "download": "M12 4v11M7.5 10.5 12 15l4.5-4.5M5 20h14",
    "plane": "M3 13.5l6.5-1.5L16 5.5a1.6 1.6 0 0 1 2.4 2.1L12 14l-1.5 6.5-2-1.5.5-4.5-4.5.5z",
    "laptop": "M5 6h14v9H5zM3 18.5h18",
    "moon": "M19.5 14.5A8 8 0 1 1 9.5 4.5a6.2 6.2 0 0 0 10 10z",
    "repeat": "M4 9h13l-3-3M20 15H7l3 3",
    "globe": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM3 12h18M12 3c2.5 2.6 3.5 5.6 3.5 9s-1 6.4-3.5 9c-2.5-2.6-3.5-5.6-3.5-9S9.5 5.6 12 3z",
    "users": "M9 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM2.5 20a6.5 6.5 0 0 1 13 0M16 4.3a3.5 3.5 0 0 1 0 6.4M18.5 14.5A6.5 6.5 0 0 1 21.5 20",
    "phone": "M7 3h10v18H7zM11 18h2",
    "in": "M17 7 7 17M7 9.5V17h7.5",
    "out": "M7 17 17 7M9.5 7H17v7.5",
    "clock": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7.5V12l3 2",
    "filter": "M4 6h16M7 12h10M10 18h4",
    "swap": "M7 4.5v15M4 16.5l3 3 3-3M17 19.5v-15M14 7.5l3-3 3 3",
    "keyboard": "M3 6.5h18v11H3zM7 10h.01M10.5 10h.01M14 10h.01M17.5 10h.01M8 14h8",
}


def icon(name, size=22, color="currentColor", sw=1.7):
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
        f'stroke-linejoin="round"><path d="{ICONS[name]}"/></svg>'
    )


# ---------------------------------------------------------------- helpers
def money(v, cur="AED", sign="", big=False, rtl=False):
    s = f"{abs(v):,.2f}"
    whole, dec = s.split(".")
    dec_cls = "dec big" if big else "dec"
    if rtl:
        return f'<span class="num">{sign}{whole}<span class="{dec_cls}">.{dec}</span> <span class="cur">د.إ</span></span>'
    return f'<span class="num"><span class="cur">{sign}{cur}</span> {whole}<span class="{dec_cls}">.{dec}</span></span>'


_clip = [0]


def bar(w, frac, color=None, today=None, h=10, rtl=False):
    """Grassfeld progress bar: solid spent part, hatched remainder, Today tick."""
    color = color or ORANGE
    _clip[0] += 1
    cid = f"c{_clip[0]}"
    pad = 5 if today is not None else 0
    H = h + pad * 2
    sw = w * min(frac, 1)

    def X(x):
        return w - x if rtl else x

    lines = []
    x = sw - h
    while HATCH_ON and x < w + h:
        x0, x1 = X(x), X(x + h)
        lines.append(f'<line x1="{x0:.1f}" y1="{pad + h}" x2="{x1:.1f}" y2="{pad}" stroke="{HATCH}" stroke-width="1.6"/>')
        x += 5.5
    spent_x = w - sw if rtl else 0
    out = [
        f'<svg width="{w}" height="{H}" viewBox="0 0 {w} {H}" style="display:block;overflow:visible">',
        f'<defs><clipPath id="{cid}"><rect x="0" y="{pad}" width="{w}" height="{h}" rx="{h/2}"/></clipPath></defs>',
        f'<g clip-path="url(#{cid})"><rect x="0" y="{pad}" width="{w}" height="{h}" fill="{TRACK}"/>',
        "".join(lines),
        f'<rect x="{spent_x:.1f}" y="{pad}" width="{sw:.1f}" height="{h}" rx="{h/2}" fill="{color}"/></g>',
    ]
    if today is not None:
        tx = X(w * today)
        out.append(f'<rect x="{tx - 1.25:.1f}" y="0" width="2.5" height="{H}" rx="1.25" fill="{INK}"/>')
    out.append("</svg>")
    return "".join(out)


def legend_swatch(kind, color=None):
    color = color or ORANGE
    if kind == "solid":
        return f'<span class="sw" style="background:{color}"></span>'
    if kind == "hatch" and not HATCH_ON:
        return f'<span class="sw" style="background:{TRACK}"></span>'
    if kind == "hatch":
        return (
            '<svg width="12" height="12" viewBox="0 0 12 12" style="flex:none">'
            f'<rect width="12" height="12" rx="3" fill="{TRACK}"/>'
            f'<path d="M-2 8 4-2M2 12 10 0M6 14 14 2" stroke="{HATCH}" stroke-width="1.6"/></svg>'
        )
    return f'<span class="sw" style="border:1.5px solid {INK3}"></span>'


def arc(cx, cy, r, a0, a1):
    def pt(a):
        rad = math.radians(a - 90)
        return cx + r * math.cos(rad), cy + r * math.sin(rad)

    x0, y0 = pt(a0)
    x1, y1 = pt(a1)
    large = 1 if a1 - a0 > 180 else 0
    return f"M{x0:.2f} {y0:.2f}A{r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}"


def status_bar(dark=False, time="9:41"):
    c = "#fff" if dark else INK
    return f"""
<div class="status" style="color:{c}">
  <span class="time">{time}</span>
  <div class="island"></div>
  <span class="sys">
    <svg width="18" height="12" viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1" fill="{c}"/><rect x="5" y="5.5" width="3" height="6.5" rx="1" fill="{c}"/><rect x="10" y="3" width="3" height="9" rx="1" fill="{c}"/><rect x="15" y="0" width="3" height="12" rx="1" fill="{c}"/></svg>
    <svg width="16" height="12" viewBox="0 0 16 12"><path d="M8 11.5 5.6 8.9a3.4 3.4 0 0 1 4.8 0zM3.4 6.7a6.5 6.5 0 0 1 9.2 0l-1.4 1.4a4.5 4.5 0 0 0-6.4 0zM1 4.3a9.9 9.9 0 0 1 14 0l-1.4 1.4a7.9 7.9 0 0 0-11.2 0z" fill="{c}"/></svg>
    <svg width="27" height="13" viewBox="0 0 27 13"><rect x=".5" y=".5" width="23" height="12" rx="3.8" stroke="{c}" stroke-opacity=".4" fill="none"/><rect x="2" y="2" width="17" height="9" rx="2.4" fill="{c}"/><path d="M25 4.5v4a2 2 0 0 0 0-4z" fill="{c}" fill-opacity=".45"/></svg>
  </span>
</div>"""


TABS = [("home", "Home"), ("activity", "Activity"), ("insights", "Insights"), ("goals", "Goals")]
TABS_AR = ["الرئيسية", "العمليات", "التحليلات", "الأهداف"]


def tab_bar(active, rtl=False):
    items = []
    for i, (ic, label) in enumerate(TABS):
        on = ic == active
        lab = TABS_AR[i] if rtl else label
        cls = "tab on" if on else "tab"
        col = CLAY if on else INK
        items.append(f'<div class="{cls}" style="color:{col}">{icon(ic, 24, sw=1.8)}<span>{lab}</span></div>')
    side = "left" if rtl else "right"
    other = "right" if rtl else "left"
    return f"""
<div class="tabbar glass" style="{other}:16px">{''.join(items)}</div>
<div class="ai-btn glass" style="{side}:16px">
  <div class="orb">{icon('sparkle', 24, '#fff', 1.8)}</div>
</div>"""


def tile(ic, bg, fg, size=40, isz=20):
    return f'<div class="tile" style="width:{size}px;height:{size}px;background:{bg};color:{fg}">{icon(ic, isz)}</div>'


def row(ic, bg, fg, title, sub, amount, amount_color=INK, right_sub=None, rtl=False):
    rs = f'<div class="rsub">{right_sub}</div>' if right_sub else ""
    return f"""
<div class="row">
  {tile(ic, bg, fg)}
  <div class="grow"><div class="rtitle">{title}</div><div class="rsub">{sub}</div></div>
  <div class="ramt"><div style="color:{amount_color}">{amount}</div>{rs}</div>
</div>"""


def screen(name, body, bg, extra_cls="", rtl=False, lang="en"):
    d = ' dir="rtl"' if rtl else ""
    return f'<section class="screen {extra_cls}" data-name="{name}" lang="{lang}"{d} style="background:{bg}">{body}</section>'


# backgrounds: pale Silt canvas with a section tint washing in from the top
BG_HOME = ("radial-gradient(120% 55% at 10% 0%, rgba(222,101,56,.30) 0%, rgba(222,101,56,0) 60%),"
           "radial-gradient(90% 45% at 100% 8%, rgba(217,201,168,.85) 0%, rgba(217,201,168,0) 65%),"
           "linear-gradient(#F6F2EB, #F3EFE8)")
BG_ACT = ("radial-gradient(110% 45% at 90% 0%, rgba(217,201,168,.9) 0%, rgba(217,201,168,0) 65%),"
          "radial-gradient(80% 40% at 0% 5%, rgba(222,101,56,.16) 0%, rgba(222,101,56,0) 60%),"
          "linear-gradient(#F6F2EB, #F3EFE8)")
BG_INS = ("radial-gradient(110% 50% at 0% 0%, rgba(61,122,148,.22) 0%, rgba(61,122,148,0) 60%),"
          "radial-gradient(90% 45% at 100% 5%, rgba(217,201,168,.8) 0%, rgba(217,201,168,0) 65%),"
          "linear-gradient(#F5F2EC, #F3EFE8)")
BG_GOALS = ("radial-gradient(110% 50% at 100% 0%, rgba(157,191,106,.40) 0%, rgba(157,191,106,0) 60%),"
            "radial-gradient(90% 45% at 0% 5%, rgba(217,201,168,.75) 0%, rgba(217,201,168,0) 65%),"
            "linear-gradient(#F5F3EC, #F3EFE8)")
BG_AI = ("radial-gradient(90% 40% at 50% 12%, rgba(222,101,56,.26) 0%, rgba(222,101,56,0) 65%),"
         "radial-gradient(80% 40% at 0% 60%, rgba(61,122,148,.10) 0%, rgba(61,122,148,0) 60%),"
         "linear-gradient(#F7F3EC, #F3EFE8)")


def sheet_backdrop(bg):
    """Blurred, dimmed app content behind a sheet."""
    return f"""
<div class="backdrop" style="background:{bg}">
  <div class="ghost" style="top:70px;height:28px;width:180px"></div>
  <div class="ghost" style="top:118px;height:210px"></div>
  <div class="ghost" style="top:344px;height:84px"></div>
  <div class="ghost" style="top:444px;height:150px"></div>
</div>
<div class="dim"></div>"""


# ======================================================================
# 1. Home
# ======================================================================
def home_body():
    return f"""
{status_bar()}
<div class="content">
  <div class="hdr">
    <div>
      <div class="hello">Good morning, Alex</div>
      <div class="meta">Pay cycle · 25 Mar → 24 Apr</div>
    </div>
    <div class="hdr-actions">
      <div class="iconbtn glass">{icon('bell', 20)}</div>
      <div class="avatar glass">AJ</div>
    </div>
  </div>

  <div class="card budget">
    <div class="between"><div class="ctitle">April pay cycle</div><div class="meta">for <b>9</b> days</div></div>
    <div class="meta" style="margin-top:2px">25 Mar → 24 Apr</div>
    <div class="between" style="margin-top:16px;align-items:flex-end">
      <div class="hero">{legend_swatch('hatch')}{money(6660, big=True)} <span class="hero-lab">Left</span></div>
    </div>
    <div style="margin-top:12px">{bar(313, .63, today=.68)}</div>
    <div class="today" style="padding-left:{313*.68 - 14:.0f}px">Today</div>
    <div class="between legend-wrap">
      <div class="legend">
        <div>{legend_swatch('solid')}<span>Spent</span><b>63%</b></div>
        <div>{legend_swatch('hatch')}<span>Left</span><b>37%</b></div>
        <div>{legend_swatch('outline')}<span>Budget</span></div>
      </div>
      <div class="amounts">
        <div>{money(11340)}</div>
        <div>{money(6660)}</div>
        <div class="strong">{money(18000)}</div>
      </div>
    </div>
    <div class="dots"><span class="on"></span><span></span><span></span></div>
  </div>

  <div class="quick glass">
    <div class="q">{tile('mic', 'rgba(222,101,56,.14)', CLAY, 44, 22)}<span>Say it</span></div>
    <div class="qdiv"></div>
    <div class="q">{tile('scan', 'rgba(222,101,56,.14)', CLAY, 44, 22)}<span>Scan</span></div>
    <div class="qdiv"></div>
    <div class="q">{tile('pen', 'rgba(222,101,56,.14)', CLAY, 44, 22)}<span>Type</span></div>
  </div>

  <div class="card slim">
    {tile('heart', 'rgba(157,191,106,.25)', CANOPY, 40)}
    <div class="grow"><div class="rtitle">Family support</div><div class="rsub">3 people · AED 3,300 a month</div></div>
    <div class="count">2 of 3 sent</div>{icon('chev', 18, INK3)}
  </div>

  <div class="section"><span class="caps">Recent</span><span class="link">See all</span></div>
  <div class="card list">
    {row('salary', 'rgba(79,138,60,.13)', POS, 'Salary', 'Emirates NBD · 25 Mar', money(19500, sign='+'), POS)}
    {row('cheque', 'rgba(222,101,56,.13)', CLAY, 'Rent cheque 3 of 4', 'Cheque · 1 Apr', money(6250, sign='−'))}
    {row('cart', 'rgba(201,160,74,.18)', '#8A6A22', 'Carrefour', 'Groceries · Today', money(312.50, sign='−'))}
  </div>
</div>
{tab_bar('home')}"""


# ======================================================================
# 2. Home, Arabic (RTL)
#
# Written in visual (left-to-right) order with no dir="rtl": the HTML-to-Figma
# converter ignores direction, so the mirrored layout is spelled out, and every
# text run is a single direction (Arabic words, or numbers) so Figma's own bidi
# pass can't reorder a mixed string.
# ======================================================================
def vis(*runs, cls="", align="end"):
    spans = "".join(f"<span>{r}</span>" for r in runs)
    return f'<div class="vis {cls}" style="justify-content:flex-{align}">{spans}</div>'


def ar_amt(v, sign="", big=False, color=None, align="start"):
    whole, dec = f"{abs(v):,.2f}".split(".")
    d = "dec big" if big else "dec"
    c = f' style="color:{color}"' if color else ""
    return vis('<span class="cur">د.إ</span>',
               f'<span class="num"{c}>{sign}{whole}<span class="{d}">.{dec}</span></span>', align=align)


def ar_row(ic, bg, fg, title_runs, sub_runs, amount):
    return f"""
<div class="row">
  <div class="ramt">{amount}</div>
  <div class="grow ar-text"><div class="rtitle">{vis(*title_runs)}</div><div class="rsub">{vis(*sub_runs)}</div></div>
  {tile(ic, bg, fg)}
</div>"""


def home_ar_body():
    tabs = "".join(
        f'<div class="tab{" on" if ic == "home" else ""}" style="color:{CLAY if ic == "home" else INK}">{icon(ic, 24, sw=1.8)}<span>{lab}</span></div>'
        for (ic, _), lab in reversed(list(zip(TABS, TABS_AR)))
    )
    tick = 313 - 313 * .68
    return f"""
{status_bar()}
<div class="content">
  <div class="hdr">
    <div class="hdr-actions">
      <div class="avatar glass">أ</div>
      <div class="iconbtn glass">{icon('bell', 20)}</div>
    </div>
    <div class="ar-text">
      <div class="hello">صباح الخير، أليكس</div>
      <div class="meta">{vis('أبريل', '24', '←', 'مارس', '25', '·', 'دورة الراتب')}</div>
    </div>
  </div>

  <div class="card budget">
    <div class="between"><div class="meta">{vis('أيام', '<b>9</b>', 'متبقي')}</div><div class="ctitle">دورة أبريل</div></div>
    <div class="meta" style="margin-top:2px">{vis('أبريل', '24', '←', 'مارس', '25')}</div>
    <div class="hero" style="justify-content:flex-end;margin-top:16px">
      <span class="hero-lab">متبقي</span>{ar_amt(6660, big=True)}{legend_swatch('hatch')}
    </div>
    <div style="margin-top:12px">{bar(313, .63, today=.68, rtl=True)}</div>
    <div class="today" style="padding-left:{tick - 12:.0f}px">اليوم</div>
    <div class="between legend-wrap">
      <div class="amounts" style="text-align:left">
        {ar_amt(11340)}{ar_amt(6660)}<div class="strong">{ar_amt(18000)}</div>
      </div>
      <div class="legend" style="align-items:flex-end">
        <div><b>63%</b><span>المصروف</span>{legend_swatch('solid')}</div>
        <div><b>37%</b><span>المتبقي</span>{legend_swatch('hatch')}</div>
        <div><span>الميزانية</span>{legend_swatch('outline')}</div>
      </div>
    </div>
    <div class="dots"><span></span><span></span><span class="on"></span></div>
  </div>

  <div class="quick glass">
    <div class="q">{tile('pen', 'rgba(222,101,56,.14)', CLAY, 44, 22)}<span>اكتب</span></div>
    <div class="qdiv"></div>
    <div class="q">{tile('scan', 'rgba(222,101,56,.14)', CLAY, 44, 22)}<span>امسح</span></div>
    <div class="qdiv"></div>
    <div class="q">{tile('mic', 'rgba(222,101,56,.14)', CLAY, 44, 22)}<span>تحدّث</span></div>
  </div>

  <div class="card slim">
    {icon('chevl', 18, INK3)}<div class="count">{vis('3', 'من', '2', 'أُرسل')}</div>
    <div class="grow ar-text"><div class="rtitle">{vis('دعم العائلة')}</div><div class="rsub">{vis('شهريًا', 'د.إ', '3,300', '·', 'أشخاص', '3')}</div></div>
    {tile('heart', 'rgba(157,191,106,.25)', CANOPY, 40)}
  </div>

  <div class="section"><span class="link">عرض الكل</span><span class="caps">آخر العمليات</span></div>
  <div class="card list">
    {ar_row('salary', 'rgba(79,138,60,.13)', POS, ['الراتب'], ['مارس', '25', '·', 'الإمارات دبي الوطني'], ar_amt(19500, '+', color=POS))}
    {ar_row('cheque', 'rgba(222,101,56,.13)', CLAY, ['4', 'من', '3', 'شيك الإيجار'], ['أبريل', '1', '·', 'شيك'], ar_amt(6250, '−'))}
    {ar_row('cart', 'rgba(201,160,74,.18)', '#8A6A22', ['كارفور'], ['بقالة · اليوم'], ar_amt(312.50, '−'))}
  </div>
</div>
<div class="ai-btn glass" style="left:16px"><div class="orb">{icon('sparkle', 24, '#fff', 1.8)}</div></div>
<div class="tabbar glass" style="right:16px">{tabs}</div>"""


# ======================================================================
# 3. Voice entry sheet
# ======================================================================
def voice_body():
    wave = "".join(
        f'<rect x="{i*7}" y="{(40-h)/2}" width="3.5" height="{h}" rx="1.75" fill="{ORANGE if i < 26 else HATCH}"/>'
        for i, h in enumerate([8, 14, 22, 30, 18, 10, 24, 36, 28, 16, 12, 20, 32, 40, 26, 14, 8, 18, 28, 22, 12, 16, 30, 24, 10, 6, 12, 8, 14, 6, 10, 6])
    )
    return f"""
{status_bar()}
{sheet_backdrop(BG_HOME)}
<div class="sheet glass-sheet" style="top:300px">
  <div class="grabber"></div>
  <div class="between"><div class="stitle">Say it</div><div class="iconbtn glass sm">{icon('close', 18)}</div></div>
  <div class="meta center" style="margin-top:6px">Try “Paid 45 for groceries”, in English or Arabic</div>

  <div class="mic-wrap">
    <svg width="220" height="40" viewBox="0 0 220 40">{wave}</svg>
  </div>
  <div class="quote glass-inset">“Spent 45 on groceries at Carrefour, then sent Priya 1,000”</div>

  <div class="caps" style="margin:18px 4px 8px">Nestly understood 2 entries</div>
  <div class="card list flat">
    {row('cart', 'rgba(201,160,74,.18)', '#8A6A22', 'Carrefour', 'Groceries · Today · Cash', money(45, sign='−'))}
    {row('heart', 'rgba(157,191,106,.25)', CANOPY, 'Priya', 'Family support · Today', money(1000, sign='−'))}
  </div>

  <div class="btns">
    <div class="btn secondary">Edit</div>
    <div class="btn primary grow">{icon('check', 18, '#fff', 2.2)}Add 2 entries</div>
  </div>
</div>"""


# ======================================================================
# 4. Scan cheque sheet
# ======================================================================
def scan_body():
    return f"""
{status_bar()}
{sheet_backdrop(BG_HOME)}
<div class="sheet glass-sheet" style="top:150px">
  <div class="grabber"></div>
  <div class="between"><div class="stitle">Scan</div><div class="iconbtn glass sm">{icon('close', 18)}</div></div>
  <div class="seg glass-inset" style="margin-top:14px">
    <div>Receipt</div><div class="on">Cheque</div><div>Bill</div>
  </div>

  <div class="cheque">
    <div class="between"><span class="chq-bank">EMIRATES NBD</span><span class="chq-date">01 · 05 · 2026</span></div>
    <div class="chq-line"><span>Pay</span><b>Al Barsha Properties LLC</b></div>
    <div class="chq-line"><span>Dirhams</span><b>Six thousand two hundred fifty only</b></div>
    <div class="between" style="margin-top:10px"><span class="chq-micr">⑈000431⑈ 0260 ⑆</span><span class="chq-amt">AED 6,250.00</span></div>
    <div class="scan-ok">{icon('check', 16, '#fff', 2.4)}</div>
  </div>

  <div class="card list flat" style="margin-top:16px">
    <div class="kv"><span>Amount</span><b>{money(6250)}</b></div>
    <div class="kv"><span>Payee</span><b>Al Barsha Properties</b></div>
    <div class="kv"><span>Category</span><b>Rent</b></div>
    <div class="kv"><span>Cheque date</span><b>1 May 2026 <span class="chip warn">Post-dated</span></b></div>
  </div>

  <div class="card slim flat" style="margin-top:10px">
    {tile('bell', 'rgba(201,160,74,.18)', '#8A6A22', 36, 18)}
    <div class="grow"><div class="rtitle">Remind me 3 days before</div><div class="rsub">Check the account can cover it</div></div>
    <div class="toggle on"><span></span></div>
  </div>

  <div class="btns">
    <div class="btn secondary">{icon('repeat', 18)}Rescan</div>
    <div class="btn primary grow">{icon('check', 18, '#fff', 2.2)}Add expense</div>
  </div>
</div>"""


# ======================================================================
# 5. Activity (transactions)
# ======================================================================
def activity_body():
    return f"""
{status_bar()}
<div class="content">
  <div class="hdr"><div class="title">Activity</div>
    <div class="hdr-actions"><div class="iconbtn glass">{icon('filter', 20)}</div><div class="iconbtn glass accent">{icon('plus', 22, '#fff', 2)}</div></div>
  </div>
  <div class="search glass">{icon('search', 18, INK3)}<span>Search Talabat, rent, Mum…</span></div>
  <div class="pills">
    <div class="pill on">All</div><div class="pill">Income</div><div class="pill">Spending</div><div class="pill">Cash</div><div class="pill">Family</div>
  </div>

  <div class="summary glass">
    <div><div class="meta">In this cycle</div><div class="sumv" style="color:{POS}">{money(19500, sign='+')}</div></div>
    <div class="vdiv"></div>
    <div><div class="meta">Out this cycle</div><div class="sumv">{money(11340, sign='−')}</div></div>
  </div>

  <div class="caps grp">Today</div>
  <div class="card list">
    {row('cart', 'rgba(201,160,74,.18)', '#8A6A22', 'Carrefour', 'Groceries · Cash', money(312.50, sign='−'))}
    {row('bag', 'rgba(222,101,56,.13)', CLAY, 'Talabat', 'Food delivery · Mashreq card', money(68, sign='−'))}
    {row('car', 'rgba(61,122,148,.14)', WET, 'Salik', 'Transport · Auto-captured', money(8, sign='−'))}
  </div>
  <div class="caps grp">Mon, 13 Apr</div>
  <div class="card list">
    {row('heart', 'rgba(157,191,106,.25)', CANOPY, 'Mum · Al Ansari', 'Family support · ₹ 33,900', money(1500, sign='−'))}
    {row('bolt', 'rgba(201,160,74,.18)', '#8A6A22', 'DEWA', 'Utilities · Bill', money(412.30, sign='−'))}
  </div>
</div>
{tab_bar('activity')}"""


# ======================================================================
# 6. New transaction sheet
# ======================================================================
def new_tx_body():
    cats = [("cart", "Groceries", True), ("bag", "Food", False), ("car", "Transport", False),
            ("home", "Rent", False), ("bolt", "Bills", False), ("heart", "Family", False),
            ("cup", "Coffee", False), ("plus", "More", False)]
    grid = "".join(
        f'<div class="cat{" on" if on else ""}">{tile(ic, ORANGE if on else "rgba(255,255,255,.7)", "#fff" if on else INK, 46, 22)}<span>{lab}</span></div>'
        for ic, lab, on in cats
    )
    return f"""
{status_bar()}
{sheet_backdrop(BG_ACT)}
<div class="sheet glass-sheet" style="top:96px">
  <div class="grabber"></div>
  <div class="between"><div class="stitle">New entry</div><div class="iconbtn glass sm">{icon('close', 18)}</div></div>
  <div class="seg glass-inset" style="margin-top:14px"><div class="on">Expense</div><div>Income</div><div>Transfer</div></div>

  <div class="amount-in">
    <div class="curpick glass">AED {icon('chevd', 14, INK2, 2)}</div>
    <div class="bigamt">312<span class="dec big">.50</span></div>
    <div class="meta">≈ USD 85.08</div>
  </div>

  <div class="caps" style="margin:4px 4px 10px">Category</div>
  <div class="catgrid">{grid}</div>

  <div class="card list flat" style="margin-top:14px">
    <div class="kv">{tile('wallet', 'rgba(34,32,30,.06)', INK, 32, 17)}<span class="grow">Paid with</span><b>Cash</b>{icon('chev', 16, INK3)}</div>
    <div class="kv">{tile('calendar', 'rgba(34,32,30,.06)', INK, 32, 17)}<span class="grow">Date</span><b>Today · April cycle</b>{icon('chev', 16, INK3)}</div>
    <div class="kv">{tile('repeat', 'rgba(34,32,30,.06)', INK, 32, 17)}<span class="grow">Repeat</span><b>Never</b>{icon('chev', 16, INK3)}</div>
    <div class="kv">{tile('pen', 'rgba(34,32,30,.06)', INK, 32, 17)}<span class="grow muted">Add a note</span></div>
  </div>

  <div class="btns"><div class="btn primary grow">{icon('check', 18, '#fff', 2.2)}Add expense</div></div>
</div>"""


# ======================================================================
# 7. Insights
# ======================================================================
def insights_body():
    vals = [(ORANGE, "Rent", 6250), (DRY, "Groceries", 1240), (SHOOT, "Family", 2300),
            (WET, "Transport", 620), (CANOPY, "Bills", 412.30), (HATCH, "Other", 517.70)]
    total = sum(v for *_, v in vals)
    segs = [(v / total, c, n, v) for c, n, v in vals]
    a = 0
    paths = []
    for f, c, *_ in segs:
        a1 = a + f * 360
        paths.append(f'<path d="{arc(90, 90, 74, a + 4, a1 - 4)}" stroke="{c}" stroke-width="22" stroke-linecap="round" fill="none"/>')
        a = a1
    donut = f'<svg width="180" height="180" viewBox="0 0 180 180">{"".join(paths)}</svg>'
    cat_rows = ""
    limits = {"Rent": 6250, "Groceries": 1100, "Family": 3300, "Transport": 800}
    for f, c, name, v in segs[:4]:
        lim = limits[name]
        over = v > lim
        cat_rows += f"""
<div class="catrow">
  <div class="between"><span class="rtitle"><span class="dot" style="background:{c}"></span>{name}</span>
  <span class="lim"><b style="color:{NEG if over else INK}">{money(v)}</b> <span class="muted">of {lim:,}</span></span></div>
  <div style="margin-top:8px">{bar(305, v/lim, NEG if over else c, h=8)}</div>
</div>"""
    return f"""
{status_bar()}
<div class="content">
  <div class="hdr"><div class="title">Insights</div><div class="iconbtn glass">{icon('download', 20)}</div></div>
  <div class="pills"><div class="pill on">Spending</div><div class="pill">Income</div><div class="pill">Money flow</div><div class="pill">Family</div></div>
  <div class="stepper">{icon('chevl', 18, INK2)}<span>April cycle · 25 Mar → 24 Apr</span>{icon('chev', 18, INK2)}</div>

  <div class="card donut-card">
    <div class="donut">{donut}<div class="donut-c"><div class="meta">Spent</div><div class="dv">AED 11,340</div><div class="meta">of 18,000 budget</div></div></div>
    <div class="seg glass-inset sm" style="margin-top:14px;width:200px"><div class="on">Totals</div><div>Over time</div></div>
  </div>

  <div class="card slim insight">
    {tile('sparkle', 'rgba(222,101,56,.14)', CLAY, 40)}
    <div class="grow"><div class="rtitle">Groceries are <span style="color:{NEG}">AED 140</span> over</div><div class="rsub">Mostly weekend Carrefour runs. Move AED 140 from Coffee?</div></div>
  </div>

  <div class="section"><span class="caps">Categories</span><span class="caps">Spent / limit</span></div>
  <div class="card cats">{cat_rows}</div>
</div>
{tab_bar('insights')}"""


# ======================================================================
# 8. Goals
# ======================================================================
def goal_card(ic, bg, fg, name, saved, target, color, note, status, status_cls):
    return f"""
<div class="card goal">
  <div class="between">
    <div class="flex">{tile(ic, bg, fg, 40)}<div><div class="rtitle">{name}</div><div class="rsub">{note}</div></div></div>
    <div class="iconbtn plain">{icon('chev', 18, INK3)}</div>
  </div>
  <div class="between" style="margin-top:14px;align-items:flex-end">
    <div class="gval">{money(saved)}</div><div class="meta">of {target:,}</div>
  </div>
  <div style="margin-top:8px">{bar(313, saved/target, color)}</div>
  <div class="between" style="margin-top:10px"><span class="chip {status_cls}">{status}</span><span class="meta"><b>{saved/target:.0%}</b> saved</span></div>
</div>"""


def goals_body():
    return f"""
{status_bar()}
<div class="content">
  <div class="hdr"><div class="title">Goals</div><div class="iconbtn glass accent">{icon('plus', 22, '#fff', 2)}</div></div>

  <div class="summary glass">
    <div><div class="meta">Saved so far</div><div class="sumv">{money(21600)}</div></div>
    <div class="vdiv"></div>
    <div><div class="meta">This cycle</div><div class="sumv" style="color:{POS}">+AED 2,350</div></div>
  </div>

  {goal_card('shield', 'rgba(79,138,60,.13)', POS, 'Emergency fund', 12400, 30000, POS, 'AED 1,200 every payday', 'On track', 'ok')}
  {goal_card('moon', 'rgba(222,101,56,.13)', CLAY, 'Umrah with family', 6800, 18000, ORANGE, 'Target Feb 2027', 'On track', 'ok')}
  {goal_card('plane', 'rgba(61,122,148,.14)', WET, 'Summer in Kerala', 2400, 9000, WET, 'Target Jul 2026', '2 cycles behind', 'warn')}
</div>
{tab_bar('goals')}"""


# ======================================================================
# 9. New goal sheet (contribution plan)
# ======================================================================
def new_goal_body():
    colors = [ORANGE, POS, WET, DRY, CANOPY, "#7A5C9E"]
    dots = "".join(
        f'<span class="cdot{" on" if i == 0 else ""}" style="background:{c}"></span>' for i, c in enumerate(colors)
    )
    return f"""
{status_bar()}
{sheet_backdrop(BG_GOALS)}
<div class="sheet glass-sheet" style="top:96px">
  <div class="grabber"></div>
  <div class="between"><div class="stitle">New goal</div><div class="iconbtn glass sm">{icon('close', 18)}</div></div>

  <div class="card slim flat" style="margin-top:14px">
    {tile('moon', 'rgba(222,101,56,.13)', CLAY, 44, 22)}
    <div class="grow"><div class="flabel">Goal name</div><div class="fval">Umrah with family</div></div>
  </div>
  <div class="card slim flat" style="margin-top:8px">
    <div class="grow"><div class="flabel">Target amount</div><div class="fval big">{money(18000)}</div></div>
  </div>

  <div class="pills" style="margin-top:12px"><div class="pill">Emergency</div><div class="pill on">Travel</div><div class="pill">Home</div><div class="pill">Education</div><div class="pill">Wedding</div></div>

  <div class="caps" style="margin:18px 4px 8px">Plan contributions</div>
  <div class="linked">
    <div class="card slim flat"><div class="grow"><div class="flabel">Every payday</div><div class="fval">{money(1200)}</div></div></div>
    <div class="eq glass">=</div>
    <div class="card slim flat"><div class="grow"><div class="flabel">Reach it by</div><div class="fval">Feb 2027</div></div>{icon('calendar', 20, INK2)}</div>
  </div>
  <div class="presets"><div>6 cycles</div><div class="on">10 cycles</div><div>12 cycles</div></div>

  <div class="tip">{icon('sparkle', 18, CLAY)}<span>At your current savings rate this is realistic. You saved AED 2,350 last cycle.</span></div>

  <div class="caps" style="margin:16px 4px 10px">Colour</div>
  <div class="cdots">{dots}</div>

  <div class="btns"><div class="btn primary grow">{icon('goals', 18, '#fff', 2)}Create goal</div></div>
</div>"""


# ======================================================================
# 10. Nestly AI
# ======================================================================
def ai_body():
    mini = f"""
<div class="mini">
  <div class="between"><span class="meta">Talabat · April cycle</span><span class="chip bad">+18%</span></div>
  <div class="gval" style="margin-top:4px">{money(486)}</div>
  <div style="margin-top:8px">{bar(236, 486/400, NEG, h=8)}</div>
  <div class="between" style="margin-top:6px"><span class="meta">11 orders</span><span class="meta">Limit AED 400</span></div>
</div>"""
    return f"""
{status_bar()}
<div class="ai-top">
  <div class="iconbtn glass">{icon('chevl', 20)}</div>
  <div class="ai-name glass"><span class="orb sm">{icon('sparkle', 14, '#fff', 2)}</span>Nestly AI</div>
  <div class="iconbtn glass">{icon('clock', 20)}</div>
</div>
<div class="content chat" style="padding-top:116px">
  <div class="bubble bot">Morning Alex. You have <b>AED 6,660</b> left for 9 days, about <b>AED 740 a day</b>. Ask me anything about your money.</div>
  <div class="bubble me">How much did I spend on Talabat this cycle?</div>
  <div class="bubble bot">AED 486 across 11 orders. That's 18% more than March and AED 86 over your limit.{mini}</div>
  <div class="chips">
    <div class="chip-q glass">Move AED 100 from Coffee</div>
    <div class="chip-q glass">Can I afford a new phone?</div>
    <div class="chip-q glass" lang="ar" dir="rtl">كم صرفت على البقالة؟</div>
  </div>
</div>
<div class="composer">
  <div class="iconbtn glass">{icon('plus', 22)}</div>
  <div class="input glass"><span>Ask or log, e.g. “coffee 18”</span>{icon('mic', 20, INK2)}</div>
  <div class="iconbtn glass accent">{icon('send', 19, '#fff', 2)}</div>
</div>"""


# ======================================================================
# 11. Profile & settings
# ======================================================================
def set_row(ic, label, value=None, toggle=None, danger=False):
    col = NEG if danger else INK
    right = ""
    if toggle is not None:
        right = f'<div class="toggle{" on" if toggle else ""}"><span></span></div>'
    else:
        right = (f'<span class="muted">{value}</span>' if value else "") + icon("chev", 16, INK3)
    return f'<div class="kv">{tile(ic, "rgba(184,50,42,.10)" if danger else "rgba(34,32,30,.06)", col, 32, 17)}<span class="grow" style="color:{col}">{label}</span>{right}</div>'


def profile_body():
    return f"""
{status_bar()}
<div class="content tight">
  <div class="hdr"><div class="title">Profile</div><div class="iconbtn glass">{icon('close', 20)}</div></div>
  <div class="card prof">
    <div class="avatar big">AJ</div>
    <div class="grow"><div class="rtitle" style="font-size:19px">Alex Johnson</div><div class="rsub">alex@example.com · Dubai</div></div>
    <div class="iconbtn glass sm">{icon('pen', 16)}</div>
  </div>

  <div class="caps grp">Money</div>
  <div class="card list flat">
    {set_row('calendar', 'Payday', '25th of the month')}
    {set_row('salary', 'Monthly income', 'AED 19,500')}
    {set_row('globe', 'Currencies', 'AED · INR')}
    {set_row('users', 'Family support', '3 people')}
  </div>

  <div class="caps grp">Capture</div>
  <div class="card list flat">
    {set_row('phone', 'Read bank alerts', toggle=True)}
    {set_row('keyboard', 'Language', 'English · العربية')}
    {set_row('bell', 'Payday & cheque reminders', toggle=True)}
  </div>

  <div class="caps grp">Account</div>
  <div class="card list flat">
    {set_row('shield', 'Privacy & data')}
    {set_row('logout', 'Sign out', danger=True)}
  </div>
</div>"""


# ---------------------------------------------------------------- CSS
def build_css():
    return f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#D8D2C8;font-family:"Schibsted Grotesk","Helvetica Neue",Arial,sans-serif;color:{INK};
  display:flex;flex-wrap:wrap;gap:48px;padding:48px;-webkit-font-smoothing:antialiased}}
[lang=ar]{{font-family:"IBM Plex Sans Arabic","Schibsted Grotesk",sans-serif}}
.screen{{width:393px;height:852px;position:relative;overflow:hidden;flex:none}}
.status{{position:absolute;top:0;left:0;right:0;height:54px;display:flex;align-items:center;justify-content:space-between;padding:0 30px 0 44px;z-index:20}}
[dir=rtl] .status{{direction:ltr}}
.time{{font-weight:600;font-size:17px;letter-spacing:-.2px;font-family:"Schibsted Grotesk",sans-serif}}
.island{{position:absolute;left:50%;top:11px;width:124px;height:36px;margin-left:-62px;border-radius:20px;background:#000}}
.sys{{display:flex;gap:6px;align-items:center}}
.content{{position:absolute;inset:0;padding:62px 16px 0}}
.hdr{{display:flex;justify-content:space-between;align-items:center;margin:4px 4px 16px}}
.hdr-actions{{display:flex;gap:10px;align-items:center}}
.hello{{font-size:24px;font-weight:700;letter-spacing:-.4px}}
.title{{font-size:32px;font-weight:700;letter-spacing:-.8px}}
.meta{{font-size:13px;color:{INK2}}}
.meta b{{color:{INK};font-weight:600}}
.muted{{color:{INK3}}}
.center{{text-align:center}}
.between{{display:flex;justify-content:space-between;align-items:center}}
.flex{{display:flex;gap:12px;align-items:center}}
.grow{{flex:1;min-width:0}}

/* Liquid Glass */
.glass{{background:linear-gradient(160deg,rgba(255,255,255,.78),rgba(255,255,255,.42));
  border:1px solid rgba(255,255,255,.85);
  box-shadow:0 8px 28px rgba(70,45,20,.10),0 1px 2px rgba(70,45,20,.06),inset 0 1px 0 rgba(255,255,255,1),inset 0 -1px 1px rgba(255,255,255,.35);
  backdrop-filter:blur(24px) saturate(180%);-webkit-backdrop-filter:blur(24px) saturate(180%)}}
.glass-inset{{background:rgba(34,32,30,.05);border:1px solid rgba(34,32,30,.04)}}
.glass-sheet{{background:linear-gradient(180deg,rgba(252,250,246,.92),rgba(247,243,236,.96));
  border:1px solid rgba(255,255,255,.9);box-shadow:0 -10px 40px rgba(40,25,10,.18),inset 0 1px 0 #fff;
  backdrop-filter:blur(30px) saturate(180%);-webkit-backdrop-filter:blur(30px) saturate(180%)}}
.iconbtn{{width:44px;height:44px;border-radius:22px;display:flex;align-items:center;justify-content:center;color:{INK};flex:none}}
.iconbtn.sm{{width:34px;height:34px}}
.iconbtn.plain{{width:28px;height:28px}}
.iconbtn.accent{{background:linear-gradient(160deg,#EA8257,{ORANGE} 55%,#C9532A);border:1px solid rgba(255,255,255,.45);
  box-shadow:0 8px 20px rgba(222,101,56,.35),inset 0 1px 0 rgba(255,255,255,.55)}}
.avatar{{width:44px;height:44px;border-radius:22px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:{CLAY}}}
.avatar.big{{width:60px;height:60px;border-radius:30px;font-size:20px;color:#fff;background:linear-gradient(160deg,#EA8257,{ORANGE} 55%,#C9532A);box-shadow:inset 0 1px 0 rgba(255,255,255,.5)}}

/* Cards */
.card{{background:rgba(255,255,255,.80);border:1px solid rgba(255,255,255,.95);border-radius:22px;padding:18px;
  box-shadow:0 1px 2px rgba(70,45,20,.04)}}
.card.flat{{background:rgba(255,255,255,.72)}}
.card+.card{{margin-top:10px}}
.ctitle{{font-weight:600;font-size:16px}}
.rtitle{{font-weight:600;font-size:15px;display:flex;align-items:center;gap:8px}}
.rsub{{font-size:12.5px;color:{INK2};margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.num{{white-space:nowrap}}
[dir=rtl] .num{{direction:ltr;unicode-bidi:isolate;display:inline-block}}
.cur{{font-size:.82em;font-weight:500}}
.dec{{color:{INK3}}}
.hero{{display:flex;align-items:center;gap:8px;font-size:30px;font-weight:700;letter-spacing:-.6px}}
.hero .cur{{font-size:18px;font-weight:600}}
.hero-lab{{font-size:13px;font-weight:400;color:{INK2};letter-spacing:0;align-self:flex-end;margin-bottom:5px}}
.today{{font-size:11px;color:{INK2};margin-top:2px}}
.legend-wrap{{margin-top:10px;align-items:flex-start}}
.legend{{display:flex;flex-direction:column;gap:7px;font-size:13px;color:{INK2}}}
.legend>div{{display:flex;align-items:center;gap:8px}}
.legend b{{color:{INK};font-weight:600}}
.sw{{width:12px;height:12px;border-radius:3px;display:inline-block;flex:none}}
.amounts{{text-align:right;font-size:13.5px;display:flex;flex-direction:column;gap:6px;color:{INK2}}}
.amounts .strong{{color:{INK};font-weight:600}}
.dots{{display:flex;gap:5px;justify-content:center;margin-top:14px}}
.dots span{{width:6px;height:6px;border-radius:3px;background:{TRACK}}}
.dots .on{{width:18px;background:{INK}}}

.quick{{margin-top:12px;border-radius:24px;display:flex;align-items:center;padding:12px 8px}}
.q{{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;font-size:13px;font-weight:600}}
.qdiv{{width:1px;height:44px;background:rgba(34,32,30,.08)}}
.tile{{border-radius:12px;display:flex;align-items:center;justify-content:center;flex:none}}
.card.slim{{display:flex;align-items:center;gap:12px;padding:12px 14px;margin-top:12px}}
.count{{font-size:13px;font-weight:600;color:{CLAY}}}
.section{{display:flex;justify-content:space-between;align-items:center;margin:20px 6px 8px}}
.caps{{font-size:11.5px;letter-spacing:.9px;text-transform:uppercase;color:{INK2};font-weight:500}}
[lang=ar] .caps{{letter-spacing:0;font-size:13px}}
.grp{{margin:18px 6px 8px}}
.link{{font-size:14px;font-weight:600;color:{CLAY}}}
.card.list{{padding:4px 14px}}
.row{{display:flex;align-items:center;gap:12px;padding:11px 0}}
.row+.row,.kv+.kv{{border-top:1px solid rgba(34,32,30,.07)}}
.ramt{{text-align:right;font-weight:600;font-size:15px}}
[dir=rtl] .ramt{{text-align:left}}

/* Tab bar */
.tabbar{{position:absolute;bottom:26px;height:64px;width:291px;border-radius:32px;display:flex;align-items:center;padding:0 6px;z-index:10}}
.tab{{flex:1;height:52px;border-radius:26px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-size:10.5px;font-weight:600}}
.tab.on{{background:rgba(222,101,56,.13)}}
.ai-btn{{position:absolute;bottom:26px;width:64px;height:64px;border-radius:32px;display:flex;align-items:center;justify-content:center;z-index:10}}
.orb{{width:48px;height:48px;border-radius:24px;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(circle at 35% 28%,#F6B08E 0%,{ORANGE} 50%,#A9441D 100%);box-shadow:inset 0 1px 1px rgba(255,255,255,.6),0 4px 12px rgba(222,101,56,.35)}}
.orb.sm{{width:24px;height:24px;border-radius:12px}}

/* Sheets */
.backdrop{{position:absolute;inset:0;filter:blur(6px)}}
.ghost{{position:absolute;left:16px;right:16px;border-radius:22px;background:rgba(255,255,255,.75)}}
.dim{{position:absolute;inset:0;background:rgba(34,32,30,.30)}}
.sheet{{position:absolute;left:8px;right:8px;bottom:8px;border-radius:40px;padding:10px 18px 22px;z-index:5}}
.grabber{{width:38px;height:5px;border-radius:3px;background:rgba(34,32,30,.18);margin:0 auto 10px}}
.stitle{{font-size:22px;font-weight:700;letter-spacing:-.4px}}
.mic-wrap{{display:flex;justify-content:center;margin:22px 0 14px}}
.quote{{border-radius:18px;padding:14px 16px;font-size:16px;line-height:1.4;font-style:italic}}
.btns{{display:flex;gap:10px;margin-top:18px}}
.btn{{height:54px;border-radius:27px;display:flex;align-items:center;justify-content:center;gap:8px;font-weight:600;font-size:16px;padding:0 22px}}
.btn.primary{{background:{INK};color:#fff;box-shadow:0 8px 20px rgba(34,32,30,.22),inset 0 1px 0 rgba(255,255,255,.18)}}
.btn.secondary{{background:rgba(222,101,56,.12);color:{CLAY}}}
.seg{{display:flex;border-radius:16px;padding:3px}}
.seg>div{{flex:1;text-align:center;padding:9px 0;border-radius:13px;font-size:14px;font-weight:600;color:{INK2}}}
.seg .on{{background:#fff;color:{INK};box-shadow:0 2px 8px rgba(34,32,30,.10)}}
.seg.sm>div{{padding:7px 0;font-size:13px}}
.kv{{display:flex;align-items:center;gap:12px;padding:12px 0;font-size:14.5px}}
.kv>span:first-child{{flex:1;color:{INK2}}}
.kv b{{font-weight:600;display:flex;align-items:center;gap:6px}}
.chip{{font-size:11.5px;font-weight:600;padding:3px 8px;border-radius:8px}}
.chip.warn{{background:rgba(201,160,74,.20);color:#7E5F1B}}
.chip.ok{{background:rgba(79,138,60,.14);color:{POS}}}
.chip.bad{{background:rgba(184,50,42,.12);color:{NEG}}}
.toggle{{width:51px;height:31px;border-radius:16px;background:rgba(34,32,30,.14);padding:2px;flex:none}}
.toggle span{{display:block;width:27px;height:27px;border-radius:14px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.15)}}
.toggle.on{{background:{POS}}}
.toggle.on span{{margin-left:20px}}

/* Cheque */
.cheque{{position:relative;margin-top:16px;border-radius:18px;padding:16px;background:linear-gradient(135deg,#FBF6EC,#F1E6D2);
  border:1.5px dashed rgba(169,68,29,.45);font-size:12px;color:{INK2}}}
.chq-bank{{font-weight:700;letter-spacing:1.2px;font-size:11px;color:{INK}}}
.chq-date{{font-family:"IBM Plex Mono",monospace;font-size:12px;color:{INK}}}
.chq-line{{display:flex;gap:10px;margin-top:10px;border-bottom:1px solid rgba(34,32,30,.15);padding-bottom:4px}}
.chq-line b{{color:{INK};font-weight:500;font-family:"Newsreader",Georgia,serif;font-style:italic;font-size:14px}}
.chq-micr{{font-family:"IBM Plex Mono",monospace;letter-spacing:1px}}
.chq-amt{{font-family:"IBM Plex Mono",monospace;font-weight:500;color:{INK};border:1px solid rgba(34,32,30,.25);padding:4px 8px;border-radius:6px;background:rgba(255,255,255,.6)}}
.scan-ok{{position:absolute;top:-10px;right:-8px;width:30px;height:30px;border-radius:15px;background:{POS};display:flex;align-items:center;justify-content:center;border:3px solid #FAF7F1}}

/* Activity */
.search{{height:46px;border-radius:23px;display:flex;align-items:center;gap:10px;padding:0 16px;font-size:15px;color:{INK3}}}
.pills{{display:flex;gap:8px;margin-top:12px;overflow:hidden}}
.pill{{padding:9px 15px;border-radius:20px;font-size:14px;font-weight:600;background:rgba(255,255,255,.55);border:1px solid rgba(255,255,255,.9);white-space:nowrap;color:{INK2}}}
.pill.on{{background:{INK};color:#fff;border-color:{INK}}}
.summary{{margin-top:12px;border-radius:22px;display:flex;align-items:center;padding:14px 18px;gap:16px}}
.summary>div:not(.vdiv){{flex:1}}
.sumv{{font-size:18px;font-weight:700;margin-top:3px;letter-spacing:-.3px}}
.vdiv{{width:1px;height:36px;background:rgba(34,32,30,.10)}}

/* New entry */
.amount-in{{display:flex;flex-direction:column;align-items:center;margin:18px 0 14px;gap:6px}}
.curpick{{border-radius:16px;padding:5px 10px;font-size:13px;font-weight:600;display:flex;gap:4px;align-items:center}}
.bigamt{{font-size:52px;font-weight:700;letter-spacing:-1.5px;line-height:1}}
.catgrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px 6px}}
.cat{{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:12px;font-weight:600;color:{INK2}}}
.cat .tile{{border-radius:16px;border:1px solid rgba(255,255,255,.9);box-shadow:0 1px 3px rgba(70,45,20,.08)}}
.cat.on{{color:{CLAY}}}
.cat.on .tile{{box-shadow:0 6px 14px rgba(222,101,56,.35),inset 0 1px 0 rgba(255,255,255,.5)}}

/* Insights */
.stepper{{display:flex;justify-content:space-between;align-items:center;margin:16px 6px 10px;font-size:14px;font-weight:600}}
.donut-card{{display:flex;flex-direction:column;align-items:center}}
.donut{{position:relative;width:180px;height:180px}}
.donut-c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.dv{{font-size:22px;font-weight:700;letter-spacing:-.4px;margin:2px 0}}
.insight{{align-items:flex-start}}
.insight .rsub{{white-space:normal}}
.cats{{padding:6px 16px}}
.catrow{{padding:12px 0}}
.catrow+.catrow{{border-top:1px solid rgba(34,32,30,.07)}}
.dot{{width:8px;height:8px;border-radius:4px;display:inline-block}}
.lim{{font-size:13.5px}}
.lim b{{font-weight:600}}

/* Goals */
.goal{{padding:16px 18px}}
.gval{{font-size:22px;font-weight:700;letter-spacing:-.4px}}
.gval .cur{{font-size:14px}}

/* New goal */
.flabel{{font-size:12px;color:{INK2}}}
.fval{{font-size:17px;font-weight:600;margin-top:2px}}
.fval.big{{font-size:26px;font-weight:700;letter-spacing:-.5px}}
.linked{{position:relative;display:flex;flex-direction:column;gap:8px}}
.linked .card{{margin-top:0}}
.eq{{position:absolute;left:50%;top:50%;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:15px;display:flex;align-items:center;justify-content:center;font-weight:700;z-index:2}}
.presets{{display:flex;gap:8px;margin-top:10px}}
.presets div{{flex:1;text-align:center;padding:9px 0;border-radius:14px;font-size:13.5px;font-weight:600;color:{CLAY};background:rgba(255,255,255,.6)}}
.presets .on{{background:rgba(222,101,56,.14)}}
.tip{{display:flex;gap:10px;align-items:flex-start;margin-top:12px;padding:12px 14px;border-radius:16px;background:rgba(222,101,56,.08);font-size:13px;line-height:1.4;color:{INK2}}}
.cdots{{display:flex;gap:14px;padding:0 4px}}
.cdot{{width:30px;height:30px;border-radius:15px;display:block}}
.cdot.on{{box-shadow:0 0 0 3px #FAF7F1,0 0 0 5px {INK}}}

/* AI */
.ai-top{{position:absolute;top:58px;left:16px;right:16px;display:flex;justify-content:space-between;align-items:center;z-index:5}}
.ai-name{{height:44px;border-radius:22px;padding:0 16px 0 10px;display:flex;align-items:center;gap:8px;font-weight:700;font-size:16px}}
.chat{{display:flex;flex-direction:column;gap:10px}}
.bubble{{max-width:300px;padding:12px 15px;border-radius:22px;font-size:15px;line-height:1.42}}
.bubble.bot{{background:rgba(255,255,255,.82);border:1px solid #fff;border-bottom-left-radius:8px}}
.bubble.me{{align-self:flex-end;background:{INK};color:#fff;border-bottom-right-radius:8px}}
.mini{{margin-top:10px;padding:12px;border-radius:16px;background:rgba(34,32,30,.04)}}
.chips{{display:flex;flex-direction:column;align-items:flex-end;gap:8px;margin-top:6px}}
.chip-q{{border-radius:20px;padding:9px 14px;font-size:14px;font-weight:500}}
.composer{{position:absolute;left:16px;right:16px;bottom:30px;display:flex;gap:8px;align-items:center}}
.input{{flex:1;height:48px;border-radius:24px;display:flex;align-items:center;justify-content:space-between;padding:0 14px 0 16px;font-size:15px;color:{INK3}}}

/* Profile */
.prof{{display:flex;align-items:center;gap:14px}}
.vis{{display:flex;gap:6px;align-items:baseline}}
.vis>span{{padding:0 2px;white-space:nowrap}}
.ar-text .rsub{{overflow:visible}}
.ar-text{{text-align:right}}
.tight .grp{{margin:14px 6px 6px}}
.tight .kv{{padding:10px 0}}
.tight .hdr{{margin-bottom:12px}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700'
         '&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500'
         '&family=Newsreader:ital,wght@1,400;1,500&display=swap" rel="stylesheet">')

SCREENS = [
    ("01 Home", home_body, BG_HOME, {}),
    ("02 Home · Arabic", home_ar_body, BG_HOME, {"lang": "ar"}),
    ("03 Say it (voice)", voice_body, "#3B342D", {}),
    ("04 Scan cheque", scan_body, "#3B342D", {}),
    ("05 Activity", activity_body, BG_ACT, {}),
    ("06 New entry", new_tx_body, "#3B342D", {}),
    ("07 Insights", insights_body, BG_INS, {}),
    ("08 Goals", goals_body, BG_GOALS, {}),
    ("09 New goal", new_goal_body, "#3B342D", {}),
    ("10 Nestly AI", ai_body, BG_AI, {}),
    ("11 Profile", profile_body, BG_ACT, {}),
]


def main():
    parts = [screen(name, fn(), bg, **kw) for name, fn, bg, kw in SCREENS]
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Nestly screens</title>{FONTS}<style>{build_css()}</style></head>'
            f'<body>{"".join(parts)}</body></html>')
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html)//1024} KB, {len(parts)} screens)")


if __name__ == "__main__":
    main()

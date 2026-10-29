"""Option D: Arabic-first Nestly screens with 3D illustrations.

Brand from option C (#FF5002, IBM Plex Sans + Inter, Tajawal for Arabic) on
option B's layout, with Microsoft Fluent 3D emoji (MIT, assets/3d/) to make
the app warmer and easier to scan.

Every screen is written once, in logical order, and rendered in two languages
and two modes:

- web:   true RTL. dir="rtl" on the screen, flex/text flow from the
         direction, and LTR runs (numbers, brand names) wrapped in <bdi>.
         This follows the arabic-rtl-apps skill and is the reference for code.
- figma: the html_to_figma converter ignores dir="rtl" and Figma re-orders
         mixed Arabic/number strings, so RTL screens are baked into visual
         order: flex children reversed, and every text run single-direction.

    python3 design/nestly/build_d.py            # writes screens-d.html (web)
    python3 design/nestly/build_d.py --figma    # writes screens-d-figma.html
"""
import base64
import re
import sys
from pathlib import Path

import build as b
from build import icon
from build_b import flag

HERE = Path(__file__).parent
ASSETS = HERE / "assets" / "3d"

MAIN = "#FF5002"
MAIN_TEXT = "#C23D00"
INK = "#18120E"
INK2 = "#6B635C"
INK3 = "#A39A92"
POS = "#12A150"
NEG = "#E5484D"
TRACK = "#EEE8E3"
b.ORANGE, b.INK, b.TRACK, b.HATCH_ON = MAIN, INK, TRACK, False

HERO = ("radial-gradient(90% 70% at 85% 0%, rgba(255,170,110,.55) 0%, rgba(255,170,110,0) 60%),"
        "radial-gradient(80% 60% at 0% 100%, rgba(140,30,0,.45) 0%, rgba(140,30,0,0) 60%),"
        f"linear-gradient(160deg, #FF6A1F 0%, {MAIN} 45%, #C93C00 100%)")
BG = ("radial-gradient(110% 38% at 50% 0%, rgba(255,80,2,.12) 0%, rgba(255,80,2,0) 60%),"
      "linear-gradient(#FDEEE5, #F6F4F2 36%, #F7F5F3)")

MODE = "web"
LANG = "ar"


def rtl():
    return LANG == "ar"


def baked():
    return rtl() and MODE == "figma"


def L(ar, en):
    return ar if rtl() else en


# ---------------------------------------------------------------- text
LTR_RUN = r"[+−\-]?[A-Za-z0-9₹][A-Za-z0-9.,%₹&' ]*[A-Za-z0-9%₹]|[A-Za-z0-9]"
# Arabic run: letters, spaces and Arabic punctuation; a dot only inside a word (د.إ)
AR_RUN = r"[؀-ۿ](?:[؀-ۿً-ْ ،؟]|\.(?=[؀-ۿ]))*"
TOKENS = re.compile(AR_RUN + "|" + LTR_RUN + r"|\S")
PUNCT = set(".,،:؛!؟«»()")


def T(s):
    """A line of text. RTL web: <bdi> around LTR runs. RTL figma: visual-order runs."""
    if not rtl():
        return s
    if MODE == "web":
        return re.sub("(" + LTR_RUN + ")", r"<bdi>\1</bdi>", s)
    runs = []
    for r in (r.strip() for r in TOKENS.findall(s)):
        if not r:
            continue
        if len(r) > 1 and r[-1] in "،؟":    # trailing Arabic punctuation is its own run
            runs += [r[:-1].strip(), r[-1]]
        else:
            runs.append(r)
    if len(runs) == 1:
        return runs[0]
    spans = (f'<span class="{"pu" if r in PUNCT else "w"}">{r}</span>' for r in reversed(runs))
    return '<span class="vr">' + "".join(spans) + "</span>"


def lines(*ls):
    return "".join(f"<div>{T(x)}</div>" for x in ls)


# ---------------------------------------------------------------- layout
J = {"start": "flex-start", "end": "flex-end", "between": "space-between", "center": "center", "around": "space-around"}


def _j(key):
    j = J[key]
    if baked():
        j = {"flex-start": "flex-end", "flex-end": "flex-start"}.get(j, j)
    return j


def flow(*kids, justify="start", align="center", gap=0, cls="", style=""):
    """Horizontal row in logical order: first child sits at the reading start."""
    kids = list(reversed(kids)) if baked() else list(kids)
    return (f'<div class="flow {cls}" style="display:flex;justify-content:{_j(justify)};'
            f'align-items:{align};gap:{gap}px;{style}">{"".join(kids)}</div>')


def stack(*kids, align="start", gap=0, cls="", style=""):
    return (f'<div class="stack {cls}" style="display:flex;flex-direction:column;'
            f'align-items:{_j(align)};gap:{gap}px;{style}">{"".join(kids)}</div>')


def side(where="start"):
    """Physical side for absolute positioning: start is right in RTL."""
    return ("right" if rtl() else "left") if where == "start" else ("left" if rtl() else "right")


def chev_fwd():
    return "chevl" if rtl() else "chev"


def chev_back():
    return "chev" if rtl() else "chevl"


# ---------------------------------------------------------------- pieces
_img = {}


def img(name, size, style=""):
    if name not in _img:
        _img[name] = base64.b64encode((ASSETS / f"{name}.png").read_bytes()).decode()
    return (f'<img src="data:image/png;base64,{_img[name]}" width="{size}" height="{size}" '
            f'alt="" style="display:block;{style}">')


def t3d(name, box=44, size=30, bg="#FFF3EC"):
    return (f'<div class="t3d" style="width:{box}px;height:{box}px;background:{bg}">'
            f'{img(name, size)}</div>')


def amt(v, sign="", cls="", cur_cls="cur"):
    whole, dec = f"{abs(v):,.2f}".split(".")
    d = ' dir="ltr"' if MODE == "web" and rtl() else ""
    # Arabic: "−45.00 د.إ"; English: "−AED 45.00"
    num = f'<span class="num"{d}>{sign if rtl() else ""}{whole}<span class="dec">.{dec}</span></span>'
    cur = f'<span class="{cur_cls}">{"" if rtl() else sign}{L("د.إ", "AED")}</span>'
    parts = [num, cur] if rtl() else [cur, num]
    if baked():
        parts.reverse()
    return f'<span class="amt {cls}">{"".join(parts)}</span>'


def bar(w, frac, color=MAIN, today=None, h=8):
    return b.bar(w, frac, color, today=today, h=h, rtl=rtl())


def toggle(on=True):
    knob_left = (not on) if not rtl() else on
    return (f'<div class="toggle{" on" if on else ""}"><span style="margin-left:{0 if knob_left else 20}px">'
            f'</span></div>')


def chip(text, kind=""):
    return f'<span class="chip {kind}">{T(text)}</span>'


def status_bar(dark=False):
    c = "#fff" if dark else INK
    sb = b.status_bar(dark)
    time = f'<span class="time" style="color:{c}">9:41</span>'
    sys_icons = sb[sb.index('<span class="sys">'):sb.index("</span>\n</div>")] + "</span>"
    return (f'<div class="status">{flow(time, sys_icons, justify="between", style="width:100%")}'
            f'<div class="island"></div></div>')


def tab_bar(active):
    items = [f'<div class="tb">{icon(ic, 24, MAIN if ic == active else INK, 1.8)}'
             f'<span class="tdot" style="background:{MAIN if ic == active else "transparent"}"></span></div>'
             for ic in ["home", "activity", "insights", "goals", "sparkle"]]
    return f'<div class="tabbar glass">{flow(*items, justify="around", style="width:100%")}</div>'


def row(tile, title, sub, right, right_sub=None):
    rs = f'<div class="rsub">{T(right_sub)}</div>' if right_sub else ""
    return flow(tile,
                f'<div class="grow tx"><div class="rtitle">{T(title)}</div><div class="rsub">{T(sub)}</div></div>',
                f'<div class="ramt tx-end">{right}{rs}</div>', gap=12, cls="row")


def btn(text, kind="primary", ic=None, grow=False):
    inner = [T(text)]
    if ic:
        inner.insert(0, icon(ic, 18, "#fff" if kind == "primary" else MAIN_TEXT, 2.2))
    return f'<div class="btn {kind}{" grow" if grow else ""}">{flow(*inner, justify="center", gap=8)}</div>'


def backdrop():
    return f"""
<div class="backdrop" style="background:{BG}">
  <div style="position:absolute;left:0;right:0;top:0;height:372px;background:{HERO}"></div>
  <div class="ghost" style="top:392px;height:150px"></div>
  <div class="ghost" style="top:556px;height:110px"></div>
  <div class="ghost" style="top:680px;height:150px"></div>
</div><div class="dim"></div>"""


def sheet_head(title):
    close = f'<div class="iconbtn sm glass">{icon("close", 18)}</div>'
    return flow(f'<div class="stitle h">{T(title)}</div>', close, justify="between")


# ======================================================================
# Screens
# ======================================================================
def welcome():
    feats = [("studio_microphone", L("سجّل مصاريفك بصوتك", "Log spending by voice")),
             ("heart_with_ribbon", L("تابع دعم العائلة كل شهر", "Track family support every month")),
             ("shield", L("بدون ربط حسابك البنكي", "No bank login needed"))]
    feat_rows = "".join(flow(t3d(n, 44, 30, "#fff"), f'<div class="feat tx">{T(t)}</div>', gap=12, cls="featrow")
                        for n, t in feats)
    lang_chip = f'<div class="langchip glass">{icon("globe", 16, INK)}{L("English", "العربية")}</div>'
    return f"""
{status_bar()}
<div class="content">
  {flow(lang_chip, justify="end")}
  <div class="art">
    <div class="art-glow"></div>
    <div style="position:absolute;left:96px;top:30px">{img('money_bag', 200)}</div>
    <div style="position:absolute;{side('start')}:34px;top:12px;transform:rotate(-12deg)">{img('coin', 70)}</div>
    <div style="position:absolute;{side('end')}:40px;top:150px">{img('seedling', 62)}</div>
    <div style="position:absolute;{side('end')}:70px;top:6px">{img('sparkles', 40)}</div>
    <div style="position:absolute;{side('start')}:60px;top:170px;transform:rotate(14deg)">{img('coin', 44)}</div>
  </div>
  <div class="tx" style="margin-top:8px">
    <div class="wtitle h">{L("ميزانيتك تبدأ<br>من يوم الراتب", "Your budget starts<br>on payday")}</div>
    <div class="p" style="margin-top:10px">{L("نستلي يتابع مصاريفك من راتب إلى راتب، ويذكّرك بالفواتير والشيكات قبل موعدها.", "Nestly follows your spending from one payday to the next, and reminds you before bills and cheques are due.")}</div>
  </div>
  <div style="margin-top:18px">{feat_rows}</div>
  {flow('<span class="wdot on"></span>', '<span class="wdot"></span>', '<span class="wdot"></span>', justify="center", gap=6, style="margin-top:18px")}
  <div style="margin-top:16px">{btn(L("ابدأ الآن", "Get started"))}</div>
  <div class="link center" style="margin-top:14px">{L("لدي حساب بالفعل", "I already have an account")}</div>
</div>"""


def home():
    acts = [("studio_microphone", L("تحدّث", "Say it")), ("camera_with_flash", L("امسح", "Scan")),
            ("heart_with_ribbon", L("العائلة", "Family")), ("robot", L("المساعد", "Ask AI"))]
    act_html = flow(*[f'<div class="ra"><div class="ra-btn">{img(n, 34)}</div><span>{t}</span></div>' for n, t in acts],
                    justify="between", style="margin-top:20px")
    who = flow('<div class="av">AJ</div>',
               f'<div class="tx"><div class="hb-sm">{L("صباح الخير", "Good morning")}</div>'
               f'<div class="hb-name h">{L("أليكس جونسون", "Alex Johnson")}</div></div>', gap=10)
    btns = flow(f'<div class="iconbtn onmain">{icon("search", 20, "#fff")}</div>',
                f'<div class="iconbtn onmain">{icon("bell", 20, "#fff")}</div>', gap=10)
    budget = f"""
<div class="card">
  {flow(flow(t3d('seedling', 40, 28), f'<div class="ctitle h">{L("دورة أبريل", "April pay cycle")}</div>', gap=10),
        chip(L("9 أيام متبقية", "9 days left"), "main"), justify="between")}
  {flow(f'<div class="tx"><div class="meta">{L("المتبقي للإنفاق", "Left to spend")}</div><div class="gval h">{amt(6660)}</div></div>',
        f'<div class="tx-end meta">{lines(L("من 18,000", "of 18,000"), L("740 يوميًا", "740 a day"))}</div>',
        justify="between", align="flex-end", style="margin-top:12px")}
  <div style="margin-top:12px">{bar(321, .63, today=.68)}</div>
  {flow(f'<span class="meta">{T(L("صرفت 63%", "Spent 63%"))}</span>', f'<span class="meta">{L("اليوم", "Today")}</span>', justify="between", style="margin-top:6px")}
</div>"""
    promo = f"""
<div class="card promo">
  <div class="promo-art" style="{side('end')}:10px">{img('heart_with_ribbon', 86)}</div>
  <div class="tx" style="max-width:250px">
    <div class="ctitle h">{L("دعم العائلة", "Family support")}</div>
    <div class="p sm" style="margin-top:6px">{lines(L("تحويل أمي 1,500 د.إ مستحق", "Mum's AED 1,500 is due in 3 days."), L("خلال 3 أيام، ورصيدك يغطيه.", "Your balance covers it."))}</div>
  </div>
  {flow(f'<div class="promo-btn">{flow(T(L("تحديد كمُرسَل", "Mark as sent")), icon(chev_fwd(), 16, INK, 2), gap=4)}</div>', style="margin-top:12px")}
</div>"""
    up = f"""
{flow(f'<span class="stitle-b h">{L("القادم", "Upcoming")}</span>', f'<span class="link">{L("عرض الكل", "See all")}</span>', justify="between", cls="section")}
<div class="card list">
  {row(t3d('high_voltage'), L("ديوا", "DEWA"), L("تستحق 28 أبريل · بعد 3 أيام", "Due 28 Apr · in 3 days"), amt(412.30))}
  {row(t3d('house'), L("شيك الإيجار 4 من 4", "Rent cheque 4 of 4"), L("يُصرف 1 مايو · مؤجل", "Clears 1 May · post-dated"), amt(6250))}
</div>"""
    return f"""
<div class="hero" style="background:{HERO}">
  {status_bar(dark=True)}
  {flow(who, btns, justify="between", style="margin-top:4px")}
  <div class="hero-art" style="{side('end')}:10px">{img('money_bag', 104)}</div>
  <div class="tx" style="margin-top:20px">
    <div class="hb-sm">{T(L("الرصيد الإجمالي · 4 حسابات", "Total balance · 4 accounts"))}</div>
    <div class="hamt h">{amt(24892.65, cur_cls="hcur")}</div>
    <div class="hb-chip">{T(L("وفّرت 2,350 د.إ هذه الدورة", "AED 2,350 saved this cycle"))}</div>
  </div>
  {act_html}
</div>
<div class="panel">{budget}{promo}{up}</div>
{tab_bar('home')}"""


def say_it():
    wave_h = [8, 14, 22, 30, 18, 10, 24, 36, 28, 16, 12, 20, 32, 40, 26, 14, 8, 18, 28, 22, 12, 16, 30, 24, 10, 6, 12, 8, 14, 6, 10, 6]
    n = len(wave_h)
    rects = "".join(
        f'<rect x="{(n - 1 - i if rtl() else i) * 7}" y="{(40 - h) / 2}" width="3.5" height="{h}" rx="1.75" fill="{MAIN if i < 22 else "#DDD3CB"}"/>'
        for i, h in enumerate(wave_h))
    return f"""
{status_bar(dark=True)}
{backdrop()}
<div class="sheet glass-sheet" style="top:206px">
  <div class="grabber"></div>
  {sheet_head(L("تحدّث", "Say it"))}
  <div class="center" style="margin-top:2px">{img('studio_microphone', 84, 'margin:0 auto')}</div>
  <div class="meta center" style="margin-top:6px">{L("قلها بالعربي أو بالإنجليزي، وسنفهمها", "Say it in Arabic or English, we'll understand")}</div>
  <div class="center" style="margin:14px 0"><svg width="{n*7}" height="40" viewBox="0 0 {n*7} 40">{rects}</svg></div>
  <div class="quote tx">{lines(L("«صرفت 45 على البقالة في كارفور،", "“Spent 45 on groceries at Carrefour,"), L("وأرسلت لبريا 1,000»", "then sent Priya 1,000”"))}</div>
  <div class="caps tx" style="margin:16px 4px 8px">{L("فهمنا قيدين", "We understood 2 entries")}</div>
  <div class="card list flat">
    {row(t3d('shopping_cart', 40, 28, '#fff'), L("كارفور", "Carrefour"), L("بقالة · اليوم · نقدًا", "Groceries · Today · Cash"), amt(45, "−"))}
    {row(t3d('heart_with_ribbon', 40, 28, '#fff'), L("بريا", "Priya"), L("دعم العائلة · اليوم", "Family support · Today"), amt(1000, "−"))}
  </div>
  {flow(btn(L("أضف القيدين", "Add 2 entries"), "primary", "check", grow=True), btn(L("تعديل", "Edit"), "secondary"), gap=10, style="margin-top:16px")}
</div>"""


def scan():
    seg = flow(*[f'<div class="{c}">{t}</div>' for t, c in [(L("إيصال", "Receipt"), ""), (L("شيك", "Cheque"), "on"), (L("فاتورة", "Bill"), "")]],
               justify="between", cls="seg")
    return f"""
{status_bar(dark=True)}
{backdrop()}
<div class="sheet glass-sheet" style="top:120px">
  <div class="grabber"></div>
  {sheet_head(L("امسح", "Scan"))}
  <div style="margin-top:12px">{seg}</div>
  <div class="cheque" dir="ltr">
    <div style="display:flex;justify-content:space-between"><span class="chq-bank">EMIRATES NBD · بنك الإمارات دبي الوطني</span></div>
    <div class="chq-line"><span>Pay</span><b>Al Barsha Properties LLC</b></div>
    <div class="chq-line"><span>Dirhams</span><b>Six thousand two hundred fifty only</b></div>
    <div style="display:flex;justify-content:space-between;margin-top:10px"><span class="chq-micr">01 · 05 · 2026</span><span class="chq-amt">AED 6,250.00</span></div>
    <div class="scan-ok">{img('check_mark_button', 34)}</div>
  </div>
  <div class="card list flat" style="margin-top:14px">
    {flow(f'<span class="k">{L("المبلغ", "Amount")}</span>', f'<b>{amt(6250)}</b>', justify="between", cls="kv")}
    {flow(f'<span class="k">{L("المستفيد", "Payee")}</span>', f'<b>{T("Al Barsha Properties")}</b>', justify="between", cls="kv")}
    {flow(f'<span class="k">{L("التصنيف", "Category")}</span>', f'<b>{L("إيجار", "Rent")}</b>', justify="between", cls="kv")}
    {flow(f'<span class="k">{L("تاريخ الشيك", "Cheque date")}</span>', flow(f'<b>{T(L("1 مايو 2026", "1 May 2026"))}</b>', chip(L("مؤجل", "Post-dated"), "warn"), gap=6), justify="between", cls="kv")}
  </div>
  <div class="card slim flat" style="margin-top:10px">
    {flow(t3d('bell', 40, 28, '#fff'), f'<div class="grow tx"><div class="rtitle">{T(L("ذكّرني قبل 3 أيام", "Remind me 3 days before"))}</div><div class="rsub">{L("لتتأكد أن الرصيد يكفي", "So the account can cover it")}</div></div>', toggle(True), gap=12)}
  </div>
  {flow(btn(L("أضف المصروف", "Add expense"), "primary", "check", grow=True), btn(L("إعادة المسح", "Rescan"), "secondary"), gap=10, style="margin-top:16px")}
</div>"""


def activity():
    pills = flow(*[f'<div class="pill{" on" if i == 0 else ""}">{t}</div>' for i, t in enumerate(
        [L("الكل", "All"), L("الدخل", "Income"), L("المصاريف", "Spending"), L("نقدًا", "Cash"), L("العائلة", "Family")])],
                 gap=8, style="margin-top:12px;overflow:hidden")
    summary = flow(f'<div class="tx grow"><div class="meta">{L("دخل هذه الدورة", "In this cycle")}</div><div class="sumv h" style="color:{POS}">{amt(19500, "+")}</div></div>',
                   '<div class="vdiv"></div>',
                   f'<div class="tx grow"><div class="meta">{L("مصاريف هذه الدورة", "Out this cycle")}</div><div class="sumv h">{amt(11340, "−")}</div></div>',
                   gap=16, cls="summary glass")
    return f"""
{status_bar()}
<div class="content">
  {flow(f'<div class="title h">{L("العمليات", "Activity")}</div>', flow(f'<div class="iconbtn glass">{icon("filter", 20)}</div>', f'<div class="iconbtn accent">{icon("plus", 22, "#fff", 2)}</div>', gap=10), justify="between", cls="hdr")}
  <div class="search glass">{flow(icon("search", 18, INK3), f'<span>{T(L("ابحث: طلبات، إيجار، أمي…", "Search Talabat, rent, Mum…"))}</span>', gap=10)}</div>
  {pills}
  {summary}
  <div class="caps grp tx">{L("اليوم", "Today")}</div>
  <div class="card list">
    {row(t3d('shopping_cart'), L("كارفور", "Carrefour"), L("بقالة · نقدًا", "Groceries · Cash"), amt(312.50, "−"))}
    {row(t3d('takeout_box'), L("طلبات", "Talabat"), L("توصيل طعام · بطاقة المشرق", "Food delivery · Mashreq card"), amt(68, "−"))}
    {row(t3d('automobile'), L("سالك", "Salik"), L("مواصلات · التقاط تلقائي", "Transport · Auto-captured"), amt(8, "−"))}
  </div>
  <div class="caps grp tx">{T(L("الإثنين، 13 أبريل", "Mon, 13 Apr"))}</div>
  <div class="card list">
    {row(t3d('heart_with_ribbon'), L("أمي · الأنصاري", "Mum · Al Ansari"), L("دعم العائلة · ₹ 33,900", "Family support · ₹ 33,900"), amt(1500, "−"))}
  </div>
</div>
{tab_bar('activity')}"""


def insights():
    vals = [("house", MAIN, L("الإيجار", "Rent"), 6250, 6250), ("shopping_cart", "#F5A524", L("البقالة", "Groceries"), 1240, 1100),
            ("heart_with_ribbon", "#A78BFA", L("العائلة", "Family"), 2300, 3300), ("automobile", "#14B8A6", L("المواصلات", "Transport"), 620, 800)]
    total = 11340
    a, paths = 0, []
    for _, c, _, v, _ in vals + [(None, "#DDD3CB", None, total - sum(x[3] for x in vals), None)]:
        a1 = a + v / total * 360
        a0d, a1d = (360 - a1, 360 - a) if rtl() else (a, a1)
        paths.append(f'<path d="{b.arc(80, 80, 64, a0d + 4, a1d - 4)}" stroke="{c}" stroke-width="20" stroke-linecap="round" fill="none"/>')
        a = a1
    cats = "".join(f"""
<div class="catrow">
  {flow(flow(t3d(n, 36, 24), f'<span class="rtitle">{name}</span>', gap=10), f'<span class="lim">{flow(f"<b style=color:{NEG if v > lim else INK}>{amt(v)}</b>", f"<span class=muted>{T(L(f'من {lim:,}', f'of {lim:,}'))}</span>", gap=4)}</span>', justify="between")}
  <div style="margin-top:8px">{bar(305, min(v / lim, 1), NEG if v > lim else c)}</div>
</div>""" for n, c, name, v, lim in vals[:3])
    return f"""
{status_bar()}
<div class="content">
  {flow(f'<div class="title h">{L("التحليلات", "Insights")}</div>', f'<div class="iconbtn glass">{icon("download", 20)}</div>', justify="between", cls="hdr")}
  {flow(icon(chev_back(), 18, INK2), f'<span class="stepper">{T(L("دورة أبريل · 25 مارس ← 24 أبريل", "April cycle · 25 Mar → 24 Apr"))}</span>', icon(chev_fwd(), 18, INK2), justify="between", style="margin:2px 6px 10px")}
  <div class="card">
    {flow(f'<div class="donut"><svg width="160" height="160" viewBox="0 0 160 160">{"".join(paths)}</svg><div class="donut-c"><div class="meta">{L("المصروف", "Spent")}</div><div class="dv h">{T(L("11,340 د.إ", "AED 11,340"))}</div><div class="meta">{T(L("من 18,000", "of 18,000"))}</div></div></div>',
           f'<div class="stack-legend">{"".join(flow(f"<span class=dot style=background:{c}></span>", f"<span class=meta>{name}</span>", gap=6, style="margin:5px 0") for _, c, name, _, _ in vals)}</div>',
           justify="between")}
  </div>
  <div class="card slim insight">
    {flow(t3d('light_bulb', 48, 34), f'<div class="grow tx"><div class="rtitle">{T(L("البقالة تجاوزت الحد بـ 140 د.إ", "Groceries are AED 140 over"))}</div><div class="rsub wrap">{L("أغلبها مشتريات نهاية الأسبوع. ننقل المبلغ من بند القهوة؟", "Mostly weekend Carrefour runs. Move it from Coffee?")}</div></div>', gap=12, align="flex-start")}
  </div>
  {flow(f'<span class="stitle-b h">{L("الفئات", "Categories")}</span>', f'<span class="meta">{L("المصروف / الحد", "Spent / limit")}</span>', justify="between", cls="section")}
  <div class="card cats">{cats}</div>
</div>
{tab_bar('insights')}"""


def goals():
    def goal(n, name, note, saved, target, color, status, kind):
        return f"""
<div class="card goal">
  {flow(t3d(n, 56, 40), f'<div class="grow tx"><div class="rtitle">{name}</div><div class="rsub">{T(note)}</div></div>', icon(chev_fwd(), 18, INK3), gap=12)}
  {flow(f'<div class="gval h">{amt(saved)}</div>', f'<div class="meta">{T(L(f"من {target:,}", f"of {target:,}"))}</div>', justify="between", align="flex-end", style="margin-top:12px")}
  <div style="margin-top:8px">{bar(313, saved / target, color)}</div>
  {flow(chip(status, kind), f'<span class="meta">{T(L(f"{saved / target:.0%} مُدّخر", f"{saved / target:.0%} saved"))}</span>', justify="between", style="margin-top:10px")}
</div>"""
    summary = flow(t3d('money_with_wings', 52, 38, '#fff'),
                   f'<div class="tx grow"><div class="meta">{L("ادّخرت حتى الآن", "Saved so far")}</div><div class="sumv h">{amt(21600)}</div></div>',
                   f'<div class="tx-end"><div class="meta">{L("هذه الدورة", "This cycle")}</div><div class="sumv h" style="color:{POS}">{T(L("+2,350", "+2,350"))}</div></div>',
                   gap=12, cls="summary glass")
    return f"""
{status_bar()}
<div class="content">
  {flow(f'<div class="title h">{L("الأهداف", "Goals")}</div>', f'<div class="iconbtn accent">{icon("plus", 22, "#fff", 2)}</div>', justify="between", cls="hdr")}
  {summary}
  {goal('shield', L("صندوق الطوارئ", "Emergency fund"), L("1,200 د.إ كل يوم راتب", "AED 1,200 every payday"), 12400, 30000, POS, L("على المسار", "On track"), "ok")}
  {goal('kaaba', L("عمرة مع العائلة", "Umrah with family"), L("الموعد فبراير 2027", "Target Feb 2027"), 6800, 18000, MAIN, L("على المسار", "On track"), "ok")}
  {goal('airplane', L("صيف في كيرالا", "Summer in Kerala"), L("الموعد يوليو 2026", "Target Jul 2026"), 2400, 9000, "#14B8A6", L("متأخر دورتين", "2 cycles behind"), "warn")}
</div>
{tab_bar('goals')}"""


def family():
    people = [("M", "#F59E0B", "IN", L("أمي", "Mum"), L("كيرالا", "Kerala")), ("O", "#0EA5E9", "EG", L("عمر", "Omar"), L("القاهرة", "Cairo")),
              ("A", "#EC4899", "PH", L("آنا", "Ana"), L("مانيلا", "Manila")), ("B", "#10B981", "PK", L("بلال", "Bilal"), L("لاهور", "Lahore"))]
    ini = {"M": L("أ", "M"), "O": L("ع", "O"), "A": L("آ", "A"), "B": L("ب", "B")}

    def person(i, c, f, size=58):
        return (f'<div class="person" style="width:{size}px;height:{size}px;background:{c};font-size:{20 if size > 50 else 15}px">{ini[i]}'
                f'<span class="pflag" style="{side("end")}:-3px">{flag(f, 22 if size > 50 else 16)}</span></div>')

    recents = flow(*[f'<div class="rec">{person(i, c, f)}<div class="rtitle center">{n}</div><div class="rsub center">{s}</div></div>'
                     for i, c, f, n, s in people], justify="between", style="margin-top:10px")
    acts = flow(*[f'<div class="a3">{t3d(n, 56, 38, "#fff")}<span>{t}</span></div>' for n, t in
                  [("envelope_with_arrow", L("سجّل تحويلًا", "Log transfer")), ("chart_increasing", L("أسعار الصرف", "Rates")),
                   ("spiral_calendar", L("جدولة", "Schedule"))]], justify="around", cls="actions3")

    def prow(i, c, f, name, sub, status, kind):
        return flow(person(i, c, f, 42), f'<div class="grow tx"><div class="rtitle">{name}</div><div class="rsub">{T(sub)}</div></div>',
                    chip(status, kind), icon(chev_fwd(), 16, INK3), gap=12, cls="row")

    return f"""
{status_bar()}
<div class="content">
  {flow(f'<div class="title h">{L("إرسال للأهل", "Send home")}</div>', f'<div class="iconbtn accent">{icon("plus", 22, "#fff", 2)}</div>', justify="between", cls="hdr")}
  <div class="meta tx" style="margin:-8px 4px 12px">{T(L("دعم العائلة · 3,300 د.إ شهريًا", "Family support · AED 3,300 a month"))}</div>
  {acts}
  {flow(f'<span class="stitle-b h">{L("الأشخاص", "People")}</span>', f'<span class="link">{L("إدارة", "Manage")}</span>', justify="between", cls="section")}
  {recents}
  <div class="card list" style="margin-top:16px">
    {prow("M", "#F59E0B", "IN", L("أمي", "Mum"), L("1,500 د.إ · البنك الفيدرالي", "AED 1,500 · Federal Bank"), L("بعد 3 أيام", "Due in 3 days"), "warn")}
    {prow("O", "#0EA5E9", "EG", L("عمر", "Omar"), L("800 د.إ · CIB", "AED 800 · CIB"), L("أُرسل 12 أبريل", "Sent 12 Apr"), "ok")}
    {prow("A", "#EC4899", "PH", L("آنا", "Ana"), L("1,000 د.إ · BDO", "AED 1,000 · BDO"), L("أُرسل اليوم", "Sent today"), "ok")}
  </div>
</div>
{tab_bar('home')}"""


def success():
    return f"""
{status_bar(dark=True)}
{backdrop()}
<div class="modal">
  <div class="center">{img('party_popper', 110, 'margin:-74px auto 0')}</div>
  <div class="stitle h center" style="margin-top:10px">{L("تم تسجيل التحويل", "Logged as sent")}</div>
  <div class="p center" style="margin-top:6px">{lines(L("1,500 د.إ لأمي، حوالي ₹ 33,900.", "AED 1,500 to Mum, about ₹ 33,900."), L("اكتمل دعم العائلة لشهر أبريل: 3 من 3.", "Family support is 3 of 3 for April."))}</div>
  <div style="margin-top:18px">{btn(L("العودة للرئيسية", "Back to home"))}</div>
  <div class="link center" style="margin-top:14px">{L("مشاركة الإيصال", "Share receipt")}</div>
</div>"""


SCREENS = [("01", "Welcome", "الترحيب", welcome, BG), ("02", "Home", "الرئيسية", home, BG),
           ("03", "Say it", "تحدّث", say_it, "#2A1A10"), ("04", "Scan cheque", "مسح شيك", scan, "#2A1A10"),
           ("05", "Activity", "العمليات", activity, BG), ("06", "Insights", "التحليلات", insights, BG),
           ("07", "Goals", "الأهداف", goals, BG), ("08", "Send home", "إرسال للأهل", family, BG),
           ("09", "Logged as sent", "تم التسجيل", success, "#2A1A10")]


# ---------------------------------------------------------------- CSS
def css():
    head = '"IBM Plex Sans","Helvetica Neue",Arial,sans-serif'
    ar = '"Tajawal","IBM Plex Sans Arabic",sans-serif'
    return f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#DCD5CF;font-family:"Inter","Helvetica Neue",Arial,sans-serif;color:{INK};display:flex;flex-wrap:wrap;gap:48px;padding:48px;-webkit-font-smoothing:antialiased}}
.screen{{width:393px;height:852px;position:relative;overflow:hidden;flex:none;font-size:15px}}
.h{{font-family:{head}}}
.screen[lang=ar],.screen[lang=ar] *{{font-family:{ar};letter-spacing:0!important}}
.tx{{text-align:start}}
.tx-end{{text-align:end}}
.baked .tx{{text-align:right}}
.baked .tx-end{{text-align:left}}
.center{{text-align:center}}
.vr{{display:inline-flex;align-items:baseline;white-space:nowrap}}
.vr .w{{padding:0 .14em}}
.grow{{flex:1;min-width:0}}
.status{{position:absolute;top:0;left:0;right:0;height:54px;display:flex;align-items:center;padding:0 30px;z-index:20}}
.time{{font-family:"Inter",sans-serif!important;font-weight:600;font-size:17px}}
.island{{position:absolute;left:50%;top:11px;width:124px;height:36px;margin-left:-62px;border-radius:20px;background:#000}}
.sys{{display:flex;gap:6px;align-items:center;direction:ltr}}
.content{{position:absolute;inset:0;padding:62px 16px 0}}
.hdr{{margin:4px 4px 16px}}
.title{{font-size:30px;font-weight:600;letter-spacing:-.6px}}
[lang=ar] .title{{font-weight:700;font-size:30px}}
.meta{{font-size:13px;color:{INK2};line-height:1.5}}
[lang=ar] .meta{{font-size:13.5px;font-weight:500}}
.muted{{color:{INK3}}}
.p{{font-size:15px;line-height:1.55;color:{INK2}}}
[lang=ar] .p{{line-height:1.8;font-size:16px}}
.p.sm{{font-size:14px}}
[lang=ar] .p.sm{{font-size:15px}}
.link{{font-size:14px;font-weight:600;color:{MAIN_TEXT}}}
[lang=ar] .link{{font-weight:700}}
.caps{{font-size:13.5px;font-weight:600}}
.grp{{margin:16px 6px 8px}}
.glass{{background:rgba(255,255,255,.80);border:1px solid rgba(255,255,255,.95);box-shadow:0 8px 24px rgba(70,35,10,.08),inset 0 1px 0 #fff;backdrop-filter:blur(24px) saturate(180%);-webkit-backdrop-filter:blur(24px) saturate(180%)}}
.card{{background:#fff;border:1px solid rgba(24,18,14,.04);border-radius:22px;padding:16px;box-shadow:0 1px 3px rgba(70,35,10,.05);position:relative}}
.card+.card{{margin-top:10px}}
.card.flat{{background:#F6F4F1;border-color:transparent;box-shadow:none}}
.card.list{{padding:2px 14px}}
.card.slim{{padding:12px 14px;margin-top:10px}}
.row{{padding:11px 0}}
.row+.row,.kv+.kv{{border-top:1px solid rgba(24,18,14,.07)}}
.t3d{{border-radius:14px;display:flex;align-items:center;justify-content:center;flex:none}}
.ctitle{{font-weight:600;font-size:16px}}
[lang=ar] .ctitle{{font-weight:700;font-size:17px}}
.rtitle{{font-weight:600;font-size:15px}}
[lang=ar] .rtitle{{font-weight:700;font-size:15.5px}}
.rsub{{font-size:12.5px;color:{INK2};margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
[lang=ar] .rsub{{font-size:13px;font-weight:500}}
.rsub.wrap{{white-space:normal;line-height:1.5}}
[lang=ar] .rsub.wrap{{line-height:1.7}}
.ramt{{font-weight:600;font-size:15px;white-space:nowrap}}
.amt{{display:inline-flex;gap:4px;align-items:baseline;white-space:nowrap}}
.cur{{font-size:.8em;font-weight:500}}
.dec{{color:{INK3}}}
.num{{white-space:nowrap}}
.chip{{display:inline-block;font-size:12px;font-weight:600;padding:4px 9px;border-radius:9px;white-space:nowrap}}
[lang=ar] .chip{{font-weight:700;font-size:12.5px}}
.chip.main{{background:#FFEADF;color:{MAIN_TEXT}}}
.chip.ok{{background:rgba(18,161,80,.12);color:#0E7C3E}}
.chip.warn{{background:rgba(245,165,36,.18);color:#8A5A0B}}
.iconbtn{{width:44px;height:44px;border-radius:22px;display:flex;align-items:center;justify-content:center;flex:none}}
.iconbtn.sm{{width:34px;height:34px}}
.iconbtn.accent{{background:linear-gradient(160deg,#FF7A3D,{MAIN} 55%,#D94300);box-shadow:0 8px 20px rgba(255,80,2,.35),inset 0 1px 0 rgba(255,255,255,.5)}}
.iconbtn.onmain{{background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.3)}}
.btn{{height:54px;border-radius:27px;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:16px;padding:0 22px}}
[lang=ar] .btn{{font-weight:700;font-size:17px;height:56px}}
.btn.primary{{background:{INK};color:#fff;box-shadow:0 8px 20px rgba(24,18,14,.2)}}
.btn.secondary{{background:#FFEFE6;color:{MAIN_TEXT}}}
.btn.grow{{flex:1}}
.toggle{{width:51px;height:31px;border-radius:16px;background:rgba(24,18,14,.14);padding:2px;flex:none}}
.toggle span{{display:block;width:27px;height:27px;border-radius:14px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.15)}}
.toggle.on{{background:{POS}}}

/* welcome */
.langchip{{display:inline-flex;align-items:center;gap:6px;border-radius:16px;padding:6px 12px;font-size:13px;font-weight:600;font-family:"Inter",sans-serif}}
.screen[lang=en] .langchip{{font-family:"Tajawal",sans-serif;font-weight:700}}
.art{{position:relative;height:250px;margin-top:6px}}
.art-glow{{position:absolute;left:66px;top:40px;width:260px;height:200px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,80,2,.28),rgba(255,80,2,0))}}
.wtitle{{font-size:32px;font-weight:700;line-height:1.15;letter-spacing:-.8px}}
[lang=ar] .wtitle{{line-height:1.45;font-size:31px}}
.featrow{{padding:7px 0}}
.feat{{font-size:15px;font-weight:600}}
[lang=ar] .feat{{font-weight:700;font-size:16px}}
.wdot{{width:7px;height:7px;border-radius:4px;background:#E3D8CF;display:block}}
.wdot.on{{width:22px;background:{MAIN}}}

/* home */
.hero{{position:absolute;left:0;right:0;top:0;height:400px;padding:62px 20px 0;color:#fff}}
.hero .status{{padding:0 30px}}
.hero-art{{position:absolute;top:118px;filter:drop-shadow(0 12px 18px rgba(120,30,0,.35))}}
.av{{width:44px;height:44px;border-radius:22px;background:#fff;color:{MAIN_TEXT};font-weight:700;display:flex;align-items:center;justify-content:center;font-family:"Inter",sans-serif!important}}
.hb-sm{{font-size:13px;color:rgba(255,255,255,.9)}}
.hb-name{{font-size:17px;font-weight:600}}
[lang=ar] .hb-name{{font-weight:700}}
.hamt{{font-size:42px;font-weight:600;letter-spacing:-1px;margin-top:2px}}
[lang=ar] .hamt{{font-weight:700}}
.hamt .dec{{color:rgba(255,255,255,.6)}}
.hcur{{font-size:20px;font-weight:500;opacity:.9}}
.hb-chip{{display:inline-block;margin-top:6px;padding:5px 11px;border-radius:14px;background:rgba(255,255,255,.18);font-size:12.5px;font-weight:600}}
.ra{{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:12.5px;font-weight:600;width:72px}}
[lang=ar] .ra{{font-size:13.5px;font-weight:700}}
.ra-btn{{width:60px;height:60px;border-radius:30px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.92);box-shadow:0 6px 16px rgba(120,30,0,.25),inset 0 1px 0 #fff}}
.panel{{position:absolute;left:0;right:0;top:380px;bottom:0;background:#F6F4F2;border-radius:28px 28px 0 0;padding:16px 16px 0}}
.gval{{font-size:22px;font-weight:700;letter-spacing:-.3px;margin-top:2px}}
.promo{{background:linear-gradient(135deg,#FFF0E8,#FFF8F4);border-color:#FFE0CF;overflow:visible}}
.promo-art{{position:absolute;top:-8px;filter:drop-shadow(0 8px 12px rgba(200,60,0,.2))}}
.promo-btn{{display:inline-block;background:#fff;border-radius:14px;padding:9px 14px;font-size:14px;font-weight:600;box-shadow:0 1px 3px rgba(70,35,10,.08)}}
[lang=ar] .promo-btn{{font-weight:700}}
.section{{margin:18px 4px 8px}}
.stitle-b{{font-size:17px;font-weight:600}}
[lang=ar] .stitle-b{{font-weight:700;font-size:18px}}

/* tab bar */
.tabbar{{position:absolute;bottom:28px;left:50%;margin-left:-150px;width:300px;height:62px;border-radius:31px;display:flex;align-items:center;padding:0 10px;z-index:10}}
.tb{{display:flex;flex-direction:column;align-items:center;gap:4px;padding-top:6px}}
.tdot{{width:5px;height:5px;border-radius:3px;display:block}}

/* sheets */
.backdrop{{position:absolute;inset:0;filter:blur(6px)}}
.ghost{{position:absolute;left:16px;right:16px;border-radius:22px;background:rgba(255,255,255,.75)}}
.dim{{position:absolute;inset:0;background:rgba(24,18,14,.35)}}
.sheet{{position:absolute;left:8px;right:8px;bottom:8px;border-radius:40px;padding:10px 18px 22px;z-index:5}}
.glass-sheet{{background:#fff;box-shadow:0 -8px 30px rgba(70,35,10,.16)}}
.grabber{{width:38px;height:5px;border-radius:3px;background:rgba(24,18,14,.18);margin:0 auto 10px}}
.stitle{{font-size:22px;font-weight:700}}
[lang=ar] .stitle{{font-size:23px}}
.quote{{background:#F6F4F1;border-radius:18px;padding:12px 16px;font-size:16px;line-height:1.5}}
[lang=ar] .quote{{line-height:1.8}}
.screen[lang=en] .quote{{font-style:italic}}
.seg{{background:#F0EDEA;border-radius:16px;padding:3px}}
.seg>div{{flex:1;text-align:center;padding:9px 0;border-radius:13px;font-size:14px;font-weight:600;color:{INK2}}}
[lang=ar] .seg>div{{font-weight:700}}
.seg .on{{background:#fff;color:{INK};box-shadow:0 1px 4px rgba(70,35,10,.1)}}
.kv{{padding:11px 0;font-size:14.5px}}
.kv .k{{color:{INK2}}}
.kv b{{font-weight:600}}
[lang=ar] .kv b{{font-weight:700}}
.cheque{{position:relative;margin-top:14px;border-radius:18px;padding:14px 16px;background:linear-gradient(135deg,#FFF9F5,#FCEADF);border:1.5px dashed rgba(194,61,0,.35);font-size:12px;color:{INK2};font-family:"Inter",sans-serif!important}}
.cheque *{{font-family:"Inter","Tajawal",sans-serif!important}}
.chq-bank{{font-weight:700;font-size:10.5px;color:{INK}}}
.chq-line{{display:flex;gap:10px;margin-top:9px;border-bottom:1px solid rgba(24,18,14,.15);padding-bottom:4px}}
.chq-line b{{color:{INK};font-weight:500;font-family:"Newsreader",Georgia,serif!important;font-style:italic;font-size:14px}}
.chq-micr,.chq-amt{{font-family:"IBM Plex Mono",monospace!important;color:{INK}}}
.chq-amt{{border:1px solid rgba(24,18,14,.25);padding:3px 8px;border-radius:6px;background:rgba(255,255,255,.6)}}
.scan-ok{{position:absolute;top:-14px;right:-10px}}

/* activity */
.search{{height:46px;border-radius:23px;display:flex;align-items:center;padding:0 16px;font-size:15px;color:{INK3}}}
.search>div{{width:100%}}
.pill{{padding:8px 14px;border-radius:20px;font-size:13.5px;font-weight:500;background:#fff;border:1px solid rgba(24,18,14,.07);white-space:nowrap;color:{INK2}}}
[lang=ar] .pill{{font-weight:700;font-size:14px}}
.pill.on{{background:{INK};color:#fff;border-color:{INK}}}
.summary{{margin-top:12px;border-radius:22px;padding:14px 16px}}
.sumv{{font-size:18px;font-weight:700;margin-top:2px}}
.vdiv{{width:1px;height:36px;background:rgba(24,18,14,.1)}}

/* insights */
.stepper{{font-size:14px;font-weight:600}}
[lang=ar] .stepper{{font-weight:700}}
.donut{{position:relative;width:160px;height:160px}}
.donut-c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.dv{{font-size:19px;font-weight:700}}
.stack-legend{{padding:0 6px}}
.dot{{width:9px;height:9px;border-radius:5px;display:inline-block;flex:none}}
.cats{{padding:4px 16px}}
.catrow{{padding:11px 0}}
.catrow+.catrow{{border-top:1px solid rgba(24,18,14,.07)}}
.lim{{font-size:13.5px}}
.lim b{{font-weight:600}}

/* goals */
.goal{{padding:16px}}

/* family */
.actions3{{background:#FFEFE6;border-radius:22px;padding:14px 8px}}
.a3{{display:flex;flex-direction:column;align-items:center;gap:7px;font-size:13px;font-weight:600}}
[lang=ar] .a3{{font-weight:700;font-size:13.5px}}
.a3 .t3d{{border-radius:28px;box-shadow:0 4px 12px rgba(200,60,0,.12)}}
.rec{{display:flex;flex-direction:column;align-items:center;gap:6px;width:76px}}
.person{{position:relative;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;flex:none}}
.pflag{{position:absolute;bottom:-3px;display:block;line-height:0}}

/* modal */
.modal{{position:absolute;left:28px;right:28px;top:260px;background:#fff;border-radius:30px;padding:24px 22px 22px;z-index:6;box-shadow:0 20px 50px rgba(24,18,14,.25)}}
"""


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
         '&family=IBM+Plex+Sans:wght@400;500;600;700&family=Tajawal:wght@400;500;700;800'
         '&family=IBM+Plex+Sans+Arabic:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500'
         '&family=Newsreader:ital,wght@1,400;1,500&display=swap" rel="stylesheet">')


def render(mode):
    global MODE, LANG
    MODE = mode
    parts = []
    for num, en, ar, fn, bg in SCREENS:
        for lang in ("ar", "en"):
            LANG = lang
            name = f"D{num} {ar} · Arabic" if lang == "ar" else f"D{num} {en} · English"
            d = ' dir="rtl"' if rtl() and mode == "web" else ""
            cls = "screen baked" if baked() else "screen"
            parts.append(f'<section class="{cls}" data-name="{name}" lang="{lang}"{d} style="background:{bg}">{fn()}</section>')
    return (f'<!doctype html><html lang="ar"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Nestly screens, option D</title>{FONTS}<style>{css()}</style></head>'
            f'<body>{"".join(parts)}</body></html>'), len(parts)


def main():
    mode = "figma" if "--figma" in sys.argv else "web"
    html, n = render(mode)
    out = HERE / ("screens-d-figma.html" if mode == "figma" else "screens-d.html")
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.name} ({len(html)//1024} KB, {n} screens, {mode})")


if __name__ == "__main__":
    main()

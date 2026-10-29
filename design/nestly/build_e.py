"""Option E: Arabic-first Nestly screens in a blue fintech style with brand-tinted 3D.

- Colour use follows the reference shot: a vivid blue gradient hero that
  fades into the page, white cards with soft inner panels, list rows on the
  page with pale-blue icon tiles, an active pill in dark navy, and a labelled
  floating tab bar.
- Blue #2563EB is for the main action; dark navy #0B1736 is for secondary
  actions (and text).
- 3D: Fluent 3D emoji (MIT) tinted into one glossy blue family by tint3d.py,
  in the spirit of the Grassfeld and Opay 3D icons.
- RTL: uses build_d's flow()/T() so one source renders as real RTL (web) or
  baked visual order (figma).

    python3 design/nestly/build_e.py            # screens-e.html (web, real RTL)
    python3 design/nestly/build_e.py --figma    # screens-e-figma.html
"""
import base64
import sys
from pathlib import Path

import build as b
import build_d as d
from build import icon
from build_b import flag
from build_d import T, lines, flow, side, chev_fwd, chev_back, amt, toggle, chip, row, status_bar

HERE = Path(__file__).parent
ASSETS = HERE / "assets" / "3d-blue"

BLUE = "#2563EB"        # main action
BLUE_TEXT = "#1D4ED8"   # blue text on white (AA)
NAVY = "#0B1736"        # secondary action + text
INK2 = "#5B6680"
INK3 = "#98A2B8"
TRACK = "#E6ECF5"
POS = "#12A150"
NEG = "#E5484D"
b.ORANGE, b.INK, b.TRACK, b.HATCH_ON = BLUE, NAVY, TRACK, False
d.INK = NAVY

HERO = ("linear-gradient(180deg, #2B63F0 0%, #3A82FF 34%, #7FB0FF 58%, #CFE0FF 76%, #F6F8FC 92%)")
BG = "#F6F8FC"
L = d.L


def rtl():
    return d.rtl()


# ---------------------------------------------------------------- pieces
_img = {}


def img(name, size, style=""):
    if name not in _img:
        _img[name] = base64.b64encode((ASSETS / f"{name}.png").read_bytes()).decode()
    return (f'<img src="data:image/png;base64,{_img[name]}" width="{size}" height="{size}" '
            f'alt="" style="display:block;{style}">')


def t3d(name, box=44, size=30, bg="#EAF1FF", round_=True):
    r = box // 2 if round_ else 14
    return (f'<div class="t3d" style="width:{box}px;height:{box}px;border-radius:{r}px;background:{bg}">'
            f'{img(name, size)}</div>')


def bar(w, frac, color=BLUE, today=None, h=8):
    return b.bar(w, frac, color, today=today, h=h, rtl=rtl())


def btn(text, kind="primary", ic=None, grow=False):
    inner = [T(text)]
    if ic:
        inner.insert(0, icon(ic, 18, "#fff", 2.2))
    return f'<div class="btn {kind}{" grow" if grow else ""}">{flow(*inner, justify="center", gap=8)}</div>'


def arrow_fwd(color=BLUE, size=18):
    # forward arrow: points left in RTL
    path = "M19 12H5M11 6l-6 6 6 6" if rtl() else "M5 12h14M13 6l6 6-6 6"
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="{path}"/></svg>')


def tab_bar(active):
    tabs = [("home", L("الرئيسية", "Home")), ("activity", L("العمليات", "Activity")),
            ("insights", L("التحليلات", "Insights")), ("goals", L("الأهداف", "Goals"))]
    items = [f'<div class="tab{" on" if ic == active else ""}">{icon(ic, 22, BLUE if ic == active else INK2, 1.8)}'
             f'<span>{lab}</span></div>' for ic, lab in tabs]
    return f'<div class="tabbar">{flow(*items, justify="between", style="width:100%")}</div>'


def backdrop():
    return f"""
<div class="backdrop" style="background:{BG}">
  <div style="position:absolute;left:0;right:0;top:0;height:560px;background:{HERO}"></div>
  <div class="ghost" style="top:270px;height:200px"></div>
  <div class="ghost" style="top:540px;height:60px;background:rgba(11,23,54,.06)"></div>
  <div class="ghost" style="top:620px;height:60px;background:rgba(11,23,54,.06)"></div>
</div><div class="dim"></div>"""


def close_btn():
    return f'<div class="closeb">{icon("close", 18, INK2, 1.8)}</div>'


def sheet_head(title, sub=None):
    s = f'<div class="p tx" style="margin-top:6px">{sub}</div>' if sub else ""
    return f'{flow("<span></span>", close_btn(), justify="between")}<div class="stitle h tx">{T(title)}</div>{s}'


def hello_row(dark=True):
    c = "#fff" if dark else NAVY
    who = flow('<div class="av">AJ</div>', f'<span class="hello" style="color:{c}">{L("مرحبًا، أليكس", "Hello, Alex")}</span>', gap=12)
    icons = flow(icon("bell", 24, c, 1.6), icon("settings", 24, c, 1.6), gap=16)
    return flow(who, icons, justify="between", style="margin-top:4px")


b.ICONS["settings"] = ("M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 0 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 0 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 0 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 0 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z")


def bill_row(n, title, sub, amount, tag=None):
    s = flow(f'<span>{T(sub)}</span>', tag, gap=8, justify="start") if tag else T(sub)
    return flow(t3d(n, 48, 32), f'<div class="grow tx"><div class="rtitle">{T(title)}</div><div class="rsub">{s}</div></div>',
                f'<div class="ramt">{amount}</div>', gap=14, cls="brow")


# ======================================================================
# Screens
# ======================================================================
def welcome():
    feats = [("studio_microphone", L("سجّل مصاريفك بصوتك", "Log spending by voice")),
             ("heart_with_ribbon", L("تابع دعم العائلة كل شهر", "Track family support every month")),
             ("shield", L("بدون ربط حسابك البنكي", "No bank login needed"))]
    rows = "".join(flow(t3d(n, 44, 30), f'<div class="feat tx">{T(t)}</div>', gap=12, cls="featrow") for n, t in feats)
    return f"""
<div class="herobg" style="background:{HERO};height:520px"></div>
{status_bar(dark=True)}
<div class="content">
  {flow(f'<div class="langchip">{L("English", "العربية")}</div>', justify="end")}
  <div class="art">
    <div class="art-glow"></div>
    <div style="position:absolute;left:101px;top:26px;filter:drop-shadow(0 18px 24px rgba(10,40,140,.35))">{img('money_bag', 190)}</div>
    <div style="position:absolute;{side('start')}:30px;top:22px;transform:rotate(-14deg)">{img('coin', 74)}</div>
    <div style="position:absolute;{side('end')}:34px;top:132px;transform:rotate(10deg)">{img('shield', 70)}</div>
    <div style="position:absolute;{side('end')}:62px;top:8px">{img('sparkles', 44)}</div>
    <div style="position:absolute;{side('start')}:58px;top:168px;transform:rotate(16deg)">{img('coin', 46)}</div>
  </div>
  <div class="tx" style="margin-top:6px">
    <div class="wtitle h">{L("ميزانيتك تبدأ<br>من يوم الراتب", "Your budget starts<br>on payday")}</div>
    <div class="p" style="margin-top:8px">{L("نستلي يتابع مصاريفك من راتب إلى راتب، ويذكّرك بالفواتير والشيكات قبل موعدها.", "Nestly follows your spending from one payday to the next, and reminds you before bills and cheques are due.")}</div>
  </div>
  <div style="margin-top:12px">{rows}</div>
  <div style="margin-top:12px">{btn(L("ابدأ الآن", "Get started"))}</div>
  <div style="margin-top:10px">{btn(L("لدي حساب بالفعل", "I already have an account"), "secondary")}</div>
</div>"""


def home():
    card = f"""
<div class="card hcard">
  {flow(t3d('heart_with_ribbon', 36, 26, '#EAF1FF', False), f'<span class="ctitle h">{L("دعم العائلة", "Family support")}</span>', gap=10)}
  <div class="inner">
    <div class="p sm tx">{lines(L("تحويل أمي 1,500 د.إ مستحق خلال 3 أيام،", "Mum's AED 1,500 is due in 3 days,"), L("ورصيدك يغطيه.", "and your balance covers it."))}</div>
    <div class="wbtn">{flow(T(L("تحديد كمُرسَل", "Mark as sent")), arrow_fwd(), justify="center", gap=8)}</div>
  </div>
</div>"""
    pills = flow(f'<div class="pill on">{L("كل الفواتير", "All bills")}</div>', f'<div class="pill">{L("تحتاج إجراء", "Needs action")}</div>', gap=8, style="margin:20px 0 6px")
    tag = f'<span class="tag">{icon("clock", 13, "#C2410C", 2)}{T(L("مؤجل", "Post-dated"))}</span>'
    return f"""
<div class="herobg" style="background:{HERO}"></div>
{status_bar(dark=True)}
<div class="content">
  {hello_row()}
  <div class="center" style="margin-top:26px;color:#fff">
    <div class="hlabel">{L("المتبقي لهذه الدورة", "Left this pay cycle")}</div>
    <div class="hamt h">{amt(6660, cur_cls="hcur")}</div>
    <div class="hsub">{flow(icon("calendar", 15, "#fff", 2), T(L("9 أيام حتى الراتب · 740 د.إ يوميًا", "9 days to payday · AED 740 a day")), justify="center", gap=6)}</div>
  </div>
  {card}
  {pills}
  {bill_row('high_voltage', L("ديوا", "DEWA"), L("تستحق 28 أبريل", "Due 28 Apr"), amt(412.30))}
  {bill_row('house', L("شيك الإيجار", "Rent cheque"), L("يُصرف 1 مايو", "Clears 1 May"), amt(6250), tag)}
  <div class="addrow">{flow(icon("plus", 18, INK2, 2), L("إضافة فاتورة", "Add a bill"), justify="center", gap=8)}</div>
</div>
{tab_bar('home')}"""


def connect():
    opts = [("envelope_with_arrow", L("رسائل البنك القصيرة", "Bank SMS alerts")),
            ("mobile_phone", L("إشعارات تطبيق البنك", "Bank app notifications")),
            ("receipt", L("رفع كشف حساب", "Upload a statement")),
            ("studio_microphone", L("سجّل بصوتك أو اكتب", "Speak or type it"))]
    rows = "".join(f'<div class="opt">{flow(t3d(n, 40, 28), f"<span class=rtitle>{t}</span>", f"<div class=chevc>{icon(chev_fwd(), 14, INK3, 2)}</div>", gap=12, cls="optrow")}</div>' for n, t in opts)
    sub = L("نقرأ تنبيهات البنك فقط لتسجيل مصاريفك تلقائيًا. لا نطلب كلمة مرور بنكية أبدًا.",
            "We only read your bank alerts to log spending for you. We never ask for your bank password.")
    return f"""
{status_bar(dark=True)}
{backdrop()}
<div class="sheet float" style="top:318px">
  {sheet_head(L("اربط مصدرًا", "Connect a source"), sub)}
  <div style="margin-top:16px">{rows}</div>
</div>"""


def say_it():
    wave_h = [8, 14, 22, 30, 18, 10, 24, 36, 28, 16, 12, 20, 32, 40, 26, 14, 8, 18, 28, 22, 12, 16, 30, 24, 10, 6, 12, 8, 14, 6, 10, 6]
    n = len(wave_h)
    rects = "".join(f'<rect x="{(n - 1 - i if rtl() else i) * 7}" y="{(40 - h) / 2}" width="3.5" height="{h}" rx="1.75" fill="{BLUE if i < 22 else "#C9D6EA"}"/>' for i, h in enumerate(wave_h))
    return f"""
{status_bar(dark=True)}
{backdrop()}
<div class="sheet float" style="top:150px">
  {sheet_head(L("تحدّث", "Say it"))}
  <div style="display:flex;justify-content:center;margin-top:4px">{img('studio_microphone', 76)}</div>
  <div class="meta center" style="margin-top:6px">{L("قلها بالعربي أو بالإنجليزي، وسنفهمها", "Say it in Arabic or English, we'll understand")}</div>
  <div class="center" style="margin:12px 0"><svg width="{n*7}" height="40" viewBox="0 0 {n*7} 40">{rects}</svg></div>
  <div class="inner tx" style="margin-top:0">{lines(L("«صرفت 45 على البقالة في كارفور،", "“Spent 45 on groceries at Carrefour,"), L("وأرسلت لبريا 1,000»", "then sent Priya 1,000”"))}</div>
  <div class="caps tx" style="margin:14px 2px 2px">{L("فهمنا قيدين", "We understood 2 entries")}</div>
  {bill_row('shopping_cart', L("كارفور", "Carrefour"), L("بقالة · نقدًا", "Groceries · Cash"), amt(45, "−"))}
  {bill_row('heart_with_ribbon', L("بريا", "Priya"), L("دعم العائلة", "Family support"), amt(1000, "−"))}
  {flow(btn(L("أضف القيدين", "Add 2 entries"), "primary", "check", grow=True), btn(L("تعديل", "Edit"), "secondary"), gap=10, style="margin-top:14px")}
</div>"""


def scan():
    seg = flow(*[f'<div class="{c}">{t}</div>' for t, c in [(L("إيصال", "Receipt"), ""), (L("شيك", "Cheque"), "on"), (L("فاتورة", "Bill"), "")]], justify="between", cls="seg")
    kv = lambda k, v: flow(f'<span class="k">{k}</span>', f'<b>{v}</b>', justify="between", cls="kv")
    return f"""
{status_bar(dark=True)}
{backdrop()}
<div class="sheet float" style="top:96px">
  {sheet_head(L("امسح", "Scan"))}
  <div style="margin-top:12px">{seg}</div>
  <div class="cheque" dir="ltr">
    <div class="chq-bank">EMIRATES NBD · بنك الإمارات دبي الوطني</div>
    <div class="chq-line"><span>Pay</span><b>Al Barsha Properties LLC</b></div>
    <div class="chq-line"><span>Dirhams</span><b>Six thousand two hundred fifty only</b></div>
    <div style="display:flex;justify-content:space-between;margin-top:10px"><span class="chq-micr">01 · 05 · 2026</span><span class="chq-amt">AED 6,250.00</span></div>
    <div class="scan-ok">{img('check_mark_button', 38)}</div>
  </div>
  <div class="inner" style="padding:2px 14px">
    {kv(L("المبلغ", "Amount"), amt(6250))}
    {kv(L("المستفيد", "Payee"), T("Al Barsha Properties"))}
    {kv(L("التصنيف", "Category"), L("إيجار", "Rent"))}
    {flow(f'<span class="k">{L("تاريخ الشيك", "Cheque date")}</span>', flow(f'<b>{T(L("1 مايو 2026", "1 May 2026"))}</b>', f'<span class="tag">{T(L("مؤجل", "Post-dated"))}</span>', gap=6), justify="between", cls="kv")}
  </div>
  <div class="inner" style="padding:10px 14px">{flow(t3d('bell', 40, 28, '#fff'), f'<div class="grow tx"><div class="rtitle">{T(L("ذكّرني قبل 3 أيام", "Remind me 3 days early"))}</div><div class="rsub">{L("لتتأكد أن الرصيد يكفي", "So the account can cover it")}</div></div>', toggle(True), gap=12)}</div>
  {flow(btn(L("أضف المصروف", "Add expense"), "primary", "check", grow=True), btn(L("إعادة المسح", "Rescan"), "secondary"), gap=10, style="margin-top:14px")}
</div>"""


def activity():
    pills = flow(*[f'<div class="pill{" on" if i == 0 else ""}">{t}</div>' for i, t in enumerate(
        [L("الكل", "All"), L("الدخل", "Income"), L("المصاريف", "Spending"), L("نقدًا", "Cash"), L("العائلة", "Family")])], gap=8, style="margin-top:12px;overflow:hidden")
    summary = flow(f'<div class="tx grow"><div class="meta">{L("دخل هذه الدورة", "In this cycle")}</div><div class="sumv h" style="color:{POS}">{amt(19500, "+")}</div></div>',
                   '<div class="vdiv"></div>',
                   f'<div class="tx grow"><div class="meta">{L("مصاريف هذه الدورة", "Out this cycle")}</div><div class="sumv h">{amt(11340, "−")}</div></div>', gap=16, cls="card summary")
    return f"""
<div class="herobg soft"></div>
{status_bar()}
<div class="content">
  {flow(f'<div class="title h">{L("العمليات", "Activity")}</div>', f'<div class="iconbtn primary">{icon("plus", 22, "#fff", 2)}</div>', justify="between", cls="hdr")}
  <div class="search">{flow(icon("search", 18, INK3), f'<span>{T(L("ابحث: طلبات، إيجار، أمي…", "Search Talabat, rent, Mum…"))}</span>', gap=10)}</div>
  {pills}
  {summary}
  <div class="caps grp tx">{L("اليوم", "Today")}</div>
  {bill_row('shopping_cart', L("كارفور", "Carrefour"), L("بقالة · نقدًا", "Groceries · Cash"), amt(312.50, "−"))}
  {bill_row('takeout_box', L("طلبات", "Talabat"), L("توصيل طعام · بطاقة المشرق", "Food delivery · Mashreq card"), amt(68, "−"))}
  {bill_row('automobile', L("سالك", "Salik"), L("مواصلات · التقاط تلقائي", "Transport · Auto-captured"), amt(8, "−"))}
  <div class="caps grp tx">{T(L("الإثنين، 13 أبريل", "Mon, 13 Apr"))}</div>
  {bill_row('heart_with_ribbon', L("أمي · الأنصاري", "Mum · Al Ansari"), L("دعم العائلة · ₹ 33,900", "Family support · ₹ 33,900"), amt(1500, "−"))}
</div>
{tab_bar('activity')}"""


def insights():
    cats = [("house", L("الإيجار", "Rent"), 6250, 6250), ("shopping_cart", L("البقالة", "Groceries"), 1240, 980),
            ("heart_with_ribbon", L("العائلة", "Family"), 2300, 2300), ("automobile", L("المواصلات", "Transport"), 620, 710)]
    mx = 6250

    def pair(n, name, now, last):
        up = now > last * 1.05
        delta = (f'<span class="delta {"up" if up else "dn"}">{T(L(("+" if up else "−") + f"{abs(now - last):,} د.إ", ("+" if up else "−") + f"AED {abs(now - last):,}"))}</span>'
                 if now != last else f'<span class="delta same">{L("كما هو", "Same")}</span>')
        return f"""
<div class="cmp">
  {flow(flow(t3d(n, 36, 24), f'<span class="rtitle">{name}</span>', gap=10), delta, justify="between")}
  <div style="margin-top:8px">{bar(305, now / mx, NEG if up else BLUE, h=8)}</div>
  <div style="margin-top:4px">{bar(305, last / mx, "#C9D6EA", h=6)}</div>
</div>"""
    return f"""
<div class="herobg soft"></div>
{status_bar()}
<div class="content">
  {flow(f'<div class="title h">{L("التحليلات", "Insights")}</div>', f'<div class="iconbtn ghostb">{icon("download", 20, NAVY)}</div>', justify="between", cls="hdr")}
  <div class="verdict">
    <div class="vart" style="{side('end')}:6px">{img('light_bulb', 96)}</div>
    <div class="tx" style="max-width:230px">
      <div class="vtag">{L("خلاصة هذه الدورة", "This cycle's verdict")}</div>
      <div class="vtitle h">{L("أنت على المسار، والبقالة فقط أعلى من المعتاد", "On track. Only groceries are running high")}</div>
      <div class="vsub">{lines(L("صرفت 260 د.إ زيادة على البقالة،", "AED 260 more on groceries,"), L("أغلبها في نهاية الأسبوع.", "mostly at weekends."))}</div>
    </div>
  </div>
  {flow(f'<span class="stitle-b h">{L("مقارنة بالدورة الماضية", "Compared with last cycle")}</span>', justify="start", cls="section")}
  {flow(flow('<span class="lg" style="background:#2563EB"></span>', f'<span class="meta">{L("هذه الدورة", "This cycle")}</span>', gap=6), flow('<span class="lg" style="background:#C9D6EA"></span>', f'<span class="meta">{L("الدورة الماضية", "Last cycle")}</span>', gap=6), gap=16, style="margin:0 4px 6px")}
  <div class="card cats">{"".join(pair(*c) for c in cats[:3])}</div>
</div>
{tab_bar('insights')}"""


def goals():
    def goal(n, name, note, saved, target, status, kind):
        return f"""
<div class="card goal">
  {flow(t3d(n, 64, 48, '#EAF1FF', False), f'<div class="grow tx"><div class="rtitle">{name}</div><div class="rsub">{T(note)}</div></div>', chip(status, kind), gap=12)}
  {flow(f'<div class="gval h">{amt(saved)}</div>', f'<div class="meta">{T(L(f"من {target:,}", f"of {target:,}"))}</div>', justify="between", align="flex-end", style="margin-top:12px")}
  <div style="margin-top:8px">{bar(321, saved / target)}</div>
</div>"""
    return f"""
<div class="herobg" style="background:{HERO};height:330px"></div>
{status_bar(dark=True)}
<div class="content">
  {flow(f'<div class="title h" style="color:#fff">{L("الأهداف", "Goals")}</div>', f'<div class="iconbtn onblue">{icon("plus", 22, "#fff", 2)}</div>', justify="between", cls="hdr")}
  <div class="center" style="color:#fff;margin-top:-4px">
    <div class="hlabel">{L("ادّخرت حتى الآن", "Saved so far")}</div>
    <div class="hamt h" style="font-size:38px">{amt(21600, cur_cls="hcur")}</div>
    <div class="hsub">{T(L("+2,350 د.إ هذه الدورة", "+AED 2,350 this cycle"))}</div>
  </div>
  <div style="margin-top:22px">
    {goal('shield', L("صندوق الطوارئ", "Emergency fund"), L("1,200 د.إ كل يوم راتب", "AED 1,200 every payday"), 12400, 30000, L("على المسار", "On track"), "ok")}
    {goal('kaaba', L("عمرة مع العائلة", "Umrah with family"), L("الموعد فبراير 2027", "Target Feb 2027"), 6800, 18000, L("على المسار", "On track"), "ok")}
    {goal('airplane', L("صيف في كيرالا", "Kerala summer"), L("الموعد يوليو 2026", "Target Jul 2026"), 2400, 9000, L("متأخر دورتين", "2 cycles behind"), "warn")}
  </div>
</div>
{tab_bar('goals')}"""


def family():
    people = [("M", "#2563EB", "IN", L("أمي", "Mum"), L("كيرالا", "Kerala")), ("O", "#0EA5E9", "EG", L("عمر", "Omar"), L("القاهرة", "Cairo")),
              ("A", "#6366F1", "PH", L("آنا", "Ana"), L("مانيلا", "Manila")), ("B", "#0B1736", "PK", L("بلال", "Bilal"), L("لاهور", "Lahore"))]
    ini = {"M": L("أ", "M"), "O": L("ع", "O"), "A": L("آ", "A"), "B": L("ب", "B")}

    def person(i, c, f, size=58):
        return (f'<div class="person" style="width:{size}px;height:{size}px;background:{c};font-size:{20 if size > 50 else 15}px">{ini[i]}'
                f'<span class="pflag" style="{side("end")}:-3px">{flag(f, 22 if size > 50 else 16)}</span></div>')

    recents = flow(*[f'<div class="rec">{person(i, c, f)}<div class="rtitle center">{n}</div><div class="rsub center">{s}</div></div>' for i, c, f, n, s in people], justify="between", style="margin-top:10px")
    acts = flow(*[f'<div class="a3">{t3d(n, 58, 40, "#fff")}<span>{t}</span></div>' for n, t in
                  [("envelope_with_arrow", L("سجّل تحويلًا", "Log transfer")), ("chart_increasing", L("أسعار الصرف", "Rates")), ("spiral_calendar", L("جدولة", "Schedule"))]], justify="around", cls="actions3")

    def prow(i, c, f, name, sub, status, kind):
        return flow(person(i, c, f, 44), f'<div class="grow tx"><div class="rtitle">{name}</div><div class="rsub">{T(sub)}</div></div>', chip(status, kind), gap=12, cls="brow")

    return f"""
<div class="herobg soft"></div>
{status_bar()}
<div class="content">
  {flow(f'<div class="title h">{L("إرسال للأهل", "Send home")}</div>', f'<div class="iconbtn primary">{icon("plus", 22, "#fff", 2)}</div>', justify="between", cls="hdr")}
  <div class="meta tx" style="margin:-8px 4px 12px">{T(L("دعم العائلة · 3,300 د.إ شهريًا", "Family support · AED 3,300 a month"))}</div>
  {acts}
  {flow(f'<span class="stitle-b h">{L("الأشخاص", "People")}</span>', f'<span class="link">{L("إدارة", "Manage")}</span>', justify="between", cls="section")}
  {recents}
  <div style="margin-top:12px">
    {prow("M", "#2563EB", "IN", L("أمي", "Mum"), L("1,500 د.إ · البنك الفيدرالي", "AED 1,500 · Federal Bank"), L("بعد 3 أيام", "Due in 3 days"), "warn")}
    {prow("O", "#0EA5E9", "EG", L("عمر", "Omar"), L("800 د.إ · CIB", "AED 800 · CIB"), L("أُرسل 12 أبريل", "Sent 12 Apr"), "ok")}
    {prow("A", "#6366F1", "PH", L("آنا", "Ana"), L("1,000 د.إ · BDO", "AED 1,000 · BDO"), L("أُرسل اليوم", "Sent today"), "ok")}
  </div>
</div>
{tab_bar('home')}"""


def success():
    return f"""
{status_bar(dark=True)}
{backdrop()}
<div class="modal">
  <div style="display:flex;justify-content:center;margin-top:-78px;filter:drop-shadow(0 16px 22px rgba(10,40,140,.35))">{img('check_mark_button', 112)}</div>
  <div class="stitle h center" style="margin-top:12px">{L("تم تسجيل التحويل", "Logged as sent")}</div>
  <div class="p center" style="margin-top:6px">{lines(L("1,500 د.إ لأمي، حوالي ₹ 33,900.", "AED 1,500 to Mum, about ₹ 33,900."), L("اكتمل دعم العائلة لشهر أبريل: 3 من 3.", "Family support is 3 of 3 for April."))}</div>
  <div style="margin-top:18px">{btn(L("العودة للرئيسية", "Back to home"))}</div>
  <div style="margin-top:10px">{btn(L("مشاركة الإيصال", "Share receipt"), "secondary")}</div>
</div>"""


SCREENS = [("01", "Welcome", "الترحيب", welcome, BG), ("02", "Home", "الرئيسية", home, BG),
           ("03", "Connect a source", "اربط مصدرًا", connect, BG), ("04", "Say it", "تحدّث", say_it, BG),
           ("05", "Scan cheque", "مسح شيك", scan, BG), ("06", "Activity", "العمليات", activity, BG),
           ("07", "Insights", "التحليلات", insights, BG), ("08", "Goals", "الأهداف", goals, BG),
           ("09", "Send home", "إرسال للأهل", family, BG), ("10", "Logged as sent", "تم التسجيل", success, BG)]


# ---------------------------------------------------------------- CSS
def css():
    head = '"IBM Plex Sans","Helvetica Neue",Arial,sans-serif'
    ar = '"Tajawal","IBM Plex Sans Arabic",sans-serif'
    return f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#E3E8F0;font-family:"Inter","Helvetica Neue",Arial,sans-serif;color:{NAVY};display:flex;flex-wrap:wrap;gap:48px;padding:48px;-webkit-font-smoothing:antialiased}}
.screen{{width:393px;height:852px;position:relative;overflow:hidden;flex:none;font-size:15px}}
.h{{font-family:{head}}}
.screen[lang=ar],.screen[lang=ar] *{{font-family:{ar};letter-spacing:0!important}}
.tx{{text-align:start}}.tx-end{{text-align:end}}
.baked .tx{{text-align:right}}.baked .tx-end{{text-align:left}}
.baked .tx[style*="max-width"]{{margin-left:auto}}
.center{{text-align:center}}
.vr{{display:inline-flex;align-items:baseline;white-space:nowrap}}
.vr .w{{padding:0 .14em}}
.grow{{flex:1;min-width:0}}
.herobg{{position:absolute;left:0;right:0;top:0;height:560px}}
.herobg.soft{{height:300px;background:linear-gradient(180deg,#DCE8FF 0%,#F6F8FC 100%)}}
.status{{position:absolute;top:0;left:0;right:0;height:54px;display:flex;align-items:center;padding:0 30px;z-index:20}}
.time{{font-family:"Inter",sans-serif!important;font-weight:600;font-size:17px}}
.island{{position:absolute;left:50%;top:11px;width:124px;height:36px;margin-left:-62px;border-radius:20px;background:#000}}
.sys{{display:flex;gap:6px;align-items:center;direction:ltr}}
.content{{position:absolute;inset:0;padding:62px 20px 0}}
.hdr{{margin:4px 0 16px}}
.title{{font-size:30px;font-weight:600;letter-spacing:-.5px}}
[lang=ar] .title{{font-weight:700}}
.meta{{font-size:13px;color:{INK2};line-height:1.5}}
[lang=ar] .meta{{font-size:13.5px;font-weight:500}}
.muted{{color:{INK3}}}
.p{{font-size:15px;line-height:1.55;color:{INK2}}}
[lang=ar] .p{{line-height:1.8;font-size:16px}}
.p.sm{{font-size:14.5px}}
[lang=ar] .p.sm{{font-size:15px}}
.link{{font-size:14px;font-weight:600;color:{BLUE_TEXT}}}
.caps{{font-size:14px;font-weight:600}}
[lang=ar] .caps,[lang=ar] .link{{font-weight:700}}
.grp{{margin:16px 2px 2px}}
.card{{background:#fff;border-radius:24px;padding:16px;box-shadow:0 10px 30px rgba(20,50,120,.07),0 1px 2px rgba(20,50,120,.05);position:relative}}
.card+.card{{margin-top:12px}}
.inner{{background:#F4F6FA;border:1px solid #EEF1F6;border-radius:18px;padding:14px;margin-top:12px}}
.t3d{{display:flex;align-items:center;justify-content:center;flex:none}}
.ctitle{{font-weight:600;font-size:17px}}
[lang=ar] .ctitle{{font-weight:700}}
.rtitle{{font-weight:500;font-size:16px}}
[lang=ar] .rtitle{{font-weight:700;font-size:16px}}
.rsub{{font-size:13px;color:{INK2};margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
[lang=ar] .rsub{{font-weight:500}}
.ramt{{font-weight:600;font-size:16px;white-space:nowrap}}
.amt{{display:inline-flex;gap:4px;align-items:baseline;white-space:nowrap}}
.cur{{font-size:.8em;font-weight:500}}
.dec{{color:{INK3}}}
.num{{white-space:nowrap}}
.brow{{padding:9px 0}}
.chip{{display:inline-block;font-size:12px;font-weight:600;padding:4px 9px;border-radius:9px;white-space:nowrap}}
[lang=ar] .chip{{font-weight:700;font-size:12.5px}}
.chip.ok{{background:rgba(18,161,80,.12);color:#0E7C3E}}
.chip.warn{{background:#FFF1E6;color:#C2410C}}
.tag{{display:inline-flex;align-items:center;gap:4px;font-size:12.5px;font-weight:600;color:#C2410C}}
[lang=ar] .tag{{font-weight:700}}
.btn{{white-space:nowrap;height:54px;border-radius:27px;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:16px;padding:0 22px;color:#fff}}
[lang=ar] .btn{{font-weight:700;font-size:17px;height:56px}}
.btn.primary{{background:{BLUE};box-shadow:0 10px 22px rgba(37,99,235,.32),inset 0 1px 0 rgba(255,255,255,.25)}}
.btn.secondary{{background:{NAVY};box-shadow:0 8px 18px rgba(11,23,54,.18)}}
.btn.grow{{flex:1}}
.iconbtn{{width:44px;height:44px;border-radius:22px;display:flex;align-items:center;justify-content:center;flex:none}}
.iconbtn.primary{{background:{BLUE};box-shadow:0 8px 18px rgba(37,99,235,.32)}}
.iconbtn.onblue{{background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.35)}}
.iconbtn.ghostb{{background:#fff;box-shadow:0 2px 8px rgba(20,50,120,.08)}}
.toggle{{width:51px;height:31px;border-radius:16px;background:#D5DCE8;padding:2px;flex:none}}
.toggle span{{display:block;width:27px;height:27px;border-radius:14px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.15)}}
.toggle.on{{background:{BLUE}}}
.pill{{padding:9px 16px;border-radius:20px;font-size:14px;font-weight:500;background:#fff;border:1px solid #E4E9F1;white-space:nowrap;color:{NAVY}}}
[lang=ar] .pill{{font-weight:700}}
.pill.on{{background:{NAVY};color:#fff;border-color:{NAVY}}}

/* home */
.av{{width:44px;height:44px;border-radius:22px;background:#fff;color:{BLUE_TEXT};font-weight:700;display:flex;align-items:center;justify-content:center;border:2px solid rgba(255,255,255,.7);font-family:"Inter",sans-serif!important}}
.hello{{font-size:18px;font-weight:500}}
[lang=ar] .hello{{font-weight:700}}
.hlabel{{font-size:17px;font-weight:500;opacity:.88}}
.hamt{{font-size:48px;font-weight:600;letter-spacing:-1.5px;margin-top:2px;justify-content:center;display:flex}}
[lang=ar] .hamt{{font-weight:700}}
.hamt .dec{{color:#A9C8FF}}
.hcur{{font-size:22px;font-weight:500;opacity:.9}}
.hsub{{font-size:14px;font-weight:500;margin-top:4px;opacity:.95}}
.hcard{{margin-top:30px}}
.wbtn{{margin-top:12px;background:#fff;border:1px solid #E8ECF3;border-radius:16px;height:50px;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:15.5px;box-shadow:0 2px 6px rgba(20,50,120,.05)}}
[lang=ar] .wbtn{{font-weight:700}}
.addrow{{margin-top:8px;height:52px;border-radius:18px;background:#EEF2F8;display:flex;align-items:center;justify-content:center;color:{INK2};font-weight:500;font-size:15px}}
.addrow>div{{width:100%}}

/* tab bar */
.tabbar{{position:absolute;left:16px;right:16px;bottom:26px;height:66px;border-radius:33px;background:rgba(255,255,255,.94);box-shadow:0 10px 30px rgba(20,50,120,.12);display:flex;align-items:center;padding:0 6px;z-index:10}}
.tab{{flex:1;height:54px;border-radius:27px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:11.5px;font-weight:500;color:{INK2}}}
[lang=ar] .tab{{font-size:12px;font-weight:700}}
.tab.on{{background:#EEF2F8;color:{BLUE}}}

/* welcome */
.langchip{{display:inline-block;border-radius:16px;padding:6px 14px;font-size:13px;font-weight:600;background:rgba(255,255,255,.22);color:#fff;border:1px solid rgba(255,255,255,.4);font-family:"Inter",sans-serif!important}}
.screen[lang=en] .langchip{{font-family:"Tajawal",sans-serif!important;font-weight:700}}
.art{{position:relative;height:232px;margin-top:0}}
.art-glow{{position:absolute;left:56px;top:40px;width:280px;height:200px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.55),rgba(255,255,255,0))}}
.wtitle{{font-size:31px;font-weight:700;line-height:1.15;letter-spacing:-.6px}}
[lang=ar] .wtitle{{line-height:1.45}}
.featrow{{padding:5px 0}}
.feat{{font-size:15px;font-weight:600}}
[lang=ar] .feat{{font-weight:700;font-size:16px}}

/* sheets */
.backdrop{{position:absolute;inset:0;filter:blur(10px)}}
.ghost{{position:absolute;left:20px;right:20px;border-radius:24px;background:rgba(255,255,255,.85)}}
.dim{{position:absolute;inset:0;background:rgba(11,23,54,.18)}}
.sheet{{position:absolute;left:12px;right:12px;bottom:12px;border-radius:36px;padding:16px 20px 22px;z-index:5;background:#fff;box-shadow:0 -10px 40px rgba(11,23,54,.18)}}
.closeb{{width:40px;height:40px;border-radius:20px;background:#F1F4F8;display:flex;align-items:center;justify-content:center}}
.stitle{{font-size:24px;font-weight:600;margin-top:4px}}
[lang=ar] .stitle{{font-weight:700}}
.opt{{border:1px solid #E8ECF3;border-radius:18px;padding:12px 14px;box-shadow:0 2px 6px rgba(20,50,120,.04)}}
.opt+.opt{{margin-top:10px}}
.optrow .rtitle{{flex:1}}
.chevc{{width:28px;height:28px;border-radius:14px;background:#F4F6FA;display:flex;align-items:center;justify-content:center}}
.seg{{background:#F1F4F8;border-radius:16px;padding:3px}}
.seg>div{{flex:1;text-align:center;padding:9px 0;border-radius:13px;font-size:14px;font-weight:600;color:{INK2}}}
[lang=ar] .seg>div{{font-weight:700}}
.seg .on{{background:#fff;color:{NAVY};box-shadow:0 1px 4px rgba(20,50,120,.1)}}
.kv{{padding:11px 0;font-size:14.5px}}
.kv+.kv{{border-top:1px solid #E8ECF3}}
.kv .k{{color:{INK2}}}
.kv b{{font-weight:600}}
[lang=ar] .kv b{{font-weight:700}}
.cheque{{position:relative;margin-top:12px;border-radius:18px;padding:14px 16px;background:linear-gradient(135deg,#F7FAFF,#E8F0FF);border:1.5px dashed rgba(37,99,235,.35);font-size:12px;color:{INK2}}}
.cheque *{{font-family:"Inter","Tajawal",sans-serif!important}}
.chq-bank{{font-weight:700;font-size:10.5px;color:{NAVY}}}
.chq-line{{display:flex;gap:10px;margin-top:9px;border-bottom:1px solid rgba(11,23,54,.15);padding-bottom:4px}}
.chq-line b{{color:{NAVY};font-weight:500;font-family:"Newsreader",Georgia,serif!important;font-style:italic;font-size:14px}}
.chq-micr,.chq-amt{{font-family:"IBM Plex Mono",monospace!important;color:{NAVY}}}
.chq-amt{{border:1px solid rgba(11,23,54,.25);padding:3px 8px;border-radius:6px;background:rgba(255,255,255,.7)}}
.scan-ok{{position:absolute;top:-16px;right:-12px}}

/* activity */
.search{{height:48px;border-radius:24px;display:flex;align-items:center;padding:0 16px;font-size:15px;color:{INK3};background:#fff;box-shadow:0 2px 8px rgba(20,50,120,.06)}}
.search>div{{width:100%}}
.summary{{margin-top:14px;padding:14px 16px}}
.sumv{{font-size:18px;font-weight:700;margin-top:2px}}
.vdiv{{width:1px;height:36px;background:#E8ECF3}}

/* insights */
.verdict{{position:relative;border-radius:26px;padding:18px;background:linear-gradient(150deg,#2B63F0,#4C8DFF 60%,#8DB8FF);color:#fff;box-shadow:0 14px 30px rgba(37,99,235,.3);overflow:visible}}
.vart{{position:absolute;top:-16px;filter:drop-shadow(0 12px 16px rgba(5,25,90,.35))}}
.vtag{{display:inline-block;font-size:12px;font-weight:600;background:rgba(255,255,255,.2);padding:4px 10px;border-radius:10px}}
.vtitle{{font-size:20px;font-weight:600;line-height:1.3;margin-top:10px}}
[lang=ar] .vtitle{{font-weight:700;line-height:1.55}}
.vsub{{font-size:13.5px;opacity:.9;margin-top:8px;line-height:1.5}}
[lang=ar] .vsub{{line-height:1.8;font-size:14px}}
.section{{margin:20px 4px 8px}}
.stitle-b{{font-size:17px;font-weight:600}}
[lang=ar] .stitle-b{{font-weight:700}}
.lg{{width:10px;height:10px;border-radius:3px;display:inline-block}}
.cats{{padding:6px 16px}}
.cmp{{padding:11px 0}}
.cmp+.cmp{{border-top:1px solid #EEF1F6}}
.delta{{font-size:13px;font-weight:600}}
.delta.up{{color:{NEG}}}.delta.dn{{color:{POS}}}.delta.same{{color:{INK2}}}

/* goals */
.goal{{padding:14px 16px}}
.gval{{font-size:22px;font-weight:700}}

/* family */
.actions3{{background:#fff;border-radius:24px;padding:14px 8px;box-shadow:0 10px 30px rgba(20,50,120,.07)}}
.a3{{display:flex;flex-direction:column;align-items:center;gap:7px;font-size:13px;font-weight:600}}
[lang=ar] .a3{{font-weight:700;font-size:13.5px}}
.a3 .t3d{{background:#EAF1FF!important}}
.rec{{display:flex;flex-direction:column;align-items:center;gap:6px;width:76px}}
.person{{position:relative;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;flex:none}}
.pflag{{position:absolute;bottom:-3px;display:block;line-height:0}}

/* modal */
.modal{{position:absolute;left:24px;right:24px;top:240px;background:#fff;border-radius:32px;padding:24px 22px 22px;z-index:6;box-shadow:0 24px 60px rgba(11,23,54,.25)}}
"""


FONTS = d.FONTS


def render(mode):
    d.MODE = mode
    parts = []
    for num, en, ar, fn, bg in SCREENS:
        for lang in ("ar", "en"):
            d.LANG = lang
            name = f"E{num} {ar} · Arabic" if lang == "ar" else f"E{num} {en} · English"
            dr = ' dir="rtl"' if d.rtl() and mode == "web" else ""
            cls = "screen baked" if d.baked() else "screen"
            parts.append(f'<section class="{cls}" data-name="{name}" lang="{lang}"{dr} style="background:{bg}">{fn()}</section>')
    return (f'<!doctype html><html lang="ar"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Nestly screens, option E</title>{FONTS}<style>{css()}</style></head>'
            f'<body>{"".join(parts)}</body></html>'), len(parts)


def main():
    mode = "figma" if "--figma" in sys.argv else "web"
    html, n = render(mode)
    out = HERE / ("screens-e-figma.html" if mode == "figma" else "screens-e.html")
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.name} ({len(html)//1024} KB, {n} screens, {mode})")


if __name__ == "__main__":
    main()

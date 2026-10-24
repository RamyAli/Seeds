"""Option B: builds screens-b.html, the Nestly screens in a blue fintech style
(Revolut-like). Has a royal-blue gradient hero with a large balance, white
cards on a cool pale blue canvas, black primary buttons and an icon-only
floating tab bar.

It reuses the screen content from build.py (option A) and swaps the visual
system, then adds two screens: Family support and a "logged" success modal.

    python3 design/nestly/build_b.py
"""
from pathlib import Path

import build as b
from build import icon, money, tile, row, vis, ar_amt, bar, status_bar, screen

OUT = Path(__file__).with_name("screens-b.html")

# ---------------------------------------------------------------- tokens
BLUE = "#2F5BEA"
BLUE_DEEP = "#1B3FC4"
b.ORANGE = BLUE          # the single accent
b.CLAY = "#1F48D6"       # accent text on light grounds
b.INK = "#0E1424"
b.INK2 = "#5B6478"
b.INK3 = "#9AA2B4"
b.POS = "#12A150"
b.NEG = "#E5484D"
b.DRY = "#F5A524"
b.WET = "#14B8A6"
b.CANOPY = "#7C3AED"
b.SHOOT = "#A78BFA"
b.TRACK = "#E4E9F2"
b.HATCH = "#C9D2E3"
b.HATCH_ON = False
INK, INK2, INK3 = b.INK, b.INK2, b.INK3

# option A colours baked into the shared screen bodies, mapped to option B
RECOLOR = [
    ("rgba(222,101,56,", "rgba(47,91,234,"),
    ("rgba(157,191,106,", "rgba(124,58,237,"),
    ("rgba(79,138,60,", "rgba(18,161,80,"),
    ("rgba(61,122,148,", "rgba(20,184,166,"),
    ("rgba(201,160,74,", "rgba(245,165,36,"),
    ("rgba(184,50,42,", "rgba(229,72,77,"),
    ("rgba(34,32,30,", "rgba(14,20,36,"),
    ("rgba(70,45,20,", "rgba(20,40,90,"),
    ("rgba(40,25,10,", "rgba(20,40,90,"),
    ("rgba(169,68,29,", "rgba(31,72,214,"),
    ("rgba(217,201,168,", "rgba(160,185,245,"),
    ("#8A6A22", "#B7791F"), ("#7E5F1B", "#9A6212"),
    ("#EA8257", "#5B82F7"), ("#C9532A", "#1E43C8"), ("#F6B08E", "#A8BEFF"),
    ("#FAF7F1", "#FFFFFF"), ("#FBF6EC", "#F6F8FE"), ("#F1E6D2", "#E7EDFB"),
    ("#7A5C9E", "#EC4899"),
]

BG = ("radial-gradient(110% 38% at 0% 0%, rgba(47,91,234,.16) 0%, rgba(47,91,234,0) 60%),"
      "radial-gradient(90% 30% at 100% 0%, rgba(160,185,245,.35) 0%, rgba(160,185,245,0) 65%),"
      "linear-gradient(#E8EEFB, #F1F4F9 38%, #F4F6F9)")
HERO = ("radial-gradient(90% 70% at 85% 0%, rgba(120,160,255,.55) 0%, rgba(120,160,255,0) 60%),"
        "radial-gradient(80% 60% at 0% 100%, rgba(20,40,160,.55) 0%, rgba(20,40,160,0) 60%),"
        f"linear-gradient(160deg, #3D6BF5 0%, {BLUE} 45%, {BLUE_DEEP} 100%)")


# ---------------------------------------------------------------- chrome
TAB_ICONS = ["home", "activity", "insights", "goals", "sparkle"]


def tab_bar_b(active, rtl=False):
    icons = list(reversed(TAB_ICONS)) if rtl else TAB_ICONS
    items = "".join(
        f'<div class="tb">{icon(ic, 24, BLUE if ic == active else INK, 1.8)}'
        f'<span class="tdot" style="background:{BLUE if ic == active else "transparent"}"></span></div>'
        for ic in icons
    )
    return f'<div class="tabbar-b glass">{items}</div>'


def sheet_backdrop_b(_bg=None):
    return f"""
<div class="backdrop" style="background:{BG}">
  <div style="position:absolute;left:0;right:0;top:0;height:372px;background:{HERO}"></div>
  <div class="ghost" style="top:392px;height:150px"></div>
  <div class="ghost" style="top:556px;height:110px"></div>
  <div class="ghost" style="top:680px;height:150px"></div>
</div>
<div class="dim"></div>"""


b.tab_bar = tab_bar_b
b.sheet_backdrop = sheet_backdrop_b


def round_action(ic, label):
    return f'<div class="ra"><div class="ra-btn">{icon(ic, 22, "#fff", 1.9)}</div><span>{label}</span></div>'


def hero_amount(v, rtl=False):
    whole, dec = f"{v:,.2f}".split(".")
    if rtl:
        return vis('<span class="hcur">د.إ</span>', f'<span class="hnum">{whole}<span class="hdec">.{dec}</span></span>', align="end")
    return f'<div class="hamt"><span class="hcur">AED</span><span class="hnum">{whole}<span class="hdec">.{dec}</span></span>{icon("eye", 20, "rgba(255,255,255,.7)")}</div>'


b.ICONS["eye"] = "M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12zM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"
b.ICONS["more"] = "M6 12h.01M12 12h.01M18 12h.01"
b.ICONS["send"] = b.ICONS["send"]


# ======================================================================
# 01 Home
# ======================================================================
def home_b():
    return f"""
<div class="hero-b" style="background:{HERO}">
  {status_bar(dark=True)}
  <div class="hb-top">
    <div class="flex"><div class="av-w">AJ</div><div><div class="hb-sm">Good morning</div><div class="hb-name">Alex Johnson</div></div></div>
    <div class="hdr-actions"><div class="iconbtn onblue">{icon('search', 20, '#fff')}</div><div class="iconbtn onblue">{icon('bell', 20, '#fff')}</div></div>
  </div>
  <div class="hb-sm" style="margin-top:22px">Total balance · 4 accounts</div>
  {hero_amount(24892.65)}
  <div class="hb-chip">{icon('out', 14, '#fff', 2)}AED 2,350 saved this cycle</div>
  <div class="ra-row">
    {round_action('mic', 'Say it')}{round_action('scan', 'Scan')}{round_action('heart', 'Family')}{round_action('more', 'More')}
  </div>
</div>

<div class="body-b">
  <div class="card">
    <div class="between"><div class="ctitle">April pay cycle</div><span class="chip blue">9 days left</span></div>
    <div class="between" style="margin-top:12px;align-items:flex-end">
      <div><div class="meta">Left to spend</div><div class="gval" style="margin-top:2px">{money(6660)}</div></div>
      <div class="meta" style="text-align:right">of AED 18,000<br><b>AED 740</b> a day</div>
    </div>
    <div style="margin-top:12px">{bar(321, .63, today=.68, h=8)}</div>
    <div class="between" style="margin-top:6px"><span class="meta">Spent 63%</span><span class="meta">Today</span></div>
  </div>

  <div class="card promo">
    <div class="flex">{tile('heart', '#fff', BLUE, 34, 18)}<span class="ctitle">Family support</span></div>
    <div class="promo-text">Mum's <b>AED 1,500</b> is due in 3 days. Your balance covers it.</div>
    <div class="promo-btn">Mark as sent {icon('chev', 16, INK, 2)}</div>
  </div>

  <div class="section"><span class="stitle-b">Upcoming</span><span class="link">See all</span></div>
  <div class="pills sm"><div class="pill on">All</div><div class="pill">Bills</div><div class="pill">Cheques</div></div>
  <div class="card list" style="margin-top:10px">
    {row('bolt', 'rgba(245,165,36,.16)', '#B7791F', 'DEWA', 'Due 28 Apr · 3 days left', money(412.30))}
    {row('cheque', 'rgba(47,91,234,.12)', BLUE, 'Rent cheque 4 of 4', 'Clears 1 May · post-dated', money(6250))}
    {row('globe', 'rgba(20,184,166,.14)', '#0F8C80', 'e& Home internet', 'Due 2 May · 7 days left', money(389))}
  </div>
</div>
{tab_bar_b('home')}"""


# ======================================================================
# 02 Home, Arabic. Visual (left-to-right) order, single-direction runs.
# ======================================================================
def ar_round(ic, label):
    return round_action(ic, label)


def home_ar_b():
    m = lambda v: ar_amt(v, align="start")
    return f"""
<div class="hero-b" style="background:{HERO}">
  {status_bar(dark=True)}
  <div class="hb-top">
    <div class="hdr-actions"><div class="iconbtn onblue">{icon('bell', 20, '#fff')}</div><div class="iconbtn onblue">{icon('search', 20, '#fff')}</div></div>
    <div class="flex"><div class="ar-text"><div class="hb-sm">صباح الخير</div><div class="hb-name">أليكس جونسون</div></div><div class="av-w">أ</div></div>
  </div>
  <div class="hb-sm ar-text" style="margin-top:22px">{vis('حسابات', '4', '·', 'الرصيد الإجمالي')}</div>
  <div class="hamt" style="justify-content:flex-end">{icon('eye', 20, 'rgba(255,255,255,.7)')}{hero_amount(24892.65, rtl=True)}</div>
  <div style="display:flex;justify-content:flex-end"><div class="hb-chip">{vis('في هذه الدورة', 'د.إ', '2,350', 'وفّرت')}{icon('out', 14, '#fff', 2)}</div></div>
  <div class="ra-row">
    {ar_round('more', 'المزيد')}{ar_round('heart', 'العائلة')}{ar_round('scan', 'امسح')}{ar_round('mic', 'تحدّث')}
  </div>
</div>

<div class="body-b">
  <div class="card">
    <div class="between"><span class="chip blue">{vis('أيام', '9', 'متبقي')}</span><div class="ctitle">دورة أبريل</div></div>
    <div class="between" style="margin-top:12px;align-items:flex-end">
      <div class="meta" style="text-align:left">{vis('18,000', 'من', align='start')}{vis('يوميًا', '<b>740</b>', align='start')}</div>
      <div class="ar-text"><div class="meta">المتبقي للإنفاق</div><div class="gval" style="margin-top:2px">{ar_amt(6660, align="end")}</div></div>
    </div>
    <div style="margin-top:12px">{bar(321, .63, today=.68, h=8, rtl=True)}</div>
    <div class="between" style="margin-top:6px"><span class="meta">اليوم</span><span class="meta">{vis('63%', 'المصروف')}</span></div>
  </div>

  <div class="card promo ar-text">
    <div class="flex" style="justify-content:flex-end"><span class="ctitle">دعم العائلة</span>{tile('heart', '#fff', BLUE, 34, 18)}</div>
    <div class="promo-text">{vis('أيام', '3', 'خلال', 'د.إ', '<b>1,500</b>', 'تحويل أمي مستحق')}{vis('ورصيدك يغطيه')}</div>
    <div style="display:flex;justify-content:flex-end"><div class="promo-btn">{icon('chevl', 16, INK, 2)}تحديد كمُرسَل</div></div>
  </div>

  <div class="section"><span class="link">عرض الكل</span><span class="stitle-b">القادم</span></div>
  <div class="pills sm" style="justify-content:flex-end"><div class="pill">شيكات</div><div class="pill">فواتير</div><div class="pill on">الكل</div></div>
  <div class="card list" style="margin-top:10px">
    {ar_row_b('bolt', 'rgba(245,165,36,.16)', '#B7791F', ['ديوا'], ['متبقية', 'أيام', '3', '·', 'أبريل', '28', 'تستحق'], m(412.30))}
    {ar_row_b('cheque', 'rgba(47,91,234,.12)', BLUE, ['4', 'من', '4', 'شيك الإيجار'], ['مؤجل', '·', 'مايو', '1', 'يُصرف'], m(6250))}
  </div>
</div>
{tab_bar_b('home', rtl=True)}"""


def ar_row_b(ic, bg, fg, title_runs, sub_runs, amount):
    return f"""
<div class="row">
  <div class="ramt" style="text-align:left">{amount}</div>
  <div class="grow ar-text"><div class="rtitle">{vis(*title_runs)}</div><div class="rsub">{vis(*sub_runs)}</div></div>
  {tile(ic, bg, fg)}
</div>"""


# ======================================================================
# 12 Family support
# ======================================================================
def flag(code, size=18):
    r = size / 2
    clip = f'<clipPath id="f{code}{size}"><circle cx="{r}" cy="{r}" r="{r}"/></clipPath>'
    s = size
    body = {
        "IN": f'<rect width="{s}" height="{s/3}" fill="#FF9933"/><rect y="{s/3}" width="{s}" height="{s/3}" fill="#fff"/><rect y="{2*s/3}" width="{s}" height="{s/3}" fill="#138808"/><circle cx="{r}" cy="{r}" r="{s/9}" fill="#000080"/>',
        "EG": f'<rect width="{s}" height="{s/3}" fill="#CE1126"/><rect y="{s/3}" width="{s}" height="{s/3}" fill="#fff"/><rect y="{2*s/3}" width="{s}" height="{s/3}" fill="#000"/><circle cx="{r}" cy="{r}" r="{s/10}" fill="#C09300"/>',
        "PH": f'<rect width="{s}" height="{s/2}" fill="#0038A8"/><rect y="{s/2}" width="{s}" height="{s/2}" fill="#CE1126"/><path d="M0 0L{s*0.55} {r}L0 {s}z" fill="#fff"/><circle cx="{s*0.18}" cy="{r}" r="{s/12}" fill="#FCD116"/>',
        "PK": f'<rect width="{s}" height="{s}" fill="#01411C"/><rect width="{s/4}" height="{s}" fill="#fff"/><circle cx="{s*0.62}" cy="{r}" r="{s/5}" fill="#fff"/><circle cx="{s*0.68}" cy="{s*0.45}" r="{s/5.5}" fill="#01411C"/>',
    }[code]
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" class="flag"><defs>{clip}</defs>'
            f'<g clip-path="url(#f{code}{size})">{body}</g><circle cx="{r}" cy="{r}" r="{r-0.75}" fill="none" stroke="#fff" stroke-width="1.5"/></svg>')


def person(initials, color, code, size=60):
    return (f'<div class="person" style="width:{size}px;height:{size}px;background:{color}">{initials}'
            f'<span class="pflag">{flag(code, 22 if size > 50 else 16)}</span></div>')


def family_b():
    recents = "".join(
        f'<div class="rec">{person(i, c, f)}<div class="rtitle" style="justify-content:center">{n}</div><div class="rsub">{sub}</div></div>'
        for i, c, f, n, sub in [("M", "#F59E0B", "IN", "Mum", "Kerala"), ("O", "#0EA5E9", "EG", "Omar", "Cairo"),
                                ("A", "#EC4899", "PH", "Ana", "Manila"), ("B", "#10B981", "PK", "Bilal", "Lahore")]
    )

    def prow(i, c, f, name, sub, chip, cls):
        return f"""
<div class="row">
  {person(i, c, f, 42)}
  <div class="grow"><div class="rtitle">{name}</div><div class="rsub">{sub}</div></div>
  <span class="chip {cls}">{chip}</span>{icon('chev', 16, INK3)}
</div>"""

    return f"""
{status_bar()}
<div class="content">
  <div class="center-title">Family support</div>
  <div class="hdr" style="margin-top:14px"><div class="title">Send home</div></div>
  <div class="card actions3">
    <div class="a3">{tile('plus', '#fff', INK, 52, 22)}<span>Add person</span></div>
    <div class="a3">{tile('check', '#fff', INK, 52, 22)}<span>Log transfer</span></div>
    <div class="a3">{tile('swap', '#fff', INK, 52, 22)}<span>Rates</span></div>
  </div>

  <div class="section"><span class="stitle-b">People</span><span class="meta">AED 3,300 a month</span></div>
  <div class="recents">{recents}</div>

  <div class="between" style="margin-top:18px">
    <div class="pills sm" style="margin-top:0"><div class="pill on-blue">All</div><div class="pill">Due</div><div class="pill">Sent</div></div>
    <div class="pill">{icon('search', 14, INK2)} Search</div>
  </div>
  <div class="card list" style="margin-top:10px">
    {prow('M', '#F59E0B', 'IN', 'Mum', 'AED 1,500 · Federal Bank', 'Due in 3 days', 'warn')}
    {prow('O', '#0EA5E9', 'EG', 'Omar', 'AED 800 · CIB', 'Sent 12 Apr', 'ok')}
    {prow('A', '#EC4899', 'PH', 'Ana', 'AED 1,000 · BDO', 'Sent today', 'ok')}
  </div>
</div>
{tab_bar_b('home')}"""


# ======================================================================
# 13 Logged as sent (success modal)
# ======================================================================
def success_b():
    return f"""
{status_bar(dark=True)}
{sheet_backdrop_b()}
<div class="modal">
  <div class="okring"><div class="okdot">{icon('check', 26, '#fff', 2.4)}</div></div>
  <div class="stitle" style="text-align:center;margin-top:16px">Logged as sent</div>
  <div class="meta center" style="margin-top:8px;line-height:1.45;font-size:14px">AED 1,500 to Mum, about ₹ 33,900.<br>Family support is 3 of 3 for April.</div>
  <div class="btn primary" style="margin-top:20px">Back to home</div>
  <div class="link center" style="margin-top:14px">Share receipt</div>
</div>"""


# ---------------------------------------------------------------- CSS
def css_b():
    return b.build_css() + f"""
body{{font-family:"Inter","Helvetica Neue",Arial,sans-serif;background:#CBD3E1}}
.time{{font-family:"Inter",sans-serif}}
.title{{font-weight:600;font-size:30px;letter-spacing:-.8px}}
.hello{{font-weight:600}}
.glass{{background:rgba(255,255,255,.80);border:1px solid rgba(255,255,255,.95);
  box-shadow:0 8px 24px rgba(20,40,90,.08),inset 0 1px 0 #fff}}
.glass-inset{{background:#EEF1F6;border-color:transparent}}
.glass-sheet{{background:#fff;border:none;box-shadow:0 -8px 30px rgba(20,40,90,.16)}}
.card{{background:#fff;border:1px solid rgba(14,20,36,.04);border-radius:20px;box-shadow:0 1px 3px rgba(20,40,90,.05)}}
.card.flat{{background:#F5F7FB;border-color:transparent;box-shadow:none}}
.sheet .card.flat{{background:#F5F7FB}}
.caps{{text-transform:none;letter-spacing:0;font-size:13.5px;font-weight:600;color:{INK}}}
.pill{{background:#fff;border:1px solid rgba(14,20,36,.07);padding:8px 14px;font-size:13.5px;font-weight:500;color:{INK2};display:flex;align-items:center;gap:6px}}
.pill.on{{background:{INK};color:#fff;border-color:{INK}}}
.pill.on-blue{{background:#D6E2FF;color:{BLUE};border-color:#D6E2FF}}
.pills.sm{{margin-top:8px}}
.btn.primary{{background:{INK};box-shadow:0 8px 20px rgba(14,20,36,.20)}}
.btn.secondary{{background:#EEF2FE;color:{b.CLAY}}}
.seg .on{{box-shadow:0 1px 4px rgba(20,40,90,.10)}}
.chip.blue{{background:#E6EDFF;color:{BLUE}}}
.iconbtn.onblue{{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.28)}}
.dec{{color:{INK3}}}

/* hero */
.hero-b{{position:absolute;left:0;right:0;top:0;height:392px;padding:62px 20px 0;color:#fff}}
.hb-top{{display:flex;justify-content:space-between;align-items:center;margin-top:4px}}
.av-w{{width:44px;height:44px;border-radius:22px;background:rgba(255,255,255,.95);color:{BLUE};font-weight:700;display:flex;align-items:center;justify-content:center;font-size:15px}}
.hb-sm{{font-size:13px;color:rgba(255,255,255,.75)}}
.hb-name{{font-size:17px;font-weight:600;margin-top:1px}}
.hamt{{display:flex;align-items:center;gap:8px;margin-top:4px}}
.hcur{{font-size:22px;font-weight:500;opacity:.85;margin-right:2px}}
.hnum{{font-size:44px;font-weight:600;letter-spacing:-1.4px}}
.hdec{{opacity:.55}}
.hb-chip{{display:inline-flex;align-items:center;gap:6px;margin-top:8px;padding:5px 10px;border-radius:14px;background:rgba(255,255,255,.16);font-size:12.5px;font-weight:500}}
.ra-row{{display:flex;justify-content:space-between;margin-top:22px;padding:0 6px}}
.ra{{display:flex;flex-direction:column;align-items:center;gap:7px;font-size:12.5px;font-weight:500;width:70px}}
.ra-btn{{width:56px;height:56px;border-radius:28px;display:flex;align-items:center;justify-content:center;
  background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.32);box-shadow:inset 0 1px 0 rgba(255,255,255,.35)}}
.body-b{{position:absolute;left:0;right:0;top:372px;bottom:0;background:#F3F5F9;border-radius:28px 28px 0 0;padding:16px 16px 0}}
.promo{{background:linear-gradient(135deg,#EAF0FF,#F5F8FF);border-color:#DCE5FF}}
.promo-text{{font-size:14px;line-height:1.45;color:{INK2};margin-top:10px}}
.promo-text b{{color:{INK}}}
.promo-btn{{display:inline-flex;align-items:center;gap:4px;margin-top:12px;background:#fff;border-radius:14px;padding:9px 14px;font-size:14px;font-weight:600;box-shadow:0 1px 3px rgba(20,40,90,.08)}}
.stitle-b{{font-size:17px;font-weight:600;letter-spacing:-.2px}}
.section{{margin:18px 4px 4px}}

/* tab bar */
.tabbar-b{{position:absolute;bottom:28px;left:50%;margin-left:-150px;width:300px;height:62px;border-radius:31px;display:flex;align-items:center;justify-content:space-around;padding:0 10px;z-index:10}}
.tb{{display:flex;flex-direction:column;align-items:center;gap:4px;padding-top:6px}}
.tdot{{width:5px;height:5px;border-radius:3px;display:block}}

/* family */
.center-title{{text-align:center;font-size:16px;font-weight:500;color:{INK2};margin-top:6px}}
.actions3{{display:flex;justify-content:space-around;background:#E9EEF9;border:none;box-shadow:none;padding:16px 8px}}
.a3{{display:flex;flex-direction:column;align-items:center;gap:8px;font-size:13px;font-weight:500}}
.a3 .tile{{border-radius:26px;box-shadow:0 2px 8px rgba(20,40,90,.08)}}
.recents{{display:flex;gap:16px;margin-top:10px;padding:0 2px}}
.rec{{display:flex;flex-direction:column;align-items:center;gap:6px;width:72px;text-align:center}}
.rec .rsub{{margin-top:-4px}}
.person{{position:relative;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:20px;flex:none}}
.row .person{{font-size:15px}}
.pflag{{position:absolute;right:-3px;bottom:-3px;display:block;line-height:0}}

/* modal */
.modal{{position:absolute;left:28px;right:28px;top:250px;background:#fff;border-radius:30px;padding:28px 22px 22px;z-index:6;box-shadow:0 20px 50px rgba(14,20,36,.25)}}
.okring{{width:76px;height:76px;border-radius:38px;margin:0 auto;background:#EEF1F6;display:flex;align-items:center;justify-content:center}}
.okdot{{width:54px;height:54px;border-radius:27px;background:{INK};display:flex;align-items:center;justify-content:center}}
"""


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
         '&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500'
         '&family=Newsreader:ital,wght@1,400;1,500&display=swap" rel="stylesheet">')

SCREENS = [
    ("B01 Home", home_b, BG, {}),
    ("B02 Home · Arabic", home_ar_b, BG, {"lang": "ar"}),
    ("B03 Say it (voice)", b.voice_body, "#1B2440", {}),
    ("B04 Scan cheque", b.scan_body, "#1B2440", {}),
    ("B05 Activity", b.activity_body, BG, {}),
    ("B06 New entry", b.new_tx_body, "#1B2440", {}),
    ("B07 Insights", b.insights_body, BG, {}),
    ("B08 Goals", b.goals_body, BG, {}),
    ("B09 New goal", b.new_goal_body, "#1B2440", {}),
    ("B10 Nestly AI", b.ai_body, BG, {}),
    ("B11 Profile", b.profile_body, BG, {}),
    ("B12 Family support", family_b, BG, {}),
    ("B13 Logged as sent", success_b, "#1B2440", {}),
]


def render(title="Nestly screens, option B", fonts=FONTS, extra_css=""):
    parts = [screen(name, fn(), bg, **kw) for name, fn, bg, kw in SCREENS]
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title>{fonts}<style>{css_b()}{extra_css}</style></head>'
            f'<body>{"".join(parts)}</body></html>')
    for a, z in RECOLOR:
        html = html.replace(a, z)
    return html, len(parts)


def main():
    html, n = render()
    parts = range(n)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html)//1024} KB, {len(parts)} screens)")


if __name__ == "__main__":
    main()

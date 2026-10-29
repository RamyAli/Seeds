# Nestly app screens: Grassfeld + Liquid Glass redesign

Redesign of the Nestly screens (Figma `Nestly - Research`, section `App Screens`,
node `182:2873`). Applies the layout from `design-research/grassfeld-ui-study.md`
and the GCC recommendations from `research/gcc-competitor-analysis.md`.

- **Figma:** file `YtHvcrQYdjbx62We35S8ex`, section `Nestly redesign · Grassfeld + Liquid Glass` (node `732:735`), to the right of the original screens.
- **Source:** `build.py` generates `screens.html` (one `.screen` per frame, 393 × 852).

```
python3 design/nestly/build.py   # then open screens.html
```

## Screens

| # | Screen | Replaces |
| --- | --- | --- |
| 01 | Home | Home |
| 02 | Home, Arabic (RTL) | New |
| 03 | Say it (voice) sheet | Voice Entry |
| 04 | Scan cheque sheet | Scan Check |
| 05 | Activity | Transactions |
| 06 | New entry sheet | New Transaction |
| 07 | Insights | Analytics |
| 08 | Goals | Goals |
| 09 | New goal sheet with contribution plan | New Goal |
| 10 | Nestly AI | FinBot |
| 11 | Profile | Profile / More |

## What changed and why

**Style**
- Warm Silt canvas with a section tint washing in from the top: orange for Home,
  teal for Insights, green for Goals.
- iOS 26 Liquid Glass: a floating glass tab bar, round glass icon buttons, glass
  sheets and pills over the tinted background. Content stays on near-white cards
  so it remains readable.
- Grassfeld progress bars: solid spent, **hatched remainder**, and a **Today**
  tick. The legend uses the same swatches.
- Amounts show the decimals in grey (`AED 6,660.00`, with `.00` greyed out).
  Labels are small caps. Dates use arrows: `25 Mar → 24 Apr`.
- Seed palette: Orange is the one accent (spending, progress, AI), Loam is used
  for text and primary buttons, green means money in, red means over a limit.
  The type is Schibsted Grotesk, with IBM Plex Sans Arabic for Arabic.

**Navigation**
- Four tabs (Home, Activity, Insights, Goals) and a separate round **Nestly AI**
  button, following the iOS 26 pattern. Profile opens from the avatar, which
  replaces the "More" tab.

**GCC features**
- **Pay cycle** instead of the calendar month (`25 Mar → 24 Apr`, "for 9 days").
- **AED** everywhere, with other currencies per entry (`≈ USD 85.08`, `₹ 33,900`).
- **Family support** card on Home and a Family category.
- **Rent cheques**: scanning a cheque reads the payee and date, flags
  **post-dated** cheques and offers a reminder before the cheque clears.
- Local merchants (Carrefour, Talabat, Salik, DEWA) and banks (Emirates NBD,
  Mashreq).
- One voice note can log **several entries** in English or Arabic.
- Goals that matter in the region (Umrah, trips home), saved **per payday**.
- A full **Arabic** Home screen to prove the right-to-left layout.

## Converting to Figma

`html_to_figma` ignores `dir="rtl"`, and Figma re-orders text that mixes Arabic
with numbers. So the Arabic screen is written in visual left-to-right order,
and every text run uses a single direction (see `vis()` in `build.py`). Some
gaps between Arabic runs come out tighter in Figma than in the browser.

---

# Option B: blue fintech (Revolut-style)

A second visual direction built from two blue fintech references and the
Revolut app. It uses the same content and GCC features as option A, with a
different visual system.

- **Figma:** section `Nestly option B · Blue fintech (Revolut-style)` (node `748:735`), below option A.
- **Source:** `build_b.py` generates `screens-b.html`. It reuses the screen bodies from `build.py` and swaps the tokens, CSS and chrome.

```
python3 design/nestly/build_b.py
```

| | Option A: Grassfeld + Liquid Glass | Option B: Blue fintech |
| --- | --- | --- |
| Mood | Warm, calm, editorial | Crisp, confident, "bank-grade" |
| Canvas | Warm Silt with section tints | Cool pale blue with white cards |
| Accent | Seed Orange (matches the Nestly logo) | Royal blue `#2F5BEA` |
| Home | Pay-cycle budget card is the hero | Blue hero with **total balance** and 4 round actions; budget card below |
| Progress | Hatched "left" part + Today tick | Solid bar on a light track + Today tick |
| Tab bar | Labelled glass tabs + separate AI button | Icon-only floating bar with an active dot; AI is the 5th icon |
| Type | Schibsted Grotesk | Inter |
| Primary button | Loam (near-black) | Navy-black |

Option B adds two screens:

- **B12 Family support (Send home):** people with country flags (India,
  Egypt, Philippines, Pakistan), the monthly amount and the bank for each,
  and Due / Sent status. Quick actions are Add person, Log transfer and Rates.
- **B13 Logged as sent:** a success modal that confirms the transfer was
  logged, with the amount in the home currency.

Nestly *tracks* money, so "Send home" logs a transfer. It does not move money.

---

# Option C: #FF5002 with IBM Plex Sans, Inter and Tajawal

Option B's layout re-skinned with a new brand colour and new type.

- **Figma:** section `Nestly option C · #FF5002 · IBM Plex Sans / Inter / Tajawal` (node `764:762`), on the Nestly page below option B.
- **Source:** `build_c.py` renders option B through `build_b.render()`, then swaps the colours and adds the type rules. It writes `screens-c.html`.

```
python3 design/nestly/build_c.py
```

| Token | Value | Use |
| --- | --- | --- |
| Main | `#FF5002` | Hero, bars, icons, active tab, accent buttons, fills |
| Main text | `#C23D00` | Orange text at small sizes on white (≈5.3:1, passes WCAG AA; `#FF5002` is ≈3.2:1) |
| Ink | `#18120E` | Text and primary buttons |
| Canvas | `#F6F4F2` with a peach wash `#FDEEE5` | Backgrounds |

| Text | English | Arabic |
| --- | --- | --- |
| Headlines, titles, hero numbers | IBM Plex Sans (500–700) | Tajawal 700 |
| Body, labels, buttons in lists | Inter (400–600) | Tajawal 400–500 |

Tajawal has no 600 weight, so semibold Arabic text uses 700. All 14 font styles
resolved in Figma, with no missing fonts.

---

# Option D: Arabic-first with 3D illustrations

Built with the `arabic-rtl-apps` skill. It uses option B's layout and option
C's brand (#FF5002, IBM Plex Sans + Inter, Tajawal), and adds 3D illustrations
so the app feels friendlier and is quicker to scan.

- **Figma:** section `Nestly option D · Arabic-first + 3D (Fluent 3D emoji)` (node `788:762`), on the Nestly page below option C. The Arabic screens are in the top row, with their English versions below.
- **Source:** `build_d.py`
- **3D art:** Microsoft Fluent 3D emoji, MIT licence (`assets/3d/`, see `LICENSE-fluentui-emoji.txt`), resized to 160 px.

```
python3 design/nestly/build_d.py           # screens-d.html: real RTL (dir="rtl", <bdi>) for code reference
python3 design/nestly/build_d.py --figma   # screens-d-figma.html: baked visual order for html_to_figma
```

There are nine screens, each in Arabic and English: Welcome (new),
Home, Say it, Scan cheque, Activity, Insights, Goals, Send home and Logged as
sent.

**3D illustrations:** the Welcome hero (a money bag, coins and a seedling).
On Home, a money bag in the balance area, 3D quick actions (microphone,
camera, heart, robot) and a heart on the Family support card. 3D tiles on
every bill, transaction, category and goal (a Kaaba for Umrah, a shield for
the emergency fund, a plane for travel). A microphone on the voice sheet, a
light bulb on insights and a party popper on the success modal.

**RTL, following the skill:** each screen is written once, in logical order.

- `flow()` lays out rows and `T()` handles mixed-direction text.
- The **web** build is real RTL, with `dir="rtl"` and `<bdi>` around numbers and Latin names.
- The **figma** build bakes the same screens into visual order, because the converter ignores `dir`.
- A pixel diff of the two builds is identical for English and differs by about 1% for Arabic, which is text-run spacing.

Other skill rules applied:

- Arabic line height 1.7–1.8 for body text.
- No letter spacing on Arabic.
- Tajawal at 500/700 for labels.
- Chevrons and back arrows mirrored, and progress bars and donut charts that fill from the right.
- Toggles mirrored.
- Western digits.
- Close buttons on the left in RTL.

---

# Option E: blue with brand-tinted 3D (Arabic-first)

A new direction after feedback on option D. The colour use follows a blue
bill-tracker reference: a vivid blue gradient hero that fades into the page,
white cards with soft inner panels, list rows on the page, and a labelled
floating tab bar. The 3D follows Grassfeld and Opay: glossy objects tinted in
the brand colour, not multicolour emoji.

- **Figma:** section `Nestly option E · Blue + 3D (Arabic-first)` (node `811:762`), on the Nestly page below option D. Arabic is in the top row and English below.
- **Source:** `build_e.py` (reuses `flow()`/`T()` from `build_d.py`). `tint3d.py` turns the Fluent 3D emoji (MIT) into one glossy blue family in `assets/3d-blue/`.

```
python3 design/nestly/build_e.py           # screens-e.html (real RTL)
python3 design/nestly/build_e.py --figma   # screens-e-figma.html (for html_to_figma)
```

| Token | Value | Use |
| --- | --- | --- |
| Blue | `#2563EB` | **Main actions**: primary buttons, add buttons, active tab, toggles, progress |
| Blue text | `#1D4ED8` | Links and blue text on white |
| Navy | `#0B1736` | **Secondary actions** (secondary buttons, active filter pill) and text |
| Hero | `#2B63F0 → #3A82FF → #7FB0FF → #CFE0FF → #F6F8FC` | Gradient that fades into the page |
| Fonts | IBM Plex Sans (titles), Inter (body), Tajawal (Arabic) | |

There are ten screens, each in Arabic and English:

1. Welcome
2. Home: "left this pay cycle" in the hero, a Family support card, bills with a post-dated tag, and "Add a bill"
3. **Connect a source** (new, based on the reference's "Connect a Provider")
4. Say it
5. Scan cheque
6. Activity
7. Insights: a "verdict first" card with a 3D light bulb, and comparison bars against last cycle instead of a pie chart, as Opay does
8. Goals: a blue hero with the amount saved and large 3D goal icons
9. Send home
10. Logged as sent: a 3D check mark, with a blue primary button and a navy secondary one

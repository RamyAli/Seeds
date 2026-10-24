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

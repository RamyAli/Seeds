# UI study: Grassfeld (reference for the Seeds budgeting app)

Reference material for the personal budgeting app. This records what we like about
Grassfeld's interface so later steps can design and build from it. It is a style
reference, not something to copy: Seeds keeps its own brand (see `tokens/`), and
this file says which patterns to borrow and how they map.

## Sources

| Source | What it gave us |
| --- | --- |
| Figma `Nestly - Research`, file `YtHvcrQYdjbx62We35S8ex`, frame `715:771` | 10 App Store screenshots, nodes `713:737` … `713:767` (listed below) |
| https://www.grassfeld.com/ | Feature set, navigation, marketing tone |
| App Store listing `id1537980377` | Feature list, pricing, user praise and complaints |

Screens in the Figma frame (re-fetch with `get_screenshot` when designing):

| # | Node | Screen |
| --- | --- | --- |
| 1 | `713:737` | Event budget detail: "Hang out with friends", progress bar, to-do list, Categories / Transactions / Accounts tabs, sticky "Add Transaction" |
| 2 | `713:740` | Budgets list: Recurring / Event tabs, budget cards with shared-member avatars |
| 3 | `713:743` | Savings goal contribution plan: monthly amount ⇄ target date, 3/6/12-month presets |
| 4 | `713:746` | Periods report + "Next period prediction" card with suggested budget increase |
| 5 | `713:752` | AI assistant chat with quick-reply chips |
| 6 | `713:755` | AI assistant empty state: greeting + "Common questions" chips |
| 7 | `713:758` | Debts & Loans: "Create a unique loan" hero row + list of loan types |
| 8 | `713:761` | Analytics → Money Flow: diverging income/spend bar chart, yearly totals |
| 9 | `713:764` | Analytics → Income: donut with centred total, Totals / Over time toggle, "You earned € more" insight |
| 10 | `713:767` | Planned payments: grouped by date, Postpone / Paid actions per item |

## The look in one paragraph

Calm, airy, rounded and friendly. Each screen sits on a very pale tinted canvas,
content lives on white cards with large radii and no visible borders or shadows,
and there is exactly one strong colour (a mid royal blue) for progress and
emphasis, with green reserved for money coming in or positive news and red for
overspending. Typography is a single geometric sans with heavy weights for
amounts and headings. Delight comes from glossy 3D emoji-style illustrations
(piggy bank, bomb, house, clipboard) used as icons, never from colour noise.

## Colour

Sampled from the screenshots (approximate, ±3 per channel because of compression).

| Role | Observed | Notes |
| --- | --- | --- |
| Canvas (app background) | `#F1F6F7` | Very pale cool grey; the list area behind cards |
| Header tint, budgets | `#E0F2F2` | Pale mint wash behind the top of a budget screen |
| Header tint, analytics | `#DAEBFC` | Pale blue wash; the header tint changes per section |
| Surface (cards) | `#FFFFFF` | No border, no visible shadow |
| Subtle fill (inputs, inactive pills, secondary buttons) | `#F0F5F6` | Same family as the canvas |
| Ink (text, primary button) | `#1F1F27` | Near-black with a blue cast, not pure black |
| Secondary text | ~`#8A9099` | Dates, captions, "Left", "Today" |
| Accent / progress | `#4468D9` | Spent bars, active tab text, links ("Postpone", "In 2 months") |
| Positive / income | `#13BA4A` | Income bars, "€ 1.400" in copy, PREDICTIONS tag |
| Positive, soft | `#C0E49A` | Donut chart fill |
| Info, soft | `#9BE3EA` | Second donut segment |
| Negative / overspend | ~`#E5484D` | Overspend text and bar, "▲ € 180,00" |
| Negative, soft | ~`#F6CDD3` | Overspend bar fill |

Rules we observed:

- One accent colour per screen. Blue means "your spending"; green means "money in
  or good news"; red appears only on a problem.
- Remaining amount in a progress bar is a light **diagonal hatch**, not a flat
  grey. The legend uses the same three swatches: solid (spent), hatched (left),
  outlined (budget). This is the most distinctive detail in the app.
- Section header tints are pale and tell you where you are (mint for budgets,
  blue for analytics), with white cards sliding over them.

## Typography

- One family for the whole UI: a geometric grotesk, very likely **Manrope**
  (single-storey `g`, round `e`, tight numerals). Marketing headlines use a
  separate heavy condensed grotesk; in-app text never does.
- Scale used on screen (iPhone, pt):
  - Screen title: 22–24, bold ("Budgets", "Analytics", "Planned payments")
  - Hero amount: 20–24, bold, with **decimals de-emphasised** in grey
    ("€ 8.650**,00**", "€ 164,00")
  - Card title: 15–16, semibold
  - Body / row label: 14–15, medium
  - Caption / meta: 12–13, regular, grey ("Sep 29 → Oct 12", "for 9 days")
  - Section label: 12, regular, **ALL CAPS, letter-spaced, grey** ("SPENDINGS",
    "PLAN CONTRIBUTIONS (OPTIONAL)", "COMMON QUESTIONS", "JAN 24")
- Date ranges use an arrow: `Sep 29 → Oct 12`.
- Amounts are right-aligned in a column; secondary amounts stack under the main
  one ("€ 1.058,54 / € 2.000,00").

## Shape, spacing, depth

- Phone canvas padding ~16 pt; cards inset the same; gap between cards 8–12 pt.
- Card radius ~16 pt; buttons and inputs ~12 pt; pills/chips fully rounded.
- Circular icon buttons (~36 pt, white) for back, close, more, help, add.
- No drop shadows on cards. Depth comes from white-on-tint contrast only.
- Rows inside a card are divided by hairlines (~1 px, very light grey) with a
  chevron `›` at the right.

## Components worth borrowing

1. **Budget card** – title, date range, avatars of shared members, "⋮" menu,
   big "€ X Left", progress bar with a "Today" tick marking where you should be,
   "for N days", legend with percentages, right-aligned spent / budget amounts.
   Swipeable with page dots when there are several.
2. **Segmented tabs** – pale fill track, active segment is a white pill
   (Categories / Transactions / Accounts; Recurring 1 / Event 2 with a count).
3. **Horizontal filter pills** – scrolling row of rounded pills; active one is
   white, inactive ones pale ("Spending", "Income", "Money Flow", "Weekly").
4. **Dropdown selects in pairs** – "Money in / out ▾", "Yearly ▾" plus a square
   filter icon button.
5. **Period stepper** – `‹  2023  ›` centred above a chart.
6. **Insight card** – 3D illustration on the left, one bold sentence with the
   key number coloured, a grey supporting line ("You earned € 1.100,00 more /
   18% more than last month").
7. **Prediction card** – green caps tag, title, plain-language explanation, a
   mini breakdown (overspent / suggested increase / new limit) and one full-width
   outlined action ("Increase budget by € 180.00").
8. **List with emoji-tile icons** – 32–36 pt rounded tile with a soft tinted
   background and a 3D emoji (loan types, categories, payments).
9. **Payment item with paired actions** – secondary "Postpone" (pale fill, blue
   text) beside primary "Paid" (ink fill, white text), equal width.
10. **Linked inputs** – two stacked fields joined by a small `=` badge (monthly
    contribution ⇄ target date) with preset chips below (3 / 6 / 12 months).
11. **Sticky primary CTA** – full-width ink button pinned above the home
    indicator ("Add Transaction").
12. **Assistant chat** – soft gradient backdrop, bot avatar bubble, white user
    bubbles, quick-reply chips, input with `+`, mic and send.

## Charts

- **Money flow**: diverging bars per month, income (green) up from a zero line,
  spending (blue) down; dashed horizontal lines for monthly averages with the
  value labelled at the right edge; a thin line connecting net balance; the
  current month drawn hatched as a forecast.
- **Donut**: thick ring, gap between segments, total in the centre with a small
  grey label above ("Earn").
- **Progress bars**: rounded, ~10 pt tall, solid fill + hatched remainder.
- Chart chrome is minimal: single-letter month labels, no gridlines beyond the
  averages.

## Voice and content

- Short, friendly, second person: "We've noticed that you're spending more than
  the budget limit." "only 87% to go".
- Numbers carry the message; copy explains them in one line.
- European number format in the reference (`€ 1.058,54`). Seeds should format by
  the user's locale.

## Features seen (scope inspiration, not a commitment)

Budgets (recurring and one-off events, shared with others), transactions and
categories, bank accounts, savings goals with contribution plans, debts and
loans, planned/recurring payments, analytics (spending, income, money flow,
weekly), period reports and predictions, AI assistant, widgets.

What users praised: ease of use, a clear overview, tags for events like a trip.
What they disliked: no file import early on, rigid budgets that can't shift money
between each other, confusing subscription cancellation. Worth designing for
from the start.

## How this maps to the Seeds brand

The repo already has Seed brand tokens (`tokens/tokens.css`). Grassfeld gives us
the **structure and feel**; Seed gives the **colour and type**. Suggested
mapping, to confirm when we start building:

| Grassfeld role | Seed token |
| --- | --- |
| Canvas `#F1F6F7` | `--seed-silt` `#EFEBE3` (warm instead of cool) |
| Ink / primary button | `--seed-loam` `#22201E` |
| Accent / progress (blue) | `--seed-orange` `#DE6538` on bars; `--seed-clay` `#A9441D` for text and links |
| Positive / income (green) | `--seed-data-optimal` `#5E8F47` / `--seed-shoot` `#9DBF6A` for soft fills |
| Negative / overspend (red) | `--seed-data-alert` `#B8322A` |
| Warning / close to limit | `--seed-data-dry` `#C9A04A` |
| Header tint per section | Light tints of Husk `#D9C9A8` / Shoot / Canopy |
| Manrope UI font | Schibsted Grotesk (UI), IBM Plex Mono (amounts), Newsreader (screen titles, sparingly) |
| 3D emoji icons | Seed's 1.5 px line icons, or a single illustration style we choose later |

Open questions for the next step:

- Keep the hatched "left" pattern? It fits Seed's furrow-line graphic well.
- Seed radius is 6 px; Grassfeld's softness comes from ~16 px cards. Pick one
  for the app.
- Platform: iOS native, cross-platform, or web first.

# Competitor analysis: budgeting apps in the GCC

Research for the Seeds personal budgeting app. Covers the six apps we were asked
to look at, plus one close competitor (Expensly) that kept turning up.
Researched 18 October 2026.

## How much to trust this

- **Websites and store listings** were read directly. Prices, features and
  ratings below come from them.
- **Customer reviews are thin for the GCC apps.** Four of the five local apps
  have almost no public reviews yet (Koma: 50+ downloads; Monee.ae: 8 ratings;
  Hesabi: not enough ratings to show; Meezanya: web only, no store page). Most
  of the "weaknesses" for them are our own reading of the product, not user
  complaints. They are marked as such.
- **Reddit** blocks automated access from this environment (HTTP 403), and web
  searches returned no r/dubai or r/UAE threads. The Reddit sentiment below
  comes second-hand through review sites and is marked. Worth a manual pass
  later: search r/dubai, r/UAE, r/saudiarabia and r/ynab for "budget app".
- Several articles that came up are written by competing apps (Expendr,
  Pocket Clear). They were used for leads only, not as evidence.

## At a glance

| | **Koma** | **Meezanya** | **Monee.ae** | **Hesabi** | **Fast Budget** | **YNAB** |
| --- | --- | --- | --- | --- | --- | --- |
| Origin | UAE | UAE | Dubai | UAE (solo dev) | Italy (AppFer S.R.L.) | USA |
| Region focus | All 6 GCC | UAE | UAE | UAE (+ US/Canada bank link) | Global | US, CA, UK, EU, AU |
| Platforms | Android, web, Telegram (iOS "on its way") | Web app only (PWA) | iPhone only | iPhone / iPad only | Android, iOS, web | iOS, Android, web, Watch |
| Arabic | Full, RTL, dialects | No | No | Not in-app yet (Arabic site locale) | Yes (1 of 24–32 languages) | No |
| How spending gets in | Chat / voice / receipt photo; Android reads bank notifications | Typed one-liners ("coffee 18, fuel 145") | Bank SMS via iOS Shortcut | Reads bank alert **emails** | Manual; bank sync on top tier | Bank sync (not GCC); manual elsewhere |
| Bank login needed | No | No | No | No (email access instead) | Only for bank sync | Yes for sync |
| Free tier | Yes, 10 AI msgs / cycle | Fully free | Yes, manual only | Yes, 3 AI questions / day | Yes, one device | No, 34-day trial |
| Paid price | ~AED 23 / month | — | AED 19.99 / mo, AED 129.99 / yr | AED 49 / mo or 399 / yr (Premium); AED 99 / mo or 799 / yr (Pro) | €19.99 / yr (Premium), €29.99 / yr (Ultra); AED 69.99–104.99 / yr on iOS | $14.99 / mo or $109 / yr (AED 57.99 / 399.99 on iOS) |
| Traction | 50+ installs (Google Play) | Unknown | 4.5★, 8 ratings (UAE App Store) | No ratings yet; v1.0 June 2026 | 4.7★, 131K ratings, 5M+ installs (Play) | 4.1★, 25K ratings, 1M+ installs (Play); 4.5★, 72 ratings (UAE App Store) |

## The apps

### 1. Koma — heykoma.com

**What it is.** An AI chat-first expense tracker built around Gulf salaries.
You log by typing, speaking or photographing a receipt, and Koma files it.

**Features and services**
- Natural-language logging: "Bought headphones for 200, then gave mom 500"
  becomes two entries. Understands English, Gulf, Levantine and Egyptian
  Arabic, Arabizi and code-switching with Hindi, Urdu or Tagalog.
- Voice input and receipt photos read line by line.
- **Pay-cycle budgeting**: the month starts on payday, not the 1st. Back-dated
  entries land in the right cycle.
- **Family Support**: monthly amount set aside per person, marked "sent".
- **Lent out**: who owes you and how much is left.
- Budgets and savings goals per cycle or per month, in any of the six GCC
  currencies.
- "Ask Koma" questions about your own spending.
- **Pay Cycle Wrapped**: shareable summary, with Ramadan and Eid editions.
- Telegram bot for logging without opening the app.
- Android auto-capture (paid): reads payment notifications from bank apps you
  pick. No bank login.
- CSV import; CSV and PDF export. Full Arabic RTL, dark mode.

**Pricing.** Free: unlimited manual logging, all core features, 10 AI messages
per cycle. Koma+ about AED 23 / month for unlimited AI and auto-capture. 7-day
unlimited trial, no card.

**Target audience.** Salaried locals and expats in the Gulf, especially people
sending money to family. Clearly aimed at the mass-market expat worker, not
only professionals (the Hindi / Urdu / Tagalog support says so).

**Segment.** GCC, mass market, AI-first, freemium.

**Strengths**
- The most Gulf-native product in the set: pay cycle, family support,
  remittance-style flows, Ramadan / Eid moments, dialect Arabic.
- Lowest-effort logging of all six: chat, voice and photo.
- Generous free tier; manual logging never paywalled.
- Privacy story is clear: no bank credentials.

**Weaknesses** (our reading; no public reviews yet)
- Very early: 50+ installs on Google Play, no ratings.
- No native iPhone app, in a region where iPhone share is high among
  higher-income users.
- Chat-first can feel slow for people who want to glance at numbers; the
  value depends on AI accuracy, which is unproven at scale.
- Paid tier is mostly "more AI", which is a weak reason to pay.

### 2. Meezanya — meezanya.com

**What it is.** A free web app for UAE residents. Type expenses in plain words
and it picks the amount and category.

**Features**
- Quick-add text ("coffee 18, fuel 145") with categories it learns from your
  corrections.
- Recognises UAE merchants: Talabat, Carrefour, Careem, Salik, Noon, DEWA.
- Monthly category budgets with a bar that turns red when over.
- Monthly and year-on-year reports, category breakdowns, CSV export.
- Recurring bills (rent, subscriptions, instalments) logged monthly and
  flagged for review.
- "Who paid" per expense, so a household can see the split.
- AED by default.

**Pricing.** Free. No paid tier listed.

**Target audience.** UAE residents and expats who budget in dirhams and want
something simple.

**Segment.** UAE, simple tracker, free, web.

**Strengths**
- Zero friction to start: free, no card, no bank, works in a browser.
- UAE merchant knowledge (Salik, DEWA) is a nice local touch.
- Instalments are first-class, which matters in a market with lots of BNPL
  (Tabby, Tamara) and card instalment plans.

**Weaknesses** (our reading; no public reviews)
- No App Store or Play presence, so hard to discover and no push reminders
  the way a native app would have.
- English only.
- No multi-currency per transaction yet (they say so), which hurts expats who
  remit.
- Shared accounts with separate logins not there yet.
- No visible business model, so longevity is a question.

### 3. Monee.ae — monee.ae

**What it is.** An iPhone expense tracker "built in Dubai, for the UAE" that
turns bank SMS alerts into transactions. Live since June 2023; big 2.0
redesign with AI in late summer.

**Features**
- Auto-logging (Pro) from bank purchase SMS via an iOS Shortcut the app
  installs; works with "most banks worldwide" that send an SMS per purchase.
- Manual entry for cash, cheques, transfers, salary; split transactions.
- AI plus crowd-sourced merchant categorisation.
- Category budgets, spending habits, dashboard with month comparisons and top
  merchants. Face ID, export, account deletion. UAE PDPL privacy update.
- Support by email, phone and WhatsApp; the team helps set up the Shortcut.

**Pricing.** Basic free. Pro AED 19.99 / month or AED 129.99 / year.

**Target audience.** iPhone users in the UAE who want automation without
handing over bank details.

**Segment.** UAE, iOS, privacy-first automation, freemium.

**Strengths**
- Solves the region's biggest problem (no open banking for consumer apps) in
  a privacy-friendly way.
- Fair price for what it does; WhatsApp support suits the market.
- Longest track record of the local apps.

**Weaknesses**
- iPhone only, English only.
- 8 ratings in three years: very low traction.
- Shortcut setup is fiddly enough that they offer to help do it, which is a
  sign of onboarding friction.
- Cash, cheques and income still manual. A comparison by a competitor
  (Expendr) lists it as having no automatic capture, which suggests the
  automation is not obvious to newcomers.
- Free tier is thin (budgets are listed as Pro).

### 4. Hesabi — hesabi.ai

**What it is.** A new (v1.0 June 2026) AI personal finance app for the UAE
that reads your **bank alert emails** and builds a categorised picture of
spending across UAE banks. Built by an individual developer.

**Features**
- One total across all accounts, updated from bank notification emails.
- Auto-categorisation; personal and business accounts kept separate.
- Financial health score, **salary-cycle budgeting**, daily spending cap,
  7-day forecast.
- AI questions (3 / day free, 25 Premium, 100 Pro), optional on-device mode.
- Paid: month projection, balance history, trends, budget progress, widgets,
  daily / weekly / monthly AI advice. Pro: multiple accounts per profile,
  custom period reports, CSV export, AI re-categorisation.
- Plaid bank linking for the US and Canada (oddly, not UAE).
- Recent: guided tour, help centre, month plan built from income actually
  received.

**Pricing.** Free tier. Premium AED 49 / month, AED 14.99 / week or AED 399 /
year (7-day trial). Pro AED 99 / month, AED 29.99 / week or AED 799 / year.

**Target audience.** Professionals in the UAE with several bank accounts,
possibly side businesses.

**Segment.** UAE, AI-first, premium-priced.

**Strengths**
- Email alerts are a clever capture method: works on iPhone without
  Shortcuts, catches every bank that emails, and covers more than spending
  (balances, transfers).
- Strong feature list for a v1: health score, forecasts, salary cycle,
  personal vs business.
- On-device AI option is a good privacy answer.

**Weaknesses** (our reading; no reviews yet)
- By far the most expensive: AED 399–799 / year is 3–6× Monee and more than
  YNAB. Weekly billing tends to read as aggressive.
- iPhone only; English only in the app.
- Granting access to your email inbox is a big trust ask, especially from a
  solo developer.
- Not every UAE bank sends emails for every transaction; misses cash.
- Plaid for US / Canada suggests a split focus.

### 5. Fast Budget — fastbudget.app

**What it is.** A mature, global manual budgeting app (since 2015) from an
Italian developer. Very popular on Android.

**Features**
- Dashboard of income, spending and budgets.
- Accounts: cash, bank, prepaid, credit cards with billing cycles.
- Category budgets (weekly, monthly, yearly) with alerts.
- Unlimited categories and subcategories, recurring bills, templates,
  widgets.
- Subscriptions dashboard with renewal reminders.
- Calendar of past and upcoming money.
- Debts and credits (to banks, friends, companies).
- Net worth with forecast.
- Charts, monthly summaries, PDF reports. CSV import (web), CSV / XLS / PDF
  export. Passcode, Dropbox backup, sync across 5 devices.
- Bank sync on the top tier, where the bank is supported (not GCC banks, as
  far as we can tell).
- 24+ languages including Arabic.

**Pricing.** Free (single device, no web, no PDF, no bank sync). Premium
€19.99 / year. Ultra €29.99 / year with bank sync. On the UAE App Store:
AED 69.99 / year (Premium), AED 104.99 / year (Ultra), plus older one-off
"Pro" purchases.

**Target audience.** Anyone who wants a full-featured, cheap manual tracker,
worldwide. Also families and small businesses.

**Segment.** Global, mass market, manual, low-cost.

**Strengths**
- Huge, happy user base: 4.7★ from 131K ratings, 5M+ installs.
- Very cheap; feature-complete (debts, net worth, subscriptions, calendar).
- Reviewers praise fast entry and the reports. "Excellent reports/charts and
  monthly view vs budget."
- Arabic UI exists.

**Weaknesses (from reviews)**
- Everything is manual for GCC users.
- Feature gaps between Android and iOS: "On android you can see month to
  month… bring back option 'Balance'."
- Rough edges with scheduled payments: "an automatic credit card payment
  that was missed… I can't just add in the transaction manually."
- Mandatory subcategories feel tedious (loveMONEY review); debts section
  needs work (UAE App Store review).
- Some users want start-up guidance: "could maybe do with some advice on
  start-up and where to find certain features."
- Many confusing in-app products on iOS (old Pro, Advanced, Premium, Ultra).
- Not Gulf-aware: calendar month, no pay cycle, no remittances.

### 6. YNAB — ynab.com

**What it is.** The best-known "method" budgeting app. Zero-based budgeting:
give every unit of money a job before you spend it.

**Features**
- Zero-based plan, goals, debt payoff tools and loan calculator.
- Real-time sync, share with up to 6 people on one subscription.
- Bank sync for US, Canada, UK, EU banks; file import elsewhere.
- Photos and memos on transactions. Strong education: workshops, guides,
  community.

**Pricing.** $14.99 / month or $109 / year (AED 57.99 / AED 399.99 on the UAE
App Store). 34-day trial; free year for college students.

**Target audience.** Committed budgeters, often couples and families, who
want to change their habits and will put in the effort. Mostly North America
and Europe.

**Segment.** Global, premium, method-led.

**Strengths**
- Life-changing for people who stick with it: "I went from living pay check
  to pay check to now having a 2k buffer."
- Strong brand, community and education.
- Sharing with family is included in one price.

**Weaknesses (from reviews and second-hand Reddit sentiment)**
- **Price and price rises** are the top complaint. UAE App Store: "Price
  changes every 1.5 years!! … 2 PRICE CHANGES IN 3 YEARS!!!" Review sites say
  r/ynab now has regular complaint threads about it.
- **Learning curve**: "if you're a busy mum or you work a lot this app is
  fiddly… I watched videos for help, even joined community groups… found
  myself exhausted."
- **Bank sync** problems and gaps (PayPal, closed credit cards with debt).
- **No GCC bank sync and no Arabic.** A UAE user asks: "Please bring Apple
  Pay + YNAB integration to UAE!"
- One currency per plan, which is awkward for expats.

### Also worth watching: Expensly — expensly.app

Dubai-based, iPhone only, UAE and Saudi. Free tier is generous (manual
tracking, budgets, forecasts, daily spend limit, savings goals, **Zakat
calculator**, paste-from-email import, PDF export). Plus AED 29 / month or
AED 199 / year adds bank SMS auto-logging via Shortcuts. Arabic and English.
Bank sync and UAE credit card bill pay "coming soon".

## Market patterns

**1. No open banking for consumer apps in the GCC (yet).** None of the local
apps link to bank accounts. Each picks a workaround:

| Method | Who | Pros | Cons |
| --- | --- | --- | --- |
| Type / chat / voice | Koma, Meezanya | Works for everyone, cash included | Needs habit |
| Receipt photo | Koma | Good for groceries | Only what you photograph |
| Bank SMS via iOS Shortcut | Monee.ae, Expensly | Automatic, private | Fiddly set-up, iPhone only, misses cash |
| Bank app notifications | Koma (Android) | Automatic, no set-up per bank | Android only |
| Bank alert emails | Hesabi | Automatic on iPhone, covers balances | Inbox access is a big trust ask |
| Bank API sync | YNAB, Fast Budget | Fully automatic | Not available for GCC banks |

When open finance does reach consumer apps in the region, whoever has the
users will win; until then capture method is the main battleground.

**2. "No bank login" is a selling point,** not a limitation. Every GCC app
leads with it.

**3. Gulf-specific money life is underserved by the global apps:**
salary-cycle months, remittances and family support, multiple currencies,
cash, rent paid by cheque, BNPL instalments, Zakat, Ramadan and Eid spending,
Salik / DEWA style bills.

**4. Arabic is rare.** Only Koma and Expensly do it properly; Fast Budget has
a translation. Monee, Meezanya, Hesabi and YNAB are English only.

**5. Platform coverage is patchy.** Every local app is on one platform
(Monee, Hesabi, Expensly: iPhone; Koma: Android + web; Meezanya: web). Nobody
local is on both stores.

**6. Traction is low across the board.** The local apps are all tiny. The
only proven scale is the global manual apps. Gulf News (2024) reports many
UAE residents still prefer spreadsheets because apps don't automate anything
and charge a subscription.

**7. Price bands (per year):** Free (Meezanya) → ~AED 70–130 (Fast Budget,
Monee) → ~AED 200–280 (Expensly, Koma) → ~AED 400 (YNAB, Hesabi Premium) →
AED 800 (Hesabi Pro).

## Where Seeds could win

Based on gaps that show up in more than one competitor:

1. **Gulf-native by default**: pay-cycle months, family support and
   remittances, multi-currency per transaction, cash, cheques, instalments,
   Zakat, Ramadan / Eid views. Koma proves the idea; nobody has it on iPhone.
2. **Arabic and English from day one**, with real RTL design, not a
   translation.
3. **Both iPhone and Android.** No local competitor is.
4. **Fast capture with a choice of method**: quick-add text, receipts, and
   notification / SMS / email capture where available, with manual always free.
5. **Clear, fair pricing.** One paid tier, monthly and yearly, no weekly
   billing, no price shock. YNAB's and Hesabi's pricing is the clearest
   source of complaints and of risk.
6. **Easy start.** Onboarding that sets up budgets from salary and fixed
   bills in a few minutes, answering both YNAB's "learning curve" complaints
   and Fast Budget's "where do I find things".
7. **Calm, readable design** (see `design-research/grassfeld-ui-study.md`):
   none of the local apps has a design that stands out.

Open questions for the next step:

- Who first: expat workers sending money home (Koma's segment) or
  higher-income professionals (Hesabi / YNAB's)? It decides price, language
  set and capture method.
- UAE only at launch, or GCC-wide?
- How much AI? Every new local app leads with it; it is also what they
  charge for.

## Sources

- Koma: https://heykoma.com/ ·
  https://play.google.com/store/apps/details?id=com.heykoma.app
- Meezanya: https://meezanya.com/
- Monee.ae: https://www.monee.ae/ ·
  https://apps.apple.com/ae/app/monee-ae/id6447753044
- Hesabi: https://www.hesabi.ai/ · https://apps.apple.com/ae/app/id6778494075
- Fast Budget: https://fastbudget.app/ ·
  https://play.google.com/store/apps/details?id=com.blodhgard.easybudget ·
  https://apps.apple.com/ae/app/fast-budget-expense-manager/id1178825025 ·
  https://lovemoney.com/news/87540/budgeting-apps-fast-budget-spending-tracking-money-manager
- YNAB: https://www.ynab.com/pricing ·
  https://play.google.com/store/apps/details?id=com.youneedabudget.evergreen.app ·
  https://apps.apple.com/ae/app/ynab/id1010865877 ·
  https://www.fincomparelab.com/reviews/ynab/ (second-hand Reddit sentiment)
- Expensly: https://expensly.app/
- Market: https://gulfnews.com/your-money/budget-living/uae-residents-still-prefer-spreadsheets-over-other-money-management-tools-heres-why-1.1719849430809 ·
  https://expendrapp.com/best-expense-tracker-app-uae.html (written by a competitor)

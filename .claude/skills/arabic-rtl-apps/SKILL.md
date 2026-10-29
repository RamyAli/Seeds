---
name: arabic-rtl-apps
description: Build Arabic-first, RTL-aware web apps, components, and interfaces with proper layout direction, typography, navigation mirroring, and bilingual support. Use this skill whenever the user asks to build an app, page, component, or UI in Arabic, mentions RTL layout, asks for a bilingual (Arabic/English) interface, writes their prompt in Arabic, or references Arab/MENA audiences. Also trigger when the user mentions عربي, واجهة, تطبيق, تصميم, صفحة, or any Arabic UI terminology. Even if the user just casually says "make it Arabic" or "add Arabic support" to an existing project — use this skill. Covers React/JSX artifacts, HTML/CSS/JS, and full codebases (Next.js, etc.).
---

# Arabic RTL Apps

This skill ensures Claude builds Arabic interfaces that feel native — not like an English UI with the direction flipped. Arabic-first means the default mental model is RTL; English/LTR is the adaptation, not the other way around.

## When to activate

Detect from context. If the user writes in Arabic, mentions Arabic-speaking audiences, references Arab or MENA markets, or the task involves Arabic content — default to RTL. You don't need the user to explicitly say "make it RTL."

If the context is ambiguous, build the app RTL-ready from the start (using the patterns below) so flipping direction later is trivial.

## Core principles

### 1. Direction is structural, not decorative

RTL isn't a CSS patch — it's the foundation. Set it at the document root and let everything flow from there:

```html
<html dir="rtl" lang="ar">
```

For React artifacts and components:
```jsx
<div dir="rtl" lang="ar" style={{ fontFamily: "'IBM Plex Sans Arabic', sans-serif" }}>
```

Everything — flexbox order, text alignment, margin/padding, scroll direction — should follow naturally from the root direction. Don't fight the browser's native RTL behavior by adding unnecessary overrides.

### 2. Use `[dir="rtl"]` overrides for directional adjustments

When you need directional CSS that the root `dir` attribute can't handle alone, use attribute selectors:

```css
/* Base styles (direction-neutral) */
.card {
  padding: 1rem;
  border-radius: 8px;
}

/* RTL-specific adjustment */
[dir="rtl"] .card-icon {
  margin-left: 0.75rem;
  margin-right: 0;
}

[dir="ltr"] .card-icon {
  margin-right: 0.75rem;
  margin-left: 0;
}
```

For Tailwind CSS projects, use the `rtl:` and `ltr:` variant classes:
```jsx
<div className="mr-4 rtl:mr-0 rtl:ml-4">
```

This approach is explicit, easy to debug, and gives clear visual separation between base styles and directional adjustments. It also works predictably across all browsers and frameworks.

**Alternative approaches:** CSS logical properties (`margin-inline-start` etc.) are another valid pattern. If the user or project already uses logical properties, follow that convention. But for new projects, `[dir="rtl"]` overrides are the recommended default in this skill because they're more readable when scanning stylesheets.

### 3. Typography

**Recommended Arabic font: IBM Plex Sans Arabic** — it's clean, modern, has excellent weight range (300–700), renders well at all sizes, and is free via Google Fonts:

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

**Other strong alternatives:**
- **Noto Kufi Arabic** — geometric, modern Kufi style. Good for headlines and UI with a more traditional feel.
- **Readex Pro** — designed for digital screens, excellent readability at small sizes. Good for data-heavy interfaces.
- **Tajawal** — clean and neutral, lightweight. Good all-rounder when you want something less opinionated.
- **Cairo** — friendly and rounded. Works well for consumer-facing apps.

```css
:root {
  --font-arabic: 'IBM Plex Sans Arabic', 'Segoe UI', Tahoma, sans-serif;
}

body {
  font-family: var(--font-arabic);
}
```

**Arabic typography needs breathing room.** Arabic script is more vertically complex than Latin — connected letters, diacritics, and ascenders/descenders all need space:

- **Line height**: Use `1.7` to `1.9` for body text (vs the typical `1.5` for Latin). Cramped Arabic text is genuinely harder to read.
- **Font size**: Arabic text often appears visually smaller than Latin at the same `font-size`. Set body text to at least `16px`, and consider `18px` for content-heavy interfaces.
- **Letter spacing**: Never add positive `letter-spacing` to Arabic text. Arabic is a connected script — spacing breaks the ligatures and visual flow of words. Set it to `0` or leave it unset.
- **Font weight**: Arabic at `400` can feel thinner than Latin at `400`. For body text `400` works well with IBM Plex Sans Arabic, but for UI labels and buttons, `500` or `600` often reads better.

For bilingual interfaces, define separate font stacks:
```css
:root {
  --font-arabic: 'IBM Plex Sans Arabic', sans-serif;
  --font-english: 'Inter', 'Helvetica Neue', sans-serif;
}
```

### 4. Navigation & icon mirroring

Directional icons must flip in RTL:
- **Back/forward arrows** (← becomes →)
- **Chevrons** in breadcrumbs, accordions, and lists
- **Progress indicators** (should flow right-to-left)
- **Slide-in panels and drawers** (enter from the right in LTR → enter from the left in RTL)
- **Swipe gestures** (swipe right to go back in LTR → swipe left to go back in RTL)

```css
[dir="rtl"] .icon-back {
  transform: scaleX(-1);
}

[dir="rtl"] .breadcrumb-separator {
  transform: scaleX(-1);
}
```

**Icons that should NOT flip:**
- Checkmarks and X/close buttons
- Media controls (play, pause — these are universal)
- Clocks, phone icons, search icons
- Brand logos
- Icons representing real-world objects (camera, printer)

**Sidebar and navigation placement:**
- Main navigation sidebar goes on the **right** in RTL
- Close/dismiss buttons stay in culturally expected positions (top-left for dismiss in RTL, mirroring the reading end-point)
- Hamburger menu icon stays in its standard position but the drawer opens from the right

### 5. Layout patterns

**Flexbox and Grid automatically reverse in RTL** when you set `dir="rtl"` on the parent. Use this — don't manually reorder items:

```css
/* This automatically reverses in RTL — no override needed */
.nav {
  display: flex;
  gap: 1rem;
}
```

**Common layout gotchas to avoid:**
- Don't use `float: left/right` — it doesn't auto-flip. Use flexbox or grid instead.
- Don't hardcode `text-align: left` — omit it and let `dir` handle it, or use `text-align: start`.
- Don't use `position: absolute; left: 0` for RTL-sensitive positioning — use `[dir="rtl"]` overrides.
- Borders and shadows that imply direction (e.g., a left border accent) should flip:
  ```css
  [dir="rtl"] .accent { border-left: none; border-right: 3px solid var(--accent); }
  ```

**Card layouts in Arabic:**
Arabic users scan right-to-left and top-to-bottom. Place the most important element (image, title, or primary action) on the right side of horizontal cards. Flexbox auto-reverses in RTL, so the first child naturally appears on the right — just keep your HTML source order with the primary element first.

### 6. Forms and inputs

- Text inputs should have `dir="auto"` to handle mixed-direction input (a user might type English words in an Arabic form):
  ```html
  <input type="text" dir="auto" />
  ```
- Labels go **above** inputs (not beside them) for best Arabic readability
- Placeholder text should be right-aligned in RTL
- Validation messages appear on the right side or below the input
- For phone number inputs, the country code stays on the left (it's a number) with `dir="ltr"` on the input itself
- Number inputs: Use Western numerals (0-9) — they're the standard in modern Arabic digital interfaces across most of the Arab world. Arabic-Indic numerals (٠-٩) are rarely used in apps and websites.

### 7. Bilingual support

When building interfaces that support both Arabic and English:

**Language switching pattern:**
```jsx
const [lang, setLang] = useState('ar');
const dir = lang === 'ar' ? 'rtl' : 'ltr';
const fontFamily = lang === 'ar' ? "'IBM Plex Sans Arabic', sans-serif" : "'Inter', sans-serif";

return (
  <div dir={dir} lang={lang} style={{ fontFamily }}>
    {/* App content */}
  </div>
);
```

**Content organization:**
- For small apps and artifacts, keep translations in a simple object:
  ```js
  const t = {
    ar: { title: 'لوحة التحكم', save: 'حفظ', cancel: 'إلغاء' },
    en: { title: 'Dashboard', save: 'Save', cancel: 'Cancel' }
  };
  ```
- For larger apps, use a dedicated i18n library — but the principle stays: Arabic is the primary language, English is the fallback.

**Mixed-direction text:**
When Arabic text contains English words (brand names, technical terms), wrap them in `<bdi>` or `<span dir="ltr">` to prevent BiDi algorithm confusion:
```html
<p>تم إنشاء المشروع باستخدام <bdi>Next.js</bdi> بنجاح</p>
```

### 8. Animations and transitions

- **Slide-in transitions** should respect direction: content slides from the left in RTL (the "forward" direction)
- **Progress bars** fill from right-to-left in RTL
- **Carousel/slider** navigation: next goes left, previous goes right in RTL
- **Page transitions**: new pages enter from the left in RTL

```css
[dir="rtl"] .slide-enter {
  transform: translateX(-100%);
}
[dir="rtl"] .slide-enter-active {
  transform: translateX(0);
}
```

### 9. Spacing and visual rhythm

Arabic interfaces often feel better with slightly more generous spacing than typical Latin layouts:

- **Padding**: Add 10–20% more internal padding in cards, buttons, and containers compared to Latin defaults
- **Section margins**: Be generous — Arabic content sections benefit from clear visual separation
- **Button height**: Minimum `44px` touch target, but Arabic text in buttons often needs `48px` to breathe

### 10. Common mistakes to avoid

These are the things that most commonly go wrong in Arabic UIs — be intentional about catching them:

1. **Forgetting `dir="rtl"`** on the root element — this breaks everything downstream
2. **Hardcoding `text-align: left`** instead of letting direction handle it
3. **Not loading an Arabic font** — system fallbacks render Arabic poorly on most OS/browser combinations
4. **Adding `letter-spacing` to Arabic text** — this breaks connected letterforms and ligatures
5. **Using Latin-optimized line heights** — Arabic needs `1.7`+ for comfortable reading
6. **Not flipping directional icons** — back arrows and chevrons must mirror
7. **Forgetting `dir="auto"` on inputs** — users may type in either language
8. **Positioning with `left/right`** — these don't flip automatically; use `[dir="rtl"]` overrides
9. **Using placeholder Arabic text** — always use real, meaningful Arabic strings like "أدخل اسمك الكامل" instead of generic filler
10. **Ignoring mixed-direction text** — English words inside Arabic sentences need `<bdi>` or `dir="ltr"` wrapping

## Quick reference checklist

Before delivering any Arabic interface, verify:

- [ ] Root element has `dir="rtl"` and `lang="ar"`
- [ ] An Arabic web font is loaded and applied (IBM Plex Sans Arabic recommended)
- [ ] Line height is `1.7` or higher for body text
- [ ] No positive `letter-spacing` on Arabic text
- [ ] Directional icons (arrows, chevrons) are mirrored
- [ ] Navigation/sidebar is on the right side
- [ ] Form inputs have `dir="auto"`
- [ ] No hardcoded `text-align: left` or `float: left/right`
- [ ] Flexbox/grid layouts flow correctly without manual reordering
- [ ] Animations/transitions respect RTL direction
- [ ] Real Arabic text is used throughout (not lorem ipsum)
- [ ] Bilingual font stacks defined if both languages are present
- [ ] Mixed-direction text wrapped in `<bdi>` or `dir="ltr"` spans

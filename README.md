# Seed — Brand Guidelines

Brand identity for **Seed**, a farming company that supplies certified seed (Seed Stock) and soil sensors, field tools and the Seed Field app (Seed Sense).

Open [`brand-guidelines/index.html`](brand-guidelines/index.html) in a browser for the full guideline book.

## Contents

| Chapter | Covers |
| --- | --- |
| 01 Brand | Mission, vision, promise ("From seed to signal"), values, audiences |
| 02 Voice | Tone traits, rewrite examples, vocabulary |
| 03 Logo | Anatomy, clear space, minimum sizes, logo family, colour versions, misuse |
| 04 Colour | Primary, secondary and field-data palettes, proportions, accessible pairings |
| 05 Typography | Newsreader, Schibsted Grotesk, IBM Plex Mono, type scale, rules |
| 06 Graphics & icons | Husk brackets, furrow lines, seed spacing grid, 12 line icons |
| 07 Photography | Art direction, do and don't |
| 08 Applications | Seed packet, Seed Probe sensor, Seed Field app, business cards, buttons |
| 09 Assets | File index |

## Quick reference

| Token | Hex | Use |
| --- | --- | --- |
| Seed Orange | `#DE6538` | Logo on Loam, primary buttons, one highlight per layout |
| Loam | `#22201E` | Text, dark grounds, packaging, devices |
| Silt | `#EFEBE3` | Light backgrounds |
| Clay | `#A9441D` | Orange text and links on light grounds |
| Canopy | `#2E4B33` | Seed Stock packaging, crop content |
| Shoot | `#9DBF6A` | Healthy status, small accents on Loam |
| Husk | `#D9C9A8` | Kraft paper, secondary panels |

- **Logo clear space:** 1x on all sides, where x is the width of one bracket.
- **Minimum size:** full logo 120 px / 30 mm, mark 40 px / 10 mm.
- **Fonts:** Newsreader (display), Schibsted Grotesk (text & UI), IBM Plex Mono (data). All free on Google Fonts. The logo itself is drawn from New York and is supplied as outlines, so never retype it.

## Files

```
assets/logo/
  seed-logo-{orange,loam,silt,white}.svg      primary logo
  seed-mark-{orange,loam,silt,white}.svg      S held in the husk brackets
  seed-wordmark-{orange,loam,silt,white}.svg  wordmark only (legal lines, co-branding)
  seed-app-icon.svg                           Orange on Loam, 512 × 512
  seed-app-icon-orange.svg                    Loam on Orange, 512 × 512
tokens/
  tokens.css                                  CSS custom properties
  tokens.json                                 tokens for design tools and native apps
brand-guidelines/
  index.html                                  the guideline book
```

Logo artwork is exported from the Figma source: `Seed` file, node `111:384` ("logo orange").

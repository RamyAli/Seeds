# Lumo — energy app concept (iOS, 390 × 844)

Lumo is a fictional direct-to-consumer energy company in Dubai, made up for this concept. It isn't a real company.
The live canvas is at https://claude.ai/artifact/XptEcRsuE1hruRTaxtNH1V. Each `.dc.html` file here is one artboard from it.

| # | Artboard | File |
|---|---|---|
| 01 | Home · live energy flow (day, light) | `Main.dc.html` |
| 01b | Home · night, battery discharging (dark) | `HomeNight.dc.html` |
| 02 | Node detail · solar (interactive 24h chart) | `SolarDetail.dc.html` |
| 03 | Grid moment · lock screen push | `LockScreen.dc.html` |
| 04 | Grid moment · detail + accept (device toggles) | `GridMoment.dc.html` |
| 05 | Active event · live countdown (dark) | `ActiveEvent.dc.html` |
| 06 | Event result · rewards earned | `EventResult.dc.html` |
| 07 | Rewards wallet · points, streak, redeem | `Wallet.dc.html` |
| 08 | Edge state · cloudy day + battery offline | `CloudyDay.dc.html` |
| AR | Home + Grid moment in Arabic (RTL) | `HomeArabic.dc.html`, `GridMomentArabic.dc.html` |
| — | User flow: notification → accept → active → reward | `UserFlow.dc.html` |
| — | Mini design system: colour, type, components, motion, a11y, voice | `DesignSystem.dc.html` |

Visual language (v0.3): clean, modern UI with white cards on soft grey (#F2F3F5), a lime accent (#A6F23C), hatched bar charts, and a floating pill tab bar. Manrope is used for Latin and Readex Pro for Arabic.

3D: live Three.js (r149) scenes from `3d/lumo3d.js`:
- `home`: an isometric villa with rooftop solar, a wall battery, an EV and charger, a grid pylon, a pool and palms, plus energy particles flowing along arcs. It has day, night and cloudy themes, and a mirrored version for RTL.
- `panel`: a solar array with a moving sun.
- `coin`: the rewards coin.

On the canvas, `three.min.js` and `lumo3d.js` are loaded as uploaded assets.

`canvas.json` holds the artboard layout. The files use the Design canvas format: inline styles, plus a small `DCLogic` class for state such as the toggles, the countdown and the points counter.

## v4 · Warm minimal (canvas page "v4")

This version takes its style from architectural smart-home UIs. Every v4 artboard file starts with `W4`. It has:
- warm greige and concrete tones (#E7E4DF ground, #F6F4F1 paper cards, frosted cards over the 3D view)
- big numerals in Hanken Grotesk Light, with IBM Plex Sans Arabic for Arabic
- one pale-lime hero tile per screen (#DDF57A), orange tick-mark dials (#EE7A3B), black-knob pill toggles, round nav buttons and black primary buttons

`3d/lumo3d-v4.js` adds:
- warm, warmNight and warmCloudy themes for a cantilevered concrete villa with glowing windows
- a `devices` scene showing an AC unit, a home battery and an EV wallbox

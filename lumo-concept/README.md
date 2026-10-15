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

`canvas.json` holds the artboard layout. The files use the Design canvas format: inline styles, plus a small `DCLogic` class for state such as the toggles, the countdown and the points counter.

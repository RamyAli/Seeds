# Glass icons for Framer

Two code components:

- `GlassIcon.tsx`: one animated glass icon. In the right-hand panel you pick the icon, base color, animation (loop, on hover, paused), speed, and glass style for light or dark backgrounds.
- `GlassColorSlider.tsx`: an optional slider visitors can drag on the live site. Every Glass Icon with **Follow slider** on changes color with it.

## Add them to your project

1. In Framer, open **Assets** (left panel) → **Code** → **+** → **New code file**. Name it `GlassIcon`.
2. Delete the starter code, paste in the full contents of `GlassIcon.tsx`, and save (Cmd/Ctrl + S).
3. Optional: repeat for `GlassColorSlider.tsx` if you want the live slider.
4. Drag **GlassIcon** from Assets → Code onto the canvas. Resize it like any frame; the drawing scales to fit (designed at 160 × 140).
5. Select it and set **Icon**, **Base color**, **Animation** and **Speed** in the right-hand panel.

Tips

- Place icons on a solid or gradient background; the frosted effect needs something behind the glass.
- Choose **Glass: Dark bg** when the section behind the icon is dark.
- **On hover** plays the animation only while the pointer is over the icon, which suits nav items and cards.
- Turn **Follow slider** off on an icon to keep its own color even when a slider is on the page.

## Lottie alternative

Framer can also play Lottie files natively: Insert → Media → Lottie, then upload a file from `lottie/json/` (or a .lottie from `lottie/dotlottie/`). That route has no live color control; pick the color before exporting on the Glass Icon Lottie page.

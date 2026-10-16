# Glass icons as Lottie

- `json/`: one Lottie (Bodymovin) JSON per icon, 160 × 140, 60 fps, looping.
- `dotlottie/`: the same animations as .lottie files, plus `glass-icons-all.lottie` with all ten.

These are built at the default blue (hue 227) with light glass. For another color, use the Glass Icon Lottie page (`motion/glass-icons-lottie.html`) or rebuild here:

```
node lottie/build.js 20          # orange
node lottie/build.js 150 dark    # green, glass for dark backgrounds
```

The generator is `motion/glass-lottie.js`. Frosted glass uses a Gaussian Blur effect on a matted copy of the gradient; lottie-web renders it, while players without blur support show the colors sharp through the glass.

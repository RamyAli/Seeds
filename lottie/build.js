// Builds the glass icons as Lottie JSON and dotLottie files at the default blue (hue 227).
// Usage: node lottie/build.js [hue] [light|dark]
const fs = require("fs");
const path = require("path");
const GL = require("../motion/glass-lottie.js");

const hue = Number(process.argv[2] ?? 227);
const glass = process.argv[3] ?? "light";
const out = path.join(__dirname);
fs.mkdirSync(path.join(out, "json"), { recursive: true });
fs.mkdirSync(path.join(out, "dotlottie"), { recursive: true });

const all = [];
for (const icon of GL.ICONS) {
  const json = GL.build(icon, { hue, glass });
  const id = "glass-" + icon;
  fs.writeFileSync(path.join(out, "json", id + ".json"), JSON.stringify(json));
  fs.writeFileSync(path.join(out, "dotlottie", id + ".lottie"), GL.dotLottie([{ id, json }]));
  all.push({ id, json });
}
fs.writeFileSync(path.join(out, "dotlottie", "glass-icons-all.lottie"), GL.dotLottie(all));
console.log(`Built ${all.length} icons at hue ${hue}, ${glass} glass`);

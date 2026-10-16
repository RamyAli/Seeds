/*
 * Glass Lottie — builds the ten glass icons as Lottie (Bodymovin) JSON in any base hue,
 * and packs them as dotLottie (.lottie) files. Works in the browser (window.GlassLottie)
 * and in Node (module.exports).
 *
 * Frosted glass in Lottie: each glass shape is drawn as
 *   tint layer (translucent fill + white edge)
 *   matte layer (the same shape, used as an alpha track matte)
 *   blurred copy of the gradient layer behind it (Gaussian Blur effect), shown through the matte
 * Players without blur support show the copy sharp through the tint instead.
 */
(function (root) {
  "use strict";

  var W = 160, H = 140, FPS = 60;
  var ICONS = ["folder", "toggle", "play", "location", "search", "chat", "download", "windows", "lock", "people"];
  var TITLES = { folder: "Folder", toggle: "Toggle", play: "Play", location: "Location", search: "Search", chat: "Chat", download: "Download", windows: "Windows", lock: "Lock", people: "People" };

  var SPRING = [0.34, 1.56, 0.64, 1];
  var SMOOTH = [0.65, 0, 0.35, 1];
  var EASE_IO = [0.42, 0, 0.58, 1];
  var EASE_OUT = [0, 0, 0.58, 1];
  var EASE_IN = [0.42, 0, 1, 1];

  // ---------- colour ----------
  function hsl(h, s, l) {
    h = ((h % 360) + 360) % 360; s /= 100; l /= 100;
    var k = function (n) { return (n + h / 30) % 12; };
    var a = s * Math.min(l, 1 - l);
    var f = function (n) { return l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1))); };
    return [r3(f(0)), r3(f(8)), r3(f(4))];
  }
  function r3(x) { return Math.round(x * 1000) / 1000; }
  function palette(hue, glass) {
    var dark = glass === "dark";
    return {
      ga: hsl(hue, 100, 59), gb: hsl(hue, 100, 72), gc: hsl(hue + 44, 76, 53),
      glass: dark ? hsl(hue, 100, 80) : hsl(hue, 75, 87), glassOp: dark ? 17 : 58,
      edgeOp: dark ? 16 : 55,
      knob: dark ? hsl(hue, 100, 97) : [1, 1, 1],
      white: [1, 1, 1]
    };
  }

  // ---------- SVG path -> Lottie bezier ----------
  function arcToCubics(x1, y1, rx, ry, phi, fa, fs, x2, y2) {
    var rad = phi * Math.PI / 180, cos = Math.cos(rad), sin = Math.sin(rad);
    var dx = (x1 - x2) / 2, dy = (y1 - y2) / 2;
    var x1p = cos * dx + sin * dy, y1p = -sin * dx + cos * dy;
    var lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry);
    if (lam > 1) { rx *= Math.sqrt(lam); ry *= Math.sqrt(lam); }
    var num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p;
    var den = rx * rx * y1p * y1p + ry * ry * x1p * x1p;
    var co = Math.sqrt(Math.max(0, num / den)) * (fa === fs ? -1 : 1);
    var cxp = co * rx * y1p / ry, cyp = -co * ry * x1p / rx;
    var cx = cos * cxp - sin * cyp + (x1 + x2) / 2, cy = sin * cxp + cos * cyp + (y1 + y2) / 2;
    var ang = function (ux, uy, vx, vy) {
      var a = Math.atan2(ux * vy - uy * vx, ux * vx + uy * vy);
      return a;
    };
    var t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry);
    var dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry);
    if (!fs && dt > 0) dt -= 2 * Math.PI;
    if (fs && dt < 0) dt += 2 * Math.PI;
    var n = Math.ceil(Math.abs(dt) / (Math.PI / 2) - 1e-9), out = [];
    var step = dt / n, kk = 4 / 3 * Math.tan(step / 4);
    var pt = function (t) { return [cx + rx * Math.cos(t) * cos - ry * Math.sin(t) * sin, cy + rx * Math.cos(t) * sin + ry * Math.sin(t) * cos]; };
    var dv = function (t) { return [-rx * Math.sin(t) * cos - ry * Math.cos(t) * sin, -rx * Math.sin(t) * sin + ry * Math.cos(t) * cos]; };
    for (var i = 0; i < n; i++) {
      var a = t1 + i * step, b = a + step, p0 = pt(a), p3 = pt(b), d0 = dv(a), d3 = dv(b);
      out.push([[p0[0] + kk * d0[0], p0[1] + kk * d0[1]], [p3[0] - kk * d3[0], p3[1] - kk * d3[1]], p3]);
    }
    return out;
  }

  // Returns a list of Lottie path values {i,o,v,c}
  function parsePath(d, ox, oy) {
    ox = ox || 0; oy = oy || 0;
    var toks = d.match(/[MLHVQCAZ]|-?\d*\.?\d+(?:e-?\d+)?/gi), p = 0;
    var num = function () { return parseFloat(toks[p++]); };
    var contours = [], cur = null, x = 0, y = 0, cmd = null;
    function start(px, py) { cur = { v: [[px, py]], i: [[0, 0]], o: [[0, 0]], c: false }; contours.push(cur); x = px; y = py; }
    function seg(c1, c2, e) {
      var n = cur.v.length - 1;
      cur.o[n] = [c1[0] - cur.v[n][0], c1[1] - cur.v[n][1]];
      cur.v.push([e[0], e[1]]); cur.i.push([c2[0] - e[0], c2[1] - e[1]]); cur.o.push([0, 0]);
      x = e[0]; y = e[1];
    }
    function line(ex, ey) { seg([x, y], [ex, ey], [ex, ey]); }
    while (p < toks.length) {
      if (/[A-Za-z]/.test(toks[p])) cmd = toks[p++].toUpperCase();
      switch (cmd) {
        case "M": start(num(), num()); cmd = "L"; break;
        case "L": line(num(), num()); break;
        case "H": line(num(), y); break;
        case "V": line(x, num()); break;
        case "Q": {
          var qx = num(), qy = num(), ex = num(), ey = num();
          seg([x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y)], [ex + 2 / 3 * (qx - ex), ey + 2 / 3 * (qy - ey)], [ex, ey]);
          break;
        }
        case "C": seg([num(), num()], [num(), num()], [num(), num()]); break;
        case "A": {
          var rx = num(), ry = num(), rot = num(), fa = num(), fs = num(), ax = num(), ay = num();
          arcToCubics(x, y, rx, ry, rot, fa, fs, ax, ay).forEach(function (s) { seg(s[0], s[1], s[2]); });
          break;
        }
        case "Z": {
          var last = cur.v.length - 1, f = cur.v[0], l = cur.v[last];
          if (last > 0 && Math.abs(f[0] - l[0]) < 1e-6 && Math.abs(f[1] - l[1]) < 1e-6) {
            cur.i[0] = cur.i[last]; cur.v.pop(); cur.i.pop(); cur.o.pop();
          }
          cur.c = true; x = f[0]; y = f[1]; cmd = null;
          break;
        }
        default: p++;
      }
    }
    return contours.map(function (c) {
      return {
        i: c.i.map(rnd), o: c.o.map(rnd), c: c.c,
        v: c.v.map(function (v) { return [r2(v[0] + ox), r2(v[1] + oy)]; })
      };
    });
  }
  function r2(x) { return Math.round(x * 100) / 100; }
  function rnd(p) { return [r2(p[0]), r2(p[1])]; }

  function rrect(x, y, w, h, r) {
    var t = typeof r === "number" ? [r, r, r, r] : r; // tl tr br bl
    return "M" + (x + t[0]) + " " + y + " H" + (x + w - t[1]) + " A" + t[1] + " " + t[1] + " 0 0 1 " + (x + w) + " " + (y + t[1]) +
      " V" + (y + h - t[2]) + " A" + t[2] + " " + t[2] + " 0 0 1 " + (x + w - t[2]) + " " + (y + h) +
      " H" + (x + t[3]) + " A" + t[3] + " " + t[3] + " 0 0 1 " + x + " " + (y + h - t[3]) +
      " V" + (y + t[0]) + " A" + t[0] + " " + t[0] + " 0 0 1 " + (x + t[0]) + " " + y + " Z";
  }
  function circle(cx, cy, r) {
    return "M" + (cx - r) + " " + cy + " A" + r + " " + r + " 0 1 1 " + (cx + r) + " " + cy + " A" + r + " " + r + " 0 1 1 " + (cx - r) + " " + cy + " Z";
  }

  // ---------- animated values ----------
  function st(v) { return { a: 0, k: v }; }
  // keys: [[percent, value(number|array), ease?], ...]; ease applies to the segment leaving that key
  function anim(keys, period, defEase, opts) {
    opts = opts || {};
    var repeat = opts.repeat || 1, delay = opts.delay || 0, total = period * repeat;
    var arr = function (v) { return Array.isArray(v) ? v : [v]; };
    var list = [];
    for (var r = 0; r < repeat; r++) {
      keys.forEach(function (k) { list.push({ t: (k[0] / 100 + r) * period + delay, v: arr(k[1]), e: k[2] || defEase }); });
    }
    if (delay) {
      // Delayed loops shift into the hold at the end of each cycle; pin the comp edges to the rest value
      var rest = arr(keys[0][1]);
      list = list.filter(function (k) { return k.t < total - 1e-6; });
      list.unshift({ t: 0, v: rest, e: defEase });
      list.push({ t: total, v: rest, e: defEase });
    }
    // drop duplicate times (end of one cycle == start of next)
    var out = [];
    list.forEach(function (k) { if (out.length && Math.abs(out[out.length - 1].t - k.t) < 1e-6) out[out.length - 1] = k; else out.push(k); });
    return {
      a: 1,
      k: out.map(function (k, idx) {
        var kf = { t: Math.round(k.t * FPS * 100) / 100, s: k.v.map(r2) };
        if (idx < out.length - 1) {
          var n = k.v.length;
          kf.o = { x: fill(n, k.e[0]), y: fill(n, k.e[1]) };
          kf.i = { x: fill(n, k.e[2]), y: fill(n, k.e[3]) };
        }
        return kf;
      })
    };
  }
  function fill(n, v) { var a = []; for (var i = 0; i < n; i++) a.push(v); return a; }

  // ---------- shape items ----------
  function shPath(d) { return parsePath(d).map(function (k) { return { ty: "sh", ks: st(k) }; }); }
  function tr() { return { ty: "tr", p: st([0, 0]), a: st([0, 0]), s: st([100, 100]), r: st(0), o: st(100), sk: st(0), sa: st(0) }; }
  function gradStops(pal, reverse) {
    var c = reverse ? [pal.gc, pal.gb, pal.ga] : [pal.ga, pal.gb, pal.gc];
    return { p: 3, k: st([0].concat(c[0], [0.52], c[1], [1], c[2])) };
  }
  function cssLinear(box, deg) {
    var a = deg * Math.PI / 180, dx = Math.sin(a), dy = -Math.cos(a);
    var cx = box[0] + box[2] / 2, cy = box[1] + box[3] / 2;
    var L = (Math.abs(box[2] * dx) + Math.abs(box[3] * dy)) / 2;
    return { s: [r2(cx - dx * L), r2(cy - dy * L)], e: [r2(cx + dx * L), r2(cy + dy * L)] };
  }
  function gradFill(pal, box, deg, reverse) {
    var se = cssLinear(box, deg);
    return { ty: "gf", o: st(100), r: 1, bm: 0, g: gradStops(pal, reverse), s: st(se.s), e: st(se.e), t: 1, nm: "Gradient" };
  }
  function gradStroke(pal, box, deg, w, reverse) {
    var se = cssLinear(box, deg);
    return { ty: "gs", o: st(100), w: st(w), g: gradStops(pal, reverse), s: st(se.s), e: st(se.e), t: 1, lc: 2, lj: 2, ml: 4, bm: 0, nm: "Gradient stroke" };
  }
  function fl(c, op) { return { ty: "fl", c: st(c.concat([1])), o: st(op == null ? 100 : op), r: 1, bm: 0, nm: "Fill" }; }
  function sk(c, op, w) { return { ty: "st", c: st(c.concat([1])), o: st(op), w: st(w), lc: 2, lj: 2, ml: 4, bm: 0, nm: "Stroke" }; }
  function group(name, items) { return { ty: "gr", nm: name, it: items.concat([tr()]) }; }

  // ---------- icon definitions ----------
  // Every element: { kind: "grad"|"glass"|"solid", groups(pal) -> shape groups, pivot, anim: {p, s, r, o} keys, ease }
  function defs(pal) {
    var g140 = function (box) { return gradFill(pal, box, 140); };
    return {
      folder: { period: 2.8, els: [
        { id: "paper", kind: "grad", shapes: [group("paper", shPath(rrect(30, 20, 100, 72, 12)).concat([g140([30, 20, 100, 72])]))],
          pivot: [80, 56], ease: SPRING, p: [[0, [0, 0]], [15, [0, 0]], [40, [0, -18]], [65, [0, -18]], [88, [0, 0]], [100, [0, 0]]] },
        { id: "front", kind: "glass", path: parsePathStr("M16 0 H50 Q57 0 61 6 L66 14 H120 Q136 14 136 30 V70 Q136 86 120 86 H16 Q0 86 0 70 V16 Q0 0 16 0 Z", 12, 42),
          pivot: [80, 128], ease: SMOOTH, s: [[0, [100, 100]], [15, [100, 100]], [40, [97, 90]], [65, [97, 90]], [88, [100, 100]], [100, [100, 100]]] }
      ] },
      toggle: { period: 3, els: [
        { id: "orb", kind: "grad", shapes: [group("orb", shPath(circle(122, 52, 30)).concat([g140([92, 22, 60, 60])]))],
          pivot: [122, 52], ease: SPRING,
          p: [[0, [0, 0]], [26, [0, 0]], [40, [-6, 2]], [70, [-6, 2]], [90, [0, 0]], [100, [0, 0]]],
          s: [[0, [100, 100]], [26, [100, 100]], [40, [112, 112]], [70, [112, 112]], [90, [100, 100]], [100, [100, 100]]] },
        { id: "track", kind: "glass", path: rrect(8, 46, 112, 54, 27), pivot: [64, 73] },
        { id: "knob", kind: "solid", shapes: [
            group("knob", shPath(circle(35, 73, 20)).concat([fl(pal.knob)])),
            group("ring", shPath(circle(35, 73, 19)).concat([sk(pal.gb, 35, 2)]))
          ], pivot: [35, 73], ease: SPRING,
          p: [[0, [0, 0]], [20, [0, 0]], [40, [58, 0]], [70, [58, 0]], [90, [0, 0]], [100, [0, 0]]] }
      ] },
      play: { period: 2.4, els: [
        { id: "back", kind: "grad", shapes: [group("back", parsePathShapes("M0 12 Q0 0 11 6 L64 40 Q72 48 64 56 L11 90 Q0 96 0 84 Z", 12, 22).concat([g140([12, 22, 72, 96])]))],
          pivot: [48, 70], ease: SPRING, p: [[0, [0, 0]], [20, [0, 0]], [42, [14, 0]], [60, [0, 0]], [100, [0, 0]]] },
        { id: "front", kind: "glass", path: parsePathStr("M0 16 Q0 0 15 7 L98 48 Q106 56 98 64 L15 105 Q0 112 0 96 Z", 42, 14),
          pivot: [95, 70], ease: SPRING, p: [[0, [0, 0]], [12, [0, 0]], [34, [14, 0]], [52, [0, 0]], [100, [0, 0]]] }
      ] },
      location: { period: 2.8, els: [
        { id: "land", kind: "grad", shapes: [group("land", parsePathShapes("M18 0 H106 Q114 0 116 8 L124 38 Q124 46 116 46 H8 Q0 46 0 38 L8 8 Q10 0 18 0 Z", 18, 84).concat([g140([18, 84, 124, 46])]))],
          pivot: [80, 130], ease: EASE_OUT,
          s: [[0, [100, 100]], [21, [100, 100]], [25, [104, 90]], [33, [100, 100]], [37, [100, 100]], [40, [102, 96]], [46, [100, 100]], [100, [100, 100]]] },
        { id: "pin", kind: "glass", path: parsePathStr("M30 0 A30 30 0 0 1 60 30 C60 50 42 64 30 86 C18 64 0 50 0 30 A30 30 0 0 1 30 0 Z", 50, 8),
          pivot: [80, 51], ease: EASE_IO,
          p: [[0, [0, -46], [0.5, 0, 0.9, 0.5]], [22, [0, 0], EASE_OUT], [30, [0, -12], EASE_IN], [38, [0, 0]], [78, [0, 0]], [94, [0, -46]], [100, [0, -46]]],
          o: [[0, 0, [0.5, 0, 0.9, 0.5]], [22, 100, EASE_OUT], [38, 100], [78, 100], [94, 0], [100, 0]],
          children: [{ id: "hole", kind: "solid", shapes: [group("hole", shPath(circle(80, 38, 11)).concat([fl(pal.white, 88)]))] }] }
      ] },
      search: { period: 3.2, els: [
        { id: "lens", kind: "grad", shapes: [group("lens", shPath(circle(104, 52, 18)).concat(shPath("M118 66 L138 86")).concat([gradStroke(pal, [78, 26, 70, 70], 135, 7)]))],
          pivot: [113, 61], ease: SMOOTH, p: [[0, [0, 0]], [10, [0, 0]], [45, [-62, 0]], [58, [-62, 0]], [92, [0, 0]], [100, [0, 0]]] },
        { id: "bar", kind: "glass", path: rrect(6, 56, 104, 34, 12), pivot: [58, 73] }
      ].concat([0, 1, 2, 3].map(function (k) {
        return { id: "dot" + (k + 1), kind: "solid", shapes: [group("dot", shPath(circle(25.5 + k * 14, 73, 3.5)).concat([fl(pal.white)]))],
          pivot: [25.5 + k * 14, 73], ease: EASE_OUT, delay: (3 - k) * 0.1,
          s: [[0, [100, 100]], [24, [100, 100]], [32, [170, 170]], [42, [100, 100]], [100, [100, 100]]] };
      })) },
      chat: { period: 3.6, els: [
        { id: "b1", kind: "grad", shapes: [group("b1", parsePathShapes("M14 0 H86 Q100 0 100 14 V60 Q100 74 86 74 H22 L5 91 Q0 94 0 88 V14 Q0 0 14 0 Z", 10, 10).concat([g140([10, 10, 100, 92])]))],
          pivot: [60, 56], ease: EASE_IO, p: [[0, [0, 0]], [50, [-3, -4]], [100, [0, 0]]] },
        { id: "b2", kind: "glass", path: parsePathStr("M14 0 H84 Q98 0 98 14 V88 Q98 94 93 91 L76 74 H14 Q0 74 0 60 V14 Q0 0 14 0 Z", 52, 40),
          pivot: [101, 86], ease: EASE_IO, p: [[0, [0, 0]], [50, [3, 3]], [100, [0, 0]]],
          children: [0, 1, 2].map(function (k) {
            return { id: "typing" + (k + 1), kind: "solid", shapes: [group("dot", shPath(circle(83 + k * 18, 77, 6)).concat([fl(pal.white)]))],
              pivot: [83 + k * 18, 77], ease: EASE_IO, period: 1.2, repeat: 3, delay: k * 0.15,
              p: [[0, [0, 0]], [30, [0, -7]], [60, [0, 0]], [100, [0, 0]]],
              o: [[0, 75], [30, 100], [60, 75], [100, 75]] };
          }) }
      ] },
      download: { period: 4, els: [
        { id: "arrow", kind: "grad", shapes: [
            group("shaft", shPath("M80 60 V106").concat([gradStroke(pal, [62, 56, 36, 76], 180, 8, true)])),
            group("head", shPath("M67 106 L80 122 L93 106 Z").concat([sk(pal.ga, 100, 6), fl(pal.ga)]))
          ], pivot: [80, 94], ease: [0.45, 0, 0.55, 1], period: 2, repeat: 2,
          p: [[0, [0, -30]], [42, [0, 2]], [52, [0, -3]], [60, [0, 0]], [84, [0, 0]], [100, [0, 14]]],
          o: [[0, 0], [15, 100], [60, 100], [84, 100], [100, 0]] },
        { id: "cloud", kind: "glass", path: parsePathStr("M50 90 A45 45 0 1 1 93.8 34.7 A30 30 0 1 1 110 90 Z", 10, 8),
          pivot: [81, 53], ease: EASE_IO, p: [[0, [0, 0]], [50, [-3, -4]], [100, [0, 0]]] }
      ] },
      windows: { period: 3.2, els: [
        { id: "back", kind: "grad", shapes: [group("back", shPath(rrect(54, 18, 96, 70, 10)).concat([g140([54, 18, 96, 70])]))],
          pivot: [102, 53], ease: SPRING,
          p: [[0, [0, 0]], [15, [0, 0]], [42, [6, 4]], [62, [6, 4]], [88, [0, 0]], [100, [0, 0]]],
          s: [[0, [100, 100]], [15, [100, 100]], [42, [94, 94]], [62, [94, 94]], [88, [100, 100]], [100, [100, 100]]] },
        { id: "front", kind: "glass", path: rrect(10, 52, 96, 70, 10), pivot: [58, 87], ease: SPRING,
          p: [[0, [0, 0]], [15, [0, 0]], [42, [30, -22]], [62, [30, -22]], [88, [0, 0]], [100, [0, 0]]] }
      ] },
      lock: { period: 2.8, els: [
        { id: "shackle", kind: "grad", shapes: [group("shackle", shPath("M52 70 V42 A28 28 0 0 1 108 42 V70").concat([gradStroke(pal, [42, 6, 76, 66], 90, 9)]))],
          pivot: [108.1, 70], ease: SMOOTH,
          p: [[0, [0, 0]], [15, [0, 0]], [32, [0, -16]], [42, [0, -16]], [58, [0, -16]], [68, [0, -16]], [76, [0, 2]], [82, [0, 0]], [100, [0, 0]]],
          r: [[0, 0], [15, 0], [32, 0], [42, -22], [58, -22], [68, 0], [76, 0], [82, 0], [100, 0]] },
        { id: "body", kind: "glass", path: rrect(32, 56, 96, 78, 16), pivot: [80, 95], ease: EASE_OUT,
          p: [[0, [0, 0]], [75, [0, 0]], [79, [0, 3]], [86, [0, 0]], [100, [0, 0]]],
          children: [
            { id: "glow", kind: "solid", shapes: [group("glow", shPath(circle(80, 95, 13)).concat([fl(pal.white)]))], pivot: [80, 95], ease: EASE_OUT,
              o: [[0, 0], [30, 0], [42, 35], [58, 35], [70, 0], [100, 0]] },
            { id: "key", kind: "solid", shapes: [group("key", shPath(circle(80, 95, 7)).concat([fl(pal.white)]))], pivot: [80, 95], ease: EASE_OUT,
              s: [[0, [100, 100]], [30, [100, 100]], [42, [125, 125]], [58, [125, 125]], [70, [100, 100]], [100, [100, 100]]] }
          ] }
      ] },
      people: { period: 3, els: [
        { id: "back person", kind: "grad", shapes: [
            group("head", shPath(circle(103, 35, 25)).concat([g140([78, 10, 50, 50])])),
            group("body", shPath(rrect(64, 62, 92, 54, [46, 46, 14, 14])).concat([g140([64, 62, 92, 54])]))
          ], pivot: [110, 63], ease: SPRING, p: [[0, [0, 0]], [18, [0, 0]], [40, [12, 0]], [64, [12, 0]], [88, [0, 0]], [100, [0, 0]]] },
        { id: "head", kind: "glass", path: circle(65, 47, 25), pivot: [65, 47], ease: SPRING,
          p: [[0, [0, 0]], [30, [0, 0]], [40, [0, -6]], [50, [0, 0]], [100, [0, 0]]] },
        { id: "body", kind: "glass", path: rrect(12, 74, 106, 58, [53, 53, 14, 14]), pivot: [65, 103] }
      ] }
    };
  }
  // Helpers for paths given in element-local coordinates
  function parsePathStr(d, ox, oy) { return { d: d, ox: ox, oy: oy }; }
  function parsePathShapes(d, ox, oy) { return parsePath(d, ox, oy).map(function (k) { return { ty: "sh", ks: st(k) }; }); }
  function glassPathShapes(path) {
    if (typeof path === "string") return shPath(path);
    return parsePathShapes(path.d, path.ox, path.oy);
  }

  // ---------- build ----------
  function build(icon, opts) {
    opts = opts || {};
    var hue = opts.hue == null ? 227 : opts.hue, glass = opts.glass || "light";
    var pal = palette(hue, glass), def = defs(pal)[icon];
    if (!def) throw new Error("Unknown icon: " + icon);
    var total = def.period, frames = Math.round(total * FPS);
    var layers = [], nextInd = 1;

    function ks(el, identity) {
      var t = { o: st(100), r: st(0), p: st([0, 0, 0]), a: st([0, 0, 0]), s: st([100, 100, 100]) };
      if (identity || !el) return t;
      var period = el.period || def.period, o = { repeat: el.repeat, delay: el.delay };
      var pv = el.pivot || [0, 0];
      t.a = st([pv[0], pv[1], 0]);
      if (el.p) t.p = anim(el.p.map(function (k) { return [k[0], [pv[0] + k[1][0], pv[1] + k[1][1]], k[2]]; }), period, el.ease || EASE_IO, o);
      else t.p = st([pv[0], pv[1], 0]);
      if (el.s) t.s = anim(el.s, period, el.ease || EASE_IO, o);
      if (el.r) t.r = anim(el.r, period, el.ease || EASE_IO, o);
      if (el.o) t.o = anim(el.o, period, el.ease || EASE_IO, o);
      return t;
    }
    function opacityOf(el) {
      return el && el.o ? anim(el.o, el.period || def.period, el.ease || EASE_IO, { repeat: el.repeat, delay: el.delay }) : null;
    }
    function layer(nm, shapes, t, extra) {
      var L = { ddd: 0, ind: nextInd++, ty: 4, nm: nm, sr: 1, ks: t, ao: 0, shapes: shapes, ip: 0, op: frames, st: 0, bm: 0 };
      for (var k in extra) L[k] = extra[k];
      return L;
    }
    var blur = { ty: 29, nm: "Gaussian Blur", np: 5, mn: "ADBE Gaussian Blur 2", ix: 1, en: 1, ef: [
      { ty: 0, nm: "Blurriness", mn: "ADBE Gaussian Blur 2-0001", ix: 1, v: st(26) },
      { ty: 7, nm: "Blur Dimensions", mn: "ADBE Gaussian Blur 2-0002", ix: 2, v: st(1) },
      { ty: 7, nm: "Repeat Edge Pixels", mn: "ADBE Gaussian Blur 2-0003", ix: 3, v: st(0) }
    ] };

    var gradEl = def.els.filter(function (e) { return e.kind === "grad"; })[0];
    var top = [], middle = [], bottom = [];

    // Gradient layer (bottom). It is hidden wherever glass covers it (inverted alpha matte below),
    // so only the blurred copy shows through the glass, like CSS backdrop-filter.
    var glassEls = def.els.filter(function (e) { return e.kind === "glass"; });
    var cutout = layer("glass cutout", glassEls.map(function (el) {
      var t = ks(el), g = group(el.id, glassPathShapes(el.path).concat([fl(pal.white)]));
      var gt = g.it[g.it.length - 1];
      gt.a = st([t.a.k[0], t.a.k[1]]); gt.p = t.p; gt.s = t.s; gt.r = t.r; gt.o = t.o;
      return g;
    }), ks(null, true), { td: 1 });
    var gradLayer = layer(gradEl.id, gradEl.shapes, ks(gradEl), { tt: 2 });
    bottom.push(cutout, gradLayer);
    var gradOpacity = opacityOf(gradEl);
    // Invisible frame around the stage: widens the blurred copy's bounds so players that size
    // the matte region from the layer's bounding box do not clip the blur.
    var bounds = group("bounds", shPath(rrect(-40, -40, W + 80, H + 80, 0)).concat([fl(pal.white, 0)]));

    def.els.forEach(function (el) {
      if (el.kind === "glass") {
        var glassShapes = glassPathShapes(el.path);
        var tint = layer(el.id + " glass", [group("glass", glassShapes.concat([sk(pal.white, pal.edgeOp, 1.5), fl(pal.glass, pal.glassOp)]))], ks(el));
        var tintOpacity = opacityOf(el);
        var matteKs = ks(null, true); if (tintOpacity) matteKs.o = tintOpacity;
        var matte = layer(el.id + " matte", [group("matte", glassPathShapes(el.path).concat([fl(pal.white)]))], matteKs, { td: 1, parent: tint.ind });
        var copyKs = ks(null, true); if (gradOpacity) copyKs.o = gradOpacity;
        var copy = layer(el.id + " frost", JSON.parse(JSON.stringify(gradEl.shapes)).concat([JSON.parse(JSON.stringify(bounds))]), copyKs, { tt: 1, parent: gradLayer.ind, ef: [blur] });
        (el.children || []).forEach(function (c) {
          var cks = ks(c); if (!c.o && tintOpacity) cks.o = tintOpacity;
          // Children share the stage coordinate space, so parenting alone makes them follow the glass
          top.push(layer(c.id, c.shapes, cks, { parent: tint.ind }));
        });
        middle.push(tint, matte, copy);
      } else if (el.kind === "solid") {
        top.push(layer(el.id, el.shapes, ks(el)));
      }
    });

    // Lottie draws layers[0] on top. Matte pairs must stay adjacent: matte directly above its target.
    var ordered = top.slice().reverse().concat(middle, bottom);
    return {
      v: "5.7.4", fr: FPS, ip: 0, op: frames, w: W, h: H, nm: "Glass " + TITLES[icon], ddd: 0,
      meta: { g: "Glass Icon Motion", d: "Frosted glass " + TITLES[icon] + " icon, base hue " + hue + "°" },
      assets: [], layers: ordered, markers: []
    };
  }

  // ---------- zip / dotLottie ----------
  var CRC = (function () {
    var t = [];
    for (var n = 0; n < 256; n++) { var c = n; for (var k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
    return t;
  })();
  function crc32(b) { var c = 0xFFFFFFFF; for (var i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }
  function utf8(s) { return new TextEncoder().encode(s); }
  // files: [{name, data: Uint8Array|string}] -> Uint8Array (stored, no compression)
  function zip(files) {
    var parts = [], central = [], offset = 0;
    files.forEach(function (f) {
      var name = utf8(f.name), data = typeof f.data === "string" ? utf8(f.data) : f.data, crc = crc32(data);
      var lh = new DataView(new ArrayBuffer(30));
      lh.setUint32(0, 0x04034b50, true); lh.setUint16(4, 20, true); lh.setUint16(6, 0x0800, true); lh.setUint16(8, 0, true);
      lh.setUint16(10, 0, true); lh.setUint16(12, 0x21, true); lh.setUint32(14, crc, true);
      lh.setUint32(18, data.length, true); lh.setUint32(22, data.length, true); lh.setUint16(26, name.length, true); lh.setUint16(28, 0, true);
      var ch = new DataView(new ArrayBuffer(46));
      ch.setUint32(0, 0x02014b50, true); ch.setUint16(4, 20, true); ch.setUint16(6, 20, true); ch.setUint16(8, 0x0800, true);
      ch.setUint16(10, 0, true); ch.setUint16(12, 0, true); ch.setUint16(14, 0x21, true); ch.setUint32(16, crc, true);
      ch.setUint32(20, data.length, true); ch.setUint32(24, data.length, true); ch.setUint16(28, name.length, true);
      ch.setUint32(42, offset, true);
      parts.push(new Uint8Array(lh.buffer), name, data);
      central.push(new Uint8Array(ch.buffer), name);
      offset += 30 + name.length + data.length;
    });
    var cdSize = central.reduce(function (s, p) { return s + p.length; }, 0);
    var end = new DataView(new ArrayBuffer(22));
    end.setUint32(0, 0x06054b50, true); end.setUint16(8, files.length, true); end.setUint16(10, files.length, true);
    end.setUint32(12, cdSize, true); end.setUint32(16, offset, true);
    var all = parts.concat(central, [new Uint8Array(end.buffer)]);
    var out = new Uint8Array(all.reduce(function (s, p) { return s + p.length; }, 0)), o2 = 0;
    all.forEach(function (p) { out.set(p, o2); o2 += p.length; });
    return out;
  }
  // One or more animations -> dotLottie bytes
  function dotLottie(anims) {
    var manifest = {
      version: "1", generator: "Glass Icon Motion", author: "", revision: 1,
      animations: anims.map(function (a) { return { id: a.id, speed: 1, loop: true, autoplay: true, direction: 1, playMode: "normal" }; }),
      activeAnimationId: anims[0].id
    };
    return zip([{ name: "manifest.json", data: JSON.stringify(manifest) }].concat(anims.map(function (a) {
      return { name: "animations/" + a.id + ".json", data: JSON.stringify(a.json) };
    })));
  }

  var api = { ICONS: ICONS, TITLES: TITLES, build: build, dotLottie: dotLottie, zip: zip, palette: palette };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.GlassLottie = api;
})(typeof window !== "undefined" ? window : this);

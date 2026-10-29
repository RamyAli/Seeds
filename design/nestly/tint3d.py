"""Tint Fluent 3D emoji into one glossy brand-blue family (option E)."""
import sys, os
from PIL import Image, ImageOps

def hx(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
STOPS = [(0, hx('#06174A')), (.28, hx('#1541C4')), (.52, hx('#2563EB')), (.74, hx('#6FA3FF')), (.90, hx('#CFE1FF')), (1, hx('#FFFFFF'))]

def lut():
    out = []
    for i in range(256):
        t = i / 255
        for (t0, c0), (t1, c1) in zip(STOPS, STOPS[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                out.append(tuple(int(c0[j] + (c1[j] - c0[j]) * k) for j in range(3)))
                break
    return out

L = lut()
src, dst = sys.argv[1], sys.argv[2]
for f in sorted(os.listdir(src)):
    if not f.endswith('_3d.png'):
        continue
    im = Image.open(os.path.join(src, f)).convert('RGBA')
    a = im.getchannel('A')
    g = ImageOps.autocontrast(im.convert('L'), cutoff=1, mask=a.point(lambda v: 255 if v > 128 else 0))
    mean = sum(v for v, al in zip(g.get_flattened_data(), a.get_flattened_data()) if al > 128) / max(1, sum(1 for al in a.get_flattened_data() if al > 128))
    gamma = 1.0 + max(0, (mean - 120) / 110)          # bright objects get pushed into the blues
    g = g.point(lambda v: int(255 * (v / 255) ** gamma))
    rgb = Image.new('RGB', im.size)
    rgb.putdata([L[v] for v in g.get_flattened_data()])
    out = rgb.convert('RGBA'); out.putalpha(a)
    out.thumbnail((200, 200), Image.LANCZOS)
    out.save(os.path.join(dst, f.replace('_3d', '')), optimize=True)

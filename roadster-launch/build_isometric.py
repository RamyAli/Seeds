"""Isometric line illustration of the Roadster launch stage.

World axes (metres): x across the runway, y along it (the car drives toward -y),
z up. The ramp entry sits at y = 0; the runway runs back to y = 45.
"""
import math, os

COS30 = math.cos(math.radians(30))
VIEW = (1, 1, 1)                       # direction toward the viewer
LIGHT = (-0.35, 0.55, 0.76)
LINE, LINE_SOFT, LED = '#8c8c8c', '#b8b8b8', '#e5484d'

def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u**3*a + 3*u*u*t*b + 3*u*t*t*c + t**3*d for a, b, c, d in zip(p0, p1, p2, p3))

def curve(segs, n=40):
    pts = []
    for s in segs:
        pts += [bez(*s, i/n) for i in range(0 if not pts else 1, n+1)]
    return pts

# Ramp profile in (u, z): u is distance past the ramp entry, z height.
INNER = curve([((0, 0), (5.5, 0), (10, 4.5), (10, 10)),
               ((10, 10), (10, 18), (3.5, 23.5), (-6, 23.5))])
OUTER = curve([((1, 0), (6.25, 0.4), (11, 4.5), (11, 10)),
               ((11, 10), (11, 18.75), (4, 24.5), (-6, 24.5))])
RAMP_X = (0.0, 6.0)
MAST_U, MAST_X, MAST_H = (12, 15), (-0.5, 6.5), 26.0

def W(x, u, z): return (x, -u, z)      # ramp-local (x, u, z) -> world

def sub(a, b): return tuple(i-j for i, j in zip(a, b))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return sum(i*j for i, j in zip(a, b))
def norm(a):
    l = math.sqrt(dot(a, a)) or 1
    return tuple(i/l for i in a)

S = 17.0
OX, OY = 0.0, 0.0
def P(p):
    x, y, z = p
    return (OX + (x - y)*COS30*S, OY + ((x + y)*0.5 - z)*S)

items = []   # (depth, svg) painted back to front

def depth(pts): return sum(dot(p, VIEW) for p in pts)/len(pts)

def shade(n, lo=0.80, hi=1.0):
    k = 0.5 + 0.5*dot(norm(n), norm(LIGHT))
    v = int(255*(lo + (hi-lo)*k))
    return f'#{v:02x}{v:02x}{v:02x}'

def poly_svg(pts, fill, stroke=None, sw=0.8, extra=''):
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in map(P, pts))
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else f' stroke="{fill}" stroke-width="0.6"'
    return f'<polygon points="{d}" fill="{fill}"{st}{extra}/>'

def face(pts, n=None, stroke=None, bias=0.0, cull=True, fill=None, lo=0.86):
    if n is None: n = cross(sub(pts[1], pts[0]), sub(pts[2], pts[0]))
    if cull and dot(n, VIEW) <= 0: return
    items.append((depth(pts)+bias, poly_svg(pts, fill or shade(n, lo), stroke)))

def seg(a, b, color=LINE, sw=0.8, bias=0.0, step=1.0, dash=None):
    n = max(1, int(math.dist(a, b)/step))
    for i in range(n):
        p = tuple(a[k]+(b[k]-a[k])*i/n for k in range(3))
        q = tuple(a[k]+(b[k]-a[k])*(i+1)/n for k in range(3))
        (x1, y1), (x2, y2) = P(p), P(q)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        items.append((depth([p, q])+bias, f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{da}/>'))

def polyline(pts, **kw):
    for a, b in zip(pts, pts[1:]): seg(a, b, step=99, **kw)

def box(x0, x1, y0, y1, z0, z1, stroke=LINE, lo=0.86):
    v = lambda i, j, k: ((x0, x1)[i], (y0, y1)[j], (z0, z1)[k])
    for f, n in (([v(1,0,0), v(1,1,0), v(1,1,1), v(1,0,1)], (1,0,0)),
                 ([v(0,1,0), v(1,1,0), v(1,1,1), v(0,1,1)], (0,1,0)),
                 ([v(0,0,1), v(1,0,1), v(1,1,1), v(0,1,1)], (0,0,1))):
        face(f, n, stroke=stroke, lo=lo)

# ---------------------------------------------------------------- ramp
def profile_normal(prof, i):
    a, b = prof[max(i-1, 0)], prof[min(i+1, len(prof)-1)]
    du, dz = b[0]-a[0], b[1]-a[1]
    l = math.hypot(du, dz)
    return (-dz/l, du/l)                    # toward the concave side (u, z)

def n3(nu, nz): return (0, -nu, nz)

for prof, sign in ((INNER, 1), (OUTER, -1)):
    for i in range(len(prof)-1):
        (u1, z1), (u2, z2) = prof[i], prof[i+1]
        nu, nz = profile_normal(prof, i)
        q = [W(RAMP_X[0], u1, z1), W(RAMP_X[1], u1, z1), W(RAMP_X[1], u2, z2), W(RAMP_X[0], u2, z2)]
        face(q, n3(sign*nu, sign*nz), lo=0.80 if sign > 0 else 0.74)
for i in range(len(INNER)-1):              # side panels (C-shaped)
    a, b, c, d = INNER[i], INNER[i+1], OUTER[i+1], OUTER[i]
    for x, n in ((RAMP_X[1], (1, 0, 0)), (RAMP_X[0], (-1, 0, 0))):
        face([W(x, *a), W(x, *b), W(x, *c), W(x, *d)], n, lo=0.84)
face([W(RAMP_X[0], *INNER[-1]), W(RAMP_X[1], *INNER[-1]), W(RAMP_X[1], *OUTER[-1]), W(RAMP_X[0], *OUTER[-1])], (0, 1, 0), stroke=LINE)

for x in RAMP_X:                           # outlines
    # the far deck edge is a silhouette: lift it past the strips it bounds
    polyline([W(x, u, z) for u, z in INNER], bias=0.6 if x else 3.2, sw=1.1)
    polyline([W(x, u, z) for u, z in OUTER], bias=0.6, sw=1.1)
polyline([W(RAMP_X[1]-0.12, u, z) for u, z in INNER], color=LED, sw=1.6, bias=0.5)
polyline([W(RAMP_X[0]+0.12, u, z) for u, z in INNER], color=LED, sw=1.6, bias=0.5)
for x in (2.0, 4.0):                       # white lane lines
    polyline([W(x, u + 0.02*profile_normal(INNER, i)[0], z + 0.02*profile_normal(INNER, i)[1])
              for i, (u, z) in enumerate(INNER)], color=LINE_SOFT, sw=0.9, bias=0.4)

def outer_at_z(z):                         # rear bulge of the ramp at height z
    return max((p for p in OUTER if abs(p[1]-z) < 0.4), key=lambda p: p[0])
def outer_at_u_top(u):
    return min((p for p in OUTER if p[1] > 15), key=lambda p: abs(p[0]-u))

# ---------------------------------------------------------------- truss mast
def lattice(x0, x1, u0, u1, z0, z1, axis, step):
    """Box truss: four chords along `axis` with rungs and zig-zag diagonals."""
    c = [(x0, u0), (x1, u0), (x1, u1), (x0, u1)] if axis == 'z' else None
    if axis == 'z':
        for x, u in c: seg(W(x, u, z0), W(x, u, z1), sw=1.0)
        n = int((z1-z0)/step)
        for k in range(n+1):
            z = z0 + k*step
            for (xa, ua), (xb, ub) in zip(c, c[1:]+c[:1]):
                seg(W(xa, ua, z), W(xb, ub, z), sw=0.7)
                if k < n:
                    za, zb = (z, z+step) if k % 2 else (z+step, z)
                    seg(W(xa, ua, za), W(xb, ub, zb), color='#b4b4b4', sw=0.6)
    else:                                   # chords along u at height z0..z1
        c = [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
        for x, z in c: seg(W(x, u0, z), W(x, u1, z), sw=1.0)
        n = int((u1-u0)/step)
        for k in range(n+1):
            u = u0 + k*step
            for (xa, za), (xb, zb) in zip(c, c[1:]+c[:1]):
                seg(W(xa, u, za), W(xb, u, zb), sw=0.7)
                if k < n:
                    ua, ub = (u, u+step) if k % 2 else (u+step, u)
                    seg(W(xa, ua, za), W(xb, ub, zb), color='#b4b4b4', sw=0.6)

lattice(*MAST_X, *MAST_U, 0, MAST_H, 'z', 2.0)
for x0 in (MAST_X[0], RAMP_X[1]-0.5):       # two overhead gantry beams
    lattice(x0, x0+1.0, -6, MAST_U[1], 24.6, MAST_H, 'u', 1.5)
for u in range(-5, 15, 3):                  # cross ties between the beams
    seg(W(MAST_X[0]+1, u, MAST_H), W(RAMP_X[1]-0.5, u, MAST_H), sw=0.7)
for x in (0.0, 6.0):
    for u in (-4, -1, 2, 5, 8):             # hangers beam -> ramp back
        pu, pz = outer_at_u_top(u)
        seg(W(x, pu, pz), W(x, pu, 24.6), sw=0.7)
    for z in (3, 7, 11, 15, 19):            # struts ramp back -> mast
        pu, pz = outer_at_z(z)
        seg(W(x, pu, pz), W(x, MAST_U[0], pz), sw=0.7)
    seg(W(x, outer_at_z(3)[0], 3), W(x, MAST_U[0], 7), color='#b4b4b4', sw=0.6)
for x, ax in ((MAST_X[0], -4), (MAST_X[1], 10)):
    seg(W(x, MAST_U[1], MAST_H), W(ax, 25, 0), color='#b9b9b9', sw=0.6, step=2)
    box(ax-0.4, ax+0.4, -25.4, -24.6, 0, 0.4)

# ---------------------------------------------------------------- car
CAR = [(0, .32), (0, .72), (.35, .84), (1.55, .94), (2.1, 1.17), (2.9, 1.14),
       (3.55, .82), (4.3, .62), (4.3, .32)]
GLASS = [(1.75, .97), (2.18, 1.12), (2.86, 1.1), (3.3, .86)]

K = 1.35                                   # drawn slightly oversize so the cars read at this scale
def car(xc, y0, z0, heading=-1):
    """Car with rear end at y0; heading -1 drives toward -y."""
    w = 1.9*K
    pt = lambda x, u, z: (x, y0 + heading*u*K, z0 + z*K)
    for x, nx in ((xc, -1), (xc+w, 1)):
        face([pt(x, u, z) for u, z in CAR], (nx, 0, 0), stroke=LINE, lo=0.9)
        if nx > 0:
            face([pt(x+0.01, u, z) for u, z in GLASS], (1, 0, 0), stroke=LINE, fill='#e4e4e4')
            for wu in (0.8, 3.5):
                face([pt(x+0.03, wu + .36*math.cos(t/12*math.tau), .36 + .36*math.sin(t/12*math.tau))
                      for t in range(12)], (1, 0, 0), stroke=LINE, fill='#d6d6d6', cull=False)
    for (u1, z1), (u2, z2) in zip(CAR, CAR[1:]+CAR[:1]):
        q = [pt(xc, u1, z1), pt(xc+w, u1, z1), pt(xc+w, u2, z2), pt(xc, u2, z2)]
        n = cross(sub(q[1], q[0]), sub(q[3], q[0]))
        if dot(n, (0, heading*((u1+u2)/2 - 2.15), (z1+z2)/2 - 0.7)) < 0: n = tuple(-i for i in n)
        face(q, n, stroke=LINE, lo=0.86)

def plume(x, y, z, length=7):
    pts = [(x-0.25, y, z), (x+0.25, y, z), (x+0.9, y, z-length), (x-0.9, y, z-length)]
    items.append((depth(pts)-3, poly_svg(pts, '#eef1f4', '#cfd6dd', 0.6, ' stroke-dasharray="2 3"')))

car(3 - 0.95*K, 30, 0)
HX, HY, HZ = 3 - 0.95*K, 13.0, 15.0              # hovering car after leaving the lip
for du in (0.7, 2.15, 3.6): plume(HX+0.95*K, HY+du*K, HZ+0.3*K)
car(HX, HY, HZ, heading=1)

# ---------------------------------------------------------------- lights & camera
for fx, fy in ((-7, 22), (16, 12), (-6, -4), (12, 41)):
    seg((fx, fy, 0), (fx, fy, 7), sw=1.0)
    box(fx-0.6, fx+0.6, fy-0.25, fy+0.25, 7, 7.8)
    box(fx-0.5, fx+0.5, fy-0.5, fy+0.5, 0, 0.3)
box(9.6, 11.2, 18, 19.8, 0.15, 0.7)        # camera dolly
seg((10.4, 18.9, 0.7), (10.4, 18.9, 2.2), sw=1.0)
box(10.1, 10.7, 18.5, 19.4, 2.2, 2.7)

# ---------------------------------------------------------------- ground layer
under = []
def flat(pts, fill, stroke='none', sw=0.8, extra=''):
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in map(P, pts))
    under.append(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>')
def flat_line(pts, color, sw=0.8, extra=''):
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in map(P, pts))
    under.append(f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{extra}/>')

GZ = -0.25
CX, CY = 3.0, 6.0
for r in (11, 21, 33, 46):
    flat_line([(CX + r*math.cos(t/180*math.pi), CY + r*math.sin(t/180*math.pi), GZ) for t in range(0, 361, 3)], '#dddddd')
flat_line([(CX-70, CY, GZ), (CX+70, CY, GZ)], '#dddddd')
flat_line([(CX, CY-70, GZ), (CX, CY+70, GZ)], '#dddddd')

def sh(p, z0=GZ):                          # project onto the ground along the light
    x, y, z = p
    h = z - z0
    return (x + 0.42*h, y - 0.18*h, z0)
SH = '#efefef'
for i in range(len(INNER)-1):
    for x in RAMP_X:
        flat([sh(W(x, *INNER[i])), sh(W(x, *INNER[i+1])), sh(W(x, *OUTER[i+1])), sh(W(x, *OUTER[i]))], SH, SH, 0.6)
    flat([sh(W(RAMP_X[0], *INNER[i])), sh(W(RAMP_X[1], *INNER[i])), sh(W(RAMP_X[1], *INNER[i+1])), sh(W(RAMP_X[0], *INNER[i+1]))], SH, SH, 0.6)
mx0, mx1 = MAST_X; mu0, mu1 = MAST_U
# runway slab
flat([(-1, 0, GZ), (7, 0, GZ), (7, 45, GZ), (-1, 45, GZ)], '#f1f1f1')
flat([(7, 0, GZ), (7, 45, GZ), (7, 45, 0), (7, 0, 0)], '#e6e6e6', LINE)
flat([(-1, 45, GZ), (7, 45, GZ), (7, 45, 0), (-1, 45, 0)], '#ececec', LINE)
flat([(-1, 0, 0), (7, 0, 0), (7, 45, 0), (-1, 45, 0)], '#fbfbfb', LINE)
for x in (-0.75, 6.75):
    flat_line([(x, 0, 0), (x, 45, 0)], LED, 1.6)
flat_line([(3, 1, 0), (3, 44, 0)], '#cfcfcf', 0.8, ' stroke-dasharray="10 8"')
for x in (9.8, 11.0):                      # camera dolly rails
    flat_line([(x, 2, GZ), (x, 44, GZ)], '#c4c4c4', 0.8)
# hover-car shadow on the runway
flat([(HX + 0.42*15 + (dx+1)*0.95*K, HY - 0.18*15 + (2.15 + dy*2.3)*K, 0) for dx, dy in
      [(math.cos(t/16*math.tau), math.sin(t/16*math.tau)) for t in range(16)]], '#ececec')

# ---------------------------------------------------------------- car path
def offset_inner(d):
    return [W(3.0, u + d*profile_normal(INNER, i)[0], z + d*profile_normal(INNER, i)[1]) for i, (u, z) in enumerate(INNER)]
path = [(3.0, 27.5, 0.6), (3.0, 0, 0.6)] + offset_inner(0.6)
lip = path[-1]
path += [bez((lip[1], lip[2]), (lip[1]+4, lip[2]), (HY + 2, HZ + 6), (HY + 2.9*K, HZ + 1.6*K), t/20) for t in range(1, 21)]
path = path[:len(offset_inner(0.6))+2] + [(3.0, y, z) for y, z in path[len(offset_inner(0.6))+2:]]
pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in map(P, path))

# ---------------------------------------------------------------- output
allpts = []
import re
for _, svg in items:
    allpts += [float(v) for v in re.findall(r'-?\d+\.\d', svg)]
xs = [P(p)[0] for p in [(CX-46, CY, 0), (CX+46, CY, 0)]]
ys = [P(p)[1] for p in [(3, -14, MAST_H), (CX, CY+46, 0)]]
WIDTH, HEIGHT = 2000, 1200
sc = min((WIDTH-120)/(xs[1]-xs[0]), (HEIGHT-120)/(ys[1]-ys[0]), 1.0)
tx = WIDTH/2 - sc*(P((CX, CY, 0))[0])
ty = 70 - sc*ys[0]
items.sort(key=lambda t: t[0])
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">',
       f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>',
       f'<g transform="translate({tx:.1f} {ty:.1f}) scale({sc:.3f})">']
out += under + [s for _, s in items]
out.append(f'<polyline points="{pts}" fill="none" stroke="#8a8a8a" stroke-width="1.1" stroke-dasharray="5 6" stroke-linecap="round"/>')
out.append('</g>')
out.append('<text x="80" y="1110" font-family="Helvetica Neue, Arial, sans-serif" font-size="22" letter-spacing="9" fill="#6f6f6f">ROADSTER  LAUNCH  STAGE</text>')
out.append('<text x="80" y="1140" font-family="Helvetica Neue, Arial, sans-serif" font-size="13" letter-spacing="3" fill="#a3a3a3">ISOMETRIC SET-UP · NOT TO SCALE FOR CONSTRUCTION</text>')
out.append('</svg>')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stage-isometric.svg'), 'w').write('\n'.join(out))

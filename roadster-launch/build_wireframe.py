import math
W, H = 1720, 1180
GY = 620          # ground line (elevation)
M = 20            # px per metre
X0 = 1300         # x of ramp vertical tangent
def px(X): return X0 + M*X
def py(Y): return GY - M*Y

def bez(p0,p1,p2,p3,t):
    u=1-t
    return tuple(u**3*a+3*u*u*t*b+3*u*t*t*c+t**3*d for a,b,c,d in zip(p0,p1,p2,p3))
OUTER = [((1120,620),(1225,612),(1320,530),(1320,420)),
         ((1320,420),(1320,245),(1180,130),(980,130))]
pts=[bez(*seg,i/400) for seg in OUTER for i in range(401)]
def outer_x_at_y(y):
    best=min(pts,key=lambda p:abs(p[1]-y)+(0 if p[0]>1200 else 1e3)); return best[0]
def outer_y_at_x(x):
    cand=[p for p in pts if p[1]<300]; return min(cand,key=lambda p:abs(p[0]-x))[1]

o=[]
a=o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">')
a('''<defs>
<pattern id="g1" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#1d3a5f" stroke-width="0.5"/></pattern>
<pattern id="g5" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" fill="none" stroke="#28507f" stroke-width="0.8"/></pattern>
<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#9fc3ea"/></marker>
<marker id="tr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10z" fill="#ffb547"/></marker>
<style>
.ln{fill:none;stroke:#cfe3ff;stroke-width:1.6}
.thin{fill:none;stroke:#9fc3ea;stroke-width:0.9}
.truss{fill:none;stroke:#7fa6d4;stroke-width:1}
.dim{fill:none;stroke:#9fc3ea;stroke-width:0.8}
.led{fill:none;stroke:#ff3b3b;stroke-width:3}
.traj{fill:none;stroke:#ffb547;stroke-width:2;stroke-dasharray:8 6}
.t{fill:#cfe3ff;font-size:13px}
.s{fill:#8fb2db;font-size:11px}
.h{fill:#ffffff;font-size:15px;font-weight:700;letter-spacing:2px}
.n{fill:#0b1a2e;font-size:12px;font-weight:700}
</style></defs>''')
a(f'<rect width="{W}" height="{H}" fill="#0b1a2e"/>')
a(f'<rect x="40" y="40" width="{W-80}" height="{GY-40+40}" fill="url(#g1)"/><rect x="40" y="40" width="{W-80}" height="{GY-40+40}" fill="url(#g5)"/>')
a(f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#3d6797" stroke-width="1.5"/>')

# --- Title block
a('<text x="60" y="80" class="h">TESLA ROADSTER LAUNCH — STAGE WIREFRAME</text>')
a('<text x="60" y="102" class="s">SIDE ELEVATION + PLAN · 1 small grid square = 1 m · all dimensions estimated from reference photos</text>')

# --- Ground & runway (elevation)
a(f'<line x1="40" y1="{GY}" x2="{W-40}" y2="{GY}" class="ln" stroke-width="2"/>')
for x in range(40,W-40,14): a(f'<line x1="{x}" y1="{GY+1}" x2="{x-8}" y2="{GY+9}" class="thin" stroke-opacity=".4"/>')
a(f'<line x1="100" y1="{GY-2}" x2="1100" y2="{GY-2}" class="led"/>')

# --- Ramp
a('<path class="ln" stroke-width="2.2" fill="#12345a" fill-opacity=".55" d="M1100 620 C1210 620 1300 530 1300 420 C1300 260 1170 150 980 150 L980 130 C1180 130 1320 245 1320 420 C1320 530 1225 612 1120 620 Z"/>')
# LED edge on ramp riding surface
a('<path class="led" stroke-width="2" d="M1100 618 C1208 618 1298 530 1298 420 C1298 262 1170 152 982 152"/>')

# --- Tower mast (x 1340..1400, y 98..620)
mx1,mx2,top=1340,1400,98
a(f'<rect x="{mx1}" y="{top}" width="{mx2-mx1}" height="{GY-top}" class="ln"/>')
y=GY; flip=0
while y>top+30:
    a(f'<line x1="{mx1}" y1="{y}" x2="{mx2}" y2="{y}" class="truss"/>')
    a(f'<line x1="{mx1 if flip else mx2}" y1="{y}" x2="{mx2 if flip else mx1}" y2="{y-30}" class="truss"/>')
    y-=30; flip^=1
# Top gantry beam (x 1000..1400, y 98..128)
a(f'<rect x="1000" y="{top}" width="{mx2-1000}" height="30" class="ln"/>')
x=1000; flip=0
while x<mx1:
    a(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{top+30}" class="truss"/>')
    a(f'<line x1="{x}" y1="{top if flip else top+30}" x2="{x+30}" y2="{top+30 if flip else top}" class="truss"/>')
    x+=30; flip^=1
# struts ramp -> mast
for yy in (560,500,440,380,320,260,200):
    xo=outer_x_at_y(yy); a(f'<line x1="{xo:.1f}" y1="{yy}" x2="{mx1}" y2="{yy}" class="truss"/>')
for yy1,yy2 in ((560,500),(440,380),(320,260)):
    a(f'<line x1="{outer_x_at_y(yy1):.1f}" y1="{yy1}" x2="{mx1}" y2="{yy2}" class="truss"/>')
# hangers beam -> ramp back
for xx in (1030,1090,1150,1210,1260):
    a(f'<line x1="{xx}" y1="128" x2="{xx}" y2="{outer_y_at_x(xx):.1f}" class="truss"/>')
# base braces + guy cable
a(f'<line x1="{mx2}" y1="470" x2="1460" y2="{GY}" class="truss"/><line x1="{mx2}" y1="{GY}" x2="1460" y2="{GY}" class="truss"/>')
a(f'<line x1="{mx2}" y1="{top}" x2="1520" y2="{GY}" class="thin" stroke-dasharray="3 3"/>')
a(f'<rect x="1512" y="{GY-6}" width="16" height="6" class="ln"/>')
# gantry lights / cameras
for xx in (1040,1120,1200):
    a(f'<rect x="{xx-6}" y="88" width="12" height="10" class="thin"/>')
# floodlights
def flood(x,y,dirx):
    a(f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" fill-opacity=".9"/>')
    for ang in (-25,-10,5):
        r=math.radians(ang); a(f'<line x1="{x}" y1="{y}" x2="{x+dirx*60*math.cos(r):.1f}" y2="{y+60*math.sin(r)-20:.1f}" class="thin" stroke-opacity=".5"/>')
flood(560,GY-10,1); flood(1180,GY-10,-1); flood(70,GY-12,1)
# camera dolly
a(f'<rect x="590" y="{GY-14}" width="30" height="10" class="ln"/><circle cx="596" cy="{GY-3}" r="3" class="ln"/><circle cx="614" cy="{GY-3}" r="3" class="ln"/><line x1="605" y1="{GY-14}" x2="605" y2="{GY-30}" class="ln"/><rect x="598" y="{GY-38}" width="14" height="8" class="ln"/>')

# --- Trajectory
a('<path class="traj" d="M200 606 L1100 606 C1202 606 1286 530 1286 420 C1286 270 1168 164 980 164 C860 164 760 210 700 290" marker-end="url(#tr)"/>')

# --- Car silhouettes
CAR='M-43 0 L-43 -8 Q-40 -13 -30 -14 L-12 -15 Q-2 -24 10 -23 Q25 -20 35 -12 Q43 -10 43 -6 L43 0 Z'
def car(x,y,rot,thr=False):
    g=f'<g transform="translate({x} {y}) rotate({rot})">'
    if thr:
        for tx in (-28,0,28):
            g+=f'<path d="M{tx-5} 2 L{tx+5} 2 L{tx+9} 70 L{tx-9} 70 Z" fill="#9fc3ea" fill-opacity=".25" stroke="#9fc3ea" stroke-width=".8" stroke-dasharray="2 3"/>'
    g+=f'<path d="{CAR}" fill="#0b1a2e" stroke="#ffffff" stroke-width="1.6"/>'
    g+='<circle cx="-27" cy="0" r="6" fill="#0b1a2e" stroke="#fff" stroke-width="1.4"/><circle cx="27" cy="0" r="6" fill="#0b1a2e" stroke="#fff" stroke-width="1.4"/></g>'
    a(g)
car(300,GY-6,0); car(1294,440,-90); car(1080,156,180); car(640,330,0,thr=True)

# phase markers
def mark(n,x,y,lbl,anchor='start',dx=14):
    a(f'<circle cx="{x}" cy="{y}" r="10" fill="#ffb547"/><text x="{x}" y="{y+4}" text-anchor="middle" class="n">{n}</text>')
    a(f'<text x="{x+(dx if anchor=="start" else -dx)}" y="{y+4}" text-anchor="{anchor}" class="t">{lbl}</text>')
mark(1,300,560,'Accelerate on approach runway')
mark(2,1150,560,'Transition', 'end')
mark(3,1250,330,'Vertical climb', 'end')
mark(4,1010,235,'Inverted · exit lip', 'end')
mark(5,600,430,'Thrusters fire · controlled hover', 'start')

# --- Labels w/ leaders
def lab(x1,y1,x2,y2,txt,anchor='start',sub=None):
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="dim"/><circle cx="{x1}" cy="{y1}" r="2.5" fill="#9fc3ea"/>')
    a(f'<text x="{x2+(6 if anchor=="start" else -6)}" y="{y2+4}" text-anchor="{anchor}" class="t">{txt}</text>')
    if sub: a(f'<text x="{x2+(6 if anchor=="start" else -6)}" y="{y2+19}" text-anchor="{anchor}" class="s">{sub}</text>')
lab(1370,98,1420,60,'Top gantry truss','start','lights + overhead cameras')
lab(1400,180,1450,180,'Steel truss mast','start','~3 m square section')
lab(1460,360,1490,330,'Guy cable / backstay','start')
lab(1323,470,1450,450,'Ramp deck (concrete-look)','start','two white lane lines')
lab(980,140,900,140,'Launch lip','end','overhangs runway')
lab(560,GY-10,520,GY-35,'Floodlight','end')
lab(612,GY-34,680,GY-48,'Camera dolly','start')
lab(800,GY-2,800,GY-30,'Red LED edge strip','start')

# --- Dimensions
def vdim(x,y1,y2,txt):
    a(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="dim" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    a(f'<text transform="translate({x-6} {(y1+y2)/2}) rotate(-90)" text-anchor="middle" class="s">{txt}</text>')
def hdim(y,x1,x2,txt):
    a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="dim" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    a(f'<text x="{(x1+x2)/2}" y="{y-5}" text-anchor="middle" class="s">{txt}</text>')
vdim(940,GY,150,'lip ≈ 23.5 m'); a('<line x1="934" y1="150" x2="980" y2="150" class="dim" stroke-dasharray="2 3"/>')
vdim(1670,GY,98,'tower ≈ 26 m'); a('<line x1="1400" y1="98" x2="1676" y2="98" class="dim" stroke-dasharray="2 3"/>')
vdim(1230,GY,420,'≈ 10 m'); a('<line x1="1224" y1="420" x2="1300" y2="420" class="dim" stroke-dasharray="2 3"/>')
hdim(70,980,1320,'ramp reach ≈ 17 m'); a('<line x1="980" y1="64" x2="980" y2="128" class="dim" stroke-dasharray="2 3"/><line x1="1320" y1="64" x2="1320" y2="420" class="dim" stroke-dasharray="2 3"/>')
hdim(655,1100,1300,'transition ≈ 10 m')
hdim(655,100,1100,'approach runway — 50 m shown (full length TBD)')
a(f'<text x="60" y="{GY+50}" class="h" font-size="13">SIDE ELEVATION</text>')

# --- PLAN VIEW
PY=760
a(f'<text x="60" y="{PY-12}" class="h" font-size="13">PLAN VIEW</text>')
c=870
a(f'<rect x="100" y="{c-80}" width="1000" height="160" class="ln" fill="#12345a" fill-opacity=".3"/>')
a(f'<line x1="100" y1="{c-78}" x2="1100" y2="{c-78}" class="led"/><line x1="100" y1="{c+78}" x2="1100" y2="{c+78}" class="led"/>')
a(f'<line x1="100" y1="{c}" x2="1100" y2="{c}" class="thin" stroke-dasharray="14 10" stroke-opacity=".6"/>')
a(f'<rect x="980" y="{c-60}" width="340" height="120" class="ln" fill="#12345a" fill-opacity=".6"/>')
a(f'<line x1="980" y1="{c-20}" x2="1320" y2="{c-20}" class="thin"/><line x1="980" y1="{c+20}" x2="1320" y2="{c+20}" class="thin"/>')
a(f'<line x1="1100" y1="{c-60}" x2="1100" y2="{c+60}" class="thin" stroke-dasharray="4 4"/><line x1="1300" y1="{c-60}" x2="1300" y2="{c+60}" class="thin" stroke-dasharray="4 4"/>')
a(f'<rect x="{mx1}" y="{c-70}" width="60" height="140" class="ln"/><line x1="{mx1}" y1="{c-70}" x2="{mx2}" y2="{c+70}" class="truss"/><line x1="{mx2}" y1="{c-70}" x2="{mx1}" y2="{c+70}" class="truss"/>')
for yy in (c-66,c+66): a(f'<line x1="1000" y1="{yy}" x2="{mx1}" y2="{yy}" class="truss" stroke-dasharray="6 4"/>')
a(f'<line x1="{mx2}" y1="{c}" x2="1520" y2="{c}" class="thin" stroke-dasharray="3 3"/><rect x="1512" y="{c-8}" width="16" height="16" class="ln"/>')
a(f'<g transform="translate(300 {c})"><rect x="-43" y="-19" width="86" height="38" rx="10" fill="#0b1a2e" stroke="#fff" stroke-width="1.6"/><path d="M-5 -15 Q15 0 -5 15" class="thin"/></g>')
a(f'<line x1="350" y1="{c}" x2="960" y2="{c}" class="traj" marker-end="url(#tr)"/>')
a(f'<line x1="100" y1="{c+105}" x2="1100" y2="{c+105}" class="thin" stroke-dasharray="10 5"/><rect x="590" y="{c+98}" width="30" height="14" class="ln"/>')
for xx in (70,560,1180): a(f'<circle cx="{xx}" cy="{c-100 if xx!=1180 else c+100}" r="6" fill="#fff" fill-opacity=".9"/>')
lab(980,c-60,940,c-110,'Ramp footprint (lip → back)','end')
lab(1100,c+60,1100,c+130,'ground entry','start')
lab(1370,c-70,1420,c-110,'Mast footprint','start')
lab(1170,c-66,1210,c-110,'Gantry truss (overhead)','start')
lab(1520,c,1540,c+50,'Cable anchor','end')
lab(700,c+105,720,c+130,'Camera dolly track','start')
vdim(80,c-80,c+80,'≈ 8 m'); vdim(1250,c-60,c+60,'≈ 6 m')
a(f'<line x1="1240" y1="{c-60}" x2="1256" y2="{c-60}" class="dim"/>')
hdim(c-95,980,1100,'overhang ≈ 6 m')

# --- Notes
NY=1030
a(f'<line x1="40" y1="{NY-20}" x2="{W-40}" y2="{NY-20}" class="thin" stroke-opacity=".5"/>')
a(f'<text x="60" y="{NY}" class="h" font-size="13">KEY NUMBERS FOR THE SIMULATION (estimates)</text>')
notes=['Car ≈ 4.3 m long · 1.9 m wide · ~2 t with thruster pack',
       'Ramp profile: ~10 m quarter-curve into vertical, then curls ~180° to an inverted lip at ≈ 23.5 m',
       'Top curl radius ≈ 8 m → needs v_top > √(g·r) ≈ 9 m/s to stay pressed to the deck',
       'Energy: v_entry ≳ √(v_top² + 2·g·23.5) ≈ 23 m/s (≈ 85 km/h) frictionless — plan ~110 km/h with losses']
for i,t in enumerate(notes): a(f'<text x="60" y="{NY+24+i*20}" class="t">• {t}</text>')
a(f'<text x="900" y="{NY}" class="h" font-size="13">LEGEND</text>')
leg=[('<line x1="0" y1="0" x2="40" y2="0" class="led"/>','Red LED edge lighting'),
     ('<line x1="0" y1="0" x2="40" y2="0" class="traj"/>','Car path'),
     ('<line x1="0" y1="0" x2="40" y2="0" class="truss"/>','Steel truss members'),
     ('<line x1="0" y1="0" x2="40" y2="0" class="thin" stroke-dasharray="3 3"/>','Cable / hidden / reference')]
for i,(s,t) in enumerate(leg):
    yy=NY+20+i*20
    a(f'<g transform="translate(900 {yy})">{s}</g><text x="950" y="{yy+4}" class="t">{t}</text>')
a(f'<text x="{W-60}" y="{H-36}" text-anchor="end" class="s">rev A · 2026-10-17 · wireframe for simulation set-up</text>')
a('</svg>')
open(__import__('os').path.join(__import__('os').path.dirname(__file__),'stage-wireframe.svg'),'w').write('\n'.join(o))

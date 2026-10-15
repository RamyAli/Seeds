import math
BACKR=150; CHESTR=95
def cc(p1,r1,p2,r2):
    # intersections of circles
    dx,dy=p2[0]-p1[0],p2[1]-p1[1]; d=math.hypot(dx,dy)
    a=(r1*r1-r2*r2+d*d)/(2*d); h=math.sqrt(max(r1*r1-a*a,0))
    mx,my=p1[0]+a*dx/d,p1[1]+a*dy/d
    return [(mx+h*dy/d,my-h*dx/d),(mx-h*dy/d,my+h*dx/d)]
def tpt(C,c,r):  # point where circle (c,r) internally touches big circle centred C
    dx,dy=c[0]-C[0],c[1]-C[1]; d=math.hypot(dx,dy)
    return (c[0]+r*dx/d, c[1]+r*dy/d)
def tp(P, c, r, side):
    dx,dy=c[0]-P[0],c[1]-P[1]; d=math.hypot(dx,dy); th=math.atan2(dy,dx); a=math.asin(r/d)
    t=th+side*a; L=math.sqrt(d*d-r*r)
    return (P[0]+math.cos(t)*L, P[1]+math.sin(t)*L)
def f(p): return f"{p[0]:.2f} {p[1]:.2f}"
def bird(H,rh,B,rb,T):
    # back: arc radius BACKR through T, internally tangent to head; centre to the lower-right
    Cb=max(cc(H,BACKR-rh,T,BACKR),key=lambda p:p[0]+p[1])
    back=tpt(Cb,H,rh)
    # chest: arc radius CHESTR tangent to head and body; centre to the left
    Cc=min(cc(H,CHESTR-rh,B,CHESTR-rb),key=lambda p:p[0])
    h1=tpt(Cc,H,rh); b1=tpt(Cc,B,rb)
    belly=max((tp(T,B,rb,1),tp(T,B,rb,-1)),key=lambda p:p[1])
    return (f"M{f(T)} A{BACKR} {BACKR} 0 0 1 {f(back)} A{rh} {rh} 0 0 1 {f(h1)} "
            f"A{CHESTR} {CHESTR} 0 0 1 {f(b1)} A{rb} {rb} 0 0 1 {f(belly)} Z")

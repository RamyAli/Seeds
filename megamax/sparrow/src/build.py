import json, sys
sys.path.insert(0,'.')
from gen import bird
from txt import text_path
P=json.load(open('p.json'))
GREEN='#004E3C'; INK='#1C1C1C'
def mask_body(uid):
    H,rh,B,rb,T=P['H'],P['rh'],P['B'],P['rb'],P['T']; g=6; k=P['k']
    shapes=f'<path d="{bird(H,rh,B,rb,T)}"/><path d="{P["beak"]}"/><path d="{P["tail"]}"/>'
    bc,br,bw=P['branch']; e=P['eye']
    return f'''<mask id="{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200"><rect width="200" height="200" fill="#fff"/><circle cx="{bc[0]}" cy="{bc[1]}" r="{br}" fill="none" stroke="#000" stroke-width="{bw}"/><g transform="{P['tf']}"><g fill="#fff" stroke="#fff" stroke-width="{2*g/k:.3f}" stroke-linejoin="round">{shapes}</g><g fill="#000">{shapes}</g><path d="{P['wing']}" fill="none" stroke="#fff" stroke-width="{g/k:.3f}"/><circle cx="{e[0]}" cy="{e[1]}" r="{e[2]}" fill="#fff"/></g></mask>'''
def mark_group(uid, fill, x=0, y=0, s=1):
    return f'<defs>{mask_body(uid)}</defs><g transform="translate({x} {y}) scale({s})"><circle cx="100" cy="100" r="96" fill="{fill}" mask="url(#{uid})"/></g>'
def svg(w,h,body,vb=None):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb or f"0 0 {w} {h}"}" width="{w}" height="{h}">{body}</svg>'
M800='fonts/m800.ttf'; M600='fonts/m600.ttf'
def words(x, base, size, col, subcol, align='left'):
    d1,w1=text_path('MEGAMAX',M800,size,0,0,track=20)
    sub_size=size*0.262
    # subline tracked to same width as MEGAMAX
    _,w0=text_path('INTERNATIONAL TRADING',M600,sub_size,0,0,0)
    tr=(w1-w0)/(len('INTERNATIONAL TRADING')-1)/sub_size*1000
    d2,w2=text_path('INTERNATIONAL TRADING',M600,sub_size,0,0,tr)
    ox = x if align=='left' else x-w1/2
    return (f'<path transform="translate({ox:.2f} {base})" d="{d1}" fill="{col}"/>'
            f'<path transform="translate({ox:.2f} {base+size*0.52:.2f})" d="{d2}" fill="{subcol}"/>'), w1
out={}
out['mark']=svg(200,200,mark_group('a',GREEN))
out['mark-white']=svg(200,200,mark_group('a','#FFFFFF'))
# horizontal: mark height 200 → text cap height ≈ mark*0.36
t,w=words(236,118,84,INK,GREEN); W=int(236+w+12)
out['horizontal']=svg(W,200,mark_group('a',GREEN)+t)
t,w=words(236,118,84,'#FFFFFF','#9FD3B5'); out['horizontal-reverse']=svg(W,200,mark_group('a','#FFFFFF')+t)
# stacked
t,w=words(0,296,84,INK,GREEN,'center'); SW=int(w+16)
t,w=words(SW/2,296,84,INK,GREEN,'center')
out["stacked"]=svg(SW,350,mark_group('a',GREEN,SW/2-100,0)+t)
import os; os.makedirs('out',exist_ok=True)
for k,v in out.items(): open(f'out/megamax-sparrow-{k}.svg','w').write(v)
print(list(out))

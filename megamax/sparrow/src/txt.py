from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
_c={}
def text_path(s, font, size, x, y, track=0):
    """Outline text; baseline at y; track in em/1000. Returns (d, width)."""
    if font not in _c: _c[font]=TTFont(font)
    t=_c[font]; gs=t.getGlyphSet(); cmap=t.getBestCmap(); upm=t['head'].unitsPerEm; k=size/upm
    pen=SVGPathPen(gs); cx=0; n=len(s)
    for i,ch in enumerate(s):
        g=cmap[ord(ch)]
        gs[g].draw(TransformPen(pen,(k,0,0,-k,x+cx,y)))
        cx+=gs[g].width*k + (track*size/1000 if i<n-1 else 0)
    return pen.getCommands(), cx

#!/usr/bin/env python3
"""Apply the Muralha stage-footer geometry fix to the existing index.html.
Run from the repository root: python3 tools/fix_muralha_footer.py
Does not publish or trigger the iPhone workflow.
"""
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "index.html"
text = path.read_text(encoding="utf-8")
before = """tx((en?'Stage ':'Fase ')+n,[302,1650,150,40],1,32,'#512014');tx((en?'Suggested level ':'Nível sugerido ')+rec,[292,1688,162,26],1,19,'#512014');tx((en?'Your team: ':'Seu time: ')+avg,[292,1712,162,26],1,19,avg>=rec?'#1f6a2a':'#a8261c');"""
after = """/* Alinhamento 18nov: textos em x=310..488, após a miniatura (x=206..300), antes do ícone de informações. */const footX=310,footW=178;tx((en?'Stage ':'Fase ')+n,[footX,1653,footW,31],1,29,'#512014');tx((en?'Suggested level ':'Nível sugerido ')+rec,[footX,1685,footW,25],1,19,'#512014');tx((en?'Your team: ':'Seu time: ')+avg,[footX,1711,footW,25],1,19,avg>=rec?'#1f6a2a':'#a8261c');"""
if text.count(before) != 1:
    if after in text:
        print("Already applied; nothing changed.")
        raise SystemExit(0)
    raise SystemExit("Original footer not found exactly once; no changes made.")
# Geometry assertions against thumbnail, play button and panel.
rects = [(310,1653,178,31),(310,1685,178,25),(310,1711,178,25)]
panel,thumbnail,play=(172,1644,548,100),(206,1654,94,74),(540,1609,164,161)
def overlaps(a,b):
    return max(a[0],b[0])<min(a[0]+a[2],b[0]+b[2]) and max(a[1],b[1])<min(a[1]+a[3],b[1]+b[3])
for i,rect in enumerate(rects):
    assert panel[0] <= rect[0] and panel[1] <= rect[1]
    assert rect[0]+rect[2] <= panel[0]+panel[2] and rect[1]+rect[3] <= panel[1]+panel[3]
    assert not overlaps(rect,thumbnail) and not overlaps(rect,play)
    assert not any(overlaps(rect,other) for j,other in enumerate(rects) if j != i)
path.write_text(text.replace(before,after),encoding="utf-8")
print("Patched index.html (without altering images or animations).")

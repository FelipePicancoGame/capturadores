import json,pytesseract,re
from PIL import Image,ImageOps
U=json.load(open('et2/uik.json'));M=json.load(open('et2/map2.json'))
done={(v['kit'],v['part']) for v in M.values()}|{('loja','preco_max')}
out=[]
for k,v in U.items():
  p=v['a'].split('?')[0];
  try: A=Image.open('app/'+p if not p.startswith('/') else 'app'+p).convert('RGB')
  except Exception as e: print('x',k,e);continue
  for part,r in v['fr'].items():
    if (k,part) in done: continue
    c=A.crop((r[0],r[1],r[0]+r[2],r[1]+r[3]))
    if c.width<60 or c.height<20: continue
    sc=max(1,int(600/max(c.width,1)))
    big=c.resize((c.width*sc,c.height*sc))
    best=''
    for im in (big,ImageOps.invert(big)):
      t=pytesseract.image_to_string(ImageOps.grayscale(im),lang='eng',config='--psm 6')
      w=[x for x in re.findall(r'[A-Za-zÀ-ú]{3,}',t)]
      if len(' '.join(w))>len(best): best=' '.join(w)
    if best: out.append((k,part,r[2],r[3],best[:80]));print(k,part,best[:80])
json.dump(out,open('et2/ocr.json','w'),ensure_ascii=False,indent=0)

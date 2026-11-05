#!/usr/bin/env python3
"""OTIMIZA05NOV (Felipe: 'executa essas otimizações'): tira as imagens base64 de dentro do index.html
e salva em blobs/<md5>.<ext> (mesmos bytes, sem perder qualidade). Pode rodar de novo quantas vezes quiser.
Uso: python3 tools/extrai_base64.py index.html [minimo_em_caracteres=4000]"""
import re,sys,base64,hashlib,os
f=sys.argv[1];MIN=int(sys.argv[2]) if len(sys.argv)>2 else 4000
root=os.path.dirname(os.path.abspath(f));s=open(f,encoding='utf-8').read()
EXT={'png':'png','webp':'webp','jpeg':'jpg','jpg':'jpg','gif':'gif','svg+xml':'svg'}
n=0;saved=0
def rep(m):
    global n,saved
    lit=m.group(0)
    if len(lit)<MIN:return lit
    mime=m.group(1);ext=EXT.get(mime)
    if not ext:return lit
    try:b=base64.b64decode(m.group(2),validate=True)
    except Exception:return lit
    h=hashlib.md5(b).hexdigest();p=f'blobs/{h}.{ext}';fp=os.path.join(root,p)
    if not os.path.exists(fp):open(fp,'wb').write(b)
    n+=1;saved+=len(lit)-len(p);return p
s2=re.sub(r'data:image/([a-z+]+);base64,([A-Za-z0-9+/]+=*)',rep,s)
open(f,'w',encoding='utf-8').write(s2);print(f'{n} imagens tiradas, {saved/1e6:.1f} MB a menos; agora {len(s2)/1e6:.1f} MB')

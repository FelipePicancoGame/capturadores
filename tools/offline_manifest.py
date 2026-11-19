# OFFLINE18NOV: lista completa do que o jogo usa (pro "Jogar offline" só dizer pronto quando tudo estiver baixado).
# 1) caminhos escritos no index.html  2) blobs citados só pelo nome  3) arquivos das pastas que o jogo monta o nome na hora (ex.: 'assets/cfg13/'+k+'.webp')
import re,os,json
os.chdir(os.path.join(os.path.dirname(__file__),'..'))
s=open('index.html').read()
EXT=('.webp','.png','.jpg','.jpeg','.mp3','.ogg','.m4a','.wav','.json','.gif','.woff','.woff2','.ttf','.otf')
re1=re.compile(r'(?:\./)?((?:assets|blobs)/[A-Za-z0-9_/.%-]+\.(?:webp|png|jpg|jpeg|mp3|ogg|m4a|wav|json|gif|woff2?|ttf|otf))')
out=set(p for p in re1.findall(s) if os.path.isfile(p))
for r,_,fs in os.walk('blobs'):
  for f in fs:
    p=os.path.join(r,f)
    if f.endswith(EXT) and os.path.splitext(f)[0] in s: out.add(p)
for r,_,fs in os.walk('assets'):
  if (r+'/') in s:
    for f in fs:
      if f.endswith(EXT): out.add(os.path.join(r,f))
json.dump(sorted(out),open('offline.json','w'),separators=(',',':'))
print('offline.json',len(out),'arquivos',round(sum(os.path.getsize(p) for p in out)/1e6),'MB')

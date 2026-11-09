import re,json,sys
s=open(sys.argv[1]).read()
# só código (sem blobs base64 longos)
PT=re.compile(r"[ãõçáéíóúâêôàÃÕÇÁÉÍÓÚÂÊÔ]|\b(você|não|com|pra|para|uma|seu|sua|dos|das|toque|jogar|voltar|escolher|vida|fase|onda|ganhe|ganhou|cartas?|monstrinhos?|nível|melhor|pegar|agora|aqui|todos|cada|quando|mais|menos|está|isso|esse|essa|também|ainda|já|vez|dia|hoje|moedas|cristais|loja|sair|fechar|abrir|novo|nova|perdeu|venceu)\b",re.I)
out=set()
for m in re.finditer(r"'((?:[^'\\\n]|\\.){3,200})'",s):
  t=m.group(1)
  if '${' in t or 'data:' in t or '/_blob' in t or 'blobs/' in t: continue
  if re.search(r'[{}();=<>]',t) : continue
  if PT.search(t): out.add(t.replace("\\'","'"))
for m in re.finditer(r'"((?:[^"\\\n]|\\.){3,200})"',s):
  t=m.group(1)
  if re.search(r'[{}();=<>]',t) or 'data:' in t: continue
  if PT.search(t) and not s[m.end():m.end()+9].startswith(':"blobs/') and not s[m.end():m.end()+10].startswith(': "blobs/'): out.add(t.replace('\\"','"'))
json.dump(sorted(out),open(sys.argv[2],'w'),ensure_ascii=False)
print(len(out))

# Gera audit.html = index.html + gancho window.__X(codigo) para testes com Playwright. Só local; NÃO commitar audit.html.
import pathlib
raiz=pathlib.Path(__file__).resolve().parent.parent
s=(raiz/'index.html').read_text(encoding='utf-8');k='window.__T={MONANIM,'
assert k in s,'marcador nao achado'
(raiz/'audit.html').write_text(s.replace(k,'window.__X=function(c){return eval(c)};'+k,1),encoding='utf-8')
print('ok: audit.html')

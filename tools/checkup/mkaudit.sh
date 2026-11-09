#!/bin/sh
# gera app/audit.html (index.html + __X) — NUNCA commitar
cd "$(dirname "$0")/app" && python3 -c "
s=open('index.html').read();k='window.__T={MONANIM,';assert k in s
open('audit.html','w').write(s.replace(k,'window.__X=function(c){return eval(c)};'+k,1))"

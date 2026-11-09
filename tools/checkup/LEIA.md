# Check-up geral (PT e EN)
1. Copie o repositório e um salvo cheio para `audit/save2.txt` (pasta acima de `checkup/`).
2. Gere `audit.html` = index.html com `window.__X=function(c){return eval(c)};` antes de `window.__T={MONANIM,` e rode `node srvgz.js` (porta 8790).
3. `node checkup.js <pt|en> menus` e cada grupo `play_*` de steps.json → fotos em `out/<lang>/`, textos em `out/<lang>_<grupo>.json`.
4. Frases sem tradução: `lits.py` + `trcheck.js` (literais), `tpl.js` (frases com números), `gscan2.js` (listas do jogo). Arte com palavra: `ocr.py`.

# Check-up geral (PT e EN)
1. Copie o repositório e um salvo cheio para `audit/save2.txt` (pasta acima de `checkup/`).
2. Gere `audit.html` = index.html com `window.__X=function(c){return eval(c)};` antes de `window.__T={MONANIM,` e rode `node srvgz.js` (porta 8790).
3. `node checkup.js <pt|en> menus` e cada grupo `play_*` de steps.json → fotos em `out/<lang>/`, textos em `out/<lang>_<grupo>.json`.
4. Frases sem tradução: `lits.py` + `trcheck.js` (literais), `tpl.js` (frases com números), `gscan2.js` (listas do jogo). Arte com palavra: `ocr.py`.

## Novidades 09/nov
- `probe.js`: `VW=393 VH=793 node probe.js <pt|en> passos.json` — passos `[[nome,código,espera]]`, nome com `_` não tira foto; fotos em out/probe.
- `mkaudit.sh`: monta o audit.html (nunca commitar).
- Ordem do check-up: reports do dia → artes do Drive do dia → alinhamentos → telas PT/EN → relatório (ver claude/CHECKUP_GERAL_LISTA.md no projeto).

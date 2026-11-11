# Tarefa para o Codex — medir XP por minuto de cada modo do jogo

Jogo: `index.html` (um arquivo só, JavaScript). Não altere o `index.html` nem nada fora da pasta `robos/`.

## Objetivo
Medir, jogando com um robô no código real do jogo, **quanta XP o time ganha por minuto de jogo** em cada modo:
Muralha (`wallMode`), Torres (`towerMode`), Horda (`survMode`), Arena (`arenaStage`), Combina (`m3New`), Expedição (`expMode` ou equivalente) e batalha no mapa (luta contra selvagem).

## Como montar
1. Copie `index.html` para `robos/audit.html` e, logo antes do texto `window.__T={MONANIM,`, insira:
   `window.__X=function(c){return eval(c)};`
   (isso deixa o robô executar código dentro do jogo; NUNCA commite o audit.html).
2. Sirva a pasta com `python3 -m http.server 8790` e abra com Playwright (Chromium, viewport 390x844).
3. Bloqueie `https://script.google.com/**` (responda `{"ok":1}`) e arquivos `.mp3/.ogg/.wav` (404).
4. Antes de cada partida, dentro do jogo:
   - `say=async()=>{};fadeTo=async()=>{};bioTipShow=async()=>{};saveGame=()=>{};`
   - `flags.tut={world:1,battle:1,wall:1,surv:1,td:1,exp:1,match:1,arena:1};`
   - `mgCap=()=>50;` (tira o limite da história, para medir a XP pura)
   - time: `party.length=0; for(const sp of ['fagulho','brotim','marolo','pedrisco']) party.push(mk(sp, NIVEL));`
   - fase: `STG={mode:'<wall|td|surv|arena>', i:FASE-1, bio:murBioI(FASE-1), mult:.85+Math.min(FASE-1,15)*.1+Math.max(0,FASE-1-15)*.06};`
5. Rode o jogo chamando `update()` em laço (60 chamadas = 1 segundo de jogo). Limpe `ui.length=0` quando aparecer janela. Faça o robô jogar de forma razoável (escolher carta, construir torre, desviar na Horda etc.).
6. Meça para cada partida:
   - `xp` = soma de `m.xp` dos 4 monstrinhos depois − antes
   - `seg` = número de `update()` / 60
   - `venceu` (sim/não)
   - `xpMin` = xp / (seg/60)

## Pontos a medir
- Fases 5, 10, 20, 30. Nível do time = régua da fase (`stgRuler(FASE-1)`) e régua+4.
- 3 partidas por ponto. Mapa: 10 lutas contra selvagem do nível da régua (só o monstrinho que luta ganha XP — anote também por monstrinho).

## Entrega
Arquivo `robos/RESULTADO_XP.md` com uma tabela: modo | fase | nível | xp por partida | segundos | xp por minuto | vitórias.
E os robôs que você escreveu dentro de `robos/` (sem o audit.html).

Observação: o Combina hoje não dá XP (só moedas) — confirme. A Arena talvez também não dê — confirme.

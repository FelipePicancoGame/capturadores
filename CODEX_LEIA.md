# CÓPIA DE TESTE — Arena (para o ChatGPT/Codex)

**Esta branch NÃO é o jogo oficial.** Não faça merge na `main`, não faça push na `main`, não mude GitHub Pages, não rode os workflows do `.github/` (TestFlight/App Store) e não toque em save real de jogador.

## 1. Base
- Repositório: `https://github.com/FelipePicancoGame/capturadores` (público)
- Branch de teste: **`codex-arena-teste`**
- Base: `main` na versão **cv-v679**, commit **`f324f54`** ("Torres: balao do tutorial menor…").
- Commit de preparação da cópia (isolamento + dados de teste): o primeiro commit desta branch depois do `f324f54`.
- A `main` é o jogo oficial (GitHub Pages publica a `main`). Nada nesta branch é publicado.

## 2. Pasta e como rodar
```bash
git clone -b codex-arena-teste https://github.com/FelipePicancoGame/capturadores.git capturadores-teste
cd capturadores-teste
python3 -m http.server 8790          # ou: npx http-server -p 8790 -c-1
```
- Jogo: http://localhost:8790/index.html
- Com gancho de teste (`window.__X(código)` para Playwright): `python3 teste-codex/mkaudit.py` → http://localhost:8790/audit.html (não commitar `audit.html`; está no `.gitignore`).
- Teste rápido: `npm i playwright && npx playwright install chromium && node teste-codex/smoke.js` (abre em 375×667, carrega o save de teste, entra na Arena e salva `teste-codex/smoke_arena.png`).
- Preview hospedado (só leitura, da branch): https://raw.githack.com/FelipePicancoGame/capturadores/codex-arena-teste/index.html — o raw.githack às vezes demora para atualizar depois de um push; o confiável é o localhost.
- O repositório tem ~800 MB de arte (`blobs/`, `assets/`). Clone raso ajuda: `git clone --depth 1 -b codex-arena-teste …`.

## 3. Isolamento (bloco `COPIA_TESTE_CODEX` no topo do `index.html`)
- Todo `localStorage`/`sessionStorage` recebe o prefixo `TESTE_CODEX::`. A chave oficial `capturadores-vale-v1` nunca é lida nem escrita, mesmo na mesma origem.
- Service worker desligado (não registra e não usa Cache Storage).
- Rede de dados desligada: Google Apps Script (jogadores, reports, presentes, dupla) e Supabase (FPimpulse) recebem resposta falsa `{"ok":1}`. Nada chega à planilha real.
- Faixa vermelha "CÓPIA DE TESTE" no topo.
- **Esse bloco nunca pode ir para a `main`.**

## 4. Dados de teste
- `teste-codex/save_teste.json`: time de 5 monstrinhos, tutoriais vistos, id de jogador falso 999001.
- Carrega sozinho na primeira abertura. `?reset=1` na URL apaga e recarrega o save de teste.
- Em script Playwright, grave save com a chave `TESTE_CODEX::capturadores-vale-v1` (ou use `?reset=1`).
- Entrar numa fase da Arena pelo console (audit.html), depois de tocar CONTINUAR na tela inicial:
  `__X("ui.length=0,STG={mode:'arena',i:0,bio:BIOMES[0],mult:.85},arenaStage()")`
- Atalhos úteis: `AR` (estado da partida), `arUpdate()`, `arEnd('win')`, `arStgEnd(why)`.

## 5. Problemas a corrigir — conferidos no cv-v679 (antes de mexer)
O relatório da auditoria cv-v670 **não foi encontrado** no projeto nem no Drive. Os itens abaixo foram conferidos direto no código:

1. **Estrelas com vida extra — EXISTE.** O bloco `ARENAAD18NOV` (perto do fim do script principal) embrulha `arUpdate` e, durante a proteção (`A.prot>0`), põe `A.lives=L+99`. Se a última onda termina nesse quadro, `arStgEnd` calcula `stars=win?Math.max(1,A.lives):0` → até 100 estrelas. Regra pedida: **vitória com a vida extra (`A.vidaUsou`) = 1 estrela; nenhum resultado acima de 3.** Conferir também onde as estrelas são gravadas no progresso (`flags`/mapa de fases).
2. **Veneno fora da estatística — EXISTE.** O tique do veneno em `arUpdate` faz `e.hp-=e.poison` direto, sem passar por `arHit`/`arConta` (bloco `DANOCONTA18NOV`). Também ver `arPoison` (habilidades com `veneno:[f,dur,max]`, acúmulo e `area`/`praga`, ~bloco de habilidades da Arena). Corrigir total (`A.dmgT`) e autoria (`A.dmgBy[sp]`), incluindo acúmulos e propagação.
3. **Enxame sem autor — EXISTE (provável).** O wrapper de `arFire` do Zumbitron (`enxame:[6,.45,2]`) chama `arHit` direto, fora de onde `AR_CUR` é definido; o dano entra em `A.dmgT` sem `src`. Confirmar com teste e atribuir ao monstrinho que disparou.
4. **Título do andar cortado em 375×667 — NÃO REPRODUZIDO por mim.** Reproduzir antes de corrigir (retorno automático da Arena para o mapa das Masmorras/andares).

## 6. Mudanças recentes na Arena (podem afetar os testes)
- cv-v670–674: mais inimigos por onda (`ARNK=4`), vida ajustada (`ARHK`, `arHkOnda`, "RAMPA19NOV"), custo de chamar sobe +5 (`ARCUSTO`), inimigos pequenos em grupo e grandes espalhados (`TAMANHOS20NOV`, `arGapSpawn`), sem limite de tamanho para não-chefe.
- cv-v678: selo colorido "N★" nas peças (`ESTRELAS20NOV`), "+30% PODER" ao tocar a carta (`PODER20NOV`), herói brilhando com a magia carregada (`MAGIA20NOV`), música para durante o anúncio (`ANUNCIOMUSICA20NOV`).
- `DANOCONTA18NOV` (18/nov) já unificou a conta de dano em `arConta`; queimadura e poça passaram a contar. Veneno e enxame ficaram de fora.
- Nenhuma dessas mudanças corrige os 4 problemas acima.

## 7. Decisões do projeto (não mudar)
- Jogo de celular em retrato. Não criar modo paisagem.
- Sem escolha de cartas durante as ondas; cartas/fragmentos só no final.
- Ajudas opcionais (exercício de 30 s) podem melhorar recompensas ou dar vida extra.
- Não mudar dificuldade, economia ou progressão além do necessário para corrigir os defeitos. Se precisar, escreva a proposta primeiro.
- Cada mudança no código leva um comentário com marcador (ex.: `/* ESTRELASVIDA_CODEX */`) explicando o porquê.

## 8. Limitações de acesso
- Sem senhas, tokens ou chaves. Não use os secrets do repositório nem rode workflows.
- Sem acesso à planilha real, ao Supabase ou ao Drive a partir desta cópia (rede bloqueada de propósito).
- Arena em dupla precisa de 2 aparelhos e do servidor real: fica fora deste teste.
- Ao terminar: commits só na branch `codex-arena-teste` (ou numa branch nova a partir dela) e um resumo do que mudou com antes/depois. O Claude/Felipe decidem o que vai para a `main`.

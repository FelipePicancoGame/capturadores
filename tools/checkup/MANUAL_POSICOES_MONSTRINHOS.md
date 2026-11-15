# Manual de posições dos monstrinhos — Capturadores do Vale

Regra de ouro: **antes de colocar qualquer monstrinho ou animação nova no jogo, rodar o avaliador** (`node checkup/murav.js`) e olhar as fotos. Se ele reprovar, não sobe.

## Posição em cada parte do jogo

| Onde | Monstrinho do jogador | Inimigo | Quando ataca |
|---|---|---|---|
| **Muralha** | **DE COSTAS, virado pra cima** (sempre, parado ou atacando) | de frente, descendo | jogador: golpe de costas pra cima · inimigo: de frente |
| **Muralha em Dupla** | igual à Muralha: DE COSTAS | de frente | igual à Muralha |
| **Batalha** | de costas, embaixo à esquerda | de frente, em cima à direita | jogador: **pra cima e pra direita** · inimigo: pra baixo e pra esquerda |
| **Mapa (andando atrás do herói)** | vira pra onde anda (8 direções); parado fica de frente | — | — |
| **Horda** | vira pra onde anda (8 direções) | vira pra onde anda | — |
| **Torres** | olha pro inimigo que está mirando | vira pra onde anda | olha pro alvo |
| **Expedição** | parado em pose de luta, olhando pros inimigos (pra direita) | olhando pro jogador (pra esquerda) | um olha pro outro |
| **Arena** | vira pra onde anda / pro alvo | vira pra onde anda / pro alvo | olha pro alvo |
| **Cartas, Coleção, Equipe, Treino, Loja, Ficha** | **de frente, reto** (sem lado, sem diagonal) | — | — |

## Regras que o Felipe já deu
- Monstrinho sempre reto: **sem ficar de lado, sem diagonal, sem olhar pra cima ou pra baixo** quando é pra estar de frente ou de costas (28/out).
- Na Muralha, **todo** monstrinho do jogador fica **virado pra cima** (14/nov).
- Na Batalha, atacando: **pra cima e pra direita** (14/nov).
- Todo monstrinho precisa de "lançar poder" **de frente** (como atacante) e **de costas** (como defensor) (28/out).

## Como cada animação tem que existir (para o Buchecha)
1. Parado de frente + andar de frente.
2. Parado de costas + andar de costas (é o que aparece na Muralha e na Batalha).
3. Andar nas 8 direções (mapa, Horda, Torres, Arena).
4. Ataque de frente (inimigo) e ataque de costas (jogador).
- Arte vista de cima (Arena) **não serve** para a Batalha nem para a Muralha.

## Avaliador
- **Muralha:** `node checkup/murav.js` (todos) ou `node checkup/murav.js estrelim,fornalho` (só alguns).
  - Põe cada monstrinho na Muralha, anota como ele foi desenhado e tira foto de cada um em `checkup/out/murav/`.
  - **APROVADO** só se todos estiverem de costas. **FRENTE** = erro.
- Depois de passar no avaliador, **olhar as fotos**: o avaliador garante que usou a folha "de costas", mas só o olho garante que a folha está certa (ex.: costas que na verdade é de lado).
- Batalha: `node checkup/estatk.js` (foto do ataque do jogador; tem que ir pra cima e pra direita).

## Erros que já aconteceram (para não repetir)
- 14/nov: Estrelim aparecia **de frente** na Muralha. Causa: o jogo só usava a animação de costas quando o monstrinho tinha a arte parada "n_"; quem não tinha caía no desenho de frente.
- 14/nov: Estrelim na Batalha virado pro lado errado (o jogo espelha o parado) → usar a versão virada.
- 14/nov: ataque do Estrelim vindo da Arena (visto de cima) virava pro lado errado na Batalha → tirado e pedido novo ao Buchecha.
- 11/nov: costas do Arvorito e outros eram de lado (diagonal) → na Muralha usam o 1º quadro do ataque (de costas reto).

## Situação em 14/nov (cv-v584)
- Avaliador rodou nos 71 monstrinhos. **26 estavam DE FRENTE na Muralha** e foram corrigidos (agora de costas): Infernalho, Tsunamor, Florestão, Cordilhão, Cascal, Choquinho, Trovoar, Corujito, Corujão, Aurorion, Peixonete, Tubarete, Caranguejo, Cogumelim, Cogumelão, Cabrito, Cabritão, Cacauzinho, Cascopedra, Trovim 2, Sombrin, Psiuto, Estrelim, Estrelux, Estelarion (+ Trovim 3).
- **22 não têm NENHUMA arte de costas** (continuam de frente até o Buchecha fazer): Ventania, Furacão, Ratangão, Ratorrei, Zumbitron, Tempestor, Espectron, Magmorra, Floraia, Corujarca, Tubarrei, Caranguerra, Pinçador, Cogumestre, Carneirão, Glacimor, Pinguimperador, Dracobrasa, Sombrale, Noctavio, Mentora, Psiquara.
- Olhando as fotos, conferir: Tubarete, Cordilhão, Cabritão, Cacauzinho e Estrelux estão de costas **na diagonal** (não reto); Corujito e Corujão de costas parecem uma nuvem.

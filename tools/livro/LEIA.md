# Livro dos Monstrinhos + vigia automática

Livro publicado: https://claude.ai/artifact/43uWQuvf9FiiZ94qaTifqB (atualizar sempre esse mesmo, com `url`).

## Rodar
```
python3 tools/livro/dump.py /tmp/livro            # lê o jogo no Chrome headless (não muda nada no jogo)
python3 tools/livro/gen.py /tmp/livro cv-vNNN DD/MM/AAAA
```
Saídas: `/tmp/livro/livro-monstrinhos.html` (o livro) e `/tmp/livro/problemas.json` (conferência automática).

## O que a conferência automática olha
- monstrinho fora da Coleção (DEXLIST), sem arte carregando, golpe que não existe;
- líder de arena com tipo que não existe;
- sem especial próprio na Muralha, sem poder na Arena;
- linha que não aprende golpe depois do nível 20, 2 golpes no mesmo nível, golpe que ninguém usa;
- tipo sem fraqueza; nome de golpe/especial sem inglês; arte com menos de 150 px; erro ao abrir o jogo.

`arte_notas.json` = notas de arte feitas olhando (não automáticas). Tirar a nota quando a arte nova entrar ou o Felipe decidir.

## Decisões do Felipe (não tratar como erro)
- Brasinha e Brasalor azuis (Fogo): escolha dele. Brasalor = dragãozinho azul de 4 patas; o com asas é a forma 3.
- Ratonga esverdeado é o que ele quer.

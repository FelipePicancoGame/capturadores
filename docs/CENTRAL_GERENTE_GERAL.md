# Central do Gerente Geral — Capturadores do Vale (cópia no repositório)

O Felipe fala com o **gerente geral**. Cada setor tem um chat especialista que trabalha só no seu setor.

## Onde ficam os pedidos
Quadro "Central do Vale": https://claude.ai/artifact/GU9KUzr4CCn83dcRComngg
- `pedidos`: setor, titulo, detalhe, status (novo / fazendo / feito), resposta
- `relatorios`: setor, titulo, texto, versao, criado

## Setores e quem faz
| id na Central | Chat |
|---|---|
| estatistica, equilibrio | Chat da Estatística (Equilíbrio não tem chat próprio) |
| alinhamento | Chat Alinhamento/Arte |
| traducao | Chat Tradução |
| livro | Chat Livro dos Monstrinhos |
| buchecha | Chat Chefe de arte (fila do Buchecha) |
| arena, gerente | Gerente geral |

## Protocolo de todo chat especialista
1. Ao começar: ler na Central os pedidos do seu setor com status "novo" ou "fazendo" (ArtifactData, query em `pedidos`, setor == seu id).
2. Trabalhar só no seu setor. Coisa de outro setor vira pedido novo para aquele setor.
3. Pegou: status "fazendo". Terminou: "feito" + `resposta` em uma linha.
4. Sempre escrever um relatório em `relatorios` (setor, título, o que mudou, versão cv-vN / Oficial vN).
5. Antes de mexer no jogo: git pull. Outros chats mexem no mesmo código. Nunca commitar audit.html.
6. Regra do Felipe: publicar no App E no Oficial. Se só publicou no App, dizer no relatório.

## Nome do jogo (decisão do Felipe, 15/nov 16h03: "tudo Tame Rush")
- Nome novo: **Tame Rush**, em TUDO, igual em português e inglês. Não é mais "Valekin: Tame Rush" nem "Capturadores do Vale".
- NÃO mudar (quebra save, compras ou links): chave de save `capturadores-vale-v1`, `CapturadoresApp`, bundle `com.capturadoresdovale.app` e os IDs das compras, endereço `felipepicancogame.github.io/capturadores`, e-mail `capturadoresdovale@gmail.com`, nome do repositório, prefixo `cv-v`.
- Texto novo no jogo: escrever "Tame Rush". "Capturador" (o jogador) e "Vale" (o lugar) continuam.
- Falta arte: o logo pintado da tela inicial (4 imagens `tela_inicial_*`) ainda diz CAPTURADORES DO VALE, e as fotos da App Store também. Pedido ao Buchecha no Drive (PEDIDO_CLAUDE_15nov_NOME_TAME_RUSH); só entra depois do OK do Felipe.

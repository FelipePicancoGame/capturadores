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

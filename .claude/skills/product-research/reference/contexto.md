# Product Research · Referência: Quando usar, a tese da recombinação, antes de começar e pré-flight (ETAPA 0)

> O texto integral do quando usar com a tese que governa a skill (clonar, criar do zero, recombinar), das leituras iniciais (idioma, profile, consulta à base pelo índice, sistemas completos) e do pré-flight com o nicho default e a escolha do destino do banco de marcas (Notion ou HTML). Abra antes da ETAPA 0.5.

## Quando Usar

Quando o membro ainda não tem produto ou quer encontrar o próximo. A skill existe pra responder uma pergunta só: **qual combinação de elementos que o mercado já provou (mecanismo, ângulo, formato do produto, posicionamento, oferta) eu consigo montar de um jeito que nenhum concorrente escalado está usando — sem clonar ninguém e sem inventar nada do zero?**

A tese que governa a skill inteira:

- **Clonar** uma marca escalada coloca o membro num leilão com quem já tem histórico de pixel, prova social e caixa. Sem diferencial, ele paga o CPM mais caro pra entregar a mesma mensagem.
- **Criar do zero** (mecanismo novo, formato novo, ângulo nunca testado) custa o teste inteiro — e a maior parte dos testes do zero morre.
- **Recombinar** elementos validados por marcas diferentes é o meio do caminho: cada peça já provou que vende, e a combinação é nova. O máximo de invenção permitido é **aprimorar** um mecanismo que já escala.

## Antes de Começar

0. **Idioma do relatório (rule 0 — INVIOLÁVEL)**: leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo, páginas do Notion) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (hooks, headlines, ads, páginas) e VOC literal (frases de review) permanecem SEMPRE em inglês US**, independente do `report_language`.
1. Leia `workspace/profile.md` — budget diário, ferramentas conectadas (TrendTrack, Notion), nicho de interesse se o membro já declarou.

> **Índice completo dos frameworks desta skill: `.claude/lib/kb-index/` (mapa skill→domínio no README).** A skill `product-research` puxa do domínio `product-research`. Nas ETAPAS 5, 7 e no naming, onde a skill pede "puxe os SISTEMAS NOMEADOS", rode `search_knowledge` com a `best_query` EXATA de cada framework — nunca query genérica tipo "product research" ou "market sophistication".
>
> **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill product-research --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 10 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão.

2. **Puxe os SISTEMAS COMPLETOS**, não resumos (ex: os 5 estágios de sophistication de Schwartz com claims e respostas estratégicas, não "sophistication"). Internalize ANTES de analisar — os frameworks são pra APLICAR na decomposição e no ranking de cada marca, não pra citar.

### ETAPA 0 — Pre-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

1. Leia `workspace/profile.md`. Se **não existir**, aborte com: `"Rode \`setup\` primeiro — profile.md ausente."` (ofereça rodar o setup inline).
2. Localize `manifest.json`:
   - Procure um `manifest.json` em `workspace/*/manifest.json` cujo `setup_complete === true`.
   - Se existir, leia `product_slug` — é o path canônico pra qualquer salvamento até o produto vencedor ser escolhido (ver SALVAR).
   - **Se houver MAIS de um** manifest com `setup_complete === true`, NÃO escolha silenciosamente: liste os `product_name` e pergunte em 1 linha qual é o alvo. Se o membro já nomeou o produto no trigger, use esse.
   - Se **não existir**, aborte com: `"Rode \`setup\` primeiro — manifest.json ausente."` (ofereça rodar o setup inline).
3. Confirme que `setup` está em `skills_completed`. Caso contrário, re-rode o setup.
4. **Nicho.** Default desta skill é **health & supplements** (é o nicho dos filtros fixos da ETAPA 0.5). Se o membro quer outro nicho, ele diz e você troca só o filtro de nicho — o resto do método é idêntico.
5. **Onde salvar o banco de marcas.** Verifique se há tools de Notion na sessão (prefixo `mcp__claude_ai_Notion__` ou `mcp__notion__` — qualquer prefixo com `notion`). Se NÃO houver, pergunte UMA vez, em 1 linha:

   > "Quer que eu salve o banco de marcas no Notion (uma página por marca, com links dos ads, LP, tráfego, reviews e a jogada recomendada)? Se sim, conecta o Notion MCP agora — no claude.ai / Claude Desktop: Settings → Connectors → Notion → conectar; no Claude Code: `claude mcp add --transport http notion https://mcp.notion.com/mcp` e autorize no browser. Se preferir, eu salvo tudo em HTML na pasta do produto."

   Grave a escolha (`notion` ou `html`) e siga. A pesquisa não espera o Notion — ela roda igual; só o destino muda (ver SALVAR).

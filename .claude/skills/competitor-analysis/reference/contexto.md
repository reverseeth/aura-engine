# Competitor Analysis · Referência: Quando usar, antes de começar e pré-flight (ETAPA 0)

> O texto integral do quando usar, das leituras iniciais (idioma, product-research e banco de marcas, market-research, consulta à base pelo índice) e do pré-flight com os arquivos obrigatórios e os dois caminhos quando falta algum. Abra antes da ETAPA 0.5.

## Quando Usar
Quando o membro tem produto definido e market research feito, e precisa mapear o cenário competitivo com profundidade operacional antes de criar oferta e copy. A análise aqui alimenta: mecanismo único (o que NÃO usar), posicionamento (onde ninguém está), claims (o que evitar e o que explorar), e estrutura de funil (o que o mercado converteu).

## Antes de Começar

1. Leia `workspace/profile.md`. Leia o campo `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do `report_language`. Observação importante específica desta skill: copy literal de concorrentes (headlines, hooks, claims, transcrições de ads) permanece no idioma original do ad — é evidência, não tradução.
2. Leia `workspace/[produto]/product-research/product-research.md` e `product-research/banco-de-marcas.md` (se existirem — as marcas escaladas do nicho já vêm com LP mais escalada, ads mais escalados, tráfego, mecanismos e ângulos; são os primeiros concorrentes desta análise) e `product-research/dados.json` (`validated_elements[]` é a semente da `validated_library` da ETAPA 7 — aprofunde, não refaça)
3. Leia `workspace/[produto]/market-research/market-research.md` (overview competitivo básico + gaps já identificados; se não existir, leia o legado `relatorio.md`)
4. **Puxe os SISTEMAS NOMEADOS da base** — NUNCA use query genérica tipo "competitor analysis". Pra cada ETAPA, rode `search_knowledge` (com `deep=true`) usando a `best_query` exata de cada framework relevante listado nas próprias ETAPAs abaixo. O domínio desta skill é `competitor-positioning`; o índice está em **`.claude/lib/kb-index/`** (mapa skill→domínio no `README.md`). Esta skill opera em detalhe EXECUTIVO, não conceitual — puxe o sistema completo de cada framework, não o resumo de superfície.

> **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill competitor-analysis --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 10 buscas por etapa. As queries já embutidas na etapa são o mínimo garantido. Não repita busca de framework já puxado na sessão.

### ETAPA 0 — Pre-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

1. Leia `workspace/profile.md`. Se TOTALMENTE ausente → sem profile não há o que inferir; ofereça rodar o setup inline: `"Não achei seu profile. Rode \`setup\` agora (eu conduzo aqui mesmo) e a gente segue."`
2. Leia `workspace/[produto]/manifest.json` (identifique `[produto]` via manifest com `setup_complete === true`). Se TOTALMENTE ausente → ofereça rodar o setup inline (mesma mensagem do item 1).
3. Valide a existência de TODOS os arquivos obrigatórios:
   - `workspace/[produto]/product-research/product-research.md`
   - `workspace/[produto]/market-research/market-research.md`
   - `workspace/[produto]/market-research/dados.json`
4. Valide que `skills_completed` do manifest contém `"product-research"` E `"market-research"`.
5. Se faltar qualquer arquivo obrigatório dos itens 3-4 (mas profile + manifest existem), NÃO aborte seco. Ofereça ≥2 caminhos: **(A)** Rodar a skill faltante agora (`product research` ou `market research`), OU **(B)** prosseguir com default genérico marcando `manifest.skipped_preflight += ["<arquivo>"]` e avisando no output final que recomenda re-executar com o arquivo real. Default conservador = (A).

# Consistency Audit · Referência: Base de conhecimento pelo índice, quando usar e pré-flight

> O texto integral da consulta à base pelo índice (domínios, limite de buscas, critério por check), de quando usar com os exemplos reais de drift, e do pré-flight (manifest, idioma do report com a copy em inglês, e o safeguard de input parcial). Abra antes da ETAPA 1.

## Base de conhecimento (consulta pelo índice, NUNCA query genérica)

Esta skill audita coerência cross-phase; quando precisar JULGAR qualidade de um claim, proof, ou alinhamento (não só comparar strings), puxe SISTEMAS NOMEADOS da base via `search_knowledge` — nunca query genérica tipo "audit checklist" ou "landing page review". A consulta segue o índice (`.claude/lib/kb-index/README.md`):

Os domínios desta skill são **`copy-proof-persuasion-structure`** e **`page-landing-cro`**. Rode `python3 .claude/lib/kb-index/kb_lookup.py --skill consistency-audit --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 6 buscas por etapa. As queries já embutidas na etapa são o mínimo garantido. Não repita busca de framework já puxado na sessão. O critério de relevância é por CHECK: só entra a entrada que muda o veredito do check em análise. Escrita é da `copy-engine` e design é da `page-design`; aqui é julgamento de auditoria.

Mapa skill→domínio no README do kb-index.

## Quando Usar

Antes de launch oficial (ads go-live + page em produção), rodar esta skill pra pegar incoerências acumuladas ao longo das skills, da `product-research` à `creative-engine` — incluindo os artefatos pré-launch da `bonus-delivery` (Fase A) e da `retention-engine` (Fase A), que na ordem canônica já existem neste ponto. Exemplos reais de drift:

- Mecanismo único nomeado "X" na skill `offer-builder` virou "X-alt" nas variações de hook da skill `creative-engine`
- VOC phrase repetida 12x no market research NÃO aparece em nenhum hook do ad batch
- Hook do ad promete resultado "in 14 days" mas a página inteira fala em "30 days"
- Guarantee copy diz "90 days" mas `offer-builder/dados.json` diz 30 days
- Ad primary text menciona bonus que foi removido na última iteração do offer stack

## Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

- [ ] `workspace/[produto]/manifest.json` existe com `setup_complete: true`
- [ ] Pelo menos 3 skills completed em `skills_completed[]` (senão não há o que comparar)

**report_language:** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo — inclusive `issue` e `fix_suggested` dos findings) e toda conversa com o membro usam esse idioma, seguindo o padrão de linguagem simples da regra 0 do `.claude/CLAUDE.md` (nenhuma sigla sem explicação imediata, zero frase de analista comprimida, números estatísticos em palavras). **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language — o trecho auditado é citado no original, o veredito sobre ele vai no idioma do report.

**Input parcial (safeguard):** se `copy-engine/{copy-engine.md,dados.json}` E `creative-engine/dados.json` estiverem AMBOS ausentes, não há copy nem ad pra cruzar — force `launch_recommendation: "CAUTION"` (nunca `GO`), registre cada artefato faltante em `artefacts_missing[]`, e marque os checks que dependem deles como `"skipped"` (nunca `"pass"`). Não aborte: rode os checks que forem possíveis com o que existe e avise no output final que recomenda re-executar após gerar copy/criativos.

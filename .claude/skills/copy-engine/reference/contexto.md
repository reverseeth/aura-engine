# Copy Engine · Referência: Pré-flight, quando usar e antes de começar

> O texto integral do pré-flight (checklist dos inputs com os campos a extrair de cada `dados.json`, o gate de VOC com as três opções e o flag `voc_forced_continue`, o `copy_language`, os dois caminhos do ES1), o quando usar e a lista de leituras iniciais com a consulta à base pelo índice. Abra antes do Input Extraction.

### Pré-flight (OBRIGATÓRIO)

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.
- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `product_slug` do manifest NÃO começa com `dev-placeholder-` (senão, pare: "rode product research primeiro")
- [ ] `market-research/dados.json` existe → extrair `awareness_distribution`, `sophistication_stage`, `voc_top20` (se presente), `voc_phrases`, `voc_count`, `voc_adequacy`
  - `voc_top20` é o ranking curado da Skill `market-research` (20 frases com `rank` + `count` + `category`) — é a fonte primária do `voc_checklist` (Input Extraction). `voc_phrases` é o objeto `{problem:[], desire:[], frustration:[]}` — se precisar usar (fallback legado), **achate os 3 pools** num único array antes (não assuma array plano). `voc_count` = total de frases únicas somando os 3 pools.
- [ ] **VOC adequacy check:** se `voc_adequacy == "insufficient"` OU `voc_count < 15` → PARE com mensagem:
  > ⚠️  VOC atual: {N} frases únicas. Mínimo pra copy direta: 15.
  >     Copy sem VOC real é invenção — vai soar genérica e não converter.
  >     Opções:
  >     1. Rode skill `market-research` de novo com mais fontes (Reddit, Amazon reviews, TikTok comments)
  >     2. Me cola manualmente 10-15 frases de clientes reais (reviews, DMs, comentários)
  >     3. Prossiga mesmo assim reconhecendo limitação (copy ficará abstrata)

  Se membro escolher 3, marca `"voc_forced_continue": true` no output pra Skill `ad-analysis` diagnosticar depois.
- [ ] `competitor-analysis/competitor-analysis.md` existe (ou o legado `relatorio.md` — mesmo fallback vale pras outras fases)
- [ ] `offer-builder/dados.json` existe → extrair `mechanism` (objeto `{name, ...}` — usar `mechanism.name`, NÃO tratar como string), `pricing`, `guarantee`, `bonuses[]` (cada bonus tem `condition` — dirige a copy de GWP/stack, ver ETAPA 4)
- [ ] `offer-builder/research-foundation.json` (se existir) → extrair `proof_items[]` — o banco de provas (estudos, números, citações) que vira munição de specificity na copy. É munição, não teto: a copy não fica limitada ao que está lá.
- [ ] Ler `manifest.copy_language` (se presente; default `"en"`) — confirma o idioma da copy consumidor-final. Não confundir com `report_language` (idioma dos relatórios internos): a copy pública segue `copy_language`, que hoje é sempre inglês US pro mercado US

Se faltar qualquer arquivo de fase anterior (`market-research`/`competitor-analysis`/`offer-builder`), em vez de abortar seco ofereça ≥2 caminhos:
> **(A)** Rodar a skill faltante agora (`market-research`/`competitor-analysis`/`offer-builder`), OU **(B)** prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` e avisando no output final que recomenda re-executar com o arquivo real. VOC com opção 3 já segue esse padrão acima. Exceção: se `manifest.json` ou `profile.md` estiverem TOTALMENTE ausentes, não há o que inferir — ofereça rodar o setup (skill `setup`) inline.

## Quando Usar
Quando o membro tem market research, competitor analysis e oferta prontos, e precisa escrever a copy da página que vai converter o tráfego pago. Copy aqui é escrita com base em decisões ESTRATÉGICAS derivadas dos documentos anteriores, não em opiniões ou intuições.

## Antes de Começar

1. Leia `workspace/profile.md` — em especial `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno desta skill (strategy brief, sweeps documentados, `.md`/`.html` descritivos) e toda conversa com o membro usam esse idioma, seguindo o padrão de linguagem simples da regra 0 do `.claude/CLAUDE.md` (nenhuma sigla sem explicação imediata, zero frase de analista comprimida, números estatísticos em palavras). **A copy consumidor-final (headlines, leads, hero, bullets, CTAs, advertorial, email hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do `report_language` — copy pública nunca traduz.
2. Leia `workspace/[produto]/market-research/market-research.md` (psychographics, awareness/sophistication, VOC literal, objeções, root cause)
3. Leia `workspace/[produto]/competitor-analysis/competitor-analysis.md` (claims saturados a evitar, gaps, posicionamento recomendado, swipe file)
4. Leia `workspace/[produto]/offer-builder/offer-builder.md` (mecanismo único com 3 versões, bundles, garantia, unit economics)
5. **Puxe os SISTEMAS NOMEADOS da base — não query genérica.** Esta skill é o coração do sistema. NUNCA dispare uma busca tipo "copy framework" ou "headlines" — sempre o nome do sistema + sua query curada. Os domínios desta skill são `copy-headlines-leads`, `copy-proof-persuasion-structure` e `persuasion-psychology` (mapa skill→domínio no `README.md` da lib). Rode `python3 .claude/lib/kb-index/kb_lookup.py --skill copy-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 14 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão. As queries embutidas nas ETAPAs 2-6 abaixo ficam no ponto onde cada framework é usado.

# Marketplace Engine · Referência: Os sistemas nomeados a puxar

> A regra de consulta pelo índice, o recorte do que esta skill puxa e o que fica com as vizinhas, e a lista dos sistemas do domínio próprio e dos domínios vizinhos, com a query exata de cada um. Abra antes de qualquer etapa.

### Puxe os SISTEMAS NOMEADOS da base

Rode `search_knowledge` (deep=true) com a `best_query` exata de cada sistema. **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill marketplace-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 6 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão. No domínio `affiliate-creator-channels` esta skill puxa as entradas de canal (Amazon Playbook, TikTok Shop, Social Snowball, recrutamento pago, custom link e a regra de entrada de marketplace); Creator Farming e Whitelist Ads são território da `creator-engine`/`creative-engine`/`ad-strategy` e não se puxam aqui. **Esta skill é a consumidora que faltava** dos sistemas de marketplace marcados como dormant no índice (`use_in_skill: "—"`) — a partir dela, eles são puxáveis.

**Do domínio `affiliate-creator-channels`:**

- **Marketplace como canal secundário (regra de entrada)** — `quando abrir marketplace como canal secundario Amazon TikTok Shop regra de entrada`
- **Amazon Playbook (SEO, ninja low-bid, slash-through, custom link, TACOS)** — `playbook Amazon SEO de listagem ninja low bid slash through custom link TACOS`
- **Operação de TikTok Shop** — `operacao de TikTok Shop samples afiliados comissao e conteudo`
- **Social Snowball (programa de afiliados automatizado)** — `Social Snowball programa de afiliados automatizado comissao por cliente`
- **Recrutamento pago de afiliados** — `recrutar afiliados com trafego pago apply to be brand ambassador`
- **Custom Link + atribuição de afiliado** — `custom link de afiliado atribuicao de venda por creator`

**De domínios vizinhos (entradas de canal marcadas também pra esta skill):**

- **"Não abra canal que você não domina"** _(meta-ads-strategy)_ — `não abra canal que você não domina enquanto há espaço no Meta branded search é defesa`
- **Google Search Stronghold + setup 80-20** _(meta-ads-strategy — o sinal de busca de marca)_ — `Google Search Stronghold branded search proteger a marca converter copy do Facebook`
- **Trademark + Facebook Brand Rights Protection** _(meta-ads-strategy — compartilhada com a `setup`)_ — `trademark registrado brand rights protection fake DMCA derrubou 300 ads`
- **Affiliate Recruitment via Paid Ads + TikTok Shop como máquina de conteúdo** _(scaling)_ — `rodar paid ads para recrutar afiliados save 40% apply to be brand ambassador TikTok Shop conteudo`
- **Brand Ambassador Ladder (retainer + comissão em degraus)** _(creatives-hooks-formats)_ — `retainer 500 por video semanal performance program regra do 2-3 comissao decrescente 10 5 2.5 1`
- **Creative Strategy em 9 Dimensões (a dimensão de canal de venda)** _(meta-ads-strategy)_ — `9 dimensoes self-audit business brand creative sales channel funnel production testing measurement`

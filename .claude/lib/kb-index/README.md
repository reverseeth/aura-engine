# Aura KB Index (índice da base de conhecimento)

Catálogo de **1309 entradas de frameworks/sistemas nomeados** da base Aura (um mesmo framework aparece em mais de um domínio quando serve a skills diferentes), por domínio, com a query exata pra puxar cada um e a skill que deve usar. Gerado 2026-06-20; **append incremental em 2026-09-01** (19 domínios); **retag geral + 19 entradas novas na criação das skills 15-20** (mesma data). O catálogo em si vive no `frameworks.json` e é consultado pelo `kb_lookup.py`; este README guarda só as notas de atualização, o modo de uso e o mapa skill → domínios.

> **Atualização 2026-09-01 — append incremental, chave congelada.** As 541 entradas originais tiveram `name` e `best_query` **preservados byte a byte**: 276 dessas queries estão copiadas literalmente dentro de 14 arquivos de skill (373 ocorrências), e reescrevê-las quebraria metade do corpo de skills em silêncio — `search_knowledge` aceita qualquer string, então a skill não daria erro, só passaria a puxar conteúdo errado. Esta revisão fez três coisas e só três: (a) **acrescentou 749 entradas** aos 14 domínios existentes e criou **5 domínios novos**; (b) corrigiu `source` e `one_line` das entradas antigas (os dois campos que nenhuma skill copia) para refletir a hierarquia de fontes revisada; (c) marcou explicitamente os domínios sem skill consumidora. **Regra permanente: `name` e `best_query` de entrada já publicada são imutáveis.** Se uma query precisar mudar de verdade, `grep -rF "<query>" .claude/skills/` primeiro, e a edição da skill entra no MESMO commit.
>
> **Hierarquia de fontes (revisada 2026-09-01):** a fonte primária 2026 (P1) e a fonte primária high-ticket 2026 (P1) são **primárias em todo DTC/ecommerce, inclusive Meta Ads**. Segundo nível (P2): a masterclass interna, livros (quando são a fonte original) e swipe files. Onde a doutrina mudou de fato, a entrada antiga foi **mantida** e carimbada com nota `SUPERSEDED`/`ATUALIZADO` apontando o substituto — nunca apagada.
>
> **Atualização 2026-09-01 (2ª onda — skills 16-20):** com a criação das skills 16-creator, 17-promo, 18-team, 19-ops e 20-marketplace (e a 15-finance já no ar), 170 entradas tiveram `use_in_skill` atualizado — só esse campo; `name` e `best_query` seguem congelados — e **19 entradas novas** entraram por append nos domínios existentes. Os três domínios órfãos ganharam consumidora; restam **5 entradas dormant** no arquivo inteiro (todas em `ops-scale-risk`). Na mesma revisão, as citações de **07b** em `use_in_skill` (43 casos) foram trocadas por **07a** ou removidas: decisão de página nasce na 07a — a 07b só compila o que foi aprovado e não consulta este índice.

## Como as skills usam este índice (revisado 2026-09-17)

Toda skill que consulta a base puxa SISTEMAS NOMEADOS pela `best_query` exata, nunca por query genérica ("headlines", "offer"). A lista do que existe para cada skill sai de um script, e não da leitura do `frameworks.json`: o arquivo inteiro tem cerca de 200 mil tokens e nunca deve ser aberto numa sessão.

1. **Liste as entradas da skill.** No início de cada ETAPA que consulta a base, rode `python3 .claude/lib/kb-index/kb_lookup.py --skill <id> --domain <domínio desta etapa>` e trabalhe com a lista impressa: uma linha por entrada (nome, `best_query` e resumo), agrupadas por domínio, com o total no fim. O `--skill` aceita o id do registro (`copy-engine`) ou o apelido numérico antigo (`06`). Omita o `--domain` quando a etapa cruza vários domínios: sem ele, o script mostra todas as entradas marcadas para a skill, em qualquer domínio. `--grep <texto>` filtra por nome ou resumo; `--format json` devolve a mesma lista para uso por script; `--list-domains` mostra os domínios e o tamanho de cada um.
2. **Puxe as entradas relevantes à etapa** com `search_knowledge`, usando a `best_query` exata e `deep=true`. É a query curada que traz o sistema completo (as 35 fórmulas de Caples, não "fórmulas de headline").
3. **Limite por etapa.** No máximo 6 buscas nas skills leves (setup, bonus-delivery, page-build, tracking-setup, checkout-aov, agentic-readiness, consistency-audit, content-recycler, ops-engine, marketplace-engine), 10 nas médias (product-research, sourcing, market-research, competitor-analysis, ad-strategy, ad-analysis, scale-engine, retention-engine, finance-engine, creator-engine, promo-engine, team-engine) e 14 nas pesadas (offer-builder, copy-engine, page-design, creative-engine). As queries já embutidas no texto da skill são o mínimo garantido de cada etapa.
4. **Não repita busca de framework já puxado na mesma sessão.** Entradas duplicadas entre domínios (ex: Hormozi Value Equation, LF8) apontam para o MESMO conteúdo; reuse o resultado.

O campo `skills` de cada entrada (lista de ids do `.claude/skills.json`) é derivado do texto de `use_in_skill` pelo `normalize_index.py`. Depois de qualquer edição do `frameworks.json`, rode `python3 .claude/lib/kb-index/normalize_index.py` (`--check` só confere). O `check_embedded_queries.py` confirma que as `best_query` embutidas nas skills continuam existindo no índice. As contagens por domínio citadas dentro das skills são informativas; a fonte da verdade do tamanho de um domínio é o total que o `kb_lookup.py` imprime.

## Mapa skill → domínios deste índice

| Skill | Domínios a consultar |
|---|---|
| 00 | pontual: brand-building-bonus-aov (member stage), market-research-voc (brand voice) |
| 01 | product-research |
| 01b | **supply-chain-sourcing** (NOVO 2026-09-01) |
| 02 | market-research-voc, persuasion-psychology |
| 03 | competitor-positioning |
| 04 | offer-mechanism, offer-pricing-guarantee, brand-building-bonus-aov, **finance-projections** (NOVO) |
| 05 | brand-building-bonus-aov |
| 06 | copy-headlines-leads, copy-proof-persuasion-structure, persuasion-psychology |
| 07a | page-landing-cro |
| 07c | meta-ads-strategy (só as entradas de CAPI / Pixel / Event Match Quality) |
| 07d | page-landing-cro (checkout / AOV / profit), brand-building-bonus-aov, offer-pricing-guarantee |
| 08 | creatives-hooks-formats, persuasion-psychology |
| 09 | copy-proof-persuasion-structure, page-landing-cro |
| 10 | meta-ads-strategy, persuasion-psychology |
| 11 | meta-ads-strategy |
| 12 | scaling, **finance-projections** (NOVO) |
| 13 | retention-email, persuasion-psychology |
| 14 | creatives-hooks-formats, page-landing-cro |
| 15 | **finance-projections** (dona do domínio — inclusive os 4 sistemas antes dormant: Float Stack, Função Financeira em 3 Camadas, Triângulo de Forecasts, Banking Sheet) |
| 16 | creatives-hooks-formats (motor creator/UGC), affiliate-creator-channels, meta-ads-strategy, scaling, team-hiring-ops, competitor-positioning, product-research |
| 17 | **transversal — não tem domínio próprio:** meta-ads-strategy, scaling, finance-projections, creatives-hooks-formats, retention-email, offer-pricing-guarantee, page-landing-cro, brand-building-bonus-aov, market-research-voc, supply-chain-sourcing |
| 18 | **team-hiring-ops** (todas as entradas), ops-scale-risk (founder/gargalo), scaling (modelo por faixa + time criativo) |
| 19 | **ops-scale-risk**, meta-ads-strategy (Anti-Ban, Trademark/BRP), brand-building-bonus-aov (Product Moat) |
| 20 | **affiliate-creator-channels**, meta-ads-strategy (canal/defesa de marca), scaling (recrutamento pago + TikTok Shop), creatives-hooks-formats (Brand Ambassador Ladder) |

Este mapa é a **fonte de verdade** skill→domínio; as entradas de cada domínio saem do `kb_lookup.py` (`--list-domains` mostra os domínios e o tamanho de cada um). As skills **07b** (compile determinístico HTML→Liquid — toda decisão de conteúdo/design nasce na 07a) e **07e** (agentic-readiness — não existe domínio de AEO na base; as fontes dela são docs oficiais + verificação na loja viva) não consultam este índice.

**A 01b consulta o índice.** Até 2026-09-01 o `.claude/CLAUDE.md` instruía por escrito que a skill 01b-sourcing NÃO usasse a base ("não há domínio de sourcing/fornecedor lá") — era verdade quando o índice foi gerado e deixou de ser. A correção foi concluída na mesma data: o `CLAUDE.md` hoje manda a 01b puxar o domínio `supply-chain-sourcing` pelo índice, e a skill traz o bloco "puxe os SISTEMAS NOMEADOS" como as demais consumidoras.

### Ex-órfãos: os três domínios ganharam consumidora (2026-09-01)

Até a criação das skills 16-20, três domínios estavam indexados **sem nenhuma skill consumidora** (marcados com `use_in_skill: "—"`). Deixou de ser o caso:

| Domínio | Entradas | Consumidora hoje |
|---|---:|---|
| `team-hiring-ops` | 63 | **18-team-engine** — todas as entradas. As 8 que já transferiam pra skills vivas mantêm a consumidora original ao lado (08/09/11/12), e `Creator Pipeline` + `Ad Bounties` também servem à **16**. |
| `ops-scale-risk` | 17 | **19-ops-engine** — constraint de 12 meses, o que quebra por faixa, Headaches per Dollar, registro de marca/BRP, exits + 3 sistemas novos (backups worst-case, pre-order, memos WAFM). As 4 entradas de founder/gargalo também servem à **18**; `Expectativa de winning ad` e `Mini-memo de criativo (WAFM)` seguem com 08/12. **5 entradas continuam dormant** (Stack legal/financeiro US, Reorder Point + Safety Stock, Cash Conversion Cycle, SLA de 3PL, Agency Ops). |
| `affiliate-creator-channels` | 8 | **20-marketplace-engine** — 6 das 8 (Amazon Playbook, TikTok Shop, Social Snowball, Recrutamento pago, Custom Link, regra de entrada de marketplace). O recorte creator/afiliado serve também à **16**; `Creator Farming` e `Whitelist Ads` são território da 16/08/10 e não se puxam na 20. |

> **Slots (nota histórica):** as recomendações antigas desta seção citavam slots "16-team-engine", "17-ops-engine" e "18-marketplace-engine" (e antes disso 15/16/17). Os slots reais ficaram: **15-finance**, **16-creator**, **17-promo** (transversal — não tem domínio próprio neste índice), **18-team**, **19-ops**, **20-marketplace**.

**Regra que permanece:** não puxe entrada marcada `—` até existir skill que a leia. Restam **5** entradas assim no arquivo inteiro — todas em `ops-scale-risk`, listadas acima.

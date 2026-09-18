---
name: copy-engine
description: Engine de escrita de copy completo a partir do market research, da competitor analysis e da oferta. Escreve PDP, landing page, advertorial ou long-form sales page com headlines pelo processo de 100 linhas condensado, lead tipado pelo awareness, hero patterns de ecom, frameworks de persuasão (Cialdini, Sugarman, Hopkins), proof stacking, CTAs como call to value, 9 sweeps de revisão (8 de revisão mais o markup audit) e a linguagem exata do cliente. Modela a estrutura contra espécimes reais de swipe file antes de escrever e audita o resultado pelo método de markup (4 U's, 4 emoções, loop Objection-Claim-Proof-Benefit). O sistema decide a estratégia de copy sozinho, sem consultar o membro sobre decisões estratégicas. Use quando o membro disser "copy", "escrever copy", "copy da página", "copy do ad", "PDP copy", "landing page copy", ou depois da skill de oferta.
---

# Copy Engine · Passo 6 · apelido antigo: 06 <!-- gen:title -->

## Quando usar

Quando o membro tem market research, competitor analysis e oferta prontos e precisa da copy da página que vai converter o tráfego pago. A copy nasce de decisões estratégicas derivadas dos documentos anteriores, nunca de opinião. O sistema decide e apresenta as decisões como fato; ao membro cabem só duas perguntas de entrada.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova (só leia da numerada se a migração não puder rodar; escreva sempre na pasta sem número). Checklist completa em `reference/contexto.md`.

- [ ] `workspace/[produto]/manifest.json` existe e `product_slug` não começa com `dev-placeholder-`
- [ ] `market-research/dados.json`: `awareness_distribution`, `sophistication_stage`, `voc_top20`, `voc_phrases` (3 pools; achatar se precisar), `voc_count`, `voc_adequacy`
- [ ] Gate de VOC: `voc_adequacy == "insufficient"` ou `voc_count < 15` = PARE e ofereça as três opções (re-rodar a `market-research` com mais fontes, o membro cola dez a quinze frases reais, prosseguir reconhecendo a limitação); a opção 3 grava `voc_forced_continue: true` pra `ad-analysis`
- [ ] `competitor-analysis/competitor-analysis.md` (ou o legado `relatorio.md`)
- [ ] `offer-builder/dados.json`: `mechanism` é objeto (use `mechanism.name`), `pricing`, `guarantee`, `bonuses[]` com `condition`; `research-foundation.json` (se existir): `proof_items[]` é munição, não teto
- [ ] `manifest.copy_language` (default `en`): idioma da copy pública, sempre inglês US

Arquivo de fase anterior faltando (ES1): (A) rodar a skill faltante agora ou (B) seguir com default genérico marcando `manifest.skipped_preflight`. Manifest ou profile totalmente ausentes: oferecer o `setup` inline.

## Contexto a carregar

1. `workspace/profile.md` (`report_language`, default `pt-BR`, pra todo output interno e conversa; copy consumidor-final e VOC literal sempre em inglês US), `market-research/market-research.md`, `competitor-analysis/competitor-analysis.md` e `offer-builder/offer-builder.md`.
2. Input Extraction (`reference/input-extraction.md`): as oito variáveis lidas DIRETO dos `dados.json`, sem recomputar o que já foi decidido (leia o `resumo` de cada arquivo primeiro; sem `resumo`, leia inteiro): `dominant_awareness` (com `dominant_awareness_secondary` presente, lead híbrido), `sophistication`, `voc_checklist` = `voc_top20` na ordem do rank, `mechanism`, `guarantee` e `offer_stack`, `core_avatar` e `sub_avatars[]` (o lead fala com UM sub-avatar), `labels[]` (call-out) e `market_vocabulary` (`words_used[]` com `saturated_in_market`, `words_absent[]` com `market_says_instead`). Produto legado sem os campos 6 a 8: derive do objeto `avatar` e recomende re-rodar a `market-research`.
3. Base pelo índice (domínios `copy-headlines-leads`, `copy-proof-persuasion-structure` e `persuasion-psychology`): `python3 .claude/lib/kb-index/kb_lookup.py --skill copy-engine --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 14 buscas por etapa; as queries embutidas em `reference/` são o mínimo garantido; nunca query genérica nem busca repetida.

## Fluxo da skill

### ETAPA 1 · Perguntas ao membro (apenas 2)

Leia `reference/perguntas-ao-membro.md`. Tipo de página (PDP, landing, advertorial ou "não sei": Unaware e Problem Aware → advertorial; Solution Aware → landing; Product e Most Aware → PDP) e página atual (link lido por `WebFetch`, fetcher resiliente ou paste, como baseline do que manter e reescrever). Nenhuma outra pergunta.

### ETAPA 2 · Estratégia de copy (o sistema decide)

Leia `reference/estrategia-de-copy.md`. Puxe os sistemas de seleção (awareness, lead dimensions, sophistication, Big Idea, hero sections, porta-voz, Rule of One). Decida: tipo de lead pela tabela awareness → lead (e o sistema que constrói cada lead), hero pattern de ecom cruzado com os 5 tipos canônicos, ângulo principal = o gap mais forte da `competitor-analysis` virando Big Idea, com o sub-avatar de `angle` correspondente como o "one reader", tom de voz pelo psicográfico e `core_desire_behind`, framework de organização por tipo de página, e como servir as 4 modalities (Spontaneous, Competitive, Humanistic, Methodical) com os princípios de influência. Apresente o brief em 6 a 8 linhas como fato, com placeholders vindos do Input Extraction, e siga sem pedir aprovação. Grave o `lead_type` top-level no `dados.json` (contrato com a `page-design`).

### ETAPA 2.5 · Seleção de espécime (swipe modeling, obrigatória)

Leia `reference/especime.md`. 2.5A: escolha 1 espécime primário (e no máximo 1 secundário) em `.claude/lib/swipe-models/specimens.json` pela precedência `page_type` → awareness → sophistication → vertical, lendo a `regra_diagnostica` antes de fechar. 2.5B: puxe a anatomia com a `best_query` do espécime e a régua dos 11 blocos; sem anatomia, próximo espécime. 2.5C: monte a tabela de blocos (bloco, trabalho, o que entra do research) e declare os 4 a 6 pilares; é essa tabela que vira a copy. 2.5D: o lead cumpre os 4 passos do Makepeace. Modelar estrutura, nunca conteúdo. Grave `specimen_primary`, `specimen_secondary` e `specimen_block_map`.

### ETAPA 3 · Headlines (processo de 100 linhas, condensado)

Leia `reference/headlines.md`. Puxe os sistemas de headline. 3A: 20 a 30 variações cobrindo os tipos (benefício, curiosidade, problema, resultado específico, mecanismo, contrarian, pergunta, testimonial, autoridade, perda), com VOC literal, `labels[]` como call-out e o gate de vocabulário já na geração (termo saturado fora de headline; termo ausente fora de tudo). 3B: categorize e escolha o top 5 justificado. 3C: 3 hipóteses diferentes pra A/B (ângulo dominante, ângulo secundário, formato).

### ETAPA 4 · Página completa (seção por seção)

Leia `reference/pagina-hero-a-mecanismo.md`, depois `reference/pagina-prova-e-oferta.md` e `reference/pagina-garantia-a-adicionais.md`, cada um na seção correspondente. Ordem macro do pitch: payoff, belief, recomendação. Hero (headline número 1, sub-headline com o mecanismo, CTA como call to value, instrução visual); Trust Bar se há credenciais; Benefits em 3 a 5 bullets com a frase do consumidor, o benefício e o emocional; Unique Mechanism na versão de 1 parágrafo (2 a 3 em landing ou advertorial) adaptado ao awareness; Prova Social em stack (3 a 5 testimonials reais com nome, foto e resultado; sem depoimento real, `{{TESTIMONIAL_PLACEHOLDER_N}}` e a lista do que coletar, nunca depoimento fictício); Oferta com bundles, bump, stack ancorado e savings, e a copy de bônus seguindo `bonuses[].condition` (`cart_threshold` explícito, `unconditional`, `tier_specific` só no tier); Garantia em 2 a 3 frases; FAQ que quebra as top 5 objeções da `market-research`; CTA final como call to value repetido em 3 a 5 pontos; Urgency/Scarcity curta e com razão real, ou página sem urgência; seções adicionais quando cabem, com `## Specs` e `specs[]` recomendados em toda PDP.

### ETAPA 5 · Advertorial (alternativa à ETAPA 4)

Leia `reference/advertorial.md`. Estrutura de 7 seções (headline editorial, lead com as 4 perguntas do leitor, background story, root cause da `market-research`, mechanism reveal, product build-up, reveal e close com urgência real), tom editorial, parágrafos curtos, nomes canônicos H2 do Output Schema.

### ETAPA 6 · Auto-revisão (9 sweeps)

Leia `reference/sweeps.md`. Nenhum sweep suaviza claim nem insere aviso (regra 8b). 1 clareza; 2 cobertura de VOC (60% ou mais das top 20, literais ou parafraseadas) com o gate de vocabulário (`words_absent[]` proibido, `saturated_in_market` fora de headline, ao menos um `labels[]` na peça); 3 especificidade Hopkins; 4 fluxo Sugarman com o em-dash check acionável (zero em headline, no máximo 2 em copy longa, reescrever e re-contar); 4.5 dieta de copy (proposta de corte mostrada ao membro antes de aplicar, teste do pilar, re-rodar 2 e 4); 5 objeções; 6 CTAs; 7 originalidade contra claims saturados; 8 força (claim hedged vira claim direto com prova ao lado); 9 markup audit (gate de entrada dos 4 U's, Ideal Prospect e Big Promise, veredito de reescrever o lead e voltar à ETAPA 3, teste da primeira página, camadas de estrutura, 4 emoções, lead de 4 passos, psicologia e oferta, loop Objection → Claim → Proof → Benefit, folha de doze defeitos, tabela de arco). Documente o que mudou em cada sweep.

### ETAPA 7 · Variações pra teste A/B

Leia `reference/variacoes-ab.md`. 3 headlines (da 3C), 2 heros, 2 CTAs e 3 a 5 email follow-up hooks em inglês (material da `retention-engine`), cada um com hipótese; heros e CTAs em `hero.variants[]` e `cta_variants[]`.

## SALVAR

`mkdir -p workspace/[produto]/copy-engine/`. `copy-engine.md` com as seções canônicas de `reference/output-schema.md` (PDP e landing: `## Hero` a `## Email Follow-up Hooks`; advertorial: as 7 seções de `## Advertorial Headline` a `## Reveal + Close` mais `## Urgency/Scarcity` e `## Email Follow-up Hooks`), contendo brief, headlines, página, revisão dos sweeps e variações; `.html` por `python3 tools/render_report.py <md>` (convenções em `.claude/templates/aura-html-components.md`); `dados.json` no schema de `reference/dados-json.md` (`lead_type`, `voc_coverage`, `voc_forced_continue`, espécime, `markup_audit`), lido direto pela `page-design` e pela `page-build`. Depois `python3 tools/manifest.py <slug> complete copy-engine` e `python3 .claude/lib/workspace-index/build_index.py <slug>`. O `dados.json` abre pelo objeto `resumo`, até doze campos curtos com o que a fase seguinte lê de primeira; ele espelha campos que já estão no arquivo e é preenchido por último (formato em `reference/dados-json.md`).

## Mensagem final

Texto integral em `reference/salvar-e-mensagem-final.md`: copy completa, Big Idea, mecanismo aplicado, VOC integrado, objeções quebradas, 3 headlines pra teste; próximo passo 'page' (`page-design`), depois 'build page', 'tracking', 'checkout', 'bônus' e 'retention' (Fase A), e só então os criativos.

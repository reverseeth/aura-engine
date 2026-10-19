---
name: offer-builder
description: Construção da oferta como motor econômico do negócio. Abre perguntando o modelo de estoque (com estoque, sem estoque ou sem estoque com migração), cria o mecanismo único por recombinação validada a partir da competitor-analysis (criação original como complemento), junta o banco de provas, define preço por 3 âncoras, bundles, assinatura com desconto invertido, bump e upsell pelo Gate de Complementaridade, stack de valor e bônus, garantia, e passa no gate de oferta irrecusável contra o concorrente principal (vencer em 2 eixos visíveis + 1 diferencial exclusivo, teste "burro de dizer não"). Fecha com unit economics do primeiro pedido e da recompra (margem de contribuição, nunca lucro), AOV e PSM projetados, simulação de budget e 12 sanity checks, pelo cânone unit-economics. Entrega um doc curto com a ficha da oferta primeiro. Use quando o membro disser "offer", "oferta", "montar oferta", "construir oferta", "pricing", "bundle", ou quando market research e competitor analysis estiverem prontos.
---

# Offer Builder · Passo 5 · apelido antigo: 04 <!-- gen:title -->

## Quando usar

Produto definido e pesquisa pronta: falta a estrutura econômica (mecanismo, preço, bundles, bump, upsell, garantia, unit economics) que diz se os ads são viáveis em escala. Sem oferta estruturada, nenhuma copy converte de forma sustentável.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova.

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `market-research/dados.json` (`awareness_distribution`, `sophistication_stage`) e `market-research/market-research.md` (fallback legado `relatorio.md`)
- [ ] `competitor-analysis/competitor-analysis.md` e `competitor-analysis/dados.json`
- [ ] `report_language` de `workspace/profile.md` (default `pt-BR`): conversa e doc nesse idioma, com a linguagem simples da regra 0; copy pública (`offer_stack`, copy do bump, garantia, `no_brainer_lines`) e VOC sempre em inglês US

Arquivo de fase anterior faltando (ES1): (A) rodar a skill faltante agora ou (B) seguir com default genérico marcando `manifest.skipped_preflight`. Manifest ou profile ausentes: oferecer o `setup` inline. Íntegra em `reference/contexto.md`.

## Contexto a carregar

Detalhe em `reference/contexto.md`. Em todo `dados.json` de fase anterior, leia primeiro o objeto `resumo`; abra o arquivo inteiro só na etapa que precisar.

1. `workspace/profile.md` (ferramentas, budget diário) e, se existir, `product-research/dados.json` (`plays[]`, `validated_elements[]`, `winner`)
2. `market-research/`: a oferta é a resposta direta ao market research
3. `competitor-analysis/` (`validated_library`, `top_creatives`, `alternative_solutions`, `claims_saturation`) mais `creative-patterns.json` se existir
4. `sourcing/dados.json` se existir (custo real e rota logística)
5. `brand.md` se existir: o mecanismo reforça o posicionamento; conflito real entre os dois é decisão do membro
6. `finance-engine/dados.json` se existir (`fixed_costs_monthly`, `payback_window_days_measured`, `runway_months`); nunca é pré-requisito
7. O cânone `.claude/lib/unit-economics/README.md` (margem de contribuição não é lucro; primeiro pedido vs recompra; CAC vs CPA e piso de CAC; espiral do ROAS); onde a skill divergir, o cânone vence
8. Base pelo índice: `python3 .claude/lib/kb-index/kb_lookup.py --skill offer-builder --domain <domínio>` (`offer-mechanism`, `offer-pricing-guarantee`, `brand-building-bonus-aov` e as entradas de `finance-projections` desta skill); `best_query` exata com `deep=true`, até 14 buscas adicionais por etapa; as queries embutidas em `reference/` são piso e não contam no teto

## Fluxo da skill

### ETAPA 0 · Modelo de estoque (sempre a primeira pergunta)

Leia `reference/coletar-produto.md`. Pergunte antes de tudo: (A) comprar estoque, (B) sem estoque, com o agente enviando cada pedido, ou (C) começar sem estoque e migrar quando provar. Se `sourcing` ou o profile já respondem, confirme em 1 linha. A resposta muda o custo por unidade, o prazo de entrega, a garantia (sem estoque, conta da entrega), os bundles e o caixa. Grave `fulfillment_model` e `delivery_days_estimate`.

### ETAPA 1 · Coletar informações do produto (3 perguntas)

Mesmo arquivo. Extraia o máximo da página antes de perguntar; `sourcing` fechado já traz o custo real. As 3 perguntas: (1) custos item a item pelo cânone §1, no formato do modelo de estoque (sem estoque, o preço do agente por pedido entregue + o preço da unidade extra no pacote), gravados em `cogs_breakdown`; (2) features, só se não extraiu; (3) produto complementar ("não sei" não trava). Margem de contribuição abaixo de US$ 20 para e avisa depois da ETAPA 5.

### ETAPA 2 · Mecanismo único

Leia `reference/mecanismo-unico.md`. 5 a 7 candidatos: Rota A, recombinação validada da `validated_library` (default: aprimorar um mecanismo validado ou cruzar mecanismo e ângulo validados); Rota B, criação original quando não há mecanismo com evidência de escala ou o mercado está no estágio 5. Filtro S.I.N., score de um a dez em cinco eixos, recomende o maior e grave `mechanism.validation_source`. Documente a lógica do problema (UMP) e da solução (UMS), sem escrever copy.

### ETAPA 2.5 · Banco de provas

Leia `reference/banco-de-provas.md`. Números, estudos, patentes e o que os concorrentes escalados citam, salvos em `research-foundation.json` com `best_numbers`. É munição pra copy, nunca teto: claim que o mecanismo sustenta entra mesmo sem item no banco.

### ETAPA 3 · Estrutura de oferta

Leia `reference/pricing-e-assinatura.md`: preço pelas 3 âncoras (valor, concorrente, economia; divergência acima de 0,40 manda revisar), bundles Solo, Popular (3×) e Best Value (6×), e, em consumível, a arquitetura de assinatura com o desconto invertido. Depois `reference/complementaridade-e-stack.md`: todo componente de AOV passa pelo Gate de Complementaridade (físico primeiro: acessório, more-of-same, downsell), bump e upsell com taxas conservadoras em `aov_levers`, stack com cada entregável nomeado pela regra do `Not: "___"`, `bonuses[]` no enum canônico com `condition`.

### ETAPA 4 · Garantia

Leia `reference/garantia.md`. Tipo pelo estágio de sofisticação, margem, ceticismo do avatar, tipo de produto e modelo de estoque; copy em 2 a 3 frases.

### ETAPA 4.5 · Oferta irrecusável contra o concorrente

Leia `reference/oferta-irrecusavel.md`. Tabela lado a lado com o concorrente principal (preço por dose, bundle, bônus, garantia, frete, prazo). A nossa vence em pelo menos 2 eixos visíveis e tem 1 diferencial que ele não tem; se não, reforce brinde físico, bundle, garantia ou frete e refaça. Teste "burro de dizer não" com as 3 frases: é gate de save. Grave `competitor_comparison`.

### ETAPA 5 · Unit economics

Leia `reference/unit-economics.md`. Tabela 5A do primeiro pedido (é a que governa o spend) e 5B da recompra (obrigatória em consumível ou assinatura); o AOV blended só descreve. Margem de contribuição, nunca lucro; breakeven CAC e ROAS; tetos de CAC pra 2× e 3×; CAC medido no Shopify, não CPA da plataforma; PSM teórico no teto de 2×; piso de CAC de US$ 15 a 25.

### ETAPA 6 · AOV projetado

Leia `reference/aov-e-psm.md`. Taxas conservadoras (bump 20%, upsell 8%), mix 50/35/15, guardrail de canibalização de bundle em net AOV.

### ETAPA 7 · PSM projetado

Mesmo arquivo. PSM com o AOV projetado (recompra estimada não entra), com LTV e PSM explicados como conceitos separados. Abaixo de 1,1, as saídas em ordem: AOV, custo, preço, pivotar; nunca reduzir o teto de CAC por decreto.

### ETAPA 8 · Simulação de budget

Leia `reference/simulacao-de-budget.md`. Pergunte o custo fixo mensal só se não estiver gravado; dois níveis com margem de contribuição e resultado depois dos fixos em linhas separadas; sem os fixos, `result_after_fixed_monthly: null`. Grave `budget_viability`.

### ETAPA 9 · Validação final

Leia `reference/sanity-checks.md`. Os 12 checks; 3 e 12 bloqueiam o save, o 8 é aviso com `margin_warning`. Registre `sanity_checks`.

## SALVAR

Em `workspace/[produto]/offer-builder/`: `offer-builder.md` com a estrutura de `reference/salvar-e-mensagem-final.md` (ficha da oferta primeiro, números numa tabela, detalhes curtos), o `.html` por `python3 tools/render_report.py <md>`, `dados.json` no schema de `reference/dados-json.md` (schema em `.claude/templates/schemas/`; falhou a validação, não salve o `.md`; o objeto `resumo` é preenchido por último) e `research-foundation.json`. Depois `python3 tools/manifest.py <slug> set target_cpa <n> breakeven_roas <n> psm_theoretical <n>`, `python3 tools/manifest.py <slug> complete offer-builder` e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/salvar-e-mensagem-final.md`: mecanismo, modelo de estoque e prazo, onde vence o concorrente, margem por pedido, CPA alvo e viabilidade; convide a revisão e, quando fechar, `'copy'`.

---
name: offer-builder
description: Construção da oferta como motor econômico do negócio. Mecanismo único por duas rotas (recombinação validada a partir da validated_library da competitor-analysis como default, criação original como complemento) com filtro S.I.N. e a lógica de UMP e UMS sem escrever copy, banco de provas, pricing por triangulação de 3 âncoras, bundles, arquitetura de assinatura com o desconto invertido (prêmio no one-time), Gate de Complementaridade pra todo componente de AOV, bump, upsell, stack de valor com cada entregável nomeado pela regra do Not, bônus no enum canônico, garantia, unit economics do primeiro pedido e da recompra em tabelas separadas (margem de contribuição, nunca lucro), AOV e PSM projetados, simulação de budget em 2 níveis e 12 sanity checks, tudo pelo cânone unit-economics. Use quando o membro disser "offer", "oferta", "montar oferta", "construir oferta", "pricing", "bundle", ou quando market research e competitor analysis estiverem prontos.
---

# Offer Builder · Passo 5 · apelido antigo: 04 <!-- gen:title -->

## Quando usar

Quando o membro tem produto definido e pesquisa pronta e precisa da estrutura econômica completa: mecanismo único, preço, bundles, bumps, upsells, garantia e unit economics viáveis pra escalar com tráfego pago. Sem oferta estruturada, nenhuma copy converte de forma sustentável. A oferta é o motor econômico: as decisões daqui dizem se os ads são viáveis em escala.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova.

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `market-research/dados.json` (`awareness_distribution`, `sophistication_stage`) e `market-research/market-research.md` (fallback legado `relatorio.md`)
- [ ] `competitor-analysis/competitor-analysis.md` e `competitor-analysis/dados.json`
- [ ] `report_language` de `workspace/profile.md` (default `pt-BR`): output interno e conversa nesse idioma, com a linguagem simples da regra 0; copy pública (`offer_stack`, copy do bump, promise da garantia) e VOC literal sempre em inglês US; a lógica do mecanismo é documentação interna, e quem escreve a copy dele é a `copy-engine`

Arquivo de fase anterior faltando (ES1): (A) rodar a skill faltante agora ou (B) seguir com default genérico marcando `manifest.skipped_preflight`. Manifest ou profile totalmente ausentes: oferecer o `setup` inline. Íntegra em `reference/contexto.md`.

## Contexto a carregar

Leia nesta ordem (detalhe em `reference/contexto.md`). Em todo `dados.json` de fase anterior, leia primeiro o objeto `resumo` e abra o arquivo inteiro só na etapa que precisar do detalhe; arquivo antigo sem `resumo` se lê inteiro, como antes.

1. `workspace/profile.md` (ferramentas, budget diário) e, se existir, `product-research/product-research.md` mais `product-research/dados.json` (`plays[]`, `validated_elements[]`, `winner`)
2. `market-research/market-research.md` e `market-research/dados.json`: a oferta é a resposta direta ao market research
3. `competitor-analysis/competitor-analysis.md` e `competitor-analysis/dados.json` (`validated_library`, `top_creatives`, `alternative_solutions`, `claims_saturation`) mais `creative-patterns.json` se existir (`recurring_claims` com `market_validated`)
4. `brand.md` se existir: o mecanismo reforça o posicionamento, nunca compete com ele; conflito real entre o posicionamento e o mecanismo mais forte é decisão do membro, não sua
5. `finance-engine/dados.json` se existir: `fixed_costs_monthly` (ETAPA 8), `contribution_margin_pct`, `payback_window_days_measured` e `runway_months` (check 8 da ETAPA 9); ausente, tudo funciona como antes, ela nunca é pré-requisito
6. O cânone `.claude/lib/unit-economics/README.md` (§1 margem de contribuição não é lucro; §2 primeiro pedido vs recompra; §3 CAC vs CPA e piso de CAC; §4 espiral do ROAS); onde a skill divergir, o cânone vence
7. Base pelo índice: `python3 .claude/lib/kb-index/kb_lookup.py --skill offer-builder --domain <domínio desta etapa>` (domínios `offer-mechanism`, `offer-pricing-guarantee`, `brand-building-bonus-aov` e as entradas de `finance-projections` desta skill); `best_query` exata com `deep=true`, no máximo 14 buscas por etapa; as queries embutidas em `reference/` são o mínimo garantido; nunca query genérica nem busca repetida

## Fluxo da skill

### ETAPA 1 · Coletar informações do produto (3 perguntas)

Leia `reference/coletar-produto.md`. Extraia o máximo da página do produto antes de perguntar. Se `sourcing/dados.json` está `closed`, o COGS real já está lá; em `quoting` ou `samples`, estimativa conservadora com `cogs_estimated: true`. As 3 perguntas: (1) COGS item a item pelo stack do cânone §1 (produto entregue, frete, pick & pack, pagamento, taxas, app de assinatura, fee de agência em % do spend, provisão de reembolso; ad spend fica fora, ele é o CAC do PSM), gravado em `cogs_breakdown`; (2) features, só se não extraiu; (3) produto complementar ("não sei" não trava). Decisões automáticas com as flags `*_estimated`. Sanity check depois da ETAPA 5: margem de contribuição abaixo de US$ 20 para e avisa; se o membro segue, `margin_warning: true` no manifest (exceção única: `scaling` com payback e caixa medidos, check 8).

### ETAPA 2 · Mecanismo único

Leia `reference/mecanismo-unico.md` e puxe os sistemas de mecanismo pela `best_query` exata (lista no arquivo). 2A: 5 a 7 candidatos por duas rotas, Rota A recombinação validada como default (A1 aprimorar mecanismo validado subindo um estágio de sofisticação; A2 cruzar mecanismo e ângulo validados) e Rota B criação original quando a `validated_library` não sustenta ou o mercado está no estágio 5; regras transversais (evitar saturação alta, preemptar claim sem dono, `validation_source` em cada candidato); filtro S.I.N. 2B: score de um a dez em diferenciação, credibilidade, memorabilidade, expandibilidade e match com awareness. 2C: recomende o maior score com justificativa e grave `mechanism.validation_source`. 2D: documente a LÓGICA de UMP e UMS e a externalização de culpa, sem escrever copy.

### ETAPA 2.5 · Banco de provas

Leia `reference/banco-de-provas.md`. Busca curta (estudos e o espelho PMC, comunicados, patentes, o que os concorrentes escalados citam), um item por prova no formato do arquivo, salvo em `offer-builder/research-foundation.json` com `best_numbers`. É munição pra copy, nunca teto.

### ETAPA 3 · Estrutura de oferta

Leia `reference/pricing-e-assinatura.md` e puxe os sistemas de pricing e de assinatura (listas no arquivo). Preço por triangulação (value, competitor, economics); divergência `(máx − mín) ÷ mediana` acima de 0,40 manda revisar. Bundles Solo, Popular (3×) e Best Value (6×). Produto consumível decide a arquitetura de assinatura (`subscription_first`, `onetime_plus_sub_no_reorder`, `no_subscription`) com o desconto invertido: o assinante paga o preço-base e o one-time sobe ~15% (`onetime_premium_pct`), revalidando as âncoras. Depois leia `reference/complementaridade-e-stack.md`: todo componente de AOV passa pelo Gate de Complementaridade (more-of-same, consumption chaining, aceleração de resultado, problema adjacente; fora disso, reprovado; sem candidato externo, more-of-same sempre existe); bump e upsell com taxas conservadoras, registrados em `aov_levers`; stack de valor com cada entregável nomeado pela regra do `Not: "___"`; `bonuses[]` no enum canônico com `condition` obrigatória.

### ETAPA 4 · Garantia

Leia `reference/garantia.md` e puxe os sistemas de garantia (lista no arquivo). Escolha o tipo pelo estágio de sofisticação, pela margem, pelo ceticismo do avatar e pelo tipo de produto; escreva a copy em 2 a 3 frases.

### ETAPA 5 · Unit economics

Leia `reference/unit-economics.md` e puxe os sistemas de unit economics (lista no arquivo). Duas tabelas separadas: 5A primeiro pedido (uma linha por variação; é a que governa spend) e 5B recompra (obrigatória em consumível ou assinatura); 5C AOV blended só descreve, nunca decide. Fórmulas: custo variável total com todos os itens do `cogs_breakdown`; margem de contribuição, nunca lucro; `weighted_margin_per_order` como denominador canônico; breakeven CAC e ROAS; tetos de CAC pra 2× e 3×; CAC do Shopify, não CPA de plataforma (`cac_basis`); PSM teórico = LTV ÷ (CAC + COGS) no teto de 2×; piso de CAC de US$ 15 a 25.

### ETAPA 6 · AOV projetado

Leia `reference/aov-e-psm.md`. Taxas de aceitação realistas (bump 20% e upsell 8%, conservadoras), mix baseline 50/35/15, benchmarks de categoria e o guardrail de canibalização de bundle em net AOV.

### ETAPA 7 · PSM projetado

Mesmo arquivo. PSM com o AOV projetado como LTV-proxy (recompra estimada não entra); explique LTV e PSM como conceitos separados e diga por que o custo é CAC e não CPA. Abaixo de 1,1, as saídas em ordem: AOV, COGS, preço, pivotar; nunca reduzir o teto de CAC por decreto.

### ETAPA 8 · Simulação de budget

Leia `reference/simulacao-de-budget.md`. Pergunte o custo fixo mensal (não pergunte o que já está gravado na `finance-engine` ou no manifest), monte a tabela nos dois níveis com margem de contribuição e resultado após custos fixos como linhas distintas; a palavra lucro só na última linha e só com os fixos informados; sem eles, a frase inteira no relatório e `result_after_fixed_monthly: null`. Grave `budget_viability`.

### ETAPA 9 · Validação final

Leia `reference/sanity-checks.md`. Os 12 checks, com a alternativa por payback medido no check 8; registre `sanity_checks` como total, passed e failed. Os checks 3 e 12 bloqueiam o save; o 8 é aviso com `margin_warning`. No relatório, as checagens viram afirmações do que está validado.

## SALVAR

Todo relatório `.md` ganha `.html` por `python3 tools/render_report.py <md>`. Em `workspace/[produto]/offer-builder/`: `offer-builder.md` (seções listadas em `reference/salvar-e-mensagem-final.md`, só o resultado), `dados.json` no schema de `reference/dados-json.md` (schema em `.claude/templates/schemas/`; se falhar validação, não salve o `.md`) e `research-foundation.json`. Depois `python3 tools/manifest.py <slug> set target_cpa <n> breakeven_roas <n> psm_theoretical <n>` e `python3 tools/manifest.py <slug> complete offer-builder`; então `python3 .claude/lib/workspace-index/build_index.py <slug>`. O `dados.json` abre pelo objeto `resumo`, até doze campos curtos com o que a fase seguinte lê de primeira; ele espelha campos que já estão no arquivo e é preenchido por último (formato em `reference/dados-json.md`).

## Mensagem final

Íntegra em `reference/salvar-e-mensagem-final.md`. Primeira versão da oferta: mecanismo e rota, PSM projetado, viabilidade pro budget, margem de contribuição por pedido (e a frase sobre os fixos quando não informados); convide a revisão (o nome gruda, pricing e stack, garantia) e, quando fechar, `'copy'`.

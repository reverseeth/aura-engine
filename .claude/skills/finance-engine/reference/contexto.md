# Finance Engine · Referência: Índice e cânone, quando usar, idioma, pré-flight e contexto a carregar

> O texto integral das notas de índice e de cânone, do quando usar (os dois momentos naturais, o que a skill responde e o que ela não faz), da regra de idioma, do pré-flight com o escape quando falta a offer-builder e da lista completa do contexto a carregar (manifest, offer-builder, ad-analysis, scale-engine, retention-engine, rodadas anteriores e as laterais). Abra antes da ETAPA 1.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (domínio `finance-projections`, mapa skill→domínio no README). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica.
>
> **Cânone que governa esta skill:** `.claude/lib/unit-economics/README.md`. Ele já declara a `finance-engine` como **dona do modelo completo** (§5). Esta skill **referencia** o cânone — não redefine margem de contribuição, first order vs repeat order, CAC vs CPA nem a espiral do ROAS. Onde o texto daqui divergir do cânone, **o cânone vence**, e a divergência é bug desta skill.

## Quando Usar

Quando a pergunta é sobre o **negócio inteiro como máquina financeira**, não sobre um pedido nem sobre um ad set. Gatilhos: "finance", "finanças", "números", "projeção", "quanto vou faturar", "fluxo de caixa", "quanto preciso de capital", "meu negócio dá lucro", "quanto posso gastar em ads", "quanto tempo meu caixa aguenta".

**Não é fase do pipeline — é skill de consulta, como a `consistency-audit`.** Dois momentos naturais:

- **Logo depois da `offer-builder` (Modo A):** "a oferta que acabei de montar fecha a conta do negócio?" A `offer-builder` responde por pedido; a `finance-engine` responde por mês, com o custo fixo dentro.
- **A qualquer momento depois do lançamento (Modo B):** com mês fechado na mão, medir de verdade — alavancas, cohorts, payback, caixa. Recorrente por natureza: o banking sheet é ritual semanal, a calibragem de cohort é mensal, a revisão de LTV é semestral.

**O que esta skill responde e nenhuma outra respondia:** qual é minha margem de contribuição, qual é meu piso de CAC, quanto tempo leva meu payback, quanto caixa preciso pra rodar 90 dias, e o que acontece se eu mexer numa alavanca.

**O que ela NÃO faz:** não desenha oferta (`offer-builder`), não decide budget de ad set nem estrutura de campanha (`ad-strategy`/`scale-engine`), não classifica criativo (`ad-analysis`). Ela entrega o **número** que essas skills consultam.

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. Copy consumidor-final não existe nesta skill — ela não produz nada que vá pro consumidor.

### Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `workspace/[produto]/offer-builder/dados.json` existe — é a fonte do **stack de custos variáveis** (`cogs_breakdown`, 8 campos) e do AOV esperado
- [ ] **Modo B adicionalmente:** existe pelo menos **1 mês fechado** com ad spend do período E contagem de clientes novos do Shopify (`new customer = TRUE`). Sem os dois, o modo é A — não force B com dado pela metade

Se `offer-builder/dados.json` faltar, não aborte seco (rule `emergency-escape-paths.md` ES1). Ofereça **(A)** rodar a skill `offer-builder` agora, **OU (B)** prosseguir pedindo direto ao membro o AOV e o stack de custos variáveis item a item, marcando `manifest.skipped_preflight += ["offer-builder/dados.json"]` e avisando no output que recomenda re-executar depois da `offer-builder`.

### Contexto a carregar

1. `workspace/profile.md` — stage e budget declarado (define linguagem e apetite; ver `member-stage-awareness.md`)
2. `workspace/[produto]/manifest.json` — em especial **`manifest.fixed_costs_monthly`** (campo canônico já existente no schema; escrito pelo membro através da `offer-builder`, `ad-analysis`, `scale-engine` ou desta skill). Se existir, **use e confirme**; não pergunte de novo o que já está gravado
3. `workspace/[produto]/offer-builder/dados.json` — leia:
   - **`cogs_breakdown`** (8 campos, todos em dinheiro POR PEDIDO): `product_delivered`, `shipping_to_customer`, `pick_pack`, `payment_processing`, `taxes_and_duties`, `subscription_app_fee`, `agency_fee_variable`, `refund_chargeback_provision`
   - **`unit_economics`**: `weighted_margin_per_order` (denominador de margem canônico de todo o framework), `contribution_margin_pct`, `breakeven_cpa`, `breakeven_roas`, `target_cpa_primary_2x/3x`, `cac_basis`, `repeat_order{}`, `aov_blended`
   - **`pricing.aov_expected`** e **`budget_viability.fixed_costs_monthly`** (pode estar `null` — é exatamente o buraco que esta skill fecha)
4. `workspace/[produto]/ad-analysis/dados.json` **(se existir)** — spend real, CPA real, ROAS real, AOV real, `psm_real`. É a matéria-prima do Modo B
5. `workspace/[produto]/scale-engine/dados.json` **(se existir)** — `cash_flow.cash_gap_projected` e `fixed_cost_gate` da última rodada de escala. A `scale-engine` estima caixa sozinha hoje; aqui o número é recalculado com o fixo dentro e devolvido pra ela
6. `workspace/[produto]/retention-engine/dados.json` **(se existir)** — take rate de assinatura e sinais de recompra, que alimentam a alavanca de % de recorrentes
7. Rodadas anteriores desta skill em `workspace/[produto]/finance-engine/` — comparar premissas com o realizado é metade do valor do Modo B
8. **Skills laterais (se existirem — leitura aditiva, nunca pré-requisito):**
   - `promo-engine/dados.json` → janela promocional fechada no período: o mês da janela entra em `monthly_notes[]` automaticamente ("promoção no site inteiro") e o cohort de nov/dez (ou da janela) é marcado pra **não calibrar o decay** sem a nota — cohort de promo tem LTV atípico e compará-lo com mês normal quebra o modelo
   - `team-engine/dados.json` → `payroll.current_monthly_total` (ou `payroll_delta_monthly`, o delta de contratação planejada): entra nos custos fixos do monthly model — contratação nova SEM atualizar o fixo é exatamente o furo que o Modo A existe pra fechar
   - `marketplace-engine/dados.json` → `channels[].fees_and_commissions` (fees e comissões por canal) (Amazon/TikTok Shop/afiliados): comissão é **custo variável por pedido daquele canal** — quando houver receita de marketplace no período, o stack de variáveis do canal é montado à parte (a margem blended esconde canal deficitário)

---
name: finance-engine
description: Engine financeira da marca, dona do modelo completo do cânone de unit economics (4 alavancas, cohorts, ciclo de caixa). Roda em dois modos decididos pelos dados, sem perguntar mais que o necessário. Modo A, planejar sem histórico (monthly model, cobertura do fixo, piso de CAC, caixa pra 90 dias, benchmarks DTC). Modo B, medir com meses fechados (4 alavancas, cohorts e LTV medido, payback, teto de escala, stack de float, banking sheet). É a skill que calcula a espiral do ROAS e publica o breakeven_roas_with_fixed que a ad-analysis e a scale-engine consultam antes de recomendar qualquer corte de spend. Nunca chama de lucro um número que não subtraiu custo fixo; nunca estima custo fixo, CAC real nem contagem de clientes novos, pede. Use quando o membro disser "finance", "finanças", "números", "projeção", "quanto vou faturar", "fluxo de caixa", "quanto preciso de capital", "meu negócio dá lucro", "quanto posso gastar em ads", "payback", "runway".
---

# Finance Engine · Lateral · apelido antigo: 15 <!-- gen:title -->

## Quando usar

Quando a pergunta é sobre o negócio inteiro como máquina financeira, não sobre um pedido nem sobre um ad set. Skill de consulta, com dois momentos naturais: logo depois da `offer-builder` (Modo A, a oferta fecha a conta do mês com o custo fixo dentro?) e a qualquer momento depois do lançamento, com mês fechado na mão (Modo B, medir de verdade, com ritual semanal, mensal e semestral). Entrega o número que a oferta, a análise de ads e a escala consultam; não desenha oferta nem decide budget. O cânone `.claude/lib/unit-economics/README.md` governa; onde esta skill divergir, o cânone vence.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` existe.
2. `offer-builder/dados.json` existe (stack de custos variáveis, `cogs_breakdown` com 8 campos, e AOV esperado); faltando, escape ES1: (A) rodar a `offer-builder` agora ou (B) pedir AOV e stack item a item marcando `skipped_preflight`.
3. Modo B só com pelo menos 1 mês fechado com ad spend do período e contagem de clientes novos do Shopify; sem os dois, o modo é A.

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`); esta skill não produz copy consumidor-final.
2. `profile.md` (stage e budget), `manifest.fixed_costs_monthly` (se existir, use e confirme), `offer-builder/dados.json` (`cogs_breakdown`, `unit_economics`, `pricing.aov_expected`, `budget_viability`) e, se existirem, os `dados.json` da `ad-analysis`, da `scale-engine` e da `retention-engine`, rodadas anteriores desta skill e as laterais `promo-engine`, `team-engine` e `marketplace-engine` (leitura aditiva). Lista integral em `reference/contexto.md`.
3. As quatro regras que não se negociam (`reference/regras-e-sistemas.md`): nunca chamar de lucro o que não subtraiu custo fixo (só `operating_income` merece o nome); CAC é spend ÷ clientes novos do Shopify, nunca CPA de plataforma; a espiral do ROAS é conta desta skill; custo fixo, CAC real e clientes novos nunca se estimam, faltando vão pra `pending_inputs[]`.
4. Base pelo índice (domínio `finance-projections`): `python3 .claude/lib/kb-index/kb_lookup.py --skill finance-engine --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas por etapa; o mínimo dos dois modos e o adicional do Modo B estão em `reference/regras-e-sistemas.md` com as queries exatas; nunca query genérica nem busca repetida.

## Fluxo da skill

ETAPAs 1 a 6 e 12 a 14 rodam nos dois modos; ETAPAs 7 a 11 são só do Modo B e são puladas em silêncio sem histórico (sem seção vazia no relatório).

### ETAPA 1 · Detectar o modo e completar só o que falta

Leia `reference/modo-e-inputs.md`. O modo é decidido pelos dados: nenhum mês fechado com spend e clientes novos é Modo A; 1 a 2 meses é Modo B com cohort não calibrado; 3 ou mais é Modo B calibrado. Grave `mode` e `mode_reason`; nunca rode o Modo B com número inventado. Pré-popule tudo dos artefatos antes de perguntar; depois, numa única mensagem, peça só o que não vive em arquivo: custo fixo mensal e caixa disponível nos dois modos; clientes novos do Shopify, ad spend total, curva de LTV se houver e `payout_lag_days` no Modo B.

### ETAPA 2 · Monthly model (o resultado do mês linha a linha)

Leia `reference/monthly-model.md`. Fixos em dinheiro, variáveis como % do AOV (teste: se a receita dobra, o custo dobra?). Tabela na sequência do cânone, sem pular linha, da receita ao resultado operacional (`null` enquanto os fixos forem `null`). Destaque `gross_margin_needed_to_exist` (o próprio fixo) e `revenue_at_gross_margin_to_exist` (fixo ÷ margem bruta %).

### ETAPA 3 · Margem de contribuição e ponto de cobertura do fixo

Leia `reference/margem-e-piso-de-cac.md`. Publique `contribution_margin_monthly`, `fixed_cost_coverage_ratio` (abaixo de 1,0 a operação consome caixa, por mais bonito que esteja o ROAS) e `revenue_to_cover_fixed` (fixo ÷ margem de contribuição %). Separe first order de repeat order sempre, com `unit_economics` e `unit_economics.repeat_order` da `offer-builder`: o primeiro pedido carrega o CAC e os fees de spend, a recompra não.

### ETAPA 4 · Piso de CAC e checagem do CPA-alvo

Mesmo arquivo. Piso físico do Meta em escala entre 15 e 25 dólares; abaixo disso, desconfie da atribuição. Três checagens: `cac_max_first_order` = `weighted_margin_per_order`; o CPA-alvo da `offer-builder` (2x e 3x) é alcançável contra o piso (abaixo do piso o problema é AOV, não mídia); AOV sustenta tráfego pago. Ordem de ataque no vermelho: CAC, LTV, COGS, AOV; COGS acima de 30% é teto de longo prazo.

### ETAPA 5 · A espiral do ROAS (o número que a `ad-analysis` e a `scale-engine` consultam)

Leia `reference/espiral-do-roas.md`; é a razão principal de a skill existir. Fórmulas do arquivo com os números do membro: `breakeven_roas_with_fixed` = (1 + fixos ÷ spend mensal) ÷ `margin_rate`, que cai conforme o spend sobe, e `spend_to_breakeven_with_fixed`. Linha divisória: ROAS acima do breakeven de variável, cortar aumenta o prejuízo (a saída costuma ser subir spend aceitando ROAS menor); abaixo dele, cortar é certo. Gate de saída: fixos conhecidos, publique `breakeven_roas_with_fixed`, `spend_to_breakeven_with_fixed`, `verdict` e `cut_spend_recommendation_allowed`; fixos desconhecidos, `null`, `verdict: "blocked_pending_fixed_costs"`, `cut_spend_recommendation_allowed: false` e a recomendação vira pergunta. É o contrato com a `ad-analysis` e a `scale-engine`: quando este arquivo existe, nenhuma das duas corta spend por queda de ROAS sem ler daqui.

### ETAPA 6 · Caixa pra rodar 90 dias

Leia `reference/caixa-90-dias.md`. `cash_needed_90d` = spend diário × `payout_lag_days` × 1,3 + fixo × 3 + desembolso de estoque − margem de contribuição acumulada projetada em 90 dias. `payout_lag_days` é campo do membro (loja nova ou primeiro pico: 7 a 14 dias, conferindo reserva rolante). Publique `runway_months` = caixa ÷ burn mensal. Guard-rails do arquivo sempre no relatório (float não conserta oferta quebrada).

### ETAPA 7 · [Modo B] As 4 alavancas

Leia `reference/alavancas.md`. AOV, CAC por cliente novo pago, ad spend e % de recorrentes. Baseline com o mês fechado e simulação de uma alavanca por vez, com o delta de margem de contribuição e de resultado operacional; ranqueie e nomeie `highest_impact_lever`. No vermelho, diagnóstico por eliminação; nunca recomende as quatro ao mesmo tempo.

### ETAPA 8 · [Modo B] Cohorts com decay factor e LTV medido

Leia `reference/cohorts.md`. Tabela por cohort (colunas do arquivo; `total_margin` é a coluna de decisão). Decay calculado da série real ou assumido em cerca de 0,8, com `decay_source` declarado; calibragem a cada mês fechado até 3 a 5 meses, depois congelada e revista a cada 6 meses. Aviso obrigatório: erro de 5% inverte o resultado; sem 3 meses reais, payback modelado no mês 2. Marca sem cohort: `calibrated: false`, nunca curva inventada. LTV é dólares, não retenção; pico de churn por volta do dia 45, que a `retention-engine` ataca.

### ETAPA 9 · [Modo B] Payback, first-order profitability e teto de escala

Leia `reference/payback-e-teto-de-escala.md`. `first_order_profitable` = CAC real abaixo de `cac_max_first_order`; lucrativo no primeiro pedido, escale até perto do zero a zero. Janela de payback de referência de 90 dias, com `payback_window_days_measured` lido do `total_margin`; perder no primeiro pedido é decisão só com LTV medido e caixa que aguenta. Taxa de aumento do CAC (referência 4:1, ou a real por mil dólares de spend) e `scale_ceiling_monthly_spend`, o plateau do resultado operacional, escrito de forma acionável.

### ETAPA 10 · [Modo B] Ciclo de conversão de caixa (o stack de float)

Leia `reference/float-e-banking-sheet.md`. Faturamento da Meta (net 45, modele com 44), serviço de pagamento de boletos, cartão de prazo longo (net 60): cerca de 105 dias de float a cerca de 1,4% líquido. Recalcule `cash_needed_90d` com e sem o stack e mostre as duas linhas; extensão ao fornecedor; guard-rails repetidos no relatório.

### ETAPA 11 · [Modo B] Banking sheet semanal e notas mensais

Mesmo arquivo. Banking sheet com uma linha por dia (colunas do arquivo), ritual semanal de 45 minutos em todas as contas, transferência própria não conta; template em `banking-sheet.csv`. `monthly_notes[]` com mês, evento e efeito pra todo mês fora da curva. Camada contábil ausente vira pendência com efeito prático.

### ETAPA 12 · Stress test padrão

Leia `reference/stress-test.md`. CAC +20%, LTV −20% e COGS +5 pontos, cada um com margem de contribuição, resultado operacional e `survives`; no Modo B, mais reembolso +2 pontos e repasse atrasado de 7 a 14 dias. Cenário que derruba o resultado abaixo de zero sai em destaque em qualquer recomendação de escalar.

### ETAPA 13 · Benchmarks e veredito

Leia `reference/benchmarks-e-sanidade.md`. Referências DTC (tabela do arquivo), Four Quarter Accounting ao lado da repartição real, a exceção de COGS alto com margem absoluta grande. Veredito em linguagem direta com uma alavanca única, e o memo de decisão em quatro blocos (por quê, o quê, como, agora e depois) quando a decisão custa dinheiro.

### ETAPA 14 · Checagens de sanidade

Mesmo arquivo: os doze itens (nenhum "lucro" sem fixo, `cac_basis` sempre `shopify_new_customer`, nada estimado nos três campos, first e repeat separados, só o resultado no doc, entre outros). Falha em qualquer um bloqueia o `.md`.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/finance-engine/`; `finance-engine.md` nos treze blocos da ordem do arquivo (os do Modo B só no Modo B; pendências sem narrar tentativas), `finance-engine.html` por `python3 tools/render_report.py workspace/[produto]/finance-engine/finance-engine.md`, `banking-sheet.csv` só no Modo B e `dados.json` no schema de `reference/dados-json.md` (o contrato lido pela `offer-builder`, `ad-strategy`, `ad-analysis`, `scale-engine` e `retention-engine`; caminhos exatos em `reference/contrato-de-leitura.md`). Manifest pelo script: `python3 tools/manifest.py <slug> complete finance-engine`, `set fixed_costs_monthly` quando o membro informar e `set finance` com o resumo de oito campos do arquivo; nunca escrever `manifest.stage`; `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`: primeira versão é draft e melhora a cada mês fechado. Quatro versões: Modo A com os fixos, Modo A sem os fixos, Modo B e input crítico faltando (o que falta e o que destrava).

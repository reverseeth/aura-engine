# Offer Builder · Referência: Unit economics do primeiro pedido e da recompra (ETAPA 5)

> Os sistemas nomeados de unit economics, a separação entre primeiro pedido e recompra (tabelas 5A e 5B, AOV blended 5C) e as fórmulas: custo variável total, margem de contribuição (nunca lucro), breakeven CAC e ROAS, tetos de CAC, a diferença CAC vs CPA, o PSM teórico e o piso de CAC. Abra na ETAPA 5.

### ETAPA 5 — Unit Economics (Tabela Completa)

**Puxe estes SISTEMAS NOMEADOS de unit economics antes de calcular (rode a `best_query` de cada — vale também pra ETAPAs 6/7):**
- **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS golden ratio growth`) — o golden ratio que substitui ROAS; é o núcleo das ETAPAs 5-7.
- **Unit Economics Hierarchy (CPA vs CAC, GPT)** (rode `unit economics CPA vs CAC blended CPA GPT net profit hero offer`) — separa CPA de CAC e define o denominador correto de margem.
- **Hormozi LTGP:CAC Ratio** (rode `Hormozi LTGP CAC ratio 3 to 1 lifetime gross profit acquisition cost`) — alvo 3:1 de lifetime gross profit sobre CAC.
- **Client Financed Acquisition (CFA)** (rode `Hormozi client financed acquisition front end covers CAC backend pure profit`) — front-end (bump/upsell) cobre o CAC, backend vira lucro.
- **Pricing Leverage Math (5% Price = 50% Profit)** (rode `pricing leverage 5 percent price increase 50 percent profit thin margin`) — quando a margem é fina, mexer no preço move o lucro desproporcionalmente (input pra ETAPA 7 quando PSM < 1.1).

**Primeiro pedido e recompra são DUAS economias diferentes e vão em DUAS tabelas separadas** (cânone §2). Misturar as duas numa média esconde exatamente o que decide o negócio: o primeiro pedido carrega o CAC inteiro, a recompra não carrega nenhum. Um produto pode ser deficitário na primeira compra e excelente na segunda — e a decisão de spend depende de qual dos dois você está olhando.

O que cai em cada lado:

| Componente | Primeiro pedido | Recompra |
|---|---|---|
| CAC | carrega ele inteiro | não carrega |
| Fee de agência atrelado a % do ad spend | sim | não |
| Upsell pós-compra | infla o AOV e não se repete | não existe |
| Brinde de entrada, bundle de introdução, desconto de primeira compra | sim, e piora a margem | não |
| Kit/peça cara que só vai na 1ª remessa | sim (a marca de lâmina manda o cabo na primeira e só lâminas depois) | não |
| Resultado típico | AOV maior, margem pior | AOV possivelmente menor, margem bem melhor |

**5A — Economia do PRIMEIRO PEDIDO** (uma linha por variação da oferta — é esta tabela que governa a decisão de spend):

| Variação | AOV | COGS entregue | Pick&Pack | Frete | Pagamento | Taxas | App assinatura | Fee agência variável | Provisão reembolso | Custo variável total | Margem contrib. $ | Margem contrib. % | Breakeven ROAS | Teto de CAC (2× ROAS) | Teto de CAC (3× ROAS) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Solo | | | | | | | | | | | | | | | |
| 3-pack | | | | | | | | | | | | | | | |
| 6-pack | | | | | | | | | | | | | | | |
| Solo + Bump | | | | | | | | | | | | | | | |
| 3-pack + Bump | | | | | | | | | | | | | | | |
| Solo + Upsell | | | | | | | | | | | | | | | |

(A coluna "Provisão reembolso" fica vazia quando a devolução já foi descontada do AOV como net AOV na ETAPA 6 — a provisão conta uma vez só, e o relatório diz em qual dos dois lugares ela está.)

**5B — Economia da RECOMPRA** (obrigatória quando o produto é consumível ou tem assinatura; produto sem recompra prevista → grave `repeat_order: null` e diga isso no relatório em uma linha):

| Item | Valor |
|---|---|
| AOV da recompra (sem upsell pós-compra, sem kit de entrada) | |
| Custo variável total (sem CAC, sem fee de agência atrelado a spend) | |
| Margem de contribuição $ | |
| Margem de contribuição % | |

A diferença costuma ser grande o bastante pra inverter a leitura da oferta: no mesmo pedido de US$ 100 do exemplo canônico, a margem de contribuição do primeiro pedido é US$ 18,70 (18,7%) e a da recompra é US$ 60,70 (60,7%).

**5C — AOV blended** (só quando as duas tabelas existem; é o número que descreve a operação inteira, nunca o que decide spend):

`AOV blended = (AOV 1ª ordem × nº de 1ªs ordens + AOV de recompra × nº de recompras) ÷ total de transações`

Grave como `unit_economics.aov_blended`. **Nenhum cálculo de breakeven, teto de CAC ou PSM usa o blended** — todos usam a tabela 5A. O blended existe pra o membro entender o painel dele, não pra decidir mídia.

### Unit Economics — Fórmulas

Receita por pedido:
- AOV = Average Order Value (Preço × unidades médias por pedido)

Custo variável por pedido:
- Custo variável total = COGS entregue + Frete + Pick&Pack + Processamento de pagamento (%) + Taxas/Impostos + App de assinatura (0,5–1%, se houver) + Fee de agência (% do spend, se houver) + Provisão de reembolso/chargeback (se não estiver descontada no net AOV) — **os itens do `cogs_breakdown` da ETAPA 1, nenhum de fora** (omitir qualquer um infla a margem e distorce breakeven_cpa/teto de CAC/PSM). Ad spend fica FORA desta soma: ele entra como CAC no PSM.

Margem de contribuição por pedido:
- **Margem de contribuição $ = AOV − Custo variável total**

> **Este número NÃO é lucro** (cânone §1). Lucro = margem de contribuição − custos fixos. Toda a ETAPA 5 opera antes dos custos fixos, e por isso nenhum número desta etapa pode ser rotulado como "lucro" — nem na tabela, nem no relatório, nem na conversa com o membro.

> **Denominador canônico:** toda a unit economics usa `weighted_margin_per_order` (margem de contribuição média ponderada por AOV do PRIMEIRO PEDIDO, considerando bumps + upsells) como denominador. Quando a oferta não tem bump/upsell, ele iguala `margin_per_unit`. Os campos `breakeven_cpa`, `target_cpa_primary_2x/3x` e `breakeven_roas` do `offer-builder/dados.json` derivam SEMPRE de `weighted_margin_per_order` (ver "Nota sobre nomenclatura" no Output Schema). A Skill `ad-analysis` lê assim.

**Breakeven CAC / Breakeven ROAS** (o ponto de empate — empate contra os custos variáveis, ainda antes dos fixos):
- Breakeven CAC = weighted_margin_per_order
- Breakeven ROAS = AOV / weighted_margin_per_order
- Exemplo: AOV $118, weighted_margin_per_order $72 → Breakeven CAC = $72, Breakeven ROAS = 118/72 = 1.64
- Significa: precisa gerar $1.64 de receita para cada $1 em ads só para empatar

**Teto de CAC** (custo máximo de aquisição para N× ROAS desejado):
- Teto de CAC para ROAS N = weighted_margin_per_order / N
- Exemplo: weighted_margin $72, quer 2× ROAS → teto = 72/2 = $36
- Para 3× ROAS → teto = 72/3 = $24
- Sanidade: teto (2×) < breakeven_cac SEMPRE ($36 < $72).

> **CAC ≠ CPA — e é aqui que a diferença aparece** (cânone §3). **CPA de plataforma** é o custo por compra que o Meta reporta, e ele conta conversões atribuídas pela própria plataforma, incluindo compras de clientes que já existiam. **CAC** é `ad spend ÷ clientes NOVOS`, e o número de clientes novos vem do **Shopify** (`new customer = TRUE`), não do gerenciador de ads. Numa loja com recompra, o CPA de plataforma é sempre menor que o CAC real — o denominador dele está inflado com gente que já era cliente. Decisão de aquisição (é este o caso destes tetos) usa **CAC**; misturar os dois torna o modelo fake.
>
> Os campos JSON continuam com os nomes `breakeven_cpa` e `target_cpa_primary_2x/3x` porque são contrato de leitura das skills `checkout-aov`/`ad-strategy`/`ad-analysis` — **o nome é legado, o conteúdo é teto de CAC**. Registre a base explicitamente em `unit_economics.cac_basis: "shopify_new_customer"` pra que a comparação com o número medido não seja feita contra o CPA do gerenciador.

**PSM — Profitable Scaling Margin** (o "golden ratio" que substitui ROAS na decisão de escala; é a **MESMA fórmula** que a skill `ad-analysis` grava como `psm_real`, pra que o teórico do offer e o real medido sejam comparáveis — a skill `scale-engine` lê os dois):
- **PSM = LTV / (CAC + COGS)** — LTV = AOV projetado do primeiro pedido quando não há histórico de recompra (proxy); **COGS = somatório de TODOS os itens do `cogs_breakdown`, exatamente como a Skill `ad-analysis` define — nunca só o custo do produto**; **CAC = custo por cliente NOVO que o membro aceitaria pagar (base Shopify, não CPA de plataforma)**. Avalie no **teto de 2×**, NÃO no breakeven (no breakeven, PSM = 1.0 por definição: AOV = weighted_margin + COGS = CAC breakeven + COGS).
- Exemplo (mesmos números do exemplo acima): AOV/LTV $118, weighted_margin $72 → COGS (somatório do breakdown) = 118 − 72 = **$46**; CAC-alvo (2×) $36 → PSM = 118 / (36 + 46) = **1.44**.
- Thresholds (idênticos às skills `ad-analysis`/`scale-engine`): **>1.3 escala agressiva · 1.1–1.3 escala estável (+5%) · 1.0–1.1 breakeven · <1.0 não viável**.
- Grave como `psm_theoretical` no `dados.json`. A skill `ad-analysis` grava `psm_real` (mesma fórmula, com o custo de aquisição real medido); a skill `scale-engine` compara os dois.

**Piso de CAC (gate de sanidade — cânone §3):** o leilão tem um chão físico dado por CPM e CTR. No melhor caso realista (CPM ~US$ 10–15, CTR ~3%), o **CAC mínimo em escala fica em US$ 15–25**. Um teto de CAC abaixo disso não é um alvo apertado, é um alvo que não existe: nenhuma operação de 8 dígitos roda com CAC de US$ 15. Se o teto de CAC (2×) da oferta cair abaixo de US$ 25, a oferta não sustenta escala e o caminho é AOV/LTV, não "mídia melhor" — a checagem formal está no check 12 da ETAPA 9. Se o CAC medido depois vier ABAIXO desse piso, desconfie da atribuição antes de comemorar.

**Regra crítica:** o teto de CAC pra 2× ROAS deve ser viável com o budget do membro E acima do piso de US$ 25. Se a margem de contribuição < $15-20, a oferta não sustenta ads a não ser em volume muito alto.

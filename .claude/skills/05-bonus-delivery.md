---
name: bonus-delivery
description: Pipeline de bônus de ECOMMERCE — gera o asset entregável (e-book/guide/checklist em PDF), configura o gift-with-purchase (GWP) na loja, e rastreia access/take-rate. NÃO é bônus de info-product. Tipos primários são os 4 que realmente movem AOV e percepção de valor num DTC: gift-with-purchase, e-book/guide rumo ao dream outcome, free complementary SKU, free gift wrapping (Q4). Use quando o membro disser "bonus delivery", "bônus", "como entregar o bônus", "configurar GWP", ou após a oferta (Skill 04) definir o stack de valor com bonuses[]. Roda em DUAS fases: Fase A (gerar assets + configurar GWP/entrega) ANTES do go-live de ads — bônus prometido na PDP no dia 1 precisa existir no dia 1; Fase B (tracking de take-rate e iteração) PÓS-LAUNCH, junto da Fase B da 13 — e só com campanha de fato ATIVA e pedidos existindo (skill 10 completa ≠ ads no ar).
---

# Bonus Delivery — Bônus de Ecommerce

## O que esta skill faz (e o que NÃO faz)

A **definição** do bônus (qual bônus, valor ancorado, por que entra no stack) acontece na **Skill 04 (offer-builder)** — ela tem o contexto de avatar, margem e AOV. Esta skill **não inventa bônus**: ela lê o que a 04 definiu e **executa**.

O que justifica a 05 como skill standalone é o trabalho operacional que a 04 não faz:

1. **Gerar o ASSET entregável** quando o bônus é digital (PDF do e-book/guide/checklist, com design da marca do membro).
2. **Configurar o GWP na loja** (gift-with-purchase via app ou Shopify Function) — coordenado com a **07d-checkout-aov**.
3. **Disparar o email de entrega** quando o bônus é digital ou condicional — coordenado com a **Skill 13 (retention)**, que é o executor de email.
4. **Rastrear access rate / take-rate** — o KPI que diz se o bônus está agregando valor percebido ou só inflando o stack.

**Posicionamento na ordem — DUAS fases (isso resolve o paradoxo de launch):** o offer_stack da 04 promete os bônus na PDP desde o dia 1 (a 06 imprime literal, a 07b deploya). Um comprador do dia 1 NÃO pode receber promessa de e-book que ainda não foi gerado, nem de brinde que a loja não sabe adicionar ao carrinho. Por isso:

- **Fase A — Launch-readiness (ANTES do go-live de ads, logo depois da 07d):** gerar o asset digital (PDF do e-book/guide), configurar GWP/complementary/gift-wrap na loja (coordenado com a 07d), hospedar o arquivo, garantir o acesso do comprador do dia 1 (link do asset na thank-you page / order status — funciona mesmo antes do flow de email existir) e produzir o payload de email pra Skill 13. **Todo bônus visível na PDP precisa sair da Fase A antes do primeiro ad** — a Skill 09 (consistency audit) verifica isso no gate de launch (promise↔config).
- **Fase B — Tracking e iteração (PÓS-launch, junto da Fase B da 13):** com a campanha ATIVA e pedidos acontecendo (dupla condição do pré-flight), a 05 volta em D+30 pra puxar take-rate/access rate agregados (ETAPA 4) e alimentar a iteração da oferta na 04. (O flow de email de entrega em si já nasce na Fase A da 13, que roda pré-launch — o que é pós-launch aqui é o TRACKING.)

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (mapa skill→domínio no `README.md`, queries exatas em `frameworks.json`). O domínio desta skill é **brand-building-bonus-aov** — o tamanho do domínio é o que o `frameworks.json` disser (fonte da verdade), não um número fixo aqui. Sempre que uma ETAPA mandar "puxar da base", rode `search_knowledge` com a `best_query` NOMEADA do framework relevante daquela fase — **nunca query genérica**.
>
> **Contrato de cobertura (regra 2026-09 do kb-index):** a puxada é cobertura, não amostra. No início de cada ETAPA que consulta a base, enumere no `frameworks.json` TODAS as entradas do domínio cujo `use_in_skill` inclui esta skill; as queries embutidas abaixo são o núcleo mínimo garantido, **nunca o teto** — entrada relevante não-embutida é pra puxar do mesmo jeito ("talvez informa esta etapa?" = puxa). Não repita framework já puxado na sessão. Antes de fechar a ETAPA, confira a lista enumerada: nada relevante fica sem puxar.

## Tipos de bônus

O Aura Engine modela bônus de **ecommerce DTC**, não de info-product. Os 4 tipos PRIMÁRIOS abaixo são os que movem AOV e take-rate numa loja física-de-produto. Cada um tem playbook completo (ETAPA 2). Os tipos de subscription/membership ficam num bloco curto no fim — são caso de borda, não o foco.

### Princípio do stack de 2 bônus (puxado da base)

**Puxe os SISTEMAS NOMEADOS antes de modelar o stack** (rode a `best_query` de cada um):
- **Razor-Blade vs Handle — Bonus Fit Principle** (rode `razor blade vs handle bonus fit natural complement to product`) — sustenta o 1º bônus (fit natural com o produto).
- **Second Fun/Emotional Bonus — Care-Package Principle** (rode `second bonus fun emotional delightful care package t-shirt hoodie offer optimization`) — sustenta o 2º bônus (hit hedônico).
- **Bonus Types Taxonomy — presuppose-success / enables-success / partner cross-promo / course-as-bonus** (rode `bonus types presuppose success enables success graduation gift access partner complementary`) — classifica cada bônus pelo papel psicológico, não pelo formato.

Se a oferta tem **mais de um** bônus, eles trabalham em papéis diferentes:

- **1º bônus (primário):** presupõe sucesso no produto principal. Faz o cliente extrair mais resultado do que comprou (o e-book que ensina a usar, o complementary SKU que potencializa). É o "give away the blade, sell the handle" — fit natural com o produto, razor-blade test.
- **2º bônus (fun/emocional):** o presente que gera empolgação. Não precisa ser racional. Sticker pack, sample size, gift wrapping bonito, um item low-COGS que dá aquele "não acreditei que veio de graça". É o hit hedônico que vira boca-a-boca.

Congruência visual importa: na PDP, "free" deve **aparecer** (imagem do brinde, badge), não só ser texto. Quando o cliente vê os brindes empilhados, o stack ganha força.

## Pré-flight

1. Ler `workspace/profile.md` → `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). Toda doc interna desta skill (.md/.html/.json descritivo) E toda conversa com o membro usam esse idioma. O asset entregável ao consumidor (PDF do e-book, email) é **sempre em inglês** (mercado US), independente do `report_language` — rule 0 do CLAUDE.md.
2. Ler `workspace/[produto]/manifest.json` → detectar `stage` (member-stage-awareness). Influencia recomendação de tipo: **starter** → priorizar e-book/guide (custo zero de produzir) e GWP de baixo COGS; **scaling** → pode sustentar complementary SKU físico e GWP mais robusto.
3. Detectar a FASE — a **Fase B exige DUPLA condição** (skill completa ≠ ads no ar: a 10 cria a campanha em PAUSED):
   - **(1)** `manifest.skills_completed` contém `"10-ad-strategy"`, **E**
   - **(2)** a campanha está de fato ATIVA / há pedidos no período — evidência: o membro confirma que ativou, `11-ad-analysis/dados.json` existe com spend registrado, ou há pedidos no Shopify desde o launch.

   As duas valem E os assets/config de todos os `bonuses[]` existem → **Fase B** (ETAPA 4, tracking). Qualquer outra combinação (10 ausente, campanha ainda em PAUSED, ou bônus sem asset/config) → **Fase A** (ETAPAs 1-3 + config).
4. `04-offer-builder/dados.json` existe com `bonuses[]` preenchido. Pra cada bonus, `type` E `condition` claros (não default "pdf"). Se `condition` estiver ausente (oferta gerada antes do campo existir), inferir: bônus presente no offer_stack da PDP = `unconditional`; GWP com threshold definido = `cart_threshold` — e gravar a inferência de volta no `dados.json` da 04.
5. **Escape path (ES1):** se `04-offer-builder/dados.json` está ausente/corrompido, oferecer (A) re-rodar Skill 04 ou (B) proceder com bônus genérico marcando `manifest.skipped_preflight`. Não abortar seco.

Se `bonuses[]` está vazio mas o membro quer um bônus, **voltar pra 04** — é lá que se decide. A 05 não cria oferta.

## Fluxo da Skill

### ETAPA 1 — Parse dos bonuses definidos na 04

Ler `04-offer-builder/dados.json.bonuses[]`. Schema esperado — este é o **enum canônico** (fonte: Output Schema da Skill 04, reproduzido idêntico lá e aqui):

```json
{
  "id": "bonus-01",
  "name": "nome humano do bônus",
  "description": "1-2 frases: o que é / por que vale",
  "value_anchored": 49,
  "type": "gift_with_purchase | free_complementary_sku | free_ebook | gift_wrapping | digital_guide | discount_code | workbook | checklist | community_access | video_series | consultation_call | trial_extension",
  "format_hint": "in_box | shopify_function | gift_app | pdf | notion | figma | wistia | klaviyo_email | shopify_discount | circle_invite",
  "condition": "unconditional | cart_threshold | tier_specific",
  "delivery_trigger": "post_purchase | on_signup | day_7_post_purchase | on_first_reorder"
}
```

Se o `dados.json` da 04 tiver um `type` fora dessa lista, volte pra 04 e corrija LÁ (não inventar mapeamento local — o enum é único).

Pra cada bonus, identificar o playbook correspondente na ETAPA 2.

### ETAPA 2 — Playbook por tipo (primários)

#### `gift_with_purchase` (GWP) — brinde físico low-COGS acima de threshold

A alavanca de AOV mais direta. Add um item de baixo COGS quando o cart subtotal cruza um threshold.

**Puxe os SISTEMAS NOMEADOS pra calibrar o GWP** (rode a `best_query`):
- **Profit Optimization 4 Categories + AOV Builders (Bundles, Free-Shipping Threshold, Volume Discounts, GWP, Pack Sizes)** (rode `profit optimization four categories AOV builders bundles free shipping threshold volume discount GWP profit per visitor`) — define onde o GWP encaixa no mapa de AOV e a métrica profit/visitor.
- **AOV Money Close + Offer Bump + Add-More-Packages** (rode `AOV money close offer bump add more packages biggest package most popular checkout`) — posiciona o threshold do GWP junto do tier "most popular".
- **3x+ Markup Rule + $60 AOV Floor (Margin Validation for Paid-Traffic Brands)** (rode `3x markup rule 60 dollar AOV floor COGS shipping margin paid traffic CPM fixed`) — sanity check de margem: o brinde low-COGS não pode furar o piso.

**0. Ler `condition` do bonus (da 04) — define a mecânica ANTES de qualquer threshold:**
   - `unconditional` → o brinde foi prometido na PDP a TODO comprador: **auto-add em toda compra** (app/Function SEM threshold). Colocar threshold aqui quebra a promessa da página.
   - `cart_threshold` → seguir os passos 1-2 abaixo (threshold ancorado no AOV). A copy da página DEVE refletir a condição ("FREE over $X") — coordenar com 06/07a.
   - `tier_specific` → o brinde destrava num tier específico (3-pack/6-pack): gatilho por produto/variant do tier, não por subtotal.

**1. Definir o threshold (cart subtotal — só pra `condition: cart_threshold`):** ancorar no AOV. Ler `04-offer-builder/dados.json` (price, offer_stack) e o AOV histórico se existir (manifest ou Stripe). Regra prática: threshold ~10-20% **acima** do AOV atual, pra empurrar o cliente a adicionar 1 item a mais sem ser inalcançável. Se não houver AOV histórico, usar o preço do tier principal × 1.1 como proxy e marcar como teórico.

**2. Sourcing low-COGS:** o brinde precisa ter percepção de valor alta e custo real baixo (sample size do próprio catálogo, item complementar barato, kit emocional). O `value_anchored` na PDP ancora no **varejo real** do item, nunca num "sticker price" inventado (ver Compliance abaixo).

**3. Implementação Shopify (caminho real — NÃO draft order):**
   - **Caminho A — App de gift-with-purchase** (BOLD, Gift Box, Free Gifts BOGO, etc): config no admin do app "free product when cart ≥ $threshold". Mais rápido pra starter, sem código.
   - **Caminho B — Shopify Functions** (cart transform / discount function): regra "add free variant / 100% off quando cart subtotal ≥ threshold". Mais robusto e sem mensalidade de app, mas exige a function publicada na loja. Coordenar com **07d-checkout-aov** (é config de checkout/store, mora lá).
   - **NUNCA** usar draft order pra GWP — não escala, quebra com self-checkout, e não dispara no fluxo normal de compra.

**4. Congruência "free" na PDP:** garantir que o brinde **apareça** visualmente (imagem do gift, badge "FREE GIFT over $X"). Coordenar com a página (07a/07b) — ícone SVG, nunca emoji (rule 7).

**5. KPI = take-rate.** A métrica é quantos % dos pedidos destravam o brinde (escolhem o tier ou cruzam o threshold). Benchmark da base: a escolha do tier full-size (o tamanho cheio, que destrava o brinde) subiu de **30% pra 52%** dos pedidos ao adicionar o GWP; AOV +12%, lucro por visitante +20%. Registrar take-rate no snapshot (ETAPA 4) assim que houver dado.

#### `free_ebook` / `digital_guide` / `workbook` / `checklist` — asset digital rumo ao dream outcome

O e-book/guide que ajuda o cliente a **alcançar o resultado** que o produto promete (não um PDF genérico). Razor-blade fit: o asset faz o cliente ter mais sucesso com o produto → mais retenção e reorder.

**Puxe os SISTEMAS NOMEADOS pra ancorar o asset no dream outcome** (rode a `best_query`):
- **Hormozi Value Equation (Dream Outcome × Perceived Likelihood / Time Delay × Effort & Sacrifice)** (rode `Hormozi value equation dream outcome perceived likelihood time delay effort sacrifice`) — o e-book deve mover ≥1 das 4 variáveis (tipicamente reduzir Time Delay e Effort pra chegar no resultado).
- **Razor-Blade vs Handle (Bonus Fit Principle)** (rode `razor blade vs handle bonus fit natural complement to product`) — o asset só vale se faz o cliente extrair mais do produto principal, não como "PDF qualquer".

**1. Gerar o conteúdo** alinhado ao dream outcome (ler `02-market-research/dados.json` pra VOC e desire, `04-offer-builder/dados.json` pro mecanismo). O e-book é REAL e específico do avatar, não "10 daily tips". Exemplo bom: skincare 45-65 → "The 14-Day Glow Protocol: exactly when to apply, what to pair, what to avoid".

**2. Produzir o PDF:** Markdown → HTML → PDF (weasyprint ou headless Chrome). Design da **marca do membro** (cores/fonte da brand, não do Aura). Conteúdo **em inglês** (consumidor US). Salvar em `workspace/[produto]/05-bonus-delivery/bonuses/[bonus-id]/[bonus-id].pdf`.

**3. Entrega:** link na thank-you page / order status (config da Fase A — é o que garante o acesso do comprador do dia 1, antes do flow de email existir) + link no email post-purchase (ver ETAPA 3, executado pela 13). Asset hospedado em Shopify Files API, S3 ou R2.

**4. KPI = access rate** (% que abre/baixa). Logar na ETAPA 4.

#### `free_complementary_sku` — produto complementar grátis

Um SKU do catálogo que **vai bem com o principal** dado grátis (não um threshold genérico). Funciona como GWP atrelado a um produto específico ("compre o sérum, ganhe o cleanser travel-size").

**1. Confirmar o fit:** o complementary precisa potencializar o resultado do principal (razor-blade). Se for só "outro produto qualquer", questionar o membro.
**2. Implementação:** mesma mecânica do GWP (app ou Function, NÃO draft order), mas o gatilho é o **produto** no cart, não o subtotal. Coordenar com 07d.
**3. In-box vs auto-add:** se o complementary já é estoque físico, pode ser **in-box gift** — documentar pro fulfillment incluir em toda caixa do SKU principal. Se for via cart, app/Function.
**4. KPI = take-rate + attach impact** (sobe o reorder do complementary depois?).

#### `gift_wrapping` — embrulho de presente grátis (Q4)

Bônus sazonal de alto valor percebido e COGS quase zero. Brilha em Q4/gifting season e converte o avatar "comprando pra outra pessoa".

**1. Implementação:** opção de gift-wrap grátis no cart/checkout (cart attribute, line-item property, ou app de gift options). Coordenar com 07d (checkout) — é config de loja.
**2. Fulfillment:** documentar pro fulfillment center: "embrulhar pedidos com a flag gift_wrap". In-box, não digital.
**3. Personalização por persona** (da base — exemplo Original Grain): quem chega de ad de gifting vê a opção de gift-wrap + card em destaque; quem chega de self-purchase, não. Coordenar com a página se houver split de persona.
**4. KPI = attach rate do gift-wrap.**

#### `discount_code` — código de desconto complementar (suporte, não primário)

Code na Shopify Admin pra produto complementar, com expiração (30-60 dias pós-purchase). Único por customer (tag `uniqueCode`) ou compartilhado. Delivery: email + thank-you page com botão copy-to-clipboard. É bônus de **reorder/backend**, não de aquisição.

Como é alavanca de LTV/backend, **puxe o SISTEMA NOMEADO** antes de dimensionar o desconto (rode a `best_query`): **Kennedy Price Minimizers (5 Strategies) + Damaging Admission** (rode `Kennedy price minimizers five strategies compare apples oranges damaging admission`) — pra enquadrar o code como minimizador de preço percebido no reorder, não como erosão de margem.

### ETAPA 2b — Tipos de subscription/membership only (caso de borda)

Estes tipos só fazem sentido pra negócios de **subscription/membership**, não DTC físico padrão. Se o membro vende produto físico one-time, **não recomendar** — geralmente é o domínio errado (info-product) herdado. Playbook curto:

- **`community_access`** — Circle (single-use invite, mais seguro) / Discord / Skool. Link no email post-purchase. Só se a marca opera comunidade ativa.
- **`video_series`** — Wistia/Vimeo com password, gated page Shopify. Só se há conteúdo em vídeo de valor.
- **`consultation_call`** — Calendly/Cal.com com quota diária. **Escala mal**: se vender >50 unidades/dia, desligar ou cobrar fee simbólico.
- **`trial_extension`** — extender via Shopify Subscription app (se subscription) ou license key UUID com expiração.

Se algum bonus da 04 caiu num desses por engano (era pra ser ecom), surface pro membro: "Esse bônus tá modelado como [tipo de subscription], mas seu produto é físico one-time. Quer trocar pra [gift_with_purchase / free_ebook]? Isso é decisão de oferta, ajusto na 04."

### ETAPA 3 — Email de entrega (integra com Skill 13)

**Divisão de papéis (fonte única de verdade):** a 05 **gera o ASSET do bônus** (PDF, link, config GWP) e define o `delivery_trigger`. A **Skill 13 (retention) é o ÚNICO executor de email** (Klaviyo/ESP) — ela monta o flow e entrega. A 05 **não dispara email sozinha nem duplica lógica de email**: produz o **conteúdo do email + o trigger** como um payload que a 13 consome. Toda a mecânica de flow (trigger técnico, delays, draft/ativação, HTML do email no ESP) mora na 13. Ver a tabela "Divisão de papéis pós-compra" na Skill 13.

Mapear `delivery_trigger` → fluxo da 13 (espelho literal da tabela "delivery_trigger → email que entrega" da Skill 13, que é a fonte única):

| `delivery_trigger` | Fluxo / email que entrega o bonus (Skill 13) |
|---|---|
| `post_purchase` | Post-Purchase Welcome — Email 1 (obrigado) |
| `day_7_post_purchase` | Post-Purchase Welcome — Email 3 (~dia 7) |
| `on_first_reorder` | Replenishment — Email 2/3 (no reorder) |
| `on_signup` | Welcome Series — Email 1 (boas-vindas) |

(Win-back é OUTRO flow na 13 — reativação de cliente inativo, não entrega de bônus. Nenhum `delivery_trigger` mapeia pra ele.)

GWP físico e gift-wrapping geralmente **não precisam de email de entrega** (vão na caixa). E-book, discount_code, community e digital precisam.

**Timing (Fase A vs Fase B):** o payload (template abaixo + trigger) é produzido na **Fase A da 05**, antes do go-live — e a **Fase A da 13 roda logo em seguida na ordem canônica** (flows de recuperação pré-launch), montando o flow post-purchase que carrega este email já com o `{{BONUS_LINK}}` preenchido. O link na thank-you page / order status (config da Fase A) segue como rede de segurança: garante o acesso do comprador do dia 1 mesmo se o membro ainda não ativou o flow no ESP.

Template base do email (gerado em inglês, repassado pra 13):

```
Subject: Your [bonus name] is ready

Hey [First Name],

Thanks for ordering [product]. Here's the bonus you unlocked:

[BONUS NAME] (a [value-anchored] value)

[Description — 1-2 sentences toward the dream outcome]

Access it here: [CTA link or instructions]

Questions? Just reply to this email.

— [Brand]
```

Compliance do email: subject < 50 chars, 1 CTA só, reply-to monitorado, unsubscribe link. Sem emoji no subject (consistência com o tom da marca; opcional, decisão do membro).

### ETAPA 4 — Tracking (access rate / take-rate) — Fase B

**Não existe log por compra.** O Claude não roda a cada pedido e esta skill não configura webhook — modelar delivery por compra geraria um arquivo que nasce vazio e nunca é alimentado. A métrica nasce AGREGADA, puxada das fontes reais no re-run da skill.

**No re-run (D+30 e a cada ciclo depois):**

1. **Shopify Analytics / Admin API** → take-rate: pedidos elegíveis no período vs pedidos que destravaram o brinde/tier (GWP, complementary, gift-wrap, tier do bundle).
2. **Klaviyo (via Skill 13)** → access rate: open/click do email de entrega (e-book, discount code, community).
3. Gravar um **snapshot agregado por bônus** em `workspace/[produto]/05-bonus-delivery/dados.json` — array em **APPEND** (um item por bônus por período; o histórico mostra a evolução):

```json
[
  {
    "bonus_id": "bonus-01",
    "type": "gift_with_purchase",
    "delivery_channel": "shopify_function",
    "condition": "cart_threshold",
    "threshold": 65,
    "value_anchored": 49,
    "period": "2026-06-01..2026-06-30",
    "orders_eligible": 420,
    "orders_with_bonus": 219,
    "take_rate": 0.52,
    "access_rate": null,
    "source": "shopify_analytics | klaviyo | manual",
    "snapshot_at": "2026-07-01T14:00:00Z"
  }
]
```

KPIs por tipo:
- GWP / complementary SKU / gift-wrapping → **take-rate** (% dos pedidos elegíveis que destravam o brinde).
- E-book / digital / community → **access rate** (% que abre/baixa/aceita).

**Threshold de alarme:** access/take-rate < **30%** → o bônus não está agregando valor percebido. Surface pro membro como sinal de iteração na oferta (volta pra 04), não como falha desta skill. Benchmark de GWP saudável: take-rate sobe pra ~50%+.

**Pra ler take-rate como sinal econômico (não só vaidade), puxe os SISTEMAS NOMEADOS** (rode a `best_query`):
- **Funnel Economics Profit Map (CRO + COGS + AOV + LTV levers)** (rode `funnel economics increase AOV lower COGS increase LTV CRO profit map supplement peptide example`) — onde o GWP/asset move o lucro (AOV via take-rate, LTV via reorder).
- **Profitable Scaling Margin (PSM = LTV / (CPA + COGS))** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS golden ratio`) — se o GWP sobe AOV mas o COGS do brinde derruba PSM, o bônus está caro demais; itera na 04.

### ETAPA 5 — Integrações

| Integração | Pra quê | Caminho |
|---|---|---|
| **Shopify** (app GWP / Functions / Admin API) | Configurar GWP, complementary, gift-wrap, discount code | Coordenar config de checkout com **07d-checkout-aov** |
| **Skill 13 (retention)** | Disparar email de entrega | A 13 é o executor; a 05 fornece conteúdo + trigger |
| **File hosting** (Shopify Files API / S3 / R2) | Hospedar PDF do e-book/guide | Gerar link público |
| **Fulfillment center** | In-box gift (complementary físico, gift-wrap) | Documentar instrução pro membro repassar |

## Compliance — valor ancorado e Kennedy Level-2

**Puxe os SISTEMAS NOMEADOS antes de fechar valor ancorado e garantia** (rode a `best_query`):
- **FTC Anchored-Value / Fictitious-Pricing Legality (sell-the-bonus rule)** (rode `FTC anchored value fictitious pricing bonus must be actually sold legality`) — base legal do item 1 abaixo.
- **Kennedy Five-Level Guarantee Hierarchy (incl. Refund + Keep the Premium, Deliberate Redundancy, Guarantee the Letter)** (rode `Kennedy five level guarantee hierarchy refund keep the premium guarantee the letter itself`) — base do Level-2 (item 2).
- **Compliance Sweep (will→helps-to, claims→mice-type, fake-urgency cut, unauthorized-endorsement cut)** (rode `FTC compliance sweep will helps to claims mice type fake urgency endorsement cut`) — varredura do nome/descrição do bônus na PDP (item 3).

1. **FTC anchored-value:** o `value_anchored` do bônus deve ancorar no **preço de varejo real** do item, não num "sticker price" colado num item que nunca foi vendido por aquele preço. Ancorar valor falso em item não-vendido é frágil legalmente. Se o e-book "vale $49" mas nunca foi vendido, usar uma âncora defensável (preço de guides comparáveis no mercado) ou baixar a âncora.
2. **Kennedy Level-2 (keep-the-premium-on-refund):** atar o bônus à garantia — "se pedir reembolso, **fica com o bônus de qualquer forma**". Sinaliza confiança suprema e reduz fricção de compra. Coordenar com a `guarantee` do `04-offer-builder/dados.json` (se a garantia já é Level-2, a copy da página deve refletir; ver Skill 06/07). Surface pro membro se quiser ativar isso e ainda não está na oferta.
3. **Ad-flag words (rule 8b):** o nome/descrição do bônus que aparece na PDP segue ad-safe (Meta crawler lê a landing). Em doc interno, ok mencionar livre.

## Anti-patterns (FORBIDDEN)

- **Default "free PDF bonus"** sem justificar o fit com o dream outcome (e-book genérico tem access rate baixíssima).
- **Modelar bônus de info-product** (community/video/call) pra produto físico one-time — domínio errado.
- **GWP via draft order** — caminho errado; usar app ou Shopify Function.
- Bônus sem `delivery_trigger` (fica em limbo, nunca entregue).
- **Prometer bônus na PDP e deixar asset/config pra depois do launch** — a Fase A existe exatamente pra isso; comprador do dia 1 recebe o que a página prometeu.
- **Colocar threshold num bônus `condition: unconditional`** (quebra a promessa da página) — e vice-versa: auto-add num GWP que a página anuncia como "FREE over $X".
- Modelar log por compra (customer_id/delivered_at) — não há quem alimente; tracking é snapshot agregado (ETAPA 4).
- Discount code sem expiração (vira promo eterna).
- In-box gift (complementary/gift-wrap) sem coordenar com fulfillment (não vai na caixa).
- `value_anchored` inflado em item não-vendido (frágil no FTC).
- GWP threshold abaixo do AOV (queima margem sem empurrar AOV pra cima).
- Sobrescrever o `05-bonus-delivery/dados.json` em vez de dar append (perde o histórico de snapshots).

## Regras de rigor

1. **Bônus real e específico** — cada entrega é tangível e útil pro avatar. Recusar gerar bônus genérico sem justificar relevância.
2. **Promise↔Config check** — bônus prometido no stack da Skill 04 (visível na PDP) precisa ter asset + delivery/GWP setup completos **ANTES do go-live de ads** (Fase A). A Skill 09 (consistency audit) e a rule `.claude/rules/pre-launch-gates.md` verificam essa promessa ("Free [bonus] with purchase") no gate de launch.
3. **Access/take-rate tracking** — sempre que possível, medir. Bônus nunca acessado/escolhido = sinal de oferta fraca, itera na 04.
4. **Fallback graceful** — se a API de hosting/Function falha, gerar PDF como último recurso E avisar o membro pra setup manual depois (ES6).

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/05-bonus-delivery/bonuses/` antes de salvar.

1. **`workspace/[produto]/05-bonus-delivery/bonuses/[bonus-id]/`** — assets do bônus (PDF do e-book, screenshots da config GWP, instruções de fulfillment, etc — conforme type). Estes seguem o **design da marca do membro** (não do Aura) e o **consumidor-final é em inglês**.
2. **`workspace/[produto]/05-bonus-delivery/bonus-delivery.md`** — doc operacional pra AI ler em skills futuras: cada bônus com type, condition, canal de entrega, trigger, threshold (se cart_threshold), path do asset, KPI esperado, e status da Fase A (pronto pro launch?). Escrito no `report_language`.
3. **`workspace/[produto]/05-bonus-delivery/bonus-delivery.html`** — visualização humana usando `.claude/templates/aura-report-template.html` como base. **Logo SVG Aura no topo** (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html`). Componentes: `.section-label` por bônus, `.pill` pro type tag, `.kpi-grid` pra take-rate/access rate (quando disponível), `.callout` pro threshold de GWP.
4. **`workspace/[produto]/05-bonus-delivery/dados.json`** — array de snapshots agregados por bônus/período com take-rate/access rate (ETAPA 4, Fase B). Append, nunca sobrescrever.

Atualizar `manifest.json.skills_completed` com `"05-bonus-delivery"`.

- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html).

## Mensagem Final (framing de draft — iteration-driven-refinement)

> "Fase A da entrega de bônus pronta pros [N] bônus da oferta:
>
> 1. [Bonus 1 — tipo — condition — canal de entrega / threshold se cart_threshold]
> 2. [Bonus 2 — tipo — canal de entrega]
>
> O GWP tá configurado via [app/Function] conforme a condição da oferta ([auto-add em toda compra / threshold de $X ancorado no seu AOV]). Os e-books/assets digitais tão em `bonuses/` e o link de acesso já aparece na thank-you page — comprador do dia 1 recebe o que a página promete. O payload do email de entrega tá pronto pro fluxo da Skill 13.
>
> Testa comprando 1 unidade pra validar que o brinde aparece no cart e o link chega. Me diz se o threshold/condição tá certo ou se quer ajustar.
>
> Próximo passo na ordem de launch: diga **'retention'** (Skill 13 Fase A — flows de recuperação: abandoned cart + post-purchase; o payload do email de bônus que preparei entra direto no flow post-purchase de lá). Depois de ~30 dias com ads ATIVOS (campanha rodando, não só criada), roda `bonus delivery` de novo (Fase B): eu puxo os agregados do Shopify/Klaviyo, gravo o snapshot no `05-bonus-delivery/dados.json` e mostro take-rate/access rate por bônus pra gente iterar a oferta."

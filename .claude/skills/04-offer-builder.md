---
name: offer-builder
description: Engine de construção de oferta com mecanismo único, stack de valor, bundles, bumps, upsells, garantia, e unit economics completa. Use quando o membro disser "offer", "oferta", "montar oferta", "construir oferta", "pricing", "bundle", ou quando o market research e competitor analysis estiverem prontos e o membro quiser estruturar a oferta antes de escrever a copy. A oferta é o MOTOR ECONÔMICO do negócio — decisões aqui determinam se ads são viáveis em escala.
---

# Offer Builder Engine

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` + `README.md`; o mapa skill→domínio está no README). Os domínios desta skill são `offer-mechanism` (41), `offer-pricing-guarantee` (54) e `brand-building-bonus-aov` (27). Sempre que uma ETAPA mandar "puxar os sistemas da base", rode `search_knowledge` com a `best_query` NOMEADA de cada framework relevante — **NUNCA query genérica**. Os frameworks de maior impacto já estão embutidos nas ETAPAs abaixo; o restante do domínio fica disponível no índice.

### Pré-flight (OBRIGATÓRIO)
Valide antes de prosseguir:
- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `02-market-research/dados.json` existe (awareness_distribution, sophistication_stage) E `02-market-research/relatorio.md` existe (narrativa: pain points, desires, objeções)
- [ ] `03-competitor-analysis/relatorio.md` E `03-competitor-analysis/dados.json` existem
- [ ] Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language. As 3 versões do mecanismo (version_short/medium/long) são copy pública — permanecem em inglês se o mercado for US.

Se faltar qualquer arquivo de fase anterior (02/03), em vez de abortar seco, ofereça ao membro 2 caminhos (escape-path ES1):
- **(A)** Rodar a skill faltante agora pra gerar o arquivo real, OU
- **(B)** Prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` e avisando no output final que recomenda re-executar esta skill quando o arquivo real existir.

Se `manifest.json` ou `profile.md` estiverem TOTALMENTE ausentes (membro nunca rodou setup), aí sim pare — mas ofereça rodar o setup (Skill 00) inline.

## Quando Usar
Quando o membro tem produto definido, market research pronto, e precisa construir a estrutura econômica completa: mecanismo único, preço, bundles, bumps, upsells, garantia, e unit economics viáveis pra escalar com ads pagos. Sem oferta estruturada, nenhum copy (por melhor que seja) vai converter sustentavelmente.

## Antes de Começar

1. Leia `workspace/profile.md` (ferramentas disponíveis, budget diário — informa viabilidade econômica; lê também `report_language` conforme o pré-flight)
2. Leia `workspace/[produto]/01-product-research/relatorio.md` (se existir — tem features, COGS preliminar, potencial de oferta)
3. Leia `workspace/[produto]/02-market-research/relatorio.md` (narrativa: pain points, desires, root cause, objeções) E `02-market-research/dados.json` (campos estruturados: awareness_distribution, sophistication_stage, voc_phrases) — a oferta é a RESPOSTA direta ao market research
4. Leia `workspace/[produto]/03-competitor-analysis/relatorio.md` E `03-competitor-analysis/dados.json` (claims saturados a evitar, mecanismos já usados, gaps de oferta identificados)
5. **Puxe os SISTEMAS NOMEADOS da base — não query genérica.** Para cada ETAPA desta skill, rode `search_knowledge` (com `deep=true`) usando a `best_query` exata de cada framework relevante. A lista completa do domínio desta skill (122 frameworks em `offer-mechanism`, `offer-pricing-guarantee`, `brand-building-bonus-aov`) está em `.claude/lib/kb-index/` (`frameworks.json` / `README.md`). Os frameworks de maior impacto já estão NOMEADOS e embutidos dentro de cada ETAPA abaixo (mecanismo → ETAPA 2, pricing/garantia → ETAPAs 3-4, economics/PSM → ETAPAs 5-7). Aprofunde em cada um até ter domínio completo — pricing é decisão estratégica, não técnica. NUNCA fundamente uma decisão de oferta numa busca genérica do tipo "offer pricing" — sempre puxe o sistema nomeado.

## Fluxo da Skill

### ETAPA 1 — Coletar Informações do Produto (3 Perguntas Apenas)

Antes de perguntar, extraia o máximo automaticamente da página do produto (dado salvo no profile pela Skill 00 ou puxando via web fetch agora se o link estiver no profile). Features, ingredientes, claims, preço atual de mercado — tudo que conseguir.

**Faça APENAS estas 3 perguntas, na ordem:**

**1. Custos (COGS breakdown — NÃO aceite agregado):**

Não aceite "custo total" agregado. Pergunte separadamente:
1. Custo do produto (na fábrica / fornecedor) por unidade
2. Frete médio por pedido (informe região principal: Brasil interior? EUA West Coast?)
3. Pick & pack (fulfillment center): R$/$ por pedido
4. Gateway fee: % + taxa fixa (Stripe: 3.99% + R$0.39 típico)
5. Taxas e impostos incidentes por pedido

Documente cada um em `04-offer-builder/dados.json` → `cogs_breakdown`.

**2. Features/ingredientes (CONDICIONAL):**
- SE não conseguiu extrair da página automaticamente: "Liste as features ou ingredientes principais do produto."
- SE conseguiu extrair: NÃO pergunte; mostre o que extraiu e peça confirmação rápida ("tá certo? falta alguma coisa?").

**3. Produto complementar:**
"Tem algum produto complementar que poderia vender junto? (se não souber, diz 'não sei')"

**Decisões automáticas do sistema (NÃO PERGUNTE):**
- **Preço final**: definido pelo framework de pricing abaixo (Etapa 3), triangulando 3 ancoras (value / competitor / economics)
- **Pick & pack**: se o membro não souber, estime ~$2-3 por unidade E **marcar `"pick_pack_estimated": true` no JSON companion** (membro precisa validar)
- **Gateway fee**: se o membro não souber, estime ~3% do AOV + taxa fixa E **marcar `"gateway_fee_estimated": true`**

**Sanity check obrigatório depois de calcular Unit Economics (Etapa 5):**

Se `Margem $` < $20 → PARAR e avisar membro:
> ⚠️  Margem por unidade calculada: $X. Isso é muito baixo pra ecommerce direct-response.
>     Com margem < $20, o CPA aceitável fica < $10-15, praticamente impossível em Meta Ads hoje.
>
>     Causas prováveis:
>     - COGS subestimado (provável se vc não tinha todos os itens do breakdown — veja `pick_pack_estimated`, `gateway_fee_estimated`)
>     - Preço de venda abaixo do competitivo (vê o framework de pricing na Etapa 3)
>     - Produto com AOV inerentemente baixo (considera bundle pra aumentar AOV)
>
>     Opções:
>     1. Reveja COGS itemizado real (peça fatura pro fornecedor)
>     2. Aumenta preço via bundle 2-3 unidades ou upsell pós-compra
>     3. Abandona esse produto — margem não sobe via marketing
>
>     Prosseguir mesmo assim? (sim/não)

Se continuar, marca `"margin_warning": true` no manifest pra Skills 10/12 alertarem escala agressiva.

### ETAPA 2 — MECANISMO ÚNICO (A Parte Mais Importante)

O mecanismo único é o que diferencia seu produto de TODO concorrente. Sem mecanismo forte, a copy vira commodity disputando no preço. Com mecanismo forte, você cria um espaço sem concorrência direta (blue ocean) dentro de qualquer nicho.

**Puxe estes SISTEMAS NOMEADOS da base antes de ideação (rode a `best_query` de cada — NUNCA query genérica):**
- **Unique Mechanism Theory (UMP/UMS — UMP é o mecanismo do problema, UMS é o mecanismo da solução)** (rode `unique mechanism UMP UMS theory two-part problem solution`) — o framework-mãe: mecanismo do problema + mecanismo da solução.
- **UMP/UMS Internal Structure** (rode `UMP UMS structure trigger surprising cause quiz specific delivery`) — anatomia interna do mecanismo (trigger → causa surpreendente → delivery específico).
- **S.I.N. Filter (Simple, Intuitive, New)** (rode `mechanism SIN filter simple intuitive new`) — o filtro aplicado em 2A/2B abaixo.
- **Proprietary Mechanism Naming (Gum Name)** (rode `proprietary mechanism gum name nickname ritual hack effect`) — como cunhar o nome proprietário (2-4 palavras).
- **The Big 3: New Mechanism / New Information / New Identity** (rode `new mechanism new information new identity big 3 sophisticated market`) — qual eixo usar conforme sophistication.
- **Market Sophistication (5 Stages)** (rode `market sophistication 5 stages Schwartz new mechanism identification`) — determina QUE tipo de mecanismo o mercado ainda aceita.
- **Reeves USP (3 Requirements + 3 Roads)** (rode `Reeves USP three requirements three roads preemptive claim`) — garante que o mecanismo vira proposição única defensável.
- **Hopkins Reason-Why Rule** (rode `Hopkins reason why rule every claim needs a reason`) — todo claim do mecanismo precisa de um porquê concreto.

Frameworks adjacentes de mecanismo (Big Domino, Three False Beliefs, Schwartz Mechanization, Big Idea, Sugarman Concept Selling, Hormozi MAGIC Naming) estão no índice `.claude/lib/kb-index/` — puxe conforme o vertical exigir.

**2A — Ideação (Gerar 5-7 Opções):**

Com base em:
- Features/ingredientes do produto
- Root cause research da Skill 02 (causa-raiz proprietária)
- Gaps do competitor analysis (mecanismos já usados — evitar)
- Awareness level do mercado (Schwartz) e sophistication stage (determina que tipo de mecanismo funciona)

Gere 5-7 opções de mecanismo único. Cada um com:

- **Nome proprietário** (2-4 palavras, memorável, proprietário-soando, pronunciável)
- **Explicação simples** (2-3 frases — como funciona na prática)
- **Base real do produto** (ingrediente, feature, processo, combinação — NÃO inventar ciência falsa)
- **Por que é diferente dos concorrentes** (qual claim rompe, qual gap preenche)
- **Em qual nível de awareness funciona melhor**
- **Match com sophistication stage** (ingredient-based pra Estágio 3, information-based pra Estágio 4, identification pra Estágio 5)

**Aplicar o filtro S.I.N. (Simple / Intuitive / New):**
- **Simple** (fácil de entender de primeira, sem jargão — "Joint Drought Protocol" comunica na hora, não exige explicação técnica)
- **Intuitive** (faz sentido imediato pro avatar, a lógica "clica" sozinha — "Lipid Barrier Breach" sugere causa e solução sem precisar de aula)
- **New** (soa novo pro mercado, mesmo que a ciência subjacente seja antiga — reformulação criativa de algo conhecido)

Nomes pode vir de:
- Renomear ingredientes/componentes existentes pra novo propósito (ex: num suplemento: "Bioavailable Matrix" em vez de "complexo"; num wearable: "Adaptive Core Module" em vez de "sensor")
- Combinar 2-3 features em conceito unificado (ex: "Triple Action Stack", "Dual Channel System")
- Nomear um processo interno (ex: "48-Hour Activation Protocol", "7-Day Reset Method")
- Reposicionar uma feature secundária como central (ex: transformar feature "com antioxidantes" em "Free Radical Neutralization System"; feature "bateria de 72h" em "Perpetual Charge Architecture")

**2B — Avaliação Rigorosa:**

Pra CADA opção de mecanismo, score 1-10 em:

| Dimensão | O que avaliar |
|---|---|
| **Diferenciação** (1-10) | Quão diferente dos claims dos concorrentes? |
| **Credibilidade** (1-10) | A ciência/lógica por trás é defensável? Fake = 1, baseado em research real = 10 |
| **Memorabilidade** (1-10) | O nome "gruda"? É fácil de repetir? |
| **Expandibilidade** (1-10) | Dá pra expandir em 2-3 parágrafos pra copy sem soar repetitivo? |
| **Match com awareness** (1-10) | Funciona pro nível de awareness dominante do TAM? |

Score final = soma / 5.

**2C — Recomendação:**

Recomende o mecanismo com maior score total, com justificativa explícita por que esse vence os outros.

**2D — Escrever 3 Versões do Mecanismo (pra uso em copy/ads):**

Para o mecanismo recomendado, escreva:

- **Versão de 1 frase** (pra headlines, hooks, ads): ex: "Nossa fórmula ativa o [Mechanism Name] em 48 horas." (produto-agnóstico — adaptar ao vertical: skincare, supplement, fitness, gadget, etc)
- **Versão de 1 parágrafo** (pra PDP e body de ads): explica como funciona + por que é diferente, em ~3-4 frases.
- **Versão de 2-3 parágrafos** (pra landing page dedicada ou advertorial — expansão completa): inclui causa raiz do problema + como o mecanismo a endereça + por que os outros mecanismos não funcionam + evidência (ingredient research, estudos, se disponível).

### ETAPA 2.5 — Research Foundation (OBRIGATÓRIO — Lastro de Evidência)

Mecanismo sem lastro científico/empírico é claim vazio e vira copy fraca, ad reprovado e member frustrado. Antes de prosseguir pra Etapa 3, você DEVE construir a base de evidência que sustenta o mecanismo recomendado.

**Fontes a consultar (web search extensivo):**

1. **Estudos científicos / papers peer-reviewed**
   - PubMed (`site:pubmed.ncbi.nlm.nih.gov`)
   - Google Scholar (`site:scholar.google.com`)
   - ResearchGate, ScienceDirect, NIH
   - Queries: nome do ingrediente/processo + "clinical trial", "peer-reviewed", "mechanism of action", "efficacy study", "randomized controlled trial"

2. **Press releases / comunicados de pesquisa institucional**
   - Harvard Health Publishing, Mayo Clinic, Cleveland Clinic, WebMD
   - Press releases de fornecedores de ingrediente (Lonza, DSM, BASF, etc — têm whitepapers técnicos)

3. **Regulatório / referências oficiais**
   - FDA GRAS status (se aplicável)
   - EMA monographs, EFSA opinions
   - USP Pharmacopeia

4. **Reviews sistemáticas e meta-análises** (evidência de maior grau)
   - Cochrane Library
   - Meta-analyses em periódicos da especialidade

5. **Patents** (ingrediente/processo protegido)
   - Google Patents — procurar prior art que sustenta o mecanismo

**Para CADA claim do mecanismo (causa-raiz, ingrediente ativo, resultado esperado, diferenciação), documente:**

```json
{
  "claim": "texto do claim",
  "evidence_type": "peer_reviewed_study|meta_analysis|press_release|regulatory|patent|empirical_observation",
  "source_title": "título completo",
  "source_url": "url completa",
  "source_date": "YYYY-MM-DD",
  "strength": "strong|moderate|weak",
  "strength_rationale": "por que essa classificação",
  "quote_or_summary": "trecho literal ou resumo 1-2 frases",
  "usage_rights": "public|paywalled|needs_permission"
}
```

**Regras de rigor (NÃO NEGOCIÁVEIS):**

- Proibido inventar estudo ou extrapolar além do que a fonte afirma literalmente
- Proibido citar "estudos mostram que..." sem fonte rastreável com URL
- Se a evidência é `weak` (anecdotal, in-vitro só, animal study único, tamanho amostral pequeno), o claim precisa ser suavizado ("helps with", "supports", "may contribute") — não afirmado categoricamente
- Se NENHUMA evidência for encontrada pra um claim central, o mecanismo precisa ser reformulado antes de prosseguir — não escreva copy sobre fundação vazia

**Output dessa etapa:**

Arquivo `workspace/[produto]/04-offer-builder/research-foundation.json` contendo:
```json
{
  "mechanism_name": "...",
  "evidence_items": [ { ... } ],
  "summary_statement": "2-3 frases resumindo a base de evidência do mecanismo",
  "confidence_score": "high|medium|low",
  "gaps_and_risks": "claims que ficaram sem lastro forte — a serem suavizados na copy"
}
```

Esse arquivo é lido pelas skills 06 (copy) e 08 (creatives) pra ancorar afirmações com fonte verificável. Copy sem `04-offer-builder/research-foundation.json` acessível roda com warning "claims unverified — escalate carefully".

### ETAPA 3 — Estrutura de Oferta

Monte a arquitetura econômica completa:

**Produto Principal:**
- **Nome do produto** (se ainda não tem, sugira — pode incluir mecanismo no nome: ex: "[Brand] — [Mechanism Name] [Category]", adaptar ao vertical)
- **Preço base**: ver framework de pricing abaixo (triangulação de 3 ancoras)
- **Core deliverable**: o produto em si (1 unidade / X ml / Y cápsulas)

**Puxe estes SISTEMAS NOMEADOS de pricing/value antes de ancorar (rode a `best_query` de cada):**
- **Hormozi Value Equation** (rode `Hormozi value equation dream outcome perceived likelihood time delay effort sacrifice`) — sustenta a ancora value-anchored abaixo.
- **Anchoring & Adjustment** (rode `pricing anchoring adjustment set high anchor was price SSN auction Ariely`) — como ancorar o preço alto antes do real.
- **Decoy Effect (Asymmetric Dominance)** (rode `decoy effect asymmetric dominance Economist subscription Williams-Sonoma bread machine`) — desenha o bundle de 3 tiers.
- **Extremeness Aversion** (rode `extremeness aversion three tiers middle option beer experiment`) — por que o 3-pack "Popular" no meio vende mais.
- **Charm Pricing (Endings in 9)** (rode `charm pricing nine ending left-digit effect 24 percent catalog`) — terminação de preço.
- **3x+ Markup Rule + $60 AOV Floor** (rode `3x markup rule 60 dollar AOV floor COGS shipping margin paid traffic CPM fixed`) — piso de margem pra tráfego pago (cruza com o sanity de margem da ETAPA 1).
- **Hormozi Virtuous Cycle of Price** (rode `Hormozi virtuous cycle of price premium pricing better clients`) — quando subir o preço melhora o negócio.

Pricing psychology adjacente (Coherent Arbitrariness, Zero Price Effect, Mental Accounting, Endowment, Transaction Utility, Kennedy Five Price Minimizers) está no índice — puxe se o framing do preço exigir.

**Framework de pricing (escolher UMA ancora, validar com as outras 2):**
- **Value-anchored**: Preço = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort)  [Hormozi Value Equation]
- **Competitor-anchored**: Mediana dos top 3 concorrentes × modificador (1.1-1.3 se diferenciação alta; 0.8-0.95 se entrada competitiva)
- **Economics-anchored**: COGS × 4 a 6 (ecommerce direct-response padrão para viabilizar paid acquisition)
Se as 3 ancoras divergirem > 40%, revisitar offer antes de prosseguir.

**Bundles (estrutura clássica):**

| Bundle | Quantidade | Preço | Preço por unidade | Savings vs solo |
|---|---|---|---|---|
| Solo | 1x | $X | $X | — |
| Popular | 3x | $Y | $Y/3 | ~$Z ou ~Z% |
| Best Value | 6x | $W | $W/6 | ~$A ou ~A% |

Regra prática (pode ajustar):
- 3-pack: ~25-35% savings vs 3× solo
- 6-pack: ~40-50% savings vs 6× solo

Marcar **Popular** no 3-pack (visualmente destacado — driver de AOV). Best Value no 6-pack (pra clientes que compram em volume alto (whales)).

**Checkout Bump:**
- Produto complementar de baixo preço ($9-19 tipicamente) ou add-on (frete expresso, versão com mais, etc)
- Incremento de 15-30% na taxa de aceitação se bem posicionado
- Copy curta do bump (1 frase + 1 benefício)

**Upsell Pós-Compra:**
- Produto complementar de alto ticket ($47-97+) que amplia o resultado
- Apresentado na thank-you page após a compra
- Taxa de aceitação tipica 5-15%
- Copy do upsell (2-3 frases + principal benefício + oferta)

**Stack de Valor Com Ancoragem:**

**Puxe estes SISTEMAS NOMEADOS de stack/bônus antes de montar (rode a `best_query` de cada):**
- **Bonus Stacking (Value Stack / Stack Slide)** (rode `value stack stack slide bonus stacking standalone value exceeds price`) — soma cumulativa que faz o preço parecer pequeno.
- **Razor-Blade vs Handle (Bonus Fit Principle)** (rode `razor blade vs handle bonus fit natural complement to product`) — cada bônus deve aumentar o consumo/resultado do produto principal.
- **Bonus Types Taxonomy** (rode `bonus types presuppose success enables success graduation gift access partner complementary`) — escolhe o `type` certo (não default pra PDF), alimenta o campo `bonuses[]` do JSON.
- **FTC Anchored-Value / Fictitious-Pricing Legality** (rode `FTC anchored value fictitious pricing bonus must be actually sold legality`) — o `value_anchored` de cada bônus precisa ser legalmente sustentável (o bônus tem que ser realmente vendível por aquele valor).

Liste tudo que vem no pacote com valor ancorado:
- Produto principal: valor $X
- Bonus 1 (ex: guia digital, checklist, protocol card): $Y
- Bonus 2 (ex: acesso a comunidade, suporte): $Z
- Bonus 3 (ex: consultoria inicial, material extra): $W
- **Valor total**: $X+Y+Z+W
- **Preço hoje**: $(preço real)
- **Economia percebida**: $(diferença)

Cada bonus é REAL (entregável), não inflado artificialmente. O stack cria percepção de valor desproporcional ao preço.

**OBRIGATÓRIO — Registrar bonuses no campo top-level `bonuses[]` do `04-offer-builder/dados.json`.** Skill 05 (bonus-delivery) lê desse campo pra montar o pipeline de entrega. Pra cada bonus do stack, gerar entry:

```json
{
  "id": "bonus-01",
  "name": "texto igual ao da stack",
  "description": "1-2 frases do que é e por que vale",
  "value_anchored": 49,
  "type": "gift_with_purchase | free_complementary_sku | free_ebook | gift_wrapping | digital_guide | discount_code | workbook | checklist | community_access | video_series | consultation_call | trial_extension",
  "format_hint": "in_box | shopify_function | gift_app | pdf | notion | figma | wistia | klaviyo_email | shopify_discount | circle_invite",
  "delivery_trigger": "post_purchase | on_signup | day_7_post_purchase | on_first_reorder"
}
```

**Tipos NÃO default pra "PDF":** escolher o type que realmente bate com o avatar. Se membro disser "bonus é PDF só porque é fácil", questionar: "Esse avatar REALMENTE quer PDF? Pra [avatar profile], [alternative type] costuma ter access rate maior." Documentar essa decisão.

### ETAPA 4 — Garantia (Risk Reversal)

**Puxe estes SISTEMAS NOMEADOS de garantia/risk-reversal antes de escolher (rode a `best_query` de cada — NUNCA query genérica):**
- **Hormozi Four Guarantee Types** (rode `Hormozi four guarantee types unconditional conditional anti-guarantee implied`) — o menu de 4 tipos que mapeia nos "Tipos possíveis" abaixo.
- **Guarantee Stacking** (rode `Hormozi guarantee stacking short-term unconditional long-term conditional`) — combinar uma incondicional curta + uma condicional longa.
- **Guarantee Naming** (rode `Hormozi naming your guarantee vivid memorable Club a Baby Seal Shark Infested Waters`) — dar nome vívido à garantia (entra na copy da garantia abaixo).
- **Longer Guarantee = Fewer Refunds Paradox** (rode `longer guarantee fewer refunds one year vs 30 day eye off calendar Cashvertising`) — por que prazo maior reduz reembolsos (tira o olho do calendário).
- **The Guarantee Math** (rode `guarantee math net sales conversion lift refund rate Fladlien buyback`) — calcula se o lift de conversão cobre o refund rate antes de cravar o tipo (cruza com a margem da ETAPA 5).

Kennedy Five-Level Guarantee Hierarchy e Guarantee Power Statement Template estão no índice — puxe se precisar de hierarquia mais granular ou template de frase.

**Tipos possíveis:**
- **Money-back** (30, 60, 90 dias): baixo risco pro cliente, médio risco pro merchant
- **Results-based** ("se não funcionar, reembolsamos"): forte psicologicamente, exige evidência clara de uso
- **Extended trial** (primeiro mês grátis, cancela depois): baixa barreira de entrada mas exige subscription
- **Double-your-money-back**: agressivo, usa sophistication alto, mas blindado contra abuso (com critérios)

**Recomende o tipo certo baseado em:**
- Sophistication stage (estágios mais altos pedem garantias mais agressivas)
- Margem da oferta (margem pequena não aguenta money-back generoso)
- Ceticismo do avatar (market research — "já tentei X" → garantia forte converte)
- Tipo de produto (consumível vs duradouro)

**Escreva a copy da garantia** (2-3 frases, tom confiante mas claro sobre condições):
Exemplo: "90-day results guarantee. If you don't see visible improvement in the first 90 days, send us a photo — we'll refund every penny. No questions, no hoops."

### ETAPA 5 — Unit Economics (Tabela Completa)

**Puxe estes SISTEMAS NOMEADOS de unit economics antes de calcular (rode a `best_query` de cada — vale também pra ETAPAs 6/7):**
- **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS golden ratio growth`) — o golden ratio que substitui ROAS; é o núcleo das ETAPAs 5-7.
- **Unit Economics Hierarchy (CPA vs CAC, GPT)** (rode `unit economics CPA vs CAC blended CPA GPT net profit hero offer`) — separa CPA de CAC e define o denominador correto de margem.
- **Hormozi LTGP:CAC Ratio** (rode `Hormozi LTGP CAC ratio 3 to 1 lifetime gross profit acquisition cost`) — alvo 3:1 de lifetime gross profit sobre CAC.
- **Client Financed Acquisition (CFA)** (rode `Hormozi client financed acquisition front end covers CAC backend pure profit`) — front-end (bump/upsell) cobre o CAC, backend vira lucro.
- **Pricing Leverage Math (5% Price = 50% Profit)** (rode `pricing leverage 5 percent price increase 50 percent profit thin margin`) — quando a margem é fina, mexer no preço move o lucro desproporcionalmente (input pra ETAPA 7 quando PSM < 1.1).

Crie uma tabela de unit economics pra CADA variação da oferta (solo, bundle, com bump, com upsell):

| Variação | AOV | COGS | Pick&Pack | Frete | Gateway | Custo Total | Margem $ | Margem % | Breakeven ROAS | Target CPA (2× ROAS) | Target CPA (3× ROAS) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Solo | | | | | | | | | | | |
| 3-pack | | | | | | | | | | | |
| 6-pack | | | | | | | | | | | |
| Solo + Bump | | | | | | | | | | | |
| 3-pack + Bump | | | | | | | | | | | |
| Solo + Upsell | | | | | | | | | | | |

### Unit Economics — Fórmulas

Receita por unidade vendida:
- AOV = Average Order Value (Preço × unidades médias por pedido)

Custo por unidade vendida:
- Custo Total = COGS + Frete + Pick&Pack + Gateway Fee (%)

Margem por unidade:
- Margem $ = AOV − Custo Total

> **Denominador canônico:** toda a unit economics usa `weighted_margin_per_order` (margem média ponderada por AOV, considerando bumps + upsells) como denominador. Quando a oferta não tem bump/upsell, ele iguala `margin_per_unit`. Os campos `breakeven_cpa`, `target_cpa_primary_2x/3x` e `breakeven_roas` do `04-offer-builder/dados.json` derivam SEMPRE de `weighted_margin_per_order` (ver "Nota sobre nomenclatura" no Output Schema). A Skill 11 lê assim.

**Breakeven CPA / Breakeven ROAS** (o ponto de empate, antes de lucro):
- Breakeven CPA = weighted_margin_per_order
- Breakeven ROAS = AOV / weighted_margin_per_order
- Exemplo: AOV $118, weighted_margin_per_order $72 → Breakeven CPA = $72, Breakeven ROAS = 118/72 = 1.64
- Significa: precisa gerar $1.64 de receita para cada $1 em ads só para empatar

**Target CPA** (CPA máximo para N× ROAS desejado):
- Target CPA para ROAS N = weighted_margin_per_order / N
- Exemplo: weighted_margin $72, quer 2× ROAS → CPA máximo = 72/2 = $36
- Para 3× ROAS → CPA máximo = 72/3 = $24
- Sanidade: target (2×) < breakeven_cpa SEMPRE ($36 < $72).

**PSM — Profitable Scaling Margin** (o "golden ratio" que substitui ROAS na decisão de escala; é a **MESMA fórmula** que a skill 11 grava como `psm_real`, pra que o teórico do offer e o real medido sejam comparáveis — a skill 12 lê os dois):
- **PSM = LTV / (CPA + COGS)** — LTV = AOV projetado quando não há histórico de recompra (proxy); COGS do `cogs_breakdown`; CPA = o CPA-alvo que o membro aceitaria. Avalie no **target 2×**, NÃO no breakeven (avaliar no breakeven daria sempre PSM = 1.0; no 2× daria sempre 2.0 se usasse margem/CPA — por isso a fórmula canônica usa LTV e COGS, que refletem a estrutura real).
- Exemplo: AOV/LTV $118, COGS $30, CPA-alvo (2×) $36 → PSM = 118 / (36 + 30) = **1.79**.
- Thresholds (idênticos às skills 11/12): **>1.3 escala agressiva · 1.1–1.3 escala estável (+5%) · 1.0–1.1 breakeven · <1.0 não viável**.
- Grave como `psm_theoretical` no `dados.json`. A skill 11 grava `psm_real` (mesma fórmula, com o CPA real medido); a skill 12 compara os dois.

**Regra crítica:** Target CPA pra 2× ROAS deve ser viável com o budget do membro. Se a margem $ < $15-20, a oferta não sustenta ads a não ser em volume muito alto.

### ETAPA 6 — AOV Projetado (com Bump e Upsell Acceptance)

**Puxe estes SISTEMAS NOMEADOS de AOV/upsell antes de projetar (rode a `best_query` de cada):**
- **Profit Optimization 4 Categories + AOV Builders** (rode `profit optimization four categories AOV builders bundles free shipping threshold volume discount GWP profit per visitor`) — o menu de alavancas de AOV (bundle, threshold de frete grátis, volume discount, GWP).
- **Free-Plus-Shipping & Order Form Bump** (rode `Brunson free plus shipping buyer 10x order form bump 20 to 50 percent`) — taxas de aceitação realistas do bump (20-50%) que calibram a estimativa abaixo.
- **Three OTO Structures** (rode `Brunson three OTO structures next thing do it faster need help upsell`) — estrutura o upsell pós-compra (próxima coisa / fazer mais rápido / preciso de ajuda).
- **AOV Money Close + Offer Bump + Add-More-Packages** (rode `AOV money close offer bump add more packages biggest package most popular checkout`) — qual pacote destacar e como apresentar o "add more" no checkout.

Estime taxas de aceitação realistas (ajustar depois com dados reais):
- **Bump acceptance**: 20-35% (conservador: 20%)
- **Upsell acceptance**: 5-15% (conservador: 8%)

Calcule AOV projetado:

AOV = (% compra solo × preço solo)
    + (% compra 3-pack × preço 3-pack)
    + (% compra 6-pack × preço 6-pack)
    + (bump acceptance × preço bump)
    + (upsell acceptance × preço upsell)

Baseline mix (ajustar com data depois):
- 50% solo, 35% 3-pack, 15% 6-pack (mix típico com Popular destacado no 3-pack)

### ETAPA 7 — PSM Projetado (Profitable Scaling Margin)

Reavalie o PSM com o **AOV projetado da ETAPA 6** (pós bump/upsell) como LTV-proxy, pela MESMA fórmula da ETAPA 5 (a mesma que a skill 11 usa pro `psm_real`):

**Fórmula:** PSM = LTV / (CPA + COGS) — agora LTV = AOV projetado (ETAPA 6), CPA = target 2× (ou um CPA esperado de benchmark, se o membro tiver), COGS do `cogs_breakdown`. Se houver dado de recompra, use LTV com reorder ao longo de 30-60-90 dias (eleva o PSM e justifica CPA mais alto).

- **PSM < 1.0**: cada cliente perde dinheiro em escala — oferta NÃO viável
- **PSM 1.0–1.1**: breakeven, cresce devagar com risco
- **PSM 1.1–1.3**: escala estável, +5% por ciclo
- **PSM > 1.3**: escala agressiva viável

Se PSM projetado < 1.1 — oferta **não sustenta escala lucrativa** com economics atuais. Sugira em ordem:
1. **Aumentar AOV** (primeira opção, sem arriscar volume):
   - Bundle (ex: 3-pack desconto 15%)
   - Upsell no checkout (complemento de $20-40 com margem alta)
   - Assinatura com desconto 10-15% (aumenta LTV)
2. **Reduzir COGS** (fornecedor alternativo, negociar volume, frete agregado)
3. **Aumentar preço** (só se posicionamento competitivo permitir; re-validar pricing anchors)
4. **Pivotar oferta** — mudar mecanismo ou público-alvo
NUNCA "reduzir target CPA mágica"; CPA é output de eficácia, não input.

### ETAPA 8 — Viabilidade com Budget do Membro

Cruze unit economics com budget diário do membro (do profile):

- Com target CPA de $X, quantas vendas/dia o budget do membro viabiliza?
- Ex: budget $100/dia, CPA target $30 → ~3 vendas/dia
- AOV projetado × 3 vendas/dia = ~$Y/dia em receita
- Margem total projetada = $Z/dia

É viável? Pra qual revenue tier (da Skill 12) essa oferta leva o membro em 30/60/90 dias?

### ETAPA 9 — Validação Final (Sanity Checks)

Antes de salvar, responda HONESTAMENTE:

1. **A oferta faz sentido pro awareness level dominante?** (se é Problem Aware, a oferta foca em educação; se é Product Aware, foca em diferenciação; etc)
2. **O mecanismo é genuinamente diferente dos concorrentes?** (passa no filtro S.I.N. + não é commodity do estágio de sophistication)
3. **As economics permitem escalar?** (PSM > 1.1 — escala estável; CPA target viável com budget do membro)
4. **O stack de valor é convincente SEM inflar?** (cada bonus é real, útil, entregável)
5. **A garantia quebra a objeção de risco identificada no market research?** (não é genérica — ataca o medo específico do avatar)
6. **Pricing triangulado (as 3 ancoras convergem < 40% de diferença)?**
7. **COGS breakdown completo (produto + frete + pick&pack + gateway + taxas), sem valor agregado?**
8. **Margem $ ≥ $20 em pelo menos uma variação?** (senão CPA viável inviabiliza ads)
9. **Bundle structure aumenta AOV sem canibalizar margem?**
10. **breakeven_roas < 3.0?** (se >3, a oferta depende de CAC muito baixo — validar com @analyst)
11. **`04-offer-builder/research-foundation.json` existe e cobre todos os claims centrais do mecanismo com fonte rastreável?** (sem fundação de evidência, copy da Skill 06 sai sem lastro — bloqueante)

Registre o resultado em `04-offer-builder/dados.json` → `sanity_checks` como `{ "total": 11, "passed": N, "failed": [<números dos checks que falharam>] }` (NÃO um inteiro hard-coded). Se alguma resposta for "não", **itere antes de salvar**. Uma oferta fraca que passa adiante vira ad ruim, copy genérica, e membro frustrado em 30 dias.

**Bloqueio de save (checks críticos):** se QUALQUER um dos checks críticos falhar — check 3 (economics/PSM viável), check 8 (margem $ ≥ $20 em ao menos uma variação), ou check 11 (`04-offer-builder/research-foundation.json` cobre os claims centrais) — NÃO salve o `04-offer-builder/dados.json` final. Itere até passar, ou aplique o escape-path correspondente (ES1 pra foundation faltante; ETAPA 7 pra economics; ETAPA 1 sanity de margem). Os demais checks que falharem entram em `failed[]` como aviso, mas não bloqueiam.

### Output Schema — `04-offer-builder/relatorio.md` + `04-offer-builder/dados.json`

O markdown é humano; o JSON é para as skills 06/07/10/11/12. Estrutura obrigatória:

`.json`:
```json
{
  "offer_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "mechanism": {
    "name": "...",
    "version_short": "1 frase (inglês US se mercado for US)",
    "version_medium": "1 parágrafo (inglês US se mercado for US)",
    "version_long": "2-3 parágrafos (inglês US se mercado for US)",
    "sin_score": { "simplicity": 9, "intuitiveness": 8, "novelty": 7 }
  },
  "pricing": {
    "main_sku_price": 97.00,
    "aov_expected": 118.00,
    "currency": "USD"
  },
  "cogs_breakdown": {...},
  "unit_economics": {
    "margin_per_unit": 58.50,
    "weighted_margin_per_order": 72.00,
    "breakeven_cpa": 72.00,
    "breakeven_roas": 1.64,
    "target_cpa_for_2x": 36.00,
    "target_cpa_for_3x": 24.00,
    "target_cpa_primary_2x": 36.00,
    "target_cpa_primary_3x": 24.00,
    "psm_theoretical": 2.0
  },
  "guarantee": { "type": "...", "duration_days": 30 },
  "offer_stack": "Stack montado: produto principal $97 + Bonus 01 ($49) + Bonus 02 ($39) + Bonus 03 ($29) = valor total ancorado $214. Membro paga $97 (savings de $117). String pré-montada para a Skill 06 usar literal em copy de página/ad sem reformatar.",
  "bonuses": [
    {
      "id": "bonus-01",
      "name": "nome humano",
      "description": "o que é / por que vale",
      "value_anchored": 49,
      "type": "digital_guide|digital_template|physical_freebie|community_access|video_series|consultation_call|discount_code|trial_extension|workbook|checklist",
      "format_hint": "pdf|notion|figma|wistia|in_box|klaviyo_email|shopify_discount|circle_invite",
      "delivery_trigger": "post_purchase|on_signup|day_7_post_purchase|on_first_reorder"
    }
  ],
  "sanity_checks": { "total": 11, "passed": 11, "failed": [] }
}
```

Atualizar `manifest.json`: adicionar `target_cpa`, `breakeven_roas`, `psm_theoretical`, adicionar skill em `skills_completed`.

Depois de atualizar o manifest, regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza o `ABRIR-AQUI.html`).

**Nota sobre nomenclatura dos unit_economics** — `weighted_margin_per_order` é o denominador de margem CANÔNICO de toda a unit economics. TODOS os derivados saem dele, NÃO de `margin_per_unit`:
- `breakeven_cpa` = `weighted_margin_per_order`
- `target_cpa_primary_2x` = `weighted_margin_per_order / 2`
- `target_cpa_primary_3x` = `weighted_margin_per_order / 3`
- `breakeven_roas` = `aov_expected / weighted_margin_per_order`
- Sanidade: `target_cpa_primary_2x` < `breakeven_cpa` SEMPRE.

No exemplo acima: weighted_margin_per_order 72 → breakeven_cpa 72, target_2x 36 (72/2), target_3x 24 (72/3), breakeven_roas 1.64 (118/72). A Skill 11 (ad-analysis) lê por esses nomes "primary"/"weighted" e assume esse denominador único. Os campos legacy (`margin_per_unit`, `target_cpa_for_2x/3x`) são emitidos em paralelo só por compat. `weighted_margin_per_order` = margem média ponderada por AOV (considera bumps + upsells); `margin_per_unit` é a margem unitária do SKU principal. Se a oferta não tem bump/upsell, os dois valores são iguais — mas os derivados de CPA sempre referenciam `weighted_margin_per_order`. `offer_stack` é a string pré-montada que a Skill 06 consome literal.

**Se `04-offer-builder/dados.json` falhar validação, NÃO salvar `.md`.**

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer-builder/relatorio.md` → `04-offer-builder/relatorio.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).


`workspace/[produto]/04-offer-builder/relatorio.md` contendo:
1. Mecanismo único recomendado (com scoring das 5-7 opções geradas) + 3 versões (1 frase / 1 parágrafo / 2-3 parágrafos)
2. **Research Foundation** (Etapa 2.5) — evidências que sustentam o mecanismo, com fontes rastreáveis
3. Estrutura de oferta completa (produto principal, bundles, bump, upsell, stack de valor)
4. Garantia recomendada + copy
5. Tabela de unit economics (Etapa 5)
6. AOV projetado (Etapa 6)
7. PSM projetado (Etapa 7)
8. Viabilidade com budget (Etapa 8)
9. Respostas aos sanity checks (Etapa 9)

Também salvar companion `04-offer-builder/research-foundation.json` conforme schema da Etapa 2.5.

## Mensagem Final

"Oferta construída. Mecanismo único: **[Nome do Mecanismo]**. PSM projetado: [valor]. Viável pro seu budget: [sim/com ajustes].

Próximo passo: diga **'copy'** pra escrever a copy completa da página aplicando o mecanismo, stack, garantia, e linguagem do market research."

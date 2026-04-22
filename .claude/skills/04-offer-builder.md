---
name: offer-builder
description: Engine de construção de oferta com mecanismo único, stack de valor, bundles, bumps, upsells, garantia, e unit economics completa. Use quando o membro disser "offer", "oferta", "montar oferta", "construir oferta", "pricing", "bundle", ou quando o market research e competitor analysis estiverem prontos e o membro quiser estruturar a oferta antes de escrever a copy. A oferta é o MOTOR ECONÔMICO do negócio — decisões aqui determinam se ads são viáveis em escala.
---

# Offer Builder Engine

### Pré-flight (OBRIGATÓRIO)
Valide antes de prosseguir:
- [ ] `/workspace/[produto]/manifest.json` existe
- [ ] `02-market-research.json` existe (awareness_distribution, sophistication_stage)
- [ ] `03-competitor-analysis.md` existe
Se faltar qualquer um, PARE e peça ao membro rodar a skill faltante.

## Quando Usar
Quando o membro tem produto definido, market research pronto, e precisa construir a estrutura econômica completa: mecanismo único, preço, bundles, bumps, upsells, garantia, e unit economics viáveis pra escalar com ads pagos. Sem oferta estruturada, nenhum copy (por melhor que seja) vai converter sustentavelmente.

## Antes de Começar

1. Leia `/workspace/profile.md` (ferramentas disponíveis, budget diário — informa viabilidade econômica)
2. Leia `/workspace/[produto]/01-product-research.md` (se existir — tem features, COGS preliminar, potencial de oferta)
3. Leia `/workspace/[produto]/02-market-research.md` (pain points, desires, root cause, objeções — a oferta é a RESPOSTA direta ao market research)
4. Leia `/workspace/[produto]/03-competitor-analysis.md` (claims saturados a evitar, mecanismos já usados, gaps de oferta identificados)
5. Consulte a base Aura extensivamente sobre unique mechanisms (UMP/UMS, S.I.N. filter, ideação, avaliação, ranking, expansão), offer engineering (tipos de oferta, stack de valor, ancoragem), Hormozi value equation ($100M Offers — dream outcome, perceived likelihood, time delay, effort & sacrifice), pricing psychology (anchoring, decoys, framing), unit economics (COGS, margin, breakeven ROAS, target CPA), profitable scaling margin (PSM), garantias (risk reversal frameworks, money-back vs results-based vs extended trial), upsells e bumps (case studies, regras de checkout optimization), economia de funil, naming, e princípios clássicos de direct response sobre oferta (Hopkins, Ogilvy, Kennedy, Halbert). Aprofunde em cada framework até ter domínio completo — pricing é decisão estratégica, não técnica.

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

Documente cada um em `04-offer.json` → `cogs_breakdown`.

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

Se continuar, marca `"margin_warning": true` no manifest pra Skills 08/10 alertarem escala agressiva.

### ETAPA 2 — MECANISMO ÚNICO (A Parte Mais Importante)

O mecanismo único é o que diferencia seu produto de TODO concorrente. Sem mecanismo forte, a copy vira commodity disputando no preço. Com mecanismo forte, você cria um "blue ocean" dentro de qualquer nicho.

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

**Aplicar o filtro S.I.N.:**
- **Specific** (pode ser nomeado especificamente — "Joint Drought Protocol" em vez de "formula pra articulação")
- **Intriguing** (desperta curiosidade — "Lipid Barrier Breach" em vez de "hidratação")
- **New** (soa novo pro mercado, mesmo que a ciência subjacente seja antiga — reformulação criativa de algo conhecido)

Nomes pode vir de:
- Renomear ingredientes existentes pra novo propósito (ex: "Ceramide Matrix" em vez de "ceramidas")
- Combinar 2-3 features em conceito unificado (ex: "Triple Peptide Stack")
- Nomear um processo interno (ex: "48-Hour Activation")
- Reposicionar uma feature secundária como central (ex: transformar "com antioxidantes" em "Free Radical Neutralization System")

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

- **Versão de 1 frase** (pra headlines, hooks, ads): ex: "Nossa fórmula ativa a Triple Collagen Cascade em 48 horas."
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

Arquivo `/workspace/[produto]/04-research-foundation.json` contendo:
```json
{
  "mechanism_name": "...",
  "evidence_items": [ { ... } ],
  "summary_statement": "2-3 frases resumindo a base de evidência do mecanismo",
  "confidence_score": "high|medium|low",
  "gaps_and_risks": "claims que ficaram sem lastro forte — a serem suavizados na copy"
}
```

Esse arquivo é lido pelas skills 05 (copy) e 07 (creatives) pra ancorar afirmações com fonte verificável. Copy sem `research-foundation.json` acessível roda com warning "claims unverified — escalate carefully".

### ETAPA 3 — Estrutura de Oferta

Monte a arquitetura econômica completa:

**Produto Principal:**
- **Nome do produto** (se ainda não tem, sugira — pode incluir mecanismo no nome: ex: "ClariForm — Collagen Cascade Serum")
- **Preço base**: ver framework de pricing abaixo (triangulação de 3 ancoras)
- **Core deliverable**: o produto em si (1 unidade / X ml / Y cápsulas)

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

Regra de thumb (pode ajustar):
- 3-pack: ~25-35% savings vs 3× solo
- 6-pack: ~40-50% savings vs 6× solo

Marcar **Popular** no 3-pack (visualmente destacado — driver de AOV). Best Value no 6-pack (pra whales).

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

Liste tudo que vem no pacote com valor ancorado:
- Produto principal: valor $X
- Bonus 1 (ex: guia digital, checklist, protocol card): $Y
- Bonus 2 (ex: acesso a comunidade, suporte): $Z
- Bonus 3 (ex: consultoria inicial, material extra): $W
- **Valor total**: $X+Y+Z+W
- **Preço hoje**: $(preço real)
- **Economia percebida**: $(diferença)

Cada bonus é REAL (entregável), não inflado artificialmente. O stack cria percepção de valor desproporcional ao preço.

### ETAPA 4 — Garantia (Risk Reversal)

Consulte a base Aura sobre tipos de garantia e escolha:

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

**Breakeven ROAS** (o mínimo de ROAS pra empatar, antes de lucro):
- Breakeven ROAS = AOV / Margem $
- Exemplo: AOV $100, Custo Total $40, Margem $60 → Breakeven ROAS = 100/60 = 1.67
- Significa: precisa gerar $1.67 de revenue para cada $1 em ads só para empatar

**Target CPA** (CPA máximo para N× ROAS desejado):
- Target CPA para ROAS N = Margem $ / (N − 1)
- Exemplo: Margem $60, quer 2× ROAS → CPA máximo = 60/(2−1) = $60
- Para 3× ROAS → CPA máximo = 60/(3−1) = $30

**PSM** (Profit-to-Spend Multiple, após cobrir CAC):
- PSM = Margem $ / CPA observado (ex: Margem $60, CPA $30 → PSM = 2.0)
- Viabilidade: PSM >= 1.2 é mínimo; PSM >= 1.5 é confortável

**Regra crítica:** Target CPA pra 2× ROAS (= Margem $) deve ser ≥ $30 pra viabilizar scaling com ads pagos. Se Margem $ < $15-20, a oferta não sustenta ads a não ser em volume muito alto.

### ETAPA 6 — AOV Projetado (com Bump e Upsell Acceptance)

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

### ETAPA 7 — PSM Projetado (Profit-to-Spend Multiple)

Aplique os princípios de PSM (ver Etapa 5 pra fórmula completa).

**Fórmula:** PSM = Margem $ / CPA observado (ou projetado)

Considere também LTV ao longo de 30-60-90 dias (com reorder rate se aplicável) para refinar a avaliação de escala.

- **PSM < 1.0**: cada cliente perde dinheiro em escala — oferta NÃO viável
- **PSM = 1.0-1.2**: break-even, cresce devagar com risco
- **PSM > 1.2**: crescimento lucrativo, pode escalar com confiança
- **PSM > 1.5**: oferta forte, escala agressiva viável

Se PSM projetado < 1.2 — oferta **não é viável** com economics atuais. Sugira em ordem:
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
- AOV projetado × 3 vendas/dia = ~$Y/dia em revenue
- Margem total projetada = $Z/dia

É viável? Pra qual revenue tier (da Skill 10) essa oferta leva o membro em 30/60/90 dias?

### ETAPA 9 — Validação Final (Sanity Checks)

Antes de salvar, responda HONESTAMENTE:

1. **A oferta faz sentido pro awareness level dominante?** (se é Problem Aware, a oferta foca em educação; se é Product Aware, foca em diferenciação; etc)
2. **O mecanismo é genuinamente diferente dos concorrentes?** (passa no filtro S.I.N. + não é commodity do estágio de sophistication)
3. **As economics permitem escalar?** (PSM > 1.2, CPA target viável com budget do membro)
4. **O stack de valor é convincente SEM inflar?** (cada bonus é real, útil, entregável)
5. **A garantia quebra a objeção de risco identificada no market research?** (não é genérica — ataca o medo específico do avatar)
6. **Pricing triangulado (as 3 ancoras convergem < 40% de diferença)?**
7. **COGS breakdown completo (produto + frete + pick&pack + gateway + taxas), sem valor agregado?**
8. **Margem $ ≥ $20 em pelo menos uma variação?** (senão CPA viável inviabiliza ads)
9. **Bundle structure aumenta AOV sem canibalizar margem?**
10. **breakeven_roas < 3.0?** (se >3, a oferta depende de CAC muito baixo — validar com @analyst)
11. **`04-research-foundation.json` existe e cobre todos os claims centrais do mecanismo com fonte rastreável?** (sem fundação de evidência, copy da Skill 05 sai sem lastro — bloqueante)

Se alguma resposta for "não", **itere antes de salvar**. Uma oferta fraca que passa adiante vira ad ruim, copy genérica, e membro frustrado em 30 dias.

### Output Schema — `04-offer.md` + `04-offer.json`

O markdown é humano; o JSON é para as skills 05/06/08/09/10. Estrutura obrigatória:

`.json`:
```json
{
  "offer_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "mechanism": {
    "name": "...",
    "version_short": "1 frase",
    "version_medium": "1 parágrafo",
    "version_long": "2-3 parágrafos",
    "sin_score": { "specificity": 9, "intrigue": 8, "novelty": 7 }
  },
  "pricing": {
    "main_sku_price": 97.00,
    "aov_expected": 127.50,
    "currency": "BRL"
  },
  "cogs_breakdown": {...},
  "unit_economics": {
    "margin_per_unit": 62.50,
    "breakeven_roas": 2.04,
    "target_cpa_for_2x": 62.50,
    "target_cpa_for_3x": 31.25,
    "psm_theoretical": 2.0
  },
  "guarantee": { "type": "...", "duration_days": 30 },
  "bonuses": [...],
  "sanity_checks_passed": 9
}
```

Atualizar `manifest.json`: adicionar `target_cpa`, `breakeven_roas`, `psm_theoretical`, adicionar skill em `skills_completed`.

**Se `04-offer.json` falhar validação, NÃO salvar `.md`.**

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `/workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer.md` → `04-offer.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).


`/workspace/[produto]/04-offer.md` contendo:
1. Mecanismo único recomendado (com scoring das 5-7 opções geradas) + 3 versões (1 frase / 1 parágrafo / 2-3 parágrafos)
2. **Research Foundation** (Etapa 2.5) — evidências que sustentam o mecanismo, com fontes rastreáveis
3. Estrutura de oferta completa (produto principal, bundles, bump, upsell, stack de valor)
4. Garantia recomendada + copy
5. Tabela de unit economics (Etapa 5)
6. AOV projetado (Etapa 6)
7. PSM projetado (Etapa 7)
8. Viabilidade com budget (Etapa 8)
9. Respostas aos sanity checks (Etapa 9)

Também salvar companion `04-research-foundation.json` conforme schema da Etapa 2.5.

## Mensagem Final

"Oferta construída. Mecanismo único: **[Nome do Mecanismo]**. PSM projetado: [valor]. Viável pro seu budget: [sim/com ajustes].

Próximo passo: diga **'copy'** pra escrever a copy completa da página aplicando o mecanismo, stack, garantia, e linguagem do market research."

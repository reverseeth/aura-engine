---
name: copy-engine
description: Engine de escrita de copy completo baseado em market research, competitor analysis, e oferta. Escreve PDPs, landing pages, advertoriais, ou long-form sales pages aplicando headlines (processo de 100 linhas, fórmulas), leads tipados por awareness, hero sections (5 tipos), 10x page plan, frameworks de persuasão (Cialdini, Sugarman, Hopkins), proof stacking, CTAs (call to value), 7 sweeps de revisão, e linguagem EXATA do customer. Use quando o membro disser "copy", "escrever copy", "copy da página", "copy do ad", "PDP copy", "landing page copy", ou após a skill de oferta. O sistema DECIDE a estratégia de copy automaticamente — não consulta o membro sobre decisões estratégicas.
---

# Copy Engine

### Pré-flight (OBRIGATÓRIO)
- [ ] `/workspace/[produto]/manifest.json` existe
- [ ] `product_slug` do manifest NÃO começa com `dev-placeholder-` (senão, pare: "rode product research primeiro")
- [ ] `02-market-research.json` existe → extrair `awareness_distribution`, `sophistication_stage`, `voc_phrases`, `voc_count`, `voc_adequacy`
- [ ] **VOC adequacy check:** se `voc_adequacy == "insufficient"` OU `voc_count < 15` → PARE com mensagem:
  > ⚠️  VOC atual: {N} frases únicas. Mínimo pra copy direta: 15.
  >     Copy sem VOC real é invenção — vai soar genérica e não converter.
  >     Opções:
  >     1. Rode skill 02 (market-research) de novo com mais fontes (Reddit, Amazon reviews, TikTok comments)
  >     2. Me cola manualmente 10-15 frases de clientes reais (reviews, DMs, comentários)
  >     3. Prossiga mesmo assim reconhecendo limitação (copy ficará abstrata)

  Se membro escolher 3, marca `"voc_forced_continue": true` no output pra Skill 09 diagnosticar depois.
- [ ] `03-competitor-analysis.md` existe
- [ ] `04-offer.json` existe → extrair `mechanism`, `pricing`, `guarantee`
- [ ] `04-research-foundation.json` existe → extrair `evidence_items[]`, `confidence_score`, `gaps_and_risks`
  - Se ausente: WARN "Research foundation não rodou (Skill 04 Etapa 2.5). Claims na copy vão sair sem lastro verificável. Opções: (1) voltar pra skill 04 e rodar Etapa 2.5; (2) prosseguir marcando `claims_unverified: true` no output — skill 11 (consistency-audit) vai bloquear launch depois."
  - Se existe mas `confidence_score == "low"`: WARN "Evidence weak — claims fortes (clinically proven, X% melhoria) vão ser suavizados automaticamente pra 'helps with', 'designed to support'. Skill 11 vai re-validar antes de launch."
- [ ] Extrair `product_vertical` do manifest (default "other" se ausente) — usado pelo Compliance Pre-flight (Sweep 8)
Se faltar qualquer um (exceto VOC com opção 3 e research-foundation com acknowledgment), PARE.

## Quando Usar
Quando o membro tem market research, competitor analysis e oferta prontos, e precisa escrever a copy da página que vai converter o tráfego pago. Copy aqui é escrita com base em decisões ESTRATÉGICAS derivadas dos documentos anteriores, não em opiniões ou intuições.

## Antes de Começar

1. Leia `/workspace/profile.md`
2. Leia `/workspace/[produto]/02-market-research.md` (psychographics, awareness/sophistication, VOC literal, objeções, root cause)
3. Leia `/workspace/[produto]/03-competitor-analysis.md` (claims saturados a evitar, gaps, posicionamento recomendado, swipe file)
4. Leia `/workspace/[produto]/04-offer.md` (mecanismo único com 3 versões, bundles, garantia, unit economics)
5. Consulte a base Aura extensivamente sobre copywriting: headlines (processo de 100 linhas, fórmulas clássicas de Caples/Hopkins/Schwartz/Sugarman), leads (5 tipos por awareness de Schwartz — Story Lead, Secret Lead, Proclamation Lead, Problem-Solution Lead, Offer/Direct Lead), hero sections (5 tipos e quando usar cada), 10x page plan, landing page frameworks, long-form sales page structure (15-point themeplate), VSL structure (8 blocos), advertorial blueprint (7 seções Zakaria), listicles como advertorial, techniques de persuasão (even-if, loss aversion, future pacing, belief stacking), Cialdini's 6 principles + pre-suasion, Sugarman's triggers (slippery slide, sentence rhythm, curiosity), StoryBrand SB7, Kennedy sales letter structure, proof e credibilidade (testimonials, authority, specificity de Hopkins), CTAs como call to value (não call to action), crossheads e estrutura visual, 4 decision making modalities (Spontaneous/Competitive/Humanistic/Methodical), rule of one, 7 sweeps de revisão, behavioral psychology (System 1 vs System 2), wireframing e validação, frameworks como PAS/AIDA/PASO/PCPO, brand voice e tom, e qualquer framework adjacente que apareça. **Esta skill é o coração do sistema — explore cada framework de copy a fundo.**

## Fluxo da Skill

### Input Extraction (automático)
Antes de gerar copy, carregue:
1. `dominant_awareness` = stage com maior % em `awareness_distribution` do market research JSON
2. `sophistication` = `sophistication_stage` (1-5)
3. `voc_checklist` = array das 20 VOC phrases mais repetidas (substring matching em `voc_phrases`)
4. `mechanism` = do `04-offer.json`
5. `guarantee` + `offer_stack` = do `04-offer.json`
Use ESTAS variáveis ao gerar — sem placeholders hardcoded.

### ETAPA 1 — Perguntas ao Membro (APENAS 2)

Faça APENAS estas duas perguntas:

**1. Tipo de página:**
"Que tipo de página vamos escrever?
- PDP (Shopify)
- Landing Page dedicada
- Advertorial
- Não sei (o sistema recomenda baseado no awareness level)"

Se o membro disser "não sei", use o awareness level dominante do market research pra decidir:
- **Unaware / Problem Aware** → Advertorial (educação antes do pitch)
- **Solution Aware** → Landing Page dedicada
- **Product Aware / Most Aware** → PDP

**2. Página atual:**
"Tem página atual que quer melhorar? Se sim, me manda o link."

- SE mandar o link: leia/extraia a página (web fetch) e use como baseline — identifique o que manter (o que funciona) e o que reescrever (o que tá fraco).
- SE não tiver: partimos do zero.

**NENHUMA outra pergunta ao membro.** Todas as decisões estratégicas abaixo são tomadas automaticamente pelo sistema.

### ETAPA 2 — Estratégia de Copy (SISTEMA DECIDE)

O sistema apresenta as decisões como FATO (não pedido de aprovação) e segue pra escrita. Todas vêm do market research + competitor analysis + oferta:

**Tipo de Lead** (5 tipos de Schwartz):

| Awareness dominante | Lead recomendado |
|---|---|
| Unaware | Story Lead ou Big Idea Lead |
| Problem Aware | Problem-Solution Lead ou Story Lead |
| Solution Aware | Secret Lead ou Proclamation Lead |
| Product Aware | Offer Lead ou Direct Lead |
| Most Aware | Direct Lead (apela pra oferta/urgência direto) |

**Tipo de Hero Section** (5 tipos):
- **Authority hero** (expert, doctor, scientist apresentando): indicado pra Solution Aware + high-trust products
- **UGC/Testimonial hero**: indicado pra Problem Aware + baixa confiança inicial
- **Product-hero** (produto em destaque): Product Aware + Most Aware
- **Problem-agitate hero**: Problem Aware com dor forte e frequente
- **Demo/before-after hero**: quando transformação visual é forte e rápida

Decisão aplica: awareness + tipo de produto + presença de visual transformation + tipo de cetiscismo do avatar.

**Ângulo Principal** (do competitor analysis):
- Escolha o gap mais forte identificado na Skill 03 (angle que NENHUM concorrente está usando)
- Esse vira o **Big Idea** da página — o ângulo dominante que unifica headline, subheadline, e hook

**Tom de Voz** (do market research):
Definido pelo perfil psicográfico:
- Sofisticado/educado (público com renda alta, educação, sophistication interna)
- Casual/conversacional (público mainstream, Gen Z/millennial)
- Técnico/autoridade (público que valoriza credenciais — saúde, finanças)
- Emocional/empático (público vulnerable — chronic pain, grief, self-image)
- Urgente/direto (público transactional, maduro em ads)

**Framework de Organização:**
- **PDP** → estrutura: Hero → Trust Bar → Benefícios → Mecanismo → Prova Social → Oferta/Stack → Garantia → FAQ → CTA final
- **Landing Page** → 10x Page Plan ou PAS on Steroids
- **Advertorial** → 7-section blueprint (Zakaria): Headline → Lead → Background Story → Root Cause → Unique Mechanism → Product Build-Up → Product Reveal → Close
- **Long-form Sales Page** → 15-point themeplate ou 8-block VSL structure

**Como servir as 4 Decision Making Modalities**:

Toda página precisa SIMULTANEAMENTE servir os 4 tipos de decisor (senão perde conversão de 25-75% dos visitantes):

- **Spontaneous** (decide rápido, emocional) → hero visual forte + promessa clara + CTA óbvio acima do fold
- **Competitive** (quer dominar, odeia perder vantagem) → comparação, "best in class", escassez, urgência
- **Humanistic** (empático, social) → testimonials, UGC, story do fundador, comunidade
- **Methodical** (analítico, quer provas) → ingredient breakdown, estudos, FAQ detalhada, specs, reviews com detalhes técnicos

Apresente a estratégia (6-8 linhas no máximo) como um BRIEF antes de escrever:

> Baseado no market research (awareness: {{dominant_awareness}}, Sophistication: Estágio {{sophistication_stage}}) e gaps do competitor analysis ([gap X]), vou escrever [tipo de página] com [tipo de lead], hero [tipo], ângulo [ângulo], tom [tom], usando o framework [X]. Mecanismo único: {{mechanism.name}}. VOC phrases prioritárias: [3 frases-chave do voc_checklist]. Objeções principais a quebrar: [3].

(Os placeholders `{{...}}` indicam valores vindos do Input Extraction — NÃO usar números fixos como "45%" ou "Estágio 4".)

Não peça aprovação — segue direto pra escrita. O membro pode ajustar depois se quiser, mas o default é o sistema executar a decisão fundamentada.

### ETAPA 3 — Headlines (Processo de 100 Linhas)

Aplique os princípios de o processo de 100 linhas (Caples, expandido) e as fórmulas clássicas.

**3A — Geração (20-30 variações):**

Gere 20-30 variações de headline aplicando as fórmulas. Cobrir diferentes tipos:

- **Benefício direto**: "Get [outcome] without [pain]"
- **Curiosidade**: "The [adjective] secret [audience] don't know about [topic]"
- **Problema**: "If you [problem], you're not alone — but there's a reason"
- **Resultado com especificidade**: "[Specific number] [specific outcome] in [specific time]"
- **Mecanismo único**: "Introducing the [mechanism name] — [what it does]"
- **Contrarian/controversy**: "Why [common belief] is actually making [problem] worse"
- **Question hook**: "What if [familiar problem] wasn't your fault?"
- **Testimonial hook**: "[Specific person] lost [specific number] in [time] — here's how"
- **Authority**: "[Expert title] reveals the [claim]"
- **Fear of loss**: "The [thing you're missing] that [outcome]"

Use linguagem EXATA do VOC do market research sempre que possível. Hopkins: "specificity in headlines converts 2-3x over generality".

**3B — Categorização + Top 5:**

Categorize as 20-30 por tipo. Selecione **top 5** com justificativa explícita por que cada uma funciona pro awareness level + ângulo + tom + Big Idea.

**3C — 3 pra Teste A/B:**

Das top 5, escolha 3 que representam HIPÓTESES DIFERENTES (não variações cosméticas):
- Headline 1: hipótese de ângulo dominante
- Headline 2: hipótese alternativa (ângulo secundário)
- Headline 3: hipótese de formato diferente (ex: pergunta vs afirmação)

Justifique cada escolha.

### ETAPA 4 — Página Completa (Seção por Seção)

Escreva a página inteira, seção por seção, na ordem definida pelo framework escolhido. Para cada seção, aplique frameworks específicos.

#### Hero Section

- **Headline**: a #1 das top 5 (pode ajustar um pouco pra fit com hero)
- **Sub-headline**: 1-2 linhas que expandem a promessa, introduzem o mecanismo único
- **CTA principal**: texto do botão (call to VALUE, não call to action — ex: "Get My [Outcome]" em vez de "Buy Now")
- **Instrução visual**: que imagem/vídeo colocar (hero type já decidido — authority/UGC/product/problem/demo)

#### Trust Bar (opcional)

Se o produto tem credenciais (mídia coverage, certificações, reviews count), coloca logo abaixo do hero:
"Featured in Forbes · 4.8★ (12,000 reviews) · Dermatologist-tested"

#### Benefits / Problem Block

Use a linguagem EXATA do VOC. Não parafraseie. Cada bullet:
- Começa com a frase/palavra do consumidor (do market research)
- Expande com o benefício funcional
- Termina com o emocional (o "por trás do por trás" do desejo)

3-5 bullets de benefício. Se é Problem Aware/Unaware, começa com dor; se é Solution/Product Aware, começa com resultado.

#### Unique Mechanism Expandido

Use a **versão 1 parágrafo** do mecanismo da oferta (ou a 2-3 parágrafos se for LP dedicada ou advertorial). Adaptado ao awareness level:
- Problem Aware → explica a root cause ANTES do mecanismo (educação)
- Solution Aware → compara com soluções genéricas e posiciona o mecanismo como a evolução
- Product Aware → foca na especificidade do mecanismo (ingredientes, dosagem, processo)

Inclua:
- Nome do mecanismo (do 04-offer.md)
- Como funciona (biology/mechanism of action se aplicável)
- Por que é diferente
- Referência a evidência (estudo, ingredient research, patents se aplicável)

#### Prova Social (Proof Stacking)

Aplicar os frameworks de proof (Hopkins specificity, Sugarman satisfaction conviction, Made to Stick credibility):

- **Social proof volume**: número de clientes, reviews, anos no mercado
- **Specific testimonials**: 3-5 testimonials com NOMES COMPLETOS, FOTOS, e RESULTADOS ESPECÍFICOS (com datas e números quando possível)

  Se o membro não tem testimonials reais ainda (lançamento novo):
  - Use `{{TESTIMONIAL_PLACEHOLDER_1}}` no copy e liste no final:
    "### Testimonials needed: [frase_motora, resultado_especifico, perfil_demografico] × 3"
  - NÃO gere testimonials fictícios com nomes aleatórios.
  - Proof stack fica com placeholder até membro coletar via email / WhatsApp com clientes existentes.
- **Authority proof**: menções em mídia, certificações, endorsement de experts
- **Before/After** (se visual e o produto permite): imagens com legendas
- **Science/ingredient research**: evidência técnica se apropriado

Organize em formato visual navegável (tiles, carrossel, grid).

#### Oferta / Stack Com Ancoragem

Do `04-offer.md`:
- Produto com nome
- Bundles (Solo / Popular 3-pack / Best Value 6-pack) com savings visíveis
- Bump (produto complementar baixo ticket)
- Stack de valor: "Você recebe [X + Y + Z] no valor de $[total ancorado]. Hoje: $[preço]"
- Savings visíveis ("Você economiza $[diff] hoje")

Aplique **pricing psychology**: ancoragem de preço, decoy effect (3-pack Popular faz 1-pack parecer caro e 6-pack parecer econômico), framing (foco em "savings" não em "preço").

#### Garantia

Do `04-offer.md`, a copy de garantia (2-3 frases, tom confiante, detalhes claros).

Posicione com destaque visual (box, shield icon, destaque colorido).

#### FAQ

Cada FAQ quebra uma objeção REAL do market research. Pegue as **Top 5 objeções priorizadas** da Skill 02 e escreva a resposta que quebra cada uma. Nada de FAQ genérica ("qual o prazo de envio" — isso vai em lugar específico, não é FAQ estratégica).

FAQ estratégica típica:
- "Vai funcionar pra mim se eu já tentei X?" (quebra "já tentei e não deu certo")
- "É seguro pra [condição específica do avatar]?" (quebra medo)
- "E se não funcionar?" (reforça garantia)
- "Por que é diferente do [concorrente comum]?" (quebra comparação)
- "Quando começo a ver resultado?" (quebra time delay)

#### CTA Final

Call to VALUE, não call to action. Reforça o outcome + remove fricção:
- "Claim My [Outcome]" (não "Buy Now")
- "Start My [Transformation]"
- "Get [Specific Result] Today"

Repita CTA em 3-5 pontos da página (após hero, após mecanismo, após social proof, após oferta, no final).

#### Seções Adicionais (se fizer sentido)

- **Comparação com concorrentes** (se Product Aware): tabela "Nosso produto vs [concorrente A] vs [concorrente B]" com dimensões claras (ingrediente, preço, guarantee, mechanism)
- **How it works** (se mechanism exige explicação): 3-step visual (Step 1 → Step 2 → Step 3) com ícones e copy curta
- **Before/After grid** (se visual): 3-4 comparisons
- **Ingredient/feature spotlight** (se ingredient-based mechanism): cada ingrediente com benefit e research

### ETAPA 5 — Se for ADVERTORIAL (Alternativa à Etapa 4)

Se o tipo de página definido é Advertorial, siga a **estrutura de 7 seções** (Zakaria blueprint):

1. **Irresistible Headline** (estilo editorial, não-vendedor: "The Weird 30-Second Ritual That's Changing How Women Over 40 Handle [Problem]")
2. **Lead** que pulls readers in (primeiras 100-200 palavras — responde as 4 perguntas mentais do leitor: por que ler agora? por que isso importa? por que isso é diferente? por que vai funcionar pra mim?)
3. **Background Story** (storytelling pessoal ou de terceiro — builds empathy + credibility — aplica a Discovery Story)
4. **Root Cause Explanation** — use a causa raiz do market research (Etapa 6 da Skill 02). Explique o problema de forma clara, externaliza a culpa (genética, hormônios, indústria — NÃO o leitor)
5. **Unique Mechanism Reveal** — apresente o mecanismo único como a descoberta, a revelação (use a versão de 2-3 parágrafos do 04-offer.md)
6. **Product Build-Up** — traz o produto no contexto do mecanismo. Primeiros parágrafos são sobre o MÉTODO/PRODUTO antes da oferta
7. **Product Reveal + Close** — oferta, stack, garantia, urgência, CTA. Manipulation close (scarcity real, bonus que expiram, urgency com razão)

Tom editorial (não vendedor). Use parágrafos curtos (2-4 linhas). Inclua imagens/quotes entre parágrafos.

### ETAPA 6 — Auto-Revisão (7 Sweeps)

Antes de entregar, faça **7 sweeps de revisão** :

1. **Clarity sweep**: cada frase é clara em primeira leitura? Jargão sem explicação?
2. **Customer voice sweep (VOC compliance)**: checklist dinâmico — passe o `voc_checklist` como lista. Para cada frase VOC:
   - [ ] Aparece LITERAL no copy? (marca se sim)
   - [ ] Aparece parafraseada? (marca se só aproximação)
   - [ ] Ausente? (marca como gap)

   Taxa mínima: >= 60% das top-20 VOC phrases presentes literais ou parafraseadas. Se < 60%, regerar seções fracas.
3. **Specificity sweep**: Hopkins — cada claim genérico foi substituído por específico? ("many customers" → "12,847 customers"; "fast results" → "visible improvement in 14 days")
4. **Flow sweep**: slippery slide de Sugarman — cada frase compele a próxima? Onde há quebra de fluxo?
5. **Objection sweep**: cada objeção do market research foi quebrada em algum lugar? Onde está omitida?
6. **CTA sweep**: CTAs são call to VALUE? Aparecem em frequência certa (não muito, não pouco)?
7. **Originality sweep**: comparar com os claims saturados do competitor analysis — onde estou usando um claim saturado? substitua por ângulo original.
8. **Compliance Pre-flight sweep** (OBRIGATÓRIO antes de salvar o arquivo final):

   Claude deve rodar este prompt INLINE (não invocar arquivo externo) pra cada peça de copy gerada — headlines, primary texts, advertorial sections, CTAs, crossheads:

   ```
   Você é Compliance Pre-flight Checker. Analise a copy abaixo contra Meta Ad Policy, FTC substantiation, FDA cosmetic boundary (se vertical = beauty/skincare/supplements), e AI style red flags.

   Vertical: {product_vertical do manifest — default "other"}
   Asset type: {headline | primary_text | advertorial_section | cta | crosshead}
   Plataforma: Meta Ads (padrão)

   Red flags de referência (categoria do vertical): {leia `.claude/lib/compliance-preflight/red_flags.json`, filtre pelo vertical}

   Copy a analisar:
   \"{copy_text}\"

   Retorne JSON conforme `.claude/lib/compliance-preflight/output-schema.json`:
   {
     "risk_score": 0-100,
     "severity": "low|medium|high|critical",
     "overall_verdict": "APPROVE|APPROVE_WITH_EDIT|REVISE|REJECT",
     "triggers": [{"phrase": "...", "severity": "...", "reason": "...", "eixo": "...", "suggested_replacement": "..."}],
     "rewrite_suggestion": "..." // só se severity >= high
     "em_dash_count": N,
     "ai_style_score": 0-10,
     "recommendation": "..."
   }
   ```

   Ação conforme severity:
   - `critical` → PARAR, reportar triggers ao membro, aplicar `rewrite_suggestion` ou pedir revisão manual
   - `high` → aplicar `rewrite_suggestion` automaticamente + logar em `/workspace/[produto]/05-compliance-log.json`
   - `medium` → manter copy original, logar warning
   - `low` → salvar silenciosamente (sem output)

   Log consolidado em `/workspace/[produto]/05-compliance-log.json`. Se diretório não existir, `mkdir -p` antes de escrever.

Para cada sweep, documente o que mudou (as edits são o output do sweep).

### ETAPA 7 — Variações pra Teste A/B

Gere:
- **3 headlines** diferentes (já feito na Etapa 3C — compile aqui)
- **2 hero sections** com abordagens diferentes (authority vs problem-agitate, por exemplo)
- **2 CTAs diferentes** (call to value variations)

Documente a hipótese por trás de cada variação.

## Output Schema — Seções Canônicas (`05-copy.md`)

O markdown DEVE ter as seções NOMEADAS ASSIM (case-sensitive, H2). Cada seção contém texto pronto pra colar, SEM comentários de instrução no output final.

```
## Hero
### Headlines (ranked)
### Subheadline
### CTA Primary
### CTA Secondary

## Mechanism
## Benefits
## Social Proof
## Offer Stack
## Guarantee
## FAQ
## Urgency/Scarcity
## Email Follow-up Hooks
```

## JSON Companion Obrigatório — `05-copy.json`

Schema:
```json
{
  "copy_id": "uuid-v4",
  "product_slug": "...",
  "offer_id": "ref ao 04-offer.json",
  "hero": {
    "headlines": [
      {"id": "h-01", "text": "...", "type": "benefit|curiosity|authority|contrarian|big_idea", "score": 9.2, "reasoning": "..."}
    ],
    "top_5_ranked": ["h-01", "h-07", "h-12", "h-03", "h-18"],
    "ab_test_picks": ["h-01", "h-07", "h-12"],
    "subheadline": "...",
    "cta_primary": "...",
    "cta_secondary": "..."
  },
  "mechanism_copy": "...",
  "benefits": [{"title": "...", "body": "...", "voc_refs": ["..."]}],
  "social_proof": {"testimonials": [...], "proof_stack": [...]},
  "offer_stack": "...",
  "guarantee_copy": "...",
  "faq": [{"q": "...", "a": "..."}],
  "urgency": "...",
  "email_hooks": ["..."],
  "voc_compliance": { "total_checked": 20, "literal_hits": 14, "paraphrased": 5, "missing": 1 },
  "decision_modalities_covered": ["spontaneous", "competitive", "humanistic", "methodical"]
}
```

**Skill 06 vai ler diretamente este JSON** — se inválido, skill 06 não prossegue.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de salvar, garanta o diretório:** `mkdir -p /workspace/[produto]/`.

**Toda skill que salva `.md` em `/workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `05-copy.md` → `05-copy.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

Atualizar `manifest.json`: adicionar `05-copy-engine` em `skills_completed`, atualizar `updated_at`.

`/workspace/[produto]/05-copy.md` contendo (seções canônicas acima):
1. Strategy brief (Etapa 2 — tipo de página, lead, hero, ângulo, tom, framework, modalities mapping)
2. 20-30 headlines geradas + top 5 + 3 pra teste A/B
3. Página completa seção por seção (Etapa 4 ou 5)
4. Revisão após 7 sweeps (mudanças documentadas, incluindo VOC compliance %)
5. Variações pra teste (Etapa 7)

Também salvar `/workspace/[produto]/05-copy.json` no schema acima.

## Mensagem Final

"Copy completa pro [tipo de página]. Big Idea: [big idea]. Mecanismo aplicado: [nome]. VOC integrado, objeções quebradas, 3 variações de headline pra teste.

Próximo passo: diga **'page'** pra construir a página no Shopify (aplicar a copy no tema atual ou clonar o design de um concorrente que você gosta). Só depois da página pronta é que fazemos os criativos — não adianta criar ads pra uma página que ainda não existe."

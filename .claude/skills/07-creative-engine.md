---
name: creative-engine
description: Engine de criação de briefings de criativos para Meta Ads (3-2-2 format). Gera conceitos baseados nas 3 verticais de pesquisa (competitiva, consumidor, interna), produz briefings completos com scripts de vídeo segundo-a-segundo, hooks exatos, image ad specs, primary texts meaningfully different, headlines, LP congruency recommendations, e hooks bank pra iterações futuras. Use quando o membro disser "creatives", "criativos", "briefings", "ads", "criar anúncios", ou quando a copy estiver pronta. A mensagem final orienta edição em ferramentas externas (CapCut, Submagic, Captions) + voiceover no ElevenLabs.
---

# Creative Engine

## Quando Usar
Quando o membro tem copy pronta (Skill 05) e precisa dos briefings de criativos pra rodar no Meta. Cada briefing é completo: tudo que precisa pra filmar ou gerar (UGC humano, UGC com AI, stock, ou imagem), editar, e subir no Ads Manager.

## Antes de Começar

### Pré-flight (OBRIGATÓRIO)
- [ ] `manifest.json` existe com 05-copy-engine em skills_completed
- [ ] `04-offer.json` (target_cpa, mechanism) existe
- [ ] `02-market-research.json` (awareness_distribution, voc_phrases) existe
- [ ] **Pixel/CAPI validados**: pedir screenshot do Events Manager mostrando Match Quality ≥ 80% — se membro não pode fornecer, AVISAR que criativos serão desperdiçados e sugerir configurar pixel primeiro
- [ ] Se existe `/workspace/[produto]/09-analysis/NEXT_BATCH_IDEAS.md` (output do loop 09→07 fechado), LER e usar como input para priorizar ângulos no novo batch

### Quando rodar essa skill (decision tree)
- **Primeira vez** (nunca rodou para este produto): sim, proceed
- **Após skill 09 recomendar 'creatives'**: sim, proceed — LER NEXT_BATCH_IDEAS.md primeiro
- **Refresh por fadiga**: só execute se `09-ad-analysis` reportou no último ciclo:
  - `frequency > 1.4` E `ctr_drop_pct > 20` em 7 dias, OU
  - CPM subiu > 30% em 7 dias com freq < 1.3 (saturation de audience), OU
  - top-performing criativo tem > 14 dias de idade
- **Diversificação** (skill 10 pediu mais diversity): use ratio "2× budget → 2× creative" só em escala >$1k/dia; abaixo disso, use 1.5×

### Contexto a carregar

1. Leia `/workspace/profile.md` (budget → informa quantos conceitos testar; ferramentas → informa tipo de material viável)
2. Leia `/workspace/[produto]/02-market-research.md` (VOC literal, trigger events, objeções, dores/desejos hierarquizados, root cause — TUDO vai pra script)
3. Leia `/workspace/[produto]/03-competitor-analysis.md` (top criativos transcritos dos concorrentes, gaps de formato/ângulo, swipe file, claims saturados)
4. Leia `/workspace/[produto]/04-offer.md` (mecanismo único com 3 versões, stack, garantia)
5. Leia `/workspace/[produto]/05-copy.md` (big idea, headlines top 5, CTAs, linguagem usada na LP)
6. Consultas à base de conhecimento (tópicos-chave com resumo inline + referência):

   **Hook-Bridge-Hold-CTA** (estrutura de vídeo ad):
   - Hook (0-3s) captura atenção com pattern interrupt + Big 4 emotion dominante
   - Bridge (3-8s) transiciona da promessa pro corpo estabelecendo credibilidade
   - Hold (8-18s) desenvolve mecanismo/proof/benefit usando slippery slide (cada frase compelle a próxima)
   - CTA (18-22s) call-to-value (não action) + guarantee badge visual
   - [REF: knowledge base query — `mcp__aura__search_knowledge("hook bridge hold CTA video ads")`]

   **Big 4 Emotions** (escolher 1 dominante por hook):
   - Curiosity (pattern interrupt, mistério), Urgency (tempo/escassez real), Fear (dor amplificada), Delight (desejo/transformação)
   - [REF: knowledge base query — `mcp__aura__search_knowledge("Big 4 Emotions hook")`]

   **Slippery Slope** (Sugarman, estrutura de copy):
   - Primeira frase existe só pra fazer ler a segunda; segunda pra fazer ler a terceira; cada linha é um gancho pro próximo
   - Aplicação em vídeo: cada beat de 2-3s tem pattern interrupt visual ou verbal
   - [REF: knowledge base query — `mcp__aura__search_knowledge("slippery slope Sugarman copy")`]

   Tópicos adicionais a consultar conforme necessário: `[REF: mcp__aura__search_knowledge("3-2-2 flexible ads format")]`, `[REF: mcp__aura__search_knowledge("ad angles 3 research verticals")]`, `[REF: mcp__aura__search_knowledge("funnel creative playbook Olympic Rings")]`, `[REF: mcp__aura__search_knowledge("ugly ads convert image")]`, `[REF: mcp__aura__search_knowledge("UGC pipeline creator briefs Zakaria")]`, `[REF: mcp__aura__search_knowledge("natural speech converter voiceover")]`, `[REF: mcp__aura__search_knowledge("winning ad rate 9 step process")]`.

## Fluxo da Skill

### ETAPA 1 — Material Disponível + Creator Archetype (Pergunta 1)

Pergunte:

"Que tipo de material você tem pra montar os ads?
- Clips do TikTok/Reels de outros criadores (stolen-footage style)
- Vídeos do fornecedor/fabricante
- UGC gerado por AI (Higgsfield, Arcads, HeyGen, etc)
- Fotos de produto
- Creator humano contratado (pago pra gravar)
- Self-recorded (você mesmo grava)
- Mix de tudo acima"

**Creator Archetype Auto-Selection (realista):**

A maioria dos membros NÃO vai pagar creator humano ($150-500 por vídeo) e NÃO vai querer gravar a si mesmo (barreira alta). Selecione archetype default com base na resposta + budget do profile:

| Resposta do membro | Budget < $500/mês | Budget $500-2k/mês | Budget > $2k/mês |
|--------------------|-------------------|--------------------|-------------------|
| "não tenho nada" / "só fotos" | **AI UGC + stock + motion graphics** (default) | AI UGC + founder-led opcional | AI UGC + 1-2 creators humanos |
| "tenho clips do TikTok" | Stolen-footage + AI UGC | Stolen-footage + AI UGC | Stolen-footage + creator humano |
| "tenho vídeo do fornecedor" | Demonstração + motion graphics | Demo + AI UGC complementar | Demo + creator humano |
| "posso gravar eu mesmo" | Founder-led + AI UGC | Founder-led + AI UGC | Founder-led + creator humano |
| "tenho creator contratado" | Raro — mas priorize o creator | Creator humano primary | Creator humano primary |

**Default geral (se membro estiver em dúvida):** AI UGC + stock + motion graphics. Esse mix é acessível, escalável, e cobre 80% dos cenários.

Use o archetype pra influenciar FORMATO e SCRIPT dos conceitos:
- **AI UGC** (Higgsfield/Arcads): avatar-driven, natural speech converter obrigatório pra não soar robotizado, duração 15-22s ideal
- **Stolen-footage**: cortes rápidos, UGC-style hooks de pattern interrupt, nenhuma voz off
- **Motion graphics**: claim-heavy, text-forward, ideal pra listicle hooks e mechanism explainers
- **Founder-led**: talking head caseiro, tom pessoal, storytelling, duração 25-45s
- **Demonstração**: close-up do produto em uso, b-roll intercalado, mínimo de talking, foco em proof visual
- **Creator humano**: UGC tradicional com spokesperson, maior range de duração e complexidade de script

### ETAPA 2 — Calcular Quantidade de Conceitos

**Fórmula:** `Budget diário / Target CPA = máximo de ad sets ativos`

Exemplos:
- Budget $50/dia com CPA target $25 → máximo 2 ad sets ativos → **2 conceitos**
- Budget $100/dia com CPA target $20 → máximo 5 ad sets → **5 conceitos**
- Budget $300/dia com CPA target $30 → máximo 10 ad sets → mas o prático é **6-8 conceitos** (rest goes to champions + page tests)
- Budget $1000+/dia → **8-12 conceitos novos por batch** (com champions rodando em paralelo)

Ajuste pra estágio do membro:
- **Fase de teste (sem champions)**: todos os slots pra conceitos novos
- **Tem champions**: 1-2 ad sets de champions + resto em conceitos novos

Mostre ao membro (sem pedir confirmação):

"Com seu budget de $[X]/dia e target CPA ~$[Y] (da oferta), vou gerar **[N] conceitos novos** pra testar. Cada conceito = 1 ad set com 3-2-2 (3 criativos + 2 primary texts + 2 headlines)."

### ETAPA 3 — Gerar Ângulos (3 Verticais da Vault)

Referência: `[REF: mcp__aura__search_knowledge("3 research verticals competitive consumer internal ad angles")]`.

Gere ângulos em 3 verticais:

**Vertical 1 — Competitiva:**
O que os concorrentes NÃO estão dizendo que você pode dizer (gaps do competitor analysis).
- "Ninguém está endereçando a dor [X] — nosso ad atacará direto"
- "Todo mundo usa angle de resultado — nós vamos de angle de causa raiz"
- "Concorrentes fazem autoridade de doctor — nós vamos peer-to-peer UGC"

Gere 3-5 ângulos desta vertical.

**Vertical 2 — Consumidor:**
Dos dados do market research (VOC, trigger events, objeções):
- "Hook baseado na frase exata [VOC phrase X] que aparece 8x no review mining"
- "Trigger event [Y] (ex: antes de casamento) como cenário do ad"
- "Ângulo de objeção quebrada [Z] (ex: 'já tentei X, mas aqui está por que este é diferente')"

Gere 3-5 ângulos.

**Vertical 3 — Interna (Oferta/Mecanismo):**
O que é único do seu produto/oferta:
- "Mecanismo único [nome] — apresentado como revelação/descoberta"
- "Garantia agressiva como angle ('90-day guarantee — you pay nothing if it doesn't work')"
- "Stack de valor como angle ('Tudo isso por $X')"
- "Combinação rara de ingredientes como ângulo técnico"

Gere 3-5 ângulos.

### ETAPA 4 — Selecionar os Top N + Apresentar Pro Membro (Pergunta 2)

Das 9-15 opções de ângulo, selecione os **N conceitos mais fortes** (N vem da Etapa 2). Critérios de seleção:
- Cobrir posições diferentes do funil (TOF + MOF + BOF — não todos no mesmo awareness)
- Cobrir ângulos das 3 verticais (não concentrar em uma só)
- Priorizar ângulos DE GAPS (ninguém faz) sobre ângulos de posição já ocupada

Apresente ao membro em formato compacto:

"Esses são os [N] conceitos que recomendo testar:

1. [Conceito] — [ângulo em 1 frase] (vertical: [competitiva/consumidor/interna], posição: [TOF/MOF/BOF])
2. ...

Quer ajustar algum antes de eu gerar os briefings completos?"

- Se o membro disser "tá bom" / "segue" / "manda" → vai pra Etapa 5
- Se pedir ajuste → aplique e confirme antes de gerar briefings

### ETAPA 4.5 — Regras estruturais globais (aplicadas a TODO briefing)

Antes de gerar briefings individuais, estas regras se aplicam a qualquer conceito, independente de vertical/formato:

**A. Aspect ratio — sempre 9:16**

Todo criativo (vídeo ou imagem) é produzido em **9:16 (1080×1920)**. Meta/Instagram/TikTok rodam Reels/Stories nessa razão, e versões 1:1/4:5 derivam do 9:16 via crop central ou re-framing manual (documentar esse crop no briefing quando aplicável). Nunca produza 4:5 ou 1:1 como versão primária — vai perder placements de Reels/Stories/TikTok.

**B. Plataforma primária — TikTok vs Meta difference**

Pergunte ao membro (se não estiver no profile): "Esse batch vai rodar primariamente em Meta (FB/IG) ou TikTok?" Use a resposta pra calibrar o briefing:

| Aspecto | Meta (FB/IG Reels) | TikTok |
|---------|---------------------|--------|
| Hook timing | 0-3s com pattern interrupt forte | 0-2s — TikTok penaliza mais rápido |
| Tom | Mais polido aceitável | Mais cru/UGC-native convert melhor |
| Duration ideal | 15-22s TOF, até 45s MOF | 12-20s cap — scroll é mais rápido |
| Text overlay | Importante pra hook retention | Essencial — muitos assistem sem som |
| CTA | Explícito + badge visual | Soft CTA ("link na bio" não funciona em ad — usar CTA button nativo) |
| Música/trending sound | Menos crítico | Trending sound aumenta reach orgânico — aproveitar |
| Format | Flexible Ad Format permite variações dentro de 1 ad | 1 criativo = 1 ad set |

Se o batch roda em **ambas** as plataformas, o briefing tem 2 versões do script: Meta-optimized e TikTok-optimized. Não assuma portabilidade 1:1.

**C. Word count validation por duration (spoken script)**

Cadência de fala natural pra ad é **2.3 a 2.8 palavras por segundo** (mais lento que fala casual pra dar tempo de processar). Use esse range pra validar se o script cabe na duração alvo.

| Duration alvo | Word count ideal (fala) | Word count teto absoluto |
|---------------|-------------------------|--------------------------|
| 10s | 23-28 palavras | 30 |
| 15s | 35-42 palavras | 45 |
| 22s | 50-62 palavras | 68 |
| 30s | 70-85 palavras | 92 |
| 45s | 105-125 palavras | 135 |

**Regra:** ao gerar script de voiceover/fala, ANTES de salvar, conte as palavras e confirme que cabe no range. Se estourar, corte — não deixe o editor precisar acelerar a fala pra caber (soa robótico e destrói retention).

Text overlay não conta nesse cálculo — overlay roda em paralelo à fala.

**D. Spoken vs Overlay — disciplina de jargão técnico**

Siglas, números complexos, nomes científicos, compostos químicos, unidades de medida e claims regulatórios são **sempre text overlay**, **nunca** na fala. Regras:

- Siglas (qualquer acrônimo de 2+ letras maiúsculas) → overlay
- Números com decimais, percentuais, ou unidades técnicas → overlay (`"48.5% improvement"`, `"2,500 IU"`)
- Nomes de ingrediente/composto químico complexos → overlay
- Estudos citados com N amostral, duração, peer-review status → overlay ou gráfico
- Regulatory references (FDA status, clinical trial phase) → overlay ou disclaimer

**Motivo:** a fala precisa fluir emocionalmente. Siglas/números faladas quebram ritmo, desligam avatares 35+, soam clinicamente desinteressante. No overlay, o mesmo dado ganha peso de evidência visual sem matar cadência.

**Regra de ouro:** se a frase contém ≥2 elementos técnicos, quebrar — a parte emocional vai na fala, os dados duros vão no overlay lado-a-lado.

**E. Big 4 Emotions — obrigatório marcar dominante no hook**

Todo criativo (e todo hook na Hooks Bank) DEVE declarar explicitamente qual das Big 4 emotions domina:

- **Curiosity** — pattern interrupt, mistério, pergunta incompleta, "o que poucos sabem"
- **Urgency** — tempo escasso, janela limitada, risco de perder
- **Fear** — dor amplificada, consequência negativa, "se você não fizer X"
- **Delight** — desejo/transformação, imagem de futuro melhor, prazer antecipado

NÃO permitir hook sem emoção dominante atribuída. Se o hook não encaixa em nenhuma das 4, ele é fraco — reescrever.

**F. VOC traceability — cada claim/hook linka a VOC phrase**

Cada hook, cada primary text, cada headline precisa ser rastreável a uma fonte no `02-market-research.json` (VOC phrases, trigger events, objeções, dores hierarquizadas). Documentar no output JSON:

```json
{
  "asset_id": "c-01-h-03",
  "text": "texto do hook",
  "voc_source": {
    "ref_id": "voc-phrase-0042",
    "original_phrase": "frase exata do review/post/comment",
    "source_type": "amazon_review|reddit_thread|tiktok_comment|g2_review|...",
    "confidence": "direct_quote|paraphrase|inferred_pattern"
  },
  "emotion_dominant": "curiosity|urgency|fear|delight"
}
```

Claim sem VOC rastreável **OU** sem evidência no `04-research-foundation.json` da Skill 04 = marcar `"voc_source": null, "requires_manual_review": true` e listar no output final pra o membro validar. Proibido inventar frase de avatar sem lastro.

**G. Hook-swap — OPCIONAL, não sempre**

O padrão "1 body × N hook variants" (manter corpo do vídeo e só trocar hook) funciona BEM quando:
- Conceito ganhou e quer testar variações de abertura sem refazer produção
- Body é genérico (product demo, lifestyle footage, motion graphics reutilizável)
- Budget não comporta refilmagem/re-render

Hook-swap NÃO funciona quando:
- Conceito depende de storytelling coeso (founder-led, UGC narrativo)
- Ângulo do hook é tão específico que o body precisa acompanhar (ex: hook de causa-raiz exige body educacional)
- Plataforma detecta "same-body creative" como duplicata (TikTok especificamente)

**Regra:** na Etapa 5, declare explicitamente `hook_swap_viable: true|false` por conceito. Se `false`, Etapa 7 (Hooks Bank) gera hooks pra FUTUROS conceitos novos (não pra swap no atual).

**H. Compliance pré-geração (gate leve antes da Etapa 7.5)**

Além do compliance pass final da Etapa 7.5, aplicar **soft check** durante geração:

- Zero travessão (—) em headlines (regra 8a do CLAUDE.md)
- Zero palavras ad-flag (Botox/Filler/Injection/Cure/Treat/Anti-aging literal) em qualquer peça de copy pra consumidor (regra 8b)
- Substituições automáticas do CLAUDE.md já aplicadas na primeira geração (não deixar pro compliance checker consertar depois)

Esse soft check evita 80% do retrabalho pós-compliance.

### ETAPA 5 — Gerar Briefings Completos (Um Por Conceito)

Para CADA conceito aprovado, gere o briefing completo aplicando os frameworks.

**Formato do briefing:**

---

# BRIEFING DE CONCEITO #[N]

**Conceito:** [nome/descrição curta do conceito]
**Ângulo:** [razão de compra que estamos comunicando]
**Vertical:** [competitiva / consumidor / interna]
**Awareness Level:** [Unaware / Problem Aware / Solution Aware / Product Aware / Most Aware]
**Posição no Funil:** [TOF / MOF / BOF]
**Formato Principal:** [UGC vídeo / demo vídeo / static / carrossel / motion graphics]
**Big Idea:** [a ideia unificadora em 1 frase]

---

## 3 CRIATIVOS (Variações do Mesmo Conceito)

### Criativo #1

**Tipo:** [vídeo UGC / vídeo demonstração / imagem estática / carrossel / motion graphics]

**SE VÍDEO (script segundo-a-segundo):**

Duração alvo: [15s / 22s / 30s — baseada em posição de funil; TOF mais curto, BOF pode ser mais longo]

Estrutura: Hook → Bridge → Hold → CTA (framework)

- **[00:00-00:03] HOOK** (aplica Big 4 Emotions: curiosity, urgency, fear, delight — escolher 1 dominante)
  - **Texto/fala EXATA**: "[texto literal — 1-2 frases]"
  - **Visual**: [descrição do que aparece na tela]
  - **Text overlay** (se houver): "[texto]"
  - **Tipo de hook**: [problem / result / curiosity / controversy / social proof / authority]
  - **Thumbstop score esperado**: (estimativa 1-10 baseada em força do hook)

- **[00:03-00:08] BRIDGE** (transição do hook pro corpo)
  - **Texto/fala**: "[texto]"
  - **Visual**: [descrição]
  - **Função**: [estabelecer credibilidade / apresentar problema / mostrar o pattern interrupt]

- **[00:08-00:18] HOLD** (desenvolvimento — mecanismo, proof, benefit)
  - **Texto/fala**: "[texto]"
  - **Visual**: [descrição]
  - **Aplicação do slippery slide**: cada frase deve compelir a próxima (Sugarman)
  - **Proof element presente**: [testimonial / número específico / demo / authority]

- **[00:18-00:22] CTA**
  - **Texto/fala**: "[texto — call to value, não call to action: 'Get my [outcome]' > 'Shop now']"
  - **Visual**: [CTA text overlay + produto em tela + badge de garantia]

**Música/SFX:** [tipo de música ou "sem música" — background que não distrai]
**Precisa de voiceover ElevenLabs?** [sim/não — UGC é geralmente não; demo/motion graphics é sim]
**Se sim, script de voiceover separado:**
```
[script completo e humanizado da locução — pode usar o Natural Speech Converter framework: contrações, pausas naturais, frases curtas]
```

**SE IMAGEM:**

- **Descrição visual principal**: [o que aparece — produto + contexto + modelo se houver]
- **Texto overlay principal** (hook): "[texto grande]"
- **Textos secundários**: "[subheadline ou benefits]"
- **CTA visual**: "[texto do botão/badge visual]"
- **Estilo**: [clean product shot / lifestyle / ugly ad / meme-style — "ugly ads convert" principle]
- **Elementos de proof**: [rating stars / review count / featured-in badges / guarantee shield]

### Criativo #2 — [Variação: formato diferente]

[Mesmo formato, mas com variação meaningful — ex: se #1 é UGC, #2 é demonstração; se #1 é problem-focused, #2 é result-focused]

### Criativo #3 — [Variação: angle ou visual diferente]

[Mesmo conceito, outra execução]

---

## 2 PRIMARY TEXTS (Meaningfully Different)

**IMPORTANTE**: Não são variações cosméticas. Cada primary text usa ESTRUTURA, ÂNGULO, e HOOK diferentes.

### Primary Text 1 — [Angle A]

[Copy completa — 100-300 palavras]

Estrutura:
- Hook (primeira linha acima do "See more")
- Corpo (dor/solução/mecanismo/proof/oferta)
- CTA linha final

### Primary Text 2 — [Angle B — diferente de A]

[Copy completa — estrutura diferente]

---

## 2 HEADLINES (Abaixo do Vídeo/Imagem)

Duas headlines que representam hipóteses diferentes. Cada uma é um frame de valor real.

- **Headline 1**: "[texto — max 40 chars ideal]" — frame: [benefício / urgência / offer / pergunta]
- **Headline 2**: "[texto]" — frame: [frame diferente]

---

## URL DE DESTINO

**Destino**: [PDP / Landing Page / Advertorial]

**Justificativa de congruência**:
- Message match: [como o ad conecta com o headline da LP]
- Visual match: [tom visual bate entre ad e LP?]
- Promise match: [a promessa do ad é mantida/expandida na LP, não trocada]

Se o conceito é TOF (cold traffic, awareness low), a LP precisa de mais educação → recomendar advertorial ou LP dedicada. Se é BOF/retargeting (warm), PDP direto funciona.

---

## RACIONAL ESTRATÉGICO

- **Por que esse conceito**: [1-2 frases justificando a aposta com base em market research/competitor analysis]
- **O que esperamos aprender**: [a pergunta que esse teste responde — ex: "o angle de causa raiz (hormônios) converte melhor que angle direto de resultado?"]
- **Success criteria**: [ex: CPA dentro do target em 3-7 dias; thumbstop > 5; CTR > 1.5%]

---

### ETAPA 6 — Recomendação de LP Congruente

Pra cada conceito, documente explicitamente qual LP da fase de copy ele deve direcionar:

| Conceito | Awareness | LP recomendada | Por quê |
|---|---|---|---|
| 1 | Problem Aware | Advertorial | Hook de dor → educação do mecanismo → produto |
| 2 | Solution Aware | Landing Page dedicada | Compara + mecanismo |
| 3 | Product Aware | PDP | Direto pra oferta |

Se o membro só tem uma LP, recomende adaptações (sessões-chave a adicionar na PDP existente pra servir TOF).

### ETAPA 7 — Hooks Bank (10 Alternativas)

Pra uso em iterações futuras, gere **10 hooks alternativos** categorizados. **Só aplique swap se o conceito tiver `hook_swap_viable: true` na Etapa 4.5.G** — senão, esses hooks servem como semente pra conceitos NOVOS, não pra trocar no conceito atual.

- **Problema** (3 hooks): frases de abertura que lideram com a dor
- **Resultado** (3 hooks): frases que lideram com o outcome desejado
- **Curiosidade** (2 hooks): que despertam mistério ou pattern interrupt
- **Prova social** (2 hooks): que lideram com testimonial ou número

Cada hook deve declarar:
- Big 4 emotion dominante (curiosity/urgency/fear/delight)
- VOC source (ref ao `02-market-research.json`, conforme Etapa 4.5.F)
- Word count (≤ 10 palavras ideal pro primeiro beat do vídeo)
- Aspect ratio: 9:16 (sempre)

Cada hook = 1-2 frases, formato de vídeo hook ou image headline.

Esses hooks ficam na biblioteca pra iteração futura.

### ETAPA 7.4 — Carregar DNA aprendido (PRE-STEP silent)

Antes de finalizar os briefings, checar se existe DNA de criativos anteriores deste produto:

1. Verificar se `/workspace/[produto]/creative-dna/dna-profile.json` existe
2. Se existir E `total_creatives >= 10`:
   - Extrair top 5 features com maior delta winners vs losers
   - Injetar como constraint soft no prompt de refinamento: "Baseado em DNA de N criativos anteriores, priorizar [features]. Reservar 20% de variação pra novelty."
3. Se não existir ou total < 10: proceder normalmente sem bias

Silent. Membro não vê esse step.

### ETAPA 7.5 — Compliance Pre-flight (OBRIGATÓRIO antes de salvar)

Antes de finalizar os briefings e hooks bank, rodar compliance check em TODA peça de copy que vai pro consumidor final.

**Invocação:**
1. Ler `.claude/lib/compliance-preflight/checker.md` (prompt completo) e `.claude/lib/compliance-preflight/red_flags.json` (base de regras)
2. Para CADA item abaixo, rodar o checker:
   - Hook (primeiros 3s do script de cada criativo)
   - Voiceover script completo (se houver)
   - Primary text de cada ad (2 versões por conceito)
   - Headlines (2 por conceito)
   - Text overlays (todos os beats)
   - Hooks Bank (10 alternativos)
3. Parse da resposta JSON:
   - `severity == critical`: PARAR, reportar ao membro, aplicar `rewrite_suggestion` ou pedir revisão manual
   - `severity == high`: aplicar `rewrite_suggestion` automaticamente, logar em `/workspace/[produto]/07-compliance-log.json`
   - `severity == medium`: manter original, logar warning
   - `severity == low`: salvar silenciosamente
4. Sanity pass final: zero termos ad-flag (Botox, filler, injection, cure, treat) em qualquer peça pública. Travessão (—) zero em headlines, ≤2 em copy longa.

Output log em `/workspace/[produto]/07-compliance-log.json`:
```json
{
  "checked_at": "ISO timestamp",
  "total_pieces": 45,
  "flags_critical": 0,
  "flags_high": 2,
  "flags_medium": 3,
  "pieces_rewritten": 2,
  "triggers_by_eixo": {"Meta Policy": 3, "FTC": 2, "AI Style": 1},
  "details": [...]
}
```

### ETAPA 7.6 — DNA Registry Extraction (silent)

Após compliance pass, pra cada criativo gerado:

1. Ler `.claude/lib/creative-dna/feature_schema.json` e `.claude/lib/creative-dna/extractor.md`
2. Rodar o extractor prompt com:
   - Briefing completo do criativo
   - Awareness level dominante do market research
   - Compliance risk score do Pre-flight
3. Parse JSON response (features estruturadas conforme schema)
4. Salvar em `/workspace/[produto]/creative-dna/features-[creative-id].json`
5. Invocar:
   ```
   python3 .claude/lib/creative-dna/registry.py init /workspace/[produto]  # se ainda não inicializado
   python3 .claude/lib/creative-dna/registry.py add /workspace/[produto] [creative-id] features-[creative-id].json --product [slug]
   ```

Silent pro membro. Se extração falhar (Claude retorna malformed JSON), logar erro em `/workspace/[produto]/creative-dna/extraction-errors.log` mas não bloquear skill.

### ETAPA 8 — Resumo de Produção

Crie um resumo operacional pro membro executar:

| Item | Quantidade | Onde editar/gerar |
|---|---|---|
| Vídeos a filmar | [X] | [UGC com pessoa real / telefone próprio / contratar creator] |
| Vídeos a gerar com AI | [Y] | [Higgsfield / Arcads / etc + script fornecido] |
| Voiceovers a gerar | [Z] | ElevenLabs com scripts fornecidos (voz recomendada: [voz]) |
| Imagens a criar | [W] | [Photoshop / Canva / AI / stock + descrição fornecida] |
| Primary texts prontos | [N × 2] | Copy pra colar no Ads Manager |
| Headlines prontas | [N × 2] | Copy pra colar |

**Tempo estimado de produção:** [baseado em tipo de material disponível — UGC humano toma 3-5 dias; AI UGC toma 1-2 dias; stock + edição toma 1 dia]

### Limitação Meta Flexible Ads

Meta NÃO fornece breakdown por creative individual em Flexible Ad Format. Para isolar winners:
- Adicionar UTM `utm_content=[concept-id]` único por conceito no link
- Pós-compra, cruzar com Shopify analytics por UTM
- Se precisar de breakdown DENTRO do Ads Manager: rodar 3 ad sets separados com 1 criativo cada (não flexible), custo: exige 3× volume de spend pra learning

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `/workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer.md` → `04-offer.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

**Garantir diretório:** `mkdir -p /workspace/[produto]/07-creatives/` antes de salvar.

Outputs em `/workspace/[produto]/07-creatives/` (nomenclatura normalizada):

- `07-creative-strategy.md` (estratégia macro — quantos conceitos, ângulos escolhidos, racional agregado)
- `07-concept-01.md`, `07-concept-02.md`, `07-concept-03.md` (briefs individuais — Etapa 5 completa, um arquivo por conceito)
- `07-hooks-bank.md` (Etapa 7 — 10 hooks alternativos)
- `07-production-summary.md` (Etapa 8 — resumo operacional)
- `07-creatives.json` (manifest do batch — ver schema abaixo)

### JSON companion — `07-creatives.json`

```json
{
  "batch_id": "uuid",
  "product_slug": "...",
  "creator_archetype_default": "ai_ugc|stolen_footage|motion_graphics|founder_led|demo|creator_human",
  "platform_primary": "meta|tiktok|both",
  "aspect_ratio_primary": "9:16",
  "concepts": [
    {
      "id": "c-01",
      "name": "...",
      "angle": "problem|result|curiosity|social|authority|comparison|controversy|identification",
      "vertical": "competitive|consumer|internal",
      "awareness_level": "unaware|problem_aware|solution_aware|product_aware|most_aware",
      "funnel_position": "TOF|MOF|BOF",
      "hook_swap_viable": true,
      "format": "video_ugc|video_demo|static_image|carousel|motion_graphic",
      "duration_target_seconds": 22,
      "word_count_spoken": 55,
      "word_count_within_limit": true,
      "hooks": [
        {
          "text": "texto do hook",
          "emotion_dominant": "curiosity",
          "voc_source": { "ref_id": "voc-phrase-0042", "original_phrase": "...", "confidence": "direct_quote" }
        }
      ],
      "primary_texts": [
        { "text": "...", "angle": "A|B", "voc_source": {...}, "compliance_clean": true }
      ],
      "headlines": [
        { "text": "...", "frame": "benefit|urgency|offer|question", "voc_source": {...}, "compliance_clean": true }
      ]
    }
  ],
  "total_assets": 3,
  "format": "3-2-2",
  "next_batch_ideas_applied": ["ref-01", "ref-02"],
  "compliance_summary": {
    "ad_flag_words_found": 0,
    "em_dash_in_headlines": 0,
    "unresolved_claims_without_voc": 0,
    "unresolved_claims_without_research_foundation": 0
  }
}
```

### Atualizar manifest

Após salvar, atualizar `/workspace/[produto]/manifest.json`:
- Adicionar `07-creative-engine` em `skills_completed`
- Registrar `last_batch_id`, `batch_count`, e `next_batch_ideas_applied` (refs lidas de `NEXT_BATCH_IDEAS.md`, se houver)

## Mensagem Final

"Briefings de criativos prontos. Próximos passos:

- Filme os vídeos seguindo os scripts (ou gere com AI UGC se aplicável)
- Gere voiceovers no ElevenLabs com os scripts marcados
- Agora edite os vídeos usando sua ferramenta de edição preferida (CapCut, Submagic, Captions, ou similar). Os briefings acima têm tudo que você precisa: scripts, hooks, text overlays, e estrutura do ad. Quando os criativos estiverem prontos, diga 'ad strategy' pra montar a campanha no Meta."

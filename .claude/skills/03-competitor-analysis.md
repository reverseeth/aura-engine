---
name: competitor-analysis
description: Engine de análise profunda de concorrentes que mapeia PDPs, ads em Meta Ad Library, claims, alternative solutions, e gap analysis. Use quando o membro disser "competitor analysis", "análise de concorrentes", "analisar concorrentes", ou quando o market research estiver completo e o membro quiser entender o cenário competitivo antes de montar a oferta. Este é o input decisivo pra posicionamento: onde você vai BRIGAR e onde você vai CONTORNAR.
---

# Competitor Analysis Engine

## Quando Usar
Quando o membro tem produto definido e market research feito, e precisa mapear o cenário competitivo com profundidade operacional antes de criar oferta e copy. A análise aqui alimenta: mecanismo único (o que NÃO usar), posicionamento (onde ninguém está), claims (o que evitar e o que explorar), e estrutura de funil (o que o mercado converteu).

## Antes de Começar

1. Leia `/workspace/profile.md`
2. Leia `/workspace/[produto]/01-product-research.md` (se existir — tem concorrentes já identificados)
3. Leia `/workspace/[produto]/02-market-research.md` (overview competitivo básico + gaps já identificados)
4. Consulte a base Aura extensivamente sobre competitor research (extração de claims, organização de swipe files), reconnaissance engine (técnicas de research via social), cloaker breaking (quando concorrentes escondem páginas), alternative solution research (mapeando TUDO que o avatar já tentou), market sophistication (claims saturados), análise de ad angles, classificação de criativos por posição no funil (4Pi signatures TOF/MOF/BOF), swipe file method, e os 15 fatores da estrutura de funil. Aprofunde em cada sub-conceito — esta skill opera em detalhe EXECUTIVO, não conceitual.

## Fluxo da Skill

### ETAPA 0 — Pre-flight

1. Leia `/workspace/profile.md`. Se ausente → aborte: `"Rode \`setup\` primeiro."`
2. Leia `/workspace/[produto]/manifest.json` (identifique `[produto]` via manifest com `setup_complete === true`). Se ausente → aborte: `"Rode \`setup\` primeiro."`
3. Valide a existência de TODOS os arquivos obrigatórios:
   - `/workspace/[produto]/01-product-research.md`
   - `/workspace/[produto]/02-market-research.md`
   - `/workspace/[produto]/02-market-research.json`
4. Valide que `skills_completed` do manifest contém `"01-product-research"` E `"02-market-research"`.
5. Falhou qualquer item → aborte com mensagem específica: `"Rode \`<skill faltante>\` primeiro."`

### ETAPA 1 — Identificar Concorrentes

Se o product research já identificou concorrentes, use essa lista como base (5-10 marcas). Se não, pergunte:

"Você já sabe quem são seus concorrentes? Se sim, me manda os links das lojas deles. Se não sabe, diga 'não sei' — o sistema encontra sozinho."

**SE o membro mandar links:** use como base e complemente se for menos de 5.

**SE o membro disser que não sabe:** pesquise automaticamente (web search):
- `"[produto]" brand site:.com`
- `"[produto]" shop`
- Meta Ad Library busca: categoria + palavras-chave
- TikTok Shop Best Sellers na categoria
- Amazon Best Sellers na categoria
- Similarweb pra identificar lojas com tráfego no nicho

Identifique **5-10 concorrentes** ATIVOS (têm ads rodando agora + loja funcional). Se encontrar menos de 5, amplie a busca pra produtos ADJACENTES que resolvem o mesmo problema (ex: se o produto é colágeno em pó, inclua serums anti-aging, tratamentos capilares com collagen boost, e clínicas de estética — são alternativas que o avatar considera).

**Validação de URLs (obrigatória)**: para cada URL de concorrente identificada, faça um HTTP HEAD request com timeout de **5 segundos**. Classifique:

- **Acessível (2xx / 3xx)** → inclua na análise principal
- **Inacessível (4xx, 5xx, timeout, DNS error)** → **NÃO** inclua na análise principal. Liste numa seção dedicada **"Concorrentes descartados por inacessibilidade"** com: URL, status/erro, e hora do check.

Se a inacessibilidade for por Cloudflare/bot-protection (status 403/503 + header `cf-*`), tente o fallback da Etapa 2 antes de descartar (Wayback → Google Cache → archive.today).

### ETAPA 1B — Ads Screenshots dos Concorrentes

Verifique no `/workspace/profile.md` se o membro tem SpyBox/Adsparo.

**SE TEM:**
"Cola screenshots dos ads mais escalados dos concorrentes — se tiver acesso ao SpyBox ou Adsparo. Se não tiver esses screenshots em mãos agora, tudo bem: sigo com o Meta Ad Library público."

**SE NÃO TEM:** pule a pergunta, use Meta Ad Library público direto na Etapa 3.

### ETAPA 2 — Análise de PDPs dos Concorrentes

Pra cada concorrente, acesse a página de produto (web fetch). Se tiver cloaker/Cloudflare bloqueando, execute os fallbacks **em sequência** (pare na primeira que retornar snapshot válido com > 500 bytes de HTML):

**Tentativa 1 — Wayback Machine**:
- Consulte `https://archive.org/wayback/available?url=<url>` e valide que `archived_snapshots.closest` existe e `timestamp` é dos últimos 365 dias.
- Se houver, faça fetch do snapshot.

**Tentativa 2 — Google Cache**:
- `https://webcache.googleusercontent.com/search?q=cache:<url>`
- Valide que o body não é a página de erro do Google (contém conteúdo da PDP).

**Tentativa 3 — archive.today**:
- Tente `https://archive.ph/newest/<url>` e valide redirect para snapshot real.

**Se NENHUM fallback funcionar**: pule esse concorrente específico (**não aborte a skill inteira**). Documente em "Concorrentes descartados por inacessibilidade" com a sequência de tentativas e motivo do descarte. Continue para os demais concorrentes.

Outros fallbacks opcionais quando possível: view-source direto, scraping via Playwright com user-agent de browser real.

**Pra cada PDP, documente:**

**Estrutura da página (aplicando frameworks):**
- **Tipo de hero section**: autoridade (expert/doctor), UGC/testimonial, product-hero, problem-agitate, lifestyle, demo/before-after (aplica os 5 tipos de hero)
- **Headline principal exata** (copie literalmente)
- **Sub-headline exata**
- **Como apresenta o produto**: foto, vídeo (quanto tempo?), GIF, demonstração
- **Bullet points de benefício** (copie as primeiras 5)
- **Mecanismo único?** Qual nome? Como apresenta? (ingredient, process, tech, combo)
- **Stack visual de valor?** Quantos itens? Com ancoragem de preço?
- **Preço**: base + bundles oferecidos (2-pack, 3-pack, subscription) com % savings
- **Guarantee**: tipo (money-back, satisfaction, results-based), duração (30/60/90 dias), copy exata
- **Social proof**: tipo (reviews count + média, UGC, mídia, certificações, endorsements)
- **FAQ**: quais perguntas aborda? Quantas?
- **CTAs**: quantos, onde, que copy usa nos botões
- **Shipping**: grátis? a partir de quanto? tempo estimado?
- **Aplicação dos 15 Fatores de Funil**: quais fatores a página cobre bem, quais ignora

**Copy analysis (frameworks):**
- **Tipo de lead** (Story, Secret, Proclamation, Problem-Solution, Offer, Direct — identificar aplicando os 5 tipos de lead por awareness de Schwartz)
- **Nível de awareness que a página assume** do visitante (dita onde no funil essa LP está)
- **Gatilhos de persuasão usados** (escassez, autoridade, prova social, reciprocidade, compromisso — identifique quais da lista dos 6 de Cialdini)
- **Grande promessa** (qual é? quão específica?)
- **Quais objeções a página tenta quebrar** (com que técnica)
- **Tom de voz** (sofisticado, casual, técnico, emocional, urgente, educativo)
- **Congruência ad→página**: se o concorrente tem ads ativos, a LP espelha o ad? (Message match, visual match, promise match)

### ETAPA 3 — Análise de Ads no Meta Ad Library (Agrupamento Por Aparições)

Pra cada concorrente, pesquise no Meta Ad Library (web fetch / scraping via Playwright quando possível).

**Regras críticas:**

1. **NÃO use tempo de veiculação como métrica de escala** — muitos criativos rodam há meses sem spend significativo
2. **Agrupe criativos idênticos ou quase idênticos** (mesmo vídeo com variação de overlay ou 1-2 palavras trocadas) e conte o número de APARIÇÕES
3. **Mais aparições = mais ad sets usando esse criativo = mais escalado**. Essa é a métrica.

**Métricas quantitativas:**
- Total de ads ativos no momento
- Número de criativos únicos (após agrupamento)
- **Top 10 criativos por aparições** (proxy de escala)

**Análise qualitativa dos top 10 criativos:**
Pra cada um dos top 10:

- **Tipo**: imagem estática, vídeo UGC (spokesperson falando), vídeo demonstração, antes/depois, carrossel, vídeo motion-graphic
- **Transcrição** (se vídeo): hook dos primeiros 3 segundos (texto E fala literal) + 2-3 frases do corpo do script + CTA de fechamento
- **Visual descrição do hook**: o que aparece na tela nos primeiros 3 segundos
- **Ângulo** (classificar aplicando frameworks de ad angles):
  - Problema (dor/frustração)
  - Resultado (desejo/transformação)
  - Curiosidade (mistério/revelação)
  - Autoridade (expert/estudo/credencial)
  - Comparação (vs X, melhor que Y)
  - Social proof (testimonial, UGC, número de clientes)
  - Controvérsia (contrarian, "o que não te contam")
  - Identificação ("pra mulheres como você")
- **Copy do ad (primary text)**: copia literal
- **CTA**: qual e como está formulado
- **Landing page destino**: PDP? landing page dedicada? advertorial? listicle?

### ETAPA 3B — Classificação dos Criativos por Posição no Funil

Aplicando as **4Pi signatures** (padrões de métrica que indicam posição no funil), classifique cada top criativo como:

- **TOF (Top of Funnel)**: hook de interrupção, tom emocional, problema+agitação, awareness-building. Geralmente frequency < 1.1, CPM moderado, CPC alto.
- **MOF (Middle of Funnel)**: educação do mecanismo, social proof, comparação. Frequency 1.15-1.3, CPM mais alto, CTR mais baixo mas conversão melhor.
- **BOF (Bottom of Funnel)**: retargeting/warm audiences, foco na oferta (preço, garantia, urgência). Frequency > 1.3, CPM alto, CTR baixo mas ROAS alto.

Se todos os top criativos estão numa posição só, o concorrente tem **funil desbalanceado** — oportunidade pra você cobrir as outras posições.

**CAVEAT OBRIGATÓRIO no output**: sem acesso a métricas reais de CPM/frequency/CTR dos concorrentes (públicos via Meta Ad Library **não** incluem essas métricas), a classificação TOF/MOF/BOF é **ESPECULATIVA** — baseada apenas em sinais qualitativos (formato do hook, tom, tipo de CTA). Imprima no output desta etapa:

> ⚠ Classificação 4Pi aqui é especulativa (sem métricas reais de performance dos concorrentes). Re-valide TOF/MOF/BOF quando houver ads LIVE nossos com dados de frequency/CPM/CTR reais — a classificação pode mudar significativamente.

### ETAPA 4 — Claims Compilation Completa

Compile TODOS os claims que os concorrentes fazem, classificados por tipo:

**Claims diretos** (promessa de resultado):
- "Reduz rugas em 30 dias"
- "Resultados visíveis em 1 semana"
- "Perde 5kg em 30 dias"

**Claims de mecanismo** (como funciona):
- "Tecnologia de micro-corrente"
- "Infusão de ácido hialurônico"
- "Fórmula com peptídeos patenteada"

**Claims de autoridade** (credencial):
- "Recomendado por dermatologistas"
- "Aprovado pela FDA"
- "Desenvolvido por cientistas de Harvard"

**Claims de prova social** (evidência):
- "50.000+ clientes satisfeitas"
- "4.8 estrelas em 12.000 reviews"
- "Featured in Forbes, Vogue, NYT"

**Classifique cada claim:**

| Classificação | Significado | Ação |
|---|---|---|
| **SATURADO** | Todos ou quase todos usam | EVITAR — o público não acredita mais |
| **COMUM** | Maioria usa | USAR com twist próprio (especificidade de Hopkins) |
| **RARO** | Poucos usam | OPORTUNIDADE — diferenciação moderada |
| **AUSENTE** | Ninguém usa | OPORTUNIDADE FORTE — diferenciação máxima |

Apresente em tabela:

| Claim | Categoria | Quantos usam | Classificação | Ação |
|---|---|---|---|---|

**Claims Saturation matrix (output obrigatório)**: além da tabela acima, gere uma matriz enxuta focada em saturação — usada pelas skills 04 e 05 para escolher/evitar claims:

```
## Claims Saturation
| Claim | # Concorrentes usando | Saturação |
|-------|----------------------|-----------|
| "Clinically proven"   | 9/10 | ALTA — evitar |
| "30-day results"      | 4/10 | MÉDIA — usar com twist |
| "Doctor-formulated"   | 2/10 | BAIXA — oportunidade |
```

Regra de conversão: ≥70% dos concorrentes → ALTA / evitar; 30-69% → MÉDIA / usar com twist; < 30% → BAIXA / oportunidade; 0% → AUSENTE / oportunidade forte (destaque).

### ETAPA 5 — Alternative Solution Research

Esta é a etapa mais negligenciada E mais valiosa. Não basta mapear concorrentes diretos — mapeie TUDO que o avatar já tentou pra resolver o problema.

Pesquise (web search + review mining):

**Soluções concorrentes diretas** (já cobertas nas etapas 1-3)

**Soluções adjacentes da mesma categoria**:
- Outros formatos do mesmo problema (se seu produto é serum, mapeie cremes, tratamentos profissionais, procedimentos estéticos, rotinas DIY)

**Remédios caseiros / DIY**:
- O que as pessoas fazem em casa pra tentar resolver? (dicas de TikTok, receitas de avó, hacks)

**Tratamentos profissionais**:
- Médicos, dermatologistas, clínicas especializadas — qual o range de preço, tempo, invasividade?

**Outras categorias que roubam share**:
- O que mais consome o orçamento que o avatar poderia gastar no seu produto? (maquiagem disfarçando o problema, roupas disfarçando, terapia mental pra aceitar, etc)

**Produtos da mesma marca mas não concorrentes**:
- O que os grandes players oferecem que captura parte da demanda?

Esta análise é crítica pra montar a **oferta**: seu produto não compete só com outros DTCs, compete com TUDO que o avatar já gasta dinheiro tentando resolver. A narrativa de copy depois precisa posicionar seu produto contra TODAS essas alternativas, não só contra outros ecom brands.

### ETAPA 6 — Gap Analysis Completo

A parte mais valiosa estrategicamente. Identifique:

**Gaps de público (Avatar):**
- Segmento que NENHUM concorrente aborda (ex: todos falam com mulheres 25-35, ninguém fala com 45+; todos focam em iniciantes, ninguém com avançadas)
- Situação/trigger event que ninguém explora (pré-casamento, pós-parto, pós-divórcio, aposentadoria)
- Identidade que ninguém captura (profissional de carreira, mãe-que-se-perdeu, atleta recreativa)

**Gaps de messaging:**
- **Dor real do market research que nenhuma PDP aborda**
- Objeção que ninguém quebra (ex: "é caro demais" — ninguém justifica)
- Benefício que ninguém destaca
- Medo ou desejo secundário ignorado

**Gaps de formato:**
- Todos usam UGC mas ninguém usa demonstração close-up? Gap.
- Todos usam vídeo, ninguém usa carrossel educativo? Gap.
- Todos usam hook de problema, ninguém usa hook de resultado?
- Todos têm LP dedicada, ninguém usa advertorial?

**Gaps de oferta:**
- Ninguém oferece garantia forte (ou oferece mas não destaca)?
- Ninguém faz bundle com produto complementar?
- Ninguém tem subscription/refill?
- Ninguém tem bump de checkout?

**Gaps de mecanismo:**
- Todos usam o mesmo mecanismo genérico? Qual?
- Existe espaço pra criar mecanismo proprietário baseado em ingrediente/processo único do seu produto?
- Existe combinação de ingredientes que ninguém nomeou?

### ETAPA 7 — Síntese Estratégica

Compile tudo num relatório acionável:

**1. Mapa Competitivo (Tabela Resumo)**

| Concorrente | Preço base | Mecanismo | Claim principal | Posicionamento | Forças | Fraquezas |
|---|---|---|---|---|---|---|

**2. Padrões do Mercado**
- **Baseline**: o que TODOS fazem (você precisa fazer no mínimo isso pra não parecer incompleta)
- **Tendência**: o que a MAIORIA faz (considere fazer com twist)
- **Saturado**: claims e angles que DEVEM SER EVITADOS
- **Winning patterns**: criativos/ângulos/formatos que estão escalando AGORA (top 10 da Etapa 3)

**3. Oportunidades de Diferenciação (Ranqueadas por Potencial)**

Cada oportunidade com:
- Tipo (audience, messaging, format, offer, mechanism)
- Descrição
- Por que é oportunidade (o gap específico)
- Como explorar (ação concreta)
- Potencial (alto/médio/baixo baseado em demand do gap + facilidade de execução)

Liste mínimo 5 oportunidades, ranqueadas.

**4. Recomendação de Posicionamento**

Baseado em toda a análise, a recomendação estratégica:
- **Como este produto deve se posicionar** pra diferenciar-se (em 2-3 frases)
- **Qual mecanismo único perseguir** (sugestão alinhada com gaps)
- **Qual avatar focar** (segmento underserved)
- **Qual ângulo principal de comunicação** (hook dominante)
- **Qual tipo de página** (advertorial / LP dedicada / PDP robusta) baseado em awareness + concorrência

**5. Swipe File**

- **Top 3 elementos dos concorrentes que vale ADAPTAR** (não copiar — adaptar o princípio). Para CADA item gere um bullet estruturado com **COMO adaptar** concretamente:

  ```
  Item #1: [descrição curta do elemento — ex: "Hook de autoridade do concorrente X"]
  Por que funciona: [princípio + evidência de escala da Etapa 3]
  COMO adaptar: [passo-a-passo aplicado ao NOSSO produto/mecanismo — 2-3 frases com exemplo concreto, incluindo o hook/copy adaptado e o contexto de uso]
  Onde usar: [ad TOF / ad MOF / advertorial seção X / PDP hero / etc.]
  ```

- **Top 3 elementos que NÃO vale seguir**: saturados ou fracos. Para cada: `Elemento → Por que evitar → Alternativa sugerida` (ex: "todo mundo usa 'clinically proven' — saturado; alternativa: claim de mecanismo específico com nome proprietário").

### Data Source Audit (antes de salvar)

Seção obrigatória no output (md + json):

```
## Data Source Audit
- Concorrentes analisados: N
- Concorrentes descartados por inacessibilidade: [lista com URL + motivo + fallbacks tentados]
- Fontes usadas: Meta Ad Library (N ads analisados), Wayback Machine (N snapshots), Google Cache (N hits), archive.today (N hits), scraping direto (N páginas)
- Métricas reais disponíveis: [sim/não — note que Meta Ad Library público NÃO inclui CPM/freq/CTR]
- Timestamp da coleta: YYYY-MM-DDTHH:MM:SSZ
```

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de qualquer write**, garanta: `mkdir -p /workspace/[produto]/`.

**Toda skill que salva `.md` em `/workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer.md` → `04-offer.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

Salvar TRÊS artefatos:

1. **`/workspace/[produto]/03-competitor-analysis.md`**
2. **`/workspace/[produto]/03-competitor-analysis.html`**
3. **`/workspace/[produto]/03-competitor-analysis.json`** — JSON companion estruturado:

```json
{
  "competitors_analyzed": [
    { "name": "", "url": "", "accessible": true, "price_base": 0, "mechanism": "", "main_claim": "", "positioning": "", "strengths": [], "weaknesses": [] }
  ],
  "competitors_discarded": [
    { "url": "", "reason": "http_403|timeout|no_snapshot", "fallbacks_tried": ["wayback","gcache","archive_today"] }
  ],
  "claims_saturation": [
    { "claim": "", "count": 0, "total": 0, "saturation": "HIGH|MEDIUM|LOW|ABSENT" }
  ],
  "funnel_classification": { "TOF": 0, "MOF": 0, "BOF": 0, "classification_confidence": "speculative" },
  "gaps": { "audience": [], "messaging": [], "format": [], "offer": [], "mechanism": [] },
  "swipe_adapt": [ { "item": "", "why": "", "how_to_adapt": "", "where_to_use": "" } ],
  "swipe_avoid": [ { "item": "", "why_avoid": "", "alternative": "" } ],
  "positioning_recommendation": { "angle": "", "mechanism": "", "avatar_segment": "", "page_type": "" },
  "data_source_audit": { "collected_at": "", "meta_ad_library_ads_count": 0, "wayback_hits": 0, "gcache_hits": 0, "archive_today_hits": 0 }
}
```

Estrutura do `.md`:
1. Lista de concorrentes analisados + links (+ seção separada "Concorrentes descartados por inacessibilidade")
2. PDP analysis por concorrente (Etapa 2)
3. Meta Ad Library findings + top creatives transcritos (Etapa 3)
4. Classificação de posição de funil + CAVEAT especulativo (Etapa 3B)
5. Claims compilation table + Claims Saturation matrix (Etapa 4)
6. Alternative solutions map (Etapa 5)
7. Gap analysis (Etapa 6)
8. Síntese estratégica — posicionamento + swipe file com "COMO adaptar" (Etapa 7)
9. Data Source Audit

**Atualize o `manifest.json`**:

- `skills_completed` ← adicione `"03-competitor-analysis"` (sem duplicar)
- `updated_at` ← timestamp atual ISO-8601 UTC

## Mensagem Final

"Análise competitiva completa. Agora temos:
- Market research profundo (Skill 02)
- Mapa competitivo completo com gaps acionáveis (esta skill)

Próximo passo: diga **'offer'** pra construir a oferta com mecanismo único, stack de valor, garantia, e unit economics. A oferta vai puxar direto das recomendações de posicionamento desta análise + do perfil psicográfico do market research."

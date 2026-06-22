---
name: competitor-analysis
description: Engine de análise profunda de concorrentes que mapeia PDPs, ads em Meta Ad Library, claims, alternative solutions, e gap analysis. Use quando o membro disser "competitor analysis", "análise de concorrentes", "analisar concorrentes", ou quando o market research estiver completo e o membro quiser entender o cenário competitivo antes de montar a oferta. Este é o input decisivo pra posicionamento: onde você vai BRIGAR e onde você vai CONTORNAR.
---

# Competitor Analysis Engine

## Quando Usar
Quando o membro tem produto definido e market research feito, e precisa mapear o cenário competitivo com profundidade operacional antes de criar oferta e copy. A análise aqui alimenta: mecanismo único (o que NÃO usar), posicionamento (onde ninguém está), claims (o que evitar e o que explorar), e estrutura de funil (o que o mercado converteu).

## Antes de Começar

1. Leia `workspace/profile.md`. Leia o campo `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do `report_language`. Ressalva específica desta skill: copy literal de concorrentes (headlines, hooks, claims, transcrições de ads) permanece no idioma original do ad — é evidência, não tradução.
2. Leia `workspace/[produto]/01-product-research/relatorio.md` (se existir — tem concorrentes já identificados)
3. Leia `workspace/[produto]/02-market-research/relatorio.md` (overview competitivo básico + gaps já identificados)
4. **Puxe os SISTEMAS NOMEADOS da base** — NUNCA use query genérica tipo "competitor analysis". Pra cada ETAPA, rode `search_knowledge` (com `deep=true`) usando a `best_query` exata de cada framework relevante listado nas próprias ETAPAs abaixo. O índice completo do domínio desta skill (domínio `competitor-positioning`, 31 frameworks) está em **`.claude/lib/kb-index/`** (`frameworks.json` + `README.md` com o mapa skill→domínio). Esta skill opera em detalhe EXECUTIVO, não conceitual — puxe o sistema completo de cada framework, não o resumo de superfície.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (domínio `competitor-positioning`; o README mapeia skill→domínio). Os blocos `**Nome do framework** (rode \`best_query\`)` embutidos nas ETAPAs abaixo são os de MAIOR IMPACTO — não a lista inteira. Quando uma ETAPA precisar de mais profundidade, consulte o índice.

## Fluxo da Skill

### ETAPA 0 — Pre-flight

1. Leia `workspace/profile.md`. Se TOTALMENTE ausente → sem profile não há o que inferir; ofereça rodar o setup inline: `"Não achei seu profile. Rode \`setup\` agora (eu conduzo aqui mesmo) e a gente segue."`
2. Leia `workspace/[produto]/manifest.json` (identifique `[produto]` via manifest com `setup_complete === true`). Se TOTALMENTE ausente → ofereça rodar o setup inline (mesma mensagem do item 1).
3. Valide a existência de TODOS os arquivos obrigatórios:
   - `workspace/[produto]/01-product-research/relatorio.md`
   - `workspace/[produto]/02-market-research/relatorio.md`
   - `workspace/[produto]/02-market-research/dados.json`
4. Valide que `skills_completed` do manifest contém `"01-product-research"` E `"02-market-research"`.
5. Se faltar qualquer arquivo obrigatório dos itens 3-4 (mas profile + manifest existem), NÃO aborte seco. Ofereça ≥2 caminhos: **(A)** Rodar a skill faltante agora (`product research` ou `market research`), OU **(B)** prosseguir com default genérico marcando `manifest.skipped_preflight += ["<arquivo>"]` e avisando no output final que recomenda re-executar com o arquivo real. Default conservador = (A).

### ETAPA 0.5 — TrendTrack MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis. Se SIM, use TrendTrack como fonte primária pra ETAPAs 1-3 e fallback de Cloudflare/cloaker fica desnecessário:

- **`mcp__trendtrack__search_shops`** com niche/keyword → substitui Etapa 1 manual de identificação de concorrentes (browse 1M+ Shopify stores indexados, com sinais de receita/crescimento).
- **`mcp__trendtrack__find_similar_shops`** após identificar 1 concorrente forte → encontra adjacentes ranqueados por similaridade.
- **`mcp__trendtrack__brief_competitor`** com domínio → substitui ETAPA 2 (PDP analysis) + ETAPA 3 (ads no Meta Ad Library) numa chamada só, retornando deep-dive com ads, email patterns, opportunities. Fim das corridas com cloaker/archive.today.
- **`mcp__trendtrack__scan_ad`** com URL/ID de ad → substitui análise manual de hook/ângulo na ETAPA 3, e dá assessment de scaling (volume + reach).

Pra cada concorrente, prefira 1 chamada `brief_competitor` em vez de 4-5 chamadas web fetch. Custa créditos — não desperdiçar em concorrente irrelevante. Limite: 5-10 concorrentes principais.

Se uma chamada falhar → silent fallback pra ETAPA tradicional, sem avisar membro.

Se TrendTrack NÃO estiver disponível, pule esta etapa e siga ETAPAs 1-3 normalmente.

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

Se a inacessibilidade for por Cloudflare/bot-protection (status 403/503 + header `cf-*`), tente o fallback da Etapa 2 antes de descartar (Wayback → archive.today).

### ETAPA 1B — Ads Screenshots dos Concorrentes

Verifique no `workspace/profile.md` se o membro tem SpyBox/Adsparo.

**SE TEM:**
"Cola screenshots dos ads mais escalados dos concorrentes — se tiver acesso ao SpyBox ou Adsparo. Se não tiver esses screenshots em mãos agora, tudo bem: sigo com o Meta Ad Library público."

**SE NÃO TEM:** pule a pergunta, use Meta Ad Library público direto na Etapa 3.

### ETAPA 2 — Análise de PDPs dos Concorrentes

**Frameworks a puxar da base ANTES de analisar (rode cada `best_query`):**
- **Competitor Research Process (Extracting Claims)** (rode `competitor research process extracting claims messaging hooks customer feedback differentiation`) — o método de extração estruturada que organiza tudo abaixo.
- **Schwartz Market Sophistication — 5 Stages** (rode `market sophistication five stages Schwartz enlarge claim new mechanism identity skepticism`) — pra ler em que stage de sofisticação o mercado está pela forma como os concorrentes tratam o claim/mecanismo.
- **Schwartz Mechanization Stages — Name / Describe / Feature** (rode `Schwartz mechanization stages name describe feature mechanism promise reason why headline`) — pra classificar COMO cada concorrente apresenta o mecanismo (só nomeia? descreve? detalha feature?).

Pra cada concorrente, acesse a página de produto (web fetch). Se tiver cloaker/Cloudflare bloqueando, execute os fallbacks **em sequência** (pare no primeiro que retornar conteúdo válido > 500 bytes):

**Tentativa 1 — Fetcher Playwright da Aura (navegador real — resolve Cloudflare/429/JS na maioria dos casos; rule `.claude/rules/resilient-fetch.md`):**
```bash
python3 .claude/lib/web-fetch/fetch.py "<url-da-pdp>" --mode text --json
```
Se vier `blocked: false`, use o conteúdo — é a página **AO VIVO** (melhor que snapshot). É a tentativa preferencial.

**Tentativa 2 — Wayback Machine**:
- Consulte `https://archive.org/wayback/available?url=<url>` e valide que `archived_snapshots.closest` existe e `timestamp` é dos últimos 365 dias.
- Se houver, faça fetch do snapshot.

**Tentativa 3 — archive.today**:
- Tente `https://archive.ph/newest/<url>` e valide redirect para snapshot real.

**Se NENHUM fallback funcionar** (hard-CAPTCHA tipo PerimeterX, ou todos caíram): pule esse concorrente específico (**não aborte a skill inteira**). Documente em "Concorrentes descartados por inacessibilidade" com a sequência de tentativas (`aura_fetch`, `wayback`, `archive_today`) e motivo do descarte. Continue para os demais concorrentes.

**Safeguard de integridade — threshold crítico de acessibilidade:**

Depois de tentar todos os concorrentes + todos os fallbacks, calcule:

```
access_rate = concorrentes_com_PDP_analisada / total_concorrentes_identificados
```

- `access_rate >= 0.5` → proceder normalmente
- `0.3 <= access_rate < 0.5` → proceder com WARNING no output: `"Cobertura parcial — {N}/{total} concorrentes inacessíveis. Análise competitiva pode ter gaps. Considere análise manual via screenshots."`
- `access_rate < 0.3` → **PARAR SKILL E PEDIR AÇÃO DO MEMBRO**. Não proceder com análise baseada em < 30% do universo competitivo, senão Skills 04/06 vão assumir "mercado limpo" (falsa premissa). Mensagem:

  > ⚠️  Só consegui acessar {N}/{total} ({access_rate:.0%}) das PDPs de concorrentes. O resto bloqueou por bot-protection (Cloudflare, Shopify App check, etc) e todos os fallbacks falharam.
  >
  > Sem análise competitiva real, Skills 04 (Offer) e 06 (Copy) vão voar no escuro. Opções:
  > 1. Me manda screenshots dos concorrentes inacessíveis por WhatsApp/paste
  > 2. Passa pra mim dados do SpyBox/Kalodata sobre claims e estrutura deles
  > 3. Adia competitor analysis até conseguir acesso (mudar IP, VPN, etc)
  >
  > O que prefere?

Outros fallbacks opcionais quando possível: view-source direto, scraping via Playwright com user-agent de browser real.

**Pra cada PDP, documente:**

**Estrutura da página (aplicando frameworks):**
- **Tipo de hero section**: autoridade (expert/doctor), UGC/testimonial, product-hero, problem-agitate, lifestyle, demo/before-after (aplica os 5 tipos de hero)
- **Headline principal exata** (copie literalmente)
- **Sub-headline exata**
- **Como apresenta o produto**: foto, vídeo (quanto tempo?), GIF, demonstração
- **Bullet points de benefício** (copie as primeiras 5)
- **Mecanismo único?** Qual nome? Como apresenta? (ingredient, process, tech, combo). Classifique a apresentação pelos **Schwartz Mechanization Stages** (Name / Describe / Feature): só dá nome ao mecanismo, descreve como funciona, ou detalha cada feature? O stage de mecanização revela em que ponto da sofisticação o concorrente acha que o mercado está.
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
- **Gatilhos de persuasão usados** (escassez, autoridade, prova social, reciprocidade, compromisso — identifique quais da lista dos 6 de Cialdini). Anote também se o concorrente usa **Vampire Claims / Vampire Video** (rode `vampire claims vampire video mosaic structure architectural support single USP`) — elementos chamativos que roubam atenção do claim central, sinal de página mal-arquitetada que você pode explorar.
- **Grande promessa** (qual é? quão específica?)
- **Quais objeções a página tenta quebrar** (com que técnica)
- **Tom de voz** (sofisticado, casual, técnico, emocional, urgente, educativo)
- **Congruência ad→página**: se o concorrente tem ads ativos, a LP espelha o ad? (Message match, visual match, promise match)

### ETAPA 3 — Análise de Ads no Meta Ad Library (Agrupamento Por Aparições)

**Frameworks a puxar da base ANTES de varrer ads (rode cada `best_query`):**
- **Reconnaissance Engine (Competitive Research via Social)** (rode `reconnaissance engine competitive research via social Instagram transcribe competitor videos algorithm`) — método de research via social/algoritmo pra achar e transcrever os criativos que o concorrente está rodando além do Meta Ad Library.
- **Winning Ad Extraction / Processing Learnings** (rode `winning ads extracting strategies process learnings AdSpy shares validated hook why it works`) — como extrair o "porquê funciona" de cada criativo escalado, não só descrever.

Pra cada concorrente, pesquise no Meta Ad Library. Se o `WebFetch` for barrado (comum — é SPA pesado em JS), use o fetcher da Aura, que renderiza a página: `python3 .claude/lib/web-fetch/fetch.py "<url-do-ad-library>" --mode text --wait 5000 --json`. Lembre: o Meta Ad Library público **não** traz métricas (CPM/freq/CTR) → a classificação de funil da 3B é especulativa.

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

### ETAPA 3C — Scaled Creative Deep Analysis (opcional, mas recomendado)

Se o membro tiver acesso a plataformas de inteligência de criativos (Adsparo, SpyBox, Kalodata, Pipiads, Foreplay, Minea, Atria) ou listas curadas de criativos que ESCALARAM (não apenas "ativos"), peça pra enviar:

1. **URLs públicas** de vídeo ad (Meta Ad Library direct links, TikTok urls, ou assets hospedados)
2. **Uploads de vídeo/imagem** diretamente pro workspace (salvar em `workspace/[produto]/03-competitor-analysis/creatives-inbox/`)
3. **CSV/planilha** com lista de criativos + métricas se disponível (spend, days live, impressions estimadas)

Critério de curadoria do membro: só criativos que ESCALARAM (proxy: 90+ dias ativos com variação semanal, OU métricas diretas de plataforma de inteligência mostrando alto spend/impressões). Ads recém-lançados NÃO servem pra essa análise — a ideia é extrair padrões do que o mercado já VALIDOU.

**Pipeline de análise profunda:**

**Pré-flight de transcrição** (antes do primeiro criativo):

Valide que Whisper está acessível — uma das três opções DEVE estar disponível:

```bash
# Opção 1: openai-whisper instalado localmente
python3 -c "import whisper; print('ok')" 2>/dev/null

# Opção 2: faster-whisper (recomendado pra batch > 10 criativos)
python3 -c "import faster_whisper; print('ok')" 2>/dev/null

# Opção 3: OpenAI API (Whisper endpoint)
test -n "$OPENAI_API_KEY" && echo "ok"
```

Se NENHUMA disponível, mostre ao membro:

```
Pra análise profunda de criativos, preciso de Whisper. Opções:

1. Local (sem custo recorrente):
   pip install openai-whisper      # baseline
   pip install faster-whisper      # 4-5x mais rápido

2. API (pay-per-use, ~$0.006/min):
   export OPENAI_API_KEY=sk-...

Escolhe uma e me avisa quando tiver setup.
```

PARE a Etapa 3C até membro confirmar. Se nenhum Whisper estiver disponível e o membro não conseguir configurar, grave `creative_deep_analysis.status: "whisper_unavailable"` no JSON companion e prossiga sem. Se o membro quiser pular essa etapa, grave `creative_deep_analysis.status: "skipped"` e prossiga sem.

**Para cada criativo recebido:**

**1. Transcrição de áudio (vídeos):**
- Usar Whisper `medium` OU `large-v3-turbo` (na CLI: `--model turbo`) — NUNCA `base` ou `small` (essas geram transcrição com erros demais pra análise confiável)
- Se o membro tem OpenAI API: `whisper-1` endpoint (baseline, equivalente a `large-v2`)
- CLI local: `whisper <arquivo> --model medium --language en` (ou `--model turbo` se disponível)
- Output obrigatório: transcript com timestamps por palavra (`word_timestamps=true`) pra mapear hook/bridge/hold/CTA
- Salvar em `workspace/[produto]/03-competitor-analysis/creatives-inbox/transcripts/[creative-id].json`

**2. Extração de padrões (por criativo):**
- Hook primeiros 3s: texto literal + Big 4 emotion dominante (curiosity/urgency/fear/delight)
- Bridge 3-8s: técnica de transição usada
- Hold 8-end: mecanismo apresentado, proof elements, slippery slope detectável
- CTA: call-to-value vs call-to-action, urgência explícita ou não
- Visual beats: corte a cada X segundos, pattern interrupts, b-roll vs talking head
- Text overlay strategy: siglas/claims técnicos em overlay vs falados, tempo de exibição
- Aspect ratio usado (9:16 quase sempre pra Reels/Stories/TikTok)

**3. Agregação de padrões (cross-creative):**

Depois de transcrever N criativos, identifique:

- **Hook archetypes recorrentes**: quais formas de abrir aparecem em ≥ 30% dos criativos escalados?
- **Claim overlap**: quais afirmações aparecem em múltiplos criativos (e devem ser consideradas "validadas pelo mercado")?
- **Duration distribution**: histograma de durações — qual faixa concentra os escalados? (típico: 15-22s pra TOF, 25-45s pra MOF)
- **Format mix**: % UGC humano / AI UGC / stock + motion / demonstração / antes-depois
- **Spoken vs overlay split**: claims técnicos ficam em overlay ou na fala? Padrão dominante?
- **CTA cadence**: CTA único no final OU CTA bumper no meio + final?
- **Music/SFX patterns**: música, sem música, só ambience
- **Opening visual**: talking head close, product shot, b-roll lifestyle, text card

Output obrigatório: `workspace/[produto]/03-competitor-analysis/creative-patterns.json`:

```json
{
  "analyzed_at": "ISO timestamp",
  "creatives_analyzed_count": 12,
  "transcription_model": "whisper-medium|whisper-large-v3-turbo|whisper-1",
  "hook_archetypes": [
    { "pattern": "descrição", "frequency_pct": 42, "examples_creative_ids": ["c-03","c-07","c-11"] }
  ],
  "recurring_claims": [
    { "claim": "texto", "count": 5, "market_validated": true }
  ],
  "duration_histogram": { "0-15s": 2, "15-22s": 5, "22-30s": 3, "30-45s": 2 },
  "format_distribution": { "ugc_human": 5, "ugc_ai": 3, "motion_graphic": 2, "demo": 2 },
  "spoken_vs_overlay_policy": "siglas/numbers em overlay; claims emocionais falados",
  "cta_pattern": "CTA bumper em 50% + final CTA em 100%",
  "opening_visual_pattern": "talking head close-up (67%), product shot (25%), other (8%)"
}
```

Esse arquivo vira input crítico pra Skill 08 (Creative Engine) — criativos novos nascem ancorados em padrões validados + 20-30% de novelty intencional pra testar rupturas.

Quando esta etapa rodar até o fim, grave no JSON companion `creative_deep_analysis.status: "completed"`, `creative_deep_analysis.creatives_analyzed_count` (N transcritos) e `creative_deep_analysis.patterns_file` (path do `03-competitor-analysis/creative-patterns.json`). Assim as skills 08/09 leem o status direto, sem adivinhar a existência do arquivo.

**Se membro NÃO enviar criativos**: pular essa etapa e prosseguir, gravando `creative_deep_analysis.status: "skipped"`. A skill 08 roda em modo "cold" (sem patterns de referência) — funciona, mas com menos sinal de mercado.

### ETAPA 4 — Claims Compilation Completa

**Frameworks a puxar da base ANTES de classificar (rode cada `best_query`):**
- **The Preemptive Claim (Schlitz / Live Steam)** (rode `preemptive claim Hopkins Schlitz live steam own common claim first to say`) — um claim COMUM (não único) que ninguém ainda CRAVOU como dono pode virar oportunidade forte se você for o primeiro a explicá-lo. Aplique ao classificar claims COMUM/RARO: existe claim que todos têm mas ninguém "possui"?
- **Schwartz Market Sophistication — 5 Stages** (rode `market sophistication five stages Schwartz enlarge claim new mechanism identity skepticism`) — a saturação de claims é o sintoma direto do stage de sofisticação. Stage 3-5 exige mecanismo novo/identidade, não claim ampliado.

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

**Claims Saturation matrix (output obrigatório)**: além da tabela acima, gere uma matriz enxuta focada em saturação — usada pelas skills 04 e 06 para escolher/evitar claims:

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

**Frameworks a puxar da base ANTES de mapear (rode cada `best_query`):**
- **Category Economics / 'Pork and Beans' Insight** (rode `Hopkins pork and beans category economics what behavior replacing true competition status quo`) — a verdadeira concorrência não é outro DTC, é o comportamento/status quo que seu produto substitui. Use isso pra enquadrar TODA alternativa (DIY, profissional, status quo "não fazer nada").
- **Consumer Insights Database (3-source lift)** (rode `consumer insights database review mining Reddit Amazon ad comments three source lift customer language`) — método de review mining cross-fonte (Reddit + Amazon + ad comments) pra descobrir o que o avatar já tentou e abandonou, na linguagem dele.

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

A parte mais valiosa estrategicamente.

**Frameworks a puxar da base ANTES de mapear gaps (rode cada `best_query`):**
- **Cherchez le Creneau — 8 Types of Holes in the Mind** (rode `cherchez le creneau eight types holes in the mind size price age gender distribution`) — o sistema completo dos 8 tipos de "buraco" na mente (tamanho, preço, idade, gênero, distribuição, etc.). Cada tipo de gap abaixo (público, messaging, oferta, mecanismo) deve ser cruzado contra esses 8 buracos pra não perder um vetor de diferenciação.
- **New Mechanism / New Information / New Identity (The Big 3)** (rode `new mechanism new information new identity Big 3 sophisticated market break resistance`) — quando o mercado está saturado (claims ALTA na Etapa 4), o gap de MECANISMO abaixo se resolve por uma das 3 rotas: mecanismo novo, informação nova, ou identidade nova.

Identifique:

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

**Gaps de mecanismo** (cruze com **The Big 3** acima — mecanismo/informação/identidade nova):
- Todos usam o mesmo mecanismo genérico? Qual?
- Existe espaço pra criar mecanismo proprietário baseado em ingrediente/processo único do seu produto?
- Existe combinação de ingredientes que ninguém nomeou? (gap de **mecanismo novo** — rota mais forte em mercado sofisticado)

### ETAPA 7 — Síntese Estratégica

**Frameworks a puxar da base ANTES de sintetizar (rode cada `best_query`) — estes sustentam a Recomendação de Posicionamento (#4) e o Swipe File (#5):**
- **Reeves' Unique Selling Proposition (USP) — 3-Part Test** (rode `USP unique selling proposition Reeves three requirements proposition uniqueness selling power`) — teste de 3 partes pra validar se a diferenciação proposta é proposição + única + com poder de venda.
- **Three Roads to a USP (Three Roads to Rome)** (rode `three roads to a USP find real difference improve product preemptive claim`) — as 3 rotas pra construir USP quando o produto parece paridade (achar diferença real / melhorar produto / preemptive claim).
- **Ries & Trout Positioning — The Mental/Product Ladder** (rode `positioning Ries Trout mental ladder product ladder battle for the mind perception`) — pra situar onde o produto entra na escada mental do mercado vs concorrentes.
- **The Against Position / Uncola & Repositioning the Competition** (rode `against position uncola repositioning the competition Avis Tylenol aspirin inconvenient truth`) — quando o líder domina, posicione-se CONTRA ele (Avis/Uncola). Rota direta pra recomendação de ângulo principal.
- **Kennedy USP Construction Formula** (rode `Kennedy USP construction formula narrow positioning meaningful specifics guarantee Domino's`) — fórmula prática (positioning estreito + especificidade + garantia) pra cravar a recomendação em 1 frase acionável.
- **Swipe File Method & Handcopy Practice** (rode `swipe file method handcopy practice Kennedy collect organize winning ads patterning technique`) — método pra organizar o swipe file do #5 abaixo (o que ADAPTAR, princípio extraído, não copiar literal).
- **Storytelling as Hardest-to-Replicate Angle (Founder Story / Villain)** (rode `storytelling hardest to replicate founder story villain narrative defensible angle status quo`) — quando todo gap tático é copiável, a narrativa (founder story / vilão) é o ângulo mais defensável. Considere na recomendação de ângulo.

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
- Fontes usadas: Meta Ad Library (N ads analisados), Wayback Machine (N snapshots), archive.today (N hits), scraping direto (N páginas)
- Métricas reais disponíveis: [sim/não — note que Meta Ad Library público NÃO inclui CPM/freq/CTR]
- Timestamp da coleta: YYYY-MM-DDTHH:MM:SSZ
```

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de qualquer write**, garanta: `mkdir -p workspace/[produto]/03-competitor-analysis/`.

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer-builder/relatorio.md` → `04-offer-builder/relatorio.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

Salvar os seguintes artefatos:

1. **`workspace/[produto]/03-competitor-analysis/relatorio.md`**
2. **`workspace/[produto]/03-competitor-analysis/relatorio.html`**
3. **`workspace/[produto]/03-competitor-analysis/dados.json`** — JSON companion estruturado (ver abaixo)
4. **`workspace/[produto]/03-competitor-analysis/creative-patterns.json`** — SE membro forneceu criativos pra análise profunda (Etapa 3C); senão, pular. Schema definido na própria Etapa 3C.
5. **`workspace/[produto]/03-competitor-analysis/creatives-inbox/transcripts/[creative-id].json`** — transcripts Whisper individuais (um por criativo).

```json
{
  "competitors_analyzed": [
    { "name": "", "url": "", "accessible": true, "price_base": 0, "mechanism": "", "main_claim": "", "positioning": "", "strengths": [], "weaknesses": [] }
  ],
  "competitors_discarded": [
    { "url": "", "reason": "http_403|timeout|no_snapshot", "fallbacks_tried": ["wayback","archive_today"] }
  ],
  "claims_saturation": [
    { "claim": "", "count": 0, "total": 0, "saturation": "HIGH|MEDIUM|LOW|ABSENT" }
  ],
  "funnel_classification": { "TOF": 0, "MOF": 0, "BOF": 0, "classification_confidence": "speculative" },
  "gaps": { "audience": [], "messaging": [], "format": [], "offer": [], "mechanism": [] },
  "swipe_adapt": [ { "item": "", "why": "", "how_to_adapt": "", "where_to_use": "" } ],
  "swipe_avoid": [ { "item": "", "why_avoid": "", "alternative": "" } ],
  "positioning_recommendation": { "angle": "", "mechanism": "", "avatar_segment": "", "page_type": "" },
  "creative_deep_analysis": { "status": "completed|skipped|whisper_unavailable", "creatives_analyzed_count": 0, "patterns_file": "workspace/[produto]/03-competitor-analysis/creative-patterns.json" },
  "data_source_audit": { "collected_at": "", "meta_ad_library_ads_count": 0, "wayback_hits": 0, "archive_today_hits": 0 }
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
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug`; atualiza ABRIR-AQUI.html).

## Mensagem Final

"Análise competitiva completa. Agora temos:
- Market research profundo (Skill 02)
- Mapa competitivo completo com gaps acionáveis (esta skill)

Próximo passo: diga **'offer'** pra construir a oferta com mecanismo único, stack de valor, garantia, e unit economics. A oferta vai puxar direto das recomendações de posicionamento desta análise + do perfil psicográfico do market research."

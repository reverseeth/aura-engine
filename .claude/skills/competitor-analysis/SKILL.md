---
name: competitor-analysis
description: Engine de análise profunda de concorrentes, depois do market research e antes da oferta. Identifica 5 a 10 concorrentes ativos, analisa as PDPs pela cascade resiliente com um piso de cobertura, varre os ads no Meta Ad Library agrupando por aparições (a métrica de escala), classifica os criativos por posição no funil, transcreve e disseca os criativos escalados em creative-patterns.json, registra formatos, landings, radar e o catálogo de ads escalados com link, compila os claims com a matriz de saturação, mapeia as soluções alternativas que o avatar já tentou, faz o gap analysis pelos 8 buracos da mente e fecha com a síntese estratégica (posicionamento, swipe file com como adaptar e a validated library de mecanismos e ângulos validados com evidência de escala, que alimenta a recombinação da offer-builder). Use quando o membro disser "competitor analysis", "análise de concorrentes", "analisar concorrentes", ou quando o market research estiver completo.
---

# Competitor Analysis · Passo 4 · apelido antigo: 03 <!-- gen:title -->

## Quando usar

Quando o membro tem produto definido e market research feito, e precisa mapear o cenário competitivo com profundidade operacional antes de criar oferta e copy. A análise alimenta o mecanismo único, o posicionamento, os claims e a estrutura de funil: onde brigar e onde contornar.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/profile.md` e `workspace/[produto]/manifest.json` (`setup_complete === true`); ausentes, oferecer rodar o `setup` inline.
2. Obrigatórios: `product-research/product-research.md`, `market-research/market-research.md` e `market-research/dados.json`; `product-research` e `market-research` em `skills_completed`.
3. Faltou algum: nunca abortar seco; (A) rodar a skill faltante agora ou (B) seguir com default genérico marcando `manifest.skipped_preflight` e avisando no fim. Default conservador é (A).

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`); copy consumidor-final e VOC literal sempre em inglês US; copy literal de concorrente (headlines, hooks, claims, transcrições) fica no idioma original do ad, porque é evidência.
2. `product-research/product-research.md`, `banco-de-marcas.md` e `dados.json` (`validated_elements[]` é a semente da `validated_library` da ETAPA 7: aprofunde, não refaça); `market-research/market-research.md` (legado `relatorio.md`).
3. Base pelo índice (domínio `competitor-positioning`): `python3 .claude/lib/kb-index/kb_lookup.py --skill competitor-analysis --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas adicionais por etapa; as queries embutidas nos arquivos de `reference/` são piso obrigatório, rodam sempre e não contam no teto; nunca query genérica nem busca repetida.

## Fluxo da skill

### ETAPA 0 · Pré-flight

É a checklist acima; o texto integral está em `reference/contexto.md`.

### ETAPA 0.5 · MCPs de research (opcionais)

Leia `reference/mcps-de-research.md`. Com TrendTrack (`mcp__trendtrack__*`), ele vira a fonte primária das ETAPAs 1 a 3: lojas e similares na ETAPA 1, brief por domínio nas ETAPAs 2 e 3, scan de ad; 1 brief por concorrente, só nos 5 a 10 principais (gasta créditos). Com Foreplay (`mcp__foreplay__*`), fonte primária de criativos escalados nas ETAPAs 3 e 3C. Chamada que falhar cai em silêncio pro método tradicional.

### ETAPA 1 · Identificar concorrentes

Leia `reference/identificar-concorrentes.md`. Base: a lista da `product-research` (5 a 10 marcas); senão, links do membro ou busca automática. Alvo: 5 a 10 concorrentes ativos, ampliando pra produtos adjacentes se faltar. Validação de URL por HEAD com 5 segundos: 2xx e 3xx entram; 4xx, 5xx e timeout passam pela cascade inteira da ETAPA 2 antes de qualquer descarte; só erro de DNS descarta direto. Descartado vai pra `competitors_discarded[]` com motivo e fallbacks tentados; o relatório lista só os analisados.

### ETAPA 1B · Ads screenshots dos concorrentes

Mesmo arquivo. Membro com SpyBox ou Adsparo no profile: peça os screenshots dos ads mais escalados, sem bloquear; sem eles, Meta Ad Library público na ETAPA 3.

### ETAPA 2 · Análise de PDPs dos concorrentes

Leia `reference/analise-de-pdps.md` e puxe os três sistemas (extração de claims, sofisticação, mechanization stages). Cascade por PDP, parando no primeiro conteúdo válido: `WebFetch`; `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text --json` (preferencial); Wayback; archive.today; tudo falhou, pule o concorrente, nunca a skill. Safeguard: `access_rate` = PDPs analisadas ÷ concorrentes identificados; 0,5 ou mais segue; entre 0,3 e 0,5 segue com aviso de cobertura parcial; abaixo de 0,3 pare e peça ação do membro. Por PDP, documente a estrutura (os itens do arquivo, com o mecanismo classificado por Name, Describe ou Feature) e a copy (tipo de lead, awareness assumido, gatilhos, grande promessa, objeções, tom, congruência entre ad e página).

### ETAPA 3 · Ads no Meta Ad Library (agrupamento por aparições)

Leia `reference/ads-no-meta-ad-library.md` e puxe os dois sistemas (reconnaissance engine, winning ad extraction). Fetcher com `--wait 5000` quando o `WebFetch` barrar. Regras críticas: tempo de veiculação não é métrica de escala (só as duas exceções da 3C e da 3F); agrupe criativos idênticos ou quase e conte aparições; mais aparições é mais escalado. Métricas: ads ativos, criativos únicos, top 10 por aparições. Por criativo do top 10: tipo, transcrição do hook dos primeiros 3 segundos mais corpo e CTA, visual do hook, ângulo (as oito classes do arquivo), primary text literal, CTA e página de destino.

### ETAPA 3B · Posição no funil

Mesmo arquivo. Classifique cada top criativo em TOF, MOF ou BOF pelas assinaturas 4Pi. Tudo numa posição só é funil desbalanceado, uma oportunidade. A classificação é qualitativa: grave `funnel_classification.classification_confidence: "speculative"` e re-valide na `ad-analysis`; no relatório, sem bloco de aviso.

### ETAPA 3C · Scaled creative deep analysis (opcional, recomendada)

Leia `reference/criativos-escalados.md`. Fonte: Foreplay, ou os criativos que o membro curou de plataformas de spy, só os que escalaram por um dos 3 sinais (evergreen de 90 dias ou mais; o mesmo ângulo em 3 ou mais gerações em 4 a 8 semanas; métrica direta de spend). Transcrição pela cascade de 3 degraus (Groq API, Whisper local `medium` ou `turbo`, transcript do membro), sempre com timestamps por palavra; nunca inventar transcrição; sem nenhum degrau, pare a etapa até o membro escolher, ou grave `whisper_unavailable` ou `skipped`. Por criativo, os padrões de hook, bridge, hold, CTA e visual; transcript em `creatives-inbox/transcripts/`. Agregação em `creative-patterns.json` (hook archetypes, claims recorrentes cruzados com a saturação da ETAPA 4, duração, formato, overlay, CTA, abertura), o input da `creative-engine`. Grave `creative_deep_analysis` (`status`, `creatives_analyzed_count`, `patterns_file`). Molde slot a slot de 1 a 3 peças escaladas (descoberta no TrendTrack, cânone `.claude/lib/ad-molds/`): `reference/molde-de-criativo.md`.

### ETAPA 3D · Formato dos criativos escalados

Leia `reference/formato-landings-e-radar.md`. Pra cada criativo do top 10 e dos transcritos, o formato como objeto próprio: tipo estrutural, duração com o ponto em que o hook termina, padrão de iteração do concorrente (o que congela e o que troca) e evidência de escala; consolide em `ad_formats[]`, que a `creative-engine` lê pra montar o batch com formatos já validados.

### ETAPA 3E · Páginas de destino, formato de cada uma e radar

Mesmo arquivo. `traffic_landings[]` com a URL literal de destino dos ads escalados e as páginas de maior tráfego (tabela com links no `.md`); `landing_formats[]` com o formato de cada página de destino (os oito valores do arquivo), os ads que caem nela e o que decidiu a classificação, mais `dominant_landing_format` no `resumo` (terceiro sinal do `page_type` na `page-design`); `monitoring_radar[]` com o que vigiar depois do launch, onde, o sinal e a ação (a `ad-analysis` relê).

### ETAPA 3F · Ads escalados com link (doc dedicado)

Leia `reference/ads-escalados-com-link.md`. Com TrendTrack: por marca, busca pelo domínio e depois pelo nome; três ordenações (duplicatas, alcance, dias no ar) deduplicadas, com duplicatas como métrica primária; por ad, os campos do arquivo com o link da biblioteca montado com o id real (alcance só existe pra ads na União Europeia; zero não é gasto zero); reporte o que a busca revelou além dos ads. Sem TrendTrack, a versão manual com os links dos cartões do Ad Library. Saída: `ads-escalados.md` e `.html` (texto integral) mais `ads-escalados-dados.json`, e `top_creatives[].ad_library_url` no `dados.json`.

### ETAPA 4 · Claims compilation e matriz de saturação

Leia `reference/claims.md` e puxe os dois sistemas (preemptive claim, sofisticação). Compile todos os claims por tipo, classifique cada um em SATURADO, COMUM, RARO ou AUSENTE com a ação, e gere a matriz Claims Saturation (70% ou mais dos concorrentes é ALTA, evitar; de 30% a 69% MÉDIA, usar com twist; abaixo de 30% BAIXA, oportunidade; zero é AUSENTE, oportunidade forte), que a `offer-builder` e a `copy-engine` usam.

### ETAPA 5 · Alternative solution research

Leia `reference/solucoes-alternativas.md` e puxe os dois sistemas (category economics, consumer insights de três fontes). Mapeie tudo que o avatar já tentou (adjacentes, DIY, profissionais, categorias que roubam share, grandes players). A oferta compete com tudo isso, não só com outros DTCs.

### ETAPA 6 · Gap analysis completo

Leia `reference/gap-analysis.md` e puxe os dois sistemas (cherchez le creneau, the Big 3). Gaps de público, de messaging (a dor do market research que nenhuma PDP aborda), de formato, de oferta e de mecanismo (rota de mecanismo, informação ou identidade nova), cada um cruzado com os 8 buracos da mente.

### ETAPA 7 · Síntese estratégica

Leia `reference/sintese-estrategica.md` e puxe os nove sistemas antes de sintetizar. Sete blocos: mapa competitivo (tabela resumo); padrões do mercado (baseline, tendência, saturado, winning patterns); no mínimo 5 oportunidades de diferenciação ranqueadas; recomendação de posicionamento (mecanismo, avatar, ângulo principal, tipo de página); swipe file com o Top 3 a adaptar (com o como adaptar) e o Top 3 a evitar com alternativa; validated library (mecanismos e ângulos com a evidência de escala; sinal `high` pelo critério da 3C), que alimenta a Rota A da `offer-builder`; e o resumo e conclusão em texto corrido, que se sustenta sozinho. Fontes só em `dados.json.sources`, nunca no relatório.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/competitor-analysis/`; `competitor-analysis.md` nas onze seções do arquivo, com a conclusão em texto corrido no fim, texto integral, nunca truncado; `competitor-analysis.html` por `python3 tools/render_report.py workspace/[produto]/competitor-analysis/competitor-analysis.md`; `dados.json` no schema de `reference/dados-json.md`; `creative-patterns.json`, `ad-molds.json` e os transcripts se a 3C rodou; `ads-escalados.md`, `.html` e `ads-escalados-dados.json` se a 3F rodou. Manifest pelo script: `python3 tools/manifest.py <slug> complete competitor-analysis` (valida o `dados.json` contra o schema da fase) e `python3 .claude/lib/workspace-index/build_index.py <slug>`. O `dados.json` abre pelo `resumo`, o bloco que a fase seguinte lê de primeira.

## Mensagem final

Íntegra em `reference/mensagem-final.md`: primeira versão da análise pronta, com o mapa competitivo, os gaps acionáveis e a validated library; convite pra revisar a recomendação de posicionamento e as oportunidades ranqueadas antes de seguir; próximo passo 'offer'.

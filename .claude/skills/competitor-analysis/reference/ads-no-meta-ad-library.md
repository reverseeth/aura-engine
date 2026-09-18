# Competitor Analysis · Referência: Ads no Meta Ad Library, agrupamento por aparições e posição no funil (ETAPAs 3 e 3B)

> Os dois sistemas a puxar, o fetcher com espera, as regras críticas (tempo de veiculação não é escala, agrupar e contar aparições), as métricas, a análise qualitativa dos top 10 criativos e a classificação TOF, MOF e BOF pelas assinaturas 4Pi com a confiança gravada no `dados.json`. Abra na ETAPA 3.

### ETAPA 3 — Análise de Ads no Meta Ad Library (Agrupamento Por Aparições)

**Frameworks a puxar da base ANTES de varrer ads (rode cada `best_query`):**
- **Reconnaissance Engine (Competitive Research via Social)** (rode `reconnaissance engine competitive research via social Instagram transcribe competitor videos algorithm`) — método de research via social/algoritmo pra achar e transcrever os criativos que o concorrente está rodando além do Meta Ad Library.
- **Winning Ad Extraction / Processing Learnings** (rode `winning ads extracting strategies process learnings AdSpy shares validated hook why it works`) — como extrair o "porquê funciona" de cada criativo escalado, não só descrever.

Pra cada concorrente, pesquise no Meta Ad Library. Se o `WebFetch` for barrado (comum — é SPA pesado em JS), use o fetcher da Aura, que renderiza a página: `python3 .claude/lib/web-fetch/fetch.py "<url-do-ad-library>" --mode text --wait 5000 --json`. Lembre: o Meta Ad Library público **não** traz métricas (CPM/freq/CTR) → a classificação de funil da 3B é especulativa.

**Regras críticas:**

1. **NÃO use tempo de veiculação como métrica de escala** — muitos criativos rodam há meses sem spend significativo. Duas exceções, e só elas: na ETAPA 3C, "evergreen 90+ dias" entra como UM dos três sinais de criativo escalado (nunca sozinho como métrica); na ETAPA 3F, dias no ar só desempatam depois de duplicatas e alcance.
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

**Confiança da classificação (vai no `dados.json`, não no relatório):** sem acesso a métricas reais de CPM/frequency/CTR dos concorrentes (públicos via Meta Ad Library **não** incluem essas métricas), a classificação TOF/MOF/BOF é baseada em sinais qualitativos (formato do hook, tom, tipo de CTA). Grave `funnel_classification.classification_confidence: "speculative"` e re-valide TOF/MOF/BOF na skill `ad-analysis` quando houver ads nossos ao vivo com frequency/CPM/CTR reais. No relatório, a classificação aparece como está, sem bloco de aviso.

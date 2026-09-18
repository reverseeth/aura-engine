# Competitor Analysis · Referência: Scaled creative deep analysis (ETAPA 3C)

> As fontes de criativos escalados e os 3 sinais de escala, a cascade de transcrição em 3 degraus (Groq, Whisper local, transcript do membro) com a mensagem de setup, a extração de padrões por criativo, a agregação cross-creative, o schema do `creative-patterns.json` e os campos de status `creative_deep_analysis`. Abra na ETAPA 3C.

### ETAPA 3C — Scaled Creative Deep Analysis (opcional, mas recomendado)

Se o **Foreplay MCP** estiver conectado (tools `mcp__foreplay__*` — ver ETAPA 0.5), puxe os criativos escalados direto por ele, sem pedir uploads ao membro. Senão: se o membro tiver acesso a plataformas de inteligência de criativos (Adsparo, SpyBox, Kalodata, Pipiads, Foreplay, Minea, Atria) ou listas curadas de criativos que ESCALARAM (não apenas "ativos"), peça pra enviar:

1. **URLs públicas** de vídeo ad (Meta Ad Library direct links, TikTok urls, ou assets hospedados)
2. **Uploads de vídeo/imagem** diretamente pro workspace (salvar em `workspace/[produto]/competitor-analysis/creatives-inbox/`)
3. **CSV/planilha** com lista de criativos + métricas se disponível (spend, days live, impressions estimadas)

Critério de curadoria do membro — **proxy de escalado (critério 2026)**: só criativos que ESCALARAM, por qualquer um destes 3 sinais:
- **(a) Evergreen** — 90+ dias ativos (criativo que segue rodando meses só sobrevive pagando a conta);
- **(b) Ângulo iterado** — o mesmo ângulo repetido em **3+ gerações de criativos num período de 4-8 semanas** (a marca re-lança variações novas do mesmo ângulo — a iteração contínua, não o tempo sozinho, é o sinal de spend mais confiável em ciclo curto; ver Regra crítica 1 da ETAPA 3);
- **(c) Métricas diretas** — plataforma de inteligência mostrando alto spend/impressões.

Ads recém-lançados sem nenhum dos 3 sinais NÃO servem pra essa análise — a ideia é extrair padrões do que o mercado já VALIDOU.

**Pipeline de análise profunda:**

**Pré-flight de transcrição** (antes do primeiro criativo) — **cascade em 3 degraus, nesta ordem:**

**Degrau 1 — Groq API (`whisper-large-v3-turbo`)** — preferencial: rápido, barato (~$0.02-0.04 por hora de áudio) e sem instalar nada:

```bash
test -n "$GROQ_API_KEY" && echo "ok"
# transcrição com timestamps por palavra (pra mapear hook/bridge/hold/CTA):
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F model=whisper-large-v3-turbo \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -F file=@<arquivo-de-video-ou-audio>
```

**Degrau 2 — Whisper local** (se não há `GROQ_API_KEY`):

```bash
python3 -c "import faster_whisper; print('ok')" 2>/dev/null   # recomendado pra batch > 10 criativos
python3 -c "import whisper; print('ok')" 2>/dev/null          # openai-whisper baseline
```

Modelo `medium` OU `turbo` (large-v3-turbo) — NUNCA `base`/`small` (erros demais pra análise confiável). CLI: `whisper <arquivo> --model medium --language en --word_timestamps True`.

**Degrau 3 — Membro:** se nem Groq nem Whisper local estão disponíveis, peça o transcript ao membro (plataformas de ad spy exportam transcrição; ou ele cola o texto do ad). **NUNCA invente transcrição** — sem transcript real, o criativo sai da análise profunda.

Se nenhum degrau estiver disponível, mostre ao membro:

```
Pra análise profunda de criativos, preciso de transcrição. Opções (em ordem de facilidade):

1. Groq API (rápido, ~centavos por batch): export GROQ_API_KEY=gsk_...
2. Whisper local (sem custo recorrente):
   pip install faster-whisper      # 4-5x mais rápido
   pip install openai-whisper      # baseline
3. Me manda o transcript de cada criativo (export da plataforma de spy, ou colado).

Escolhe uma e me avisa quando tiver setup.
```

PARE a Etapa 3C até membro confirmar. Se nenhum degrau sair e o membro não conseguir configurar, grave `creative_deep_analysis.status: "whisper_unavailable"` no JSON companion e prossiga sem. Se o membro quiser pular essa etapa, grave `creative_deep_analysis.status: "skipped"` e prossiga sem.

**Para cada criativo recebido:**

**1. Transcrição de áudio (vídeos):**
- Use o degrau ativo da cascade (Groq `whisper-large-v3-turbo` → Whisper local `medium`/`turbo` → transcript do membro)
- Output obrigatório: transcript com timestamps por palavra (Groq: `timestamp_granularities[]=word`; local: `--word_timestamps True`) pra mapear hook/bridge/hold/CTA. Se o transcript veio do membro sem timestamps, mapeie hook/bridge/hold/CTA por posição aproximada no texto
- Salvar em `workspace/[produto]/competitor-analysis/creatives-inbox/transcripts/[creative-id].json`

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
- **Claim overlap**: quais afirmações aparecem em múltiplos criativos? Essas são **validadas pelo mercado** (é o que está convertendo em ad) — MAS cruze cada uma com a matriz Claims Saturation da ETAPA 4: se o claim também está SATURADO nas PDPs, ele serve como prova/base do argumento, não como headline (headline saturada morre no feed). Registre os dois sinais no JSON (`market_validated` + `also_saturated_pdp` + `usage`).
- **Duration distribution**: histograma de durações — qual faixa concentra os escalados? (típico: 15-22s pra TOF, 25-45s pra MOF)
- **Format mix**: % UGC humano / AI UGC / stock + motion / demonstração / antes-depois
- **Spoken vs overlay split**: claims técnicos ficam em overlay ou na fala? Padrão dominante?
- **CTA cadence**: CTA único no final OU CTA bumper no meio + final?
- **Music/SFX patterns**: música, sem música, só ambience
- **Opening visual**: talking head close, product shot, b-roll lifestyle, text card

Output obrigatório: `workspace/[produto]/competitor-analysis/creative-patterns.json`:

```json
{
  "analyzed_at": "ISO timestamp",
  "creatives_analyzed_count": 12,
  "transcription_model": "groq-whisper-large-v3-turbo|whisper-medium|whisper-large-v3-turbo|member_provided",
  "hook_archetypes": [
    { "pattern": "descrição", "frequency_pct": 42, "examples_creative_ids": ["c-03","c-07","c-11"] }
  ],
  "recurring_claims": [
    { "claim": "texto", "count": 5, "market_validated": true, "also_saturated_pdp": false, "usage": "anchor_headline|proof_only" }
  ],
  "duration_histogram": { "0-15s": 2, "15-22s": 5, "22-30s": 3, "30-45s": 2 },
  "format_distribution": { "ugc_human": 5, "ugc_ai": 3, "motion_graphic": 2, "demo": 2 },
  "spoken_vs_overlay_policy": "siglas/numbers em overlay; claims emocionais falados",
  "cta_pattern": "CTA bumper em 50% + final CTA em 100%",
  "opening_visual_pattern": "talking head close-up (67%), product shot (25%), other (8%)"
}
```

Esse arquivo vira input crítico pra Skill `creative-engine` (Creative Engine) — criativos novos nascem ancorados em padrões validados + 20-30% de novelty intencional pra testar rupturas. Leitura correta dos dois sinais: claim `market_validated` E não saturado na PDP (`usage: "anchor_headline"`) = ancorar criativos nele; `also_saturated_pdp: true` (`usage: "proof_only"`) = usar só como prova/base, nunca como headline.

Quando esta etapa rodar até o fim, grave no JSON companion `creative_deep_analysis.status: "completed"`, `creative_deep_analysis.creatives_analyzed_count` (N transcritos) e `creative_deep_analysis.patterns_file` (path do `competitor-analysis/creative-patterns.json`). Assim as skills `creative-engine`/`consistency-audit` leem o status direto, sem adivinhar a existência do arquivo.

**Se membro NÃO enviar criativos**: pular essa etapa e prosseguir, gravando `creative_deep_analysis.status: "skipped"`. A skill `creative-engine` roda em modo "cold" (sem patterns de referência) — funciona, mas com menos sinal de mercado.

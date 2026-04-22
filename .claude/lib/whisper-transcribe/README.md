# Whisper Transcribe — sub-pipeline

Sub-pipeline de transcrição de áudio/vídeo pra análise de criativos escalados dos concorrentes (Skill 03 Etapa 3C) e qualquer outro uso que precise de texto a partir de mídia.

## Modelos suportados

SOMENTE estes dois modelos. `base` e `small` têm taxa de erro inaceitável pra análise de copy de ad:

| Modelo | Uso | Custo (local) | Velocidade |
|--------|-----|---------------|------------|
| `medium` | Default recomendado | ~2GB RAM, ~3x real-time CPU | Médio |
| `turbo-large` (`large-v3-turbo`) | Quando precisa máxima precisão | ~6GB RAM, ~1.5x real-time GPU | Rápido em GPU |

Opções de execução:

1. **OpenAI API** (mais simples, custo por minuto): `whisper-1` endpoint
2. **Local CLI** (sem custo, precisa CPU/GPU decente): `openai-whisper` PyPI package
3. **faster-whisper** (local, otimizado): `faster-whisper` PyPI — 4-5x mais rápido

## Uso — CLI local

```bash
# Instalação
pip install openai-whisper

# Transcrição básica (medium)
whisper video.mp4 --model medium --language en --output_format json --word_timestamps True

# Turbo-large (se disponível e tem GPU)
whisper video.mp4 --model large-v3-turbo --language en --output_format json --word_timestamps True
```

Output JSON contém:
- `text` — transcript completo
- `segments[]` — cada segmento com start/end timestamps + texto
- `words[]` (se `--word_timestamps True`) — timestamp por palavra, essencial pra mapear hook/bridge/hold/CTA

## Uso — OpenAI API (Node/Python)

```python
from openai import OpenAI
client = OpenAI()

with open("video.mp4", "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )

print(transcript.text)
print(transcript.words)
```

Custo (OpenAI pricing aproximado): ~$0.006 por minuto de áudio. Criativo de 22s custa ~$0.0022.

## Uso — faster-whisper (recomendado pra batch >10 criativos)

```bash
pip install faster-whisper

# Via Python
from faster_whisper import WhisperModel
model = WhisperModel("medium", device="cpu", compute_type="int8")
segments, info = model.transcribe("video.mp4", word_timestamps=True)
```

Até 4-5x mais rápido que `openai-whisper` oficial em CPU.

## Output schema (padronizado pro Aura Engine)

Todo transcript salvo em `/workspace/[produto]/03-creatives-inbox/transcripts/[creative-id].json` segue:

```json
{
  "creative_id": "c-01",
  "source_url": "https://...",
  "source_file": "creative-01.mp4",
  "transcription_model": "medium|turbo-large|whisper-1",
  "duration_seconds": 22.4,
  "language": "en",
  "text": "transcript completo...",
  "segments": [
    { "start": 0.0, "end": 3.2, "text": "hook text" }
  ],
  "words": [
    { "word": "Why", "start": 0.0, "end": 0.24 }
  ],
  "extracted_at": "ISO timestamp"
}
```

## Regras operacionais

1. **NUNCA usar `base` ou `small`** — transcrição com erros inviabiliza análise downstream
2. **Sempre `word_timestamps: true`** — sem isso não dá pra mapear beats do vídeo (hook 0-3s, bridge 3-8s, etc)
3. **Language explícito quando possível** — evita auto-detect errado em criativos curtos
4. **Retry on failure** — Whisper às vezes falha em áudio com música alta. Se retornar < 10 palavras pra vídeo > 10s, re-rodar com modelo maior (turbo-large)
5. **Timeout**: 10× a duração do vídeo como limite (vídeo de 22s → timeout 220s)

## Integração com Skills

- **Skill 03 Etapa 3C**: pipeline principal — transcreve criativos enviados pelo membro, alimenta `03-creative-patterns.json`
- **Skill 09** (ad-analysis): pode re-transcrever winners pra comparar padrões vs losers
- **Skill 17** (content-recycler): transcreve winners pra derivar novas variações

## Limitações conhecidas

- Música alta + fala sussurrada → erro
- Sotaques muito marcados (accent pesado) → erro ocasional
- Text overlay NÃO é capturado (só áudio) — Whisper é audio-only
- Linguagem mista (code-switching Portuguese/English) → escolher `--language` da fala dominante

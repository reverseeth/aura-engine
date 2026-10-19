# Creative Engine · Referência: Criativos validados do TrendTrack, puxar, transcrever e modelar (ETAPA 0.5)

> A busca dos criativos mais validados do mercado no TrendTrack (filtros fixos e armadilhas), a escolha das peças, a transcrição pela cascade (Brand Tracker, `scan_ad`, skill `watch`), o corte em molde no mesmo schema da `competitor-analysis`, o `validated-molds.json` e o registro do ad modelado por conceito. Abra na ETAPA 0.5, antes de gerar ângulos.

### ETAPA 0.5 — O batch nasce do que já vende

Todo conceito do batch parte de um criativo que já está pagando a própria conta no mercado. A skill não inventa estrutura: ela puxa os anúncios mais validados do TrendTrack, lê a transcrição de cada um e reescreve a peça segundo a segundo com o argumento da Aura (VOC da `market-research`, mecanismo e oferta da `offer-builder`, buracos e ângulos da `competitor-analysis`).

A regra é a do cânone `.claude/lib/ad-molds/README.md`: **a estrutura vem do ad validado, o conteúdo vem da Aura.** Mesmo tipo de hook, mesma ordem de blocos, mesmo ritmo, mesma duração por bloco, mesmo tipo de frase. A frase, a afirmação, o número e o nome de mecanismo são os do membro.

#### 1. As duas fontes de ad validado

1. **Os escalados da `competitor-analysis`**, que já estão na mão: `competitor-analysis/ad-molds.json` (moldes prontos), `top_creatives` e o catálogo `ads-escalados-dados.json`. Concorrente direto, mesmo avatar.
2. **Os mais validados do mercado no TrendTrack**, com os mesmos filtros da descoberta da `product-research` (`.claude/skills/product-research/reference/descoberta-trendtrack.md`), recortados pelo nicho do produto. É aqui que entram as marcas que mais vendem fora da lista de concorrentes diretos: formato que escala em suplemento de sono costuma escalar em suplemento de articulação.

#### 2. A busca no TrendTrack (MCP)

Com tools `mcp__trendtrack__*` na sessão, rode antes a intenção **Account → créditos** (hoje `check_credits`) e diga ao membro em uma linha quantas chamadas a etapa gasta: 2 a 4 de busca, 1 por peça escolhida de `scan_ad` e 1 por marca de transcrição. A intenção de busca é **Discover → ads em lote** (hoje `search_ads`), casada pelo que a sessão expõe (`.claude/lib/trendtrack-integration/README.md`).

| Filtro | Param da tool (hoje) |
|---|---|
| Status: active | `status: "active"` |
| Days Running: 14 a 60 | `min_days_running: 14`, `max_days_running: 60` |
| Language: english | `ad_languages: ["en"]` |
| Niche: o do produto (default beauty & care, health & supplements) | `category_ids: [<ids de lookup_filter_ids type categories>]` |
| Ad rank: top 5% | `ad_rank_mode: "percentile"`, `max_ad_rank_value: 5` |
| Growth rank: rising | `growth_rank: [{ "period": "last7d", "direction": "rising" }]` (pouco resultado: `last30d`) |
| Active ads da página: min 200 | `min_active_ads: 200` |
| Países: EUA, Canadá, Austrália e Reino Unido | `ad_countries: { "include": ["US", "CA", "AU", "GB"] }` |
| Monthly traffic: min 200k | `min_traffic: 200000` |
| Ordenação | passada 1 `sort_by: "adOrder"`, `order: "asc"`; passada 2 `sort_by: "longestRunning"`, `order: "desc"` |
| Diversidade | `max_ads_per_brand: 2`, `limit: 20` |
| Formato | uma passada com `media_type: "video"` e outra com `"image"` quando o batch tem estático |

Para afunilar no produto, passe `query` com 1 a 3 palavras do problema ou do ingrediente (`search_in: "ad_copy"`). Busca magra: tire a `query` e fique só com o nicho.

Armadilhas, as mesmas da `competitor-analysis` (`.claude/skills/competitor-analysis/reference/molde-de-criativo.md`, bloco 1): `sort_by` sempre definido (sem ele entra o `trend_signal` de crescimento de 7 dias com filtro de alcance que ninguém pediu); mercado por `ad_countries`, nunca `main_countries`; conferir linha a linha o tipo de mídia e os dias no ar; alcance não é régua de escala fora da União Europeia (escala se lê por dias no ar, duplicatas, rank e ads ativos da página).

**Sem TrendTrack:** o membro aplica os mesmos filtros no browser (TrendTrack → Explorer → Meta Ads) e cola, por ad, o link, a mídia e os dias no ar. Nunca fingir que abriu a ferramenta.

#### 3. Escolha das peças

Uma peça por conceito previsto na capacidade de teste (ETAPA 2), mais uma ou duas de reserva. Ordem de preferência: rank mais forte, depois mais duplicatas, depois mais dias no ar dentro da janela de 14 a 60. Duas peças com a mesma estrutura aparente contam como uma; use a vaga num formato diferente (depoimento, demonstração, mecanismo, antes e depois, lista, estático de copy longa). Os moldes que já existem em `competitor-analysis/ad-molds.json` entram primeiro no pool e não se refazem.

De cada peça guarde: marca, id e link do ad (Ad Library ou TrendTrack), Media URL (Thumbnail URL só em estático), dias no ar, duplicatas, rank, ads ativos da página e LP de destino.

#### 4. Transcrição, a cascade

1. **Brand Tracker** (hoje `get_brandtracker_transcripts`): devolve o texto corrido dos vídeos da marca, com o número de usos. A marca precisa estar no Brand Tracker do membro; se não estiver, adicione com a intenção correspondente (hoje `add_to_brandtracker`) e avise em uma linha. Sem marcação de tempo: serve pra ler a peça inteira e pré-selecionar.
2. **`scan_ad`** com o id do ad ou o `collation_id`: hook transcrito, estrutura, enquadramento da copy, LP e veredito de escala.
3. **Transcrição cronometrada** pela cascade da `competitor-analysis` (Groq, Whisper local `medium` ou `turbo`, transcript do membro) ou pela skill `watch` no vídeo (Media URL ou link da Ad Library): ela extrai os quadros por troca de cena, o ritmo (cortes por minuto, duração dos planos), o microscópio dos primeiros 10 segundos e a transcrição local por whisper.cpp, sem o áudio sair da máquina.

O molde precisa de tempo: os degraus 1 e 2 sozinhos dão o texto e o hook, e o degrau 3 dá os segundos. Sem nenhum degrau com tempo, a peça entra só como referência de hook e formato (campo `modeled_ad` preenchido, `mold_id` nulo). Nunca inventar transcrição.

#### 5. Corte em molde

O corte em slots, a leitura da imagem por visão e o schema são os da `competitor-analysis` (`.claude/skills/competitor-analysis/reference/molde-de-criativo.md`, blocos 5 a 7), com os vocabulários fechados de `.claude/lib/ad-molds/molds.json`. Estático: o molde vira a ordem dos blocos da imagem (headline, sub, prova, oferta, CTA) com a contagem de palavras de cada um.

Salve em `workspace/[produto]/creative-engine/validated-molds.json`, no mesmo schema do `ad-molds.json`, com dois campos a mais por molde: `source: "trendtrack_market" | "competitor_analysis"` e `ad` (`brand`, `ad_url`, `media_url`, `days_running`, `duplicates`, `ad_rank`, `page_active_ads`, `lp_url`). Nenhum campo guarda a fala do ad; a transcrição fica em `creative-engine/validated-ads/transcripts/`.

#### 6. O que muda nas etapas seguintes

- **ETAPA 3:** cada ângulo candidato nasce casado com uma peça do pool. Ângulo sem peça que sirva continua valendo, mas desce na fila.
- **ETAPA 5:** o roteiro de cada conceito é escrito em cima do molde da peça (`reference/molde-e-injecao.md`), com a tabela slot a slot e a origem de cada argumento. Os 3 criativos do pack 3-2-2 compartilham o molde.
- **Registro:** todo conceito grava `modeled_ad` no `dados.json` e uma linha no briefing: marca, link do ad, link da mídia, dias no ar e a frase do encaixe. É o que deixa a `ad-analysis` ligar um breakthrough à peça que deu a estrutura.

#### Checagem antes de fechar a etapa

- Créditos informados antes da primeira chamada.
- Cada peça tem link do ad, link da mídia e dias no ar dentro de 14 a 60 (ou é molde herdado da `competitor-analysis`).
- Nenhuma frase, afirmação, número ou nome de mecanismo do ad aparece no `validated-molds.json`.
- O pool cobre a capacidade de teste ou a falta está dita ao membro em uma linha.

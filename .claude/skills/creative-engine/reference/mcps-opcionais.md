# Creative Engine · Referência: MCPs da produção (ETAPAs 0.5, 0.6 e 0.7)

> TrendTrack (a fonte dos criativos validados), Foreplay (sinal extra) e Higgsfield (a rota principal de produção): o que cada um faz, os limites de chamada, o custo de créditos e o caminho sem o MCP. Abra quando houver tools com esses prefixos na sessão, e na ETAPA 5.7 da Rota A.

### ETAPA 0.5 — TrendTrack MCP (a fonte dos criativos validados)

Com tools `mcp__trendtrack__` na sessão, o TrendTrack é a fonte principal do batch: a skill puxa os criativos mais validados do mercado, as transcrições e corta cada peça em molde. Procedimento inteiro em `reference/validados-trendtrack.md`. Além disso, 1 chamada de **`creative_inspiration_pack`** (nicho + palavras do problema) calibra os hooks da ETAPA 7 com aberturas que estão rodando agora.

Sem TrendTrack, o membro cola os ads pelo caminho manual do mesmo arquivo.

### ETAPA 0.6 — Foreplay MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__foreplay__` disponíveis (ad spy: 200M+ ads em Facebook, Instagram, TikTok, YouTube e LinkedIn, busca por marca e domain intelligence; o watchlist Spyder já entrega transcrição de hooks). Se SIM, ele entra como fonte extra de peças validadas no pool da ETAPA 0.5 (mesma escolha, mesma transcrição, mesmo molde) e de hooks ativos no nicho. Limite: 1 a 2 chamadas por batch. Se NÃO estiver disponível, siga normalmente (setup opcional em `.claude/automations/setup-mcps.md`).

### ETAPA 0.7 — Higgsfield MCP (rota principal de produção)

Com tools `mcp__higgsfield__` na sessão (MCP oficial da Higgsfield: 30+ modelos de imagem, vídeo e áudio, OAuth pelo browser, créditos do plano do membro, sem API key), a Rota A deixa de entregar só prompts e **renderiza os criativos in-session**. Sem o MCP, qualquer outra IA de imagem e vídeo serve (Veo, Kling, Sora, Runway, Midjourney, GPT Image e similares): a skill entrega os prompts autocontidos de sempre e o membro gera lá.

**Créditos antes de tudo.** Rode `balance`, some o custo estimado do batch (`ads_studio_quote` quando o caminho for o Ads Studio) e pergunte em uma linha: "Higgsfield conectado, com [saldo] créditos. O batch gasta cerca de [N]. Renderizo os [X] criativos ou prefere só os prompts?". Sem aprovação, nada é gerado.

**Qual tool pra cada peça:**

| Peça | Caminho no Higgsfield |
|---|---|
| Estático de produto (studio, lifestyle, ad pack) | `generate_image` (o modelo vem de `models_explore` com `action: "recommend"`); catálogo de product shots por `get_presets` com `source: "marketing_studio"`, `category: "product-shot"` |
| Estático de anúncio por template | Marketing Studio: `show_marketing_studio_v2` (UGC, ads, posters) ou `get_presets` com `source: "marketing_studio"`; abrir o catálogo nunca autoriza `execute_preset` sem a aprovação dos créditos |
| Vídeo UGC, tutorial, unboxing, review, TV spot | Marketing Studio nos modos `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_review`, `product_showcase`, `tv_spot`; marca e produto cadastrados uma vez (`ads_studio_create_brand`, `ads_studio_add_product`) e reusados em todo batch |
| Vídeo com produto em quadro | `generate_video` em image-to-video a partir da foto real do produto (`media_upload` → `media_confirm`), hierarquia I2V-first de `reference/rota-de-producao.md` |
| Mesma pessoa em vários criativos | `ai_influencer_prepare` → `ai_influencer_generate` (avatar fixo); é o único jeito de manter o rosto entre takes |
| Variações de um vídeo que já roda | `get_workflow_instructions` com `{ "workflow": "ad-multiplier" }` |
| Vídeo de várias etapas sem preset | `get_workflow_instructions` sem argumento, antes de gerar |
| Pontuar o hook antes de subir | `virality_predictor` no vídeo pronto: hook fraco volta pra reescrita antes de virar ad |

Lotes independentes vão por `generate_image_batch` / `generate_video_batch`, depois `jobs_wait` e um `show_generation_by_ids`.

**Skills oficiais da Higgsfield como apoio.** O repositório `github.com/higgsfield-ai/skills` traz `higgsfield-generate` (imagem, vídeo, áudio e Marketing Studio), `higgsfield-product-photoshoot` (modos `product_shot`, `lifestyle_scene`, `closeup_product_with_person`, `ad_creative_pack`, `social_carousel`, `moodboard_pin`, `hero_banner`, entre outros), `higgsfield-soul-id` (identidade de rosto treinada) e `higgsfield-brandkit` (identidade visual). Instalação: `npx skills add higgsfield-ai/skills`, ou no Claude Code `/plugin marketplace add higgsfield-ai/skills` e `/plugin install higgsfield@higgsfield`. Quando instaladas, a skill pode chamá-las pra peça específica (o `ad_creative_pack` do `product-photoshoot` pros estáticos, por exemplo); o briefing e a copy continuam vindo daqui.

**Regras que não mudam com o Higgsfield:**

- Prompt de vídeo por clipe nasce do zero e é autocontido: cada take é renderizado sem memória dos outros, então nada de "a mesma mulher do take anterior". Consistência de pessoa só com avatar fixo.
- Todo render passa pelo Limpador de Metadados antes de ser registrado: `bash tools/strip-metadata.sh workspace/[produto]/creative-engine/renders/` (o Higgsfield grava `hf-job-id` e C2PA no arquivo). Detalhe em `reference/entregavel-de-producao.md`.

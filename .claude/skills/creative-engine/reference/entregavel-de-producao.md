# Creative Engine · Referência: Entregável de produção (ETAPA 5.7): prompts de IA, EDL e mix

> Ramo A (prompts por clipe via directors, roteamento por tipo de cena, takes ou geração contínua, render in-session com o Higgsfield MCP, `prompts-index.json`), Ramo B (EDL com tabela timecode e usage rights) e Ramo C. Abra na ETAPA 5.7.

### ETAPA 5.7 — Entregável de produção (ramifica pela rota da ETAPA 1.0)

Após gerar os briefings (Etapa 5), pra CADA conceito gere o entregável de produção. Não é etapa opcional — é parte do entregável final. **A forma do entregável depende da rota escolhida na ETAPA 1.0:**

- **Rota A (IA)** → **Ramo A**: prompts production-ready por clipe (fluxo atual: marketing-studio-director / gpt-image-2-director).
- **Rota B (montagem)** → **Ramo B**: EDL / roteiro de montagem (`concept-XX-edl.md`).
- **Rota C (Mix)** → **Ramo C**: para cada conceito, rodar o ramo correspondente ao `concept.production_route` (alguns A, outros B).

Decida por conceito olhando `concept.production_route` (no Mix) ou a `production_route` global do batch.

---

#### Ramo A — Prompts production-ready de IA (Higgsfield/Veo/Sora/Kling + GPT Image 2.0)

Pra CADA conceito de rota A, gerar prompts prontos pra colar nas ferramentas de geração externas.

**Duração e estrutura de geração — depende do modelo (ETAPA 1.0, Pergunta 1.5):**

Antes de compor o prompt de vídeo, leia `creative-engine/dados.json → ai_video_model` e aplique:

- **Modelo de clipe curto (Higgsfield; Sora/outro quando o ad estoura o limite):** validar a duração falada por word count (ETAPA 4.5.C). Se o script passa do limite do modelo (~15s Higgsfield), **dividir em takes autocontidos** — hook num take, body (mecanismo/prova/CTA) começando no take seguinte (hook e body NUNCA no mesmo take), cada take 100% autocontido (sem referência a outro clipe). Lógica completa em `marketing-studio-director.md` (MULTI-SHOT SPLITTING). Entregável = 1 pasta por conceito, 1 arquivo por take.
- **Modelo de geração contínua (Veo 3.1 ~60s; Sora 2 ~25s quando cabe; Kling longo):** gerar o ad inteiro numa **única geração contínua** — um roteiro só, coeso, sem split. A regra "autocontido sem memória cross-shot" **NÃO se aplica** aqui (é roteiro contínuo). Entregável = 1 arquivo único por conceito (`prompt-c01-video.txt`), com o roteiro contínuo (hook → bridge → hold → CTA encadeados) + link/instrução de generation do modelo. O `marketing-studio-director.md` é canônico só pra Higgsfield; pra modelo longo, adaptar a saída pra um roteiro contínuo (mesma copy do briefing, sem dividir em shots).

**Roteamento por tipo de cena (doutrina da ETAPA 1.0):** cena com produto/rótulo em quadro = **I2V a partir da foto real** (anexar a foto como `<<<image_1>>>`); talking head = **avatar fixo + lip-sync**; B-roll atmosférico sem produto = T2V. NUNCA gerar produto/rótulo via T2V puro — alucina embalagem e texto.

**Diretores disponíveis** (em `.claude/lib/prompt-directors/`):

| Director | Ferramenta alvo | Quando invocar |
|---|---|---|
| `marketing-studio-director.md` | Higgsfield Marketing Studio (vídeo) | Conceito com componente de vídeo (qualquer formato: UGC, demo, motion graphic, hyper motion, TV spot, etc) |
| `gpt-image-2-director.md` | GPT Image 2.0 (imagem) | Conceito com componente de imagem estática (PDP-style hero, layout denso com texto, infografia, mockup, ou single-frame cinematográfico) |

**Statics — sistemas de prompt da base (rodar ANTES de compor o prompt de imagem de qualquer conceito com static):** puxe **Prompt Básico de Statics (9 hooks) + Prompt Banger + $100K Static Ads Prompt** — rode a `best_query` exata `prompt basico 9 hooks mass desire testing approach banger headlines inspired by example ad`. São três sistemas: o **básico** gera 9 hooks por mass desire pra teste; o **Banger** produz headlines a partir de um ad de exemplo (alimente com um winner real — da Skill `ad-analysis` se houver histórico, ou um escalado do nicho vindo da `competitor-analysis`/ETAPA 0.5/0.6); o **$100K Static Ads Prompt** monta o static completo. O output desses sistemas vira INPUT do `gpt-image-2-director` (headline/overlay/estrutura extraídos do briefing) — o director continua sendo quem formata o prompt final de imagem.

**Processo por conceito:**

1. Identificar quais formatos o conceito tem (vídeo? imagem? ambos? — vem da Etapa 5 do briefing)
2. Para cada formato presente, carregar o director correspondente:
   - Vídeo → ler `.claude/lib/prompt-directors/marketing-studio-director.md`
   - Imagem → ler `.claude/lib/prompt-directors/gpt-image-2-director.md`; se a imagem tem pessoa fotorrealista, aplicar POR CIMA as regras obrigatórias de `.claude/lib/prompt-directors/real-people-imagery.md` (pessoa crível, lote distribuído por pesquisa, zero pele exposta, embalagem por referência, câmera/luz, contexto imperfeito)
3. Compor input pro director extraindo do briefing:
   - **Pra Higgsfield (vídeo)**: hook completo + bridge + hold + CTA + visual descriptions de cada beat + duração + creator archetype + plataforma primária + product/avatar attached (se houver)
   - **Pra GPT Image 2.0 (imagem)**: descrição visual principal + texto overlay + estilo + proof elements + estrutura de layout (se denso) ou cena cinematográfica (se single-frame)
4. Rodar o director conforme as regras do SKILL.md dele:
   - Marketing Studio: identifica preset (UGC/Tutorial/Unboxing/Hyper Motion/Product Review/TV Spot/Wild Card/UGC Virtual Try On/Pro Virtual Try On), aplica preset-specific rules, retorna 1 parágrafo + link Higgsfield
   - GPT Image 2.0: roteia entre Format A (JSON estruturado pra layout denso), Format B (prosa cinematográfica pra single image), ou Format C (meta-prompt pra theme-only) — retorna code block do prompt
5. Salvar em `workspace/[produto]/creative-engine/prompts/`:
   - **Geração contínua (Veo/Sora dentro do limite/Kling) OU vídeo curto que cabe num take só:** 1 arquivo `prompt-c01-video.txt` — roteiro único (contínuo pros modelos longos; take único pros curtos)
   - **Vídeo curto que estoura o limite do modelo (Higgsfield >15s, multi-shot):** 1 PASTA por conceito (`c01-[slug]/`) com 1 arquivo por take (`shot-1.txt`, `shot-2.txt`, …). Shot 1 = hook; body começa no shot 2 (hook e body NUNCA no mesmo take, cada take autocontido). Cada arquivo de take tem: cabeçalho (conceito, hook, nº do shot, duração estimada, preset), o parágrafo pra colar na ferramenta, o link de generation, e ABAIXO as notas pro membro (produto SIM/NÃO, consistência avatar/cenário, pronúncia) — notas nunca dentro do parágrafo colado.
   - **Imagem:** `prompt-c01-image.txt` (se conceito tem componente de imagem)
   - Quando split, também salvar `_LEIA-PRIMEIRO.txt` na raiz de `prompts/` explicando ordem dos takes, durações e como juntar no editor com 1 voiceover por cima. (Geração contínua não precisa de `_LEIA-PRIMEIRO` — é um clipe só.)

**Inputs herdados (CRÍTICO — não duplicar trabalho):**

- A copy exata (hook, headline, subhead, dialogue) vem do briefing — director NÃO inventa copy nova, só formata
- Product fidelity: se o membro tem foto do produto, o prompt do director menciona explicitamente "<<<image_1>>> = product"
- Avatar fidelity: se há foto de avatar/creator, mesma referência `<<<image_n>>>`
- Aspect ratio 9:16 já é regra global (Etapa 4.5.A) — director NÃO especifica aspect, ferramenta seleciona

**Hard rule — directors são opacos:**

Os SKILL.md dos directors são canônicos. Não modificar conteúdo deles dentro da Skill `creative-engine`. Se a saída precisar de ajuste, ajustar o INPUT (extrato do briefing) que vai pro director, não o director. Se houver bug recorrente em algum director, atualizar `.claude/lib/prompt-directors/[director].md` em commit separado.

**Render in-session (se Higgsfield MCP conectado — ETAPA 0.7):**

Se há tools `mcp__higgsfield__*` na sessão E o membro aprovou o render, após salvar cada prompt:

1. Chamar a tool de geração correspondente à rota da cena (I2V com a foto real do produto pra cenas com produto; lip-sync pra takes de avatar; T2V só pra B-roll)
2. Salvar o vídeo resultante em `workspace/[produto]/creative-engine/renders/`, **com o índice da EXECUÇÃO no nome** — as 3 execuções do pack 3-2-2 são 3 arquivos distintos, e a `ad-strategy` sobe cada uma como um ad separado dentro do ad set do conceito: `c0X-[creative-n].mp4` na geração contínua, ou `c0X-[creative-n]-shot-N.mp4` quando o modelo exige split em takes (Pergunta 1.5 da ETAPA 1.0)
3. **Limpar os metadados do render** antes de registrar: `bash tools/strip-metadata.sh workspace/[produto]/creative-engine/renders/` (regra 12 — o Higgsfield grava `hf-job-id` e C2PA no arquivo; o limpador remove sem re-encodar e renomeia pra `asset-xxxx.mp4`). Se o ffmpeg não estiver instalado, ofereça instalar (`brew install ffmpeg` / `winget install Gyan.FFmpeg`) e, enquanto isso, deixe o render em `renders/` marcado como `metadata_clean: false` no `dados.json` — ele NÃO sobe assim
4. Registrar cada path (já com o nome `asset-xxxx.mp4`) em `production_prompts.video.rendered_files[]` no `dados.json`, **um item por execução** (`creative_n` de 1 a 3, na mesma ordem do pack e do `utm_content=[concept-id]-[creative-n]` da Skill `ad-strategy`), com `metadata_clean: true`. Execução ainda não renderizada fica com `file: null` — a lista sempre tem os 3 itens

Falha de render (créditos esgotados, timeout, tool error) NÃO bloqueia a skill — o prompt salvo continua sendo o entregável e o membro gera manualmente (escape-path: sempre ≥2 caminhos). Sem o MCP, o fluxo é o atual (prompts pra colar).

**Output secundário — `prompts-index.json`:**

Em `workspace/[produto]/creative-engine/prompts/prompts-index.json`:

```json
{
  "generated_at": "ISO",
  "concepts": [
    {
      "concept_id": "c-01",
      "video_prompt_file": "prompt-c01-video.txt",
      "video_prompt_folder": "c01-slug/|null",
      "_comment_video_prompt_folder": "preenchida só quando multi-shot (Higgsfield estourando o limite); senão null",
      "video_shots": [
        { "file": "shot-1.txt", "phase": "hook", "duration_sec": 4, "product_ref": false },
        { "file": "shot-2.txt", "phase": "body", "duration_sec": 14, "product_ref": true }
      ],
      "video_director": "marketing-studio-director",
      "video_preset": "UGC|Tutorial|...",
      "image_prompt_file": "prompt-c01-image.txt",
      "image_director": "gpt-image-2-director",
      "image_format": "json|prose|meta"
    }
  ]
}
```

---

#### Ramo B — EDL / roteiro de montagem (`concept-XX-edl.md`)

Pra CADA conceito de rota B (montagem de clipes), gerar um **EDL (Edit Decision List)** — o roteiro que o editor segue pra montar o ad juntando footage real. NÃO é prompt de IA. É um plano de montagem timecode a timecode.

**Insumo:** o briefing completo do conceito (Etapa 5) — hook, bridge, hold, CTA, durações, copy exata, text overlays. A copy NÃO muda; o EDL só decide com qual footage cada beat é coberto.

**Estrutura do arquivo `workspace/[produto]/creative-engine/concept-XX-edl.md`:**

```
# EDL — Conceito #[N]: [nome]

**Ângulo (frase):** [...]  ·  **Método:** [marksman/sniper]  ·  **Awareness:** [...]  ·  **Funil:** [TOF/MOF/BOF]
**Duração total alvo:** [Xs]  ·  **Aspect ratio:** 9:16 (1080×1920)
**Voiceover:** [sim/não — se sim, script vem do briefing, gerado no ElevenLabs por cima da montagem]

## Roteiro de montagem

| Timecode | Tipo de clipe | Fonte sugerida | Text overlay | Legenda (caption) | Transição |
|----------|---------------|----------------|--------------|-------------------|-----------|
| 00:00–00:03 | Hook / pattern interrupt | UGC licenciado (Billo/Insense) OU stock — pessoa reagindo | "[overlay literal]" | "[caption literal]" | hard cut |
| 00:03–00:08 | Bridge / problema | UGC ou b-roll do produto | "[overlay]" | "[caption]" | jump cut |
| 00:08–00:18 | Hold / mecanismo+prova | demo do produto + close-up | "[overlay com número/dado]" | "[caption]" | match cut |
| 00:18–00:22 | CTA | produto em tela + badge garantia | "[CTA overlay]" | "[caption]" | — |

> Para as 3 execuções do 3-2-2, repita a tabela conforme o método (ETAPA 4.5.A.0.2). **Sniper:** varia SÓ a linha do hook (00:00–00:03) — #2 e #3 trocam só o clipe e o overlay de abertura, o resto da montagem é idêntico. **Marksman:** #2 e #3 trocam o clipe, o overlay e a **legenda de abertura** para abrir um ângulo diferente; as linhas de bridge/hold/CTA permanecem idênticas (é o hold universal) e precisam sustentar os 3 ângulos.

## Referência de timing (modelar concorrente)

[Se o membro indicou um criativo escalado de concorrente como referência: descrever a ESTRUTURA/ritmo dele — "hook nos primeiros 2s, corta a cada 1.5s, prova no segundo 9, CTA no `team-engine`" — como guia de montagem. NUNCA instruir a baixar/reusar o clipe do concorrente. É referência de timing, não asset.]

## ⚠️ Usage rights (OBRIGATÓRIO — ler antes de montar)

Todo footage usado na montagem precisa ser **licenciado pra uso comercial em ads**:

- ✅ **UGC licenciado** (Billo, Insense, Trend.io, ou creator contratado com cessão de direitos por escrito pra paid ads)
- ✅ **Stock pago** com licença comercial (Artgrid, Storyblocks, Envato — confirmar que cobre paid social)
- ✅ **Material próprio** (você filmou / é dono)
- ❌ **Clipe de TikTok/Reels de terceiro** — NÃO é livre. Baixar e reusar footage de outro criador sem licença é violação de copyright e expõe a conta de ads a strike/ban. Um criativo de concorrente serve SÓ como referência de timing/estrutura (coluna acima), nunca como asset na montagem final.
- ❌ Música/trending sound de catálogo não-licenciado em ad pago (em orgânico TikTok ok; em ad pago precisa de áudio licenciado).

Se o membro não tem footage licenciado pra um beat, o EDL marca esse beat como `[FALTA FOOTAGE — opções: contratar UGC Billo/Insense (~$X) | stock pago | filmar próprio]` em vez de sugerir reuso.
```

**Salvar:** `concept-XX-edl.md` por conceito de rota B, em `workspace/[produto]/creative-engine/`. Não gera arquivo em `prompts/` (não há prompt de IA pra esse conceito). Registrar no `creative-engine/dados.json` (`concept.edl_file`).

---

#### Ramo C — Mix (ambos)

Para cada conceito, rodar o ramo do seu `concept.production_route`: conceitos `ai` seguem o Ramo A (prompts em `prompts/`), conceitos `edl` seguem o Ramo B (`concept-XX-edl.md`). Um mesmo batch pode ter os dois tipos de entregável lado a lado. O `creative-engine/dados.json` registra a rota de cada conceito e o arquivo correspondente.

# Creative Engine · Referência: Regras estruturais globais (ETAPA 4.5, blocos A.0 a D e F a I)

> As regras que valem pra todo briefing: método de teste e as 4 hard rules do 3-2-2, ângulo é frase e conceito é embalagem, awareness lock, aspect ratio, plataforma primária, word count por duração e limite por modelo, jargão só em overlay, origem da VOC, hook-swap, estilo e limpeza de metadados. O bloco E (zona emocional) está em `reference/zona-emocional.md`. Abra na ETAPA 4.5.

### ETAPA 4.5 — Regras estruturais globais (aplicadas a TODO briefing)

Antes de gerar briefings individuais, estas regras se aplicam a qualquer conceito, independente de vertical/formato:

**A.0. 3-2-2 — Método de teste + Hard Rules (GATE — ler antes de gerar qualquer briefing)**

Um 3-2-2 = 3 criativos + 2 primary texts + 2 headlines = 1 post ID = **1 conceito**. Cada 3-2-2 responde **UMA pergunta**. Qual pergunta ele responde depende do **método de teste** escolhido — e é o método que define o que os 3 criativos podem variar entre si.

> **Onde o 3-2-2 vive na campanha:** com a estrutura atual (Skill `ad-strategy`, ETAPA 3.3: 1 campanha com CBO → N ad sets broad/Advantage+), **1 conceito = 1 ad set = 1 pack 3-2-2**. Os 3 criativos do conceito entram como os 3 ads daquele ad set, com os 2 primary texts e as 2 headlines do pack. Criativo de um conceito nunca sobe no ad set de outro: é a separação por ad set que preserva a resposta pra "qual conceito funcionou" quando a Skill `ad-analysis` lê.

**A.0.1 — Escolha o método ANTES das hard rules (cânone `.claude/lib/ad-taxonomy/README.md` §7)**

O cânone define três métodos; a Skill `creative-engine` usa dois e nunca os redefine localmente:

| Método | Quando | O que os 3 criativos variam |
|---|---|---|
| **Marksman** | **primeiro** teste de um produto/avatar — achar DIREÇÃO | **3 ângulos distintos**, um por criativo, sobre um **hold universal** |
| **Sniper** | depois que a direção existe — extrair o máximo do ângulo vencedor | **1 ângulo**, 3 execuções: varia só hook/abertura/visual de entrada |
| Shotgun | volume alto em conta madura (fora do escopo de um batch da Aura) | — |

**Default por conceito, derivado do cânone §7 ("imagens → Marksman; vídeos → Sniper; toda iteração → Sniper"):**

| Situação do conceito | `testing_method` default |
|---|---|
| Primeiro teste, formato **imagem** (static, product photography, infográfico, meme) | **`marksman`** |
| Primeiro teste, formato **vídeo** | **`sniper`** (Marksman em vídeo é a rota avançada — só se o membro for experiente e o hold universal passar no gate A.0.2) |
| **Conceito que É iteração** (itera um criativo que já rodou, ou o ângulo já teve direção num batch anterior) | **`sniper`**, sempre — sem exceção. A regra é POR CONCEITO, não por batch: num batch derivado da `ad-analysis`, um conceito de direção NOVA pode ser `marksman` — é o retorno do cânone §7 quando a performance platôa e o ângulo já foi "snipado" |
| Ângulo já venceu e o conceito está aprofundando comportamento/experiência do sub-avatar | **`sniper`** |

Grave `testing_method` por conceito no `dados.json`. Na apresentação da ETAPA 4, declare o método de cada conceito junto do ângulo — o membro precisa saber se aquele pack está procurando direção ou extraindo profundidade.

**A.0.2 — As 4 Hard Rules (a #1 muda com o método; 2, 3 e 4 valem nos dois)**

1. **ÂNGULO — depende do método.**
   - **Se `sniper`:** os 3 criativos testam **o mesmo ângulo**. Varia só hook/abertura/visual de entrada. O hold é **específico e profundo**, colado naquele ângulo.
   - **Se `marksman`:** os 3 criativos testam **3 ângulos distintos** (é o ponto do método — achar qual ângulo o mercado favorece), com **hold universal** ancorado no `core_avatar.surface_desire` da Skill `market-research`. Fórmula do cânone: **hooks mais específicos + hold mais genérico**.
   - **Gate do Marksman (obrigatório):** o hold precisa ser declarado universal e **validado contra os 3 hooks, um a um** — se ele não sustenta qualquer um dos 3 ângulos, o conceito não é Marksman válido. Hold específico demais com hooks de ângulos diferentes colados na frente é "meio Sniper, meio Marksman" e não ensina nada. Registre `hold_universal_validated: true` no `dados.json`; `false` bloqueia o conceito até o hold ser reescrito ou o método virar `sniper`.
   - **Gate do Sniper (obrigatório):** o hold NÃO pode ser genérico. Hook forte seguido de hold que serviria para qualquer hook (o caso do neck guard: *"career-ending injury"* seguido de "breathable, secure, 15x stronger") é problema de execução disfarçado de ângulo morto. O hold do Sniper mostra comportamento, experiência e emoção daquele sub-avatar específico.
2. **MESMO formato** — 3 vídeos OU 3 imagens, **nunca misturar**. Variação de formato (vídeo↔imagem) vira um **3-2-2 SEPARADO**, não criativo #2 dentro do mesmo. Vale nos dois métodos.
3. **MESMO awareness level** — os 3 travados no mesmo nível de Schwartz (ver "Awareness lock" logo abaixo). Awareness diferente = conceito diferente. Vale nos dois métodos.
4. **MESMO intent** — mesma pergunta de teste, mesma posição de funil, mesmo formato de entrega. Body/mecanismo/prova/CTA permanecem coerentes entre os 3 (no Marksman, "coerente" = o mesmo hold universal; no Sniper, = o mesmo hold específico). Vale nos dois métodos.

**Variação que NUNCA é permitida dentro de um 3-2-2, em nenhum método:** formato diferente (#1 vídeo, #2 imagem), awareness diferente (#1 TOF, #3 BOF), intent diferente. Qualquer uma dessas exige um 3-2-2 novo (= novo conceito). Ângulo diferente é permitido **apenas** em `marksman` — em `sniper` continua proibido e vira conceito separado na ETAPA 2.

**A.0.3 — Ângulo é frase; conceito é embalagem (GATE: todo ad precisa de um ângulo)**

O cânone §7 é literal: *"Ângulo é a razão de compra em frase ('para de virar de um lado pro outro a noite toda'). Conceito é a embalagem (comparação, depoimento, autoridade). Skill que pede 'escolha o ângulo' e oferece uma lista de formatos está pedindo conceito."*

Por isso os dois vivem em campos separados do `dados.json`, e a skill **força a frase**:

- **`angle`** — string obrigatória, **em frase completa, voltada ao cliente, dando uma razão de compra**. A fonte é `sub_avatars[].angle` do `market-research/dados.json` (já vem em frase, um por sub-avatar). Ângulo novo criado aqui (ETAPA 3, Verticais 1 e 3) segue o mesmo formato de frase.
- **`concept_type`** — enum fechado da embalagem: `problem|result|curiosity|social|authority|comparison|controversy|identification`. É a estratégia do teste (o que VOCÊ quer aprender), não a razão de compra.

**Teste de classificação, aplicado a toda entrada de `angle` antes de gerar briefing:**

| Frase | Classificação | Por quê |
|---|---|---|
| "stops tossing and turning all night" | **ângulo** | dá razão de compra |
| "brings back your energy" | **ângulo** | dá razão de compra |
| "us vs them" | conceito | comparação **de quê**? o "quê" é o ângulo |
| "before & after" | conceito | é a embalagem |
| "problem aware ads" | conceito | de qual problema? |
| "post-it note ads" | formato | nem conceito é |

**Gate (roda no checklist da ETAPA 9):** todo conceito tem `angle` preenchido, em frase, passando no teste acima. Uma palavra solta, um rótulo de formato ou um valor do enum `concept_type` no campo `angle` = **reprovado**, volte à ETAPA 3. Mesmo quando o conceito nasce de uma pergunta de formato ("testar UGC"), o ângulo ainda precisa existir: *"EVERY AD NEEDS AN ANGLE — se o conceito é 'testar formato UGC', você ainda precisa definir o que está vendendo."*

**Awareness lock:** trave o awareness_level do conceito e aplique aos 3 criativos. Valide cada conceito contra `awareness_distribution` de `market-research/dados.json` — se o nível escolhido tem peso <10% na distribuição do mercado, emita warning ("awareness X representa só Y% do mercado; confirma a aposta?") antes de prosseguir.

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
| Format | 1 criativo = 1 ad dentro do ad set do conceito (breakdown nativo por ad) | 1 criativo = 1 ad set |

Se o batch roda em **ambas** as plataformas, o briefing tem 2 versões do script: Meta-optimized e TikTok-optimized. Não assuma portabilidade 1:1.

**C. Word count validation por duration (spoken script)**

Cadência de fala natural pra ad é **2.8 a 3.0 palavras por segundo** (mesma referência canônica do `marketing-studio-director.md`: ~43 palavras ≈ 15s). Use esse range pra validar se o script cabe na duração alvo. O director é a fonte única — se houver divergência, vale a do director.

| Duration alvo | Word count ideal (fala) | Word count teto absoluto |
|---------------|-------------------------|--------------------------|
| 10s | 28-30 palavras | 33 |
| 15s | 42-45 palavras | 48 |
| 22s | 62-66 palavras | 72 |
| 30s | 84-90 palavras | 98 |
| 45s | 126-135 palavras | 145 |

**Regra:** ao gerar script de voiceover/fala, ANTES de salvar, conte as palavras e confirme que cabe no range. Se estourar, corte — não deixe o editor precisar acelerar a fala pra caber (soa robótico e destrói retention).

Text overlay não conta nesse cálculo — overlay roda em paralelo à fala.

**Limite de duração por geração — depende do modelo (só relevante pra Rota A/IA):** o split em takes ≤15s **não é universal** — é o limite do **Higgsfield**. O comportamento depende do `ai_video_model` escolhido na ETAPA 1.0 (Pergunta 1.5):

- **Modelo de clipe curto (Higgsfield ~15s; Sora/outro quando o ad estoura o limite):** cada geração é 1 clipe renderizado do zero, **sem memória dos clipes anteriores**. Se o script falado passa do limite, NÃO acelere a fala nem corte — **divida em takes** ≤limite: hook num take, body (mecanismo/prova/CTA) começando no take seguinte (hook e body nunca no mesmo take), cada take 100% autocontido. Lógica completa em `marketing-studio-director.md` (MULTI-SHOT SPLITTING). Entregável = 1 pasta por conceito, 1 arquivo por take.
- **Modelo de geração contínua (Veo 3.1 ~60s; Sora 2 ~25s quando cabe; Kling longo):** gera o ad inteiro numa **geração única contínua** — sem split, mais coeso. A regra "autocontido por clipe sem memória cross-shot" **NÃO se aplica** (é um roteiro contínuo). Entregável = 1 arquivo único por conceito.

A validação de word count por duração (tabela acima) vale em qualquer caso — o que muda é se o script vira 1 clipe contínuo ou vários takes. Detalhe operacional na ETAPA 5.7 (Ramo A). Na Rota B (montagem), não há "geração" — a duração é controlada na edição via o EDL.

**D. Spoken vs Overlay — disciplina de jargão técnico**

Siglas, números complexos, nomes científicos, compostos químicos, unidades de medida e claims regulatórios são **sempre text overlay**, **nunca** na fala. Regras:

- Siglas (qualquer acrônimo de 2+ letras maiúsculas) → overlay
- Números com decimais, percentuais, ou unidades técnicas → overlay (`"48.5% improvement"`, `"2,500 IU"`)
- Nomes de ingrediente/composto químico complexos → overlay
- Estudos citados com N amostral, duração → overlay ou gráfico

**Motivo:** a fala precisa fluir emocionalmente. Siglas/números faladas quebram ritmo, desligam avatares 35+, soam clinicamente desinteressante. No overlay, o mesmo dado ganha peso de evidência visual sem matar cadência.

**Regra de ouro:** se a frase contém ≥2 elementos técnicos, quebrar — a parte emocional vai na fala, os dados duros vão no overlay lado-a-lado.


> **Bloco E (Valence × Intensity, as 4 Hook Emotions e o hook archetype):** está em `reference/zona-emocional.md`, que se abre junto com este arquivo.

**F. Origem da VOC — registrar de qual frase real o hook nasceu**

Hook, primary text ou headline que nasce de uma frase real de cliente (VOC phrases, trigger events, objeções, dores hierarquizadas do `market-research/dados.json`) registra a origem no output JSON — é o que permite à Skill `ad-analysis` medir qual frase do mercado vendeu:

```json
{
  "asset_id": "c-01-h-03",
  "text": "texto do hook",
  "voc_source": {
    "ref_id": "voc-001",
    "original_phrase": "frase exata do review/post/comment",
    "source_type": "amazon_review|reddit_thread|tiktok_comment|g2_review|...",
    "confidence": "direct_quote|paraphrase|inferred_pattern"
  },
  "emotion_dominant": "curiosity|urgency|fear|delight"
}
```

`ref_id` é o **id estável cunhado pela Skill `market-research`** (`voc-001`, `voc-002`… em `voc_top20[]` e `voc_evidence[]` de `market-research/dados.json`) — use o id da frase de origem. Produto legado sem ids na `market-research`: gravar `"ref_id": null` e preencher `original_phrase`. Hook que nasce de ângulo, mecanismo ou insight (não de uma frase literal) grava `"voc_source": null` e segue — não é falha, é informação pra `ad-analysis`.

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

**H. Estilo (rule 8 do CLAUDE.md)**

- Zero travessão (—) em headlines; ≤2 em copy longa (8a)
- Claim direto, específico, sem aviso, disclaimer ou suavização inserida por conta própria (8b) — a peça sai na força que a pesquisa sustenta

**I. Limpeza de metadados — obrigatória antes de QUALQUER upload (regra 12 do CLAUDE.md)**

Todo gerador de IA (Higgsfield, Veo, Sora, Kling, GPT Image, Midjourney) grava metadados de proveniência no arquivo — EXIF/XMP/IPTC, manifesto C2PA, chunks de texto como o `hf-job-id` do Higgsfield — e as plataformas de ads leem isso. Nenhum criativo sobe sem passar pelo **Limpador de Metadados** (`tools/limpador-de-metadados/`), que remove tudo sem alterar um pixel nem um frame e renomeia pra `asset-xxxx.<ext>`:

- **O membro:** 2 cliques em `Limpador de Metadados` na pasta da Aura (o hook de início de sessão deixa lá o lançador do sistema dele) → arrasta os criativos finais, arquivos ou a pasta inteira, ou usa os botões de escolher → cada arquivo é substituído pelo limpo `asset-xxxx`, na mesma pasta. É o último passo antes de subir, depois da edição (CapCut/Submagic exportam com metadados próprios — limpa o arquivo FINAL, não o bruto).
- **A skill:** tudo que o Higgsfield MCP renderizou em `renders/` passa por `bash tools/strip-metadata.sh workspace/[produto]/creative-engine/renders/` antes de ser entregue (in-place; os nomes viram `asset-xxxx.mp4` e `rendered_files[]` no `dados.json` é atualizado com os nomes novos).
- **A receita de upload** (`upload-creative-to-meta.md`) recusa arquivo cujo nome não é `asset-xxxx` até rodar o limpador nele.
- Listar no resumo de produção (ETAPA 8) o passo de limpeza como último item antes do upload.

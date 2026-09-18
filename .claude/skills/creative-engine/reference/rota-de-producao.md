# Creative Engine · Referência: Rota de produção e material disponível (ETAPAs 1.0 e 1)

> A Pergunta 0 (rota A, B ou C, com o default por stage e nicho), a hierarquia de rotas de geração de vídeo por IA, a Pergunta 1.5 (modelo de geração e o que ele muda), a Pergunta 1 (material disponível), a matriz de creator archetype e o Creator Diversity Matrix. Abra na ETAPA 1.0.

### ETAPA 1.0 — Rota de Produção (Pergunta 0 — ANTES de tudo)

Antes de calcular conceitos, gerar ângulos ou briefings, defina **COMO os criativos vão existir no mundo**. Essa escolha muda o entregável final (prompts de IA vs roteiro de montagem) e como o briefing é escrito. É a primeira pergunta da skill.

Antes de perguntar, calcule o **default recomendado** por stage + nicho (member-stage-awareness + profile), e apresente já com a recomendação marcada — sem travar a escolha do membro:

| Stage / contexto | Default recomendado | Razão |
|---|---|---|
| Starter (budget < $50/dia, primeiro batch) | **Rota A (IA)** | Custo marginal por variação quase zero, sem creator, gera volume rápido pra preencher os ad sets de teste |
| Validating | **Mix (Rota C)** | IA pra volume + 1-2 montagens modeladas em concorrentes que já escalam no nicho |
| Scaling | **Mix (Rota C)** | Diversidade de produção é lever de scale (Skill `scale-engine`); IA + UGC licenciado + montagens |
| Nicho de alta confiança visual (skincare/beauty 45+, supplement, onde UGC humano real converte muito mais que avatar de IA) | **Rota B ou Mix** | Avatar de IA derruba credibilidade nesses nichos; modelar o que já vende e montar com UGC real rende mais |

Pergunte ao membro (no `report_language`):

"Como você quer produzir esses criativos? Tem 3 rotas:

- **(A) Gerar com IA** — você roda os clipes no Higgsfield Marketing Studio (ou outro modelo) a partir de prompts prontos. Rápido, barato por variação, sem precisar de creator. Entrego **prompts prontos por clipe**. *(custo de referência: Higgsfield Ultra ~$129/mês; gera volume ilimitado de variações)*
- **(B) Modelar concorrente / montar clipes** — você (ou um editor) monta o ad juntando footage real: UGC licenciado (Billo, Insense), stock, ou material próprio, seguindo um **roteiro de montagem (EDL)** que eu entrego — tabela com timecode, tipo de clipe, fonte sugerida, text overlay, legenda exata e transição. Um criativo escalado de concorrente serve SÓ como referência de *timing/estrutura*, nunca pra reusar o clipe dele.
- **(C) Mix** — alguns conceitos com IA, outros com montagem. Diversidade de produção ajuda na escala.

Minha recomendação pro seu caso: **Rota [X]** — [razão de 1 frase]. Quer seguir com ela ou prefere outra?"

Salve a escolha em `manifest.json → production_route: "ai" | "edl" | "mix"` e no `creative-engine/dados.json → production_route`. Para **Mix**, na ETAPA 4 (seleção de conceitos) marque por conceito qual rota cada um segue (`concept.production_route`).

**Se Rota A (ou conceito A no Mix) — hierarquia de rotas de geração (doutrina de vídeo AI, ordem de preferência):**

1. **Image-to-video (I2V) a partir de foto REAL do produto** — default pra QUALQUER cena com produto/rótulo em quadro (Kling 3.x é o modelo de referência). O primeiro frame nasce ancorado na foto real, então embalagem, rótulo e texto do produto NÃO alucinam. Peça a foto do produto ao membro antes de compor os prompts.
2. **Avatar fixo + lip-sync** — rota talking head (UGC/testimonial). Consistência da pessoa entre takes só existe com avatar fixo; o script vem do briefing e o lip-sync anima a fala.
3. **Text-to-video (T2V — Sora 2 / Veo 3.1)** — SÓ pra storyboard e B-roll atmosférico (lifestyle, textura, cenário) SEM produto/rótulo em quadro. T2V alucina texto e embalagem; nunca é o asset principal de direct response.

Um mesmo conceito pode combinar as 3 rotas (ex: hook I2V com produto + B-roll T2V + take de avatar lip-sync) — o roteamento por tipo de cena corta custo vs gerar tudo no modelo premium.

**Opção externa pra talking-head (menção, não integração):** se o membro quer volume de vídeo testimonial-style sem gravar gente real e sem montar avatar, o **Arcads** (arcads.ai) transforma script em vídeo UGC com ator AI em minutos (~$2.20/vídeo a partir de $110/mês; alternativa: Creatify, workflow URL-do-produto → ad). A skill escreve o script (o forte da Aura) e o membro renderiza lá. É redundante com a rota avatar + lip-sync pra quem já paga Higgsfield — só recomende se o membro já assina ou pediu explicitamente essa classe de ferramenta.

**Pergunta 1.5: qual modelo de geração?**

A escolha do modelo define **duração e estrutura de geração** (ETAPA 5.7, Ramo A). Pergunte (ou leia de `profile.md → ai_video_model` se já registrado):

"Qual gerador de vídeo de IA você vai usar?
- **Higgsfield Marketing Studio** (clipes curtos, ~15s max por geração) — default, presets de marketing prontos
- **Veo 3.1** (até 60s contínuo)
- **Sora 2** (até 25s contínuo)
- **Kling 3.x** (clipes longos contínuos; modelo de referência pra image-to-video de product shots)
- Outro / não sei → assumo Higgsfield"

Guarde em `creative-engine/dados.json → ai_video_model`. O impacto:

| Modelo | Limite por geração | Estrutura de geração | Regra "autocontido por clipe" |
|---|---|---|---|
| **Higgsfield Marketing Studio** | ~15s | **Split em takes** ≤15s (hook num take, body no seguinte) | **APLICA** — cada take é renderizado do zero, sem memória dos outros |
| **Veo 3.1** | ~60s | **Geração contínua única** (o ad inteiro num prompt) | NÃO aplica — é um roteiro contínuo, mais coeso e mais barato |
| **Sora 2** | ~25s | **Geração contínua única** se o ad cabe em ~25s; senão split | NÃO aplica abaixo do limite |
| **Kling 3.x** | longo | **Geração contínua única** | NÃO aplica |

A regra de **"clipe autocontido sem memória cross-shot"** (herdada do `marketing-studio-director.md`) vale **só pra modelos de clipe CURTO** (Higgsfield, e Sora/qualquer modelo quando o ad estoura o limite). Pra modelos longos, gerar o ad inteiro numa **geração contínua** — mais coeso, mais barato, sem split. O split fixo ≤15s da versão antiga era limite do Higgsfield, **não** uma regra universal.

**Se Rota B (ou conceito B no Mix):**

Não há modelo de IA a escolher. O entregável vira um **EDL/roteiro de montagem** por conceito (ETAPA 5.7, Ramo B). Avise o membro que a fonte das imagens precisa ser **licenciada** (UGC de Billo/Insense, stock pago, ou material próprio) — clipe de TikTok/Reels de terceiro NÃO é livre pra reusar. Esse aviso reaparece formalizado no bloco de **usage rights** do EDL.

### ETAPA 1 — Material Disponível + Creator Archetype (Pergunta 1)

Pergunte:

"Que tipo de material você tem pra montar os ads?
- Clips do TikTok/Reels de outros criadores (servem como referência de estrutura/timing, não como footage — ver bloco de Usage Rights)
- Vídeos do fornecedor/fabricante
- UGC gerado por AI (Higgsfield, Arcads, HeyGen, etc)
- Fotos de produto
- Creator humano contratado (pago pra gravar)
- Self-recorded (você mesmo grava)
- Mix de tudo acima"

**Creator Archetype Auto-Selection (realista):**

A maioria dos membros NÃO vai pagar creator humano ($150-500 por vídeo) e NÃO vai querer gravar a si mesmo (barreira alta). Selecione archetype default com base na resposta + budget do profile:

| Resposta do membro | Budget < $500/mês | Budget $500-2k/mês | Budget > $2k/mês |
|--------------------|-------------------|--------------------|-------------------|
| "não tenho nada" / "só fotos" | **AI UGC + stock + motion graphics** (default) | AI UGC + founder-led opcional | AI UGC + 1-2 creators humanos |
| "tenho clips do TikTok" | Montagem licenciada + AI UGC | Montagem licenciada + AI UGC | Montagem licenciada + creator humano |
| "tenho vídeo do fornecedor" | Demonstração + motion graphics | Demo + AI UGC complementar | Demo + creator humano |
| "posso gravar eu mesmo" | Founder-led + AI UGC | Founder-led + AI UGC | Founder-led + creator humano |
| "tenho creator contratado" | Raro — mas priorize o creator | Creator humano primary | Creator humano primary |

**Default geral (se membro estiver em dúvida):** AI UGC + stock + motion graphics. Esse mix é acessível, escalável, e cobre 80% dos cenários.

**Coerência com a rota de produção (ETAPA 1.0):** se o membro escolheu **Rota A (IA)**, o archetype default é `ai_ugc`/`motion_graphics` (gerável por prompt). Se escolheu **Rota B (montagem)**, o archetype tende a `demo`/`creator_human`/`licensed_montage` (footage real montado) — a pergunta de material acima já vira input do EDL. Na **Rota C (Mix)**, cada conceito carrega seu próprio archetype conforme a rota daquele conceito.

> **"Montagem licenciada" (`licensed_montage`):** clipes de TikTok/Reels que o membro coletou servem SÓ como referência de timing/estrutura — o clipe de terceiro NUNCA entra na montagem final (violação de copyright + risco de strike/ban na conta de ads; ver bloco de Usage Rights no Ramo B). A montagem real usa stock pago, UGC licenciado (Billo/Insense) ou material próprio, modelando a ESTRUTURA do que já escala.

Use o archetype pra influenciar FORMATO e SCRIPT dos conceitos:
- **AI UGC** (Higgsfield/Arcads): avatar-driven, ajuste de fala natural obrigatório pra não soar robotizado, duração 15-22s ideal
- **Montagem licenciada** (estilo modelado em criadores): cortes rápidos, UGC-style hooks de pattern interrupt, nenhuma voz off — estrutura modelada, footage 100% licenciado
- **Motion graphics**: carregado de claims, com muito texto na tela, ideal pra listicle hooks e mechanism explainers
- **Founder-led**: talking head caseiro, tom pessoal, storytelling, duração 25-45s
- **Demonstração**: close-up do produto em uso, b-roll intercalado, mínimo de talking, foco em proof visual
- **Creator humano**: UGC tradicional com spokesperson, maior range de duração e complexidade de script

**Diversidade de talento entre conceitos (variável Avatar do mapa de composição):** ao definir QUEM aparece/grava em cada conceito, puxe o **Creator Diversity Matrix** da base — rode a `best_query` exata `creator diversity matrix idade raca genero idioma espanhol caracteristicas fisicas psicografia` — e varie deliberadamente os 6 eixos (idade, raça, gênero, idioma, características físicas, psicografia) ENTRE os conceitos do batch, em vez de repetir o mesmo perfil de talento em todos. Espanhol nos EUA é subvalorizado: um criativo em espanhol escalou a $10k/dia só regravando ads em inglês já provados. A matriz vale igual pra creator humano e pra avatar de IA (a rota avatar fixo + lip-sync da ETAPA 1.0 escolhe o avatar pelos mesmos eixos), e o eixo escolhido de cada conceito fica declarado no campo **Avatar** do briefing (ETAPA 5).

> **Handoff:** aqui os creators entram só como FONTE de material do batch. O motor operacional de creators (seeding, casting, ambassadors, whitelisting) é a skill **creator-engine**: pedido de recrutar, gerir ou whitelistar creators vai pra ela, não pra esta skill.

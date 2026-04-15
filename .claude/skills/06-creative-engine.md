---
name: creative-engine
description: Engine de criação de briefings de criativos para Meta Ads. Use quando o membro disser "creatives", "criativos", "briefings", "ads", "criar anúncios", ou quando a copy estiver pronta e o membro precisar dos briefings de criativos.
---

# Creative Engine

## Quando Usar
Quando o membro tem copy pronta e precisa dos briefings de criativos pra rodar no Meta.

## Antes de Começar
1. Leia /workspace/profile.md (especialmente orçamento diário)
2. Leia /workspace/[produto]/02-market-research.md (Voice of Customer, awareness level)
3. Leia /workspace/[produto]/03-competitor-analysis.md (o que concorrentes fazem e NÃO fazem)
4. Leia /workspace/[produto]/04-offer.md (mecanismo único, oferta)
5. Leia /workspace/[produto]/05-copy.md (headlines, copy aprovada)
6. Consulte a base Aura com as seguintes buscas (deep=true):
   - "ad definitions concept angle variation 3-2-2 format"
   - "ad angles how to create selling strategy"
   - "ad formats roadmap creative video image carousel"
   - "3-2-2 flexible ads format rules testing"
   - "funnel creative playbook olympic rings model"
   - "video ads examples hooks content editing"
   - "image ads creation breakdowns"
   - "building creative with AI complete process"
   - "write your video ads script"
   - "hooks video ads first 3 seconds"
   - "new information ads market sophistication"
   - "processo 9 etapas ads 7-8 digitos"
   - "winning ad rate hit rate volume"
   - "hero offer best customer second scale"
   - "partnership ads creator content 3 rules"
7. Internalize TUDO antes de começar

## Conceitos Fundamentais (da base Aura)

Antes de gerar qualquer briefing, o Claude Code deve entender:

- **Conceito/Batch**: a estratégia do teste — o que estamos testando nesse batch
- **Ângulo**: a razão de compra que estamos comunicando (o "por quê comprar")
- **Variação**: execuções diferentes do mesmo ângulo
- **Formato**: como entregamos o ad (UGC, demonstração, imagem, carrossel, etc)
- **3-2-2**: 3 criativos + 2 primary texts + 2 headlines = 12 combinações = 1 ad object no Meta
- **Hit rate > Volume**: menos criativos com mais intenção escala mais que volume sem pesquisa

## Fluxo da Skill

### ETAPA 1 — Material Disponível

Pergunte ao membro:

"Que tipo de material você tem pra montar os ads?
- Clips do TikTok/Reels de outros criadores
- Vídeos do fornecedor/fabricante
- UGC gerado por AI (Higgsfield, etc)
- Fotos de produto
- Mix de tudo acima"

Use a resposta pra influenciar o FORMATO dos conceitos recomendados (ex: se só tem fotos de produto, prioriza imagem estática e carrossel; se tem clips do TikTok, prioriza UGC-style; se tem AI UGC, prioriza avatar-driven).

### ETAPA 2 — Definir Quantidade de Conceitos

Consulte a base Aura: "how many ads test budget concepts per week 3-2-2"

Calcule baseado no orçamento do membro (do profile.md):

**Fórmula: Budget diário / Target CPA = máximo de ad sets ativos**

Exemplo: $100/dia com CPA target de $20 = máximo 5 ad sets (incluindo champions).
Se está começando (sem champions): pode ter até 5 ad sets de teste = 5 conceitos.
Se já tem champions: 1 champions + até 4 conceitos novos.

Mostre ao membro: "Com seu budget de $X/dia, vou gerar [N] conceitos. Cada conceito = 1 ad set com um 3-2-2 (3 criativos + 2 texts + 2 headlines)."

Não peça confirmação do número — segue com [N].

### ETAPA 3 — Definir Ângulos

Consulte a base Aura: "ad angles how to create" e "3 research verticals competitive consumer internal"

Gere ângulos baseados nas 3 verticais de pesquisa (decisão automática, sem consulta ao membro):

1. **Vertical Competitiva** (do competitor analysis): gaps que os concorrentes NÃO exploram.
2. **Vertical do Consumidor** (do market research): dores, desejos, linguagem real.
3. **Vertical Interna** (da oferta/mecanismo): o mecanismo, ingrediente ou processo único.

Selecione os [N] ângulos mais fortes e apresente pro membro em formato de resumo:

"Esses são os [N] conceitos que recomendo testar:
1. [Conceito + ângulo em 1 frase]
2. ...

Quer ajustar algum antes de eu gerar os briefings completos?"

Se o membro disser "tá bom" / "segue" → vai pra etapa 4.
Se o membro pedir ajuste → aplique e confirme.

### ETAPA 3 — Gerar Briefings por Conceito

Para cada conceito aprovado, gere o briefing completo:

**BRIEFING DE CONCEITO #[N]**

**Conceito:** [o que estamos testando]
**Ângulo:** [a razão de compra]
**Awareness Level:** [de quem estamos falando]
**Formato:** [UGC / demonstração / antes-depois / imagem / carrossel / etc]

**3 Criativos (variações do mesmo conceito):**

Para CADA criativo:

**Criativo [N].1:**
- Tipo: [vídeo UGC / vídeo demonstração / imagem estática / carrossel]
- Se VÍDEO:
  - Hook (primeiros 3 segundos — texto/fala EXATA): "[texto]"
  - Descrição visual do hook: [o que aparece na tela]
  - Corpo do script (fala completa ou text overlays por momento):
    - [00:00-00:03] Hook: "[texto]" — [descrição visual]
    - [00:03-00:08] Problema: "[texto]" — [descrição visual]
    - [00:08-00:15] Solução/Mecanismo: "[texto]" — [descrição visual]
    - [00:15-00:22] Resultado/Prova: "[texto]" — [descrição visual]
    - [00:22-00:25] CTA: "[texto]" — [descrição visual]
  - Duração alvo: [15-30 segundos]
  - Música: [tipo de música ou "sem música"]
  - Precisa de voiceover ElevenLabs? [sim/não]
  - Se sim: script de voiceover separado: "[texto completo da locução]"
- Se IMAGEM:
  - Descrição visual: [o que aparece]
  - Texto overlay principal: "[texto]"
  - Textos secundários: "[textos]"
  - CTA visual: "[texto do botão/badge]"

**2 Primary Texts (body copy do ad):**

Primary Text 1: [copy completa — ângulo direto]
Primary Text 2: [copy completa — ângulo diferente, não reescrita cosmética]

As duas devem ser meaningfully different: ângulos diferentes, hooks diferentes, estruturas diferentes. NÃO são variações de palavras.

**2 Headlines:**

Headline 1: [frame de valor #1]
Headline 2: [frame de valor #2]

Novamente: dois frames reais de valor, não variações cosméticas.

**URL de destino:** [PDP / landing page / advertorial — qual e por quê]

**Racional estratégico:**
- Por que esse conceito? [justificativa baseada na pesquisa]
- O que esperamos aprender? [a pergunta que esse teste responde]
- Como saberemos se ganhou? [a campanha inteira melhorou, não só métricas isoladas do ad]

### ETAPA 4 — Page Testing (LP Congruency)

Consulte a base Aura: "landing page congruency customer journey ad to page"

Para cada conceito, recomende a landing page mais congruente:
- Se o ângulo é educacional → advertorial ou listicle
- Se o ângulo é direto → PDP
- Se o ângulo é oferta → landing page de oferta

Se possível, sugira duplicar os 3 criativos com URL diferente pra testar a LP (o "page testing ad set" da vault). Isso permite testar 2 jornadas com os mesmos criativos.

### ETAPA 5 — Hooks Bank

Consulte a base Aura: "hooks video ads first 3 seconds categories"

Para os conceitos de vídeo, gere ADICIONALMENTE um banco de 10 hooks alternativos:
- 3 hooks de problema ("Your skin isn't aging — it's...")
- 3 hooks de resultado ("How I got glass skin in...")
- 2 hooks de curiosidade ("Dermatologists don't want you to know...")
- 2 hooks de prova social ("50,000 women switched to this because...")

Esses hooks são pra iterar depois. Quando o conceito ganhar e o membro quiser testar variações de hook, ele já tem material.

### ETAPA 6 — Resumo de Produção

No final, apresente um resumo claro do que o membro precisa produzir:

**Resumo de Produção — Batch #1**

| Item | Quantidade |
|------|-----------|
| Conceitos | [N] |
| Criativos (total) | [N x 3] |
| Primary Texts (total) | [N x 2] |
| Headlines (total) | [N x 2] |
| Vídeos que precisam ser filmados | [N] |
| Vídeos que precisam de voiceover ElevenLabs | [N] |
| Imagens que precisam ser criadas | [N] |

**Próximos passos pra o membro:**
1. Filme os vídeos seguindo os scripts acima
2. Gere os voiceovers no ElevenLabs com os scripts marcados
3. Edite os vídeos usando sua ferramenta preferida (CapCut, Submagic, Captions, ou similar) — os briefings acima têm tudo: scripts, hooks, text overlays, estrutura
4. Quando os criativos estiverem prontos, diga 'ad strategy' pra montar a campanha

### SALVAR

Salve em: /workspace/[produto]/06-creatives/
- 06-creative-strategy.md (visão geral: ângulos, conceitos, racional)
- 06-briefing-conceito-01.md
- 06-briefing-conceito-02.md
- (um arquivo por conceito)
- 06-hooks-bank.md
- 06-production-summary.md

Ao final diga: "Briefings de criativos prontos. Próximos passos:
- Filme os vídeos seguindo os scripts
- Gere voiceovers no ElevenLabs
- Agora edite os vídeos usando sua ferramenta de edição preferida (CapCut, Submagic, Captions, ou similar). Os briefings acima têm tudo que você precisa: scripts, hooks, text overlays, e estrutura do ad. Quando os criativos estiverem prontos, diga 'ad strategy' pra montar a campanha no Meta."

---
name: content-recycler
description: Pega 1 criativo winner e gera 9 derivadas adaptadas a canais diferentes (advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube pre-roll, SMS, package insert, podcast ad). Reaproveita o winner em 9 canais sem produção nova. Use quando o membro disser "recycle [id]", "reaproveitar winner", "content recycler", "tirar mais dos ads". Zero infra externa, só Claude + Python.
---

# Content Recycler (Skill 14)

Skill auxiliar invocável. Reutiliza criativos vencedores em 9 formatos diferentes.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` + `README.md`, mapa skill→domínio no README). O domínio desta skill é **creatives-hooks-formats** (43 sistemas). Quando uma etapa pede "consultar a base", NUNCA use query genérica — puxe os SISTEMAS NOMEADOS rodando `search_knowledge` com a `best_query` de cada framework relevante pra aquela etapa (`deep=true`).

## Quando usar

**Manual**: membro diz `recycle [creative-id]` ou `recycle winner`.

**Automático** (futuro, com Shadow Brain #1 rodando): disparada quando a skill 11 já marcou um criativo como winner em `latest.winners[]`.

## Pré-flight

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (README.md/.html, essence.json descritivo) e toda conversa com o membro usam esse idioma. **As 9 derivadas consumidor-final (advertorial, email, TikTok, blog, Pinterest, YouTube, SMS, package insert, podcast) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

- [ ] `manifest.json` existe
- [ ] Pelo menos 1 criativo em `workspace/[produto]/08-creative-engine/` OU membro forneceu fonte alternativa
- [ ] `.claude/lib/content-recycler/recycler.md` existe (este lib é o engine)
- [ ] `.claude/lib/content-recycler/formats.json` existe (specs dos 9 formatos)
- [ ] `.claude/lib/compliance-preflight/` existe (pra rodar check em cada derivada)

**Detecção de winner (quando input é `recycle winner`):**

Se membro digitou `recycle winner` (sem ID específico):
1. Ler `workspace/[produto]/11-ad-analysis/dados.json` (produzido pela Skill 11)
2. Ler `latest.winners[]` — o array JÁ vem filtrado pela skill 11 (só criativos com `outcome == "winner"`). A 14 NÃO recomputa critério; apenas ordena por `spend_total` desc (tiebreak `days_active` desc). Se precisar de target pra exibir, leia explícito de `manifest.target_cpa`.
3. Se `winners.length === 1` → usar `winners[0].creative_id`
4. Se `winners.length >= 2` → apresentar lista ordenada (id + cpa + roas + spend) e perguntar qual reciclar
5. Se `winners.length === 0` OU campo `winners` ausente (versão antiga do `dados.json`) → responder:
   > "Campanha ainda não tem winner identificado pela skill 11.
   >
   > Opções:
   > 1. Aguardar mais dados (normalmente 5-10 dias após launch)
   > 2. Rodar skill 11 de novo pra atualizar análise
   > 3. Forçar reciclagem de um criativo específico: `recycle [creative-id]`"
6. Se `dados.json` não existir (skill 11 nunca rodou) → oferecer 2 caminhos (não abortar seco):
   > "Skill 11 não foi rodada ainda, então não tenho winner identificado automaticamente. Opções:
   > (A) Rodar `run analysis` agora pra identificar o winner, OU
   > (B) reciclar um criativo específico direto: `recycle [creative-id]`."

## Fluxo

Siga exatamente o fluxo descrito em `.claude/lib/content-recycler/recycler.md`:

1. **Identificação do winner** — input `[creative-id]` ou `winner` (lê `latest.winners[]` já marcado pela skill 11, ordena por spend_total)

2. **Extração de essência** — destilar big idea, hook, mechanism, avatar, voice em `essence.json`. Esta etapa decide o que de fato pode ser reaproveitado: isole o que é replicável (ângulo, mecanismo, prova) do que é descartável (formato específico do criativo). Puxe os SISTEMAS NOMEADOS abaixo (rode `search_knowledge` com a `best_query`, `deep=true`):
   - **Hook Writing Framework — 3 Functions of a Hook** (rode `hook framework 3 functions ad video stop scroll create curiosity`) — pra identificar qual das 3 funções o hook winner cumpre antes de reembalar.
   - **Ad Definitions — Concept / Angle / Variation / Format** (rode `ad definitions concept angle variation format 3-2-2 testing structure`) — separa o que é CONCEITO/ÂNGULO reaproveitável (viaja entre canais) do que é só FORMATO descartável.
   - **Storytelling as the Hardest-to-Replicate Angle** (rode `storytelling hardest to replicate angle founder story defensible creative`) — se a essência for narrativa de fundador/origem, ela é o ativo mais defensável; preserve-a intacta nas 9 derivadas.
   - **Show Don't Tell** (rode `show don't tell behavioral change when telling aren't selling spoken language video`) — destila a demonstração central do winner pra carregá-la pros formatos visuais (TikTok, Pinterest, YouTube).

3. **Consultar base Aura por formato** — para CADA uma das 9 derivadas, puxe os SISTEMAS NOMEADOS do domínio (não query genérica; `deep=true`). Curadoria de maior impacto por formato:
   - **Advertorial / Blog SEO** → **Caples' Four U's Hierarchy** (rode `Caples four U's hierarchy unique useful urgent ultra-specific headlines`) + **Hopkins' Specificity Rule** (rode `Hopkins specificity rule 1-2 second rule vague vs specific claims`) + **Objection → Claim → Proof → Benefit cycle (the Hold)** (rode `objection claim proof benefit cycle hold section one cycle`) — headlines específicas e ciclos de prova pra long-form.
   - **Organic TikTok / YouTube pre-roll** → **Gap Theory of Curiosity** (rode `gap theory of curiosity hooks counterintuitive open loop slippery slope`) + **Slippery Slope Principle** (rode `slippery slope principle open loops pattern interrupt end with intrigue video script`) + **4-Section Video Ad Structure (Hook / Bridge / Hold / CTA)** (rode `video ad script 4 section structure hook bridge hold CTA timing 30-45 seconds`) + **Strategic Pacing** (rode `strategic pacing rapid cuts hook bridge solution CTA video editing rhythm`) — reembala o winner em estrutura de vídeo orgânico com ritmo de corte por seção.
   - **Pinterest carousel / package insert (estáticos)** → **Static/Image Archetypes by Funnel Position** (rode `static image archetypes funnel position plain reminder direct response complexity rule`) + **13+ Winning Static Ad Templates** (rode `13 winning static ad templates avatar callout nutella meme breakdown why it works`) — escolhe arquétipo estático certo pra cada slide.
   - **Email sequence / SMS / Podcast ad** → **The Big 4 Emotions** (rode `Big 4 Emotions NEW ONLY EASY ANYBODY SAFE PREDICTABLE BIG FAST`) + **Brunson's Five Curiosity Hooks** (rode `Brunson five curiosity hooks controversial bold prediction conspiracy reframe angles`) — reframes de curiosidade pra subject lines / aberturas de SMS / leitura de podcast quando o ângulo do winner já saturou no feed.
   - **Transversal a TODAS as 9** → **Congruency — The Multiplier** (rode `congruency multiplier ad landing page offer visual message emotional continuity`) — cada derivada mantém continuidade de mensagem/promessa com o winner e com `04-offer-builder/dados.json` (sem deriva de mecanismo).
   - Demais frameworks do domínio (Hormozi Callout System, What-Who-When Matrix, SUCCESs, New Opportunity vs Improvement, etc.) ficam disponíveis em `.claude/lib/kb-index/` pra puxar sob demanda quando o formato pedir.

4. **Gerar 9 derivadas** em paralelo (advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube preroll, SMS, package insert, podcast ad)
5. **Compliance Pre-flight em cada** — severity >= high dispara auto-rewrite
6. **Gerar README.md + compliance-log.json** consolidados

## Email-sequence: não colidir com os flows da Skill 13

A derivada `email` que esta skill gera é uma **variação A/B de nutrição derivada do winner** — uma sequência de e-mails que reaproveita o ângulo/hook do criativo vencedor pra testar outra mensagem de nutrição. Ela **NÃO é um flow de lifecycle** e **NÃO substitui nem sobrescreve** o welcome / post-purchase / abandoned-cart da **Skill 13** (que é a fonte única de verdade dos flows de retenção).

Regras pra não colidir:
- **Nunca** instruir o membro a importar essa sequência "como welcome flow" no Klaviyo — isso desligaria/duplicaria o welcome da 13.
- Posicionar como **flow separado / teste paralelo** (ex: segmento de teste, ou campanha one-off), que roda **ao lado** dos flows da 13, não no lugar deles.
- Se o membro ainda não rodou a Skill 13, recomendar rodar a 13 primeiro (welcome/post-purchase são baseline de retenção) e usar esta derivada só como variação de teste depois.

## Output

Pasta `workspace/[produto]/14-content-recycler/[source-id]/` com:
- `README.md` — índice + instruções de distribuição
- `README.html` — companion humano (rule 6b do CLAUDE.md)
- `essence.json` — essência extraída (reusável)
- `compliance-log.json` — log consolidado
- 9 arquivos `.md`, um por formato (advertorial, email, TikTok, blog, Pinterest, YouTube preroll, SMS, package insert, podcast)
- 9 arquivos `.html` correspondentes — um pra cada `.md` (rule 6b: dual output obrigatório)

Além das pastas por source-id, escreva também no topo de `workspace/[produto]/14-content-recycler/` um índice `relatorio.md` + `relatorio.html` que lista todas as fontes recicladas (cada `[source-id]` com seus 9 formatos e link pra pasta). Esse índice é o relatório humano que o painel do produto exibe.

## SALVAR (dual output — rule 6b do CLAUDE.md)

Toda derivada salva em `workspace/[produto]/14-content-recycler/[source-id]/` DEVE ter `.md` (fonte pra AI) + `.html` companion (visualização humana). Use `.claude/templates/aura-report-template.html` como base — copie o CSS inline e a logo SVG do `.claude/templates/aura-logo-snippet.html` LITERALMENTE no topo do `<body>`. NUNCA gere HTML sem a logo SVG nem com texto "AURA"/"Aura Engine" no lugar dela.

Depois de salvar todos os outputs e atualizar o `manifest.json`:
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza ABRIR-AQUI.html).

## Sucesso

- [ ] 9 arquivos `.md` gerados
- [ ] 9 arquivos `.html` companion gerados (rule 6b)
- [ ] Cada um passa compliance check (severity ≤ medium)
- [ ] Essence.json salvo
- [ ] README.md + README.html com índice pronto

## Customização

Pra adicionar novo formato (ex: LinkedIn post, Substack newsletter, Twitter thread), editar `.claude/lib/content-recycler/formats.json` adicionando entry com:
- `id`, `name`, `output_file`
- `length_words` range
- `structure` template
- `tone`
- `compliance_notes`

Próxima rodada da skill gera automaticamente também esse formato.

## Mensagem final ao membro

```
✓ Content Recycler rodou em [source-id]
  9 formatos gerados em workspace/[produto]/14-content-recycler/[source-id]/

  Compliance: [X críticos, Y high, Z medium, W low]
  Rewrites aplicados: [N]

  Distribuição sugerida:
  → Advertorial: publicar como LP secundária pra cold traffic
  → Email sequence: variação A/B de nutrição (NÃO sobrescrever o welcome da Skill 13 — rodar como flow/teste separado)
  → TikTok orgânico: post na conta da marca
  → Blog: publicar pra SEO, registrar no Search Console
  → Pinterest: criar board, pin semanal
  → YouTube pre-roll: campaign separada
  → SMS: wire no Postscript como opt-in trigger
  → Package insert: enviar pro fornecedor imprimir
  → Podcast: outreach pra shows do nicho

  Abra o README.md da pasta pra ver índice completo.
```

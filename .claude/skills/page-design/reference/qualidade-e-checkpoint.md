# Page Design · Referência: Regras de qualidade comuns, self-review visual e checkpoint de aprovação (sub-etapa 3.7)

> As ground rules das três rotas (markers `data-aura-section`, SVG, travessão, tipografia, performance budget, imagens do mapa de mídia, call-to-value, 4 modalities, receita por sessão, congruência e tratamento por page_type), o self-review por screenshot desktop e mobile lido por visão e o checkpoint como draft navegável com versionamento e escalada. Abra depois de gerar o `page.html`, antes do membro ver.

### 3.7 Regras de qualidade COMUNS (as três rotas)

Independente da rota, `design/page.html` precisa passar nas mesmas ground rules antes do checkpoint. **A régua é bloqueante: a página não vai ao membro sem passar.**

- **Marcação de sections:** cada section marcada com `<section data-aura-section="hero">`, `data-aura-section="benefits">`, etc (um por section do plano, usando os mesmos ids de `sections_plan[].id`) — isso permite o SPLIT determinístico na `page-build` sem ambiguidade. Se a rota não gerou esses markers (comum no HTML que vem de fora, rotas 2 e 3), você os injeta antes de salvar.
- **Ícones SVG inline** (Lucide/Heroicons/Phosphor), NUNCA emojis na UI da página (rule 7).
- **Copy sem cara de AI:** minimizar travessão (rule 8a, zero em headlines).
- **Tipografia/layout:** type scale modular (1.25 ou 1.333); fluid type `clamp()` em headings; spacing generoso (padding-block 5-8rem em hero/oferta); WCAG AA contraste; focus-visible; `prefers-reduced-motion`; touch targets ≥44px; responsivo real, mobile-first.
- **Performance (budget de página):** imagens comprimidas (WebP/AVIF quando possível) e `loading="lazy"` abaixo da dobra; a imagem do hero SEM lazy (é o LCP) e COM `width`/`height` explícitos (zero layout shift); ZERO JavaScript de runtime (interação = `<details>`/CSS). Proxy simples: HTML+CSS ≤ ~150KB, página total com imagens ≤ ~1.5MB — o alvo real é LCP mobile < 2.5s. A `page-build` re-valida isso como gate (GATE 1) antes do deploy; estourar aqui = retrabalho lá.
- **Imagens do mapa de mídia (ETAPA 1.6):** toda section com `media.required` tem a imagem REAL no slot, ou placeholder EXPLÍCITO (visivelmente marcado) com `acquisition_plan` registrado no `page-plan.json`. Nunca stock aleatório fingindo ser final, nunca `src` de sandbox de gerador, nunca imagem ou foto da página de referência (rotas 2 e 3).
- **CTAs como call-to-VALUE** ("Start My 30-Day Glow", não "Buy Now"). Fundamente em **CTAs / Calls to Value** (rode `CTAs buttons friction anxiety calls to value lizard brain first person mirror headline`) e decida direto vs stepping-stone com **Direct vs Transitional CTA** (rode `direct vs transitional CTA Miller buy now download guide stepping stone`).
- **Serve as 4 modalities ao mesmo tempo** — antes do checkpoint, confira que o `page.html` atende **4 Decision Making Modalities** (rode `4 decision making modalities spontaneous competitive humanistic methodical web copy`): Spontaneous (CTA rápido acima da dobra), Competitive (comparison/diferenciação), Humanistic (prova social, rostos, histórias), Methodical (specs, garantia, FAQ). Falta de uma = furo de conversão.
- **Régua econômica da página** — a página é avaliada também pelo número que ela terá que sustentar: **Revenue per Session** (rode `revenue per session AOV vezes CVR problema de site ou de tráfego`) — receita por sessão = AOV × conversão, referência em torno de $2,50. Não é métrica pra medir agora (não há tráfego ainda); é a régua que a Skill `ad-analysis` vai usar pra separar problema de página de problema de tráfego — desenhe a página sabendo que ela responde por esse número (hero que segura a dobra, oferta que sustenta o AOV da `offer-builder`, CTA sem fricção).
- **Congruência ad→page:** o topo da página tem que ecoar a promessa do ad que traz o tráfego — valide com **Congruence Principle** (rode `congruence principle message match ad to landing page scent Kennedy consistency rule`).
- **Tratamento por page_type:** advertorial → editorial (dek, drop caps, ritmo de leitura); listicle → o mesmo tratamento editorial com os itens numerados e visíveis na varredura (número grande, subtítulo por item, respiro entre eles); landing/pdp → benefit-forward com proof acima da dobra; quiz → uma tela por vez, progresso sempre visível e altura estável entre perguntas. Em advertorial e listicle, aplique os **Ogilvy 14 Readability Devices** (rode `Ogilvy 14 readability devices drop caps captions subheads reverse type`) e a **Double Readership Path** (rode `Kennedy double readership path skimmers analytical readers subheads PS`) pra servir skimmers e leitores analíticos.

Se a rota entregou HTML que viola alguma dessas (comum no HTML ingerido das rotas 2 e 3), **corrija inline** antes de salvar — não devolva ao membro pra ele consertar.

### Self-review visual (OBRIGATÓRIO antes do checkpoint — o membro nunca vê defeito óbvio)

Ler o HTML como texto NÃO é ver a página. Antes de apresentar QUALQUER draft ao membro, você olha a página renderizada com os próprios olhos:

1. **Renderize** `design/page.html` no Playwright via `file://` (skill `webapp-testing`) e capture screenshot **full-page** em DUAS larguras: desktop (1440px) e mobile (390px).
2. **LEIA os dois screenshots por visão** e caçe defeitos: hierarquia frouxa (headline que não domina a dobra), contraste insuficiente na prática (texto sobre imagem/surface), spacing quebrado (sections coladas ou buracos gigantes), imagem estourada/distorcida/com overflow, texto cortado ou colidindo em mobile, CTA invisível, placeholder implícito parecendo final, tipografia que caiu pra fallback (serif genérica onde devia ter a heading font). **Página parecendo parede de texto** (mobile principalmente — blocos longos entre CTAs, seções que repetem a mesma ideia): não corte copy por conta própria aqui — sinalize e rode a dieta de copy da Skill `copy-engine` (sweep 4.5), que corta redundância preservando prova/VOC e com aprovação do membro.
3. **Auto-corrija inline** o que encontrar (post-task-self-audit: silent fix) e re-screenshote. Repita até os dois screenshots passarem.
4. Só então apresente o draft ao membro no checkpoint abaixo. Repita este self-review a cada versão nova (`page-v2.html`...) antes de devolver ao membro.
5. **Na rota 3, o teste de vizinhança da 3.5 faz parte deste self-review:** seções vizinhas com assinatura visual diferente (peso de título, botão, espaçamento, largura) reprovam e voltam pro passo de unificação.

### Checkpoint de aprovação (iteration-driven-refinement)

Apresente como **draft navegável**, não como "pronto". Adapte a pergunta à rota:
> "Página montada (rota [escolhida]). Abre `design/page.html` no browser e me diz o que ajustar. Pergunta granular: o tom tá certo (mais editorial ou mais direto)? O hero puxa atenção? A hierarquia de proof convence? Itero até você dizer 'tá bom'."

**Este HTML é a FONTE ÚNICA DE VERDADE visual.** O membro aprova AQUI, antes de qualquer Liquid existir. Não avance pra `page-build` sem aprovação. E não declare aprovado com slot de imagem pendente: cada section com `media.required` tem a imagem REAL, ou o placeholder EXPLÍCITO da ETAPA 1.6 com `acquisition_plan` registrado no `page-plan.json` (avise o membro que a `page-build` bloqueia o deploy enquanto o placeholder existir).

- Cada iteração salva versão nova (`design/page-v2.html`, `-v3`), não sobrescreve. Log em `workspace/[produto]/page/iterations-log.json`.
- Max 3 iterações sem progresso → escalate, oferecendo trocar de rota: na rota 1, peça uma referência concreta (print ou página que ele curta) e ofereça a rota 2 ou 3; na rota 2, ofereça outra página de referência ou desenhar do zero pela rota 1; na rota 3, ofereça reduzir o número de fontes (quanto mais fonte, mais difícil unificar) ou desenhar as seções problemáticas pela rota 1.
- Quando o membro aprova, consolide como `design/page.html` (versão canônica): é o HTML aprovado da própria rota, ou a variação escolhida promovida a arquivo final quando a rodada ofereceu mais de uma. Diga: "Salvando como `design/page.html` — fonte única de verdade. A `page-build` vai compilar exatamente isso em Liquid."

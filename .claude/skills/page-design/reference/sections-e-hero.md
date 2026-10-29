# Page Design · Referência: Sections pela narrativa, hero_type, blocks e plano ao membro (sub-etapas 1.2 a 1.5)

> Como as sections nascem da narrativa do produto fora do advertorial e do listicle, a lista de exemplos de section (inclusive o bloco `specs` pros agentes de compra), os exemplos de planos diferentes, a escolha do `hero_type` entre os 5 canônicos com StoryBrand e Grunt Test, a decisão de blocks por section e o modelo de apresentação do plano ao membro. Abra nas sub-etapas 1.2 a 1.5.

### 1.2 As sections nascem da narrativa do produto

Vale pros `page_type` que não são `advertorial` nem `listicle` (esses dois seguem o mapa canônico de `reference/page-type.md`, e o `quiz` segue a 1.7). Não existe conjunto padrão de sections nem bloco obrigatório. Monte a sequência a partir da história que este produto precisa contar, nesta ordem de perguntas:

1. **Problema:** que dor ou desejo a pessoa traz, nas palavras da VOC da `market-research`.
2. **Mecanismo:** por que este produto resolve, e por que o que ela já tentou não resolveu.
3. **Prova:** o que torna a promessa crível pra esse nível de ceticismo.
4. **Oferta:** o que ela leva, por quanto, e o que reduz o risco.
5. **Objeções:** o que ainda segura a compra, nas objeções ranqueadas da copy.

Cada pergunta vira uma ou mais sections, ou nenhuma, quando a copy não tem o que dizer ali. Os ids saem do papel da section na narrativa, em kebab-case e em inglês (viram o marker `data-aura-section`).

**Exemplos de section (lista de referência, não menu fechado):**
- `hero`, `offer`, `faq`, `cta-final` — aparecem na maioria das páginas, mas entram porque a narrativa pede, não por padrão
- `trust-bar` — quando tem 3+ selos de autoridade (media, certificação, rating)
- `benefits` — sempre que a copy tem bullets VOC-loaded (quase sempre); peso maior em Stage 4-5 de sophistication
- `mechanism` — **SÓ se o produto tem mecanismo único** (ingrediente patenteado, processo proprietário, inovação). Commodity → PULE (mecanismo forçado parece falso)
- `social-proof` — essencial em alto ceticismo (skincare, saúde, wellness); pular em impulse barato
- `guarantee` — proporcional ao risco percebido (caro/duradouro = section grande; impulse = uma linha)
- `comparison-table` — quando o produto é disruptor numa categoria madura
- `before-after` — cosmético / estético / transformação visual
- `how-it-works` — produtos com 3+ passos de uso
- `ingredients` — skincare / supplements / food
- `specs` — bloco de especificações objetivas (materiais/ingredientes com dosagem, dimensões/peso, quantidade por unidade, certificações, modo de uso). Recomendado em TODA pdp: agentes de compra AI (ChatGPT/Perplexity shopping) decidem lendo specs e dados estruturados, não copy sensorial — sem esse bloco a página fica invisível pra esse tráfego. A copy vem da seção `## Specs` da `copy-engine` (`dados.json.specs[]`) (fatos verificáveis, sem adjetivos); a skill `agentic-readiness` audita depois, junto da camada GEO/Schema.org que a `page-build` injeta
- `founder-story` — DTC com narrativa de origem forte
- `video-demo` — produto que precisa ver em ação
- `sustainability` — claim ambiental relevante
- `gift-guide` — sazonais / presenteáveis
- `app-embed` — reviews apps (Okendo, Judge.me), subscription widgets

Nomes de section que não estão na lista valem, desde que o papel na narrativa esteja claro no plano.

**Exemplos de planos diferentes:**
> Nootropic premium ($89, Stage 4, alto ceticismo, ingrediente patenteado, Product-Aware): hero → trust-bar → mechanism → benefits → ingredients → social-proof → founder-story → offer → guarantee → faq → cta-final
> Camiseta básica ($25, Stage 2, baixo ceticismo, sem mecanismo, Most-Aware): hero → benefits → offer → social-proof → faq → cta-final

### 1.3 Escolher o `hero_type` dos 5 canônicos

Puxe o framework nomeado: **Hero Sections (5 Types + Selection)** (rode `hero sections 5 types value prop dreamstate problem segment campaign selection`) pra ter os 5 tipos canônicos (value-prop, dreamstate, problem, segment, campaign) e os critérios de seleção. Cruze com **StoryBrand 5 Website Essentials** (rode `StoryBrand five website essentials above the fold offer CTA images of success`) e valide a clareza do topo com o **Grunt Test** (rode `StoryBrand grunt test 5 second clarity hero section three questions`) — o herói tem que passar nos 3 segundos. Escolha 1 hero baseado no `page_type`, awareness, e na natureza do produto (transformação visual vs commodity vs categoria nova). Registre o `hero_type` no strategy block — a direção da ETAPA 3, a construção da ETAPA 4 e a `page-build` usam isso pra dar a direção do hero. Pra advertorial, o "hero" tende a ser editorial (headline + dek + abertura de história); pra landing/pdp, benefit-forward com CTA e proof acima da dobra.

### 1.4 Decidir blocks por section

Pra cada section do plano, decida: monolítica (só settings) ou com blocks; quais blocks universais (heading, paragraph, button_row, eyebrow quando a direção pedir, etc — ver Catálogo na `page-build`), nenhum deles obrigatório, e quais type-specific (benefit_card, pricing_tier, review_card, faq_item...). Isso vira `sections_plan[].blocks` no `page-plan.json`. Não precisa detalhar settings aqui (a `page-build` deriva do HTML) — basta listar os block types que cada section vai ter.

### 1.5 Mostrar o plano ao membro

> "Pro seu produto [X] (awareness [Y] → page_type [Z]), o plano é:
> 1. hero ([hero_type]) — headline + CTA + proof acima da dobra
> 2. mechanism — porque tem [mecanismo real], section importante
> ...
> Seções que NÃO vou incluir: before-after (produto ingestível, não visual), comparison-table (sem concorrente direto).
> Algum ajuste antes de eu desenhar?"

Aguarde confirmação ou ajuste. Só então siga.

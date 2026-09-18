# Page Design · Referência: Brand signals, a cascade unificada até o design-signals.json (ETAPA 2)

> O shape do `design-signals.json`, a leitura do `brand.md` antes de qualquer pergunta, os quatro caminhos da cascade (Refero MCP, screenshot lido por visão, design-clone pra hex exato, gerador de 3 paletas), a prova de paletas na página real com tokens em trio R,G,B, a regra de dois temas e o resumo ao membro. Abra na ETAPA 2.

## ETAPA 2 — BRAND SIGNALS (cascade unificada → `design-signals.json`)

Isto NÃO é a fonte do layout. É só extração de signals (paleta, tipografia, vibe) que vão alimentar QUALQUER rota de design escolhida na ETAPA 3 (a rota 1 desenha com eles; a rota 2 os aplica sobre o esqueleto de layout da página de referência; a rota 3 os usa como o token único que unifica as seções de fontes diferentes). O layout em si vem da rota escolhida na ETAPA 3 — aqui só sai a direção de cor/tipografia/densidade.

Os 4 caminhos convergem TODOS pro MESMO arquivo `workspace/[produto]/page/design-signals.json`:

```json
{
  "source": "refero | screenshot_vision | design_clone | manual",
  "source_detail": "Linear (via Refero) | print da loja X | hex extraído de competitor.com | paleta gerada Verde de Farmácia · harmonia analogous · base apothecary-calm",
  "heading_font": "'Fraunces', Georgia, serif",
  "body_font": "'Inter', -apple-system, sans-serif",
  "palette": {
    "background": "#FDFAF4",
    "surface": "#F5EDE0",
    "foreground": "#231F20",
    "primary": "#D85C4A",
    "on_primary": "#FFF8F1",
    "accent": "#9CAF88",
    "muted": "#B0A99F",
    "border": "#E3DAC9"
  },
  "radius": { "base_px": 12, "pill_px": 1000 },
  "shadow": "subtle | medium | strong",
  "density": "airy | medium | compact"
}
```

Antes de começar, **leia `workspace/[produto]/brand.md` PRIMEIRO** — as skills `setup` (ETAPA 5A) e 01 (etapa SALVAR) criam esse arquivo e prometem ao membro literalmente que "a `page-design` lê esse arquivo na brand discovery e só pergunta o que faltar". O que já estiver preenchido lá (posicionamento, arquétipo/tom, paleta com hex reais, tipografia, do/don'ts) entra DIRETO como brand discovery — não pergunte de novo o que o arquivo já responde (hex reais do brand.md alimentam a paleta dos signals sem cascade). Depois, pergunte em UMA mensagem SÓ o que estiver ausente ou marcado `[preencher]` (estilo visual desejado: minimalist editorial / bold modern / clinical premium / wellness organic / custom; cores da marca se houver, ou "escolhe pra mim"; tem site de referência cujo visual ele curte?). Se `brand.md` não existir, faça a brand discovery mínima completa nessa mesma mensagem única. Use as respostas pra dirigir a cascade.

### Caminho 1 — Refero MCP (preferencial, catálogo curado)

Detecta tools com prefixo `mcp__refero__` na sessão. Se disponíveis, vibe search no catálogo de ~200 design systems premium (Cursor, Linear, Vercel, Notion, Stripe, etc.).

1. Construa a query a partir da brand discovery (ex: "editorial magazine ultralight italic premium" / "modern SaaS clean tech minimal"). Se o membro nomeou um site específico, pule direto pro `refero_get`.
2. `mcp__refero__refero_search(query=<query>, limit=5)` — ou `mcp__refero__refero_get(hostname="<site>.com")` quando nomeou um site.
3. Apresente 2-3 candidatos (nome + 1 frase do `northStar`). Membro escolhe (ou pede mais 3 com search refinada).
4. `chosen = mcp__refero__refero_get(uuid=<id>)` → extrair `chosen.designSystem` (typography + colors role-tagged + spacing + radius). Mapeie pro shape de `design-signals.json`.

Se Refero retorna zero resultados úteis OU o membro não gostou de nenhum, caia pro Caminho 2.

### Caminho 2 — SCREENSHOT → VISÃO (fallback PRIMÁRIO)

Substitui o scraping de computed-styles do design-clone como fallback principal. Imune a Cloudflare, JS pesado, markup bagunçado — exatamente o que faz o scraping travar.

1. Peça ao membro um **print full-page** da loja de referência (qualquer concorrente, mesmo nichado fora do catálogo Refero). OU, se o membro deu uma URL e prefere automatizar, a Aura captura **1 screenshot** via `webapp-testing`/Playwright — SÓ o screenshot, sem extrair DOM:
   ```
   # via skill webapp-testing — navegar à URL, full-page screenshot, salvar em /tmp/ref-[produto].png
   ```
2. **Leia a imagem com visão nativa** (Read tool no PNG, ou o screenshot capturado). Extraia da imagem:
   - Paleta dominante (background, foreground, primary/accent, surfaces) — nomeie em hex aproximado
   - Tipografia (serif vs sans no heading; peso; vibe — editorial / técnica / geométrica)
   - Radius (cantos retos vs arredondados vs pill), profundidade de shadow, densidade (airy vs compact)
3. Preencha `design-signals.json` com `source: "screenshot_vision"`.

> Hex extraído de imagem é aproximado — está OK. São signals de direção, não pixel-exato. A rota de design da ETAPA 3 ajusta pra garantir contraste WCAG e hierarquia.

### Caminho 3 (opcional) — design-clone para hex exato

Só pra quem QUER hex exato de um concorrente nichado e tem o venv do design-clone instalado (skill `setup`). Não é o fallback primário (screenshot→visão é). Se o membro pedir, use o caminho canônico — o wrapper orquestra downloader → analyzer → pattern-extractor e a cascade de captura sozinho (não chame os scripts soltos):

```bash
python3 tools/design-clone/aura_clone.py "URL" --output=/tmp/ref-[produto] --skip-images
```

Leia o bloco `design_system` de `/tmp/ref-[produto]/patterns.json` e **cheque o campo `design_system_source`**: se `"extracted"`, mapeie pro shape do `design-signals.json` com `source: "design_clone"`; se `"defaults_fallback"` (o site não rendeu CSS computado real), **IGNORE o bloco e caia pro próximo caminho** — nada de paleta inventada. Se o modo signals abortar com "engine não extrai computed-styles" (a captura veio do single-file-cli, que não gera computed-styles), ou se Playwright não estiver instalado, pule graciosamente pro Caminho 2 (screenshot→visão) ou pro Caminho 4.

### Caminho 4 — Gerador de 3 paletas (último recurso, e o único que não precisa de referência)

Quando Refero não tem match E o membro não tem print nem URL. Não é mais um menu de 8 presets prontos: a Aura gera **3 paletas candidatas pra ESTE produto**, com o motivo de cada uma, e o membro escolhe vendo a cor aplicada na página real.

1. Peça a descrição livre da vibe se ele quiser dar uma ("editorial sério, low-pressure"), e converta pra hex qualquer cor que ele tenha citado por extenso (tabela de nomes logo abaixo). Isso vira semente, nunca decisão.
2. Rode o gerador:
   ```bash
   python3 .claude/lib/design-presets/palette_engine.py \
     --vertical <supplements|health|beauty|home|relationship|other> \
     --avatar "<core_avatar_line da market-research>" \
     --skepticism <baixo|médio|alto, o ceticismo da market-research> \
     [--seed "#AABBCC,#112233"] [--lang en] [--theme dark]
   ```
   Saem exatamente 3 candidatas: nome curto, o motivo em uma frase (o que aquela família de cor comunica naquela vertical, pra aquele avatar), a relação de matiz declarada (análoga, complementar dividida ou tríade) e a paleta role-tagged inteira, com os trios R,G,B já prontos.
3. O script confere sozinho, antes de imprimir: saturação viva no `primary` e no `accent` (nunca cinza), harmonia que bate com a distância real de matiz, contraste WCAG AA no texto e no texto secundário contra o fundo e contra a superfície dos cartões, e no texto do botão contra o botão, 3:1 na cor de apoio sobre o fundo, e as 3 candidatas distintas entre si. **Paleta que não passa é corrigida ou o script sai com erro** — nenhuma sai com aviso. Se sair com erro, reporte a mensagem e siga pela descrição livre.
4. **Prove as 3 na página real** (bloco abaixo). Nunca peça a escolha por amostra de cor solta.
5. Com a escolha do membro, grave no `design-signals.json`: `source: "manual"`, `source_detail: "paleta gerada [Nome] · harmonia [harmony] · base [base_preset]"` (o preset base precisa aparecer: é por ele que a `page-build` acha os pesos de fonte em `presets.json`), a `palette` inteira da candidata, e `heading_font`, `body_font`, `radius`, `shadow` e `density` **LITERAIS** do bloco `non_color_tokens` dela.

**Os 8 presets continuam vivos como base do gerador, não como menu.** Cada candidata herda de um preset o perfil de claridade e saturação dos neutros, a tipografia e a forma, e troca só o matiz. Não ofereça a lista dos 8 ao membro, e não copie cor de `presets.json` à mão.

Mesma entrada devolve sempre as mesmas 3 candidatas: re-rodar a skill no mesmo produto não troca a paleta debaixo do membro. Se ele pedir ajuste depois de escolher, aplique e registre como `"paleta gerada [Nome] (customizado)"`.

Se o membro passou nomes de cor por extenso (ex: "sage green"), valide via regex de hex `^#([0-9A-Fa-f]{3,8})$` ou converta por nome (sage green `#9CAF88`, dusty rose `#D4A5A5`, off-white `#FDFAF4`, navy `#14213D`, terracotta `#C66B3D`, olive `#6B7040`, etc). Se a cor não for reconhecível, peça o hex.

### Prova de paletas na página real (obrigatória no Caminho 4)

Paleta não se escolhe por swatch (a amostra de cor isolada). Sempre que a cascade deixou mais de uma candidata viva, e no Caminho 4 são sempre 3, gere uma página comparadora self-contained: a MESMA página (ou as 2-3 seções mais representativas: hero, oferta e uma seção escura) renderizada em CADA paleta candidata, com navegação por abas ou âncoras, pro membro decidir VENDO a cor aplicada no contexto real. Ao lado de cada aba, o nome e o motivo daquela candidata, pra escolha ser informada.

A implementação usa o sistema de tokens por snippet: todo valor de cor entra como trio R,G,B (ex: `--tk-bg: 246,245,241` pra um fundo areia, `--tk-ink: 34,34,36` pra um grafite) e é consumido como `rgb(var(--tk-bg))` ou `rgba(var(--tk-bg), .5)`. Trocar a paleta inteira significa trocar 1 bloco de tokens, e o formato em trio dá transparência (alpha) sem duplicar a paleta. No Caminho 4 os blocos saem prontos do gerador (`--format css` devolve um `[data-palette="p1"]` por candidata, com todos os roles): copie os blocos, nunca converta hex a hex na mão. A paleta vencedora vira o `design-signals.json`/`design-tokens.json` normalmente.

**Dois temas, duas paletas:** quando o membro mantém 2 ou mais temas com paletas diferentes (teste A/B de identidade visual), o snippet de tokens é POR-TEMA — as sections são as mesmas, muda só o snippet de paleta de cada tema. A disciplina de push por-tema está na rule `shopify-theme-safety.md`: nunca pushar snippet de paleta em lote genérico (um push amplo leva a paleta de um tema pro outro sem ninguém perceber), conferir o tema alvo antes de cada push, e `--allow-live` exige atenção redobrada porque o tema publicado é a loja no ar.

### Output da ETAPA 2

Salve `design-signals.json` e mostre ao membro um resumo curto:
> "Peguei a vibe [da Linear via Refero / do print da loja X via visão / da paleta [Nome] que você escolheu]:
> - Fontes: **[heading_font]** (títulos) + **[body_font]** (corpo)
> - Paleta: fundo **[background]** · texto **[foreground]** · accent **[primary]**
> - Radius **[radius]px** · shadow **[shadow]** · density **[density]**
> Vou usar isso como direção visual. O layout e a estrutura vêm da sua copy — só a paleta/tipografia é inspirada."

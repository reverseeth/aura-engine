# Design Clone — Aura Engine (ferramenta auxiliar)

**Status:** ferramenta auxiliar usada pela 07a-page-design em **dois cenários distintos**:

1. **Brand signals (caminho 3, opcional):** extrair sinais de paleta/tipografia de um site de referência quando o membro quer **hex exato** e passa um link na **07a-page-design ETAPA 2 (Brand Signals)**. Os signals alimentam o `frontend-design` via `design-signals.json`.
2. **Clone-and-adapt (rota de design recomendada por velocidade):** quando o membro indica uma PDP/landing de concorrente que acha bonita, a 07a captura a **ESTRUTURA** dela (ordem + tipo + layout de cada section) e gera um **esqueleto HTML** vazio que o Claude preenche com a copy/brand/produto do **MEMBRO** (06-copy / 04-offer). Herda a hierarquia de conversão validada, não o conteúdo.

**Em ambos os cenários, nenhum código/copy/imagem/marca do concorrente vai pro tema.** O cenário 1 só extrai signals agregados; o cenário 2 só extrai estrutura (placeholders vazios). Adaptar estrutura + trocar todo o conteúdo é defensável; copiar 1:1 não.

## Posição na cascade de brand signals (07a ETAPA 2)

A skill 07a-page-design ETAPA 2 monta o `design-signals.json` por cascade unificada:

1. **Refero MCP** (`mcp__refero__`) — catálogo curado de ~200 sites premium, preferencial.
2. **Screenshot → visão (fallback PRIMÁRIO)** — o membro tira um print full-page da loja de referência (ou a Aura captura 1 screenshot via Playwright só pro print, sem extrair DOM) e o Claude **lê a imagem com visão nativa** pra extrair paleta/tipografia/vibe. Imune a Cloudflare/JS/markup bagunçado — exatamente o que faz o scraping de computed-styles travar.
3. **design-clone (estes scripts) — caminho 3, opcional** — extração via Playwright dos computed-styles, pra quem quer **hex exato** de um concorrente nichado fora do catálogo Refero (ex: PDPs de skincare/microneedling). Mais frágil (depende do site renderizar limpo), por isso fica abaixo do screenshot→visão.
4. **Manual / 8 presets** — membro descreve a vibe ou escolhe um preset.

## Pré-requisitos

```bash
pip install -r requirements.txt
playwright install chromium
```

## Uso no fluxo da 07a-page-design (cenário de signals)

Quando o membro quer hex exato e passa um site de referência visual na ETAPA 2 (Brand Signals):

```bash
# 1. Baixa a página renderizada
python3 downloader.py "URL" /tmp/ref-<produto>

# 2. Identifica sections (input do extractor)
python3 analyzer.py /tmp/ref-<produto>

# 3. Extrai design_system abstrato (o único output usado)
python3 pattern-extractor.py /tmp/ref-<produto>
```

A 07a-page-design lê apenas o bloco `design_system` de `/tmp/ref-<produto>/patterns.json` (que vira fonte de `design-signals.json`):

```json
{
  "design_system": {
    "typography": { "heading_font": "...", "body_font": "..." },
    "colors": { "background_primary": "#...", "text_primary": "#...", "accents": [...] },
    "shape": { "border_radius_px": 8, "shadow_style": "subtle" },
    "spacing": { "density": "medium", "avg_padding_px": 24 }
  }
}
```

Esse bloco vira input pro `frontend-design` da 07a (signals de cor/tipografia/vibe). O resto do `patterns.json` (sections detectadas) é ignorado — a estrutura da página vem sempre da copy do membro, não do concorrente.

## Scripts

| Script | Papel |
|---|---|
| `downloader.py` | Renderiza página com Playwright, salva HTML/CSS/fontes/imagens + `computed-styles.json` |
| `analyzer.py` | Detecta sections semanticamente — necessário pro pattern-extractor, output ignorado pela 07a |
| `pattern-extractor.py` | **Core do caminho de signals.** Produz `design_system` abstrato (cores, fontes, radius, shadow, density) |
| `liquid-converter.py` | Conversor canônico HTML→Liquid. **NÃO é usado pela 07a** (que só extrai signals); é o conversor obrigatório da **07b-page-build** (compile determinístico). Detalhes no fluxo da 07b. |
| `preview.py` | Renderiza `.liquid` como HTML standalone pra debug |

`pattern-extractor.py` é o único script acionado pela 07a no caminho 3 de signals. O **modo `clone-and-adapt`** do `aura_clone.py` reusa `downloader.py` + `analyzer.py` e monta o esqueleto in-process (não há script separado). `liquid-converter.py` vive no fluxo da 07b, não aqui.

## CLI unificado (`aura_clone.py`)

Orquestra o pipeline inteiro num único comando, com validação de URL/path, error recovery e manifest estruturado.

```bash
python3 aura_clone.py <url> --output=<dir> [--product=<slug>] [--skip-images] [--pattern-only]
```

Exemplo:

```bash
python3 aura_clone.py https://competitor.com/product/x \
    --output=/tmp/ref-mybrand \
    --product=mybrand
```

Estrutura de output:

```
<dir>/
    raw/           HTML, CSS, imagens e computed-styles.json (saída bruta do downloader)
    analysis.json  Saída do analyzer (sections detectadas)
    patterns.json  Saída do pattern-extractor (design_system abstrato)
    manifest.json  URL, timestamp, versão do wrapper, status de cada passo
```

Flags:

| Flag | Efeito |
|---|---|
| `--product=<slug>` | Registra o slug no manifest (não altera processamento). |
| `--skip-images` | Hint para o downloader pular download de assets pesados. |
| `--pattern-only` | Roda o analyzer como pré-requisito mas foca no `patterns.json`. |

Error recovery: se o `downloader` falha, o pipeline aborta. Se o `analyzer` falha, o wrapper emite warning mas tenta o `pattern-extractor` mesmo assim (existem casos em que `sections.json` parcial é suficiente).

## Modo `clone-and-adapt` (esqueleto estrutural pra 07a)

Captura a **ESTRUTURA** de uma URL de referência (ordem + tipo semântico + layout de cada section) e produz um **esqueleto HTML** com sections vazias/placeholder. Esse esqueleto é o ponto de partida da rota *Clone-and-adapt* da 07a-page-design (ETAPA 3): o Claude preenche cada placeholder com a copy/brand/imagens do **membro** (06-copy / 04-offer), gerando `design/page.html`. **Zero copy/imagem/marca do concorrente entra no esqueleto** — só a hierarquia/layout.

```bash
python3 aura_clone.py clone-and-adapt <url> --output=<dir> [--product=<slug>]
```

Exemplo:

```bash
python3 aura_clone.py clone-and-adapt https://competitor.com/products/x \
    --output=/tmp/clone-mybrand \
    --product=mybrand
```

Pipeline interno: `downloader` (renderiza DOM) → `analyzer` (detecta sections) → `skeleton-builder` (in-process, monta o esqueleto). Diferente do modo signals, **não** roda o `pattern-extractor`.

Estrutura de output:

```
<dir>/
    raw/            HTML/CSS/screenshot do concorrente (referência LOCAL, não vai pro tema)
    analysis.json   Sections detectadas (ordem + tipo + layout)
    skeleton.html   ESQUELETO estrutural: placeholders comentados, zero conteúdo do concorrente
    skeleton.json   Mesma estrutura em dados (a 07a/Claude consome este pra preencher)
    manifest.json   URL, timestamp, versão, status de cada passo, clone_mode
```

Cada section do esqueleto vira um `<section class="section-NN-<tipo>" data-semantic data-layout>` com `placeholder-heading`, `placeholder-body`, `placeholder-media` (N slots) e `placeholder-grid` (N cards repetíveis) conforme o layout detectado. O layout coarse é derivado só dos campos estruturais do analyzer (`repeating_pattern` → grid de N colunas; FAQ/steps viram lista vertical) — **nenhum hex, fonte ou texto do concorrente** entra no esqueleto.

**Fallback de screenshot (anti-bot/Cloudflare).** Se o scraping de DOM falha (challenge anti-bot, timeout, 4xx num challenge), o `downloader` captura automaticamente um **screenshot full-page** (`raw/fallback-screenshot.png`) e grava `raw/fallback.json` sinalizando o modo degradado. O `clone-and-adapt` detecta esse caso, não gera esqueleto, e aponta o membro pra **rota screenshot→visão da 07a** (o Claude lê a imagem com visão nativa e reconstrói a estrutura). O manifest registra `"mode": "screenshot_fallback"` e `"skeleton": null`.

## Security

Todos os scripts aplicam validação defensiva antes de qualquer I/O ou fetch de rede:

- **URL allowlist (anti-SSRF).** `validate_url()` em `downloader.py` aceita apenas `http://` / `https://`; bloqueia `file://`, `javascript:`, `data:`, e qualquer host que resolva para ranges privados/loopback (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `::1`, `fc00::/7`, `fe80::/10`).
- **Path validation (anti path-traversal).** Outputs são resolvidos e verificados contra uma allowlist: `$TMPDIR`, `$HOME/aura-engine/workspace`, e o diretório corrente (`cwd`). Paths fora disso levantam `ValueError` antes de qualquer write.
- **Write atômico para imagens.** `download_image` escreve em `<hash>.tmp` e faz `os.replace()` pra evitar race conditions entre checar-existe e gravar.
- **Schema Shopify validado.** `liquid-converter.py` roda `validate_shopify_schema()` antes de serializar: IDs únicos, tipos válidos (`text`, `inline_richtext`, `richtext`, `image_picker`, `color`, `range`, `select`, `checkbox`, `number`, `url`, `textarea`, `header`, `paragraph`), `label` obrigatório exceto em `header`/`paragraph`.
- **XSS / Liquid-injection guard.** Defaults textuais passam por `html.escape` e têm `{{ }}` / `{% %}` escapados pra não quebrar parsing Liquid downstream.

## Troubleshooting

| Sintoma | Causa provável | Ação |
|---|---|---|
| `downloader.py` trava em `networkidle` | Site JS-heavy ou trackers lentos | Script faz fallback automático `networkidle → load → domcontentloaded`. Se ainda timeout, tente novamente (Cloudflare pode estar emitindo challenge). |
| `URL demorou demais ou é JS-heavy; tente outra` | Timeout global (60s) esgotado | Verifique se o site carrega manualmente; considere aumentar `NAVIGATION_TIMEOUT_MS` em `downloader.py`. |
| `ERRO: Host resolve para IP privado/loopback` | URL aponta pra host interno (SSRF prevention) | Use apenas URLs públicas. Para desenvolvimento local use mock server com domínio público falso. |
| `ERRO: Path fora da allowlist` | Output path não resolve em `$TMPDIR`, `$HOME/aura-engine/workspace`, ou `cwd` | Escolha destino dentro da allowlist ou rode a partir do diretório desejado. |
| Cloudflare challenge / 403 | Proteção anti-bot ativa | No modo `clone-and-adapt`, o downloader cai automaticamente no fallback de screenshot full-page (`raw/fallback-screenshot.png`) → siga pela rota screenshot→visão da 07a. No modo signals, tente User-Agent diferente ou intervenção manual. |
| `clone-and-adapt` retorna `skeleton: null` no manifest | DOM scraping falhou; só o screenshot ficou disponível | Esperado em sites com anti-bot forte. Use `raw/fallback-screenshot.png` na rota screenshot→visão (Claude lê a imagem e reconstrói a estrutura). |
| `playwright install chromium` falhou | Falta de deps no OS | Siga [docs oficiais do Playwright](https://playwright.dev/python/docs/browsers) para deps nativas. |
| `patterns.json` sem accents | Site com fundo/texto quase-branco puro | Fix em `is_vivid()` filtra branco puro (`> 240,> 240`); se mesmo assim vazio, o site não tem cor acento proeminente. |
| Liquid gerado quebra no theme editor | Schema inválido ou escape ausente | A validação `validate_shopify_schema()` deve pegar. Se passar e quebrar no editor, abra issue com schema em anexo. |

## Princípios

- **Zero código do concorrente no output final.** A 07a só extrai signals agregados (paleta + fontes + tokens); o HTML/CSS da página é gerado fresh via `frontend-design`.
- **Theme-agnostic.** Sections geradas no fluxo storefront têm namespacing próprio (`page-<produto>-<tipo>`), zero dependência do tema pai.
- **Validação obrigatória.** Toda section .liquid gerada passa pela skill `shopify-plugin:shopify-liquid` antes de instalar no tema.

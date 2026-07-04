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

## Cascade de CAPTURA (como o `aura_clone.py` obtém o DOM)

Independente do modo (signals ou clone-and-adapt), a captura segue esta ordem:

1. **`downloader.py`** — Playwright headless **com stealth** (mesmo init-script do `fetch.py` da lib web-fetch). Único caminho que extrai `computed-styles.json` (fidelidade máxima pro design_system).
2. **`snapshot.py`** — wrapper do `single-file-cli` (SingleFile). Entra automaticamente quando o downloader não consegue DOM (`--engine=auto`, default). Produz HTML self-contained; o wrapper promove a versão AI-readable pra `page.html` e o pipeline segue. **Atenção:** essa engine não extrai computed-styles — serve pro **clone-and-adapt** (estrutura); no modo **signals** o pipeline falha honesto (o pattern-extractor recusa gerar design_system sem CSS computado real — nada de paleta inventada).
3. **Screenshot-fallback** — o downloader salva `raw/fallback-screenshot.png` pra rota screenshot→visão da 07a. Se o screenshot capturou uma **página de challenge** (Cloudflare/Turnstile), o `fallback.json` marca `challenge_detected: true` e o wrapper avisa que ele NÃO serve pra rota visão.
4. **MANUAL (vence Cloudflare/login):** o membro instala a [extensão SingleFile](https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle) no Chrome dele, abre a página normalmente, clica no ícone da extensão (1 clique salva o .html completo em Downloads) e entrega o arquivo. A Aura ingere com `aura_clone.py --from-file=<arquivo.html>` — mesmo pipeline, browser real do membro, imune a anti-bot.

## Pré-requisitos

Em macOS/Linux modernos o `pip install` direto falha (PEP 668, "externally-managed-environment") — use venv:

```bash
cd tools/design-clone
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium
```

(a skill 00-setup faz isso automaticamente)

**Bootstrap automático (não precisa ativar o venv):** todos os entry-points (`aura_clone.py`, `downloader.py`, `analyzer.py`, `pattern-extractor.py`, `liquid-converter.py`) usam o mesmo padrão de re-exec do `fetch.py` da lib web-fetch — se o `python3` do sistema não tiver as deps, o script se re-executa sozinho no `.venv` (deste diretório, com fallback pro venv da web-fetch). Ou seja: `python3 aura_clone.py ...` direto FUNCIONA, desde que o venv exista. Sem venv nenhum, os scripts degradam graciosamente (ingestão `--from-file` segue funcionando; os passos que precisam de browser/bs4 imprimem o comando de setup).

**Opcional — captura via SingleFile (`snapshot.py` com URL):** precisa de Node.js >= 20 (`brew install node`). O `single-file-cli` baixa on-demand via `npx -y -p single-file-cli`; instalação global opcional: `npm install -g single-file-cli`. A **ingestão de arquivo local** (`--from-file`) não precisa de Node nem de browser.

## Uso no fluxo da 07a-page-design (cenário de signals)

Quando o membro quer hex exato e passa um site de referência visual na ETAPA 2 (Brand Signals), o caminho canônico é o wrapper (orquestra os 3 passos e a cascade de captura):

```bash
python3 aura_clone.py "URL" --output=/tmp/ref-<produto>
```

Os 3 passos que rodam por baixo (só pra debug individual — no modo signals o analyzer é OPCIONAL: o pattern-extractor lê direto o `computed-styles.json` e não requer `sections.json`):

```bash
# 1. Baixa a página renderizada
python3 downloader.py "URL" /tmp/ref-<produto>

# 2. Identifica sections (opcional no modo signals — só agrega contexto; obrigatório no clone-and-adapt)
python3 analyzer.py /tmp/ref-<produto>

# 3. Extrai design_system abstrato (o único output usado — lê o computed-styles.json)
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

Esse bloco vira input pro `frontend-design` da 07a (signals de cor/tipografia/vibe). O resto do `patterns.json` é ignorado — a estrutura da página vem sempre da copy do membro, não do concorrente.

## Scripts

| Script | Papel |
|---|---|
| `downloader.py` | Renderiza página com Playwright **stealth**, salva HTML/CSS/fontes/imagens + `computed-styles.json` + `meta.json`. Recupera stylesheets cross-origin via fetch do próprio contexto do browser. |
| `snapshot.py` | Snapshot fiel via `single-file-cli` (subprocess — AGPL, nunca vendorizado) OU ingestão de .html salvo pela extensão SingleFile. Gera `ref.full.html` + `ref.ai.html`. |
| `analyzer.py` | Detecta sections semanticamente (atravessa o wrapper `<main>` de temas Shopify; match de hints por token, não substring) — input obrigatório do skeleton-builder (clone-and-adapt); no modo signals é opcional (só agrega o `analysis.json` de contexto) |
| `pattern-extractor.py` | **Core do caminho de signals.** Produz `design_system` abstrato (cores, fontes, radius, shadow, density). Input único: o `computed-styles.json` do downloader — não requer o analyzer |
| `liquid-converter.py` | Conversor canônico HTML→Liquid. **NÃO é usado pela 07a** (que só extrai signals); é o conversor obrigatório da **07b-page-build** (compile determinístico). Detalhes no fluxo da 07b. |
| `preview.py` | Renderiza `.liquid` como HTML standalone pra debug |

O **modo `clone-and-adapt`** do `aura_clone.py` reusa a captura + `analyzer.py` e monta o esqueleto in-process (não há script separado). `liquid-converter.py` vive no fluxo da 07b, não aqui.

## CLI unificado (`aura_clone.py`)

Orquestra o pipeline inteiro num único comando, com validação de URL/path, cascade de captura, error recovery e manifest estruturado.

```bash
python3 aura_clone.py <url> --output=<dir> [--product=<slug>]
                      [--engine=auto|downloader|singlefile]
                      [--skip-images] [--pattern-only]

# Ingestão manual (arquivo salvo pela extensão SingleFile do membro):
python3 aura_clone.py --from-file=<arquivo.html> --output=<dir>
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
    raw/           HTML, CSS, imagens e computed-styles.json (saída bruta da captura)
    analysis.json  Saída do analyzer (sections detectadas)
    patterns.json  Saída do pattern-extractor (design_system abstrato)
    manifest.json  URL, timestamp, versão do wrapper, engine usada, status de cada passo
```

Flags:

| Flag | Efeito |
|---|---|
| `--product=<slug>` | Registra o slug no manifest (não altera processamento). |
| `--engine=auto\|downloader\|singlefile` | Engine de captura. `auto` (default) = downloader com fallback automático pro single-file-cli; `downloader` = só Playwright; `singlefile` = só single-file-cli (sem computed-styles — serve pro clone-and-adapt; no modo signals não gera patterns.json). |
| `--from-file=<path>` | Ingere um .html local já salvo (extensão SingleFile do membro). Dispensa a URL e não precisa de browser/Node. |
| `--skip-images` | Pula o download de imagens (`AURA_SKIP_IMAGES=1` pro downloader) — mais rápido quando só os signals interessam. |
| `--pattern-only` | Pula o analyzer e gera só o `patterns.json` (o pattern-extractor lê direto o `computed-styles.json` — não requer `sections.json`). |

Error recovery: o wrapper LIMPA outputs derivados de runs anteriores no mesmo `--output` antes de começar (`fallback.json`, `sections.json`, `patterns.json` velhos — um retry pós-bloqueio não herda estado stale). Se a captura falha em todas as engines automatizadas, o wrapper aborta com a rota screenshot→visão ou manual (ver Fallbacks). Se o `analyzer` falha: no modo **clone-and-adapt** o pipeline aborta com mensagem clara (sem sections não há esqueleto); no modo **signals** o wrapper avisa e segue sem `analysis.json` — o `pattern-extractor` lê direto o `computed-styles.json` e não depende dele.

Exit codes do wrapper: `0` sucesso (output final existe), `1` input inválido, `2` pipeline incompleto (ver manifest/stderr).

## `snapshot.py` (SingleFile — snapshot fiel + ingestão manual)

Wrapper subprocess do [`single-file-cli`](https://github.com/gildas-lormeau/single-file-cli) (licença AGPL — por isso é sempre invocado como processo externo via npx/binário, nunca vendorizado no repo). Reusa o Chromium que o Playwright já instala (zero download extra de browser).

```bash
# Captura de URL (precisa de Node >= 20; single-file-cli baixa on-demand via npx)
python3 snapshot.py "https://competitor.com/products/x" --output /tmp/sf-mybrand

# Ingestão de arquivo salvo pela extensão SingleFile (não precisa de Node)
python3 snapshot.py ~/Downloads/pagina-salva.html --output /tmp/sf-mybrand
```

Gera SEMPRE 2 arquivos + resumo:

```
<dir>/
    ref.full.html   Verdade visual imutável (14MB+ em loja real, linhas de ~1M chars)
    ref.ai.html     Versão AI-readable (data-URIs stripped, linhas re-quebradas)
    snapshot.json   Fonte, ferramenta, timestamp, bytes de cada versão
```

**Protocolo de leitura (obrigatório — a IA nunca lê o snapshot cru):**

1. `ref.full.html` é **verdade visual, nunca input de leitura**: o membro abre no browser; a Aura só o usa renderizando `file://` pra screenshot (rota visão). Ler cru estoura contexto e o Read trunca linhas gigantes (corrompe o que a IA vê).
2. `ref.ai.html` tem os data-URIs base64 e SVGs url-encoded trocados por placeholders `data:image/STRIPPED` e linhas re-quebradas — mas mesmo ele é lido **sempre segmentado**: grep por marcos (`<section`, `<h1`, classes de section) + Read com offset/limit nos trechos-alvo, ou extração programática (analyzer/pattern-extractor).
3. `ref.ai.html` NÃO é verdade visual (whitespace alterado pelo rewrap) — pra aprovação visual, sempre `ref.full.html` no browser.

Exit codes: `0` ok · `1` input/output inválido · `2` captura/pós-processamento falhou · `3` Chromium do Playwright não encontrado (`playwright install chromium`, ou env `AURA_CHROMIUM` apontando um Chrome) · `6` single-file-cli indisponível (sem npx/node — imprime o setup e a alternativa manual).

**Rota manual pro membro não-técnico (1 clique, vence Cloudflare/login):**

1. Instalar a extensão SingleFile no Chrome: <https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle>
2. Abrir a página do concorrente normalmente (logado, challenge resolvido — é o browser real).
3. Clicar no ícone da extensão — ela salva um único .html completo em Downloads.
4. Entregar o arquivo à Aura: `python3 aura_clone.py --from-file=~/Downloads/<arquivo>.html --output=/tmp/clone-<produto>` (ou arrastar o arquivo pro chat).

O arquivo salvo é referência de concorrente = material de trabalho do membro — vive em `workspace/`/`tmp`, **jamais é commitado** (rule 11 do CLAUDE.md).

## Modo `clone-and-adapt` (esqueleto estrutural pra 07a)

Captura a **ESTRUTURA** de uma URL de referência (ordem + tipo semântico + layout de cada section) e produz um **esqueleto HTML** com sections vazias/placeholder. Esse esqueleto é o ponto de partida da rota *Clone-and-adapt* da 07a-page-design (ETAPA 3): o Claude preenche cada placeholder com a copy/brand/imagens do **membro** (06-copy / 04-offer), gerando `design/page.html`. **Zero copy/imagem/marca do concorrente entra no esqueleto** — só a hierarquia/layout.

```bash
python3 aura_clone.py clone-and-adapt <url> --output=<dir> [--product=<slug>]

# Ou a partir do arquivo salvo pela extensão SingleFile:
python3 aura_clone.py clone-and-adapt --from-file=<arquivo.html> --output=<dir>
```

Pipeline interno: captura (cascade downloader → singlefile → screenshot) → `analyzer` (detecta sections) → `skeleton-builder` (in-process, monta o esqueleto). Diferente do modo signals, **não** roda o `pattern-extractor`.

Estrutura de output:

```
<dir>/
    raw/            HTML/CSS/screenshot do concorrente (referência LOCAL, não vai pro tema)
    analysis.json   Sections detectadas (ordem + tipo + layout)
    skeleton.html   ESQUELETO estrutural: placeholders comentados, zero conteúdo do concorrente
    skeleton.json   Mesma estrutura em dados (a 07a/Claude consome este pra preencher)
    manifest.json   URL, timestamp, versão, engine, status de cada passo, clone_mode
```

Cada section do esqueleto vira um `<section class="section-NN-<tipo>" data-semantic data-layout>` com `placeholder-heading`, `placeholder-body`, `placeholder-media` (N slots) e `placeholder-grid` (N cards repetíveis) conforme o layout detectado. O layout coarse é derivado só dos campos estruturais do analyzer (`repeating_pattern` → grid de N colunas; FAQ/steps viram lista vertical) — **nenhum hex, fonte ou texto do concorrente** entra no esqueleto.

## Fallbacks (anti-bot/Cloudflare)

Se o scraping de DOM falha (challenge anti-bot, timeout, 4xx), o fluxo degrada em ordem:

1. **single-file-cli** (`--engine=auto`): o wrapper tenta o `snapshot.py` automaticamente — motor de captura diferente, mesma máquina.
2. **Screenshot full-page**: o `downloader` salva `raw/fallback-screenshot.png` + `raw/fallback.json`. O wrapper não gera esqueleto/patterns e aponta o membro pra **rota screenshot→visão da 07a**. O manifest ganha `"mode": "screenshot_fallback"` (top-level) e `"skeleton": null`.
3. **Challenge detectado**: antes de aceitar o screenshot, o downloader confere se a tela é o interstitial ("Just a moment…", Turnstile) e espera até ~14s pelo auto-resolve. Se persistir, `fallback.json` ganha `challenge_detected: true`, o exit code do downloader é `5` e o wrapper avisa que o screenshot **não serve** pra rota visão — a saída é a rota manual (extensão SingleFile + `--from-file`).

Exit codes do `downloader.py`: `0` DOM completo · `1` erro fatal/deps · `3` fallback com screenshot utilizável · `4` nem screenshot saiu · `5` screenshot é página de challenge.

## Security

Todos os scripts aplicam validação defensiva antes de qualquer I/O ou fetch de rede:

- **URL allowlist (anti-SSRF).** `validate_url()` em `downloader.py` aceita apenas `http://` / `https://`; bloqueia `file://`, `javascript:`, `data:`, e qualquer host que resolva para ranges privados/loopback (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `::1`, `fc00::/7`, `fe80::/10`). No download de imagens, **cada hop de redirect é revalidado** (um 302 pra host interno é bloqueado). **Limitação conhecida:** redirects seguidos pelo Playwright durante a navegação principal não são revalidados — a validação cobre a URL inicial e os fetches auxiliares.
- **Path validation (anti path-traversal).** Outputs são resolvidos e verificados contra uma allowlist: `$TMPDIR`, `/tmp`, `<repo>/workspace` (derivado da posição real do repo, não assume `~/aura-engine`), o layout legado `$HOME/aura-engine/workspace`, e o `cwd` **apenas quando está dentro do repo**. Paths fora disso levantam `ValueError` antes de qualquer write.
- **Write atômico para imagens.** `download_image` escreve em `.tmp` e faz `os.replace()` — nunca fica meio-arquivo no disco.
- **AGPL isolado.** `single-file-cli` roda exclusivamente como subprocess externo (npx/binário global); nenhum código dele entra neste repo.
- **Schema Shopify validado.** `liquid-converter.py` roda `validate_shopify_schema()` antes de serializar: IDs únicos, tipos válidos (`text`, `inline_richtext`, `richtext`, `image_picker`, `color`, `range`, `select`, `checkbox`, `number`, `url`, `textarea`, `header`, `paragraph`), `label` obrigatório exceto em `header`/`paragraph`.
- **XSS / Liquid-injection guard.** Defaults textuais passam por `html.escape` e têm `{{ }}` / `{% %}` escapados pra não quebrar parsing Liquid downstream.

## Troubleshooting

| Sintoma | Causa provável | Ação |
|---|---|---|
| `downloader.py` trava em `networkidle` | Site JS-heavy ou trackers lentos | Script faz fallback automático `networkidle → load → domcontentloaded`. Se ainda timeout, o wrapper cai pro single-file-cli e depois pro screenshot. |
| Scroll "não termina" em página com feed infinito | Lazy append re-estica o scrollHeight | O scroll tem teto duplo (120 passos / 45s de relógio) — trunca, loga `scroll truncado em Xpx` e segue com o que carregou. |
| `ERRO: Host resolve para IP privado/loopback` | URL aponta pra host interno (SSRF prevention) | Use apenas URLs públicas. Para desenvolvimento local use mock server com domínio público falso. |
| `ERRO: Path fora da allowlist` | Output path não resolve em `/tmp`, `$TMPDIR`, `<repo>/workspace` (ou cwd dentro do repo) | Escolha destino dentro da allowlist. |
| Cloudflare challenge / 403 | Proteção anti-bot ativa | Cascade automática: stealth → single-file-cli → screenshot. Se o `fallback.json` marcar `challenge_detected: true`, o screenshot é o interstitial (inútil pra visão) — use a rota manual: extensão SingleFile + `--from-file`. |
| Site bloqueia mesmo com stealth | Fingerprint de headless detectada | Tente `--engine=singlefile`; sobrescreva o UA com env `AURA_UA="<UA do seu Chrome>"`; último recurso = rota manual (extensão). |
| `clone-and-adapt` retorna `skeleton: null` no manifest | DOM falhou em todas as engines; só o screenshot ficou | Esperado em anti-bot forte. Screenshot ok → rota screenshot→visão; `challenge_detected` → rota manual. |
| `snapshot.py` sai com código 6 | Node/npx ausentes | `brew install node` (ou use a ingestão local `--from-file`, que não precisa de Node). |
| `snapshot.py` sai com código 3 | Chromium do Playwright ausente | `playwright install chromium` ou env `AURA_CHROMIUM=<path do Chrome>`. |
| `playwright install chromium` falhou | Falta de deps no OS | Siga [docs oficiais do Playwright](https://playwright.dev/python/docs/browsers) para deps nativas. |
| `patterns.json` sem accents | Site com fundo/texto quase-branco puro | Fix em `is_vivid()` filtra branco puro (`> 240,> 240`); se mesmo assim vazio, o site não tem cor acento proeminente. |
| Modo signals aborta com "engine não extrai computed-styles" | Captura veio do single-file-cli/--from-file | Esperado — o pattern-extractor exige CSS computado real (anti-alucinação). Pra signals, rode `--engine=downloader`; pra paleta quando o site bloqueia, use a rota screenshot→visão. A captura serve pro clone-and-adapt. |
| Liquid gerado quebra no theme editor | Schema inválido ou escape ausente | A validação `validate_shopify_schema()` deve pegar. Se passar e quebrar no editor, abra issue com schema em anexo. |

## Princípios

- **Zero código do concorrente no output final.** A 07a só extrai signals agregados (paleta + fontes + tokens) ou o esqueleto estrutural com placeholders vazios (clone-and-adapt); o HTML da página nasce da rota de design escolhida na 07a, sempre com copy/imagens/marca 100% do membro. No `liquid-converter.py`, o único caminho que injetaria markup da página de origem no tema (Modo B legacy, `--sections-json`) é **BLOQUEADO por default** e exige `--allow-competitor-markup` — permitido só quando a página de origem é PRÓPRIA do membro.
- **A IA nunca lê snapshot cru.** `ref.full.html` é verdade visual (browser/screenshot); leitura sempre via `ref.ai.html` segmentado ou extração programática.
- **Theme-agnostic.** Sections geradas no fluxo storefront têm namespacing próprio (`page-<produto>-<tipo>`), zero dependência do tema pai.
- **Validação obrigatória.** Toda section .liquid gerada passa pela skill `shopify-plugin:shopify-liquid` antes de instalar no tema.

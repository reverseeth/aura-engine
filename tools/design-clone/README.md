# Design Clone — Aura Engine (ferramenta auxiliar)

**Status:** ferramenta auxiliar, não pipeline principal. A skill 06 (page-engine) gera páginas Shopify do zero a partir da copy — não clona design de concorrente. Estes scripts existem pra um único caso: **extrair sinais de paleta/tipografia de um site de referência** quando o membro passa um link na Etapa 2.1 (Brand Discovery) da skill 06. Os signals alimentam os specialists `designer-color-system` e `designer-typography-scale`. Nenhum código do concorrente vai pro tema.

## Pré-requisitos

```bash
pip install -r requirements.txt
playwright install chromium
```

## Uso no fluxo da skill 06 (único cenário suportado)

Quando o membro passa um site de referência visual na Etapa 2.1:

```bash
# 1. Baixa a página renderizada
python3 downloader.py "URL" /tmp/ref-<produto>

# 2. Identifica sections (input do extractor)
python3 analyzer.py /tmp/ref-<produto>

# 3. Extrai design_system abstrato (o único output usado)
python3 pattern-extractor.py /tmp/ref-<produto>
```

A skill 06 lê apenas o bloco `design_system` de `/tmp/ref-<produto>/patterns.json`:

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

Esse bloco vira input pros specialists de design na Etapa 3. O resto do `patterns.json` (sections detectadas) é ignorado — a estrutura da página vem sempre da copy do membro, não do concorrente.

## Scripts

| Script | Papel no fluxo atual |
|---|---|
| `downloader.py` | Renderiza página com Playwright, salva HTML/CSS/fontes/imagens + `computed-styles.json` |
| `analyzer.py` | Detecta sections semanticamente — necessário pro pattern-extractor, output ignorado pela skill |
| `pattern-extractor.py` | **Core.** Produz `design_system` abstrato (cores, fontes, radius, shadow, density) |
| `liquid-converter.py` | Legacy. Converte HTML (scraped ou fresh) em Liquid section. NÃO é usado pela skill 06 — ela gera Liquid direto via `frontend-design` + schema mapping próprio |
| `preview.py` | Legacy. Renderiza `.liquid` como HTML standalone pra debug |

Os scripts legacy (`liquid-converter.py`, `preview.py`) continuam funcionais pra quem quiser cenários avançados de clone literal fora do fluxo padrão, mas **não são acionados pela skill 06**.

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
| Cloudflare challenge / 403 | Proteção anti-bot ativa | Tente User-Agent diferente; algumas páginas exigem intervenção manual. O script aborta em resposta `>= 400` (exceto redirects). |
| `playwright install chromium` falhou | Falta de deps no OS | Siga [docs oficiais do Playwright](https://playwright.dev/python/docs/browsers) para deps nativas. |
| `patterns.json` sem accents | Site com fundo/texto quase-branco puro | Fix em `is_vivid()` filtra branco puro (`> 240,> 240`); se mesmo assim vazio, o site não tem cor acento proeminente. |
| Liquid gerado quebra no theme editor | Schema inválido ou escape ausente | A validação `validate_shopify_schema()` deve pegar. Se passar e quebrar no editor, abra issue com schema em anexo. |

## Princípios

- **Zero código do concorrente no output final.** A skill 06 só extrai signals agregados (paleta + fontes + tokens); o HTML/CSS da página Shopify é gerado fresh via `frontend-design`.
- **Theme-agnostic.** Sections geradas pela skill 06 têm namespacing próprio (`page-<produto>-<tipo>`), zero dependência do tema pai.
- **Validação obrigatória.** Toda section .liquid gerada passa pela skill `shopify-plugin:shopify-liquid` antes de instalar no tema.

# Design Clone — Aura Engine (ferramenta auxiliar)

Duas ferramentas de storefront e o venv delas:

1. **`downloader.py --mode bands`:** o capturador do **modo referência** da `page-design` (ETAPA 4). Divide uma página em faixas e grava a geometria, os estilos, os textos e os assets de cada uma, por largura. Alimenta o `tools/page-qa/geodiff.py` (a página do membro segue a geometria da referência?) e o `tools/page-qa/legal_check.py` (sobrou texto, asset, fonte ou marca da referência?). Também captura o próprio `page.html` do membro, por `file://`.
2. **`liquid-converter.py`:** o compilador da `page-build`. Converte o HTML aprovado na `page-design` em sections Liquid editáveis, por código.

Da referência sai só geometria, nunca copy, imagem, logo, fonte ou claim: a regra está em `.claude/skills/page-design/reference/modo-referencia.md`.

## Pré-requisitos

Playwright, bs4 e requests num venv próprio (o Python moderno é externally-managed, PEP 668):

```bash
python3 -m venv tools/design-clone/.venv
tools/design-clone/.venv/bin/pip install -r tools/design-clone/requirements.txt
tools/design-clone/.venv/bin/playwright install chromium
```

**Bootstrap automático:** os scripts fazem re-exec no venv (`_venv_bootstrap.py`), então `python3 tools/design-clone/downloader.py ...` direto funciona com o venv criado. O mesmo venv serve de reserva para o fetcher `.claude/lib/web-fetch/fetch.py`, que usa o `lxml` daqui.

## `downloader.py`

```bash
# modo referência: faixas em 1440 e 390
python3 tools/design-clone/downloader.py <url> workspace/<slug>/page/reference-capture/<n>/ --mode bands [--widths 1440,390]

# a página do próprio membro, para o geodiff
python3 tools/design-clone/downloader.py "file://$PWD/workspace/<slug>/page/design/page.html" workspace/<slug>/page/reference-capture/page/ --mode bands
```

Saída por largura, em `<out>/<largura>/`:

| Arquivo | O que tem |
|---|---|
| `bands.json` | Uma faixa por filho de primeiro nível com mais de 120px: índice, tag, seletor, topo, altura, fundo, `aura_section` (na página do membro), colunas e as caixas de texto, mídia e CTA normalizadas pela largura |
| `section-NN.json` | Estilos computados de cada faixa |
| `texts.json` | Todo texto visível |
| `assets.json` | Todo `src`, `srcset` e `url()` |

`--mode full` (padrão antigo) ainda captura o HTML renderizado, o CSS computado e os assets, mas nenhuma skill o usa hoje.

**Exit codes:** `0` ok · `1` erro fatal (dependência, URL ou caminho inválido) · `2` o `robots.txt` proíbe a captura · `3` HTTP de erro, só o screenshot saiu · `4` nem o screenshot saiu · `5` página de challenge (Cloudflare, Turnstile). Em 2, 3 e 5 a `page-design` oferece o modo direção.

## `liquid-converter.py`

Uso, padrões que aplica e limites em `.claude/skills/page-build/reference/split-e-compile.md` e `.claude/skills/page-build/reference/padroes-do-conversor.md`. Resumo:

```bash
python3 tools/design-clone/liquid-converter.py --batch <staging>/batch-manifest.json --emit-template-json <staging>/templates/page.<slug>.json
```

- `design_tokens` no manifest (ou `--design-tokens`): o hex de cada papel de cor vira o setting `color_<papel>`, com rótulo em português no editor ("Cor primária"); o resto continua `color_N`.
- `theme_dir` no manifest (ou `--theme-dir`): seção que já está no tema com `color_N` mantém os ids, para o membro não perder o que editou.
- Irmãos repetidos só viram block quando têm a mesma estrutura interna; irmãos diferentes ficam como settings da seção, sem perder copy.

## Módulos de apoio

| Arquivo | O que faz |
|---|---|
| `_css_utils.py` | `rewrite_css_for_namespace` (namespacing do CSS de cada section) e `CSS_COLOR_LITERAL_RE` (o `tokens.py` conta cores soltas com ele) |
| `_venv_bootstrap.py` | Re-exec no venv que tem as dependências |

## Segurança

- **URL allowlist (anti-SSRF).** `validate_url()` aceita só `http://` e `https://` e bloqueia hosts que resolvem para ranges privados ou loopback. `file://` só no modo `bands` e só dentro da allowlist de caminhos.
- **`robots.txt`.** O modo `bands` checa o `robots.txt` (stdlib `urllib.robotparser`) antes de capturar e sai com 2 se ele proibir.
- **Path validation (anti path-traversal).** Saídas resolvidas e conferidas contra a allowlist: `$TMPDIR`, `/tmp` e `<repo>/workspace`.
- **Schema Shopify validado.** O `liquid-converter.py` roda `validate_shopify_schema()` antes de serializar.
- **Liquid-injection guard.** Defaults textuais passam por `html.escape`, com `{{ }}` e `{% %}` escapados.
- **Capturas são locais.** Tudo em `page/reference-capture/` fica no `workspace/`, que nunca é commitado.

## Troubleshooting

| Sintoma | Causa provável | Ação |
|---|---|---|
| `downloader.py` trava em `networkidle` | Site JS-heavy ou trackers lentos | Fallback automático `networkidle → load → domcontentloaded` |
| Exit 5 | Challenge anti-bot | Outra URL de referência ou o modo direção |
| `ERRO: Host resolve para IP privado/loopback` | URL interna (SSRF) | Só URLs públicas |
| `ERRO: Path fora da allowlist` | Saída fora de `/tmp`, `$TMPDIR` ou `<repo>/workspace` | Escolha destino dentro da allowlist |
| `playwright install chromium` falhou | Dependências do sistema | [Docs do Playwright](https://playwright.dev/python/docs/browsers) |
| Liquid quebra no theme editor | Schema inválido ou escape ausente | Valide com a skill `shopify-plugin:shopify-liquid`; se passar e quebrar, abra issue com o schema |

## Princípios

- **Zero código da página de origem no output final.** A referência dá geometria; o HTML nasce na `page-design` com o conteúdo do membro, e o `legal_check.py` confere.
- **Theme-agnostic.** Sections geradas têm namespacing próprio (`page-<produto>-<tipo>`), zero dependência do tema pai.
- **Validação obrigatória.** Toda section `.liquid` gerada passa pela skill `shopify-plugin:shopify-liquid` antes de instalar no tema.

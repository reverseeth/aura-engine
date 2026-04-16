---
name: page-deploy
description: Cria o template JSON da página com blocks pré-populados, valida (blocks não-vazios, block_order consistente, types válidos), faz deploy seguro no Shopify (duplicate → pull → cp → push --nodelete), gera preview URLs + report machine-readable. Terceira e última skill da cadeia Page Engine. Invoque depois de `page-sections`.
---

# Page Deploy — ETAPAS 9-11

Esta é a **terceira** das 3 skills da cadeia Page Engine modularizada. Ela:

1. Valida que `page-sections` rodou e que shopify-cli está instalado
2. Cria o `templates/page.[produto].json` com blocks **pré-populados com copy real**
3. Roda validação OBRIGATÓRIA de blocks (não-vazios, block_order consistente, types válidos)
4. Faz deploy safe no Shopify: duplicate → pull → cp → push --nodelete
5. Gera report humano (.md) + machine-readable (.json)
6. Suporta iteration loop (ajustes sem regenerar do zero)

## Pré-flight

Valide antes de qualquer ação:

### Skill anterior
- [ ] `/workspace/[produto]/06-page/06-plan.json` existe e é parseável
- [ ] `/workspace/[produto]/06-page/06-sections-report.md` existe
- [ ] `/workspace/[produto]/manifest.json` tem `06b-page-sections` em `skills_completed`
- [ ] `<staging>/sections/page-[produto]-*.liquid` tem ao menos 1 arquivo

### Shopify CLI
```bash
which shopify && shopify --version
```

- Se **não instalado**, mostre instruções específicas por plataforma:
  ```
  # macOS (Homebrew)
  brew tap shopify/shopify && brew install shopify-cli
  
  # Cross-platform (npm)
  npm i -g @shopify/cli @shopify/theme
  ```
  **ABORTE** a skill até o membro confirmar que instalou.

- Se instalado, prossiga.

## Paths normalizados (variáveis top-level)

Todos os comandos desta skill usam estas variáveis. **Defina no topo** (substituindo `[produto]` pelo slug):

```bash
PRODUTO="[slug]"
STAGING_DIR="/workspace/${PRODUTO}/06-page/staging"
THEME_DIR="/workspace/${PRODUTO}/06-page/theme-clone"
OUTPUT_DIR="/workspace/${PRODUTO}/06-page"
STORE=""  # preenchido abaixo
```

### Detecção da loja

1. Leia `/workspace/[produto]/manifest.json` e tente extrair `product_url` ou `store_url`.
2. Extraia o domínio `.myshopify.com`:
   - Se `product_url = "https://acme.myshopify.com/products/..."` → `STORE="acme.myshopify.com"`.
   - Se é custom domain (`acme.com`), **pergunte ao membro**: "Qual o domínio `.myshopify.com` da sua loja?"
3. Se não conseguir detectar, pergunte diretamente:
   > "Qual seu store handle `.myshopify.com`? (ex: `acme-store.myshopify.com`)"
4. Salve em `STORE`.

**Todos os `shopify theme ...` comandos usam `--store "$STORE"` a partir daqui.**

## ETAPA 9 — Create Page Template (blocks pré-populados com a copy)

**REGRA DE OURO:** Quando o membro abre `/pages/[produto]` no theme editor, a página tem que estar **100% montada** com todos os blocks no lugar certo + todos os settings preenchidos com a copy real. Não é pra ele arrastar nada. Ele só edita/deleta/adiciona se quiser.

Pra isso, o `templates/page.[produto].json` **precisa listar TODOS os blocks** dentro de cada section, com settings inline. **Section sem `blocks: {...}` preenchido NÃO funciona** — se a entry tiver só `settings: {}` (sem a key `blocks`), ou `blocks: {}` vazio, a página renderiza zero blocks. Apesar dos defaults estarem no schema, o Shopify só popula blocks do preset quando o membro adiciona a section manualmente via "Add section". Pra páginas pré-montadas via template JSON, os blocks precisam estar **explícitos no próprio JSON** com `blocks: {...}` + `block_order: [...]`.

**Padrão correto do template JSON:**

```json
{
  "sections": {
    "hero": {
      "type": "page-[produto]-hero",
      "blocks": {
        "badge": {
          "type": "badge",
          "settings": {
            "text": "[eyebrow da copy]",
            "show_dot": true,
            "dot_color": "[cor do design system]",
            "variant": "solid",
            "font_size": 13,
            "padding_x": 14,
            "padding_y": 7,
            "radius": 99,
            "space_after": 20,
            "custom_css": ""
          }
        },
        "heading": {
          "type": "heading",
          "settings": {
            "text": "[hero headline da copy, com <em>palavra</em> pra emphasis]",
            "size": "display2",
            "font": "serif",
            "weight": "500",
            "line_height": 10,
            "letter_spacing": "-0.03em",
            "space_after": 24
          }
        },
        "paragraph": {
          "type": "paragraph",
          "settings": {
            "text": "<p>[sub-headline da copy]</p>",
            "size": "lg",
            "line_height": 15,
            "max_width": 48,
            "space_after": 24
          }
        },
        "cta_row": {
          "type": "button_row",
          "settings": {
            "alignment": "flex-start",
            "gap": 12,
            "radius": 4,
            "btn_1_show": true,
            "btn_1_label": "[CTA principal]",
            "btn_1_variant": "primary",
            "btn_1_price": "[preço se aplicável]",
            "btn_2_show": true,
            "btn_2_label": "[CTA secundário]",
            "btn_2_variant": "ghost",
            "btn_3_show": false
          }
        },
        "stats": {
          "type": "stats_bar",
          "settings": {
            "columns": 3,
            "show_divider": true,
            "stat_1_show": true,
            "stat_1_label": "[label 1]",
            "stat_1_value": "[value 1 com <span>unit</span>]",
            "stat_2_show": true,
            "stat_2_label": "[label 2]",
            "stat_2_value": "[value 2]",
            "stat_3_show": true,
            "stat_3_label": "[label 3]",
            "stat_3_value": "[value 3]"
          }
        },
        "tag_1": {
          "type": "tag",
          "settings": {"eyebrow": "[tag 1 eyebrow]", "title": "[tag 1 title]", "position": "tl", "rotation": -3, "theme": "light"}
        },
        "tag_2": {
          "type": "tag",
          "settings": {"eyebrow": "[tag 2 eyebrow]", "title": "[tag 2 title]", "position": "br", "rotation": 3, "theme": "dark"}
        }
      },
      "block_order": ["badge", "heading", "paragraph", "cta_row", "stats", "tag_1", "tag_2"],
      "settings": {
        "layout": "split-lr",
        "container_max": 1280,
        "padding_y": 112,
        "column_gap": 56,
        "image_ratio": "adapt",
        "image_fit": "cover",
        "color_bg_top": "[design system bg]",
        "color_bg_bottom": "[design system bg2]",
        "color_text": "[design system text]",
        "color_heading": "[design system heading]",
        "color_accent": "[design system accent]",
        "color_on_accent": "[design system on-accent]"
      }
    }
  },
  "order": ["hero", "benefits", "mechanism", "proof", "offer", "guarantee", "faq", "cta_final"]
}
```

**Pseudocódigo acima — só o hero expandido.** Replique a estrutura pras outras sections do plano (benefits, mechanism, etc), cada uma com `blocks: {...}` + `block_order: [...]` + `settings: {...}` completos. JSON real não aceita `/* comentários */` nem `...` — todo bloco fica listado explicitamente.

**Checklist final do template JSON:**
- [ ] TODA section tem `blocks: {...}` pré-populado (não `{}`)
- [ ] TODO block tem `settings: {...}` com os valores da copy real (não vazios)
- [ ] Cada section tem `block_order: [...]` com a ordem correta
- [ ] Section `settings` têm as cores do design system aplicadas
- [ ] `order: [...]` lista todas as sections na sequência persuasiva (hero → proof → offer → cta)
- [ ] Copy REAL populada: hero headline, sub-headline, CTAs, stats, benefits VOC, testimonials, tiers, FAQ questions+answers, CTA final — tudo do `05-copy.md`

**Quando salvar:** `<staging>/templates/page.[produto].json`.

### Validação de template JSON (OBRIGATÓRIO antes de deploy)

Para cada section em `sections`:

- [ ] `blocks` existe e é objeto **não-vazio**
- [ ] `block_order` existe e referencia apenas chaves de `blocks`
- [ ] Todo block em `block_order` existe em `blocks`
- [ ] Todo block tem `type` válido (presente no section.liquid correspondente — cruza com o Liquid em `<staging>/sections/`)
- [ ] Sem typos em setting IDs (comparar contra schema da section)

**Snippet de validação (rodar antes de todo push):**

```python
import json
import re
from pathlib import Path

PRODUTO = "<slug>"
STAGING = Path(f"/workspace/{PRODUTO}/06-page/staging")
TEMPLATE_JSON = STAGING / "templates" / f"page.{PRODUTO}.json"
SECTIONS_DIR = STAGING / "sections"

with open(TEMPLATE_JSON) as f:
    data = json.load(f)

errors = []

# Build mapping: section_type -> set of block types declared in Liquid schema
section_block_types: dict[str, set[str]] = {}
for liquid_file in SECTIONS_DIR.glob("*.liquid"):
    content = liquid_file.read_text(encoding="utf-8")
    # Crude but effective: parse schema block types from `"type": "xxx"` inside {% schema %}
    match = re.search(r"\{% schema %\}(.*?)\{% endschema %\}", content, re.DOTALL)
    if not match:
        continue
    schema_raw = match.group(1).strip()
    try:
        schema = json.loads(schema_raw)
    except json.JSONDecodeError:
        errors.append(f"{liquid_file.name}: schema JSON invalido")
        continue
    block_types = {b["type"] for b in schema.get("blocks", [])}
    # Section "type" (referenced from template JSON) = filename without .liquid
    section_type = liquid_file.stem
    section_block_types[section_type] = block_types

for sid, section in data["sections"].items():
    section_type = section.get("type")
    if not section_type:
        errors.append(f"{sid}: sem 'type'")
        continue

    blocks = section.get("blocks", {})
    if not blocks:
        errors.append(f"{sid} ({section_type}): blocks vazio — 0 blocks serao renderizados")

    order = section.get("block_order", [])
    if blocks and not order:
        errors.append(f"{sid} ({section_type}): tem blocks mas block_order ausente")
    for bk in order:
        if bk not in blocks:
            errors.append(f"{sid}: block_order referencia '{bk}' que nao existe em blocks")

    allowed_types = section_block_types.get(section_type, set())
    for bk, binfo in blocks.items():
        btype = binfo.get("type")
        if not btype:
            errors.append(f"{sid}.{bk}: block sem 'type'")
            continue
        if allowed_types and btype not in allowed_types:
            errors.append(
                f"{sid}.{bk}: type '{btype}' nao existe no schema do section '{section_type}' "
                f"(allowed: {sorted(allowed_types)})"
            )

# Validate order references existing sections
for sid in data.get("order", []):
    if sid not in data["sections"]:
        errors.append(f"order: '{sid}' nao existe em sections")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print(f"Template JSON valido: {len(data['sections'])} sections, order OK.")
```

**Execute antes de `shopify theme push`:**

```bash
python3 -c "<snippet acima>"
```

Se qualquer error for encontrado, **ABORTE o push**. Volte pra `page-sections` pra adicionar o block type faltante, ou corrija o template JSON.

## ETAPA 10 — Install no tema do membro (safe preview)

**Regra:** nunca modifique o tema live do membro. Sempre trabalhe numa duplicata unpublished. A Shopify CLI faz isso em 4 comandos.

### 10.1 Detectar tema ao vivo

```bash
shopify theme list --json --store "$STORE"
```

Identifique o theme com `"role": "live"` no output JSON e anote o ID. Chame de `LIVE_THEME_ID`.

### 10.2 Duplicar o tema live (cria cópia unpublished)

```bash
shopify theme duplicate \
  --theme "$LIVE_THEME_ID" \
  --name "[$PRODUTO] Preview (Aura)" \
  --store "$STORE" \
  --force --json
```

Output inclui o ID novo. Chame de `NEW_THEME_ID`.

### 10.3 Pullar a cópia pra pasta local

```bash
mkdir -p "$THEME_DIR"
shopify theme pull \
  --theme "$NEW_THEME_ID" \
  --store "$STORE" \
  --path "$THEME_DIR" \
  --force
```

### 10.4 Instalar os arquivos gerados

```bash
# Copia section files + template JSON pro tema duplicado
cp "$STAGING_DIR"/sections/page-"$PRODUTO"-*.liquid "$THEME_DIR"/sections/
mkdir -p "$THEME_DIR"/templates
cp "$STAGING_DIR"/templates/page."$PRODUTO".json "$THEME_DIR"/templates/
```

**Não tem diretório `blocks/`** — todos os blocks são inline no schema da section.

### 10.5 Push pra cópia unpublished

```bash
shopify theme push \
  --theme "$NEW_THEME_ID" \
  --store "$STORE" \
  --path "$THEME_DIR" \
  --nodelete --json
```

O `--nodelete` preserva tudo que já existe no tema copiado. Se aparecer `"warning": "..."` no JSON com campo `"errors"`, resolva os erros (veja "Debug — Quando push falha" abaixo) e re-push.

### 10.6 Dar o preview link ao membro

Theme editor direto no template:
```
https://$STORE/admin/themes/$NEW_THEME_ID/editor?template=page.$PRODUTO
```

Preview da storefront (precisa a página "[produto]" existir no Admin → Pages):
```
https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID
```

**IMPORTANTE:** o dropdown "Theme template" no admin Pages SÓ lista templates do tema LIVE. Como `page.[produto]` só existe na cópia unpublished, não aparece lá. Workaround: usar `?view=[produto]` na URL do storefront pra forçar o template alternate, OU o theme editor direto (funciona sempre).

## ETAPA 10.5 — Report ao membro

Gere **2 arquivos** de report em `/workspace/[produto]/06-page/`:

### 1. `06-deploy-report.md` (humano)

Conteúdo:

1. **Sections geradas** + justificativa do plano específico (copie da `06-plan.md`).
2. **Lista de arquivos criados** (paths absolutos):
   - `<staging>/sections/page-[produto]-*.liquid`
   - `<staging>/templates/page.[produto].json`
   - Arquivos instalados no `$THEME_DIR`
3. **Preview links** (theme editor + storefront com `?view=`).
4. **Como subir pra produção** (quando satisfeito):

   > ⚠️ **Aviso**: `shopify theme publish` substitui o tema live atual. Antes, duplique o live como backup:
   > ```
   > # 1. Backup do live atual (recomendado antes de publicar a cópia Aura):
   > shopify theme duplicate --theme $LIVE_THEME_ID --name "Pre-Aura Backup $(date +%Y%m%d)" --store $STORE --force
   > 
   > # 2. Depois publica a cópia Aura como live:
   > shopify theme publish --theme $NEW_THEME_ID --store $STORE
   > ```
   > Se der ruim: abre admin → Online Store → Themes → encontra "Pre-Aura Backup [data]" → Publish.
5. **Settings expostos** por block/section (resumo compacto).
6. **Issues conhecidas** da `page-sections` ETAPA 8 + quaisquer warnings do push.

### 2. `06-deploy-report.json` (machine-readable)

```json
{
  "deploy_id": "<uuid>",
  "produto": "[slug]",
  "store": "<STORE>",
  "live_theme_id": "<LIVE_THEME_ID>",
  "theme_id": "<NEW_THEME_ID>",
  "theme_name": "[Produto] Preview (Aura)",
  "preview_url_editor": "https://<STORE>/admin/themes/<NEW_THEME_ID>/editor?template=page.<produto>",
  "preview_url_storefront": "https://<STORE>/pages/<produto>?preview_theme_id=<NEW_THEME_ID>",
  "sections_deployed": [
    {"id": "hero", "type": "page-<produto>-hero", "blocks_count": 7},
    {"id": "benefits", "type": "page-<produto>-benefits", "blocks_count": 5}
  ],
  "template_deployed": "template.product.page.json",
  "validation_passed": true,
  "validation_errors": [],
  "push_warnings": [],
  "staging_dir": "/workspace/<produto>/06-page/staging",
  "theme_clone_dir": "/workspace/<produto>/06-page/theme-clone",
  "deployed_at": "2026-MM-DDTHH:MM:SSZ"
}
```

## ETAPA 11 — Iteration Loop

Termine perguntando: 

> "Página gerada, validada e deployada. Quer ajustar algo? Pode pedir coisas como: 'hero muito apertado, mais ar', 'cores mais escuras', 'features em 2 colunas em vez de 3', 'adicionar countdown na oferta'. Vou refinar sem regenerar tudo do zero."

Para ajustes futuros:

- **Mudanças de spacing/layout** → edite o `{% stylesheet %}` da section afetada em `$STAGING_DIR/sections/` → revalide (`shopify-plugin:shopify-liquid`) → re-cp pro `$THEME_DIR` → `shopify theme push --theme $NEW_THEME_ID --nodelete`.
- **Mudanças estruturais** (novos settings/blocks) → edite section Liquid + template JSON → rode validação de blocks (ETAPA 9) → push.
- **Mudanças de copy** → atualize os defaults no schema E os pré-populados no template JSON → push.
- **Sempre** revalide com `shopify-plugin:shopify-liquid` após qualquer mudança.
- **Sempre** rode o snippet Python de validação do template JSON antes de push — erros pegos aqui evitam 80% dos problemas.

Atualize `06-deploy-report.json` a cada iteração (campo novo `iterations: [...]` com timestamp + mudanças).

## SALVAR (dual output obrigatório — rule 6b do CLAUDE.md)

Salve um relatório completo em **DOIS arquivos** dentro de `/workspace/[produto]/06-page/`:

1. **`06-page.md`** (fonte — a AI lê nas fases seguintes)
2. **`06-page.html`** (visualização humana — o membro abre no browser)
3. **`06-deploy-report.json`** (machine-readable)

Conteúdo de `06-page.md` + `06-page.html`:

- Plano de sections (copie de `06-plan.md`) + justificativa por que incluiu/excluiu cada section
- Brand discovery answers (da `page-planning`) — incluindo se usou referência visual e qual
- Design system completo (copie de `06-design-system.md`) — paleta, tipografia, spacing, breakpoints
- Variante de hero escolhida + por quê (da `06-sections-report.md`)
- Lista de arquivos criados com paths absolutos
- Settings expostos por section (resumo compacto)
- Preview links (theme editor + storefront)
- Issues conhecidas (se houver)
- Histórico de iterações (ETAPA 11) — atualize a cada refinement

**Como gerar o `.html`:** use o design system de `.claude/templates/aura-report-template.html` — copie o CSS completo + estrutura de componentes (section-label, callout, note, opportunity, pill, table-wrap, quote, kpi-grid). Self-contained (CSS inline, sem server). Inclua o logo SVG do Aura no topo. Responsivo mobile (overflow-wrap, word-break em code/callout).

Atualize `/workspace/[produto]/manifest.json` adicionando `06c-page-deploy` ao array `skills_completed`.

Ao final diga:

> "Page-deploy completo. Próximo passo: rode `shopify theme dev` pra ver ao vivo, ou diga 'creatives' pra gerar briefings de criativos pra ads, ou 'scale' pra estratégia de escala."

## Debug — Quando `shopify theme push` falha

Quando o push retorna JSON com campo `"errors"`, leia a mensagem do erro e aja conforme a tabela:

| Mensagem de erro (trecho) | Causa provável | Solução |
|---|---|---|
| `Section type 'X' does not refer to an existing section file` | Template JSON referencia section que não foi installada ainda OU falhou install | Verifique ordem dos arquivos no `cp`; push a section primeiro |
| `Theme block 'blocks/X.liquid' does not exist` | Theme blocks referenciados mas arquivos não existem | Refatore pra blocks inline (volte pra `page-sections`) |
| Page template não aparece no dropdown "Theme template" do admin Pages | Admin só lista templates do tema LIVE; seu template tá na cópia unpublished | Use theme editor direto: `/admin/themes/$NEW_THEME_ID/editor?template=page.$PRODUTO` |
| `shopify theme duplicate` trava esperando confirmação | Contexto não-interativo | Flag `--force` já incluída no comando da 10.2 — confira se não foi removida |
| Blocks aparecem vazios na preview | Template JSON tem `"blocks": {}` ou ausente | Rode o snippet Python da ETAPA 9 — vai pegar o erro antes |
| `Missing width and height attributes on img tag` e outros erros de Liquid | Problema nas sections, não no template JSON | Volte pra `page-sections` Debug table |

**Fluxo:** sempre leia o JSON do push (`--json`), filtre `"errors"`, resolva erro por erro. Pra erros de Liquid (sections), consulte a tabela de debug em `page-sections`.

## Como invocar specialists

Esta skill depende principalmente de:

| Specialist | Skill name |
|---|---|
| **Validação Liquid** | `shopify-plugin:shopify-liquid` |

Quaisquer ajustes de código/design disparados no iteration loop (ETAPA 11) re-invocam os specialists da `page-sections` — mas o fluxo principal desta skill é validação + deploy, não geração.

## Referências cruzadas

- **Skill anterior:** `page-sections` (gera os `.liquid` consumidos aqui)
- **Primeira skill da cadeia:** `page-planning` (gera `06-plan.json` + `06-design-system.md`)
- **Próxima skill no fluxo Aura Engine:** `07-creative-engine` (gera briefings de criativos pra ads depois que a página está no ar)

## Comandos úteis (referência pro membro)

> Estes comandos rodam no terminal **real** do membro (não dentro do `!` do Claude Code, que é não-interativo).

Baixar o tema Shopify (uma vez):
```bash
mkdir -p ~/shopify-theme && cd ~/shopify-theme
shopify theme pull --store SUA-LOJA.myshopify.com --theme ID-DO-TEMA
```

Preview ao vivo (durante edição):
```bash
cd ~/shopify-theme
shopify theme dev --store SUA-LOJA.myshopify.com
```

Push pro tema (quando satisfeito):
```bash
cd ~/shopify-theme
shopify theme push --store SUA-LOJA.myshopify.com --theme ID-DO-TEMA
```

Substitua `SUA-LOJA.myshopify.com` e `ID-DO-TEMA` pelos valores reais do membro. Pra descobrir o ID:
```bash
shopify theme list --store SUA-LOJA.myshopify.com
```

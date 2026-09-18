# Page Build · Referência: SPLIT e COMPILE+POPULATE (ETAPAs 1 e 2)

> O split do HTML aprovado por `data-aura-section` (ETAPA 1), o `liquid-converter.py` numa invocação só (caminho batch e Modo C por section), o rename semântico dos block types editando `.liquid` e template JSON juntos, o contrato de variant IDs do `pricing_tier`, as interações removidas pelo conversor e a restauração obrigatória dos SVGs grandes (ETAPA 2). Abra nas ETAPAs 1 e 2.

## ETAPA 1 — SPLIT (HTML aprovado → fragmentos por section)

O `design/page.html` aprovado tem cada section marcada com `<section data-aura-section="hero">` etc (a `page-design` garante esses markers nas três rotas de design — §3.7 dela). Splite:

1. Parse do `design/page.html`. Pra cada `<section data-aura-section="X">`, extraia o fragmento HTML completo daquela section → salve em `${STAGING_DIR}/html/<X>.html`. Os ids `X` batem com `sections_plan[].id` de `page-plan.json`.
2. Extraia o CSS (do `<style>` do documento, ou do `.css` companion se houver) → `${STAGING_DIR}/html/page.css`. O conversor injeta isso no `{% stylesheet %}` de cada section (namespaced). **Fora dessa extração fica o bloco `<style data-aura-fonts="...">`**: ele carrega a fonte pelo caminho do arquivo de design (`assets/fonts/...`, ou a fonte em base64 quando a `page-design` usou o modo `inline`), e nenhum dos dois existe na loja. Remova o bloco antes do split, anote a família e os pesos que ele declarava e provisione a fonte no passo 6.4b (asset do tema). Deixar o bloco entrar = caminho quebrado em cada section, ou a fonte inteira duplicada em todas elas.
3. **Se os marcadores `data-aura-section` faltarem** (HTML antigo ou editado à mão): splite por âncoras/headings de section seguindo o `section_order` de `page-plan.json`, ou peça à `page-design` pra re-emitir o HTML com os marcadores pela rota que gerou a página. Não chute fronteiras de section.

Resultado: N fragmentos HTML (1 por section do plano) + 1 CSS compartilhado.

## ETAPA 2 — COMPILE+POPULATE (liquid-converter.py, UMA invocação)

O `liquid-converter.py` é o conversor **CANÔNICO e OBRIGATÓRIO** (não é mais "legacy/draft" — é o caminho determinístico). O que ele aplica por código está na seção **Padrões aplicados pelo conversor** abaixo: text→settings (everything-editable), color settings inline no root + `| escape`, tokens (shadow/radius/font) como `var(--x)`+setting com migração de hardcoded, form `/cart/add` nativo, blocks inline com copy real por instância, CSS filtrado e rescopado por section, POPULATE do template JSON.

**COMPILE e POPULATE saem da MESMA invocação** — nunca rode o conversor duas vezes sobre o mesmo `--output` (a segunda execução regenera o `.liquid` do zero e apaga renames manuais).

### Caminho preferido — batch (página inteira numa invocação)

Monte `${STAGING_DIR}/batch-manifest.json`:

```json
{
  "product_slug": "[slug]",
  "page_handle": "[slug]",
  "sections": [
    { "type": "hero", "html": "workspace/[slug]/page/staging/html/hero.html", "css": "workspace/[slug]/page/staging/html/page.css", "namespace": "page-[slug]-hero", "output": "workspace/[slug]/page/staging/sections/page-[slug]-hero.liquid" }
  ]
}
```

(1 entry por section do `section_order`; `html`/`css` aceitam path ou conteúdo inline.) Rode:

```bash
python3 ${TOOLS_DIR}/liquid-converter.py \
  --batch ${STAGING_DIR}/batch-manifest.json \
  --emit-template-json ${STAGING_DIR}/templates/page.${PRODUTO}.json
```

O batch converte todas as sections + emite o `page.[produto].json` populado (ordem = ordem do manifest) numa passada.

### Caminho alternativo — Modo C por section (quando só 1 section muda, ex: iteration loop)

```bash
python3 ${TOOLS_DIR}/liquid-converter.py \
  --html ${STAGING_DIR}/html/<id>.html \
  --css ${STAGING_DIR}/html/page.css \
  --type <id> \
  --output ${STAGING_DIR}/sections/page-${PRODUTO}-<id>.liquid \
  --namespace page-${PRODUTO}-<id> \
  --product-slug ${PRODUTO} \
  --emit-template-json ${STAGING_DIR}/templates/page.${PRODUTO}.json \
  --page-handle ${PRODUTO}
```

- `<id>` = o id da section (`hero`, `benefits`, `mechanism`, `offer`...) de `sections_plan`.
- O merge single-section do `--emit-template-json` PRESERVA a posição da section no `order[]` (re-compilar o hero não o manda pro fim).
- **NÃO use `--blocks-dir`** (deprecado e ignorado — blocks são inline no schema; nenhum `blocks/*.liquid` é gerado).
- O Modo B legacy (`--sections-json`, markup de página de concorrente) é **BLOQUEADO por default** — exige `--allow-competitor-markup` e só se usa em página PRÓPRIA. O fluxo desta skill é sempre Modo C/batch sobre o HTML aprovado da `page-design`.

### Depois do compile — rename semântico (Claude, editando .liquid + template JSON JUNTOS)

O conversor dá nomes genéricos aos block types (derivados do `--type`/classes). **SÓ AGORA** (depois da última invocação do conversor) renomeie pros type-specific do Catálogo: `benefit_card`, `pricing_tier`, `review_card`, `faq_item`, `mechanism_card`... Cada rename toca 4 lugares em sincronia: o `{% when '<tipo>' %}` no markup, o `type` no `schema.blocks[]`, o `type` em `presets[0].blocks` (se presente), e o `type` de cada block no `templates/page.[produto].json`. Rode o snippet de validação da ETAPA 4 depois — ele acusa type órfão.

**Contrato de variant IDs (lido pela recipe `deploy-shopify-product.md`):** todo block `pricing_tier` DEVE expor os settings `variant_id` (text, default vazio — preenchido pela recipe/membro com o ID real) e `qty` (number — a quantidade do tier: 1/3/6, default preenchido com o valor real do tier). O conversor já emite settings de CTA `variant_id_*`/`cta_quantity_*` quando detecta o form de compra; no rename, normalize-os pra `variant_id`/`qty` dentro do block `pricing_tier`. É por `qty` que a recipe casa block ↔ variant criada no Shopify.

Também confira que interações removidas pelo conversor (`<script>` sai com warning listando cada um) foram reimplementadas de forma nativa (`<details><summary>` pra FAQ/accordion, CSS puro pra tabs simples) — nunca perder interação silenciosamente.

### Restauração de SVGs grandes (OBRIGATÓRIA pós-compile)

O conversor substitui todo `<svg>` com mais de 500 chars por `<span class="icon-placeholder">` (padrão 9). Ilustração de mecanismo, selo de garantia, logo de mídia — tudo isso some silenciosamente se você não restaurar. Protocolo:

1. **Inventário:** `grep -n 'icon-placeholder' ${STAGING_DIR}/sections/*.liquid` — cada match é um SVG substituído. Cruze com o fragmento fonte (`${STAGING_DIR}/html/<section>.html`) pra identificar QUAL SVG original ocupava aquele lugar (posição no markup + contexto).
2. **Reinjeção:** substitua cada `<span class="icon-placeholder">` pelo SVG ORIGINAL do fragmento fonte — inline no markup do `.liquid` (default), ou como setting `html`/`icon_custom_svg` se o membro precisar editá-lo no theme editor.
3. **Verificação:** re-rode o grep — **zero `icon-placeholder` residual** nos `.liquid` antes da ETAPA 3. Página deployada com ícone/ilustração faltando é drift visual que o fidelity check (6.11) pegaria caro lá na frente — mate aqui.

(Como o rename semântico: se re-COMPILAR uma section, a restauração daquela section precisa ser re-aplicada.)

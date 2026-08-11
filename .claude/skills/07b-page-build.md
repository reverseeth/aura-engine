---
name: page-build
description: Segunda skill da fase STOREFRONT. COMPILE+POPULATE determinístico do design/page.html aprovado na 07a em sections Liquid via liquid-converter.py (Modo C por section ou --batch pra página inteira, por código não por reasoning), valida cada section com shopify-plugin:shopify-liquid (3 retries), roda os gates de launch (compliance + promise↔config), faz DEPLOY seguro no Shopify (shopify-theme-safety integral, marker data-aura-build) e conduz a PUBLICAÇÃO do tema com aprovação do membro (grava manifest.storefront). Use quando o membro disser "build page", "deploy", "subir página", depois de aprovar o design na 07a.
---

# 07b — Page Build (COMPILE determinístico + POPULATE + DEPLOY)

Segunda e última skill da fase **STOREFRONT** (07a → 07b). A 07a produziu o `design/page.html` aprovado — a FONTE ÚNICA DE VERDADE visual. Esta skill **compila esse HTML em Liquid por CÓDIGO, não por reasoning**, popula o template com a copy real, passa os gates de launch e deploya no Shopify.

Princípio: **conversão determinística mata as traduções lossy e o drift.** O Liquid é gerado mecanicamente do HTML aprovado via `tools/design-clone/liquid-converter.py` (Modo C por section, ou `--batch` pra página inteira). O Claude entra só pra (a) splitar o HTML por section, (b) renomear blocks semanticamente DEPOIS do compile, (c) reimplementar interações que o conversor removeu (`<script>` sai com warning — usar `<details>` nativo etc.), (d) validar. O que o conversor aplica por código e o que ele NÃO faz está na seção **Padrões aplicados pelo conversor** — não afirme capacidade que não existe.

**O que esta skill faz:**

1. Pré-flight — exige `design/page.html` aprovado + `design-tokens.json` + `page-plan.json`.
2. SPLIT — separa o HTML aprovado em fragmentos por section (via marcadores `data-aura-section`) + o CSS.
3. COMPILE+POPULATE — roda `liquid-converter.py` numa invocação só (preferir `--batch`; ou Modo C por section com `--emit-template-json`). O template `page.[produto].json` sai populado com blocks/block_order/settings e a copy real.
4. RENAME semântico — o Claude renomeia os block types genéricos pros type-specific (editando `.liquid` E template JSON juntos), SÓ DEPOIS do compile (nunca re-rode o conversor por cima de renames) — mais a RESTAURAÇÃO dos SVGs grandes que o conversor substituiu por placeholder (inventário + reinjeção do original).
5. VALIDATE — cada `.liquid` passa por `shopify-plugin:shopify-liquid` (3 retries) + snippet de validação cruzada do template JSON + **check bloqueante de imagens/placeholders** (nenhuma section com imagem vazia/placeholder do mapa de mídia da 07a; zero `{{PLACEHOLDER}}` residual).
5.5. GEO / Schema (agent-readability) — gera o JSON-LD Schema.org (Product + Offer + AggregateRating + BreadcrumbList + FAQPage das perguntas reais da section faq) de `04-offer-builder/dados.json` + `06-copy-engine/dados.json` + reviews, valida, e injeta no template como bloco `custom_liquid` + um bloco "agent-readable facts" (specs, envio/retorno, disponibilidade, garantia) em texto limpo separado da copy persuasiva.
6. GATES (blocking) — GATE 1 compliance (ad-flag, CLI canônica) + GATE 2 promise↔config + GATE 3 performance budget, ANTES do deploy.
7. DEPLOY — shopify-theme-safety integral (duplicate → pull --nodelete → **provisionamento de web fonts** → push --nodelete + marker `data-aura-build` + criação da página + smoke test).
8. PUBLISH — com aprovação explícita do membro: backup do live → `shopify theme publish` → grava `manifest.storefront` (theme_id, page_url, published_at) que a 07d e a 10 leem → **fidelity check por visão** (screenshot da página no ar vs `design/page.html` aprovado; divergiu = corrige antes de encerrar).
9. Dual output (.md + .html, logo SVG) + iteration loop.

**Outputs em `workspace/[produto]/07-page/`:** `staging/html/*.html` + `staging/html/page.css` (fragmentos do SPLIT), `staging/sections/page-[produto]-*.liquid`, `staging/templates/page.[produto].json`, `staging/geo/product-schema.json` (JSON-LD), `staging/geo/agent-facts.html`, `page-report.md` + `page-report.html`, `deploy-report.json`. (O conversor NÃO gera `blocks/*.liquid` — blocks são inline no schema da section.)

---

## Pré-flight

1. Leia `workspace/profile.md` → `report_language` (default `pt-BR`; também em `manifest.report_language`). Relatórios internos e conversa nesse idioma. Copy consumidor-final permanece em inglês US.
2. **Gate de consistência (skill 09)** — leia `workspace/[produto]/09-consistency-audit/dados.json` se existir:
   - `launch_recommendation == "BLOCK"` → o deploy da página NÃO está bloqueado por si só (a página existir não gasta dinheiro), mas avise o membro dos items críticos e recomende rodar `consistency audit` de novo. O gate 09 é pré-requisito do **LAUNCH** (gateia a skill 10), não do deploy da página.
   - `"CAUTION"` → mostre warnings, peça confirmação.
   - `"GO"` ou ausente → siga (recomende rodar a 09 antes do launch).
3. Valide os inputs (sob `workspace/[produto]/07-page/`):
   - [ ] `design/page.html` existe (HTML aprovado da 07a — **sem ele, PARE e direcione pra 07a**; não existe modo "gera Liquid direto")
   - [ ] `design-tokens.json` existe e parseia
   - [ ] `page-plan.json` existe com bloco `strategy` + `sections_plan` + `section_order` (plans novos trazem `sections_plan[].media` — o mapa de mídia que o check bloqueante da ETAPA 4 usa; plan legado sem `media` é tolerado, o check degrada pro mínimo)
   - [ ] `manifest.json` tem `07a-page-design` em `skills_completed`
   - [ ] Plugin `shopify-plugin:shopify-liquid` disponível (se falhar, instrua `/plugin install shopify-plugin@shopify-plugin`)
4. Dirs de staging: `workspace/[produto]/07-page/staging/{html,sections,templates,geo}/` (criar com `mkdir -p`).

Se `design/page.html` faltar → "Não achei o design aprovado. Rode `07a-page-design` primeiro — preciso do `design/page.html` que você aprova antes de gerar Liquid."

---

## Paths normalizados (defina no topo)

```bash
PRODUTO="[slug]"
PAGE_DIR="workspace/${PRODUTO}/07-page"
DESIGN_HTML="${PAGE_DIR}/design/page.html"
STAGING_DIR="${PAGE_DIR}/staging"
THEME_DIR="${PAGE_DIR}/theme-clone"
TOOLS_DIR="tools/design-clone"
STORE=""  # preenchido na detecção da loja (ETAPA 6.1)
```

---

## ETAPA 1 — SPLIT (HTML aprovado → fragmentos por section)

O `design/page.html` aprovado tem cada section marcada com `<section data-aura-section="hero">` etc (a 07a garante esses markers em QUALQUER rota de design — §3.7 dela, inclusive handoff do canvas, clone-and-adapt e site-builders). Splite:

1. Parse do `design/page.html`. Pra cada `<section data-aura-section="X">`, extraia o fragmento HTML completo daquela section → salve em `${STAGING_DIR}/html/<X>.html`. Os ids `X` batem com `sections_plan[].id` de `page-plan.json`.
2. Extraia o CSS (do `<style>` do documento, ou do `.css` companion se houver) → `${STAGING_DIR}/html/page.css`. O conversor injeta isso no `{% stylesheet %}` de cada section (namespaced).
3. **Se os marcadores `data-aura-section` faltarem** (HTML antigo ou editado à mão): splite por âncoras/headings de section seguindo o `section_order` de `page-plan.json`, ou peça à `frontend-design` pra re-emitir o HTML com os marcadores. Não chute fronteiras de section.

Resultado: N fragmentos HTML (1 por section do plano) + 1 CSS compartilhado.

---

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
    { "type": "hero", "html": "workspace/[slug]/07-page/staging/html/hero.html", "css": "workspace/[slug]/07-page/staging/html/page.css", "namespace": "page-[slug]-hero", "output": "workspace/[slug]/07-page/staging/sections/page-[slug]-hero.liquid" }
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
- O Modo B legacy (`--sections-json`, markup de página de concorrente) é **BLOQUEADO por default** — exige `--allow-competitor-markup` e só se usa em página PRÓPRIA. O fluxo desta skill é sempre Modo C/batch sobre o HTML aprovado da 07a.

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

---

## ETAPA 3 — VALIDATE (shopify-plugin:shopify-liquid, 3 retries)

Cada `.liquid` gerado passa pelo skill `shopify-plugin:shopify-liquid` (modo validate). Protocolo determinístico (3 tentativas):

1. **Validate** — se OK, próxima section.
2. **Auto-fix + revalidate** — modo `fix` do plugin, revalida.
3. **Leitura manual do erro** — consulte a tabela **Debug — Quando validação falha** (abaixo), aplique o fix, revalide. Se ainda falhar → **PARE e reporte** ao membro (arquivo, erro exato, tentativas, ação manual sugerida).

Se o plugin estiver indisponível, **instale antes de seguir** (`/plugin marketplace add Shopify/shopify-ai-toolkit` + `/plugin install shopify-plugin@shopify-plugin`) — não existe fallback manual confiável; validar Liquid "no olho" é exatamente o modo de falha que esta skill elimina.

---

## ETAPA 4 — Validação do template JSON populado

O POPULATE já aconteceu na ETAPA 2 (o `--emit-template-json`/batch monta o `templates/page.[produto].json` com `blocks{}` + `block_order[]` + `settings{}` populados, usando a copy real do HTML como `default` de cada setting). Esta etapa valida o resultado — não re-roda o conversor.

**Modelo de blocks vs settings:** o conversor emite conteúdo ÚNICO (hero headline, eyebrow, sub, CTA único) como **section settings** (grupo Content — editável no theme editor) e conteúdo REPETÍVEL (benefit cards, pricing tiers, review cards, FAQ items, ingredients, steps) como **blocks** arrastáveis/reordenáveis, com UMA instância por item real do HTML (FAQ de 5 perguntas = 5 instâncias distintas). Sections monolíticas (só settings) são válidas e comuns (ex: hero).

**Erro #1 histórico (vale só pra sections COM blocks):** quando uma section É block-based (schema define block types repetíveis), o `templates/page.[produto].json` precisa ter `blocks: {...}` + `block_order: [...]` EXPLÍCITOS — senão renderiza ZERO daqueles blocks (o Shopify só popula preset blocks quando o membro adiciona a section manualmente via "Add section"). O POPULATE resolve isso. Sections monolíticas (settings-only) legitimamente têm `blocks: {}` e renderizam do markup direto.

Notas pra ajustes manuais no JSON:
- **Inserção em ordem reversa** (rule `reverse-order-insertion`): quando o Claude insere múltiplas sections no `order[]`/`sections{}` à mão, insere da maior posição pra menor pra não deslocar índices. No modo batch/merge o conversor já cuida disso.
- As cores das section settings vêm de `design-tokens.json` (role-tagged: background/surface/foreground/primary/accent/border).

### Validação do template JSON (OBRIGATÓRIA antes do deploy)

Pra cada section em `sections`:
- [ ] Se a section é **block-based** (schema do `.liquid` define block types), `blocks` é objeto **não-vazio** com `block_order`. Sections **monolíticas** (só settings, ex: hero) legitimamente têm `blocks: {}` — não é erro (o snippet abaixo já distingue os dois casos)
- [ ] `block_order` referencia apenas chaves de `blocks`; todo block de `block_order` existe em `blocks`
- [ ] Todo block tem `type` válido presente no schema da section `.liquid` correspondente
- [ ] `order[]` lista todas as sections na sequência persuasiva (`section_order` de `page-plan.json`)
- [ ] Copy REAL populada (hero headline, sub, CTAs, stats, benefits VOC, tiers, FAQ Q+A, CTA final) — tudo de `06-copy`
- [ ] **Se `page_type = advertorial`:** o href dos soft CTAs aponta pro destino de `page-plan.json.destination_ref` (a 07a define obrigatoriamente: handle/URL da pdp_lean de 2ª passada, PDP existente trabalhada, ou checkout direto). Advertorial é pré-lander — o soft CTA é `<a href>` de navegação pro destino, NUNCA form `/cart/add` (o fechamento acontece na página de destino). Se `destination_ref` estiver `null` num advertorial, PARE e mande o membro de volta pra 07a ETAPA 1 — advertorial no ar com CTA sem destino manda tráfego pago pro vazio.

Snippet de validação cruzada (roda antes de todo push — cruza template JSON contra os schemas dos `.liquid`):

```python
import json, re
from pathlib import Path
PRODUTO = "[slug]"
STAGING = Path(f"workspace/{PRODUTO}/07-page/staging")
TEMPLATE_JSON = STAGING / "templates" / f"page.{PRODUTO}.json"
SECTIONS_DIR = STAGING / "sections"
data = json.loads(TEMPLATE_JSON.read_text(encoding="utf-8"))
errors = []
section_block_types = {}
for lf in SECTIONS_DIR.glob("*.liquid"):
    m = re.search(r"\{% schema %\}(.*?)\{% endschema %\}", lf.read_text(encoding="utf-8"), re.DOTALL)
    if not m: continue
    try: schema = json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        errors.append(f"{lf.name}: schema JSON invalido"); continue
    section_block_types[lf.stem] = {b["type"] for b in schema.get("blocks", [])}
for sid, section in data["sections"].items():
    st = section.get("type"); blocks = section.get("blocks", {}); order = section.get("block_order", [])
    allowed = section_block_types.get(st, set())  # block types definidos no schema do .liquid
    # Section monolitica (schema SEM blocks) pode ter blocks vazio — conteudo unico vive em settings.
    # So e erro se o schema DEFINE blocks (conteudo repetivel: cards/tiers/reviews/faq) mas o template nao populou.
    if allowed and not blocks: errors.append(f"{sid} ({st}): schema define blocks mas template tem blocks vazio — 0 blocks renderizados")
    if blocks and not order: errors.append(f"{sid} ({st}): tem blocks mas block_order ausente")
    for bk in order:
        if bk not in blocks: errors.append(f"{sid}: block_order referencia '{bk}' inexistente")
    for bk, bi in blocks.items():
        bt = bi.get("type")
        if allowed and bt not in allowed:
            errors.append(f"{sid}.{bk}: type '{bt}' nao existe no schema de '{st}' (allowed: {sorted(allowed)})")
for sid in data.get("order", []):
    if sid not in data["sections"]: errors.append(f"order: '{sid}' nao existe em sections")
if errors: print("\n".join(errors)); raise SystemExit(1)
print(f"Template JSON valido: {len(data['sections'])} sections, order OK.")
```

Se qualquer erro → **ABORTE o push**, corrija (adicione o block type faltante no `.liquid` via re-COMPILE, ou corrija o template JSON).

### Check bloqueante — imagens e placeholders residuais (roda junto da validação acima)

Dois vazamentos históricos que esta validação mata antes do deploy: página no ar com slot de imagem vazio, e placeholder de template (`{{TESTIMONIAL_1}}`, `{{IMAGE_URL}}`) renderizando literal pro consumidor.

**1. Imagens do mapa de mídia (bloqueante).** Leia `page-plan.json.sections_plan[].media`:
- Qualquer section com `media.status: "placeholder"` → **BLOCK**: o plano de obtenção da 07a não foi cumprido. Fix paths (ES1-style): **(A)** membro fornece a imagem agora (salvar em `design/assets/`, atualizar o HTML aprovado + re-COMPILE da section, ou subir via admin → Files e apontar a setting), ou **(B)** voltar à 07a ETAPA 1.6 pra redecidir a mídia daquela section (ex: rebaixar pra `required: false` se a section vive de ícone). Não existe path (C) "deploya assim mesmo".
- Pra toda section com `media.required: true` e `status: "ready"`: confira que a setting de imagem correspondente no template JSON não está vazia (valor `shopify://shop_images/...` ou asset real). Setting `image_picker` vazia numa section que exige imagem = **BLOCK** com os mesmos fix paths. (Plano legado sem campo `media`: aplique o check no mínimo ao hero — hero sem imagem em landing/pdp é sempre erro.)

**2. Placeholders textuais residuais (bloqueante).** Liquid legítimo usa minúsculas com namespace (`{{ section.settings.x }}`); placeholder de template usa MAIÚSCULAS (`{{TESTIMONIAL_1}}`). Grep obrigatório:

```bash
grep -rnE '\{\{ ?[A-Z][A-Z0-9_]* ?\}\}' "${STAGING_DIR}/sections" "${STAGING_DIR}/templates" && echo "BLOCK: placeholder residual"
```

Qualquer match → **BLOCK**: substitua pelo conteúdo real da 06 (testimonial/copy de verdade) ou remova o elemento se o conteúdo não existe (nunca inventar um depoimento pra preencher). Zero matches = prossegue.

---

## ETAPA 4.5 — GEO / Schema (agent-readability — citação por AI search)

A loja precisa ser **legível por máquina**, não só por humano. ChatGPT, Perplexity e o Google AI Mode citam páginas que entregam fatos estruturados e verificáveis em vez de copy persuasiva crua. O Shopify já liga Agentic Storefronts por default, então o crawler de AI passa nessa página de qualquer jeito — a questão é se ele acha o que precisa pra te citar. Páginas com Schema.org completo são citadas com muito mais frequência que páginas sem (a diferença é grande). É barato (texto + um bloco JSON) e vira um moat que poucos concorrentes têm.

**Honestidade com o membro (não vender fantasia):** o ganho HOJE é **discovery e citação** — aparecer na resposta do ChatGPT/Perplexity quando alguém pesquisa o problema que o produto resolve, com a loja linkada como fonte. NÃO é "venda fechada dentro do chat" (esse fluxo de checkout agêntico ainda está engatinhando). O que se constrói agora é presença na camada de AI search antes dos concorrentes — quando a venda-dentro-do-chat amadurecer, quem já tem Schema limpo larga na frente. Posicione assim, sem prometer receita imediata.

Esta etapa NÃO toca o design visual nem a copy persuasiva. Ela adiciona duas camadas invisíveis pro consumidor humano e visíveis pro crawler: (1) o **JSON-LD Schema.org** no `<head>`/markup, (2) um bloco de **fatos legíveis por agente** em texto limpo.

### 4.5.1 — Montar o JSON-LD (Product + Offer + AggregateRating + BreadcrumbList + FAQPage)

Leia as fontes (todas já existem na cadeia; não invente nenhum campo):

- `workspace/[produto]/04-offer-builder/dados.json` → nome do produto, preço, `compare_at_price`, moeda, garantia (dias), unique mechanism, descrição da oferta.
- `workspace/[produto]/06-copy-engine/dados.json` → headline/descrição do produto, specs/benefícios em texto, brand, **e as perguntas/respostas REAIS da section faq** (fonte do nó FAQPage — as mesmas Q&A que a página exibe, nunca perguntas inventadas só pro Schema).
- **Reviews** → `04-offer-builder/dados.json` (se traz `social_proof`/`rating`) OU a review app real (Judge.me/Loox/Yotpo via Admin API, se conectada) OU o número que o GATE 2 já valida em `promise-check.json`. **O rating do Schema TEM que bater com o rating exibido na página e com a review app real** (senão é structured-data fraudulento — Google penaliza e pode disparar manual action).

**Regra dura — sem dado, sem nó.** Se um campo não tem fonte real (ex: rating sem review app conectada, ou `compare_at_price` ausente), **OMITA o nó/propriedade** em vez de inventar. `AggregateRating` só entra se há reviews reais e contáveis. Schema com número fabricado é pior que Schema ausente (vira manual action no Google Search Console).

Monte `staging/geo/product-schema.json` com este shape (preencha dos arquivos, sem placeholders soltos):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Product",
      "name": "<04-offer-builder product_name>",
      "description": "<06-copy descrição factual do produto, sem hype — o que é, o que faz>",
      "brand": { "@type": "Brand", "name": "<brand>" },
      "image": ["<URL absoluta da imagem principal do produto>"],
      "sku": "<SKU se disponível>",
      "offers": {
        "@type": "Offer",
        "price": "<preço numérico, ex 49.00>",
        "priceCurrency": "<USD>",
        "availability": "https://schema.org/InStock",
        "url": "<URL absoluta da PDP>",
        "priceValidUntil": "<data futura se há promo time-bound, senão omitir>",
        "hasMerchantReturnPolicy": {
          "@type": "MerchantReturnPolicy",
          "applicableCountry": "US",
          "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
          "merchantReturnDays": "<dias de garantia de 04-offer-builder>",
          "returnMethod": "https://schema.org/ReturnByMail",
          "returnFees": "https://schema.org/FreeReturn"
        },
        "shippingDetails": {
          "@type": "OfferShippingDetails",
          "shippingRate": { "@type": "MonetaryAmount", "value": "0", "currency": "USD" },
          "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "US" }
        }
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "<rating real, ex 4.7>",
        "reviewCount": "<N real de reviews>",
        "bestRating": "5"
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://<STORE>/" },
        { "@type": "ListItem", "position": 2, "name": "<categoria/coleção>", "item": "https://<STORE>/collections/<handle>" },
        { "@type": "ListItem", "position": 3, "name": "<product_name>", "item": "<URL absoluta da PDP>" }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "<pergunta REAL da section faq (copy da 06), texto idêntico ao da página>",
          "acceptedAnswer": { "@type": "Answer", "text": "<resposta REAL da section faq, texto limpo sem markup>" }
        }
      ]
    }
  ]
}
```

O nó **FAQPage** cobre TODAS as perguntas da section faq da página (uma entrada `Question` por Q&A, na mesma ordem). Se a página não tem section faq, omita o nó inteiro (mesma regra dura: sem dado, sem nó) — mas registre no `deploy-report.json` que a página saiu sem FAQ (a 07e vai apontar isso como gap de agent-readability).

Notas de montagem:
- **Coerência com o GATE 2** (ETAPA 5): `merchantReturnDays`, `returnFees` (free vs paid), `shippingDetails` (free shipping vs cobrado) e `priceValidUntil` (promo time-bound) TÊM que bater com o que `promise-check.json` valida contra a config real da Shopify. Se a promise de free shipping só cobre US, o `shippingDestination` é US — não invente cobertura mundial. **O Schema é mais uma superfície onde a promise tem que ser verdade** (Gate 2 cobre isso na ETAPA 5; se o Schema diverge da config, o gate barra).
- `availability` reflete o estoque real (`InStock`/`OutOfStock`/`PreOrder`).
- `priceValidUntil`: só se há promo com data-fim FIXA real (mesma regra do countdown na seção Padrões — nunca rolling/evergreen).
- `image`/`url`/`item` são URLs **absolutas** (`https://$STORE/...`), nunca relativas.

### 4.5.2 — Validar o JSON-LD (obrigatório antes de injetar)

```python
import json, urllib.parse
from pathlib import Path
PRODUTO = "[slug]"
SCHEMA = Path(f"workspace/{PRODUTO}/07-page/staging/geo/product-schema.json")
data = json.loads(SCHEMA.read_text(encoding="utf-8"))  # falha de parse = JSON inválido, corrija
assert data.get("@context") == "https://schema.org", "@context ausente/errado"
graph = data.get("@graph") or [data]
types = {n.get("@type") for n in graph}
errors = []
if "Product" not in types: errors.append("nó Product ausente")
if "BreadcrumbList" not in types: errors.append("nó BreadcrumbList ausente")
for node in graph:
    if node.get("@type") == "Product":
        if not node.get("name"): errors.append("Product.name vazio")
        off = node.get("offers", {})
        if not off.get("price"): errors.append("Offer.price vazio")
        if not off.get("priceCurrency"): errors.append("Offer.priceCurrency vazio")
        if not str(off.get("url","")).startswith("http"): errors.append("Offer.url não-absoluta")
        ar = node.get("aggregateRating")
        if ar:  # se existe, tem que ser real e completo (senão OMITA o nó inteiro)
            rv = float(ar.get("ratingValue", 0)); rc = int(ar.get("reviewCount", 0))
            if not (0 < rv <= 5): errors.append(f"ratingValue fora de 0–5: {rv}")
            if rc < 1: errors.append("aggregateRating sem reviewCount real — OMITA o nó se não há reviews")
    if node.get("@type") == "BreadcrumbList":
        for li in node.get("itemListElement", []):
            if not str(li.get("item","")).startswith("http"): errors.append("Breadcrumb item não-absoluto")
    if node.get("@type") == "FAQPage":  # RECOMENDADO (não bloqueia se ausente) — mas se existe, tem que ser válido
        qs = node.get("mainEntity", [])
        if not qs: errors.append("FAQPage sem mainEntity — OMITA o nó se a página não tem FAQ")
        for q in qs:
            if not q.get("name"): errors.append("FAQPage Question.name vazio")
            if not (q.get("acceptedAnswer") or {}).get("text"): errors.append("FAQPage acceptedAnswer.text vazio")
if "FAQPage" not in types:
    print("AVISO: nó FAQPage ausente (RECOMENDADO quando a página tem section faq — a 07e audita isso)")
if errors: print("\n".join(errors)); raise SystemExit(1)
print("JSON-LD válido:", ", ".join(sorted(types)))
```

Required = **Product + BreadcrumbList** (a validação barra sem eles). **FAQPage é RECOMENDADO**: não bloqueia se ausente (página sem FAQ existe), mas quando a página TEM section faq o nó deve estar presente e com as perguntas idênticas às da página — a 07e (agentic readiness) audita exatamente isso.

Falhou → corrija (preencher campo de fonte real, ou OMITIR o nó que não tem dado) e revalide. Não injete JSON-LD que não passou.
Validação externa adicional recomendada ao membro (não bloqueante): colar o `product-schema.json` no [Google Rich Results Test](https://search.google.com/test/rich-results) e no [Schema.org validator](https://validator.schema.org/) depois do deploy.

### 4.5.3 — Injetar no template (bloco `custom_liquid`, editável)

O JSON-LD entra como um bloco `custom_liquid` (`type: "liquid"` do Catálogo — editável, não o nativo) numa section de baixa visibilidade (ex: rodapé da PDP ou hero). Markup:

```liquid
<script type="application/ld+json">
{{ block.settings.jsonld_code }}
</script>
```

Onde `jsonld_code` é o `product-schema.json` minificado (single-line). Em loja Shopify com produto real, prefira ligar os campos dinâmicos a `{{ product.* }}` quando existirem (preço/disponibilidade ficam sempre em sincronia automática); para página de produto custom (`page.[produto]`), use os valores literais validados do `product-schema.json`. No `templates/page.[produto].json`, esse bloco entra com `block_order` (ordem reversa, rule `reverse-order-insertion`, como o resto do POPULATE).

> Por que `custom_liquid` e não hardcode no `.liquid`: mantém o JSON-LD **editável no theme editor** (DO NOT da skill: nada hardcoded), e o membro consegue atualizar preço/rating sem re-COMPILE.

### 4.5.4 — Bloco "agent-readable facts" (texto limpo, separado da copy persuasiva)

Além do JSON-LD (máquina), gere um bloco de **fatos em prosa limpa** que o crawler de AI extrai com facilidade e cita com confiança. Separe RIGOROSAMENTE da copy persuasiva: aqui é fato verificável, não hook nem benefício emocional. É o que o ChatGPT lê pra responder "qual a política de envio da loja X?" ou "esse produto tem garantia?".

Gere `staging/geo/agent-facts.html` — uma section discreta no fim da PDP (`data-aura-section="product-facts"`), 16-18px, ícones SVG (rule 7, nada de emoji em página). Cobre, **só com dados reais das fontes**:

| Categoria | Fonte | Exemplo de fato (factual, sem hype) |
|---|---|---|
| **Specs do produto** | `06-copy-engine/dados.json` / `04-offer-builder/dados.json` | "30ml serum. 0.5% encapsulated retinal. Fragrance-free, vegan." |
| **Envio** | config Shopify (mesma do Gate 2) | "Free US shipping. Ships in 1–2 business days from [state]." |
| **Retorno / garantia** | `04-offer-builder/dados.json` (dias) + policy page | "90-day money-back guarantee. Free returns by mail." |
| **Disponibilidade** | estoque real | "In stock. Ships immediately." |
| **Garantia/durabilidade** | `04-offer-builder/dados.json` | "Each bottle lasts ~60 days at the recommended use." |
| **Quem é** | brand snapshot | "Made by [brand], a [categoria] company." |

Regras do bloco:
- **Frase declarativa curta, verificável.** Nada de "the best", "revolutionary", "transform your skin" — isso é copy persuasiva, mora nas outras sections. Aqui é o "spec sheet" que a AI cita.
- Permanece em **inglês US** (é consumer-facing — regra inviolável do CLAUDE.md, igual ao resto da página).
- **Ad-safe** (rule 8b) e **sem travessão em excesso** (rule 8a) — passa pelo GATE 1 junto com o resto na ETAPA 5.
- Bate 1:1 com o JSON-LD e com a config real (envio/retorno/garantia/disponibilidade): JSON-LD, agent-facts e config são a MESMA verdade em três formatos.
- Esse bloco vira uma section a mais no SPLIT→COMPILE→POPULATE se você quiser editabilidade total; ou, mais simples, um `custom_liquid` companion do bloco JSON-LD. Escolha pela complexidade da página (section dedicada se o membro quer controle fino; `custom_liquid` se é só prosa estável).

> A copy persuasiva (hero, benefits, mechanism) continua intocada. Agent-facts é uma CAMADA ADICIONAL, não substitui nada. Humano lê a copy; AI cita os facts.

### 4.5.5 — Member-stage

Starter ($300–1000/mês, primeira loja): entregue o Schema completo mesmo assim (é baseline, custa quase nada e o ganho de discovery compounda) mas explique em 2 linhas o que é e por que importa, sem jargão. Validating/scaling: entregue e siga; mencione a validação externa (Rich Results Test) como passo opcional pós-deploy.

---

## ETAPA 5 — GATES de launch (blocking, ANTES do deploy)

Os dois gates da rule `pre-launch-gates.md` rodam sobre a copy injetada ANTES do push, mais o GATE 3 (performance budget) desta skill. **Inclua o bloco agent-facts (ETAPA 4.5.4) na varredura do GATE 1** (é consumer-facing) e confira que o JSON-LD (ETAPA 4.5.1) não contradiz a config real no GATE 2 (envio/retorno/garantia/rating/preço são a mesma verdade da página).

### GATE 1 — Ad-flag compliance

Consolide TODA a copy consumidor-final do template JSON (settings + blocks + agent-facts) num arquivo e rode a CLI canônica (rule `pre-launch-gates.md`):
```bash
# 1. salvar a copy consolidada
#    → workspace/[produto]/07-page/staging/gate1-copy.md
# 2. rodar o gate
python3 .claude/lib/compliance-preflight/run.py \
  --file workspace/${PRODUTO}/07-page/staging/gate1-copy.md \
  --vertical <manifest.product_vertical> \
  --stage pre_page \
  --json
```
Decisão pelo `overall_verdict` do JSON: `critical` → **BLOCK** (apresenta as flags com suas `rewrite_suggestions[]`, pede revisão). `warning` → BLOCK por default: aplica as `rewrite_suggestions[]` e **re-roda o check**; se virar `pass`, prossegue; se continuar `warning`/`critical`, loga em `workspace/[produto]/compliance-warnings.json` e o deploy só segue com decisão explícita do membro. `pass` → PASS.

Também cheque: zero travessão em headlines, ≤2 em copy longa (rule 8a); zero emoji na UI da página (rule 7 — ícones SVG).

### GATE 2 — Promise ↔ Config

Pra cada promise na copy/página (free shipping, "90-day money-back", "Use code XXXX", "Limited time — ends [date]", "Rated 4.X by N", "Made in [country]", "FDA cleared"), valide contra a config real da loja Shopify. Output em `workspace/[produto]/promise-check.json`. `fail ≥ 1` → **BLOCK deploy** com `fix` sugerido (ajustar copy OU ajustar config — membro escolhe, re-valida). `warn` → membro decide. Todos `pass` → prossegue.

**Mecânica executável por tipo de promise** (a skill só tem credencial de theme CLI — não assuma acesso Admin API que não existe; registre em cada item do `promise-check.json` o `method` que validou):

| Promise | Método de validação | `method` |
|---|---|---|
| Garantia/returns ("90-day money-back") | `curl -s https://$STORE/policies/refund-policy` e conferir os dias declarados | `policy_page_curl` |
| Free shipping / threshold | Perguntar ao membro com screenshot de Settings → Shipping (starter), OU Admin API `deliveryProfiles` se houver token de app (Dev Dashboard + client_credentials) conectado | `member_screenshot` / `admin_api` |
| Discount code ("Use code XXXX") | Screenshot de Discounts no admin, OU Admin API discount codes se houver token | `member_screenshot` / `admin_api` |
| Rating ("Rated 4.X by N") | Números reais da review app (Judge.me/Loox/Yotpo — painel ou API dela) | `review_app` |
| Regulatório ("Made in", "FDA cleared") | Confirmação documentada do membro + artefato (doc/link) | `member_confirmation` |

Sem método disponível pra um item → o item fica `warn` com nota "não-verificável agora" e o membro decide — NUNCA marcar `pass` sem verificação real (gate que "assume pass" é teatro).

O **JSON-LD e o bloco agent-facts (ETAPA 4.5)** são superfícies de promise adicionais: confira que `merchantReturnDays`/`returnFees`, `shippingDetails`, `availability`, `priceValidUntil`, `price` e `aggregateRating` do Schema batem com a config real e com `promise-check.json`. Schema divergente da config = structured-data fraudulento (manual action no Google) → trate como `fail` no gate.

> Sem bypass automático. Se o membro insistir em override, registre em `manifest.compliance_override` com `risk_acknowledged: true` (ES3 — exige o membro digitar "EU ACEITO O RISCO").

### GATE 3 — Performance budget (a página aprovada tem que ser rápida no 4G do consumidor)

Página lenta mata o CPA antes do criativo ter chance: cada segundo de LCP a mais derruba conversão de tráfego pago mobile. O alvo real é **LCP mobile < 2.5s**; o gate usa proxies simples e verificáveis.

**Checks estáticos (pré-push, sobre os `.liquid` + template JSON):**
- [ ] Toda imagem renderiza via `image_url | image_tag` com `width:` adequada (o CDN da Shopify serve WebP/AVIF e redimensiona — nunca a original de 4000px) e `loading: 'lazy'` nas sections abaixo da dobra.
- [ ] A imagem do hero SEM lazy (é o candidato a LCP) e COM `width`/`height` no `<img>` (o `image_tag` já emite — confira que ninguém removeu).
- [ ] Zero `<script>` de runtime nos `.liquid` das sections (grep; única exceção: `application/ld+json` da ETAPA 4.5 — não é runtime).
- [ ] CSS filtrado por section (padrão 7 do conversor) — sem N cópias do `page.css` no tema.

**Check de peso (pós-push, junto do smoke test 6.8):**
```bash
curl -s -o /dev/null -w '%{size_download}\n' "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO"   # HTML: alvo ≤ ~200KB
# peso das imagens above-the-fold (hero): curl -sI em cada src do hero e some content-length — alvo ≤ ~300KB
```
Página total (HTML + CSS + imagens) alvo ≤ ~1.5MB. **Estouro grosseiro (ex: imagem multi-MB no hero) = BLOCK do publish** até corrigir (reduzir `width:` do `image_url`, recomprimir o asset); desvio pequeno = warning com fix aplicado na hora. Registre o resultado em `deploy-report.json.gates.performance`.

---

## ETAPA 6 — DEPLOY (shopify-theme-safety INTEGRAL)

### 6.1 Shopify CLI + detecção da loja

```bash
which shopify && shopify version
```
Se não instalado, instrua (`brew install shopify-cli` ou `npm i -g @shopify/cli @shopify/theme`) e **ABORTE** até confirmar.

**Logue a versão no deploy-report.** O Shopify CLI 4.x (mai/2026+) se **auto-atualiza** via package manager entre sessões e removeu comandos legados (`theme serve` → `theme dev`). Se um deploy que funcionava ontem quebrar hoje com "command not found"/flag inválida, o primeiro suspeito é upgrade automático da CLI — cheque o changelog do release antes de debugar o tema. (Os comandos desta skill — `push/pull/duplicate/list/publish` com `--nodelete`/`--allow-live`/`--json` — continuam válidos no 4.x.)

Detecte `STORE`: leia `manifest.json` (`product_url`/`store_url`), extraia `.myshopify.com`. Se custom domain ou ausente, pergunte: "Qual seu store handle `.myshopify.com`?". Todos os `shopify theme ...` usam `--store "$STORE"`.

### 6.2 Backup + duplicate (Regra 6)

Nunca toque o tema live direto. Duplique primeiro (insurance barata):
```bash
shopify theme list --json --store "$STORE"   # identifica role:"live" → LIVE_THEME_ID
shopify theme duplicate --theme "$LIVE_THEME_ID" --name "[$PRODUTO] Preview (Aura)" --store "$STORE" --force --json   # → NEW_THEME_ID
```

### 6.3 Pull antes de editar (Regras 1+2 — `--nodelete`)

```bash
mkdir -p "$THEME_DIR"
shopify theme pull --theme "$NEW_THEME_ID" --store "$STORE" --path "$THEME_DIR" --nodelete --force
```
> `--nodelete` protege arquivos locais recém-criados. No iteration loop, SEMPRE pull antes de re-push pra não sobrescrever settings que o membro mexeu no theme editor.

### 6.4 Instalar arquivos gerados + marker `data-aura-build` (Regra 4)

```bash
cp "$STAGING_DIR"/sections/page-"$PRODUTO"-*.liquid "$THEME_DIR"/sections/
mkdir -p "$THEME_DIR"/templates
cp "$STAGING_DIR"/templates/page."$PRODUTO".json "$THEME_DIR"/templates/
```

Marker de verificação de push: **atributo de dados no elemento raiz da section hero** (comentário Liquid NÃO renderiza no HTML — jamais serviria pra verificar). Compute e injete:

```bash
HASH8=$(shasum -a 256 "$THEME_DIR/sections/page-${PRODUTO}-hero.liquid" | cut -c1-8)
# adicionar ao elemento raiz do markup da section hero (a tag mais externa, fora do schema):
#   data-aura-build="${PRODUTO}-${HASH8}"
```

O atributo é inerte, identifica o build, e **fica no arquivo** (não há re-push de limpeza; a cada re-compile do hero, recalcule o hash). É o mesmo mecanismo da `shopify-theme-safety.md` Regras 4/5.

### 6.4b Provisionar web fonts (a tipografia aprovada TEM que carregar de verdade)

O CSS das sections declara `font-family` — mas declarar não carrega a fonte. Se `heading_font`/`body_font` de `design-tokens.json` são web fonts e o tema não as serve, a tipografia aprovada no `design/page.html` **cai silenciosamente pro fallback do sistema** (Georgia onde devia ser Fraunces) e ninguém percebe até a página estar no ar. Protocolo:

1. Leia `heading_font` e `body_font` de `design-tokens.json`. Fontes de sistema (`-apple-system`, Georgia, Arial, `system-ui`...) → nada a fazer, pule.
2. Pra cada web font (o caminho padrão dos presets/signals é Google Fonts): confira se o tema clonado JÁ carrega a família — `grep -ri 'fonts.googleapis\|@font-face' "$THEME_DIR"/layout/theme.liquid "$THEME_DIR"/assets/*.css | grep -i "<família>"`. Já carrega → pule.
3. **Não carrega → provisione por um dos dois caminhos:**
   - **Caminho A — Google Fonts (default):** injete no `<head>` do `$THEME_DIR/layout/theme.liquid` (antes do primeiro `<link rel="stylesheet">`):
     ```html
     <link rel="preconnect" href="https://fonts.googleapis.com">
     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
     <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600&family=Inter:wght@400;500;600&display=swap">
     ```
     Só as famílias e SÓ OS PESOS que a página usa (se o preset veio de `.claude/lib/design-presets/presets.json`, o campo `google_fonts` lista exatamente isso — cada peso extra é KB no LCP). `display=swap` obrigatório.
   - **Caminho B — self-host:** baixe os `.woff2` das famílias/pesos, suba em `assets/` do tema, e declare `@font-face` no CSS da(s) section(s) (ou num snippet incluído pelo theme.liquid). Use quando o membro não quer dependência do Google ou o tema tem CSP restritiva.
4. **Validação (obrigatória):** no smoke test (6.8), `curl -s` a preview e confirme que o `<link>` do Google Fonts (ou o `@font-face`) da família está presente no HTML servido; no fidelity check (6.11), o screenshot confirma visualmente que o heading NÃO caiu pra fallback. Sem os dois checks, este passo é teatro.

> `theme.liquid` é template crítico (afeta a loja inteira) — o backup do 6.2 já cobre; a edição é aditiva (só `<link>` no `<head>`), nunca remova nada do arquivo.

### 6.5 Push (Regra 3 — `--nodelete`; `--allow-live` só no tema live)

Fluxo padrão = cópia unpublished (`NEW_THEME_ID`). `--allow-live` só quando o push é no tema LIVE (ex: hotfix pós-publicação).
```bash
shopify theme push --theme "$NEW_THEME_ID" --store "$STORE" --path "$THEME_DIR" --nodelete --json
# push no LIVE (exceção, com backup já feito em 6.2):
# shopify theme push --theme "$LIVE_THEME_ID" --store "$STORE" --path "$THEME_DIR" --nodelete --allow-live --json
```
Leia o `--json` procurando `"errors"` (não só `"warning"`). Resolva erro por erro (tabela de debug abaixo).

### 6.6 Criar a página no admin (pré-requisito da verificação)

`shopify page create` NÃO existe na CLI — a página é criada uma vez, manualmente:

> "Abre **Admin → Online Store → Pages → Add page**. Título: `[nome do produto]`. **Confere que o handle (final da URL) ficou exatamente `[produto]`** (edita em 'Edit website SEO' se o Shopify gerou outro). Pode deixar o template default por enquanto — a atribuição do template vem depois da publicação. Salva e me avisa."

- Se houver Admin API token/MCP conectado (`mcp__shopify__*`), crie via `pageCreate` em vez de pedir ao membro.
- No iteration loop (página já existe), pule este passo.
- Enquanto o tema não é publicado, o template `page.[produto]` não aparece no dropdown do admin Pages (só lista templates do tema LIVE) — por isso o preview usa `?view=[produto]`, que força o template alternativo.

### 6.7 Marker verification (Regra 4) — NUNCA pull pós-push não-verificado

```bash
curl -s "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO" | grep data-aura-build
```
- Marker encontrado com o hash atual → push OK.
- Página retorna 404 → a página não foi criada (volte ao 6.6) — NÃO é falha de push, não faça rollback.
- Página 200 mas marker ausente (ou hash ANTIGO) → push rejeitado silenciosamente (theme lock? rate limit 429? compile error? arquivo stale?). Diagnostique pela Regra 5 da `shopify-theme-safety.md` ANTES de qualquer pull. **Nunca pull depois de push não-verificado** (o tema remoto antigo sobrescreveria o trabalho local).

### 6.8 Smoke test (Regra 7) — antes de dizer "tá no ar"

```bash
curl -sI "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO"   # esperar 200
curl -s  "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO" | grep -E "(500|Liquid error)"   # esperar zero
curl -sI "https://$STORE/cart.js"   # esperar 200
```
- 404 aqui = página não criada no admin (6.6) — instrução ao membro, NÃO rollback.
- 500/`Liquid error` no corpo, ou `cart.js` fora do ar → falha real: rollback pro backup duplicado (Regra 6) e reporte antes de tentar de novo (ES4 oferece paths alternativos).
- Cobertura ampliada numa rodada só: `python3 .claude/lib/theme-verify/verify_page.py` checa overflow horizontal, presença das seções e erros de console em desktop+mobile de uma vez.

### 6.9 Preview links + aprovação do membro

```
Theme editor: https://$STORE/admin/themes/$NEW_THEME_ID/editor?template=page.$PRODUTO
Storefront:   https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO
```
O membro revisa o preview (é o gate humano antes do go-live). Iterou? Volte ao iteration loop. Aprovou? Siga pro 6.10.

### 6.10 PUBLISH (go-live — só com aprovação explícita)

Sem este passo a página vive pra sempre num tema unpublished: a 07d editaria o tema errado e a Skill 10 mandaria tráfego pago pra uma URL 404. O fluxo:

1. **Confirmação explícita** — publicar troca o tema da loja INTEIRA, não só a página: "Preview aprovado. Posso publicar o tema `[nome]`? Isso torna ele o tema live da loja (a página entra no ar em `https://$STORE/pages/$PRODUTO`)."
2. **Backup do live atual** (mais um rollback point além do 6.2):
   ```bash
   shopify theme duplicate --theme "$LIVE_THEME_ID" --name "BACKUP-$(date +%Y%m%d)-pre-publish" --store "$STORE" --force --json
   ```
3. **Publicar:**
   ```bash
   shopify theme publish --theme "$NEW_THEME_ID" --store "$STORE"
   ```
4. **Atribuir o template à página** (agora o dropdown lista): "Admin → Pages → `[produto]` → Theme template → seleciona `[produto]` → Save." Confirme com `curl -sI "https://$STORE/pages/$PRODUTO"` (200) + grep do `data-aura-build` na URL pública.
5. **Gravar no manifest** (contrato lido pela 07d — tema onde a página vive — e pela Skill 10 — URL de destino da campanha):
   ```json
   "storefront": { "theme_id": "<NEW_THEME_ID>", "page_url": "https://<STORE>/pages/<produto>", "published_at": "<ISO-8601>" }
   ```

Se o membro NÃO quiser publicar ainda (loja em construção), tudo bem — mas deixe explícito: "A página só existe no preview. Antes da Skill 10 (ads), a gente precisa publicar — a campanha usa a URL pública do `manifest.storefront.page_url`." NÃO grave `manifest.storefront` sem publicação (a 10 bloqueia sem ele, que é o comportamento certo).

> Aviso anti-drift: depois de publicado, NÃO edite as sections da Aura via Sidekick/AI do theme editor — isso cria drift silencioso entre o design aprovado e o que está no ar. Ajustes passam pelo iteration loop desta skill.

### 6.11 Fidelidade visual (screenshot da página no ar vs design aprovado — antes de encerrar)

"Compilou e passou nos gates" não é "ficou igual ao que o membro aprovou". O último check é olhar a página REAL com os próprios olhos, contra a fonte única de verdade:

1. **Screenshot full-page da página no ar** via Playwright (skill `webapp-testing`), em desktop (1440px) e mobile (390px). Publicou → use a URL pública (`manifest.storefront.page_url`); não publicou → rode sobre a preview URL (6.9) mesmo assim — o check não é opcional.
2. **Screenshot do `design/page.html` aprovado** (file://) nas MESMAS larguras (reuse os screenshots do self-review da 07a se ainda refletirem a versão aprovada).
3. **Compare os pares POR VISÃO**, ponto a ponto: ordem e presença das sections; tipografia (heading caiu pra serif/sans genérica? → o 6.4b falhou, volte lá); cores/tokens (CTA na cor errada = setting não populada); imagens (slot vazio, placeholder vazado, imagem esticada/cortada); spacing/hierarquia (section colada, padding sumido); FAQ/accordion funcionando (`<details>` renderizado).
4. **Divergência real → corrigir ANTES de encerrar a skill** (via iteration loop: ajuste no HTML aprovado + re-COMPILE da section, ou fix pontual no `.liquid`/template JSON + re-push + re-screenshot). Diferença trivial de rendering (anti-aliasing, scrollbar, fonte com hinting levemente diferente) não conta. **Nunca declare "no ar" com a página divergente do design que o membro aprovou.**
5. Se a página usa fonte custom, rode `python3 .claude/lib/theme-verify/font_census.py` — censo da fonte COMPUTADA elemento a elemento (declarar a família não é carregar); se tem seção animada (marquee/carrossel), rode `motion_check.py` com `--throttle` — bug de animação em mobile real só aparece com rede lenta + cache frio.
6. Registre no `deploy-report.json`: `"fidelity_check": {"passed": true, "compared_at": "<ISO>", "divergences_fixed": ["..."]}`.

---

## ETAPA 7 — Reports (dual output — rule 6b) + iteration loop

### Reports

Salve `page-report.md` (fonte pra AI) + `page-report.html` (humano) + `deploy-report.json`. O `.html` usa `.claude/templates/aura-report-template.html` (CSS inline, self-contained) e **abre com o bloco SVG da logo copiado LITERAL de `.claude/templates/aura-logo-snippet.html`** (rule 6b — NUNCA texto; o 07c/deploy antigo não tinha logo, agora tem). Componentes Aura, responsivo mobile.

Conteúdo do `.md`/`.html`: plano de sections + justificativa (de `page-plan.json`), brand signals usados (source), design system, variante aprovada, lista de arquivos com paths absolutos, settings expostos por section (resumo), **resumo da camada GEO** (nós Schema.org gerados + fatos do bloco agent-facts + o que ganha: discovery/citação por AI search, não venda-no-chat — seja honesto com o membro), fontes provisionadas (6.4b), preview links, resultado dos gates (compliance + promise-check + performance) e do fidelity check (6.11), issues conhecidas, histórico de iterações.

`deploy-report.json`:
```json
{
  "deploy_id": "<uuid>", "produto": "[slug]", "store": "<STORE>",
  "live_theme_id": "<LIVE_THEME_ID>", "theme_id": "<NEW_THEME_ID>",
  "cli_version": "<output de shopify version>",
  "preview_url_editor": "https://<STORE>/admin/themes/<NEW_THEME_ID>/editor?template=page.<produto>",
  "preview_url_storefront": "https://<STORE>/pages/<produto>?preview_theme_id=<NEW_THEME_ID>&view=<produto>",
  "sections_deployed": [{"id": "hero", "type": "page-<produto>-hero", "blocks_count": 0}, {"id": "benefits", "type": "page-<produto>-benefits", "blocks_count": 4}],
  "geo": {"jsonld_types": ["Product", "Offer", "AggregateRating", "BreadcrumbList", "FAQPage"], "jsonld_validated": true, "agent_facts_block": true, "schema_path": "workspace/<produto>/07-page/staging/geo/product-schema.json"},
  "gates": {"compliance": "pass", "promise_check": "pass", "performance": "pass"},
  "fonts_provisioned": {"method": "google_fonts | font_face | none_needed", "families": ["Fraunces", "Inter"], "verified_in_html": true},
  "validation_passed": true, "validation_errors": [], "push_warnings": [],
  "marker_verified": true, "smoke_test_passed": true,
  "fidelity_check": {"passed": true, "compared_at": "2026-MM-DDTHH:MM:SSZ", "divergences_fixed": []},
  "published": false, "page_url": null,
  "staging_dir": "workspace/<produto>/07-page/staging",
  "deployed_at": "2026-MM-DDTHH:MM:SSZ"
}
```

Atualize `manifest.json`: adicione `07b-page-build` a `skills_completed`; se ainda ausente, grave `store_url`; se o 6.10 publicou, o bloco `storefront` (`theme_id`/`page_url`/`published_at`) já foi gravado lá — confira que `published`/`page_url` do deploy-report batem com ele.

Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza o `ABRIR-AQUI.html`).

### Iteration loop (iteration-driven-refinement)

> "Página compilada, validada, gates passados e deployada (preview acima). Como o Liquid foi gerado deterministicamente do HTML que você aprovou, o theme editor é pixel-idêntico ao que você viu. Quer ajustar? Pode pedir 'hero mais apertado', 'cores mais escuras', 'features em 2 colunas', 'adicionar countdown na oferta'. Refino sem regenerar do zero."

Pra ajustes:
- **Só markup/schema/CSS de section** (spacing, layout, cor, texto, blocks novos dentro de section existente) → ajuste o HTML aprovado (`design/page.html`), re-rode SPLIT→COMPILE só da section afetada (Modo C single-section) OU edite o `{% stylesheet %}` direto → revalide → push APENAS das sections alteradas com `--only "sections/<arquivo>.liquid"`. O template JSON no ar não entra nesse push — as fotos, os textos e a ordem que o membro configurou no theme editor ficam intactos.
- **Estrutural** (section nova, remoção ou reordenação — mexe no template JSON) → NUNCA regenerar o template por cima do que está no ar: regenerar do preset apaga em silêncio as fotos e os textos que o membro configurou no editor. Fluxo da Regra 6b da `shopify-theme-safety.md`: `shopify theme pull --only` do template no ar → `python3 tools/theme-template-merge.py` (`--add`/`--remove`/`--move`) → push do template mergeado. A section nova em si compila e valida como sempre (validação de blocks — ETAPA 4) e sobe com `--only`.
- **Re-compile apaga renames E restaurações**: o conversor regenera o `.liquid` do zero — depois de qualquer re-COMPILE, re-aplique o rename semântico daquela section (ETAPA 2), re-rode a restauração de SVGs grandes dela (grep `icon-placeholder`), e recalcule o hash do `data-aura-build` se foi o hero.
- **Preço/rating/política mudou** → regenere o `product-schema.json` e o bloco agent-facts (ETAPA 4.5), revalide o JSON-LD, e confira que ainda bate com a config (Gate 2) antes do re-push. Schema e config nunca podem divergir.
- **FAQ mudou (pergunta adicionada/removida/reescrita na section faq)** → regenere o nó FAQPage do `product-schema.json` e revalide — as Q&A do Schema têm que continuar idênticas às da página.
- **SEMPRE pull antes de re-push** (Regra 1) pra preservar settings que o membro mexeu no editor.
- **SEMPRE** revalide com `shopify-plugin:shopify-liquid` + rode o snippet de validação do template JSON antes de cada push.
- Atualize `deploy-report.json` (`iterations: [...]` com timestamp + mudanças). Max 3 iterações sem progresso → escalate.

### Mensagem final

> "Page-build completo. [Se publicou: 'Página no ar em `<page_url>`.' / Se não: 'Página no preview — publica quando você aprovar; sem publicar, a campanha da Skill 10 não tem URL de destino.'] Próximo passo: 'tracking' (07c-tracking-setup — pixel + CAPI antes dos criativos), depois 'checkout' (07d-checkout-aov). Na sequência vêm o bônus Fase A (skill 05, se a sua oferta tem bônus) e a retention Fase A (skill 13 — flows de recuperação: abandoned cart + post-purchase, infraestrutura que se arma ANTES de ligar tráfego), e só então 'creatives' (skill 08)."

---

## Self-audit silencioso (rule post-task-self-audit) — deep audit (skill peso crítico)

Antes de declarar concluído, rode os 5 gates expandidos e corrija inline (sem mencionar): cada section do `section_order` virou um `.liquid` validado; template JSON tem `blocks{}` + `block_order[]` não-vazios em toda section **block-based** (schema define blocks) — sections monolíticas legitimamente ficam com `blocks: {}` (NÃO "corrija" injetando blocks fantasma); copy injetada veio de `06` (não inventada); **zero `icon-placeholder` residual nos `.liquid` (restauração de SVGs grandes da ETAPA 2 rodou) e zero placeholder `{{MAIÚSCULA}}` nas sections/template (check bloqueante da ETAPA 4)**; **nenhuma section com `media.required` sem imagem e nenhum `media.status: "placeholder"` sobrevivente do `page-plan.json`**; cores das section settings batem com `design-tokens.json`; **web fonts provisionadas (6.4b) e confirmadas no HTML servido — a tipografia aprovada não caiu pra fallback**; blocks `pricing_tier` expõem `qty` + `variant_id` (contrato da recipe deploy-shopify-product); **JSON-LD da ETAPA 4.5 valida (Product + BreadcrumbList no mínimo), todo campo vem de fonte real (nenhum rating/preço inventado — nó omitido se sem dado), e Schema + agent-facts + config são a MESMA verdade (envio/retorno/garantia/rating/preço)**; GATE 1, GATE 2 e GATE 3 (performance budget) passaram (sem override silencioso), incluindo o bloco agent-facts na varredura de compliance; marker `data-aura-build` verificado (hash atual) + smoke test OK antes de declarar "no ar"; **fidelity check do 6.11 rodou (screenshots por visão, live/preview vs design aprovado) e divergências reais foram corrigidas**; se publicou, `manifest.storefront` gravado com theme_id/page_url/published_at; logo SVG presente no `page-report.html`. Surface só o que exige decisão (gate `critical` sem rewrite seguro, promise `fail` que precisa escolha copy-vs-config, rating do Schema que diverge da review app e precisa escolha de qual fonte vale, publicar ou não o tema, placeholder de imagem que só o membro pode resolver).

---

# REFERÊNCIA TÉCNICA

Os ativos abaixo vinham da skill antiga `page-sections`. Aqui são **referência** que o conversor + a validação usam — não é geração manual de Liquid. O fluxo principal é determinístico (COMPILE via `liquid-converter.py`); esta seção explica o QUE o conversor produz e como debugar.

## Padrões aplicados pelo conversor (por código, determinísticos)

O que o `liquid-converter.py` (v3) REALMENTE aplica — valide o output contra esta lista, e NÃO afirme capacidade fora dela:

1. **Texto → settings (everything-editable)** — toda tag FOLHA com texto direto vira setting (inclui `<div class="price">$49</div>`, eyebrows em div). Texto misto com inline tags (`<em>/<strong>/<br>`) vira `inline_richtext` (tags preservadas, attrs removidos); `<p>` longo (>80 chars) vira `richtext`. Dedup: texto idêntico reutiliza o MESMO setting (2 CTAs "Buy Now" = 1 `cta_label`).
2. **Cores (CRÍTICO)** — toda cor extraída vira `color` setting E é injetada INLINE no root da section via `style="--c-x: {{ section.settings.color_x | escape }}; ..."` (NUNCA só em `:root` do stylesheet, senão o theme editor não aplica). `| escape` em TODA interpolação dentro de `style=""` — sem isso, aspas internas (`"Playfair Display", serif`) fecham o atributo e órfãm as vars seguintes. O merge respeita `style=""` existente no root.
3. **Tokens de design → settings** — `box-shadow`/`border-radius`/`font-size`/`font-family` viram `var(--x)` + setting, com migração automática de usages hardcoded no CSS (migrados ANTES das cores — shadow com hex vira 1 setting de shadow, não setting morto).
4. **Imagens → `image_picker`** + selects de aspect-ratio e fit, com `image_url | image_tag` responsivo.
5. **CTA de compra → form `/cart/add` nativo** (detecção por classe/texto/href) com settings `variant_id`/`quantity`/`after_add` e fallback URL (degrada pra `<a>` quando variant vazio). Form POST dispara `cart_updated` no Shopify Web Pixel → propaga AddToCart pra Meta Pixel/CAPI/GA4/TikTok. `<a href="/cart/add?id=X">` (GET) quebra essa cascade — pixel cego.
6. **Blocks inline com copy real por instância** — padrão repetido (cards/tiers/reviews/faq) vira block LOCAL no schema da section (`{% for block in section.blocks %}{% case block.type %}`), TODOS os itens convertidos com os defaults DAQUELE item (FAQ de 5 = 5 instâncias distintas). Irmãos fora do padrão (ex: cta-row no fim do grid) são preservados no markup.
7. **CSS por section** — `:root/html/body` rescopados pro namespace; o `page.css` é FILTRADO pras regras que a section usa (sem N cópias do CSS no tema).
8. **Schema names ≤ 25 chars** (section e blocks) — automático, com validação interna (`validate_shopify_schema`: types válidos, ids únicos, labels).
9. **`<script>` removidos COM warning** listando cada um — reimplementar a interação de forma nativa (`<details>` pra FAQ) em vez de perder silenciosamente. `<svg>` grandes viram placeholder.

**O que o conversor NÃO faz (passo manual do Claude quando a página precisar — nunca afirmar como automático):**

- **Ícones em 3 camadas** (preset enum + `icon_custom_svg` + `none`) — SVG >500 chars vira placeholder, SVG pequeno fica inline. Se o design pede ícones editáveis, o Claude adiciona os settings à mão.
- **`countdown_banner` / Subscribe & Save / selling plan** — não gerados. Se a oferta pede countdown, implementação manual respeitando a regra: deadline FIXO real (sale end/launch/drop), NUNCA rolling per-user nem reset evergreen (Meta detecta fake scarcity → disapproval). Subscribe & Save: `<input type="radio" name="selling_plan" value="ID">` do app de subscription.
- **"Regra dos 4 headers" e `custom_css` por block** (`#pu-{{ block.id }}`) — não gerados; adicionar manualmente só se o membro precisar de override fino por block.
- **Texto solto misturado com sub-árvores** (`<div>Texto <div>...</div></div>`) fica hardcoded — reestruture o HTML no design se precisar editável.
- **Cores em `style=""` inline do HTML de origem** não são tokenizadas (só no CSS).
- **Validação semântica de Liquid** — o schema JSON é validado por código, mas rodar `shopify-plugin:shopify-liquid` em cada arquivo continua obrigatório (ETAPA 3).

## Catálogo de Block Types

Este catálogo é o **vocabulário de conteúdo** pro rename semântico (ETAPA 2) — NÃO é a lista de settings que o conversor emite (ele deriva os settings do markup real de cada item; os "Settings-chave" abaixo são referência do que costuma existir, e `custom_css` é adição manual opcional, nunca automática). Realização concreta: conteúdo de instância ÚNICA (1 eyebrow, 1 heading, 1 CTA num hero) vira **section setting** (grupo Content, editável); conteúdo REPETÍVEL (vários cards/tiers/reviews/faq items) vira **block** (`{% case block.type %}`, arrastável/reordenável). O `{% case %}` gerado contém só o(s) type(s) do padrão repetido detectado — os "universais" NÃO são gerados como block types; aparecem como settings quando o conteúdo é único.

**Universais (conteúdo estrutural — settings quando único; vocabulário de nomeação quando o padrão repetido cai numa dessas categorias):**

| Block | Uso | Settings-chave |
|---|---|---|
| `eyebrow` | Label acima de headings | text · size · weight · transform · tracking · color · space b/a · **custom_css** |
| `heading` | Título (h1/h2/h3) com `<em>` | text (inline_richtext) · size · font · weight · color · line_height · letter_spacing · max_width · **custom_css** |
| `paragraph` | Texto longo | text (richtext) · size · color · line_height · max_width · **custom_css** |
| `badge` | Pill/chip com dot | text · show_dot · dot_color · variant · bg · text_color · radius · **custom_css** |
| `button_row` | Até 3 botões inline | alignment · gap · radius · por botão (show/label/url/variant/bg/text/price) · **custom_css** |
| `stats_bar` | Até 5 stats em grid | columns · gap · show_divider · por stat (show/label/value inline_richtext) · **custom_css** |
| `trust_row` | Até 6 trust items | alignment · gap · show_divider · por item (icon/label) · **custom_css** |
| `tag` | Floating tag sobre imagem | eyebrow · title · position (tl/tr/bl/br) · rotation · theme · bg · text · radius · **custom_css** |
| `divider` | Linha separadora | style · color · thickness · width% · **custom_css** |
| `icon` | Ícone isolado | icon · size · color · **custom_css** |
| `spacer` | Espaço vertical | height · **custom_css** |
| `custom_liquid` | Escape hatch (`type: "liquid"`) | code · **custom_css** |
| `custom_html` | HTML estático (`type: "html"`) | html · **custom_css** |

**Type-specific (além dos universais):**
- Benefits → `benefit_card` (num/icon + title + body + accent)
- Proof / social-proof → `review_card` (stars + quote + author + avatar + featured)
- Offer → `pricing_tier` (name + price + strap + features richtext + CTA form `/cart/add` + **`qty` + `variant_id`** — contrato da recipe deploy-shopify-product + badge + popular + image) · `countdown_banner` (limit 1; implementação manual — o conversor não gera)
- Guarantee → `promise_item` (title + body + accent + icon)
- FAQ → `faq_item` (question + answer richtext + open_by_default) — usar `<details><summary>` nativo
- Mechanism → `mechanism_card` / `ingredient_card` / `process_step` / `science_card` (nomeie conforme o mecanismo real)
- Before-after → `comparison_pair` (before_image + after_image + label)
- Ingredients → `ingredient` (name + role + dosage + image)
- How-it-works → `step` (number + title + description + image)

**Regra dos 4 headers (organização manual opcional):** Content (o quê) · Style (como) · Spacing (onde) · Advanced (custom_css com `id="pu-{{ block.id }}"` + `<style>` scoped). O conversor NÃO emite isso automaticamente — é padrão de organização pro Claude aplicar à mão quando um block precisa de controle fino.

**Blocks inline no schema, NUNCA theme blocks em `/blocks/*.liquid`** com `{% content_for 'block' type: block.type %}` — o validator do Shopify bloqueia vars dinâmicas ("The 'id' argument should be a string"). O conversor gera inline (nenhum `blocks/*.liquid` é escrito; `--blocks-dir` é deprecado e ignorado).

## Limitações Shopify conhecidas (o conversor + validação respeitam)

1. `<img>` precisa `width`+`height` — usar `image_tag` (auto-adiciona): `{{ image | image_url: width: 1600 | image_tag: loading: 'lazy' }}`.
2. `url` setting não aceita `#anchor` como default — só `http(s)://` ou `/path/`. Deixe default vazio.
3. `inline_richtext` não aceita attributes em tags — só `<em>`, `<strong>`, `<br>`, `<span>`, `<a>`, `<u>`, `<p>` sem attrs.
4. `richtext` wrapa em `<p>` automático — não envolva em `<p>` no markup (evita `<p><p>`).
5. Aspect-ratio: use `data-adapt="true"` + seletor `[data-adapt='true']` (o conversor já faz).
6. Dropdown "Theme template" do admin Pages só lista templates do tema LIVE.
7. `shopify theme duplicate` precisa `--force` em contexto não-interativo.
8. Package-lock do plugin aponta pro registry privado `npm.shopify.io` — se `validate.mjs` falha com `ERR_MODULE_NOT_FOUND`, rode no dir do plugin: `rm package-lock.json && npm install --registry=https://registry.npmjs.org/`.
9. Range settings: max 101 steps. `(max - min) / step ≤ 100`.
10. Range default deve alinhar ao step: `(default - min) % step == 0`.
11. **Preset de section ≠ blocks em template JSON.** Section entry sem `blocks` (ou `blocks: {}` vazio) renderiza ZERO blocks. O POPULATE (ETAPA 4) resolve isso emitindo `blocks: {...}` + `block_order: [...]` explícitos.
12. Blocks inline (`{% case block.type %}`) passa; theme blocks em `/blocks/*.liquid` com `{% content_for 'block' %}` dinâmico FALHA.
13. `inline_richtext` renderiza HTML no browser mas o preview editor pode mostrar raw — use `info` no setting.
14. Custom Liquid em block: `type: "liquid"` (pré-renderiza no push); `type: "html"` é estático XSS-safe.
15. `shopify page create` não existe na CLI — a criação da página é o passo 6.6 do DEPLOY (membro no admin, com handle exatamente `[produto]`, ou `pageCreate` via Admin API/MCP quando conectado). Sem a página criada, o storefront responde 404 (não é falha de push); o theme editor URL (`?template=page.[produto]`) roda mesmo sem a página existir.
16. **Default de `richtext`/`inline_richtext` sem `<p>` = arquivo inteiro rejeitado em silêncio.** O valor default de um setting `richtext` no schema (e o valor correspondente em template JSON) PRECISA ser `"<p>...</p>"` — texto puro faz o Shopify rejeitar O ARQUIVO INTEIRO em silêncio: o push reporta ok, o servidor mantém a versão velha, e nenhum erro de validação aparece. Mesmo sintoma pra setting `text` com default `""` (use ausência de default). Diagnóstico: bisection de settings — remova metade dos defaults, pushe, confira o marker `data-aura-build`; repita até isolar o campo culpado.
17. **Filtro encadeado DENTRO de argumento nomeado quebra o Liquid em runtime.** `style: 'x' | append: var | append: 'y'` dentro de `image_tag` (ou qualquer filtro com argumentos nomeados) estoura `wrong number of arguments (given 3, expected 2)` SÓ em runtime — a página quebra com o setting preenchido e funciona com ele vazio (o sintoma parece "a imagem sumiu"). Regra: assign-first SEMPRE — monte a string completa num `{%- assign -%}` e passe a variável pronta como valor do argumento.
18. **`image_picker` não aceita default de imagem arbitrária** — só datasource `shopify://shop_images/...`. Section que exige imagem trata a ausência com placeholder explícito no Liquid, nunca com default no schema.

## Debug — Quando validação ou push falha

| Mensagem (trecho) | Causa | Solução |
|---|---|---|
| `Missing width and height attributes on img tag` | `<img>` sem dimensões | `image_tag` filter (conversor já aplica) |
| `default must be a string or datasource access path` | `url` default com `#anchor`/relativo | default vazio ou absoluto |
| `invalid inline richtext: Attribute 'X' is not permitted` | `inline_richtext` com class/aria/data | strip attrs (só tags simples) |
| `Range settings must have at most 101 steps` | `(max-min)/step > 100` | aumentar step / reduzir range |
| `default must be a step in the range` | default não múltiplo do step | `(default-min) % step == 0` |
| `Opening tag does not have a matching closing tag` | HTML quebrado em `{% if %}` | atributos/classes condicionais, não tags partidas |
| `The 'id' argument should be a string` | theme block dinâmico `{% content_for 'block' %}` | refatorar pra blocks inline `{% case block.type %}` |
| `Section type 'X' does not refer to an existing section file` | template JSON referencia section não instalada | push a section antes; conferir ordem do `cp` |
| Blocks aparecem vazios na preview | `blocks: {}` no template JSON | rodar o snippet de validação da ETAPA 4 |
| Cor mudada no editor não aplica | CSS var hardcoded em `:root` em vez de inline no root | Padrão 2 da seção Padrões (conversor injeta inline; se quebrou, re-COMPILE) |
| Meta Pixel não registra AddToCart | CTA `<a href="/cart/add?id=X">` em vez de form POST | Padrão 5 da seção Padrões (conversor gera form `/cart/add` nativo) |
| Push trava esperando confirmação (tema LIVE) | falta `--allow-live` | adicionar flag |
| `ERR_MODULE_NOT_FOUND @shopify/theme-check-common` | registry privado do plugin | `rm package-lock.json && npm install --registry=https://registry.npmjs.org/` |

## Acessibilidade — checklist WCAG 2.1 AA (quality standard universal)

Regras universais que NÃO restringem design — garantem que qualquer página seja usável por todos. O `frontend-design` (07a) já respeita; valide no output compilado:

- **Semântica:** `<h1>` 1×/página (hero); heading order sem pular níveis; `<section>/<article>/<header>/<main>` onde aplicável; `<button>` pra ações, `<a href>` pra navegação; FAQ com `<details><summary>` nativo.
- **Alt/labels:** todo `<img>` com `alt` descritivo (ou `alt=""` decorativo); `<button>` só-ícone com `aria-label`; ícone decorativo `aria-hidden="true"`; links com texto descritivo (nunca "clique aqui"); `<label for>` em forms.
- **Contraste:** texto normal ≥ 4.5:1; texto grande ≥ 3:1; UI/focus rings ≥ 3:1; cor nunca é o único indicador de estado. Liquid `color_contrast` filter valida.
- **Foco/teclado:** `:focus-visible` com outline visível em todo interativo; tab order = ordem visual; nada escondido atrás de hover-only; modais com focus trap.
- **Movimento:** `@media (prefers-reduced-motion: reduce)` desligando transitions/animations; auto-play com pause; nada piscando >3×/s.
- **Responsividade:** funciona em 320px; texto nunca em px pequeno (clamp, mínimo ≥14px body); touch targets ≥ 44×44px; legível a 200% zoom.

Validação: Lighthouse Accessibility ≥ 95; navegação só-teclado; VoiceOver/NVDA (headings + labels fazem sentido).

## DO NOT

- Usar o block NATIVO `custom_liquid` do Shopify (HTML cru não-editável). O nosso `custom_liquid` customizado (`type: "liquid"`) é OK porque é editável.
- Hardcode texto/imagens/cores no markup (sempre settings).
- Usar classes do tema pai (`.product-card`, `.btn`) — sempre namespace próprio (`page-[produto]-X`).
- Usar `asset_url`/caminhos hardcoded de imagem (sempre `image_picker`).
- `!important` em CSS; IDs em selectors (use classes).
- Importar libraries JS/CSS externas; jQuery/React/Vue/Tailwind no output final (vanilla CSS em `{% stylesheet %}`).
- Salvar um `.liquid` sem validar com `shopify-plugin:shopify-liquid`.
- Pushar no live sem backup + `--allow-live` + `--nodelete`.
- Pushar snippet/asset de paleta em lote genérico quando há mais de um tema ativo com paletas diferentes — arquivo de identidade é POR-TEMA (rule `shopify-theme-safety`, disciplina multi-tema).
- Pull depois de push não-verificado (marker ausente) — sobrescreve trabalho local.
- Criar sections que "só funcionam no Horizon" — sempre theme-agnostic, self-contained.
- Gerar Liquid por reasoning manual em vez de rodar o `liquid-converter.py` — a conversão é determinística por design.

## Como invocar specialists

| Specialist | Skill name |
|---|---|
| **Validação Liquid** (crítico) | `shopify-plugin:shopify-liquid` |
| Geração/ajuste de HTML (07a; iteration) | `frontend-design` |
| Captura de screenshot (signals 07a; fidelity check 6.11) | `webapp-testing` |

A validação Liquid é parte do plugin Shopify AI Toolkit (`/plugin marketplace add Shopify/shopify-ai-toolkit` + `/plugin install shopify-plugin@shopify-plugin`). Sem ele, instrua a instalar antes.

## Referências cruzadas

- **Skill anterior:** `07a-page-design` (gera o `design/page.html` aprovado + `design-tokens.json` + `page-plan.json` que esta skill consome)
- **Conversor canônico:** `tools/design-clone/liquid-converter.py` (batch: `--batch <manifest.json> --emit-template-json`; Modo C: `--html --css --type --output --namespace --product-slug --emit-template-json --page-handle`; `--blocks-dir` é deprecado/ignorado; Modo B legacy exige `--allow-competitor-markup`)
- **Contrato de publicação:** `manifest.storefront` (`theme_id`/`page_url`/`published_at`, gravado no 6.10) — a 07d opera no tema onde a página vive e a Skill 10 lê `page_url` como destino da campanha
- **Próxima no fluxo:** `07c-tracking-setup` (pixel + CAPI antes dos criativos) → `07d-checkout-aov` → `05-bonus-delivery` Fase A (se a oferta tem bônus) → `13-retention-engine` Fase A (flows de recuperação: abandoned cart + post-purchase) → `08-creative-engine`
- **Gate de launch:** `09-consistency-audit` (pré-requisito da skill 10, não do deploy da página)
- **Camada GEO (ETAPA 4.5):** JSON-LD Schema.org (Product + Offer + AggregateRating + BreadcrumbList + FAQPage das perguntas reais) de `04-offer-builder/dados.json` + `06-copy-engine/dados.json` + reviews, validado antes de injetar, mais o bloco agent-facts — pra citação por ChatGPT/Perplexity/Google AI Mode. Validação externa opcional pós-deploy: Google Rich Results Test + validator.schema.org.

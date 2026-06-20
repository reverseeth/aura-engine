---
name: page-build
description: Segunda skill da fase STOREFRONT. COMPILE determinístico do design/page.html aprovado na 07a em sections Liquid via liquid-converter.py (Modo C, por código não por reasoning), valida cada section com shopify-plugin:shopify-liquid (3 retries), POPULATE do templates/page.[produto].json com blocks pré-populados, roda os gates de launch (compliance + promise↔config) e faz DEPLOY seguro no Shopify (shopify-theme-safety integral). Use quando o membro disser "build page", "deploy", "subir página", depois de aprovar o design na 07a.
---

# 07b — Page Build (COMPILE determinístico + POPULATE + DEPLOY)

Segunda e última skill da fase **STOREFRONT** (07a → 07b). A 07a produziu o `design/page.html` aprovado — a FONTE ÚNICA DE VERDADE visual. Esta skill **compila esse HTML em Liquid por CÓDIGO, não por reasoning**, popula o template com a copy real, passa os gates de launch e deploya no Shopify.

Princípio: **conversão determinística mata as traduções lossy e o drift.** O Liquid é gerado mecanicamente do HTML aprovado via `tools/design-clone/liquid-converter.py` (Modo C). O Claude entra só pra (a) splitar o HTML por section, (b) nomear blocks semanticamente, (c) validar. O conversor aplica os 6 padrões críticos por código — impossível de esquecer.

**O que esta skill faz:**

1. Pré-flight — exige `design/page.html` aprovado + `design-tokens.json` + `07-plan.json`.
2. SPLIT — separa o HTML aprovado em fragmentos por section (via marcadores `data-aura-section`) + o CSS.
3. COMPILE — roda `liquid-converter.py` Modo C por section (CLI exato).
4. VALIDATE — cada `.liquid` passa por `shopify-plugin:shopify-liquid` (3 retries).
5. POPULATE — o conversor emite `templates/page.[produto].json` com blocks/block_order/settings populados com a copy real (ordem reversa).
5.5. GEO / Schema (agent-readability) — gera o JSON-LD Schema.org (Product + Offer + AggregateRating + BreadcrumbList) de `04-offer.json` + `06-copy.json` + reviews, valida, e injeta no template como bloco `custom_liquid` + um bloco "agent-readable facts" (specs, envio/retorno, disponibilidade, garantia) em texto limpo separado da copy persuasiva.
6. GATES (blocking) — GATE 1 compliance (ad-flag) + GATE 2 promise↔config, ANTES do deploy.
7. DEPLOY — shopify-theme-safety integral (duplicate → pull --nodelete → push --allow-live --nodelete + marker verification + smoke test).
8. Dual output (.md + .html, logo SVG) + iteration loop.

**Outputs em `workspace/[produto]/07-page/`:** `staging/sections/page-[produto]-*.liquid`, `staging/blocks/*.liquid` (se houver), `staging/templates/page.[produto].json`, `staging/geo/product-schema.json` (JSON-LD), `staging/geo/agent-facts.html`, `07-page.md` + `07-page.html`, `07-deploy-report.json`.

---

## Pré-flight

1. Leia `workspace/profile.md` → `report_language` (default `pt-BR`; também em `manifest.report_language`). Relatórios internos e conversa nesse idioma. Copy consumidor-final permanece em inglês US.
2. **Gate de consistência (skill 09)** — leia `workspace/[produto]/09-consistency-audit.json` se existir:
   - `launch_recommendation == "BLOCK"` → o deploy da página NÃO está bloqueado por si só (a página existir não gasta dinheiro), mas avise o membro dos items críticos e recomende rodar `consistency audit` de novo. O gate 09 é pré-requisito do **LAUNCH** (gateia a skill 10), não do deploy da página.
   - `"CAUTION"` → mostre warnings, peça confirmação.
   - `"GO"` ou ausente → siga (recomende rodar a 09 antes do launch).
3. Valide os inputs (sob `workspace/[produto]/07-page/`):
   - [ ] `design/page.html` existe (HTML aprovado da 07a — **sem ele, PARE e direcione pra 07a**; não existe modo "gera Liquid direto")
   - [ ] `design-tokens.json` existe e parseia
   - [ ] `07-plan.json` existe com bloco `strategy` + `sections_plan` + `section_order`
   - [ ] `manifest.json` tem `07a-page-design` em `skills_completed`
   - [ ] Plugin `shopify-plugin:shopify-liquid` disponível (se falhar, instrua `/plugin install shopify-plugin@shopify-plugin`)
4. Dirs de staging: `workspace/[produto]/07-page/staging/{sections,blocks,templates,geo}/` (criar com `mkdir -p`).

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
STORE=""  # preenchido na detecção da loja (ETAPA 7)
```

---

## ETAPA 1 — SPLIT (HTML aprovado → fragmentos por section)

O `design/page.html` aprovado tem cada section marcada com `<section data-aura-section="hero">` etc (a 07a pediu isso ao `frontend-design`). Splite:

1. Parse do `design/page.html`. Pra cada `<section data-aura-section="X">`, extraia o fragmento HTML completo daquela section → salve em `${STAGING_DIR}/html/<X>.html`. Os ids `X` batem com `sections_plan[].id` de `07-plan.json`.
2. Extraia o CSS (do `<style>` do documento, ou do `.css` companion se houver) → `${STAGING_DIR}/html/page.css`. O conversor injeta isso no `{% stylesheet %}` de cada section (namespaced).
3. **Se os marcadores `data-aura-section` faltarem** (HTML antigo ou editado à mão): splite por âncoras/headings de section seguindo o `section_order` de `07-plan.json`, ou peça à `frontend-design` pra re-emitir o HTML com os marcadores. Não chute fronteiras de section.

Resultado: N fragmentos HTML (1 por section do plano) + 1 CSS compartilhado.

---

## ETAPA 2 — COMPILE (liquid-converter.py Modo C, por section)

O `liquid-converter.py` é o conversor **CANÔNICO e OBRIGATÓRIO** (não é mais "legacy/draft" — é o caminho determinístico). Ele aplica por código os 6 padrões críticos (ver seção **Padrões aplicados pelo conversor** abaixo): color settings inline no root + `| escape`, shadow/radius/font como `var(--x)`+setting+migração de hardcoded, form `/cart/add` nativo, everything-editable, ícones 3 camadas.

Pra **cada section**, rode (CLI exato — Modo C):

```bash
python3 ${TOOLS_DIR}/liquid-converter.py \
  --html ${STAGING_DIR}/html/<id>.html \
  --css ${STAGING_DIR}/html/page.css \
  --type <id> \
  --output ${STAGING_DIR}/sections/page-${PRODUTO}-<id>.liquid \
  --blocks-dir ${STAGING_DIR}/blocks \
  --namespace page-${PRODUTO}-<id> \
  --product-slug ${PRODUTO}
```

- `<id>` = o id da section (`hero`, `benefits`, `mechanism`, `offer`...) de `sections_plan`.
- O conversor extrai cores → CSS vars + color settings, detecta padrões repetíveis → blocks, faz dedup de settings, naming semântico, e valida o schema internamente (`validate_shopify_schema`).
- **O Claude entra depois pra nomear blocks semanticamente** (o conversor dá nomes genéricos a partir das classes BEM; renomeie pros type-specific certos: `benefit_card`, `pricing_tier`, `review_card`, `faq_item`, `mechanism_card` conforme o Catálogo) e pra conferir que os universais (`eyebrow`, `heading`, `paragraph`, `button_row`, `divider`, `spacer`, `custom_liquid`, `custom_html`) e os type-specific da section estão presentes no `{% case block.type %}`.

### Batch (modo wrapper, se disponível)

Se o conversor expõe o modo batch (GAP-E), uma única invocação converte a página inteira (loop por section) e já chama o POPULATE — preferível a orquestrar N chamadas à mão. Use o batch quando existir; senão, loop manual por section (acima).

---

## ETAPA 3 — VALIDATE (shopify-plugin:shopify-liquid, 3 retries)

Cada `.liquid` gerado passa pelo skill `shopify-plugin:shopify-liquid` (modo validate). Protocolo determinístico (3 tentativas):

1. **Validate** — se OK, próxima section.
2. **Auto-fix + revalidate** — modo `fix` do plugin, revalida.
3. **Leitura manual do erro** — consulte a tabela **Debug — Quando validação falha** (abaixo), aplique o fix, revalide. Se ainda falhar → **PARE e reporte** ao membro (arquivo, erro exato, tentativas, ação manual sugerida).

Comando manual (se o plugin estiver indisponível):
```bash
node .../shopify-liquid/scripts/validate.mjs --filename page-${PRODUTO}-<id>.liquid --filetype sections --code "$(cat <file>)" --model ... --client-name claude-code --artifact-id ${PRODUTO}-<id> --revision 1
```

---

## ETAPA 4 — POPULATE (template JSON com blocks pré-populados)

**Modelo de blocks vs settings:** o conversor emite conteúdo ÚNICO (hero headline, eyebrow, sub, CTA único) como **section settings** (grupo Content — editável no theme editor) e conteúdo REPETÍVEL (benefit cards, pricing tiers, review cards, FAQ items, ingredients, steps) como **blocks** arrastáveis/reordenáveis. Ambos vêm com a copy real pré-preenchida. Sections monolíticas (só settings) são válidas e comuns (ex: hero).

**Erro #1 histórico (vale só pra sections COM blocks):** quando uma section É block-based (schema define block types repetíveis), o `templates/page.[produto].json` precisa ter `blocks: {...}` + `block_order: [...]` EXPLÍCITOS — senão renderiza ZERO daqueles blocks (o Shopify só popula preset blocks quando o membro adiciona a section manualmente via "Add section"). O POPULATE resolve isso. Sections monolíticas (settings-only) legitimamente têm `blocks: {}` e renderizam do markup direto.

O conversor emite o template JSON populado (GAP-B). Rode o POPULATE via os flags novos do conversor:

```bash
python3 ${TOOLS_DIR}/liquid-converter.py \
  --html ${STAGING_DIR}/html/<id>.html \
  --css ${STAGING_DIR}/html/page.css \
  --type <id> \
  --output ${STAGING_DIR}/sections/page-${PRODUTO}-<id>.liquid \
  --blocks-dir ${STAGING_DIR}/blocks \
  --namespace page-${PRODUTO}-<id> \
  --product-slug ${PRODUTO} \
  --emit-template-json ${STAGING_DIR}/templates/page.${PRODUTO}.json \
  --page-handle ${PRODUTO}
```

- `--emit-template-json <path>` — o conversor monta/atualiza `templates/page.[produto].json`, inserindo a section convertida com `blocks{}` + `block_order[]` + `settings{}` populados, usando a copy real do HTML como `default` de cada setting.
- `--page-handle <handle>` — handle da página no template.
- **Inserção em ordem reversa** (rule `reverse-order-insertion`): quando o conversor (ou o Claude, se ajustar o JSON à mão) insere múltiplas sections no `order[]`/`sections{}`, insere da maior posição pra menor pra não deslocar índices. No modo batch o conversor já cuida disso.
- As cores das section settings vêm de `design-tokens.json` (role-tagged: background/surface/foreground/primary/accent/border).

### Validação do template JSON (OBRIGATÓRIA antes do deploy)

Pra cada section em `sections`:
- [ ] Se a section é **block-based** (schema do `.liquid` define block types), `blocks` é objeto **não-vazio** com `block_order`. Sections **monolíticas** (só settings, ex: hero) legitimamente têm `blocks: {}` — não é erro (o snippet abaixo já distingue os dois casos)
- [ ] `block_order` referencia apenas chaves de `blocks`; todo block de `block_order` existe em `blocks`
- [ ] Todo block tem `type` válido presente no schema da section `.liquid` correspondente
- [ ] `order[]` lista todas as sections na sequência persuasiva (`section_order` de `07-plan.json`)
- [ ] Copy REAL populada (hero headline, sub, CTAs, stats, benefits VOC, tiers, FAQ Q+A, CTA final) — tudo de `06-copy`

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

---

## ETAPA 4.5 — GEO / Schema (agent-readability — citação por AI search)

A loja precisa ser **legível por máquina**, não só por humano. ChatGPT, Perplexity e o Google AI Mode citam páginas que entregam fatos estruturados e verificáveis em vez de copy persuasiva crua. O Shopify já liga Agentic Storefronts por default, então o crawler de AI passa nessa página de qualquer jeito — a questão é se ele acha o que precisa pra te citar. Páginas com Schema.org completo são citadas com muito mais frequência que páginas sem (a diferença é grande). É barato (texto + um bloco JSON) e vira um moat que poucos concorrentes têm.

**Honestidade com o membro (não vender fantasia):** o ganho HOJE é **discovery e citação** — aparecer na resposta do ChatGPT/Perplexity quando alguém pesquisa o problema que o produto resolve, com a loja linkada como fonte. NÃO é "venda fechada dentro do chat" (esse fluxo de checkout agêntico ainda está engatinhando). O que se constrói agora é presença na camada de AI search antes dos concorrentes — quando a venda-dentro-do-chat amadurecer, quem já tem Schema limpo larga na frente. Posicione assim, sem prometer receita imediata.

Esta etapa NÃO toca o design visual nem a copy persuasiva. Ela adiciona duas camadas invisíveis pro consumidor humano e visíveis pro crawler: (1) o **JSON-LD Schema.org** no `<head>`/markup, (2) um bloco de **fatos legíveis por agente** em texto limpo.

### 4.5.1 — Montar o JSON-LD (Product + Offer + AggregateRating + BreadcrumbList)

Leia as fontes (todas já existem na cadeia; não invente nenhum campo):

- `workspace/[produto]/04-offer.json` → nome do produto, preço, `compare_at_price`, moeda, garantia (dias), unique mechanism, descrição da oferta.
- `workspace/[produto]/06-copy.json` → headline/descrição do produto, specs/benefícios em texto, brand.
- **Reviews** → `04-offer.json` (se traz `social_proof`/`rating`) OU a review app real (Judge.me/Loox/Yotpo via Admin API, se conectada) OU o número que o GATE 2 já valida em `promise-check.json`. **O rating do Schema TEM que bater com o rating exibido na página e com a review app real** (senão é structured-data fraudulento — Google penaliza e pode disparar manual action).

**Regra dura — sem dado, sem nó.** Se um campo não tem fonte real (ex: rating sem review app conectada, ou `compare_at_price` ausente), **OMITA o nó/propriedade** em vez de inventar. `AggregateRating` só entra se há reviews reais e contáveis. Schema com número fabricado é pior que Schema ausente (vira manual action no Google Search Console).

Monte `staging/geo/product-schema.json` com este shape (preencha dos arquivos, sem placeholders soltos):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Product",
      "name": "<04-offer product_name>",
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
          "merchantReturnDays": "<dias de garantia de 04-offer>",
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
    }
  ]
}
```

Notas de montagem:
- **Coerência com o GATE 2** (ETAPA 5): `merchantReturnDays`, `returnFees` (free vs paid), `shippingDetails` (free shipping vs cobrado) e `priceValidUntil` (promo time-bound) TÊM que bater com o que `promise-check.json` valida contra a config real da Shopify. Se a promise de free shipping só cobre US, o `shippingDestination` é US — não invente cobertura mundial. **O Schema é mais uma superfície onde a promise tem que ser verdade** (Gate 2 cobre isso na ETAPA 5; se o Schema diverge da config, o gate barra).
- `availability` reflete o estoque real (`InStock`/`OutOfStock`/`PreOrder`).
- `priceValidUntil`: só se há promo com data-fim FIXA real (mesma regra do countdown — Padrão 6; nunca rolling/evergreen).
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
if errors: print("\n".join(errors)); raise SystemExit(1)
print("JSON-LD válido:", ", ".join(sorted(types)))
```

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
| **Specs do produto** | `06-copy.json` / `04-offer.json` | "30ml serum. 0.5% encapsulated retinal. Fragrance-free, vegan." |
| **Envio** | config Shopify (mesma do Gate 2) | "Free US shipping. Ships in 1–2 business days from [state]." |
| **Retorno / garantia** | `04-offer.json` (dias) + policy page | "90-day money-back guarantee. Free returns by mail." |
| **Disponibilidade** | estoque real | "In stock. Ships immediately." |
| **Garantia/durabilidade** | `04-offer.json` | "Each bottle lasts ~60 days at the recommended use." |
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

Os dois gates da rule `pre-launch-gates.md` rodam sobre a copy injetada ANTES do push. **Inclua o bloco agent-facts (ETAPA 4.5.4) na varredura do GATE 1** (é consumer-facing) e confira que o JSON-LD (ETAPA 4.5.1) não contradiz a config real no GATE 2 (envio/retorno/garantia/rating/preço são a mesma verdade da página).

### GATE 1 — Ad-flag compliance

Rode sobre TODA a copy injetada nas sections/template:
```bash
python3 .claude/lib/compliance-preflight/run.py \
  --input "<toda a copy consumidor-final do template JSON>" \
  --config .claude/lib/compliance-preflight/red_flags.json \
  --schema .claude/lib/compliance-preflight/output-schema.json
```
Decisão: `critical` → **BLOCK** (apresenta `rewrite_suggestion`, pede revisão). `high` → BLOCK por default, aplica rewrite automático e re-roda; se passar (low/medium), prossegue. `medium` → WARN (loga em `workspace/[produto]/compliance-warnings.json`, notifica). `low` → PASS.

Também cheque: zero travessão em headlines, ≤2 em copy longa (rule 8a); zero emoji na UI da página (rule 7 — ícones SVG).

### GATE 2 — Promise ↔ Config

Pra cada promise na copy/página (free shipping, "90-day money-back", "Use code XXXX", "Limited time — ends [date]", "Rated 4.X by N", "Made in [country]", "FDA cleared"), valide contra a config real da loja Shopify (shipping zones, policy pages, discount codes, review app, regulatório). Output em `workspace/[produto]/promise-check.json`. `fail ≥ 1` → **BLOCK deploy** com `fix` sugerido (ajustar copy OU ajustar config — membro escolhe, re-valida). `warn` → membro decide. Todos `pass` → prossegue.

O **JSON-LD e o bloco agent-facts (ETAPA 4.5)** são superfícies de promise adicionais: confira que `merchantReturnDays`/`returnFees`, `shippingDetails`, `availability`, `priceValidUntil`, `price` e `aggregateRating` do Schema batem com a config real e com `promise-check.json`. Schema divergente da config = structured-data fraudulento (manual action no Google) → trate como `fail` no gate.

> Sem bypass automático. Se o membro insistir em override, registre em `manifest.compliance_override` com `risk_acknowledged: true` (ES3 — exige o membro digitar "EU ACEITO O RISCO").

---

## ETAPA 6 — DEPLOY (shopify-theme-safety INTEGRAL)

### 6.1 Shopify CLI + detecção da loja

```bash
which shopify && shopify --version
```
Se não instalado, instrua (`brew install shopify-cli` ou `npm i -g @shopify/cli @shopify/theme`) e **ABORTE** até confirmar.

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

### 6.4 Instalar arquivos gerados + marker (Regra 4)

```bash
cp "$STAGING_DIR"/sections/page-"$PRODUTO"-*.liquid "$THEME_DIR"/sections/
[ -d "$STAGING_DIR/blocks" ] && [ "$(ls -A "$STAGING_DIR"/blocks 2>/dev/null)" ] && cp "$STAGING_DIR"/blocks/*.liquid "$THEME_DIR"/blocks/ 2>/dev/null
mkdir -p "$THEME_DIR"/templates
cp "$STAGING_DIR"/templates/page."$PRODUTO".json "$THEME_DIR"/templates/
```
Insira o marker único `{%- comment -%}AURA-PUSH-MARKER-<timestamp>{%- endcomment -%}` no topo da section hero antes do push (verificação pós-push).

### 6.5 Push (Regra 3 — `--allow-live` + `--nodelete`)

Fluxo padrão = cópia unpublished (`NEW_THEME_ID`). `--allow-live` só quando o membro explicitamente quer push no tema LIVE.
```bash
shopify theme push --theme "$NEW_THEME_ID" --store "$STORE" --path "$THEME_DIR" --nodelete --json
# push no LIVE (exceção, com backup já feito em 6.2):
# shopify theme push --theme "$LIVE_THEME_ID" --store "$STORE" --path "$THEME_DIR" --nodelete --allow-live --json
```
Leia o `--json` procurando `"errors"` (não só `"warning"`). Resolva erro por erro (tabela de debug abaixo).

### 6.6 Marker verification (Regra 4) — NUNCA pull pós-push não-verificado

```bash
curl -s "https://$STORE/products/<handle>?preview_theme_id=$NEW_THEME_ID" | grep AURA-PUSH-MARKER
```
- Marker encontrado → push OK. Remova o marker do arquivo local e re-push (limpeza).
- Marker ausente → push rejeitado silenciosamente (theme lock? rate limit 429? compile error?). Diagnostique pela Regra 5 ANTES de qualquer pull. **Nunca pull depois de push não-verificado** (o tema remoto antigo sobrescreveria o trabalho local).

### 6.7 Smoke test (Regra 7) — antes de dizer "tá no ar"

```bash
curl -sI "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID"   # esperar 200
curl -s  "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID" | grep -E "(404|500|Liquid error)"   # esperar zero
curl -sI "https://$STORE/cart.js"   # esperar 200
```
Se qualquer smoke falha → rollback automático pro backup duplicado (Regra 6) e reporte antes de tentar de novo (ES4 oferece paths alternativos).

### 6.8 Preview links

```
Theme editor: https://$STORE/admin/themes/$NEW_THEME_ID/editor?template=page.$PRODUTO
Storefront:   https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID
```
> O dropdown "Theme template" do admin Pages só lista templates do tema LIVE. Como `page.[produto]` está na cópia unpublished, use o theme editor direto (sempre funciona) ou `?view=[produto]` no storefront.

---

## ETAPA 7 — Reports (dual output — rule 6b) + iteration loop

### Reports

Salve `07-page.md` (fonte pra AI) + `07-page.html` (humano) + `07-deploy-report.json`. O `.html` usa `.claude/templates/aura-report-template.html` (CSS inline, self-contained) e **abre com o bloco SVG da logo copiado LITERAL de `.claude/templates/aura-logo-snippet.html`** (rule 6b — NUNCA texto; o 07c/deploy antigo não tinha logo, agora tem). Componentes Aura, responsivo mobile.

Conteúdo do `.md`/`.html`: plano de sections + justificativa (de `07-plan.json`), brand signals usados (source), design system, variante aprovada, lista de arquivos com paths absolutos, settings expostos por section (resumo), **resumo da camada GEO** (nós Schema.org gerados + fatos do bloco agent-facts + o que ganha: discovery/citação por AI search, não venda-no-chat — seja honesto com o membro), preview links, resultado dos gates (compliance + promise-check), issues conhecidas, histórico de iterações.

`07-deploy-report.json`:
```json
{
  "deploy_id": "<uuid>", "produto": "[slug]", "store": "<STORE>",
  "live_theme_id": "<LIVE_THEME_ID>", "theme_id": "<NEW_THEME_ID>",
  "preview_url_editor": "https://<STORE>/admin/themes/<NEW_THEME_ID>/editor?template=page.<produto>",
  "preview_url_storefront": "https://<STORE>/pages/<produto>?preview_theme_id=<NEW_THEME_ID>",
  "sections_deployed": [{"id": "hero", "type": "page-<produto>-hero", "blocks_count": 7}],
  "geo": {"jsonld_types": ["Product", "Offer", "AggregateRating", "BreadcrumbList"], "jsonld_validated": true, "agent_facts_block": true, "schema_path": "workspace/<produto>/07-page/staging/geo/product-schema.json"},
  "gates": {"compliance": "pass", "promise_check": "pass"},
  "validation_passed": true, "validation_errors": [], "push_warnings": [],
  "marker_verified": true, "smoke_test_passed": true,
  "staging_dir": "workspace/<produto>/07-page/staging",
  "deployed_at": "2026-MM-DDTHH:MM:SSZ"
}
```

Atualize `manifest.json` adicionando `07b-page-build` a `skills_completed`.

### Iteration loop (iteration-driven-refinement)

> "Página compilada, validada, gates passados e deployada (preview acima). Como o Liquid foi gerado deterministicamente do HTML que você aprovou, o theme editor é pixel-idêntico ao que você viu. Quer ajustar? Pode pedir 'hero mais apertado', 'cores mais escuras', 'features em 2 colunas', 'adicionar countdown na oferta'. Refino sem regenerar do zero."

Pra ajustes:
- **Spacing/layout/cor** → ajuste o HTML aprovado (`design/page.html`) e re-rode SPLIT→COMPILE só da section afetada, OU edite o `{% stylesheet %}`/template JSON direto → revalide → re-push.
- **Estrutural** (novos blocks/sections) → re-COMPILE + re-POPULATE → validação de blocks (ETAPA 4) → push.
- **Preço/rating/política mudou** → regenere o `product-schema.json` e o bloco agent-facts (ETAPA 4.5), revalide o JSON-LD, e confira que ainda bate com a config (Gate 2) antes do re-push. Schema e config nunca podem divergir.
- **SEMPRE pull antes de re-push** (Regra 1) pra preservar settings que o membro mexeu no editor.
- **SEMPRE** revalide com `shopify-plugin:shopify-liquid` + rode o snippet de validação do template JSON antes de cada push.
- Atualize `07-deploy-report.json` (`iterations: [...]` com timestamp + mudanças). Max 3 iterações sem progresso → escalate.

### Mensagem final

> "Page-build completo. Próximo passo: 'tracking' (07c-tracking-setup — pixel + CAPI antes dos criativos), ou 'checkout' (07d-checkout-aov), ou 'creatives' (skill 08)."

---

## Self-audit silencioso (rule post-task-self-audit) — deep audit (skill peso crítico)

Antes de declarar concluído, rode os 5 gates expandidos e corrija inline (sem mencionar): cada section do `section_order` virou um `.liquid` validado; template JSON tem `blocks{}` não-vazio em TODA section; copy injetada veio de `06` (não inventada); cores das section settings batem com `design-tokens.json`; **JSON-LD da ETAPA 4.5 valida (Product + BreadcrumbList no mínimo), todo campo vem de fonte real (nenhum rating/preço inventado — nó omitido se sem dado), e Schema + agent-facts + config são a MESMA verdade (envio/retorno/garantia/rating/preço)**; GATE 1 e GATE 2 passaram (sem override silencioso), incluindo o bloco agent-facts na varredura de compliance; marker verificado + smoke test OK antes de declarar "no ar"; logo SVG presente no `07-page.html`. Surface só o que exige decisão (gate `critical` sem rewrite seguro, promise `fail` que precisa escolha copy-vs-config, rating do Schema que diverge da review app e precisa escolha de qual fonte vale).

---

# REFERÊNCIA TÉCNICA

Os ativos abaixo vinham da skill antiga `page-sections`. Aqui são **referência** que o conversor + a validação usam — não é geração manual de Liquid. O fluxo principal é determinístico (COMPILE via `liquid-converter.py`); esta seção explica o QUE o conversor produz e como debugar.

## Padrões aplicados pelo conversor (por código, determinísticos)

O `liquid-converter.py` Modo C aplica estes 6 padrões automaticamente. Conheça-os pra validar que o output está correto:

- **Padrão 1 + 1.5 (CRÍTICO)** — toda cor extraída vira `color` setting E é injetada INLINE no root da section via `style="--c-x: {{ section.settings.color_x | escape }}; ..."` (NUNCA só em `:root` do stylesheet, senão o theme editor não aplica). `| escape` em TODA interpolação dentro de `style=""` (até numérico) — sem isso, aspas internas (`"Playfair Display", serif`) fecham o atributo e órfãm as vars seguintes (página renderiza sem radius/shadow/fonte, silenciosamente).
- **Padrão 1.6 + 5 (everything-editable)** — `box-shadow`/`border-radius`/`font-size`/`font-family` que vêm de token viram `var(--x)` + setting, com migração automática de usages hardcoded no CSS (grep/replace). Exceções: focus rings (`0 0 0 3px`), mono fonts contextuais, `clamp()` em fluids.
- **Padrão 2 (ícones, 3 camadas)** — todo block com icon: preset enum + `icon_custom_svg` textarea (override) + opção `none`. Markup condicional: custom SVG > preset > none.
- **Padrão 3 (auditoria de cores)** — cada cor visível tem color setting próprio (média 15-30 por section). Não economizar.
- **Padrão 4 (CTAs de offer)** — pricing/offer usam `<form action="/cart/add" method="post">` nativo com settings `variant_id`/`quantity`/`after_add`/`cta_fallback_url` (+ Subscribe & Save), NÃO `<a href>`. Form POST dispara `cart_updated` no Shopify Web Pixel → propaga AddToCart pra Meta Pixel/CAPI/GA4/TikTok automaticamente. `<a href="/cart/add?id=X">` (GET) quebra essa cascade — pixel cego.
- **Padrão 6 (countdown/subscribe)** — `countdown_banner` (limit 1) com deadline FIXO real (sale end/launch/drop) ou `compare_at_price`; NUNCA rolling per-user nem reset evergreen (Meta detecta fake scarcity → disapproval). Subscribe & Save: `<input type="radio" name="selling_plan" value="ID">` do app (Shopify Subscriptions native / Loop / Recharge / Skio / Seal).

## Catálogo de Block Types

Este catálogo é o **vocabulário de conteúdo** que o conversor reconhece. Realização concreta: conteúdo de instância ÚNICA (1 eyebrow, 1 heading, 1 CTA num hero) vira **section setting** (grupo Content, editável); conteúdo REPETÍVEL (vários cards/tiers/reviews/faq items) vira **block** (`{% case block.type %}`, arrastável/reordenável). Os "universais" abaixo são tipicamente settings quando aparecem 1×; os "type-specific" são tipicamente blocks (repetem por natureza).

**Universais (conteúdo estrutural — settings quando único, block `{% when 'X' %}` quando repetido):**

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
- Offer → `pricing_tier` (name + price + strap + features richtext + CTA form `/cart/add` + badge + popular + image) · `countdown_banner` (limit 1)
- Guarantee → `promise_item` (title + body + accent + icon)
- FAQ → `faq_item` (question + answer richtext + open_by_default) — usar `<details><summary>` nativo
- Mechanism → `mechanism_card` / `ingredient_card` / `process_step` / `science_card` (nomeie conforme o mecanismo real)
- Before-after → `comparison_pair` (before_image + after_image + label)
- Ingredients → `ingredient` (name + role + dosage + image)
- How-it-works → `step` (number + title + description + image)

**Regra dos 4 headers em todo block:** Content (o quê) · Style (como) · Spacing (onde) · Advanced (custom_css). Todo block emite `id="pu-{{ block.id }}"` + `<style>#pu-{{ block.id }} { {{ block.settings.custom_css }} }</style>` pra scoping.

**Blocks inline no schema, NUNCA theme blocks em `/blocks/*.liquid`** com `{% content_for 'block' type: block.type %}` — o validator do Shopify bloqueia vars dinâmicas ("The 'id' argument should be a string"). O conversor gera inline.

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
15. Admin API: `shopify page create` não existe — o membro cria a página em Admin → Pages → Add page; a skill entrega o theme editor URL direto (`?template=page.[produto]`) que roda sem a página existir antes.

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
| Cor mudada no editor não aplica | CSS var hardcoded em `:root` em vez de inline no root | Padrão 1 (conversor injeta inline; se quebrou, re-COMPILE) |
| Meta Pixel não registra AddToCart | CTA `<a href="/cart/add?id=X">` em vez de form POST | Padrão 4 (conversor gera form `/cart/add` nativo) |
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
- Pull depois de push não-verificado (marker ausente) — sobrescreve trabalho local.
- Criar sections que "só funcionam no Horizon" — sempre theme-agnostic, self-contained.
- Gerar Liquid por reasoning manual em vez de rodar o `liquid-converter.py` — a conversão é determinística por design.

## Como invocar specialists

| Specialist | Skill name |
|---|---|
| **Validação Liquid** (crítico) | `shopify-plugin:shopify-liquid` |
| Geração/ajuste de HTML (07a; iteration) | `frontend-design` |
| Captura de screenshot (signals 07a) | `webapp-testing` |

A validação Liquid é parte do plugin Shopify AI Toolkit (`/plugin marketplace add Shopify/shopify-ai-toolkit` + `/plugin install shopify-plugin@shopify-plugin`). Sem ele, instrua a instalar antes.

## Referências cruzadas

- **Skill anterior:** `07a-page-design` (gera o `design/page.html` aprovado + `design-tokens.json` + `07-plan.json` que esta skill consome)
- **Conversor canônico:** `tools/design-clone/liquid-converter.py` (Modo C — flags `--html --css --type --output --blocks-dir --namespace --product-slug --emit-template-json --page-handle`)
- **Próxima no fluxo:** `07c-tracking-setup` (pixel + CAPI antes dos criativos) → `07d-checkout-aov` → `08-creative-engine`
- **Gate de launch:** `09-consistency-audit` (pré-requisito da skill 10, não do deploy da página)
- **Camada GEO (ETAPA 4.5):** JSON-LD Schema.org (Product + Offer + AggregateRating + BreadcrumbList) de `04-offer.json` + `06-copy.json` + reviews, validado antes de injetar, mais o bloco agent-facts — pra citação por ChatGPT/Perplexity/Google AI Mode. Validação externa opcional pós-deploy: Google Rich Results Test + validator.schema.org.

# Page Build · Referência: GEO / Schema, agent-readability (ETAPA 4.5)

> O porquê da camada legível por máquina e a honestidade com o membro, a montagem do JSON-LD (Product, Offer, AggregateRating, BreadcrumbList e FAQPage das perguntas reais) com a regra sem dado sem nó, o script de validação, a injeção como bloco `custom_liquid`, o bloco de agent-readable facts e a nota por member-stage. Abra na ETAPA 4.5.

## ETAPA 4.5 — GEO / Schema (agent-readability — citação por AI search)

A loja precisa ser **legível por máquina**, não só por humano. ChatGPT, Perplexity e o Google AI Mode citam páginas que entregam fatos estruturados e verificáveis em vez de copy persuasiva crua. O Shopify já liga Agentic Storefronts por default, então o crawler de AI passa nessa página de qualquer jeito — a questão é se ele acha o que precisa pra te citar. Páginas com Schema.org completo são citadas com muito mais frequência que páginas sem (a diferença é grande). É barato (texto + um bloco JSON) e vira um moat que poucos concorrentes têm.

**Honestidade com o membro (não vender fantasia):** o ganho HOJE é **discovery e citação** — aparecer na resposta do ChatGPT/Perplexity quando alguém pesquisa o problema que o produto resolve, com a loja linkada como fonte. NÃO é "venda fechada dentro do chat" (esse fluxo de checkout agêntico ainda está engatinhando). O que se constrói agora é presença na camada de AI search antes dos concorrentes — quando a venda-dentro-do-chat amadurecer, quem já tem Schema limpo larga na frente. Posicione assim, sem prometer receita imediata.

Esta etapa NÃO toca o design visual nem a copy persuasiva. Ela adiciona duas camadas invisíveis pro consumidor humano e visíveis pro crawler: (1) o **JSON-LD Schema.org** no `<head>`/markup, (2) um bloco de **fatos legíveis por agente** em texto limpo.

### 4.5.1 — Montar o JSON-LD (Product + Offer + AggregateRating + BreadcrumbList + FAQPage)

Leia as fontes (todas já existem na cadeia; não invente nenhum campo):

- `workspace/[produto]/offer-builder/dados.json` → nome do produto, preço, `compare_at_price`, moeda, garantia (dias), unique mechanism, descrição da oferta.
- `workspace/[produto]/copy-engine/dados.json` → headline/descrição do produto, specs/benefícios em texto, brand, **e as perguntas/respostas REAIS da section faq** (fonte do nó FAQPage — as mesmas Q&A que a página exibe, nunca perguntas inventadas só pro Schema).
- **Reviews** → `offer-builder/dados.json` (se traz `social_proof`/`rating`) OU a review app real (Judge.me/Loox/Yotpo via Admin API, se conectada). O rating do Schema é o mesmo que a página exibe.

**Regra dura — sem dado, sem nó.** Se um campo não tem fonte real (ex: rating sem review app conectada, ou `compare_at_price` ausente), **OMITA o nó/propriedade** em vez de inventar. `AggregateRating` só entra se há reviews reais e contáveis. Schema com número fabricado é pior que Schema ausente (vira manual action no Google Search Console).

Monte `staging/geo/product-schema.json` com este shape (preencha dos arquivos, sem placeholders soltos):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Product",
      "name": "<offer-builder product_name>",
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
          "merchantReturnDays": "<dias de garantia de offer-builder>",
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
          "name": "<pergunta REAL da section faq (copy da `copy-engine`), texto idêntico ao da página>",
          "acceptedAnswer": { "@type": "Answer", "text": "<resposta REAL da section faq, texto limpo sem markup>" }
        }
      ]
    }
  ]
}
```

O nó **FAQPage** cobre TODAS as perguntas da section faq da página (uma entrada `Question` por Q&A, na mesma ordem). Se a página não tem section faq, omita o nó inteiro (mesma regra dura: sem dado, sem nó) — mas registre no `deploy-report.json` que a página saiu sem FAQ (a `agentic-readiness` vai apontar isso como gap de agent-readability).

Notas de montagem:
- `merchantReturnDays`, `returnFees` (free vs paid), `shippingDetails` (free shipping vs cobrado) e `priceValidUntil` (promo time-bound) saem da oferta (`offer-builder`) e da política da loja. Se o frete grátis cobre só US, o `shippingDestination` é US.
- `availability` reflete o estoque real (`InStock`/`OutOfStock`/`PreOrder`).
- `priceValidUntil`: só se há promo com data-fim FIXA real (mesma regra do countdown na seção Padrões — nunca rolling/evergreen).
- `image`/`url`/`item` são URLs **absolutas** (`https://$STORE/...`), nunca relativas.

### 4.5.2 — Validar o JSON-LD (obrigatório antes de injetar)

```python
import json, urllib.parse
from pathlib import Path
PRODUTO = "[slug]"
SCHEMA = Path(f"workspace/{PRODUTO}/page/staging/geo/product-schema.json")
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
    print("AVISO: nó FAQPage ausente (RECOMENDADO quando a página tem section faq — a `agentic-readiness` audita isso)")
if errors: print("\n".join(errors)); raise SystemExit(1)
print("JSON-LD válido:", ", ".join(sorted(types)))
```

Required = **Product + BreadcrumbList** (a validação barra sem eles). **FAQPage é RECOMENDADO**: não bloqueia se ausente (página sem FAQ existe), mas quando a página TEM section faq o nó deve estar presente e com as perguntas idênticas às da página — a `agentic-readiness` audita exatamente isso.

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
| **Specs do produto** | `copy-engine/dados.json` / `offer-builder/dados.json` | "30ml serum. 0.5% encapsulated retinal. Fragrance-free, vegan." |
| **Envio** | config Shopify (a mesma da ETAPA 4.5.1) | "Free US shipping. Ships in 1–2 business days from [state]." |
| **Retorno / garantia** | `offer-builder/dados.json` (dias) + policy page | "90-day money-back guarantee. Free returns by mail." |
| **Disponibilidade** | estoque real | "In stock. Ships immediately." |
| **Garantia/durabilidade** | `offer-builder/dados.json` | "Each bottle lasts ~60 days at the recommended use." |
| **Quem é** | brand snapshot | "Made by [brand], a [categoria] company." |

Regras do bloco:
- **Frase declarativa curta, verificável.** Nada de "the best", "revolutionary", "transform your skin" — isso é copy persuasiva, mora nas outras sections. Aqui é o "spec sheet" que a AI cita.
- Permanece em **inglês US** (é consumer-facing — regra inviolável do CLAUDE.md, igual ao resto da página).
- **Sem travessão em excesso** (rule 8a) e **sem aviso/disclaimer inserido por conta própria** (rule 8b) — entra na passada de estilo da ETAPA 5.
- Bate 1:1 com o JSON-LD e com a config real (envio/retorno/garantia/disponibilidade): JSON-LD, agent-facts e config são a MESMA verdade em três formatos.
- Esse bloco vira uma section a mais no SPLIT→COMPILE→POPULATE se você quiser editabilidade total; ou, mais simples, um `custom_liquid` companion do bloco JSON-LD. Escolha pela complexidade da página (section dedicada se o membro quer controle fino; `custom_liquid` se é só prosa estável).

> A copy persuasiva (hero, benefits, mechanism) continua intocada. Agent-facts é uma CAMADA ADICIONAL, não substitui nada. Humano lê a copy; AI cita os facts.

### 4.5.5 — Member-stage

Starter ($300–1000/mês, primeira loja): entregue o Schema completo mesmo assim (é baseline, custa quase nada e o ganho de discovery compounda) mas explique em 2 linhas o que é e por que importa, sem jargão. Validating/scaling: entregue e siga; mencione a validação externa (Rich Results Test) como passo opcional pós-deploy.

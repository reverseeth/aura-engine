# Agentic Readiness · Referência: Perplexity Merchant Program e qualidade do feed do Google Merchant Center (ETAPAs 7 e 8)

> O registro no programa do Perplexity e os cinco critérios do feed do produto hero (título, descrição, imagens, GTIN, preço e disponibilidade). Abra na ETAPA 7.

### ETAPA 7 — Perplexity Merchant Program

Registro grátis, taxa zero, sem mínimo de receita, com caminho simplificado pra lojas Shopify — coloca o catálogo dentro do shopping do Perplexity. Não dá pra automatizar (exige a conta do merchant):

1. Passar ao membro o passo a passo: perplexity.ai → Merchant Program → conectar a loja Shopify.
2. Marcar `registered` / `pending` (pendente NÃO bloqueia o launch — é upside, não gate).

### ETAPA 8 — Qualidade do feed do Google Merchant Center

O feed (o catálogo de produtos que o Google lê) alimenta o Google AI Mode e o shopping dos assistentes. Se o membro tem Merchant Center conectado (app Google & YouTube), auditar o produto hero:

- **Título ≥ 30 caracteres** e descritivo pra query de agente — "Magnesium Glycinate Sleep Support, 120 Capsules" acha comprador; título só com nome de marca não (é o erro da maioria das lojas).
- **Descrição ≥ 500 caracteres** com specs e uso.
- **≥ 3 imagens** do produto.
- **GTIN preenchido** no feed (ou `identifier_exists: false` declarado quando não há).
- Preço/disponibilidade do feed = PDP (mismatch derruba o listing).

Sem Merchant Center conectado: recomendar a conexão (grátis) e marcar `pending` — de novo, upside, não gate.

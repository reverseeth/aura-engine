# Social Engine · Referência: Templates do Marketing Studio e a fórmula do grid (ETAPA 2)

> Como ler o catálogo de templates de imagem do Marketing Studio do Higgsfield, cadastrar marca e produto no Ads Studio, classificar os templates contra a direção do feed, montar o banco de templates aprovados e a fórmula das 9 posições do grid. Inclui o caminho sem Higgsfield. Abra na ETAPA 2.

## 1. Higgsfield conectado (tools com prefixo `mcp__higgsfield__`)

Os nomes das tools abaixo são os de hoje. Se mudarem, procure pela intenção.

1. **Saldo primeiro** (hoje `balance`, e `show_plans_and_credits` pro custo por modelo). Diga ao membro em uma linha quanto tem e quanto custa um lote de 9.
2. **Marca e produto no Ads Studio** (hoje `ads_studio_list_brands` e `ads_studio_list_products`). Se a marca não existe, cadastre (hoje `ads_studio_create_brand`) com o nome, a paleta e o tom do `brand.md`. Se o produto não existe, cadastre (hoje `ads_studio_add_product`) com as fotos reais do produto: render do produto inventado pela IA quebra a confiança na primeira compra. Sem foto real, peça ao membro antes de seguir.
3. **Catálogo de templates de imagem** (hoje `get_presets` com `source: "marketing_studio"`, e `category: "product-shot"` pros de foto de produto; o painel geral abre por `show_marketing_studio_v2`). Pagine até ler o catálogo inteiro. Abrir o catálogo nunca autoriza rodar um template: execução só depois do sim de custo da ETAPA 3.
4. **O que já foi gerado** (hoje `show_marketing_studio_generations`): se o membro já usou o Marketing Studio, os resultados que ele guardou dizem o gosto dele.

## 2. Classifique cada template contra a direção

Pra cada template, uma linha: nome, o que ele produz, nota de 1 a 5 de encaixe na direção do feed (paleta, tratamento de foto, composição) e o papel no grid que ele cumpre. Templates com nota 4 ou 5 entram no banco. Template que bate com algum item de "Proibido" sai, mesmo bonito.

**Banco mínimo de 12 templates aprovados**, cobrindo os papéis da fórmula abaixo. Com menos de 12, a rotina repete template em menos de uma semana e o feed fica monótono. Se o catálogo não fecha 12, complete com prompts próprios no mesmo estilo (hoje `generate_image`, com o modelo recomendado por `models_explore` com `action: "recommend"`).

## 3. A fórmula do grid 3x3

O lote diário são 9 posts que, juntos, formam um bloco 3x3 coerente no perfil. Cada posição tem um papel fixo; o template e o assunto giram todo dia.

| Posição | Papel | Exemplo de assunto |
|---|---|---|
| 1 | Produto herói | O produto na luz da assinatura, sem texto |
| 2 | Dor do cliente | Frase de VOC curta sobre a imagem |
| 3 | Mecanismo | O mecanismo nomeado da oferta em uma imagem |
| 4 | Textura ou ingrediente | Close sem texto |
| 5 | Prova | Depoimento, número ou antes e depois |
| 6 | Lifestyle | O produto na rotina do avatar |
| 7 | Educação | Um fato curto que o avatar não sabia |
| 8 | Oferta | Bundle, bônus ou garantia, com o CTA |
| 9 | Marca | Cor sólida da paleta com uma frase da marca |

Ajuste a fórmula à direção aprovada (ex.: marca de beleza troca "Mecanismo" por "Como usar"), mas mantenha o equilíbrio: no máximo três posições com texto pesado, pelo menos duas sem texto nenhum, e a oferta aparece uma vez por lote.

## 4. Sem Higgsfield

A fórmula e a direção valem igual. Pra cada posição, escreva um prompt autocontido (cada geração começa do zero, sem citar "a imagem anterior"): assunto, composição, luz, fundo, paleta em código hex, proporção 4:5 e o texto exato, se houver. O membro roda em qualquer IA de imagem (GPT Image, Midjourney, Nano Banana, Flux) e devolve os arquivos em `social-engine/<data>/`. A rotina da ETAPA 5, nesse caso, entrega os 9 prompts e as legendas por dia, em vez das imagens.

## 5. Onde fica salvo

`social-engine/dados.json` → `higgsfield`: `{ "brand_id": "...", "product_ids": ["..."], "credits_per_batch": 0 }`, `templates_bank[]`: `{ "id": "...", "name": "...", "role": "produto herói | dor | ...", "fit": 5 }` e `grid_formula[]` com os 9 papéis. No `social-engine.md`, a seção "Banco de templates e fórmula do grid".

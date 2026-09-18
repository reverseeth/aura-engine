# Setup · Referência: Criar o manifest, a fonte única de verdade (ETAPA 5B)

> Cada campo do `manifest.json` com a regra de preenchimento (slug, budget canônico, tier, stage, idiomas, ESP, vertical pelo enum), as duas perguntas opcionais de quem já vende, a carimbada do `framework_version` pelo `migrate.py`, a validação pelo `manifest.py` e o exemplo completo. Abra na ETAPA 5B.

### ETAPA 5B — Criar Manifest (fonte única de verdade)

Paralelamente ao `profile.md`, crie o arquivo `workspace/[produto]/manifest.json`. Este é o **ÚNICO** local que todas as skills seguintes leem/atualizam para descobrir paths, progresso, e métricas. Substitui qualquer inferência manual de caminho.

- `product_slug` — gere via slugify do nome do produto detectado na Etapa 4 (lowercase, ASCII, hyphens; regex `^[a-z0-9-]+$`). Se não houver produto (Situação A), use `dev-placeholder-[YYYYMMDD]` e a skill `product-research` substituirá depois.
- `product_name` — nome humano do produto (ou "TBD — product research pending" para Situação A).
- `product_url` — URL informada pelo membro, se houver.
- `store_url` — URL da loja Shopify (de `SHOPIFY_LINK`), se o membro deu o link.
- `created_at` / `updated_at` — timestamps ISO-8601 UTC (mesmo valor inicial).
- `setup_complete: true`.
- `budget_daily` — o valor NUMÉRICO de `BUDGET` em dólares/dia (ex: `80`). É o campo canônico de budget que as skills leem (member-stage-awareness usa `budget_daily < 50` como sinal de stage; a `tracking-setup` usa na decision tree do analytics stack) — grave sempre.
- `budget_tier` — mapeie de `BUDGET` (starter / standard / escala-inicial / escala-avancada). Campo ECONÔMICO derivado de `budget_daily`, separado de `stage`.
- `stage` — mapeie da `SITUACAO`: A/B → `starter`, C → `validating`, D → `scaling`.
- `market` — default `"US"`.
- `copy_language` — default `"en"` (copy consumidor-final é sempre inglês US).
- `report_language` — valor capturado em `REPORT_LANGUAGE` na ETAPA 2.6 (`pt-BR` ou `en`), espelhando o `profile.md`.
- `esp` — valor de `ESP` (`klaviyo` / `omnisend` / `mailerlite` / `shopify_email` / `none` — enum exato do manifest-schema).
- `product_vertical` — infira do nome/descrição auto-extraídos na ETAPA 4, usando EXCLUSIVAMENTE o enum do manifest-schema.json: `beauty` / `skincare` / `supplements` / `health` / `fitness` / `fashion` / `home` / `pet` / `food` / `financial` / `tech` / `education` / `other`. Se ambíguo, pergunte em 1 linha; default `"other"`.
- `skills_completed: ["setup"]`.
- `framework_version` — NÃO preencha à mão: logo depois de gravar o manifest, rode `python3 tools/migrate.py --product [produto]`. Em produto novo não há nada a migrar e o script só carimba a versão atual do layout do workspace (o hook de início de sessão faria isso na próxima sessão; rodar agora deixa o manifest completo desde o primeiro minuto).

**Se SITUACAO = C ou D (já vende):** faça 2 perguntas opcionais rápidas (1 mensagem só) e grave o que vier:
- AOV médio aproximado → `aov_baseline` (número em dólares).
- Margem ou COGS aproximada por pedido → `cogs_estimate` (número em dólares).
Se o membro não souber/responder, deixe vazio. Para SITUACAO A/B deixe ambos vazios — a skill `offer-builder` preenche depois.

Schema completo em `.claude/templates/manifest-schema.json`. Depois de gravar, valide com `python3 tools/manifest.py [produto] validate` (estrutural; propriedades opcionais ainda não preenchidas não acusam).

Exemplo:

```json
{
  "product_slug": "collagen-glow",
  "product_name": "Collagen Glow",
  "product_url": "https://example.com",
  "store_url": "https://example.myshopify.com",
  "created_at": "2026-04-16T13:00:00Z",
  "updated_at": "2026-04-16T13:00:00Z",
  "setup_complete": true,
  "budget_daily": 80,
  "budget_tier": "standard",
  "stage": "validating",
  "market": "US",
  "copy_language": "en",
  "report_language": "pt-BR",
  "esp": "klaviyo",
  "product_vertical": "skincare",
  "aov_baseline": 72,
  "cogs_estimate": 14,
  "skills_completed": ["setup"]
}
```

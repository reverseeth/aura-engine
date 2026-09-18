# Page Build · Referência: Referência técnica, specialists e referências cruzadas

> Os specialists invocados (validação Liquid, `frontend-design`, `webapp-testing`) e as referências cruzadas da skill (anterior, conversor, contrato de publicação, próxima no fluxo, gate de launch, camada GEO). Abra quando precisar do mapa.

## Como invocar specialists

| Specialist | Skill name |
|---|---|
| **Validação Liquid** (crítico) | `shopify-plugin:shopify-liquid` |
| Geração/ajuste de HTML (`page-design`; iteration) | `frontend-design` |
| Captura de screenshot (signals `page-design`; fidelity check 6.11) | `webapp-testing` |

A validação Liquid é parte do plugin Shopify AI Toolkit (`/plugin marketplace add Shopify/shopify-ai-toolkit` + `/plugin install shopify-plugin@shopify-plugin`). Sem ele, instrua a instalar antes.

## Referências cruzadas

- **Skill anterior:** `page-design` (gera o `design/page.html` aprovado + `design-tokens.json` + `page-plan.json` que esta skill consome)
- **Conversor canônico:** `tools/design-clone/liquid-converter.py` (batch: `--batch <manifest.json> --emit-template-json`; Modo C: `--html --css --type --output --namespace --product-slug --emit-template-json --page-handle`; `--blocks-dir` é deprecado/ignorado; Modo B legacy exige `--allow-competitor-markup`)
- **Contrato de publicação:** `manifest.storefront` (`theme_id`/`page_url`/`published_at`, gravado no 6.10) — a `checkout-aov` opera no tema onde a página vive e a Skill `ad-strategy` lê `page_url` como destino da campanha
- **Próxima no fluxo:** `tracking-setup` (pixel + CAPI antes dos criativos) → `checkout-aov` → `bonus-delivery` Fase A (se a oferta tem bônus) → `retention-engine` Fase A (flows de recuperação: abandoned cart + post-purchase) → `creative-engine`
- **Gate de launch:** `consistency-audit` (pré-requisito da skill `ad-strategy`, não do deploy da página)
- **Camada GEO (ETAPA 4.5):** JSON-LD Schema.org (Product + Offer + AggregateRating + BreadcrumbList + FAQPage das perguntas reais) de `offer-builder/dados.json` + `copy-engine/dados.json` + reviews, validado antes de injetar, mais o bloco agent-facts — pra citação por ChatGPT/Perplexity/Google AI Mode. Validação externa opcional pós-deploy: Google Rich Results Test + validator.schema.org.

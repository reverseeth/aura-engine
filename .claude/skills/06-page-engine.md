---
name: page-engine
description: DEPRECATED — use 06a-page-planning + 06b-page-sections + 06c-page-deploy. Esta skill foi dividida em 3 para manutenibilidade. Se ativada por trigger antigo ("page", "página", "build page"), redirecione imediatamente pra `page-planning` como primeira etapa da cadeia.
---

# Page Engine — MODULARIZADA

Esta skill foi dividida em 3 skills menores pra melhorar performance e manutenibilidade (o arquivo monolítico tinha 1055 linhas / 68 KB):

1. **`page-planning`** (06a) — Pre-flight, detecção de tipo de página (advertorial vs landing vs hybrid), brand discovery, referência visual (opcional), design system generation (orquestra 5 specialists: color-system → typography → spacing → grid → tokens). Outputs em `/workspace/[produto]/06-page/`: `06-design-system.md` + `06-plan.md` + `06-plan.json`.

2. **`page-sections`** (06b) — Gera 3 variantes de hero (membro escolhe A/B/C), converte pro padrão de **blocks inline no schema** Shopify, replica pras demais sections do plano, roda UX writing pass + self-critique (design critique + Nielsen + WCAG 2.1 AA + QA checklist). Validação via `shopify-plugin:shopify-liquid` com retry logic explícita (3 tentativas). Outputs: arquivos `.liquid` em `<staging>/sections/` + `06-sections-report.md`.

3. **`page-deploy`** (06c) — Cria `templates/page.[produto].json` com blocks pré-populados com copy real, roda validação OBRIGATÓRIA de blocks (não-vazios, block_order consistente, types válidos contra schema do Liquid), faz deploy safe no Shopify (duplicate → pull → cp → push --nodelete), gera preview URLs + report humano + machine-readable (`06-deploy-report.json`). Suporta iteration loop.

## Cadeia de uso (ordem obrigatória)

```
page-planning → page-sections → page-deploy
```

Cada skill faz pre-flight da anterior — `page-sections` bloqueia se `06-plan.json` não existir; `page-deploy` bloqueia se `<staging>/sections/*.liquid` não existir + shopify-cli não estiver instalado.

## Migração / Referências cruzadas

O conteúdo anterior foi migrado **integralmente**. Nenhuma lógica foi removida — apenas reorganizada:

| Conteúdo original | Nova localização |
|---|---|
| ETAPA 0 (pesquisa Aura, detecção produto, inputs) | `page-planning` |
| ETAPA 1 (plano de sections + menu + eyebrows criativos) | `page-planning` |
| ETAPA 2 + 2.1 (brand discovery + referência visual) | `page-planning` |
| ETAPA 3 (design system orchestration) | `page-planning` |
| ETAPA 4 (hero 3 variantes) + mapeamento ASCII→Liquid | `page-sections` |
| ETAPA 4.5 (padrão de blocks inline + validação cruzada) | `page-sections` |
| ETAPA 5 (hero Liquid + validação + retry logic) | `page-sections` |
| Catálogo de Block Types Universais | `page-sections` |
| ETAPA 6 (remaining sections) | `page-sections` |
| ETAPA 7 (UX writing) | `page-sections` |
| ETAPA 8 (self-critique) | `page-sections` |
| WCAG checklist + qualidade visual + DO NOT | `page-sections` |
| Debug table (erros de Liquid) | `page-sections` |
| Limitações Shopify (1-15) | `page-sections` |
| ETAPA 9 (template JSON + validação de blocks OBRIGATÓRIA) | `page-deploy` |
| ETAPA 10 (install Shopify — duplicate/pull/cp/push) | `page-deploy` |
| ETAPA 10.5 (report humano + machine-readable) | `page-deploy` |
| ETAPA 11 (iteration loop) | `page-deploy` |
| Debug push table | `page-deploy` |

## Correções aplicadas durante a modularização

Esta reorganização veio com fixes identificados em auditoria:

- **Pre-flight em todas as 3 skills** (valida skill anterior + manifest)
- **Validação de hex em brand discovery** (regex + tabela fixa de 30 cores comuns pra fallback de nomes)
- **Script-exists check** antes de rodar `tools/design-clone/aura_clone.py` — pula graciosamente se ausente
- **Lista canônica de specialists** em design system orchestration (substitui prose)
- **Mapeamento ASCII→Liquid explícito** (letra escolhida → variante específica)
- **Catálogo completo de block types universais** + validação cruzada com template JSON
- **Retry logic explícita** pro `shopify-plugin:shopify-liquid` (3 tentativas: validate → fix → manual)
- **Shopify CLI pre-flight** (`which shopify` com instruções de install por plataforma)
- **Paths normalizados** via variáveis top-level (`STAGING_DIR`, `THEME_DIR`, `STORE`)
- **Loja detection** a partir do `product_url` do manifest → fallback pra prompt
- **Validação de template JSON** com snippet Python executável antes de push (pega `blocks: {}` vazio ANTES do deploy falhar)
- **Machine-readable report** (`06-deploy-report.json`)
- **Referência atualizada** pra `tools/design-clone/_css_utils.py` (módulo novo do Batch A)

## Trigger behavior (compatibilidade)

Se o membro invocar esta skill via trigger antigo ("page", "página", "build page", "shopify page", "gerar página"), redirecione imediatamente pra `page-planning` — primeira etapa da cadeia.

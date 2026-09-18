# Market Research · Referência: SALVAR, os três artefatos, os consumidores e o manifest

> O dual output pelo `render_report.py`, o diretório, os três artefatos, a lista de quem consome o `dados.json` e a atualização do manifest pelo script com os campos gravados. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `offer-builder/offer-builder.md` → `offer-builder/offer-builder.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana e nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).


**Antes de qualquer write**, garanta: `mkdir -p workspace/[produto]/market-research/`.

Salvar TRÊS artefatos:

1. **`workspace/[produto]/market-research/market-research.md`** — fonte canônica para AI das próximas skills
2. **`workspace/[produto]/market-research/market-research.html`** — visualização humana, gerada com `python3 tools/render_report.py workspace/[produto]/market-research/market-research.md`
3. **`workspace/[produto]/market-research/dados.json`** — JSON companion estruturado:


Este é o DOCUMENTO MAIS IMPORTANTE. Ele alimenta:
- Skill `competitor-analysis` — usa gaps e claims identificados
- Skill `offer-builder` — usa pain points, desires, root cause, mechanism hints
- Skill `copy-engine` — usa VOC literal, lead type, awareness level, objeções, `core_avatar` (a quem a copy se dirige), `labels` (os apelidos do mercado que entram na copy) e `market_vocabulary` (as palavras permitidas e as proibidas)
- Skills `page-design` e `page-build` (cadeia storefront `page-design` → `page-build`) — usa tudo da copy + proof stacking
- Skill `creative-engine` — usa trigger events, VOC, visual hooks, `market_vocabulary`, e **`sub_avatars[]` como persona/micro-persona de cada conceito, com `sub_avatars[].angle` como o ângulo de entrada** (é o contrato que substitui a leitura genérica de "sub-avatares da Skill `market-research`")
- Skill `ad-strategy` — usa awareness pra targeting

**Atualize o `manifest.json` pelo script `tools/manifest.py`** (fonte única de verdade; nunca editar o JSON à mão: `python3 tools/manifest.py <slug> set <chave> <valor-json> [...]` para os campos e `python3 tools/manifest.py <slug> complete market-research` para a marca, que valida o `market-research/dados.json` contra `.claude/templates/schemas/market-research.dados.schema.json` antes de marcar):

- `market` ← mercado geográfico confirmado na ETAPA 1 (`US` / `UK` / `EU` / `global`) — sem isso o manifest fica pra sempre com o default `"US"` do setup, divergindo do relatório
- `voc_count` ← número total de frases VOC únicas coletadas
- `voc_adequacy` ← `"ok" | "medium" | "insufficient"` (mesmo valor do dados.json)
- `awareness_distribution` ← objeto com os 5 níveis em inteiros 0-100
- `sophistication_stage` ← inteiro 1-5
- `skills_completed` ← `python3 tools/manifest.py <slug> complete market-research` (o script não duplica e grava `updated_at`)

**Regenera o painel do produto:** `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` do manifest — atualiza o `ABRIR-AQUI.html`).

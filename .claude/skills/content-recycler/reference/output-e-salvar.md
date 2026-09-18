# Content Recycler · Referência: Output por trilha, índice do produto e SALVAR

> A estrutura de pastas por criativo fonte, o que sai sempre, o que sai em cada trilha, o índice no topo da pasta da skill, a regra do dual output e a atualização do manifest e do painel. Abra ao salvar.

## Output

Pasta `workspace/[produto]/content-recycler/[source-id]/`.

**Sempre (comum às duas trilhas):**
- `essence.json` — essência + `framework_template` + `psychological_mechanism` (reusável)

**Trilha 1 (sempre que a skill roda):**
- `amplification-plan.md` + `amplification-plan.html` — o plano com uma seção por movimento (iterações pelos 4 elementos, ports de formato, brief de LP/prelander, pacote de canal Axon/TikTok, item de ABO pra Skill `scale-engine`)
- `creator-report.md` + `creator-report.html` — o report compartilhável com creators/editor

**Trilha 2 (só quando rodada):**
- 9 arquivos `.md`, um por formato (advertorial, email, TikTok, blog, Pinterest, YouTube preroll, SMS, package insert, podcast)
- 9 arquivos `.html` correspondentes — um pra cada `.md` (rule 6b: dual output obrigatório)
- `README.md` + `README.html` — índice das 9 derivadas + instruções de distribuição (rule 6b do CLAUDE.md)

Além das pastas por source-id, escreva também no topo de `workspace/[produto]/content-recycler/` um índice `content-recycler.md` + `content-recycler.html` que lista todas as fontes trabalhadas (cada `[source-id]` com a classe lida, o plano de amplificação e — quando existirem — os 9 formatos, com link pra pasta). Esse índice é o relatório humano que o painel do produto exibe.

## SALVAR (dual output — rule 6b do CLAUDE.md)

Todo relatório salvo em `workspace/[produto]/content-recycler/[source-id]/` — o plano de amplificação, o creator report e cada derivada da Trilha 2 — DEVE ter `.md` (fonte pra AI) + `.html` companion (visualização humana). O `.html` nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

Depois de salvar todos os outputs:
- Atualizar o manifest pelo script: `python3 tools/manifest.py <slug> complete content-recycler` (não duplica, faz backup e grava `updated_at`; nunca editar o JSON à mão).
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza ABRIR-AQUI.html).

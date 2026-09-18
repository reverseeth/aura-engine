# Copy Engine · Referência: SALVAR e mensagem final

> O diretório, o dual output pelo `render_report.py`, a atualização do manifest pelo script, o conteúdo do `copy-engine.md` em cinco partes e o texto integral da mensagem final com a sequência da fase STOREFRONT. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de salvar, garanta o diretório:** `mkdir -p workspace/[produto]/copy-engine/`.

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `copy-engine/copy-engine.md` → `copy-engine/copy-engine.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana e nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

Atualizar o manifest pelo script: `python3 tools/manifest.py <slug> complete copy-engine` (marca a skill com backup, valida o `copy-engine/dados.json` contra `.claude/templates/schemas/copy-engine.dados.schema.json` e grava `updated_at`; nunca editar o JSON à mão). Em seguida, regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug`; atualiza ABRIR-AQUI.html).

`workspace/[produto]/copy-engine/copy-engine.md` contendo (seções canônicas acima):
1. Strategy brief (Etapa 2 — tipo de página, lead, hero, ângulo, tom, framework, modalities mapping)
2. 20-30 headlines geradas + top 5 + 3 pra teste A/B
3. Página completa seção por seção (Etapa 4 ou 5)
4. Revisão após os sweeps (mudanças documentadas, incluindo a taxa de cobertura de VOC)
5. Variações pra teste (Etapa 7)

Também salvar `workspace/[produto]/copy-engine/dados.json` no schema acima.

## Mensagem Final

"Copy completa pro [tipo de página]. Big Idea: [big idea]. Mecanismo aplicado: [nome]. VOC integrado, objeções quebradas, 3 variações de headline pra teste.

Próximo passo: diga **'page'** pro design da página (skill `page-design` — você escolhe a rota de design e aprova o HTML navegável, com essa copy dentro, ANTES de qualquer código existir); depois **'build page'** pra compilar e subir no Shopify (`page-build`), **'tracking'** (`tracking-setup`) e **'checkout'** (`checkout-aov`). Com a loja pronta, armamos a infraestrutura de launch — **'bônus'** (`bonus-delivery` Fase A, se a oferta tem bônus) e **'retention'** (`retention-engine` Fase A: flows de recuperação, abandoned cart + post-purchase) — e só então os criativos. Não adianta criar ads pra uma página que ainda não existe."

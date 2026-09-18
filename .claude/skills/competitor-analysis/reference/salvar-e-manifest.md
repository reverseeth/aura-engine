# Competitor Analysis · Referência: SALVAR, os artefatos, a estrutura do relatório e o manifest

> A regra do dual output, os sete artefatos, a estrutura do `.md` em onze seções, as regras de escrita (texto integral, posicionamento como a frase de como o concorrente se vende) e a atualização do manifest pelo script. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de qualquer write**, garanta: `mkdir -p workspace/[produto]/competitor-analysis/`.

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `offer-builder/offer-builder.md` → `offer-builder/offer-builder.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana e nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

Salvar os seguintes artefatos:

1. **`workspace/[produto]/competitor-analysis/competitor-analysis.md`**
2. **`workspace/[produto]/competitor-analysis/competitor-analysis.html`** — gerado a partir do item 1 com `python3 tools/render_report.py workspace/[produto]/competitor-analysis/competitor-analysis.md` (o mesmo vale pro `ads-escalados.html` do item 6)
3. **`workspace/[produto]/competitor-analysis/dados.json`** — JSON companion estruturado (ver abaixo)
4. **`workspace/[produto]/competitor-analysis/creative-patterns.json`** — SE membro forneceu criativos pra análise profunda (Etapa 3C); senão, pular. Schema definido na própria Etapa 3C.
5. **`workspace/[produto]/competitor-analysis/creatives-inbox/transcripts/[creative-id].json`** — transcripts Whisper individuais (um por criativo).
6. **`workspace/[produto]/competitor-analysis/ads-escalados.md`** + **`ads-escalados.html`** — SE a Etapa 3F rodou (tabela dos ads mais escalados por marca, com links; texto integral).
7. **`workspace/[produto]/competitor-analysis/ads-escalados-dados.json`** — SE a Etapa 3F rodou (schema na própria Etapa 3F).

Estrutura do `.md`:
1. Lista de concorrentes analisados + links
2. PDP analysis por concorrente (Etapa 2)
3. Meta Ad Library findings + top creatives transcritos (Etapa 3)
4. Classificação de posição de funil (Etapa 3B)
5. Análise de formato dos criativos escalados (Etapa 3D)
6. Páginas de destino com tráfego (tabela com links) + radar de monitoramento (Etapa 3E)
6b. Referência ao doc dedicado de ads escalados com links (`ads-escalados.md`, Etapa 3F — se rodou)
7. Claims compilation table + Claims Saturation matrix (Etapa 4)
8. Alternative solutions map (Etapa 5)
9. Gap analysis (Etapa 6)
10. Síntese estratégica — posicionamento + swipe file com "COMO adaptar" + validated library (Etapa 7)
11. Resumo e Conclusão (Etapa 7, item 7 — texto corrido, fecha o relatório)

Regras de escrita do `.md`/`.html`: texto INTEGRAL sempre — NUNCA truncar conteúdo em tabelas ou cards (posicionamentos, claims, hooks cortados com "..." perdem exatamente a parte que importa); posicionamento de concorrente é a frase de COMO ELE SE VENDE (entendível sozinha), nunca resumo interno de analista — a leitura estratégica vai em campo/parágrafo separado.

**Atualize o `manifest.json` pelo script** (nunca editar o JSON à mão):

- `skills_completed` ← `python3 tools/manifest.py <slug> complete competitor-analysis` (faz backup, valida o `competitor-analysis/dados.json` contra `.claude/templates/schemas/competitor-analysis.dados.schema.json`, não duplica e grava `updated_at`)
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug`; atualiza ABRIR-AQUI.html).

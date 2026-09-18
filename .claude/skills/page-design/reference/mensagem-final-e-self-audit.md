# Page Design · Referência: Mensagem final, self-audit silencioso e referências cruzadas

> O texto integral da mensagem final com framing de draft, a checklist completa dos 5 gates do self-audit desta skill e as referências cruzadas (próxima skill, conversor, presets, doutrina de imagem, auditoria). Abra antes de declarar concluído.

## Mensagem final (framing de draft)

> "Design da página pronto e aprovado por você (rota [escolhida], salvo em `design/page.html` — fonte única de verdade). Plano + strategy em `page-plan.json`, tokens em `design-tokens.json`.
> Próximo passo: rode **page-build** (ou diga 'build page' / 'deploy'). Ela vai compilar esse HTML exato em sections Liquid editáveis, popular o template e subir no Shopify. Como o Liquid é gerado deterministicamente do HTML que você aprovou, o que você vê no theme editor vai ser pixel-idêntico ao que aprovou aqui."

## Self-audit silencioso (rule post-task-self-audit)

Antes de declarar concluído, rode os 5 gates internos e corrija inline (sem mencionar): `mechanism_name` em `page-plan.json` bate LITERAL com `offer-builder/dados.json`; `page_type` é coerente com os três sinais da 1.1 e `strategy.page_type_signals` está preenchido com os três e com o `resolved_by` (divergência de família só fecha com `member`); se `page_type` é `advertorial` ou `listicle`, `destination_ref` está definido (não null) E o `sections_plan` segue o mapa canônico da 1.1 (as 7 seções da copy da `copy-engine` mapeadas 1:1, nada inventado); eyebrows são criativos (não rótulos de framework); a copy inserida em `design/page.html` veio de `06` (não inventada); **todo `sections_plan[]` tem o campo `media` preenchido (ETAPA 1.6) — nenhum placeholder implícito, todo `status: "placeholder"` tem `acquisition_plan` específico, e nenhum lifestyle gerado por AI nasceu de prompt de texto puro com rótulo/embalagem em quadro**; **o self-review visual rodou (screenshots desktop 1440 + mobile 390 lidos por visão) e os defeitos achados foram corrigidos ANTES do checkpoint**; se o Caminho 4 foi usado, os tokens vieram LITERAIS de `.claude/lib/design-presets/presets.json` (não inventados); `design-tokens.json` e `design-signals.json` existem e parseiam; `section_order` e `sections_plan` consistentes entre si; `design_route` registrado no plan; nas rotas 2/5, a normalização da 3.6c rodou de verdade (zero `<script>` no `page.html`, CSS plano, assets locais/estáveis); markers `data-aura-section` presentes em todas as sections (qualquer rota, inclusive handoff do canvas e clone-and-adapt); regras de qualidade comuns da 3.7 passaram (SVG, contraste, performance budget); os `.html` internos gerados pelo `render_report.py`. **Se a rota foi clone-and-adapt: confirme que NENHUMA copy, imagem, logo, claim ou nome de marca do concorrente vazou pra `design/page.html` — só o esqueleto de layout.** Surface só o que exige decisão do membro (ex: conflito de nome de mecanismo entre 02 e 04, ou rota escolhida que ficou inviável a meio caminho).

## Referências cruzadas

- **Próxima skill:** `page-build` (compila `design/page.html` em Liquid + deploya)
- **Conversor canônico (usado pela `page-build`):** `tools/design-clone/liquid-converter.py` (Modo C)
- **Presets de design (Caminho 4):** `.claude/lib/design-presets/presets.json` (tokens completos e fixos dos 8 presets + README)
- **Doutrina de imagem AI (ETAPA 1.6):** skill `creative-engine` ETAPA 1.0 (foto-real-primeiro — produto/rótulo nunca nasce de prompt de texto)
- **Skill que audita o output:** `consistency-audit` (lê `page-plan.json` strategy + `design-tokens.json`)

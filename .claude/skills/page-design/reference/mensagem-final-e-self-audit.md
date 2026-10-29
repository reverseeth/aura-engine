# Page Design · Referência: Mensagem final, self-audit silencioso e referências cruzadas

> O texto integral da mensagem final com framing de draft e o link de preview, a checklist curta do self-audit desta skill (a maior parte lida do `qa-metrics.json` e do `legal_check`) e as referências cruzadas (próxima skill, conversor, presets, doutrina de imagem, auditoria). Abra antes de declarar concluído.

## Mensagem final (framing de draft)

> "Design da página pronto e aprovado por você (modo [direção | referência], salvo em `design/page.html` — fonte única de verdade). Preview pra abrir no celular: [preview_url] (link público, sem as suas fontes; a tipografia final você aprova na loja). Plano + strategy em `page-plan.json`, tokens em `design-tokens.json`[; diferença da página pra sua marca: [drift]% em [chaves que mudaram] — a marca não muda por isso].
> Próximo passo: rode **page-build** (ou diga 'build page' / 'deploy'). Ela vai compilar esse HTML exato em sections Liquid editáveis, popular o template e subir no Shopify. Como o Liquid é gerado deterministicamente do HTML que você aprovou, o que você vê no theme editor vai ser pixel-idêntico ao que aprovou aqui."

Sem preview (a skill `deploy-to-vercel` não existe na sessão ou o membro recusou o link público), a frase do preview sai e a aprovação fica nas capturas. Se o `tokens.py` falhou depois da aprovação, a mensagem diz o erro e o comando pra rodar de novo (`reference/design-tokens.md`) no lugar da linha dos tokens.

## Self-audit silencioso (rule post-task-self-audit)

Antes de declarar concluído, corrija inline (sem mencionar) o que falhar. Os gates de página saem dos arquivos, não de prosa repetida aqui:

1. **QA medido:** `page/qa-metrics.json` existe, foi gravado depois da última edição do `page.html` (o `page_sha256` bate) e não tem item bloqueante em `fail`, ou o item está em `page-plan.json.qa_overrides` com motivo e data. No modo referência, o `legal_check` está em `pass` (nunca liberável).
2. **Revisor:** `page/review.md` existe, ou a rubrica do modelo rodou porque não havia subagente; o que ficou abaixo de 3 depois da terceira rodada foi dito ao membro.
3. **Plano:** `page-plan.json` valida no schema, com `schema_version: 2`, `build_mode`, `direction_ref`, `qa_metrics_ref` e `preview_url` (ou `null`) preenchidos; `section_order` e `sections_plan` batem entre si.
4. **Estratégia:** `mechanism_name` bate LITERAL com `offer-builder/dados.json`; `strategy.page_type_signals` tem os três sinais e o `resolved_by` (divergência de família só fecha com `member`); advertorial e listicle têm `destination_ref` e seguem o mapa canônico das 7 seções de `reference/page-type.md`.
5. **Copy e commerce:** a copy do `page.html` é a da `copy-engine`, sem aviso, asterisco ou claim suavizado; toda superfície de compra está em `commerce.buy_surfaces[]` com as quantidades, `subscription_shown` bate com o `offer-builder` e todo id de `promised_on_page[]` existe em `bonuses[]`. Com `quiz`, as regras do bloco `quiz` de `reference/quiz-funnel.md` (uma pergunta que roteia, nenhuma tela órfã, todo resultado com superfície de compra) e o item M8 da régua.
6. **Mídia:** todo `sections_plan[]` tem `media`, todo `placeholder` tem `acquisition_plan` específico, e a geração da 1.6.3, se rodou, seguiu `reference/imagens-higgsfield.md` (autorização antes, mesma foto real, metadados limpos).
7. **Tokens e fontes:** `design-tokens.json` saiu do `tools/page-qa/tokens.py`, o `type.families[]` bate com a família que a página usa, e família de arquivo tem a cópia em `design/assets/fonts/` e o bloco `data-aura-fonts` no `<head>`. A marca só foi escrita se estava vazia.
8. **Segunda opinião:** se rodou, a versão promovida passou pelo mesmo QA e a rodada está no `iterations-log.json` com a vencedora.
9. **Relatórios:** os `.html` internos saíram do `render_report.py`.

Surface só o que exige decisão do membro (ex: conflito de nome de mecanismo entre a `offer-builder` e a `copy-engine`, ou modo escolhido que ficou inviável a meio caminho).

## Referências cruzadas

- **Próxima skill:** `page-build` (compila `design/page.html` em Liquid + deploya)
- **Conversor canônico (usado pela `page-build`):** `tools/design-clone/liquid-converter.py` (Modo C)
- **Gerador de paletas (ETAPA 2, marca vazia):** `.claude/lib/design-presets/palette_engine.py` (3 candidatas com motivo, harmonia declarada e contraste AA; os 8 presets de `presets.json` são a base dele + README)
- **Doutrina de imagem AI (ETAPA 1.6):** skill `creative-engine` ETAPA 1.0 (foto-real-primeiro — produto/rótulo nunca nasce de prompt de texto)
- **Geração de imagem in-session (sub-etapa 1.6.3, só com `mcp__higgsfield__`):** `reference/imagens-higgsfield.md` (o que se gera por `media.kind`, a régua lida por visão, as 3 tentativas e o caminho do arquivo até o slot); o prompt de pessoa é o da lib `.claude/lib/prompt-directors/real-people-imagery.md`
- **Segunda opinião (ETAPA 5, opcional):** `reference/brief-codex.md` (o briefing autossuficiente, o que o membro anexa e o placar de duas colunas)
- **Funil de quiz (sub-etapa 1.7, só com `page_type: quiz`):** `reference/quiz-funnel.md` (mapa de telas, de onde sai cada pergunta, os perfis e a oferta de cada um, o mecanismo sem JavaScript e o bloco `quiz` do plano); do outro lado, `.claude/skills/page-build/reference/quiz-sections.md` compila o funil numa section só
- **QA medido e revisor (ETAPA 5):** `.claude/lib/theme-verify/verify_page.py` (itens e bloqueantes no README da pasta), `reference/revisor.md` e `reference/qualidade-e-checkpoint.md`
- **Skill que audita o output:** `consistency-audit` (lê `page-plan.json` strategy + `design-tokens.json`)

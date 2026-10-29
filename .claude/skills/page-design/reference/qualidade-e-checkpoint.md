# Page Design · Referência: QA medido, revisor, preview e aprovação (ETAPAS 5 e 6)

> A medição do `page.html` pelo `verify_page.py` (`qa-metrics.json`), o revisor sem contexto (`review.md`), as rodadas de correção, a decisão do membro sobre item bloqueante, as regras de conversão que o revisor não vê, o preview de layout na Vercel, a aprovação com as fontes reais e os tokens finais com a política da marca. Abra depois que a ETAPA 4 gravou o `page.html`, antes do membro ver.

## ETAPA 5 · QA

### 5.1 Medir

```bash
python3 .claude/lib/theme-verify/verify_page.py "file://$PWD/workspace/[produto]/page/design/page.html" \
  --json-out workspace/[produto]/page/qa-metrics.json \
  --plan workspace/[produto]/page/page-plan.json \
  --shots-dir workspace/[produto]/page/qa-shots/ \
  [--legal workspace/[produto]/page/reference-capture/legal.json] \
  [--geodiff workspace/[produto]/page/reference-capture/geodiff.json]
```

`--legal` e `--geodiff` só no modo referência. O script mede em 390, 768 e 1440, regrava o `qa-metrics.json` do zero e sai com 1 quando há item bloqueante em `fail`. Os itens, os limites e o que cada um mede estão em `.claude/lib/theme-verify/README.md` e em `reference/regua-de-design.md` (cada item da régua diz se é medido, com o id, ou julgado).

- **Bloqueantes:** `script_tags`, `section_markers`, `section_ids_match_plan`, `horizontal_overflow`, `section_height_zero`, `broken_images`, `html_css_kb` e, no modo referência, `legal_check`.
- **Avisos:** o resto (contraste, tamanhos de fonte, gradientes, largura de linha, headline em 390, margens, faixas vazias, peso total, erros de console, geodiff). Aviso não trava, mas entra na rodada seguinte quando o revisor também aponta.

Sem o Playwright no venv (exit 3), avise em uma linha, siga com o revisor sobre capturas que você tirar como der, e registre no `page-plan.json` que a página não tem QA medido: a `page-build` vai bloquear até o membro rodar o setup do Playwright.

`page_type: quiz`: além disso, capture cada tela pelo endereço (`#`, `#q1`, ..., `#result-a`) nas duas larguras; a altura estável entre telas é o item M8 da régua.

### 5.2 O revisor sem contexto

Um subagente que vê só a página renderizada, as referências e a direção. É ele que pega o que o autor não vê.

- Chame pela tool `Agent` com `subagent_type: "general-purpose"`, o conteúdo de `reference/revisor.md` como prompt, com os caminhos preenchidos: `page/qa-shots/desktop-full.png`, `page/qa-shots/mobile-full.png`, as `page/references/<n>/desktop-full.png` das 3 marcadas e o `page/direction.md`. Não passe a conversa, o plano nem o HTML como texto.
- Ele grava `page/review.md`: nota de 1 a 5 em tipografia, espaço, cor, hierarquia, aderência à direção e sinais de "feito por IA", e as 5 correções de maior impacto.
- **Não há subagente** quando a tool `Agent` não está na sessão. Aí você mesmo pontua com a rubrica de `reference/revisor.md`, olhando só as capturas, e marca no topo do `review.md`: "revisão pelo autor (sem subagente)".

O revisor não bloqueia. As correções dele definem a rodada seguinte.

### 5.3 Rodadas de correção

Cada rodada: aplique as correções do `review.md` e os `fail` do `qa-metrics.json`, meça de novo (5.1) e chame o revisor de novo (5.2). O teto de rodadas e o critério de parada estão em `reference/regua-de-design.md`; pare antes do teto quando não houver item bloqueante em `fail` e nenhuma nota do revisor abaixo de 3. Corrigir um item costuma quebrar outro: a medição é sempre da página inteira.

Página parecendo parede de texto (mobile principalmente): não corte copy por conta própria; sinalize e rode a dieta de copy da `copy-engine` (sweep 4.5), com aprovação do membro.

### 5.4 Item bloqueante que sobrou

Depois do teto, item bloqueante em `fail` vai para o membro, em uma linha por item: o que está errado, o que foi tentado, o que depende dele.

- **Liberáveis:** `horizontal_overflow`, `broken_images` e `html_css_kb`. O membro decide; se liberar, registre em `page-plan.json.qa_overrides` um `{ "item": "<id>", "motivo": "<palavras do membro>", "data": "<YYYY-MM-DD>" }`. É o pré-flight da `page-build` (`tools/page-qa/qa_gate.py`) que combina a medição com a liberação.
- **Nunca liberáveis:** `script_tags`, `section_markers`, `section_ids_match_plan`, `section_height_zero` e `legal_check`. Sem eles a `page-build` não compila, a seção renderiza vazia ou a página expõe material de terceiro. Corrija ou volte à ETAPA 4.

### 5.5 O que o revisor não vê (conversão)

A medição e o revisor cobrem forma. Antes do checkpoint, confira você, no texto da página:

- **CTAs como call-to-value** ("Start My 30-Day Glow", não "Buy Now"). Fundamente em **CTAs / Calls to Value** (rode `CTAs buttons friction anxiety calls to value lizard brain first person mirror headline`) e decida direto vs stepping-stone com **Direct vs Transitional CTA** (rode `direct vs transitional CTA Miller buy now download guide stepping stone`).
- **As 4 modalities** (rode `4 decision making modalities spontaneous competitive humanistic methodical web copy`): Spontaneous (CTA acima da dobra), Competitive (diferenciação), Humanistic (prova social, rostos), Methodical (specs, garantia, FAQ). Falta de uma = furo de conversão.
- **Revenue per Session** (rode `revenue per session AOV vezes CVR problema de site ou de tráfego`): AOV × conversão, referência em torno de $2,50. É a régua que a `ad-analysis` vai usar; desenhe sabendo disso.
- **Congruência ad→página** (rode `congruence principle message match ad to landing page scent Kennedy consistency rule`): o topo ecoa a promessa do ad.
- **Por `page_type`:** advertorial e listicle seguem o contrato de `reference/page-type.md` (ids das 7 seções, botão único com âncora `#offer`), com a estética da direção; aplique os **Ogilvy 14 Readability Devices** (rode `Ogilvy 14 readability devices drop caps captions subheads reverse type`) e a **Double Readership Path** (rode `Kennedy double readership path skimmers analytical readers subheads PS`). Landing e PDP: prova acima da dobra. Quiz: `reference/quiz-funnel.md`.
- **Imagens do mapa de mídia:** toda seção com `media.required` tem a imagem real no slot, ou o placeholder explícito com `acquisition_plan`. Nunca imagem da referência, nunca `src` de sandbox.
- **Ícones SVG inline**, nunca emoji na UI.

Corrija inline o que faltar antes de mostrar.

## ETAPA 6 · Preview, aprovação, tokens e salvar

### 6.1 Preview de layout no celular (Vercel)

Com a skill `deploy-to-vercel`: avise em uma linha que o preview é um **link público** (quem tiver o link vê a página) e só publique com o sim do membro. Copie `page/design/` para `page/preview/` **sem** `assets/fonts/` (arquivo de fonte licenciada não vai para servidor de terceiro) e rode o deploy sem conta da skill:

```bash
bash ~/.claude/skills/deploy-to-vercel/resources/deploy.sh workspace/[produto]/page/preview
```

Grave o `previewUrl` devolvido em `page-plan.json.preview_url`. No preview a fonte local cai no fallback: ele serve para conferir layout, ritmo e toque no celular, não tipografia. Sem a skill, ou com o membro recusando o link público, siga só com as capturas.

### 6.2 Checkpoint de aprovação

Apresente como **draft navegável**, não como pronto: as capturas de `page/qa-shots/` (1440 e 390, com as fontes reais), o link de preview para abrir no celular, o resumo do `qa-metrics.json` (bloqueantes e avisos) e as notas do `review.md`.

> "Página montada (modo [direção|referência]). Abre o link no celular pra sentir o layout e olha as capturas pra fonte (no link ela cai no fallback). O que ajustar? O hero puxa atenção? A hierarquia de prova convence? A aprovação final de tipografia é na 6.9 da `page-build`, no tema, com a fonte real."

- **Segunda opinião, uma vez** (`reference/brief-codex.md`): o briefing que o membro cola no Codex; o HTML que voltar passa pela normalização e pela mesma ETAPA 5, e o membro escolhe pelo placar.
- Cada iteração com o membro salva versão nova (`design/page-v2.html`...), passa pela ETAPA 5 de novo e entra no `workspace/[produto]/page/iterations-log.json`.
- 3 iterações sem progresso: ofereça trocar de modo (direção ↔ referência) ou sortear outra direção na ETAPA 3.
- Não declare aprovado com slot de imagem pendente sem `acquisition_plan` (a `page-build` bloqueia o deploy enquanto o placeholder existir).
- Aprovado: consolide em `design/page.html` e meça uma última vez (5.1), para o `qa-metrics.json` corresponder ao arquivo final (o `qa_gate.py` confere o hash).

### 6.3 Tokens e marca

```bash
python3 tools/page-qa/tokens.py workspace/[produto]/page/design/page.html \
  --out workspace/[produto]/page/design-tokens.json \
  --source <brand_tokens|dembrandt|palette_engine|manual> [--preset-base <id>] \
  [--brand-out workspace/[produto]/brand/brand-tokens.json]
python3 tools/page-qa/tokens.py --diff workspace/[produto]/page/design-tokens.json workspace/[produto]/brand/brand-tokens.json
```

- `--brand-out` só quando o `brand-tokens.json` está vazio (`source: "none"`); depois de gravar, valide com `python3 tools/schema_validate.py .claude/templates/schemas/brand.brand-tokens.schema.json workspace/[produto]/brand/brand-tokens.json`. Marca não vazia: nunca escreva nela.
- O `--diff` dá o drift da página contra a marca (0 a 100 e o que mudou); ele vai para a mensagem final.
- **`tokens.py` falhou depois da aprovação** (exit 1, mais de 5 cores soltas; ou 2): a página continua aprovada, a marca não é tocada, o manifest **não** marca `page-design` como concluída, e a mensagem final diz o erro e o comando para rodar de novo depois de mover as cores soltas para o `:root`.

Depois, `page-plan.json` e manifest pela `reference/page-plan-e-salvar.md`.

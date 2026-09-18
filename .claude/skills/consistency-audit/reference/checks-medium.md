# Consistency Audit · Referência: Check battery, bloco MEDIUM (ETAPA 2, checks M1 a M7)

> Os checks de correção desejável: claim saturado (M1), gap não explorado (M2), hook-swap (M3), duração do script (M4), tipo de página e primeiro olhar (M5), tokens de design (M6) e placeholders (M7), com os sistemas da base e as queries exatas. Abra na ETAPA 2.

#### MEDIUM (nice to fix)

**M1. Saturated claim usage**
- Claims marcados como `saturation: HIGH` em `competitor-analysis/dados.json` aparecendo em hero ou hooks → `severity: medium`
- **Exceção que rebaixa o finding:** um claim saturado pode ser legítimo SE a copy o reapresenta com diferenciação. Puxe pra avaliar:
  - **Hopkins' Preemptive Claim (Schlitz Beer)** (rode `Hopkins preemptive claim Schlitz beer first to make common claims specific Road 3`) — se a copy é a PRIMEIRA a tornar o claim comum específico/concreto, ela "rouba" o claim saturado; nesse caso rebaixe pra pass/note, não medium.
  - **Inoculation Theory (McGuire)** (rode `Inoculation theory McGuire weakened attack vaccination strengthen attitudes competitor argument`) — se a copy antecipa o ceticismo ("você já ouviu isso de todo mundo, mas...") antes de fazer o claim saturado, é uso forte, não fraco.
  - **Defeito Reatribuído como Prova (Uncle Jim's Hail-Marked Apples)** (rode `macas marcadas por granizo prova de altitude menos pedidos de reembolso defeito reatribuido`) — terceiro caminho de rebaixamento: se a copy pega o elemento saturado ou negativo e o reatribui como evidência de qualidade (a marca do granizo virando prova de altitude), é uso forte — rebaixe pra pass/note.

**M2. Gap não explorado**
- `competitor-analysis/dados.json.gaps` é o objeto `{audience, messaging, format, offer, mechanism}` — achate as 5 dimensões numa lista única antes de cruzar (mesma situação do `voc_phrases` no H1; iterar como array direto falha).
- Gap forte identificado e nenhuma peça de copy/ad explora → `severity: medium`

**M3. Hook-swap misuse**
- Conceito marcado `hook_swap_viable: false` mas o Hooks Bank (`creative-engine/dados.json.hooks_bank[]`) tá sendo usado como swap source nesse conceito → `severity: medium`

**M4. Duration/word count mismatch**
- Script marcado pra 22s mas word count cabe em 15s (ou vice-versa) → `severity: medium`, `fix: ajustar duration ou cortar script`

**M5. Page type vs awareness**
- `page/page-plan.json.page_type` deve ser coerente com o awareness dominante de `market-research/dados.json` (Unaware/Problem Aware → advertorial; Solution Aware → landing; Product/Most Aware → pdp_robust/pdp_lean — mesma tabela da `page-design` ETAPA 1.1).
- Mismatch → `severity: medium` (a `page-design` confirma isso com o membro na criação; aqui é rede de segurança contra drift pós-iteração). `page-plan.json` ausente → `"skipped"`.
- **Além do tipo, julgue o PRIMEIRO OLHAR e o mix de seções** (quando `page/design/page.html` existe — a página com a copy real inserida). Puxe:
  - **Grunt Test (5-Second Clarity Diagnostic)** (rode `StoryBrand grunt test 5 second clarity hero section three questions`) — o hero responde em 5 segundos: o que é, o que melhora na minha vida, o que eu faço pra comprar? Falhar qualquer uma das 3 → `severity: medium` no mesmo check.
  - **Os 4 formatos de 5-Second Test (Memory Dump / Attitudinal / Target ID / Mix)** (rode `quatro formatos teste 5 segundos memory dump attitudinal target ID mix test`) — indica o formato certo pra VALIDAR o primeiro olhar (memory dump pro que a página comunica; target ID pra quem ela parece servir); usar no fix path quando o Grunt Test acima falhar — é o teste que o membro roda pra confirmar o fix.
  - **Button Placement Rules por estágio de awareness** (rode `botao nao pertence ao hero unless product-aware clique reflexo lizard brain nao converte`) — cruze com o awareness dominante da `market-research` (mesmo input deste check): CTA de compra no hero com público majoritariamente não-product-aware (advertorial/landing) → `severity: medium` no mesmo check.
  - **Decision Maker Sweep (DM Sweep)** (rode `Decision Maker Sweep mapear secoes spontaneous competitive humanistic methodical 10x page plan`) — mapeie `sections_plan[]`/as seções da página contra os 4 perfis de decisor (spontaneous, competitive, humanistic, methodical); perfil inteiro sem NENHUMA seção que o sirva (ex.: zero specs/FAQ pro methodical) → `severity: medium`.
  - **16 Táticas de Redução de Bounce** (rode `reduzir bounce rate auditoria mobile repensar hero mover proof bar reduzir CTAs para um`) — o MENU DE FIX dos findings deste check, na ordem de diagnóstico list → offer → copy; na re-validação pós-iteração (quando `ad-analysis/dados.json` existe e aponta clique sem conversão), vira a fila de correção da página.

**M6. Design tokens vs design system**
- Paleta e tipografia de `page/design-tokens.json` (variação aprovada) devem bater com o documentado em `page/design-system.md`.
- Divergência (hex do accent diferente, font-family trocada) → `severity: medium`, `fix: regenerar o design system a partir dos tokens da variação aprovada (`page-design`)`. Artefatos ausentes → `"skipped"`.

**M7. Placeholders não-resolvidos em template/copy deployada**
- Varrer os artefatos consumidor-final que já existem — `copy-engine/copy-engine.md` (copy final), `page/design/page.html` (design aprovado com a copy real inserida), o template JSON/sections populados pela `page-build`, e os emails da `retention-engine` Fase A (`retention-engine/[fluxo]/email-N.html`) — procurando tokens de placeholder que deveriam ter sido substituídos por conteúdo real: `{{ALGO_EM_CAPS}}` (ex: `{{BONUS_LINK}}`, `{{MECHANISM_NAME}}`), stand-ins entre colchetes (`[HEADLINE]`, `[PLACEHOLDER]`, `[TBD]`), números de mentira (`XX%`, `$XX`) e "lorem ipsum".
- **Exceções (não são finding):** tags Liquid legítimas de objeto (`{{ product.title }}`, `{{ shop.* }}`, `{% ... %}`) e merge tags de ESP (`{{ first_name }}` do Klaviyo) — o alvo são stand-ins de CONTEÚDO em caixa alta ou colchetes, não a sintaxe do template.
- Placeholder achado → `severity: medium` (caso clássico: `{{BONUS_LINK}}` num email ainda em draft aguardando o asset da `bonus-delivery` — fix: "colar o link do asset da `bonus-delivery` antes de ativar o flow"). **Escalar pra `severity: high` se o placeholder está numa superfície JÁ PUBLICADA** (PDP/landing no ar) — consumidor vendo `{{...}}` na página quebra a confiança na hora.

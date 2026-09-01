---
name: consistency-audit
description: Auditoria cross-phase que valida consistência entre os artefatos gerados nas skills 01-08, incluindo a página (07a — page-plan.json/design-tokens), o checkout (07d) e os artefatos pré-launch da 05 (Fase A — assets de bônus) e da 13 (Fase A — flows de recuperação). Detecta drift (mecanismo muda entre offer, copy e página, VOC phrase não aparece em nenhum hook, claim sem research foundation, promessa sem config de loja, bonus removido da oferta mas ainda anunciado, placeholder não-resolvido em copy deployada, etc). Use quando o membro disser "audit", "consistência", "review", "verificar coerência" ou antes de launch oficial. Roda smoke checks em minutos, retorna report com severity-ranked issues e fix paths.
---

# Cross-Phase Consistency Audit

## Base de conhecimento (contrato de cobertura — NUNCA query genérica)

Esta skill audita coerência cross-phase; quando precisar JULGAR qualidade de um claim, proof, ou alinhamento (não só comparar strings), puxe SISTEMAS NOMEADOS da base via `search_knowledge` — nunca query genérica tipo "audit checklist" ou "landing page review". E a puxada é **cobertura do tópico, não amostra** (contrato completo: `.claude/lib/kb-index/README.md`):

1. **Abra a seção inteira dos domínios, sempre.** No início da ETAPA 2 (check battery), abra `.claude/lib/kb-index/frameworks.json` e enumere TODAS as entradas dos domínios **`copy-proof-persuasion-structure`** e **`page-landing-cro`** cujo `use_in_skill` inclui a 09 — não só as embutidas nos checks. As queries embutidas abaixo são o **núcleo mínimo garantido de cada check, nunca o teto**: entrada relevante ao julgamento de um check que não está embutida É PARA SER PUXADA do mesmo jeito.
2. **Rode a `best_query` exata de cada entrada relevante, com `deep=true`**, puxando o sistema completo (as 10 categorias de proof de Schwab, não "tipos de prova").
3. **Relevância é por CHECK, não por preguiça:** a pergunta é "esta entrada muda o veredito deste check?" — se a resposta for "talvez", puxa. Só se descarta o que claramente pertence a outra skill (escrita é da 06, design é da 07a — aqui é julgamento de auditoria).
4. **Não repita busca de framework já puxado na mesma sessão** — entradas duplicadas entre os dois domínios apontam pro MESMO conteúdo; reuse o resultado.
5. **Encerramento:** antes de fechar a ETAPA 2, releia a lista enumerada do passo 1 e confirme que nenhuma entrada relevante ficou sem puxar.

A contagem de entradas por domínio **vem sempre do próprio `frameworks.json`** (fonte da verdade) — nunca de número fixo escrito no texto desta skill. Mapa skill→domínio no README do kb-index.

## Quando Usar

Antes de launch oficial (ads go-live + page em produção), rodar esta skill pra pegar incoerências acumuladas ao longo das skills 01-08 — incluindo os artefatos pré-launch da 05 (Fase A) e da 13 (Fase A), que na ordem canônica já existem neste ponto. Exemplos reais de drift:

- Mecanismo único nomeado "X" na skill 04 virou "X-alt" nas variações de hook da skill 08
- VOC phrase repetida 12x no market research NÃO aparece em nenhum hook do ad batch
- Claim "clinically proven" aparece no hero da página mas `04-offer-builder/research-foundation.json` não tem estudo correspondente
- Guarantee copy diz "90 days" mas `04-offer-builder/dados.json` diz 30 days
- Promo banner promete "free US shipping" mas Shopify shipping zones cobram $X em algumas regiões
- Ad primary text menciona bonus que foi removido na última iteração do offer stack

## Pré-flight

- [ ] `workspace/[produto]/manifest.json` existe com `setup_complete: true`
- [ ] Pelo menos 3 skills completed em `skills_completed[]` (senão não há o que comparar)

**report_language:** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo — inclusive `issue` e `fix_suggested` dos findings) e toda conversa com o membro usam esse idioma, seguindo o padrão de linguagem simples da regra 0 do `.claude/CLAUDE.md` (nenhuma sigla sem explicação imediata, zero frase de analista comprimida, números estatísticos em palavras). **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language — o trecho auditado é citado no original, o veredito sobre ele vai no idioma do report.

**Input parcial (safeguard):** se `06-copy-engine/{copy-engine.md,dados.json}` E `08-creative-engine/dados.json` estiverem AMBOS ausentes, não há copy nem ad pra cruzar — force `launch_recommendation: "CAUTION"` (nunca `GO`), registre cada artefato faltante em `artefacts_missing[]`, e marque os checks que dependem deles como `"skipped"` (nunca `"pass"`). Não aborte: rode os checks que forem possíveis com o que existe e avise no output final que recomenda re-executar após gerar copy/criativos.

## Fluxo da Skill

### ETAPA 1 — Load artefatos

Ler todos os artefatos disponíveis (só os que existem):

- `01-product-research/product-research.md` (+ json se existir)
- `02-market-research/market-research.md` (se não existir, leia o legado `relatorio.md` — mesmo fallback vale pras outras fases) + `02-market-research/dados.json` → extract `voc_phrases[]`, `awareness_distribution`, `sophistication_stage`
- `03-competitor-analysis/competitor-analysis.md` + `03-competitor-analysis/dados.json` → extract `claims_saturation[]`, `swipe_adapt[]`, `positioning_recommendation`
- `03-competitor-analysis/creative-patterns.json` (se existir) → extract `hook_archetypes[]`, `recurring_claims[]`
- `04-offer-builder/offer-builder.md` + `04-offer-builder/dados.json` → extract `mechanism.name`, `mechanism.ump.name`, `mechanism.ums.name`, `guarantee`, `pricing`, `bonuses[]` (schemas legados podem ter `mechanism.version_short` no lugar de `ump`/`ums` — aceitar ambos)
- `04-offer-builder/research-foundation.json` → extract `evidence_items[]`, claims supported, `confidence_score`, `mechanism_name` (top-level)
  - **Se AUSENTE:** automaticamente criar CRITICAL finding C2b "Research foundation não rodou — todos os claims de copy/ads saem sem lastro verificável." Oferecer 2 caminhos: **(A)** rodar Skill 04 Etapa 2.5 agora pra gerar o lastro, OU **(B)** prosseguir com o check flagado como critical marcando `manifest.skipped_preflight += ["04-offer-builder/research-foundation.json"]` e avisando no output final que recomenda re-executar. Não pule o check.
  - **Sinal explícito adicional:** `06-copy-engine/dados.json.claims_unverified: true` dispara o MESMO finding C2b, mesmo que o `research-foundation.json` exista agora — significa que a copy foi escrita ANTES do lastro existir (membro escolheu prosseguir no pré-flight da 06). Nesse caso o fix é re-validar os claims da copy contra o research-foundation atual (não basta o arquivo existir; a copy nasceu sem ele). Mais robusto que só detectar ausência do arquivo, porque cobre o cenário do membro gerar o research-foundation DEPOIS da copy.
- `05-bonus-delivery/bonus-delivery.md` **(if exists)** + assets em `05-bonus-delivery/bonuses/[bonus-id]/` → extract status da Fase A por bônus (asset gerado? GWP/delivery configurado? "pronto pro launch"?) — alimenta o H5. Se há bônus visível na PDP e a 05 nunca rodou, o próprio H5 flaga (não bloqueia a carga).
- `06-copy-engine/copy-engine.md` + `06-copy-engine/dados.json` → extract headlines, hero, mechanism mentions, claims, promises + os campos top-level `lead_type` (enum: `story|big_idea|problem_agitation|mechanism|secret|proclamation|offer|direct` — alimenta o H2) e os flags de pré-flight `claims_unverified` (alimenta o C2b) e `voc_forced_continue` (contexto pro H1: se `true`, a copy nasceu com VOC insuficiente — coverage baixo no H1 ganha essa causa provável no finding, com fix "re-rodar skill 02 e re-gerar a copy")
- `07-page/page-plan.json` → extract `strategy.mechanism_name`, `page_type`, `sections_plan[]`, `section_order`, `brand_discovery` (alimenta C1c e M5)
- `07-page/design-system.md` → extract paleta, tipografia (alimenta M6 — comparação com os tokens)
- `07-page/design-tokens.json` (gerado por 07a, qualquer rota) → tokens extraídos da variação aprovada (alimenta M6)
- `07d-checkout-aov/dados.json` **(if exists)** → extract config aplicada de bump/upsell/free-shipping threshold (alimenta o C4: promessa de checkout vs config real)
- `08-creative-engine/dados.json` → extract hooks, primary_texts, headlines per concept + `hooks_bank[]` top-level
- `13-retention-engine/[fluxo]/email-N.html` + `flow-metadata.json` **(if exists — a Fase A da 13 roda pré-launch na ordem canônica: abandoned cart + post-purchase)** → alimenta o M7 (placeholders tipo `{{BONUS_LINK}}` ainda não preenchidos) e dá contexto ao gate (flows de recuperação prontos antes do go-live)
- `10-ad-strategy/dados.json` **(if exists)** — no modo pré-launch ainda não existe (a 10 roda depois da 09); só lê se presente, nunca bloqueia por ausência.
- `11-ad-analysis/dados.json` **(if exists)** → extract `psm_real`, `winners[]`, `recommended_action` — só existe na re-execução pós-iteração, nunca no pré-launch.
- `manifest.json.agentic` **(if exists)** → `{ready, channel_enabled, score, checked_at}` escrito pela 07e — **contexto INFORMATIVO no gate de launch, NUNCA bloqueante** (agentic readiness é canal incremental, não pré-requisito de ads). Se presente com `ready: false` ou itens `blocked_pending` em `07e-agentic-readiness/dados.json`, mencione no output como nota informativa: esses itens apontam pras mesmas superfícies que o C4 (promise↔config) já confere (JSON-LD/agent-facts vs config real da loja) — se o C4 achou drift nessas superfícies, o dado da 07e ajuda a localizar. Ausente → silêncio (a 07e pode não ter rodado; não é finding).

> **A 09 roda em dois momentos:** (1) **gate pré-launch** — antes de ads go-live e page em produção, com artefatos 01-08; nesse modo `10-ad-strategy/dados.json` e `11-ad-analysis/dados.json` não existem ainda e devem ser lidos só `if exists` (inversão de dependência: a 10 e a 11 dependem da 09 passar, não o contrário). (2) **re-validação pós-iteração** — depois de corrigir issues ou rodar batches, quando 10/11 já existem e entram no cruzamento.

### ETAPA 2 — Check battery (ordenada por severity)

#### CRITICAL (bloqueia launch)

**C1. Mecanismo name consistency**
- `04-offer-builder/dados.json.mechanism.name` deve aparecer LITERALMENTE em:
  - Pelo menos 1 headline de `06-copy-engine/copy-engine.md`, E
  - Pelo menos 1 conceito de `08-creative-engine/dados.json` — vale no hook, no Bridge/Hold do script ou em primary text. Não exija o nome literal no hook de 3s: a doutrina de hook da 08 é abrir loop (gap theory), não explicar; o mecanismo pode entrar no corpo do ad.
- Ausente em AMBOS os lados (copy E ads) → `severity: critical`, `fix: inject mechanism name in hero + no corpo de pelo menos 1 conceito`
- Presente em só UM dos lados → `severity: high` (drift parcial: o consumidor vê o mecanismo numa fase da jornada e não na outra)

**C1b. Mechanism name normalizado (04 ↔ research-foundation)**
- `04-offer-builder/dados.json.mechanism.name` DEVE ser idêntico a `04-offer-builder/research-foundation.json.mechanism_name` (campo top-level).
- Divergência → `severity: critical`, `check_id: "mechanism-drift"`, `fix: alinhar o nome do mecanismo entre offer e research-foundation antes de propagar pra copy/ads`. (É a fonte da verdade do mecanismo; se essas duas já divergem, todo C1 abaixo herda o drift.)

**C1c. Mechanism name na página (04 ↔ 07-plan)**
- `07-page/page-plan.json.strategy.mechanism_name` DEVE ser idêntico a `04-offer-builder/dados.json.mechanism.name` — a 07a grava esse campo LITERAL exatamente pra este check (ver nota no schema da 07a).
- Divergência → `severity: critical` (a página é o artefato de maior visibilidade pro consumidor; mecanismo com nome diferente na página vs ads quebra o message match do funil inteiro), `fix: corrigir o strategy block do page-plan.json e re-gerar a section afetada`.
- `07-page/page-plan.json` ausente (página ainda não planejada) → check `"skipped"`.

**C2. Claim sem research foundation**
- Pra cada claim forte em `06-copy-engine/copy-engine.md` (hero, mechanism section, proof blocks) e `08-creative-engine/dados.json` (hooks + primary_texts):
  - Cross-check com `04-offer-builder/research-foundation.json.evidence_items[]`
  - Se o claim NÃO tem match → `severity: critical`, `fix: add evidence OR soften claim ("helps with" instead of "proven to")`
- **Não é só "tem match sim/não" — julgue se o PROOF SUSTENTA o CLAIM.** Puxe estes sistemas da base pra calibrar o veredito (rode a `best_query` de cada um):
  - **Bencivenga's 'Yeah, Sure' Principle** (rode `Bencivenga yeah sure principle proof must match claims promise outweighs proof doctors headache`) — proof tem que ser proporcional à ousadia do claim; claim grande com proof fraco dispara o reflexo "yeah, sure". É o gate central deste check.
  - **Hopkins' Specificity Principle (Reason-Why)** (rode `Hopkins specificity principle reason-why platitudes generalities specific claims transformation`) — claim vago/genérico (sem número, sem mecanismo, sem reason-why) é fraco mesmo "com evidence". Flag claim que é platitude.
  - **Schwab's Ten Categories of Proof** (rode `Schwab ten categories of proof taxonomy five principles presenting proof testimonials`) — classifica o TIPO de proof disponível em `04-offer-builder/research-foundation.json`; se o claim exige proof tipo X mas só existe tipo Y, é gap real.
  - **Made to Stick — Audience-Testable Credibility + Sinatra Test** (rode `Made to Stick three wellsprings credibility external internal audience-testable Heath` e `Sinatra Test one example so impressive establishes credibility case study`) — se um único caso/demo carrega o claim sozinho, marca como forte; se nem isso existe, agrava o finding.
  - **Puffery (hipérbole como bypass de substanciação)** (rode `puffery hiperbole evitar sustentar claim biggest no-brainer OMG that was easy`) — separa claim que EXIGE lastro de hipérbole reconhecível que dispensa substanciação ("best decision ever"); evita finding falso em cima de puffery legítima — e pega o inverso: número ou promessa concreta tentando passar por puffery.
  - **Auditoria de prova — vocabulário de Kyle Milligan + o "Imagery Hack"** (rode `auditoria de prova numere as provas 3 to 6 examples mais fraca no meio fracao vence porcentagem`) — julga a APRESENTAÇÃO do proof que existe: provas numeradas, 3 a 6 exemplos, a mais fraca no meio, fração vencendo porcentagem. Evidence presente mas mal apresentada é finding de fix barato (medium, não critical).
  - **Auditoria de especificidade** (rode `auditoria de especificidade claims especificos 21 a 53% mais criveis timeline do processo`) — régua medida pro julgamento do Hopkins acima: claim específico é 21 a 53% mais crível; claim sem número, timeline ou detalhe de processo perde essa margem mesmo "com evidence".
  - **Os 4 Erros de Conversão que o Critique caça (Kyle Milligan)** (rode `selling from your heels, pinte a imagem antes de oferecer o dinheiro de volta, mostre o resultado não o processo`) — lente de erro de conversão sobre os mesmos claims: vender na defensiva (claim hedged demais mesmo com lastro), mostrar o processo em vez do resultado, e oferecer o dinheiro de volta antes de pintar a imagem — este último alimenta também o C3.
  - **Greek Sweep (Ethos / Logos / Pathos)** (rode `greek sweep ethos logos pathos passada de edicao prova e emocao long copy`) — mapeia onde a peça concentra prova vs emoção; trecho todo pathos carregando claim forte sem nenhum logos por perto é exatamente onde este check mais acha gap.
  - **Empty vs Performance Testimonial (Settle) + os 3 formatos de elite** (rode `empty vs performance testimonial criterio de descarte retrato demografico asset nomeado`) — quando o "evidence" do claim é depoimento/review: depoimento vazio ("love it!") não sustenta claim de performance; aplicar o critério de descarte antes de aceitar o match.

**C3. Guarantee copy divergente**
- `04-offer-builder/dados.json.guarantee.duration_days` vs texto em `06-copy-engine/copy-engine.md` guarantee section vs `08-creative-engine/dados.json` primary_texts
- Divergência (30 vs 60 vs 90 dias) → `severity: critical`
- **Não é só duração — julgue também a POSIÇÃO da garantia.** O sistema **Os 4 Erros de Conversão** (mesma puxada do C2 — não repita a busca) marca como erro oferecer o dinheiro de volta ANTES de pintar a imagem do resultado: garantia aparecendo antes do value build na página/copy → `severity: medium` no mesmo `check_id` (a divergência de duração continua `critical`).

**C4. Promessa sem config**
- Trigger o Promise↔Config gate (`.claude/rules/pre-launch-gates.md`)
- Inclui o checkout (se `07d-checkout-aov/dados.json` existe): threshold de free-shipping prometido na barra/copy vs threshold configurado; desconto prometido no bump/upsell vs desconto realmente aplicado na config — promessa não-cumprida no checkout é onde nasce chargeback
- **Urgência/escassez também é promessa.** Puxe **Urgency / Scarcity / FOMO como três alavancas distintas** (rode `urgency scarcity FOMO tres alavancas distintas hot sauce seeds of regret why 500`) — toda urgência/escassez em página/copy/ad precisa de mecânica REAL por trás: deadline que existe de verdade, estoque verdadeiro, limite com "Why?" respondível. Alavanca anunciada sem lastro na config/realidade da loja → mesmo tratamento de promessa sem config (`fail`).
- Qualquer `fail` → `severity: critical`

**C5. Ad-flag compliance drift**
- Trigger Compliance Pre-flight em todo output consumidor-final
- `severity: critical` em qualquer peça → reportar

#### HIGH (recomendar fix antes de launch)

**H1. VOC coverage**
- `02-market-research/dados.json.voc_phrases` é o objeto `{problem:[], desire:[], frustration:[]}` — achate os 3 pools numa lista única de frases.
- **Denominador = subconjunto prioritário, NUNCA o pool inteiro.** Monte o subconjunto das **20 frases mais repetidas** (é o mesmo `voc_checklist` que a Skill 06 usa — se a 06 já rodou, reuse a lista dela). Dividir pelo `voc_count` total penalizaria matematicamente quem coletou mais VOC: com 80+ frases coletadas e um batch starter de 2-3 conceitos, 30% do pool inteiro é fisicamente impossível de cobrir.
- `coverage = frases do subconjunto prioritário parafraseadas em hooks/headlines/primary_texts da skill 08 (incluindo o hooks_bank[] top-level) / 20`.
- Coverage < 30% → `severity: high` (copy não tá espelhando voz do cliente)
- **Não conte só presença — julgue se a frase exata do cliente foi PRESERVADA ou diluída pra jargão de marketer.** Calibre com:
  - **Collier's Mental Conversation / Enter the Conversation** (rode `Collier six essentials sales letter mental conversation enter conversation in customer's mind word pictures`) — a copy entra na conversa que JÁ acontece na cabeça do cliente? VOC parafraseada pra linguagem corporativa perde isso, mesmo "cobrindo" o tema.
  - **Cashvertising — PVAs + VAKOG Mental Movies** (rode `Cashvertising extreme specificity PVAs powerful visual adjectives VAKOG mental movies five senses`) — VOC forte é palpável/sensorial; se a copy abstraiu a dor concreta do cliente, flag mesmo com coverage alto.
  - **Mona Lisa Frame** (rode `Mona Lisa Frame show dont tell placa embaixo do quadro half the words double the examples`) — VOC forte MOSTRA a cena; se a frase que o cliente descreveu virou afirmação abstrata na copy, é telling: o tema foi coberto, mas a frase morreu no caminho.
  - **Voz como Bloco Estrutural + auditoria de "Us" Language** (rode `character bloco funcional regular guy humble paint the picture not much us language`) — mede quanto a copy fala de si ("we/our formula") em vez de entrar na conversa do cliente; excesso de us-language derruba o espírito deste check mesmo com o coverage numérico ok.

**H2. Awareness alignment**
- Awareness dominante em `02-market-research/dados.json` deve alinhar com o tipo de lead escolhido pela 06 — leia o campo **top-level `lead_type` de `06-copy-engine/dados.json`** (enum: `story|big_idea|problem_agitation|mechanism|secret|proclamation|offer|direct`, gravado na ETAPA 2 da 06). Só caia pra inferir da prosa de `copy-engine.md` se o campo não existir (dados.json legado, gerado antes do contrato).
- Unaware/Problem Aware → deveria ser `story`/`secret`
- Product/Most Aware → deveria ser `offer`/`direct`
- Mismatch → `severity: high`
- **Pra julgar SE o lead realmente serve o awareness level (não só "qual tipo é"), puxe:**
  - **Bencivenga's IF...THEN + I=B+C + Shake-Me-Awake Test** (rode `Bencivenga IF THEN construction I equals B plus C interest benefit curiosity shake me awake test`) — lead pra audiência menos aware precisa de mais Curiosity no I=B+C; lead direto pra audiência aware pode liderar com Benefit. Confira o balanço da abertura contra o awareness.
  - **Brunson's Epiphany Bridge + Three False Beliefs** (rode `Brunson big domino three false beliefs vehicle internal external epiphany bridge story expert secrets`) — pra Unaware/Problem Aware, o Story/Secret Lead tem que carregar a epiphany bridge e quebrar as crenças falsas; se a copy pula direto pro produto, o mismatch é mais grave que só "tipo de lead errado".
  - **Grade de Auditoria de Long-Form (Kyle Milligan — 4 grades + 7 críticas)** (rode `quatro grades auditoria 4 U's lead Makepeace checklist desejabilidade Beats body copy formula`) — a régua MEDIDA pro lead e pra ordem da peça: lead de 4 passos com `[END LEAD]` demarcado, a oferta abrindo entre 48% e 70% da peça, credibilidade entrando DEPOIS da prova. Lead do tipo certo pro awareness mas abrindo a oferta cedo demais é finding deste mesmo check.

**H3. Sophistication vs mechanism match**
- Stage 3 → mercado cansou das promessas: exige um **mecanismo novo featured no headline** (o "como funciona" diferente vira o gancho principal).
- Stage 4 → mercado já viu o mecanismo: exige **elaborar o MESMO mecanismo** (mais forte, mais rápido, mais fácil), não trocar de mecanismo nem virar "information-based".
- Stage 5 → mercado cansou de mecanismos: exige **identification** (identidade/pertencimento, não o mecanismo).
- Check contra `04-offer-builder/dados.json.mechanism`: comparar SE/COMO um mecanismo está featured no headline (Stage 3) ou sendo elaborado (Stage 4), e se Stage 5 puxa identity. Mismatch → `severity: high`.
- **Pra julgar a FORÇA do headline contra o stage (não só "tem mecanismo sim/não"), puxe:**
  - **Schwartz's 38 Verbalization Techniques** (rode `Schwartz 38 verbalization techniques strengthen headline measure compare metaphorize paradox three functions`) — em Stage 3/4 o headline tem que intensificar o mecanismo (measure, compare, metaphorize); headline morno que só NOMEIA o mecanismo é fraco mesmo "alinhado".
  - **Reeves' USP + Vampire Claims** (rode `Reeves USP burning glass vampire claims mosaic structure single proposition unrelated claims`) — em mercado saturado, claims não-relacionados drenam a única proposição; flag headline/hook que dilui o mecanismo único com promessas paralelas.
  - **Caples' Three Classes of Headlines** (rode `Caples three classes headlines self-interest news curiosity six first-paragraph formulas shocker preview`) — Stage 3 (mecanismo novo) pede classe News/Curiosity; Stage 4 (elaborar) pede Self-Interest reforçado. Confira a classe do headline contra o stage.
  - **NESB em modo diagnóstico + "Selling From Your Heels"** (rode `NESB modo diagnostico auditoria de landing page selling from your heels paint the picture`) — scorecard de desejabilidade (New/Easy/Safe/Big) aplicado ao headline/hero: em Stage 3/4 o "New" tem que estar carregado pelo MECANISMO, não por adjetivo; headline na defensiva (heels) em mercado saturado é fraqueza mesmo com o mecanismo presente.
  - **3 Checks de Copy (Visualize / Falsify / Only You)** (rode `3 checks visualize falsify only you filtro de copy antes de publicar`) — o competitor-swap test operacionaliza o Reeves acima: ponha o produto do maior concorrente no headline/hook — se a peça continua fazendo sentido, o mecanismo não está carregando a proposição (finding deste mesmo check).

**H4. Ad angles diversification**
- **Dim 1 — emotion:** `emotion_dominant` vive em `08-creative-engine/dados.json.concepts[].emotion_dominant` (nível do concept; também dentro de `concepts[].hooks[]`). O batch deve cobrir ≥ 2 emotions distintas das 4 Hook Emotions que a 08 grava: **curiosity, urgency, fear, delight** (é o enum literal do campo — não usar nenhuma outra lista).
- **Dim 2 — embalagem:** ler **`08-creative-engine/dados.json.concepts[].concept_type`** — é o campo com cardinalidade fixa (o enum de 8 que antes se chamava `angle`). Deve cobrir ≥ 3 valores distintos (ou ≥ 3 verticais distintas se o schema usar `vertical`). **Fallback legado:** produto antigo em que `concepts[].angle` ainda é um dos 8 valores do enum → conte por ali.
- **Dim 2b — ângulo (só quando `testing_method == "marksman"`):** `concepts[].angle` agora é **frase livre** (a razão de compra, ex.: "para de virar de um lado pro outro a noite toda"), não enum — contar valores distintos ali não mede mais diversificação de embalagem. Num conceito Marksman, exija **3 frases de ângulo distintas lendo `concepts[].angles[]`** — o array que a 08 grava exatamente pra isso (itens `{creative_n, angle, sub_avatar_id}`, um por criativo; obrigatório quando `testing_method: "marksman"`, `null` em sniper): as 3 strings `angles[].angle` do conceito devem ser distintas entre si. **`concepts[].angle` NÃO serve pra essa contagem** — no marksman ele carrega só o ângulo do criativo #1 (alias do item `creative_n: 1`). **Fallback legado:** dados.json gerado antes do contrato (conceito marksman sem `angles[]`) → conferir os 3 ângulos listados no briefing do conceito (`concept-NN`, que os lista um por criativo); se nem o briefing os trouxer, contar frases distintas de `concepts[].angle` através do pack e registrar no finding que a leitura é parcial (só o ângulo #1 de cada conceito). Num pack Sniper, o ângulo único é a premissa do método e **não é finding**. Cânone: `.claude/lib/ad-taxonomy/README.md` §7.
- Se concentrado em 1 emotion OU < 3 `concept_type`/verticais → `severity: high`, `fix: gerar concept complementar com emotion/embalagem ausente`.

> **Dim 1 continua válida:** `emotion_dominant` foi preservado pela 08 como campo **derivado** de `valence`/`intensity` (justamente para não quebrar este gate), e mantém os 4 valores literais.

**H5. Bonus drift (promessa fantasma)**
- Toda menção a bonus em hooks/primary_texts/headlines de `08-creative-engine/dados.json` e no hero/offer stack de `06-copy-engine/copy-engine.md` deve ter entry correspondente em `04-offer-builder/dados.json.bonuses[]` (o campo que a Skill 05 consome).
- Bonus mencionado na copy/ad e AUSENTE do `bonuses[]` atual → `severity: high` (promessa fantasma: bonus removido do stack ainda sendo anunciado — exatamente o drift do exemplo em "Quando Usar"), `fix: remover a menção OU devolver o bonus ao stack (decisão do membro)`.
- Bonus presente em `bonuses[]` e nunca mencionado em copy/ad → não é finding (nem toda oferta anuncia todos os bônus em toda peça).
- **Fase A da Skill 05 completa (gate de launch):** todo bônus visível na PDP (`condition: unconditional` ou `cart_threshold`) precisa ter a Fase A da 05 concluída ANTES do go-live — asset existente em `05-bonus-delivery/bonuses/[bonus-id]/` (PDF/config GWP conforme `type`) E status "pronto pro launch" no `05-bonus-delivery/bonus-delivery.md`. Bônus prometido na página sem asset/config → `severity: high`, `fix: rodar a Fase A da Skill 05 antes do primeiro ad`. Skill 05 nunca rodou e há bônus na PDP → mesmo finding.
- **Condition ↔ copy da página:** a `condition` de cada `bonuses[]` deve bater com a copy — `cart_threshold` exige a condição explícita na página ("FREE over $X", com o X do threshold configurado); `unconditional` exige promessa SEM condição (e auto-add sem threshold na config). Página prometendo incondicionalmente um GWP que na config só destrava acima de threshold (ou vice-versa) → `severity: high`, `fix: alinhar copy OU config (decisão do membro — ver Skill 05 ETAPA 2)`.

#### MEDIUM (nice to fix)

**M1. Saturated claim usage**
- Claims marcados como `saturation: HIGH` em `03-competitor-analysis/dados.json` aparecendo em hero ou hooks → `severity: medium`
- **Exceção que rebaixa o finding:** um claim saturado pode ser legítimo SE a copy o reapresenta com diferenciação. Puxe pra avaliar:
  - **Hopkins' Preemptive Claim (Schlitz Beer)** (rode `Hopkins preemptive claim Schlitz beer first to make common claims specific Road 3`) — se a copy é a PRIMEIRA a tornar o claim comum específico/concreto, ela "rouba" o claim saturado; nesse caso rebaixe pra pass/note, não medium.
  - **Inoculation Theory (McGuire)** (rode `Inoculation theory McGuire weakened attack vaccination strengthen attitudes competitor argument`) — se a copy antecipa o ceticismo ("você já ouviu isso de todo mundo, mas...") antes de fazer o claim saturado, é uso forte, não fraco.
  - **Defeito Reatribuído como Prova (Uncle Jim's Hail-Marked Apples)** (rode `macas marcadas por granizo prova de altitude menos pedidos de reembolso defeito reatribuido`) — terceiro caminho de rebaixamento: se a copy pega o elemento saturado ou negativo e o reatribui como evidência de qualidade (a marca do granizo virando prova de altitude), é uso forte — rebaixe pra pass/note.

**M2. Gap não explorado**
- `03-competitor-analysis/dados.json.gaps` é o objeto `{audience, messaging, format, offer, mechanism}` — achate as 5 dimensões numa lista única antes de cruzar (mesma situação do `voc_phrases` no H1; iterar como array direto falha).
- Gap forte identificado e nenhuma peça de copy/ad explora → `severity: medium`

**M3. Hook-swap misuse**
- Conceito marcado `hook_swap_viable: false` mas o Hooks Bank (`08-creative-engine/dados.json.hooks_bank[]`) tá sendo usado como swap source nesse conceito → `severity: medium`

**M4. Duration/word count mismatch**
- Script marcado pra 22s mas word count cabe em 15s (ou vice-versa) → `severity: medium`, `fix: ajustar duration ou cortar script`

**M5. Page type vs awareness**
- `07-page/page-plan.json.page_type` deve ser coerente com o awareness dominante de `02-market-research/dados.json` (Unaware/Problem Aware → advertorial; Solution Aware → landing; Product/Most Aware → pdp_robust/pdp_lean — mesma tabela da 07a ETAPA 1.1).
- Mismatch → `severity: medium` (a 07a confirma isso com o membro na criação; aqui é rede de segurança contra drift pós-iteração). `page-plan.json` ausente → `"skipped"`.
- **Além do tipo, julgue o PRIMEIRO OLHAR e o mix de seções** (quando `07-page/design/page.html` existe — a página com a copy real inserida). Puxe:
  - **Grunt Test (5-Second Clarity Diagnostic)** (rode `StoryBrand grunt test 5 second clarity hero section three questions`) — o hero responde em 5 segundos: o que é, o que melhora na minha vida, o que eu faço pra comprar? Falhar qualquer uma das 3 → `severity: medium` no mesmo check.
  - **Os 4 formatos de 5-Second Test (Memory Dump / Attitudinal / Target ID / Mix)** (rode `quatro formatos teste 5 segundos memory dump attitudinal target ID mix test`) — indica o formato certo pra VALIDAR o primeiro olhar (memory dump pro que a página comunica; target ID pra quem ela parece servir); usar no fix path quando o Grunt Test acima falhar — é o teste que o membro roda pra confirmar o fix.
  - **Button Placement Rules por estágio de awareness** (rode `botao nao pertence ao hero unless product-aware clique reflexo lizard brain nao converte`) — cruze com o awareness dominante da 02 (mesmo input deste check): CTA de compra no hero com público majoritariamente não-product-aware (advertorial/landing) → `severity: medium` no mesmo check.
  - **Decision Maker Sweep (DM Sweep)** (rode `Decision Maker Sweep mapear secoes spontaneous competitive humanistic methodical 10x page plan`) — mapeie `sections_plan[]`/as seções da página contra os 4 perfis de decisor (spontaneous, competitive, humanistic, methodical); perfil inteiro sem NENHUMA seção que o sirva (ex.: zero specs/FAQ pro methodical) → `severity: medium`.
  - **16 Táticas de Redução de Bounce** (rode `reduzir bounce rate auditoria mobile repensar hero mover proof bar reduzir CTAs para um`) — o MENU DE FIX dos findings deste check, na ordem de diagnóstico list → offer → copy; na re-validação pós-iteração (quando `11-ad-analysis/dados.json` existe e aponta clique sem conversão), vira a fila de correção da página.

**M6. Design tokens vs design system**
- Paleta e tipografia de `07-page/design-tokens.json` (variação aprovada) devem bater com o documentado em `07-page/design-system.md`.
- Divergência (hex do accent diferente, font-family trocada) → `severity: medium`, `fix: regenerar o design system a partir dos tokens da variação aprovada (07a)`. Artefatos ausentes → `"skipped"`.

**M7. Placeholders não-resolvidos em template/copy deployada**
- Varrer os artefatos consumidor-final que já existem — `06-copy-engine/copy-engine.md` (copy final), `07-page/design/page.html` (design aprovado com a copy real inserida), o template JSON/sections populados pela 07b, e os emails da 13 Fase A (`13-retention-engine/[fluxo]/email-N.html`) — procurando tokens de placeholder que deveriam ter sido substituídos por conteúdo real: `{{ALGO_EM_CAPS}}` (ex: `{{BONUS_LINK}}`, `{{MECHANISM_NAME}}`), stand-ins entre colchetes (`[HEADLINE]`, `[PLACEHOLDER]`, `[TBD]`), números de mentira (`XX%`, `$XX`) e "lorem ipsum".
- **Exceções (não são finding):** tags Liquid legítimas de objeto (`{{ product.title }}`, `{{ shop.* }}`, `{% ... %}`) e merge tags de ESP (`{{ first_name }}` do Klaviyo) — o alvo são stand-ins de CONTEÚDO em caixa alta ou colchetes, não a sintaxe do template.
- Placeholder achado → `severity: medium` (caso clássico: `{{BONUS_LINK}}` num email ainda em draft aguardando o asset da 05 — fix: "colar o link do asset da 05 antes de ativar o flow"). **Escalar pra `severity: high` se o placeholder está numa superfície JÁ PUBLICADA** (PDP/landing no ar) — consumidor vendo `{{...}}` na página quebra a confiança na hora.

### ETAPA 3 — Output (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/09-consistency-audit/` antes de salvar.

Salvar TRÊS artefatos em `workspace/[produto]/09-consistency-audit/`:

1. **`09-consistency-audit/consistency-audit.md`** — fonte legível pela AI e pelo membro
2. **`09-consistency-audit/consistency-audit.html`** — visualização humana usando `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained). Logo SVG do Aura no topo copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto. Usar componentes:
   - `.danger` pra critical issues
   - `.callout` pra high
   - `.note` pra medium
   - `.pill` pra status tags (BLOCK/CAUTION/GO)
   - `.kpi-grid` pra counters (critical/high/medium)
3. **`09-consistency-audit/dados.json`** — machine-readable schema abaixo

**Priorização dos fixes (sistema nomeado):** antes de salvar, puxe **ICE Hypothesis Prioritization** (rode `hipotese if then because ICE score impacto confianca facilidade priorizar recomendacoes`) e aplique aos findings: cada `fix_suggested` escrito como hipótese se-então-porque ("SE alinharmos o nome do mecanismo no hero, ENTÃO o message match do funil fecha, PORQUE o consumidor vê o mesmo nome do ad à página"), e a fila de correção do report ordenada por severity primeiro e score ICE (impacto × confiança × facilidade) como desempate dentro da mesma severity — o membro ataca primeiro o fix de maior impacto que custa menos. A severity continua sendo o que decide o gate (ETAPA 4); o ICE só ordena o trabalho.

Atualizar o manifest e regenerar o painel:

- Atualizar `workspace/[produto]/manifest.json` adicionando `"09-consistency-audit"` em `skills_completed`.
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html, onde `<slug>` é o `product_slug`).

Schema do JSON:

```json
{
  "audit_id": "uuid",
  "audited_at": "ISO",
  "artefacts_loaded": ["01-product-research", "..."],
  "artefacts_missing": [],
  "checks_run": 20,
  "issues_critical": 2,
  "issues_high": 3,
  "issues_medium": 4,
  "launch_recommendation": "BLOCK|CAUTION|GO",
  "findings": [
    {
      "check_id": "C2",
      "severity": "critical",
      "status": "fail",
      "artifact": "06-copy-engine/copy-engine.md hero section",
      "issue": "Claim 'visibly firmer skin in 14 days' não tem evidence em 04-offer-builder/research-foundation.json",
      "fix_suggested": "Adicionar study com N=X amostra OR reescrever como 'designed to help with firmness'",
      "auto_fixable": false
    }
  ]
}
```

> O array de problemas chama-se `findings[]` — é o nome que o gate de deploy lê. Cada finding tem `status` ∈ `pass|fail|skipped`; checks não-rodáveis por artefato ausente entram como `"skipped"`, nunca `"pass"`. `artefacts_missing[]` lista os inputs esperados que não existiam.

Markdown com o mesmo conteúdo em formato humano (componentes `.danger` pra critical, `.callout` pra high, `.note` pra medium).

### ETAPA 4 — Decisão

- `issues_critical > 0` → `launch_recommendation: "BLOCK"` (mostrar ao membro como **BLOQUEAR**) → mensagem pro membro: "BLOQUEADO. [N] issues críticas. Corrige antes de lançar."
- `issues_high > 0 E critical == 0` → `CAUTION` (mostrar ao membro como **CUIDADO**) → "CUIDADO. Dá pra lançar, mas [N] issues high — fix recomendado."
- `artefacts_missing` inclui `06-copy-engine` E `08-creative-engine` (input parcial) → força no mínimo `CAUTION`, nunca `GO`, mesmo sem critical/high — não dá pra atestar coerência de copy/ad que ainda não existe.
- Tudo limpo E nenhum artefato essencial faltando → `GO` (mostrar ao membro como **PODE LANÇAR**) → "PODE LANÇAR. Auditoria passou. Próximo passo: diga **'ad strategy'** pra montar a campanha."

## Mensagem Final

"Auditoria completa. Recomendação de lançamento: [BLOQUEAR/CUIDADO/PODE LANÇAR].

- Critical: [N]
- High: [N]
- Medium: [N]

Report salvo em `workspace/[produto]/09-consistency-audit/consistency-audit.html`. Abre no browser pra revisar cada issue com fix sugerido.

[Se BLOQUEAR/CUIDADO:] Depois de corrigir, rode `consistency-audit` de novo pra re-validar.
[Se PODE LANÇAR:] **GO → próximo passo: diga 'ad strategy'** (Skill 10) pra montar a campanha de teste."

---
name: content-recycler
description: Pega 1 criativo classificado como BREAKTHROUGH pela skill 11 (cânone `.claude/lib/ad-taxonomy/README.md` §2 — KPI do ad melhor que o KPI da campanha E puxando spend) e roda duas trilhas. Trilha 1, default e primeira: amplificação do que já provou escalar — iteração pelos 4 elementos (ângulo, mecanismo, autoridade, avatar), port do ângulo pra outros formatos, brief de LP/prelander dedicada, pacote de adaptação pra Axon/AppLovin e TikTok, duplicação em ad set ABO próprio e creator report. Trilha 2, sob pedido: as 9 derivadas de canal (advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube pre-roll, SMS, package insert, podcast ad) como jogada de marca e de LTV, nunca de performance. NUNCA dispara com KPI winner — o cânone o trata como loser para decisão. Use quando o membro disser "recycle [id]", "reaproveitar winner", "content recycler", "tirar mais dos ads". Zero infra externa, só Claude + Python.
---

# Content Recycler (Skill 14)

Skill auxiliar invocável. Pega um criativo que **já provou escalar** e tira dele tudo que ele ainda pode dar — primeiro dentro do tráfego pago (Trilha 1), depois nos canais próprios (Trilha 2).

> **O gatilho é `breakthrough`, não "winner".** As 4 classes de resultado são definidas no cânone `.claude/lib/ad-taxonomy/README.md` §2 e medidas pela skill 11 — esta skill LÊ a classificação e nunca a recomputa. Só `breakthrough` (KPI do AD melhor que o KPI da CAMPANHA **e** puxando spend) libera reciclagem. `KPI winner` bate o KPI mas não puxa spend, e o cânone o trata como **loser para decisão**: reciclar um KPI winner é multiplicar um criativo que nunca provou nada em escala — o KPI bonito veio de amostra pequena.

> **Duas trilhas, nesta ordem.** **Trilha 1 — Amplificação** roda primeiro, sempre: é o que se faz de verdade com um ad que venceu (iterar, portar, dar página própria, levar pra outro canal, dar budget dedicado, devolver pro pipeline criativo). **Trilha 2 — Derivadas de formato** são as 9 peças de canal próprio; continuam disponíveis, mas como jogada de **marca e de LTV**, não de performance. Quem escala a conta é a Trilha 1.

> **Fonte primária da Trilha 2 é a lib, não a base.** A estrutura "1 criativo → 9 formatos" (specs, length, tom, compliance de cada derivada) vem INTEIRA de `.claude/lib/content-recycler/` (`recycler.md` = engine do fluxo, `formats.json` = specs dos 9 formatos) — não existe framework "9 derivadas" na base de conhecimento, então NUNCA busque isso lá. A Trilha 1 não vem da lib: ela vem do cânone `.claude/lib/ad-taxonomy/README.md` (§2 classes, §5 escala, §7 Sniper) mais os movimentos descritos aqui. A base entra só pros **frameworks de copy NOMEADOS**: os domínios desta skill no índice `.claude/lib/kb-index/` (`frameworks.json` + `README.md`, mapa skill→domínio) são **creatives-hooks-formats** (102 sistemas, principal) e **page-landing-cro** (87 sistemas — relevante pra LP/prelander da Trilha 1 e pras derivadas advertorial e blog SEO). Quando uma etapa pede "consultar a base", NUNCA use query genérica — puxe os SISTEMAS NOMEADOS rodando `search_knowledge` com a `best_query` de cada framework relevante pra aquela etapa (`deep=true`).

## Quando usar

**Manual**: membro diz `recycle [creative-id]`, `recycle breakthrough` ou `recycle winner` (as três entradas caem na mesma detecção abaixo).

**Automático** (futuro): disparada automaticamente quando a skill 11 classifica um criativo como `breakthrough`. Hoje o trigger é sempre manual.

## Pré-flight

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (README.md/.html, `essence.json` descritivo, `amplification-plan.md`, `creator-report.md`) e toda conversa com o membro usam esse idioma. **As 9 derivadas consumidor-final (advertorial, email, TikTok, blog, Pinterest, YouTube, SMS, package insert, podcast), o `framework_template`, os hooks/scripts citados nos briefs da Trilha 1, a copy de end card e a VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

- [ ] `manifest.json` existe
- [ ] Pelo menos 1 criativo em `workspace/[produto]/08-creative-engine/` OU membro forneceu fonte alternativa
- [ ] `.claude/lib/ad-taxonomy/README.md` existe (cânone das 4 classes — o gatilho e a régua de ABO saem daqui)
- [ ] `.claude/lib/content-recycler/recycler.md` existe (engine da Trilha 2)
- [ ] `.claude/lib/content-recycler/formats.json` existe (specs dos 9 formatos)
- [ ] `.claude/lib/compliance-preflight/` existe (pra rodar check em cada derivada)

**Detecção de breakthrough (quando o input não traz ID específico):**

1. Ler `workspace/[produto]/11-ad-analysis/dados.json` (produzido pela Skill 11).
2. Selecionar os criativos que a skill 11 classificou como **`breakthrough`** no campo canônico **`ad_class`** (enum do cânone §2: `breakthrough` | `spend_winner` | `kpi_winner` | `loser`). Fonte, nesta ordem:
   - **Primária:** o array **`breakthroughs[]`** do `dados.json` (contém apenas `ad_class == "breakthrough"`). `manifest.breakthroughs[]` espelha o mesmo conteúdo como estado consolidado, e `manifest.ad_classification[]` (também gravado pela 11) traz a classe de CADA criativo — é nele que se confere a classe de um id específico quando o `dados.json` da rodada não estiver à mão.
   - **Fallback legado**, só se nenhum dos três existir (análise antiga): `winners[]`, aceitando os DOIS shapes — **ids string** (o alias moderno: conteúdo idêntico a `breakthroughs[]`) ou **objetos com métricas** (produto antigo; extrair o id de `creative_id`/`id`). No shape objeto, use `ad_class == "breakthrough"` se o campo existir; sem ele, o rótulo positivo das análises velhas era `outcome == "winner"` — e esse rótulo NÃO distingue breakthrough de `kpi_winner`. Nesse caso, avise o membro de que a classificação canônica não existe e recomende re-rodar a Skill 11 antes de reciclar. **`winners[]` está DEPRECADO**: nunca fonte nova. Nunca reciclar um criativo só por ele aparecer num array chamado `winners[]`.
   - Os outros dois arrays da 11 (`spend_winners[]` e `kpi_winners[]`) **não** são fonte de reciclagem — entram só nas regras 3 e 4 abaixo.

   A 14 **NÃO recomputa critério** (classificar é responsabilidade exclusiva da 11); apenas ordena por `spend_total` desc (tiebreak `days_active` desc). Se precisar de target pra exibir, leia explícito de `manifest.target_cpa`.
3. **`kpi_winner` nunca entra** — nem quando aparece em `kpi_winners[]`, nem quando o membro pede pelo id. O cânone §2 o trata como loser para decisão. Se o membro insistir, explique em uma linha (bateu o KPI com pouco spend, não provou escala) e ofereça o caminho certo: iterar via Skill 08.
4. **`spend_winner` entra só pela porta estreita** (o array `spend_winners[]` da 11). O cânone §2 manda **iterar, não escalar**: ele libera exclusivamente o **Movimento 1** da Trilha 1 (iteração pelos 4 elementos). Sem LP dedicada, sem port de canal, sem duplicação em ABO, sem Trilha 2. Diga isso ao membro antes de começar.
5. Se houver 1 breakthrough → usar ele. Se houver ≥2 → apresentar a lista ordenada (id + cpa + roas + spend) e perguntar qual amplificar primeiro.
6. Se `breakthroughs[]` vier vazio (nenhum criativo com `ad_class == "breakthrough"`) → a resposta honesta não é "aguardar mais dados". Diga quantos criativos caíram em cada classe e responda:
   > "Você ainda não tem um ad que escala: nenhum criativo foi classificado como breakthrough (KPI do ad melhor que o da campanha **e** puxando spend). [Se houver KPI winners: X criativos bateram o KPI sem puxar spend — e ad que não puxa spend não provou nada em escala, então multiplicá-lo só multiplica um teste pequeno.]
   >
   > O próximo passo é a Skill 08 (mais criativo), não a 14. Opções:
   > 1. Rodar `creatives` pra gerar o próximo batch
   > 2. Rodar `run analysis` de novo, se a campanha andou desde a última leitura
   > 3. Se existe `spend_winner`, rodar só a iteração pelos 4 elementos: `recycle [creative-id]`"
7. Se `dados.json` não existir (skill 11 nunca rodou) → oferecer 2 caminhos (não abortar seco):
   > "Skill 11 não foi rodada ainda, então não tenho a classificação dos criativos. Opções:
   > (A) Rodar `run analysis` agora pra classificar, OU
   > (B) trabalhar um criativo específico direto: `recycle [creative-id]`."

Quando o membro passa `[creative-id]` direto, cheque a classe desse id (`ad_class` no `dados.json` da 11, ou `manifest.ad_classification[]`) antes de rodar: `breakthrough` → tudo liberado; `spend_winner` → só o Movimento 1; `kpi_winner` ou `loser` → recusa com a explicação do item 3. Se o id não estiver em nenhuma análise (criativo nunca rodado), avise que não há classificação e que o plano sai sem lastro de performance — o membro decide se segue.

## Fluxo

As ETAPAS 0 e 1 são comuns às duas trilhas. Depois delas, a **Trilha 1 roda primeiro, sempre**; a Trilha 2 só quando o membro pedir.

### ETAPA 0 — Identificação do breakthrough

Input `[creative-id]` ou `breakthrough`/`winner` (detecção do pré-flight). Registre o **`ad_class` lido** (`breakthrough` ou `spend_winner`) — é ele que define quais movimentos ficam liberados no resto da execução. Se o input é um `[creative-id]` de conceito (formato `c-NN`), abra primeiro `workspace/[produto]/08-creative-engine/dados.json` pros campos estruturados e use `concept-NN.md` como brief complementar (ETAPA 1 do `recycler.md`).

> **Onde a lib diverge, esta skill vence.** A ETAPA 1 do `recycler.md` ainda fala em `winner` / `outcome == "winner"`. Aquele texto é a engine dos 9 formatos, não a fonte do gatilho — o gatilho é o `breakthrough` do cânone §2, definido aqui. Nunca reciclar um criativo por ele aparecer num array chamado `winners[]`.

### ETAPA 1 — Extração da essência E do framework

Destile big idea, hook, mecanismo, avatar e voz em `essence.json` seguindo a ETAPA 2 do `.claude/lib/content-recycler/recycler.md` (fontes rastreáveis: `mechanism_name` LITERAL de `04-offer-builder`, `voc_refs[]` herdadas de `08-creative-engine`/`02-market-research`, sanity check de drift que PARA e surface ao membro).

**Só a essência não basta — o que viaja é o FRAMEWORK.** O script do criativo não viaja: ele é feito daquele produto, daquele avatar e daquele mecanismo. O padrão por trás do script viaja pra qualquer avatar, canal e mecanismo. Dois exemplos do que é script e do que é framework:

- Script: `"I think I just got scammed"` (tradução livre: "acho que acabei de ser passado pra trás"). Framework: `"I think [negative thing] just happened (to me)"`.
- Script: `"I ordered X but they sent me [muito mais]"`. Framework: `"I thought I was getting X, I got Y instead"`.

Hook específico gasta com uso em massa; framework não gasta. Por isso o `essence.json` ganha dois campos além do schema da lib:

```json
{
  "framework_template": "<o padrão do hook/script com o slot vazio — ex: 'I think [negative thing] just happened (to me)'. Sempre em inglês US, do mesmo jeito que roda no ad>",
  "psychological_mechanism": "<POR QUE o padrão funciona, em 1 frase: o efeito na cabeça do avatar, não a descrição do hook. Ex: 'tira do avatar o peso da culpa e do fracasso'>"
}
```

- **Como extrair (subir um nível):** pegue a frase literal do breakthrough, remova o que é específico daquele produto/avatar e deixe o slot. Se o que sobrou não faz sentido para outro avatar, você tirou específico de menos.
- **Como usar:** quem não é bom de copy piora o hook ao reescrever. Toda aplicação nova do framework sai em 3 versões — **1 controle** (o hook 1:1 do original) + **2 reescritas** com palavras próprias — e o teste decide qual fica.
- **Para que serve o `psychological_mechanism`:** é o juiz de toda iteração da Trilha 1. O aprendizado a extrair de um breakthrough nunca é "o hook é bom", é o mecanismo psicológico que ele aciona. Iteração que muda o texto e muda junto o que é COMUNICADO não é iteração, é conceito novo mal rotulado.

Puxe os SISTEMAS NOMEADOS abaixo pra sustentar a destilação (rode `search_knowledge` com a `best_query`, `deep=true`):
   - **Hook Writing Framework — 3 Functions of a Hook** (rode `hook framework 3 functions ad video stop scroll create curiosity`) — pra identificar qual das 3 funções o hook cumpre antes de reembalar.
   - **Ad Definitions — Concept / Angle / Variation / Format** (rode `ad definitions concept angle variation format 3-2-2 testing structure`) — separa o que é CONCEITO/ÂNGULO reaproveitável (viaja entre canais) do que é só FORMATO descartável.
   - **Storytelling as the Hardest-to-Replicate Angle** (rode `storytelling hardest to replicate angle founder story defensible creative`) — se a essência for narrativa de fundador/origem, ela é o ativo mais defensável; preserve-a intacta nas duas trilhas.
   - **Show Don't Tell** (rode `show don't tell behavioral change when telling aren't selling spoken language video`) — destila a demonstração central do criativo pra carregá-la pros formatos visuais.

---

## Trilha 1 — Amplificação (default, roda primeiro)

Breakthrough é caro e raro: pelo cânone §2, a expectativa de hit rate de super winner é de **1-3% dos criativos testados**, e um super winner absorve 30-40% do spend. O primeiro trabalho com um deles não é espalhá-lo por canais orgânicos — é extrair dele mais spend lucrativo. São 6 movimentos, e eles saem num **plano único** (`amplification-plan.md`, uma seção por movimento). Esta skill **especifica**; quem executa é a Skill 08 (criativo), a 07a/06 (página e copy) e a 12 (escala).

**Movimento 1 — Iterar pelos 4 elementos.**
Diagnostique o criativo por: **(1) ângulo**, **(2) mecanismo**, **(3) autoridade**, **(4) avatar**. O elemento que estiver faltando ou fraco é a PRIMEIRA iteração (UGC sem autoridade → plugar autoridade; mecanismo confuso → deixá-lo óbvio). Depois, nesta ordem: variações de valence/intensity (a carga da emoção — positiva ou negativa — cruzada com o quanto ela é intensa) → outros formatos → outras formas de dizer a mesma coisa → começar *in media res* (a peça abre já dentro da ação) → testar um nível de awareness acima e um abaixo do atual. Ângulo aqui é a **razão de compra em frase** ("para de virar de um lado pro outro a noite toda"), não a embalagem — a distinção é do cânone §7, e é lá também que está a régua: **toda iteração é Sniper** (1 ângulo, 3 execuções). Saída: lista de iterações priorizadas, cada uma com o elemento que ataca e o que precisa permanecer constante. Handoff pra Skill 08.

**Movimento 2 — Portar o ângulo pra outros formatos.**
O formato às vezes comunica melhor a mesma mensagem — static que venceu vira vídeo com voiceover, e o contrário também. A regra dura: varie a superfície (formato, palavras) mantendo constante **o que é comunicado**; o `psychological_mechanism` do `essence.json` é o juiz. O erro clássico é trocar o texto, trocar junto a mensagem e depois ler o resultado como se fosse teste de formato. Saída: 2-3 ports com o mesmo `framework_template`, cada um acompanhado da frase do que precisa continuar sendo comunicado. Handoff pra Skill 08.

**Movimento 3 — Construir LP/prelander dedicada.**
Um breakthrough basta pra justificar página própria (prelander é a página que o ad abre antes da página do produto). Congruência é **decisão de destino**, não checagem no fim: ad de open loop ("clique pra saber mais") não pode cair em product page. O tipo de página segue o awareness do ad — problem-aware pede advertorial ou pré-venda educacional; product/solution-aware pede listicle (a página em formato de lista, "5 razões por que..."), porque educar de novo entedia. Julgue a página pela melhora de **KPI**, nunca por spend (página pega spend fácil quando o ad é bom, e isso não prova nada). Ressalva de sequência: pra conceito net-new ainda não validado, não gaste tempo construindo LP — espere direção. Operacional no Meta: ad set novo no mesmo CBO com o breakthrough duplicado apontando pra nova LP; pros ads novos do ângulo, controle vs nova LP. Saída: seção de brief com tipo de página, ângulo, mecanismo, autoridade, prova e o que a página precisa completar que o ad deixou em aberto. Handoff pra Skill 07a-page-design (e 06 pra copy).

**Movimento 4 — Portar pra Axon/AppLovin e TikTok.**
Criativo validado no Meta viaja entre plataformas; o que muda é formato e mecânica nativa. No Axon/AppLovin são só duas adaptações técnicas: vídeo em **9:16** (safe zones não importam) e **end card** criado à parte no Ads Manager do Axon (estático com elementos animados — CTA/oferta — exibido no fim do vídeo; usar os melhores statics como base, e pedir ajuda ao account manager do Axon). Régua de canal novo: **US$ 250-1.000/dia por 60-90 dias** — quanto maior o CPA, mais spend pra crackear o canal; a maioria desiste em 1-2 semanas e não descobre nada. Prioridade pós-Meta: AppLovin ≈ TikTok empatados. Saída: seção com a lista de assets a re-exportar em 9:16, o brief do end card e a régua de budget/janela.

**Movimento 5 — Duplicar em ad set ABO próprio.**
Criativo novo que começa a puxar spend rouba o spend do que já estava rodando dentro do CBO. A resposta é do cânone §5: cada breakthrough ganha **1 ad set próprio em campanha ABO, começando a ~10% do budget diário da campanha principal**, mantendo o ad original rodando no CBO. Isto **não é executado aqui** — a dona da execução de escala é a **Skill 12**. A 14 registra o item no plano já com o valor calculado sobre o budget diário da campanha principal (`manifest.budget_daily`) e aponta pra 12; se a 12 já promoveu este criativo, o plano só referencia o que já existe.

**Movimento 6 — Devolver como creator report.**
O breakthrough volta pro pipeline de conteúdo como briefing: report dos ads que mais gastaram nos últimos 30 dias, mais o comentário do que está rodando, que linguagem está funcionando, que promoções vêm aí e que vídeos valem reação. É assim que o creator sai com ideias prontas sem que ninguém escreva script. Saída: `creator-report.md` compartilhável (se o membro grava um Loom em cima, melhor). Sem creators contratados, o mesmo doc serve de brief pro editor.

**Fechamento da Trilha 1**: apresente o plano ao membro como draft e ofereça a Trilha 2 como próximo passo opcional — nunca rode as 9 derivadas sem ele pedir.

---

## Trilha 2 — Derivadas de formato (9 canais, sob pedido)

As 9 derivadas continuam inteiras e continuam valendo — mas com o enquadramento honesto: são jogada de **marca, canal próprio e LTV**. Elas não escalam a conta; quem escala é a Trilha 1. Rode quando o membro pedir explicitamente (ou quando ele aceitar a oferta no fecho da Trilha 1). Um criativo `spend_winner` não entra aqui.

Siga o fluxo do `.claude/lib/content-recycler/recycler.md` a partir da ETAPA 3 — a essência já foi extraída na ETAPA 1 acima:

3. **Consultar base Aura por formato** — para CADA uma das 9 derivadas, puxe os SISTEMAS NOMEADOS do domínio (não query genérica; `deep=true`). Curadoria de maior impacto por formato:
   - **Advertorial / Blog SEO** → **Caples' Four U's Hierarchy** (rode `Caples four U's hierarchy unique useful urgent ultra-specific headlines`) + **Hopkins' Specificity Rule** (rode `Hopkins specificity rule 1-2 second rule vague vs specific claims`) + **Objection → Claim → Proof → Benefit cycle (the Hold)** (rode `objection claim proof benefit cycle hold section one cycle`) — headlines específicas e ciclos de prova pra long-form.
   - **Organic TikTok / YouTube pre-roll** → **Gap Theory of Curiosity** (rode `gap theory of curiosity hooks counterintuitive open loop slippery slope`) + **Slippery Slope Principle** (rode `slippery slope principle open loops pattern interrupt end with intrigue video script`) + **4-Section Video Ad Structure (Hook / Bridge / Hold / CTA)** (rode `video ad script 4 section structure hook bridge hold CTA timing 30-45 seconds`) + **Strategic Pacing** (rode `strategic pacing rapid cuts hook bridge solution CTA video editing rhythm`) — reembala o breakthrough em estrutura de vídeo orgânico com ritmo de corte por seção.
   - **Pinterest carousel / package insert (estáticos)** → **Static/Image Archetypes by Funnel Position** (rode `static image archetypes funnel position plain reminder direct response complexity rule`) + **13+ Winning Static Ad Templates** (rode `13 winning static ad templates avatar callout nutella meme breakdown why it works`) — escolhe arquétipo estático certo pra cada slide.
   - **Email sequence / SMS / Podcast ad** → **The Big 4 Emotions** (rode `Big 4 Emotions NEW ONLY EASY ANYBODY SAFE PREDICTABLE BIG FAST`) + **Brunson's Five Curiosity Hooks** (rode `Brunson five curiosity hooks controversial bold prediction conspiracy reframe angles`) — reframes de curiosidade pra subject lines / aberturas de SMS / leitura de podcast quando o ângulo do breakthrough já saturou no feed.
   - **Transversal a TODAS as 9** → **Congruency — The Multiplier** (rode `congruency multiplier ad landing page offer visual message emotional continuity`) — cada derivada mantém continuidade de mensagem/promessa com o criativo fonte e com `04-offer-builder/dados.json` (sem deriva de mecanismo). O `psychological_mechanism` do `essence.json` é o teste: se a derivada não aciona o mesmo mecanismo, ela virou outro conceito.
   - Demais frameworks do domínio (Hormozi Callout System, What-Who-When Matrix, SUCCESs, New Opportunity vs Improvement, etc.) ficam disponíveis em `.claude/lib/kb-index/` pra puxar sob demanda quando o formato pedir.

4. **Gerar 9 derivadas** em paralelo (advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube preroll, SMS, package insert, podcast ad)
5. **Compliance Pre-flight em cada** — protocolo por severity (o mesmo da ETAPA 4 do `recycler.md`): `critical` → PARAR essa derivada, mostrar triggers + rewrite ao membro e aguardar aprovação (nunca auto-reescrever claim critical silenciosamente); `high` → auto-rewrite + log + re-rodar o check; `medium` → salvar original + logar warning; `low` → salvar silencioso
6. **Gerar README.md + compliance-log.json** consolidados

## Email-sequence: não colidir com os flows da Skill 13

A derivada `email` que esta skill gera é uma **variação A/B de nutrição derivada do breakthrough** — uma sequência de e-mails que reaproveita o ângulo/hook do criativo pra testar outra mensagem de nutrição. Ela **NÃO é um flow de lifecycle** e **NÃO substitui nem sobrescreve** o welcome / post-purchase / abandoned-cart da **Skill 13** (que é a fonte única de verdade dos flows de retenção).

Ela também **não valida nada**: e-mail fala com quem já é cliente ou já é lista, então o resultado dele não diz se o ângulo funciona em tráfego frio. Validação de ângulo e de oferta acontece na Trilha 1, no tráfego pago.

Regras pra não colidir:
- **Nunca** instruir o membro a importar essa sequência "como welcome flow" no Klaviyo — isso desligaria/duplicaria o welcome da 13.
- Posicionar como **flow separado / teste paralelo** (ex: segmento de teste, ou campanha one-off), que roda **ao lado** dos flows da 13, não no lugar deles.
- Se o membro ainda não rodou a Skill 13, recomendar rodar a 13 primeiro (welcome/post-purchase são baseline de retenção) e usar esta derivada só como variação de teste depois.

## Output

Pasta `workspace/[produto]/14-content-recycler/[source-id]/`.

**Sempre (comum às duas trilhas):**
- `essence.json` — essência + `framework_template` + `psychological_mechanism` (reusável)
- `README.md` + `README.html` — índice do que foi produzido + instruções de distribuição (rule 6b do CLAUDE.md)

**Trilha 1 (sempre que a skill roda):**
- `amplification-plan.md` + `amplification-plan.html` — o plano com uma seção por movimento (iterações pelos 4 elementos, ports de formato, brief de LP/prelander, pacote de canal Axon/TikTok, item de ABO pra Skill 12)
- `creator-report.md` + `creator-report.html` — o report compartilhável com creators/editor

**Trilha 2 (só quando rodada):**
- 9 arquivos `.md`, um por formato (advertorial, email, TikTok, blog, Pinterest, YouTube preroll, SMS, package insert, podcast)
- 9 arquivos `.html` correspondentes — um pra cada `.md` (rule 6b: dual output obrigatório)
- `compliance-log.json` — log consolidado das derivadas

Além das pastas por source-id, escreva também no topo de `workspace/[produto]/14-content-recycler/` um índice `content-recycler.md` + `content-recycler.html` que lista todas as fontes trabalhadas (cada `[source-id]` com a classe lida, o plano de amplificação e — quando existirem — os 9 formatos, com link pra pasta). Esse índice é o relatório humano que o painel do produto exibe.

## SALVAR (dual output — rule 6b do CLAUDE.md)

Todo relatório salvo em `workspace/[produto]/14-content-recycler/[source-id]/` — o plano de amplificação, o creator report e cada derivada da Trilha 2 — DEVE ter `.md` (fonte pra AI) + `.html` companion (visualização humana). Use `.claude/templates/aura-report-template.html` como base — copie o CSS inline e a logo SVG do `.claude/templates/aura-logo-snippet.html` LITERALMENTE no topo do `<body>`. NUNCA gere HTML sem a logo SVG nem com texto "AURA"/"Aura Engine" no lugar dela.

Depois de salvar todos os outputs:
- Atualizar `manifest.json`: adicionar `"14-content-recycler"` em `skills_completed` (se ainda não estiver) + `updated_at`.
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza ABRIR-AQUI.html).

## Sucesso

**Gatilho (bloqueia tudo):**
- [ ] O criativo fonte está classificado como `breakthrough` pela skill 11 — ou como `spend_winner`, e nesse caso só o Movimento 1 rodou
- [ ] Nenhum `kpi_winner` foi reciclado

**Trilha 1:**
- [ ] `essence.json` salvo com `framework_template` e `psychological_mechanism` preenchidos (nenhum dos dois vazio ou parafraseando o script)
- [ ] `amplification-plan.md` + `.html` com os 6 movimentos endereçados (os que a classe libera; os bloqueados aparecem com o motivo)
- [ ] Cada movimento tem handoff explícito (08 / 07a / 12) — nenhum movimento fica sem dono
- [ ] `creator-report.md` + `.html` gerados

**Trilha 2 (se rodada):**
- [ ] 9 arquivos `.md` gerados
- [ ] 9 arquivos `.html` companion gerados (rule 6b)
- [ ] Cada um passa compliance check (severity ≤ medium)
- [ ] README.md + README.html com índice pronto

## Customização (Trilha 2)

Pra adicionar novo formato (ex: LinkedIn post, Substack newsletter, Twitter thread), editar `.claude/lib/content-recycler/formats.json` adicionando entry com:
- `id`, `name`, `output_file`
- `length_words_total` range (+ opcional `length_words_per_email`/`length_words_per_pin` quando o formato tem unidades, seguindo as entries existentes)
- `structure` template
- `tone`
- `compliance_notes`

Próxima rodada da skill gera automaticamente também esse formato.

## Mensagem final ao membro

**Depois da Trilha 1 (sempre):**

```
✓ Plano de amplificação pronto pra [source-id] ([classe lida])
  workspace/[produto]/14-content-recycler/[source-id]/amplification-plan.md

  Diagnóstico dos 4 elementos:
  → Ângulo: [o ângulo em frase] · Mecanismo: [nome canônico]
  → Autoridade: [presente/ausente] · Avatar: [avatar]
  → Elemento mais fraco (primeira iteração): [elemento]

  Framework que viaja: [framework_template]
  Por que funciona: [psychological_mechanism]

  Próximos passos, por dono:
  → Skill 08: [N] iterações Sniper + [N] ports de formato
  → Skill 07a: LP/prelander [tipo de página] pro ângulo
  → Skill 12: duplicar em ad set ABO próprio a ~10% do budget da campanha
  → Canal novo: [N] assets em 9:16 + end card (Axon/AppLovin, TikTok)
  → Creators/editor: creator-report.md

  Opcional: quer que eu gere também as 9 derivadas de canal próprio
  (advertorial, email, TikTok orgânico, blog, Pinterest, YouTube, SMS,
  package insert, podcast)? É jogada de marca e LTV, não de escala.
```

**Depois da Trilha 2 (só se rodada):**

```
✓ 9 formatos gerados em workspace/[produto]/14-content-recycler/[source-id]/

  Compliance: [X críticos, Y high, Z medium, W low]
  Rewrites aplicados: [N]

  Distribuição sugerida:
  → Advertorial: publicar como LP secundária pra cold traffic
  → Email sequence: variação A/B de nutrição (NÃO sobrescrever o welcome da Skill 13 — rodar como flow/teste separado)
  → TikTok orgânico: post na conta da marca
  → Blog: publicar pra SEO, registrar no Search Console
  → Pinterest: criar board, pin semanal
  → YouTube pre-roll: campaign separada
  → SMS: wire no Postscript como opt-in trigger
  → Package insert: enviar pro fornecedor imprimir
  → Podcast: outreach pra shows do nicho

  Abra o README.md da pasta pra ver índice completo.
```

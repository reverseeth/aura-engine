---
name: offer-builder
description: Engine de construção de oferta com mecanismo único, stack de valor, bundles, bumps, upsells, garantia, e unit economics completa. A ideação de mecanismo roda em 2 rotas (default = recombinação validada a partir da validated_library da Skill 03) e todo componente de AOV passa pelo Gate de Complementaridade. Use quando o membro disser "offer", "oferta", "montar oferta", "construir oferta", "pricing", "bundle", ou quando o market research e competitor analysis estiverem prontos e o membro quiser estruturar a oferta antes de escrever a copy. A oferta é o MOTOR ECONÔMICO do negócio — decisões aqui determinam se ads são viáveis em escala.
---

# Offer Builder Engine

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` + `README.md`; o mapa skill→domínio está no README). Os domínios desta skill são `offer-mechanism`, `offer-pricing-guarantee` e `brand-building-bonus-aov` (mais as entradas de `finance-projections` marcadas pra 04, lidas nas ETAPAs de economics). **O tamanho de cada domínio é o que o `frameworks.json` disser hoje — nunca um número decorado neste texto.** Sempre que uma ETAPA mandar "puxar os sistemas da base", rode `search_knowledge` com a `best_query` NOMEADA de cada framework relevante — **NUNCA query genérica**. As queries embutidas nas ETAPAs abaixo são o núcleo mínimo garantido de cada etapa, nunca o teto; a cobertura completa segue o contrato do item 5 do "Antes de Começar".

> **Cânone de economia unitária: `.claude/lib/unit-economics/README.md`.** É a fonte de verdade única de margem de contribuição, CAC, ROAS e decisão de spend — as skills 04, 11, 12 e 15 leem de lá e **nenhuma redefine esses conceitos localmente**. Esta skill APLICA o cânone; quando um número ou uma definição desta skill divergir do cânone, o cânone vence. Os pontos que mais importam aqui: §1 (margem de contribuição ≠ lucro; stack completo de custos variáveis), §2 (primeiro pedido ≠ recompra), §3 (CAC ≠ CPA; piso de CAC) e §4 (por que ROAS isolado inverte a decisão).

### Pré-flight (OBRIGATÓRIO)
Valide antes de prosseguir:
- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `02-market-research/dados.json` existe (awareness_distribution, sophistication_stage) E `02-market-research/market-research.md` existe (narrativa: pain points, desires, objeções; se não existir, procure o legado `relatorio.md` — mesmo fallback vale pras outras fases)
- [ ] `03-competitor-analysis/competitor-analysis.md` E `03-competitor-analysis/dados.json` existem
- [ ] Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language. Nesta skill, copy pública é só `offer_stack`, a `copy` do bump e a promise da garantia — a LÓGICA do mecanismo (ump/ums) é documentação interna e vai no report_language; quem escreve a copy do mecanismo é a Skill 06. Todo output interno segue também a **linguagem simples da regra 0 do CLAUDE.md**: sigla explicada na primeira vez, número estatístico em palavras, e o teste "alguém de fora do setor entende cada frase de primeira?".

Se faltar qualquer arquivo de fase anterior (02/03), em vez de abortar seco, ofereça ao membro 2 caminhos (escape-path ES1):
- **(A)** Rodar a skill faltante agora pra gerar o arquivo real, OU
- **(B)** Prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` e avisando no output final que recomenda re-executar esta skill quando o arquivo real existir.

Se `manifest.json` ou `profile.md` estiverem TOTALMENTE ausentes (membro nunca rodou setup), aí sim pare — mas ofereça rodar o setup (Skill 00) inline.

## Quando Usar
Quando o membro tem produto definido, market research pronto, e precisa construir a estrutura econômica completa: mecanismo único, preço, bundles, bumps, upsells, garantia, e unit economics viáveis pra escalar com ads pagos. Sem oferta estruturada, nenhum copy (por melhor que seja) vai converter sustentavelmente.

## Antes de Começar

1. Leia `workspace/profile.md` (ferramentas disponíveis, budget diário — informa viabilidade econômica; lê também `report_language` conforme o pré-flight)
2. Leia `workspace/[produto]/01-product-research/product-research.md` (se existir — tem features, COGS preliminar, potencial de oferta)
3. Leia `workspace/[produto]/02-market-research/market-research.md` (narrativa: pain points, desires, root cause, objeções) E `02-market-research/dados.json` (campos estruturados: awareness_distribution, sophistication_stage, voc_phrases) — a oferta é a RESPOSTA direta ao market research
4. Leia `workspace/[produto]/03-competitor-analysis/competitor-analysis.md` E `03-competitor-analysis/dados.json` (claims saturados a evitar, gaps de oferta, e os campos `validated_library`, `top_creatives` e `alternative_solutions` — matéria-prima da Rota A de mecanismo e do Gate de Complementaridade). Leia também `03-competitor-analysis/creative-patterns.json` SE existir (`recurring_claims` com `market_validated` — claims que o mercado já validou em ad)
4b. Leia `workspace/[produto]/brand.md` SE existir (posicionamento em 1 frase — vem da Etapa 7 da Skill 03 — mais o nome da marca e o vocabulário que ele gera). O mecanismo da ETAPA 2 tem que REFORÇAR esse posicionamento, não competir com ele: se o posicionamento é "a marca do despertar das 3h", um mecanismo sobre "energia diurna" está brigando com a própria marca. Na recomendação 2C isso vira gate qualitativo: candidato que contradiz o posicionamento do brand.md não pode ser recomendado sem o conflito aparecer — e se o conflito for real (o mecanismo mais forte apontar pra OUTRO posicionamento), não decida sozinho: apresente os dois lados ao membro (posicionamento atual vs o que o mecanismo sugere) e deixe ele escolher qual prevalece
4c. Leia `workspace/[produto]/15-finance-engine/dados.json` **SE existir** — a skill 15 é a dona do modelo financeiro completo (cânone §5) e fecha os buracos que esta skill hoje deixa em aberto. Quatro campos (os mesmos do `handoff.for_skill_04` da 15), cada um com o ponto exato onde entra:
   - **`monthly_model.fixed_costs_monthly`** → ETAPA 8: é o número que faz `result_after_fixed_monthly` deixar de nascer `null`. Existindo, **não pergunte de novo** — só confirme.
   - **`monthly_model.contribution_margin_pct`** → ETAPA 8: a margem de contribuição **medida** do negócio, contra a qual a projetada desta skill é conferida.
   - **`payback.payback_window_days_measured`** → ETAPA 9, check 8: com LTV medido, a janela de payback vira alternativa ao gate de margem mínima por pedido.
   - **`cash.runway_months`** → ETAPA 9, check 8: a segunda perna da alternativa por payback — o caixa precisa aguentar a janela (`runway_months × 30 ≥ payback_window_days_measured`). Sem ele (ou `null`), a alternativa por payback não fecha.

   **Fallback (o arquivo não existe, ou o campo veio `null`):** o comportamento é exatamente o de hoje — a ETAPA 8 pergunta os fixos ao membro e grava `null` se ele não souber, e o check 8 vale integralmente pela margem por pedido. A 15 nunca é pré-requisito desta skill; ela roda naturalmente **depois** da 04 (é a 04 que entrega o stack de custos variáveis pra ela), então na primeira rodada de oferta o arquivo simplesmente não existe.

5. **Contrato de cobertura da base (REGRA — `.claude/lib/kb-index/README.md`).** A puxada não é uma amostra, é cobertura do tópico:
   1. **Abra a seção inteira dos domínios, sempre.** No início de cada ETAPA que consulta a base, abra `frameworks.json` e **enumere TODAS as entradas de `offer-mechanism`, `offer-pricing-guarantee` e `brand-building-bonus-aov` cujo `use_in_skill` inclui a 04** (nas ETAPAs de economics, some as entradas de `finance-projections` marcadas pra 04). A contagem de cada domínio é a que o `frameworks.json` mostrar na hora — nunca um número decorado no texto da skill.
   2. **Rode a `best_query` exata de cada entrada relevante à etapa, com `deep=true`.** É a query curada que traz o sistema completo. As queries embutidas nas ETAPAs abaixo (mecanismo → ETAPA 2, oferta/assinatura/stack → ETAPA 3, garantia → ETAPA 4, economics/PSM → ETAPAs 5-7) são o **núcleo mínimo garantido daquela etapa, nunca o teto**: entrada relevante que não está embutida É PARA SER PUXADA do mesmo jeito.
   3. **Critério de relevância é por ETAPA, não por preguiça:** a pergunta é "esta entrada informa a decisão desta etapa?" — se a resposta for "talvez", puxa. Só se descarta o que claramente pertence a outra etapa desta skill (e será puxado lá).
   4. **Não repita busca de framework já puxado na mesma sessão:** entradas duplicadas entre domínios apontam pro MESMO conteúdo — reuse o resultado.
   5. **Check de encerramento de etapa:** antes de fechar cada ETAPA, releia a lista enumerada do passo 1 e confirme que nenhuma entrada relevante ficou sem puxar. Se ficou, puxe agora — é este check que garante o padrão "sem deixar passar nada importante da base".

   Pricing é decisão estratégica, não técnica — aprofunde em cada sistema até ter domínio completo. NUNCA fundamente uma decisão de oferta numa busca genérica do tipo "offer pricing" — sempre o sistema nomeado, pela `best_query`.

## Fluxo da Skill

### ETAPA 1 — Coletar Informações do Produto (3 Perguntas Apenas)

Antes de perguntar, extraia o máximo automaticamente da página do produto (dado salvo no profile pela Skill 00 ou puxando via web fetch agora se o link estiver no profile). Features, ingredientes, claims, preço atual de mercado — tudo que conseguir.

**Antes das perguntas, cheque `workspace/[produto]/sourcing/dados.json` (Skill 01b).** Se existir com `status: "closed"`, o COGS real já está lá (`landed_cost_per_unit`, `three_pl.pick_pack_per_order`, `logistics_route`) — use esses números direto, não pergunte custo ao membro e não marque `cogs_estimated`. Se existir com qualquer `status` diferente de `"closed"` (`quoting` ou `samples` — cotação/amostra ainda aberta), rode com estimativa conservadora + `cogs_estimated: true` e avise que os números refrescam quando a cotação fechar.

**Faça APENAS estas 3 perguntas, na ordem (pulando o que o sourcing já respondeu):**

**1. Custos (COGS breakdown — NÃO aceite agregado):**

O stack de custos variáveis é o do cânone §1 (`.claude/lib/unit-economics/README.md`) — **item a item, nunca agregado**. Pergunte separadamente:

1. Custo do produto **entregue** (fully loaded): produto na fábrica + embalagem + frete de entrada (inbound) + tarifa de importação, por unidade. Custo cru de matéria-prima subestima a linha inteira.
2. Frete médio por pedido até o cliente (informe região principal: Brasil interior? EUA West Coast?) — **incluindo a parcela de frete grátis que a loja absorve**
3. Pick & pack (fulfillment center): R$/$ por pedido
4. Processamento de pagamento: ~3% + taxa fixa (Stripe US: 2.9% + $0.30; Stripe BR: 3.99% + R$0.39; Shopify Payments fica na mesma faixa)
5. Taxas e impostos incidentes por pedido
6. **App de assinatura: 0,5–1% por transação** — só quando a oferta tem assinatura (Seal, Skio, Loop e similares). Parece pequeno e não é: 1% de US$ 1 milhão por mês é US$ 10 mil por mês, permanente. No breakdown, grave o valor por pedido (% × AOV).
7. **Fee de agência quando é cobrado como % do ad spend** — é custo variável, não despesa fixa: agência a 5% de um spend de US$ 1 milhão custa US$ 50 mil. No breakdown, grave o valor por pedido (% × custo de aquisição por pedido), usando o CAC de referência da categoria ou o CAC-alvo declarado pelo membro — uma passada só, sem recalcular em loop quando o teto de CAC mudar. Se a agência cobra valor fixo mensal, ela NÃO entra aqui — vai pros custos fixos da ETAPA 8.
8. **Provisão de reembolso e chargeback** — nunca zero. Entra **uma vez só**: ou como linha de custo aqui, ou como desconto no net AOV da ETAPA 6. Contar nos dois lugares subestima a margem duas vezes.

Os itens 6 e 7 são exatamente os que somem das planilhas: num pedido de US$ 100 com margem de contribuição de US$ 18,70, os dois juntos somam US$ 3 — **16% da margem**. Numa oferta com assinatura, onde o app de subscription é obrigatório, o erro é sistemático.

**Ad spend NÃO entra no `cogs_breakdown`.** Ele é o maior custo variável do cânone, mas nesta skill ele aparece como **CAC** no denominador do PSM (ETAPAs 5 e 7). Somar nos dois lugares conta o mesmo dinheiro duas vezes e derruba a margem artificialmente.

Documente cada um em `04-offer-builder/dados.json` → `cogs_breakdown`.

**2. Features/ingredientes (CONDICIONAL):**
- SE não conseguiu extrair da página automaticamente: "Liste as features ou ingredientes principais do produto."
- SE conseguiu extrair: NÃO pergunte; mostre o que extraiu e peça confirmação rápida ("tá certo? falta alguma coisa?").

**3. Produto complementar:**
"Tem algum produto complementar que poderia vender junto? (se não souber, diz 'não sei')"

Se a resposta for "não sei", NÃO trave: o Gate de Complementaridade da ETAPA 3 deriva candidatos do market research automaticamente.

**Decisões automáticas do sistema (NÃO PERGUNTE):**
- **Preço final**: definido pelo framework de pricing abaixo (Etapa 3), triangulando 3 ancoras (value / competitor / economics)
- **Pick & pack**: se o membro não souber, estime ~$2-3 por unidade E **marcar `"pick_pack_estimated": true` no JSON companion** (membro precisa validar)
- **Gateway fee**: se o membro não souber, estime ~3% do AOV + taxa fixa E **marcar `"gateway_fee_estimated": true`**
- **App de assinatura**: se a oferta tem assinatura e o membro não sabe a taxa do app, use o topo da faixa (1% do valor da transação) E **marcar `"sub_app_fee_estimated": true`**. Oferta sem assinatura = 0, não estimativa.
- **Fee de agência**: pergunte apenas se o membro paga agência **por percentual do ad spend** (se paga valor fixo ou não tem agência, o campo é 0 aqui). Não invente percentual.

**Sanity check obrigatório depois de calcular Unit Economics (Etapa 5):**

Se a **margem de contribuição por pedido** < $20 → PARAR e avisar membro:
> ⚠️  Margem de contribuição por unidade calculada: $X (receita menos custos variáveis — ainda não é lucro; os custos fixos do negócio não estão descontados aqui).
>     Isso é muito baixo pra ecommerce direct-response: o CAC aceitável fica abaixo de $10-15, e o piso físico de CAC em Meta hoje é US$ 15–25 (cânone §3). Ou seja, o número exigido não existe no leilão.
>
>     Causas prováveis:
>     - COGS subestimado (provável se vc não tinha todos os itens do breakdown — veja `pick_pack_estimated`, `gateway_fee_estimated`, `sub_app_fee_estimated`)
>     - Preço de venda abaixo do competitivo (vê o framework de pricing na Etapa 3)
>     - Produto com AOV inerentemente baixo (considera bundle pra aumentar AOV)
>
>     Opções:
>     1. Reveja COGS itemizado real (peça fatura pro fornecedor)
>     2. Aumenta preço via bundle 2-3 unidades ou upsell pós-compra
>     3. Abandona esse produto — margem não sobe via marketing
>
>     Prosseguir mesmo assim? (sim/não)

Se continuar, marca `"margin_warning": true` no manifest pra Skills 10/12 alertarem escala agressiva.

> **Exceção única, e ela não é chute:** membro em `scaling` com janela de payback **medida** (`15-finance-engine/dados.json` → `payback.payback_window_days_measured ≤ 90`, com cohort calibrado) **e caixa medido que aguenta a janela** (`cash.runway_months` do mesmo arquivo) pode operar com margem de primeiro pedido abaixo de $20 de propósito, porque a recompra devolve dentro da janela. As condições completas estão no check 8 da ETAPA 9 — sem elas, o alerta acima vale integralmente.

### ETAPA 2 — MECANISMO ÚNICO (A Parte Mais Importante)

O mecanismo único é o que diferencia seu produto de TODO concorrente. Sem mecanismo forte, a copy vira commodity disputando no preço. Com mecanismo forte, você cria um espaço sem concorrência direta (blue ocean) dentro de qualquer nicho.

**Puxe estes SISTEMAS NOMEADOS da base antes de ideação (rode a `best_query` de cada — NUNCA query genérica):**
- **Unique Mechanism Theory (UMP/UMS — UMP é o mecanismo do problema, UMS é o mecanismo da solução)** (rode `unique mechanism UMP UMS theory two-part problem solution`) — o framework-mãe: mecanismo do problema + mecanismo da solução.
- **UMP/UMS Internal Structure** (rode `UMP UMS structure trigger surprising cause quiz specific delivery`) — anatomia interna do mecanismo (trigger → causa surpreendente → delivery específico).
- **S.I.N. Filter (Simple, Intuitive, New)** (rode `mechanism SIN filter simple intuitive new`) — o filtro aplicado em 2A/2B abaixo.
- **Os 3 tipos de mecanismos (New / Unspoken / Renamed)** (rode `tres tipos de mecanismo new unspoken renamed its toasted bone broth ordem de busca`) — os três tipos (novo, não dito e renomeado) com a ordem de busca entre eles: antes de fabricar mecanismo novo, cheque se o produto já tem um mecanismo não dito ("it's toasted") ou renomeável (bone broth).
- **Fabricação de Mecanismo — receita de 4 passos + pipeline de 9 passos** (rode `fabricar mecanismo composto real indisponivel vilao decompor em constituintes protocolo numerado`) — o caminho da commodity ao new mechanism: partir de um composto real e indisponível, definir o vilão, decompor em constituintes e virar protocolo numerado. Alimenta a Rota B (criação original) da 2A.
- **Proprietary Mechanism Naming (Gum Name)** (rode `proprietary mechanism gum name nickname ritual hack effect`) — como cunhar o nome proprietário (2-4 palavras).
- **The Big 3: New Mechanism / New Information / New Identity** (rode `new mechanism new information new identity big 3 sophisticated market`) — qual eixo usar conforme sophistication.
- **Market Sophistication (5 Stages)** (rode `market sophistication 5 stages Schwartz new mechanism identification`) — determina QUE tipo de mecanismo o mercado ainda aceita.
- **Reeves USP (3 Requirements + 3 Roads)** (rode `Reeves USP three requirements three roads preemptive claim`) — garante que o mecanismo vira proposição única defensável.
- **Hopkins Reason-Why Rule** (rode `Hopkins reason why rule every claim needs a reason`) — todo claim do mecanismo precisa de um porquê concreto.

Frameworks adjacentes de mecanismo (Big Domino, Three False Beliefs, Schwartz Mechanization, Big Idea, Sugarman Concept Selling, Hormozi MAGIC Naming) estão no índice `.claude/lib/kb-index/` — puxe conforme o vertical exigir.

**2A — Ideação (Gerar 5-7 Opções por DUAS rotas):**

Inputs (pras duas rotas):
- Features/ingredientes do produto
- Root cause research da Skill 02 (causa-raiz proprietária)
- `03-competitor-analysis/dados.json` → `validated_library` (mecanismos + ângulos com evidência de veiculação/escala) e `claims_saturation`
- `03-competitor-analysis/creative-patterns.json` (se existir) → `recurring_claims` com `market_validated: true`
- Awareness level do mercado (Schwartz) e sophistication stage (determina que tipo de mecanismo funciona)

**Rota A — Recombinação validada (DEFAULT).** Criar mecanismo do zero é mais caro e arriscado do que recombinar o que o mercado já validou com dinheiro alheio — a validação de mercado é o ativo. Gere a maioria dos candidatos por aqui:

- **A1 — Aprimorar mecanismo validado (mantendo o ângulo):** pegue um mecanismo da `validated_library` com evidência de escala e construa a versão 2: mais específica, mais crível, com um elemento novo (ingrediente, número, etapa do processo) — subindo **+1 no estágio de sofisticação** (Schwartz: quando o mercado já aceitou um mecanismo, a versão ampliada/melhorada dele é o que vence o controle). O nome proprietário é SEMPRE nosso — aprimorar ≠ clonar. `validation_source: "improved_validated"`.
- **A2 — Cruzar mecanismo validado × ângulo validado de OUTRA marca/vertical adjacente:** combinação única, porém pré-validada nas duas pontas (ex: mecanismo de gut health cruzado com ângulo de skincare via ligação intestino-pele). Use `validated_library.mechanisms` de um lado e `validated_library.angles` (ou ângulo escalado de vertical adjacente) do outro. `validation_source: "crossed_validated"`.

**Rota B — Criação original (complementar).** O fluxo clássico: features + root cause + gaps de mecanismo da 03. Use quando a `validated_library` não tem NENHUM mecanismo com evidência real de escala (dias rodando, nº de criativos no mesmo ângulo — o critério é a qualidade da evidência, não a contagem: 2 mecanismos bem evidenciados sustentam a Rota A), ou quando o mercado está em **estágio 5** de sofisticação (pede identidade nova, não mecanismo recombinado). `validation_source: "original"`.

**Regras transversais (valem pras duas rotas):**
- EVITAR mecanismos/claims com saturação ALTA na matriz Claims Saturation da 03 (o público não acredita mais)
- PREEMPTAR claim comum sem dono (Preemptive Claim — claim que vários usam mas ninguém CRAVOU como seu). Fontes: `claims_saturation` dá os candidatos com `count > 0` (claim/count/total/saturation — o campo NÃO diz quem é dono); **quem já "possui" cada claim vem da narrativa do `03-competitor-analysis/competitor-analysis.md`** (a análise por concorrente mostra quem cravou o quê). Claim frequente no JSON + sem dono no relatório = candidato a preempção.
- Registrar em CADA candidato o `validation_source` (de onde veio a validação: qual mecanismo/ângulo, de qual concorrente, com que evidência)

Gere 5-7 opções de mecanismo único no total (mix das rotas — se a validated_library sustentar, 4-5 da Rota A + 1-2 da Rota B). Cada um com:

- **Nome proprietário** (2-4 palavras, memorável, proprietário-soando, pronunciável)
- **Explicação simples** (2-3 frases — como funciona na prática)
- **Base real do produto** (ingrediente, feature, processo, combinação — NÃO inventar ciência falsa)
- **Por que é diferente dos concorrentes** (qual claim rompe, qual gap preenche)
- **Em qual nível de awareness funciona melhor**
- **Match com sophistication stage** (ingredient-based pra Estágio 3, information-based pra Estágio 4, identification pra Estágio 5)
- **validation_source** (improved_validated / crossed_validated / original) + o que valida (qual mecanismo/ângulo de qual concorrente, com que evidência da validated_library)

**Aplicar o filtro S.I.N. (Simple / Intuitive / New):**
- **Simple** (fácil de entender de primeira, sem jargão — "Joint Drought Protocol" comunica na hora, não exige explicação técnica)
- **Intuitive** (faz sentido imediato pro avatar, a lógica "clica" sozinha — "Lipid Barrier Breach" sugere causa e solução sem precisar de aula)
- **New** (soa novo pro mercado, mesmo que a ciência subjacente seja antiga — reformulação criativa de algo conhecido)

Nomes pode vir de:
- Renomear ingredientes/componentes existentes pra novo propósito (ex: num suplemento: "Bioavailable Matrix" em vez de "complexo"; num wearable: "Adaptive Core Module" em vez de "sensor")
- Combinar 2-3 features em conceito unificado (ex: "Triple Action Stack", "Dual Channel System")
- Nomear um processo interno (ex: "48-Hour Activation Protocol", "7-Day Reset Method")
- Reposicionar uma feature secundária como central (ex: transformar feature "com antioxidantes" em "Free Radical Neutralization System"; feature "bateria de 72h" em "Perpetual Charge Architecture")

**2B — Avaliação Rigorosa:**

Pra CADA opção de mecanismo, score 1-10 em:

| Dimensão | O que avaliar |
|---|---|
| **Diferenciação** (1-10) | Quão diferente dos claims dos concorrentes? |
| **Credibilidade** (1-10) | A ciência/lógica por trás é defensável? Fake = 1, baseado em research real = 10 |
| **Memorabilidade** (1-10) | O nome "gruda"? É fácil de repetir? |
| **Expandibilidade** (1-10) | Dá pra expandir em 2-3 parágrafos pra copy sem soar repetitivo? |
| **Match com awareness** (1-10) | Funciona pro nível de awareness dominante do TAM? |

Score final = soma / 5.

**2C — Recomendação:**

Recomende o mecanismo com maior score total, com justificativa explícita por que esse vence os outros. Registre o `validation_source` do vencedor em `dados.json` → `mechanism.validation_source`.

**2D — Documentar a LÓGICA do Mecanismo (sem escrever copy):**

A oferta define a estratégia do mecanismo; a copy nasce na Skill 06. **NUNCA escreva versões prontas de copy do mecanismo aqui (headline, parágrafo de PDP, expansão de advertorial)** — copy pré-escrita na oferta enviesa a Skill 06, que deve reler todo o research e decidir os ângulos sozinha. Documente, no report_language:

- **UMP (o problema):** nome próprio + a lógica de por que as soluções atuais falham, com os estudos/evidências citados (claim_ids da ETAPA 2.5).
- **UMS (a solução):** nome próprio + a lógica de por que a nossa entrega funciona, com os estudos citados.
- **Externalização de culpa:** de quem/do que é a culpa pela falha das soluções anteriores (nunca do avatar).

É essa lógica (nomes + causa + evidência) que a Skill 06 expande em copy nas versões que ELA decidir (headline, parágrafo, expansão longa) conforme awareness e formato de página.

### ETAPA 2.5 — Research Foundation (OBRIGATÓRIO — Lastro de Evidência)

Mecanismo sem lastro científico/empírico é claim vazio e vira copy fraca, ad reprovado e member frustrado. Antes de prosseguir pra Etapa 3, você DEVE construir a base de evidência que sustenta o mecanismo recomendado.

**Fontes a consultar (web search extensivo):**

1. **Estudos científicos / papers peer-reviewed**
   - PubMed (`site:pubmed.ncbi.nlm.nih.gov`)
   - Google Scholar (`site:scholar.google.com`)
   - ResearchGate, ScienceDirect, NIH
   - Queries: nome do ingrediente/processo + "clinical trial", "peer-reviewed", "mechanism of action", "efficacy study", "randomized controlled trial"

2. **Press releases / comunicados de pesquisa institucional**
   - Harvard Health Publishing, Mayo Clinic, Cleveland Clinic, WebMD
   - Press releases de fornecedores de ingrediente (Lonza, DSM, BASF, etc — têm whitepapers técnicos)

3. **Regulatório / referências oficiais**
   - FDA GRAS status (se aplicável)
   - EMA monographs, EFSA opinions
   - USP Pharmacopeia

4. **Reviews sistemáticas e meta-análises** (evidência de maior grau)
   - Cochrane Library
   - Meta-analyses em periódicos da especialidade

5. **Patents** (ingrediente/processo protegido)
   - Google Patents — procurar prior art que sustenta o mecanismo

**Para CADA claim do mecanismo (causa-raiz, ingrediente ativo, resultado esperado, diferenciação), documente:**

```json
{
  "claim": "texto do claim",
  "evidence_type": "peer_reviewed_study|meta_analysis|press_release|regulatory|patent|empirical_observation",
  "source_title": "título completo",
  "source_url": "url completa",
  "source_date": "YYYY-MM-DD",
  "strength": "strong|moderate|weak",
  "strength_rationale": "por que essa classificação",
  "quote_or_summary": "trecho literal ou resumo 1-2 frases",
  "usage_rights": "public|paywalled|needs_permission"
}
```

**Regras de rigor (NÃO NEGOCIÁVEIS):**

- Proibido inventar estudo ou extrapolar além do que a fonte afirma literalmente
- Proibido citar "estudos mostram que..." sem fonte rastreável com URL
- Se a evidência é `weak` (anecdotal, in-vitro só, animal study único, tamanho amostral pequeno), o claim precisa ser suavizado ("helps with", "supports", "may contribute") — não afirmado categoricamente
- Se NENHUMA evidência for encontrada pra um claim central, o mecanismo precisa ser reformulado antes de prosseguir — não escreva copy sobre fundação vazia

**Output dessa etapa:**

Arquivo `workspace/[produto]/04-offer-builder/research-foundation.json` contendo:
```json
{
  "mechanism_name": "...",
  "evidence_items": [ { ... } ],
  "summary_statement": "2-3 frases resumindo a base de evidência do mecanismo",
  "confidence_score": "high|medium|low",
  "gaps_and_risks": "claims que ficaram sem lastro forte — a serem suavizados na copy"
}
```

Esse arquivo é lido pelas skills 06 (copy) e 08 (creatives) pra ancorar afirmações com fonte verificável. Copy sem `04-offer-builder/research-foundation.json` acessível roda com warning "claims unverified — escalate carefully".

### ETAPA 3 — Estrutura de Oferta

Monte a arquitetura econômica completa:

**Produto Principal:**
- **Nome do produto** (se ainda não tem, sugira — pode incluir mecanismo no nome: ex: "[Brand] — [Mechanism Name] [Category]", adaptar ao vertical)
- **Preço base**: ver framework de pricing abaixo (triangulação de 3 ancoras)
- **Core deliverable**: o produto em si (1 unidade / X ml / Y cápsulas)

**Puxe estes SISTEMAS NOMEADOS de pricing/value antes de ancorar (rode a `best_query` de cada):**
- **Offer Rebuild (0.47x → 3.6x ROAS só mudando a oferta)** (rode `mesmos ads mesma conta só mudou a oferta, subscription destrói CPA 100x`) — o caso que prova que a oferta é a alavanca desta etapa inteira: mesmos ads, mesma conta, e o ROAS saiu de 0,47x pra 3,6x só com a troca da oferta. A mesma puxada traz o efeito da palavra "subscription" usado no bloco de assinatura abaixo.
- **Hormozi Value Equation** (rode `Hormozi value equation dream outcome perceived likelihood time delay effort sacrifice`) — sustenta a ancora value-anchored abaixo.
- **Anchoring & Adjustment** (rode `pricing anchoring adjustment set high anchor was price SSN auction Ariely`) — como ancorar o preço alto antes do real.
- **Decoy Effect (Asymmetric Dominance)** (rode `decoy effect asymmetric dominance Economist subscription Williams-Sonoma bread machine`) — desenha o bundle de 3 tiers.
- **Extremeness Aversion** (rode `extremeness aversion three tiers middle option beer experiment`) — por que o 3-pack "Popular" no meio vende mais.
- **Charm Pricing (Endings in 9)** (rode `charm pricing nine ending left-digit effect 24 percent catalog`) — terminação de preço.
- **3x+ Markup Rule + $60 AOV Floor** (rode `3x markup rule 60 dollar AOV floor COGS shipping margin paid traffic CPM fixed`) — piso de margem pra tráfego pago (cruza com o sanity de margem da ETAPA 1).
- **Hormozi Virtuous Cycle of Price** (rode `Hormozi virtuous cycle of price premium pricing better clients`) — quando subir o preço melhora o negócio.

Pricing psychology adjacente (Coherent Arbitrariness, Zero Price Effect, Mental Accounting, Endowment, Transaction Utility, Kennedy Five Price Minimizers) está no índice — puxe se o framing do preço exigir.

**Framework de pricing (escolher UMA ancora, validar com as outras 2):**
- **Value-anchored**: Preço = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort)  [Hormozi Value Equation]
- **Competitor-anchored**: Mediana dos top 3 concorrentes × modificador (1.1-1.3 se diferenciação alta; 0.8-0.95 se entrada competitiva)
- **Economics-anchored**: COGS × 4 a 6 (ecommerce direct-response padrão para viabilizar paid acquisition)

**Régua objetiva de divergência das âncoras:** `divergência = (âncora_máx − âncora_mín) / âncora_mediana`. Se **> 0.40**, revisitar a oferta antes de prosseguir. Exemplo: âncoras $49 / $62 / $97 → (97 − 49) / 62 = **0.77** → divergem demais, revisar (provavelmente o value-anchored está inflado ou o economics-anchored expõe COGS alto). Divergência ≤ 0.40 = as três contam a mesma história; escolha a âncora primária e siga.

**Bundles (estrutura clássica):**

| Bundle | Quantidade | Preço | Preço por unidade | Savings vs solo |
|---|---|---|---|---|
| Solo | 1x | $X | $X | — |
| Popular | 3x | $Y | $Y/3 | ~$Z ou ~Z% |
| Best Value | 6x | $W | $W/6 | ~$A ou ~A% |

Regra prática (pode ajustar):
- 3-pack: ~25-35% savings vs 3× solo
- 6-pack: ~40-50% savings vs 6× solo

Marcar **Popular** no 3-pack (visualmente destacado — driver de AOV). Best Value no 6-pack (pra clientes que compram em volume alto (whales)).

**Arquitetura de assinatura (decisão OBRIGATÓRIA pra produto consumível):**

**Puxe estes SISTEMAS NOMEADOS de assinatura antes de decidir (rode a `best_query` de cada):**
- **Estrutura da Oferta de Assinatura (não dê desconto — suba o preço do one-time)** (rode `você paga mais por NÃO assinar, one-click upsell na thank you page, produto grátis melhor que desconto`) — o sistema completo por trás da regra do desconto invertido abaixo: prêmio no one-time, produto grátis no lugar de desconto, one-click upsell na thank-you page.
- **Arquitetura Hume: soft offer envolvendo continuidade dura** (rode `entrada grátis envolvendo assinatura recorrente, micro-compromisso de $5, cancel anytime como feature`) — a intro offer: entrada grátis ou micro-compromisso de $5 embrulhando a assinatura recorrente, com o cancel anytime vendido como feature. Candidata quando o avatar é cético de assinatura mas a janela de consumo pede recorrência.
- **Try Before You Buy (o efeito da palavra "subscription")** — o efeito em si já veio na puxada do Offer Rebuild acima (a palavra "subscription" na página destrói o CPA — não repita a busca). Pro enquadramento substituto, rode `try before you buy enquadramento de assinatura sem a palavra subscription` — a assinatura é apresentada como "experimente antes de comprar", nunca pela palavra "subscription"; isso vale pro nome do selling plan que a 07b implementa e pra copy que a 06 escreve.

Se o produto é consumível (acaba e precisa recomprar: supplement, skincare, café, etc), decida AQUI a arquitetura de assinatura — ela muda o LTV, o PSM e o que a 07b (selling plan na PDP), a 07d (superfícies de checkout) e a 13 (flow de replenishment) implementam. Três arquiteturas possíveis:

| Arquitetura | O que é | Quando escolher | Impacto no LTV/PSM |
|---|---|---|---|
| `subscription_first` | Subscribe & Save como opção destacada na PDP, com o preço de assinatura no preço-base e o **one-time ~15% mais caro**; one-time como alternativa | Janela de consumo curta (≤ 45 dias), categoria acostumada com assinatura (supplements, café), preço one-time majorado que ainda cabe na âncora de concorrente | LTV 2-4× o do one-time; PSM sobe porque o LTV real substitui o proxy de AOV nas ETAPAs 5/7; churn de assinatura vira a métrica a vigiar |
| `onetime_plus_sub_no_reorder` | PDP vende one-time; a assinatura é oferecida no momento do REORDER (flow de replenishment da 13) e no pós-compra | Produto novo sem prova de consumo, avatar cético de assinatura, ou preço de entrada alto que a assinatura assustaria | LTV cresce mais devagar, mas sem custo de conversão na 1ª compra; a 13 carrega a conversão pra assinatura no timing certo |
| `no_subscription` | Sem selling plan; volume via bundle 3/6-pack | Produto não-consumível, consumível com janela > 90 dias, ou operação sem app de subscription | LTV depende de reorder manual; o 6-pack "Best Value" faz o papel do supply longo |

Critérios de decisão: janela de consumo (≤ 45 dias favorece `subscription_first`), familiaridade do avatar com assinatura na categoria (market research), preço (o prêmio de ~15% no one-time precisa caber na âncora de concorrente desta ETAPA), e stage (starter sem app de subscription instalado → começar `onetime_plus_sub_no_reorder` e migrar quando o consumo estiver provado). Produto não-consumível → `no_subscription` sem cerimônia.

**Regra de precificação da assinatura — o desconto é INVERTIDO (obrigatória em qualquer arquitetura com assinatura):**

**Não dê desconto ao assinante. Suba o preço do one-time em ~15%.** O assinante paga o preço-base; quem NÃO assina é que paga mais. O enquadramento na página é esse: você paga mais por não assinar.

Por que a inversão importa em vez de ser detalhe de framing: desconto de assinatura entrega margem em TODA recompra — exatamente onde a economia já é a melhor da operação, porque a recompra não carrega CAC nem fee de agência atrelado a spend (cânone §2). O prêmio no one-time produz o mesmo diferencial percebido sem tirar margem de nenhum pedido, e ainda melhora a margem de contribuição de quem compra avulso. Registrar como `onetime_premium_pct` (o quanto o one-time fica ACIMA do preço de assinatura), nunca como desconto.

O prêmio no one-time é uma mudança de preço real: revalide as 3 âncoras da triangulação desta ETAPA com o preço majorado antes de cravar. Se o one-time majorado estoura a âncora de concorrente, o caminho é reduzir o prêmio, não voltar pro desconto de assinatura.

**Registrar em `04-offer-builder/dados.json` → `subscription_architecture`** (campo top-level, enum acima) + `onetime_premium_pct` se houver assinatura — a 07b lê pra decidir se a PDP tem selling plan (Subscribe & Save) e com qual dos dois preços em cada opção, a 07d pra superfícies de checkout, e a 13 pro flow de replenishment (na arquitetura 2, o Email 2 do replenishment é ONDE a assinatura é oferecida — o framing lá também é prêmio no one-time, não desconto). Se escolheu `subscription_first`, refaça o PSM da ETAPA 7 com o LTV de assinatura (não só o AOV projetado) — é exatamente o cenário em que o LTV real diverge do proxy.

**Gate de Complementaridade (OBRIGATÓRIO pra TODO componente de AOV — bump, upsell, bundle-mate, GWP):**

Nenhum componente entra na oferta por ser "um produto que dá pra vender junto". Todo candidato passa pela hierarquia abaixo — avalie na ordem; a categoria mais alta em que ele se encaixa define a prioridade:

1. **More-of-same** — mais unidades do PRÓPRIO produto (bundle, supply maior). Default e maior aceitação: pra comprador NOVO de tráfego frio, o que mais converte no pós-compra não é complemento, é o mesmo produto com desconto exclusivo do momento (operadores de supplements documentaram publicamente AOV saindo de $70-80 pra $100-130 só com isso). Inclui o "big swing": supply de 3-6 meses a 3-5× o valor do pedido — aceita menos, mas ganha em lucro por visitante.
2. **Consumption chaining** — item consumido JUNTO, no mesmo ritual de uso do produto principal (o cleanser antes do sérum, o shaker do pré-treino).
3. **Aceleração de resultado** — item que encurta o tempo até o resultado do desejo central (menos Time Delay = Value Equation melhor).
4. **Problema adjacente** — o PRÓXIMO problema que o avatar enfrenta DEPOIS de alcançar o resultado (o passo seguinte da jornada).

**REPROVADO:** componente que não se encaixa em NENHUMA das 4 = complemento aleatório — fica fora da oferta.

**Se o membro respondeu "não sei" na pergunta 3 da ETAPA 1:** NÃO pule e NÃO aceite qualquer coisa. DERIVE 3-5 candidatos das 4 categorias cruzando o market research: ritual de uso + desejo central + jornada do avatar (`02-market-research/market-research.md` + `dados.json`) e o que o avatar já compra/tenta pra resolver o problema (`alternative_solutions` da 02 e da 03). Apresente cada candidato com a categoria em que se encaixa.

**Branch "sem complemento viável":** se nenhum candidato externo passa no gate, a categoria 1 (more-of-same) SEMPRE existe — bundle e big swing não dependem de segundo produto. Zere as linhas de bump/upsell externo na tabela de unit economics (ETAPA 5) em vez de forçar componente aleatório.

**Segmentação novo vs recorrente:** a hierarquia acima vale pro funil FRIO (comprador novo). Cliente recorrente inverte: produto complementar não-testado converte 20-35% melhor pra quem já confia na marca — essa é alavanca das Skills 07d (superfícies de checkout pra recorrente) e 13 (retention), não do funil de aquisição.

**Checkout Bump:**
- Componente aprovado no Gate (tipicamente categoria 2-4) de baixo preço ($9-19) ou add-on (frete expresso, versão com mais, etc)
- Taxa de aceitação: 20-35% quando bem posicionado (conservador: 20%). O teto de 20-50% vem do order-form bump de funil dedicado; em checkout Shopify real o range observado fica mais perto do piso — recalibre com o take rate real após 2 semanas
- Copy curta do bump (1 frase + 1 benefício)

**Upsell Pós-Compra:**
- Prioridade 1 (tráfego frio): **more-of-same** — o próprio produto com desconto exclusivo do momento pós-compra, ou o big swing (supply 3-6 meses)
- Prioridade 2: componente aprovado no Gate de maior ticket ($47-97+) que amplia o resultado
- Apresentado na thank-you page após a compra (a 07d implementa a superfície)
- Taxa de aceitação: média da plataforma 3-8%; oferta bem casada (Gate + more-of-same) chega a 8-14% (conservador: 8%)
- Copy do upsell (2-3 frases + principal benefício + oferta)

**OBRIGATÓRIO — Registrar bump, upsell e tiers de bundle no bloco top-level `aov_levers` do `04-offer-builder/dados.json`** (estrutura exata no Output Schema no fim desta skill). A Skill 07d lê DESSE bloco na ETAPA 1 dela — não da prosa acima (a prosa é a versão humana). Alavanca que a oferta não tem = `null` (nunca inventar).

**Stack de Valor Com Ancoragem:**

**Puxe estes SISTEMAS NOMEADOS de stack/bônus antes de montar (rode a `best_query` de cada):**
- **Bonus Stacking (Value Stack / Stack Slide)** (rode `value stack stack slide bonus stacking standalone value exceeds price`) — soma cumulativa que faz o preço parecer pequeno.
- **Razor-Blade vs Handle (Bonus Fit Principle)** (rode `razor blade vs handle bonus fit natural complement to product`) — cada bônus deve aumentar o consumo/resultado do produto principal.
- **Bonus Types Taxonomy** (rode `bonus types presuppose success enables success graduation gift access partner complementary`) — escolhe o `type` certo (não default pra PDF), alimenta o campo `bonuses[]` do JSON.
- **FTC Anchored-Value / Fictitious-Pricing Legality** (rode `FTC anchored value fictitious pricing bonus must be actually sold legality`) — o `value_anchored` de cada bônus precisa ser legalmente sustentável (o bônus tem que ser realmente vendível por aquele valor).
- **P.S. que Acrescenta — Fast-Reply Gift** (rode `P.S. acrescenta bonus novo fast-reply gift nao recapitula oferta 154 de 179`) — padrão medido em 154 de 179 peças: o P.S. ACRESCENTA um bônus novo (o fast-reply gift, prêmio por agir agora) em vez de recapitular a oferta. A decisão de oferta é aqui: se o stack tiver um bônus com essa vocação, marque-o — a Skill 06 escreve o P.S.; a oferta define qual bônus ele entrega.

**Nomeação dos entregáveis — a regra do `Not: "___"` (OBRIGATÓRIA antes de escrever o stack):**

A palavra genérica da categoria é **proibida em toda a pilha de entregáveis**. Se o stack lista "e-book", "vídeo", "newsletter", "acesso ao grupo", ele está descrevendo **formato** em vez de nomear **ativo** — e formato não tem valor percebido. Ninguém paga por "um PDF"; paga pelo ativo que aquele PDF é.

Como executar, item por item (produto principal, bônus e entregáveis inclusos):

1. Escreva a palavra genérica que você ia usar, marcada como proibida: `Not: "e-book"`.
2. Nomeie o ativo pelo trabalho que ele faz na vida do comprador, não pelo arquivo que ele é.
3. Só entra no stack o nome do passo 2.

Exemplos reais desse método aplicado numa peça vencedora: email virou **"Mission Order"**, vídeo virou **"Debriefing"**, site virou **"Digital Headquarters"**, carteira virou **"Victory Scorecard"**. Na peça auditada a anotação `Not: "___"` aparece 9 vezes só na seção de oferta — a disciplina é item a item, não uma passada geral no fim.

Detalhe completo do método em `.claude/lib/swipe-models/specimens.json` → nó `auditoria`, camada `rosa-nomeacao`. **E puxe o sistema completo da base:** rode `not X renomear termo generico por proprietario newsletter research service charter member` (deep=true) — é a entrada `Not: X` do índice, com o percurso da oferta inteira trocando cada termo-commodity por nome proprietário (newsletter → research service, assinante → charter member).

Dois limites que evitam erro na aplicação:
- **O nome nomeia, não promete o que o ativo não entrega.** Nome proprietário não é licença pra inflar: o entregável continua sendo o que é, e o `value_anchored` continua preso à regra de valor legalmente sustentável (o bônus tem que ser realmente vendível por aquele valor).
- **O nome é copy pública (inglês US); o formato técnico continua nos campos de máquina.** `bonuses[].name` e a string `offer_stack` recebem o nome proprietário; `type` e `format_hint` continuam com o enum técnico (`free_ebook`, `pdf`, `community_access`) — é isso que a Skill 05 usa pra montar a entrega. Não há contradição entre os dois campos: o comprador lê o ativo, o pipeline lê o formato.

Liste tudo que vem no pacote com valor ancorado (todos os nomes já passados pela regra acima):
- Produto principal: valor $X
- Bonus 1 (o ativo nomeado — `Not: "guia digital"`): $Y
- Bonus 2 (o ativo nomeado — `Not: "acesso ao grupo"`): $Z
- Bonus 3 (o ativo nomeado — `Not: "consultoria inicial"`): $W
- **Valor total**: $X+Y+Z+W
- **Preço hoje**: $(preço real)
- **Economia percebida**: $(diferença)

Cada bonus é REAL (entregável), não inflado artificialmente. O stack cria percepção de valor desproporcional ao preço. Bônus físicos (`gift_with_purchase` / `free_complementary_sku`) também passam no **Gate de Complementaridade** acima; os digitais seguem o Razor-Blade (o mesmo gate aplicado a conteúdo: o bônus aumenta o consumo/resultado do produto principal, senão descarta).

**OBRIGATÓRIO — Registrar bonuses no campo top-level `bonuses[]` do `04-offer-builder/dados.json`.** Skill 05 (bonus-delivery) lê desse campo pra montar o pipeline de entrega. Pra cada bonus do stack, gerar entry (enum idêntico ao do Output Schema no fim desta skill — é o enum canônico):

```json
{
  "id": "bonus-01",
  "name": "o ativo nomeado — texto igual ao da stack, nunca a palavra de formato (regra do Not: \"___\")",
  "description": "1-2 frases do que é e por que vale",
  "value_anchored": 49,
  "type": "gift_with_purchase | free_complementary_sku | free_ebook | gift_wrapping | digital_guide | discount_code | workbook | checklist | community_access | video_series | consultation_call | trial_extension",
  "format_hint": "in_box | shopify_function | gift_app | pdf | notion | figma | wistia | klaviyo_email | shopify_discount | circle_invite",
  "condition": "unconditional | cart_threshold | tier_specific",
  "delivery_trigger": "post_purchase | on_signup | day_7_post_purchase | on_first_reorder"
}
```

**`condition` é OBRIGATÓRIO e a Skill 05 configura a entrega exatamente por ele:** bônus mostrado no offer_stack da PDP a TODO comprador = `unconditional` (auto-add em toda compra — threshold aqui quebraria a promessa da página); GWP destravado por subtotal do carrinho = `cart_threshold` (e a copy da página DEVE dizer a condição: "FREE over $X"); brinde de tier específico (3-pack/6-pack) = `tier_specific`. Mismatch entre condition e o que a página promete é promessa quebrada na cara do comprador.

**Tipos NÃO default pra "PDF":** escolher o type que realmente bate com o avatar. Se membro disser "bonus é PDF só porque é fácil", questionar: "Esse avatar REALMENTE quer PDF? Pra [avatar profile], [alternative type] costuma ter access rate maior." Documentar essa decisão.

### ETAPA 4 — Garantia (Risk Reversal)

**Puxe estes SISTEMAS NOMEADOS de garantia/risk-reversal antes de escolher (rode a `best_query` de cada — NUNCA query genérica):**
- **Hormozi Four Guarantee Types** (rode `Hormozi four guarantee types unconditional conditional anti-guarantee implied`) — o menu de 4 tipos que mapeia nos "Tipos possíveis" abaixo.
- **Guarantee Stacking** (rode `Hormozi guarantee stacking short-term unconditional long-term conditional`) — combinar uma incondicional curta + uma condicional longa.
- **Guarantee Naming** (rode `Hormozi naming your guarantee vivid memorable Club a Baby Seal Shark Infested Waters`) — dar nome vívido à garantia (entra na copy da garantia abaixo).
- **Longer Guarantee = Fewer Refunds Paradox** (rode `longer guarantee fewer refunds one year vs 30 day eye off calendar Cashvertising`) — por que prazo maior reduz reembolsos (tira o olho do calendário).
- **The Guarantee Math** (rode `guarantee math net sales conversion lift refund rate Fladlien buyback`) — calcula se o lift de conversão cobre o refund rate antes de cravar o tipo (cruza com a margem da ETAPA 5).
- **As Quatro Formas dos Mestres (taxonomia de garantia por MECÂNICA)** (rode `devolver o pacote vazio, dobro do dinheiro, nem cobrar até funcionar, árbitro externo`) — classifica a garantia pela mecânica, não pelo prazo: devolver o pacote vazio, dobro do dinheiro, não cobrar até funcionar, árbitro externo. Amplia o menu de "Tipos possíveis" abaixo.
- **Escada de 3 Níveis + tipologia em 5 formatos (arquivo de 179 promos)** (rode `139 de 179 promos com refund, keep the gifts, performance pledge com número e prazo`) — os padrões MEDIDOS de garantia: escalada em 3 níveis, keep the gifts (o cliente devolve o produto e fica com os bônus), performance pledge com número e prazo — 139 de 179 promos com refund.

Kennedy Five-Level Guarantee Hierarchy e Guarantee Power Statement Template estão no índice — puxe se precisar de hierarquia mais granular ou template de frase.

**Tipos possíveis:**
- **Money-back** (30, 60, 90 dias): baixo risco pro cliente, médio risco pro merchant
- **Results-based** ("se não funcionar, reembolsamos"): forte psicologicamente, exige evidência clara de uso
- **Extended trial** (primeiro mês grátis, cancela depois): baixa barreira de entrada mas exige subscription
- **Double-your-money-back**: agressivo, usa sophistication alto, mas blindado contra abuso (com critérios)

**Recomende o tipo certo baseado em:**
- Sophistication stage (estágios mais altos pedem garantias mais agressivas)
- Margem da oferta (margem pequena não aguenta money-back generoso)
- Ceticismo do avatar (market research — "já tentei X" → garantia forte converte)
- Tipo de produto (consumível vs duradouro)

**Escreva a copy da garantia** (2-3 frases, tom confiante mas claro sobre condições):
Exemplo: "90-day results guarantee. If you don't see visible improvement in the first 90 days, send us a photo — we'll refund every penny. No questions, no hoops."

### ETAPA 5 — Unit Economics (Tabela Completa)

**Puxe estes SISTEMAS NOMEADOS de unit economics antes de calcular (rode a `best_query` de cada — vale também pra ETAPAs 6/7):**
- **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS golden ratio growth`) — o golden ratio que substitui ROAS; é o núcleo das ETAPAs 5-7.
- **Unit Economics Hierarchy (CPA vs CAC, GPT)** (rode `unit economics CPA vs CAC blended CPA GPT net profit hero offer`) — separa CPA de CAC e define o denominador correto de margem.
- **Hormozi LTGP:CAC Ratio** (rode `Hormozi LTGP CAC ratio 3 to 1 lifetime gross profit acquisition cost`) — alvo 3:1 de lifetime gross profit sobre CAC.
- **Client Financed Acquisition (CFA)** (rode `Hormozi client financed acquisition front end covers CAC backend pure profit`) — front-end (bump/upsell) cobre o CAC, backend vira lucro.
- **Pricing Leverage Math (5% Price = 50% Profit)** (rode `pricing leverage 5 percent price increase 50 percent profit thin margin`) — quando a margem é fina, mexer no preço move o lucro desproporcionalmente (input pra ETAPA 7 quando PSM < 1.1).

**Primeiro pedido e recompra são DUAS economias diferentes e vão em DUAS tabelas separadas** (cânone §2). Misturar as duas numa média esconde exatamente o que decide o negócio: o primeiro pedido carrega o CAC inteiro, a recompra não carrega nenhum. Um produto pode ser deficitário na primeira compra e excelente na segunda — e a decisão de spend depende de qual dos dois você está olhando.

O que cai em cada lado:

| Componente | Primeiro pedido | Recompra |
|---|---|---|
| CAC | carrega ele inteiro | não carrega |
| Fee de agência atrelado a % do ad spend | sim | não |
| Upsell pós-compra | infla o AOV e não se repete | não existe |
| Brinde de entrada, bundle de introdução, desconto de primeira compra | sim, e piora a margem | não |
| Kit/peça cara que só vai na 1ª remessa | sim (a marca de lâmina manda o cabo na primeira e só lâminas depois) | não |
| Resultado típico | AOV maior, margem pior | AOV possivelmente menor, margem bem melhor |

**5A — Economia do PRIMEIRO PEDIDO** (uma linha por variação da oferta — é esta tabela que governa a decisão de spend):

| Variação | AOV | COGS entregue | Pick&Pack | Frete | Pagamento | Taxas | App assinatura | Fee agência variável | Provisão reembolso | Custo variável total | Margem contrib. $ | Margem contrib. % | Breakeven ROAS | Teto de CAC (2× ROAS) | Teto de CAC (3× ROAS) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Solo | | | | | | | | | | | | | | | |
| 3-pack | | | | | | | | | | | | | | | |
| 6-pack | | | | | | | | | | | | | | | |
| Solo + Bump | | | | | | | | | | | | | | | |
| 3-pack + Bump | | | | | | | | | | | | | | | |
| Solo + Upsell | | | | | | | | | | | | | | | |

(A coluna "Provisão reembolso" fica vazia quando a devolução já foi descontada do AOV como net AOV na ETAPA 6 — a provisão conta uma vez só, e o relatório diz em qual dos dois lugares ela está.)

**5B — Economia da RECOMPRA** (obrigatória quando o produto é consumível ou tem assinatura; produto sem recompra prevista → grave `repeat_order: null` e diga isso no relatório em uma linha):

| Item | Valor |
|---|---|
| AOV da recompra (sem upsell pós-compra, sem kit de entrada) | |
| Custo variável total (sem CAC, sem fee de agência atrelado a spend) | |
| Margem de contribuição $ | |
| Margem de contribuição % | |

A diferença costuma ser grande o bastante pra inverter a leitura da oferta: no mesmo pedido de US$ 100 do exemplo canônico, a margem de contribuição do primeiro pedido é US$ 18,70 (18,7%) e a da recompra é US$ 60,70 (60,7%).

**5C — AOV blended** (só quando as duas tabelas existem; é o número que descreve a operação inteira, nunca o que decide spend):

`AOV blended = (AOV 1ª ordem × nº de 1ªs ordens + AOV de recompra × nº de recompras) ÷ total de transações`

Grave como `unit_economics.aov_blended`. **Nenhum cálculo de breakeven, teto de CAC ou PSM usa o blended** — todos usam a tabela 5A. O blended existe pra o membro entender o painel dele, não pra decidir mídia.

### Unit Economics — Fórmulas

Receita por pedido:
- AOV = Average Order Value (Preço × unidades médias por pedido)

Custo variável por pedido:
- Custo variável total = COGS entregue + Frete + Pick&Pack + Processamento de pagamento (%) + Taxas/Impostos + App de assinatura (0,5–1%, se houver) + Fee de agência (% do spend, se houver) + Provisão de reembolso/chargeback (se não estiver descontada no net AOV) — **os itens do `cogs_breakdown` da ETAPA 1, nenhum de fora** (omitir qualquer um infla a margem e distorce breakeven_cpa/teto de CAC/PSM). Ad spend fica FORA desta soma: ele entra como CAC no PSM.

Margem de contribuição por pedido:
- **Margem de contribuição $ = AOV − Custo variável total**

> **Este número NÃO é lucro** (cânone §1). Lucro = margem de contribuição − custos fixos. Toda a ETAPA 5 opera antes dos custos fixos, e por isso nenhum número desta etapa pode ser rotulado como "lucro" — nem na tabela, nem no relatório, nem na conversa com o membro.

> **Denominador canônico:** toda a unit economics usa `weighted_margin_per_order` (margem de contribuição média ponderada por AOV do PRIMEIRO PEDIDO, considerando bumps + upsells) como denominador. Quando a oferta não tem bump/upsell, ele iguala `margin_per_unit`. Os campos `breakeven_cpa`, `target_cpa_primary_2x/3x` e `breakeven_roas` do `04-offer-builder/dados.json` derivam SEMPRE de `weighted_margin_per_order` (ver "Nota sobre nomenclatura" no Output Schema). A Skill 11 lê assim.

**Breakeven CAC / Breakeven ROAS** (o ponto de empate — empate contra os custos variáveis, ainda antes dos fixos):
- Breakeven CAC = weighted_margin_per_order
- Breakeven ROAS = AOV / weighted_margin_per_order
- Exemplo: AOV $118, weighted_margin_per_order $72 → Breakeven CAC = $72, Breakeven ROAS = 118/72 = 1.64
- Significa: precisa gerar $1.64 de receita para cada $1 em ads só para empatar

**Teto de CAC** (custo máximo de aquisição para N× ROAS desejado):
- Teto de CAC para ROAS N = weighted_margin_per_order / N
- Exemplo: weighted_margin $72, quer 2× ROAS → teto = 72/2 = $36
- Para 3× ROAS → teto = 72/3 = $24
- Sanidade: teto (2×) < breakeven_cac SEMPRE ($36 < $72).

> **CAC ≠ CPA — e é aqui que a diferença aparece** (cânone §3). **CPA de plataforma** é o custo por compra que o Meta reporta, e ele conta conversões atribuídas pela própria plataforma, incluindo compras de clientes que já existiam. **CAC** é `ad spend ÷ clientes NOVOS`, e o número de clientes novos vem do **Shopify** (`new customer = TRUE`), não do gerenciador de ads. Numa loja com recompra, o CPA de plataforma é sempre menor que o CAC real — o denominador dele está inflado com gente que já era cliente. Decisão de aquisição (é este o caso destes tetos) usa **CAC**; misturar os dois torna o modelo fake.
>
> Os campos JSON continuam com os nomes `breakeven_cpa` e `target_cpa_primary_2x/3x` porque são contrato de leitura das skills 07d/10/11 — **o nome é legado, o conteúdo é teto de CAC**. Registre a base explicitamente em `unit_economics.cac_basis: "shopify_new_customer"` pra que a comparação com o número medido não seja feita contra o CPA do gerenciador.

**PSM — Profitable Scaling Margin** (o "golden ratio" que substitui ROAS na decisão de escala; é a **MESMA fórmula** que a skill 11 grava como `psm_real`, pra que o teórico do offer e o real medido sejam comparáveis — a skill 12 lê os dois):
- **PSM = LTV / (CAC + COGS)** — LTV = AOV projetado do primeiro pedido quando não há histórico de recompra (proxy); **COGS = somatório de TODOS os itens do `cogs_breakdown`, exatamente como a Skill 11 define — nunca só o custo do produto**; **CAC = custo por cliente NOVO que o membro aceitaria pagar (base Shopify, não CPA de plataforma)**. Avalie no **teto de 2×**, NÃO no breakeven (no breakeven, PSM = 1.0 por definição: AOV = weighted_margin + COGS = CAC breakeven + COGS).
- Exemplo (mesmos números do exemplo acima): AOV/LTV $118, weighted_margin $72 → COGS (somatório do breakdown) = 118 − 72 = **$46**; CAC-alvo (2×) $36 → PSM = 118 / (36 + 46) = **1.44**.
- Thresholds (idênticos às skills 11/12): **>1.3 escala agressiva · 1.1–1.3 escala estável (+5%) · 1.0–1.1 breakeven · <1.0 não viável**.
- Grave como `psm_theoretical` no `dados.json`. A skill 11 grava `psm_real` (mesma fórmula, com o custo de aquisição real medido); a skill 12 compara os dois.

**Piso de CAC (gate de sanidade — cânone §3):** o leilão tem um chão físico dado por CPM e CTR. No melhor caso realista (CPM ~US$ 10–15, CTR ~3%), o **CAC mínimo em escala fica em US$ 15–25**. Um teto de CAC abaixo disso não é um alvo apertado, é um alvo que não existe: nenhuma operação de 8 dígitos roda com CAC de US$ 15. Se o teto de CAC (2×) da oferta cair abaixo de US$ 25, a oferta não sustenta escala e o caminho é AOV/LTV, não "mídia melhor" — a checagem formal está no check 12 da ETAPA 9. Se o CAC medido depois vier ABAIXO desse piso, desconfie da atribuição antes de comemorar.

**Regra crítica:** o teto de CAC pra 2× ROAS deve ser viável com o budget do membro E acima do piso de US$ 25. Se a margem de contribuição < $15-20, a oferta não sustenta ads a não ser em volume muito alto.

### ETAPA 6 — AOV Projetado (com Bump e Upsell Acceptance)

**Puxe estes SISTEMAS NOMEADOS de AOV/upsell antes de projetar (rode a `best_query` de cada):**
- **Profit Optimization 4 Categories + AOV Builders** (rode `profit optimization four categories AOV builders bundles free shipping threshold volume discount GWP profit per visitor`) — o menu de alavancas de AOV (bundle, threshold de frete grátis, volume discount, GWP).
- **Free-Plus-Shipping & Order Form Bump** (rode `Brunson free plus shipping buyer 10x order form bump 20 to 50 percent`) — taxas de aceitação realistas do bump (20-50%) que calibram a estimativa abaixo.
- **Three OTO Structures** (rode `Brunson three OTO structures next thing do it faster need help upsell`) — estrutura o upsell pós-compra (próxima coisa / fazer mais rápido / preciso de ajuda).
- **AOV Money Close + Offer Bump + Add-More-Packages** (rode `AOV money close offer bump add more packages biggest package most popular checkout`) — qual pacote destacar e como apresentar o "add more" no checkout.

Estime taxas de aceitação realistas (ajustar depois com dados reais):
- **Bump acceptance**: 20-35% (conservador: 20%) — o teto de 20-50% é de order-form bump de funil dedicado; checkout Shopify real fica mais perto do piso
- **Upsell acceptance (post-purchase)**: média da plataforma 3-8%; oferta bem casada (Gate de Complementaridade + more-of-same) 8-14% (conservador: 8%)
- Referência de lift 2026: página post-purchase bem construída adiciona 12-22% no valor do pedido; as 3 superfícies juntas (cart + checkout + post-purchase) ≈ +22% de AOV

Calcule AOV projetado:

AOV = (% compra solo × preço solo)
    + (% compra 3-pack × preço 3-pack)
    + (% compra 6-pack × preço 6-pack)
    + (bump acceptance × preço bump)
    + (upsell acceptance × preço upsell)

Baseline mix (ajustar com data depois):
- 50% solo, 35% 3-pack, 15% 6-pack (mix típico com Popular destacado no 3-pack)

**Sanity de categoria (benchmarks 2026 — o AOV projetado deve cair numa faixa crível):**
- Beauty/personal care: AOV $55-137 (média global $74; impulso single-SKU $30-55, bundle de rotina $75-95, skincare premium com assinatura $100-137)
- Supplements: $45-65 transacional; bundle 90 dias $90-120 (billing trimestral triplica o AOV efetivo e derruba o payback do CAC de ~3 pedidos pra 1)
- Shopify DTC geral: $85-95 (top 20% acima de $120); CAC de referência nas duas categorias ≈ $61; margem bruta 60-70%; recompra 37.7% em supplements vs 25-30% em beauty

Se o AOV projetado ficar muito fora da faixa da categoria sem justificativa clara (posicionamento premium, bundle robusto), reveja o mix antes de prosseguir.

**Guardrail de canibalização de bundle (net AOV, não AOV bruto):**
- Desconto de 15% num bundle que sobe o AOV em 30% derruba a margem de contribuição em **6-7 pontos percentuais**, A MENOS que **mais de 20% dos pedidos do bundle sejam incrementais** (gente que não teria comprado o solo full-price). Sem histórico, assuma o cenário conservador (incrementalidade baixa) e avalie o bundle pela **margem de contribuição líquida**, nunca pelo AOV do painel.
- Net AOV: desconte devoluções — com 15% de returns, AOV $120 no painel é ~$102 real. Use o net nas projeções de PSM da ETAPA 7. Se a provisão de reembolso/chargeback já entrou como linha de custo no `cogs_breakdown` (item 8 da ETAPA 1), **não desconte de novo aqui** — a provisão conta uma vez só.

### ETAPA 7 — PSM Projetado (Profitable Scaling Margin)

Reavalie o PSM com o **AOV projetado da ETAPA 6** (pós bump/upsell) como LTV-proxy, pela MESMA fórmula da ETAPA 5 (a mesma que a skill 11 usa pro `psm_real`):

**Fórmula:** PSM = LTV / (CAC + COGS) — agora LTV = AOV projetado do primeiro pedido (ETAPA 6, ajustado pra net AOV se houver estimativa de devoluções), **CAC = teto de CAC 2× da ETAPA 5** (ou um CAC esperado de benchmark, se o membro tiver — custo por cliente NOVO, medido no Shopify com `new customer = TRUE`, nunca o CPA que o gerenciador de ads reporta; cânone §3), COGS = somatório de todos os itens do `cogs_breakdown` (igual à ETAPA 5 e à Skill 11). Se houver dado de recompra medido, use LTV com reorder ao longo de 30-60-90 dias — aí o LTV deixa de ser proxy do primeiro pedido, o PSM sobe e justifica um teto de CAC mais alto. Sem dado medido, o LTV permanece o do primeiro pedido: **recompra estimada não entra no PSM** (cânone §2 — a economia da recompra é outra tabela, não um multiplicador otimista nesta).

- **PSM < 1.0**: cada cliente perde dinheiro em escala — oferta NÃO viável
- **PSM 1.0–1.1**: breakeven, cresce devagar com risco
- **PSM 1.1–1.3**: escala estável, +5% por ciclo
- **PSM > 1.3**: escala agressiva viável

**No relatório (.md/.html), explique LTV e PSM como conceitos separados, em linguagem simples** — o membro confunde os dois. LTV é um valor em dinheiro (quanto um cliente rende ao longo do tempo; sem histórico, o proxy é o AOV projetado do primeiro pedido). PSM é uma razão: LTV dividido pelo custo de trazer e entregar o cliente (CAC + COGS) — acima de 1,0 o cliente rende mais do que custa; acima de 1,3 dá pra escalar forte. Mostre os dois números lado a lado (o LTV que alimenta o cálculo e o PSM resultante), nos cenários sem recompra e com recompra.

**No mesmo trecho do relatório, diga em uma frase por que o custo de aquisição usado aqui é o CAC e não o CPA do gerenciador**: o gerenciador conta como conversão a compra de quem já era cliente, então o custo por cliente NOVO (Shopify, `new customer = TRUE`) é sempre maior que o CPA reportado. É esse número maior que a oferta precisa aguentar.

Se PSM projetado < 1.1 — oferta **não sustenta escala lucrativa** com economics atuais. Sugira em ordem:
1. **Aumentar AOV** (primeira opção, sem arriscar volume):
   - Bundle (ex: 3-pack desconto 15%)
   - Upsell no checkout (complemento de $20-40 com margem alta)
   - Assinatura **sem desconto**: o preço de assinatura fica no preço-base e o one-time sobe ~15% (regra da ETAPA 3). Aumenta o LTV sem entregar margem em cada recompra
2. **Reduzir COGS** (fornecedor alternativo, negociar volume, frete agregado)
3. **Aumentar preço** (só se posicionamento competitivo permitir; re-validar pricing anchors)
4. **Pivotar oferta** — mudar mecanismo ou público-alvo
NUNCA "reduzir o teto de CAC magicamente"; o custo de aquisição é output de eficácia no leilão, não input — e abaixo de US$ 15–25 ele não existe (piso de CAC, ETAPA 5).

### ETAPA 8 — Simulação de Budget (2 níveis)

Simule a operação em DOIS níveis: o budget diário declarado do membro (do profile) E o dobro dele. O membro decide budget olhando cenários lado a lado, não um número isolado. Pra cada nível, com o CAC de referência (mediano da categoria, ou o CAC-alvo se o membro declarou um — custo por cliente NOVO, não CPA de plataforma; ver cânone §3):

**Antes de montar a tabela, pergunte uma coisa ao membro:** *"Quanto você tem de custo fixo por mês no negócio? (aluguel, salários, ferramentas, agência de valor fixo, contabilidade — tudo que você paga mesmo vendendo zero.)"* Se ele não souber ou não quiser informar, siga com a tabela mesmo assim e trate a ausência conforme a regra abaixo. Grave em `budget_viability.fixed_costs_monthly` (`null` quando não informado — nunca zero por omissão; zero só quando o membro declarar zero).

**Não pergunte o que já está gravado.** Se `15-finance-engine/dados.json.monthly_model.fixed_costs_monthly` existir (ou `manifest.fixed_costs_monthly` — é o mesmo campo canônico, compartilhado entre as skills 04, 11, 12 e 15), pré-popule dali e só confirme: *"seus custos fixos ainda são US$ X/mês?"*. Grave a origem em `budget_viability.fixed_costs_source`. Com o número na mesa, **as duas últimas linhas da tabela têm número** e `result_after_fixed_monthly` deixa de ser `null` nos dois cenários.

**Conferência contra o medido (só quando a 15 rodou):** compare a margem de contribuição % que esta simulação projeta com `monthly_model.contribution_margin_pct` da 15, que é a margem **medida** do negócio. Divergência grande é sinal de que uma das duas premissas está errada — quase sempre um custo variável que ficou fora do `cogs_breakdown`, ou um mix de bundle que na prática não aconteceu. Registre o número medido em `budget_viability.contribution_margin_pct_measured` e, se divergir, diga qual das duas o relatório está usando e por quê. **Sem a 15, a linha simplesmente não existe** e a projeção segue como hoje.

| Métrica | Budget declarado | 2× o budget |
|---|---|---|
| Clientes novos por dia (budget ÷ CAC) | ... | ... |
| Margem de contribuição por dia (clientes × margem de contribuição por pedido) | ... | ... |
| Investimento no mês (budget × 30) | ... | ... |
| Clientes novos no mês | ... | ... |
| **Margem de contribuição no mês** | ... | ... |
| Custos fixos no mês | ... | ... |
| **Resultado após custos fixos — é este o número que pode ser chamado de lucro** | ... | ... |

Os custos fixos são o MESMO valor nos dois níveis: eles não crescem porque o budget cresceu. É por isso que o nível 2× costuma melhorar o resultado mesmo com eficiência um pouco pior — mais volume dilui a mesma base fixa (cânone §4).

**Regra de rótulo (cânone §1 — inegociável):** margem de contribuição é receita menos custos variáveis. **Lucro é margem de contribuição menos custos fixos.** A palavra "lucro" só pode aparecer na última linha da tabela, e só quando os custos fixos foram informados. Isso vale na tabela, no texto do relatório, no `dados.json` e em qualquer mensagem ao membro.

**Quando os custos fixos NÃO forem conhecidos:** as duas últimas linhas ficam explicitamente sem número (não zere, não omita a linha, não deslize pra chamar a margem de "lucro"). O relatório diz a frase inteira, na cara: *"Margem de contribuição de US$ X por mês; sem os custos fixos informados não dá para dizer se há lucro."* Grave `result_after_fixed_monthly: null` no cenário correspondente.

**Três ressalvas obrigatórias junto da tabela** (senão a simulação engana): (1) o número simulado conta só a primeira compra — recompra soma por cima, com a economia melhor da tabela 5B; (2) **margem de contribuição não é lucro** — quando os fixos não estão na conta, o que a tabela mostra é o dinheiro que sobra ANTES de pagar a estrutura do negócio; (3) o CAC tende a subir conforme o investimento cresce, então o nível 2× é estimativa de mesma eficiência, não promessa.

Registre em `dados.json` → `budget_viability`: `cac_ref`, `fixed_costs_monthly` e `scenarios[]` (um objeto por nível: `daily_budget`, `new_customers_per_day`, `contribution_margin_per_day`, `monthly_spend`, `new_customers_per_month`, `contribution_margin_per_month`, `result_after_fixed_monthly`) + `caveats` + `verdict`. **Não existe campo com a palavra `profit` neste bloco** — o único número que mereceria o nome é `result_after_fixed_monthly`, e ele é `null` sempre que os fixos não foram informados.

Cruze com as projeções 30/60/90 com cash flow da Skill 12 — em qual patamar de receita mensal essa oferta coloca o membro em 30, 60 e 90 dias?

### ETAPA 9 — Validação Final (Sanity Checks)

Antes de salvar, responda HONESTAMENTE:

1. **A oferta faz sentido pro awareness level dominante?** (se é Problem Aware, a oferta foca em educação; se é Product Aware, foca em diferenciação; etc)
2. **O mecanismo é genuinamente diferente dos concorrentes?** (passa no filtro S.I.N. + não é commodity do estágio de sophistication)
3. **As economics permitem escalar?** (PSM > 1.1 — escala estável; teto de CAC viável com budget do membro)
4. **O stack de valor é convincente SEM inflar?** (cada bonus é real, útil, entregável — e cada item do stack passou na regra do `Not: "___"`: nenhum entregável aparece pela palavra de formato, todos aparecem pelo ativo nomeado)
5. **A garantia quebra a objeção de risco identificada no market research?** (não é genérica — ataca o medo específico do avatar)
6. **Pricing triangulado (as 3 âncoras convergem — `(máx−mín)/mediana ≤ 0.40`, régua da ETAPA 3)?**
7. **COGS breakdown completo (COGS entregue + frete + pick&pack + processamento de pagamento + taxas + app de assinatura quando há assinatura + fee de agência quando é % do spend + provisão de reembolso), sem valor agregado?**
8. **Margem de contribuição ≥ $20 em pelo menos uma variação do PRIMEIRO PEDIDO (tabela 5A)?** (senão o teto de CAC viável inviabiliza ads)

   > **Alternativa por payback medido (só para membro em `scaling`, só com LTV medido).** Perder no primeiro pedido é decisão, não acidente — desde que o cohort devolva o dinheiro dentro de uma janela conhecida e o caixa aguente a janela. Se `manifest.stage == "scaling"` **E** `15-finance-engine/dados.json` traz `payback.payback_window_days_measured ≤ 90` com `cohorts.decay_source: "calculated"` e `cohorts.calibrated: true` (LTV medido, não estimado), **o check 8 passa por essa via** mesmo com margem de contribuição do primeiro pedido abaixo de $20: o gate deixa de ser a margem por pedido e passa a ser a janela de payback. Grave `budget_viability.payback_window_days_measured` e marque o check como aprovado por payback, dizendo isso no relatório em uma frase (o membro precisa saber que a oferta se sustenta no segundo pedido, não no primeiro). A segunda condição do cânone é **caixa que aguenta a janela**, e ela agora é verificável aqui: leia `cash.runway_months` do mesmo arquivo (a 15 passou a publicá-lo no `handoff.for_skill_04`). Regra: `runway_months × 30 ≥ payback_window_days_measured` → as duas condições fechadas, o check passa por payback. Se `runway_months` for `null` (a 15 rodou em Modo A, sem caixa medido) ou menor que a janela, **o check NÃO passa por essa via** — volta a valer o gate de margem, e o relatório diz em uma frase que o payback fecha mas o caixa não sustenta a janela (a diferença importa: a oferta é boa, o financiamento dela é que falta).
   >
   > **As três condições são cumulativas e nenhuma se estima.** Faltando qualquer uma — a 15 não rodou, o cohort não está calibrado, o `decay_source` é `assumed`, ou o stage é `starter`/`validating` — **o gate de margem mínima vale integralmente, como hoje**. É o mesmo recorte que o cânone aplica: sem LTV medido e sem caixa pra bancar a janela, a economia do primeiro pedido é a única que decide.
9. **Bundle structure aumenta AOV sem canibalizar margem?** (rode o guardrail de net AOV da ETAPA 6: desconto que sobe AOV bruto mas derruba a margem de contribuição líquida reprova)
10. **breakeven_roas < 3.0?** (se > 3.0, a oferta depende de um custo de aquisição baixo demais pra ser realista — trate como falha do check e volte pra ETAPA 7: aumentar AOV, reduzir COGS ou repricing, antes de salvar)
11. **`04-offer-builder/research-foundation.json` existe e cobre todos os claims centrais do mecanismo com fonte rastreável?** (sem fundação de evidência, copy da Skill 06 sai sem lastro — bloqueante)
12. **O teto de CAC (2×) está acima do piso de US$ 25?** (piso físico de CAC no leilão: US$ 15–25, cânone §3. Teto abaixo disso exige um custo de aquisição que não existe em escala — bloqueante. Saídas, nesta ordem: subir AOV (ETAPA 6), subir preço (ETAPA 3), ou sustentar a conta com LTV de recompra **medido** — nunca estimado — e recalcular o PSM da ETAPA 7 com esse LTV real)

Registre o resultado em `04-offer-builder/dados.json` → `sanity_checks` como `{ "total": 12, "passed": N, "failed": [<números dos checks que falharam>] }` (NÃO um inteiro hard-coded). Se alguma resposta for "não", **itere antes de salvar**. Uma oferta fraca que passa adiante vira ad ruim, copy genérica, e membro frustrado em 30 dias.

**No relatório (.md/.html), as checagens aparecem como AFIRMAÇÕES do que está validado, com a evidência em 1 frase — nunca em formato de pergunta** (o formato de pergunta acima é ferramenta interna da skill; ver `.claude/rules/report-only-results.md`). Ex: "Margem de contribuição sustenta tráfego pago. X% por pedido no primeiro pedido; CAC de empate acima do mediano da categoria."

**Bloqueio de save (checks críticos):** se QUALQUER um dos checks críticos falhar — check 3 (economics/PSM viável), check 8 (margem de contribuição ≥ $20 em ao menos uma variação do primeiro pedido, **ou a alternativa por payback medido descrita nele**), check 11 (`04-offer-builder/research-foundation.json` cobre os claims centrais) ou check 12 (teto de CAC acima do piso de US$ 25) — NÃO salve o `04-offer-builder/dados.json` final. Itere até passar, ou aplique o escape-path correspondente (ES1 pra foundation faltante; ETAPA 7 pra economics; ETAPA 1 sanity de margem; ETAPAs 3/6 pra teto de CAC abaixo do piso). Os demais checks que falharem entram em `failed[]` como aviso, mas não bloqueiam.

### Output Schema — `04-offer-builder/offer-builder.md` + `04-offer-builder/dados.json`

O markdown é humano; o JSON é para as skills 06/07/10/11/12. Estrutura obrigatória:

`.json`:
```json
{
  "offer_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "mechanism": {
    "name": "...",
    "ump": { "name": "nome próprio do mecanismo do problema", "logic": "por que as soluções atuais falham (report_language; cita claim_ids da research foundation)" },
    "ums": { "name": "nome próprio do mecanismo da solução", "logic": "por que a nossa entrega funciona (report_language; cita claim_ids)" },
    "sin_score": { "simplicity": 9, "intuitiveness": 8, "novelty": 7 },
    "validation_source": "improved_validated|crossed_validated|original",
    "copy_left_to_skill_06": true
  },
  "pricing": {
    "main_sku_price": 97.00,
    "aov_expected": 118.00,
    "currency": "USD"
  },
  "subscription_architecture": "subscription_first | onetime_plus_sub_no_reorder | no_subscription",
  "onetime_premium_pct": 15,
  "sub_discount_pct": 0,
  "cogs_breakdown": {
    "product_delivered": 18.00,
    "shipping_to_customer": 6.50,
    "pick_pack": 2.50,
    "payment_processing": 3.50,
    "taxes_and_duties": 1.50,
    "subscription_app_fee": 0.90,
    "agency_fee_variable": 0.00,
    "refund_chargeback_provision": 2.10
  },
  "unit_economics": {
    "basis": "first_order",
    "cac_basis": "shopify_new_customer",
    "margin_per_unit": 58.50,
    "weighted_margin_per_order": 72.00,
    "contribution_margin_pct": 61.0,
    "breakeven_cpa": 72.00,
    "breakeven_roas": 1.64,
    "target_cpa_for_2x": 36.00,
    "target_cpa_for_3x": 24.00,
    "target_cpa_primary_2x": 36.00,
    "target_cpa_primary_3x": 24.00,
    "psm_theoretical": 1.44,
    "repeat_order": {
      "aov": 97.00,
      "variable_costs_total": 32.00,
      "contribution_margin_per_order": 65.00,
      "contribution_margin_pct": 67.0
    },
    "aov_blended": 108.00
  },
  "guarantee": { "type": "...", "duration_days": 30 },
  "offer_stack": "Main product ($97 value) + Bonus 01 ($49 value) + Bonus 02 ($39 value) + Bonus 03 ($29 value) = $214 total value. Today: $97 (you save $117).",
  "aov_levers": {
    "bump": { "name": "...", "price": 14.00, "copy": "1 frase + 1 benefício (inglês US, ad-safe)", "take_projected": 0.20 },
    "upsell": { "name": "...", "price": 67.00, "anchor_was": 97.00, "oto_structure": "more_of_same | next_thing | do_it_faster | need_help", "take_projected": 0.08 },
    "bundles": [
      { "qty": 1, "price": 97.00, "label": "Solo", "savings_pct": 0 },
      { "qty": 3, "price": 197.00, "label": "Popular", "savings_pct": 32 },
      { "qty": 6, "price": 327.00, "label": "Best Value", "savings_pct": 44 }
    ]
  },
  "bonuses": [
    {
      "id": "bonus-01",
      "name": "o ativo nomeado (regra do Not: \"___\", ETAPA 3) — nunca a palavra de formato",
      "description": "o que é / por que vale",
      "value_anchored": 49,
      "type": "gift_with_purchase | free_complementary_sku | free_ebook | gift_wrapping | digital_guide | discount_code | workbook | checklist | community_access | video_series | consultation_call | trial_extension",
      "format_hint": "in_box | shopify_function | gift_app | pdf | notion | figma | wistia | klaviyo_email | shopify_discount | circle_invite",
      "condition": "unconditional | cart_threshold | tier_specific",
      "delivery_trigger": "post_purchase | on_signup | day_7_post_purchase | on_first_reorder"
    }
  ],
  "budget_viability": {
    "cac_ref": 45.00,
    "fixed_costs_monthly": null,
    "fixed_costs_source": "member | manifest | 15-finance-engine | unknown",
    "contribution_margin_pct_measured": null,
    "payback_window_days_measured": null,
    "scenarios": [
      { "daily_budget": 50, "new_customers_per_day": 1.1, "contribution_margin_per_day": 12.00, "monthly_spend": 1500, "new_customers_per_month": 33, "contribution_margin_per_month": 360, "result_after_fixed_monthly": null },
      { "daily_budget": 100, "new_customers_per_day": 2.2, "contribution_margin_per_day": 24.00, "monthly_spend": 3000, "new_customers_per_month": 66, "contribution_margin_per_month": 720, "result_after_fixed_monthly": null }
    ],
    "caveats": "margem de contribuição não é lucro (custos fixos não informados, portanto não descontados); conta só a 1ª compra; CAC tende a subir com o investimento (2× = estimativa de mesma eficiência)",
    "verdict": "..."
  },
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

> **Os números do exemplo acima são ILUSTRATIVOS e independentes entre si** — servem pra mostrar o formato de cada campo, não pra compor um caso econômico coerente único. Não re-derive um campo a partir de outro usando os valores do exemplo; as fórmulas canônicas estão na "Nota sobre nomenclatura" abaixo e nas ETAPAs 5-7. (`onetime_premium_pct` só existe quando `subscription_architecture` ≠ `no_subscription`; `repeat_order` é `null` quando o produto não tem recompra prevista, e `aov_blended` só existe quando `repeat_order` existe.)

**Campos de economia unitária — o que cada um significa (cânone: `.claude/lib/unit-economics/README.md`):**
- `cogs_breakdown` traz o stack de custos variáveis item a item (§1). **Todo campo do bloco é valor em dinheiro POR PEDIDO, nunca percentual solto** — a Skill 11 SOMA os valores deste bloco pra obter o COGS canônico, e um percentual no meio da soma corromperia o número. Fee que nasce como % (pagamento, app de assinatura, agência) entra aqui já convertido pro valor do pedido médio. `subscription_app_fee` = 0 quando não há assinatura; `agency_fee_variable` = 0 quando a agência cobra valor fixo (aí ela é custo FIXO e vai em `budget_viability.fixed_costs_monthly`) ou quando não há agência. **Ad spend nunca entra aqui** — ele é o CAC do PSM.
- `unit_economics.basis: "first_order"` declara que todos os campos canônicos do bloco (margem, breakeven, tetos de CAC, PSM, `contribution_margin_pct`) são do PRIMEIRO PEDIDO. A economia da recompra vive só em `repeat_order` — com o próprio `contribution_margin_pct` dela —, e nenhum derivado de mídia sai de lá (§2).
- `unit_economics.cac_basis: "shopify_new_customer"` declara que o custo de aquisição do modelo é CAC por cliente novo medido no Shopify (`new customer = TRUE`), não o CPA que a plataforma de ads reporta (§3). Os campos mantêm o nome `*_cpa_*` por contrato com as skills 07d/10/11 — o nome é legado, o conteúdo é CAC.
- `budget_viability` não tem nenhum campo chamado "profit". `contribution_margin_per_day/month` é margem de contribuição; `result_after_fixed_monthly` é o único número que pode ser chamado de lucro, e é `null` enquanto `fixed_costs_monthly` for `null` (§1).
- `contribution_margin_pct_measured` e `payback_window_days_measured` são **cópias** do `15-finance-engine/dados.json` (`monthly_model.contribution_margin_pct` e `payback.payback_window_days_measured`) — esta skill lê, nunca calcula nem estima. Ficam `null` quando a 15 não rodou, e nesse estado a ETAPA 8 e o check 8 operam exatamente como antes. `fixed_costs_source` registra de onde veio o número dos fixos.

Atualizar `manifest.json`: adicionar `target_cpa`, `breakeven_roas`, `psm_theoretical`, adicionar skill em `skills_completed`.

Depois de atualizar o manifest, regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza o `ABRIR-AQUI.html`).

**Nota sobre nomenclatura dos unit_economics** — `weighted_margin_per_order` é o denominador de margem CANÔNICO de toda a unit economics. TODOS os derivados saem dele, NÃO de `margin_per_unit`:
- `breakeven_cpa` = `weighted_margin_per_order`
- `target_cpa_primary_2x` = `weighted_margin_per_order / 2`
- `target_cpa_primary_3x` = `weighted_margin_per_order / 3`
- `breakeven_roas` = `aov_expected / weighted_margin_per_order`
- Sanidade: `target_cpa_primary_2x` < `breakeven_cpa` SEMPRE.

No exemplo acima: weighted_margin_per_order 72 → breakeven_cpa 72, target_2x 36 (72/2), target_3x 24 (72/3), breakeven_roas 1.64 (118/72), psm_theoretical 1.44 (118/(36+46), COGS = somatório do breakdown). A Skill 11 (ad-analysis) lê por esses nomes "primary"/"weighted" e assume esse denominador único. Os campos legacy (`margin_per_unit`, `target_cpa_for_2x/3x`, `sub_discount_pct`) são emitidos em paralelo só por compat — `sub_discount_pct` sai SEMPRE `0` desde a inversão do desconto de assinatura (ETAPA 3); o número vivo é `onetime_premium_pct`. `weighted_margin_per_order` = margem média ponderada por AOV (considera bumps + upsells); `margin_per_unit` é a margem unitária do SKU principal. Se a oferta não tem bump/upsell, os dois valores são iguais — mas os derivados de CPA sempre referenciam `weighted_margin_per_order`. `offer_stack` é a string pré-montada que a Skill 06 consome literal em copy de página/ad — é copy pública: SEMPRE inglês US (é estrutura de oferta com valores, não copy de mecanismo — a copy do mecanismo nasce inteira na Skill 06 a partir de `ump`/`ums`).

**Enum canônico de `bonuses[]`:** os valores de `type`, `format_hint`, `condition` e `delivery_trigger` do schema acima são o enum ÚNICO do framework — reproduzidos idênticos na ETAPA 3 desta skill e no pré-flight da Skill 05. Não criar valores fora dessa lista.

**Bloco `aov_levers` (contrato machine-readable com a 07d):** espelha ESTRUTURADO o que a ETAPA 3 define em prosa — bump (nome, preço, copy curta, take projetado), upsell (nome, preço, âncora "was", estrutura de OTO, take projetado) e os tiers de bundle (`{qty, price, label, savings_pct}`). A Skill 07d lê DAQUI na ETAPA 1 dela (fim do parsing de prosa; a prosa da ETAPA 3 continua sendo a versão humana). Alavanca que a oferta não tem = campo `null` (ex: oferta sem upsell → `"upsell": null`) — a 07d registra como `not_in_offer`, nunca inventa. `take_projected` em fração (0.20 = 20%), consistente com as taxas conservadoras da ETAPA 3. `copy` do bump é consumidor-final: inglês US, ad-safe (rule 8b).

**Se `04-offer-builder/dados.json` falhar validação, NÃO salvar `.md`.**

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer-builder/offer-builder.md` → `04-offer-builder/offer-builder.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).


`workspace/[produto]/04-offer-builder/offer-builder.md` contendo:
1. Mecanismo único recomendado — a LÓGICA de UMP e UMS com nomes e estudos citados (Etapa 2D; sem versões de copy)
2. **Research Foundation** (Etapa 2.5) — evidências que sustentam o mecanismo, com fontes rastreáveis
3. Estrutura de oferta completa (produto principal, bundles, arquitetura de assinatura se consumível, bump, upsell, stack de valor)
4. Garantia recomendada + copy
5. Unit economics em DUAS tabelas separadas — primeiro pedido (5A) e recompra (5B) — mais o AOV blended quando as duas existem (Etapa 5). Nenhum número desta seção é chamado de "lucro"
6. AOV projetado (Etapa 6)
7. LTV e PSM explicados como conceitos separados + PSM projetado, com a frase que separa CAC de CPA (Etapa 7)
8. Simulação de budget em 2 níveis, com margem de contribuição e resultado após custos fixos como linhas distintas (Etapa 8)
9. Checagens de sanidade como afirmações do que está validado (Etapa 9)

O doc segue `.claude/rules/report-only-results.md`: só o resultado — sem narração de processo, sem descrição de ausências, sem referência à conversa.

Também salvar companion `04-offer-builder/research-foundation.json` conforme schema da Etapa 2.5.

## Mensagem Final

"Primeira versão da oferta pronta. Mecanismo único: **[Nome do Mecanismo]** (rota: [recombinação validada / criação original]). PSM projetado: [valor]. Viável pro seu budget: [sim/com ajustes].

Margem de contribuição por pedido: [valor] — é o que sobra depois dos custos variáveis. [SE os custos fixos não foram informados: "Sem os seus custos fixos mensais na conta, não dá pra dizer se há lucro; me passa esse número quando tiver e eu fecho a simulação."]

Revisa antes de seguir: o nome do mecanismo gruda? O pricing e o stack fazem sentido pro seu avatar? A garantia ataca o medo certo? Me diz o que não fecha e eu itero.

Quando fechar: diga **'copy'** pra escrever a copy completa da página aplicando o mecanismo, stack, garantia, e linguagem do market research."

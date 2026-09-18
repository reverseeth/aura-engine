# Page Design · Referência: PLAN e a escolha do page_type pelos três sinais (ETAPA 1, sub-etapa 1.1)

> Os três sinais do `page_type` (consciência dominante, tipo de abertura da copy, formato que os concorrentes escalados usam), as famílias de formato e o que fazer quando o terceiro sinal diverge, a tabela awareness → page_type com os cinco formatos que ela decide e o quiz à parte, o tie-break sintático e a página híbrida, o destino obrigatório do soft CTA do advertorial e do listicle (`destination_ref`), o mapa canônico 1:1 das 7 seções da copy e os frameworks que sustentam a decisão. Abra na sub-etapa 1.1.

## ETAPA 1 — PLAN (estratégia + plano de sections)

A página NÃO tem estrutura fixa. Cada produto merece um plano que reflita sua estratégia. A skill `copy-engine` já tomou essas decisões — respeite-as.

### 1.1 Detectar `page_type` — três sinais, nesta ordem de peso

O `page_type` sai de três sinais, e o peso é o da ordem em que aparecem:

1. **Consciência dominante do mercado** — `dominant_awareness` de `market-research/dados.json`, pela tabela abaixo.
2. **Tipo de abertura da copy** — o campo top-level `lead_type` de `copy-engine/dados.json` (a `copy-engine` grava na ETAPA 2 dela; é o contrato machine-readable entre as duas skills). `story`, `big_idea` e `problem_agitation` casam com `advertorial` e `listicle`; `mechanism`, `secret` e `proclamation` casam com `landing`; `offer` e `direct` casam com `pdp_robust` e `pdp_lean`. `lead_type` ausente (produto de versão antiga): siga só pelo awareness e anote a lacuna.
3. **Formato que os concorrentes escalados de fato usam** — `dominant_landing_format` do `resumo` de `competitor-analysis/dados.json`, com o detalhe por página em `landing_formats[]` (URL, formato, quantos ads caem nela). É o sinal do dinheiro que já está rodando no nicho, e por isso entra na decisão; mas ele nunca decide sozinho.

**Famílias de formato.** Os três sinais só são comparáveis depois de agrupados: `advertorial` e `listicle` são a família do pré-lander editorial (educa primeiro, fecha em outra página); `landing` e `vsl` são a família da página de venda dedicada; `pdp_robust` e `pdp_lean` são a família da página de produto; `quiz` é família própria. `home` não é família nenhuma: ad que cai na página inicial do concorrente é ausência de página dedicada, e esse sinal é descartado.

**O que fazer com o terceiro sinal:**

| Situação | O que a skill faz |
|---|---|
| Os três sinais na mesma família e na mesma variante | Decide, segue, e diz o `page_type` ao membro em uma frase |
| Terceiro sinal na mesma família, variante diferente (`advertorial` contra `listicle`, `pdp_robust` contra `pdp_lean`) | Adota a variante do concorrente e informa em uma linha, com o número de ads que a sustenta. Não pergunta: a estratégia da página não muda, muda o tratamento |
| Terceiro sinal em outra família | Mostra a divergência em duas linhas, com o número de ads que sustenta o formato do concorrente, e o membro decide |
| `dominant_landing_format` é `null`, ou a `competitor-analysis` não rodou | Decide pelos dois primeiros sinais, sem mencionar o terceiro |
| O formato dominante é `vsl` | A página que a Aura produz mais próxima é a `landing` com hero de vídeo e a section `video-demo` no plano. Se os dois primeiros sinais também apontam `landing`, siga assim; se apontam outra família, mostre a divergência |

**Nunca troque o `page_type` só pelo sinal do concorrente sem mostrar.** Divergência de família sempre passa pelo membro, e a pergunta cabe em duas linhas: qual formato os dois primeiros sinais pedem, qual o concorrente roda e com quantos ads.

A divergência é mostrada assim:

> "A consciência do mercado e a abertura da copy pedem uma `landing`. Os concorrentes escalados mandam o tráfego pra advertorial: 14 dos 19 ads escalados caem em página de matéria.
> Sigo com a landing ou vou de advertorial?"

`quiz` não sai da consciência dominante nem do lead da copy: ele chega pelo formato do concorrente ou por pedido direto do membro. Nos dois casos quem decide é ele, e a decisão fica registrada como `page_type_signals.resolved_by: "member"`. O quiz serve quando o avatar se divide em perfis com necessidades diferentes e a recomendação certa depende da resposta do visitante — responder já compromete a pessoa com o resultado. Estrutura típica: abertura com a promessa do resultado → perguntas com ramificação → tela de leitura do resultado → resultado por perfil → oferta ancorada no resultado.

**Página híbrida:** `dominant_awareness_secondary` presente no `dados.json` da `market-research` (empate de até 5 pontos percentuais) significa página híbrida: grave `hybrid: true` no bloco strategy do `page-plan.json` e escolha o page_type que serve os dois níveis. Na dúvida, o do nível de MENOR consciência — página que educa converte os dois; página que assume conhecimento perde quem sabe menos.

| Awareness (Schwartz) | page_type | Lógica | Estrutura típica |
|---|---|---|---|
| **Problem-Aware** (ou Unaware aquecido pra problem) | `advertorial` | Mercado sente a dor mas não conhece a solução — precisa de narrativa editorial que educa antes de vender | hook → problem → agitation → mechanism → proof → soft CTA → FAQ (7-section blueprint) |
| **Problem-Aware**, com `sophistication_stage` 4 ou 5, ou com o formato do concorrente em listicle | `listicle` | Mesma consciência do advertorial, leitor que já leu a história longa de todo mundo e agora varre: a lista numerada entrega a mesma educação em blocos curtos | hook → promessa da lista → itens numerados (subtítulo, prova e micro-argumento em cada) → o item que apresenta o produto → soft CTA → FAQ |
| **Solution-Aware** | `landing` | Conhece o tipo de solução, não a sua marca — precisa de persuasão NESP focada em diferenciação | hero benefit + CTA → proof → mechanism → offer → guarantee → faq → cta-final |
| **Product-Aware** | `pdp_robust` | Conhece seu produto, compara — precisa de PDP completa que vence objeções e ancora valor | hero → benefits → mechanism → social-proof → comparison → offer → guarantee → faq → cta-final |
| **Most-Aware** | `pdp_lean` | Só precisa do empurrão final (preço/oferta/urgência) | hero curto → offer → proof condensada → guarantee → cta-final |

**Tie-break sintático** (só se awareness ambíguo entre dois níveis): copy abre com narrativa "I used to..." / "Doctor reveals..." e sem CTA no topo → puxa pra `advertorial` (ou `listicle`, se o corpo já vem em itens numerados); copy abre com pricing tiers/bundles explícitos no topo → puxa pra `landing`/`pdp`. Hybrid (narrativa abrindo + offer stack convergindo nos últimos 40%) é válido — marque `page_type` como o dominante e anote `hybrid: true` no strategy.

**Se `page_type = advertorial` ou `listicle` — defina o DESTINO do soft CTA (obrigatório):** os dois são pré-lander e não fecham a venda sozinhos; o soft CTA precisa apontar pra uma página que fecha. Pergunte ao membro e registre a escolha em `page-plan.json.destination_ref`:
- **(a) Rodar a cadeia `page-design`→`page-build` uma SEGUNDA vez** pra gerar a página de fechamento (`pdp_lean` com a oferta da `offer-builder`) — recomendado quando não existe PDP trabalhada;
- **(b) PDP existente da loja** — só se a copy/oferta dela já foram trabalhadas (apontar pra PDP default do tema quebra a congruência exigida na 3.7);
- **(c) Checkout direto** com a oferta da `offer-builder` (produto simples, membro quer funil curto).

A `page-build` usa `destination_ref` pra linkar o soft CTA. Sem destino definido, a página vai ao ar mandando tráfego pago pra uma página sem copy nem oferta — NÃO pule esta decisão. Nos demais page_types, `destination_ref` fica `null`.

**Se `page_type = advertorial` ou `listicle` — mapa canônico copy→sections (estrutura da masterclass interna):** a skill `copy-engine` grava a copy do advertorial com 7 seções canônicas de heading fixo. O `sections_plan` NÃO usa o menu genérico da 1.2 cru — a espinha é este mapa 1:1 (não improvise ids; a `page-build` splita por eles):

| Seção canônica da copy (`copy-engine`) | `sections_plan[].id` | Papel na página |
|---|---|---|
| `## Advertorial Headline` | `hero` | headline editorial + dek — **sem CTA no topo** (é editorial, não landing) |
| `## Lead` | `lead` | abertura da história (relato em primeira pessoa / cena que fisga) |
| `## Background Story` | `background-story` | contexto do protagonista, a luta antes da descoberta |
| `## Root Cause` | `root-cause` | a causa raiz do problema que ninguém contou pro leitor |
| `## Mechanism Reveal` | `mechanism-reveal` | a virada: o mecanismo que ataca a causa raiz |
| `## Product Build-Up` | `product-buildup` | do mecanismo ao produto — prova, credibilidade, especificidade |
| `## Reveal + Close` | `reveal-close` | revelação do produto + **soft CTA apontando pro `destination_ref`** |

Sections opcionais podem entrar DEPOIS da espinha (ex: `social-proof` se a copy tem depoimentos, `faq` se há objeções mapeadas) — nunca no meio da narrativa, que quebra o ritmo editorial. Se alguma das 7 seções não existir no `copy-engine.md` do produto, PARE e avise o membro: o advertorial da `copy-engine` está incompleto — rode a `copy-engine` de novo antes de desenhar a página (não invente a seção faltante).

O `listicle` usa o MESMO mapa: a copy é a mesma, o que muda é o tratamento. `background-story`, `root-cause`, `mechanism-reveal` e `product-buildup` viram os itens numerados da lista, cada um com o próprio subtítulo e a própria prova, e o `hero` anuncia quantos itens vêm ("7 razões..."). Nada de reescrever a copy pra caber na lista: quem decide o conteúdo é a `copy-engine`.

**Se `page_type = quiz`:** a 1.2 (menu de sections) dá lugar à sub-etapa 1.7, em `reference/quiz-funnel.md` — o funil inteiro: abertura, perguntas com a que roteia, ramificação, leitura do resultado, um perfil de resultado por sub-avatar e a oferta ancorada nele. O mapa de telas vive no bloco `quiz` do `page-plan.json`; o `sections_plan` continua sendo a lista de sections do split e tem a entry `quiz`, que é o funil inteiro numa section só. O fechamento acontece na própria tela de resultado, então `destination_ref` fica `null`.

**Frameworks que sustentam essa decisão** (puxe os nomeados, não query genérica):
- **Schwartz 5 Stages of Awareness** (rode `Schwartz five stages of awareness unaware problem aware solution aware product aware most aware`) + **Schwartz 5 Stages of Market Sophistication** (rode `market sophistication five stages Schwartz mechanism claim escalation jaded market`) — confirme que o awareness lido da `market-research` casa com o lead type da `copy-engine`.
- Se `page_type = advertorial` ou `listicle`: **Advertorial / Editorial-Look Principle** (rode `advertorial editorial look principle 5x readership Halbert Kennedy native ad`) + **Listicle Advertorials (2 Types)** (rode `listicle advertorial product-focused education-focused types awareness bridge`) pra escolher product-focused vs education-focused (é esse framework que rege o `listicle`), e **PCPO body copy** (rode `PCPO problem cure proof offer body copy framework web page`) pra estruturar o corpo editorial (Problem → Cure → Proof → Offer).
- Se `page_type = landing`: **NESP** (já puxado na 0.1) dirige a diferenciação Solution-Aware.
- Se `page_type = pdp_robust/pdp_lean`: **AOV Builders** (rode `checkout optimization AOV order bump upsell gift with purchase bundle threshold money close`) informam a ancoragem de oferta — note que a execução de bump/upsell vive na `checkout-aov`, aqui só dimensiona a section de oferta.

Confirme o `page_type` detectado com o membro antes de prosseguir (1 frase + a lógica; duas linhas quando o terceiro sinal diverge de família). Grave os três sinais e como a divergência se resolveu em `page-plan.json.strategy.page_type_signals` — é o que permite auditar depois por que a página tem o formato que tem.

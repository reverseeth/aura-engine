# Page Design · Referência: PLAN e a escolha do page_type pelo awareness (ETAPA 1, sub-etapa 1.1)

> A tabela awareness → page_type, o contrato com o `lead_type` da `copy-engine`, o tie-break sintático e a página híbrida, o destino obrigatório do soft CTA do advertorial (`destination_ref`), o mapa canônico 1:1 das 7 seções da copy do advertorial e os frameworks que sustentam a decisão. Abra na sub-etapa 1.1.

## ETAPA 1 — PLAN (estratégia + plano de sections)

A página NÃO tem estrutura fixa. Cada produto merece um plano que reflita sua estratégia. A skill `copy-engine` já tomou essas decisões — respeite-as.

### 1.1 Detectar `page_type` — PRIMARIAMENTE pelo awareness (Schwartz)

O `page_type` é decidido pelo **awareness level** lido de `market-research/dados.json` (campo `dominant_awareness`) e confirmado pelo campo **top-level `lead_type`** de `copy-engine/dados.json` (a `copy-engine` grava esse campo na ETAPA 2 dela — é o contrato machine-readable entre as duas skills). Confirmação: lead `story`/`big_idea`/`problem_agitation` casa com `advertorial`; `mechanism`/`secret`/`proclamation` casa com `landing`; `offer`/`direct` casa com `pdp_robust`/`pdp_lean`. Se `lead_type` estiver ausente (dados.json de produto legado), siga só pelo awareness e anote a lacuna. Heurística sintática é só **tie-break**. Se `dominant_awareness_secondary` presente no dados.json da `market-research` (empate ±5pp), trate a página como híbrida: grave `hybrid: true` no bloco strategy do `page-plan.json` e escolha o page_type que serve os dois níveis (na dúvida, o do nível de menor awareness — página que educa converte os dois; página que assume conhecimento perde o menos consciente).

| Awareness (Schwartz) | page_type | Lógica | Estrutura típica |
|---|---|---|---|
| **Problem-Aware** (ou Unaware aquecido pra problem) | `advertorial` | Mercado sente a dor mas não conhece a solução — precisa de narrativa editorial que educa antes de vender | hook → problem → agitation → mechanism → proof → soft CTA → FAQ (7-section blueprint, listicle) |
| **Solution-Aware** | `landing` | Conhece o tipo de solução, não a sua marca — precisa de persuasão NESP focada em diferenciação | hero benefit + CTA → proof → mechanism → offer → guarantee → faq → cta-final |
| **Product-Aware** | `pdp_robust` | Conhece seu produto, compara — precisa de PDP completa que vence objeções e ancora valor | hero → benefits → mechanism → social-proof → comparison → offer → guarantee → faq → cta-final |
| **Most-Aware** | `pdp_lean` | Só precisa do empurrão final (preço/oferta/urgência) | hero curto → offer → proof condensada → guarantee → cta-final |

**Tie-break sintático** (só se awareness ambíguo entre dois níveis): copy abre com narrativa "I used to..." / "Doctor reveals..." e sem CTA no topo → puxa pra `advertorial`; copy abre com pricing tiers/bundles explícitos no topo → puxa pra `landing`/`pdp`. Hybrid (narrativa abrindo + offer stack convergindo nos últimos 40%) é válido — marque `page_type` como o dominante e anote `hybrid: true` no strategy.

**Se `page_type = advertorial` — defina o DESTINO do soft CTA (obrigatório):** advertorial é pré-lander, não fecha a venda sozinho; o soft CTA precisa apontar pra uma página que fecha. Pergunte ao membro e registre a escolha em `page-plan.json.destination_ref`:
- **(a) Rodar a cadeia `page-design`→`page-build` uma SEGUNDA vez** pra gerar a página de fechamento (`pdp_lean` com a oferta da `offer-builder`) — recomendado quando não existe PDP trabalhada;
- **(b) PDP existente da loja** — só se a copy/oferta dela já foram trabalhadas (apontar pra PDP default do tema quebra a congruência exigida na 3.7);
- **(c) Checkout direto** com a oferta da `offer-builder` (produto simples, membro quer funil curto).

A `page-build` usa `destination_ref` pra linkar o soft CTA. Sem destino definido, o advertorial vai ao ar mandando tráfego pago pra uma página sem copy nem oferta — NÃO pule esta decisão.

**Se `page_type = advertorial` — mapa canônico copy→sections (estrutura da masterclass interna):** a skill `copy-engine` grava a copy do advertorial com 7 seções canônicas de heading fixo. O `sections_plan` de um advertorial NÃO usa o menu genérico da 1.2 cru — a espinha é este mapa 1:1 (não improvise ids; a `page-build` splita por eles):

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

**Frameworks que sustentam essa decisão** (puxe os nomeados, não query genérica):
- **Schwartz 5 Stages of Awareness** (rode `Schwartz five stages of awareness unaware problem aware solution aware product aware most aware`) + **Schwartz 5 Stages of Market Sophistication** (rode `market sophistication five stages Schwartz mechanism claim escalation jaded market`) — confirme que o awareness lido de `02` casa com o lead type de `06`.
- Se `page_type = advertorial`: **Advertorial / Editorial-Look Principle** (rode `advertorial editorial look principle 5x readership Halbert Kennedy native ad`) + **Listicle Advertorials (2 Types)** (rode `listicle advertorial product-focused education-focused types awareness bridge`) pra escolher product-focused vs education-focused, e **PCPO body copy** (rode `PCPO problem cure proof offer body copy framework web page`) pra estruturar o corpo editorial (Problem → Cure → Proof → Offer).
- Se `page_type = landing`: **NESP** (já puxado na 0.1) dirige a diferenciação Solution-Aware.
- Se `page_type = pdp_robust/pdp_lean`: **AOV Builders** (rode `checkout optimization AOV order bump upsell gift with purchase bundle threshold money close`) informam a ancoragem de oferta — note que a execução de bump/upsell vive na `checkout-aov`, aqui só dimensiona a section de oferta.

Confirme o `page_type` detectado com o membro antes de prosseguir (1 frase + a lógica).

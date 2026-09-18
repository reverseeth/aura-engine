# Page Design · Referência: Escolha da fonte de design, rotas viáveis e menu ao membro (ETAPA 3, sub-etapas 3.1 e 3.2)

> A detecção em runtime das cinco rotas, a tabela completa do menu (como funciona, qualidade, custo, automação, quando usar), a pergunta ao membro, o default sugerido sem imposição e as notas sobre Sidekick e prontidão pra IA de busca. Abra nas sub-etapas 3.1 e 3.2.

## ETAPA 3 — ESCOLHA DA FONTE DE DESIGN (o membro escolhe a rota)

Aqui o design nasce. A causa raiz de página "horrível" é gerar do zero sem referência concreta: sai genérico. Por isso a `page-design` NÃO escolhe a rota por você. Ela **apresenta as opções e o MEMBRO escolhe.** Todas as rotas convergem pro MESMO arquivo: `workspace/[produto]/page/design/page.html` — a **FONTE ÚNICA DE VERDADE visual**, aprovada pelo membro antes de qualquer Liquid existir. O resto da skill (tokens, plan, `page-build`) segue idêntico, independente da rota escolhida.

### 3.1 Detectar rotas viáveis (runtime)

Antes de apresentar o menu, detecte o que está disponível NESTA sessão e só ofereça as rotas viáveis:

| Rota | Disponível quando |
|---|---|
| **1. Clone-and-adapt** | `tools/design-clone/` existe no repo (sempre presente no framework). O membro precisa ter uma URL de concorrente cuja página ele ache boa (ou um .html da página salvo com a extensão SingleFile — ver degrau 4 da cascade na §3.3). |
| **2. Claude Design (handoff)** | Sempre ofertável — depende só do membro ter acesso ao canvas do `claude.ai/design` (Claude Pro/Max). Não há tool a detectar; é um handoff manual de arquivo. |
| **3. AIDesigner MCP** | Há tools com prefixo `mcp__aidesigner__` na sessão. Se ausente, NÃO liste como rota ativa — mencione em 1 linha "rota paga opcional, conecte o MCP se quiser" e siga. |
| **4. frontend-design (fallback)** | Sempre disponível (skill nativa). É a rota de menor qualidade — só quando o membro não tem referência nem quer desenhar. |
| **5. AI site-builders (v0 / Lovable / Manus)** | Rota EXTERNA — só entra no menu se o membro mencionar que usa algum deles (não ofereça espontaneamente). O membro descreve a página num desses geradores, eles criam o HTML. Ponto de atenção: trazem **runtime próprio** (stack/hospedagem deles), não Liquid nativo do Shopify — então serve como landing externa OU o membro exporta o HTML e a `page-build` reintegra ao tema. |

> Refero (`mcp__refero__`), se presente, já foi usado na ETAPA 2 pra brand signals — NÃO é uma rota de design de página aqui, é fonte de signals que alimenta qualquer rota.

### 3.2 Apresentar o menu ao membro (no `report_language`)

Mostre esta tabela (traduzida pro idioma do membro, listando só as rotas viáveis da 3.1):

| Rota | Como funciona | Qualidade de design | Custo | Automação | Quando usar |
|---|---|---|---|---|---|
| **1. Clone-and-adapt** *(padrão recomendado p/ velocidade)* | Você indica 1 PDP/landing de concorrente que acha bonita. A Aura captura só a **estrutura/layout** dela e adapta com a SUA copy (`copy-engine`), oferta (`offer-builder`) e imagens. Herda hierarquia e fluxo de conversão já validados no mercado. | Alta — parte de um layout que já converte | Zero | Alta | Você viu uma página de concorrente que funciona e quer velocidade sem reinventar layout |
| **2. Claude Design (handoff)** | Você desenha/itera a página no canvas visual do `claude.ai/design`, exporta como HTML standalone, e cola o arquivo aqui. A Aura consome esse HTML como `page.html`. | Alta — controle visual fino, aprovação no canvas | Incluso no Claude Pro/Max (consome mais token, mesmo limite) | Média (design semi-manual no canvas — isso é feature: você aprova visualmente antes do Liquid) | Você quer controle visual total e gosta de iterar num canvas |
| **3. AIDesigner MCP** *(se conectado)* | Roda dentro do Claude Code injetando padrões de design premium; cospe HTML/CSS limpo direto como `page.html`. | Alta | ~$20/mês (MCP pago) | Alta | Você já tem o MCP e quer design premium automatizado sem sair do Claude Code |
| **4. frontend-design** *(fallback)* | Gera a página via skill nativa, **com direção forte** (brand-signals da ETAPA 2 + referência concreta + estilo nomeado). | A mais baixa do menu — única gerada do zero, sem referência | Zero | Total | Você NÃO tem página de referência nem quer desenhar no canvas. É o fallback. |
| **5. AI site-builders (v0 / Lovable / Manus)** *(rota externa — só aparece se você usa um deles)* | Você descreve a página num desses geradores, ele cria o HTML, e você cola aqui como `page.html`. Eles trazem **runtime próprio** (não é Liquid nativo do Shopify) — então serve como landing externa OU a `page-build` exporta/reintegra ao tema. Consumida igual à rota 2 (você traz o HTML; a Aura injeta os markers `data-aura-section` e segue pra 3.7). | Alta — geradores modernos | Free tier / pago conforme uso | Média (gera no app deles; você traz o HTML) | Você já usa v0/Lovable/Manus e prefere desenhar lá fora, ciente de que o runtime é deles |

Pergunte direto, sem decidir por ele:
> "Qual rota você prefere pro design da página? A **1 (clone-and-adapt)** é a mais rápida e costuma sair melhor, porque parte de um layout de concorrente que já converte — você só me indica uma página que acha boa. Mas escolhe a que fizer sentido pra você."

Auto-sugira a rota 1 como **default** (não imposição) por velocidade e qualidade, mas respeite a escolha do membro. Se o membro estiver em stage starter (member-stage-awareness) e sem referência em mente, explique a rota 4 sem empurrar custo.

Depois da escolha, vá pra sub-etapa correspondente (rota 1 → 3.3 · rota 2 → 3.4 · rota 3 → 3.5 · rota 4 → 3.6 · rota 5 → 3.6b). **Toda rota termina gerando `design/page.html` + indo pra 3.7 (regras de qualidade comuns) + checkpoint de aprovação.** Crie o dir com `mkdir -p workspace/[produto]/page/design`.

> **Ajustes rápidos no admin (Sidekick) — pós-launch:** depois que a página estiver no ar (pós-07b), o membro pode usar o **Sidekick** (a IA dentro do admin do Shopify) pra microajustes pontuais — trocar uma imagem, ajustar um texto, mexer numa cor — sem voltar pro Claude Code. Não substitui a `page-design`/`page-build` (que constroem a página inteira com a copy real e fazem o deploy versionado e seguro): é só pro retoque rápido depois. Mencione isso ao membro só se for útil no contexto, não como rota de design.

> **Prontidão pra IA de busca (GEO):** independente da rota escolhida aqui, a `page-build` adiciona a camada GEO/Schema.org (`product-schema.json` + `agent-facts.html`) pra a página ser entendida e citada quando alguém pesquisa o produto no ChatGPT, Claude ou Perplexity (search/shopping). A rota desta etapa é só decisão **visual** — a prontidão pra IA de busca é garantida no build (`page-build`), não depende da rota.

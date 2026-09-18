# Page Design · Referência: Escolha da fonte de design, rotas viáveis e menu ao membro (ETAPA 3, sub-etapas 3.1 e 3.2)

> A detecção em runtime das três rotas, a tabela do menu (como funciona, qualidade, o que o membro precisa ter, quando usar), a pergunta ao membro, o default sugerido sem imposição e as notas sobre Sidekick e prontidão pra IA de busca. Abra nas sub-etapas 3.1 e 3.2.

## ETAPA 3 — ESCOLHA DA FONTE DE DESIGN (o membro escolhe a rota)

Aqui o design nasce. São **três rotas**, e a `page-design` NÃO escolhe por você: ela **apresenta as opções e o MEMBRO escolhe.** Todas convergem pro MESMO arquivo: `workspace/[produto]/page/design/page.html` — a **FONTE ÚNICA DE VERDADE visual**, aprovada pelo membro antes de qualquer Liquid existir. O resto da skill (tokens, plan, `page-build`) segue idêntico, independente da rota.

A régua de qualidade da 3.7 é **bloqueante nas três**: a página não chega ao membro sem passar. Rota que entregou HTML violando a régua é corrigida inline aqui, nunca devolvida pro membro consertar.

### 3.1 Detectar rotas viáveis (runtime)

Antes de apresentar o menu, detecte o que está disponível NESTA sessão e nesta máquina; só ofereça as rotas viáveis:

| Rota | Disponível quando |
|---|---|
| **1. Do zero, com o Claude Design** *(padrão)* | A tool `Artifact` existe na sessão — é ela que abre o canvas de design dentro do Claude Code (padrão do Claude Code atual). Ausente: a rota some do menu e o default passa a ser a rota 2. |
| **2. Clonar uma página inteira com o SingleFile** | O membro tem uma marca de referência cuja página ele acha boa E a loja Shopify conectada (`shopify theme list --store "$STORE"` responde). Sem a loja conectada, mostre a rota com o pré-requisito em uma linha e ofereça instalar e logar a CLI agora (o mesmo passo 6.1 da `page-build`) ou seguir por outra rota. |
| **3. Quebra-cabeça de seções** | O membro tem pelo menos duas fontes de referência: arquivos `.html` de páginas diferentes, prints de seções (Pinterest, Figma, Dribbble) ou os dois misturados. |

> Refero (`mcp__refero__`), se presente, já foi usado na ETAPA 2 pra brand signals — NÃO é rota de design aqui, é fonte de signals que alimenta qualquer rota.

### 3.2 Apresentar o menu ao membro (no `report_language`)

Mostre esta tabela (traduzida pro idioma do membro, listando só as rotas viáveis da 3.1):

| Rota | Como funciona | Qualidade de design | O que você precisa ter | Quando usar |
|---|---|---|---|---|
| **1. Do zero, com o Claude Design** *(padrão)* | A página nasce inteira aqui dentro, no canvas de design do Claude Code (a tela onde ela aparece montada): suas seções na ordem do plano, sua copy real, a paleta e a tipografia escolhidas na ETAPA 2 e suas imagens nos slots. Você vê a página montada, pede ajuste, eu refaço. | Alta — desenho sob medida pro seu produto, com a régua de design como gate | Nada. Já está tudo aqui | Você quer a página desenhada do zero pro seu produto, sem depender de referência de terceiro |
| **2. Clonar uma página inteira com o SingleFile** | Você salva a página da marca que acha boa com a extensão SingleFile e me diz onde o arquivo está. Eu pego só o **esqueleto de layout**, encaixo no seu plano de seções, troco 100% do conteúdo pelo seu (copy, oferta, imagens, paleta) e a `page-build` compila em seções editáveis no editor da Shopify, direto na sua loja. | Alta — parte de um layout que já converte no seu mercado | A extensão SingleFile no Chrome, a URL da página de referência e a loja Shopify já conectada aqui | Você viu uma página que funciona e quer a mesma estrutura, com o seu conteúdo e velocidade |
| **3. Quebra-cabeça de seções** | Você me manda várias referências: arquivos `.html` de páginas diferentes, prints de seções que achou no Pinterest, Figma ou Dribbble, ou os dois. Eu leio os prints, extraio a estrutura de cada seção e monto **uma página só**, com espaçamento, tipografia e paleta unificados. Cada seção vira uma seção editável no editor da Shopify. | Alta — o melhor de cada referência, unificado. Não pode parecer colagem: isso é gate | Duas ou mais referências (arquivo, print ou os dois) | Você gostou do hero de uma página, da prova social de outra e da oferta de uma terceira |

Pergunte direto, sem decidir por ele:
> "Qual rota você prefere pro design da página? A **1 (do zero, com o Claude Design)** é o padrão: a página nasce aqui inteira, desenhada pro seu produto, e você ajusta o que quiser vendo pronto. A **2** parte do layout de uma marca que você acha boa. A **3** junta várias referências numa página só. Escolhe a que fizer sentido pra você."

Auto-sugira a rota 1 como **default** (não imposição). Se o membro já chegou com uma referência forte na cabeça ("quero igual à página da marca X"), diga em uma linha que a rota 2 entrega isso mais rápido e deixe ele decidir.

Depois da escolha, vá pra sub-etapa correspondente (rota 1 → 3.3 · rota 2 → 3.4 · rota 3 → 3.5). **Toda rota termina gerando `design/page.html` + passando pela 3.7 (regras de qualidade comuns e self-review) + checkpoint de aprovação.** As rotas 2 e 3 passam antes pela normalização da 3.6, porque ingerem HTML de fora. Crie o dir com `mkdir -p workspace/[produto]/page/design`.

> **Ajustes rápidos no admin (Sidekick) — pós-launch:** depois que a página estiver no ar (pós-`page-build`), o membro pode usar o **Sidekick** (a IA dentro do admin do Shopify) pra microajustes pontuais — trocar uma imagem, ajustar um texto, mexer numa cor — sem voltar pro Claude Code. Não substitui a `page-design`/`page-build` (que constroem a página inteira com a copy real e fazem o deploy versionado e seguro): é só pro retoque rápido depois. Mencione isso ao membro só se for útil no contexto, não como rota de design.

> **Prontidão pra IA de busca (GEO):** independente da rota escolhida aqui, a `page-build` adiciona a camada GEO/Schema.org (`product-schema.json` + `agent-facts.html`) pra a página ser entendida e citada quando alguém pesquisa o produto no ChatGPT, Claude ou Perplexity (search/shopping). A rota desta etapa é só decisão **visual** — a prontidão pra IA de busca é garantida no build (`page-build`), não depende da rota.

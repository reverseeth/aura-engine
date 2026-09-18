# Market Research · Referência: Voice of Customer, a mineração das frases exatas (ETAPA 5, primeira parte)

> Os sistemas a puxar (review mining, 4 estrelas, atalhos do Google, consumer insights, says vs does, filtro de densidade, Shulex), a regra de nunca parafrasear e de manter o inglês US, os mínimos por tipo de frase e as fontes de primeira mão quando o membro já tem lista ou clientes (giveaway survey e warm calls). Abra na ETAPA 5.

### ETAPA 5 — Voice of Customer (Linguagem EXATA — Mínimo 35 Frases)

**Sistemas a puxar da base antes de minerar (rode cada `best_query`):**
- **Voice of Customer Research (Review Mining / Surveys / Interviews)** (rode `Voice of Customer review mining process extracting verbatim phrases from reviews`) — o processo de extração de frases exatas
- **4-Star Review Mining (avoid 1s and 5s)** (rode `four star reviews mining avoid 5 star 1 star fake reviews honest language`) — onde está a linguagem honesta (evitar 1s e 5s)
- **Google Review-Mining Shortcuts (site:amazon.com inurl product-reviews)** (rode `Amazon review mining google shortcut tired of wasn't until tried site operator`) — operadores de busca pra achar frases rápido
- **Consumer Insights Database (where + what + how to mine)** (rode `consumer insights database mine reviews reddit tiktok ad comments fears desires motivations`) — mapa de fontes (Reddit, TikTok, ad comments)
- **Says-vs-Does (Trust Behavior, Not Surveys)** (rode `says vs does trust purchasing behavior not surveys beer survey national enquirer right answer bias`) — filtra o que as pessoas DIZEM do que realmente FAZEM
- **Review Density Filter (Organize For Best Reviews)** (rode `filtrar reviews por tamanho LEN body ordenar Z A manter 200 300 mais longas`) — antes de ler review por review numa base grande: filtre pelo tamanho do texto (o comprimento do campo body), ordene do maior pro menor e fique com as 200-300 mais longas — são as densas em linguagem aproveitável; review de uma linha quase nunca rende frase de copy
- **Amazon Mining com Shulex + mapa de níveis de preço** (rode `shulex chatgpt for amazon top pros cons purchase motivation usage scenarios QA`) — a rota Amazon da varredura por plataforma: extrai das listagens os top pros e cons, a motivação de compra, os cenários de uso e o Q&A, cruzando os achados com um mapa de níveis de preço do mercado

Das pesquisas da etapa 4, extraia e organize SEPARADAMENTE. **NUNCA PARAFRASEAR** — capture exatamente como as pessoas falam. Isso vai pra copy e criativos literalmente. **VOC permanece SEMPRE no idioma original do consumidor (inglês US), nunca traduzir** — mesmo com `report_language: "pt-BR"`. É matéria-prima literal; o resto do relatório fica no idioma do membro, as frases não.

- **Frases exatas descrevendo o PROBLEMA** — mínimo 15 frases
- **Frases exatas descrevendo o DESEJO** — mínimo 10 frases
- **Frases exatas descrevendo FRUSTRAÇÕES com produtos existentes** — mínimo 10 frases
- **Palavras e expressões recorrentes** (aparecem 3+ vezes na base de pesquisa) — com a contagem gravada, não só a lista

Essas frases são ouro. Hopkins escreveu em 1923: "a boa copy fala a linguagem do consumidor". Esse é o raw material.

**Fontes de primeira mão — quando o membro JÁ tem lista ou clientes (cheque o `profile.md`/manifest antes de assumir que não tem):**

Review de concorrente é a linguagem do cliente DOS OUTROS. Se o membro já vende, a fonte mais rica é o cliente dele — e a base tem dois sistemas prontos pra isso:

- **Giveaway Survey System (Viral Sweep + Klaviyo + Custom GPT)** (rode `giveaway survey system viral sweep bonus entries klaviyo entry rate benchmark`) — VOC em massa disfarçado de sorteio: as bonus entries (entradas extras que o participante ganha por responder) compram respostas escritas dos próprios clientes. Regra de qualificação do sistema: lista de compradores abaixo de 2.000-3.000 pessoas → NÃO rodar (a amostra não paga o esforço); acima disso, é a fonte de primeira mão mais barata que existe — o prêmio se paga e o produto real do sorteio é o dado.
- **Warm Calls — Customer Phone Call Research** (rode `warm call cliente script como voce chegou ate nossa marca pausa nao fale mais nada`) — ligação pro cliente com o script "como você chegou até a nossa marca?" seguida da instrução mais difícil: **pausa — não fale mais nada** e deixe o cliente preencher o silêncio. Poucas ligações rendem frases inteiras, com contexto e emoção, que nenhum review entrega. As frases entram na base de VOC com `source` próprio.

Membro pré-launch, sem lista e sem clientes: pule este bloco sem warning — as fontes públicas da ETAPA 4 cobrem a rodada, e este bloco entra na re-rodada da skill quando a marca tiver compradores.

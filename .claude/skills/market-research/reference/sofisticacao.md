# Market Research · Referência: Market Sophistication, os 5 estágios (ETAPA 3)

> Os sistemas a puxar (inclusive o Buzzword Tally), o fallback de coleta de claims quando a `product-research` não rodou, a tabela dos 5 estágios com a resposta estratégica e a classificação dos claims em saturados, comuns, raros e ausentes. Abra na ETAPA 3.

### ETAPA 3 — Market Sophistication Analysis (5 Estágios)

**Sistemas a puxar da base antes de classificar o estágio (rode cada `best_query`):**
- **Eugene Schwartz — 5 Stages of Market Sophistication** (rode `market sophistication five stages Schwartz mechanism claim escalation jaded market`)
- **Three Strategic Responses for Sophisticated Markets (New Mechanism / New Information / New Identity)** (rode `New Mechanism New Information New Identity three strategic responses sophisticated markets`) — define a resposta estratégica certa pros estágios 3/4/5
- **Market Sophistication Headline Templates (by stage)** (rode `market sophistication headline templates by stage markets retrace insight cigarette cycle`) — ancora os claims comuns/saturados de cada estágio
- **Schwartz Deadly Sincerity & The Turn** (rode `Schwartz deadly sincerity damaging admission product flaw the turn transition believability`) — recurso pra estágio saturado onde claims diretos morreram
- **Buzzword Tally (medição de saturação de mensagem)** (rode `contagem de buzzwords tally +1 cada repeticao medir mensagem saturada fatigada`) — a classificação saturado/comum/raro/ausente abaixo não é palpite, é contagem: +1 a cada repetição do mesmo claim/buzzword nos ads e PDPs coletados. O claim mais contado é a mensagem mais fatigada do mercado. Essa mesma contagem alimenta o `saturated_in_market` do vocabulário na ETAPA 5

Analise o mercado através dos claims dos concorrentes identificados no product research.

**Fallback quando a Skill `product-research` não rodou (caminho NORMAL pra quem já tem produto — ver ETAPA 0):** não existe lista prévia de claims. Colete AGORA: use a tool `WebSearch` pra identificar os 5-10 concorrentes ativos do nicho (buscas por categoria de produto, marcas citadas na VOC, "best [categoria]" em listicles) e a **Meta Ad Library pública** (`https://www.facebook.com/ads/library/`) pra extrair os claims dos ads ATIVOS de cada um — via `WebFetch`, e se barrar (JS/rate-limit), o fetcher Playwright: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text` (rule `resilient-fetch.md`). 10-15 claims reais bastam pra classificar o estágio. Essa coleta NÃO é retrabalho: a ETAPA 7 (Competitive Landscape) reaproveita os MESMOS concorrentes e claims — colete uma vez, use duas.

- **Quantos produtos/soluções similares já existem?** (contagem de marcas ativas com ads escalados)
- **Quais claims já foram feitos?** Liste os 10-15 principais claims do mercado
- **Em qual estágio está?**:

| Estágio | Características | Resposta Estratégica |
|---|---|---|
| **1** | Virgin market. Produto novo, crowd não conhece a categoria | Claim direto simples: "X faz Y" |
| **2** | Claim direto com superlativo ainda funciona | "MAIS efetivo", "MAIS rápido", "MAIS barato que concorrentes" |
| **3** | Claims diretos saturados — precisa de **mecanismo único** | Nome proprietário de ingrediente/processo/tecnologia |
| **4** | Mecanismos saturados — precisa de **nova informação** | Descoberta recente, causa-raiz nova, expansão de mecanismo existente |
| **5** | Tudo saturado — precisa de **identificação** | Falar com quem a pessoa quer SER, não com o problema funcional |

Liste:
- **Claims saturados a EVITAR** (todo concorrente usa)
- **Claims comuns** (maioria usa, usar com twist próprio)
- **Claims raros** (poucos usam, oportunidade)
- **Claims ausentes** (ninguém usa, oportunidade forte)

Defina a resposta estratégica certa pro estágio identificado.

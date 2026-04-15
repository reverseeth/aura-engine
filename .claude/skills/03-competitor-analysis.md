---
name: competitor-analysis
description: Engine de análise profunda de concorrentes que mapeia PDPs, ads em Meta Ad Library, claims, alternative solutions, e gap analysis. Use quando o membro disser "competitor analysis", "análise de concorrentes", "analisar concorrentes", ou quando o market research estiver completo e o membro quiser entender o cenário competitivo antes de montar a oferta. Este é o input decisivo pra posicionamento: onde você vai BRIGAR e onde você vai CONTORNAR.
---

# Competitor Analysis Engine

## Quando Usar
Quando o membro tem produto definido e market research feito, e precisa mapear o cenário competitivo com profundidade operacional antes de criar oferta e copy. A análise aqui alimenta: mecanismo único (o que NÃO usar), posicionamento (onde ninguém está), claims (o que evitar e o que explorar), e estrutura de funil (o que o mercado converteu).

## Antes de Começar

1. Leia `/workspace/profile.md`
2. Leia `/workspace/[produto]/01-product-research.md` (se existir — tem concorrentes já identificados)
3. Leia `/workspace/[produto]/02-market-research.md` (overview competitivo básico + gaps já identificados)
4. Consulte a base Aura extensivamente sobre competitor research (extração de claims, organização de swipe files), reconnaissance engine (técnicas de research via social), cloaker breaking (quando concorrentes escondem páginas), alternative solution research (mapeando TUDO que o avatar já tentou), market sophistication (claims saturados), análise de ad angles, classificação de criativos por posição no funil (4Pi signatures TOF/MOF/BOF), swipe file method, e os 15 fatores da estrutura de funil. Aprofunde em cada sub-conceito — esta skill opera em detalhe EXECUTIVO, não conceitual.

## Fluxo da Skill

### ETAPA 1 — Identificar Concorrentes

Se o product research já identificou concorrentes, use essa lista como base (5-10 marcas). Se não, pergunte:

"Você já sabe quem são seus concorrentes? Se sim, me manda os links das lojas deles. Se não sabe, diga 'não sei' — o sistema encontra sozinho."

**SE o membro mandar links:** use como base e complemente se for menos de 5.

**SE o membro disser que não sabe:** pesquise automaticamente (web search):
- `"[produto]" brand site:.com`
- `"[produto]" shop`
- Meta Ad Library busca: categoria + palavras-chave
- TikTok Shop Best Sellers na categoria
- Amazon Best Sellers na categoria
- Similarweb pra identificar lojas com tráfego no nicho

Identifique **5-10 concorrentes** ATIVOS (têm ads rodando agora + loja funcional). Se encontrar menos de 5, amplie a busca pra produtos ADJACENTES que resolvem o mesmo problema (ex: se o produto é colágeno em pó, inclua serums anti-aging, tratamentos capilares com collagen boost, e clínicas de estética — são alternativas que o avatar considera).

### ETAPA 1B — Ads Screenshots dos Concorrentes

Verifique no `/workspace/profile.md` se o membro tem SpyBox/Adsparo.

**SE TEM:**
"Cola screenshots dos ads mais escalados dos concorrentes — se tiver acesso ao SpyBox ou Adsparo. Se não tiver esses screenshots em mãos agora, tudo bem: sigo com o Meta Ad Library público."

**SE NÃO TEM:** pule a pergunta, use Meta Ad Library público direto na Etapa 3.

### ETAPA 2 — Análise de PDPs dos Concorrentes

Pra cada concorrente, acesse a página de produto (web fetch). Se tiver cloaker/Cloudflare bloqueando, tente:
- Acessar via arquivo.web (Wayback Machine) se houver snapshot recente
- Acessar via Google Cache
- Scraper view-source diretamente

**Pra cada PDP, documente:**

**Estrutura da página (aplicando frameworks da vault):**
- **Tipo de hero section**: autoridade (expert/doctor), UGC/testimonial, product-hero, problem-agitate, lifestyle, demo/before-after (aplica os 5 tipos de hero da vault)
- **Headline principal exata** (copie literalmente)
- **Sub-headline exata**
- **Como apresenta o produto**: foto, vídeo (quanto tempo?), GIF, demonstração
- **Bullet points de benefício** (copie as primeiras 5)
- **Mecanismo único?** Qual nome? Como apresenta? (ingredient, process, tech, combo)
- **Stack visual de valor?** Quantos itens? Com ancoragem de preço?
- **Preço**: base + bundles oferecidos (2-pack, 3-pack, subscription) com % savings
- **Guarantee**: tipo (money-back, satisfaction, results-based), duração (30/60/90 dias), copy exata
- **Social proof**: tipo (reviews count + média, UGC, mídia, certificações, endorsements)
- **FAQ**: quais perguntas aborda? Quantas?
- **CTAs**: quantos, onde, que copy usa nos botões
- **Shipping**: grátis? a partir de quanto? tempo estimado?
- **Aplicação dos 15 Fatores de Funil** (vault): quais fatores a página cobre bem, quais ignora

**Copy analysis (frameworks da vault):**
- **Tipo de lead** (Story, Secret, Proclamation, Problem-Solution, Offer, Direct — identificar aplicando os 5 tipos de lead por awareness de Schwartz)
- **Nível de awareness que a página assume** do visitante (dita onde no funil essa LP está)
- **Gatilhos de persuasão usados** (escassez, autoridade, prova social, reciprocidade, compromisso — identifique quais da lista dos 6 de Cialdini)
- **Grande promessa** (qual é? quão específica?)
- **Quais objeções a página tenta quebrar** (com que técnica)
- **Tom de voz** (sofisticado, casual, técnico, emocional, urgente, educativo)
- **Congruência ad→página**: se o concorrente tem ads ativos, a LP espelha o ad? (Message match, visual match, promise match)

### ETAPA 3 — Análise de Ads no Meta Ad Library (Agrupamento Por Aparições)

Pra cada concorrente, pesquise no Meta Ad Library (web fetch / scraping via Playwright quando possível).

**Regras críticas:**

1. **NÃO use tempo de veiculação como métrica de escala** — muitos criativos rodam há meses sem spend significativo
2. **Agrupe criativos idênticos ou quase idênticos** (mesmo vídeo com variação de overlay ou 1-2 palavras trocadas) e conte o número de APARIÇÕES
3. **Mais aparições = mais ad sets usando esse criativo = mais escalado**. Essa é a métrica.

**Métricas quantitativas:**
- Total de ads ativos no momento
- Número de criativos únicos (após agrupamento)
- **Top 10 criativos por aparições** (proxy de escala)

**Análise qualitativa dos top 10 criativos:**
Pra cada um dos top 10:

- **Tipo**: imagem estática, vídeo UGC (spokesperson falando), vídeo demonstração, antes/depois, carrossel, vídeo motion-graphic
- **Transcrição** (se vídeo): hook dos primeiros 3 segundos (texto E fala literal) + 2-3 frases do corpo do script + CTA de fechamento
- **Visual descrição do hook**: o que aparece na tela nos primeiros 3 segundos
- **Ângulo** (classificar aplicando frameworks de ad angles da vault):
  - Problema (dor/frustração)
  - Resultado (desejo/transformação)
  - Curiosidade (mistério/revelação)
  - Autoridade (expert/estudo/credencial)
  - Comparação (vs X, melhor que Y)
  - Social proof (testimonial, UGC, número de clientes)
  - Controvérsia (contrarian, "o que não te contam")
  - Identificação ("pra mulheres como você")
- **Copy do ad (primary text)**: copia literal
- **CTA**: qual e como está formulado
- **Landing page destino**: PDP? landing page dedicada? advertorial? listicle?

### ETAPA 3B — Classificação dos Criativos por Posição no Funil

Aplicando as **4Pi signatures** da vault (padrões de métrica que indicam posição no funil), classifique cada top criativo como:

- **TOF (Top of Funnel)**: hook de interrupção, tom emocional, problema+agitação, awareness-building. Geralmente frequency < 1.1, CPM moderado, CPC alto.
- **MOF (Middle of Funnel)**: educação do mecanismo, social proof, comparação. Frequency 1.15-1.3, CPM mais alto, CTR mais baixo mas conversão melhor.
- **BOF (Bottom of Funnel)**: retargeting/warm audiences, foco na oferta (preço, garantia, urgência). Frequency > 1.3, CPM alto, CTR baixo mas ROAS alto.

Se todos os top criativos estão numa posição só, o concorrente tem **funil desbalanceado** — oportunidade pra você cobrir as outras posições.

### ETAPA 4 — Claims Compilation Completa

Compile TODOS os claims que os concorrentes fazem, classificados por tipo:

**Claims diretos** (promessa de resultado):
- "Reduz rugas em 30 dias"
- "Resultados visíveis em 1 semana"
- "Perde 5kg em 30 dias"

**Claims de mecanismo** (como funciona):
- "Tecnologia de micro-corrente"
- "Infusão de ácido hialurônico"
- "Fórmula com peptídeos patenteada"

**Claims de autoridade** (credencial):
- "Recomendado por dermatologistas"
- "Aprovado pela FDA"
- "Desenvolvido por cientistas de Harvard"

**Claims de prova social** (evidência):
- "50.000+ clientes satisfeitas"
- "4.8 estrelas em 12.000 reviews"
- "Featured in Forbes, Vogue, NYT"

**Classifique cada claim:**

| Classificação | Significado | Ação |
|---|---|---|
| **SATURADO** | Todos ou quase todos usam | EVITAR — o público não acredita mais |
| **COMUM** | Maioria usa | USAR com twist próprio (especificidade de Hopkins) |
| **RARO** | Poucos usam | OPORTUNIDADE — diferenciação moderada |
| **AUSENTE** | Ninguém usa | OPORTUNIDADE FORTE — diferenciação máxima |

Apresente em tabela:

| Claim | Categoria | Quantos usam | Classificação | Ação |
|---|---|---|---|---|

### ETAPA 5 — Alternative Solution Research

Esta é a etapa mais negligenciada E mais valiosa. Não basta mapear concorrentes diretos — mapeie TUDO que o avatar já tentou pra resolver o problema.

Pesquise (web search + review mining):

**Soluções concorrentes diretas** (já cobertas nas etapas 1-3)

**Soluções adjacentes da mesma categoria**:
- Outros formatos do mesmo problema (se seu produto é serum, mapeie cremes, tratamentos profissionais, procedimentos estéticos, rotinas DIY)

**Remédios caseiros / DIY**:
- O que as pessoas fazem em casa pra tentar resolver? (dicas de TikTok, receitas de avó, hacks)

**Tratamentos profissionais**:
- Médicos, dermatologistas, clínicas especializadas — qual o range de preço, tempo, invasividade?

**Outras categorias que roubam share**:
- O que mais consome o orçamento que o avatar poderia gastar no seu produto? (maquiagem disfarçando o problema, roupas disfarçando, terapia mental pra aceitar, etc)

**Produtos da mesma marca mas não concorrentes**:
- O que os grandes players oferecem que captura parte da demanda?

Esta análise é crítica pra montar a **oferta**: seu produto não compete só com outros DTCs, compete com TUDO que o avatar já gasta dinheiro tentando resolver. A narrativa de copy depois precisa posicionar seu produto contra TODAS essas alternativas, não só contra outros ecom brands.

### ETAPA 6 — Gap Analysis Completo

A parte mais valiosa estrategicamente. Identifique:

**Gaps de público (Avatar):**
- Segmento que NENHUM concorrente aborda (ex: todos falam com mulheres 25-35, ninguém fala com 45+; todos focam em iniciantes, ninguém com avançadas)
- Situação/trigger event que ninguém explora (pré-casamento, pós-parto, pós-divórcio, aposentadoria)
- Identidade que ninguém captura (profissional de carreira, mãe-que-se-perdeu, atleta recreativa)

**Gaps de messaging:**
- **Dor real do market research que nenhuma PDP aborda**
- Objeção que ninguém quebra (ex: "é caro demais" — ninguém justifica)
- Benefício que ninguém destaca
- Medo ou desejo secundário ignorado

**Gaps de formato:**
- Todos usam UGC mas ninguém usa demonstração close-up? Gap.
- Todos usam vídeo, ninguém usa carrossel educativo? Gap.
- Todos usam hook de problema, ninguém usa hook de resultado?
- Todos têm LP dedicada, ninguém usa advertorial?

**Gaps de oferta:**
- Ninguém oferece garantia forte (ou oferece mas não destaca)?
- Ninguém faz bundle com produto complementar?
- Ninguém tem subscription/refill?
- Ninguém tem bump de checkout?

**Gaps de mecanismo:**
- Todos usam o mesmo mecanismo genérico? Qual?
- Existe espaço pra criar mecanismo proprietário baseado em ingrediente/processo único do seu produto?
- Existe combinação de ingredientes que ninguém nomeou?

### ETAPA 7 — Síntese Estratégica

Compile tudo num relatório acionável:

**1. Mapa Competitivo (Tabela Resumo)**

| Concorrente | Preço base | Mecanismo | Claim principal | Posicionamento | Forças | Fraquezas |
|---|---|---|---|---|---|---|

**2. Padrões do Mercado**
- **Baseline**: o que TODOS fazem (você precisa fazer no mínimo isso pra não parecer incompleta)
- **Tendência**: o que a MAIORIA faz (considere fazer com twist)
- **Saturado**: claims e angles que DEVEM SER EVITADOS
- **Winning patterns**: criativos/ângulos/formatos que estão escalando AGORA (top 10 da Etapa 3)

**3. Oportunidades de Diferenciação (Ranqueadas por Potencial)**

Cada oportunidade com:
- Tipo (audience, messaging, format, offer, mechanism)
- Descrição
- Por que é oportunidade (o gap específico)
- Como explorar (ação concreta)
- Potencial (alto/médio/baixo baseado em demand do gap + facilidade de execução)

Liste mínimo 5 oportunidades, ranqueadas.

**4. Recomendação de Posicionamento**

Baseado em toda a análise, a recomendação estratégica:
- **Como este produto deve se posicionar** pra diferenciar-se (em 2-3 frases)
- **Qual mecanismo único perseguir** (sugestão alinhada com gaps)
- **Qual avatar focar** (segmento underserved)
- **Qual ângulo principal de comunicação** (hook dominante)
- **Qual tipo de página** (advertorial / LP dedicada / PDP robusta) baseado em awareness + concorrência

**5. Swipe File**

- **Top 3 elementos dos concorrentes que vale ADAPTAR** (não copiar — adaptar o princípio): escolha os 3 mais fortes que a Etapa 3 identificou (ex: "o hook de autoridade do concorrente X funciona bem porque Y — adapte pra nosso mecanismo")
- **Top 3 elementos que NÃO vale seguir**: saturados ou fracos (ex: "todo mundo usa 'clinically proven' — é commodity, descarta")

## SALVAR

`/workspace/[produto]/03-competitor-analysis.md`

Estrutura:
1. Lista de concorrentes analisados + links
2. PDP analysis por concorrente (Etapa 2)
3. Meta Ad Library findings + top creatives transcritos (Etapa 3)
4. Classificação de posição de funil (Etapa 3B)
5. Claims compilation table (Etapa 4)
6. Alternative solutions map (Etapa 5)
7. Gap analysis (Etapa 6)
8. Síntese estratégica — posicionamento + swipe file (Etapa 7)

## Mensagem Final

"Análise competitiva completa. Agora temos:
- Market research profundo (Skill 02)
- Mapa competitivo completo com gaps acionáveis (esta skill)

Próximo passo: diga **'offer'** pra construir a oferta com mecanismo único, stack de valor, garantia, e unit economics. A oferta vai puxar direto das recomendações de posicionamento desta análise + do perfil psicográfico do market research."

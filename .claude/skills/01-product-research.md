---
name: product-research
description: Engine completo de pesquisa e validação de produto. Use quando o membro disser "product research", "pesquisa de produto", "encontrar produto", ou descrever que precisa de um produto pra vender. Requer que o membro cole dados do Kalodata/SpyBox.
---

# Product Research Engine

## Quando Usar
Quando o membro ainda não tem produto ou quer validar/encontrar um novo produto pra testar.

## Antes de Começar
1. Leia /workspace/profile.md pra entender o contexto do membro
2. Consulte a base Aura com as seguintes buscas (deep=true):
   - "product research criteria validation filtering"
   - "market desires mass desire magnitude"
   - "market sophistication stages determination"
   - "product market awareness Schwartz levels"
   - "unique mechanism UMP UMS differentiation"
   - "avatar core sub avatars underserved"
3. Internalize os frameworks e critérios ANTES de começar a análise

## Fluxo da Skill

### ETAPA 1 — Receber dados do Kalodata / SpyBox

Antes de pedir dados, verifique em `/workspace/profile.md` se o membro tem SpyBox disponível:

**SE tem SpyBox (ou Kalodata):**

Diga ao membro:

"Preciso que você abra o Kalodata (ou SpyBox) e faça o seguinte:
1. Aplique os filtros:
   - Period: Last 30 Days
   - Revenue: $100k - $500k
   - Revenue Growth Rate: >0%
   - Avg. Unit Price: >$60
   - Category: sem filtro (não marque nenhuma categoria)
2. Selecione entre 5 e 15 produtos que parecem promissores
3. Me mande: screenshots dos produtos OU copie e cole os dados (nome, preço, faturamento estimado, categoria, link)

Se você também tiver dados do Similar Web sobre os concorrentes, cole também. Se não tiver, eu faço o que puder com outras fontes."

**SE NÃO tem SpyBox/Kalodata (fallback):**

Diga ao membro:

"Você não tem acesso ao SpyBox/Kalodata — sem problema. Me descreva o tipo de produto que te interessa:
- Categoria / nicho
- Faixa de preço-alvo
- Público que quer atingir

Eu pesquiso usando fontes públicas (Meta Ad Library, TikTok Shop Trending, Amazon Best Sellers, Reddit) e te volto com candidatos pra analisar."

ESPERE o membro enviar os dados antes de prosseguir.

### ETAPA 2 — Filtragem Inicial

Para CADA produto que o membro enviou, aplique os filtros técnicos (consulte a base Aura: "product research criteria validation"):

- AOV total após bundles potenciais garante margem saudável (markup 3x+ sobre COGS + frete)? Se não → DESCARTA (explique por quê). O filtro de preço mínimo de $60 já vem do Kalodata; o check aqui é sobre viabilidade de margem com a estrutura de bundles.
- Markup mínimo de 3x sobre COGS + frete é viável? Se não → DESCARTA
- Produto é leve (não complica logística)? Se não → FLAG DE RISCO (não descarta, mas sinaliza)
- É produto com bateria/eletrônico? Se sim → FLAG DE RISCO (defect rate, questões legais)
- É sazonal? Se sim → FLAG (não descarta, mas sinaliza que é operação de curto prazo)

Mostre uma tabela com cada produto e o resultado da filtragem. Produtos descartados saem da análise. Produtos com flags continuam mas com o risco documentado.

### ETAPA 3 — Google Trends

Para cada produto que PASSOU na filtragem, pesquise no Google Trends (use web search):

- Termos relacionados ao produto e ao nicho nos últimos 5 anos
- Classifique: QUEDA CONSISTENTE → DESCARTA | FLAT → ACEITÁVEL | SUBINDO → BOM
- Mostre o resultado por produto

### ETAPA 4 — USPTO Trademark

Para cada produto que ainda está na lista, pesquise (use web search):

- Existe trademark ativo pro nome do produto ou marca mais conhecida vendendo ele?
- Se sim: é marca grande com recursos legais? → DESCARTA
- Se não tem trademark ou é marca pequena → PASSA

### ETAPA 5 — Meta Ad Library

Para cada produto que ainda está na lista, acesse o Meta Ad Library (use web search e scraping quando possível):

- Identifique os principais concorrentes vendendo aquele produto ou similar
- Quantos ads ativos cada concorrente tem
- IMPORTANTE: agrupe criativos iguais ou quase iguais. Cada aparição de um criativo = um ad set usando ele. Mais aparições = mais escalado. NÃO use tempo de veiculação como métrica de escala.
- Para os top 5 criativos mais escalados (mais aparições): identifique hook, ângulo, tipo de criativo (UGC, demonstração, antes/depois, etc), copy principal, CTA
- Se possível, transcreva vídeos dos top criativos

### ETAPA 6 — Review Mining

Para cada produto que ainda está na lista, pesquise (use web search):

- Amazon reviews (positivas E negativas)
- Reddit discussions
- TikTok comments
- Fóruns relevantes

Extraia e organize:
- DORES: o que as pessoas reclamam sobre produtos similares (com frequência de menção)
- DESEJOS: o que as pessoas querem que o produto faça (com intensidade)
- OBJEÇÕES: o que impede as pessoas de comprar (medo, preço, ceticismo)
- LINGUAGEM: frases exatas que os consumidores usam (essas vão direto pra copy e criativos depois)
- GAPS: reclamações recorrentes que NENHUM concorrente resolve

### ETAPA 7 — Validação de Eficácia

Para cada produto, pesquise (use web search):

- O produto realmente funciona? Há estudos, evidências, consensus de especialistas?
- Classifique: FUNCIONA COMPROVADAMENTE | FUNCIONA PARCIALMENTE | GIMMICK
- Se for gimmick → DESCARTA com explicação

### ETAPA 8 — Análise Estratégica

AQUI É ONDE A BASE AURA IMPORTA MAIS. Consulte a base com deep=true para cada um desses conceitos e aplique aos produtos:

1. **Magnitude do Desejo** (busque "market desires mass desire magnitude"):
   - FRACO (organizar mesa, gerenciar cabos) → preço baixo, volume alto, inviável com ads
   - MÉDIO (melhorar sono, mais energia)
   - FORTE (perder peso, atrair sexo oposto, resolver dor crônica) → ticket alto, persuasão mínima

2. **Market Awareness** (busque "product market awareness Schwartz levels"):
   - Em qual nível de consciência o mercado está? (Unaware, Problem Aware, Solution Aware, Product Aware, Most Aware)
   - Isso determina TODO o approach de copy e criativos depois

3. **Market Sophistication** (busque "market sophistication stages determination"):
   - Qual estágio? (1 a 5)
   - Quais claims já foram usados e estão saturados?
   - É possível entrar com novo mecanismo ou nova informação?

4. **Possibilidade de Mecanismo Único** (busque "unique mechanism UMP UMS differentiation"):
   - Consigo criar um mecanismo proprietário e diferenciado?
   - Tem ingrediente, feature, ou processo que pode ser renomeado/reposicionado?

5. **Possibilidade de Avatar Underserved** (busque "avatar core sub avatars underserved"):
   - Existe um segmento do público que os concorrentes ignoram?
   - Posso falar com esse segmento de forma diferenciada?

6. **Potencial de Oferta:**
   - Consigo criar stack de valor com bundles, bumps, upsells?
   - Consigo ter AOV acima de $60?

7. **Potencial Criativo:**
   - Tem storytelling possível?
   - Tem ângulos inexplorados que os concorrentes não usam?

### ETAPA 9 — Ranking Final

Crie um ranking dos produtos do melhor pro pior com score de 1-10 baseado em TODOS os critérios acima.

Para CADA produto mostre:

**[Nome do Produto] — Score: X/10 — Veredicto: TESTAR / TALVEZ / DESCARTAR**

- 3 razões principais pra testar
- 3 riscos principais
- Ângulo de diferenciação sugerido
- Nível de dificuldade: FÁCIL / MÉDIO / DIFÍCIL

Para o produto #1 (melhor ranqueado), entregue ADICIONALMENTE:

- Mecanismo único sugerido (nome + explicação de 2-3 frases)
- Avatar principal sugerido (quem é, o que sente, o que quer)
- Estrutura de oferta preliminar (produto base + bundle + bump sugeridos)
- 3 hooks de criativo que exploram ângulos que os concorrentes NÃO usam
- Próximo passo recomendado

### SALVAR

Salve o relatório completo em:
/workspace/[nome-do-produto-vencedor]/01-product-research.md

Se o membro quiser prosseguir com o produto vencedor, indique: "Diga 'market research' pra aprofundar a pesquisa do [produto]."

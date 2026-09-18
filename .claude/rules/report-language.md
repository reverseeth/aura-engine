---
name: report-language
description: Idioma e estilo de escrita de todo relatório interno e da conversa com o membro (a regra 0 do CLAUDE.md por inteiro, mais as sete regras de escrita simples). O CLAUDE.md traz só o resumo; esta rule é a fonte única.
paths:
  - .claude/skills/**/SKILL.md
  - .claude/templates/
  - workspace/
---

# Report Language (NON-NEGOTIABLE)

> **Fonte única.** A regra de idioma e estilo dos relatórios vive aqui por inteiro. O `.claude/CLAUDE.md` traz apenas um resumo de quatro linhas e aponta para esta rule. Se algum outro texto de estilo conflitar com o que está aqui, esta rule vence. Aplica a todo relatório salvo em `workspace/`, de toda skill, e à conversa com o membro.

## Regra 0 (idioma e estilo de escrita)

O idioma dos relatórios INTERNOS (market research, competitor analysis, offer briefs, copy docs internas, ad strategy, audits, briefings, análises) é definido pelo membro durante a Skill `setup`, salvo em `workspace/profile.md` como `report_language: "pt-BR"` ou `report_language: "en"`. **TODA skill que gera relatório interno DEVE ler esse campo antes de começar e escrever no idioma escolhido.** Se o profile ainda não existir (membro nunca rodou setup), default é `pt-BR`.

**REGRA INVIOLÁVEL:** copy que vai pro consumidor final (ads, landing pages, PDPs do mercado US) **continua sempre em inglês**, independente do `report_language`. A escolha vale só pra documentação interna que o membro lê pra entender o trabalho — nunca afeta copy pública.

**SÓ O RESULTADO NOS DOCS (vale pros dois idiomas):** todo relatório salvo em `workspace/` contém apenas o conteúdo final — nunca narração de processo ou correções ("removi X", "corrigido"), descrição do que o doc NÃO contém ("sem componente Y"), referência à conversa com o membro ("você perguntou", "como você pediu"), auto-referência da AI, ou checagens em formato de pergunta. Meta-informação vive no chat e no `dados.json`, nunca no doc. Regra completa em `.claude/rules/report-only-results.md`.

### Se `report_language: "pt-BR"` (default):

- **PRINCÍPIO INEGOCIÁVEL:** o leitor é um profissional de marketing brasileiro AVANÇADO, e o texto tem que ser 100% entendível na PRIMEIRA leitura, sem reler. Português brasileiro natural e bem explicado. **NUNCA misture inglês e português dentro da mesma frase de um jeito que trave a interpretação.** Se o membro precisar reler pra entender, a frase está mal escrita.
- **LINGUAGEM SIMPLES É PRIORIDADE MÁXIMA (vale pra TODO relatório de TODA skill):**
  - **Nenhuma sigla sem explicação imediata em português simples — e prefira nem usar a sigla.** Exemplos do padrão: CAGR → "crescendo cerca de X% ao ano"; RCT → "estudo clínico de alta qualidade (com sorteio de participantes e grupo de comparação)"; meta-análise → "estudo que soma os resultados de vários estudos"; NIH → "os institutos nacionais de saúde dos EUA"; Cochrane → "rede internacional independente que revisa estudos de medicina"; big CPG → "as gigantes de produtos de consumo (Danone, Nestlé...)"; MOQ → "pedido mínimo"; co-packer → "fábrica terceirizada que envasa"; FDA/FTC → sempre com a descrição do que a agência faz na primeira vez. Siglas que o marqueteiro BR já fala no dia a dia (CPA, ROAS, LTV, TAM, VOC, PDP, CTA) continuam liberadas.
  - **Zero frase de analista comprimida.** "Escala provada por terceiros validando a curva" é PROIBIDO — desdobre em frases completas que uma pessoa inteligente de fora do setor entende de primeira ("outras empresas já provaram que esse mercado compra: são X milhões de clientes e as gigantes estão lançando linhas próprias").
  - **Números estatísticos em palavras:** em vez de "RR 0.69", escreva "reduziu o sintoma em cerca de 30% nos estudos". O número técnico pode vir entre parênteses se agregar, nunca sozinho.
  - **Toda citação de cliente em inglês (VOC) ganha "tradução livre:" em português logo ao lado.** O original permanece (é matéria-prima de copy) — a tradução evita que o membro trave.
  - **Teste final antes de salvar:** "uma pessoa inteligente que NÃO é do setor entenderia cada frase de primeira?" Se não, reescreva. Clareza vence concisão.
- **Inglês cru só é permitido para os poucos termos que um marqueteiro brasileiro avançado de fato fala em inglês no dia a dia:** funnel, hook, headline, CTA, copy, awareness (e os níveis: unaware/problem-aware/solution-aware/product-aware/most-aware), landing page, advertorial, bundle, upsell, lead, ROAS, CPA, LTV, TAM, VOC/Voice of Customer, PDP, claim, targeting, retargeting, lookalike, review, label/rótulo, scoop, gut health, wellness, glow, debloat/bloat, hype, scam, A/B test, split-test, tráfego hot/warm/cold, GLP-1, subscribe & save. Nomes próprios de frameworks (Schwartz, Cialdini, Hopkins, Hormozi, etc.) e nomes de mecanismo ficam como estão.
- **Todo jargão de framework em inglês deve ser TRADUZIDO ou explicado em português na primeira vez que aparece — nunca jogado cru no meio do texto.** Exemplos: scope → alcance; staying power → poder de permanência; blended power → força combinada; belief gap → barreira de crença; core desire → desejo central; on-ramp → porta de entrada; the Turn → a virada; reason-why → justificativa; proof → prova; yes-momentum → encadear "sins"; gut-skin axis → ligação intestino-pele; food system → sistema alimentar moderno; players → concorrentes; drift/retrace → caminhando/avançando; tipping point → ponto de virada; sticky → que gruda na cabeça; crawler → robô; sign-in wall → barreira de login; peer-reviewed → revisada por pares; findings → resultados. (Deadly Sincerity, Damaging Admission, New Identity/Information/Mechanism etc. podem manter o nome do framework, mas SEMPRE com a explicação em português ao lado.)
- **Palavras esquisitas / proibidas (o membro rejeitou) e o que usar no lugar:**
  - "cauda" (no sentido de faixa/grupo) → "faixa", "um grupo de", "presença na faixa 35-45" (NUNCA "cauda forte 35-45")
  - "a mais grossa" / "a camada mais grossa" → "a maior camada", "o maior bloco", "a maior fatia"
  - "maioria conversível" / "conversível" → "a maior parte de quem dá pra converter", "quem está pronto pra comprar"
  - "ressalva" / "caução" → "alerta", "ponto de atenção", "observação importante"
  - "buraco" (no sentido de gap de mercado) → "lacuna" (lacuna de mercado) ou "déficit" (déficit de fibra)
  - "centro de gravidade" → "o ponto onde a estratégia se apoia"
  - "sinal mais alto" → "o indicador mais forte"
  - "stat mais dura" → "o dado mais forte"
  - "frases exatas" (NÃO "verbatim") · "base de pesquisa"/"pesquisa" (NÃO "corpus") · "coletadas" (NÃO "compiladas via cross-referencing") · "ceticismo" (NÃO "skepticism", salvo dentro de framework nomeado)
  - metáforas de guerra/violência em análise competitiva ("onde cada um sangra", "metade da batalha", "guerra", "arsenal", "flanco", "ferida") → linguagem direta: "a fraqueza de cada um", "metade do trabalho", "conjunto de provas", "espaço aberto"
  - metáforas rebuscadas no lugar de palavra simples ("miolo" → "a parte central" · "esqueleto" → "estrutura" · "alicerce" → "base" · "colheita" → "resultado" · "mora nele" → "está nele"). Regra geral: se existe a palavra direta, use a direta — metáfora só quando ela explica melhor que o termo literal
- **PORTUGUÊS NATURAL, NÃO "PORTUGUÊS DE IA":** o texto em português dos relatórios deve soar como uma pessoa explicando com calma, em frases completas (sujeito, verbo e complemento), e nunca como texto de efeito. Padrões PROIBIDOS nas partes em português: (a) a construção "não é X, é Y" usada como frase de impacto ("Não é rótulo, é um sistema" → escrever "O nome funciona como um sistema, e não como um simples rótulo", ou apenas afirmar o que a coisa É); (b) fragmentos sem verbo usados como frase ("A inversão central: o clube é a condição" → "A ideia que faz o nome funcionar é uma inversão: ..."); (c) dois-pontos dramáticos abrindo mini-decreto ("Decisão: página sem urgência" → "Por isso a página vai ao ar sem urgência nenhuma"); (d) personificação forçada ("um sistema que a copy inteira fala", "o nome trabalha em camadas" → dizer quem faz o quê); (e) três itens paralelos perfeitos em sequência como recurso de ritmo. Teste antes de salvar: leia o parágrafo em voz alta — se soa como legenda de post ou slogan, reescreva como explicação. Esses padrões continuam PERMITIDOS dentro da copy consumidor-final em inglês, onde contraste e fragmento são ferramentas de venda deliberadas.
- NUNCA force uma palavra em inglês onde o português funciona naturalmente. NUNCA use jargão acadêmico ou estatístico sem explicar entre parênteses na primeira vez.
- **VOC literal (frases de cliente entre aspas) permanece SEMPRE em inglês US** — é matéria-prima, não traduzir nem tratar como mistura de línguas.
- Frases devem ser completas e fazer sentido para um marqueteiro brasileiro avançado de primeira. Antes de salvar qualquer relatório, releia mentalmente: "alguma frase mistura as duas línguas de um jeito confuso, usa jargão cru ou sigla sem explicação? Se sim, reescreva."

### Se `report_language: "en"`:

- Write in clear, direct, natural English. The member needs to understand without a dictionary.
- Marketing/ecommerce terms stay in English (Voice of Customer, funnel, awareness, targeting, CPA, ROAS, etc.) — same vocabulary, just don't mix Portuguese.
- Avoid academic or statistical jargon without explaining (if essential, explain in parentheses first time used).
- **Plain language is top priority:** no acronym without an immediate plain-English explanation (prefer dropping the acronym: CAGR → "growing about X% per year"; RCT → "high-quality clinical study"); no compressed analyst-speak; statistical numbers in words ("about 30% less nausea in the studies" instead of "RR 0.69"). Final test before saving: "would a smart person outside the industry understand every sentence on first read?"
- Complete sentences with chained logic — not generic empty bullets.
- Same Hopkins-style specificity rule applies ("47% reduction in 14 days" > "fast results").
- Conversation with the member also happens in English from setup onwards.

### Conversação geral com o membro

Independente de qual skill esteja rodando, a conversa direta com o membro (perguntas, confirmações, mensagens finais) usa o idioma do `report_language`. Pra membro `en`, perguntas ficam em inglês; pra `pt-BR`, em português.

## As sete regras de escrita (valem para todo relatório de toda skill)

O leitor é inteligente, mas não é químico, não é nutricionista e não decora sigla. Ele abre o relatório para decidir se investe dinheiro. Cada frase precisa ser entendida na primeira leitura, sem releitura e sem adivinhação.

**1. Uma ideia por frase.** No máximo cerca de 20 palavras por frase. Se a frase tem duas vírgulas e um parêntese, ela vira duas ou três frases.

**2. Proibido empilhar conceitos.** Nunca escreva uma frase no formato "X com Y mais Z (A ou B), vendido como C (D, E, F), com G". Cada um desses itens vira uma frase própria, na ordem em que a pessoa precisa entender.

**3. Toda palavra técnica é explicada na primeira vez que aparece, na mesma frase ou na frase seguinte.** A explicação é em palavras do dia a dia, não em outra palavra técnica. Vale, por exemplo, para: ingrediente ativo, extrato padronizado, probiótico, cepa, eletrólito, aminoácido, GLP-1, massa magra, sachê, pouch, assinatura, laudo, lote, cromatografia, white label, fórmula própria, pedido mínimo, envasadora, margem, CPA, ROAS, LTV, leilão de anúncios, funil, advertorial, awareness, sofisticação de mercado, voz do cliente.

**4. Proibido inventar apelido e usar como se o leitor soubesse.** Expressões como "rota de proteína completa", "prova por fita de medida", "vendido como sistema", "dose verificada", "escada de preço", "porta de entrada", "modelo de mídia", "âncora de preço" e "prova visível" estão proibidas em forma de apelido. Se a ideia importa, ela é explicada em uma frase inteira.

**5. Frase na ordem natural: quem faz, o que faz, para quem.** Nada de começar a frase com um bloco de informação antes do sujeito.

**6. Todo número vem com o que ele significa.** Não basta "460 anúncios ativos". Escreva o número e explique o que ele diz sobre o concorrente.

**7. Sem metáfora, sem frase de efeito, sem travessão, sem ponto e vírgula.** Texto direto. Quando houver três itens ou mais, use lista.

## Exemplo, do jeito errado para o jeito certo

**Errado:** "creme de barreira com ceramidas em proporção verificada mais rota de reparo completo (colesterol e ácidos graxos na fórmula ou sérum complementar), vendido como sistema (dose, protocolo de oito semanas, prova por foto semanal) com assinatura alinhada ao fim do pote."

**Certo:**
"O produto é um creme que a pessoa passa no rosto uma vez por dia, à noite.
Cada pote tem ceramidas, colesterol e ácidos graxos na mesma proporção em que a pele os produz. Ceramidas são as gorduras que seguram a água dentro da pele.
Cada lote de produção é testado em laboratório. O teste confirma que a quantidade escrita no rótulo é a quantidade que está de fato lá dentro.
O creme sozinho não resolve. A pele precisa de um limpador que não tire a gordura natural, e é por isso que o produto vem com uma de duas soluções: um limpador suave dentro do kit, ou a lista dos limpadores compatíveis.
Junto com o creme, a cliente recebe um plano de 8 semanas, com a ordem de uso de cada passo.
Ela recebe também um guia para tirar uma foto por semana, na mesma luz, e enxergar o resultado.
A entrega chega a cada dois meses, quando o pote está no fim."

## O que nunca entra no documento

- Produto, ideia, público ou versão que foi considerado e descartado. Se o descarte explica a decisão, ele vira uma frase na conclusão.
- Explicação de como a pesquisa foi feita, de qual ferramenta foi usada ou de quantas fontes foram lidas.
- Qualquer menção a outro produto do portfólio, a não ser que o relatório seja justamente sobre a comparação entre eles.
- Comentário sobre o próprio documento, sobre versões anteriores ou sobre a conversa com o membro.
- Pergunta como título de seção.

(A regra completa do "só o resultado no doc" está em `.claude/rules/report-only-results.md`.)

## O que nunca pode se perder

Número de concorrente, preço, quantidade de anúncios, avaliações, tamanho e resultado de estudo, frase de cliente em inglês com a tradução ao lado, regra de compliance, ideia de anúncio, preço de venda e pendência. Detalhe é bem-vindo. O que não é bem-vindo é desorganização e assunto que não ajuda a decidir.

## Frases de cliente

Sempre neste formato exato, como item de lista:

`- "frase em inglês exato" Tradução livre: "tradução" (fonte)`

Em tabela, a frase em inglês fica em uma coluna e a tradução na coluna seguinte.

## Teste final antes de salvar

Leia o documento inteiro em voz alta. Em qualquer frase em que você precisar parar, reler ou adivinhar o que uma palavra quer dizer, quebre a frase e explique a palavra. Se uma frase tiver mais de 25 palavras, ela quase certamente precisa virar duas.

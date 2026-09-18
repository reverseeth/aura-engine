# Sourcing · Referência: Due diligence, descoberta e triagem de fornecedores (ETAPA 2)

> Os três sistemas a puxar, a rede ampla com as fontes além do Alibaba, o filtro comportamental do WeChat, os 5 testes de trade company disfarçada de fábrica, a avaliação das respostas, a estrutura de qualidade da fábrica, as amostras rotuladas, os sinais de alerta de `red_flags[]` e a classificação em começar, escalar ou descartar. Abra na ETAPA 2.

### ETAPA 2 — Due Diligence: descoberta e triagem de fornecedores

É onde tudo começa: fundação ruim entrega resultado ruim. Anúncio bonito não é evidência de nada — foto de catálogo e selo de perfil são o que a plataforma vende, não o que a fábrica é.

**Puxe antes desta etapa:**
- **Supplier Screening Funnel** (rode `triagem de 50+ fornecedores filtro WeChat samples rotulados factory A B C`)
- **Trade-Company-Posing-as-Factory Detection** (rode `identificar trade company se passando por fábrica nome cidade certificados Alibaba`)
- **Factory Quality Maturity Assessment** (rode `avaliar estrutura de qualidade da fábrica quality manager DFMEA PFMEA spec sheets na linha`)

**2.1 — Rede ampla, não três links.** O alvo é contatar **50 ou mais** empresas, não 3. O volume é o que ensina o preço real de mercado e o prazo real da categoria — e permite repassar a informação de um pra testar a honestidade do outro.

**Fontes além do Alibaba** (as melhores fábricas de contrato, do nível que produz pra grandes marcas de beleza, **não estão no Alibaba**): base pública de registro da FDA (skincare e dispositivos), associações do setor, **listas de expositores de feiras** do segmento, e LinkedIn (funciona pouco, mas já rendeu achados).

**2.2 — O primeiro filtro é comportamental.** Peça "me adiciona no WeChat" (o aplicativo de mensagens usado por toda a indústria chinesa). Quem não cumpre uma instrução simples na primeira mensagem também não vai cumprir uma especificação de produção. Elimine sem dó.

**2.3 — Os 5 testes de trade company disfarçada de fábrica.** É a situação mais comum do Alibaba, e não é maldade — é o jogo. Rode os cinco:

1. **Nome × cidade** — nome de empresa chinesa quase sempre começa pela cidade. Compare o nome do perfil no Alibaba, o nome nos certificados e o nome na fachada (peça foto/vídeo). Divergiu, é intermediário.
2. **Geografia industrial** — a cidade faz sentido pra categoria? Eletrônico se concentra em Shenzhen e Dongguan; fábrica de exportação fica perto de porto. Cidade no interior distante, sem polo da categoria, é sinal de alerta. Confirme com uma busca por categoria e observe onde os produtores se concentram.
3. **Queda absurda de preço** — preço que despenca pela metade numa negociação indica intermediário: fábrica não tem essa margem pra cortar.
4. **Paradoxo do inglês perfeito** — inglês impecável e papo comercial fluido tende a ser trade company; inglês fraco com domínio técnico profundo tende a ser fábrica. Fábrica responde rápido e com especificidade (tem acesso direto a ficha técnica, certificado e engenheiro); intermediário enrola.
5. **Verifique o certificado com quem emitiu** — peça o certificado, confira se o nome bate com o da empresa, procure o laboratório e ligue perguntando se eles fazem negócio com aquela fábrica. Já se viu certificado emitido pra NOME DIFERENTE do da fábrica que o apresenta.

Identificou? Não descarte automaticamente — em algumas categorias (utensílios de cozinha, brinquedo pet) trabalhar com trade company é praticamente inevitável. Registre o tipo real no `dados.json` e **precifique a decisão sabendo o que está pagando.**

**2.4 — Como avaliar as respostas** (esses são os sinais que separam fornecedor bom de vitrine):
- **Velocidade** de resposta e quantos follow-ups uma pergunta simples exige.
- **Franqueza direta** — a cultura chinesa de negócio costuma falar "em volta"; quem responde direto e rápido é ouro.
- **Profundidade técnica** sobre o produto (não sobre a venda).
- **Porte real**: quantos operadores de linha, tem time dedicado de qualidade, tem equipamento de teste em casa, tem linha automatizada.
- **Acesso direto ao engenheiro** ou tudo passa por vendedor.
- **Transparência**: entrega a lista de materiais e o detalhamento de ingredientes? Quem não entrega, quase sempre é intermediário.
- **Postura proativa**: pergunte "qual o defeito mais estranho que vocês já viram nesse produto e como resolveram? Qual o plano pra isso não acontecer comigo?". Fabricante que avisa do problema antes de você descobrir é raro e vale muito.

**2.5 — Estrutura de qualidade da fábrica** (perguntas que separam quem tem sistema de quem tem discurso): existe um gerente de qualidade e com quem ele fala? Existe pessoal DEDICADO à qualidade (engenheiro "de vários chapéus" não conta)? Eles fazem análise preventiva de falha de projeto e de processo? Como as fichas técnicas são trocadas na linha quando muda o produto, e quem é o responsável? Fábrica com documentação impecável ainda exige que você entenda o que está lendo — profissionalismo aparente também é risco.

**2.6 — Amostras rotuladas.** Peça amostra de 3 a 5 finalistas, **rotule como Fábrica A / B / C / D** e teste em planilha por critério fixo da categoria (skincare: cheiro, textura, eficácia; eletrônico: mapear defeitos possíveis, desempenho, durabilidade — incluindo teste de queda). Consolide os envios num endereço só. **Produto que falha no seu próprio teste falharia no cliente, com review pública.**

**Sinais de alerta que bloqueiam (registre em `red_flags[]`):**
- Resposta vaga sobre o processo de produção (sem transparência).
- Resposta lenta ou vários follow-ups pra pergunta simples — prevê como as crises vão ser conduzidas.
- "Não se preocupe, a gente resolve depois" num problema de protótipo. Resolva ANTES do molde de dezenas de milhares de dólares.
- Inflexibilidade e falta de cooperação — custa lançamento, alocação de linha e ajuste de fornecedor.
- Certificação ausente = inexperiência na categoria ou canal de venda inviável.
- **Quem GARANTE redução de preço sem explicar como.** Costumam flexibilizar qualidade (componente de segunda linha no lugar do de primeira) pra cumprir a promessa. Exija o plano de COMO o preço vai cair.

Classifique cada candidato: **começar** (pedido mínimo baixo, resposta rápida, frete simples) vs **escalar** (fabricante real, OEM/ODM, preço que despenca no volume) vs **descartar** (com o motivo).

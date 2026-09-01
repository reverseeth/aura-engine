---
name: sourcing
description: Fornecedor, cotação, qualidade e condições de pagamento do produto físico. Use quando o membro disser "sourcing", "fornecedor", "supplier", "cotação", "Alibaba", "3PL", "frete da China", "fábrica", "MOQ", "payment terms", "prazo de pagamento", "inspeção", "QC", "defeito", "compliance", "Chinese New Year", ou quando um produto escolhido precisar de custo real antes da oferta. Explica a operação em linguagem simples, faz due diligence do fornecedor (inclusive identificar trade company disfarçada de fábrica), monta a mensagem de cotação, cobra compliance por categoria, negocia condições de pagamento e incoterm, arma o sistema de qualidade (golden sample, QC ponta a ponta, taxa de defeito) e entrega o custo real pro COGS da Skill 04.
---

# Sourcing Engine

## Quando Usar

Depois que o produto foi escolhido (Skill 01) e antes da oferta ter custo real (Skill 04). É uma fase **opcional e paralela**: pode rodar ao mesmo tempo que as Skills 02/03 (a pesquisa não depende do fornecedor). Membro com fornecedor privado ou operação dropship usa as partes que servem (cotação, condições de pagamento, qualidade, logística, comparação) e pula o resto.

O objetivo de saída: **fornecedor escolhido + custo por unidade real + condições de pagamento acordadas + plano de qualidade + rota logística definida** — o pacote que transforma o COGS estimado da Skill 04 em COGS de verdade, e que decide quanto caixa o membro tem livre pra comprar tráfego.

**Duas alavancas dominam esta skill**, e as duas costumam ser ignoradas por quem está começando:

1. **Condições de pagamento** (quando você paga, não só quanto paga). É a alavanca número 1 de caixa: mais caixa livre = mais verba de anúncio = mais escala. Pausar anúncio por falta de caixa custa caro duas vezes, porque depois é preciso reotimizar a campanha do zero.
2. **Taxa de defeito** (quantas unidades chegam com problema). Cada ponto percentual a menos de defeito vale de 3% a 6% de margem de lucro — mais do que a maioria das negociações de preço entrega.

Quem fecha uma cotação sem tocar nessas duas fecha metade do trabalho.

## Base de conhecimento (NUNCA query genérica)

Esta skill puxa **SISTEMAS NOMEADOS** de supply chain e sourcing da base — nunca query genérica do tipo "fornecedor" ou "sourcing". Em cada ETAPA abaixo, rode `search_knowledge` (com `deep=true`) usando a `best_query` **exata** de cada framework listado ali, e puxe o sistema completo (ex: os 5 testes de trade company disfarçada de fábrica, não "dicas de Alibaba").

**Índice completo do domínio desta skill (`supply-chain-sourcing`, 36 sistemas): `.claude/lib/kb-index/`** — `frameworks.json` (machine-readable) e `README.md` (mapa skill → domínio). Os sistemas de maior impacto já estão NOMEADOS dentro de cada ETAPA. Alguns deles são compartilhados com outras skills (compliance e defeito também alimentam a 01 e a 04; packaging também alimenta a 04 e a 07a) — quando esta skill os puxa, o recorte é sempre a decisão de fornecedor.

## Antes de Começar

0. **Idioma do relatório (rule 0 — INVIOLÁVEL)**: leia `report_language` de `workspace/profile.md` (default `pt-BR`). Todo output interno e conversa com o membro usam esse idioma. A mensagem de cotação pro fornecedor é em **inglês** (é comunicação comercial externa, não copy de consumidor).
1. Leia `workspace/profile.md` — em especial a seção de sourcing (fornecedor privado? preferência de produto simples? verba disponível).
2. Leia `workspace/[produto]/manifest.json` e o output da Skill 01 (produto escolhido, formato, mecanismo pretendido) — a cotação precisa perguntar EXATAMENTE o que o posicionamento promete (dose, material, duração, especificação).
3. **Identifique a categoria** (skincare, suplemento, eletrônico/gadget, vestuário, pet, casa). A categoria decide três coisas ao longo da skill: quais testes de conformidade são obrigatórios (ETAPA 5), qual rota de produto é realista (ETAPA 3) e qual taxa de defeito é esperada (ETAPA 10).
4. **Cheque a data de hoje contra o calendário chinês** (ETAPA 12). Entre novembro e março, o Ano Novo Chinês muda TODAS as recomendações de prazo desta skill — e é o erro mais caro que um membro comete no primeiro pedido.
5. Quando precisar checar algo na web (cidade da fábrica × categoria, número de registro em base pública, reputação de laboratório), vale a `.claude/rules/resilient-fetch.md`: descoberta pela tool `WebSearch`, aprofundamento pelo fetcher da Aura. **Nunca invente um dado de verificação que você não conseguiu confirmar** — registre como pendência.

## Fluxo da Skill

### ETAPA 0 — Pré-flight

1. Se `workspace/profile.md` ou o `manifest.json` do produto não existirem, ofereça rodar o `setup` inline antes de seguir. Se houver mais de um manifest com `setup_complete: true` e o membro não nomeou o produto no pedido, liste os `product_name` e pergunte em 1 linha qual é o alvo.
2. Identifique o que o membro JÁ tem: links de anúncio (Alibaba/1688/AliExpress), fornecedor privado com contato, cotações antigas, pedido já colocado, nada. A skill entra no ponto certo — não repete o que está feito.
3. Se `sourcing/dados.json` já existe, leia e continue de onde parou (a skill é reentrante: cotação enviada numa sessão, comparação em outra, qualidade em outra).
4. **Se o membro já tem fornecedor e já fez pedido**, o valor desta skill muda de lugar: pule as ETAPAs 2-6 e entre direto nas ETAPAs 8 (condições de pagamento), 10 (qualidade e taxa de defeito) e 12 (calendário e prevenção de ruptura de estoque). São as três que rendem dinheiro em operação já rodando.
5. Se a Skill 04 já rodou com custo estimado, anote: o fechamento desta skill atualiza o `cogs_breakdown` de lá (ETAPA 13).

### ETAPA 1 — A Operação Explicada (linguagem simples, sempre incluir no relatório)

O membro não é comprador profissional. Antes de qualquer análise, o relatório explica os termos da operação como se fosse a primeira vez — ele relê quando precisar. Adapte os exemplos ao produto dele.

**Puxe antes de escrever esta etapa:**
- **4 Supplier Types Framework** (rode `4 tipos de fornecedores factory trade company dropshipping agent sourcing company`)
- **Factory Size Selection** (rode `porte de fábrica pequena média 100-200 pessoas grande MOQ acesso a engenheiro`)
- **Incoterms as Payment Clock** (rode `incoterms EXW FOB DDP quando o relógio dos net terms começa effective payment terms`)

**Com quem você está falando de verdade — os 4 tipos de fornecedor:**

| Tipo | O que é | A favor | Contra |
|---|---|---|---|
| **Fábrica** | Quem produz. Divide-se em fábrica de componente (plástico, garrafa, bateria, placa) e fábrica de montagem — a de montagem é com quem você fala | Preço mais baixo, engenheiros próprios, customização de verdade | Pedido mínimo mais alto; produz UMA categoria só; volume pequeno não é prioridade; inglês fraco; pouca transparência sobre os fornecedores dela |
| **Trade company** (empresa comercial) | Escritório que não fabrica nada e revende de uma rede de fábricas. Muito comum no Alibaba | Variedade dentro da categoria, inglês fluente, pedido mínimo menor; algumas fábricas só vendem por elas | Preço maior (margem embutida e invisível); se apresenta como fábrica; customização e resolução de defeito mais lentas (camada extra de telefone-sem-fio) |
| **Agente de dropshipping** | Armazém + escritório de compras: acha o produto e despacha pedido a pedido | Pedido mínimo de 50-100 unidades (ótimo pra testar venda), qualquer categoria, cotação em menos de 24h | O negócio deles é despachar volume, não cuidar do produto: due diligence fraca, costumam comprar de trade company (DUAS camadas de margem escondida), evitam customização real, nem sempre usam fábrica em conformidade |
| **Sourcing company** (empresa de sourcing) | Time de pesquisa com rede ampla de fábricas, sem amarra de categoria | Due diligence forte, representa a SUA marca na China, negocia preço e prazo de pagamento em seu nome, visita a fábrica, ajuda no planejamento de compra | Depender demais dela (ela controla a conversa com o fornecedor); e uma sourcing company ruim é só uma trade company disfarçada |

**Régua da taxa suspeita:** sourcing company cobrando **5%** raramente fecha a conta pelo trabalho que faz — quase sempre há margem escondida no preço; na comparação real elas costumam sair 5% a 15% mais caras do que anunciam. Peça o modelo de remuneração por escrito antes de começar.

**O porte da fábrica muda o que você consegue:**
- **Pequena** (até 50-75 pessoas): faminta por negócio, dá atenção especial — mas com poucos recursos, engenheiro ocupado e produção mais lenta. Só compensa pra quem já tem experiência.
- **Média** (cerca de 100 a 200 pessoas): melhor preço (sistemas mais eficientes) e mais recursos de teste e controle de qualidade. **É o melhor ponto de partida pra maioria.**
- **Grande** (200 ou mais): capacidade enorme, mas pedido mínimo altíssimo, fila de produção e processos internos que impedem acesso direto ao engenheiro. Só com volume muito alto.

**Sobre o fornecedor (vocabulário da conversa):**
- **MOQ (pedido mínimo)** — a quantidade mínima que a fábrica aceita produzir. "MOQ 500" = ela só produz a partir de 500 unidades.
- **OEM** — a fábrica produz a fórmula/produto DELA com a SUA marca na embalagem. O caminho mais comum pra começar.
- **ODM** — a fábrica desenvolve um produto NOVO ou ajustado pra você (sua fórmula, sua especificação). Mais caro, pedido mínimo maior, mais controle. Detalhado na ETAPA 3.
- **Private label / white label** — nomes comerciais pro mesmo conceito do OEM: produto pronto de fábrica, rótulo seu.
- **Spec sheet (ficha técnica)** — cada ingrediente/material COM quantidade, dimensões, peso. Sem ficha técnica completa, não há pedido.
- **BOM (lista de materiais)** — a lista de todos os componentes com o custo de cada um. Fábrica que entrega a lista está mostrando onde ganha dinheiro; quem se recusa, quase sempre é intermediário.
- **CoA (laudo do lote)** — o laudo de laboratório de cada lote provando que o que está no rótulo está no produto. É o documento que sustenta claims na página.
- **GMP / GMPC** — certificação de boas práticas de fabricação (limpeza, controle de qualidade, gestão de produção). O mínimo aceitável pra qualquer coisa que encosta no corpo.
- **Lead time (prazo de produção)** — o prazo entre aprovar a arte e ter o produto pronto pra embarcar.
- **Sample (amostra)** — custa pouco e evita comprar volume de um produto que você nunca tocou.
- **COGS** — o custo total pra ter 1 unidade pronta pra vender: produto + frete + impostos de importação, tudo somado. É o número que define quanta margem sobra pra pagar anúncio.

**O frete internacional — e o detalhe que quase ninguém vê: o incoterm também define QUANDO você paga.**

O incoterm (o regime de entrega) não decide só quem paga o frete. Ele decide **de que momento começa a contar o prazo de pagamento** que você negociar. "Pagar em 30 dias" significa coisas muito diferentes em cada regime:

| Regime | Quem faz o quê | Quando o relógio do prazo começa |
|---|---|---|
| **EXW (na porta da fábrica)** | Preço do produto na porta da fábrica; você organiza todo o frete | Na saída da fábrica |
| **FOB (posto no porto)** | A fábrica entrega no porto e carrega o contêiner; você assume dali | Na entrega ao porto |
| **DDP (entregue com impostos pagos)** | Serviço porta a porta: frete + desembaraço + imposto + entrega no armazém, tudo num preço só | Na entrega no seu armazém |
| **DDU / DAP** | O fornecedor entrega no destino, mas os impostos de importação chegam DEPOIS, de surpresa, pro destinatário pagar | Regime a evitar quando se está começando |

**Por que isso vale dinheiro:** o mesmo "pago em 30 dias" no regime DDP dá muito mais fôlego de caixa que no regime EXW, porque no DDP a contagem só começa quando a mercadoria já está no seu armazém (perto de virar venda), enquanto no EXW ela começa com a carga ainda tendo semanas de mar pela frente. Ao comparar duas propostas, compare o prazo EFETIVO (prazo negociado + tempo de trânsito), nunca o prazo nominal. **FOB costuma ser melhor que EXW** pra carga de contêiner: o transporte terrestre sai mais barato pela fábrica, o desembaraço de exportação fica resolvido, o risco até o porto é deles, e às vezes o preço até melhora (a fábrica recebe incentivo de exportação).

**Sobre quem guarda e envia o produto (as 4 rotas):**

| Rota | O que é | Prós | Contras |
|---|---|---|---|
| **Dropship direto** | O fornecedor envia da China pro cliente final, pedido a pedido | Zero estoque, zero risco de capital | Entrega de 1-3 semanas mata review e recompra; sem controle de unboxing |
| **3PL** | Um armazém terceirizado no país de venda recebe seu estoque e envia cada pedido por você (ex. nos EUA: ShipBob, ShipMonk) | Entrega rápida local, unboxing seu, você nunca toca no produto | Custo por pedido (separação e embalagem) + mensalidade de armazenagem |
| **FBA (Amazon)** | O 3PL da Amazon — obrigatório pra vender com Prime | Logística resolvida dentro da Amazon | Taxas maiores, regras rígidas, faz sentido só se o canal Amazon importa |
| **Estoque em casa** | Você mesmo recebe e envia | Custo mínimo, controle total | Vira seu trabalho diário; não escala |

**O caminho recomendado pra loja própria vendendo nos EUA: comprar da China SEM "mandar da China"** — pedir envio **DDP direto pro 3PL americano**. O produto sai da fábrica e entra no armazém; o cliente recebe em 2-5 dias com a sua embalagem; o membro nunca toca uma caixa.

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

### ETAPA 3 — Rota do Produto (define prazo, orçamento e risco)

Antes de cotar, decida qual das três rotas o produto exige. Elas têm prazos e orçamentos incomparáveis, e escolher a errada é o que faz um lançamento atrasar meses.

**Puxe antes desta etapa:**
- **Parallel Multi-Sourcing Formula Method** (rode `fórmula custom multi-sourcing paralelo 15-20 samples scent texture effectiveness`)
- **ODM Product Development Pipeline** (rode `ODM eletrônicos concept industrial design tooling prototyping mass production`)
- **Component Lead-Time Sequencing** (rode `lead time de matéria-prima por componente baterias 45 dias plásticos 20 dias`)

**Rota A — Estoque pronto / rótulo seu (white label).** Produto que já existe no catálogo da fábrica, com a sua marca na embalagem. É a rota default pra validar com dinheiro pequeno. Prazo: o da produção da embalagem, não do produto.

**Rota B — Fórmula própria (skincare, suplemento).** Três caminhos: (a) replicar um produto concorrente; (b) replicar e acrescentar ingredientes — o mais comum, porque é o que cria diferenciação; (c) fórmula 100% do zero (exige químico contratado; dá mais controle e propriedade da fórmula, mas a fábrica ainda vai ajustar pela disponibilidade de ingrediente).

O método que acelera: peça amostra a **3-5 fábricas, cada uma com 2-5 variações** — 15 a 20 produtos na mesa. Avalie cheiro, textura e eficácia, monte um ranking das variações E dos fornecedores, e afunile de 5 para 2 fábricas. Trabalhar com uma fábrica só é o risco de nenhuma amostra prestar e recomeçar do zero.

**O gargalo é a garrafa, não a fórmula.** Decida cedo entre rótulo adesivo e impressão direta no frasco (ETAPA 11), e obtenha as linhas de corte (o desenho técnico do frasco e da caixa) pro designer trabalhar. Prazos reais da primeira ordem: garrafa com impressão direta cerca de 30 dias, caixa 10-15 dias, envase e montagem 10-15 dias — **total de 40 a 50 dias na primeira ordem** (o mínimo já alcançado fica perto de 30). A maior alavanca de prazo é **comprar o dobro de garrafas na primeira ordem**: a segunda ordem cai pra cerca de 25 dias e passa a caber no ciclo mensal de compra do ecommerce.

Da pesquisa de fornecedor ao início da produção: de 6 semanas a 3 meses. O caso mais rápido (8 semanas) foi replicação direta de um produto existente corrigindo o que os clientes reclamavam, escolhendo entre 20 amostras.

**Rota C — Produto novo com molde próprio (ODM, tipicamente eletrônico).** É outro esporte. Sequência: conceito e desenho → design industrial (forma e ergonomia) → design estrutural (arquivos 3D) → protótipo impresso em 3D → protótipo usinado → **molde** → produção piloto → produção em massa. Com packaging correndo em paralelo ao molde.

Ordens de grandeza pra dizer ao membro antes que ele se comprometa: **US$ 50 mil a 100 mil antes de fabricar a primeira unidade** (taxas de desenvolvimento, protótipos de até cerca de US$ 1.000 cada em várias rodadas, e **molde de US$ 20 mil a 70 mil** conforme a complexidade), e **lançamento em 9 a 12 meses**. Negocie pagamento por fase: "se eu não aprovar o protótipo, não pago o desenvolvimento". Depois que o molde é aberto, o produto está travado — mudança depois disso custa meses.

**Risco de propriedade intelectual (o alerta que não pode faltar no relatório):** se a fábrica fizer o design industrial sem acordo prévio, **ela pode ficar dona do seu registro de desenho industrial na China** e você fica travado com ela. Antes de deixar a fábrica desenhar qualquer coisa, é preciso acordo de propriedade intelectual por escrito, com advogado da área.

**Em qualquer rota, sequencie os componentes pelo mais lento.** Bateria leva cerca de 45 dias contra cerca de 20 de plástico e eletrônico comum — encomendar tudo junto significa esperar o mais lento sem necessidade. Ingrediente importado (ativo francês, biotina) e frasco com impressão direta entram na mesma conta.

### ETAPA 4 — Mensagem de Cotação (inglês, pronta pra enviar)

Monte UMA mensagem com os 9 blocos abaixo, adaptada ao produto (a mesma pra todos os canais — chat do Alibaba, fornecedor privado, agente). Cotação boa é a que força o fornecedor a responder o que o anúncio esconde:

**Puxe antes:** **Target Price Rule + Phase-Gated Payments** (rode `sempre dê target price para a fábrica formular dentro do orçamento derivar do CAC`).

1. **SPEC SHEET** — lista completa de ingredientes/materiais COM quantidades por unidade. Se o posicionamento depende de um número (dose, gramatura, potência), pergunte EXPLICITAMENTE se há versões diferentes em estoque e o custo de ajustar só esse número.
2. **PERFORMANCE** — o dado que sustenta a promessa central (duração, liberação, resistência, capacidade — o que o mecanismo do produto promete).
3. **MATERIAL DE CONTATO** — do que é feito o que encosta no cliente (adesivo, tecido, plástico): segurança, resíduo, reclamações de irritação.
4. **TARGET PRICE + BILL OF MATERIALS** — **sempre declare um preço-alvo por unidade.** As fábricas usam o alvo pra formular DENTRO do seu orçamento, não pra extrair margem; sem alvo, elas chutam alto ou entregam algo que não fecha a sua conta. O alvo se deriva da economia da oferta (quanto o produto precisa custar pra o custo de aquisição de cliente caber na margem), não de "o mais barato possível". Peça junto a lista de materiais com custo por componente — quem entrega está mostrando onde ganha dinheiro.
5. **COUNT & PACKAGING** — unidades por embalagem no padrão de fábrica; capacidade de produzir a SUA embalagem impressa; efeitos de acabamento disponíveis e o que cada um adiciona por unidade; preço unitário em 3-4 degraus de quantidade.
6. **COMPLIANCE** — exporta regularmente pro país de venda? Certificações e testes exigidos pela categoria, um a um, com o nome do laboratório que emite (a lista da ETAPA 5), laudo por lote em laboratório terceiro, orientação de rótulo conforme a regulação local, validade.
7. **SAMPLES & LEAD TIME** — custo e prazo da amostra; prazo de produção após aprovar a arte; **prazo de cada matéria-prima separadamente** (é o que revela o componente mais lento); calendário de parada da fábrica no próximo Ano Novo Chinês.
8. **PAYMENT TERMS** — qual a condição padrão deles, o que muda com previsão de compra declarada, e o que precisa ser demonstrado pra abrir prazo. Perguntar na primeira mensagem não fecha nada, mas ancora a conversa e revela quem tem flexibilidade (ETAPA 8).
9. **SHIPPING** — cotação **DDP** até o endereço do 3PL, em 2 quantidades (ex: 500 e 1.000 unidades): custo, prazo de trânsito, e a alternativa FOB pra comparação (a diferença entre as duas é o que você está pagando pela conveniência).

Feche com pressão saudável: "We're comparing suppliers and will order from whoever answers these points clearly."

### ETAPA 5 — Compliance por Categoria (o que exigir e como verificar)

Conformidade não é custo, é seguro: a alfândega pode APREENDER produto irregular, e marketplace exige documentação até pra criar anúncio. Circula muita desinformação em grupo de ecommerce — o relatório traz a lista real da categoria do membro.

**Puxe antes:** **Category Compliance Matrix + Big Three Labs** (rode `compliance por categoria skincare supplements eletrônicos FDA GMPC FCC UL CE`).

**Skincare.** *Fábrica registrada na FDA* (a agência americana de alimentos e medicamentos) **não é a mesma coisa** que *produto aprovado pela FDA* — registro é cadastro em base de dados com número; aprovação é outro processo, de eficácia. Vender "aprovado pela FDA" com base num registro é falso. Certificação de boas práticas de fabricação de cosmético e quatro testes: microbiologia (bactéria e fungo), estabilidade (validade real), compatibilidade (fórmula × embalagem, pra não haver reação química com o frasco) e teste de conservantes. País de origem é obrigatório no rótulo.

**Suplemento.** Registro da fábrica na FDA (a responsabilidade final é SEMPRE da marca, nunca da fábrica), notificação de ingrediente novo quando aplicável, alegação de alergênico e vegano só com prova. Testes: microbiologia, **metais pesados** (chumbo e mercúrio entram pela extração, pelo solvente ou pelo maquinário), teste de identidade dos ingredientes, e **laudo por lote em laboratório terceiro** (5 a 7 dias úteis na China). Nunca confie apenas no laudo interno da fábrica.

**Eletrônico.** Certificação de emissões de rádio e interferência é obrigatória e leva cerca de 2 semanas — **faça ANTES da produção** (já houve brinquedo de pelúcia que emitia som e precisou da certificação, descoberto às vésperas do embarque). Certificação de segurança elétrica é tecnicamente opcional e efetivamente obrigatória (marketplaces exigem; o órgão emissor audita fábrica e controla os selos). Na Europa, marcação CE com as diretrizes de substâncias químicas e restrição de materiais perigosos — que valem inclusive pra EMBALAGEM produzida na China e enviada pra envase na Europa. Teste de queda, e **documentação de segurança de bateria de lítio**: sem ela, a carga não embarca de avião, e isso sozinho mata um lançamento.

**Vendendo na Amazon.** Código de barras oficial (compre logo — é barato e rápido, e a troca de 3PL trava sem ele; fulfillment chinês ignora o código e isso vira armadilha), ficha de segurança do produto, relatórios de teste, e carta de autorização entre marca e fábrica com os números de registro.

**Laboratórios terceiros — os três grandes:** SGS (o mais reconhecido globalmente), Intertek (inclusive segurança elétrica) e Eurofins (forte em microbiologia e química, o mais usado em suplemento e skincare). Reserve **US$ 2.000 a 10.000** de orçamento de testes e peça cotação aos três (escopo, preço e prazo variam bastante). Termine TODOS os testes antes do embarque. Consultoria de graça: os laboratórios têm especialista por categoria que funciona como braço comercial — pedir cotação já rende a lista exata de testes que o produto exige.

**Verificação (não aceite o PDF e siga em frente):** peça o número de registro e procure na base pública; ligue pro emissor perguntando se ele produz pra quem diz produzir; confirme se a certificação está vigente (troca de gestão ou de máquina tira a fábrica de conformidade rápido); exija laudo de laboratório terceiro, não interno.

**Sinal de alerta:** preços diferentes "com certificado" e "sem certificado" da mesma fábrica não fazem sentido — a fábrica é registrada ou não é. Isso é intermediário vendendo papel.

Certificação leva de 1 a 3 meses: coloque no cronograma do lançamento desde já, não depois.

### ETAPA 6 — Agentes de Sourcing Parceiros da Aura

Quando o membro precisa de mais do que um anúncio do Alibaba — produto custom, negociação de preço, inspeção de fábrica, consolidação de mais de um fornecedor num embarque só — a Aura tem agentes de sourcing parceiros na China. Contato direto por WhatsApp, conversa em inglês:

| Agente | WhatsApp |
|---|---|
| Yohn Ding | +86 185 5268 5200 |
| Josie | +86 193 2642 1242 |
| Brain Lee | +86 178 3718 2265 |
| Mark | +86 193 9607 4873 |

**Quando o agente vale a pena:** (a) o produto exige customização que anúncio de estoque não cobre; (b) o volume justifica negociar direto com fábrica; (c) o membro quer inspeção antes do embarque (agente visita a fábrica e confere o lote); (d) vários itens de fornecedores diferentes num contêiner só; (e) o membro quer herdar condições de pagamento que sozinho não conseguiria (ETAPA 8).

**Como abordar:** mandar a mesma mensagem de cotação da ETAPA 4 + 1 parágrafo de contexto (produto, mercado de venda, volume inicial pretendido). O agente cobra comissão sobre o pedido ou taxa por serviço — **pergunte o modelo na primeira conversa e aplique a régua da taxa suspeita da ETAPA 1.** Um parceiro com presença legal na China assina contrato localmente válido, o que importa: contrato internacional entre empresa americana ou europeia e fábrica chinesa vale, na prática, pouco mais que uma sugestão no papel.

### ETAPA 7 — Comparar Cotações e Decidir

Quando as respostas voltarem, monte a tabela comparativa (uma linha por fornecedor):

| Fornecedor | Tipo real | Custo/un | MOQ | Incoterm | DDP até o 3PL | Prazo | Ficha técnica | Lista de materiais | Compliance | Condição de pagamento | Papel |
|---|---|---|---|---|---|---|---|---|---|---|---|

- **Fornecedor de COMEÇO** ≠ **fornecedor de ESCALA** — e está tudo bem ter os dois. Começo: pedido mínimo baixo, frete simples, entrega rápida (validar com dinheiro pequeno). Escala: fabricante real, preço que cai no volume, OEM completo (migrar depois que o produto vende).
- **Critério de transparência como desempate:** entre duas propostas parecidas, ganha quem entregou o detalhamento de ingredientes ou a lista de materiais. Quem não entrega quase sempre é intermediário, e você vai descobrir isso mais tarde e mais caro.
- **Desconfie de quem GARANTE preço menor sem explicar a origem da redução** (sinais de alerta da ETAPA 2).
- **Antes de qualquer pedido de volume: amostras.** Peça de 2-3 finalistas e TESTE pessoalmente no uso real do produto.
- **Compare prazo de pagamento EFETIVO, não nominal** (ETAPA 1): prazo negociado + tempo de trânsito do incoterm.
- Checagem de sanidade da margem: custo desembarcado (produto + frete rateado + imposto) ÷ preço de venda pretendido — abaixo de cerca de 30% do preço de venda é confortável pra tráfego pago; acima disso, renegociar ou repensar preço (a régua fina é da Skill 04).

### ETAPA 8 — Condições de Pagamento e Incoterm (a alavanca nº 1 de caixa)

Cada dia que você paga mais tarde é um dia de caixa livre pra comprar tráfego. Esta etapa vale mais que a maioria das negociações de preço, e é a que ninguém faz.

**Puxe antes desta etapa:**
- **The 3 Negotiation Moments** (rode `3 momentos certos para negociar com fábrica forecast 3 6 12 meses payment terms`)
- **Rolling Deposit** (rode `rolling deposit 10-30% permanente aperto de mão financeiro matéria-prima forecast`)
- **Creative Payment Structures** (rode `pay-as-you-ship fábrica estoca line of credit $500k limite $250k net 30`)
- **Duty Cash-Flow Levers** (rode `Periodic Monthly Statement CBP free trade zone pagar duty só ao internalizar tarifas`)
- **Logistics Net Terms** (rode `net 30 com freight forwarder pagar fulfillment semanal em vez de por ordem`)
- **Tariff-as-Leverage Negotiation** (rode `tarifa como argumento de negociação com a fábrica leniência desconto extended terms`)
- **Guanxi Supplier Relationship System** (rode `guanxi relacionamento com fornecedor chinês cliente favorito visitas KTV jantar`)

**A regra dura, antes de tudo: NUNCA pague 100% adiantado.** Nunca, em nenhum cenário. Com tudo pago, uma inspeção final que encontra problema te deixa sem nenhuma alavanca — e ainda pagando frete aéreo pra salvar o lançamento. Pra quem está testando fábrica direta em pedido pequeno, a plataforma de pagamento do próprio Alibaba serve de proteção e arbitragem (deixa de fazer sentido em volume grande).

**Os 3 momentos certos de negociar** (negociar o tempo todo desgasta e piora o resultado):

1. **Antes da 1ª ordem** — entenda o prazo de cada componente e negocie que **velocidade e qualidade também são moeda**, não só preço. O jeito que funciona é ser genuinamente simpático e perguntar: "pago o depósito amanhã, dá pra melhorar um pouco?" — e observar a reação. Apresente o futuro sem exagerar: fabricante chinês pensa de forma transacional e de curto prazo, e promessa inflada destrói confiança.
2. **Na 1ª ordem (ou logo depois)** — entregue a **previsão de compra de 3, 6 e 12 meses**. Isso deixa a fábrica preparar linha, gente e fornecedores dela, e é o que abre a conversa de reduzir prazo e custo (em skincare: quais matérias-primas ela mantém em estoque pra você; em eletrônico: com componente em casa, algumas fábricas montam em uma semana — é o caminho real pro "prazo de 7 dias" que os anúncios prometem).
3. **Depois da previsão cumprida (algumas ordens depois)** — aí sim negocie **prazo de pagamento**: sair do padrão 30% adiantado / 70% antes do embarque para algo como **30% depósito / 40% no embarque / 30% em 30 dias após o embarque**. Quanto mais séria a previsão demonstrada, mais receptivos.

**Credibilidade vem antes do prazo.** Marca de sucesso com fornecedor NOVO não ganha prazo de cara — pedir cedo demais até azeda a relação. Espere ter que provar: demonstrativo financeiro, histórico de vendas, análise de crédito. Se a fábrica resistir, faça a pergunta certa: **"o que eu preciso provar ou entregar pra destravar o próximo degrau?"** É um jogo de aproximação contínua.

**Modelos além do 30/70:**

| Modelo | Como funciona | Pra quem |
|---|---|---|
| **Depósito rotativo** | Você deixa 10-30% permanentes na fábrica cobrindo matéria-prima da sua previsão; a cada embarque paga 100% daquela ordem (ou em 15/30 dias) e o depósito continua lá | Quem compra com regularidade e quer a fábrica sempre com material comprado |
| **Pague conforme embarca** | Deposita sobre um volume grande (ex: 30.000 unidades vendendo 10.000/mês); a fábrica produz e ESTOCA por conta dela; você paga o saldo por lote conforme manda embarcar | Multi-produto; garante reposição instantânea se um item estourar |
| **Linha de crédito** | Limite de crédito com prazo — ex: US$ 500 mil em ordens com limite de US$ 250 mil a 30 dias: paga metade adiantado e flutua o resto | Quem já tem histórico; define exposição previsível pros dois lados |

Caso real de linha de crédito: durante o desenvolvimento de produtos novos (taxas de desenvolvimento, amostras, certificações e molde, tudo sem receita entrando), a marca condicionou — "pra continuarmos desenvolvendo com vocês, precisamos de linha de crédito nas ordens atuais" — e conseguiu prazo significativo, lançando vários produtos no mesmo ano. Uma visita presencial com apresentação formal (volume anual, explicação do custo de aquisição de cliente em linguagem que a fábrica entenda, potencial de crescimento se o caixa destravar) já rendeu **20% de depósito com saldo em 60 dias após o embarque** numa marca de skincare.

**A fábrica avalia risco por categoria, e isso decide o que ela pode conceder:** fórmula própria de skincare usa ingrediente comprado só pra você — se suas vendas caem, ela fica com material inutilizável, então o prazo é mais duro. Gadget de rótulo próprio usa material compartilhado entre várias marcas, o risco é menor e o prazo é melhor. Saber disso muda o pedido pra algo aceitável.

**Alternativa quando o prazo não vem:** peça que a fábrica invista em **cortar o prazo de produção** (de 20 para 7 dias, por exemplo). Você compra menos por vez, e o caixa respira igual.

**Volume emprestado (group buying).** Uma sourcing company que representa mais de 100 marcas consolida compras nas mesmas fábricas e ganha condições que você sozinho não teria — e pode estender a você. Vale o mesmo pra empresa de fulfillment que faz sourcing. **Cobre isso delas**: "por que vocês não estão me repassando prazo? Levem numa fábrica da rede que dê." A alavanca é real, porque você sempre pode fazer o sourcing por conta própria ou trocar de parceiro.

**Onde mais existe prazo (e quase ninguém procura):**
- **Imposto de importação em fatura mensal** — trocar o débito automático de tributos pelo extrato mensal do órgão aduaneiro libera caixa E dá tempo de auditar se a cobrança está certa. É prazo de pagamento pros seus impostos.
- **Zona franca** — com tarifa instável, mandar pra zona franca e pagar o imposto só ao internalizar a mercadoria (exige contrato e papelada ANTES do embarque, e regras a cumprir).
- **Prazo com o transportador** — com embarques mensais de volume, negocie 30 dias sobre o frete dos últimos 30 dias.
- **Prazo com a empresa de fulfillment** — o custo de fulfillment **muitas vezes supera o custo do produto**. Pagar semanal ou quinzenal em vez de por pedido pode liberar mais caixa que a negociação com a fábrica.
- **Tarifa como argumento** — "meu custo era X e virou Y com a tarifa paga adiantado no desembaraço, preciso de leniência" abre desconto ou prazo estendido; as fábricas sabem que afeta todo mundo.

**Relacionamento não é decoração, é preço.** Na China, negócio e amizade se misturam de propósito, e a relação converte em prioridade, preço, prazo e favor. A meta não é ser o cliente número 1, é ser **o cliente favorito**: consistência de pedido, previsão realista, visita presencial (problema que arrasta por semanas no chat se resolve numa tarde na fábrica), e aceitar a cultura do jantar. Se a fábrica faz um produto ótimo mas a relação não flui, procure outra que faça o mesmo produto — você vai conviver muito com essas pessoas.

### ETAPA 9 — Contratos Mínimos Antes de Produzir

Conformidade sem contrato deixa toda a responsabilidade com você. Não force todos os contratos no dia 1 (cria atrito) — priorize pelo risco do produto e feche **antes da produção**. Quando é o que você precisa pra ganhar o negócio, eles assinam.

**Puxe antes:** **Manufacturer Agreement Stack** (rode `MSA brand authorization letter produção paralela AQL defect tolerances waivers`).

1. **Acordo de fabricação (MSA)** — exige por escrito que a fábrica siga os passos de conformidade acordados (laboratórios específicos, certificados legítimos). É o que permite repassar multa e prejuízo: certificado falsificado passa a ser responsabilidade contratual dela.
2. **Carta de autorização de marca** — a fábrica só produz a sua marca mediante os seus pedidos de compra. Evita produção paralela e fornecedores dela oferecendo o seu produto a terceiros ("faço um monte dessa caixa, quer produzir esse produto?"). **E é fiscalizada na exportação chinesa**: já houve embarque de produto licenciado flagrado e **bloqueado no porto** por falta da carta, resolvido só com escalonamento de urgência. Não é burocracia opcional.
3. **Qualidade dentro do contrato** — procedimentos de inspeção (pré-produção, durante a linha e antes do embarque), **tolerância de defeito acordada por escrito**, plano de ação corretiva, e responsabilidade por defeito (desconto na fatura seguinte). Critério aceito por escrito é o que transforma "qualidade" em cobrança executável.
4. **Termo de liberação antecipada (skincare)** — fábrica em conformidade que faria semanas de teste de compatibilidade e microbiologia permite liberar antes SE você assinar assumindo a responsabilidade. É troca consciente de velocidade por risco, não descuido.
5. **Política de garantia negociada ANTES** (ETAPA 10) — o que a fábrica cobre, o que ela considera defeito de fabricação, e em que formato ela aceita o relatório.
6. **Acordo de propriedade intelectual antes de qualquer design** (ETAPA 3) — sem ele, o design pode ficar com a fábrica.

Mantenha certificados e relatórios de teste organizados e acessíveis: auditoria acontece, e em processo de venda da empresa ela é minuciosa.

### ETAPA 10 — Qualidade: golden sample, QC ponta a ponta e a matemática do defeito

Aqui está a alavanca de margem que quase ninguém puxa. Espremer preço rende pouco e machuca a relação; reduzir defeito rende mais e melhora tudo.

**Puxe antes desta etapa:**
- **Golden Sample + Photographic Evidence QC System** (rode `golden sample assinado evidência fotográfica de cada batch QC remoto`)
- **End-to-End QC Checkpoint Chain** (rode `checkpoints QC do sub-vendor à assembly causa raiz conflito de interesse fulfillment`)
- **Go/No-Go Acceptance Criteria** (rode `go no-go acceptance criteria specs ao milímetro pilot batch accelerated age testing`)
- **Defect Rate Margin Math** (rode `defect rate matemática da margem cada ponto percentual custa $32.000 CAC no refund`)
- **CS-as-Defect-Sensor Tracking System** (rode `tracking de defeitos via customer service troubleshoot antes de refund buckets report limpo`)
- **Warranty & Compensation Play** (rode `warranty policy negociada antes over-shipping crédito próxima ordem double dip`)

**10.1 — A matemática que justifica tudo nesta etapa.**

Vender uma unidade defeituosa custa muito mais do que o preço do produto: custo do produto + frete + **o custo de aquisição do cliente** (a parte que todo mundo esquece) + a recompra que não vai acontecer + o dano de reputação (nota pior faz o custo de mídia subir) + o tempo do atendimento.

O caso de referência, num produto de gadget: preço de venda US$ 49,99; produto US$ 5,80; frete US$ 8,75; com retorno de 2,2 sobre o anúncio, o custo de aquisição fica em US$ 22,72 — sobra **US$ 12,73 por unidade vendida**. Quando essa unidade sai defeituosa e vira **reposição**, entram mais US$ 5,80 de produto e US$ 8,75 de frete: aquele cliente vira **prejuízo de US$ 1,82** (recuperável só se a fábrica repõe o produto, e só depois de revender). Quando vira **reembolso**, a receita é zero e você pagou produto + frete + aquisição — os mesmos US$ 5,80 + 8,75 + 22,72 saem do bolso sem nada entrar.

Rodando isso em 100.000 unidades, metade em reposição e metade em reembolso, sem recompra: **cada ponto percentual de defeito custa cerca de US$ 32.000**. Num produto com recompra de 25% (skincare, assinatura), cerca de US$ 44.000. Traduzido em margem: **cada 1% a menos de defeito vale de 3% a 6% de margem de lucro** (na divisão meio a meio). Se a maioria aceita reposição (75% reposição / 25% reembolso), o ganho fica em 2% a 4%; se a maioria exige reembolso (25%/75%), sobe pra 4% a 8%. O ganho é maior quando a taxa de partida é alta: sair de 7% para 6% vale mais que sair de 3% para 2%. E esses números **não incluem** reputação nem horas de atendimento — o benefício real é maior.

**Como aplicar aos números do membro** (a fórmula, com os dados dele — não repita os do caso):
- Custo de uma unidade reposta = custo do produto entregue + frete até o cliente.
- Custo de uma unidade reembolsada = custo do produto entregue + frete até o cliente + custo de aquisição do cliente.
- **Provisão de defeito por pedido = taxa de defeito × (fatia em reposição × custo da reposição + fatia em reembolso × custo do reembolso).**

Esse número vai pro `dados.json` e alimenta a linha de provisão de reembolso da Skill 04 (ETAPA 13).

**Referências de mercado quando o membro ainda não tem dado próprio:** gadget entre 6% e 10% é comum; skincare com vazamento fica em torno de 5%. Use como ponto de partida marcado como estimativa (`defect_rate_basis: "benchmark"`), nunca como se fosse medição.

**Quando priorizar redução de defeito:** taxa alta, categoria de recompra alta, clientes preferindo reembolso a reposição, ou escala chegando. Em 100 mil unidades por mês com 5% de defeito são 5.000 chamados de atendimento — o time trava.

**10.2 — Golden sample: a referência que decide tudo depois.**

Uma amostra perfeita, que reflete exatamente a unidade final desejada, **assinada** pelo dono da marca (ou representante). A fábrica guarda uma, você guarda outra. Nunca aceite uma amostra de referência abaixo do padrão: ela vira a régua de tudo — inclusive das cobranças futuras.

**10.3 — QC ponta a ponta (a cadeia inteira, não só o fim).**

Fábricas dividem a inspeção em três momentos: **entrada** (o material que chega), **linha** (durante a produção) e **saída** (antes de embarcar). Para todo componente crítico, isso precisa existir também **no fornecedor do componente**, na saída dele. Sem checkpoint na cadeia inteira, um defeito que nasceu num componente vira discussão de "ele disse, ela disse" e nunca acha a causa.

Caso ilustrativo: brinquedos de pelúcia cujo tecido vinha de outra província com problema de costura e bordado. Havia inspeção de terceiro na montagem e fabricante cooperativo — e só resolveu quando um terceiro investigou a causa raiz na PRIMEIRA fábrica, a do tecido.

Como operar isso à distância:
- Peça o **plano de produção** da fábrica primeiro. Entendendo as etapas, você sabe onde pedir evidência.
- Exija **foto e vídeo de CADA lote em cada etapa** (cor, risco, dimensão, encaixe). Com o tempo você reconhece os rostos e as etapas, e passa a detectar padrão.
- Se o problema persistir, contrate **inspeção de terceiro por amostragem de 5% a 10% do pedido** (inspecionar 100% é caro e desnecessário), com o pacote completo de instruções — sem instrução detalhada, sai caro, lento e aberto a interpretação.
- **Receba o relatório da inspeção ANTES de pagar o saldo.** É por isso que a regra de nunca pagar 100% adiantado (ETAPA 8) e o plano de qualidade são a mesma conversa.
- Aprovação de embarque: se a fábrica escolhe as 5 unidades "aleatórias", ela escolhe as perfeitas. Precisa de alguém imparcial puxando unidade de verdade.

**Duas regras que não se dobram:**
- **Nunca deixe a inspeção exclusivamente com o fornecedor** — os incentivos conflitam: qualidade consistente adiciona tempo de ciclo e custo que ele não colocou no preço.
- **Nunca use a empresa de fulfillment como inspetora.** Ela ganha dinheiro embarcando — é conflito estrutural com o jeito que ela faz dinheiro. Caso real: o fulfillment reportou 100% das unidades riscadas; devolvidas à fábrica e reinspecionadas com foto e vídeo, a maioria estava intacta, e o MESMO lote voltou e passou. Além disso, a inspeção do armazém não conversa com quem controla a produção: sem causa raiz, o problema se repete.

**10.4 — Critérios de aceite (transformar "qualidade" em régua).**

Durante a produção piloto, observe as unidades saindo da linha e classifique as imperfeições entre aceitáveis e reprovadas. Especifique **ao milímetro**: um risco de 1mm × 5mm é aceitável, 1,5mm de largura é rejeitado — com amostras de referência mostrando "esse nível passa, esse não". Perfeição de 100% não é compatível com produção eficiente; as concessões precisam ser conscientes e escritas.

- **Suplemento, skincare e beleza:** em vez de milímetro, exija **lote piloto** com as matérias-primas exatas em pequena escala — misturar, testar textura, cor e cheiro contra a amostra de referência, com laudo de análise e calibração de máquina ANTES de cada produção em massa.
- **Eletrônico:** inspeção de bateria por amostragem acordada + **teste de envelhecimento acelerado** (carga e descarga máximas por 80 a 100 ciclos, medindo capacidade e voltagem). Botão, chave e cabo testados lote a lote. Reprovou, o lote inteiro volta pro fornecedor do componente com nova inspeção completa — conte esse atraso no cronograma.

**10.5 — O atendimento como sensor de defeito (e como recuperar o dinheiro).**

O time de atendimento é o único sensor confiável de taxa de defeito que você tem:
1. Treine pra **diagnosticar antes de reembolsar** — boa parte do que chega como "defeito" é uso errado, por falta de instrução ou expectativa mal calibrada.
2. Reposição ou reembolso só com defeito real confirmado.
3. Classifique em **categorias específicas**: chegou morto, não carrega, componente quebrado, não funciona como esperado.
4. Reporte **semanal, mensal e trimestral** — a taxa, as melhorias e os defeitos novos.
5. Compartilhe com a fábrica em formato **limpo e digerível**, só com defeitos reais. Relatório sujo (misturando erro de uso) destrói a sua credibilidade e trava qualquer compensação — fábrica não reconhece erro de uso, e vai te ensinar a educar o cliente.

**Recuperar receita com o fornecedor** (combinado ANTES, nunca cobrado depois): negocie a política de garantia desde o começo — o que ela cobre, o que ela considera defeito de fabricação, qual formato de relatório ela aceita, e o que cobre em dinheiro (preço cheio da venda incluindo frete e aquisição? só a reposição do produto? algo no meio?). Duas formas que funcionam: **embarque a mais** (com 5% de defeito, a fábrica embarca 5% a mais na próxima ordem — no melhor caso, 5% de crédito E 5% a mais) e crédito na próxima ordem. Esteja disposto a devolver unidades para análise, e chegue com sugestão de correção: eles não conhecem o seu mercado nem o seu cliente. Nunca chegue no fim do trimestre com uma lista gigante de cobrança do nada — mata a taxa de sucesso. E use um defeito grande como alavanca antes do próximo pedido: "tenho 12% de devolução e uma ordem de 10.000 unidades pronta; só coloco se vocês me derem solução pra esse defeito."

### ETAPA 11 — Packaging e Valor Percebido

Embalagem é o jeito mais barato de mudar percepção de valor — e vira argumento na página e no criativo (a Skill 04 e a 07a leem isso).

**Puxe antes desta etapa:**
- **Print Effects Perceived-Value Menu** (rode `print effects hot foil emboss spot UV matte soft touch menos de $0.25 por unidade`)
- **Direct Printing vs Label Wrap Decision** (rode `direct printing vs label wrap frasco vinco no sticker percebido como defeito`)
- **Print-Ready Files Checklist** (rode `arquivos print-ready die lines texto em outline call-outs edit access fábrica`)
- **Component Upgrade** (rode `component upgrade mapear defeito dos concorrentes e marquetar contra a categoria`)
- **Travel-Ready Element** (rode `travel-ready element case de viagem brandado rotina completa mídia ambulante`)

**Efeitos de impressão** custam, em muitos casos, **menos de US$ 0,25 por unidade**: relevo metálico (dourado ou rosé, que lê como status), alto-relevo, verniz localizado, acabamento fosco e o toque aveludado. Estrutura também conta: aba magnética, berço interno moldado, encarte de papel (que substitui a espuma e comunica sustentabilidade), formato que não seja a caixa cúbica básica. Cada efeito muda pedido mínimo e prazo — planeje junto com o cronograma, não depois.

**No painel frontal** ficam apenas os pontos de venda vitais e o ingrediente ou recurso principal — de preferência com nome próprio (nome batizado costuma valer registro de marca).

**Impressão direta no frasco vs rótulo adesivo** (a decisão que mais afeta o prazo em skincare):
- **Rótulo adesivo**: barato e rápido (permite 25 a 30 dias já na primeira ordem), mas bloqueia a visão da fórmula e pode sair torto ou vincar. **Vinco em adesivo é classificado como DEFEITO pelo cliente** — vira reclamação e entra na conta da ETAPA 10.
- **Impressão direta**: o produto parece feito sob medida mesmo sendo de catálogo, aceita relevo metálico e verniz, e o custo sobe pouco — mas o pedido mínimo e o prazo aumentam (frasco em cerca de 25 a 35 dias).
- Prazo curto sendo prioridade, use rótulo adesivo bem desenhado: dá pra elevar bastante o valor percebido pelo design.

**Elemento de viagem:** um estojo, nécessaire ou versão de tamanho reduzido, sempre com a marca. É a embalagem que o cliente NÃO joga fora — vira mídia ambulante e sobe o valor percebido do conjunto. Uma marca europeia de cuidado feminino lançou pacotes de viagem mirando o início da temporada de viagens e continuou vendendo fora da época, com a recompra puxada por quem viaja muito. Se já há muito estoque sem essa embalagem, dá pra comprar a bolsa separada e montar a oferta "leve a rotina completa e ganhe a bolsa".

**Melhoria de componente como arma de marketing:** defina o teto de custo do produto e trabalhe de trás pra frente pelos componentes. Mapeie o defeito que mais aparece nos concorrentes (a Skill 03 já tem isso nas reviews deles), resolva o componente que causa esse defeito, e marquete contra a categoria: "todos os problemas dessa categoria vêm deste componente; eu resolvi pelo mesmo preço."

**Arquivos prontos pra fábrica** (evita dias de retrabalho): confirme o formato de arquivo COM a fábrica antes de produzir a arte; medidas desenhadas claramente no arquivo; pacote de fontes e texturas incluídos; texto convertido em contorno; indicação de onde vai cada efeito de impressão; e peça à fábrica a checklist do que ela precisa, validando antes de enviar. **Não dê acesso de edição à fábrica** — edição feita por eles introduz falha secundária (imagem de versão antiga, fonte trocada), e o que sai impresso não é o que você aprovou.

### ETAPA 12 — Calendário: Ano Novo Chinês e prevenção de ruptura de estoque

**Puxe antes desta etapa:**
- **Chinese New Year Playbook** (rode `Chinese New Year playbook cronologia shutdown pedidos até dezembro embarques 8-10 fev`)
- **Hybrid Shipping + Inventory Roll-Forward** (rode `hybrid shipping air freight só para o buffer de 10 dias inventory roll-forward CNY`)
- **Integrated Q1+Q2 Planning** (rode `planejamento Q1 Q2 armadilha Q4-heavy front-load SKUs janelas de negociação janeiro março`)
- **Post-CNY Re-Audit** (rode `pós-CNY re-auditar fábrica trocou sub-vendors quality manager corrective action plan`)
- **Gift-Giving & CNY Ritual Calendar** (rode `gift giving fornecedor pagar saldos antes do Chinese New Year annual party VIP customer`)
- **Supply Chain Threat Hierarchy** (rode `hierarquia de problemas supply chain stockout desligar ads defect rate inventário`)

**12.1 — A hierarquia dos problemas (define a prioridade de tudo):**

1. **Ruptura de estoque é o pior.** Pedido sem produto derruba a operação: o prazo explode e o caminho passa a ser **desligar os anúncios** — e reotimizar a campanha do zero depois é caríssimo. O antídoto é planejamento de compra que cruza a venda atual + o estoque do dia + os prazos, pra prever a data em que o estoque acaba e a data em que a recompra precisa ser feita.
2. **Taxa de defeito vem em segundo** (ETAPA 10).
3. **Estoque encalhado em terceiro** — e defeito vira encalhe. Prazo de pagamento negociado (ETAPA 8) é o que evita capital preso.

**12.2 — O Ano Novo Chinês, com a cronologia real.** É a maior migração humana do mundo: o feriado oficial cai em fevereiro, mas o país para bem antes e demora muito a voltar.

| Momento | O que acontece |
|---|---|
| Até o fim de dezembro | Prazo real pra colocar o pedido que precisa sair antes do feriado |
| Meados de janeiro | **Os fornecedores de matéria-prima fecham ANTES das montadoras** (aço e algodão param por volta do dia 15) |
| Semanas antes do feriado | Os trabalhadores começam a ir embora; as cidades industriais esvaziam |
| Cerca de 8 a 10 de fevereiro | Últimos embarques saem |
| Semana final | Nada acontece; os 3PLs chineses fecham por cerca de uma semana |
| Fim de fevereiro / início de março | Volta oficial, com cerca de metade da capacidade |
| **Meados de março** | **Capacidade normal** — parte dos trabalhadores não volta (muitos trocam de emprego no reinício do ano) e a fábrica precisa recontratar e retreinar |

**O que fazer, na ordem:**
- **Pergunte a cada fornecedor** (a resposta muda de fábrica pra fábrica; não existe resposta única): "qual o prazo da matéria-prima antes e depois do feriado, e quanto eu preciso comprar ou depositar AGORA pra operar liso na volta?" e "qual o calendário de parada de vocês?". **Documente por fábrica.**
- **Emita os pedidos de compra antes do feriado.** Se o gatilho de compra de material da fábrica é o seu pedido formal, previsão sem pedido não compra matéria-prima nenhuma.
- **Embarque parcial**: se a ordem não sai inteira, negocie sair em partes; identifique o item que está travando tudo (costuma ser a embalagem) e pressione ou incentive aquele fornecedor específico.
- **Logística com antecedência**: reserve contêiner com semanas de antecedência (já houve produção heroica concluída e navio só duas semanas depois). Perto do feriado, sobretaxas dobram ou triplicam, e contêiner "rola" pra semana seguinte por congestionamento.
- **Embarque híbrido pra cobrir o período sem produção**: calcule estoque atual + em trânsito + em produção contra a velocidade de venda, e projete quantos dias de suprimento você tem durante o período. Use frete aéreo APENAS pro buffer da semana a 10 dias em que o 3PL chinês está fechado, e marítimo pro resto. Decida pela economia do produto: produto pesado com frete aéreo caro pode não fechar. **Vender no empate pra NÃO desligar os anúncios costuma valer a pena** — o custo de reotimizar a campanha é maior.
- **Use a parada a favor**: o primeiro trimestre é a época oficial de desenvolvimento de produto. Feche o depósito do molde ANTES do feriado e pré-encomende o aço (a compra do aço come os primeiros 7 a 10 dias dos cerca de 30 do molde), pra o molde ser cortado assim que voltarem. Os engenheiros ficam ociosos nesse período e o design avança mais rápido que em qualquer outra época do ano.
- **Pague todo saldo pendente antes do feriado** — é a época de bônus da equipe da fábrica, e isso pesa muito na prioridade que você recebe antes e depois. Presença nas festas anuais (ou um presente do seu país, que vale mais que coisa cara) compra prioridade real.
- **Microgerencie**: se existe uma hora pra perguntar todo dia se está no prazo, é essa.
- **Depois da volta, re-audite**: pergunte se trocaram fornecedor de componente, gerente de qualidade ou pessoal de linha, e peça inspeção. Muita coisa muda de mãos no reinício do ano.

**12.3 — A armadilha do quarto trimestre pesado.** Vendeu muito no fim do ano, relaxou no primeiro trimestre, teve ruptura de estoque, passou o primeiro e o segundo trimestres correndo atrás e chegou no terceiro sem ter preparado o quarto. É um ciclo vicioso, e ele começa exatamente aqui. Mesmo produzindo fora da China (Vietnã, Malásia), componentes e engenheiros frequentemente vêm de lá — o feriado te afeta igual.

**12.4 — Confirmação de volume (o que a Skill 12 vai cobrar).** Antes de fechar esta skill, obtenha do fornecedor escolhido, **por escrito**, se ele consegue entregar o volume projetado em 30, 60 e 90 dias, e o ponto de recompra (a partir de quantos dias de estoque restante o pedido precisa ser colocado, considerando o prazo dele). Grave em `calendar.volume_confirmation_30_60_90` e `calendar.reorder_point_days`. A Skill 12 exige essa confirmação no pré-flight de escala, e sem ela a escala roda no escuro: **perto do ponto de recompra, faça o pedido, acompanhe o rastreio e NÃO escale os anúncios agressivamente** — vai bater na ruptura.

### ETAPA 13 — Contrato com a Skill 04 (COGS real)

Ao fechar a cotação, grave os números e atualize a oferta. **A 04 mantém o COGS num bloco de 8 linhas, todas em dinheiro por pedido, nunca em percentual** — o cânone é `.claude/lib/unit-economics/README.md` e a definição do bloco está na Skill 04.

**Regra de escrita (crítica): a 01b atualiza APENAS as linhas que o sourcing fecha e PRESERVA as demais com o valor que já está lá.** Nunca reescreva o `cogs_breakdown` inteiro, nunca zere um campo que esta skill não conhece.

| Campo do `cogs_breakdown` da 04 | Quem preenche | De onde vem aqui |
|---|---|---|
| `product_delivered` | **01b** | `landed_cost_per_unit` — produto na fábrica + embalagem + frete de entrada + imposto de importação, por unidade |
| `shipping_to_customer` | **01b** | `three_pl.shipping_to_customer_per_order` (inclui a parcela de frete grátis que a loja absorve) |
| `pick_pack` | **01b** | `three_pl.pick_pack_per_order` |
| `taxes_and_duties` | **01b** | Tributos por pedido que ainda NÃO estejam dentro do custo desembarcado |
| `refund_chargeback_provision` | **01b informa o piso** | `quality.defect_provision_per_order` (ETAPA 10.1) — a 04 decide o valor final, porque essa linha entra UMA vez só (ou aqui, ou como desconto no AOV líquido) |
| `payment_processing` | 04 | Não é domínio do sourcing — preservar |
| `subscription_app_fee` | 04 | Não é domínio do sourcing — preservar |
| `agency_fee_variable` | 04 | Não é domínio do sourcing — preservar |

**Cuidado com contagem dupla do imposto de importação:** no regime DDP, o imposto já está DENTRO do preço cotado e portanto dentro de `product_delivered`. Nesse caso `taxes_and_duties` cobre apenas tributos por pedido que ainda não entraram (imposto sobre a venda, taxas locais) — **jamais o imposto de importação de novo**. Registre `landed_cost_includes_duty: true` para deixar isso explícito pra Skill 04 e pra Skill 11.

Fluxo de atualização:
- Se `04-offer-builder/dados.json` já existe com `cogs_estimated: true` → atualize as linhas da tabela acima com os custos reais, recalcule unit economics/AOV/PSM e regrave (a Skill 04 define as fórmulas; os inputs vêm daqui). Remova `cogs_estimated` só quando as 4 linhas de domínio do sourcing estiverem fechadas.
- Se a Skill 04 ainda não rodou → ela lê `sourcing/dados.json` no pré-flight e nasce com COGS real (sem estimativa).
- O **preço-alvo declarado à fábrica** (ETAPA 4, bloco 4) e o COGS da 04 são o mesmo número visto dos dois lados: se a cotação voltar acima do alvo, é a oferta que precisa mudar (preço, bundle, AOV), não a planilha.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de qualquer write**: `mkdir -p workspace/[produto]/sourcing/`.

1. **`workspace/[produto]/sourcing/sourcing.md`** — relatório no report_language: a operação explicada (ETAPA 1), due diligence dos candidatos com o tipo real de cada um, rota do produto com prazo e orçamento, mensagem de cotação pronta, exigências de conformidade da categoria, agentes (se recomendados pro caso), tabela comparativa (quando houver cotações), o plano de condições de pagamento, os contratos a assinar antes de produzir, o plano de qualidade com a matemática do defeito nos números do membro, as decisões de embalagem, o calendário com as datas-limite, e a decisão com os próximos passos. Segue `.claude/rules/report-only-results.md`.
2. **`workspace/[produto]/sourcing/sourcing.html`** — companion no template `.claude/templates/aura-report-template.html` (logo SVG, componentes aura).
3. **`workspace/[produto]/sourcing/dados.json`**:

```json
{
  "product_slug": "",
  "status": "quoting|samples|closed",
  "category": "skincare|supplement|electronics|apparel|pet|home|other",
  "product_route": "ready_stock_white_label|custom_formula|odm",
  "suppliers": [
    {
      "name": "", "channel": "alibaba|1688|private|us_manufacturer|agent|trade_show|public_database|linkedin",
      "supplier_type": "factory|trade_company|dropshipping_agent|sourcing_company|unknown",
      "type_evidence": "", "factory_size": "small|medium|large|unknown",
      "contact": "", "wechat_ok": false,
      "unit_cost": 0, "moq": 0, "incoterm": "EXW|FOB|DDP|DDU_DAP",
      "ddp_to_3pl": 0, "lead_time_days": 0, "slowest_component": "", "slowest_component_days": 0,
      "payment_terms_offered": "",
      "spec_confirmed": false, "bom_provided": false,
      "compliance": { "gmp_gmpc": false, "coa_per_batch": false, "third_party_lab": "", "category_tests": [], "certificate_verified": false },
      "sample": { "label": "", "received": false, "verdict": "" },
      "role": "start|scale|discarded", "red_flags": [], "notes": ""
    }
  ],
  "chosen_supplier": "",
  "logistics_route": "ddp_to_3pl|dropship_direct|fba|home",
  "three_pl": { "provider": "", "pick_pack_per_order": 0, "shipping_to_customer_per_order": 0, "storage_monthly": 0, "payment_terms": "" },
  "landed_cost_per_unit": 0,
  "landed_cost_includes_duty": true,
  "target_price_declared": 0,
  "payment_terms": {
    "model": "standard_30_70|30_40_30|rolling_deposit|pay_as_you_ship|line_of_credit",
    "deposit_pct": 0, "balance_trigger": "", "net_days": 0,
    "incoterm_clock": "EXW|FOB|DDP", "effective_days_including_transit": 0,
    "never_100_upfront_confirmed": false, "next_threshold_to_unlock": ""
  },
  "quality": {
    "golden_sample_signed": false, "qc_chain": { "sub_vendor_oqc": false, "iqc": false, "inline": false, "final": false },
    "third_party_qc": false, "inspection_pct": 0, "report_before_balance_payment": false,
    "go_no_go_criteria": "", "aql_in_contract": false,
    "defect_rate_assumption": 0, "defect_rate_basis": "benchmark|measured",
    "defect_split": { "replacement_pct": 0, "refund_pct": 0 },
    "defect_provision_per_order": 0,
    "warranty_policy": ""
  },
  "contracts": { "msa": false, "brand_authorization_letter": false, "ip_agreement_before_design": false, "production_waiver": false },
  "packaging": { "decoration": "label_wrap|direct_print", "print_effects": [], "travel_element": false, "print_ready_files_ok": false, "cost_per_unit": 0 },
  "calendar": { "cny_exposure": "none|watch|critical", "order_by_date": "", "supplier_shutdown_window": "", "reorder_point_days": 0, "volume_confirmation_30_60_90": "" },
  "cogs_payload_for_04": {
    "product_delivered": 0, "shipping_to_customer": 0, "pick_pack": 0, "taxes_and_duties": 0,
    "refund_chargeback_provision_floor": 0,
    "fields_not_owned_here": ["payment_processing", "subscription_app_fee", "agency_fee_variable"]
  },
  "quote_message_sent_at": "",
  "pending_from_supplier": []
}
```

**Atualize o `manifest.json`**: `skills_completed` ← `"01b-sourcing"` (quando `status: "closed"`), `cogs_estimate` ← soma das linhas de domínio do sourcing (quando fechada), `updated_at`, e regenere o painel (`python3 .claude/lib/workspace-index/build_index.py <slug>`).

## Mensagem Final

(Adaptar ao ponto em que a skill parou — cotação enviada vs fechada. Nas duas versões, o membro precisa sair sabendo quais são as duas alavancas que ele ainda não puxou.)

Cotação enviada:

"Sourcing estruturado: [N] fornecedores analisados ([X] identificados como intermediário, não fábrica), mensagem de cotação pronta com preço-alvo e exigências de conformidade da categoria [+ agentes parceiros recomendados, se for o caso]. Enquanto as respostas não chegam, dá pra avançar com market research / competitor analysis — a pesquisa não depende do fornecedor. Quando os preços chegarem, me passa que eu comparo, fecho a recomendação e atualizo o custo real na oferta. Duas coisas que a gente ainda vai negociar depois do preço, e que valem mais que ele: quando você paga (prazo de pagamento é o que libera caixa pra anúncio) e quantas unidades chegam com defeito (cada 1% a menos vale de 3% a 6% de margem)."

Cotação fechada:

"Fornecedor fechado: [nome], custo desembarcado de [valor] por unidade, [incoterm] até [destino], prazo de [N] dias. Custo real já atualizado na oferta. O que fica combinado antes do primeiro pedido: [condição de pagamento acordada], amostra de referência assinada pelos dois lados, [critérios de aceite / inspeção de terceiro, se aplicável] e o relatório de inspeção antes do pagamento do saldo. [Se houver exposição ao Ano Novo Chinês: a data-limite pra colocar esse pedido é [data] — depois disso o prazo muda de patamar.]"

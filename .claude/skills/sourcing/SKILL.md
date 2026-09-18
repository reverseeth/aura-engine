---
name: sourcing
description: Fornecedor, cotação, qualidade e condições de pagamento do produto físico, em paralelo à pesquisa de mercado e antes de a oferta ter custo real. Explica a operação em linguagem simples, faz a due diligence com os 5 testes de trade company disfarçada de fábrica, decide a rota do produto, monta a mensagem de cotação em inglês com preço-alvo, cobra a conformidade por categoria com os laboratórios certos, compara cotações, negocia condições de pagamento e incoterm, fecha os contratos mínimos, arma o sistema de qualidade e a matemática do defeito, decide a embalagem, protege o calendário do Ano Novo Chinês e entrega o custo real pro COGS da offer-builder. Use quando o membro disser "sourcing", "fornecedor", "supplier", "cotação", "Alibaba", "3PL", "frete da China", "fábrica", "MOQ", "payment terms", "prazo de pagamento", "inspeção", "QC", "defeito", "compliance", "Chinese New Year", ou quando um produto escolhido precisar de custo real antes da oferta.
---

# Sourcing · Paralela, opcional · apelido antigo: 01b <!-- gen:title -->

## Quando usar

Depois que o produto foi escolhido (`product-research`) e antes de a oferta ter custo real (`offer-builder`). É opcional e paralela: roda ao mesmo tempo que `market-research` e `competitor-analysis`. Membro com fornecedor privado ou dropship usa só as partes que servem. Saída: fornecedor, custo real por unidade, condições de pagamento, plano de qualidade e rota logística. Duas alavancas dominam a skill e costumam ser ignoradas: condições de pagamento (quando você paga, a alavanca número 1 de caixa pra anúncio) e taxa de defeito (cada ponto percentual a menos vale de 3% a 6% de margem).

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/profile.md` e `manifest.json` do produto; ausentes, oferecer rodar o `setup` inline; mais de um produto = perguntar qual em 1 linha.
2. O que o membro já tem (links de anúncio, fornecedor privado, cotações antigas, pedido colocado, nada): a skill entra no ponto certo.
3. `sourcing/dados.json` existente: leia e continue de onde parou (a skill é reentrante).
4. Membro com fornecedor e pedido feito: pule as ETAPAs 2 a 6 e entre nas ETAPAs 8, 10 e 12.
5. `offer-builder` já rodou com custo estimado: o fechamento atualiza o `cogs_breakdown` de lá (ETAPA 13).

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`); a mensagem de cotação pro fornecedor é em inglês (comunicação comercial, não copy).
2. `workspace/profile.md` (seção de sourcing) e o output da `product-research` (produto, formato, mecanismo pretendido): a cotação pergunta exatamente o que o posicionamento promete.
3. Categoria do produto (skincare, suplemento, eletrônico, vestuário, pet, casa): decide os testes de conformidade (ETAPA 5), a rota realista (ETAPA 3) e a taxa de defeito esperada (ETAPA 10). Data de hoje contra o calendário chinês (ETAPA 12).
4. Base pelo índice (domínio `supply-chain-sourcing`): `python3 .claude/lib/kb-index/kb_lookup.py --skill sourcing --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas adicionais por etapa; as queries embutidas em `reference/` são piso obrigatório, rodam sempre e não contam no teto; nunca query genérica nem busca repetida. Dado de verificação não confirmado na web vira pendência, nunca invenção.

## Fluxo da skill

### ETAPA 0 · Pré-flight

É a checklist acima; o texto integral está em `reference/contexto.md`.

### ETAPA 1 · A operação explicada (linguagem simples, sempre no relatório)

Leia `reference/operacao-explicada.md` e puxe os três sistemas. O relatório explica os termos com exemplos do produto do membro: os 4 tipos de fornecedor com prós, contras e a régua da taxa suspeita; o porte da fábrica (média, de 100 a 200 pessoas, é o melhor ponto de partida); o vocabulário da conversa; o incoterm como o momento em que o prazo de pagamento começa a contar (compare prazo efetivo, nunca nominal; FOB costuma ser melhor que EXW); e as 4 rotas de quem guarda e envia. Caminho recomendado pra loja própria nos EUA: DDP direto pro 3PL americano.

### ETAPA 2 · Due diligence, descoberta e triagem

Leia `reference/due-diligence.md` e puxe os três sistemas. Rede ampla de 50 ou mais empresas, com fontes além do Alibaba; primeiro filtro comportamental (pedir WeChat); os 5 testes de trade company disfarçada de fábrica, registrando o tipo real sem descartar automaticamente; avaliação das respostas pelos sete sinais do arquivo; estrutura de qualidade da fábrica; amostras rotuladas de 3 a 5 finalistas testadas por critério fixo; sinais de alerta em `red_flags[]`. Classifique cada candidato em começar, escalar ou descartar.

### ETAPA 3 · Rota do produto (prazo, orçamento e risco)

Leia `reference/rota-do-produto.md` e puxe os três sistemas. Rota A, estoque pronto com rótulo seu (default pra validar com dinheiro pequeno); rota B, fórmula própria (amostras de 3 a 5 fábricas em paralelo; o gargalo é a garrafa, e comprar o dobro de garrafas encurta a segunda ordem); rota C, molde próprio (US$ 50 mil a 100 mil e 9 a 12 meses; pagamento por fase e acordo de propriedade intelectual antes de a fábrica desenhar). Em qualquer rota, sequencie os componentes pelo mais lento.

### ETAPA 4 · Mensagem de cotação (inglês, pronta pra enviar)

Leia `reference/mensagem-de-cotacao.md` e puxe o sistema do preço-alvo. Uma mensagem com os 9 blocos: spec sheet, performance, material de contato, preço-alvo com lista de materiais (sempre declare o alvo), contagem e embalagem, compliance, amostras e prazo por matéria-prima, condições de pagamento e frete DDP até o 3PL em 2 quantidades com a alternativa FOB. Feche com a pressão saudável do arquivo.

### ETAPA 5 · Compliance por categoria

Leia `reference/compliance.md` e puxe a matriz de compliance. A lista real de testes e registros por categoria (skincare, suplemento, eletrônico, Amazon), com a diferença entre fábrica registrada na FDA e produto aprovado. Os três grandes laboratórios (SGS, Intertek, Eurofins), orçamento de US$ 2 mil a 10 mil, todos os testes antes do embarque; verificação do certificado com o emissor; certificação leva de 1 a 3 meses e entra no cronograma agora.

### ETAPA 6 · Agentes de sourcing parceiros da Aura

Leia `reference/agentes-parceiros.md`: os quatro contatos por WhatsApp, quando o agente vale a pena (customização, volume, inspeção, consolidação, herdar condições de pagamento) e como abordar (a mensagem da ETAPA 4 mais 1 parágrafo de contexto; perguntar o modelo de remuneração na primeira conversa).

### ETAPA 7 · Comparar cotações e decidir

Leia `reference/comparar-cotacoes.md`. Tabela comparativa por fornecedor (colunas no arquivo). Fornecedor de começo e fornecedor de escala podem ser dois; transparência desempata; amostras de 2 a 3 finalistas antes de qualquer volume; prazo efetivo, não nominal; sanidade da margem pelo cânone `.claude/lib/unit-economics/README.md` §6 (custo desembarcado até cerca de 30% do preço de venda).

### ETAPA 8 · Condições de pagamento e incoterm (a alavanca número 1 de caixa)

Leia `reference/condicoes-de-pagamento.md` e puxe os sete sistemas. Regra dura: nunca pague 100% adiantado. Os 3 momentos de negociar (o prazo de pagamento só entra depois da previsão de 3, 6 e 12 meses cumprida); credibilidade vem antes do prazo ("o que eu preciso provar pra destravar o próximo degrau?"); os modelos além do 30/70; risco por categoria; cortar o prazo de produção quando o prazo de pagamento não vem; volume emprestado de sourcing company; prazo no imposto, no transportador e no fulfillment; tarifa como argumento; relacionamento como preço (ser o cliente favorito).

### ETAPA 9 · Contratos mínimos antes de produzir

Leia `reference/contratos.md` e puxe o sistema. Acordo de fabricação, carta de autorização de marca (fiscalizada na exportação), qualidade dentro do contrato com tolerância de defeito por escrito, termo de liberação antecipada em skincare, política de garantia negociada antes e acordo de propriedade intelectual antes de qualquer design. Priorize pelo risco do produto e feche antes da produção.

### ETAPA 10 · Qualidade, golden sample, QC ponta a ponta e a matemática do defeito

Leia `reference/qualidade.md` e puxe os seis sistemas. A matemática nos números do membro: custo da unidade reposta, custo da unidade reembolsada e a provisão de defeito por pedido (fórmula no arquivo), que vai pro `dados.json` e pra provisão de reembolso da `offer-builder`; benchmark só como `defect_rate_basis: "benchmark"`. Golden sample assinada pelos dois lados; QC em entrada, linha e saída, inclusive no fornecedor do componente, com foto e vídeo de cada lote, inspeção de terceiro por amostragem de 5% a 10% e relatório antes de pagar o saldo; nunca a inspeção só com o fornecedor nem com o fulfillment; critérios de aceite ao milímetro; o atendimento como sensor de defeito e a recuperação de receita combinada antes.

### ETAPA 11 · Packaging e valor percebido

Leia `reference/packaging.md` e puxe os cinco sistemas. Efeitos de impressão por menos de US$ 0,25 a unidade; painel frontal só com os pontos vitais; impressão direta versus rótulo adesivo (vinco em adesivo é defeito pro cliente); elemento de viagem; melhoria de componente como arma de marketing contra o defeito da categoria; arquivos prontos pra fábrica sem dar acesso de edição.

### ETAPA 12 · Calendário, Ano Novo Chinês e prevenção de ruptura

Leia `reference/calendario.md` e puxe os seis sistemas. Hierarquia dos problemas (ruptura de estoque é o pior, defeito em segundo, encalhe em terceiro); a cronologia real do feriado (pedidos até dezembro, capacidade normal só em meados de março); os passos do arquivo na ordem (pedidos e saldos antes do feriado, embarque híbrido só pro buffer, re-auditoria na volta); a armadilha do quarto trimestre pesado; e a confirmação de volume por escrito em 30, 60 e 90 dias com o ponto de recompra (campos `calendar.*`), que a `scale-engine` exige antes de escalar.

### ETAPA 13 · Contrato com a `offer-builder` (COGS real)

Leia `reference/contrato-com-offer-builder.md`. Atualize só as linhas do `cogs_breakdown` que o sourcing fecha (`product_delivered`, `shipping_to_customer`, `pick_pack`, `taxes_and_duties` e o piso de `refund_chargeback_provision`) e preserve as demais; nunca conte o imposto de importação duas vezes no DDP (`landed_cost_includes_duty: true`); `cogs_estimated` sai só com as quatro linhas fechadas; se a `offer-builder` ainda não rodou, ela nasce com COGS real. Cotação acima do preço-alvo muda a oferta, não a planilha.

## SALVAR

Leia `reference/salvar-e-dados-json.md`. `mkdir -p workspace/[produto]/sourcing/`; `sourcing.md` no `report_language` na ordem do arquivo (uma seção por etapa, da operação explicada à decisão, com a matemática do defeito nos números do membro), só o resultado no doc; `sourcing.html` por `python3 tools/render_report.py workspace/[produto]/sourcing/sourcing.md`; `dados.json` no schema do arquivo (`suppliers[]`, `payment_terms`, `quality`, `calendar`, `cogs_payload_for_04` e os demais blocos). Manifest pelo script: `python3 tools/manifest.py <slug> complete sourcing` só com `status: "closed"`, `set cogs_estimate` com a soma das linhas do sourcing, e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`, adaptada ao ponto em que a skill parou (cotação enviada ou fechada); nas duas versões o membro sai sabendo quais são as duas alavancas que ainda não puxou.

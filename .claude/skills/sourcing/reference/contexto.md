# Sourcing · Referência: Quando usar, as duas alavancas, base de conhecimento, antes de começar e pré-flight (ETAPA 0)

> O texto integral do quando usar com o objetivo de saída e as duas alavancas (condições de pagamento e taxa de defeito), a regra da base de conhecimento pelo índice (domínio `supply-chain-sourcing`), as leituras iniciais (idioma, profile, product-research, categoria, calendário chinês, checagem na web) e o pré-flight reentrante com o atalho de quem já tem fornecedor. Abra antes da ETAPA 1.

## Quando Usar

Depois que o produto foi escolhido (Skill `product-research`) e antes da oferta ter custo real (Skill `offer-builder`). É uma fase **opcional e paralela**: pode rodar ao mesmo tempo que as Skills `market-research`/`competitor-analysis` (a pesquisa não depende do fornecedor). Membro com fornecedor privado ou operação dropship usa as partes que servem (cotação, condições de pagamento, qualidade, logística, comparação) e pula o resto.

O objetivo de saída: **fornecedor escolhido + custo por unidade real + condições de pagamento acordadas + plano de qualidade + rota logística definida** — o pacote que transforma o COGS estimado da Skill `offer-builder` em COGS de verdade, e que decide quanto caixa o membro tem livre pra comprar tráfego.

**Duas alavancas dominam esta skill**, e as duas costumam ser ignoradas por quem está começando:

1. **Condições de pagamento** (quando você paga, não só quanto paga). É a alavanca número 1 de caixa: mais caixa livre = mais verba de anúncio = mais escala. Pausar anúncio por falta de caixa custa caro duas vezes, porque depois é preciso reotimizar a campanha do zero.
2. **Taxa de defeito** (quantas unidades chegam com problema). Cada ponto percentual a menos de defeito vale de 3% a 6% de margem de lucro — mais do que a maioria das negociações de preço entrega.

Quem fecha uma cotação sem tocar nessas duas fecha metade do trabalho.

## Base de conhecimento (NUNCA query genérica)

Esta skill puxa **SISTEMAS NOMEADOS** de supply chain e sourcing da base — nunca query genérica do tipo "fornecedor" ou "sourcing". Em cada ETAPA abaixo, rode `search_knowledge` (com `deep=true`) usando a `best_query` **exata** de cada framework listado ali, e puxe o sistema completo (ex: os 5 testes de trade company disfarçada de fábrica, não "dicas de Alibaba").

**Índice completo do domínio desta skill (`supply-chain-sourcing`, 36 sistemas): `.claude/lib/kb-index/`** (mapa skill → domínio no `README.md`). **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill sourcing --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 10 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão. Os sistemas de maior impacto já estão NOMEADOS dentro de cada ETAPA. Alguns deles são compartilhados com outras skills (compliance e defeito também alimentam a `product-research` e a `offer-builder`; packaging também alimenta a `offer-builder` e a `page-design`) — quando esta skill os puxa, o recorte é sempre a decisão de fornecedor.

## Antes de Começar

0. **Idioma do relatório (rule 0 — INVIOLÁVEL)**: leia `report_language` de `workspace/profile.md` (default `pt-BR`). Todo output interno e conversa com o membro usam esse idioma. A mensagem de cotação pro fornecedor é em **inglês** (é comunicação comercial externa, não copy de consumidor).
1. Leia `workspace/profile.md` — em especial a seção de sourcing (fornecedor privado? preferência de produto simples? verba disponível).
2. Leia `workspace/[produto]/manifest.json` e o output da Skill `product-research` (produto escolhido, formato, mecanismo pretendido) — a cotação precisa perguntar EXATAMENTE o que o posicionamento promete (dose, material, duração, especificação).
3. **Identifique a categoria** (skincare, suplemento, eletrônico/gadget, vestuário, pet, casa). A categoria decide três coisas ao longo da skill: quais testes de conformidade são obrigatórios (ETAPA 5), qual rota de produto é realista (ETAPA 3) e qual taxa de defeito é esperada (ETAPA 10).
4. **Cheque a data de hoje contra o calendário chinês** (ETAPA 12). Entre novembro e março, o Ano Novo Chinês muda TODAS as recomendações de prazo desta skill — e é o erro mais caro que um membro comete no primeiro pedido.
5. Quando precisar checar algo na web (cidade da fábrica × categoria, número de registro em base pública, reputação de laboratório), vale a `.claude/rules/resilient-fetch.md`: descoberta pela tool `WebSearch`, aprofundamento pelo fetcher da Aura. **Nunca invente um dado de verificação que você não conseguiu confirmar** — registre como pendência.

### ETAPA 0 — Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

1. Se `workspace/profile.md` ou o `manifest.json` do produto não existirem, ofereça rodar o `setup` inline antes de seguir. Se houver mais de um manifest com `setup_complete: true` e o membro não nomeou o produto no pedido, liste os `product_name` e pergunte em 1 linha qual é o alvo.
2. Identifique o que o membro JÁ tem: links de anúncio (Alibaba/1688/AliExpress), fornecedor privado com contato, cotações antigas, pedido já colocado, nada. A skill entra no ponto certo — não repete o que está feito.
3. Se `sourcing/dados.json` já existe, leia e continue de onde parou (a skill é reentrante: cotação enviada numa sessão, comparação em outra, qualidade em outra).
4. **Se o membro já tem fornecedor e já fez pedido**, o valor desta skill muda de lugar: pule as ETAPAs 2-6 e entre direto nas ETAPAs 8 (condições de pagamento), 10 (qualidade e taxa de defeito) e 12 (calendário e prevenção de ruptura de estoque). São as três que rendem dinheiro em operação já rodando.
5. Se a Skill `offer-builder` já rodou com custo estimado, anote: o fechamento desta skill atualiza o `cogs_breakdown` de lá (ETAPA 13).

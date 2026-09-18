---
name: marketplace-engine
description: Expansão de canal de venda além do site próprio, decide quando e se a marca abre Amazon, TikTok Shop e programa de afiliados, e acompanha cada canal aberto. Roda um gate antes de qualquer tática, com Meta e site provados primeiro (breakthrough na ad-analysis, conta fechando na finance-engine) e sinal de demanda transbordando (busca de marca subindo, cliente procurando a marca na Amazon, revendedor aparecendo na listagem), porque canal novo não conserta oferta quebrada. Amazon como captura da demanda que o ad já criou (SEO da listagem, defesa de marca, lances baixos, preço riscado, custom link e a régua do canal); TikTok Shop como canal de venda operado por afiliados (comissão orgânica contra comissão de ads, samples, volume vendido, incentivos de plataforma, com o conteúdo ficando na creator-engine); afiliados por tráfego pago com comissão decrescente por faixa e clientes virando afiliados automaticamente. Portar campanha paga pra outra plataforma de mídia é a content-recycler, não esta. Use quando o membro disser "amazon", "tiktok shop", "marketplace", "afiliados", "expandir canal", "vender fora do site".
---

# Marketplace Engine · Lateral · apelido antigo: 20 <!-- gen:title -->

## Quando usar

Quando a pergunta é sobre vender fora do site próprio. Não é fase do pipeline, é consulta lateral como a `finance-engine`, e o momento natural é a fase de escala, depois que a `ad-analysis` classificou um breakthrough estável e a `finance-engine` mostrou a conta fechando. Re-rodar é normal: a primeira rodada avalia canais, as seguintes atualizam status e métricas dos canais abertos. Responde quando abrir um canal secundário, qual abrir primeiro, o que precisa estar pronto antes de entrar e como acompanhar cada canal sem misturar a régua dele com a do Meta.

Fronteira com as vizinhas, em `reference/contexto.md`: conteúdo e creator são da `creator-engine`; portar campanha paga pra outra plataforma de mídia é da `content-recycler`; a conta financeira por canal, com comissão e taxa dentro, é da `finance-engine`. Esta skill decide e opera o canal, não produz criativo, não compra mídia e não fecha conta de canal nenhum.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` existe.
2. Prova de canal primário localizada: `manifest.ad_classification[]` com pelo menos um `breakthrough`, ou `manifest.finance` com mês fechado saudável. Sem nenhuma das duas a skill roda mesmo assim, mas o gate só pode sair `not_yet` ou `blocked_pending_proof`, nunca `expand`. A resposta honesta é output válido.
3. `report_language` do profile (default `pt-BR`) em todo output interno; copy que vai pro consumidor final, como texto de listagem e mensagem a creator, fica em inglês.

## Contexto a carregar

1. `profile.md` (stage e budget; para quem está começando ou validando o veredito quase sempre é "ainda não", dito sem rodeio e com o que destrava) e `manifest.json` (`stage`, `ad_classification[]`, `manifest.finance`, `manifest.marketplace` das rodadas anteriores).
2. `ad-analysis/dados.json` (a prova de que existe demanda criada pelo Meta pra transbordar), `finance-engine/dados.json` (margem e fôlego de caixa, porque comissão e taxa de marketplace são custo variável do canal e quem fecha essa conta é ela), `competitor-analysis/dados.json` (concorrente já presente no canal é leitura de sofisticação) e as rodadas anteriores em `marketplace-engine/`.
3. Os dados que a skill pede e nunca estima, com onde o membro encontra cada um, estão na tabela de `reference/contexto.md`: busca de marca, revendedor na Amazon, taxas reais do canal e volume vendido. Ferramenta paga sem MCP conectado nunca é fingida: a skill diz o que olhar e trata o retorno como dado colado pelo membro.
4. Base pelo índice (domínio `affiliate-creator-channels`, mais entradas de canal em `meta-ads-strategy`, `scaling` e `creatives-hooks-formats`): `python3 .claude/lib/kb-index/kb_lookup.py --skill marketplace-engine --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 6 buscas adicionais por etapa (as queries embutidas na etapa são piso obrigatório, rodam sempre e não contam no teto); a lista completa, com as queries exatas e o recorte do que fica com as vizinhas, está em `reference/sistemas.md`; nunca query genérica nem busca repetida.

## Fluxo da skill

### ETAPA 1 · O gate de expansão

Leia `reference/gate-de-expansao.md`. Canal secundário é agenda de quem já provou o canal primário, e a regra da fonte é não abrir canal que não se domina enquanto ainda há espaço no Meta. Condição 1: Meta e site provados, por breakthrough classificado ou mês fechado saudável; sem prova, o veredito é `blocked_pending_proof` e o relatório diz o que destrava. Condição 2: sinal de demanda transbordando, pela tabela dos quatro sinais na ordem de força. O anti-sinal bloqueia sozinho: abrir canal pra fugir de CAC ruim, criativo cansado ou oferta que não converte, porque canal novo herda a oferta e não a conserta. Grave `gate.verdict` e os sinais marcados; só `expand` libera as ETAPAs 2 a 4 como avaliação de entrada, e com `not_yet` as etapas seguintes só rodam pra canal já aberto.

### ETAPA 2 · Amazon, capturar a demanda que o ad criou

Leia `reference/amazon.md`. O pool de compradores da Amazon é quase separado do site, e sem listagem sua essa venda vai pro concorrente ou pro revendedor, paga com o seu ad. O essencial de entrada vem na ordem do arquivo: marca protegida antes da listagem (o status vem da `ops-engine` ou do membro, e a pendência aponta pra lá sem duplicar o protocolo), listagem com SEO antes de anúncio, base de prova com plano de reviews, preço riscado, anúncios internos com lance baixo incluindo a defesa da própria listagem, custom link pra tráfego externo e a régua do canal, que nunca se compara com a régua do Meta.

### ETAPA 3 · TikTok Shop, o canal operado por afiliados

Leia `reference/tiktok-shop.md`. Venda nativa dentro do app, movida por uma rede de afiliados, forte em consumíveis, beleza, saúde e casa. Esta skill opera a mecânica: comissão em dois níveis tratada como o CAC permitido do canal, samples como custo de entrada, volume vendido transparente com a jogada de bootstrap, o limite de contatos de recrutamento e os incentivos de plataforma, que são janela que fecha. Expectativa honesta: raramente é centro de lucro, e o retorno composto vem do halo de busca, do efeito cruzado entre canais e do acervo de criativo. A divisão com a `creator-engine` está no arquivo.

### ETAPA 4 · Afiliados via tráfego pago

Leia `reference/afiliados.md`. Ad que vende a oportunidade e não o produto, com candidatura, código de desconto e primeira compra; a aquisição de afiliado vira funil pago próprio e pode ser lucrativa já na aquisição. Vale depois do funil próprio provado, e especialmente em marca de identidade. A comissão é decrescente por faixa com teto mensal, nunca percentual fixo pra sempre, e a base pode ser receita ou gasto em anúncio, para testar as duas. Na versão orgânica o cliente vira afiliado sem fricção, com a conta criada na compra e o código na página de obrigado. Atribuição por link ou código único é pré-condição, e a conta da comissão vai pra `finance-engine`.

### ETAPA 5 · Sequência, plano por canal e veredito

Leia `reference/sequencia-e-veredito.md`. Um canal novo por vez, na ordem default do arquivo: Amazon primeiro quando a busca de marca já cresce, TikTok Shop quando a categoria é forte no social e a operação suporta o fluxo de creators, programa de afiliados como camada sobre canal já rodando. Para cada canal liberado, registre o plano de entrada; para cada canal aberto, atualize status e métricas com a régua do próprio canal. Métrica que o membro não passou fica `null` e entra em `pending_inputs[]`.

### ETAPA 6 · Checagens de sanidade

Leia `reference/sanity-checks.md`: os oito itens, de nenhum canal liberado sem gate a nenhuma comparação entre a régua da Amazon e a do Meta. Falha em qualquer um bloqueia o salvamento do `.md`.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/marketplace-engine/`; `marketplace-engine.md` na ordem do arquivo, `marketplace-engine.html` por `python3 tools/render_report.py workspace/[produto]/marketplace-engine/marketplace-engine.md`, e `dados.json` no schema de `reference/dados-json.md` (quem lê o quê em `reference/contrato-de-leitura.md`). Manifest pelo script: `python3 tools/manifest.py <slug> complete marketplace-engine` e `set marketplace` com o resumo dos canais, nunca `manifest.stage`, mais `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`, como draft, uma versão por veredito do gate: a de quem está liberado a abrir canal, com o plano e a primeira meta, e a de quem ainda não está, com o que destrava.

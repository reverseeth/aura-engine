---
name: content-recycler
description: Pega um criativo classificado como breakthrough pela ad-analysis (cânone de ad-taxonomy, o KPI do ad melhor que o da campanha e puxando spend) e roda duas trilhas. Trilha 1, default e primeira, é a amplificação do que já provou escalar, com iteração pelos quatro elementos (ângulo, mecanismo, autoridade, avatar), port do ângulo pra outros formatos, brief de página dedicada, pacote de adaptação pra Axon e TikTok, duplicação em ad set próprio e creator report. Trilha 2, sob pedido, são as nove derivadas de canal próprio (advertorial, sequência de email, TikTok orgânico, blog de busca, carrossel de Pinterest, pre-roll de YouTube, SMS, encarte na caixa e leitura de podcast), como jogada de marca e de valor do cliente ao longo do tempo, nunca de performance. Nunca dispara com KPI winner, que o cânone trata como perdedor para decisão. Use quando o membro disser "recycle [id]", "reaproveitar winner", "content recycler", "tirar mais dos ads". Zero infraestrutura externa.
---

# Content Recycler · Passo 21 · apelido antigo: 14 <!-- gen:title -->

## Quando usar

Skill auxiliar invocável, acionada quando o membro diz `recycle [creative-id]`, `recycle breakthrough` ou `recycle winner`. Pega um criativo que já provou escalar e tira dele tudo que ele ainda pode dar, primeiro dentro do tráfego pago e depois nos canais próprios.

O gatilho é `breakthrough`, nunca "winner". As quatro classes de resultado vivem no cânone `.claude/lib/ad-taxonomy/README.md` §2 e são medidas pela `ad-analysis`; esta skill lê a classificação e nunca a recomputa. `kpi_winner` bateu o KPI sem puxar spend e o cânone o trata como perdedor para decisão, então reciclá-lo é multiplicar um teste pequeno. `spend_winner` entra só pela porta estreita do Movimento 1.

Duas trilhas, nesta ordem: a Trilha 1, de amplificação, roda sempre e primeiro, porque é o que se faz de verdade com um ad que venceu; a Trilha 2, das nove derivadas de canal, é jogada de marca e de valor do cliente ao longo do tempo, e só roda quando o membro pede. Quem escala a conta é a Trilha 1.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra, com a detecção completa, em `reference/pre-flight-e-deteccao.md`.

1. `report_language` do profile (default `pt-BR`) em todo output interno e na conversa; as nove derivadas, o `framework_template`, os hooks e scripts dos briefs, a copy de end card e a VOC literal ficam sempre em inglês US.
2. `manifest.json` existe e há pelo menos um criativo em `creative-engine/` ou fonte alternativa dada pelo membro.
3. Existem `.claude/lib/ad-taxonomy/README.md` (cânone das classes e a régua de ad set próprio), `.claude/lib/content-recycler/recycler.md` (engine da Trilha 2) e `.claude/lib/content-recycler/formats.json` (specs dos nove formatos).
4. Sem id no input, detecte a classe pelo `ad-analysis/dados.json`, na ordem `breakthroughs[]`, `manifest.breakthroughs[]` e `manifest.ad_classification[]`, com o fallback legado de `winners[]` (deprecado) e o aviso de re-rodar a análise. Ordene por spend, com dias no ar como desempate. Com mais de um breakthrough, apresente a lista e pergunte qual amplificar primeiro. Sem nenhum, a resposta honesta do arquivo aponta pra `creative-engine`, não pra esta skill. Sem análise nenhuma, ofereça rodar a `ad-analysis` ou trabalhar um id direto.

## Contexto a carregar

1. A fonte da Trilha 2 é a lib, nunca a base: a estrutura de um criativo pra nove formatos vem inteira de `.claude/lib/content-recycler/`. A Trilha 1 vem do cânone de ad-taxonomy (§2 classes, §5 escala, §7 Sniper) mais os movimentos do arquivo de apoio.
2. Base pelo índice (domínios `creatives-hooks-formats`, principal, e `page-landing-cro` pra página e pras derivadas de texto longo): `python3 .claude/lib/kb-index/kb_lookup.py --skill content-recycler --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 6 buscas por etapa; as queries embutidas nas etapas, listadas em `reference/essencia-e-framework.md` e `reference/trilha-2-derivadas.md`, são o mínimo garantido; nunca query genérica nem busca repetida.
3. `offer-builder/dados.json` (o `mechanism_name` literal), `creative-engine/dados.json` e `market-research/dados.json` (as VOC de onde a essência herda referência), `manifest.budget_daily` (base do cálculo do ad set próprio) e `manifest.target_cpa`.

## Fluxo da skill

As ETAPAs 0 e 1 são comuns às duas trilhas. Depois delas, a Trilha 1 roda primeiro, sempre.

### ETAPA 0 · Identificação do breakthrough

Leia `reference/essencia-e-framework.md`. Registre a classe lida (`breakthrough` ou `spend_winner`), porque é ela que define os movimentos liberados no resto da execução. Id de conceito abre também o `creative-engine/dados.json` e o briefing do conceito. Onde a lib diverge, esta skill vence: o texto da lib ainda fala em winner, e o gatilho é o breakthrough do cânone.

### ETAPA 1 · Extração da essência e do framework

Mesmo arquivo. Destile big idea, hook, mecanismo, avatar e voz em `essence.json` pela etapa 2 do `recycler.md`, com fontes rastreáveis e o sanity check de drift que para e avisa o membro. Só a essência não basta: o que viaja é o framework. O `essence.json` ganha dois campos além do schema da lib, o `framework_template` (o padrão do hook com o slot vazio, em inglês US) e o `psychological_mechanism` (por que o padrão funciona, em uma frase). Toda aplicação nova do framework sai em três versões, uma controle e duas reescritas, e o teste decide. O `psychological_mechanism` é o juiz de toda iteração da Trilha 1. Puxe os sistemas nomeados do arquivo pra sustentar a destilação.

### Trilha 1 · Amplificação (default, roda primeiro)

Leia `reference/trilha-1-amplificacao.md`. Breakthrough é caro e raro, e o primeiro trabalho com um deles é extrair mais spend lucrativo, não espalhá-lo por canal orgânico. São seis movimentos, num plano único (`amplification-plan.md`, uma seção por movimento). Esta skill especifica; quem executa é a `creative-engine` (criativo), a `page-design` com a `copy-engine` (página e copy) e a `scale-engine` (escala).

1. Iterar pelos quatro elementos, atacando primeiro o que está fraco, com toda iteração em modo Sniper pelo cânone §7.
2. Portar o ângulo pra outros formatos, variando a superfície e mantendo constante o que é comunicado.
3. Construir página ou prelander dedicada, com o tipo seguindo o awareness do ad e o julgamento pelo KPI, nunca pelo spend.
4. Portar pra Axon e TikTok, com o vídeo em 9:16, o end card à parte e a régua de budget e janela do canal novo.
5. Duplicar em ad set próprio em campanha ABO, cerca de um décimo do budget diário da principal, registrado no plano e executado pela `scale-engine`.
6. Devolver como creator report, que vira briefing pros creators ou pro editor.

Feche apresentando o plano como draft e oferecendo a Trilha 2 como próximo passo opcional; nunca rode as nove derivadas sem o membro pedir.

### Trilha 2 · Derivadas de formato (nove canais, sob pedido)

Leia `reference/trilha-2-derivadas.md`. Siga o fluxo do `recycler.md` a partir da etapa 3, porque a essência já saiu na ETAPA 1: consulte a base por formato com os sistemas nomeados da curadoria, gere as nove derivadas, faça a passada de estilo em cada uma (travessão zero em headline e subject line, no máximo dois no corpo; nenhuma derivada com aviso, disclaimer ou claim suavizado) e gere o `README.md` consolidado. Criativo `spend_winner` não entra aqui. A derivada de email é variação de teste e nunca substitui os flows da `retention-engine`: as três regras estão em `reference/email-sem-colisao.md`.

## SALVAR

Leia `reference/output-e-salvar.md`. Pasta `workspace/[produto]/content-recycler/[source-id]/`, com `essence.json` sempre, o `amplification-plan.md` e o `creator-report.md` da Trilha 1, e os nove arquivos mais o `README.md` quando a Trilha 2 roda. Cada `.md` voltado ao membro ganha o `.html` companion por `python3 tools/render_report.py <caminho do .md>`. No topo da pasta da skill, o índice `content-recycler.md` e `.html` lista todas as fontes trabalhadas, com a classe lida e o que existe pra cada uma; é o relatório que o painel exibe. Depois de salvar tudo: `python3 tools/manifest.py <slug> complete content-recycler` e `python3 .claude/lib/workspace-index/build_index.py <slug>`. As checagens de sucesso e o passo a passo pra acrescentar um formato novo estão em `reference/sucesso-e-customizacao.md`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`: o bloco da Trilha 1, com o diagnóstico dos quatro elementos, o framework que viaja, o porquê de ele funcionar e os próximos passos por dono, mais a oferta da Trilha 2; e o bloco da Trilha 2, com a distribuição sugerida por canal.

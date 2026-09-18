---
name: market-research
description: Engine profundo de pesquisa de mercado que produz o Unified Research Brief, o documento mais importante do sistema. Awareness pelos 5 níveis de Schwartz com distribuição numérica do TAM, sofisticação pelos 5 estágios com os claims saturados contados, perfil psicográfico pelas Core Five (desejo antes de demografia), core avatar e sub-avatares com um ângulo por sub-avatar, Voice of Customer com no mínimo 35 frases exatas em inglês (top 20 ranqueado, ids estáveis, vocabulário real do mercado pelo teste do Ctrl+F), causa raiz, panorama competitivo e síntese acionável. Use quando o membro disser "market research", "pesquisa de mercado", "pesquisar mercado", quando o product research estiver completo, ou quando o membro já tem produto definido (product research não é pré-requisito pra quem já tem produto). Alimenta todas as fases seguintes; se for raso, tudo depois será raso.
---

# Market Research · Passo 3 · apelido antigo: 02 <!-- gen:title -->

## Quando usar

Quando o membro tem produto definido e precisa entender a fundo o mercado, o público e o cenário competitivo antes de criar oferta e copy. Product research superficial ou ausente é aceitável em alguns casos; market research superficial garante copy, criativos e ads genéricos.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/profile.md`; ausente, oferecer rodar o `setup` inline.
2. `manifest.json` com `setup_complete === true`; mais de um produto = perguntar qual em 1 linha (sem perguntar se o membro já nomeou); ausente, `setup` inline.
3. `product-research` em `skills_completed`: presente, ler os dados preliminares. Ausente: membro que já tem produto (`product_url` ou situação B, C ou D) segue direto, sem warning nem `skipped_preflight`; membro sem produto recebe (A) rodar `product research` agora ou (B) seguir com o produto descrito inline marcando `skipped_preflight`.
4. `product_slug` começando com `dev-placeholder-`: (A) rodar `product research` ou (B) seguir inline marcando `skipped_preflight`.
5. `product_slug` vira `[produto]` em todos os paths.

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`), com a regra 0 em todo output interno (VOC em inglês ganha "tradução livre:" ao lado em pt-BR); copy consumidor-final e VOC literal sempre em inglês US.
2. `product-research/product-research.md` e `product-research/banco-de-marcas.md` quando existirem (jogada vencedora, elementos validados, awareness preliminar, VOC das reviews de 1 a 2 estrelas).
3. Base pelo índice (domínios `market-research-voc` e `persuasion-psychology`): `python3 .claude/lib/kb-index/kb_lookup.py --skill market-research --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas adicionais por etapa; as queries embutidas em cada arquivo de `reference/` são piso obrigatório, rodam sempre e não contam no teto; nunca query genérica nem busca repetida.

## Fluxo da skill

### ETAPA 0 · Pré-flight

É a checklist acima; o texto integral está em `reference/contexto.md`.

### ETAPA 1 · Confirmar produto e mercado geográfico

Leia `reference/produto-e-mercado.md`. Confirme o produto (link do profile ou descrição do membro) e o mercado geográfico propondo `manifest.market` como default; "global" vira o mercado anglo-saxão. O mercado vai pro relatório e de volta pro manifest.

### ETAPA 2 · Awareness (5 níveis de Schwartz)

Leia `reference/awareness.md` e puxe os sistemas listados. Pesquise sinais de cada nível na web (volume de busca por problema e por categoria, social chatter, conteúdo do nicho) e estime a distribuição do TAM em porcentagem por nível. Sem sinal suficiente, aplique o default do bucket da tabela (nicho novo, maduro ou commodity) com `awareness_distribution_source: "default"`; palpite mais pesquisa divergente = `hybrid`. Dominante = o maior percentual; empate de níveis adjacentes (5 pontos ou menos) = `dominant_awareness` no de maior intenção de compra e o outro em `dominant_awareness_secondary`. Documente as implicações práticas por nível (advertorial, landing, PDP robusta, PDP enxuta).

### ETAPA 3 · Sofisticação (5 estágios)

Leia `reference/sofisticacao.md` e puxe os sistemas, inclusive o Buzzword Tally. Sem `product-research`, colete agora de 5 a 10 concorrentes por `WebSearch` e os claims dos ads ativos na Meta Ad Library (fetcher Playwright se barrar); de dez a quinze claims reais bastam e a ETAPA 7 reaproveita a mesma coleta. Classifique o estágio pela tabela, liste claims saturados, comuns, raros e ausentes pela contagem, e defina a resposta estratégica.

### ETAPA 4 · Perfil psicográfico profundo

Leia `reference/perfil-sistemas-e-coleta.md` e depois `reference/perfil-camadas.md`. Coleta resiliente em Reddit, Amazon, TikTok, fóruns, Quora, Trustpilot e grupos (`WebSearch` pra descobrir, `WebFetch` pra ler, fetcher Playwright quando barrar; fonte que caiu em tudo vai pra `sources.blocked_sources`, nunca VOC inventada). Construa pelas Core Five na ordem desejos, experiências, emoções, comportamentos e demografia por último. Camadas: hopes e dreams específicos, victories e failures, forças externas culpadas, prejudices, core beliefs desempacotadas em experiência, emoção e comportamento, o paradoxo; demografia só quando refina; dores hierarquizadas com frequência; desejos com o desejo por trás e o ranking de alcance, urgência e permanência; seis tipos de objeção com a quebra pelos sistemas nomeados; trigger events.

### ETAPA 4.5 · Core avatar e sub-avatares (a camada que vira ângulo)

Leia `reference/core-avatar-e-sub-avatares.md`. Core avatar com UMA categoria (quase sempre desejo de superfície, na frase "I want X"; reclamação vira desejo espelhado), escolhido pelo ranking da ETAPA 4; um core avatar até cem mil dólares por mês. Sub-avatares com duas ou mais categorias, sempre um desejo e nunca dois, demografia por último, pesquisados uma categoria por vez. Cada sub-avatar carrega um único `angle` em frase completa, nascido da lacuna entre o desejo e o que a pessoa já tentou ou faz. Colete os `labels[]` com que o mercado se nomeia. Saída obrigatória: `core_avatar`, `sub_avatars[]` e `labels[]`.

### ETAPA 5 · Voice of Customer (mínimo 35 frases exatas)

Leia `reference/voc-mineracao.md` e `reference/voc-vocabulario-e-ids.md`. Nunca parafrasear; VOC sempre em inglês US. Mínimos: quinze frases de problema, dez de desejo, dez de frustração, mais os termos recorrentes (3 ou mais vezes) com contagem. Membro com lista ou clientes: giveaway survey (só com lista acima de 2 a 3 mil compradores) e warm calls. Teste do Ctrl+F obrigatório: `market_vocabulary.words_used[]` com contagem e `saturated_in_market` (termo que domina os claims da ETAPA 3) e `words_absent[]` com o substituto real. Curadoria do `voc_top20` (id, rank, count, category). Ids estáveis `voc-NNN`: cunhados na ordem do rank na primeira execução, mesmo namespace em `voc_evidence[]`, mantidos pra sempre em re-execução (só append). Menos de 35 frases: nunca frases sintéticas; gravar `voc_count`, `voc_adequacy` (`ok` com 35 ou mais, `medium` entre 15 e 34, `insufficient` abaixo de 15, que bloqueia a `copy-engine` via `skills_blocked`) e seguir com as outras etapas.

### ETAPA 6 · Root Cause Research

Leia `reference/causa-raiz.md`. Pra cada dor central: causa superficial, causa intermediária e causa raiz proprietária (real, nova pro mercado, nomeável, que externaliza a culpa). Documente 2 a 3 opções pra oferta escolher; alimenta o advertorial e o corruption angle.

### ETAPA 7 · Competitive Landscape (overview)

Leia `reference/panorama-competitivo.md`. Os 5 a 10 maiores concorrentes, claim principal, faixa de preço, posicionamento e gaps óbvios; soluções alternativas por categoria em `alternative_solutions`. A `competitor-analysis` aprofunda.

### ETAPA 8 · Síntese estratégica (Unified Research Brief)

Leia `reference/sintese.md` e puxe os sistemas (Unified Research Document, Psychological Audit, Ultimate Message Map). Consolide nos nove blocos: visão do mercado, arquitetura de avatar e perfil, dores e desejos, VOC curada com o vocabulário, objeções e quebras, trigger events, causas raiz candidatas, panorama competitivo e implicações estratégicas (tipo de página, tipo de lead, tipo de mecanismo, ângulos ranqueados nomeando o sub-avatar).

### Regra de parada e validação final

Leia `reference/parada-e-validacao.md`. Pare quando a pesquisa produziu de 5 a 10 boas ideias de anúncio; pesquisa pausa, não termina. Antes de salvar, os doze itens da validação (35 frases exatas, `voc_top20` e ids estáveis, `core_avatar` com uma categoria, `sub_avatars[]` com um `angle` cada, `labels[]`, `market_vocabulary`, ideias de anúncio, awareness numérico, claims saturados listados, quebra por objeção, recomendações acionáveis). Fontes e procedência só no `dados.json`, nunca no relatório.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/market-research/`; três artefatos: `market-research.md` (fonte canônica), `market-research.html` por `python3 tools/render_report.py workspace/[produto]/market-research/market-research.md` e `dados.json` no schema de `reference/dados-json.md` (awareness, sofisticação, `voc_phrases`, `voc_top20`, `voc_count`, `voc_adequacy`, `skills_blocked`, `sources`, `core_avatar`, `sub_avatars[]`, `labels[]`, `market_vocabulary`, `avatar`, `trigger_events`, `objections`, `alternative_solutions`, `root_cause_candidates`, `strategic_implications`), VOC sempre em inglês. Depois `python3 tools/manifest.py <slug> set` com `market`, `voc_count`, `voc_adequacy`, `awareness_distribution` e `sophistication_stage`, `python3 tools/manifest.py <slug> complete market-research` e `python3 .claude/lib/workspace-index/build_index.py <slug>`. O `dados.json` abre pelo objeto `resumo`, até doze campos curtos com o que a fase seguinte lê de primeira; ele espelha campos que já estão no arquivo e é preenchido por último (formato em `reference/dados-json.md`).

## Mensagem final

Íntegra em `reference/mensagem-final.md`: brief completo, fundação de tudo; próximos passos 'competitor analysis' (recomendado primeiro) ou 'offer'.

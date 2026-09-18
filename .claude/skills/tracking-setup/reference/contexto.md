# Tracking Setup · Referência: Índice, quando usar, pré-flight, gate de consistência, contexto a carregar e cascade de MCP

> O texto integral das notas de índice (as 21 entradas e as três que ficam com a retention-engine), do quando usar, do pré-flight com os escapes ES1 e ES2, do gate não-bloqueante da consistency-audit, do contexto a carregar com o sistema-espinha (query exata) e da cascade de MCP pra leitura do EMQ. Abra antes da ETAPA 1.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (mapa skill→domínio no README). O índice lista **21 entradas** com `use_in_skill` incluindo a `tracking-setup` — o bloco de atribuição/tracking, espalhado por 6 domínios: `meta-ads-strategy` (4), `scaling` (8), `retention-email` (5), `finance-projections` (2), `market-research-voc` (1) e `page-landing-cro` (1). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` (`deep=true`) com a `best_query` **byte-exata** de cada um, embutida no ponto de uso das ETAPAs abaixo. NUNCA query genérica.
>
> **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill tracking-setup --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 6 buscas por etapa. As queries já embutidas na etapa são o mínimo garantido. Não repita busca de framework já puxado na sessão.
>
> **Três entradas ficam de fora por decisão explícita** (o índice lista a `tracking-setup` nelas, mas o ponto de uso real é a skill `retention-engine`): **Arquitetura Confirmation → Self-Segmenter → Welcome**, **Hot-Time Anchor** e **Métricas de SMS (EPM / CTR / UNSUB) + benchmarks** são arquitetura de flow de email, regra de horário de disparo e leitura de canal de SMS — a `tracking-setup` não constrói flow nem instala SMS; quem as puxa é a `retention-engine` (retention, Fases A/B). O que esta skill toca de email é o **sinal** (captura on-site alimentando Advanced Matching/EMQ e a lista própria), coberto na ETAPA 2.

## Quando Usar

Quando a página já está deployada na loja (Skill `page-build`) e o membro precisa garantir que cada visita e compra seja medida ANTES de gastar dinheiro com ads. As Skills `creative-engine` (creatives) e 10 (ad-strategy) exigem no pré-flight `manifest.tracking.tracking_ready == true` (Pixel + CAPI validados, EMQ ≥ 6.0 — ou o caminho `pending_traffic` da ETAPA 3 pra loja pré-launch sem volume) — esta é a skill que constrói, valida e grava esse contrato.

É uma skill **operacional** (passo a passo pra executar no Shopify + Events Manager), não conceitual. Sem ela, os criativos da `creative-engine` e a campanha da `ad-strategy` viram dinheiro queimado por falta de sinal de conversão.

## Antes de Começar

### Pré-flight (OBRIGATÓRIO)

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

- [ ] `workspace/[produto]/manifest.json` existe e é parseável
- [ ] `page-build` está em `skills_completed` (página no ar) — sem página deployada, ViewContent/AddToCart/Purchase não têm onde disparar
- [ ] Budget legível: `manifest.budget_daily` (campo numérico canônico, $/dia — gravado pela `setup`); em manifest legado sem ele, `manifest.budget_tier` e/ou o budget declarado em `workspace/profile.md` — é o que refina a decision tree do analytics stack (ETAPA 4). O `offer-builder/dados.json` NÃO tem campo de budget; não o exija por isso.
- [ ] Acesso ao Shopify admin da loja + uma conta Meta Business (Business Manager + ad account + um Pixel/Dataset)

**Arquivo de pré-flight faltante (escape path, rule ES1):** se `manifest.json` não parseia, NÃO aborte seco — ofereça **(A)** rebuild do manifest (inspeciona `workspace/[produto]/` e reconstrói, perguntando budget/stage), OU **(B)** restore do backup mais recente (`.manifest-backup-*.json`). Ver `.claude/rules/emergency-escape-paths.md` ES2.

Se `page-build` NÃO está em `skills_completed`, ofereça: **(A)** rodar `build page` (`page-build`) agora pra subir a página, OU **(B)** prosseguir só com a instalação do pixel + CAPI marcando `manifest.skipped_preflight += ["page-build"]` e avisando no output final que a validação de eventos de funil (ViewContent/AddToCart/Purchase) fica incompleta até a página existir.

### Gate de consistência (Skill `consistency-audit`) — não-bloqueante aqui

A `consistency-audit` gateia o **launch** (Skill `ad-strategy`), não o tracking. Esta skill pode rodar antes ou depois da `consistency-audit`. Se `consistency-audit/dados.json` existir com `launch_recommendation == "BLOCK"`, apenas registre no output final que o launch está bloqueado até a `consistency-audit` passar — mas siga instalando o tracking normalmente (ter pixel pronto não gasta dinheiro).

### Contexto a carregar

1. **Idioma do relatório (regra 0 do CLAUDE.md — INVIOLÁVEL):** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). **TODO output interno desta skill (relatório de setup, decision tree, instruções) e toda conversa com o membro usam esse idioma**, com a régua de linguagem simples da regra 0 (nenhuma sigla sem explicação imediata na primeira vez — EMQ, CAPI, MMM, NCPA inclusas —, zero frase de analista comprimida). Esta skill não gera copy consumidor-final, então a regra de "copy pública sempre em inglês" não tem objeto aqui.
2. Leia `manifest.json` → `stage` (starter / validating / scaling) e `budget_daily` (o valor numérico canônico de $/dia, gravado pela `setup`; fallback em manifest legado: `budget_tier` ou o `profile.md`). **O stage é o que define o analytics stack recomendado** (ver decision tree); o budget refina. Detecção automática de stage em `.claude/rules/member-stage-awareness.md` se o campo estiver ausente.
3. **Puxe os SISTEMAS NOMEADOS da base — NUNCA query genérica.** As queries estão embutidas no ponto de uso de cada ETAPA abaixo (blocos "Puxe antes"). Carregue JÁ, antes da ETAPA 1, o sistema-espinha desta skill:
   - **CAPI & Pixel Data / Event Match Quality** (rode `CAPI pixel advanced matching event match quality email click ID below 5`) — ads são um loop de feedback de dados (dado ruim entra, decisão ruim sai); os parâmetros de match de maior prioridade são **email e Click ID** (identificadores 1:1); EMQ abaixo de 5 é inutilizável pro Meta; TODOS os parâmetros de Advanced Matching ligados; e **coletar mais emails on-site é a otimização técnica de maior alavancagem** (recupera 40%+ das conversões rastreadas). É o sistema que governa as ETAPAs 1-3.

   (Deduplicação por `event_id` e os 5 eventos padrão do funil são procedimento operacional das ETAPAs 1-2, não sistema da base — não invente query pra eles. A Estrutura de Assets Anti-Ban pertence à skill `setup` no índice, não a esta.)

### Detecção de MCP (cascade)

A instalação do pixel é feita no Shopify admin (a Meta gerencia o snippet via integração nativa); o MCP entra na **verificação do Event Match Quality (EMQ)** e na leitura de datasets. Cascade:

- **Caminho 1 — MCP oficial Meta** (`mcp.facebook.com/ads`): tools `mcp__meta__ads_*`. Usar `ads_get_datasets` / equivalente de insights de dataset pra ler o EMQ programaticamente, sem screenshot manual.
- **Caminho 2 — Pipeboard** (`mcp__meta-ads__*`): fallback automático quando o oficial está indisponível.
- **Caminho 3 — manual**: o membro tira screenshot do Events Manager mostrando a dupla-coluna (Browser + Server) e o Event Match Quality (escore 0-10 por evento), e cola pra você validar visualmente.

Logue qual caminho foi usado no campo `source` do JSON de saída (convenção em `.claude/lib/mcp-detect/README.md`). Se nenhum MCP estiver presente, o Caminho 3 (manual) é o normal — não é degradação.

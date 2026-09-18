# Scale Engine · Referência: Quando usar, pré-flight e contexto a carregar

> O texto integral de quando usar (com a pré-condição honesta), a regra de idioma, o pré-flight (arquivos exigidos, as 4 classes como gatilho, escape ES1) e os itens de contexto: os arquivos a ler na ordem, a tabela dos seis campos da `finance-engine` com o ponto de uso e o fallback de cada um, o ad-log, o `sourcing`, a janela de promo e os sistemas da base com a `best_query` exata. Abra antes da ETAPA 1.

## Quando Usar
Quando o membro tem **breakthrough(s)** provados (criativo cujo KPI é melhor que o KPI da campanha **e** que puxa spend — classificação canônica em `.claude/lib/ad-taxonomy/README.md` §2, medida pela skill `ad-analysis`) e quer aumentar spend de forma sistemática sem queimar conta. Esta skill é a **camada de execução operacional** de escala: qual régua de subida e descida seguir (o Scaling Protocol da ETAPA 3.5), qual estrutura montar no Ads Manager, quanto duplicar, quando surfar, quando recuar. PSM e 4Pi continuam como leitura de diagnóstico (a skill `ad-analysis` calcula), mas o "exatamente o que fazer" vive aqui.

> **Pré-condição honesta:** escala não conserta ad ruim nem oferta fraca. Se não tem breakthrough, isto não é hora de escalar — é hora de mais criativo (skill `creative-engine`) e melhor oferta (skill `offer-builder`). Criativo que bate o KPI mas não puxa spend (`KPI winner`) **não** conta como liberação de escala. A skill detecta isso na ETAPA 3 e te manda de volta sem culpa.

### report_language (regra 0 do CLAUDE.md — INVIOLÁVEL)

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma, com o estilo de escrita da regra 0 do `.claude/CLAUDE.md` na íntegra (linguagem simples, sigla sempre explicada na primeira vez, português natural sem jargão cru). **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

### Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.
- [ ] `ad-strategy/dados.json` + `ad-analysis/dados.json` existem (`workspace/[produto]/ad-analysis/dados.json`)
- [ ] Manifest tem `ad-analysis` em `skills_completed`
- [ ] `manifest.psm_real` foi gravado por ≥ 1 análise recente (senão, rodar 11 — quem calcula `psm_real`). Leia junto `manifest.psm_real_basis` — a base decide se a comparação com o teórico vale (ver "PSM real (vs teórico)")
- [ ] Existe ≥ 1 **breakthrough** entre os criativos analisados pela `ad-analysis`. A classificação canônica é a das **4 classes** de `.claude/lib/ad-taxonomy/README.md` §2 (loser · KPI winner · spend winner · breakthrough) — a skill `scale-engine` **não redefine** essas classes, só as lê:
  - **`breakthrough`** = KPI do AD melhor que o KPI da CAMPANHA **e** puxa spend → **é o único que libera escala**.
  - **`KPI winner`** (bate o KPI mas **não** puxa spend) → **NÃO libera escala.** O KPI bonito veio de amostra pequena; o cânone manda tratá-lo como loser para decisão.
  - **`spend winner`** (puxa spend com KPI abaixo do da campanha) → itera, não escala.
  - Se `ad-analysis/dados.json` já traz a classe por criativo, use-a direto. Se traz só `winners[]` (formato anterior), aplique a régua do cânone §2 sobre os mesmos números **antes** de liberar escala — "CPA ≤ target" sozinho não distingue breakthrough de KPI winner. Para carregar o sistema nomeado, rode `breakthrough spend winner KPI winner losing ad classificação destino por categoria`.
  - Post ID dedicado (`champions[]`) segue **opcional** pra escalar. Sem breakthrough, escala é prematura.

Se algum arquivo de pré-flight faltar, não aborte seco (rule `emergency-escape-paths.md` ES1). Ofereça **(A)** rodar a skill faltante agora (`ad-analysis` pra `ad-analysis/dados.json`/`psm_real`, 10 pra ad-strategy), **OU (B)** prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` e avisando no output final que recomenda re-executar.

### Contexto a carregar

1. Leia `workspace/profile.md` (budget atual + stage — define ponto de partida e agressividade)
2. Leia `workspace/[produto]/offer-builder/offer-builder.md` (se não existir, leia o legado `relatorio.md`) + `offer-builder/dados.json` (breakeven CPA/ROAS, `cogs_breakdown`, PSM projetado — define o teto de cost cap / bid cap). Leia também `manifest.margin_warning`: se `true`, a Skill `offer-builder` flagou margem ponderada < $20/pedido — tratar como pré-requisito de prontidão na ETAPA 3 (margem apertada amplia o dano de qualquer CPA acima do alvo na escala)
3. Leia `workspace/[produto]/ad-strategy/ad-strategy.md` (estrutura de campanha atual: estamos na estrutura de teste da `ad-strategy` — 1 campanha CBO → N ad sets, 1 por conceito → 3 ads? cost cap já roda?)
4. Leia TODAS as análises em `workspace/[produto]/ad-analysis/` em ordem cronológica (trajetória real de performance, classificação por criativo, CPM por conta) + `dados.json` (handoff da skill `ad-analysis`)
5. Leia scale plans anteriores em `workspace/[produto]/scale-engine/` (se existir — comparar premissas com realidade)
5b. Leia `manifest.agentic` **(if exists)** — `{ready, channel_enabled, score, checked_at}` escrito pela Skill `agentic-readiness`. Se `ready: true`, a loja está descobrível por agentes de compra com AI (ChatGPT, Perplexity, Google AI Mode) — trate esse referral como **fonte incremental de tráfego no scale horizontal** (ver ETAPA 8). Ausente ou `ready: false` → ignorar silenciosamente (canal não existe ainda; se o membro está escalando forte, vale sugerir rodar a `agentic-readiness` como quick win).
5c. **Leia os dois cânones antes de qualquer recomendação** (leitura obrigatória, não opcional — a skill referencia, nunca redefine):
   - `.claude/lib/ad-taxonomy/README.md` — **§2** (as 4 classes que definem o gatilho de escala) e **§5** (Scaling Protocol, ABO paralelo, gate click-based e a regra de reset da meia-noite). É a fonte de verdade de QUANDO e QUANTO subir/descer.
   - `.claude/lib/unit-economics/README.md` — **§1** (margem de contribuição ≠ lucro) e **§4** (a espiral do ROAS). É o gate obrigatório antes de qualquer recomendação de cortar spend.

   Onde a skill e o cânone divergirem, **o cânone vence** — e a divergência é bug da skill, a reportar.

5d. Leia `workspace/[produto]/finance-engine/dados.json` **(se existir)** — a skill `finance-engine` é a dona do modelo financeiro completo (cânone §5) e publica os números que esta skill hoje estima sozinha. Seis campos, cada um com o ponto exato onde entra:

   | Campo da `finance-engine` | Onde esta skill usa | Fallback quando a `finance-engine` não rodou |
   |---|---|---|
   | `cash.cash_needed_90d` | ETAPA 6 — substitui o `cash_gap_projected` estimado localmente | Fórmula local da ETAPA 6 |
   | `cash.float_stack.total_float_days` | ETAPA 6 — o float real do membro no lugar do `payout_lag_days` isolado | `payout_lag_days` (3-5 nominais; 7-14 pra loja nova) |
   | `cash.runway_months` | ETAPA 6 e ETAPA 7 — quantos meses o caixa aguenta o plano | Não existe hoje; segue sem a linha |
   | `monthly_model.fixed_costs_monthly` | ETAPA 1 (não perguntar o que já está gravado), gate de corte e ETAPA 7 (camada de fixo na projeção) | Pergunta ao membro, como hoje |
   | `payback.scale_ceiling_monthly_spend` | ETAPA 3.5 — teto dos passos de +20% | Não existe hoje; o teto é descoberto empiricamente (a escola quebra e recua) |
   | `roas_spiral.cut_spend_recommendation_allowed` (+ `roas_spiral.verdict`) | Gate de corte por ROAS — decide o `fixed_cost_gate.roas_cut_recommendation` | Gate local: fixos conhecidos → conta; desconhecidos → pergunta |

   **Leitura aditiva:** esta skill **lê e aplica, nunca recalcula** os campos acima; e sem o arquivo da `finance-engine`, cada ponto de uso cai no fallback da coluna 3 — o comportamento de hoje, inteiro. A `finance-engine` nunca é pré-requisito da `scale-engine`.

5e. Leia `workspace/[produto]/ad-log.md` **(se existir)** — o registro cronológico de toda mudança executada na conta (cânone `.claude/lib/ad-log/README.md`). É DAQUI que sai a última mudança de budget e há quanto tempo ela aconteceu — **o gate de 24h entre degraus é verificado no log, não de memória** (ETAPA 3.5); e mudança recente ainda sem leitura fechada é motivo pra segurar o passo. Sem o arquivo (conta nunca operada pelas skills), o histórico vem do membro — e o log nasce na primeira mudança que esta skill instruir/executar.

5f. Leia `workspace/[produto]/sourcing/dados.json` **(se existir)** — a `sourcing` (ETAPA 12) grava `calendar.volume_confirmation_30_60_90` (confirmação escrita do fornecedor pro volume de 30/60/90 dias) e `calendar.reorder_point_days` (ponto de recompra em dias de estoque restante). Existindo, esses campos respondem o check de fornecedor da ETAPA 3 e da ETAPA 6 — **não re-pergunte ao membro**. Sourcing nunca rodou → o check segue com a pergunta de hoje.

5g. Leia `manifest.promo.active` **(se existir — a skill `promo-engine` grava; leitura aditiva, nunca pré-requisito):** se `true`, a conta está numa **janela promocional com data-fim** — degraus e reset seguem o regime da janela (exceção (a) do cânone §5: budget planejado da promo direto, surf + reset da meia-noite TODA noite sobre o gasto real), e esta skill **não "corrige" budget de promo pra baixo por conta própria** — a dona da janela é a `promo-engine`, e qualquer ajuste na campanha de promo passa por ela. O evergreen fora da promo segue o protocolo normal. Campo ausente ou `false` = sem janela, nada muda.

6. **Puxe os SISTEMAS NOMEADOS da base — NUNCA query genérica** (índice em `.claude/lib/kb-index/`, mapa skill→domínio no README):
   - Os domínios desta skill são `scaling` e `finance-projections`; entradas de outros domínios marcadas pra esta skill (ex: `ops-scale-risk`, `affiliate-creator-channels`) contam igual.
   - **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill scale-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 10 buscas por etapa. As queries já embutidas na etapa são o mínimo garantido. Não repita busca de framework já puxado na sessão.

   Mínimo a carregar antes de montar qualquer plano:
   - **Scaling Protocol & Decision Tree (fonte primária 2026)** (rode `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo`) — **a espinha única** de quando subir, segurar e descer (ETAPA 3.5). Carregue este primeiro.
   - **Reset da meia-noite** (rode `reset da meia-noite metade do spend real nunca budget nominal explode a conta`) — a regra de risco financeiro que acompanha TODA subida de budget (ETAPA 3.5)
   - **Taxonomia de Winners (Loser / KPI Winner / Spend Winner / Breakthrough)** (rode `breakthrough spend winner KPI winner losing ad classificação destino por categoria`) — define o gatilho de escala do pré-flight e da ETAPA 3
   - **Performance Gate Scaling (PGS) + The Three PGS Principles** (rode `Performance Gate Scaling PGS 3 principles trailing CPA automated rules` e `The three PGS principles never scale past margin trailing multi-day KPI campaign-based`) — nunca escalar além da margem; opera **dentro** do Scaling Protocol, não em paralelo a ele
   - **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM golden ratio LTV CPA COGS formula`) + **PSM Scaling Thresholds** (rode `PSM thresholds 1.3 aggressive 1.1 healthy breakeven zone scaling decision`) — leitura de diagnóstico (a `ad-analysis` calcula)
   - **Three Budget Scaling Methods** (rode `Three budget scaling methods farmer 5% aggressive 50% business-led MRR`) — farmer 5% vs aggressive 50% vs business-led
   - **Three Reasons Scale Breaks** (rode `three reasons scale breaks unit economics funnel imbalance cash constraints can we spend more tomorrow`) — unit economics, funnel imbalance, cash
   - **Creative Diversity as a Scaling Mechanism** (rode `creative diversity as a scaling mechanism funnel balance video image 4Pi same position`) — combustível da escala

   Aprofunde — escala errada queima budget mais rápido que ad ruim.

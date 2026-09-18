# Retention Engine · Referência: Quando usar (as duas fases), base de conhecimento e pré-flight

> O texto integral das duas fases com o framing de infraestrutura de cash flow, da consulta à base pelo índice, e do pré-flight (idioma, detecção de fase, gate phase-aware da consistency-audit, checagens por fase com o ESP, a oferta, o market research, os hooks da copy e os cohorts da finance-engine). Abra antes da ETAPA 1.

## Quando Usar — DUAS fases

Esta skill roda em dois momentos diferentes do pipeline, com escopos diferentes. O framing importa: **a Fase A é infraestrutura de cash flow, não email marketing** — campanhas/newsletters de email continuam sempre pós-launch.

**Fase A — Flows de recuperação (PRÉ-LAUNCH, na ordem canônica: depois da `checkout-aov`/`bonus-delivery` Fase A, antes dos criativos da `creative-engine`):** operador de elite nunca liga tráfego pago sem o abandoned cart flow armado — é a receita mais barata que existe (recupera parte dos ~70% de carrinhos abandonados) e custa zero (free tier do ESP). A Fase A monta APENAS os flows disparados por evento que recuperam dinheiro do tráfego do launch:
- **Abandoned Cart** (fluxo 2) — o coração da fase
- **Post-Purchase Welcome** (fluxo 3) — mata buyer's remorse, reduz refund, pede a primeira review
- **Welcome Series Email 1** SÓ SE a página promete welcome offer / há bonus com `delivery_trigger: on_signup` (promessa da página precisa existir no dia 1 — mesmo princípio da Fase A da `bonus-delivery`)

**SEM segmentação na Fase A** — não há base pra segmentar (zero ou quase zero compradores), e não precisa: são flows por evento, funcionam com o primeiro visitante.

**Fase B — Retenção completa (PÓS-LAUNCH, ≥ 50 compras no ESP):** com dados mínimos existe o que segmentar. Entram: Welcome Series completo (emails 2-4), Win-Back, Replenishment, cadência/coordenação de lista, e as ops pós-launch (chargeback, refund da garantia, CS básico — seção própria). Antes de 50 compras, segmentação é noise — por isso ela espera.

## Base de conhecimento (consulta pelo índice, NUNCA query genérica)

Esta skill puxa SISTEMAS NOMEADOS de email lifecycle e psicologia de persuasão da base — não query genérica tipo "email flows" ou "abandoned cart". A consulta segue o índice (`.claude/lib/kb-index/README.md`):

Os domínios desta skill são `retention-email` e `persuasion-psychology`. Duas entradas de OUTROS domínios também pertencem a esta skill e já estão embutidas no ponto de uso: **Desire Calendar** em `market-research-voc` e **Subscription Economics Playbook** em `finance-projections`.

**Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill retention-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 10 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão.

## Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

**Idioma (report_language).** Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). Todo output interno (`retention-engine/retention-engine.md`/`.html`, `flow-metadata.json` descritivo, mensagens e perguntas ao membro) usa esse idioma. **A copy dos emails em si (subject, preview, body, CTA) permanece SEMPRE em inglês US**, independente do report_language — é consumidor-final do mercado US.

### Detecção de FASE (primeiro passo)

Ler `manifest.retention` (se existir) + `manifest.skills_completed`:

- **Fase A** se: `manifest.retention.phase_a_done != true` E o storefront existe (`page-build` em `skills_completed` — sem loja no ar, não há evento de cart/purchase pra disparar flow). É o caminho normal pré-launch: `ad-strategy` AINDA NÃO rodou, e está tudo bem — a Fase A vem ANTES dela na ordem canônica.
- **Fase B** se: `manifest.retention.phase_a_done == true` E a campanha está ativa E há **≥ 50 compras** no ESP/Shopify (perguntar ao membro se não houver dado). Se o membro pedir "retention" com < 50 compras e Fase A já feita, explicar que win-back/segmentação prematuros viram noise e oferecer: revisar/otimizar os flows da Fase A com os dados que já existem, ou esperar o volume.
- Membro pediu explicitamente um flow específico → respeitar, mas avisar se está fora da fase (ex: win-back com 10 compras).

### Gate de consistência (Skill `consistency-audit`) — phase-aware
Ler `workspace/[produto]/consistency-audit/dados.json` **se existir**:
- **Na Fase A, arquivo ausente é o NORMAL** — a `retention-engine` Fase A roda ANTES da `consistency-audit` na ordem canônica (a `consistency-audit` audita inclusive os emails da Fase A, via check M7). Prosseguir sem cerimônia.
- Se existir com `launch_recommendation == "BLOCK"` → os fluxos de email vão herdar o drift detectado (mecanismo divergente, VOC sem rastreio, oferta diferente da página) e propagar inconsistência pra base de subscribers. Oferecer ≥2 caminhos: **(A)** rodar a skill `consistency-audit` agora pra corrigir o drift, OU **(B)** prosseguir mesmo assim marcando `manifest.skipped_preflight += ["consistency-audit"]` e avisando no output final que recomenda re-executar após corrigir.
- Se `CAUTION` → exibir warnings e pedir OK do membro antes de gerar fluxos.
- Se `GO` → prosseguir.

### Checagens por fase

- [ ] **Fase A:** `page-build` em `skills_completed` (loja no ar). **Fase B:** `ad-strategy` em `skills_completed` + campanha ativa + ≥ 50 compras (detecção acima).
- [ ] **ESP identificado (as duas fases).** Ler `manifest.esp` (e `profile.md` → `esp: "klaviyo" | "omnisend" | "mailerlite" | "shopify_email" | "none"` — enum exato do manifest-schema, `shopify_email` com underscore). Se o campo estiver **ausente** (membro nunca rodou setup completo), PERGUNTAR inline ao membro qual ESP ele usa e gravar a resposta em `manifest.esp`. Se `esp: "shopify_email"`, **não abortar** — seguir direto pro Caminho 2 (assets + setup-guide adaptado ao editor do Shopify Email); ver a nota de limitações na seção do Caminho 2. Se `esp: "none"` (membro não tem ESP), **não abortar** — recomendar Klaviyo (free tier até 250 contatos + Shopify integration nativa — o custo zero é parte do argumento da Fase A), e se o membro topar, gravar `manifest.esp = "klaviyo"` e seguir; se ele preferir decidir depois, gerar os fluxos no fallback HTML + setup-guide (seção abaixo) pra ele importar quando escolher.
- [ ] `offer-builder/offer-builder.md` (ou o legado `relatorio.md` — mesmo fallback vale pras outras fases) + `offer-builder/dados.json` carregados (pra saber a janela de reorder, guarantee period, e os `bonuses[]` com seus `delivery_trigger`)
- [ ] `market-research/market-research.md` carregado (objeções = hooks de win-back; dores = hooks de abandoned cart)
- [ ] `copy-engine/dados.json` carregado **(if exists)** → campo `email_hooks[]` (3-5 hooks de follow-up que a `copy-engine` gera na ETAPA 7, derivados das top-5 headlines + Big Idea + objeções — inglês US; também na seção canônica `## Email Follow-up Hooks` de `copy-engine.md`). É o seed dos subject lines/aberturas dos flows — ver nota em "Fluxos base". Ausente (copy legada, gerada antes do contrato) → derivar os hooks das headlines de `copy-engine.md` direto.
- [ ] `finance-engine/dados.json` carregado **(if exists)** → bloco `cohorts`, quatro campos: `ltv_pct_by_month`, `decay_factor`, `crossover_month` e `churn_spike_day`. É a curva de LTV **medida** do negócio (a `finance-engine` a calcula a partir dos cohorts reais do membro), e ela troca o benchmark por número em três lugares: o beat de churn do post-purchase (fluxo 3), a janela de reorder do replenishment (fluxo 5) e o gatilho do win-back (fluxo 4). **Fallback:** arquivo ausente, ou `cohorts.calibrated: false` / `decay_source: "assumed"` — os fluxos rodam pelos benchmarks e pela janela declarada pelo membro, exatamente como hoje. A `finance-engine` nunca é pré-requisito desta skill.

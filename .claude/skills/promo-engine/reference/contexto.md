# Promo Engine · Referência: Índice de frameworks, cânones, quando usar, idioma, pré-flight e contexto a carregar

> O texto integral do índice de frameworks e dos três cânones que governam a skill, de quando usar com a tabela da divisão de donos, da regra de idioma, do pré-flight com o escape da oferta ausente e da lista numerada do contexto a carregar. Abra antes da ETAPA 1.

> **Índice de frameworks:** os sistemas desta skill vivem espalhados em VÁRIOS domínios de `.claude/lib/kb-index/` (mapa skill→domínio no README) — `meta-ads-strategy`, `scaling`, `finance-projections`, `creatives-hooks-formats`, `retention-email`, `offer-pricing-guarantee`, `page-landing-cro`, `brand-building-bonus-aov`, `market-research-voc` e `supply-chain-sourcing`. Não existe domínio "promo" dedicado. **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill promo-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 10 buscas por etapa. As queries já embutidas na etapa são o mínimo garantido. Não repita busca de framework já puxado na sessão.
>
> **Cânones que governam esta skill:** `.claude/lib/ad-taxonomy/README.md` **§5** (Scaling Protocol e as duas exceções — **(a) promo com data-fim entra direto no budget planejado**, e o que protege a promo é o surf + o reset da meia-noite; **(b) "new reason to be scaling"** reinicia a leitura) e `.claude/lib/unit-economics/README.md` **§1** (margem de contribuição ≠ lucro) e **§4** (espiral do ROAS). Esta skill **referencia** os cânones, nunca os redefine — onde o texto daqui divergir, o cânone vence e a divergência é bug desta skill. Todo registro de mudança na conta segue o cânone `.claude/lib/ad-log/README.md`.

## Quando Usar

Quando existe (ou vai existir) uma **janela promocional com data de fim**: Black Friday/Cyber Monday e o Q4 inteiro, datas sazonais (Valentine's, Mother's Day, Memorial Day, Labor Day, Halloween) ou uma flash sale. Gatilhos: "black friday", "bfcm", "promo", "promoção", "sale", "q4", "cyber monday", "desconto sazonal".

**Não é fase do pipeline — é skill lateral, como a `finance-engine`.** Dispara por pedido do membro; a época é o motivo natural de chamar (setembro-outubro pra montar o Q4; meados de janeiro pro Valentine's — o Desire Calendar dá o timing de cada data). Pode rodar mais de uma vez por ano, uma rodada por janela.

**O que esta skill é dona e nenhuma outra era:** o calendário da janela, a mecânica da oferta promocional, o gate de números recalculados, a estrutura de campanha de promo, o plano de escala DENTRO da janela e a aterrissagem de volta pro evergreen.

**O que ela NÃO faz (divisão explícita com as vizinhas):**

| Trabalho | Dona | O que a `promo-engine` entrega pra ela |
|---|---|---|
| Produzir os assets de criativo (banners, statics, vídeos) | **08** | Brief de criativo de sale (ETAPA 6) |
| Escrever os emails/SMS e montar os sends no ESP | **13** | Calendário, janelas e segmentos (ETAPA 7) — a `retention-engine` executa os assets e mantém os flows coerentes com a promo no ar (flow nunca desliga durante campanha; se adapta) |
| Estrutura de campanha evergreen e teste de criativo | **10** | Nada — o evergreen segue intocado em paralelo |
| Escala evergreen fora de janela | **12** | O registro da janela (a exceção (a) do §5 só vale com data-fim) |
| Modelo financeiro completo | **15** | O flag de cohort de promo pra calibragem (ETAPA 10) |
| Estoque e fornecedor | **`sourcing`** | A cobrança da confirmação de volume antes da janela |
| Backups de conta, processadora e operação | **ops-engine** | Pointer na preparação |

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final permanece SEMPRE em inglês US** — nome da sale ("Black Friday Sale"), texto de banner ("25% off EVERYTHING"), headlines, emails. A escolha de idioma vale só pra documentação interna.

### Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `workspace/[produto]/offer-builder/dados.json` existe — é a fonte do stack de custos (`cogs_breakdown`, 8 campos), do `unit_economics.weighted_margin_per_order` e do `pricing.aov_expected`. Sem esses números o gate da ETAPA 4 não fecha
- [ ] Loja no ar (`manifest.storefront.page_url` ou confirmação do membro) — promoção pressupõe página publicada; sem loja, o caminho é o pipeline normal (`setup`→`ad-strategy`), não esta skill

Se `offer-builder/dados.json` faltar, não aborte seco (rule `emergency-escape-paths.md` ES1). Ofereça **(A)** rodar a skill `offer-builder` agora, **OU (B)** prosseguir pedindo direto ao membro o AOV e o custo por pedido item a item, marcando `manifest.skipped_preflight += ["offer-builder/dados.json"]`. O gate da ETAPA 4 aceita números vindos do membro — o que ele **não** aceita é número estimado.

**Histórico de ads (`ad-strategy`/`ad-analysis`) NÃO é pré-requisito**, mas muda a rota de criativo: com winners provados, a doutrina é "best ad + banner"; sem nenhum winner, a rota é a outra metade do blueprint — statics de foto do produto + oferta (ETAPA 6). **Loja nova na semana da BF é não** (CPM de US$ 300+ na semana): sem conta rodando, a recomendação honesta é não estrear na janela mais cara do ano.

### Contexto a carregar

1. `workspace/profile.md` — stage e budget (`member-stage-awareness.md`: os gates do protocolo não mudam por stage; o que muda é o apetite dentro deles — surf é coisa de `scaling`, starter roda a janela sem surf)
2. `workspace/[produto]/manifest.json` — **`target_cpa` e `breakeven_roas`** (se existirem, carregam o recálculo mais recente e prevalecem sobre o `dados.json` da `offer-builder` — mesma precedência das skills `ad-strategy` e `scale-engine`), `budget_daily`, `stage`, `breakthroughs[]`/`ad_classification[]` (matéria-prima do banner), `fixed_costs_monthly`, `esp`, `storefront.page_url`, `retention.phase_a_done`
3. `workspace/[produto]/offer-builder/dados.json` — `cogs_breakdown` (os custos em % do preço encolhem junto com o desconto; os custos em dinheiro por pedido não — a diferença é o que espreme a margem), `unit_economics` completo, `pricing.aov_expected`
4. `workspace/[produto]/finance-engine/dados.json` **(se existir)** — `handoff.for_skill_12` (custo fixo, teto de escala, caixa pra 90 dias, veredito da espiral) + `monthly_model.fixed_costs_monthly` + `roas_spiral` (a fórmula do breakeven com fixo vive na ETAPA 5 da `finance-engine` — esta skill a reaplica com a margem promocional, nunca a redefine) + `cohorts` (baseline pra leitura pós-promo). Leitura aditiva: sem o arquivo, a janela roda com margem de contribuição e a frase honesta do §1
5. `workspace/[produto]/sourcing/dados.json` **(se existir)** — `calendar.volume_confirmation_30_60_90` e `calendar.reorder_point_days` (a confirmação de volume por escrito que a janela vai consumir)
6. `workspace/[produto]/ad-analysis/dados.json` + `workspace/[produto]/ad-log.md` — classificação por criativo (o "best ad" do banner é `breakthrough` ou, na falta, o `spend_winner` mais estável), CPM da conta, trajetória
7. `workspace/[produto]/scale-engine/dados.json` **(se existir)** — escola de escala em uso, `scale_phase`, hábito de reset da meia-noite já instalado
8. `workspace/[produto]/ad-strategy/dados.json` **(se existir)** — estrutura evergreen atual, convenção de nomes, URL de destino
9. `workspace/[produto]/retention-engine/dados.json` **(se existir)** — flows ativos (o que a promo precisa adaptar, nunca desligar)
10. Rodadas anteriores desta skill em `workspace/[produto]/promo-engine/` — em especial `seasonal_vault[]` de janelas passadas: winners sazonais guardados são a primeira coisa a religar (ETAPA 6)
11. Os três cânones do header — leitura obrigatória antes de qualquer recomendação

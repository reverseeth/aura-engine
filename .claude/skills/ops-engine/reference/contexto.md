# Ops Engine · Referência: Índice, quando usar, idioma, pré-flight, contexto a carregar e a regra de honestidade

> O texto integral do índice de frameworks com a consulta pelo índice, de quando usar com os três momentos naturais e a fronteira com as vizinhas, da regra de idioma, do pré-flight, do contexto a carregar com os ponteiros de caixa e estoque, e da regra de que status de backup é confirmação do membro e nunca dedução. Abra antes da ETAPA 1.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (domínio `ops-scale-risk`, mapa skill→domínio no README). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica. **Esta skill é a consumidora que faltava** de 5 sistemas do domínio marcados como dormant no índice (`use_in_skill: "—"`) — a partir dela, eles são puxáveis. As 2 entradas do domínio que já transferem pra outras skills (expectativa de winning ad → `creative-engine`/`scale-engine`; mini-memo de criativo → `creative-engine`) continuam lá e NÃO são desta skill. O restante do domínio segue dormant de propósito (ver "O que esta skill NÃO faz").
>
> **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill ops-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 6 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão.

## Quando Usar

Quando a pergunta é sobre a **sobrevivência e a estrutura da operação**, não sobre um pedido, um ad ou o modelo financeiro. Gatilhos: "backup de conta", "risco", "processor", "processadora", "constraint", "gargalo", "operação", "continuidade", "plano B", "e se a conta cair", "memo", "exit", "moat", "quero vender a empresa um dia".

**Não é fase do pipeline — é skill de consulta lateral, como a `finance-engine`.** Três momentos naturais:

- **Cedo, logo depois do setup e antes do primeiro ad:** só a ETAPA 2 (continuidade). **Conta nova é a mais frágil da vida do negócio** — sem histórico de gasto, sem Business Manager verificado, com a processadora ainda desconfiando do volume. É exatamente quando um banimento ou uma retenção de repasse dói mais, e quando a redundância é mais barata de armar. A skill `setup` monta a estrutura; esta skill confirma que ela continua viva.
- **Recorrente:** revisão dos riscos abertos por trimestre; declaração da constraint 1 vez por ano (ou quando o negócio muda de patamar).
- **Antes de decisões grandes:** antes de escalar agressivo (`scale-engine`) e antes do Q4 — os dois momentos em que a operação quebra por trás enquanto todo mundo olha pros anúncios.

**O que esta skill responde e nenhuma outra respondia:** qual é o gargalo que decide o meu ano, o que acontece amanhã se a conta/a processadora/o fornecedor caírem, quanto do negócio depende de uma única pessoa, e o que um comprador encontraria se auditasse a operação hoje.

**O que ela NÃO faz:** não monta Business Manager nem registra marca (a montagem é da `setup` — aqui é status e processo); não calcula caixa, runway nem float (`finance-engine`); não escolhe fornecedor nem define ponto de recompra de estoque (`sourcing`); não mexe em campanha (`ad-strategy`/`ad-analysis`/`scale-engine`); não cobre contratação e gestão de time (isso é a skill team-engine) nem canais novos como Amazon e TikTok Shop (skill marketplace-engine) — quando esses assuntos aparecerem aqui, são apontados pra dona certa, não resolvidos.

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output desta skill é interno — relatório, checklist e memos usam esse idioma. Não existe copy consumidor-final aqui.

### Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

- [ ] `workspace/[produto]/manifest.json` existe. Se não existir, ofereça rodar o `setup` inline (rule `emergency-escape-paths.md` ES1) ou prosseguir em modo consulta, sem gravar nada.
- [ ] Nenhum outro arquivo é obrigatório. Esta skill roda com o que houver — quanto mais fases anteriores existirem, mais preciso fica o diagnóstico.

### Contexto a carregar

1. `workspace/profile.md` + `manifest.json` — **stage** e `budget_daily` (ver `member-stage-awareness.md`). O stage decide a profundidade: pra `starter`, a ETAPA 2 é o centro e as ETAPAs 1 e 4 são curtas (a constraint vira uma pergunta, o bloco de ativo vira leitura de direção); pra `validating`/`scaling`, as quatro ETAPAs rodam inteiras.
2. `workspace/[produto]/finance-engine/dados.json` **(se existir)** — `cash.runway_months`, `cash.cash_needed_90d`, `monthly_model.fixed_costs_monthly`. É o retrato de caixa que a ETAPA 1 usa pra avaliar a constraint de caixa. **Ponteiro, não cálculo:** nenhum número de caixa nasce aqui; se o membro quiser o modelo, o caminho é dizer "finanças".
3. `workspace/[produto]/sourcing/dados.json` **(se existir)** — `calendar.reorder_point_days`, `calendar.volume_confirmation_30_60_90`, fornecedor escolhido. É o retrato de estoque da constraint de estoque. **Ponteiro:** decisão de fornecedor e recompra é da `sourcing`.
4. `workspace/[produto]/ad-analysis/dados.json` e `scale-engine/dados.json` **(se existirem)** — spend real e fase de escala, pra dimensionar o risco de plataforma (quanto maior o gasto diário, maior o custo de um dia parado).
5. Rodadas anteriores desta skill em `workspace/[produto]/ops-engine/` — o valor da revisão recorrente é comparar o checklist e os riscos com a rodada anterior.

### Regra de honestidade (não se negocia)

**Status de backup é confirmação do membro, nunca dedução.** A skill não tem como ver se existe Business Manager reserva, se a processadora backup está configurada ou se o registro de marca saiu. Cada item do checklist é perguntado; item sem resposta fica `pending` e entra em `pending_inputs[]`. Marcar "pronto" sem confirmação explícita torna o checklist falso — e um checklist de continuidade falso é pior que nenhum, porque o membro acha que está protegido.

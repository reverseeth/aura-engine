# Ad Strategy · Referência: Criação em PAUSED via Meta Ads MCP e as proteções que funcionam em CBO (ETAPA 6)

> A cascade de MCP (oficial, Pipeboard, manual), por que o kill automatizado por performance não existe em CBO, o daily maximum por ad set e as duas automações obrigatórias, as regras invioláveis da criação (tudo em PAUSED, auditoria antes, receitas, IDs guardados, toda criação no ad-log), a mensagem ao membro e a saída ES6 em caso de falha. Abra na ETAPA 6.

### ETAPA 6 — Criação em PAUSED via Meta Ads MCP

Em vez de só entregar "cole isso no Ads Manager", esta skill **cria** a campanha + os ad sets + os ads em **PAUSED** via MCP, pro membro revisar e ativar com 1 clique. Os gates da ETAPA 1 já passaram antes deste ponto.

**Cascade de MCP** (detecção de prefixo — ver `.claude/lib/mcp-detect/README.md` e regra 10 do CLAUDE.md):

1. **Caminho 1 — MCP oficial da Meta (`mcp__meta__ads_*`):** criar a campanha (objective Sales, **CBO ligado com `daily_budget = test_budget_daily`** da ETAPA 3.1) e **um ad set por conceito** (`adsets_planejados`: audience broad/Advantage+, placements automáticos, **sem budget próprio**, com `daily_maximum` de spending limit, optimization Purchase, attribution 7d/1d) em `status: PAUSED`. O oficial é remoto e lida bem com criação de estrutura por parâmetros. (Status: o connector oficial segue em **open beta desde 2026-04-29**, com rollout gradual e sem GA — contas podem aparecer "disabled" mesmo com setup correto; é exatamente o buraco que o Caminho 2 cobre.)
2. **Caminho 2 — Pipeboard (`mcp__meta-ads__*`):** fallback automático quando o oficial está indisponível/"disabled" no rollout. **O upload do binário dos criativos (.mp4) força Pipeboard ou Playwright** mesmo quando o oficial está conectado (o oficial é remote-hosted e não lê arquivo local) — ver receita `.claude/automations/recipes/upload-creative-to-meta.md`.
3. **Caminho 3 — manual:** se nenhum MCP está conectado, entregar o passo-a-passo exato pra o membro montar no Ads Manager (a estrutura das ETAPAS 3-5, formatada pra colar campo a campo).

#### Proteções — o que É automatizável em CBO (cânone §6)

**Performance Gate Scaling (PGS) não existe nesta estrutura.** Automated Rule com condição de performance (CPA, ROAS, frequency) é **recusada pelo Meta** em campanha que usa CBO — o erro retornado é literalmente *"performance-related conditions are not available for assets that use CBO"*. Não ofereça, não tente criar, não prometa ao membro. O que entra no lugar:

1. **`Ad set spending limit → daily maximum` em cada ad set de teste (o substituto do PGS).** É teto de gasto diário no nível do ad set, não é condição de performance, então funciona em CBO. Valor: o mesmo **~3× target CPA/dia** que é o teto por ad set do cânone §1 — é o que o conceito precisa pra ser lido, e nada além disso precisa ser gasto enquanto ele não provou. Serve pra que "subir batch de madrugada" não vire conta de milhares no dia seguinte, e pra que um ad ruim que o CBO resolveu empurrar não coma o teste inteiro. Depois que o conceito prova tração, afrouxar/remover o teto é decisão do membro na Skill `scale-engine` — dentro do teste, ele fica.
2. **Automação obrigatória A — pico de gasto:** se o spend subir **5× em 24h**, pausar os ads/ad sets que subiram. Protege contra conta comprometida e contra um zero a mais digitado no budget.
3. **Automação obrigatória B — URL errada:** se a URL de destino do ad **≠ o domínio da loja** (`manifest.storefront.page_url`), desligar o ad. Protege contra ad rodando pra página errada, removida ou de terceiro.

> **Kill automatizado por performance NÃO se faz — nem aqui, nem na `ad-analysis`, nem na `scale-engine`.** Duas razões independentes: (a) tecnicamente o Meta não aceita a condição em CBO; (b) mesmo onde aceitasse, a métrica do Ads Manager engana — um ad a 1× ROAS na plataforma pode estar excelente no 1-day click de uma ferramenta de atribuição de terceiro, e desligar por metadado mata winner. **Kill é leitura, não regra:** quem decide é a Skill `ad-analysis`, com as réguas do cânone §3.

As duas automações obrigatórias e o daily maximum são oferecidos junto da estrutura e **nascem DESATIVADOS** (as rules) / são criados junto do ad set (o daily maximum). Gravar em `protections` no dados.json o que foi efetivamente criado. Se nenhum caminho MCP suportar a criação das rules, entregar o passo-a-passo pro membro criar em Ads Manager > Automated Rules e marcar `created: false` — a proteção não é opcional por doutrina, só por limite de ferramenta.

**Regras invioláveis da criação:**
- **Tudo nasce em `status: PAUSED`** (inclusive Automated Rules — nascem desativadas). O membro revisa e ativa. A skill NUNCA ativa nada sozinha.
- A **auditoria de consistência da ETAPA 1** roda ANTES de criar, e todo criativo que sobe já passou pelo Limpador de Metadados (nome `asset-xxxx`).
- Reutilizar as receitas existentes onde aplicável: `upload-creative-to-meta.md` (subir os criativos + criar o creative object) e o setup de MCP em `.claude/automations/setup-mcps.md`.
- Após criar, **guardar os IDs retornados** (campaign_id, **ad_set_ids por conceito**, ad_ids) no JSON e no manifest — a Skill `ad-analysis` lê esses IDs pra puxar insights nos dois níveis (conceito e criativo).
- **Toda criação vira linha no ad-log, na MESMA execução** (cânone `.claude/lib/ad-log/README.md`): campanha, cada ad set, cada ad e cada automação de proteção — **mesmo nascendo em PAUSED/desativada** — são registrados em `workspace/[produto]/ad-log.md`, uma linha por criação no formato do cânone (`| YYYY-MM-DD HH:MM | entidade | criado em PAUSED | skill-ad-strategy | motivo curto |`, entidades `campaign:[nome]` · `adset:[concept_id]` · `ad:[creative_id]` · `automation:[nome]`; se o arquivo não existir, criar com o cabeçalho da tabela; append-only). Mudança executada e não logada é bug de processo — é este log que a `ad-analysis` cruza com a janela de leitura e a `scale-engine` consulta antes de escalar. No Caminho 3 (manual), logar quando o membro confirmar o que criou, com executor `membro`.

**Mensagem ao membro após criar em PAUSED:**
> "Criei a campanha `[nome]` em **PAUSED** na sua conta — budget de **$[test_budget_daily]/dia no nível da campanha** (CBO), dividido entre **[N] ad sets, um por conceito** ([lista dos conceitos]), cada um com 3 criativos broad/Advantage+, otimizando pra Purchase. [Se os destinos por conceito diferem:] Cada conceito aponta pra página do nível de consciência dele — [lista conceito→página]. Esse é o número de conceitos que o seu budget consegue LER: $[budget]/dia ÷ CPA alvo de $[target_cpa] dá [max_assets] criativos com chance justa. Revisa no Ads Manager (audiência, budget, criativos, URLs de destino) e **ativa quando estiver OK**. Não ativei nada por você. [Se as proteções foram criadas:] Deixei também o teto de gasto diário por ad set e as duas regras de proteção (pico de gasto e URL errada) — desativadas, ative junto."

Se a criação via MCP falhar (rate limit, auth), aplicar `.claude/rules/emergency-escape-paths.md` ES6: backoff, depois oferecer **(A)** retomar em 1h, ou **(B)** cair pro Caminho 3 manual com a estrutura formatada.

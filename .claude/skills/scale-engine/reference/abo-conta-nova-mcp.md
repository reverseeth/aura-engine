# Scale Engine · Referência: Promoção pra ABO, conta nova e execução via Meta MCP (ETAPAs 4.4, 4.5 e 4.6)

> A execução da promoção de breakthrough pra ad set próprio em campanha ABO paralela (réguas do cânone §5), o diagnóstico de conta vs produto quando o budget trava a entrega (com o limite ético) e a criação opcional das estruturas em PAUSED via MCP, com as duas únicas automações de proteção. Abra nas ETAPAs 4.4 a 4.6.

### ETAPA 4.4 — Promoção do breakthrough pra ABO (cânone §5)

O cânone §5 aposentou o champions ad set: **cada breakthrough ganha 1 ad set próprio em campanha ABO paralela** — e a EXECUÇÃO dessa promoção vive AQUI (a `ad-analysis` sinaliza que o criativo está pronto; a `content-recycler` planeja a duplicação no Movimento 5 dela; quem cria, ajusta budget e loga é esta skill).

**Gatilho:** breakthrough novo confirmado pela `ad-analysis` (`manifest.breakthroughs[]` / `ad_classification[].class == "breakthrough"`) ainda sem ad set ABO próprio — ou o plano da `content-recycler` (Movimento 5 do `amplification-plan.md`) apontando a duplicação.

**Execução (réguas do cânone §5, sem improviso):**

1. **Campanha ABO paralela:** na primeira promoção, criar a campanha ABO (budget no nível do AD SET, sem CBO); nas promoções seguintes, **reusar a mesma campanha ABO** — não criar uma por breakthrough.
2. **1 ad set próprio por breakthrough** — nunca 2 breakthroughs no mesmo ad set.
3. **Budget inicial do ad set: ~10% do budget diário da campanha principal** (`manifest.budget_daily` / o CBO de teste da `ad-strategy`).
4. **O ad original PERMANECE rodando no CBO.** A promoção duplica, não move — o motivo do cânone: winner novo rouba spend do antigo dentro do CBO, e o ABO garante a continuidade do que já provou escalar.
5. **Depois da promoção, o degrau normal do protocolo (ETAPA 3.5) governa o ad set novo:** 48-72h acima do target antes do primeiro +20%, gate click-based, reset da meia-noite — sem regime especial.
6. **Linha no ad-log NO ATO** (cânone ad-log): `adset:[creative_id]` criado na campanha ABO, com o budget inicial e executor `skill-scale-engine` (ou `membro`, no caminho manual). Promoção executada e não logada é bug de processo.

**Como criar:** via MCP quando disponível (a MESMA cascade da ETAPA 4.6, tudo em `status: PAUSED` — o membro revisa e ativa), senão instrução passo-a-passo ao membro no Ads Manager. Registrar cada promoção em `dados.json.abo_promotions[]` (creative_id, adset_id, budget inicial, data).

### ETAPA 4.5 — Quando o budget trava a entrega → abrir nova conta

Padrão que aparece em todas as escolas: às vezes você sobe o budget e a entrega **não acompanha** — a campanha não gasta o novo budget, ou trava o aprendizado e o CPA dispara. Antes de concluir "atingi meu teto", diagnostique:

1. **É a conta ou o produto?** CPM muito acima do normal pro nicho é sinal de **conta cansada**, não de produto morto. O mesmo criativo pode dar CPM $30 numa conta e $100 noutra (a skill `ad-analysis` mede isso).
2. **Se for a conta** → a jogada legítima é **abrir uma conta de anúncio nova** e rodar o mesmo breakthrough lá. Ter contas de anúncio organizadas (1 por produto, mais contas de reserva pra resiliência) é organização e contingência legítimas — embaralhar 2 produtos numa conta confunde o aprendizado, então separar é boa prática.
3. **Na Escola B**, lembre: se a campanha boa não aguenta mais um ad set sem travar, **abra outra conta/campanha** em vez de arriscar a que está performando.

> **Limite ético (inviolável):** esta skill encode SÓ a mecânica legítima de organização de conta e campanha. **NÃO** ensina nem recomenda comprar BM/contas de terceiros, "farmar" contas, contingenciar perfil-dono-vs-anunciante pra driblar ban, produto réplica ou cloaking. Essas táticas derrubam a conta da marca real e brigam com a tese brand-building do Aura. Abrir uma conta de anúncio nova e legítima dentro do seu próprio Business Manager é resiliência; farmar conta pra driblar política não é — e não tem suporte aqui.

### ETAPA 4.6 — Execução opcional via Meta MCP (criar em PAUSED)

A escala não precisa ser só instrução manual — o membro é não-técnico, e as operações das escolas são numerosas e repetitivas. Se ele topar, criar a estrutura da escola escolhida via a MESMA cascade da Skill `ad-strategy` ETAPA 6 (oficial `mcp__meta__ads_*` → Pipeboard `mcp__meta-ads__*` → manual — detecção por prefixo, ver `.claude/lib/mcp-detect/README.md`):

- **Escola A:** as campanhas 1-1-1 do breakthrough, duplicadas com os caps decrescentes calculados ($50/$45/$40/$35…), todas em `status: PAUSED`. O surf em si continua manual — é monitoramento ativo por definição.
- **Escola B:** a campanha bid cap (bid = CPA máximo, budget 100×) em PAUSED; os ad sets novos de alimentação também nascem PAUSED a cada adição.
- **Escola C:** sem estrutura nova pra criar — só o plano de doubling (mudança de budget é sempre aprovada pelo membro, nunca automática).
- **Automações — só as DUAS de proteção do cânone §6, nunca de performance:** criar **DESATIVADAS**, pro membro revisar e ativar no Ads Manager — **(a)** spend 5× em 24h → pausar; **(b)** URL de destino ≠ domínio da loja → desligar o ad (as mesmas da Skill `ad-strategy` ETAPA 6; se já existem na conta, só conferir o estado). O único limitador aceito além delas é o **`ad set spending limit → daily maximum`** — o substituto do PGS, que o Meta recusa em campanha com CBO (*"performance-related conditions are not available for assets that use CBO"*). **Kill e escala por métrica NUNCA se automatizam — são decisão humana via protocolo (cânone §6):** nenhuma rule de scale-down/scale-up por CPA/ROAS/frequency é oferecida, criada ou prometida.
- **A regra de reset da meia-noite NÃO vira automação.** Ela depende do gasto REAL do dia, que só se conhece no fim do dia — a skill entrega o número calculado e o membro aplica. Nenhuma automated rule pode setar budget nominal sozinha.

**Regras invioláveis (as mesmas da `ad-strategy`):** tudo nasce PAUSED/desativado; o membro revisa e ativa; a skill NUNCA ativa nada sozinha. Gravar os IDs criados em `scale-engine/dados.json.mcp_execution` — e **registrar cada ação executada via MCP no `workspace/[produto]/ad-log.md` na MESMA execução** (cânone ad-log: campanhas/ad sets criados em PAUSED, automated rules criadas desativadas — executor `skill-scale-engine`). Sem MCP conectado → entregar o passo-a-passo manual formatado campo a campo (como sempre). Se a criação falhar (rate limit/auth), aplicar `.claude/rules/emergency-escape-paths.md` ES6.

# Scale Engine · Referência: As 3 escolas de escala (ETAPA 4)

> A correção factual de bidding em escala, os sistemas nomeados que sustentam o ritmo, a mecânica completa das Escolas A (cost-cap duplication + surf), B (bid cap campanha monstro) e C (budget-doubling), a tabela de escolha por stage, a graduação pra Advantage+ Sales e a variante de value optimization. Abra na ETAPA 4.

### ETAPA 4 — As 3 Escolas de Escala (variantes de intensidade dentro do protocolo)

As três escolas abaixo são **variantes de intensidade do Scaling Protocol da ETAPA 3.5**, não caminhos alternativos de mesmo nível: mudam o apetite e a mão de obra, mas nenhuma delas dispensa os gates (48-72h acima do target, gate click-based de duas portas, −20% só após 24-48h persistentes abaixo do breakeven, reset da meia-noite). Não há uma "certa" — há a certa pro **stage** e pro **apetite de risco** do membro. **Apresente as três ao membro** (tabela curta, no report_language), marque a recomendada pro stage dele, e deixe ele escolher.

> **Bidding em escala — correção factual (a "regra de ouro" anterior desta skill estava errada):** escala **não** exige cost cap nem bid cap, e Max Conversion **não** é só pra teste. A campanha principal que escala alto roda **maximize number of conversions (highest volume), bid strategy padrão** — é com esse lance que uma campanha chega a **$40 mil/dia**. O que muda de teste pra escala é o volume de sinal e a régua de decisão, não o tipo de lance.
> - **Highest volume** → default da campanha principal, em teste **e** em escala.
> - **Cost per result goal (cost cap)** → ferramenta da **zombie/graveyard campaign** (extrair ROI de ads reprovados/mortos com teto de custo), não da campanha que escala. Se o membro quiser montar essa camada, rode `zombie graveyard campaign cost per result goal ads reprovados milk the creative`.
> - **Bid cap** → opção com **ressalva declarada: bid caps têm issues.** Só com folga de margem, nunca como default. A Escola B usa bid cap por desenho — apresente-a com essa ressalva na mesa.
>
> As escolas A e B seguem disponíveis porque a mecânica de duplicação e de campanha única alimentada é real e útil. O que sai é a afirmação de que escala **obriga** um teto de lance.

**Sistemas nomeados que sustentam o ritmo das três escolas (rode os relevantes à escola escolhida):**
- **Performance Gate Scaling (PGS) + The Three PGS Principles** (rode `Performance Gate Scaling PGS 3 principles trailing CPA automated rules` e `The three PGS principles never scale past margin trailing multi-day KPI campaign-based`) — nunca escala além da margem, usa trailing multi-day KPI (não 1 dia), decisão por campanha. Opera **dentro** do Scaling Protocol (ETAPA 3.5): onde os dois discordarem de ritmo, o protocolo manda.
- **Three Budget Scaling Methods** (rode `Three budget scaling methods farmer 5% aggressive 50% business-led MRR`) — farmer (+5%/dia, conservador), aggressive (+50%, troca volatilidade por velocidade), business-led (escala atrelada a MRR/cash). Mapeia direto: C≈farmer, A≈aggressive.
- **Scaling Protocol & Decision Tree (fonte primária 2026)** (rode `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo`) — 48-72h acima do target antes de subir, depois escala a cada 24h enquanto segura. Árvore de decisão de quando subir vs segurar vs recuar.
- **Sliding Scale Rules (PGS Advanced)** (rode `sliding scale rules PGS different CPA targets spend levels 60 55 52 50`) — fundamenta os **caps decrescentes da Escola A** ($50/$45/$40/$35): cada nível de spend tem um CPA target diferente.
- **Soft Surfing (PGS Advanced)** (rode `soft surfing additional daily 5% increase CPA far below target accelerate growth`) — versão controlada do "surf de manhã" da Escola A: +5% extra quando o CPA está MUITO abaixo do target. Use isto pra calibrar o surf antes do 10× agressivo.
- **Scale-Down Rules (PGS reverse)** (rode `scale-down rules decrease budget 20% 7-day CPA exceeds target safety net`) — quando o CPA de 7 dias estoura o target, corta budget 20%. É a rede de segurança das três escolas (espelha o "recolhe quando quebra" da Escola A e o "volta pro último nível bom" da Escola C). **Hierarquia:** o gatilho duro do cânone §5 é **abaixo do breakeven por 24-48h persistentes → −20%** (um dia ruim isolado não desce); corte motivado por ROAS que ainda paga o variável passa antes pelo gate de custo fixo (ETAPA 3.5, item 6).
- **Spend Redistribution Framework (Don't Kill the Top Spender)** (rode `spend redistribution framework do not turn off top spender ROAS drops higher budget`) — quando o ROAS cai ao subir budget, NÃO desliga o top spender (matar quebra o aprendizado). Crítico pra Escola B (nunca desativa criativo) e pra surf que quebrou.
- **Levels of Scaling (Zero-to-50K to 100K/day)** (rode `levels of scaling zero to 50k 100k per day one campaign CBO raw content ASC whitelisting segmented`) — estrutura de campanha por nível de spend (one-campaign → CBO → ASC → whitelisting → segmented). Mapeia a `scale_phase` da ETAPA 2 num blueprint de estrutura real.

#### Escola A — Cost-Cap Duplication + Surf de Manhã (mais agressiva, mais upside)

> Variante de **intensidade alta** do protocolo. Usa cost cap fora da zombie campaign: legítimo como mecânica de duplicação com tetos decrescentes, desde que o membro saiba que a campanha principal de maior escala roda **highest volume** (bloco de bidding acima) — o cap aqui é escolha de controle, não requisito de escala. Registre `bidding.cost_cap_scope: "school_a_duplication"` no `dados.json`.

A mecânica:

1. **Isola o breakthrough numa campanha 1-1-1** — 1 campanha, 1 ad set, 1 criativo. Limpo, sem ruído. Se 2 criativos chegaram a breakthrough, uma estrutura 1-1-1 pra cada.
2. **Bidding = Cost Cap** (custo por resultado), setado **~10% abaixo do CPA de breakeven**. Ex: breakeven $55 → cost cap inicial **~$50** (deixa ~9% de margem de contribuição por pedido nesse teto: `margem/pedido = breakeven − cap = $5` ≈ 9% da margem de $55; não é lucro, porque o custo fixo não está descontado). O cost cap é o teto: o Facebook só gasta enquanto consegue resultado abaixo dele. **São os caps decrescentes do passo 3 que vão exigindo mais lucro por pedido** — quanto mais baixo o cap, maior a margem por venda (ex: cap ~$38 ≈ 30% de lucro/pedido).
3. **Duplica o 1-1-1 várias vezes com caps DECRESCENTES** — $50, $45, $40, $35… de $5 em $5. Cada duplicata com o mesmo budget de teste (ex: $160/dia). A lógica: cada cap mais baixo pega a eficiência num ponto diferente do leilão; o Facebook acha gasto onde dá pra entregar dentro daquele teto. Quanto mais baixo o cap, mais difícil gastar, mas mais barato o resultado.
4. **Surf de manhã (a parte agressiva).** Ao acordar, olhe as campanhas. Uma com CPA **muito** abaixo do alvo (ex: 2 vendas, gastou $30, CPA $15 num produto de breakeven $55) está pedindo budget. **Joga o budget 10×** ($160 → $1.600), observa 2-3h.
   - Continua vendendo dentro do alvo → **sobe mais** ($3k, $30k — não gasta tudo, gasta o que conseguir vendendo).
   - Gastou ~$150 a mais SEM venda nova, ou o CPA passou do breakeven → **derruba o budget de volta IMEDIATAMENTE**. Não espera prejuízo grande. Ao baixar, a campanha frequentemente volta a vender no nível anterior.
   - Sem regra fixa de %. Vai pelo que a campanha entrega naquele momento. É monitoramento ativo, não set-and-forget.
   - **À meia-noite, aplique a REGRA DE RESET (ETAPA 3.5): o budget do dia seguinte é ~50% do que a campanha REALMENTE gastou, nunca o nominal que ficou na tela.** Surfou até $30k mas gastou $4k → o dia seguinte começa em ~$2k. Deixar o nominal de pé é o erro que transforma um dia bom numa conta queimada enquanto o membro dorme. Toda instrução de surf desta skill sai com o número do reset junto.

   > Surf é "navegar a onda": quando o leilão tá te dando resultado barato, você empurra o máximo de budget enquanto a onda segura, e recolhe na hora que ela quebra. Exige presença (olhar a cada 2-3h num dia de surf). Por isso é escola de **scaling**, não de starter.

**Quando usar:** stage `scaling`, breakthrough muito estável, membro com tempo pra monitorar de manhã e estômago pra volatilidade. Maior upside, maior atenção — e reset da meia-noite todo santo dia.

#### Escola B — Bid Cap "Campanha Monstro" (mais controlada, mão menos pesada)

> Variante de **intensidade média** do protocolo, construída sobre bid cap — e bid cap carrega a **ressalva declarada do bloco de bidding: bid caps têm issues.** Apresente a escola com essa ressalva explícita: ela troca upside por controle, e o controle vem de um mecanismo de lance reconhecidamente problemático. Se o membro quer só volume estável sem esse risco, a campanha em **highest volume** rodando o protocolo entrega o mesmo crescimento sem o teto de lance.

A mecânica:

1. **1 conta de anúncio = 1 campanha de Bid Cap.** (Roda 1 dia de Max Conversion antes, só pra a conta pegar mini-dados de cliente e ajudar o bid cap a achar gasto.)
2. **Setup:** `bid cap = seu CPA máximo`; `budget = 100× o CPA máximo`. Ex: CPA máximo $30 → bid cap $30, budget diário $3.000. **Não gasta tudo** — o budget alto é só espaço; o bid cap é o teto real de custo por resultado.
3. **Alimenta a MESMA campanha continuamente** com mais ad sets de criativo (≈5 criativos por ad set). A cada 1-2 dias, adiciona um ad set novo com criativos novos. Pode chegar a 20 ad sets / 200 criativos numa única campanha "monstro".
4. **NÃO desativa criativos.** Deixa o Facebook varrer todos atrás de CPA abaixo do bid cap. O algoritmo concentra gasto onde acha resultado e ignora o resto (criativo ruim simplesmente não gasta — você não precisa matar manualmente).

**Risco e safeguard:** adicionar ad set novo numa campanha que está ótima pode **travar a entrega** (resetar o aprendizado). Se a campanha tá voando, **prefira abrir OUTRA conta/campanha** em vez de arriscar mexer na boa. Baixar o bid cap de $2 em $2 pra apertar o CPA é possível, mas arriscado (também pode travar) — faça só com folga. Isso ficou AINDA mais verdadeiro desde abril/2026: edições antes consideradas "seguras" (ajuste pequeno de bid, tweak de criativo) passaram a resetar o learning com mais facilidade — duplicar/abrir conta nova em vez de editar campanha boa é a jogada default da era.

**Quando usar:** stage `validating` ou `scaling` que quer crescimento estável com pouca mão. Menos volatilidade que a Escola A, menos upside explosivo.

#### Escola C — Budget-Doubling a cada 3 Dias (mais simples)

A mecânica:

1. Roda a campanha (highest volume é o default — cost/bid cap só se o membro quiser teto, com as ressalvas do bloco de bidding).
2. **Sobe em degraus enquanto o ROI/CPA segura.** A escola original dobra a cada 3 dias ($100 → $200 → $400 → $800…); dentro da Aura o degrau é o do protocolo (ETAPA 3.5, cânone §5): +20% a cada 24h depois de 48-72h acima do target, o que dá cerca de 1,7× a cada 3 dias. É a mesma escada, na cadência que não reseta o aprendizado.
3. Quando quebra num nível (CPA estoura o target / ROI fica negativo), **volta pro último nível bom** e segura ali. Esse é o seu teto atual ("achei meu teto").
4. Pra subir de novo depois: melhora o que está fora do Ads Manager (criativo novo da `creative-engine`, oferta melhor da `offer-builder`) e tenta dobrar de novo a partir do teto.

> Os 3 dias importam: dão dado suficiente pro Facebook estabilizar antes de cada salto e evitam reagir a um pico de 1 dia. É a versão "sem ficar no teclado" de escala — não exige surf nem gestão de N campanhas.

**Quando usar:** stage `starter` (e `validating` no começo). É a mais fácil de operar, a mais perdoável, e ensina o membro a achar o teto sem queimar conta.

#### Tabela de escolha (apresentar ao membro)

| Escola | Como funciona em 1 frase | Mão de obra | Volatilidade | Default pra stage |
|---|---|---|---|---|
| **C — Budget-doubling 3d** | Dobra a cada 3 dias até quebrar, volta pro último nível bom | Baixíssima | Baixa | **starter** |
| **B — Bid cap monstro** | 1 campanha, budget 100× CPA, bid cap = CPA máx, alimenta com ad sets, nunca desativa | Baixa-média | Média | **validating** que quer controle — com a ressalva "bid caps têm issues" |
| **A — Cost-cap + surf** | Isola o breakthrough num 1-1-1, duplica com caps decrescentes, surfa de manhã e reseta à meia-noite sobre o gasto real | Alta (olhar 2-3×/dia) | Alta | **scaling** |

Recomendação por stage (default, não trava): **starter → C**; **validating → C com passo do protocolo, ou B se quiser controle** (com a ressalva de bid cap); **scaling → A** (mais upside, mais atenção). Em qualquer stage, a campanha principal em **highest volume** rodando o protocolo puro é alternativa legítima — nenhuma escola é obrigatória pra escalar.

Pergunte ao membro qual escola quer rodar. Se ele não tiver opinião, vá com o default do stage e explique por quê. Registre a escola escolhida no `scale-engine/dados.json` (`scaling_school`) — junto com o bidding efetivo em `dados.json.bidding`, porque a escola é a intensidade, o bidding é uma escolha separada.

**Graduação pra ASC — Advantage+ Sales (nível $1K+/dia sustentado):** as três escolas seguem sendo o playbook até aí. Acima disso, o desenho operacional 2026 em ecom é **ASC como campanha principal + a estrutura de teste da Skill `ad-strategy` (1 campanha CBO → N ad sets, 1 por conceito → 3 ads) virando sandbox de teste de criativo** (breakthroughs promovidos pra ASC). Requisitos práticos: volume de conversão alto e 6-10 criativos vivos. Dois detalhes que mudam o setup: (1) configurar o **existing-customer budget cap** (reintroduzido em março/2026) pra manter o ASC prospectando em vez de virar retargeting disfarçado; (2) dentro do ASC não existe bid cap — o controle de custo é o **cost-per-result goal**. Números de lift divulgados (4.5x ROAS etc.) vêm de fontes pró-automação — trate como direcionais, valide com o SEU CPA.

**Variante condicional — value optimization (só se o AOV varia de verdade):** se o spread de AOV entre pedidos passa de ~30% (bundle/subscription/upsell forte pós-07d), otimizar por CPA uniforme sub-otimiza — paga o mesmo por pedido de $40 e de $120. Nesse caso, teste **ROAS goal + value rules** numa campanha DUPLICADA (nunca na campanha de controle), com 14+ dias de teste antes de julgar. Pra produto único de preço estável (a maioria dos membros), ignore esta variante: otimizar por CPA — no lance padrão (highest volume) ou com teto, conforme a escola — segue superior em simplicidade e controle.

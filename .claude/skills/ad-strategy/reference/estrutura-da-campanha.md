# Ad Strategy · Referência: A estrutura da campanha (sub-etapa 3.3)

> A campanha (naming, objetivo Sales, CBO com o `test_budget_daily`, uma conta por produto), os ad sets (naming com `concept_id`, otimização Purchase, sem budget próprio, um conceito por ad set, audiência broad idêntica, placements automáticos, atribuição), os criativos (pack 3-2-2, diversidade genuína, naming, CTA, destino por conceito com fallback, o schema de UTM que é a fonte única do framework), o porquê de N ad sets sob uma campanha, o eixo de página 3:2:2:2 e a nota de overflow. Abra na sub-etapa 3.3.

#### 3.3 — A estrutura

```
1 CAMPANHA (CBO)  →  N AD SETS (1 = 1 conceito, broad/Advantage+)  →  3 CRIATIVOS + 2 PRIMARY TEXTS + 2 HEADLINES cada
```

**Campanha:**
- **Campaign Name**: `[Produto]_[YYYYMMDD]_Test` (ex: `CollagenSerum_20260620_Test`)
- **Objective / Goal**: **Sales** (o objetivo de Max Conversion / otimização por Purchase; em interfaces antigas aparecia como "Conversions")
- **Special Ad Categories**: nenhum (a menos que saúde/finanças/emprego/habitação — aí marcar)
- **Budget**: **CBO no nível da CAMPANHA** (Advantage+ Campaign Budget **LIGADO**), `daily_budget = test_budget_daily` calculado na ETAPA 3.1. É o CBO que redistribui entre os conceitos — e onde ele concentra gasto é o sinal de escala que a Skill `ad-analysis` lê. Nenhum ad set de teste carrega budget próprio.
- **Campanha por produto**: **1 conta de anúncio por produto**. NÃO misturar 2 produtos na mesma conta — embaralha o aprendizado do algoritmo. Exceção: produtos muito similares (ex: variações do mesmo item) podem dividir conta.

**Ad sets (um por conceito — `adsets_planejados` da ETAPA 3.1):**
- **Ad Set Name**: `[Produto]_[concept_id]_[YYYYMMDD]` (ex: `CollagenSerum_RootCauseAngle_20260620`) — o `concept_id` no nome preserva o handoff `creative-engine`→`ad-strategy`→`ad-analysis` no nível do ad set, que é onde a leitura por conceito acontece.
- **Conversion event / Optimization**: **Purchase** (Max Conversion) em todos. Se a conta ainda não tem volume de Purchase pra otimizar, NÃO descer pra ViewContent às cegas — isso traz tráfego que não compra; preferir o warmup da ETAPA 4 pra a conta esquentar antes.
- **Budget**: **nenhum no ad set** — o budget vive na campanha (CBO). O único controle de budget no nível do ad set é o **daily maximum** de proteção da ETAPA 6, que é **teto** (proteção contra queima), nunca piso (daily minimum continua proibido — ETAPA 7).
- **Conteúdo**: exatamente **1 conceito por ad set** = o pack 3-2-2 da Skill `creative-engine` (3 criativos + 2 primary texts + 2 headlines). Não misturar conceitos dentro de um ad set: misturado, o CBO ainda distribui, mas a leitura de qual conceito funcionou morre.
- **Audience** (idêntica em todos os ad sets — a variável do teste é o conceito, não a audiência):
  - **Location**: mercado principal do market research (US/UK/EU/global).
  - **Age**: **18-65+** (broad — deixar o Meta otimizar).
  - **Gender**: **All** (a menos que o produto seja genuinamente gênero-específico com dado claro).
  - **Detailed targeting**: **Advantage+ / broad** (automático). **NÃO** adicionar interests manuais — o criativo é o targeting. Advantage+ vem batendo manual targeting na grande maioria dos casos. (Pra entender o trade-off Advantage+ broad vs true broad sem training wheels, puxe **True Broad vs Advantage+ Broad** — rode `True Broad vs Advantage Plus broad targeting training wheels`.)
  - **Languages**: idioma do mercado.
  - **Excluded**: nenhum (a menos que retargeting de aquisição precise excluir clientes existentes).
- **Placements**: **Advantage+ Placements** (automático) — Meta distribui entre Feed/Stories/Reels/etc. Não usar manual placements.
- **Schedule**: "Run continuously starting today".
- **Attribution**: 7-day click, 1-day view (padrão 2026). Em EU, restrições de consent podem limitar o view-through — se necessário, ficar só com 7d-click (confirmar com o membro). Não existe janela de 28 dias no Meta desde 2021 — não procure. E **não ligar o setting de Incremental Attribution na campanha de teste**: a régua de kill da Skill `ad-analysis` foi calibrada no baseline 7d-click/1d-view (ver nota na `ad-analysis`).

**Criativos (3 por ad set — o pack 3-2-2 do conceito):**
- Carregar os **3 criativos do conceito como 3 ads dentro do ad set daquele conceito**, com os 2 primary texts e as 2 headlines do pack. Nunca subir criativo de um conceito no ad set de outro.
- **Diversidade GENUÍNA entre os conceitos (ou seja, entre os ad sets):** no sistema de entrega pós-Andromeda/GEM, criativos muito similares são tratados como praticamente a mesma entidade — 3 ad sets com variações do mesmo visual contam como ~1 conceito pro algoritmo (e pro teste). Diversidade genuína = os conceitos diferem nas **variáveis GRANDES do ad** (persona, conceito/big idea, formato, ângulo — o mapa "As Variáveis de um Ad" da Skill `creative-engine`), não em detalhes de execução como cor de fundo ou ordem de cena. Dentro de um ad set é o contrário: os 3 criativos são 3 EXECUÇÕES do mesmo conceito, variando só a abertura. O gate de diversidade da Skill `creative-engine` já força isso — não dilua na hora de subir.
- O CBO distribui o budget entre os ad sets, e o Meta distribui entre os criativos de cada um. **Onde o gasto se concentra é onde tem escala** — esse é o sinal que a Skill `ad-analysis` vai ler, agora legível em dois níveis (conceito e criativo).
- **Ad Name** (cada um): `[concept_id]_[creative-n]_[YYYYMMDD]` (ex: `RootCauseAngle_2_20260620`) — o `concept_id` preserva o handoff `creative-engine`→`ad-strategy`→`ad-analysis` e o índice da execução (1..3, na mesma ordem do pack) mantém os 3 ads do conceito distinguíveis no relatório, em paridade com o `utm_content`.
- **CTA Button**: "Shop Now" (PDP direta) ou "Learn More" (advertorial/landing).
- **URL**: o **destino do CONCEITO** — `ad_sets[].landing_url`, lido do mapeamento de congruência da **ETAPA 6 da `creative-engine`** (a tabela conceito→LP do relatório da `creative-engine` + a linha "Destino" de cada briefing: advertorial pra conceito TOF/problem-aware, landing dedicada pra solution-aware, PDP pra product-aware). **Fallback = `manifest.storefront.page_url`** (a página publicada pela `page-build` — a URL canônica): vale quando a `creative-engine` não mapeou destino, quando o batch é legado, ou quando a página do tipo mapeado ainda não existe publicada — nesse último caso registrar o gap de congruência no relatório (a página recomendada se constrói na cadeia `page-design`/`page-build`), nunca inventar URL. Todo `landing_url` precisa ser página PUBLICADA; os 3 ads de um ad set apontam pro mesmo destino (exceção: eixo de página abaixo).
- **UTM (schema obrigatório — este bloco é a FONTE ÚNICA do framework; a Skill `creative-engine` aponta pra cá):**
  ```
  utm_source=facebook
  utm_medium=paid_social
  utm_campaign=[product-slug]_[YYYYMMDD]_test
  utm_content=[concept-id]-[creative-n]   (por CRIATIVO, não por conceito)
  utm_term={{adset.id}}   (dinâmico via macro do Meta — nunca placeholder estático; com 1 ad set por conceito, ele passa a identificar o CONCEITO)
  utm_id={{ad.id}}        (dinâmico via macro do Meta)
  ```
  **Por que `utm_content` é por criativo:** um conceito tem até 3 execuções (pack 3-2-2 da `creative-engine`) — `utm_content` só por `[concept-id]` fundiria as 3 no analytics e mataria a leitura por criativo em qualquer ferramenta que não expõe o `{{ad.id}}` (GA4, dashboard do ESP, relatório da loja). O sufixo `-[creative-n]` (ex: `rootcause-2`) dá granularidade por criativo legível por humano; o `{{ad.id}}` do `utm_id` segue como identificador único de máquina (é ele que a `ad-analysis` usa pra casar com o Ads Manager). **Normalização no upload:** se o link veio da `creative-engine` só com `[concept-id]` no `utm_content`, acrescentar o sufixo `-[creative-n]` (1..3, na ordem das execuções do pack) ao subir cada ad — nunca subir 2+ criativos com o mesmo `utm_content`.

> **Por que N ad sets sob UMA campanha com CBO — e não N campanhas, nem tudo num ad set só?** Campanhas separadas competem pelo aprendizado e fragmentam o sinal: uma campanha só, broad, fecha o learning phase mais rápido. Já jogar todos os conceitos dentro de um único ad set faz o oposto do que parece: o Meta ainda distribui, mas a leitura por conceito desaparece e cada criativo recebe uma fração de CPA longe do 1× que o cânone exige. Um ad set por conceito com o budget no CBO resolve os dois lados — a campanha aprende junta, e o gasto que cada conceito puxa é a medida de qual conceito tem escala. A diversificação em campanhas ABO separadas é assunto de **escala** (Skill `scale-engine`, cânone §5), não de teste.

**Eixo de página (3:2:2:2 — opção condicionada por budget):** existe um quarto eixo de teste além do criativo — a página de destino. O **3-2-2-2 Method** (rode `3-2-2-2 landing page testing link clicks vs landing page views clickbait`) adiciona 2 landing pages ao pack (3 criativos × 2 primary texts × 2 headlines × 2 páginas = 24 combinações) e deixa o Meta achar a melhor congruência ad↔página. **Gate do próprio material: budget ≥ US$ 2k/dia.** Abaixo disso a variável extra dilui a leitura de criativo que o teste existe pra comprar — cada ad set roda com **UMA URL só** (a do conceito, acima). Com o gate batido E 2 páginas de fato publicadas pro mesmo conceito:
- o ad set pode carregar as 2 LPs (`ad_sets[].landing_url` + `ad_sets[].landing_url_b`), mantendo o mesmo pack 3-2-2 — a página é a ÚNICA variável extra;
- a leitura da página é **por KPI, nunca por spend** (CPA/conversão por destino) — o mesmo princípio do **Page # Test** (rode `ad set Page # winners duplicados nova landing page julgar por KPI não por spend`), que é a rota certa pra testar LP nova DEPOIS do teste, com winners provados; e o ratio Link Clicks → Landing Page Views segue como detector de clickbait (LP views ≥ ~70% dos link clicks);
- a dupla de páginas sai do mapeamento da `creative-engine` ETAPA 6 + do que existe publicado — nunca duplicar a mesma página com URL diferente só pra "ligar o eixo".

**Nota de overflow (batch maior que a capacidade):** se o batch da `creative-engine` vier com mais conceitos do que `adsets_planejados` (ETAPA 3.1), NÃO suba tudo — o CBO espalha fino, nenhum conceito recebe ~3× target CPA/dia e o teste não fecha leitura. **Priorize os conceitos com ângulos genuinamente distintos** (ETAPA 3.2) e guarde o resto pro batch seguinte, que entra na fila. Nunca comprima 2 conceitos num ad set pra "caber mais": isso devolve exatamente a estrutura ilegível que a régua de capacidade existe pra evitar. Se o membro quiser mesmo testar tudo, o caminho honesto é budget maior (o que muda a capacidade), não mais ad sets no mesmo budget.

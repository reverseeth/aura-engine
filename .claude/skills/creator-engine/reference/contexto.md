# Creator Engine · Referência: Índice e cânones, quando usar (as duas fases e a divisão de donos), idioma, pré-flight e contexto a carregar

> O texto integral das notas de índice e cânones, das duas fases com a tabela de donos por artefato, da regra de idioma, do pré-flight (detecção de fase pelos dados, market-research, offer-builder, loja no ar, Fase B, rodadas anteriores) e do contexto a carregar. Abra antes da ETAPA 1.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (mapa skill→domínio no README) — domínios `affiliate-creator-channels` (esta skill é dona das entradas de pessoa: Creator Farming, Whitelist Ads e o recorte creator/afiliado; as entradas de canal são da `marketplace-engine`), `creatives-hooks-formats` (as entradas de creator/seeding/brief), `meta-ads-strategy` (partnership ads + feedback loop), `scaling` (raw content, níveis de escala, time criativo), `team-hiring-ops` (creator pipeline) e `competitor-positioning` (descoberta de whitelisting de concorrente). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica.
>
> **Cânones que governam esta skill:** `.claude/lib/ad-taxonomy/README.md` — as 4 classes de resultado (§2: só `breakthrough` libera a Fase B), o escopo estreito do Shotgun (§7: volume sem estratégia individual é legítimo SÓ no pipeline de conteúdo de creators) e a estrutura de campanha. Esta skill **não cria campanha nem mexe em budget** — quem roda o que ela produz são as skills `ad-strategy` e `scale-engine`, dentro do cânone.

## Quando Usar — DUAS fases

O motor de creators resolve o problema que trava a maioria das marcas: conteúdo. Content é o arquivo bruto (a foto ou o vídeo cru); creative é o content editado com headline, logo e copy. Cada peça de content rende um número finito de criativos antes de esgotar — e os maiores anunciantes testam cerca de **11x mais criativos** que o resto (dado citado por Hormozi em $100M Leads, a partir de dados do próprio Facebook). Sem abundância de conteúdo, não há volume de teste; sem volume de teste, não há winning ad. **"Você está literalmente vendendo conteúdo"** — ninguém toca o produto online.

**Fase A — Content Engine (paralela à `creative-engine`, pode começar antes do launch):** montar o funil que gera conteúdo humano em escala a custo perto de zero — product seeding, casting, framework de brief, coleta — e que existe pra encontrar **um brand ambassador** (embaixador da marca: o creator contratado recorrente), não pra achar um winning ad de primeira (isso é bônus). Começar cedo importa: do momento de contratar um creator externo até o conteúdo virar ad no ar passam **~26 dias** na média da fonte (com creator da casa, ~4 dias). Quem só começa a semear quando precisa de criativo já está um mês atrasado.

**Fase B — Performance Program (SÓ depois de breakthrough confirmado pela `ad-analysis`):** o creator cujo ad virou breakthrough sobe de degrau — contrato recorrente, escada de comissão, whitelisting, partnership ads, raw content campaign, e o recrutamento contínuo (creator farming e ads de recrutamento). Antes de um breakthrough existir, nada disso tem base: whitelisting amplifica o que já venceu, nunca procura vencedor.

**O que esta skill responde e nenhuma outra respondia:** de onde vem o conteúdo humano em volume, quem grava, quanto se paga em cada degrau, como o creator vencedor vira ativo recorrente da marca, e como o canal TikTok Shop vira fábrica de conteúdo.

**O que ela NÃO faz:** não decide o que o ad diz nem produz criativo por IA (`creative-engine`); não monta campanha nem mexe em budget (`ad-strategy`/`scale-engine`); não classifica criativo (`ad-analysis`); não recicla breakthrough (`content-recycler` — inclusive o `creator-report.md` do Movimento 6 continua sendo da `content-recycler`). Divisão explícita:

| Artefato / decisão | Dono | Papel desta skill (`creator-engine`) |
|---|---|---|
| Conceitos, roteiros, prompts de IA, EDLs | **08** | Fornece o conteúdo bruto licenciado e recebe os conceitos como semente de hooks dos briefs |
| Estrutura de campanha, ad sets, budget (inclui raw content campaign e campanha de whitelisting) | **`ad-strategy`/`scale-engine`** | Entrega identidades (páginas de creator com acesso), conteúdo cru e a convenção de nome com o creator |
| Classificação (loser / kpi_winner / spend_winner / breakthrough) | **11** | Lê a classificação pra saber QUAL creator venceu |
| Reciclagem de breakthrough + creator report do Movimento 6 | **14** | Fornece o roster e a regra de visibilidade de números por creator |
| Roster de creators, seeding, briefs, contratos, escada de embaixador, whitelisting/partnership como RELAÇÃO | **16 (esta)** | Dona |

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). Todo output interno (`creator-engine.md`/`.html`, conversa com o membro) usa esse idioma. **Todo material que vai pro creator fica SEMPRE em inglês US** — framework/brief, mensagens de outreach, contrato, report de feedback. Creator é público dos EUA: vale a mesma regra da copy consumidor-final.

### Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] **Detecção de fase** (primeiro passo, decidida pelos dados — não perguntada):
  - **Fase A** se `manifest.creator.phase_a_done != true`. Roda em paralelo com a `creative-engine`, a partir do momento em que existe produto com preço definido. Não exige campanha no ar. Com `phase_a_done: true` e ainda sem breakthrough, "creators" continua sendo Fase A — o ciclo de seeding, follow-up e coleta é contínuo (creator farming, ETAPA 14), não um evento único.
  - **Fase B** se existe ao menos um criativo `class: "breakthrough"` em `manifest.ad_classification[]` (ou `manifest.breakthroughs[]` não-vazio) — gravado pela `ad-analysis`. **Sem breakthrough, a Fase B não roda**: se o membro pedir "whitelisting" ou "ambassador" antes disso, explique que o programa de performance amplifica vencedor confirmado, e ofereça rodar/continuar a Fase A (que é o que produz os candidatos).
  - Membro pediu um pedaço específico (ex: "só o brief") → respeitar, avisando em uma linha se está fora da fase.
- [ ] `workspace/[produto]/market-research/dados.json` — fonte de `core_avatar` + `sub_avatars[]` (a variável de diversidade do casting). Se faltar, não aborte seco (rule `emergency-escape-paths.md` ES1): ofereça **(A)** rodar a `market-research` agora, OU **(B)** prosseguir pedindo ao membro uma descrição direta do avatar, marcando `manifest.skipped_preflight += ["market-research/dados.json"]`.
- [ ] `workspace/[produto]/offer-builder/dados.json` — preço/AOV do produto (`pricing.aov_expected`): o seeding depende do valor de varejo (regra do ≥ ~US$ 30, ETAPA 2) e a margem limita o que dá pra pagar por vídeo. Ausente → pedir preço e custo direto ao membro (mesmo escape ES1).
- [ ] **Fase A:** `page-build` em `skills_completed` é o ideal (a plataforma de seeding pede o link do site — a página "vende" a marca pro creator). Sem loja no ar, a rota de outreach manual anda mesmo assim com fotos + preço; a campanha na plataforma espera o site.
- [ ] **Fase B adicionalmente:** `workspace/[produto]/ad-analysis/dados.json` + `manifest.ad_classification[]` carregados, e os ads de creator identificáveis (convenção de nome com o creator, ou o membro aponta qual ad é de qual creator).
- [ ] Rodadas anteriores desta skill em `workspace/[produto]/creator-engine/` (roster existente continua de onde parou — nunca recomeça do zero).

### Contexto a carregar

1. `workspace/profile.md` — stage e budget (`member-stage-awareness.md`). O stage muda a rota, não a regra: **starter/validating** = seeding grátis + filmar você mesmo/família (nunca recomendar creator pago pra starter — anti-pattern explícito da rule); **scaling** = campanhas pagas por vídeo, retainers, e a Fase B inteira quando o gate abrir.
2. `workspace/[produto]/market-research/dados.json` — `sub_avatars[]` com `angle` (cada sub-avatar pede um tipo de creator diferente — é a entrada da Creator Diversity na ETAPA 3) e `market_vocabulary`.
3. `workspace/[produto]/creative-engine/dados.json` **(se existir)** — os conceitos do batch atual viram a semente do bloco de hooks do framework (ETAPA 5). Sem a `creative-engine` rodada, os `angles` dos sub-avatares da `market-research` cumprem o papel.
4. `workspace/[produto]/ad-analysis/dados.json` + `NEXT_BATCH_IDEAS.md` **(Fase B)** — quem venceu, com que ângulo, e o que a análise pede pro próximo batch (vira ideia enviada ao creator).
5. `workspace/[produto]/scale-engine/dados.json` **(se existir)** — a sub-fase de escala calibra quantos creators em retainer o negócio comporta (tabela da ETAPA 8 da `scale-engine`: de 0 no teste a 4+ na otimização) e quando raw content campaign e whitelisting entram (níveis de escala, ETAPA 14 desta skill).
6. `workspace/[produto]/content-recycler/` **(se existir)** — o `creator-report.md` de um breakthrough reciclado é material de kickoff pra novos ambassadors.

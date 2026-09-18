# Creator Engine · Referência: Gate da Fase B, winning creators e o contrato recorrente com a escada de embaixador (ETAPAs 8 e 9)

> O gate de breakthrough, a definição de winning creator, a convenção de nome e o cruzamento com a classificação, os dois modelos de contrato (retainer simples e ambassador com performance), a tabela de degraus, o teto, a base de cálculo, a alternativa por cupom e os pagamentos. Abra na ETAPA 8.

## FASE B — Performance Program

**Gate:** ≥ 1 `breakthrough` em `manifest.ad_classification[]` (cânone §2 — KPI do ad melhor que o da campanha E puxando spend). `kpi_winner` não abre o gate; `spend_winner` também não (vira candidato a observação, não a contrato).

### ETAPA 8 — [Fase B] Identificar os winning creators

**Definição da fonte: winning creator = creator cujo ad ganhou spend e escalou.** "Good is something that gets spend." O contraste que calibra: creator A → ad com US$ 60k de spend a 2x ROAS (contrata); creator B, de conteúdo "mais bonito" → US$ 66 de spend (não contrata). Zero sentimentalismo estético.

Operacional:

1. **Convenção de nome:** todo ad montado com conteúdo de creator carrega o nome do creator no nome do ad. É o que permite filtrar por creator no Ads Manager e nas ferramentas de report (custom report com "ad name contains {creator}"). Sem isso, não existe atribuição por creator — defina a convenção AGORA e registre em `handoff.for_skill_10`.
2. Cruze `manifest.ad_classification[]` com o mapa creator→ads do roster: creator com breakthrough → candidato a contrato (ETAPA 9); creator com `spend_winner` → observação (o ad entra em iteração pela `content-recycler`/`creative-engine`; o creator fica na fila); resto → continua no ciclo de seeding.
3. Meça por janelas de 90 dias por creator (ex. da fonte: US$ 26k de spend → ~US$ 93-100k gerados pelo conteúdo de uma creator de US$ 500/mês).

### ETAPA 9 — [Fase B] Contrato recorrente: retainer e a escada de embaixador

Dois modelos, por e-mail/mensagem (inglês; templates em `outreach/messages.md`):

**Modelo 1 — Retainer simples:** 1 vídeo/semana com os produtos + produtos de graça + **US$ 500/mês** (o número "simples que todo mundo aceita"; alternativa: pergunte o rate do creator primeiro — às vezes pedem menos) + convite pro canal de comunicação (Discord/Slack). Negociação é esperada (US$ 500 → US$ 750): encontre o meio-termo.

**Modelo 2 — Brand Ambassador + Performance Program:** produto grátis + base US$ 500/mês (1 vídeo/semana) + **SE o creator topar 2-3 vídeos/semana**, entra no programa de performance (a **regra do 2-3**: o programa existe pra DOBRAR/TRIPLICAR o output; quem faz 1/semana fica no retainer simples):

| Degrau | Comissão | Acumulado no exemplo |
|---|---|---|
| Primeiros US$ 10.000 | **10%** | US$ 1.000 |
| Próximos US$ 20.000 | **5%** | US$ 2.000 |
| Próximos US$ 40.000 | **2,5%** | US$ 3.000 |
| Acima de US$ 70.000 | **1%** | — |

- **Teto de payout: US$ 10.000/mês.** Apuração por mês-calendário, somando todos os vídeos do creator, com reset todo mês. Nunca comissão flat pra sempre — o degrau decrescente alinha incentivo sem corroer margem na escala (variante da fonte pra teto menor: 10% só dos primeiros US$ 5k, se o máximo desejado é US$ 500).
- **Base de cálculo: % de REVENUE ou % de AD SPEND** — troque a palavra no e-mail; a fonte split-testa os dois. Exemplos prontos no pitch fazem a conta pelo creator (vídeo gera US$ 70k → US$ 3.500 no total com a base; US$ 100k → US$ 3.800).
- **Alternativa por cupom:** código próprio do creator no ad (ex.: 20% total = 10% de desconto pro cliente + 10% pro creator), com pagamento automático via app de afiliados no Shopify — a fonte split-testa contra o modelo de %.
- **Fricção zero no pitch:** o creator NÃO precisa postar no próprio perfil — só filmar e subir no Drive (remove a maior objeção); e recebe os breakdowns dos winning ads da marca ("so you know the perfect formula").
- Pagamentos nos dias **1 e 15**; planilha de retainer (creator, nº do payout, mês, datas, valor, status) — a skill gera `roster.csv` com essas colunas.

**Incentivo alinhado é o motor:** o creator ganha quando o ad DELE escala — a qualidade sobe sem gestão.

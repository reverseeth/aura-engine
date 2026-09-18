# Retention Engine · Referência: Mapa flow e fase, frameworks de governança e seed de subject lines (ETAPA 2)

> A tabela de qual flow roda em qual fase, os quatro frameworks de governança que valem pra todos os flows (queries exatas) e o seed de subject lines vindo dos `email_hooks[]` da copy-engine. Abra na ETAPA 2.

## Fluxos base (templates — adaptam ao produto)

**Mapa fluxo → fase:**

| Fluxo | Fase | Por quê |
|---|---|---|
| 2. Abandoned Cart | **A (pré-launch)** | Recupera dinheiro do primeiro dia de tráfego — a razão de existir da Fase A |
| 3. Post-Purchase Welcome | **A (pré-launch)** | Comprador do dia 1 recebe reassurance + entrega de bônus + review request |
| 1. Welcome Series | **A só o Email 1, SE há welcome offer/bonus `on_signup`** (promessa da página existe no dia 1); série completa (emails 2-4) = **B** | Sem oferta prometida no opt-in, nurturing é assunto pós-launch |
| 4. Win-Back | **B (≥ 50 compras)** | Precisa de base com inativos — não existe pré-launch |
| 5. Replenishment | **B (≥ 50 compras)** | Precisa da janela de consumo real validada |

**Frameworks de governança que valem pra TODOS os fluxos** (puxe uma vez, aplique em todos):
- **The Rule of 1** — cada email tem UM objetivo, UM job por elemento, UM leitor; escrever o CTA primeiro (rode `Rule of 1 email one goal one job per element one reader write CTA first`)
- **3-to-1 Value-to-Sales Rule** — equilíbrio de cadência entre emails de valor e de venda, pra não queimar a lista (rode `3 to 1 rule value emails sales email balance newsletter cadence`)
- **Email/SMS Coordination Rule (echo, don't collide)** — se o membro também roda SMS, escalonar (email primeiro, SMS follow-up pra não-openers), nunca colidir (rode `email SMS coordination echo not collide send email first SMS follow up non-openers staggered cadence`)
- **Drayton Bird's Email = Direct Mail Principle** — tratar cada email como carta de uma pessoa real, subject = headline, copy longa quando o argumento exige (rode `Drayton Bird email direct mail principle long copy real person subject line headline`)

**Seed de subject lines — `copy-engine/dados.json.email_hooks[]`:** os 3-5 hooks que a `copy-engine` gerou são o ponto de partida dos subject lines e das primeiras linhas dos flows de maior volume (welcome, abandoned cart, post-purchase) — eles já carregam a Big Idea, o mecanismo nomeado e as objeções reais do mercado, então usar eles garante message match entre o que o subscriber viu no ad/página e o que chega no inbox. Adapte cada hook ao contexto do flow (o mesmo hook vira curiosity no welcome e urgency no abandoned cart), não copie 1:1 nos 5 flows. Hooks são consumidor-final: **sempre inglês US**, diretos e sem aviso (rule 8b).

# Bonus Delivery · Referência: O que a skill faz e não faz, as duas fases, índice e pré-flight

> O texto integral da divisão de papéis com a offer-builder, dos quatro trabalhos operacionais, das duas fases que resolvem o paradoxo de launch, das notas de índice e do pré-flight (idioma, stage, detecção da fase pela dupla condição, `bonuses[]` com a inferência de `condition`, escape ES1). Abra antes da ETAPA 1.

## O que esta skill faz (e o que NÃO faz)

A **definição** do bônus (qual bônus, valor ancorado, por que entra no stack) acontece na **Skill `offer-builder`** — ela tem o contexto de avatar, margem e AOV. Esta skill **não inventa bônus**: ela lê o que a `offer-builder` definiu e **executa**.

O que justifica a `bonus-delivery` como skill standalone é o trabalho operacional que a `offer-builder` não faz:

1. **Gerar o ASSET entregável** quando o bônus é digital (PDF do e-book/guide/checklist, com design da marca do membro).
2. **Configurar o GWP na loja** (gift-with-purchase via app ou Shopify Function) — coordenado com a **checkout-aov**.
3. **Disparar o email de entrega** quando o bônus é digital ou condicional — coordenado com a **Skill `retention-engine`**, que é o executor de email.
4. **Rastrear access rate / take-rate** — o KPI que diz se o bônus está agregando valor percebido ou só inflando o stack.

**Posicionamento na ordem — DUAS fases (isso resolve o paradoxo de launch):** o offer_stack da `offer-builder` promete os bônus na PDP desde o dia 1 (a `copy-engine` imprime literal, a `page-build` deploya). Um comprador do dia 1 NÃO pode receber promessa de e-book que ainda não foi gerado, nem de brinde que a loja não sabe adicionar ao carrinho. Por isso:

- **Fase A — Launch-readiness (ANTES do go-live de ads, logo depois da `checkout-aov`):** gerar o asset digital (PDF do e-book/guide), configurar GWP/complementary/gift-wrap na loja (coordenado com a `checkout-aov`), hospedar o arquivo, garantir o acesso do comprador do dia 1 (link do asset na thank-you page / order status — funciona mesmo antes do flow de email existir) e produzir o payload de email pra Skill `retention-engine`. **Todo bônus visível na PDP precisa sair da Fase A antes do primeiro ad** — a Skill `consistency-audit` verifica isso no H5.
- **Fase B — Tracking e iteração (PÓS-launch, junto da Fase B da `retention-engine`):** com a campanha ATIVA e pedidos acontecendo (dupla condição do pré-flight), a `bonus-delivery` volta em D+30 pra puxar take-rate/access rate agregados (ETAPA 4) e alimentar a iteração da oferta na `offer-builder`. (O flow de email de entrega em si já nasce na Fase A da `retention-engine`, que roda pré-launch — o que é pós-launch aqui é o TRACKING.)

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (mapa skill→domínio no `README.md`). O domínio desta skill é **brand-building-bonus-aov**. Sempre que uma ETAPA mandar "puxar da base", rode `search_knowledge` com a `best_query` NOMEADA do framework relevante daquela fase — **nunca query genérica**.
>
> **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill bonus-delivery --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 6 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão.

## Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

1. Ler `workspace/profile.md` → `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). Toda doc interna desta skill (.md/.html/.json descritivo) E toda conversa com o membro usam esse idioma. O asset entregável ao consumidor (PDF do e-book, email) é **sempre em inglês** (mercado US), independente do `report_language` — rule 0 do CLAUDE.md.
2. Ler `workspace/[produto]/manifest.json` → detectar `stage` (member-stage-awareness). Influencia recomendação de tipo: **starter** → priorizar e-book/guide (custo zero de produzir) e GWP de baixo COGS; **scaling** → pode sustentar complementary SKU físico e GWP mais robusto.
3. Detectar a FASE — a **Fase B exige DUPLA condição** (skill completa ≠ ads no ar: a `ad-strategy` cria a campanha em PAUSED):
   - **(1)** `manifest.skills_completed` contém `"ad-strategy"`, **E**
   - **(2)** a campanha está de fato ATIVA / há pedidos no período — evidência: o membro confirma que ativou, `ad-analysis/dados.json` existe com spend registrado, ou há pedidos no Shopify desde o launch.

   As duas valem E os assets/config de todos os `bonuses[]` existem → **Fase B** (ETAPA 4, tracking). Qualquer outra combinação (`ad-strategy` ausente, campanha ainda em PAUSED, ou bônus sem asset/config) → **Fase A** (ETAPAs 1-3 + config).
4. `offer-builder/dados.json` existe com `bonuses[]` preenchido. Pra cada bonus, `type` E `condition` claros (não default "pdf"). Se `condition` estiver ausente (oferta gerada antes do campo existir), inferir: bônus presente no offer_stack da PDP = `unconditional`; GWP com threshold definido = `cart_threshold` — e gravar a inferência de volta no `dados.json` da `offer-builder`.
5. **Escape path (ES1):** se `offer-builder/dados.json` está ausente/corrompido, oferecer (A) re-rodar Skill `offer-builder` ou (B) proceder com bônus genérico marcando `manifest.skipped_preflight`. Não abortar seco.

Se `bonuses[]` está vazio mas o membro quer um bônus, **voltar pra `offer-builder`** — é lá que se decide. A `bonus-delivery` não cria oferta.

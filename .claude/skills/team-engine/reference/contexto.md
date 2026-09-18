# Team Engine · Referência: Índice, réguas compartilhadas, quando usar, idioma, pré-flight e contexto a carregar

> O texto integral do índice de frameworks e das entradas vizinhas, das réguas que a skill respeita, de quando usar com os três momentos naturais e a fronteira com as vizinhas, da regra de idioma com a exceção do material que o candidato lê, do pré-flight e do contexto a carregar. Abra antes da ETAPA 1.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (domínio `team-hiring-ops`, mapa skill→domínio no README). Esta skill é a **consumidora que faltava** do maior bloco órfão da base: até ela existir, a maior parte dos sistemas estava marcada como dormant (`use_in_skill: "—"`) e só 8 tinham leitor (`creative-engine`/`consistency-audit`/`ad-analysis`/`scale-engine`). A partir dela, o domínio inteiro é puxável. Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica.
>
> Além do domínio próprio, esta skill consome **6 entradas vizinhas** — 4 do domínio `ops-scale-risk` (a decisão por gargalo e o papel do fundador) e 2 do domínio `scaling` (o foco e o tamanho de time por faixa de faturamento, já lidas pela `creative-engine`/`scale-engine` — conteúdo compartilhado, reuse o resultado se já foi puxado na sessão).
>
> **Réguas compartilhadas que esta skill respeita:** `member-stage-awareness.md` (o stage do manifest decide a apresentação) e o cânone `.claude/lib/unit-economics/README.md` §1 via skill `finance-engine` — folha de pagamento é **custo fixo**, e custo fixo nunca se estima: quando a pergunta for "cabe no caixa?", o número vem da `finance-engine` ou do membro, nunca de chute desta skill.

## Quando Usar

Quando a pergunta é sobre **gente**: contratar, delegar, montar estrutura, medir, pagar, promover ou desligar. Gatilhos: "contratar", "time", "equipe", "editor", "hiring", "org", "quem contratar", "delegar", "preciso de um editor", "quero sair do operacional", "meu time não entrega", "quanto pagar", "como demitir".

**Não é fase do pipeline — é skill de consulta lateral, como a `finance-engine`.** Três momentos naturais:

- **Quando o membro vira o gargalo:** faturamento subiu, o dia acabou e ele ainda edita vídeo, sobe ad e responde cliente. A pergunta real é "o que sai da minha mão primeiro?".
- **Quando existe vaga pra abrir:** "preciso de um editor / media buyer / strategist" — a skill monta o gabarito da vaga, o anúncio e o funil inteiro.
- **Quando o time já existe e não performa:** expectativa mal definida, KPI que ninguém acompanha, promoção e demissão no feeling. A skill instala o ciclo de gestão.

**Pra quem esta skill foi desenhada:** o membro em **`scaling`** — é nesse estágio que contratar resolve gargalo de verdade. Pra membro em `starter` ou `validating`, a resposta mais valiosa que esta skill entrega costuma ser **"ainda não"** com o motivo (ETAPA 1) — o material de referência é explícito: marca de ecommerce enxuta escala a US$ 1M+/mês com time mínimo, e a resposta raramente é "mais gente"; é "gente melhor" (muitas vezes: você, melhor).

**O que ela NÃO faz:** não recruta creator de conteúdo nem monta programa de afiliado — **creator não é funcionário**; contratação de creators, seeding, bounty com gente de fora da empresa e programa de embaixador são território da **skill `creator-engine`**. Também não calcula o modelo financeiro — quando a conversa vira "quanto de folha o negócio aguenta", esta skill lê o que a `finance-engine` publicou e aponta pra ela, sem refazer a conta.

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Exceção deliberada:** artefatos que o CANDIDATO vai ler (anúncio de vaga, mensagem de abordagem, roteiro do teste prático) saem no idioma do mercado onde o membro contrata — pra contratação remota global/EUA o padrão é inglês; se o membro contrata no Brasil, português. Pergunte uma vez e grave em `dados.json.hiring_language`.

### Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

- [ ] `workspace/[produto]/manifest.json` existe — fonte do `stage`, `budget_daily` e `fixed_costs_monthly`
- [ ] `workspace/profile.md` existe — stage declarado e contexto do membro

Se o manifest faltar (rota ES1 — arquivo ausente) ou não parsear (rota ES2 — manifest quebrado), não aborte seco (rule `emergency-escape-paths.md`): ofereça **(A)** rodar a skill `setup`, **OU (B)** prosseguir perguntando direto ao membro faturamento mensal aproximado, gasto em ads e estágio, marcando `manifest.skipped_preflight += ["manifest.json"]` quando o manifest voltar a existir. Esta skill não tem pré-requisito de outra fase — time é conversa que pode acontecer a qualquer altura.

### Contexto a carregar

1. `workspace/[produto]/manifest.json` — **`stage`** (campo canônico, `member-stage-awareness.md`), `budget_daily`, `fixed_costs_monthly` (se existir), `manifest.finance` (resumo gravado pela `finance-engine`, se existir)
2. `workspace/[produto]/finance-engine/dados.json` **(se existir)** — `monthly_model.fixed_costs_monthly`, `monthly_model.operating_income`, `monthly_model.contribution_margin`, `cash.runway_months`. É a fonte da resposta "a folha cabe?" (ETAPA 8)
3. `workspace/[produto]/ad-analysis/dados.json` **(se existir)** — volume de criativos rodados e classificação; é o dado real por trás de "quantos conceitos/mês a máquina atual produz"
4. `workspace/[produto]/scale-engine/dados.json` **(se existir)** — fase de escala; escala agressiva com key man risk alto é risco que esta skill nomeia
5. Rodadas anteriores desta skill em `workspace/[produto]/team-engine/` — org, vagas e pipeline de candidatos são artefatos vivos: continue de onde parou, não recomece

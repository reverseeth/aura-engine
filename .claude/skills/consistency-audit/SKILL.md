---
name: consistency-audit
description: Auditoria cross-phase que valida consistência entre os artefatos gerados da product-research à creative-engine, incluindo a página (page-plan.json e design-tokens da page-design), o checkout (checkout-aov) e os artefatos pré-launch da bonus-delivery (Fase A, assets de bônus) e da retention-engine (Fase A, flows de recuperação). Detecta drift (mecanismo que muda entre offer, copy e página, VOC phrase que não aparece em nenhum hook, claim sem research foundation, promessa sem config de loja, bonus removido da oferta mas ainda anunciado, placeholder não resolvido em copy deployada). Use quando o membro disser "audit", "consistência", "review", "verificar coerência" ou antes de launch oficial. Roda smoke checks em minutos e retorna report com issues ordenadas por severity e fix paths.
---

# Consistency Audit · Passo 15 · apelido antigo: 09 <!-- gen:title -->

## Quando usar

Antes do launch oficial (ads go-live e página em produção), pra pegar as incoerências acumuladas ao longo das skills, da `product-research` à `creative-engine`, incluindo os artefatos pré-launch da `bonus-delivery` (Fase A) e da `retention-engine` (Fase A). Drift típico: mecanismo nomeado "X" na `offer-builder` virou "X-alt" nos hooks; VOC repetida 12x no market research ausente de todo hook; ad promete "in 14 days" e a página fala em "30 days"; garantia de "90 days" na copy contra 30 dias no `dados.json` da oferta; ad anunciando bônus removido do stack. A skill roda em dois momentos: gate pré-launch (sem `ad-strategy` nem `ad-analysis`, lidos só se existirem) e re-validação pós-iteração, quando eles já entram no cruzamento.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` existe com `setup_complete: true` e pelo menos 3 skills em `skills_completed[]`.
2. `report_language` do profile (default `pt-BR`) em todo output interno (inclusive `issue` e `fix_suggested` dos findings) e na conversa, no padrão de linguagem simples da regra 0; copy consumidor-final e VOC literal ficam em inglês US (o trecho auditado é citado no original, o veredito vai no idioma do report).
3. Input parcial: com `copy-engine/{copy-engine.md,dados.json}` e `creative-engine/dados.json` ambos ausentes, force `launch_recommendation: "CAUTION"` (nunca `GO`), registre cada artefato em `artefacts_missing[]`, marque os checks dependentes como `"skipped"` (nunca `"pass"`) e rode o que for possível.

## Contexto a carregar

Em todo `dados.json` de fase anterior, leia primeiro o objeto `resumo` e abra o arquivo inteiro só na etapa que precisar; sem `resumo`, leia inteiro. Os checks que comparam valor literal (mecanismo, garantia, bônus) abrem o campo de origem, nunca só o `resumo`.

Base pelo índice (domínios `copy-proof-persuasion-structure` e `page-landing-cro`): `python3 .claude/lib/kb-index/kb_lookup.py --skill consistency-audit --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 14 buscas adicionais por etapa; as queries embutidas nos checks (nos arquivos `reference/checks-*.md`) são piso obrigatório, rodam sempre e não contam no teto; o critério de relevância é por check (só entra a entrada que muda o veredito); nunca query genérica nem busca repetida. Escrita é da `copy-engine` e design da `page-design`; aqui é julgamento de auditoria.

## Fluxo da skill

### ETAPA 1 · Load artefatos

Leia `reference/load-artefatos.md`. Ler só os que existem: `product-research`; `market-research` (`voc_phrases[]`, `awareness_distribution`, `sophistication_stage`; fallback pro legado `relatorio.md`); `competitor-analysis` (`claims_saturation[]`, `swipe_adapt[]`, `positioning_recommendation`, `creative-patterns.json`); `offer-builder` (`mechanism.name`, `ump` e `ums` ou o legado `version_short`, `guarantee`, `pricing`, `bonuses[]`, `research-foundation.json`); `bonus-delivery` (status da Fase A por bônus); `copy-engine` (headlines, claims, `lead_type`, `voc_forced_continue`); `page/page-plan.json`, `page/design-system.md` e `page/design-tokens.json`; `checkout-aov/dados.json`; `creative-engine/dados.json` (conceitos e `hooks_bank[]`); emails da `retention-engine` Fase A; `ad-strategy` e `ad-analysis` só se existirem; `manifest.agentic` como contexto informativo, nunca bloqueante.

### ETAPA 2 · Check battery (ordenada por severity)

Cada check grava `check_id`, `severity`, `status` (`pass|fail|skipped`), `artifact`, `issue` e `fix_suggested`. Os sistemas da base que calibram cada veredito estão listados, com a query exata, no arquivo do bloco.

**CRITICAL (bloqueia launch).** Leia `reference/checks-critical.md`.
- C1, nome do mecanismo: `mechanism.name` da oferta literal em pelo menos 1 headline da copy e em pelo menos 1 conceito dos ads (hook, Bridge/Hold ou primary text; nunca exigido no hook de 3 segundos). Ausente dos dois lados, critical; de um lado só, high.
- C1b, mecanismo normalizado: `mechanism.name` idêntico ao `mechanism_name` do `research-foundation.json` (só se existir); divergência é critical (`check_id: "mechanism-drift"`).
- C1c, mecanismo na página: `page-plan.json.strategy.mechanism_name` idêntico ao da oferta; divergência é critical; sem page-plan, `skipped`.
- C2, claim forte sem prova ao lado: todo claim forte da copy e dos ads precisa de prova perto (número, item do banco de provas, depoimento de performance, demo, comparação), na mesma seção ou na seguinte; sem prova, high; promessa do hero sem prova em lugar nenhum, critical. O fix traz a prova pra perto e nunca suaviza o claim; julga-se a apresentação da prova, não a força do claim (Bencivenga, Hopkins, Schwab, Sinatra Test, puffery, auditoria de prova, os 4 erros de conversão, Greek Sweep, depoimento vazio contra depoimento de performance).
- C3, garantia divergente: `guarantee.duration_days` contra a copy e os primary texts; divergência de duração é critical; garantia antes do value build é medium no mesmo check.
- C4, urgência e escassez: a mesma alavanca com o mesmo número, prazo e porquê no ad, na página e no checkout; desalinhada, high.

**HIGH (fix recomendado antes do launch).** Leia `reference/checks-high.md`.
- H1, cobertura de VOC: o denominador é o subconjunto das 20 frases mais repetidas (o `voc_checklist` da `copy-engine`), nunca o pool inteiro; coverage abaixo de 30% é high; julgar também se a frase do cliente foi preservada ou diluída em jargão (Collier, Cashvertising, Mona Lisa Frame, us-language). `voc_forced_continue: true` vira a causa provável no finding.
- H2, awareness: awareness dominante contra o `lead_type` top-level da `copy-engine` (unaware e problem aware pedem `story` ou `secret`; product e most aware pedem `offer` ou `direct`); mismatch é high; julgar se o lead serve o awareness (Bencivenga, Brunson, grade de long-form).
- H3, sofisticação: Stage 3 exige mecanismo novo no headline, Stage 4 exige elaborar o mesmo mecanismo, Stage 5 exige identification; mismatch é high; julgar a força do headline (Schwartz, Reeves, Caples, NESB, competitor-swap).
- H4, diversificação dos ads: 2 ou mais `emotion_dominant` distintas (curiosity, urgency, fear, delight) e 3 ou mais `concept_type` distintos; em conceito marksman, 3 frases distintas em `concepts[].angles[]` (Sniper não é finding). Concentrado, high. Cânone `.claude/lib/ad-taxonomy/README.md` §7.
- H5, bônus fantasma: toda menção a bônus na copy e nos ads precisa de entrada em `bonuses[]`; bônus visível na PDP exige a Fase A da `bonus-delivery` concluída (asset e status pronto); a `condition` de cada bônus bate com a copy da página. Cada falha é high, com a decisão do membro no fix.

**MEDIUM (bom corrigir).** Leia `reference/checks-medium.md`.
- M1, claim saturado (`saturation: HIGH`) no hero ou nos hooks; rebaixa pra pass quando a copy o reapresenta com diferenciação (preemptive claim, inoculation, defeito reatribuído como prova).
- M2, gap forte da `competitor-analysis` (as 5 dimensões achatadas numa lista) sem nenhuma peça explorando.
- M3, `hook_swap_viable: false` com o Hooks Bank usado como swap no conceito.
- M4, duração do script contra o word count.
- M5, tipo de página contra o awareness (advertorial, landing, pdp), mais o primeiro olhar e o mix de seções quando `page/design/page.html` existe (Grunt Test, teste de 5 segundos, CTA no hero por awareness, DM Sweep, táticas de bounce como menu de fix).
- M6, tokens da variação aprovada contra o `design-system.md`.
- M7, placeholders não resolvidos nos artefatos consumidor-final (`{{ALGO}}`, `[TBD]`, `XX%`, lorem ipsum), com as exceções de Liquid e merge tags; em superfície já publicada, sobe pra high.

### ETAPA 3 · Output (dual output, rule 6b do CLAUDE.md)

Leia `reference/output-e-dados-json.md`. `mkdir -p workspace/[produto]/consistency-audit/`; `consistency-audit.md` (`**Risco:**` pra critical, `**Atenção:**` pra high, `**Nota:**` pra medium, veredito em negrito no título, tabela `KPI | Valor` pros counters), `consistency-audit.html` por `python3 tools/render_report.py workspace/[produto]/consistency-audit/consistency-audit.md`, e `dados.json` no schema do arquivo (`findings[]` com `status` em `pass|fail|skipped`, `artefacts_missing[]`, counters e `launch_recommendation`). Antes de salvar, priorize os fixes pelo ICE (cada `fix_suggested` como hipótese se-então-porque; fila ordenada por severity, com o ICE como desempate). Manifest pelo script: `python3 tools/manifest.py <slug> complete consistency-audit` e `python3 .claude/lib/workspace-index/build_index.py <slug>`. Quem lê o `dados.json`: a `ad-strategy` (gate bloqueante, `BLOCK` aborta a campanha), a `page-build` (gate informativo de deploy) e a `retention-engine` na Fase A.

### ETAPA 4 · Decisão

Leia `reference/decisao-e-mensagem-final.md`. `issues_critical > 0` é `BLOCK` (BLOQUEAR); high sem critical é `CAUTION` (CUIDADO); input parcial força no mínimo `CAUTION`; tudo limpo e sem artefato essencial faltando é `GO` (PODE LANÇAR), com o próximo passo 'ad strategy'.

## SALVAR

Os três artefatos e o manifest saem na ETAPA 3, com as convenções de `reference/output-e-dados-json.md`.

## Mensagem final

Íntegra em `reference/decisao-e-mensagem-final.md`: a recomendação (BLOQUEAR, CUIDADO ou PODE LANÇAR), os contadores por severity, o caminho do `.html` pra revisar cada issue com o fix sugerido, e o passo seguinte (re-rodar a auditoria depois de corrigir, ou 'ad strategy' quando GO).

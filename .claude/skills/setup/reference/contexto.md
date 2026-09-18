# Setup · Referência: Objetivo, quando usar, consulta à base, boas-vindas e pré-flight (ETAPA 0)

> O texto integral do objetivo da skill, do quando usar, da consulta à base pelo índice com o núcleo mínimo do roteamento (ECommerce Bootstrapping, query exata), da saudação bilíngue da primeira vez e do pré-flight (workspace gravável, render de relatórios, teste único do MCP e a regra do `report_language`). Abra antes da ETAPA 1.

Esta skill roda quando o membro digita "setup" ou quando é a primeira vez usando o Aura Engine. O objetivo é: (1) garantir que o ambiente técnico está funcional, (2) entender a situação do membro com o mínimo de fricção, (3) extrair automaticamente tudo que já dá pra extrair (ex: dados da loja se o membro tem link), e (4) rotear pro próximo passo certo.

## Quando Usar

- Primeira vez que o membro abre o Claude Code na pasta do Aura Engine
- Membro digitou "setup", "onboarding", ou "configurar"
- Membro quer refazer o onboarding (ex: mudou de produto, de stack, ou de situação)

## Antes de Começar

> **Índice da base (kb-index):** esta skill NÃO usa query genérica ("fundamentos DTC", "onboarding"). Ela puxa SISTEMAS NOMEADOS pelo índice `.claude/lib/kb-index/`, e as entradas dela vivem espalhadas por vários domínios (o mapa do README aponta os principais). **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill setup --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 6 buscas por etapa. As queries já embutidas na etapa são o mínimo garantido. Não repita busca de framework já puxado na sessão.

**Núcleo mínimo do roteamento (rode a `best_query` exata):**

- **ECommerce Bootstrapping (101-Test Log, 9-in-10-Fail Sine Wave, The Crash, $10K/Hour)** (rode `ecommerce bootstrapping zero to multi 7 figures 101 testing log crash 10000 hour framework`) — o que cada estágio de membro (sem produto, com produto, vendendo, escalando) precisa priorizar e onde cada um quebra. Informa a classificação da ETAPA 3 e o roteamento da ETAPA 6.

### ETAPA 0 — Boas-vindas (só na primeira vez)

Se for a primeira vez do membro (não existe `workspace/profile.md`), abra com uma saudação curta de UMA linha, bilíngue (o idioma ainda não foi escolhido), só pra dar contexto antes dos checks técnicos:

> Bem-vindo ao Aura Engine. Vou configurar tudo pra você — leva uns 2 minutos. / Welcome to Aura Engine. I'll set everything up for you — takes about 2 minutes.

Se já existe profile (membro refazendo setup), pule a saudação e vá direto pro Pré-flight.

### Pré-flight

Antes de prosseguir, valide:

- [ ] `workspace/` existe e é gravável: `mkdir -p workspace && touch workspace/.aura-probe && rm workspace/.aura-probe` — se falhar (permissão), pare e dê a instrução de correção (sem permissão de escrita não há onde salvar nada).
- [ ] Render de relatórios disponível: `python3 tools/render_report.py --help` responde (o script e o template `.claude/templates/aura-report-template.html` vêm no repo) — se faltar, NÃO pare: a Etapa 5 salva só o `.md` e avisa.

O MCP `aura` é testado UMA vez, na ETAPA 2 (com query real) — não duplique o teste aqui.

> **report_language (rule 0 — INVIOLÁVEL):** esta skill é onde o `report_language` é DEFINIDO (ETAPA 2.6). A partir do momento em que o membro escolhe, TODA conversa e TODO output interno (.md/.html/.json descritivo) usam esse idioma; antes disso, default é `pt-BR`. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language. A escolha é gravada em `workspace/profile.md` E espelhada em `manifest.report_language`.

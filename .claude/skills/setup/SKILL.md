---
name: setup
description: Onboarding do membro na primeira vez que ele abre o Aura Engine, ou quando digita "setup", "onboarding" ou "configurar". Verifica o ambiente técnico (Node.js 20 ou mais é obrigatório; FFmpeg, Whisper, Groq, Python, single-file-cli, Playwright e o venv do design-clone são opcionais), testa o MCP da Aura com uma query real, confirma o atalho aura, pergunta o idioma dos relatórios antes de qualquer outra coisa, explica como a Aura funciona em 30 segundos, coleta 4 respostas (situação A a D, budget diário, ferramentas e ESP, links da loja e do produto), extrai dados da página do produto (preço, hero, garantia, mecanismo, cores e fontes), grava profile.md, brand.md e manifest.json (fonte única de verdade, validada pelo manifest.py), entrega o checklist de blindagem da conta Meta e roteia o membro pra fase certa pela situação dele. Use quando o membro disser "setup", "onboarding", "configurar", ou no primeiro uso do sistema.
---

# Setup · Passo 1 · apelido antigo: 00 <!-- gen:title -->

## Quando usar

Primeira vez que o membro abre o Claude Code na pasta do Aura Engine, quando ele digita "setup", "onboarding" ou "configurar", ou quando quer refazer o onboarding (mudou de produto, de stack ou de situação). O objetivo é garantir o ambiente técnico, entender a situação do membro com o mínimo de fricção, extrair sozinho tudo que já dá pra extrair e rotear pro próximo passo certo.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Íntegra em `reference/contexto.md`.

1. `workspace/` existe e é gravável (`mkdir -p workspace && touch workspace/.aura-probe && rm workspace/.aura-probe`); se falhar, pare e dê a instrução de correção.
2. `python3 tools/render_report.py --help` responde; se faltar, não pare: a ETAPA 5 salva só o `.md` e avisa.
3. O MCP `aura` é testado uma vez só, na ETAPA 2, com query real; não duplique o teste aqui.
4. `report_language` é definido nesta skill (ETAPA 2.6); antes da escolha o default é `pt-BR`. Copy consumidor-final e VOC literal ficam sempre em inglês US.

## Contexto a carregar

1. Base pelo índice: `python3 .claude/lib/kb-index/kb_lookup.py --skill setup --domain <domínio desta etapa>` (sem `--domain` quando a etapa cruza vários domínios); `best_query` exata com `deep=true`, no máximo 6 buscas adicionais por etapa; as queries embutidas nos arquivos de `reference/` são piso obrigatório, rodam sempre e não contam no teto; nunca query genérica nem busca repetida na sessão.
2. Núcleo mínimo do roteamento: o sistema ECommerce Bootstrapping (query exata em `reference/contexto.md`), que diz o que cada estágio de membro precisa priorizar e onde cada um quebra; informa a classificação da ETAPA 3 e o roteamento da ETAPA 6.

## Fluxo da skill

### ETAPA 0 · Boas-vindas (só na primeira vez)

Sem `workspace/profile.md`: saudação de uma linha, bilíngue, só pra dar contexto antes dos checks (texto em `reference/contexto.md`). Com profile (membro refazendo o setup), pule a saudação e vá direto pro pré-flight.

### ETAPA 1 · Verificação de dependências

Leia `reference/dependencias.md`. Node.js v20 ou mais é obrigatório: detecte por caminho direto, nvm e brew, e valide o número da major (v20.11.0 vira 20); ausente ou abaixo de 20 é falha, com a instrução exata de upgrade (nvm, brew ou winget). Depois liste as opcionais como "disponível", sem bloquear: FFmpeg (recomendado: o Limpador de Metadados precisa dele pra limpar vídeo), Whisper.cpp, Groq API key (transcrição rápida na `competitor-analysis`), Python 3, single-file-cli via npx, Playwright com Chromium no venv do fetcher (recomendado: sem ele Reddit, Trustpilot, Amazon e Cloudflare bloqueiam a pesquisa) e o venv de `tools/design-clone/`. Não prossiga enquanto o Node não estiver OK.

### ETAPA 2 · Verificação do MCP Aura

Leia `reference/mcp-e-atalho.md`. Rode `search_knowledge("market sophistication stages")` e confira que volta conteúdo real; mostre "Aura conectada e respondendo" sem inventar números. Se falhar, diagnostique nesta ordem: aprovação recusada (`claude mcp reset-project-choices` no terminal, fora do Claude Code, reiniciar e aprovar o servidor) e, se não resolver, registro manual do servidor com `claude mcp add` (comando completo no arquivo). Não prossiga sem o MCP funcionando.

### ETAPA 2.5 · Confirmação do atalho `aura`

O hook de início de sessão cria o alias sozinho, em zsh, bash e fish. Só confirme ao membro que da próxima vez basta abrir o Terminal e digitar `aura`; oculte a frase se o shell for outro.

### ETAPA 2.6 · Idioma dos relatórios (pergunta 1, antes de qualquer outra)

Leia `reference/idioma-e-apresentacao.md`. Pergunte, em português e em inglês na mesma mensagem, se os relatórios internos saem em português (1) ou em inglês (2); grave `REPORT_LANGUAGE` como `pt-BR` ou `en`. Daí em diante toda a conversa acontece no idioma escolhido, as 4 perguntas da ETAPA 3 saem traduzidas e o `profile.md` também; copy consumidor-final continua sempre em inglês.

### ETAPA 2.7 · Como a Aura funciona (só na primeira vez)

Mesmo arquivo. Resumo de 30 segundos, no idioma escolhido, das cinco fases (pesquisa, estratégia, loja, tráfego e pós-venda) e do painel `ABRIR-AQUI.html`; texto pronto em pt-BR e a estrutura pra `en`. Membro refazendo o setup pula esta etapa.

### ETAPA 3 · Onboarding do membro (perguntas por texto)

Leia `reference/onboarding-e-extracao.md`. Uma mensagem só com as 4 perguntas: situação (A sem produto, B tem produto e não lançou, C vende e não escala, D escala e quer otimizar), budget diário em dólares, ferramentas (TrendTrack, Higgsfield, Notion) mais a plataforma de email na pergunta 3b, e os links da loja e do produto. Parseie `SITUACAO`, `BUDGET`, `TOOLS`, `ESP` (tokens exatos do enum do manifest-schema; `shopify_email` com underscore), `LINK` e `SHOPIFY_LINK`; se faltou algo, pergunte só o que faltou. Classifique o budget sem mostrar: abaixo de 50 dólares por dia é starter, de 50 a 199 standard, de 200 a 999 escala-inicial, 1000 ou mais escala-avançada.

### ETAPA 4 · Auto-extração de dados da loja

Mesmo arquivo. Com link do produto, faça o fetch da página antes de salvar o profile: nome, preço e bundles, descrição, features, hero headline e sub-headline, garantia, tipo de hero, mecanismo único, link de checkout, 3 a 5 hex dominantes e as font-families. Cascade da rule `resilient-fetch`: `WebFetch` primeiro; barrado ou precisando do CSS cru, `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode html`; só depois documente "não acessível". O que não sair vira `[preencher]`. Tudo vai pro profile, e nenhuma skill seguinte pergunta isso de novo.

### ETAPA 5 · Salvar profile

Leia `reference/profile-e-brand.md`. `mkdir -p workspace/ workspace/[produto]/` e grave `workspace/profile.md` no formato do arquivo de apoio: idioma dos relatórios, situação, classificação e budget diário, data do setup, ferramentas com a ESP, links e o bloco de dados extraídos da página.

### ETAPA 5A · Inicializar o `brand.md` do produto

Mesmo arquivo. Situação diferente de A: copie `.claude/templates/brand.md.template` pra `workspace/[produto]/brand.md` e preencha slug, paleta, fontes e o caminho do logo com o que saiu da ETAPA 4; puxe Brand Voice Measurement (query exata no arquivo) e registre a voz atual da marca em vocabulário, tom e cadência; o resto fica `[preencher]` e o membro é avisado pra completar antes de `page`. Situação A pula (a `product-research` cria o `brand.md` do produto vencedor). Escape ES1 se o template faltar: `brand.md` mínimo inline ou pular marcando `skipped_preflight`.

### ETAPA 5B · Criar o manifest (fonte única de verdade)

Leia `reference/manifest.md`. Grave `workspace/[produto]/manifest.json` com `product_slug` (slugify; `dev-placeholder-[YYYYMMDD]` na situação A), `product_name`, `product_url`, `store_url`, `created_at` e `updated_at` em ISO-8601 UTC, `setup_complete: true`, `budget_daily` (número, campo canônico de budget), `budget_tier`, `stage` (A e B starter, C validating, D scaling), `market` US, `copy_language` en, `report_language`, `esp`, `product_vertical` pelo enum do schema (ambíguo, pergunte em 1 linha) e `skills_completed: ["setup"]`. Situação C ou D: duas perguntas opcionais numa mensagem, `aov_baseline` e `cogs_estimate`. Depois `python3 tools/migrate.py --product [produto]` (carimba `framework_version`) e `python3 tools/manifest.py [produto] validate`.

### ETAPA 5C · Blindagem da operação Meta (anti-ban + marca)

Leia `reference/blindagem-meta.md` e puxe os quatro sistemas pela query exata: estrutura de assets anti-ban (2 a 3 business managers, 3 admins reais em cada), aquecimento da conta de anúncio, trademark com Brand Rights Protection e o aviso do invoicing da Meta. Condense num checklist de 3 a 5 bullets no idioma do membro, entregue com a mensagem final; A e B recebem como "arme isso antes do primeiro ad", C e D como auditoria do que falta. A matemática do float é da `finance-engine`; quem audita os backups depois é a `ops-engine`.

### ETAPA 6 · Confirmação e roteamento inteligente

Leia `reference/roteamento.md`. Abra com `✓ Setup completo!` e a mensagem da situação (texto integral no arquivo): A vai pra `product research`, B pra `market research`, C pra `ad analysis`, D pra `scale`. Sempre feche com a lista das fases na ordem em que rodam (com os apelidos e as laterais), a frase de que cada fase lê o que as anteriores produziram e o painel `workspace/[produto]/ABRIR-AQUI.html`; em `en`, tudo traduzido, inclusive a frase do painel.

## SALVAR

Leia `reference/salvar-e-mensagem-final.md`. Quatro arquivos: `workspace/profile.md`; `workspace/profile.html` por `python3 tools/render_report.py workspace/profile.md` (se o script falhar, avise em 1 linha, siga só com o `.md` e peça um `git pull` no fim; nunca escreva o HTML à mão nem aborte o setup); `workspace/[produto]/manifest.json`; e `workspace/[produto]/brand.md` (só situação diferente de A). Profile ou manifest anterior: backup em `workspace/.profile-backup-[YYYYMMDD-HHMMSS].md` e `workspace/[produto]/.manifest-backup-[YYYYMMDD-HHMMSS].json` antes de sobrescrever. Por fim `python3 .claude/lib/workspace-index/build_index.py [product_slug]` gera o painel `ABRIR-AQUI.html`, que toda skill seguinte regenera.

## Mensagem final

Já coberta na ETAPA 6, pela situação. Acrescente a nota do `manifest.json` como fonte única: nunca editar à mão; toda alteração passa por `python3 tools/manifest.py <slug> set|complete` (backup e validação contra o schema), e o estado verificado do produto sai de `python3 tools/aura-status.py <slug>`. Íntegra em `reference/salvar-e-mensagem-final.md`.

# Setup · Referência: Verificação de dependências (ETAPA 1)

> A detecção do Node.js por caminho direto, nvm e brew, a validação da major version com a instrução de upgrade por sistema, e a lista das ferramentas opcionais (FFmpeg, Whisper.cpp, Groq API key, Python 3, Playwright com Chromium no venv do fetcher, o venv do design-clone e as ferramentas de design da page-design: Awwwards, Vercel, taste-skill, dembrandt e os opcionais 21st.dev e brag) com os comandos de instalação e teste. Abra na ETAPA 1.

### ETAPA 1 — Verificação de Dependências

Antes de qualquer pergunta, verifique se o ambiente técnico está OK. Dependência obrigatória: **Node.js v20+**.

**Node.js** — detecte de forma inteligente:

```bash
# Node via direct
node --version 2>/dev/null

# Node via nvm
NVM_DIR="${NVM_DIR:-$HOME/.nvm}"; [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && nvm current 2>/dev/null || true

# Node via brew
/opt/homebrew/bin/node --version 2>/dev/null
/usr/local/bin/node --version 2>/dev/null
```

**Valide o NÚMERO da major version, não só presença.** Parseie a saída (ex: `v20.11.0` → major `20`):

```bash
NODE_MAJOR=$(node --version 2>/dev/null | sed -E 's/^v([0-9]+).*/\1/')
[ -n "$NODE_MAJOR" ] && [ "$NODE_MAJOR" -ge 20 ] && echo "OK ($NODE_MAJOR)" || echo "FAIL"
```

Se Node estiver ausente OU a major < 20, trate como FALHA (não prossiga) e mostre a instrução de upgrade:
- Mac via nvm: `nvm install 20 && nvm use 20`
- Mac via brew: `brew install node` (ou `brew upgrade node` se já instalado em versão antiga)
- Windows: `winget install OpenJS.NodeJS.LTS` (ou nvm-windows: `nvm install 20 && nvm use 20`)

Para a dependência obrigatória:
- ✅ se instalada com major ≥ 20, mostrando a versão
- ❌ se ausente OU major < 20, com a instrução exata de upgrade acima

Também detecte ferramentas opcionais pra uso futuro, mostrando como "disponível" (não bloqueador):
- FFmpeg (RECOMENDADO — o Limpador de Metadados precisa dele pra limpar VÍDEO antes do upload, regra 12 do CLAUDE.md; e a transcrição de criativos da `competitor-analysis` também usa): `ffmpeg -version 2>/dev/null | head -1` — paths comuns: `/opt/homebrew/bin/ffmpeg`, `/usr/local/bin/ffmpeg`, `/usr/bin/ffmpeg`. Install: `brew install ffmpeg` (Mac), `winget install Gyan.FFmpeg` (Windows) ou `apt install ffmpeg` (Linux).
- Whisper.cpp: verificar `~/whisper.cpp/main`, `/usr/local/bin/whisper-cli`, `/opt/homebrew/bin/whisper-cli`. Install: `brew install whisper-cpp` (Mac) ou `git clone https://github.com/ggerganov/whisper.cpp.git ~/whisper.cpp && cd ~/whisper.cpp && make`.
- **Groq API key (opcional — transcrição rápida):** cheque `[ -n "${GROQ_API_KEY:-}" ] && echo "disponível"`. Se o membro tiver uma key da Groq no ambiente, a skill `competitor-analysis` (competitor analysis, ETAPA 3C) transcreve os vídeos dos concorrentes via API (`whisper-large-v3-turbo`) — muito mais rápido que o Whisper local. A cascade de transcrição é: Groq API (se key) → Whisper local → pedir o transcript ao membro. Sem a key, nada quebra.
- Python 3: `python3 --version` — necessário pro QA e pra captura de referência da skill `page-design` (`tools/page-qa/`, `verify_page.py`, `downloader.py`). Mac já vem com Python 3.
- **Playwright + Chromium (RECOMENDADO — coleta resiliente de pesquisa):** o fetcher `.claude/lib/web-fetch/fetch.py` usa um navegador real pra contornar bloqueios (Cloudflare/403/429/Reddit) nas skills `market-research` (VOC), 03 (PDPs/ads) e no QA da `page-design` (`verify_page.py`). Como o python moderno é externally-managed (PEP 668), instale num venv:
  ```bash
  python3 -m venv .claude/lib/web-fetch/.venv
  .claude/lib/web-fetch/.venv/bin/pip install -r .claude/lib/web-fetch/requirements.txt
  .claude/lib/web-fetch/.venv/bin/playwright install chromium
  ```
  Se já existir `tools/design-clone/.venv` com Playwright, o fetcher reusa automaticamente — pode pular. Teste: `python3 .claude/lib/web-fetch/fetch.py https://example.com --json`. Sem isso, as skills `market-research`/`competitor-analysis` funcionam só com WebSearch/WebFetch (cobertura menor quando sites bloqueiam).
- **Venv do design-clone (RECOMENDADO — captura de referência e conversor da `page-design`):** o `tools/design-clone/downloader.py` (captura em faixas do modo referência) e o `liquid-converter.py` (page-build) precisam de Playwright/bs4 num venv PRÓPRIO (mesma razão PEP 668). Crie logo após o venv do fetcher:
  ```bash
  python3 -m venv tools/design-clone/.venv
  tools/design-clone/.venv/bin/pip install -r tools/design-clone/requirements.txt
  tools/design-clone/.venv/bin/playwright install chromium
  ```
  O download do Chromium é compartilhado entre venvs (cache do Playwright em `~/Library/Caches/ms-playwright`) — se o passo anterior já baixou, este comando só registra e não baixa de novo. Os scripts do design-clone fazem bootstrap re-exec automático (mesmo padrão do fetch.py): com o venv existindo, `python3 tools/design-clone/downloader.py ...` direto funciona. Se a criação falhar (sem rede, pip bloqueado), NÃO bloqueie o setup: avise que o modo referência da `page-design` fica indisponível (o modo direção segue normal) e siga.

**Ferramentas de design da `page-design` (opcionais, não bloqueiam):** sem uma delas, a etapa que a usa roda na reserva, e o setup avisa qual. Mostre cada uma como "disponível" ou "ausente → reserva: X".
- **Node 22.13 ou mais pro MCP do Awwwards:** o `awwwards-mcp` exige isso no `engines`. Com Node 20, o resto da Aura funciona, e a page-design busca referências pelo Refero ou pelo WebSearch. Primeira execução (baixa o pacote): `npx -y awwwards-mcp@1.14.0 --help >/dev/null 2>&1 && echo "disponível"`.
- **Skills do Awwwards** (vêm dentro do pacote; dão o passo a passo de inspiração, estudo de movimento e diagnóstico):
  ```bash
  npm install --prefix ~/.cache/aura/awwwards awwwards-mcp@1.14.0
  for s in awwwards-inspiration awwwards-motion-study awwwards-setup awwwards-doctor; do cp -R ~/.cache/aura/awwwards/node_modules/awwwards-mcp/skills/$s ~/.claude/skills/; done
  ```
  Depois rode a skill `awwwards-setup` (cria `~/.awwwards-mcp/preferences.json`). O índice local (`awwwards-index`) é opcional: deixa a busca mais rápida e funciona offline.
- **Skill da Vercel (preview da página):** `npx skills add vercel-labs/agent-skills --skill deploy-to-vercel`. O preview roda sem conta e não pede token. Sem a skill, o membro abre o `page.html` local.
- **Plugins taste-skill e dembrandt:** o repo já os declara em `.claude/settings.json`; o Claude Code pede para instalar ao abrir a pasta. Sem o dembrandt, a marca sai pela reserva da ETAPA 4 (CSS cru).
- **Opcionais, só pra quem quiser:**
  - **21st.dev** (componentes de referência): MCP `https://21st.dev/api/mcp`, com a chave `TWENTYFIRST_API_KEY` no `.env` (nunca no chat nem em arquivo versionado).
  - **brag:** `claude plugin install brag@brag` (marketplace `latent-spaces/brag`).

NÃO prossiga enquanto o Node não estiver OK. As opcionais ficam como aviso — mas instalar o Playwright cedo melhora MUITO a qualidade de market research/competitor analysis (sem ele, Reddit/Trustpilot/Amazon/Cloudflare bloqueiam). Detalhes em `.claude/rules/resilient-fetch.md`.

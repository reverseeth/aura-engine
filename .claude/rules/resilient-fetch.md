# Resilient Fetch (NON-NEGOTIABLE)

> Aplica a TODA skill que busca dados na web (02 market research, 03 competitor analysis, 01 product research, 08/11/13/14 quando minerar social/reviews). Objetivo: **a Aura não trava nem inventa quando um site bloqueia.** Bloqueio é tratado, não é erro.

## A cascade (ordem obrigatória)

Pra qualquer dado que precise vir da web (VOC, PDP, ads, reviews):

1. **Descoberta = ferramenta nativa `WebSearch`.** Pra ACHAR URLs/threads/snippets, use a tool `WebSearch`. **NUNCA** scrapear HTML de buscador (google/bing/duckduckgo/brave) com fetch — isso cai em CAPTCHA/rate-limit rapidamente. Snippets de `WebSearch` já trazem muita VOC real (e a fonte/URL pra aprofundar).

2. **Fetch simples = ferramenta nativa `WebFetch`.** Tente primeiro — é mais barato e rápido.

3. **Se barrado (403/429/Cloudflare/login-soft/conteúdo só-JS) → o fetcher Playwright da Aura:**
   ```bash
   python3 .claude/lib/web-fetch/fetch.py "<url|termo>" --mode text|reddit|reviews|trends|adlib [--json]
   ```
   - **Reddit** → sempre `--mode reddit`. Cascade interna do modo: (1) front-ends redlib (com fallback entre instâncias); (2) se todos os redlib caírem → **API do Arctic Shift** (arquivo público de posts/comments do Reddit, sem key e sem login — cobre thread inteira por ID/URL). Reddit bloqueia fetch direto por IP, por isso nunca bater em reddit.com direto.
   - **Google Trends** → sempre `--mode trends` (aceita o termo direto ou a URL do explore; defaults US/5 anos). NUNCA tentar renderizar o site do Trends com `--mode text` — ele recusa navegador automatizado. O modo consulta a API de dados JSON do próprio Trends (HTTP puro → mesma API por dentro do Chromium) e devolve a série + classificação QUEDA/FLAT/SUBINDO/SPIKE pronta pra ETAPA 3 do product research. Degrau final se falhar: screenshot do membro.
   - **Meta Ad Library** → `--mode adlib` (espera + rolagem até os cartões de anúncio carregarem). Fallback: MCP TrendTrack (indexa os mesmos anúncios).
   - **Páginas de review (Amazon/Trustpilot/Loox/Yotpo)** → `--mode reviews` (rola pra carregar os widgets lazy). Amazon: URL de `/product-reviews/` é reescrita automaticamente pra página do produto (`/dp/`), que mostra os principais reviews sem login — pra volume, some fontes redundantes (Trustpilot, Target, iHerb).
   - **PDP com Cloudflare** → `--mode text`.
   - **Estudos científicos atrás de paywall/403 (ScienceDirect, journals)** → NÃO declarar bloqueado antes de tentar o espelho público: `WebSearch "PMC <título do estudo>"` → pmc.ncbi.nlm.nih.gov costuma ter o texto integral; o mínimo garantido é o resumo no PubMed. Só depois disso registrar o gap.
   - **USPTO / uspto.report (Cloudflare Turnstile)** → não insistir no site: dados de marca registrada saem por snippets do WebSearch + espelhos públicos (Justia, Trademarkia).
   - Exit code 2 = bloqueio irrecuperável; 3 = Playwright não instalado (rode o setup do README da lib).

4. **Se AINDA barrar (hard-CAPTCHA: Walmart/PerimeterX, Cloudflare Turnstile) →** caia pra: (a) MCP conectado (`mcp__trendtrack__*` pra competitor/ads, etc.), OU (b) **pedir o paste/screenshot ao membro**. **NUNCA fabricar a frase/claim que faltou.**

## Regras de integridade

- **Toda VOC e todo claim de concorrente é REAL e com fonte.** Se uma fonte caiu em todos os fallbacks, documente no Data Quality Summary / Data Source Audit (fonte tentada + motivo do bloqueio) e siga com o que tem — nunca preencher o buraco com texto plausível.
- **Fonte redundante > fonte teimosa.** Se o Walmart bloqueia mas o Amazon (mesmo produto) abre, use o Amazon. Não gaste 5 tentativas num site quando outro cobre a mesma evidência.
- **WebSearch pra descobrir, fetcher pra aprofundar.** O snippet do WebSearch é fiel pra captar a frase; o fetcher pega o thread/review inteiro quando precisar de volume e contexto.

## Dependência

O fetcher precisa de Playwright + Chromium (instalado pela skill 00 — setup, ou pelo comando no `.claude/lib/web-fetch/README.md`). Se ausente, o fetcher imprime o comando de setup; a skill informa o membro e segue com WebSearch/WebFetch enquanto isso.

## Anti-patterns (FORBIDDEN)

- Scrapear HTML de buscador (vira CAPTCHA) em vez de usar a tool `WebSearch`.
- Desistir de uma fonte importante no primeiro 403 sem tentar o fetcher Playwright.
- Inventar VOC/claim/review quando a fonte bloqueou — sempre documentar o gap e usar fonte redundante.
- Insistir num site hard-CAPTCHA quando outra fonte cobre a mesma evidência.

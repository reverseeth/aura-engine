# web-fetch — fetcher resiliente da Aura

Resolve os bloqueios que o `WebFetch` server-side sofre (403 / 429 / Cloudflare / login-wall soft / conteúdo só-JS) usando **Chromium headless real + stealth**. É o fallback que as skills usam quando o fetch nativo é barrado: VOC mining (Reddit, Trustpilot, Amazon, reviews), análise de PDP de concorrente (Cloudflare), e Meta Ad Library.

## Uso

```bash
python3 .claude/lib/web-fetch/fetch.py <url|termo> [--mode text|html|reddit|reviews|trends|adlib] [--max-chars N] [--json] [--wait MS]
```

- `--mode text` (default) — texto legível da página renderizada.
- `--mode reddit` — Reddit bloqueia fetch direto por IP. Reescreve a URL pra um front-end **redlib** (proxies open-source) com fallback automático entre instâncias (links curtos `redd.it/<id>` também são reescritos). Se **todos** os redlib e o reddit.com direto bloquearem, cai pro degrau final: a **API Arctic Shift** (archive público de Reddit, REST puro sem browser) — post + comments viram texto legível. Se ela também falhar, falha graciosa (exit 2).
- `--mode reviews` — rola a página pra carregar widgets de review lazy (Loox, Yotpo, Trustpilot). **Amazon:** a página `/product-reviews/` passou a exigir login; o fetcher reescreve automaticamente pra página do produto (`/dp/ASIN`), que mostra os principais reviews sem login. Pra volume maior de reviews da Amazon, combine com fontes redundantes (Trustpilot, Target, iHerb).
- `--mode trends` — **Google Trends sem renderizar o site** (o site recusa navegador automatizado). Consulta a API de dados JSON que o próprio Trends usa: primeiro por HTTP puro (biblioteca padrão, com o truque do cookie que a resposta 429 devolve), depois pela mesma API **por dentro do Chromium** (cookies + assinatura de rede reais). Aceita a URL do explore (lê `q`/`geo`/`date`) OU o termo direto no lugar da URL (defaults: US, 5 anos). Devolve a série temporal + classificação **QUEDA / FLAT / SUBINDO / SPIKE** (comparação: média do último ano vs histórico anterior; a série crua vem junto pra conferência). Com `--json`, o campo `trend` traz a série completa. Se tudo falhar, exit 2 → degrau final: screenshot do membro.
- `--mode adlib` — **Meta Ad Library** (página pública): os resultados chegam por JavaScript bem depois do primeiro carregamento; este modo espera + rola até o conteúdo dos anúncios aparecer (confirmação: "Library ID"/"Sponsored" no texto). Se vier só a casca, exit 2 → fallback: MCP TrendTrack (indexa os mesmos anúncios).
- `--mode html` — HTML renderado completo.
- `--json` — `{url, final_url, status, blocked, chars, text}` (+ `trend` no modo trends).

Em bloqueio irrecuperável: sai com código **2** e escreve um status claro no stderr (a skill cai pro próximo fallback). Com `--json`, o JSON `{"blocked": true, ...}` ainda vai pro stdout antes do exit 2 — o sinal vale nos dois modos. Código **3** = Playwright não instalado (ver Setup).

## A cascade de fetch resiliente (ordem que as skills seguem)

1. **Descoberta** → ferramenta nativa **WebSearch** (acha URLs + snippets; não scrapear HTML de buscador, que cai em CAPTCHA).
2. **Fetch simples** → ferramenta nativa **WebFetch**.
3. **Se barrado (403/429/Cloudflare/JS/CAPTCHA soft)** → **este fetcher** (`fetch.py`, navegador real).
4. **Se ainda barrar (hard-CAPTCHA tipo PerimeterX)** → MCP (TrendTrack/SpyBox) OU paste do membro. Nunca inventar dado.

Detalhes em `.claude/rules/resilient-fetch.md`.

## Scorecard (verificado 2026-07)

| Fonte | Bloqueio antes | Com `fetch.py` |
|---|---|---|
| Cloudflare PDP (ex: drinkag1.com) | 429 | ✅ 200 |
| Trustpilot | 403 | ✅ 200 (reviews) |
| Amazon reviews | `/product-reviews/` exige login | ✅ 200 (`--mode reviews` reescreve pra `/dp/` — reviews do produto visíveis sem login) |
| **Reddit** | 403 por IP | ✅ 200 via redlib (`--mode reddit`); degrau final = API Arctic Shift |
| **Google Trends** | "unsupported browser" (recusa headless) | ✅ série completa via API JSON (`--mode trends` — HTTP puro → API por dentro do Chromium) |
| **Meta Ad Library** | só a casca (resultados via JS tardio) | ✅ cartões de anúncio renderizados (`--mode adlib` — espera + rolagem até "Library ID"/"Sponsored" aparecerem) |
| Estudos científicos (ScienceDirect etc.) | paywall/403 | rota documentada: buscar o espelho público no **PMC** (`WebSearch "PMC <título do estudo>"` → pmc.ncbi.nlm.nih.gov); mínimo garantido = resumo no PubMed |
| Walmart | PerimeterX "Robot or human?" | ❌ hold-CAPTCHA não passa headless — **redundante com Amazon**; o fetcher falha gracioso e a skill segue pra outra fonte |
| uspto.report / Cloudflare Turnstile | interstitial | ❌ não passa — rota documentada: snippets do WebSearch + espelhos Justia/Trademarkia |

> O objetivo não é "passar 100% dos anti-bots" (CAPTCHAs hold-to-confirm e Turnstile não passam headless sem proxy residencial pago). O objetivo é **eliminar o ERRO**: detectar o bloqueio e cair pro próximo fallback de forma limpa, e **vencer a esmagadora maioria** (Cloudflare-soft, JS-render, 403, e o IP-block do Reddit via proxy).

## Setup (uma vez)

O script faz **bootstrap automático**: se o python atual não tem Playwright, ele re-executa usando o venv do framework. A skill 00 (setup) cria o venv:

```bash
python3 -m venv .claude/lib/web-fetch/.venv
.claude/lib/web-fetch/.venv/bin/pip install -r .claude/lib/web-fetch/requirements.txt
.claude/lib/web-fetch/.venv/bin/playwright install chromium
```

(Se já existe `tools/design-clone/.venv` com Playwright, o fetcher reusa ele automaticamente — não precisa duplicar.) O `.venv/` é gitignored.

## Manutenção

As instâncias **redlib** (lista `REDLIB` em `fetch.py`) podem cair com o tempo — são serviços comunitários. Se o `--mode reddit` começar a falhar, atualize a lista com instâncias vivas (busque "redlib instances" / o wiki do projeto redlib). O fetcher já tenta cada uma em ordem e cai pra próxima — e, se todas caírem, ainda tenta a **API Arctic Shift** (`ARCTIC` em `fetch.py`) como degrau final antes de desistir.

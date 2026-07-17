#!/usr/bin/env python3
"""
fetch.py — fetcher resiliente da Aura (navegador headless real + stealth).

Resolve os bloqueios que o WebFetch server-side sofre (403 / 429 / Cloudflare /
login wall soft / conteúdo só-JS) usando Chromium headless com user-agent real,
stealth e espera por conteúdo. É o FALLBACK que as skills usam quando o WebFetch
nativo é barrado (Reddit, Trustpilot, Amazon reviews, Meta Ad Library, PDPs com
Cloudflare, etc.). Hard-CAPTCHA (ex: Walmart/PerimeterX) NÃO passa — o fetcher
falha gracioso e a skill usa fonte redundante.

USO:
    python3 .claude/lib/web-fetch/fetch.py <url|termo> [--mode text|html|reddit|reviews|trends|adlib]
                                                       [--max-chars N] [--json] [--wait MS]

  --mode reddit   reescreve pra front-ends redlib (fallback entre instâncias);
                  se TODOS bloquearem, cai pra API Arctic Shift (archive público)
  --mode reviews  rola a página pra carregar widgets de review lazy (Loox/Yotpo/etc);
                  URL de /product-reviews/ da Amazon (que hoje exige login) é
                  reescrita pra página do produto, que mostra reviews sem login
  --mode trends   Google Trends SEM navegador: consulta a API de dados JSON que o
                  próprio site usa (explore → token → série temporal) e devolve a
                  série + classificação QUEDA/FLAT/SUBINDO/SPIKE. Aceita a URL do
                  explore (lê q/geo/date dela) OU o termo direto no lugar da URL.
                  Se a API limitar (429), cai pro navegador; se também bloquear,
                  exit 2 (skill pede screenshot ao membro — degrau final).
  --mode adlib    Meta Ad Library (página pública): espera longa + rolagem pra
                  forçar o carregamento dos resultados (que chegam por JS depois
                  do primeiro paint). Se vier só a casca, exit 2 (fallback: MCP
                  TrendTrack, que indexa os mesmos anúncios).
  --mode html     devolve o HTML renderado (não só o texto)
  --mode text     (default) devolve o texto legível
  --json          imprime {url, final_url, status, blocked, chars, text}
  --max-chars N   limita o texto (default 20000)

SAÍDA: por padrão imprime o texto. Em bloqueio irrecuperável, sai com código 2
(com --json o JSON {"blocked": true, ...} ainda vai pro stdout antes do exit) e
escreve um status claro no stderr (a skill cai pro próximo fallback — paste/MCP).

DEPENDÊNCIA: Playwright + Chromium. O script faz BOOTSTRAP automático: se o python
atual não tem playwright, ele re-executa usando o venv do framework
(.claude/lib/web-fetch/.venv ou tools/design-clone/.venv). Se nenhum existir, mostra
o comando de setup. A skill 00 (setup) cria o venv. (--mode trends usa só a
biblioteca padrão do python — funciona até sem o venv.)
"""
import sys, os, re, json, argparse
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

CHROME_MAJOR = "138"   # manter próximo do Chrome estável atual — versão velha demais
                       # dispara "unsupported browser" no Google Trends e similares
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      f"(KHTML, like Gecko) Chrome/{CHROME_MAJOR}.0.0.0 Safari/537.36")

# ─────────────────────────── Google Trends via API JSON ───────────────────────────
# O site do Trends é um app só-JS que ainda por cima recusa navegador headless
# ("unsupported browser"). Mas o app busca os dados numa API JSON pública — e ela
# responde a HTTP puro, sem navegador. Fluxo (o mesmo que o site faz): (1) aquecer
# cookie, (2) /api/explore devolve um token por widget, (3) /api/widgetdata/multiline
# devolve a série temporal. Só biblioteca padrão — roda antes do bootstrap do venv.

TRENDS_BASE = "https://trends.google.com"

def _trends_http(url, jar, expect_prefix):
    import urllib.request, urllib.error
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"{TRENDS_BASE}/trends/explore",
    })
    try:
        with opener.open(req, timeout=25) as resp:
            body = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        # truque documentado do Trends: a resposta 429 VEM com o cookie de sessão
        # (NID) que legitima a próxima tentativa — captura antes de propagar o erro
        try:
            jar.extract_cookies(e, req)
        except Exception:
            pass
        raise
    # as respostas da API vêm com um prefixo anti-hijack ()]}' ou )]}',) antes do JSON
    idx = body.find("{")
    if expect_prefix and idx > 0:
        body = body[idx:]
    return json.loads(body)

def _parse_trends_input(raw):
    """Aceita a URL do explore (lê q/geo/date) ou o termo cru. Defaults: US, 5 anos."""
    kw, geo, date = raw, "US", "today 5-y"
    if raw.startswith("http"):
        from urllib.parse import urlparse, parse_qs, unquote
        qs = parse_qs(urlparse(raw).query)
        kw = unquote(qs.get("q", [""])[0]) or raw
        geo = qs.get("geo", [geo])[0] or geo
        date = unquote(qs.get("date", [date])[0]) or date
    return kw, geo, date

def _trend_window(n):
    """Quantos pontos formam '1 ano recente': o Trends devolve pontos semanais em
    janelas de 5 anos (~260 pontos) e mensais em janelas maiores — a comparação
    justa é sempre último ano vs histórico anterior."""
    return 52 if n >= 150 else 12

def _classify_trend(values):
    """Buckets da ETAPA 3 do product research: QUEDA / FLAT / SUBINDO / SPIKE.
    Heurística simples e explicável sobre a série (0-100 do Trends)."""
    n = len(values)
    if n < 24:
        return "SEM-DADO"
    w = _trend_window(n)
    recent = values[-w:] if n >= w else values
    prior = values[:-w] or recent
    avg = lambda xs: sum(xs) / max(len(xs), 1)
    a_recent, a_prior = avg(recent), avg(prior)
    if a_recent >= 1.25 * max(a_prior, 1):
        # subiu forte — é subida sustentada ou pico que já desinfla? (o Trends
        # normaliza o pico da série pra 100, então "ter um 100 recente" é normal
        # em termo subindo; SPIKE exige a cauda atual bem abaixo do pico)
        peak_recent = max(recent)
        tail = avg(values[-4:])
        if peak_recent >= 2 * max(a_prior, 1) and tail < 0.5 * peak_recent:
            return "SPIKE"
        return "SUBINDO"
    if a_recent <= 0.75 * max(a_prior, 1) and avg(recent[-w // 2:]) <= avg(recent[:w // 2]):
        return "QUEDA"
    return "FLAT"

def _trends_series(kw, geo, date, get_json, max_chars):
    """Núcleo compartilhado: explore → token → série. get_json(url) → dict já parseado."""
    import urllib.parse
    req_payload = {"comparisonItem": [{"keyword": kw, "geo": geo, "time": date}],
                   "category": 0, "property": ""}
    explore_url = (f"{TRENDS_BASE}/trends/api/explore?hl=en-US&tz=240&req="
                   + urllib.parse.quote(json.dumps(req_payload)))
    widgets = get_json(explore_url)
    ts = next(w for w in widgets["widgets"] if w.get("id") == "TIMESERIES")
    data_url = (f"{TRENDS_BASE}/trends/api/widgetdata/multiline?hl=en-US&tz=240&req="
                + urllib.parse.quote(json.dumps(ts["request"]))
                + f"&token={ts['token']}")
    data = get_json(data_url)
    points = data.get("default", {}).get("timelineData", [])
    series = [(p.get("formattedTime", ""), (p.get("value") or [0])[0]) for p in points]
    values = [v for _, v in series]
    if not values:
        raise RuntimeError("série vazia")
    verdict = _classify_trend(values)
    w = _trend_window(len(values))
    avg = lambda xs: round(sum(xs) / max(len(xs), 1), 1)
    lines = [f"GOOGLE TRENDS — termo: {kw} | região: {geo} | janela: {date}",
             f"classificação: {verdict}  (média do último ano [{w} pontos]: {avg(values[-w:])} "
             f"vs média do histórico anterior: {avg(values[:-w] or values)}; "
             f"último valor: {values[-1]})",
             "", "últimos 24 pontos (data: valor 0-100):"]
    lines += [f"  {t}: {v}" for t, v in series[-24:]]
    text = "\n".join(lines)[:max_chars]
    return {"blocked": False, "status": 200, "text": text, "final_url": data_url,
            "title": f"trends:{kw}", "source": "trends-api",
            "trend": {"keyword": kw, "geo": geo, "date": date, "verdict": verdict,
                      "series": series}}

def fetch_trends(raw, max_chars=20000):
    """Degrau 1 do trends: API via HTTP puro (biblioteca padrão, sem navegador)."""
    import http.cookiejar, time as _t
    kw, geo, date = _parse_trends_input(raw)
    jar = http.cookiejar.CookieJar()
    def get_json(url):
        last_err = None
        for attempt in range(4):                      # o explore 429a fácil; o cookie que o
            try:                                      # próprio 429 devolve legitima a retentativa
                return _trends_http(url, jar, expect_prefix=True)
            except Exception as e:
                last_err = e
                _t.sleep(3 * (attempt + 1))
        raise last_err
    try:
        # aquecer cookie (o endpoint aceita melhor com cookie de sessão do site);
        # mesmo quando essas páginas respondem 429, o cookie vem junto e é capturado
        for warm in (f"{TRENDS_BASE}/?geo={geo}", f"{TRENDS_BASE}/trends/explore?geo={geo}"):
            try:
                _trends_http(warm, jar, expect_prefix=False)
            except Exception:
                pass
        return _trends_series(kw, geo, date, get_json, max_chars)
    except Exception as e:
        return {"blocked": True, "status": -1, "text": "", "final_url": raw,
                "error": f"trends-api: {str(e)[:160]}"}

def fetch_trends_browser(raw, max_chars=20000):
    """Degrau 2 do trends: a MESMA API, mas chamada por dentro do navegador —
    as requisições saem com cookies e assinatura de rede do Chromium real."""
    kw, geo, date = _parse_trends_input(raw)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox", "--disable-dev-shm-usage"])
            ctx = browser.new_context(
                user_agent=UA, locale="en-US", timezone_id="America/New_York",
                extra_http_headers={"Accept-Language": "en-US,en;q=0.9"})
            ctx.add_init_script(STEALTH)
            page = ctx.new_page()
            _mask_client_hints(ctx, page)
            from urllib.parse import quote
            page.goto(f"{TRENDS_BASE}/trends/explore?date={quote(date)}&geo={geo}&q={quote(kw)}",
                      wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3500)               # deixa o app assentar cookies de sessão
            def get_json(url):
                last_err = None
                for attempt in range(3):
                    r = ctx.request.get(url, headers={"Referer": f"{TRENDS_BASE}/trends/explore"})
                    if r.ok:
                        body = r.text()
                        idx = body.find("{")
                        return json.loads(body[idx:] if idx > 0 else body)
                    last_err = RuntimeError(f"HTTP {r.status}")
                    page.wait_for_timeout(2500 * (attempt + 1))
                raise last_err
            try:
                return _trends_series(kw, geo, date, get_json, max_chars)
            finally:
                browser.close()
    except Exception as e:
        return {"blocked": True, "status": -1, "text": "", "final_url": raw,
                "error": f"trends-browser: {str(e)[:160]}"}

# ─────────────────────────────── bootstrap do venv ────────────────────────────────

def _bootstrap():
    """Re-exec into a venv that has playwright, if the current python doesn't.

    O python do venv costuma ser SYMLINK pro python base (resolvem igual), mas
    invocar `<venv>/bin/python` ativa o site-packages do venv mesmo assim. Por
    isso NÃO comparamos resolve(); a env var guarda a lista de venvs JÁ TENTADOS
    (evita loop e ainda tenta o próximo venv se o primeiro estiver quebrado).
    """
    try:
        import playwright  # noqa
        return
    except ModuleNotFoundError:
        pass
    tried = set(filter(None, os.environ.get("AURA_FETCH_BOOTSTRAPPED", "").split(":")))
    for cand in [REPO / ".claude/lib/web-fetch/.venv/bin/python",
                 REPO / "tools/design-clone/.venv/bin/python"]:
        if str(cand) in tried or not cand.exists():
            continue
        env = {**os.environ,
               "AURA_FETCH_BOOTSTRAPPED": ":".join(sorted(tried | {str(cand)}))}
        os.execve(str(cand), [str(cand), *sys.argv], env)
    sys.stderr.write(
        "[aura-fetch] Playwright não instalado. Setup (uma vez):\n"
        f"  python3 -m venv {REPO}/.claude/lib/web-fetch/.venv\n"
        f"  {REPO}/.claude/lib/web-fetch/.venv/bin/pip install -r {REPO}/.claude/lib/web-fetch/requirements.txt\n"
        f"  {REPO}/.claude/lib/web-fetch/.venv/bin/playwright install chromium\n")
    sys.exit(3)

def _is_trends_mode():
    try:
        return sys.argv[sys.argv.index("--mode") + 1] == "trends"
    except (ValueError, IndexError):
        return False

# --mode trends usa só biblioteca padrão, MAS o fallback dele (renderizar no
# navegador quando a API limita) precisa do Playwright — então o bootstrap roda
# sempre que um venv existir; a diferença é que no trends a AUSÊNCIA de venv não
# aborta (o modo funciona sem navegador, só perde o degrau de fallback)
if _is_trends_mode():
    try:
        import playwright  # noqa
    except ModuleNotFoundError:
        tried = set(filter(None, os.environ.get("AURA_FETCH_BOOTSTRAPPED", "").split(":")))
        for cand in [REPO / ".claude/lib/web-fetch/.venv/bin/python",
                     REPO / "tools/design-clone/.venv/bin/python"]:
            if str(cand) not in tried and cand.exists():
                env = {**os.environ,
                       "AURA_FETCH_BOOTSTRAPPED": ":".join(sorted(tried | {str(cand)}))}
                os.execve(str(cand), [str(cand), *sys.argv], env)
else:
    _bootstrap()

try:
    from playwright.sync_api import sync_playwright  # noqa: E402
except ModuleNotFoundError:                          # trends sem venv: segue sem navegador
    sync_playwright = None

# script injetado antes de qualquer JS da página — esconde sinais de automação
STEALTH = """
Object.defineProperty(navigator,'webdriver',{get:()=>undefined});
Object.defineProperty(navigator,'languages',{get:()=>['en-US','en']});
Object.defineProperty(navigator,'plugins',{get:()=>[1,2,3,4,5]});
window.chrome={runtime:{}};
if(window.navigator.permissions&&window.navigator.permissions.query){
  const _q=window.navigator.permissions.query.bind(window.navigator.permissions);
  window.navigator.permissions.query=(p)=>p&&p.name==='notifications'
    ?Promise.resolve({state:Notification.permission}):_q(p);}
"""

# Client hints (cabeçalhos sec-ch-ua) entregam "HeadlessChrome" MESMO com o
# user-agent trocado — é assim que Google/Trends e outros farejam o headless.
# O override via CDP (protocolo de depuração) corrige o canal inteiro.
UA_METADATA = {
    "brands": [{"brand": "Chromium", "version": CHROME_MAJOR},
               {"brand": "Google Chrome", "version": CHROME_MAJOR},
               {"brand": "Not-A.Brand", "version": "99"}],
    "fullVersionList": [{"brand": "Chromium", "version": f"{CHROME_MAJOR}.0.0.0"},
                        {"brand": "Google Chrome", "version": f"{CHROME_MAJOR}.0.0.0"},
                        {"brand": "Not-A.Brand", "version": "99.0.0.0"}],
    "platform": "macOS", "platformVersion": "13.0.0", "architecture": "x86",
    "model": "", "mobile": False, "bitness": "64", "wow64": False,
}

def _mask_client_hints(ctx, page):
    """Sobrescreve UA + client hints via CDP (mata o tell 'HeadlessChrome')."""
    try:
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.setUserAgentOverride",
                 {"userAgent": UA, "acceptLanguage": "en-US,en;q=0.9",
                  "platform": "MacIntel", "userAgentMetadata": UA_METADATA})
    except Exception:
        pass  # sem CDP (raro), segue com o disfarce parcial de sempre

# Sinais de challenge page. HARD = frases que na prática só aparecem em interstitial
# de anti-bot. SOFT = palavras que também aparecem em conteúdo legítimo (VOC reclamando
# de captcha, thread sobre ser bloqueado) — só contam com corroboração.
HARD_SIGNS = [
    "just a moment", "verify you are human", "enable javascript and cookies",
    "checking your browser", "attention required", "cf-error", "px-captcha",
]
SOFT_SIGNS = [
    "are you a robot", "captcha", "unusual traffic", "access denied",
    "you've been blocked", "request blocked",
]

def looks_blocked(text, title, status=0):
    low = (text[:300] + " " + (title or "")).lower()
    if any(s in low for s in HARD_SIGNS):
        return True
    # sinais soft aparecem em VOC legítima ("the captcha kept failing...") — só contam
    # quando a página também é curta ou o status HTTP já denuncia bloqueio
    if any(s in low for s in SOFT_SIGNS) and (len(text.strip()) < 600
                                              or status in (403, 429, 503)):
        return True
    # página quase vazia também é sinal de bloqueio/JS-wall (piso baixo pra não
    # marcar páginas curtas legítimas como bloqueadas; a detecção real é por keyword acima)
    return len(text.strip()) < 120

def extract_text(html, max_chars):
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")
        for t in soup(["script", "style", "noscript", "svg", "template"]):
            t.decompose()
        txt = soup.get_text("\n")
    except Exception:
        txt = re.sub(r"<[^>]+>", " ", html)
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n\n", txt).strip()
    return txt[:max_chars]

# Reddit bloqueia fetch direto por IP/rede (pós-mudança de API). Usamos front-ends
# redlib (proxies open-source de Reddit) com fallback — renderizam o thread real.
REDLIB = ["https://safereddit.com", "https://redlib.catsarch.com", "https://eu.safereddit.com"]

# Degrau FINAL do --mode reddit: Arctic Shift, API pública de archive do Reddit.
# REST puro (sem browser). Se falhar, falha graciosa — o resultado bloqueado prevalece.
ARCTIC = "https://arctic-shift.photon-reddit.com/api"

def _targets(url, mode):
    if mode == "reddit":
        m = re.match(r"https?://redd\.it/([A-Za-z0-9]+)", url)
        if m:  # link curto (formato comum nos resultados do WebSearch) → thread nos redlib
            path = f"/comments/{m.group(1)}"
            return [b + path for b in REDLIB] + [url]
        path = re.sub(r"https?://(www\.|old\.|np\.|new\.)?reddit\.com", "", url)
        if not path.startswith("/"):
            return [url]
        return [b + path for b in REDLIB] + [url]
    if mode == "reviews" and "amazon." in url:
        # a página /product-reviews/ da Amazon passou a exigir login; a página do
        # PRODUTO (/dp/ASIN) ainda mostra os principais reviews sem login — vira o
        # alvo primário, com a URL original como segunda tentativa
        m = re.search(r"/product-reviews/([A-Z0-9]{10})", url)
        if m:
            host = re.match(r"https?://[^/]+", url).group(0)
            return [f"{host}/dp/{m.group(1)}", url]
    return [url]

def _reddit_post_id(url):
    m = re.search(r"redd\.it/([A-Za-z0-9]+)", url) or re.search(r"/comments/([A-Za-z0-9]+)", url)
    return m.group(1) if m else None

def _arctic_shift(url, max_chars):
    """Post + comments via API Arctic Shift. Retorna texto legível ou None (graceful fail)."""
    pid = _reddit_post_id(url)
    if not pid:
        return None
    import urllib.request
    def _get(u):
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    try:
        posts = _get(f"{ARCTIC}/posts/ids?ids={pid}").get("data") or []
        post = posts[0] if posts else {}
        parts = [p for p in [post.get("title"), post.get("selftext")] if p]
        try:
            comments = _get(f"{ARCTIC}/comments/search?link_id={pid}&limit=100").get("data") or []
        except Exception:
            comments = []
        for c in comments:
            body = (c.get("body") or "").strip()
            if body and body not in ("[deleted]", "[removed]"):
                parts.append(f"[{c.get('score', 0)} pts] {body}")
        text = "\n\n".join(parts).strip()
        return text[:max_chars] if len(text) >= 120 else None
    except Exception:
        return None

def fetch(url, mode="text", max_chars=20000, wait_ms=2500, retries=1):
    if mode == "trends":
        r = fetch_trends(url, max_chars)
        if not r.get("blocked") or sync_playwright is None:
            return r
        # HTTP puro limitou → mesma API por dentro do navegador (cookies + assinatura
        # de rede do Chromium real). Se também falhar, o resultado bloqueado prevalece
        # e a skill cai pro degrau final (screenshot do membro).
        return fetch_trends_browser(url, max_chars)
    targets = _targets(url, mode)
    last = {"blocked": True, "status": 0, "text": "", "final_url": targets[0]}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox", "--disable-dev-shm-usage",
        ])
        ctx = browser.new_context(
            user_agent=UA, locale="en-US", timezone_id="America/New_York",
            viewport={"width": 1280, "height": 900},
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        ctx.add_init_script(STEALTH)
        page = ctx.new_page()
        _mask_client_hints(ctx, page)
        for target in targets:                       # tenta cada alvo (redlib fallbacks)
            for attempt in range(retries + 1):
                try:
                    resp = page.goto(target, wait_until="domcontentloaded", timeout=30000)
                    status = resp.status if resp else 0
                    try:
                        page.wait_for_load_state("networkidle", timeout=wait_ms + 4000)
                    except Exception:
                        page.wait_for_timeout(wait_ms)
                    if mode == "reviews":
                        for _ in range(8):           # rola p/ disparar review widgets lazy
                            page.mouse.wheel(0, 2400)
                            page.wait_for_timeout(700)
                    if mode == "adlib":
                        # os resultados da Ad Library chegam por JS bem depois do
                        # primeiro paint — espera + rolagem até o conteúdo crescer
                        prev = 0
                        for _ in range(12):
                            page.mouse.wheel(0, 2000)
                            page.wait_for_timeout(1200)
                            cur = len(page.content())
                            if cur > 200_000 and cur == prev:
                                break
                            prev = cur
                    html = page.content()
                    title = page.title()
                    text = extract_text(html, max_chars)
                    blocked = looks_blocked(text, title, status) or status in (403, 429, 503)
                    last = {"blocked": blocked, "status": status, "text": text,
                            "final_url": page.url, "html": html if mode == "html" else None,
                            "title": title}
                    if not blocked:
                        browser.close()
                        return last
                    if attempt < retries:             # CF às vezes solta na retentativa;
                        page.wait_for_timeout(2000)   # sem espera morta na última tentativa
                except Exception as e:
                    last = {"blocked": True, "status": -1, "text": "",
                            "final_url": target, "error": str(e)[:200]}
                    page.wait_for_timeout(1200)
        browser.close()
    if mode == "reddit" and last.get("blocked"):
        txt = _arctic_shift(url, max_chars)           # degrau final: archive API (sem browser)
        if txt:
            return {"blocked": False, "status": 200, "text": txt,
                    "final_url": url, "title": "", "source": "arctic-shift"}
    return last

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--mode", default="text",
                    choices=["text", "html", "reddit", "reviews", "trends", "adlib"])
    ap.add_argument("--max-chars", type=int, default=20000)
    ap.add_argument("--wait", type=int, default=2500)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = fetch(a.url, mode=a.mode, max_chars=a.max_chars, wait_ms=a.wait)
    out = r.get("html") if a.mode == "html" and r.get("html") else r.get("text", "")
    if a.json:
        payload = {"url": a.url, "final_url": r.get("final_url"),
                   "status": r.get("status"), "blocked": r.get("blocked"),
                   "chars": len(out or ""), "text": out}
        if r.get("trend"):
            payload["trend"] = r["trend"]
        print(json.dumps(payload, ensure_ascii=False))
        if r.get("blocked") and not (out or "").strip():
            sys.exit(2)                              # mesmo sinal do modo texto (README)
    else:
        if r.get("blocked") and not (out or "").strip():
            sys.stderr.write(f"[aura-fetch] BLOQUEADO status={r.get('status')} "
                             f"err={r.get('error','-')} — caia pro próximo fallback "
                             f"(paste do membro / MCP TrendTrack/SpyBox).\n")
            sys.exit(2)
        print(out)
        if r.get("blocked"):
            sys.stderr.write(f"[aura-fetch] aviso: conteúdo parcial/possível bloqueio "
                             f"(status={r.get('status')}).\n")

if __name__ == "__main__":
    main()

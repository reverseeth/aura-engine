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
    python3 .claude/lib/web-fetch/fetch.py <url> [--mode text|html|reddit|reviews]
                                                 [--max-chars N] [--json] [--wait MS]

  --mode reddit   reescreve pra front-ends redlib (fallback entre instâncias);
                  se TODOS bloquearem, cai pra API Arctic Shift (archive público)
  --mode reviews  rola a página pra carregar widgets de review lazy (Amazon/Loox/etc)
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
o comando de setup. A skill 00 (setup) cria o venv.
"""
import sys, os, re, json, argparse
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

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

_bootstrap()

from playwright.sync_api import sync_playwright  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

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
    ap.add_argument("--mode", default="text", choices=["text", "html", "reddit", "reviews"])
    ap.add_argument("--max-chars", type=int, default=20000)
    ap.add_argument("--wait", type=int, default=2500)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = fetch(a.url, mode=a.mode, max_chars=a.max_chars, wait_ms=a.wait)
    out = r.get("html") if a.mode == "html" and r.get("html") else r.get("text", "")
    if a.json:
        print(json.dumps({"url": a.url, "final_url": r.get("final_url"),
                          "status": r.get("status"), "blocked": r.get("blocked"),
                          "chars": len(out or ""), "text": out}, ensure_ascii=False))
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

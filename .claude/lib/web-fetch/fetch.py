#!/usr/bin/env python3
"""
fetch.py — fetcher resiliente da Aura (navegador headless real + stealth).

Resolve os bloqueios que o WebFetch server-side sofre (403 / 429 / Cloudflare /
login wall soft / conteúdo só-JS) usando Chromium headless com user-agent real,
stealth e espera por conteúdo. É o FALLBACK que as skills usam quando o WebFetch
nativo é barrado (Reddit, Trustpilot, Amazon/Walmart reviews, Meta Ad Library,
PDPs com Cloudflare, etc.).

USO:
    python3 .claude/lib/web-fetch/fetch.py <url> [--mode text|html|reddit|reviews]
                                                 [--max-chars N] [--json] [--wait MS]

  --mode reddit   reescreve pra old.reddit.com (render server-side, amigável)
  --mode reviews  rola a página pra carregar widgets de review lazy (Amazon/Loox/etc)
  --mode html     devolve o HTML renderado (não só o texto)
  --mode text     (default) devolve o texto legível
  --json          imprime {url, final_url, status, blocked, chars, text}
  --max-chars N   limita o texto (default 20000)

SAÍDA: por padrão imprime o texto. Em bloqueio irrecuperável, sai com código 2 e
imprime um status claro (a skill cai pro próximo fallback — ex: pedir paste/MCP).

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
    isso NÃO comparamos resolve(); usamos uma flag de ambiente pra evitar loop.
    """
    try:
        import playwright  # noqa
        return
    except ModuleNotFoundError:
        pass
    if not os.environ.get("AURA_FETCH_BOOTSTRAPPED"):
        for cand in [REPO / ".claude/lib/web-fetch/.venv/bin/python",
                     REPO / "tools/design-clone/.venv/bin/python"]:
            if cand.exists():
                env = {**os.environ, "AURA_FETCH_BOOTSTRAPPED": "1"}
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
const _q=window.navigator.permissions&&window.navigator.permissions.query;
if(_q){window.navigator.permissions.query=(p)=>p&&p.name==='notifications'
  ?Promise.resolve({state:Notification.permission}):_q(p);}
"""

BLOCK_SIGNS = [
    "just a moment", "verify you are human", "enable javascript and cookies",
    "checking your browser", "are you a robot", "captcha", "unusual traffic",
    "access denied", "you've been blocked", "request blocked",
    "attention required", "cf-error", "px-captcha",
]

def looks_blocked(text, title):
    low = (text[:1500] + " " + (title or "")).lower()
    if any(s in low for s in BLOCK_SIGNS):
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

def _targets(url, mode):
    if mode == "reddit":
        path = re.sub(r"https?://(www\.|old\.|np\.|new\.)?reddit\.com", "", url)
        if not path.startswith("/"):
            return [url]
        return [b + path for b in REDLIB] + [url]
    return [url]

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
                    blocked = looks_blocked(text, title) or status in (403, 429, 503)
                    last = {"blocked": blocked, "status": status, "text": text,
                            "final_url": page.url, "html": html if mode == "html" else None,
                            "title": title}
                    if not blocked:
                        browser.close()
                        return last
                    page.wait_for_timeout(2000)       # CF às vezes solta no reload
                    if attempt < retries:
                        page.reload(wait_until="domcontentloaded", timeout=30000)
                except Exception as e:
                    last = {"blocked": True, "status": -1, "text": "",
                            "final_url": target, "error": str(e)[:200]}
                    page.wait_for_timeout(1200)
        browser.close()
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

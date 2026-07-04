#!/usr/bin/env python3
"""
downloader.py — Aura Engine design-clone pipeline (passo 1)

Renderiza uma página de concorrente usando Playwright (Chromium headless com o
mesmo stealth do fetch.py da lib web-fetch), faz scroll automático pra trigger
lazy loading, aguarda network idle, e captura HTML final + CSS computado +
imagens + fontes. Salva tudo numa pasta que o analyzer.py (passo 2) consome —
e, a partir dele, o pattern-extractor.py (modo signals) ou o skeleton-builder
do aura_clone.py (modo clone-and-adapt).

Uso:
    python3 downloader.py <URL> <output_dir>

Exemplo:
    python3 downloader.py https://competitor.com/products/X /tmp/clone-mybrand-1

Exit codes:
    0  DOM completo capturado (page.html + computed-styles + assets)
    1  erro fatal (deps ausentes, URL/path inválido)
    3  fallback: só o screenshot full-page foi salvo (anti-bot/timeout)
    4  fallback impossível (nem screenshot saiu)
    5  fallback capturou uma PÁGINA DE CHALLENGE (Cloudflare/Turnstile) — o
       screenshot NÃO serve pra rota screenshot→visão; use a rota manual
       (extensão SingleFile) via aura_clone.py --from-file

Env:
    AURA_SKIP_IMAGES=1  pula o download de imagens (mais rápido, só signals)
    AURA_UA=<string>    sobrescreve o User-Agent

Dependências:
    pip install playwright beautifulsoup4 requests
    playwright install chromium
"""

from __future__ import annotations

import asyncio
import datetime as _dt
import hashlib
import ipaddress
import json
import logging
import os
import re
import socket
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

# Bootstrap re-exec (mesmo padrão do fetch.py da lib web-fetch): se o python
# atual não tem Playwright e um venv do framework existe, re-executa nele —
# `python3 downloader.py` direto funciona desde que o venv exista. Sem venv,
# segue no python atual e o guard LAZY abaixo cuida da mensagem.
try:
    from _venv_bootstrap import bootstrap as _venv_bootstrap
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _venv_bootstrap import bootstrap as _venv_bootstrap
_venv_bootstrap("playwright")

# Imports pesados são LAZY: validate_url/validate_output_path precisam ser
# importáveis por snapshot.py/aura_clone.py mesmo sem Playwright instalado
# (ex: ingestão --from-file, que não usa browser).
try:
    from playwright.async_api import async_playwright
    from playwright.async_api import TimeoutError as PlaywrightTimeoutError

    _PLAYWRIGHT_IMPORT_ERROR: Optional[str] = None
except ImportError as _exc:  # pragma: no cover - depende do ambiente
    async_playwright = None  # type: ignore[assignment]

    class PlaywrightTimeoutError(Exception):
        """Placeholder quando Playwright não está instalado (nunca é levantada)."""

    _PLAYWRIGHT_IMPORT_ERROR = str(_exc)

try:
    import requests
except ImportError:  # pragma: no cover - depende do ambiente
    requests = None  # type: ignore[assignment]


logger = logging.getLogger("design_clone.downloader")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


VIEWPORT = {"width": 1440, "height": 900}
# Alinhado com o fetch.py da lib web-fetch (Chrome estável). Sobrescrevível via AURA_UA.
USER_AGENT = os.environ.get("AURA_UA") or (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)
SCROLL_STEP_PX = 400
SCROLL_DELAY_MS = 300
# Teto duplo do auto-scroll: páginas com feed infinito (related products,
# collections com lazy append) esticam o scrollHeight mais rápido que os passos
# — sem teto, o laço nunca termina.
MAX_SCROLL_STEPS = 120
MAX_SCROLL_SECONDS = 45
NETWORK_IDLE_TIMEOUT_MS = 15000
PAGE_DEFAULT_TIMEOUT_MS = 60000
NAVIGATION_TIMEOUT_MS = 60000

# Início do processo — usado pra distinguir artefatos deste run de artefatos
# stale de runs anteriores no mesmo output dir.
_PROC_START = time.time()

# Mesmo init-script de stealth do .claude/lib/web-fetch/fetch.py — esconde os
# sinais de automação (navigator.webdriver etc.) que tornam o Chromium headless
# muito mais bloqueável que um browser real.
STEALTH_JS = """
Object.defineProperty(navigator,'webdriver',{get:()=>undefined});
Object.defineProperty(navigator,'languages',{get:()=>['en-US','en']});
Object.defineProperty(navigator,'plugins',{get:()=>[1,2,3,4,5]});
window.chrome={runtime:{}};
if(window.navigator.permissions&&window.navigator.permissions.query){
  const _q=window.navigator.permissions.query.bind(window.navigator.permissions);
  window.navigator.permissions.query=(p)=>p&&p.name==='notifications'
    ?Promise.resolve({state:Notification.permission}):_q(p);}
"""

# Sinais de interstitial anti-bot (título e conteúdo). Se o que capturamos é a
# página de challenge, NÃO é sucesso — o wrapper precisa saber.
CHALLENGE_TITLE_SIGNS = [
    "just a moment",
    "attention required",
    "verify you are human",
    "checking your browser",
    "access denied",
    "un momento",
]
CHALLENGE_CONTENT_SIGNS = [
    "cf-challenge",
    "cf-turnstile",
    "challenge-platform",
    "px-captcha",
    "turnstile",
]


# --------------------------- URL & path validation --------------------------- #

_PRIVATE_V4_NETS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("0.0.0.0/8"),
]
_PRIVATE_V6_NETS = [
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]
_BLOCKED_SCHEMES = {"file", "javascript", "data", "ftp", "gopher", "ws", "wss"}


def _is_private_ip(ip_str: str) -> bool:
    """Retorna True se ip_str cai em um range privado/loopback/link-local."""
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return True  # host inválido == bloquear
    if isinstance(ip, ipaddress.IPv4Address):
        return any(ip in net for net in _PRIVATE_V4_NETS)
    return any(ip in net for net in _PRIVATE_V6_NETS)


def validate_url(url: str) -> str:
    """Valida URL contra SSRF. Aceita apenas http/https + hosts públicos.

    Levanta ValueError com mensagem clara se inválida.

    Limitação conhecida (documentada no README): a validação acontece na URL
    inicial. Redirects seguidos pelo Playwright durante a navegação não são
    revalidados; no download de imagens via requests, cada hop de redirect É
    revalidado (_get_with_validated_redirects).
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL vazia ou inválida")
    parsed = urlparse(url.strip())
    scheme = (parsed.scheme or "").lower()
    if scheme in _BLOCKED_SCHEMES:
        raise ValueError(f"Esquema bloqueado: {scheme!r} (use http:// ou https://)")
    if scheme not in ("http", "https"):
        raise ValueError(f"Esquema inválido: {scheme!r} (use http:// ou https://)")
    host = parsed.hostname
    if not host:
        raise ValueError("URL sem hostname")

    # Resolve DNS e valida todos os endereços retornados
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"DNS falhou para {host!r}: {exc}") from exc

    seen_ips: set[str] = set()
    for info in infos:
        sockaddr = info[4]
        ip_str = sockaddr[0]
        seen_ips.add(ip_str)
        if _is_private_ip(ip_str):
            raise ValueError(
                f"Host {host!r} resolve para IP privado/loopback {ip_str!r} (SSRF bloqueado)"
            )

    if not seen_ips:
        raise ValueError(f"Host {host!r} não resolve para nenhum IP")
    return url.strip()


def _repo_root() -> Path:
    """Raiz do repo Aura (tools/design-clone → 2 níveis acima)."""
    return Path(__file__).resolve().parents[2]


def _path_allowlist() -> list[Path]:
    """Retorna lista de diretórios permitidos para output.

    O workspace é derivado da POSIÇÃO REAL do repo (não assume ~/aura-engine);
    o layout legado ~/aura-engine/workspace continua aceito. O cwd só entra na
    allowlist quando está DENTRO do repo (cwd irrestrito enfraquecia a proteção:
    rodar de $HOME ou / permitia escrever em qualquer lugar abaixo).
    """
    repo_root = _repo_root()
    roots: list[Path] = [
        Path(tempfile.gettempdir()).resolve(),
        (repo_root / "workspace").resolve(),
    ]
    # /tmp é o destino canônico documentado (README/skill 07a) — no macOS ele
    # NÃO é o tempfile.gettempdir() ($TMPDIR aponta pra /var/folders/...).
    tmp_root = Path("/tmp")
    if tmp_root.exists():
        roots.append(tmp_root.resolve())
    home = os.environ.get("HOME")
    if home:
        roots.append((Path(home) / "aura-engine" / "workspace").resolve())
    cwd = Path.cwd().resolve()
    try:
        cwd.relative_to(repo_root)
        roots.append(cwd)
    except ValueError:
        pass
    # Normaliza e dedup
    out: list[Path] = []
    seen: set[str] = set()
    for r in roots:
        key = str(r)
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def validate_output_path(path_str: str) -> Path:
    """Valida que o output path resolve dentro da allowlist (anti path-traversal).

    Retorna o Path resolvido ou levanta ValueError.
    """
    if not path_str or not isinstance(path_str, str):
        raise ValueError("Path de output vazio ou inválido")
    candidate = Path(path_str).expanduser().resolve()
    allowed = _path_allowlist()
    for root in allowed:
        try:
            candidate.relative_to(root)
            return candidate
        except ValueError:
            continue
    allowed_str = ", ".join(str(p) for p in allowed)
    raise ValueError(
        f"Path {candidate!r} fora da allowlist. Permitido em: {allowed_str}"
    )


# ------------------------------- Scraping ----------------------------------- #


async def _launch_stealth(p):
    """Chromium headless com stealth (mesmo init-script do fetch.py da web-fetch)."""
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(
        viewport=VIEWPORT,
        user_agent=USER_AGENT,
        java_script_enabled=True,
        locale="en-US",
    )
    await context.add_init_script(STEALTH_JS)
    page = await context.new_page()
    page.set_default_timeout(PAGE_DEFAULT_TIMEOUT_MS)
    page.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)
    return browser, context, page


async def _looks_like_challenge(page) -> bool:
    """Detecta se a página atual é um interstitial anti-bot (Cloudflare etc.)."""
    try:
        title = ((await page.title()) or "").lower()
    except Exception:  # noqa: BLE001 — página pode estar num estado quebrado
        title = ""
    if any(s in title for s in CHALLENGE_TITLE_SIGNS):
        return True
    try:
        content = (await page.content())[:20000].lower()
    except Exception:  # noqa: BLE001
        return False
    return any(s in content for s in CHALLENGE_CONTENT_SIGNS)


async def auto_scroll(page) -> None:
    """Scroll incremental pra trigger lazy loading, com teto duplo.

    Páginas com feed infinito re-esticam o scrollHeight a cada passo; o teto de
    passos (MAX_SCROLL_STEPS) e de relógio (MAX_SCROLL_SECONDS) garante que o
    laço sempre termina — trunca e segue com o que carregou.
    """
    total_height = await page.evaluate("document.body.scrollHeight")
    current = 0
    steps = 0
    started = time.monotonic()
    while current < total_height:
        if steps >= MAX_SCROLL_STEPS or (time.monotonic() - started) > MAX_SCROLL_SECONDS:
            logger.warning(
                "scroll truncado em %spx após %s passos (página possivelmente infinita)",
                current,
                steps,
            )
            break
        await page.evaluate(f"window.scrollTo(0, {current})")
        await page.wait_for_timeout(SCROLL_DELAY_MS)
        current += SCROLL_STEP_PX
        steps += 1
        new_total = await page.evaluate("document.body.scrollHeight")
        if new_total > total_height:
            total_height = new_total
    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(500)


async def collect_computed_styles(page):
    """Coleta CSS computado de cada elemento visível."""
    js = """
    () => {
      const PROPS = [
        'display','position','width','height','max-width','max-height','min-width','min-height',
        'margin','padding','border','border-radius','box-shadow',
        'background','background-color','background-image','background-size','background-position','background-repeat',
        'color','font-family','font-size','font-weight','font-style','line-height','letter-spacing','text-align','text-transform','text-decoration',
        'flex-direction','flex-wrap','justify-content','align-items','align-content','gap','grid-template-columns','grid-template-rows',
        'opacity','z-index','overflow','transform','transition','cursor'
      ];
      const out = [];
      document.querySelectorAll('*').forEach((el, i) => {
        const cs = window.getComputedStyle(el);
        const styles = {};
        PROPS.forEach(p => { styles[p] = cs.getPropertyValue(p); });
        const tag = el.tagName.toLowerCase();
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) return;
        out.push({
          index: i,
          tag,
          id: el.id || null,
          classes: Array.from(el.classList),
          styles,
          rect: { top: rect.top + window.scrollY, left: rect.left, width: rect.width, height: rect.height }
        });
      });
      return out;
    }
    """
    return await page.evaluate(js)


async def collect_fonts(page):
    """Extrai font-family values únicos."""
    js = """
    () => {
      const fonts = new Set();
      document.querySelectorAll('*').forEach(el => {
        const ff = window.getComputedStyle(el).fontFamily;
        if (ff) fonts.add(ff);
      });
      return Array.from(fonts);
    }
    """
    return await page.evaluate(js)


# Expande shadow roots como <template shadowrootmode> (widgets de review DTC —
# Judge.me/Loox/Okendo — vivem em web components que page.content() não
# serializa) e marca iframes com comentário <!-- aura-iframe: URL --> pra o
# analyzer saber que existe um bloco ali.
SERIALIZE_PREP_JS = """
() => {
  const expand = (root) => {
    root.querySelectorAll('*').forEach((el) => {
      if (el.shadowRoot) {
        expand(el.shadowRoot);
        if (!el.querySelector(':scope > template[data-aura-shadow]')) {
          const tpl = document.createElement('template');
          tpl.setAttribute('shadowrootmode', 'open');
          tpl.setAttribute('data-aura-shadow', '1');
          tpl.innerHTML = el.shadowRoot.innerHTML;
          el.prepend(tpl);
        }
      }
    });
  };
  expand(document);
  let iframes = 0;
  document.querySelectorAll('iframe').forEach((f) => {
    iframes += 1;
    const src = (f.src || f.getAttribute('data-src') || '').replace(/--/g, '- -');
    f.setAttribute('data-aura-iframe-src', src);
    try {
      f.insertAdjacentHTML('beforebegin', '<!-- aura-iframe: ' + src + ' -->');
    } catch (e) {}
  });
  return iframes;
}
"""


async def collect_stylesheets(page, context) -> tuple[list[str], int, int]:
    """Consolida stylesheets. Sheets cross-origin sem CORS lançam SecurityError
    em cssRules e viriam VAZIOS (em loja Shopify, o grosso do CSS vem de
    cdn.shopify.com) — pra esses, baixa o href com o request context do próprio
    browser (cookies + UA da sessão). Retorna (textos, recuperados, perdidos).
    """
    sheets = await page.evaluate(
        "Array.from(document.styleSheets).map(s => ({ href: s.href, cssText: (() => { try { return Array.from(s.cssRules).map(r => r.cssText).join('\\n'); } catch { return ''; } })() }))"
    )
    texts: list[str] = []
    recovered = 0
    lost = 0
    for ss in sheets:
        css_text = ss.get("cssText") or ""
        href = ss.get("href")
        if not css_text and href:
            try:
                validate_url(href)
                resp = await context.request.get(href, timeout=15000)
                if resp.ok:
                    css_text = await resp.text()
                    recovered += 1
                else:
                    lost += 1
                    logger.warning("stylesheet %s respondeu HTTP %s", href, resp.status)
            except Exception as exc:  # noqa: BLE001 — sheet individual não derruba o run
                lost += 1
                logger.warning("stylesheet cross-origin perdido (%s): %s", href, exc)
        if css_text:
            texts.append(f"/* from: {href or 'inline'} */\n{css_text}")
    return texts, recovered, lost


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    """Escrita atômica: escreve em .tmp, renomeia com os.replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp.write_bytes(data)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


_VALID_IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif"}
_CTYPE_EXT = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
    "image/avif": ".avif",
}


def _get_with_validated_redirects(session, url: str, timeout: int = 10, max_redirects: int = 5):
    """GET com redirects manuais: cada hop passa por validate_url (anti-SSRF TOCTOU).

    Um 302 de host público pra host interno/metadata é bloqueado aqui.
    """
    current = url
    for _ in range(max_redirects + 1):
        r = session.get(current, timeout=timeout, allow_redirects=False)
        if r.status_code in (301, 302, 303, 307, 308):
            loc = r.headers.get("Location")
            if not loc:
                return r
            current = urljoin(current, loc)
            validate_url(current)  # levanta ValueError se o redirect for privado
            continue
        return r
    raise ValueError(f"redirects demais para {url}")


def download_image(url: str, output_dir: Path, session) -> Optional[str]:
    """Baixa imagem com write atômico. Retorna path relativo ou None.

    URLs sem extensão (imgix, /_next/image, cdn.shopify sem sufixo) são aceitas:
    a extensão sai do Content-Type da resposta.
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme.startswith("http"):
            return None
        try:
            validate_url(url)
        except ValueError as exc:
            logger.warning("URL de imagem rejeitada (%s): %s", exc, url)
            return None

        ext = os.path.splitext(parsed.path)[1].lower()
        if ext not in _VALID_IMG_EXTS:
            ext = ""  # resolve depois via Content-Type
        h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
        images_dir = Path(output_dir) / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        # Cache: se já baixamos essa URL (qualquer extensão), não rebaixa.
        cached = [p for p in images_dir.glob(f"{h}.*") if p.suffix != ".tmp"]
        if cached and cached[0].stat().st_size > 0:
            return f"images/{cached[0].name}"

        r = _get_with_validated_redirects(session, url, timeout=10)
        if r.status_code == 200 and r.content:
            if not ext:
                ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                ext = _CTYPE_EXT.get(ctype, ".jpg")
            local_name = f"{h}{ext}"
            _atomic_write_bytes(images_dir / local_name, r.content)
            return f"images/{local_name}"
    except Exception as exc:  # noqa: BLE001 — imagem individual não derruba o run
        logger.warning("falha baixando %s: %s", url, exc)
    return None


def extract_image_urls(html: str, base_url: str) -> set[str]:
    """Extrai URLs de imagem (src/data-src de <img>, srcset, background url())."""
    urls: set[str] = set()
    # <img src>/<img data-src> — SEM exigir extensão (imgix, /_next/image,
    # cdn.shopify.com sem sufixo são invisíveis pro filtro por extensão).
    for match in re.finditer(
        r'<img\b[^>]*?\s(?:src|data-src)=["\']([^"\']+)["\']', html, re.IGNORECASE
    ):
        u = match.group(1).strip()
        if u and not u.startswith("data:"):
            urls.add(urljoin(base_url, u))
    # src genérico com extensão de imagem (source/video poster/etc)
    for match in re.finditer(
        r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp|gif|svg|avif))', html, re.IGNORECASE
    ):
        urls.add(urljoin(base_url, match.group(1)))
    for match in re.finditer(r'srcset=["\']([^"\']+)["\']', html, re.IGNORECASE):
        for candidate in match.group(1).split(","):
            url = candidate.strip().split(" ")[0]
            if url and not url.startswith("data:"):
                urls.add(urljoin(base_url, url))
    for match in re.finditer(
        r'url\(["\']?([^"\')\s]+\.(?:jpg|jpeg|png|webp|gif|svg|avif))', html, re.IGNORECASE
    ):
        urls.add(urljoin(base_url, match.group(1)))
    return urls


async def _goto_with_fallback(page, url: str) -> Optional[object]:
    """Navega para `url` usando networkidle como default; fallback load em timeout."""
    try:
        return await page.goto(url, wait_until="networkidle", timeout=NAVIGATION_TIMEOUT_MS)
    except PlaywrightTimeoutError:
        logger.warning("networkidle timeout — tentando wait_until='load'")
        try:
            return await page.goto(url, wait_until="load", timeout=NAVIGATION_TIMEOUT_MS)
        except PlaywrightTimeoutError:
            logger.warning("load timeout — tentando wait_until='domcontentloaded'")
            return await page.goto(
                url, wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT_MS
            )


def _clear_stale_dom_artifacts(output_dir: Path) -> list[str]:
    """Remove artefatos de DOM de runs ANTERIORES (mtime < início do processo).

    Evita estado misto: um retry que caiu em fallback não pode deixar page.html
    velho fazendo o wrapper acreditar que tem DOM fresco (e vice-versa).
    Artefatos gerados NESTE run são preservados.
    """
    removed: list[str] = []
    for name in (
        "page.html",
        "computed-styles.json",
        "styles.css",
        "fonts.json",
        "images.json",
        "sections.json",
        "meta.json",
    ):
        f = output_dir / name
        try:
            if f.exists() and f.stat().st_mtime < _PROC_START:
                f.unlink()
                removed.append(name)
        except OSError:
            pass
    return removed


async def _capture_screenshot_fallback(url: str, output_dir: Path) -> int:
    """Fallback de último recurso: captura só o screenshot full-page da URL.

    Usado quando o scraping de DOM falha (anti-bot/Cloudflare, timeout, 4xx em
    challenge). Não tenta extrair markup/computed-styles — o screenshot serve à
    rota screenshot→visão da 07a (o Claude lê a imagem com visão nativa). Gera um
    `fallback.json` sinalizando que só o screenshot está disponível.

    Antes de fotografar, detecta se a tela é um interstitial de challenge
    ("Just a moment…"/Turnstile) e espera até ~14s pelo auto-resolve. Se o
    challenge persistir, o screenshot é INÚTIL pra rota visão — o fallback.json
    ganha `challenge_detected: true` e o exit code é 5 (não 3).

    Retorna 3 se o screenshot foi salvo, 5 se o screenshot é challenge page,
    4 se nem o screenshot foi possível.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    print("[downloader] entrando em modo fallback (screenshot full-page only)...", file=sys.stderr)
    challenge = False
    try:
        async with async_playwright() as p:
            browser, _context, page = await _launch_stealth(p)
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT_MS)
            except PlaywrightTimeoutError:
                logger.warning("fallback: navegação ainda em timeout, capturando o que houver")
            # Dá um respiro pra challenge/render parcial pintar algo na tela.
            await page.wait_for_timeout(2500)
            challenge = await _looks_like_challenge(page)
            if challenge:
                logger.warning("fallback: challenge anti-bot na tela — esperando auto-resolve...")
                for _ in range(4):
                    await page.wait_for_timeout(3000)
                    challenge = await _looks_like_challenge(page)
                    if not challenge:
                        logger.info("fallback: challenge resolveu sozinho, seguindo")
                        break
            shot_path = output_dir / "fallback-screenshot.png"
            await page.screenshot(path=str(shot_path), full_page=True)
            await browser.close()
    except Exception as exc:  # noqa: BLE001 — fallback de último recurso
        logger.error("fallback de screenshot falhou: %s", exc)
        return 4

    stale_removed = _clear_stale_dom_artifacts(output_dir)
    if stale_removed:
        logger.info("fallback: artefatos stale de run anterior removidos: %s", stale_removed)

    note = (
        "DOM scraping falhou (anti-bot/Cloudflare/timeout). Só o screenshot "
        "full-page está disponível — use a rota screenshot→visão da 07a."
    )
    if challenge:
        note = (
            "DOM scraping falhou E o screenshot capturou a PÁGINA DE CHALLENGE "
            "anti-bot (não a página real). NÃO use este screenshot na rota "
            "screenshot→visão. Rota manual: membro salva a página com a extensão "
            "SingleFile no Chrome dele e ingere via aura_clone.py --from-file."
        )
    (output_dir / "fallback.json").write_text(
        json.dumps(
            {
                "mode": "screenshot_fallback",
                "reason": "dom_scraping_failed",
                "url": url,
                "screenshot": "fallback-screenshot.png",
                "challenge_detected": challenge,
                "stale_artifacts_removed": stale_removed,
                "note": note,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    if challenge:
        print(
            "[downloader] fallback capturou uma página de CHALLENGE (Cloudflare/Turnstile) "
            "— screenshot NÃO serve pra rota visão.",
            file=sys.stderr,
        )
        return 5
    print(f"[downloader] fallback OK — screenshot full-page salvo em {shot_path}", file=sys.stderr)
    print("[downloader] (sem DOM/computed-styles; siga pela rota screenshot→visão)", file=sys.stderr)
    return 3


# --------------------------------- Main ------------------------------------- #


async def run(url: str, output_dir: Path) -> int:
    if async_playwright is None:
        print(
            "ERRO: Playwright não instalado. Rode: pip install playwright && playwright install chromium"
            + (f" (import error: {_PLAYWRIGHT_IMPORT_ERROR})" if _PLAYWRIGHT_IMPORT_ERROR else ""),
            file=sys.stderr,
        )
        return 1

    print(f"[downloader] alvo: {url}")
    print(f"[downloader] saída: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Limpa estado de fallback residual de runs anteriores no mesmo dir — um
    # retry bem-sucedido não pode ser tratado como fallback por causa de um
    # fallback.json velho.
    for name in ("fallback.json", "fallback-screenshot.png"):
        f = output_dir / name
        try:
            if f.exists():
                f.unlink()
        except OSError:
            pass

    skip_images = os.environ.get("AURA_SKIP_IMAGES") == "1"

    async with async_playwright() as p:
        browser, context, page = await _launch_stealth(p)

        print("[downloader] navegando...")
        try:
            response = await _goto_with_fallback(page, url)
        except PlaywrightTimeoutError:
            print(
                "[downloader] URL demorou demais ou é JS-heavy; tentando fallback de screenshot.",
                file=sys.stderr,
            )
            await browser.close()
            return await _capture_screenshot_fallback(url, output_dir)

        if response is not None:
            status = response.status
            # 3xx já foi seguido pelo Playwright; só aborta em 4xx/5xx
            if status >= 400:
                print(
                    f"[downloader] resposta HTTP {status} em {url} — tentando fallback de screenshot.",
                    file=sys.stderr,
                )
                await browser.close()
                return await _capture_screenshot_fallback(url, output_dir)

        try:
            await page.wait_for_load_state("networkidle", timeout=NETWORK_IDLE_TIMEOUT_MS)
        except PlaywrightTimeoutError:
            logger.warning("network-idle timeout, seguindo mesmo assim")

        # Challenge servido com HTTP 200 também existe — detectar antes de
        # gastar scroll/extração num interstitial.
        if await _looks_like_challenge(page):
            print(
                "[downloader] challenge anti-bot detectado na página — tentando fallback de screenshot.",
                file=sys.stderr,
            )
            await browser.close()
            return await _capture_screenshot_fallback(url, output_dir)

        print("[downloader] scroll automático pra trigger lazy loading...")
        await auto_scroll(page)

        print("[downloader] capturando HTML renderizado (com shadow DOM expandido)...")
        try:
            iframe_count = await page.evaluate(SERIALIZE_PREP_JS)
            if iframe_count:
                logger.info("%s iframe(s) marcados com <!-- aura-iframe: ... -->", iframe_count)
        except Exception as exc:  # noqa: BLE001 — prep é best-effort
            logger.warning("expansão de shadow DOM falhou (%s) — seguindo com light DOM", exc)
        html = await page.content()
        (output_dir / "page.html").write_text(html, encoding="utf-8")

        # meta.json: o analyzer precisa da URL de origem pra normalizar srcs
        # relativos ao casar com images.json (que guarda URLs absolutas).
        (output_dir / "meta.json").write_text(
            json.dumps(
                {"url": url, "fetched_at": _dt.datetime.now(_dt.timezone.utc).isoformat()},
                indent=2,
            ),
            encoding="utf-8",
        )

        print("[downloader] capturando screenshot...")
        try:
            await page.screenshot(
                path=str(output_dir / "viewport-screenshot.png"), full_page=True
            )
        except PlaywrightTimeoutError:
            logger.warning("screenshot timeout — pulando")

        print("[downloader] extraindo CSS computado...")
        computed = await collect_computed_styles(page)
        (output_dir / "computed-styles.json").write_text(
            json.dumps(computed, indent=2), encoding="utf-8"
        )

        print("[downloader] extraindo fontes...")
        fonts = await collect_fonts(page)
        (output_dir / "fonts.json").write_text(json.dumps(fonts, indent=2), encoding="utf-8")

        print("[downloader] coletando stylesheets...")
        stylesheet_texts, css_recovered, css_lost = await collect_stylesheets(page, context)
        if css_recovered or css_lost:
            print(
                f"[downloader] stylesheets cross-origin: {css_recovered} recuperado(s) "
                f"via fetch, {css_lost} perdido(s)"
            )
        (output_dir / "styles.css").write_text(
            "\n\n".join(stylesheet_texts), encoding="utf-8"
        )

        # Cookies do contexto → sessão de download de imagens (CDNs com hotlink
        # protection/URLs assinadas retornam 403 pra sessão anônima).
        browser_cookies = await context.cookies()
        await browser.close()

    if skip_images:
        print("[downloader] AURA_SKIP_IMAGES=1 — pulando download de imagens")
        (output_dir / "images.json").write_text("{}", encoding="utf-8")
        saved: dict[str, str] = {}
    elif requests is None:
        logger.warning("requests não instalado — pulando download de imagens")
        (output_dir / "images.json").write_text("{}", encoding="utf-8")
        saved = {}
    else:
        print("[downloader] baixando imagens...")
        image_urls = extract_image_urls(html, url)
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT, "Referer": url})
        for c in browser_cookies:
            try:
                session.cookies.set(
                    c.get("name"), c.get("value"),
                    domain=c.get("domain"), path=c.get("path", "/"),
                )
            except Exception:  # noqa: BLE001 — cookie individual não derruba o run
                pass
        saved = {}
        for img_url in image_urls:
            local = download_image(img_url, output_dir, session)
            if local:
                saved[img_url] = local
        (output_dir / "images.json").write_text(json.dumps(saved, indent=2), encoding="utf-8")

    print(f"[downloader] pronto. {len(saved)} imagens salvas em {output_dir}/images/")
    print("[downloader] arquivos gerados:")
    print("  - page.html (HTML renderizado, shadow DOM expandido, iframes marcados)")
    print("  - meta.json (URL de origem + timestamp)")
    print("  - styles.css (stylesheets consolidados, cross-origin recuperados via fetch)")
    print("  - computed-styles.json (CSS computado por elemento)")
    print("  - fonts.json (font families detectadas)")
    print(f"  - images/ ({len(saved)} arquivos)")
    print("  - images.json (mapping URL original → path local)")
    print("  - viewport-screenshot.png (referência visual)")
    return 0


async def main() -> int:
    if len(sys.argv) < 3:
        print("Uso: python3 downloader.py <URL> <output_dir>", file=sys.stderr)
        return 1
    try:
        url = validate_url(sys.argv[1])
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    try:
        output_dir = validate_output_path(sys.argv[2])
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    if async_playwright is None:
        print(
            "ERRO: Playwright não instalado. Rode: pip install playwright && playwright install chromium",
            file=sys.stderr,
        )
        return 1
    try:
        return await run(url, output_dir)
    except PlaywrightTimeoutError:
        print(
            "[downloader] URL demorou demais ou é JS-heavy; tentando fallback de screenshot.",
            file=sys.stderr,
        )
        return await _capture_screenshot_fallback(url, output_dir)
    except Exception as exc:  # noqa: BLE001 — CLI surface
        logger.error("falha fatal: %s — tentando fallback de screenshot.", exc)
        try:
            return await _capture_screenshot_fallback(url, output_dir)
        except Exception:  # noqa: BLE001
            return 1


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\n[downloader] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)

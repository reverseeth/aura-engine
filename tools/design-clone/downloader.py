#!/usr/bin/env python3
"""
downloader.py — Aura Engine design-clone pipeline (step 1 of 3)

Renderiza uma página de concorrente usando Playwright, faz scroll automático pra
trigger lazy loading, aguarda network idle, e captura HTML final + CSS
computado + imagens + fontes. Salva tudo numa pasta temporária que o
analyzer.py (step 2) vai consumir.

Uso:
    python3 downloader.py <URL> <output_dir>

Exemplo:
    python3 downloader.py https://competitor.com/products/X /tmp/clone-mybrand-1

Dependências:
    pip install playwright beautifulsoup4 requests
    playwright install chromium
"""

from __future__ import annotations

import asyncio
import hashlib
import ipaddress
import json
import logging
import os
import re
import socket
import sys
import tempfile
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

try:
    from playwright.async_api import async_playwright
    from playwright.async_api import TimeoutError as PlaywrightTimeoutError
except ImportError:
    print(
        "ERRO: Playwright não instalado. Rode: pip install playwright && playwright install chromium",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    import requests
except ImportError:
    print("ERRO: requests não instalado. Rode: pip install requests", file=sys.stderr)
    sys.exit(1)


logger = logging.getLogger("design_clone.downloader")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


VIEWPORT = {"width": 1440, "height": 900}
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
SCROLL_STEP_PX = 400
SCROLL_DELAY_MS = 300
NETWORK_IDLE_TIMEOUT_MS = 15000
PAGE_DEFAULT_TIMEOUT_MS = 60000
NAVIGATION_TIMEOUT_MS = 60000


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


def _path_allowlist() -> list[Path]:
    """Retorna lista de diretórios permitidos para output."""
    roots: list[Path] = [Path(tempfile.gettempdir()).resolve(), Path.cwd().resolve()]
    home = os.environ.get("HOME")
    if home:
        workspace = Path(home) / "aura-engine" / "workspace"
        roots.append(workspace.resolve())
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


async def auto_scroll(page) -> None:
    """Scroll incremental pra trigger lazy loading de imagens e seções."""
    total_height = await page.evaluate("document.body.scrollHeight")
    current = 0
    while current < total_height:
        await page.evaluate(f"window.scrollTo(0, {current})")
        await page.wait_for_timeout(SCROLL_DELAY_MS)
        current += SCROLL_STEP_PX
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


def download_image(url: str, output_dir: Path, session: requests.Session) -> Optional[str]:
    """Baixa imagem com write atômico anti race-condition. Retorna path relativo ou None."""
    try:
        parsed = urlparse(url)
        if not parsed.scheme.startswith("http"):
            return None
        try:
            validate_url(url)
        except ValueError as exc:
            logger.warning("URL de imagem rejeitada (%s): %s", exc, url)
            return None

        ext = os.path.splitext(parsed.path)[1].lower() or ".jpg"
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif"}:
            ext = ".jpg"
        h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
        local_name = f"{h}{ext}"
        local_path = Path(output_dir) / "images" / local_name
        local_path.parent.mkdir(parents=True, exist_ok=True)

        # Reserva o nome pra evitar race entre checar-existe e gravar.
        local_path.touch(exist_ok=True)
        # Se já tinha conteúdo (>0), considera cacheado e não rebaixa.
        try:
            if local_path.stat().st_size > 0:
                return f"images/{local_name}"
        except OSError:
            pass

        r = session.get(url, timeout=10)
        if r.status_code == 200 and r.content:
            _atomic_write_bytes(local_path, r.content)
            return f"images/{local_name}"
        # Download falhou — remove o arquivo vazio reservado
        try:
            if local_path.exists() and local_path.stat().st_size == 0:
                local_path.unlink()
        except OSError:
            pass
    except Exception as exc:
        logger.warning("falha baixando %s: %s", url, exc)
    return None


def extract_image_urls(html: str, base_url: str) -> set[str]:
    """Extrai URLs de imagem (src, srcset, background url())."""
    urls: set[str] = set()
    for match in re.finditer(
        r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp|gif|svg|avif))', html, re.IGNORECASE
    ):
        urls.add(urljoin(base_url, match.group(1)))
    for match in re.finditer(r'srcset=["\']([^"\']+)["\']', html, re.IGNORECASE):
        for candidate in match.group(1).split(","):
            url = candidate.strip().split(" ")[0]
            if url:
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


# --------------------------------- Main ------------------------------------- #


async def run(url: str, output_dir: Path) -> int:
    print(f"[downloader] alvo: {url}")
    print(f"[downloader] saída: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=VIEWPORT,
            user_agent=USER_AGENT,
            java_script_enabled=True,
        )
        page = await context.new_page()
        page.set_default_timeout(PAGE_DEFAULT_TIMEOUT_MS)
        page.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)

        print("[downloader] navegando...")
        try:
            response = await _goto_with_fallback(page, url)
        except PlaywrightTimeoutError:
            print(
                "[downloader] URL demorou demais ou é JS-heavy; tente outra.",
                file=sys.stderr,
            )
            await browser.close()
            return 2

        if response is not None:
            status = response.status
            # 3xx já foi seguido pelo Playwright; só aborta em 4xx/5xx
            if status >= 400:
                print(
                    f"[downloader] abortando: resposta HTTP {status} em {url}",
                    file=sys.stderr,
                )
                await browser.close()
                return 3

        try:
            await page.wait_for_load_state("networkidle", timeout=NETWORK_IDLE_TIMEOUT_MS)
        except PlaywrightTimeoutError:
            logger.warning("network-idle timeout, seguindo mesmo assim")

        print("[downloader] scroll automático pra trigger lazy loading...")
        await auto_scroll(page)

        print("[downloader] capturando HTML renderizado...")
        html = await page.content()
        (output_dir / "page.html").write_text(html, encoding="utf-8")

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
        stylesheet_texts: list[str] = []
        for ss in await page.evaluate(
            "Array.from(document.styleSheets).map(s => ({ href: s.href, cssText: (() => { try { return Array.from(s.cssRules).map(r => r.cssText).join('\\n'); } catch { return ''; } })() }))"
        ):
            if ss.get("cssText"):
                stylesheet_texts.append(
                    f"/* from: {ss.get('href') or 'inline'} */\n{ss['cssText']}"
                )
        (output_dir / "styles.css").write_text(
            "\n\n".join(stylesheet_texts), encoding="utf-8"
        )

        await browser.close()

    print("[downloader] baixando imagens...")
    image_urls = extract_image_urls(html, url)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    saved: dict[str, str] = {}
    for img_url in image_urls:
        local = download_image(img_url, output_dir, session)
        if local:
            saved[img_url] = local
    (output_dir / "images.json").write_text(json.dumps(saved, indent=2), encoding="utf-8")

    print(f"[downloader] pronto. {len(saved)} imagens salvas em {output_dir}/images/")
    print("[downloader] arquivos gerados:")
    print("  - page.html (HTML renderizado)")
    print("  - styles.css (stylesheets consolidados)")
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
    try:
        return await run(url, output_dir)
    except PlaywrightTimeoutError:
        print(
            "[downloader] URL demorou demais ou é JS-heavy; tente outra.",
            file=sys.stderr,
        )
        return 2
    except Exception as exc:  # noqa: BLE001 — CLI surface
        logger.error("falha fatal: %s", exc)
        return 1


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\n[downloader] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)

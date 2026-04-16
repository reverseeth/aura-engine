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

import asyncio
import json
import os
import sys
import re
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERRO: Playwright não instalado. Rode: pip install playwright && playwright install chromium", file=sys.stderr)
    sys.exit(1)

try:
    import requests
except ImportError:
    print("ERRO: requests não instalado. Rode: pip install requests", file=sys.stderr)
    sys.exit(1)


VIEWPORT = {"width": 1440, "height": 900}
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
SCROLL_STEP_PX = 400
SCROLL_DELAY_MS = 300
NETWORK_IDLE_TIMEOUT_MS = 15000


async def auto_scroll(page):
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
    """Coleta CSS computado de cada elemento visível (limitado a propriedades que importam pra visual clone)."""
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
        if (rect.width === 0 || rect.height === 0) return; // skip hidden
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
    """Extrai fontes detectadas no documento (font-family values únicos)."""
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


def download_image(url, output_dir, session):
    """Baixa uma imagem e retorna o caminho local relativo. Retorna None se falhar."""
    try:
        parsed = urlparse(url)
        if not parsed.scheme.startswith("http"):
            return None
        # Hash-based filename pra evitar colisões e paths muito longos
        ext = os.path.splitext(parsed.path)[1].lower() or ".jpg"
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif"}:
            ext = ".jpg"
        h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
        local_name = f"{h}{ext}"
        local_path = Path(output_dir) / "images" / local_name
        local_path.parent.mkdir(parents=True, exist_ok=True)
        if local_path.exists():
            return f"images/{local_name}"
        r = session.get(url, timeout=10)
        if r.status_code == 200:
            local_path.write_bytes(r.content)
            return f"images/{local_name}"
    except Exception as e:
        print(f"  [warn] falha baixando {url}: {e}", file=sys.stderr)
    return None


def extract_image_urls(html, base_url):
    """Extrai todas as URLs de imagem do HTML (src, srcset, background-image inline)."""
    urls = set()
    for match in re.finditer(r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp|gif|svg|avif))', html, re.IGNORECASE):
        urls.add(urljoin(base_url, match.group(1)))
    for match in re.finditer(r'srcset=["\']([^"\']+)["\']', html, re.IGNORECASE):
        for candidate in match.group(1).split(","):
            url = candidate.strip().split(" ")[0]
            if url:
                urls.add(urljoin(base_url, url))
    for match in re.finditer(r'url\(["\']?([^"\')\s]+\.(?:jpg|jpeg|png|webp|gif|svg|avif))', html, re.IGNORECASE):
        urls.add(urljoin(base_url, match.group(1)))
    return urls


async def main():
    if len(sys.argv) < 3:
        print("Uso: python3 downloader.py <URL> <output_dir>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    output_dir = Path(sys.argv[2]).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[downloader] alvo: {url}")
    print(f"[downloader] saída: {output_dir}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport=VIEWPORT, user_agent=USER_AGENT)
        page = await context.new_page()

        print("[downloader] navegando...")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        try:
            await page.wait_for_load_state("networkidle", timeout=NETWORK_IDLE_TIMEOUT_MS)
        except Exception:
            print("  [warn] network-idle timeout, seguindo mesmo assim", file=sys.stderr)

        print("[downloader] scroll automático pra trigger lazy loading...")
        await auto_scroll(page)

        print("[downloader] capturando HTML renderizado...")
        html = await page.content()
        (output_dir / "page.html").write_text(html, encoding="utf-8")

        print("[downloader] capturando screenshot...")
        await page.screenshot(path=str(output_dir / "viewport-screenshot.png"), full_page=True)

        print("[downloader] extraindo CSS computado...")
        computed = await collect_computed_styles(page)
        (output_dir / "computed-styles.json").write_text(json.dumps(computed, indent=2), encoding="utf-8")

        print("[downloader] extraindo fontes...")
        fonts = await collect_fonts(page)
        (output_dir / "fonts.json").write_text(json.dumps(fonts, indent=2), encoding="utf-8")

        print("[downloader] coletando stylesheets...")
        stylesheet_texts = []
        for ss in await page.evaluate(
            "Array.from(document.styleSheets).map(s => ({ href: s.href, cssText: (() => { try { return Array.from(s.cssRules).map(r => r.cssText).join('\\n'); } catch { return ''; } })() }))"
        ):
            if ss.get("cssText"):
                stylesheet_texts.append(f"/* from: {ss.get('href') or 'inline'} */\n{ss['cssText']}")
        (output_dir / "styles.css").write_text("\n\n".join(stylesheet_texts), encoding="utf-8")

        await browser.close()

    print("[downloader] baixando imagens...")
    image_urls = extract_image_urls(html, url)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    saved = {}
    for img_url in image_urls:
        local = download_image(img_url, output_dir, session)
        if local:
            saved[img_url] = local
    (output_dir / "images.json").write_text(json.dumps(saved, indent=2), encoding="utf-8")

    print(f"[downloader] pronto. {len(saved)} imagens salvas em {output_dir}/images/")
    print(f"[downloader] arquivos gerados:")
    print(f"  - page.html (HTML renderizado)")
    print(f"  - styles.css (stylesheets consolidados)")
    print(f"  - computed-styles.json (CSS computado por elemento)")
    print(f"  - fonts.json (font families detectadas)")
    print(f"  - images/ ({len(saved)} arquivos)")
    print(f"  - images.json (mapping URL original → path local)")
    print(f"  - viewport-screenshot.png (referência visual)")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
verify_page.py — verificação estrutural da página publicada (desktop + mobile).

Abre a URL real da loja num Chromium headless e falha se algo estrutural quebrou:
overflow horizontal (a página "anda de lado" no celular) ou seção presente mas com
altura 0 (a section renderizou vazia). Também reporta a altura total, os erros de
JavaScript do console (filtrando o ruído de trackers de terceiros) e salva
screenshot full-page + um recorte por seção pra conferência visual.

USO:
    verify_page.py <url> [--sections-attr ATTR] [--shots-dir DIR]
                         [--desktop-only | --mobile-only]

  --sections-attr  atributo que marca as seções a medir (default: data-aura-section).
                   Cada elemento com esse atributo vira uma linha do relatório e um
                   screenshot próprio.
  --shots-dir      pasta dos screenshots (default: ./theme-verify-shots)

Viewports: desktop 1440x1000 e mobile 390x844 (os dois por padrão).
Exit: 0 ok · 1 overflow ou seção com altura 0 · 2 página não carregou ·
      3 Playwright ausente (setup: .claude/lib/web-fetch/README.md).
"""
import sys, os, re, argparse
from pathlib import Path


def _bootstrap():
    try:
        import playwright  # noqa: F401
        return
    except ImportError:
        pass
    if os.environ.get("AURA_TV_BOOT"):
        sys.stderr.write("Playwright ausente no venv — setup: .claude/lib/web-fetch/README.md\n")
        sys.exit(3)
    repo = Path(__file__).resolve().parents[3]
    for venv in (repo / ".claude/lib/web-fetch/.venv", repo / "tools/design-clone/.venv"):
        py = venv / "bin" / "python3"
        if py.exists():
            os.environ["AURA_TV_BOOT"] = "1"
            os.execv(str(py), [str(py)] + sys.argv)
    sys.stderr.write("Playwright ausente — setup: .claude/lib/web-fetch/README.md\n")
    sys.exit(3)


_bootstrap()
from playwright.sync_api import sync_playwright, Error as PWError  # noqa: E402

UA_DESKTOP = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
UA_MOBILE = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1")

VIEWPORTS = {
    "desktop": dict(viewport={"width": 1440, "height": 1000}, user_agent=UA_DESKTOP),
    "mobile": dict(viewport={"width": 390, "height": 844}, user_agent=UA_MOBILE,
                   device_scale_factor=3, is_mobile=True, has_touch=True),
}

# erros vindos de trackers/apps de terceiros — não são problema do tema
CONSOLE_NOISE = ("facebook", "googletagmanager", "google-analytics", "doubleclick",
                 "klaviyo", "tiktok", "pinterest", "hotjar", "clarity.ms", "monorail",
                 "web-pixel", "favicon", "ERR_BLOCKED_BY_CLIENT")


def scroll_through(page):
    # rolagem progressiva: dispara lazy-load e animações de reveal antes de medir
    page.evaluate("""async () => {
        const step = Math.max(window.innerHeight * 0.8, 200);
        for (let y = 0; y <= document.documentElement.scrollHeight; y += step) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 200));
        }
        window.scrollTo(0, 0);
        await new Promise(r => setTimeout(r, 500));
    }""")


def slugify(name, fallback):
    s = re.sub(r"[^a-z0-9-]+", "-", (name or "").lower()).strip("-")[:40]
    return s or fallback


def check_viewport(browser, label, url, attr, shots_dir):
    vp = VIEWPORTS[label]
    ctx = browser.new_context(**vp)
    page = ctx.new_page()

    errors = []

    def on_console(msg):
        if msg.type == "error" and not any(n in msg.text for n in CONSOLE_NOISE):
            errors.append(msg.text)

    page.on("console", on_console)
    page.on("pageerror", lambda e: None if any(n in str(e) for n in CONSOLE_NOISE)
            else errors.append(str(e)))

    page.goto(url, wait_until="load", timeout=60000)
    page.evaluate("document.querySelector('newsletter-popup')?.remove()")
    scroll_through(page)

    overflow = page.evaluate(
        "() => { const d = document.documentElement;"
        " return Math.max(d.scrollWidth, document.body.scrollWidth) - d.clientWidth; }")
    height = page.evaluate("() => document.documentElement.scrollHeight")

    failures = []
    if overflow > 0:
        failures.append(f"{label}: overflow horizontal de {overflow}px")

    w, h = vp["viewport"]["width"], vp["viewport"]["height"]
    print(f"\n== {label} ({w}x{h}) ==")
    print(f"altura total: {height}px")
    print(f"overflow horizontal: {overflow}px {'✅' if overflow == 0 else '❌'}")

    page.screenshot(path=str(shots_dir / f"{label}-full.png"), full_page=True)

    sections = page.locator(f"[{attr}]")
    n = sections.count()
    print(f"seções ({attr}): {n}")
    if n == 0:
        print(f"  ⚠️ nenhum elemento com {attr} — nada a medir por seção")
    for i in range(n):
        el = sections.nth(i)
        name = el.get_attribute(attr) or ""
        slug = slugify(name, f"sec-{i:02d}")
        box = el.bounding_box()
        sec_h = round(box["height"]) if box else 0
        print(f"  {'✅' if sec_h > 0 else '❌'} {(name or slug):<36} {sec_h}px")
        if sec_h == 0:
            failures.append(f"{label}: seção '{name or slug}' com altura 0")
        else:
            try:
                el.screenshot(path=str(shots_dir / f"{label}-{i:02d}-{slug}.png"))
            except PWError:
                pass  # elemento saiu do DOM entre a medição e o screenshot

    if errors:
        print(f"console: {len(errors)} erro(s)")
        for e in errors[:10]:
            print(f"  ⚠️ {e[:200]}")
    else:
        print("console: 0 erros")

    ctx.close()
    return failures


def main():
    ap = argparse.ArgumentParser(description="verificação estrutural da página publicada")
    ap.add_argument("url")
    ap.add_argument("--sections-attr", default="data-aura-section")
    ap.add_argument("--shots-dir", default="./theme-verify-shots")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--desktop-only", action="store_true")
    g.add_argument("--mobile-only", action="store_true")
    args = ap.parse_args()

    labels = ["desktop", "mobile"]
    if args.desktop_only:
        labels = ["desktop"]
    if args.mobile_only:
        labels = ["mobile"]

    shots_dir = Path(args.shots_dir)
    shots_dir.mkdir(parents=True, exist_ok=True)

    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for label in labels:
            try:
                failures += check_viewport(browser, label, args.url,
                                           args.sections_attr, shots_dir)
            except PWError as e:
                sys.stderr.write(f"{label}: página não carregou — {e}\n")
                browser.close()
                sys.exit(2)
        browser.close()

    print(f"\nscreenshots em: {shots_dir.resolve()}")
    if failures:
        print("\nFALHOU:")
        for f in failures:
            print(f"  ❌ {f}")
        sys.exit(1)
    print("\n✅ página passou (sem overflow, todas as seções com altura > 0)")


if __name__ == "__main__":
    main()

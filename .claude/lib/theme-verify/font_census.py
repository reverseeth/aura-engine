#!/usr/bin/env python3
"""
font_census.py — censo de fonte da página publicada.

Percorre TODOS os elementos visíveis que têm texto direto e conta os que NÃO estão
na fonte esperada (via getComputedStyle().fontFamily). Pega o caso clássico: a
fonte custom carregou no hero, mas um botão do tema, um widget ou um bloco de app
ficou na fonte default do sistema.

USO:
    font_census.py <url> --font "Nome da Fonte" [--mobile] [--open-selector SEL]

  --font           primeira família esperada no fontFamily (obrigatório)
  --mobile         viewport de celular (390x844) em vez de desktop
  --open-selector  clica nesse seletor antes do censo — conteúdo dentro de
                   drawer/modal fechado não entra no censo sem isso

O censo espera document.fonts.ready (a fonte custom terminar de carregar) antes de
medir, pra não acusar falso infrator durante o swap.

Exit: 0 tudo na fonte · 1 há infrator · 2 página não carregou / seletor não achado ·
      3 Playwright ausente (setup: .claude/lib/web-fetch/README.md).
"""
import sys, os, argparse
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

DESKTOP = dict(viewport={"width": 1440, "height": 1000}, user_agent=UA_DESKTOP)
MOBILE = dict(viewport={"width": 390, "height": 844}, user_agent=UA_MOBILE,
              device_scale_factor=3, is_mobile=True, has_touch=True)

CENSUS_JS = """(expected) => {
    const norm = s => s.replace(/["']/g, "").trim().toLowerCase();
    const want = norm(expected);
    let checked = 0, offCount = 0;
    const bad = new Map();
    for (const el of document.querySelectorAll("body *")) {
        if (el.namespaceURI !== "http://www.w3.org/1999/xhtml") continue;
        if (["SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE", "IFRAME"].includes(el.tagName)) continue;
        const direct = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
        if (!direct) continue;
        const cs = getComputedStyle(el);
        if (cs.display === "none" || cs.visibility === "hidden") continue;
        if (!el.getClientRects().length) continue;
        checked++;
        if (norm(cs.fontFamily).startsWith(want)) continue;
        offCount++;
        const sel = el.tagName.toLowerCase()
            + (el.classList.length ? "." + [...el.classList].join(".") : "");
        if (!bad.has(sel)) bad.set(sel, { font: cs.fontFamily.split(",")[0].trim(), count: 0 });
        bad.get(sel).count++;
    }
    return { checked, offCount,
             offenders: [...bad.entries()].map(([sel, v]) => ({ sel, ...v })) };
}"""


def scroll_through(page):
    page.evaluate("""async () => {
        const step = Math.max(window.innerHeight * 0.8, 200);
        for (let y = 0; y <= document.documentElement.scrollHeight; y += step) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 200));
        }
        window.scrollTo(0, 0);
        await new Promise(r => setTimeout(r, 500));
    }""")


def main():
    ap = argparse.ArgumentParser(description="censo de fonte da página publicada")
    ap.add_argument("url")
    ap.add_argument("--font", required=True,
                    help='primeira família esperada, ex: "Nome da Fonte"')
    ap.add_argument("--mobile", action="store_true")
    ap.add_argument("--open-selector",
                    help="clica antes do censo (abre drawer/modal)")
    args = ap.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(**(MOBILE if args.mobile else DESKTOP))
        page = ctx.new_page()
        try:
            page.goto(args.url, wait_until="load", timeout=60000)
        except PWError as e:
            sys.stderr.write(f"página não carregou — {e}\n")
            sys.exit(2)
        scroll_through(page)
        page.evaluate("() => document.fonts.ready")
        if args.open_selector:
            try:
                page.locator(args.open_selector).first.click(timeout=5000)
                page.wait_for_timeout(800)  # animação do drawer/modal
            except PWError:
                sys.stderr.write(f"--open-selector não encontrou/clicou: "
                                 f"{args.open_selector}\n")
                sys.exit(2)
        result = page.evaluate(CENSUS_JS, args.font)
        browser.close()

    print(f"elementos com texto verificados: {result['checked']}")
    print(f'fora da fonte "{args.font}": {result["offCount"]}')
    if result["offCount"]:
        print("\ninfratores (até 20 seletores):")
        for o in sorted(result["offenders"], key=lambda o: -o["count"])[:20]:
            print(f"  ❌ {o['sel']}  ({o['count']}x, fonte: {o['font']})")
        sys.exit(1)
    print("✅ todos os elementos visíveis com texto estão na fonte esperada")


if __name__ == "__main__":
    main()

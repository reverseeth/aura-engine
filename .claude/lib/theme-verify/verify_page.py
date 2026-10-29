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
                         [--json-out QA.json [--plan PAGE-PLAN.json]
                          [--legal LEGAL.json] [--geodiff GEODIFF.json]]
                         [--dump-computed COMPUTED.json]

  Sem --json-out (perfil loja): o comportamento de sempre, usado pelo page-build
  na loja real. Com --json-out (perfil design): mede o page.html da page-design
  em 390/768/1440 com os itens de "QA: o que bloqueia" (docs/designs/page-design-2.md)
  e grava o qa-metrics.json. --dump-computed grava cor/fonte computadas por seção
  (entrada do `tokens.py --diff-live`) e funciona nos dois perfis.

  --sections-attr  atributo que marca as seções a medir (default: data-aura-section).
                   Cada elemento com esse atributo vira uma linha do relatório e um
                   screenshot próprio.
  --shots-dir      pasta dos screenshots (default: ./theme-verify-shots)

Viewports: desktop 1440x1000 e mobile 390x844 (os dois por padrão).
Exit: 0 ok · 1 overflow ou seção com altura 0 (perfil design: item bloqueante
      em fail) · 2 página não carregou · 3 Playwright ausente (setup: .claude/lib/web-fetch/README.md).
"""
import sys, os, re, argparse, json, hashlib
from urllib.parse import urlparse, unquote
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


# ---------------------------------------------------------------- perfil design

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "design-presets"))
from palette_engine import rgb_to_hex, contrast_ratio  # noqa: E402

DESIGN_WIDTHS = {390: "mobile", 768: "tablet", 1440: "desktop"}
VIEWPORTS["tablet"] = dict(viewport={"width": 768, "height": 1024}, user_agent=UA_MOBILE,
                           device_scale_factor=2, is_mobile=True, has_touch=True)

# Uma passada no browser devolve os dados crus de uma largura; os limites ficam no Python.
MEASURE_JS = r"""(attr) => {
  const vis = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const ownText = el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  const rgba = c => (c.match(/[\d.]+/g) || []).map(Number);
  const bgOf = el => { for (let e = el; e; e = e.parentElement) {
      const s = getComputedStyle(e), c = rgba(s.backgroundColor);
      if (c.length >= 3 && (c.length < 4 || c[3] === 1)) return c.slice(0, 3);
      if (s.backgroundImage !== 'none') return null; }
    return [255, 255, 255]; };
  const root = document.querySelector('main') || document.body;
  const skip = new Set(['HEADER', 'FOOTER', 'NAV', 'STYLE', 'LINK', 'SCRIPT', 'NOSCRIPT']);
  const texts = [...document.body.querySelectorAll('*')].filter(e => vis(e) && ownText(e));
  const contrast = texts.map(e => { const s = getComputedStyle(e);
    return {fg: rgba(s.color).slice(0, 3), bg: bgOf(e), size: parseFloat(s.fontSize),
            bold: parseInt(s.fontWeight) >= 700, tag: e.tagName.toLowerCase()}; });
  const lines = [...document.querySelectorAll('p')].filter(vis).map(p => {
    const s = getComputedStyle(p), lh = parseFloat(s.lineHeight) || parseFloat(s.fontSize) * 1.2;
    const r = p.getBoundingClientRect();
    const sec = p.closest('[data-aura-section]');
    const n = Math.max(1, Math.round(r.height / lh));
    // caracteres reais por linha (texto ÷ linhas): a estimativa por largura errava com a fonte
    return {lines: n, chars: p.textContent.replace(/\s+/g, ' ').trim().length / n,
            where: sec ? sec.getAttribute('data-aura-section') : p.className || 'p'}; });
  const h1 = document.querySelector('h1');
  let h1Lines = 0;
  if (h1) { const s = getComputedStyle(h1);
    h1Lines = Math.round(h1.getBoundingClientRect().height /
      (parseFloat(s.lineHeight) || parseFloat(s.fontSize) * 1.2)); }
  const vw = document.documentElement.clientWidth;
  const margins = [...document.querySelectorAll(`[${attr}]`)].map(sec => {
    const c = [...sec.querySelectorAll('*')].find(e => vis(e) && (ownText(e) || e.tagName === 'IMG'));
    if (!c) return null; const r = c.closest(`[${attr}] > *`)?.getBoundingClientRect() || c.getBoundingClientRect();
    return {id: sec.getAttribute(attr), diff: Math.abs(r.left - (vw - r.right))}; }).filter(Boolean);
  const content = [...document.body.querySelectorAll('img,video,svg,picture')].filter(vis)
    .concat(texts).map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.bottom + scrollY]; })
    .sort((a, b) => a[0] - b[0]);
  let gap = 0, end = 0; for (const [t, b] of content) { if (t > end) gap = Math.max(gap, t - end); end = Math.max(end, b); }
  return {
    scripts: [...document.querySelectorAll('script')].filter(s => s.type !== 'application/ld+json').length,
    unmarked: [...root.children].filter(e => !skip.has(e.tagName) && !e.hasAttribute(attr)
                && e.getBoundingClientRect().height > 0).map(e => e.tagName.toLowerCase()),
    ids: [...document.querySelectorAll(`[${attr}]`)].map(e => e.getAttribute(attr)),
    zero: [...document.querySelectorAll(`[${attr}]`)].filter(e => e.getBoundingClientRect().height === 0)
                .map(e => e.getAttribute(attr)),
    broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.currentSrc || i.src),
    overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - document.documentElement.clientWidth,
    contrast, sizes: [...new Set(texts.map(e => getComputedStyle(e).fontSize))],
    gradients: [...document.body.querySelectorAll('*')].filter(e => getComputedStyle(e).backgroundImage.includes('gradient')).length,
    lines, h1Lines, margins, emptyGap: gap, vh: innerHeight,
    // file:// não entra no Resource Timing do Chromium: soma as imagens do DOM também
    resources: [...new Set([...performance.getEntriesByType('resource').map(r => r.name),
                            ...[...document.images].map(i => i.currentSrc || i.src)])],
  };
}"""

COMPUTED_JS = r"""(attr) => [...document.querySelectorAll(`[${attr}]`)].map(sec => {
  const cs = e => e ? getComputedStyle(e) : null;
  const pick = sel => cs(sec.querySelector(sel));
  const btn = pick('a[class*=btn],a[class*=cta],button,[class*=button]');
  let bg = null; for (let e = sec; e; e = e.parentElement) { const c = getComputedStyle(e).backgroundColor;
    if (!/rgba\(.*,\s*0\)$/.test(c) && c !== 'transparent') { bg = c; break; } }
  return {section: sec.getAttribute(attr), text: cs(sec).color, background: bg,
          button: btn ? btn.backgroundColor : null,
          fonts: Object.fromEntries(['h1', 'h2', 'p'].map(t => [t, pick(t)?.fontFamily || null]))};
})"""


def _rgb_hex(c):
    return rgb_to_hex(c[:3]) if c and len(c) >= 3 else None


def _item(id_, value, limit, ok, blocking, width=None, detail="", status=None):
    return {"id": id_, "status": status or ("pass" if ok else ("fail" if blocking else "warn")),
            "blocking": blocking, "value": value, "limit": limit, "width": width, "detail": detail}


def _local_path(url):
    u = urlparse(url)
    return Path(unquote(u.path)) if u.scheme == "file" else None


def _html_css_kb(url):
    path = _local_path(url)
    if not path or not path.exists():
        return None
    html = path.read_text(encoding="utf-8", errors="replace")
    size = len(html.encode()) - sum(len(m.encode()) for m in re.findall(
        r"<style[^>]*data-aura-fonts[^>]*>.*?</style>", html, flags=re.S | re.I))
    for href in re.findall(r"<link[^>]+rel=[\"']?stylesheet[^>]*href=[\"']([^\"']+)", html, flags=re.I):
        css = (path.parent / href).resolve()
        if css.exists():
            size += css.stat().st_size
    return round(size / 1024, 1)


def _total_kb(url, resources):
    path = _local_path(url)
    total = path.stat().st_size if path and path.exists() else 0
    for r in resources:
        rp = _local_path(r)
        if rp and rp.exists():
            total += rp.stat().st_size
    return round(total / 1024, 1)


def measure_design(browser, url, attr, shots_dir):
    raw = {}
    for w, label in DESIGN_WIDTHS.items():
        # movimento reduzido: entrada no scroll (animation-timeline: view()) deixaria fora da tela
        # tudo em opacity 0 na captura de página inteira, e o revisor veria faixas em branco
        ctx = browser.new_context(**VIEWPORTS[label], reduced_motion="reduce")
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text)
                if m.type == "error" and not any(n in m.text for n in CONSOLE_NOISE) else None)
        page.goto(url, wait_until="load", timeout=60000)
        scroll_through(page)
        raw[w] = page.evaluate(MEASURE_JS, attr)
        raw[w]["console"] = errors
        page.screenshot(path=str(shots_dir / f"{label}-full.png"), full_page=True)
        if label != "tablet":
            save_tiles(page, shots_dir, label)
        ctx.close()
    return raw


TILE_HEIGHT = {"desktop": 1800, "mobile": 1600}


def save_tiles(page, shots_dir, label):
    """Fatias de cima para baixo (`<label>-NN.png`): a captura inteira de uma página longa
    passa de 10 mil px e, lida por visão, fica pequena demais para o revisor julgar."""
    width, height = page.evaluate("[innerWidth, document.documentElement.scrollHeight]")
    step = TILE_HEIGHT[label]
    for n, top in enumerate(range(0, height, step), 1):
        page.screenshot(path=str(shots_dir / f"{label}-{n:02d}.png"), full_page=True,
                        clip={"x": 0, "y": top, "width": width, "height": min(step, height - top)})


def design_items(raw, url, plan_ids, legal, geodiff, build_mode):
    d = raw[1440]
    items = [
        _item("script_tags", d["scripts"], 0, d["scripts"] == 0, True, 1440),
        _item("section_markers", len(d["unmarked"]), 0, not d["unmarked"], True, 1440,
              ", ".join(d["unmarked"])),
    ]
    if plan_ids is None:
        items.append(_item("section_ids_match_plan", None, "igual", True, True, 1440, "sem --plan", "skip"))
    else:
        items.append(_item("section_ids_match_plan", d["ids"], plan_ids, d["ids"] == plan_ids, True, 1440))
    for w in (390, 768, 1440):
        items.append(_item("horizontal_overflow", raw[w]["overflow"], 0, raw[w]["overflow"] <= 0, True, w))
    for w in (390, 1440):
        items.append(_item("section_height_zero", len(raw[w]["zero"]), 0, not raw[w]["zero"], True, w,
                           ", ".join(raw[w]["zero"])))
    items.append(_item("broken_images", len(d["broken"]), 0, not d["broken"], True, 1440,
                       ", ".join(d["broken"][:5])))
    kb = _html_css_kb(url)
    items.append(_item("html_css_kb", kb, 150, kb is None or kb <= 150, True,
                       status="skip" if kb is None else None))
    if build_mode != "reference":
        items.append(_item("legal_check", None, "pass", True, True, detail="modo direção", status="skip"))
    elif legal is None:
        items.append(_item("legal_check", None, "pass", False, True, detail="modo referência sem --legal"))
    else:
        items.append(_item("legal_check", len(legal.get("findings", [])), "pass", bool(legal.get("pass")), True))
    total = _total_kb(url, d["resources"])
    items.append(_item("page_total_kb", total, 1536, total <= 1536, False))
    for w in (390, 1440):
        low = []
        for c in raw[w]["contrast"]:
            if not c["bg"]:
                continue
            ratio = contrast_ratio(_rgb_hex(c["fg"]), _rgb_hex(c["bg"]))
            need = 3.0 if c["size"] >= 24 or (c["bold"] and c["size"] >= 18.66) else 4.5
            if ratio < need:
                low.append(f"{c['tag']} {ratio:.2f}")
        items.append(_item("contrast", len(low), 0, not low, False, w, ", ".join(low[:5])))
    items.append(_item("font_sizes_distinct", len(d["sizes"]), 7, len(d["sizes"]) <= 7, False, 1440))
    items.append(_item("gradients", d["gradients"], 3, d["gradients"] <= 3, False, 1440))
    bad = [l for l in d["lines"] if l["lines"] > 1 and not 45 <= l["chars"] <= 75]
    items.append(_item("line_length", len(bad), "45-75", not bad, False, 1440,
                       ", ".join(f"{l.get('where')} {round(l['chars'])}" for l in bad[:5])))
    m = raw[390]["h1Lines"]
    items.append(_item("headline_lines", m, 2, m <= 2, False, 390, "h1 com %d linhas em 390" % m if m > 2 else ""))
    off = [x["id"] for x in d["margins"] if x["diff"] > 8]
    items.append(_item("equal_side_margins", len(off), 8, not off, False, 1440, ", ".join(off)))
    gap = round(d["emptyGap"])
    items.append(_item("empty_bands", gap, round(0.6 * d["vh"]), gap <= 0.6 * d["vh"], False, 1440))
    if geodiff is None:
        items.append(_item("geodiff", None, 70, True, False, detail="sem --geodiff", status="skip"))
    else:
        s = geodiff.get("min_score", 0)
        items.append(_item("geodiff", s, 70, s >= 70, False))
    items.append(_item("console_errors", len(d["console"]), 0, not d["console"], False, 1440))
    return items


def run_design(args, browser, shots_dir):
    plan = json.loads(Path(args.plan).read_text()) if args.plan else {}
    plan_ids = plan.get("section_order") if args.plan else None
    legal = json.loads(Path(args.legal).read_text()) if args.legal else None
    geodiff = json.loads(Path(args.geodiff).read_text()) if args.geodiff else None
    raw = measure_design(browser, args.url, args.sections_attr, shots_dir)
    items = design_items(raw, args.url, plan_ids, legal, geodiff, plan.get("build_mode"))
    path = _local_path(args.url)
    out = {"version": 1, "page": args.url,
           "page_sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path and path.exists() else None,
           "widths": list(DESIGN_WIDTHS), "items": items,
           "blocking_fail": any(i["blocking"] and i["status"] == "fail" for i in items)}
    Path(args.json_out).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    for i in items:
        mark = {"pass": "✅", "warn": "⚠️", "fail": "❌", "skip": "·"}[i["status"]]
        print(f"{mark} {i['id']:<24} {i['value']!s:<10} limite {i['limit']!s:<8} {i['width'] or ''}")
    return out["blocking_fail"]


def dump_computed(browser, url, attr, out):
    ctx = browser.new_context(**VIEWPORTS["desktop"])
    page = ctx.new_page()
    page.goto(url, wait_until="load", timeout=60000)
    data = page.evaluate(COMPUTED_JS, attr)
    ctx.close()
    Path(out).write_text(json.dumps({"version": 1, "page": url, "sections": data},
                                    indent=2, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description="verificação estrutural da página publicada")
    ap.add_argument("url")
    ap.add_argument("--sections-attr", default="data-aura-section")
    ap.add_argument("--shots-dir", default="./theme-verify-shots")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--desktop-only", action="store_true")
    g.add_argument("--mobile-only", action="store_true")
    ap.add_argument("--json-out", help="perfil design: grava o qa-metrics.json")
    ap.add_argument("--plan", help="page-plan.json, para section_ids_match_plan")
    ap.add_argument("--legal", help="saída do legal_check.py")
    ap.add_argument("--geodiff", help="saída do geodiff.py")
    ap.add_argument("--dump-computed", help="grava cor/fonte computadas por seção")
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
        if args.dump_computed:
            dump_computed(browser, args.url, args.sections_attr, args.dump_computed)
        if args.json_out:
            try:
                failed = run_design(args, browser, shots_dir)
            except PWError as e:
                sys.stderr.write(f"página não carregou — {e}\n")
                sys.exit(2)
            browser.close()
            print(f"\nqa-metrics em: {Path(args.json_out).resolve()}")
            sys.exit(1 if failed else 0)
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

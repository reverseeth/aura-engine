#!/usr/bin/env python3
"""
motion_check.py — amostragem de animação da página publicada (marquee/loop).

Amostra a posição horizontal REAL do elemento animado (componente m41 da matriz de
transform, lida com DOMMatrix) a cada ~60ms e verifica se o movimento é contínuo:
velocidade estável, emenda do loop (wrap) do tamanho certo, zero saltos.

O caso que este script existe pra pegar: animação definida em PORCENTAGEM da
largura do container + imagens lazy sem dimensão reservada. Com cache quente e
rede rápida as imagens chegam antes do primeiro frame, a largura nunca muda e a
medição sai limpa; em rede lenta as imagens chegam NO MEIO da animação, a largura
da cópia cresce e a emenda salta na tela. Por isso o --throttle (rede 3G lenta +
cache frio, via o protocolo de automação do Chrome) faz parte do teste.

USO:
    motion_check.py <url> --selector SEL [--copy-selector SEL] [--seconds N]
                          [--throttle] [--mobile]

  --selector       o elemento que recebe o transform (obrigatório)
  --copy-selector  filho cuja largura equivale a 1 cópia do loop — habilita a
                   validação do tamanho da emenda e o rastreio de reflow (a
                   largura mudando durante o carregamento)
  --seconds        duração da amostragem (default 15)
  --throttle       emula 3G lenta: 300ms de latência, ~400 kbps de download,
                   cache desligado (o cenário real de celular)

Exit: 0 movimento limpo · 1 anomalia (salto, reflow, elemento parado) ·
      2 página/elemento não carregou · 3 Playwright ausente
      (setup: .claude/lib/web-fetch/README.md).
"""
import sys, os, time, statistics, argparse
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

SAMPLER_JS = """(a) => {
    const el = document.querySelector(a.sel);
    const copy = a.copySel ? document.querySelector(a.copySel) : null;
    window.__mv = { samples: [], timer: null };
    window.__mv.timer = setInterval(() => {
        const m = new DOMMatrix(getComputedStyle(el).transform);
        window.__mv.samples.push([
            performance.now(), m.m41,
            copy ? copy.getBoundingClientRect().width : -1,
        ]);
    }, a.interval);
}"""


def report(samples):
    widths = [w for (_, _, w) in samples if w > 0]
    w_min = min(widths) if widths else None
    w_max = max(widths) if widths else None
    # sem --copy-selector, qualquer salto > 100px conta como wrap
    wrap_thr = (w_min * 0.5) if widths else 100.0

    deltas = []
    for a, b in zip(samples, samples[1:]):
        dt = (b[0] - a[0]) / 1000.0
        if dt > 0:
            deltas.append((b[0], b[1] - a[1], dt, b[2]))

    small = [dx for (_, dx, _, _) in deltas if abs(dx) < wrap_thr]
    direction = -1 if sum(small) < 0 else 1
    speeds = [abs(dx) / dt for (_, dx, dt, _) in deltas if abs(dx) < wrap_thr]
    v_med = statistics.median(speeds) if speeds else 0.0

    wraps, anomalies = [], []
    travel = dur = 0.0
    for (t, dx, dt, w) in deltas:
        if dx * -direction > wrap_thr:  # salto contra o sentido do movimento = emenda
            wraps.append(abs(dx))
            if w > 0 and abs(abs(dx) - w) > 0.15 * w:
                anomalies.append((t, f"emenda de {abs(dx):.0f}px com cópia de {w:.0f}px"))
        elif abs(dx) > max(3 * v_med * dt, 12):
            anomalies.append((t, f"salto de {dx:+.0f}px fora do padrão "
                                 f"(~{v_med * dt:.1f}px esperado no intervalo)"))
        else:
            travel += abs(dx)
            dur += dt

    if widths and (w_max - w_min) > 0.02 * w_min:
        anomalies.append((samples[0][0],
                          f"largura da cópia variou {w_min:.0f}→{w_max:.0f}px durante o "
                          "carregamento (reflow — imagem lazy sem dimensão reservada?)"))
    if travel < 1 and not wraps:
        anomalies.append((samples[0][0], "elemento não se moveu durante a amostragem"))

    total = (samples[-1][0] - samples[0][0]) / 1000.0
    speed = travel / dur if dur else 0.0
    print(f"amostras: {len(samples)} em {total:.1f}s")
    print(f"velocidade média: {speed:.1f} px/s "
          f"(sentido: {'esquerda' if direction < 0 else 'direita'})")
    print(f"wraps (emenda do loop): {len(wraps)}"
          + (f" — tamanho médio {statistics.mean(wraps):.0f}px" if wraps else ""))
    if w_min is not None:
        stable = (w_max - w_min) <= 0.02 * w_min
        print(f"largura da cópia: min {w_min:.0f}px / max {w_max:.0f}px "
              + ("(estável ✅)" if stable else "(MUDOU durante o carregamento ❌)"))

    if anomalies:
        print(f"\nanomalias: {len(anomalies)}")
        for (t, msg) in anomalies[:10]:
            print(f"  ❌ t={t / 1000:.1f}s  {msg}")
        return 1
    print("anomalias: 0")
    print("✅ movimento limpo")
    return 0


def main():
    ap = argparse.ArgumentParser(description="amostragem de animação (marquee/loop)")
    ap.add_argument("url")
    ap.add_argument("--selector", required=True, help="elemento que recebe o transform")
    ap.add_argument("--copy-selector", help="filho cuja largura = 1 cópia do loop")
    ap.add_argument("--seconds", type=float, default=15)
    ap.add_argument("--throttle", action="store_true",
                    help="3G lenta: 300ms latência, ~400 kbps down, cache frio")
    ap.add_argument("--mobile", action="store_true")
    args = ap.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(**(MOBILE if args.mobile else DESKTOP))
        page = ctx.new_page()
        if args.throttle:
            cdp = ctx.new_cdp_session(page)
            cdp.send("Network.enable")
            cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
            cdp.send("Network.emulateNetworkConditions", {
                "offline": False, "latency": 300,
                "downloadThroughput": 50_000,  # bytes/s ≈ 400 kbps
                "uploadThroughput": 25_000,
            })
        try:
            # domcontentloaded (não "load"): a amostragem tem que começar ENQUANTO
            # as imagens ainda estão chegando — é aí que o bug aparece
            page.goto(args.url, wait_until="domcontentloaded", timeout=120000)
            page.wait_for_selector(args.selector, state="attached", timeout=60000)
        except PWError as e:
            sys.stderr.write(f"página/elemento não carregou — {e}\n")
            sys.exit(2)

        if args.copy_selector and not page.evaluate(
                "(s) => !!document.querySelector(s)", args.copy_selector):
            sys.stderr.write(f"--copy-selector não encontrou nada: {args.copy_selector}\n")
            sys.exit(2)

        page.evaluate(SAMPLER_JS, {"sel": args.selector,
                                   "copySel": args.copy_selector, "interval": 60})
        time.sleep(args.seconds)
        samples = page.evaluate(
            "() => { clearInterval(window.__mv.timer); return window.__mv.samples; }")
        browser.close()

    if len(samples) < 10:
        sys.stderr.write(f"amostragem insuficiente ({len(samples)} amostras)\n")
        sys.exit(2)
    sys.exit(report(samples))


if __name__ == "__main__":
    main()

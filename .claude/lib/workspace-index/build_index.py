#!/usr/bin/env python3
"""
build_index.py — gera o painel ABRIR-AQUI.html de um produto do Aura Engine.

É a PORTA DE ENTRADA do membro: lista cada fase (com nome amigável), mostra o que
já foi feito vs pendente, a barra de progresso, e o PRÓXIMO PASSO. Cada relatório
concluído vira um link "Abrir". Mesmo design "Editorial Intelligence" (off-white,
liquid glass, tipografia Geist, topbar flutuante, animações) dos relatórios.

Toda skill, ao terminar de salvar seus outputs, roda:
    python3 .claude/lib/workspace-index/build_index.py <produto-slug>

O idioma vem de manifest.report_language (default pt-BR). O painel reflete o estado
real escaneando as subpastas de fase (0X-<stem>/<stem>.html; legado relatorio.html).
"""
import json, sys, re, html, datetime
from pathlib import Path

# Fases na ordem lógica de execução. folder = subpasta de fase; o relatório humano é
# <stem>.html, onde stem = nome da pasta sem o prefixo numérico (ex: 02-market-research/
# market-research.html), com fallback legado relatorio.html (produtos antigos).
# Último campo = tag do card: None (core), "post" (pós-launch), "two" (skill de 2 fases:
# Fase A pré-launch + Fase B pós-launch — 05 bônus e 13 retenção). As skills "two" mantêm
# a posição do card aqui; a Fase A delas entra como próximo passo pela lógica condicional
# no build() (depois da 07d), não pela posição na lista.
PHASES = [
    ("00", "00-setup",              {"pt-BR": "Setup",                 "en": "Setup"},                  None, None),
    ("01", "01-product-research",   {"pt-BR": "Pesquisa de produto",   "en": "Product research"},       "product research", None),
    ("01b","sourcing",              {"pt-BR": "Fornecedor (sourcing)", "en": "Sourcing"},               "sourcing", "opt"),
    ("02", "02-market-research",    {"pt-BR": "Pesquisa de mercado",   "en": "Market research"},        "market research", None),
    ("03", "03-competitor-analysis",{"pt-BR": "Análise de concorrência","en": "Competitor analysis"},   "competitor analysis", None),
    ("04", "04-offer-builder",      {"pt-BR": "Oferta",                "en": "Offer"},                  "offer", None),
    ("06", "06-copy-engine",        {"pt-BR": "Copy",                  "en": "Copy"},                   "copy", None),
    ("07", "07-page",               {"pt-BR": "Página (loja)",         "en": "Page (storefront)"},      "page", None),
    ("07c","07c-tracking-setup",    {"pt-BR": "Tracking (pixel + CAPI)","en": "Tracking (pixel + CAPI)"},"tracking", None),
    ("07d","07d-checkout-aov",      {"pt-BR": "Checkout & AOV",        "en": "Checkout & AOV"},         "checkout", None),
    ("08", "08-creative-engine",    {"pt-BR": "Criativos",             "en": "Creatives"},              "creatives", None),
    ("07e","07e-agentic-readiness", {"pt-BR": "Visibilidade pra agentes de AI","en": "Agentic readiness (AI visibility)"}, "agentic readiness", None),
    ("09", "09-consistency-audit",  {"pt-BR": "Auditoria de consistência","en": "Consistency audit"},   "audit", None),
    ("10", "10-ad-strategy",        {"pt-BR": "Estratégia de ads",     "en": "Ad strategy"},            "ad strategy", None),
    ("11", "11-ad-analysis",        {"pt-BR": "Análise de ads",        "en": "Ad analysis"},            "ad analysis", None),
    ("12", "12-scale-engine",       {"pt-BR": "Escala",                "en": "Scale"},                  "scale", None),
    ("13", "13-retention-engine",   {"pt-BR": "Retenção (email/SMS)",  "en": "Retention (email/SMS)"},  "retention", "two"),
    ("05", "05-bonus-delivery",     {"pt-BR": "Entrega de bônus",      "en": "Bonus delivery"},         "bonus delivery", "two"),
    ("14", "14-content-recycler",   {"pt-BR": "Reciclagem de conteúdo","en": "Content recycler"},       "recycle", "post"),
]

# Relatório alternativo: só a fase 07 difere do padrão <folder>/<stem>.html — a página
# humana é 07-page/page-report.html (escrita pela 07b APÓS o build/deploy; nome legado
# 07-page.html). NÃO incluímos design/page.html aqui de propósito: a fase "Página" só
# conta como concluída quando a página foi de fato construída (07b), não quando só o
# design (07a) foi aprovado. Pra folders listados aqui, SOMENTE esta lista vale (o
# candidato padrão <stem>.html/relatorio.html NÃO conta — evita que um relatório de
# design marque a fase como concluída antes do deploy).
ALT_REPORT = {
    "07-page":  ["07-page/page-report.html", "07-page/07-page.html"],
}

# Fases cujo done vem SÓ do manifest (skills_completed), nunca da existência do relatório:
# a 01b salva sourcing.html já no checkpoint de cotação enviada (status "quoting"), mas a
# fase só fecha quando a cotação fecha (status "closed" → manifest). O link "Abrir
# relatório" continua aparecendo; só o badge Concluído espera o manifest.
MANIFEST_ONLY = {"sourcing"}

LOGO_SVG = ('<svg viewBox="0 0 1789.33 925.59" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            '<path d="M0,925.59h923.43l306.37-306.37h105.11c15.83,0,28.65,12.83,28.65,28.65v277.72h270.77'
            'v-308.53l-241.89,1.93c-15.91.13-28.88-12.74-28.88-28.65V0h-387.05c-33.3,0-65.23,13.24-88.76,36.8L0,925.59Z" fill="#14161A"/></svg>')

T = {
  "pt-BR": dict(title="Seu painel", sub="Tudo que a Aura já criou pra <b>{p}</b>. Abra qualquer relatório, ou siga pro próximo passo.",
                eyebrow="Aura Engine / painel", panel="Painel",
                done="Concluído", pending="Pendente", open="Abrir relatório", next="Próximo passo",
                next_post="Próximo passo (pós-launch)",
                run='Diga <code>{cmd}</code> pra rodar.', progress="{d} de {t} fases concluídas",
                alldone="Tudo pronto. Sua máquina está montada.", post="Pós-launch",
                two_phase="2 fases",
                optional="Opcional",
                order_note="As fases aparecem na ordem em que rodam — o número é o ID fixo de cada skill.",
                bonus_a="Entrega de bônus — Fase A (assets + GWP)",
                retention_a="Retenção — Fase A (flows de recuperação)"),
  "en": dict(title="Your dashboard", sub="Everything Aura has built for <b>{p}</b>. Open any report, or move to the next step.",
                eyebrow="Aura Engine / dashboard", panel="Dashboard",
                done="Done", pending="Pending", open="Open report", next="Next step",
                next_post="Next step (post-launch)",
                run='Say <code>{cmd}</code> to run it.', progress="{d} of {t} phases done",
                alldone="All set. Your machine is built.", post="Post-launch",
                two_phase="2 phases",
                optional="Optional",
                order_note="Phases appear in the order they run — the number is each skill's fixed ID.",
                bonus_a="Bonus delivery — Phase A (assets + GWP)",
                retention_a="Retention — Phase A (recovery flows)"),
}

def offer_has_bonuses(root):
    """True se a oferta (04) definiu bônus — só nesse caso o painel cobra a Fase A da 05."""
    p = root / "04-offer-builder" / "dados.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return False
    return bool(data.get("bonuses"))

def build(slug):
    root = Path.cwd() / "workspace" / slug
    if not root.exists():
        # fallback: talvez rodando de outro cwd
        root = Path(__file__).resolve().parents[3] / "workspace" / slug
    mani = {}
    mp = root / "manifest.json"
    if mp.exists():
        try: mani = json.loads(mp.read_text(encoding="utf-8"))
        except Exception: mani = {}
    lang = mani.get("report_language") or "pt-BR"
    if lang not in T: lang = "pt-BR"
    tr = T[lang]
    pname = html.escape(mani.get("product_name") or slug)
    completed = set(mani.get("skills_completed") or [])

    def report_link(folder):
        if folder in ALT_REPORT:                     # fase 07: só conta via 07b (build)
            cand = ALT_REPORT[folder]
        else:
            stem = re.sub(r"^\d+[a-z]?-", "", folder)
            cand = [f"{folder}/{stem}.html",         # esquema novo (nome descritivo)
                    f"{folder}/relatorio.html"]      # legado (produtos antigos)
        for c in cand:
            if (root / c).exists():
                return c
        return None

    rows, done_count, total = [], 0, 0
    next_phase = None   # primeira fase core pendente
    post_next = None    # primeira fase pós-launch/2-fases pendente (fallback quando o core acabou)
    done_by_sid = {}
    for sid, folder, names, cmd, tag in PHASES:
        if sid == "00":  # setup não vira card de relatório
            continue
        total += 1
        # 07a (design) pronta mas 07b (build) pendente → o trigger certo é "build page";
        # "page" re-executaria o design (07a), que já foi aprovado.
        if sid == "07" and "07a-page-design" in completed and "07b-page-build" not in completed:
            cmd = "build page"
        link = report_link(folder)
        # done = report artifact exists, OR manifest marks this phase complete.
        # match skills_completed entries as "<sid>-..." to avoid the 07/07c/07d prefix
        # collision (a bare startswith(sid) would let 07c mark the 07-page phase done).
        # fase 07 (folder 07-page) é construída pela 07b: marca done quando 07b consta
        # (a 07a só desenha; tracking/checkout 07c/07d são fases próprias e não contam aqui).
        is_done = ((link is not None and folder not in MANIFEST_ONLY)
                   or any(s == folder or s.startswith(sid + "-") for s in completed)
                   or (sid == "07" and "07b-page-build" in completed))
        done_by_sid[sid] = is_done
        if is_done: done_count += 1
        elif next_phase is None and tag is None and cmd:
            next_phase = (names[lang], cmd)
        elif post_next is None and tag and tag != "opt" and cmd:
            # fases "opt" (opcionais, ex: sourcing) nunca viram sugestão de próximo passo
            post_next = (names[lang], cmd)
        name = html.escape(names[lang])
        badge = (f'<span class="b-done">{tr["done"]}</span>' if is_done else f'<span class="b-pending">{tr["pending"]}</span>')
        post_tag = (f'<span class="b-two">{tr["two_phase"]}</span>' if tag == "two"
                    else (f'<span class="b-post">{tr["post"]}</span>' if tag == "post"
                          else (f'<span class="b-two">{tr["optional"]}</span>' if tag == "opt" else '')))
        # fase concluída via manifest mas sem HTML: sem call-to-action (mostrar "diga X
        # pra rodar" junto do badge Concluído seria contraditório pro membro)
        action = (f'<a class="open" href="{html.escape(link)}">{tr["open"]}<span aria-hidden="true">→</span></a>' if link
                  else ('' if is_done
                        else (f'<span class="run">{tr["run"].format(cmd=html.escape(cmd))}</span>' if cmd else '')))
        rows.append(f'''<div class="phase {'is-done' if is_done else 'is-pending'} reveal">
          <div class="ph-num">{sid}</div>
          <div class="ph-body"><div class="ph-name">{name} {post_tag}</div>{action}</div>
          <div class="ph-badge">{badge}</div></div>''')

    pct = round(done_count / total * 100) if total else 0
    year = datetime.date.today().year
    # Fase A das skills de 2 fases (05 bônus, 13 retenção) entra como próximo passo assim
    # que a 07d fecha: operador de elite não lança tráfego pago sem os bônus prometidos na
    # PDP existirem, nem sem abandoned cart + post-purchase flow (a receita mais barata que
    # existe — infraestrutura de launch, não campanha de email).
    fase_a = None
    if done_by_sid.get("07d"):
        if offer_has_bonuses(root) and not done_by_sid.get("05"):
            fase_a = (tr["bonus_a"], "bonus delivery")
        elif not done_by_sid.get("13"):
            fase_a = (tr["retention_a"], "retention")
    # próximo passo: Fase A condicional primeiro; depois core pendente; se o core acabou mas
    # faltam fases pós-launch, mostra a primeira delas (não deixa o card sumir); só "tudo
    # pronto" quando tudo acabou.
    next_html = ''
    if fase_a:
        chosen, label = fase_a, tr["next"]
    elif next_phase:
        chosen, label = next_phase, tr["next"]
    elif post_next and done_count < total:
        chosen, label = post_next, tr["next_post"]
    else:
        chosen = label = None
    if chosen:
        next_html = f'''<div class="next reveal"><div class="next-label">{label}</div>
          <div class="next-name">{html.escape(chosen[0])}</div>
          <div class="next-cmd">{tr["run"].format(cmd=html.escape(chosen[1]))}</div></div>'''
    elif done_count == total:
        next_html = f'<div class="next next--done reveal"><div class="next-name">{tr["alldone"]}</div></div>'

    return f'''<!doctype html><html lang="{lang}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f4f5f7">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; script-src 'self' 'unsafe-inline';">
<title>{pname} — Aura</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{
  --bg:#F4F5F7;--ink:#14161A;--ink-2:#3A424A;--muted:#5C656D;--faint:#656E76;
  --line:rgba(20,24,30,.10);--line-strong:rgba(20,24,30,.17);--line-hot:rgba(20,24,30,.30);
  --green:#0E9F6E;--green-ink:#0B7A53;
  --font:"Geist","Helvetica Neue",Helvetica,Arial,sans-serif;--mono:"Geist Mono","SFMono-Regular",Consolas,monospace;
  --ease:cubic-bezier(.23,1,.32,1);--radius:18px;
  --glass:linear-gradient(145deg,rgba(255,255,255,.86) 0%,rgba(255,255,255,.60) 42%,rgba(255,255,255,.78) 100%);
  --card-solid:linear-gradient(145deg,rgba(255,255,255,.97),rgba(255,255,255,.93));
  --shadow-card:inset 0 1px 0 rgba(255,255,255,.9),0 1px 2px rgba(24,30,40,.05),0 20px 48px -28px rgba(24,34,48,.22),0 4px 12px -8px rgba(24,34,48,.12);
  --shadow-lift:inset 0 1px 0 rgba(255,255,255,.95),0 2px 4px rgba(24,30,40,.06),0 34px 80px -40px rgba(24,34,48,.30),0 10px 26px -14px rgba(24,34,48,.18);
  --mx:50vw;--my:20vh;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{background:var(--bg);-webkit-text-size-adjust:100%}}
body{{min-height:100vh;overflow-x:hidden;font-family:var(--font);font-weight:300;color:var(--ink-2);line-height:1.6;letter-spacing:-.014em;
-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
background:radial-gradient(900px 560px at 86% -6%,rgba(120,140,165,.10),transparent 66%),radial-gradient(760px 520px at 2% 34%,rgba(150,160,172,.08),transparent 70%),linear-gradient(180deg,#F8F9FA 0%,var(--bg) 30%,#F1F2F4 100%)}}
body::before{{content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;opacity:.5;
background-image:linear-gradient(rgba(20,24,30,.028) 1px,transparent 1px),linear-gradient(90deg,rgba(20,24,30,.028) 1px,transparent 1px);
background-size:54px 54px;mask-image:linear-gradient(to bottom,black,transparent 88%)}}
body::after{{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(480px circle at var(--mx) var(--my),rgba(90,110,135,.05),transparent 70%)}}
::selection{{background:#14161A;color:#F5F6F7}}
a{{color:inherit;text-decoration:none;-webkit-tap-highlight-color:transparent}}
svg{{display:block}}
:focus-visible{{outline:2px solid rgba(20,24,30,.55);outline-offset:3px;border-radius:4px}}
.skip-link{{position:fixed;top:10px;left:10px;z-index:200;transform:translateY(-160%);padding:10px 14px;border-radius:10px;background:var(--ink);color:#F5F6F7;font-size:13px;transition:transform .18s}}
.skip-link:focus{{transform:none}}

.topbar{{position:fixed;z-index:120;top:max(14px,env(safe-area-inset-top));left:50%;transform:translateX(-50%);
display:grid;grid-template-columns:1fr auto;align-items:center;width:min(calc(100% - 32px),760px);min-height:56px;padding:8px 12px 8px 16px;
border:1px solid var(--line);border-radius:18px;background:linear-gradient(135deg,rgba(255,255,255,.88),rgba(255,255,255,.72));
box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 16px 44px -22px rgba(24,34,48,.28),0 2px 8px -4px rgba(24,34,48,.14);
-webkit-backdrop-filter:blur(20px) saturate(1.3);backdrop-filter:blur(20px) saturate(1.3)}}
.brand{{display:inline-flex;align-items:center;gap:12px;font-size:12.5px;font-weight:500;letter-spacing:.11em;text-transform:uppercase;color:var(--ink)}}
.brand svg{{height:21px;width:auto}}
.system-state{{justify-self:end;padding:0 14px;min-height:38px;display:inline-flex;align-items:center;border:1px solid var(--line);border-radius:11px;background:rgba(255,255,255,.6);color:var(--muted);font-family:var(--mono);font-size:9.5px;letter-spacing:.11em;text-transform:uppercase}}
@media(max-width:520px){{.system-state{{display:none}}}}

.wrap{{width:min(100% - 40px,760px);margin:0 auto;padding-top:calc(env(safe-area-inset-top,0px) + clamp(104px,13vh,150px))}}
@media(max-width:620px){{.wrap{{width:min(100% - 28px,760px)}}}}
.eyebrow{{display:flex;align-items:center;gap:12px;margin:0 0 24px;color:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.15em;text-transform:uppercase}}
.eyebrow::before{{content:"";width:24px;height:1px;background:var(--line-hot)}}
h1{{color:var(--ink);font-size:clamp(44px,7vw,72px);font-weight:300;line-height:.92;letter-spacing:-.05em;text-wrap:balance}}
.sub{{max-width:56ch;margin:26px 0 0;color:var(--muted);font-size:clamp(16px,1.5vw,18px);font-weight:300;line-height:1.55;letter-spacing:-.018em}}
.sub b{{color:var(--ink-2);font-weight:500}}

.progress{{position:relative;isolation:isolate;overflow:hidden;margin:clamp(40px,7vw,64px) 0 22px;padding:28px 30px;border:1px solid var(--line);border-radius:var(--radius);
background:var(--glass);box-shadow:var(--shadow-card);-webkit-backdrop-filter:blur(22px) saturate(1.4);backdrop-filter:blur(22px) saturate(1.4)}}
.prog-pct{{color:var(--ink);font-size:clamp(46px,6vw,62px);font-weight:300;line-height:.9;letter-spacing:-.05em;font-variant-numeric:tabular-nums}}
.prog-text{{margin-top:8px;color:var(--muted);font-size:14px}}
.ordernote{{margin-top:6px;color:var(--faint);font-size:12.5px;line-height:1.5}}
.bar{{height:6px;border-radius:99px;background:rgba(20,24,30,.08);overflow:hidden;margin-top:20px}}
.bar i{{display:block;height:100%;border-radius:99px;width:0;background:linear-gradient(90deg,var(--ink-2),var(--ink));transition:width 1.1s var(--ease)}}

.next,.phase{{position:relative;isolation:isolate;overflow:hidden;border-radius:var(--radius);
transform:perspective(900px) rotateX(var(--tilt-x,0deg)) rotateY(var(--tilt-y,0deg)) translateY(var(--lift,0px));
transition:transform .5s var(--ease),border-color .3s ease,box-shadow .3s var(--ease)}}
.next::before,.phase::before{{content:"";position:absolute;z-index:-1;inset:0;border-radius:inherit;pointer-events:none;opacity:.6;transition:opacity .3s var(--ease)}}
.next:hover,.phase:hover{{--lift:-4px}}
.next:hover::before,.phase:hover::before{{opacity:1}}

.next{{margin:0 0 32px;padding:32px 32px 30px;border:1px solid rgba(255,255,255,.12);
background:radial-gradient(600px circle at var(--glow-x,72%) var(--glow-y,20%),rgba(255,255,255,.08),transparent 55%),linear-gradient(150deg,#23262E 0%,#15171D 100%);
box-shadow:0 24px 64px -30px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.08)}}
.next::before{{background:linear-gradient(110deg,rgba(255,255,255,.10),transparent 24% 76%,rgba(255,255,255,.06))}}
.next:hover{{border-color:rgba(255,255,255,.2);box-shadow:0 34px 84px -34px rgba(0,0,0,.62),inset 0 1px 0 rgba(255,255,255,.12)}}
.next-label{{font-family:var(--mono);font-size:10px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:rgba(245,246,242,.55);margin-bottom:14px}}
.next-name{{color:#F5F6F2;font-size:clamp(24px,3.4vw,30px);font-weight:400;letter-spacing:-.03em;line-height:1.1;margin-bottom:12px}}
.next-cmd{{color:rgba(245,246,242,.62);font-size:15px}}
.next-cmd code{{font-family:var(--mono);background:rgba(255,255,255,.10);padding:2px 8px;border-radius:6px;color:#fff;font-size:13px}}
.next--done{{background:radial-gradient(600px circle at 70% 20%,rgba(14,159,110,.18),transparent 55%),linear-gradient(150deg,#23262E,#15171D)}}
.next--done .next-name{{margin-bottom:0}}

.phases{{display:flex;flex-direction:column;gap:12px;margin-bottom:8px}}
.phase{{display:flex;align-items:center;gap:18px;padding:20px 22px;border:1px solid var(--line);background:var(--glass);box-shadow:var(--shadow-card);
-webkit-backdrop-filter:blur(22px) saturate(1.4);backdrop-filter:blur(22px) saturate(1.4)}}
.phase::before{{background:linear-gradient(110deg,rgba(255,255,255,.7),transparent 20% 78%,rgba(255,255,255,.4)),radial-gradient(300px circle at var(--glow-x,50%) var(--glow-y,0%),rgba(88,108,140,.09),transparent 58%)}}
.phase:hover{{border-color:var(--line-strong);box-shadow:var(--shadow-lift)}}
.ph-num{{font-family:var(--mono);font-size:12px;font-weight:500;color:var(--faint);min-width:26px;letter-spacing:.04em;font-variant-numeric:tabular-nums}}
.is-done .ph-num{{color:var(--ink)}}
.ph-body{{flex:1;min-width:0}}
.ph-name{{color:var(--ink);font-size:16px;font-weight:500;letter-spacing:-.02em;display:flex;align-items:center;gap:9px;flex-wrap:wrap}}
.open{{color:var(--ink);font-size:13px;font-weight:500;display:inline-flex;align-items:center;gap:5px;margin-top:6px;
background-image:linear-gradient(currentColor,currentColor);background-size:0% 1px;background-position:0 100%;background-repeat:no-repeat;transition:background-size .25s ease}}
.open span{{transition:transform .25s var(--ease)}}
.open:hover{{background-size:100% 1px}} .open:hover span{{transform:translateX(3px)}}
.run{{color:var(--muted);font-size:13px;display:inline-block;margin-top:6px}}
.run code{{font-family:var(--mono);background:rgba(20,22,26,.05);border:1px solid var(--line);padding:1px 8px;border-radius:6px;color:var(--ink-2);font-size:12px}}
.ph-badge{{flex-shrink:0}}
.b-done,.b-pending{{font-family:var(--mono);font-size:9px;font-weight:500;text-transform:uppercase;letter-spacing:.1em;padding:5px 11px;border-radius:8px;white-space:nowrap}}
.b-done{{color:var(--green-ink);background:rgba(14,159,110,.10);border:1px solid rgba(14,159,110,.24)}}
.b-pending{{color:var(--faint);background:rgba(20,22,26,.04);border:1px solid var(--line)}}
.b-post,.b-two{{font-family:var(--mono);font-size:8px;font-weight:500;text-transform:uppercase;letter-spacing:.1em;padding:3px 8px;border-radius:6px;color:var(--muted);background:rgba(20,22,26,.05);border:1px solid var(--line)}}
.foot{{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--faint);text-align:center;margin-top:56px;padding:30px 0 max(48px,env(safe-area-inset-bottom));border-top:1px solid var(--line)}}

.js .reveal{{opacity:0;transform:translateY(22px);transition:opacity .7s var(--ease),transform .7s var(--ease);transition-delay:var(--delay,0ms)}}
.js .reveal.in{{opacity:1;transform:none}}

@media(hover:none),(pointer:coarse){{.next,.phase{{transform:none !important}}}}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){{.progress,.phase,.topbar{{background:rgba(255,255,255,.96)}}}}
@media(max-width:860px){{
  .progress,.phase,.topbar{{-webkit-backdrop-filter:none !important;backdrop-filter:none !important}}
  .progress,.phase{{background:var(--card-solid)}}
  .topbar{{background:linear-gradient(135deg,rgba(255,255,255,.97),rgba(255,255,255,.93))}}
  .next,.phase{{transform:none !important}}
}}
@media(max-width:480px){{h1{{font-size:clamp(38px,12vw,54px)}}.progress{{padding:24px 22px}}.phase{{padding:18px}}}}
@media(prefers-reduced-motion:reduce){{
  html{{scroll-behavior:auto}}
  .js .reveal{{opacity:1;transform:none;transition:none}}
  .bar i{{transition:none}}.next,.phase{{transform:none !important}}
}}
</style></head>
<body id="top">
<a class="skip-link" href="#conteudo">Pular</a>
<header class="topbar" aria-label="Aura Engine">
  <a class="brand" href="#top" role="img" aria-label="Aura Engine"><span class="brand-mark" aria-hidden="true">{LOGO_SVG}</span><span>Aura Engine</span></a>
  <div class="system-state">{tr["panel"]} · {year}</div>
</header>
<main id="conteudo" class="wrap">
  <p class="eyebrow reveal">{tr["eyebrow"]}</p>
  <h1 class="reveal">{tr["title"]}</h1>
  <p class="sub reveal">{tr["sub"].format(p=pname)}</p>
  <div class="progress reveal">
    <div class="prog-pct" data-count="{pct}" data-suffix="%">{pct}%</div>
    <div class="prog-text">{tr["progress"].format(d=done_count,t=total)}</div>
    <div class="ordernote">{tr["order_note"]}</div>
    <div class="bar"><i data-pct="{pct}"></i></div>
  </div>
  {next_html}
  <div class="phases">{''.join(rows)}</div>
  <p class="foot">Aura © {year}</p>
</main>
<script>
(function(){{
  var root=document.documentElement;
  if(!('IntersectionObserver' in window))return;
  root.classList.add('js');
  var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
  var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
  var revs=[].slice.call(document.querySelectorAll('.reveal'));
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}})}},{{threshold:.12,rootMargin:'0px 0px -6% 0px'}});
  revs.forEach(function(el,i){{el.style.transitionDelay=Math.min(i*45,420)+'ms';io.observe(el)}});
  setTimeout(function(){{revs.forEach(function(el){{el.classList.add('in')}})}},2400);
  // barra de progresso preenche + count-up do %
  function animate(){{
    var bar=document.querySelector('.bar i'); if(bar) bar.style.width=(bar.getAttribute('data-pct')||0)+'%';
    var el=document.querySelector('.prog-pct'); if(!el)return;
    var target=parseFloat(el.getAttribute('data-count'))||0, suf=el.getAttribute('data-suffix')||'';
    if(reduce){{el.textContent=target+suf;return}}
    var t0=performance.now();
    (function step(t){{var p=Math.min(1,(t-t0)/900),e=1-Math.pow(1-p,3);
      el.textContent=Math.round(target*e)+suf; if(p<1)requestAnimationFrame(step); else el.textContent=target+suf}})(t0);
  }}
  (window.requestAnimationFrame||setTimeout)(function(){{setTimeout(animate,180)}});
  // glow + tilt no ponteiro (só pointer fino)
  if(fine && !reduce){{
    var raf=0;
    window.addEventListener('pointermove',function(ev){{if(raf)return;raf=requestAnimationFrame(function(){{root.style.setProperty('--mx',ev.clientX+'px');root.style.setProperty('--my',ev.clientY+'px');raf=0}})}},{{passive:true}});
    document.querySelectorAll('.phase,.next').forEach(function(c){{
      c.addEventListener('pointermove',function(ev){{var r=c.getBoundingClientRect(),x=(ev.clientX-r.left)/r.width,y=(ev.clientY-r.top)/r.height;
        c.style.setProperty('--glow-x',(x*100)+'%');c.style.setProperty('--glow-y',(y*100)+'%');
        c.style.setProperty('--tilt-x',((.5-y)*1.6)+'deg');c.style.setProperty('--tilt-y',((x-.5)*1.8)+'deg')}});
      c.addEventListener('pointerleave',function(){{c.style.setProperty('--tilt-x','0deg');c.style.setProperty('--tilt-y','0deg')}});
    }});
  }}
}})();
</script>
</body></html>'''

def main():
    if len(sys.argv) < 2:
        print("uso: build_index.py <produto-slug>", file=sys.stderr); sys.exit(1)
    slug = sys.argv[1]
    out_root = Path.cwd() / "workspace" / slug
    if not out_root.exists():
        repo_root = Path(__file__).resolve().parents[3] / "workspace" / slug
        if repo_root.exists():
            out_root = repo_root
        else:
            # nem no cwd nem no repo — não cria pasta órfã (evita poluir o repo com um slug
            # digitado errado). A skill que cria o produto já faz mkdir antes de chamar isto.
            print(f"[aura] workspace/{slug} não existe (cwd nem repo). Rode a skill que cria o "
                  f"produto primeiro, ou confira o slug.", file=sys.stderr)
            sys.exit(1)
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "ABRIR-AQUI.html").write_text(build(slug), encoding="utf-8")
    print(f"[aura] ABRIR-AQUI.html atualizado em {out_root/'ABRIR-AQUI.html'}")

if __name__ == "__main__":
    main()

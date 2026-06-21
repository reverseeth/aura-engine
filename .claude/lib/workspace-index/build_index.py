#!/usr/bin/env python3
"""
build_index.py — gera o painel ABRIR-AQUI.html de um produto do Aura Engine.

É a PORTA DE ENTRADA do membro: lista cada fase (com nome amigável), mostra o que
já foi feito vs pendente, a barra de progresso, e o PRÓXIMO PASSO. Cada relatório
concluído vira um link "Abrir". Mesmo design premium (liquid glass + glow) dos
relatórios.

Toda skill, ao terminar de salvar seus outputs, roda:
    python3 .claude/lib/workspace-index/build_index.py <produto-slug>

O idioma vem de manifest.report_language (default pt-BR). O painel reflete o estado
real escaneando as subpastas de fase (0X-<stem>/relatorio.html).
"""
import json, sys, html, datetime
from pathlib import Path

# Fases na ordem lógica de execução. folder = subpasta de fase; o relatório humano é
# sempre <folder>/relatorio.html. "post" marca fases pós-launch (rodam depois).
PHASES = [
    ("00", "00-setup",              {"pt-BR": "Setup",                 "en": "Setup"},                  None, False),
    ("01", "01-product-research",   {"pt-BR": "Pesquisa de produto",   "en": "Product research"},       "product research", False),
    ("02", "02-market-research",    {"pt-BR": "Pesquisa de mercado",   "en": "Market research"},        "market research", False),
    ("03", "03-competitor-analysis",{"pt-BR": "Análise de concorrência","en": "Competitor analysis"},   "competitor analysis", False),
    ("04", "04-offer-builder",      {"pt-BR": "Oferta",                "en": "Offer"},                  "offer", False),
    ("06", "06-copy-engine",        {"pt-BR": "Copy",                  "en": "Copy"},                   "copy", False),
    ("07", "07-page",               {"pt-BR": "Página (loja)",         "en": "Page (storefront)"},      "page", False),
    ("07c","07c-tracking-setup",    {"pt-BR": "Tracking (pixel + CAPI)","en": "Tracking (pixel + CAPI)"},"tracking", False),
    ("07d","07d-checkout-aov",      {"pt-BR": "Checkout & AOV",        "en": "Checkout & AOV"},         "checkout", False),
    ("08", "08-creative-engine",    {"pt-BR": "Criativos",             "en": "Creatives"},              "creatives", False),
    ("09", "09-consistency-audit",  {"pt-BR": "Auditoria de consistência","en": "Consistency audit"},   "audit", False),
    ("10", "10-ad-strategy",        {"pt-BR": "Estratégia de ads",     "en": "Ad strategy"},            "ad strategy", False),
    ("11", "11-ad-analysis",        {"pt-BR": "Análise de ads",        "en": "Ad analysis"},            "ad analysis", False),
    ("12", "12-scale-engine",       {"pt-BR": "Escala",                "en": "Scale"},                  "scale", False),
    ("13", "13-retention-engine",   {"pt-BR": "Retenção (email/SMS)",  "en": "Retention (email/SMS)"},  "retention", True),
    ("05", "05-bonus-delivery",     {"pt-BR": "Entrega de bônus",      "en": "Bonus delivery"},         "bonus delivery", True),
    ("14", "14-content-recycler",   {"pt-BR": "Reciclagem de conteúdo","en": "Content recycler"},       "recycle", True),
]

# Relatório alternativo: só a fase 07 difere do padrão <folder>/relatorio.html — a página
# humana é 07-page/07-page.html (escrita pela 07b APÓS o build/deploy). NÃO incluímos
# design/page.html aqui de propósito: a fase "Página" só conta como concluída quando a
# página foi de fato construída (07b), não quando só o design (07a) foi aprovado.
# 08/11/12/14 escrevem relatorio.html no padrão, então não precisam de entrada aqui.
ALT_REPORT = {
    "07-page":  ["07-page/07-page.html"],
}

LOGO_SVG = ('<svg viewBox="0 0 1789.33 925.59" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            '<path d="M0,925.59h923.43l306.37-306.37h105.11c15.83,0,28.65,12.83,28.65,28.65v277.72h270.77'
            'v-308.53l-241.89,1.93c-15.91.13-28.88-12.74-28.88-28.65V0h-387.05c-33.3,0-65.23,13.24-88.76,36.8L0,925.59Z" fill="#14161D"/></svg>')

T = {
  "pt-BR": dict(title="Seu painel", sub="Tudo que a Aura já criou pra <b>{p}</b>. Abra qualquer relatório, ou siga pro próximo passo.",
                done="Concluído", pending="Pendente", open="Abrir relatório →", next="Próximo passo",
                next_post="Próximo passo (pós-launch)",
                run='Diga <code>{cmd}</code> pra rodar.', progress="{d} de {t} fases concluídas",
                alldone="Tudo pronto. Sua máquina está montada.", post="Pós-launch"),
  "en": dict(title="Your dashboard", sub="Everything Aura has built for <b>{p}</b>. Open any report, or move to the next step.",
                done="Done", pending="Pending", open="Open report →", next="Next step",
                next_post="Next step (post-launch)",
                run='Say <code>{cmd}</code> to run it.', progress="{d} of {t} phases done",
                alldone="All set. Your machine is built.", post="Post-launch"),
}

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
        cand = [f"{folder}/relatorio.html"] + ALT_REPORT.get(folder, [])
        for c in cand:
            if (root / c).exists():
                return c
        return None

    rows, done_count, total = [], 0, 0
    next_phase = None   # primeira fase NÃO-pós pendente
    post_next = None    # primeira fase pós-launch pendente (fallback quando o core acabou)
    for sid, folder, names, cmd, post in PHASES:
        if sid == "00":  # setup não vira card de relatório
            continue
        total += 1
        link = report_link(folder)
        # done = report artifact exists, OR manifest marks this phase complete.
        # match skills_completed entries as "<sid>-..." to avoid the 07/07c/07d prefix
        # collision (a bare startswith(sid) would let 07c mark the 07-page phase done).
        # fase 07 (folder 07-page) é construída pela 07b: marca done quando 07b consta
        # (a 07a só desenha; tracking/checkout 07c/07d são fases próprias e não contam aqui).
        is_done = (link is not None
                   or any(s == folder or s.startswith(sid + "-") for s in completed)
                   or (sid == "07" and "07b-page-build" in completed))
        if is_done: done_count += 1
        elif next_phase is None and not post and cmd:
            next_phase = (names[lang], cmd)
        elif post_next is None and post and cmd:
            post_next = (names[lang], cmd)
        name = html.escape(names[lang])
        badge = (f'<span class="b-done">{tr["done"]}</span>' if is_done else f'<span class="b-pending">{tr["pending"]}</span>')
        post_tag = f'<span class="b-post">{tr["post"]}</span>' if post else ''
        action = (f'<a class="open" href="{html.escape(link)}">{tr["open"]}</a>' if link
                  else (f'<span class="run">{tr["run"].format(cmd=html.escape(cmd))}</span>' if cmd else ''))
        rows.append(f'''<div class="phase {'is-done' if is_done else 'is-pending'} reveal">
          <div class="ph-num">{sid}</div>
          <div class="ph-body"><div class="ph-name">{name} {post_tag}</div>{action}</div>
          <div class="ph-badge">{badge}</div></div>''')

    pct = round(done_count / total * 100) if total else 0
    # próximo passo: core pendente primeiro; se o core acabou mas faltam fases pós-launch,
    # mostra a primeira delas (não deixa o card sumir); só "tudo pronto" quando tudo acabou.
    next_html = ''
    if next_phase:
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
        next_html = f'<div class="next reveal"><div class="next-name">{tr["alldone"]}</div></div>'

    return f'''<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://api.fontshare.com; font-src 'self' https://fonts.gstatic.com https://cdn.fontshare.com data:; script-src 'self' 'unsafe-inline';">
<title>{pname} — Aura</title>
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,600,700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#EFF1F5;--ink:#14161D;--ink2:#3A3E4A;--muted:#565B68;--faint:#9499A5;--line:#E5E7EE;
--accent:#2D5BFF;--accent2:#7C5CFF;--green:#0E9F6E;--glass:rgba(255,255,255,.62);--glassline:rgba(255,255,255,.75);
--display:'Satoshi','Inter',sans-serif;--sans:'Inter',-apple-system,sans-serif;--mono:'SF Mono',monospace;}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--bg);color:var(--ink);letter-spacing:-.011em;
display:flex;justify-content:center;padding:64px 24px 120px;-webkit-font-smoothing:antialiased;position:relative;min-height:100vh}}
body::before{{content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;
background:radial-gradient(48% 38% at 82% -4%,rgba(45,91,255,.13),transparent 72%),
radial-gradient(42% 40% at 8% 102%,rgba(124,92,255,.11),transparent 72%)}}
.wrap{{max-width:720px;width:100%}}
.logo svg{{height:28px;width:auto}} .logo{{margin-bottom:30px}}
h1{{font-family:var(--display);font-size:clamp(34px,5vw,48px);font-weight:600;letter-spacing:-.045em;line-height:1;margin:6px 0 16px}}
.sub{{font-size:18px;color:var(--muted);line-height:1.5;margin-bottom:34px;max-width:54ch}} .sub b{{color:var(--ink);font-weight:600}}
.bar{{height:8px;border-radius:99px;background:#E2E5EC;overflow:hidden;margin-bottom:10px}}
.bar i{{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),var(--accent2));width:{pct}%;transition:width 1s cubic-bezier(.2,.7,.3,1)}}
.prog{{font-size:13px;color:var(--faint);font-weight:500;margin-bottom:40px;letter-spacing:0}}
.next{{background:linear-gradient(160deg,rgba(22,24,34,.97),rgba(14,16,22,.97));color:#fff;border-radius:22px;padding:30px 32px;margin-bottom:36px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.08);box-shadow:0 24px 60px rgba(14,16,22,.22)}}
.next::after{{content:"";position:absolute;top:-40%;right:-8%;width:55%;height:120%;background:radial-gradient(circle,rgba(124,92,255,.5),transparent 62%);filter:blur(40px)}}
.next>*{{position:relative;z-index:1}}
.next-label{{font-size:11px;text-transform:uppercase;letter-spacing:.13em;color:#9E92FF;font-weight:600;margin-bottom:12px}}
.next-name{{font-family:var(--display);font-size:26px;font-weight:700;letter-spacing:-.03em;margin-bottom:10px;text-shadow:0 2px 30px rgba(124,92,255,.35)}}
.next-cmd{{color:#A6ABB8;font-size:15px}} .next-cmd code{{font-family:var(--mono);background:rgba(255,255,255,.1);padding:2px 8px;border-radius:6px;color:#fff;font-size:13px}}
.phases{{display:flex;flex-direction:column;gap:10px}}
.phase{{display:flex;align-items:center;gap:18px;padding:18px 22px;border-radius:16px;background:var(--glass);
-webkit-backdrop-filter:blur(20px) saturate(155%);backdrop-filter:blur(20px) saturate(155%);
border:1px solid var(--glassline);box-shadow:0 1px 2px rgba(20,22,29,.04),0 6px 18px rgba(20,22,29,.05);
transition:transform .3s cubic-bezier(.2,.7,.3,1),box-shadow .3s}}
.phase:hover{{transform:translateY(-2px);box-shadow:0 4px 8px rgba(20,22,29,.05),0 22px 50px rgba(20,22,29,.11)}}
.ph-num{{font-family:var(--display);font-size:14px;font-weight:600;color:var(--accent);min-width:26px;font-variant-numeric:tabular-nums}}
.is-pending .ph-num{{color:var(--faint)}}
.ph-body{{flex:1}} .ph-name{{font-size:16.5px;font-weight:600;letter-spacing:-.02em;display:flex;align-items:center;gap:8px}}
.open{{color:var(--accent);text-decoration:none;font-size:13.5px;font-weight:500;display:inline-block;margin-top:5px}}
.open:hover{{text-decoration:underline}}
.run{{color:var(--faint);font-size:13px;display:inline-block;margin-top:5px}} .run code{{font-family:var(--mono);background:#E7E9F0;padding:1px 7px;border-radius:5px;color:var(--ink2);font-size:12px}}
.b-done{{font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:#0B7A53;background:rgba(14,159,110,.12);border:1px solid rgba(14,159,110,.2);padding:4px 11px;border-radius:8px}}
.b-pending{{font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--faint);background:rgba(148,153,165,.1);border:1px solid rgba(148,153,165,.2);padding:4px 11px;border-radius:8px}}
.b-post{{font-size:9.5px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:#7C5CFF;background:rgba(124,92,255,.1);padding:2px 8px;border-radius:6px}}
.foot{{font-size:13px;color:var(--faint);text-align:center;margin-top:64px;padding-top:36px;border-top:1px solid var(--line)}}
.js .reveal{{opacity:0;transform:translateY(16px);transition:opacity .6s cubic-bezier(.2,.7,.3,1),transform .6s cubic-bezier(.2,.7,.3,1)}}
.js .reveal.in{{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){{.js .reveal{{opacity:1;transform:none;transition:none}}.phase{{transition:none}}}}
@media(max-width:560px){{body{{padding:36px 16px 80px}}.phase{{padding:16px}}}}
</style></head><body><div class="wrap">
<div class="logo reveal" role="img" aria-label="Aura Engine">{LOGO_SVG}</div>
<h1 class="reveal">{tr["title"]}</h1>
<p class="sub reveal">{tr["sub"].format(p=pname)}</p>
<div class="bar reveal"><i></i></div>
<div class="prog reveal">{tr["progress"].format(d=done_count,t=total)}</div>
{next_html}
<div class="phases">{''.join(rows)}</div>
<p class="foot">Aura © {datetime.date.today().year if False else 2026}</p>
</div>
<script>document.documentElement.classList.add('js');
const io=new IntersectionObserver((es)=>{{es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}})}},{{threshold:.1}});
document.querySelectorAll('.reveal').forEach((el,i)=>{{el.style.transitionDelay=(i*40)+'ms';io.observe(el)}});</script>
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

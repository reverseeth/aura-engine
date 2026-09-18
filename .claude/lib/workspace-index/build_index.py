#!/usr/bin/env python3
"""
build_index.py — gera o painel ABRIR-AQUI.html de um produto do Aura Engine e, com --global, o
painel de todos os produtos em workspace/ABRIR-AQUI.html.

É a PORTA DE ENTRADA do membro: lista cada fase (com nome amigável), mostra o que
já foi feito vs pendente, a barra de progresso, e o PRÓXIMO PASSO. Cada relatório
concluído vira um link "Abrir". Mesmo design "Editorial Intelligence" (off-white,
liquid glass, tipografia Geist, topbar flutuante, animações) dos relatórios.

Toda skill, ao terminar de salvar seus outputs, roda:
    python3 .claude/lib/workspace-index/build_index.py <produto-slug>

O painel global (um card por produto, com progresso, próximo passo e pontos a conferir):
    python3 .claude/lib/workspace-index/build_index.py --global

O idioma vem de manifest.report_language (default pt-BR). O estado real do produto (relatório
de cada fase, skills marcadas, issues) é lido do tools/aura-status.py — a mesma leitura que
o hook de fim de resposta e o membro usam —, então painel e status nunca discordam.
"""
import json, sys, re, html, datetime, importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def _load_status():
    """Importa tools/aura-status.py (o hífen no nome impede o import normal)."""
    spec = importlib.util.spec_from_file_location("aura_status", REPO / "tools" / "aura-status.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


STATUS = _load_status()

# Fases na ordem lógica de execução. folder = subpasta de fase, que leva o id da skill, sem
# número (ex.: market-research/); o relatório humano é <folder>/<folder>.html, com fallback
# legado relatorio.html (produtos antigos). Produto ainda não migrado pelo tools/migrate.py
# guarda a fase na pasta numerada antiga (LEGACY_FOLDERS): a leitura cai nela por um ciclo,
# do mesmo jeito que cai no relatorio.html.
# Primeiro campo = apelido antigo da skill (o número que o card mostra e a chave interna da
# fase; page-design e page-build compartilham o card "07"). Último campo = tag do card: None
# (core), "post" (pós-launch), "two" (skill de 2 fases: Fase A pré-launch + Fase B pós-launch,
# bonus-delivery e retention-engine), "opt" (opcional: sourcing) e "side" (consulta lateral:
# não é etapa da sequência, roda quando o membro precisa: finance-engine, creator-engine,
# promo-engine, team-engine, ops-engine e marketplace-engine). As skills "two" mantêm a
# posição do card aqui; a Fase A delas entra como próximo passo pela lógica condicional no
# build() (depois da checkout-aov), não pela posição na lista.
# A finance-engine aparece logo depois da offer-builder porque é ali que ela é consultada pela
# primeira vez ("a oferta fecha a conta do negócio inteiro, com o custo fixo dentro?"), mas
# NÃO é etapa da sequência: como a sourcing, nunca vira sugestão de próximo passo (ver
# NO_SUGGEST). As outras laterais seguem o mesmo princípio de posição (o card fica onde a
# consulta é natural pela primeira vez): a ops-engine vem logo depois do setup (o checklist
# de backups vale desde o começo, porque conta nova é a mais frágil); a creator-engine fica
# junto da creative-engine (a Fase A de seeding roda em paralelo aos criativos, e a Fase B só
# abre pós-breakthrough); a promo-engine (sazonal) e a team-engine (estágio scaling) vêm
# depois da scale-engine; a marketplace-engine (canais de venda, estágio scaling) fecha a
# lista: canal secundário é agenda de quem já provou o primário. Como a sourcing e a
# finance-engine, nenhuma vira sugestão de próximo passo.
# A content-recycler cobre as DUAS trilhas da skill: Trilha 1 (amplificação do breakthrough,
# o default, que é o que de fato escala a conta) e Trilha 2 (as 9 derivadas de canal, sob
# pedido). Por isso o card se chama "Amplificação e reciclagem", não só "reciclagem".
# A lista PHASES e o mapa LEGACY_FOLDERS são gerados pelo tools/gen_docs.py a partir do
# .claude/skills.json (não edite à mão; rode o gerador).
# gen:phases:start
PHASES = [
    ("00", "setup", {"pt-BR": "Setup", "en": "Setup"}, None, None),
    ("19", "ops-engine", {"pt-BR": "Operação (continuidade e risco)", "en": "Ops (continuity & risk)"}, "operação", "side"),
    ("01", "product-research", {"pt-BR": "Pesquisa de produto", "en": "Product research"}, "product research", None),
    ("01b", "sourcing", {"pt-BR": "Fornecedor (sourcing)", "en": "Sourcing"}, "sourcing", "opt"),
    ("02", "market-research", {"pt-BR": "Pesquisa de mercado", "en": "Market research"}, "market research", None),
    ("03", "competitor-analysis", {"pt-BR": "Análise de concorrência", "en": "Competitor analysis"}, "competitor analysis", None),
    ("04", "offer-builder", {"pt-BR": "Oferta", "en": "Offer"}, "offer", None),
    ("15", "finance-engine", {"pt-BR": "Finanças (modelo do negócio)", "en": "Finance (business model)"}, "finance", "side"),
    ("06", "copy-engine", {"pt-BR": "Copy", "en": "Copy"}, "copy", None),
    ("07", "page", {"pt-BR": "Página (loja)", "en": "Page (storefront)"}, "page", None),
    ("07c", "tracking-setup", {"pt-BR": "Tracking (pixel + CAPI)", "en": "Tracking (pixel + CAPI)"}, "tracking", None),
    ("07d", "checkout-aov", {"pt-BR": "Checkout & AOV", "en": "Checkout & AOV"}, "checkout", None),
    ("08", "creative-engine", {"pt-BR": "Criativos", "en": "Creatives"}, "creatives", None),
    ("16", "creator-engine", {"pt-BR": "Creators (conteúdo humano)", "en": "Creators (human content)"}, "creators", "side"),
    ("07e", "agentic-readiness", {"pt-BR": "Visibilidade pra agentes de AI", "en": "Agentic readiness (AI visibility)"}, "agentic readiness", None),
    ("09", "consistency-audit", {"pt-BR": "Auditoria de consistência", "en": "Consistency audit"}, "audit", None),
    ("10", "ad-strategy", {"pt-BR": "Estratégia de ads", "en": "Ad strategy"}, "ad strategy", None),
    ("11", "ad-analysis", {"pt-BR": "Análise de ads", "en": "Ad analysis"}, "ad analysis", None),
    ("12", "scale-engine", {"pt-BR": "Escala", "en": "Scale"}, "scale", None),
    ("17", "promo-engine", {"pt-BR": "Promoções (janelas sazonais)", "en": "Promos (seasonal windows)"}, "promo", "side"),
    ("18", "team-engine", {"pt-BR": "Time (contratação e gestão)", "en": "Team (hiring & management)"}, "contratar", "side"),
    ("13", "retention-engine", {"pt-BR": "Retenção (email/SMS)", "en": "Retention (email/SMS)"}, "retention", "two"),
    ("05", "bonus-delivery", {"pt-BR": "Entrega de bônus", "en": "Bonus delivery"}, "bonus delivery", "two"),
    ("14", "content-recycler", {"pt-BR": "Amplificação e reciclagem", "en": "Amplification & recycling"}, "recycle", "post"),
    ("20", "marketplace-engine", {"pt-BR": "Canais de venda (marketplace)", "en": "Sales channels (marketplace)"}, "marketplace", "side"),
]
LEGACY_FOLDERS = {
    "ops-engine": "19-ops-engine",
    "product-research": "01-product-research",
    "market-research": "02-market-research",
    "competitor-analysis": "03-competitor-analysis",
    "offer-builder": "04-offer-builder",
    "finance-engine": "15-finance-engine",
    "copy-engine": "06-copy-engine",
    "page": "07-page",
    "tracking-setup": "07c-tracking-setup",
    "checkout-aov": "07d-checkout-aov",
    "creative-engine": "08-creative-engine",
    "creator-engine": "16-creator-engine",
    "agentic-readiness": "07e-agentic-readiness",
    "consistency-audit": "09-consistency-audit",
    "ad-strategy": "10-ad-strategy",
    "ad-analysis": "11-ad-analysis",
    "scale-engine": "12-scale-engine",
    "promo-engine": "17-promo-engine",
    "team-engine": "18-team-engine",
    "retention-engine": "13-retention-engine",
    "bonus-delivery": "05-bonus-delivery",
    "content-recycler": "14-content-recycler",
    "marketplace-engine": "20-marketplace-engine",
}
# gen:phases:end

# Fases cujo done vem SÓ do manifest (skills_completed), nunca da existência do relatório:
# a sourcing salva sourcing.html já no checkpoint de cotação enviada (status "quoting"), mas a
# fase só fecha quando a cotação fecha (status "closed" → manifest). O link "Abrir
# relatório" continua aparecendo; só o badge Concluído espera o manifest.
MANIFEST_ONLY = {"sourcing"}

# Badge do card por tag: (classe CSS, chave de tradução em T). Tag ausente = sem badge.
TAG_BADGE = {"two": ("b-two", "two_phase"), "post": ("b-post", "post"),
             "opt": ("b-two", "optional"), "side": ("b-two", "side")}

# Tags que NUNCA viram sugestão de próximo passo: a fase é opcional ("opt", ex: sourcing) ou
# é consulta lateral fora da sequência ("side", ex: finanças) — o membro chama quando precisa.
NO_SUGGEST = {"opt", "side"}

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
                side="Consulta",
                order_note="As fases aparecem na ordem em que rodam. O número ao lado de cada fase é o apelido antigo da skill: chame pelo nome ou por ele.",
                bonus_a="Entrega de bônus — Fase A (assets + GWP)",
                retention_a="Retenção — Fase A (flows de recuperação)",
                issues="{n} ponto(s) a conferir: peça <code>aura-status {s}</code> na sessão.",
                g_title="Seus produtos", g_eyebrow="Aura Engine / produtos",
                g_sub="Um card por produto. Abra o painel de cada um pra ver as fases e o próximo passo.",
                g_open="Abrir painel", g_next="Próximo: ", g_progress="{d} de {t} fases",
                g_issues="{n} a conferir", g_ok="tudo em ordem",
                g_none="Nenhum produto ainda. Diga <code>setup</code> na sessão pra começar o primeiro."),
  "en": dict(title="Your dashboard", sub="Everything Aura has built for <b>{p}</b>. Open any report, or move to the next step.",
                eyebrow="Aura Engine / dashboard", panel="Dashboard",
                done="Done", pending="Pending", open="Open report", next="Next step",
                next_post="Next step (post-launch)",
                run='Say <code>{cmd}</code> to run it.', progress="{d} of {t} phases done",
                alldone="All set. Your machine is built.", post="Post-launch",
                two_phase="2 phases",
                optional="Optional",
                side="On demand",
                order_note="Phases appear in the order they run. The number next to each phase is the skill's old alias: call it by name or by the alias.",
                bonus_a="Bonus delivery — Phase A (assets + GWP)",
                retention_a="Retention — Phase A (recovery flows)",
                issues="{n} item(s) to check: ask for <code>aura-status {s}</code> in the session.",
                g_title="Your products", g_eyebrow="Aura Engine / products",
                g_sub="One card per product. Open each dashboard to see its phases and next step.",
                g_open="Open dashboard", g_next="Next: ", g_progress="{d} of {t} phases",
                g_issues="{n} to check", g_ok="all clear",
                g_none="No products yet. Say <code>setup</code> in the session to start the first one."),
}

CSS = """:root{
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
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{background:var(--bg);-webkit-text-size-adjust:100%}
body{min-height:100vh;overflow-x:hidden;font-family:var(--font);font-weight:300;color:var(--ink-2);line-height:1.6;letter-spacing:-.014em;
-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
background:radial-gradient(900px 560px at 86% -6%,rgba(120,140,165,.10),transparent 66%),radial-gradient(760px 520px at 2% 34%,rgba(150,160,172,.08),transparent 70%),linear-gradient(180deg,#F8F9FA 0%,var(--bg) 30%,#F1F2F4 100%)}
body::before{content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;opacity:.5;
background-image:linear-gradient(rgba(20,24,30,.028) 1px,transparent 1px),linear-gradient(90deg,rgba(20,24,30,.028) 1px,transparent 1px);
background-size:54px 54px;mask-image:linear-gradient(to bottom,black,transparent 88%)}
body::after{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(480px circle at var(--mx) var(--my),rgba(90,110,135,.05),transparent 70%)}
::selection{background:#14161A;color:#F5F6F7}
a{color:inherit;text-decoration:none;-webkit-tap-highlight-color:transparent}
svg{display:block}
:focus-visible{outline:2px solid rgba(20,24,30,.55);outline-offset:3px;border-radius:4px}
.skip-link{position:fixed;top:10px;left:10px;z-index:200;transform:translateY(-160%);padding:10px 14px;border-radius:10px;background:var(--ink);color:#F5F6F7;font-size:13px;transition:transform .18s}
.skip-link:focus{transform:none}

.topbar{position:fixed;z-index:120;top:max(14px,env(safe-area-inset-top));left:50%;transform:translateX(-50%);
display:grid;grid-template-columns:1fr auto;align-items:center;width:min(calc(100% - 32px),760px);min-height:56px;padding:8px 12px 8px 16px;
border:1px solid var(--line);border-radius:18px;background:linear-gradient(135deg,rgba(255,255,255,.88),rgba(255,255,255,.72));
box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 16px 44px -22px rgba(24,34,48,.28),0 2px 8px -4px rgba(24,34,48,.14);
-webkit-backdrop-filter:blur(20px) saturate(1.3);backdrop-filter:blur(20px) saturate(1.3)}
.brand{display:inline-flex;align-items:center;gap:12px;font-size:12.5px;font-weight:500;letter-spacing:.11em;text-transform:uppercase;color:var(--ink)}
.brand svg{height:21px;width:auto}
.system-state{justify-self:end;padding:0 14px;min-height:38px;display:inline-flex;align-items:center;border:1px solid var(--line);border-radius:11px;background:rgba(255,255,255,.6);color:var(--muted);font-family:var(--mono);font-size:9.5px;letter-spacing:.11em;text-transform:uppercase}
@media(max-width:520px){.system-state{display:none}}

.wrap{width:min(100% - 40px,760px);margin:0 auto;padding-top:calc(env(safe-area-inset-top,0px) + clamp(104px,13vh,150px))}
@media(max-width:620px){.wrap{width:min(100% - 28px,760px)}}
.eyebrow{display:flex;align-items:center;gap:12px;margin:0 0 24px;color:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.15em;text-transform:uppercase}
.eyebrow::before{content:"";width:24px;height:1px;background:var(--line-hot)}
h1{color:var(--ink);font-size:clamp(44px,7vw,72px);font-weight:300;line-height:.92;letter-spacing:-.05em;text-wrap:balance}
.sub{max-width:56ch;margin:26px 0 0;color:var(--muted);font-size:clamp(16px,1.5vw,18px);font-weight:300;line-height:1.55;letter-spacing:-.018em}
.sub b{color:var(--ink-2);font-weight:500}

.progress{position:relative;isolation:isolate;overflow:hidden;margin:clamp(40px,7vw,64px) 0 22px;padding:28px 30px;border:1px solid var(--line);border-radius:var(--radius);
background:var(--glass);box-shadow:var(--shadow-card);-webkit-backdrop-filter:blur(22px) saturate(1.4);backdrop-filter:blur(22px) saturate(1.4)}
.prog-pct{color:var(--ink);font-size:clamp(46px,6vw,62px);font-weight:300;line-height:.9;letter-spacing:-.05em;font-variant-numeric:tabular-nums}
.prog-text{margin-top:8px;color:var(--muted);font-size:14px}
.ordernote{margin-top:6px;color:var(--faint);font-size:12.5px;line-height:1.5}
.bar{height:6px;border-radius:99px;background:rgba(20,24,30,.08);overflow:hidden;margin-top:20px}
.bar i{display:block;height:100%;border-radius:99px;width:0;background:linear-gradient(90deg,var(--ink-2),var(--ink));transition:width 1.1s var(--ease)}

.next,.phase{position:relative;isolation:isolate;overflow:hidden;border-radius:var(--radius);
transform:perspective(900px) rotateX(var(--tilt-x,0deg)) rotateY(var(--tilt-y,0deg)) translateY(var(--lift,0px));
transition:transform .5s var(--ease),border-color .3s ease,box-shadow .3s var(--ease)}
.next::before,.phase::before{content:"";position:absolute;z-index:-1;inset:0;border-radius:inherit;pointer-events:none;opacity:.6;transition:opacity .3s var(--ease)}
.next:hover,.phase:hover{--lift:-4px}
.next:hover::before,.phase:hover::before{opacity:1}

.next{margin:0 0 32px;padding:32px 32px 30px;border:1px solid rgba(255,255,255,.12);
background:radial-gradient(600px circle at var(--glow-x,72%) var(--glow-y,20%),rgba(255,255,255,.08),transparent 55%),linear-gradient(150deg,#23262E 0%,#15171D 100%);
box-shadow:0 24px 64px -30px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.08)}
.next::before{background:linear-gradient(110deg,rgba(255,255,255,.10),transparent 24% 76%,rgba(255,255,255,.06))}
.next:hover{border-color:rgba(255,255,255,.2);box-shadow:0 34px 84px -34px rgba(0,0,0,.62),inset 0 1px 0 rgba(255,255,255,.12)}
.next-label{font-family:var(--mono);font-size:10px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:rgba(245,246,242,.55);margin-bottom:14px}
.next-name{color:#F5F6F2;font-size:clamp(24px,3.4vw,30px);font-weight:400;letter-spacing:-.03em;line-height:1.1;margin-bottom:12px}
.next-cmd{color:rgba(245,246,242,.62);font-size:15px}
.next-cmd code{font-family:var(--mono);background:rgba(255,255,255,.10);padding:2px 8px;border-radius:6px;color:#fff;font-size:13px}
.next--done{background:radial-gradient(600px circle at 70% 20%,rgba(14,159,110,.18),transparent 55%),linear-gradient(150deg,#23262E,#15171D)}
.next--done .next-name{margin-bottom:0}

.phases{display:flex;flex-direction:column;gap:12px;margin-bottom:8px}
.phase{display:flex;align-items:center;gap:18px;padding:20px 22px;border:1px solid var(--line);background:var(--glass);box-shadow:var(--shadow-card);
-webkit-backdrop-filter:blur(22px) saturate(1.4);backdrop-filter:blur(22px) saturate(1.4)}
.phase::before{background:linear-gradient(110deg,rgba(255,255,255,.7),transparent 20% 78%,rgba(255,255,255,.4)),radial-gradient(300px circle at var(--glow-x,50%) var(--glow-y,0%),rgba(88,108,140,.09),transparent 58%)}
.phase:hover{border-color:var(--line-strong);box-shadow:var(--shadow-lift)}
.ph-num{font-family:var(--mono);font-size:12px;font-weight:500;color:var(--faint);min-width:26px;letter-spacing:.04em;font-variant-numeric:tabular-nums}
.is-done .ph-num{color:var(--ink)}
.ph-body{flex:1;min-width:0}
.ph-name{color:var(--ink);font-size:16px;font-weight:500;letter-spacing:-.02em;display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.open{color:var(--ink);font-size:13px;font-weight:500;display:inline-flex;align-items:center;gap:5px;margin-top:6px;
background-image:linear-gradient(currentColor,currentColor);background-size:0% 1px;background-position:0 100%;background-repeat:no-repeat;transition:background-size .25s ease}
.open span{transition:transform .25s var(--ease)}
.open:hover{background-size:100% 1px} .open:hover span{transform:translateX(3px)}
.run{color:var(--muted);font-size:13px;display:inline-block;margin-top:6px}
.run code{font-family:var(--mono);background:rgba(20,22,26,.05);border:1px solid var(--line);padding:1px 8px;border-radius:6px;color:var(--ink-2);font-size:12px}
.ph-badge{flex-shrink:0}
.b-done,.b-pending{font-family:var(--mono);font-size:9px;font-weight:500;text-transform:uppercase;letter-spacing:.1em;padding:5px 11px;border-radius:8px;white-space:nowrap}
.b-done{color:var(--green-ink);background:rgba(14,159,110,.10);border:1px solid rgba(14,159,110,.24)}
.b-pending{color:var(--faint);background:rgba(20,22,26,.04);border:1px solid var(--line)}
.b-post,.b-two{font-family:var(--mono);font-size:8px;font-weight:500;text-transform:uppercase;letter-spacing:.1em;padding:3px 8px;border-radius:6px;color:var(--muted);background:rgba(20,22,26,.05);border:1px solid var(--line)}
.foot{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--faint);text-align:center;margin-top:56px;padding:30px 0 max(48px,env(safe-area-inset-bottom));border-top:1px solid var(--line)}

.js .reveal{opacity:0;transform:translateY(22px);transition:opacity .7s var(--ease),transform .7s var(--ease);transition-delay:var(--delay,0ms)}
.js .reveal.in{opacity:1;transform:none}

@media(hover:none),(pointer:coarse){.next,.phase{transform:none !important}}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.progress,.phase,.topbar{background:rgba(255,255,255,.96)}}
@media(max-width:860px){
  .progress,.phase,.topbar{-webkit-backdrop-filter:none !important;backdrop-filter:none !important}
  .progress,.phase{background:var(--card-solid)}
  .topbar{background:linear-gradient(135deg,rgba(255,255,255,.97),rgba(255,255,255,.93))}
  .next,.phase{transform:none !important}
}
@media(max-width:480px){h1{font-size:clamp(38px,12vw,54px)}.progress{padding:24px 22px}.phase{padding:18px}}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .js .reveal{opacity:1;transform:none;transition:none}
  .bar i{transition:none}.next,.phase{transform:none !important}
}
"""

JS = """(function(){
  var root=document.documentElement;
  if(!('IntersectionObserver' in window))return;
  root.classList.add('js');
  var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
  var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
  var revs=[].slice.call(document.querySelectorAll('.reveal'));
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  revs.forEach(function(el,i){el.style.transitionDelay=Math.min(i*45,420)+'ms';io.observe(el)});
  setTimeout(function(){revs.forEach(function(el){el.classList.add('in')})},2400);
  // barra de progresso preenche + count-up do %
  function animate(){
    var bar=document.querySelector('.bar i'); if(bar) bar.style.width=(bar.getAttribute('data-pct')||0)+'%';
    var el=document.querySelector('.prog-pct'); if(!el)return;
    var target=parseFloat(el.getAttribute('data-count'))||0, suf=el.getAttribute('data-suffix')||'';
    if(reduce){el.textContent=target+suf;return}
    var t0=performance.now();
    (function step(t){var p=Math.min(1,(t-t0)/900),e=1-Math.pow(1-p,3);
      el.textContent=Math.round(target*e)+suf; if(p<1)requestAnimationFrame(step); else el.textContent=target+suf})(t0);
  }
  (window.requestAnimationFrame||setTimeout)(function(){setTimeout(animate,180)});
  // glow + tilt no ponteiro (só pointer fino)
  if(fine && !reduce){
    var raf=0;
    window.addEventListener('pointermove',function(ev){if(raf)return;raf=requestAnimationFrame(function(){root.style.setProperty('--mx',ev.clientX+'px');root.style.setProperty('--my',ev.clientY+'px');raf=0})},{passive:true});
    document.querySelectorAll('.phase,.next').forEach(function(c){
      c.addEventListener('pointermove',function(ev){var r=c.getBoundingClientRect(),x=(ev.clientX-r.left)/r.width,y=(ev.clientY-r.top)/r.height;
        c.style.setProperty('--glow-x',(x*100)+'%');c.style.setProperty('--glow-y',(y*100)+'%');
        c.style.setProperty('--tilt-x',((.5-y)*1.6)+'deg');c.style.setProperty('--tilt-y',((x-.5)*1.8)+'deg')});
      c.addEventListener('pointerleave',function(){c.style.setProperty('--tilt-x','0deg');c.style.setProperty('--tilt-y','0deg')});
    });
  }
})();
"""


def phase_dirs(folder):
    """Pastas onde a fase pode estar: a nova primeiro, depois a numerada antiga (produto ainda não migrado)."""
    dirs = [folder]
    legacy = LEGACY_FOLDERS.get(folder)
    if legacy and legacy != folder:
        dirs.append(legacy)
    return dirs

def offer_has_bonuses(root):
    """True se a oferta (offer-builder) definiu bônus: só nesse caso o painel cobra a Fase A da bonus-delivery."""
    for d in phase_dirs("offer-builder"):
        p = root / d / "dados.json"
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return False
        return bool(data.get("bonuses"))
    return False

def product_root(slug):
    root = Path.cwd() / "workspace" / slug
    if not root.exists():
        # fallback: talvez rodando de outro cwd
        root = STATUS.WORKSPACE / slug
    return root

def lang_of(mani):
    lang = (mani or {}).get("report_language") or "pt-BR"
    return lang if lang in T else "pt-BR"

def page_shell(lang, title, eyebrow, panel_label, body):
    year = datetime.date.today().year
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f4f5f7">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; script-src 'self' 'unsafe-inline';">
<title>{title} — Aura</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{CSS}</style></head>
<body id="top">
<a class="skip-link" href="#conteudo">Pular</a>
<header class="topbar" aria-label="Aura Engine">
  <a class="brand" href="#top" role="img" aria-label="Aura Engine"><span class="brand-mark" aria-hidden="true">{LOGO_SVG}</span><span>Aura Engine</span></a>
  <div class="system-state">{panel_label} · {year}</div>
</header>
<main id="conteudo" class="wrap">
  <p class="eyebrow reveal">{eyebrow}</p>
{body}
  <p class="foot">Aura © {year}</p>
</main>
<script>
{JS}</script>
</body></html>'''

def build(slug, state=None):
    """Devolve (html do painel do produto, resumo). O resumo alimenta o painel global."""
    root = product_root(slug)
    state = state or STATUS.product_state(root)
    mani = state["manifest"] or {}
    lang = lang_of(mani)
    tr = T[lang]
    pname = html.escape(mani.get("product_name") or slug)
    # skills_completed vem do aura-status já sem o prefixo numérico antigo (produto ainda não migrado).
    completed = set(state["completed"])
    # relatório humano de cada fase: <folder>/<report_stem>.html (registro), com os nomes legados;
    # a fase de página só conta com o page-report.html da page-build (o design aprovado não fecha a fase).
    reports = state["reports"]

    rows, done_count, total = [], 0, 0
    next_phase = None   # primeira fase core pendente
    post_next = None    # primeira fase pós-launch/2-fases pendente (fallback quando o core acabou)
    done_by_folder = {}
    for sid, folder, names, cmd, tag in PHASES:
        if folder == "setup":  # setup não vira card de relatório
            continue
        total += 1
        # page-design (design) pronta mas page-build (build) pendente → o trigger certo é
        # "build page"; "page" re-executaria o design, que já foi aprovado.
        if folder == "page" and "page-design" in completed and "page-build" not in completed:
            cmd = "build page"
        link = reports.get(folder)
        # done = o relatório existe, OU o manifest marca a fase como concluída (o id da skill é
        # o nome da pasta). A fase de página (pasta page/) é construída pela page-build: marca
        # done quando page-build consta (a page-design só desenha; tracking-setup e checkout-aov
        # são fases próprias e não contam aqui).
        is_done = ((link is not None and folder not in MANIFEST_ONLY)
                   or folder in completed
                   or (folder == "page" and "page-build" in completed))
        done_by_folder[folder] = is_done
        if is_done: done_count += 1
        elif next_phase is None and tag is None and cmd:
            next_phase = (names[lang], cmd)
        elif post_next is None and tag and tag not in NO_SUGGEST and cmd:
            post_next = (names[lang], cmd)
        name = html.escape(names[lang])
        badge = (f'<span class="b-done">{tr["done"]}</span>' if is_done else f'<span class="b-pending">{tr["pending"]}</span>')
        badge_cls, badge_key = TAG_BADGE.get(tag, (None, None))
        post_tag = f'<span class="{badge_cls}">{tr[badge_key]}</span>' if badge_cls else ''
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
    # Fase A das skills de 2 fases (bonus-delivery, retention-engine) entra como próximo passo
    # assim que a checkout-aov fecha: operador de elite não lança tráfego pago sem os bônus
    # prometidos na PDP existirem, nem sem abandoned cart + post-purchase flow (a receita mais
    # barata que existe: infraestrutura de launch, não campanha de email).
    fase_a = None
    if done_by_folder.get("checkout-aov"):
        if offer_has_bonuses(root) and not done_by_folder.get("bonus-delivery"):
            fase_a = (tr["bonus_a"], "bonus delivery")
        elif not done_by_folder.get("retention-engine"):
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
    n_issues = len(state["issues"])
    issues_html = (f'\n    <div class="ordernote">{tr["issues"].format(n=n_issues, s=html.escape(slug))}</div>' if n_issues else '')

    body = f'''  <h1 class="reveal">{tr["title"]}</h1>
  <p class="sub reveal">{tr["sub"].format(p=pname)}</p>
  <div class="progress reveal">
    <div class="prog-pct" data-count="{pct}" data-suffix="%">{pct}%</div>
    <div class="prog-text">{tr["progress"].format(d=done_count,t=total)}</div>
    <div class="ordernote">{tr["order_note"]}</div>{issues_html}
    <div class="bar"><i data-pct="{pct}"></i></div>
  </div>
  {next_html}
  <div class="phases">{''.join(rows)}</div>'''
    summary = {"slug": slug, "name": pname, "lang": lang, "pct": pct, "done": done_count, "total": total,
               "next": chosen, "issues": n_issues}
    return page_shell(lang, pname, tr["eyebrow"], tr["panel"], body), summary

def build_global(summaries):
    """Painel de todos os produtos: um card por produto, no idioma da maioria dos manifests."""
    langs = [s["lang"] for s in summaries]
    lang = max(set(langs), key=langs.count) if langs else "pt-BR"
    tr = T[lang]
    cards = []
    for s in summaries:
        meta = tr["g_progress"].format(d=s["done"], t=s["total"])
        if s["next"]:
            meta += f' · {tr["g_next"]}{html.escape(s["next"][0])}'
        status = (f'<span class="b-pending">{tr["g_issues"].format(n=s["issues"])}</span>' if s["issues"]
                  else f'<span class="b-done">{tr["g_ok"]}</span>')
        cards.append(f'''<a class="phase {'is-done' if s["pct"] == 100 else 'is-pending'} reveal" href="{html.escape(s["slug"])}/ABRIR-AQUI.html">
          <div class="ph-num">{s["pct"]}%</div>
          <div class="ph-body"><div class="ph-name">{s["name"]}</div><span class="run">{meta}</span></div>
          <div class="ph-badge">{status}</div></a>''')
    n_done = sum(s["done"] for s in summaries)
    n_total = sum(s["total"] for s in summaries)
    pct = round(n_done / n_total * 100) if n_total else 0
    body = f'''  <h1 class="reveal">{tr["g_title"]}</h1>
  <p class="sub reveal">{tr["g_sub"]}</p>
  <div class="progress reveal">
    <div class="prog-pct" data-count="{len(summaries)}" data-suffix="">{len(summaries)}</div>
    <div class="prog-text">{tr["g_progress"].format(d=n_done, t=n_total)}</div>
    <div class="bar"><i data-pct="{pct}"></i></div>
  </div>
  <div class="phases">{''.join(cards) if cards else f'<div class="phase reveal"><div class="ph-body"><span class="run">{tr["g_none"]}</span></div></div>'}</div>'''
    return page_shell(lang, tr["g_title"], tr["g_eyebrow"], tr["g_title"], body)

def main():
    if len(sys.argv) < 2:
        print("uso: build_index.py <produto-slug> | --global", file=sys.stderr); sys.exit(1)
    if sys.argv[1] == "--global":
        ws = STATUS.WORKSPACE
        if not ws.is_dir():
            print("[aura] workspace/ não existe", file=sys.stderr); sys.exit(1)
        summaries = []
        for p in STATUS.products():
            _, summary = build(p.name, STATUS.product_state(p))
            summaries.append(summary)
        out = ws / "ABRIR-AQUI.html"
        out.write_text(build_global(summaries), encoding="utf-8")
        print(f"[aura] painel global atualizado em {out} ({len(summaries)} produto(s))")
        return
    slug = sys.argv[1]
    out_root = product_root(slug)
    if not out_root.exists():
        # nem no cwd nem no repo — não cria pasta órfã (evita poluir o repo com um slug
        # digitado errado). A skill que cria o produto já faz mkdir antes de chamar isto.
        print(f"[aura] workspace/{slug} não existe (cwd nem repo). Rode a skill que cria o "
              f"produto primeiro, ou confira o slug.", file=sys.stderr)
        sys.exit(1)
    page, _ = build(slug)
    (out_root / "ABRIR-AQUI.html").write_text(page, encoding="utf-8")
    print(f"[aura] ABRIR-AQUI.html atualizado em {out_root/'ABRIR-AQUI.html'}")

if __name__ == "__main__":
    main()

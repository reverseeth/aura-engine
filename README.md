# Aura Engine

AI-powered operating system for DTC ecommerce brands. Runs inside Claude Code.

## What it does

Orchestrates the full product-to-ads-to-retention workflow through 14 skills:

| # | Skill | Output |
|---|---|---|
| 00 | setup | profile + first manifest + dashboard |
| 01 | product research | product validation + score |
| 02 | market research | VOC, awareness, sophistication, root cause |
| 03 | competitor analysis | claims, gaps, creative patterns (Whisper transcription) |
| 04 | offer builder | mechanism, research foundation, pricing, guarantee |
| 05 | bonus delivery | ecom bonus asset + delivery tracking (post-launch) |
| 06 | copy engine | headlines, leads, advertorial, PDP copy |
| 07a–d | storefront | page design → build/deploy → tracking (Pixel + CAPI) → checkout/AOV |
| 08 | creative engine | ad briefings (scripts, hooks, prompts) + EDL |
| 09 | consistency audit | cross-phase drift detection + launch gate |
| 10 | ad strategy | 1-ad-set Advantage+ campaign structure + analytics |
| 11 | ad analysis | 4Pi diagnostic + next batch ideas |
| 12 | scale engine | scaling plan (vertical + horizontal) |
| 13 | retention engine | Klaviyo/ESP lifecycle flows (post-launch) |
| 14 | content recycler | 9 derivatives from 1 winning creative (post-winner) |

Plus an intelligence layer (`.claude/lib/`) providing:
- **Compliance pre-flight** — scores ad/page copy for Meta/FTC/FDA risk before submit (blocking gate)
- **KB index** — catalog of 541 named frameworks; each skill pulls the exact systems by name
- **Creative DNA** — learns what works for this member's avatar over time
- **Hook taxonomy** — 17 archetypes across the Big 4 emotions, used by skills 03/08
- **Prompt directors** — production-ready creative prompt generation (video/image)
- **Content recycler** — turns 1 winning creative into 9 format derivatives
- **Workspace index** — generates the per-product `ABRIR-AQUI.html` dashboard
- **MCP detect + TrendTrack / Refero integrations** — auto-detect optional MCPs and enrich research/design when connected
- **Automation recipes** — MCP-based deploy/sync through the Meta Ads + Shopify MCPs

> The page (07) is HTML-first: the design is generated and approved in-session as self-contained HTML+CSS (the single source of visual truth), then compiled deterministically to Liquid — no mandatory Claude Design step.

And operational rules in `.claude/rules/` (auto-loaded when relevant):

- `shopify-theme-safety.md` — pull-before-edit, `--nodelete`, silent push rejection diagnosis
- `pre-launch-gates.md` — Compliance gate + Promise↔Config gate (blocking, non-negotiable)
- `post-task-self-audit.md` — mandatory self-audit after every skill or important task (6 gates)
- `iteration-driven-refinement.md` — skills produce a draft plus an invitation to iterate, not a "done"
- `troubleshooting-patterns.md` — diagnostic tree for recurring issues
- `member-stage-awareness.md` — adapts tone/recommendation to starter/validating/scaling
- `reverse-order-insertion.md` — insert elements in descending line-number order to preserve positions
- `emergency-escape-paths.md` — 7 error scenarios, each with 2 or more paths forward

## Setup

### 1. Install Claude Code
```bash
curl -fsSL https://claude.ai/install.sh | sh          # Mac
irm https://claude.ai/install.ps1 | iex                # Windows
```

### 2. Clone and launch
```bash
git clone https://github.com/reverseeth/aura-engine.git
cd aura-engine
claude
```

### 3. Configure
Inside Claude Code, type:
```
setup
```

Follow the prompts (budget, market, tools available). Setup creates `/workspace/` with your product subfolder and a manifest.

### 4. (Optional) Connect Aura knowledge base
Full setup instructions are distributed with your Aura access. Summary:
- Desktop: Settings → Integrations → Add Custom Integration → URL `https://aura-mcp-production.up.railway.app/mcp`
- Terminal: `claude mcp add --transport http aura https://aura-mcp-production.up.railway.app/mcp`

Queries starting with `aura:` consult the knowledge base.

## Architecture

```
.claude/
├── CLAUDE.md              # main rules + auto-update hook
├── settings.json          # permissions + session hooks
├── hooks/
│   └── post-start.sh      # shell alias setup (idempotent)
├── skills/                # skill markdown files (00–14; 07 splits into 07a–d)
├── rules/                 # operational rules (auto-loaded)
│   ├── shopify-theme-safety.md
│   ├── pre-launch-gates.md
│   ├── post-task-self-audit.md
│   ├── iteration-driven-refinement.md
│   ├── troubleshooting-patterns.md
│   ├── member-stage-awareness.md
│   ├── reverse-order-insertion.md
│   └── emergency-escape-paths.md
├── lib/                   # intelligence layer
│   ├── compliance-preflight/
│   ├── content-recycler/
│   ├── creative-dna/
│   ├── hook-taxonomy/
│   ├── kb-index/          # 541 named frameworks
│   ├── mcp-detect/
│   ├── prompt-directors/
│   ├── refero-integration/
│   ├── trendtrack-integration/
│   └── workspace-index/   # ABRIR-AQUI.html dashboard generator
├── automations/           # MCP recipes
│   └── recipes/           # deploy, sync, rotate, pause
└── templates/
    ├── aura-report-template.html
    ├── aura-logo-snippet.html
    ├── aura-html-components.md
    ├── brand.md.template
    └── manifest-schema.json

workspace/                 # member data (GITIGNORED)
└── [product-slug]/        # per-product subfolder
    ├── ABRIR-AQUI.html    # dashboard — the member's entry point
    ├── manifest.json      # single source of truth
    ├── 01-product-research/   # relatorio.md / relatorio.html
    ├── 02-market-research/    # relatorio.md / relatorio.html + dados.json
    └── ...                    # one subfolder per phase (0X-stem/)

tools/
└── design-clone/          # optional design signal extractor
```

## Updates

The repo auto-pulls on each Claude Code session start (if no local changes).

You may see this message (in Portuguese) saying the repo's history was restructured and you should re-clone:
```
⚠️  Aura Engine foi atualizado com mudanças estruturais no histórico.
    Pra continuar recebendo updates automáticos, re-clone o repo:
    rm -rf ~/aura-engine
    git clone https://github.com/reverseeth/aura-engine.git ~/aura-engine
```

Just follow the instructions. Your `workspace/` content is outside the repo and stays intact.

## Privacy

- `workspace/` is gitignored — your product data, copy, campaigns, performance never leave your machine
- `.env*` and `*.key`/`*.pem` patterns are gitignored
- Never commit member-brand data in skill docs or examples (see `.claude/CLAUDE.md` rule 6b)

## License

Private — use by authorized members only.

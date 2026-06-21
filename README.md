# Aura Engine

AI-powered operating system for DTC ecommerce brands. Runs inside Claude Code.

## What it does

Orchestrates the full product-to-ads-to-retention workflow through 14 skills:

| # | Skill | Output |
|---|---|---|
| 00 | setup | profile + first manifest |
| 01 | product research | product validation + score |
| 02 | market research | VOC, awareness, sophistication, root cause |
| 03 | competitor analysis | claims, gaps, creative patterns (Whisper transcription) |
| 04 | offer builder | mechanism, research foundation, pricing, guarantee |
| 05 | copy engine | headlines, leads, advertorial, PDP copy |
| 06 | page engine | Shopify PDP deployed (Liquid 2.0, 4-variant blueprint) |
| 07 | creative engine | 3-2-2 ad briefings (scripts, hooks, texts) |
| 08 | ad strategy | CBO + Advantage+ + PGS campaign structure |
| 09 | ad analysis | 4Pi diagnostic + next batch ideas |
| 10 | scale engine | scaling plan (vertical + horizontal) |
| 11 | consistency audit | cross-phase drift detection + fix report |
| 12 | retention engine | Klaviyo/ESP lifecycle flows setup |
| 13 | bonus delivery | technical delivery pipeline for offer bonuses |
| 17 | content recycler | 9 derivatives from 1 winning creative |

Plus an intelligence layer (`.claude/lib/`) providing:
- **Compliance pre-flight** — scores ad copy for Meta/FTC/FDA risk before submit (blocking gate)
- **Creative DNA registry** — learns what works for this member's avatar over time
- **Hook taxonomy** — 17 archetypes across Big 4 emotions, used by skills 03/07/09
- **Section patterns** — 15 reusable patterns for Liquid sections (hero, proof, offer, etc)
- **Whisper transcribe** — `medium` / `turbo-large` pipeline for transcribing scaled creatives
- **Shocking stats vault** — authorized stats with a traceable source, for credible hooks
- **Design blueprint via Claude Design** — mandatory 4-variation (A/B/C/D) artifact preview before Liquid
- **Automation recipes** — MCP-based deploy/sync through the Meta Ads + Shopify MCPs

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
Full setup instructions in `/Users/gustavo/Aura.html` (user-specific distribution). Summary:
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
├── skills/                # 14 skill markdown files
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
│   ├── section-patterns/
│   ├── whisper-transcribe/
│   └── shocking-stats/
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
    ├── manifest.json      # single source of truth
    ├── 01-product-research.{md,json,html}
    ├── 02-market-research.{md,json,html}
    └── ... (outputs from each skill)

tools/
└── design-clone/          # optional design signal extractor
```

## Updates

The repo auto-pulls on each Claude Code session start (if no local changes).

If you see:
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

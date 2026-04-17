# Aura Engine

AI-powered operating system for DTC ecommerce brands. Runs inside Claude Code.

## What it does

Orchestrates the full product-to-ads workflow through 11 skills:

| # | Skill | Output |
|---|---|---|
| 00 | setup | profile + first manifest |
| 01 | product research | product validation + score |
| 02 | market research | VOC, awareness, sophistication, root cause |
| 03 | competitor analysis | claims compilation, gaps, positioning |
| 04 | offer builder | mechanism, pricing, guarantee, unit economics |
| 05 | copy engine | headlines, leads, advertorial, PDP copy |
| 06 | page engine | Shopify PDP deployed (Liquid 2.0) |
| 07 | creative engine | 3-2-2 ad briefings (scripts, hooks, texts) |
| 08 | ad strategy | CBO + Advantage+ + PGS campaign structure |
| 09 | ad analysis | 4Pi diagnostic + next batch ideas |
| 10 | scale engine | scaling plan (vertical + horizontal) |
| 17 | content recycler | 9 derivadas de 1 winner creative |

Plus an intelligence layer (`.claude/lib/`) providing:
- **Compliance pre-flight** — scores ad copy for Meta/FTC/FDA risk before submit
- **Creative DNA registry** — learns what works for this member's avatar over time
- **Stitch integration** — optional Google Stitch blueprint → Liquid pipeline
- **Automation recipes** — MCP-based deploy/sync via Meta Ads + Shopify MCPs

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
├── skills/                # 11 skill markdown files
├── lib/                   # intelligence layer
│   ├── compliance-preflight/
│   ├── content-recycler/
│   ├── creative-dna/      # SQLite + Python CRUD
│   └── stitch-integration/
├── automations/           # MCP recipes
│   └── recipes/           # deploy, sync, rotate, pause
└── templates/
    ├── aura-report-template.html
    ├── aura-logo-snippet.html
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

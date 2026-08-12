# Aura Engine

AI-powered operating system for DTC ecommerce brands. Runs inside Claude Code.

## What it does

Orchestrates the full product-to-ads-to-retention workflow through 20 skills (phases 00–14 plus optional 01b sourcing; phase 07 splits into 07a–07e):

| # | Skill | Output |
|---|---|---|
| 00 | setup | profile + first manifest + dashboard |
| 01 | product research | product validation + score |
| 01b | sourcing (optional) | supplier analysis + quote message + logistics route (DDP → 3PL) + real COGS for skill 04 |
| 02 | market research | VOC, awareness, sophistication, root cause |
| 03 | competitor analysis | claims, gaps, creative patterns (Whisper transcription) |
| 04 | offer builder | mechanism, research foundation, pricing, guarantee |
| 05 | bonus delivery | ecom bonus asset + delivery (Phase A pre-launch: assets + GWP config; Phase B post-launch: take-rate tracking) |
| 06 | copy engine | headlines, leads, advertorial, PDP copy |
| 07a | page design | HTML-first page design (brand signals + member-approved HTML) |
| 07b | page build | deterministic HTML→Liquid compile + Shopify deploy |
| 07c | tracking setup | Meta Pixel + CAPI + analytics stack |
| 07d | checkout / AOV | post-purchase upsell, cart bump, bundles, checkout trust |
| 07e | agentic readiness | AEO checklist: Agentic Storefronts channel, structured data, AI crawler access, AI visibility score (post-deploy, pre-launch) |
| 08 | creative engine | ad briefings (scripts, hooks, prompts) + EDL |
| 09 | consistency audit | cross-phase drift detection + launch gate |
| 10 | ad strategy | 1-ad-set Advantage+ campaign structure + analytics |
| 11 | ad analysis | 4Pi diagnostic + next batch ideas |
| 12 | scale engine | scaling plan (vertical + horizontal) |
| 13 | retention engine | Klaviyo/ESP lifecycle flows (Phase A pre-launch: abandoned cart + post-purchase recovery flows; Phase B post-launch: win-back/replenishment, ≥50 orders) |
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
- `post-task-self-audit.md` — mandatory self-audit after every skill or important task (5 gates, silent-fix-first)
- `iteration-driven-refinement.md` — skills produce a draft plus an invitation to iterate, not a "done"
- `troubleshooting-patterns.md` — diagnostic tree for recurring issues
- `member-stage-awareness.md` — adapts tone/recommendation to starter/validating/scaling
- `reverse-order-insertion.md` — multi-insert safety (reverse order for indexed arrays, disjoint anchors for text edits)
- `emergency-escape-paths.md` — 7 error scenarios, each with 2 or more paths forward
- `resilient-fetch.md` — WebSearch → WebFetch → Playwright fetcher cascade; never fabricate VOC/claims when a source blocks

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

### 4. Connect Aura knowledge base
Claude Code connects automatically: the repo ships a `.mcp.json` that registers the knowledge base, so the first time you open Claude Code in this folder it asks permission to use the `aura` server — approve it and you're connected. An access key is required — it's in the setup guide distributed with your Aura access (`docs/aura-setup-pt.html`). Export it before opening Claude Code (e.g. in `~/.zshrc`):

```bash
export AURA_KEY="YOUR_MEMBER_KEY"
```

Manual setup (Claude Desktop, or as a terminal fallback — replace `YOUR_MEMBER_KEY` with the key from the setup guide):
- Desktop: Settings → Integrations → Add Custom Integration → URL `https://aura-mcp-production.up.railway.app/mcp?key=YOUR_MEMBER_KEY`
- Terminal: `claude mcp add --transport http aura "https://aura-mcp-production.up.railway.app/mcp?key=YOUR_MEMBER_KEY"`

Queries starting with `aura:` consult the knowledge base.

## Architecture

```
.claude/
├── CLAUDE.md              # main rules
├── settings.json          # permissions + session hooks
├── hooks/
│   ├── post-start.sh      # shell alias + daily auto-update + installs the git pre-commit guard (idempotent)
│   └── pre-commit-guard.sh # blocks commits mixing workspace/ or containing secrets
├── skills/                # skill markdown files (00–14; 07 splits into 07a–e)
├── rules/                 # operational rules (auto-loaded)
│   ├── shopify-theme-safety.md
│   ├── pre-launch-gates.md
│   ├── post-task-self-audit.md
│   ├── iteration-driven-refinement.md
│   ├── troubleshooting-patterns.md
│   ├── member-stage-awareness.md
│   ├── reverse-order-insertion.md
│   ├── emergency-escape-paths.md
│   └── resilient-fetch.md
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
    ├── 01-product-research/   # product-research.md / .html
    ├── 02-market-research/    # market-research.md / .html + dados.json
    └── ...                    # one subfolder per phase (0X-stem/)

tools/
└── design-clone/          # optional design signal extractor
```

## Updates

The framework auto-updates once a day, at the first Claude Code session start of the day. The `post-start.sh` hook fetches `origin/main` and fast-forwards your clone when ALL of these hold:

- you're on the `main` branch
- your working tree is clean (tracked files only — `workspace/` is gitignored and never touched)
- the update is a pure fast-forward (no forced merges, no stash, no reset — ever)

On success you'll see `[aura] Aura atualizada (N commits novos)`. Network failures are silent (they never block your session).

**Opt out:** create the file `.claude/.no-auto-update`, or set the env var `AURA_AUTO_UPDATE=0`.

**If your clone diverged** (local commits on `main`, or the repo's history was restructured upstream), auto-update pauses and you'll see a warning. To re-sync **without losing your `workspace/`** (it lives INSIDE the repo folder — never `rm -rf` the folder directly):

```bash
mv ~/aura-engine/workspace ~/aura-workspace-backup
rm -rf ~/aura-engine
git clone https://github.com/reverseeth/aura-engine.git ~/aura-engine
rm -rf ~/aura-engine/workspace && mv ~/aura-workspace-backup ~/aura-engine/workspace
```

## Privacy

- `workspace/` is gitignored — your product data, copy, campaigns, performance never leave your machine
- `.env*` and `*.key`/`*.pem` patterns are gitignored
- A git pre-commit guard (installed automatically at session start) mechanically blocks any commit containing `workspace/` files or secrets
- Never commit member-brand data in skill docs or examples (see `.claude/CLAUDE.md` rule 11)

## License

Proprietary — source-available to authorized Aura members only. All rights reserved.

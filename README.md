# Aura Engine

AI-powered operating system for DTC ecommerce brands. Runs inside Claude Code.

## What it does

Orchestrates the full product-to-ads-to-retention workflow through 26 skills (phases 00–20 plus optional 01b sourcing; phase 07 splits into 07a–07e):

| # | Skill | Output |
|---|---|---|
| 00 | setup | profile + first manifest + dashboard |
| 01 | product research | product validation + score |
| 01b | sourcing (optional) | supplier analysis + quote message + logistics route (DDP → 3PL) + real COGS for skill 04 |
| 02 | market research | VOC, awareness, sophistication, root cause |
| 03 | competitor analysis | claims, gaps, creative patterns (Whisper transcription) |
| 04 | offer builder | mechanism, research foundation, pricing, guarantee |
| 05 | bonus delivery | ecom bonus asset + delivery (Phase A pre-launch: assets + GWP config; Phase B post-launch: take-rate tracking) |
| 06 | copy engine | headlines, leads, advertorial, PDP copy — structure modeled on a proven swipe-file specimen, then markup-audited |
| 07a | page design | HTML-first page design (brand signals + member-approved HTML) |
| 07b | page build | deterministic HTML→Liquid compile + Shopify deploy |
| 07c | tracking setup | Meta Pixel + CAPI + analytics stack |
| 07d | checkout / AOV | post-purchase upsell, cart bump, bundles, checkout trust |
| 07e | agentic readiness | AEO checklist: Agentic Storefronts channel, structured data, AI crawler access, AI visibility score (post-deploy, pre-launch) |
| 08 | creative engine | ad briefings (scripts, hooks, prompts) + EDL |
| 09 | consistency audit | cross-phase drift detection + launch gate |
| 10 | ad strategy | 1 CBO campaign → N ad sets (1 ad set = 1 concept, 3 creatives + 2 primary texts + 2 headlines), ad set count sized by testing capacity (budget ÷ target CPA) |
| 11 | ad analysis | 4Pi diagnostic + 4-class result taxonomy (loser / KPI winner / spend winner / breakthrough) + next batch ideas |
| 12 | scale engine | Scaling Protocol plan (+20% after 48-72h above target, −20% below breakeven, click-based gate) — vertical + horizontal |
| 13 | retention engine | Klaviyo/ESP lifecycle flows (Phase A pre-launch: abandoned cart + post-purchase recovery flows; Phase B post-launch: win-back/replenishment, ≥50 orders) |
| 14 | content recycler | amplification plan for 1 breakthrough creative (Track 1, default); 9 channel derivatives on request (Track 2) |
| 15 | finance engine | side consult, not a pipeline step — the brand's financial model in two data-decided modes: **A (plan**, no closed month: monthly model with fixed costs in, contribution margin, CAC floor, 90-day cash need, DTC benchmarks) and **B (measure**, ≥1 closed month: the 4 levers, cohorts with decay and measured LTV, 90-day payback, scale ceiling, ~105-day cash conversion cycle, weekly banking sheet). Computes the ROAS spiral and publishes the break-even ROAS with fixed costs that skills 11 and 12 read before recommending any spend cut |
| 16 | creator engine | side consult, two phases — Phase A (can start alongside 08, pre-launch): product seeding, creator casting tied to 02's sub-avatars, brief frameworks, TikTok Shop content pipeline; Phase B (only after a breakthrough confirmed by 11): recurring contracts, ambassador ladder, whitelisting, partnership ads, creator farming |
| 17 | promo engine | seasonal side skill — owns the promo window end to end (Q4/BFCM, seasonal dates, flash sales): window calendar, promo offer, the non-negotiable gate of recalculating break-even ROAS/CPA with the promo margin before any campaign goes live, Broad/WARM60/HOT90 promo campaign alongside untouched evergreen, surf scaling + midnight reset, landing back on evergreen |
| 18 | team engine | side consult — when to hire (by the real constraint, never out of desperation), how to hire (scorecard before the opening, 9-step funnel, timed practical test) and how to run the team (8-week onboarding, KPIs per role, 9-box reviews, incentives, org design); for starter/validating the honest answer is usually "not yet" |
| 19 | ops engine | side consult — 12-month constraint, continuity checklist with member-confirmed status (backup account/BM, redundant payment processor, backup bank and domain, pre-order valve, key-man risk) and the business as an asset (WAFM memos, moat test, exit-ready); the backups part matters from day one |
| 20 | marketplace engine | side consult — expansion gate first (proven Meta + site, demand overflowing), then Amazon, TikTok Shop and an affiliate program as secondary sales channels, each tracked per channel; porting paid campaigns to other ad platforms stays with skill 14 |

Plus an intelligence layer (`.claude/lib/`) providing:
- **Ad taxonomy** — the single canon for paid-media decisions: testing capacity (`assets = daily budget ÷ target CPA`, $100-150/day floor, ~3× target CPA ceiling per ad set, max 5 test ad sets under $1k/day), the CBO structure where 1 ad set = 1 concept, the 4 result classes (loser / KPI winner / spend winner / breakthrough — only breakthrough unlocks scale and recycling), kill rules, hook & hold rates, the Scaling Protocol and the parallel-ABO promotion that replaced the champions ad set, plus what can and cannot be automated (Meta refuses performance conditions on CBO; two protection automations are mandatory and ship disabled). Read by skills 08/10/11/12/14/17 — no skill redefines these locally
- **Unit economics** — the single canon for margin and spend decisions: full variable-cost stack, contribution margin vs profit (never label "profit" a number that hasn't subtracted fixed costs), first vs repeat order, CAC ≠ platform CPA, and the ROAS spiral (cutting spend on a ROAS dip can deepen the loss — no cut recommendation ships without fixed costs on the table). Skill 15 owns the full model the canon declares (4 levers, cohorts, cash cycle) and publishes the numbers the others read. Read by skills 04/11/12/15
- **Ad log** — the canon for account-change records: an append-only `ad-log.md` per product, one line per executed change (entity, change with values, executor, short reason). Written at execution time by skills 10/12/14/17 and the automation recipes; read by 11 at the start of every analysis and by 12 before scaling
- **Compliance pre-flight** — scores ad/page copy for Meta/FTC/FDA risk before submit (blocking gate)
- **KB index** — catalog of 1,309 named framework entries across 19 domains (some systems appear in more than one domain when they serve different skills); each skill pulls the exact systems by name
- **Swipe models** — 12 proven structural specimens (Agora 11-block promo, Haddad VSL chassis, Identity Lead, Halbert skeleton, Schwartz space ad…) selected by awareness × sophistication × page type, so skill 06 models copy on a piece that actually converted instead of writing from theory alone — plus the Milligan markup audit as a QA rubric (4 U's, 4 emotions, Objection→Claim→Proof→Benefit loop, 12-defect sheet)
- **Creative DNA** — learns what works for this member's avatar over time
- **Hook taxonomy** — 17 archetypes across the Big 4 emotions, used by skills 03/08
- **Prompt directors** — production-ready creative prompt generation (video/image)
- **Content recycler** — format specs behind Track 2 of skill 14 (1 breakthrough creative into 9 channel derivatives)
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
- `report-only-results.md` — every workspace report carries the final result only: no process narration, no describing what the doc leaves out, no references to the conversation

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
├── skills/                # skill markdown files (00–20; 07 splits into 07a–e)
├── rules/                 # operational rules (auto-loaded)
│   ├── shopify-theme-safety.md
│   ├── pre-launch-gates.md
│   ├── post-task-self-audit.md
│   ├── iteration-driven-refinement.md
│   ├── troubleshooting-patterns.md
│   ├── member-stage-awareness.md
│   ├── reverse-order-insertion.md
│   ├── emergency-escape-paths.md
│   ├── resilient-fetch.md
│   └── report-only-results.md
├── lib/                   # intelligence layer
│   ├── ad-log/            # canon: append-only log of every executed account change
│   ├── ad-taxonomy/       # canon: testing capacity, 4 result classes, kill rules, Scaling Protocol
│   ├── unit-economics/    # canon: contribution margin, CAC, the ROAS spiral
│   ├── swipe-models/      # 12 structural specimens + the markup audit rubric
│   ├── compliance-preflight/
│   ├── content-recycler/
│   ├── creative-dna/
│   ├── design-presets/
│   ├── hook-taxonomy/
│   ├── kb-index/          # 1,309 named framework entries, 19 domains
│   ├── mcp-detect/
│   ├── prompt-directors/
│   ├── refero-integration/
│   ├── shopify-section-patterns/
│   ├── theme-verify/
│   ├── trendtrack-integration/
│   ├── web-fetch/
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

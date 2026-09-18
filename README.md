# Aura Engine

AI-powered operating system for DTC ecommerce brands. Runs inside Claude Code.

## What it does

Orchestrates the full product-to-ads-to-retention workflow through 26 skills (a 21-step canonical sequence plus the optional `sourcing` and six side engines; the storefront phase splits into `page-design`, `page-build`, `tracking-setup`, `checkout-aov` and `agentic-readiness`):

<!-- gen:readme-table:start -->
| Step | Skill | Legacy ID | Output |
|---|---|---|---|
| 1 | Setup (`setup`) | 00 | profile + first manifest + dashboard |
| side | Ops Engine (`ops-engine`) | 19 | side consult — 12-month constraint, continuity checklist with member-confirmed status (backup account/BM, redundant payment processor, backup bank and domain, pre-order valve, key-man risk) and the business as an asset (WAFM memos, moat test, exit-ready); the backups part matters from day one |
| 2 | Product Research (`product-research`) | 01 | brand discovery on TrendTrack (native ads, image + video, fixed filters; MCP or manual), per-brand file (top LP, top ads, traffic, offer, mechanisms), Google Trends + Trustpilot 1-2★ validation, recombination plays (never clone, never from zero), 8-axis score, brand bank in Notion or HTML |
| parallel (optional) | Sourcing (`sourcing`) | 01b | supplier analysis + quote message + logistics route (DDP → 3PL) + real COGS for skill `offer-builder` |
| 3 | Market Research (`market-research`) | 02 | VOC, awareness, sophistication, root cause |
| 4 | Competitor Analysis (`competitor-analysis`) | 03 | claims, gaps, creative patterns (Whisper transcription) |
| 5 | Offer Builder (`offer-builder`) | 04 | mechanism, proof bank, pricing, guarantee |
| side | Finance Engine (`finance-engine`) | 15 | side consult, not a pipeline step — the brand's financial model in two data-decided modes: **A (plan**, no closed month: monthly model with fixed costs in, contribution margin, CAC floor, 90-day cash need, DTC benchmarks) and **B (measure**, ≥1 closed month: the 4 levers, cohorts with decay and measured LTV, 90-day payback, scale ceiling, ~105-day cash conversion cycle, weekly banking sheet). Computes the ROAS spiral and publishes the break-even ROAS with fixed costs that skills `ad-analysis` and `scale-engine` read before recommending any spend cut |
| 6 | Copy Engine (`copy-engine`) | 06 | headlines, leads, advertorial, PDP copy — structure modeled on a proven swipe-file specimen, then markup-audited |
| 7 | Page Design (`page-design`) | 07a | HTML-first page design (brand signals + member-approved HTML) |
| 8 | Page Build (`page-build`) | 07b | deterministic HTML→Liquid compile + Shopify deploy |
| 9 | Tracking Setup (`tracking-setup`) | 07c | Meta Pixel + CAPI + analytics stack |
| 10 | Checkout & AOV (`checkout-aov`) | 07d | post-purchase upsell, cart bump, bundles, checkout trust |
| 11 · 20 (two-phase) | Bonus Delivery (`bonus-delivery`) | 05 | ecom bonus asset + delivery (Phase A pre-launch: assets + GWP config; Phase B post-launch: take-rate tracking) |
| 12 · 19 (two-phase) | Retention Engine (`retention-engine`) | 13 | Klaviyo/ESP lifecycle flows (Phase A pre-launch: abandoned cart + post-purchase recovery flows; Phase B post-launch: win-back/replenishment, ≥50 orders) |
| 13 | Creative Engine (`creative-engine`) | 08 | ad briefings (scripts, hooks, prompts) + EDL |
| side | Creator Engine (`creator-engine`) | 16 | side consult, two phases — Phase A (can start alongside `creative-engine`, pre-launch): product seeding, creator casting tied to the `market-research` sub-avatars, brief frameworks, TikTok Shop content pipeline; Phase B (only after a breakthrough confirmed by `ad-analysis`): recurring contracts, ambassador ladder, whitelisting, partnership ads, creator farming |
| 14 | Agentic Readiness (`agentic-readiness`) | 07e | AEO checklist: Agentic Storefronts channel, structured data, AI crawler access, AI visibility score (post-deploy, pre-launch) |
| 15 | Consistency Audit (`consistency-audit`) | 09 | cross-phase drift detection + launch gate |
| 16 | Ad Strategy (`ad-strategy`) | 10 | 1 CBO campaign → N ad sets (1 ad set = 1 concept, 3 creatives + 2 primary texts + 2 headlines), ad set count sized by testing capacity (budget ÷ target CPA) |
| 17 | Ad Analysis (`ad-analysis`) | 11 | 4Pi diagnostic + 4-class result taxonomy (loser / KPI winner / spend winner / breakthrough) + next batch ideas |
| 18 | Scale Engine (`scale-engine`) | 12 | Scaling Protocol plan (+20% after 48-72h above target, −20% below breakeven, click-based gate) — vertical + horizontal |
| side | Promo Engine (`promo-engine`) | 17 | seasonal side skill — owns the promo window end to end (Q4/BFCM, seasonal dates, flash sales): window calendar, promo offer, the non-negotiable gate of recalculating break-even ROAS/CPA with the promo margin before any campaign goes live, Broad/WARM60/HOT90 promo campaign alongside untouched evergreen, surf scaling + midnight reset, landing back on evergreen |
| side | Team Engine (`team-engine`) | 18 | side consult — when to hire (by the real constraint, never out of desperation), how to hire (scorecard before the opening, 9-step funnel, timed practical test) and how to run the team (8-week onboarding, KPIs per role, 9-box reviews, incentives, org design); for starter/validating the honest answer is usually "not yet" |
| 21 | Content Recycler (`content-recycler`) | 14 | amplification plan for 1 breakthrough creative (Track 1, default); 9 channel derivatives on request (Track 2) |
| side | Marketplace Engine (`marketplace-engine`) | 20 | side consult — expansion gate first (proven Meta + site, demand overflowing), then Amazon, TikTok Shop and an affiliate program as secondary sales channels, each tracked per channel; porting paid campaigns to other ad platforms stays with skill `content-recycler` |
<!-- gen:readme-table:end -->

Plus an intelligence layer (`.claude/lib/`) providing:
- **Ad taxonomy** — the single canon for paid-media decisions: testing capacity (`assets = daily budget ÷ target CPA`, $100-150/day floor, ~3× target CPA ceiling per ad set, max 5 test ad sets under $1k/day), the CBO structure where 1 ad set = 1 concept, the 4 result classes (loser / KPI winner / spend winner / breakthrough — only breakthrough unlocks scale and recycling), kill rules, hook & hold rates, the Scaling Protocol and the parallel-ABO promotion that replaced the champions ad set, plus what can and cannot be automated (Meta refuses performance conditions on CBO; two protection automations are mandatory and ship disabled). Read by skills `creative-engine`/`ad-strategy`/`ad-analysis`/`scale-engine`/`content-recycler`/`promo-engine` — no skill redefines these locally
- **Unit economics** — the single canon for margin and spend decisions: full variable-cost stack, contribution margin vs profit (never label "profit" a number that hasn't subtracted fixed costs), first vs repeat order, CAC ≠ platform CPA, and the ROAS spiral (cutting spend on a ROAS dip can deepen the loss — no cut recommendation ships without fixed costs on the table). Skill `finance-engine` owns the full model the canon declares (4 levers, cohorts, cash cycle) and publishes the numbers the others read. Read by skills `offer-builder`/`ad-analysis`/`scale-engine`/`finance-engine`
- **Ad log** — the canon for account-change records: an append-only `ad-log.md` per product, one line per executed change (entity, change with values, executor, short reason). Written at execution time by skills `ad-strategy`/`scale-engine`/`promo-engine` and the automation recipes; read by `ad-analysis` at the start of every analysis and by `scale-engine` before scaling
- **KB index** — catalog of 1,309 named framework entries across 19 domains (some systems appear in more than one domain when they serve different skills); each skill pulls the exact systems by name
- **Swipe models** — 12 proven structural specimens (Agora 11-block promo, Haddad VSL chassis, Identity Lead, Halbert skeleton, Schwartz space ad…) selected by awareness × sophistication × page type, so skill `copy-engine` models copy on a piece that actually converted instead of writing from theory alone — plus the Milligan markup audit as a QA rubric (4 U's, 4 emotions, Objection→Claim→Proof→Benefit loop, 14-defect sheet)
- **Creative DNA** — learns what works for this member's avatar over time
- **Hook taxonomy** — 17 archetypes across the Big 4 emotions, used by skills `competitor-analysis`/`creative-engine`
- **Prompt directors** — production-ready creative prompt generation (video/image)
- **Content recycler** — format specs behind Track 2 of skill `content-recycler` (1 breakthrough creative into 9 channel derivatives)
- **Workspace index** — generates the per-product `ABRIR-AQUI.html` dashboard
- **Metadata cleaner** (`tools/limpador-de-metadados/`) — every creative goes through it before upload: strips EXIF/XMP/IPTC/C2PA and generator job ids without touching a pixel or a frame, renames to `asset-xxxx` in place; drag-and-drop app for the member (the session hook drops the launcher for their own OS in the repo root) + CLI for the skills
- **MCP detect + TrendTrack / Notion / Refero integrations** — auto-detect optional MCPs; TrendTrack drives product discovery, Notion stores the brand bank, Refero feeds brand signals
- **Automation recipes** — MCP-based deploy/sync through the Meta Ads + Shopify MCPs

> The page (`page-design` → `page-build`) is HTML-first: the design is generated and approved in-session as self-contained HTML+CSS (the single source of visual truth), then compiled deterministically to Liquid. Three design routes: from scratch on the Claude Design canvas (default), cloning a full page saved with SingleFile, or assembling one page out of several references.

And operational rules in `.claude/rules/` (auto-loaded when relevant):

- `shopify-theme-safety.md` — pull-before-edit, `--nodelete`, silent push rejection diagnosis
- `post-task-self-audit.md` — mandatory self-audit after every skill or important task (5 gates, silent-fix-first)
- `iteration-driven-refinement.md` — skills produce a draft plus an invitation to iterate, not a "done"
- `troubleshooting-patterns.md` — diagnostic tree for recurring issues
- `member-stage-awareness.md` — adapts tone/recommendation to starter/validating/scaling
- `reverse-order-insertion.md` — multi-insert safety (reverse order for indexed arrays, disjoint anchors for text edits)
- `emergency-escape-paths.md` — 7 error scenarios, each with 2 or more paths forward
- `resilient-fetch.md` — WebSearch → WebFetch → Playwright fetcher cascade; never fabricate VOC/claims when a source blocks
- `report-only-results.md` — every workspace report carries the final result only: no process narration, no describing what the doc leaves out, no references to the conversation
- `report-language.md` — language and writing style of every internal report and of the conversation with the member (rule 0 of CLAUDE.md in full, plus the seven plain-writing rules); single source, CLAUDE.md keeps only the summary

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
Claude Code connects automatically: the repo ships a `.mcp.json` that registers the knowledge base, so the first time you open Claude Code in this folder it asks permission to use the `aura` server. Approve it and you're connected. Nothing else to configure.

Manual setup (Claude Desktop, or as a terminal fallback):
- Desktop: Settings → Connectors (older versions: Integrations) → Add custom connector → URL `https://aura-mcp-production.up.railway.app/mcp`
- Terminal: `claude mcp add --transport http aura "https://aura-mcp-production.up.railway.app/mcp"`

Queries starting with `aura:` consult the knowledge base.

## Architecture

```
.claude/
├── CLAUDE.md              # main rules
├── settings.json          # permissions + session hooks
├── hooks/
│   ├── post-start.sh      # shell alias + daily auto-update + installs the git pre-commit guard + runs pending workspace migrations (idempotent)
│   ├── post-skill.sh      # Stop hook: runs aura-status on any product touched in the last 30 min and shows up to 10 lines
│   └── pre-commit-guard.sh # blocks commits mixing workspace/ or containing secrets
├── skills/                # one skill per id, all 26 in the native format: `<id>/SKILL.md` (the script) + `<id>/reference/*.md` (the supporting material each step opens)
├── rules/                 # operational rules (auto-loaded)
│   ├── shopify-theme-safety.md
│   ├── post-task-self-audit.md
│   ├── iteration-driven-refinement.md
│   ├── troubleshooting-patterns.md
│   ├── member-stage-awareness.md
│   ├── reverse-order-insertion.md
│   ├── emergency-escape-paths.md
│   ├── resilient-fetch.md
│   ├── report-only-results.md
│   └── report-language.md
├── lib/                   # intelligence layer
│   ├── ad-log/            # canon: append-only log of every executed account change
│   ├── ad-taxonomy/       # canon: testing capacity, 4 result classes, kill rules, Scaling Protocol
│   ├── auto-update/       # the agent's full auto-update protocol (CLAUDE.md keeps a 5-line summary)
│   ├── unit-economics/    # canon: contribution margin, CAC, the ROAS spiral
│   ├── swipe-models/      # 12 structural specimens + the markup audit rubric
│   ├── content-recycler/
│   ├── creative-dna/
│   ├── design-presets/     # palette generator (3 candidates, WCAG AA) + the 8 presets it starts from
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
    ├── manifest-schema.json
    └── schemas/           # one draft-07 schema per phase dados.json (13 skills)

workspace/                 # member data (GITIGNORED)
├── ABRIR-AQUI.html        # global dashboard, one card per product (build_index.py --global)
└── [product-slug]/        # per-product subfolder
    ├── ABRIR-AQUI.html    # dashboard — the member's entry point
    ├── manifest.json      # single source of truth
    ├── product-research/   # product-research.md / .html + dados.json + banco-de-marcas.md (+ .html when Notion is not connected)
    ├── market-research/    # market-research.md / .html + dados.json
    └── ...                    # one subfolder per phase, named after the skill id (`<id>/`)

tools/
├── render_report.py       # renders every .md report into its .html companion (template, logo, TOC; nothing hand-written)
├── gen_docs.py            # regenerates the docs derived from .claude/skills.json (incl. .claude/OVERVIEW.html)
├── aura-check.py          # framework lint (paths, skill ids, secrets, generated docs)
├── migrate.py / migrations/  # workspace layout migrations (run by the session hook)
├── manifest.py            # the only way skills write manifest.json: get / set / complete / validate (backup + schema validation)
├── aura-status.py         # verifiable product state: reports vs manifest marks, files outside the layout, dados.json vs schema
├── schema_validate.py     # minimal draft-07 validator (stdlib only) shared by manifest.py, aura-status.py and the dashboard
├── limpador-de-metadados/ # metadata cleaner (Node, zero deps): strips EXIF/XMP/IPTC/C2PA/encoder tags, lossless, renames to asset-xxxx
│   └── lancadores/        # both double-click launchers (.command / .cmd); the session hook copies the member's one to the repo root
├── strip-metadata.sh      # CLI wrapper the skills/recipes run before any upload
└── design-clone/          # optional design signal extractor

Limpador de Metadados.command|.cmd     # the launcher for THIS machine, put here by the session hook (git-ignored)
```

## Updates

The framework auto-updates once a day, at the first Claude Code session start of the day. The `post-start.sh` hook fetches `origin/main` and fast-forwards your clone when ALL of these hold:

- you're on the `main` branch
- your working tree is clean (tracked files only — `workspace/` is gitignored and never touched)
- the update is a pure fast-forward (no forced merges, no stash, no reset — ever)

On success you'll see `[aura] Aura atualizada (N commits novos)`. Network failures are silent (they never block your session).

**Opt out:** create the file `.claude/.no-auto-update`, or set the env var `AURA_AUTO_UPDATE=0`.

**If your clone diverged** (local commits on `main`, or the repo's history was restructured upstream), auto-update pauses and you'll see a warning. Re-syncing means a fresh clone, and a fresh clone only brings back what's on GitHub. Everything local-only lives INSIDE the repo folder and has to be carried over by hand: `workspace/`, `docs/historico/` (internal working docs, if you have it) and your local config files. So rename the old clone instead of deleting it:

```bash
mv ~/aura-engine ~/aura-engine-old
git clone https://github.com/reverseeth/aura-engine.git ~/aura-engine
rm -rf ~/aura-engine/workspace
mv ~/aura-engine-old/workspace ~/aura-engine/workspace
[ -d ~/aura-engine-old/docs/historico ] && mv ~/aura-engine-old/docs/historico ~/aura-engine/docs/historico
```

Nothing is lost while `~/aura-engine-old` still exists. Before removing it, run `git status --ignored --porcelain | grep '^!!'` inside it to list anything else that was local-only (`.env`, local settings, internal notes) and move over what you still need.

## Privacy

- `workspace/` is gitignored — your product data, copy, campaigns, performance never leave your machine
- `.env*` and `*.key`/`*.pem` patterns are gitignored
- A git pre-commit guard (installed automatically at session start) mechanically blocks any commit containing `workspace/` files or secrets
- Never commit member-brand data in skill docs or examples (see `.claude/CLAUDE.md` rule 11)

## License

Proprietary — source-available to authorized Aura members only. All rights reserved.

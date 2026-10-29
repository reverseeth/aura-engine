# Setup · Referência: Onboarding por texto e auto-extração da loja (ETAPAs 3 e 4)

> A mensagem única com as 4 perguntas (situação, budget, ferramentas e ESP, links), o parse das variáveis com os tokens exatos do enum, a classificação interna do budget e a extração automática da página do produto (dados, cores e fontes) pela cascade de coleta resiliente. Abra na ETAPA 3.

### ETAPA 3 — Onboarding do Membro (Perguntas por Texto)

O onboarding é feito por perguntas de texto simples. Apresente as 4 perguntas numa única mensagem bem formatada e peça pro membro responder numa mensagem só, no formato que preferir. Isso reduz fricção e funciona em qualquer ambiente (inclusive dentro do Claude Code, que não tem TTY interativo).

**Use o idioma escolhido na ETAPA 2.6.** Se `REPORT_LANGUAGE = "en"`, traduz as 4 perguntas pra inglês.

Formato da mensagem a enviar:

> Preciso de 4 respostas rápidas pra salvar seu profile:
>
> **1. Situação atual:**
> - A) Não tenho produto — quero encontrar um
> - B) Tenho produto mas ainda não lancei
> - C) Já estou vendendo mas não escalo
> - D) Já escalo e quero otimizar
>
> **2. Budget diário pra ads** (em dólares — ex: `100`)
>
> **3. Ferramentas que você tem acesso** (marca as que se aplicam): TrendTrack · Higgsfield · Notion (pra guardar o banco de marcas da pesquisa de produto)
>  → Sem TrendTrack, que é o motor da pesquisa de produto: https://app.trendtrack.io/invite/tt-d0b18d189489 dá 20% de desconto nos 3 primeiros meses.
>
> **3b. Plataforma de email (ESP)** que você usa — escolha uma:
> - A) Klaviyo
> - B) Omnisend / MailerLite / Shopify Email
> - C) Nenhum ainda
>
> **4. Link da sua loja e do produto principal** (se A, pula)
>  → Se tem Shopify, link da loja Shopify também.

Depois que o membro responder, parseie a resposta e extraia:
- `SITUACAO` → A, B, C ou D
- `BUDGET` → número em dólares
- `TOOLS` → lista das ferramentas mencionadas (TrendTrack, Higgsfield, Notion)
- `ESP` → plataforma de email escolhida na 3b: `klaviyo` (A), `omnisend` / `mailerlite` / `shopify_email` conforme o que o membro citar (B), ou `none` (C) — tokens EXATOS do enum do manifest-schema (`shopify_email` com underscore, nunca hífen)
- `LINK` → URL do produto principal (se SITUACAO ≠ A)
- `SHOPIFY_LINK` → URL da loja Shopify (se o membro informar a loja na pergunta 4)

Se o membro esquecer alguma resposta essencial, pergunte APENAS o que faltou — não re-apresente tudo.

Classifique o budget internamente pra uso futuro (não mostre ao membro). Intervalos fechados, sem sobreposição:
- < $50/dia → starter
- $50-199/dia → standard
- $200-999/dia → escala-inicial
- ≥ $1000/dia → escala-avançada

Capture TODAS as respostas (`SITUACAO`, `BUDGET`, `TOOLS`, `ESP`, `LINK`, `SHOPIFY_LINK`) pra usar na Etapa 4 (auto-extração) e Etapa 5 (salvar profile).

### ETAPA 4 — Auto-Extração de Dados da Loja

SE o membro forneceu link do produto, faça **web fetch da página** automaticamente antes de salvar o profile. Extraia:

- Nome do produto
- Preço (incluindo bundles se visíveis)
- Descrição principal
- Principais features/ingredientes
- Hero headline e sub-headline
- Se tem guarantee (tipo + duração)
- Tipo de hero section (vídeo, imagem, gif)
- Presença de mecanismo único (sim/não + nome se tiver)
- Link de checkout
- **Cores e fontes da marca** — vão para `workspace/[produto]/brand/brand-tokens.json` (DTCG, 8 papéis de cor e as famílias heading e body), não para hex soltos no profile. Ordem:
  1. **dembrandt** (MCP `mcp__plugin_dembrandt_dembrandt__*`): `check_robots` na URL da loja (é a marca do próprio membro, mas o robots vale igual), `get_design_tokens` na URL da loja ou do site, sem `sync` (devolve um `job_id`; acompanhe com `get_job_status`) e `export_dtcg` com esse `job_id`. Salve o export em `workspace/[produto]/brand/dembrandt-dtcg.json` e converta: `python3 tools/page-qa/tokens.py --from-dtcg workspace/[produto]/brand/dembrandt-dtcg.json --brand-out workspace/[produto]/brand/brand-tokens.json`. O script deriva os papéis que faltarem e recusa (exit 4) sobrescrever uma marca que já existe.
  2. **Reserva** (dembrandt ausente, robots barrando ou extração vazia): os 3 a 5 hex dominantes e as `font-family` heading e body pelo CSS cru, na cascade abaixo; a page-design monta o arquivo com eles depois.
  3. **Sem loja nem site:** grave a forma vazia, `{"$extensions": {"aura": {"source": "none"}}}`.

  Depois de gravar, valide: `python3 tools/schema_validate.py .claude/templates/schemas/brand.brand-tokens.schema.json workspace/[produto]/brand/brand-tokens.json`. Situação A não tem slug ainda: o arquivo não nasce aqui, e a page-design cria a forma vazia quando chegar a vez dela.

**Cascade de coleta (rule `.claude/rules/resilient-fetch.md`):** tente `WebFetch` primeiro. Se barrar (Cloudflare, 403, login wall) OU se precisar do CSS cru na reserva de cores e fontes (o WebFetch devolve markdown, sem `<style>`/classes), use o fetcher Playwright instalado na ETAPA 1: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode html` (devolve o HTML renderizado com CSS). Só depois desses dois degraus documente "não acessível" sem falhar. O importante é capturar o que consegue. Cores/fontes que não der pra extrair ficam como `[preencher]` na ETAPA 5A.

Salve tudo no profile pra servir de referência em TODAS as skills seguintes — nunca mais perguntamos essas informações ao membro.

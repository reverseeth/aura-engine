# Competitor Analysis · Referência: Análise de PDPs dos concorrentes (ETAPA 2)

> Os três sistemas a puxar, a cascade de fallbacks (fetcher da Aura, Wayback, archive.today), o safeguard de cobertura com a mensagem ao membro e tudo que documentar por PDP (estrutura da página e copy analysis). Abra na ETAPA 2.

### ETAPA 2 — Análise de PDPs dos Concorrentes

**Frameworks a puxar da base ANTES de analisar (rode cada `best_query`):**
- **Competitor Research Process (Extracting Claims)** (rode `competitor research process extracting claims messaging hooks customer feedback differentiation`) — o método de extração estruturada que organiza tudo abaixo.
- **Schwartz Market Sophistication — 5 Stages** (rode `market sophistication five stages Schwartz enlarge claim new mechanism identity skepticism`) — pra ler em que stage de sofisticação o mercado está pela forma como os concorrentes tratam o claim/mecanismo.
- **Schwartz Mechanization Stages — Name / Describe / Feature** (rode `Schwartz mechanization stages name describe feature mechanism promise reason why headline`) — pra classificar COMO cada concorrente apresenta o mecanismo (só nomeia? descreve? detalha feature?).

Pra cada concorrente, acesse a página de produto (web fetch). Se tiver cloaker/Cloudflare bloqueando, execute os fallbacks **em sequência** (pare no primeiro que retornar conteúdo válido > 500 bytes):

**Tentativa 1 — Fetcher Playwright da Aura (navegador real — resolve Cloudflare/429/JS na maioria dos casos; rule `.claude/rules/resilient-fetch.md`):**
```bash
python3 .claude/lib/web-fetch/fetch.py "<url-da-pdp>" --mode text --json
```
Se vier `blocked: false`, use o conteúdo — é a página **AO VIVO** (melhor que snapshot). É a tentativa preferencial.

**Tentativa 2 — Wayback Machine**:
- Consulte `https://archive.org/wayback/available?url=<url>` e valide que `archived_snapshots.closest` existe e `timestamp` é dos últimos 365 dias.
- Se houver, faça fetch do snapshot.

**Tentativa 3 — archive.today**:
- Tente `https://archive.ph/newest/<url>` e valide redirect para snapshot real.

**Se NENHUM fallback funcionar** (hard-CAPTCHA tipo PerimeterX, ou todos caíram): pule esse concorrente específico (**não aborte a skill inteira**). Registre em `dados.json.competitors_discarded[]` a sequência de tentativas (`aura_fetch`, `wayback`, `archive_today`) e o motivo do descarte. Continue para os demais concorrentes.

**Safeguard de integridade — threshold crítico de acessibilidade:**

Depois de tentar todos os concorrentes + todos os fallbacks, calcule:

```
access_rate = concorrentes_com_PDP_analisada / total_concorrentes_identificados
```

- `access_rate >= 0.5` → proceder normalmente
- `0.3 <= access_rate < 0.5` → proceder com WARNING no output: `"Cobertura parcial — {N}/{total} concorrentes inacessíveis. Análise competitiva pode ter gaps. Considere análise manual via screenshots."`
- `access_rate < 0.3` → **PARAR SKILL E PEDIR AÇÃO DO MEMBRO**. Não proceder com análise baseada em < 30% do universo competitivo, senão Skills `offer-builder`/`copy-engine` vão assumir "mercado limpo" (falsa premissa). Mensagem:

  > ⚠️  Só consegui acessar {N}/{total} ({access_rate:.0%}) das PDPs de concorrentes. O resto bloqueou por bot-protection (Cloudflare, Shopify App check, etc) e todos os fallbacks falharam.
  >
  > Sem análise competitiva real, Skills `offer-builder` (Offer) e 06 (Copy) vão voar no escuro. Opções:
  > 1. Me manda screenshots dos concorrentes inacessíveis por WhatsApp/paste
  > 2. Passa pra mim dados do SpyBox/Kalodata sobre claims e estrutura deles
  > 3. Adia competitor analysis até conseguir acesso (mudar IP, VPN, etc)
  >
  > O que prefere?

**Pra cada PDP, documente:**

**Estrutura da página (aplicando frameworks):**
- **Tipo de hero section**: autoridade (expert/doctor), UGC/testimonial, product-hero, problem-agitate, lifestyle, demo/before-after
- **Headline principal exata** (copie literalmente)
- **Sub-headline exata**
- **Como apresenta o produto**: foto, vídeo (quanto tempo?), GIF, demonstração
- **Bullet points de benefício** (copie as primeiras 5)
- **Mecanismo único?** Qual nome? Como apresenta? (ingredient, process, tech, combo). Classifique a apresentação pelos **Schwartz Mechanization Stages** (Name / Describe / Feature): só dá nome ao mecanismo, descreve como funciona, ou detalha cada feature? O stage de mecanização revela em que ponto da sofisticação o concorrente acha que o mercado está.
- **Stack visual de valor?** Quantos itens? Com ancoragem de preço?
- **Preço**: base + bundles oferecidos (2-pack, 3-pack, subscription) com % savings
- **Guarantee**: tipo (money-back, satisfaction, results-based), duração (30/60/90 dias), copy exata
- **Social proof**: tipo (reviews count + média, UGC, mídia, certificações, endorsements)
- **FAQ**: quais perguntas aborda? Quantas?
- **CTAs**: quantos, onde, que copy usa nos botões
- **Shipping**: grátis? a partir de quanto? tempo estimado?
- **Aplicação dos 15 Fatores de Funil**: quais fatores a página cobre bem, quais ignora

**Copy analysis (frameworks):**
- **Tipo de lead** (Story, Secret, Proclamation, Problem-Solution, Direct/Offer — identificar aplicando os 5 tipos de lead por awareness de Schwartz)
- **Nível de awareness que a página assume** do visitante (dita onde no funil essa LP está)
- **Gatilhos de persuasão usados** (escassez, autoridade, prova social, reciprocidade, compromisso — identifique quais da lista dos 6 de Cialdini). Anote também se o concorrente usa **Vampire Claims / Vampire Video** (rode `vampire claims vampire video mosaic structure architectural support single USP`) — elementos chamativos que roubam atenção do claim central, sinal de página mal-arquitetada que você pode explorar.
- **Grande promessa** (qual é? quão específica?)
- **Quais objeções a página tenta quebrar** (com que técnica)
- **Tom de voz** (sofisticado, casual, técnico, emocional, urgente, educativo)
- **Congruência ad→página**: se o concorrente tem ads ativos, a LP espelha o ad? (Message match, visual match, promise match)

# Page Design · Referência: Rota 1, clone-and-adapt (sub-etapa 3.3)

> A regra legal e ética, o comando `aura_clone.py clone-and-adapt`, a cascade de captura em quatro degraus (downloader, single-file, screenshot por visão, extensão SingleFile manual), a reconciliação com o plano da ETAPA 1, a geração do `page.html` e a variante de clone fiel seção a seção em quatro passos. Abra na sub-etapa 3.3.

### 3.3 Rota 1 — Clone-and-adapt

O membro indica 1 URL de concorrente. A Aura captura a **ESTRUTURA** dessa página (ordem de sections, hierarquia, layout) e a usa como **ponto de partida**, trocando TODO o conteúdo pelo do membro.

> **REGRA LEGAL E ÉTICA (inegociável):** capturar estrutura/layout e trocar 100% do conteúdo (copy, imagens, marca, paleta) é defensável. Copiar 1:1 não é. **NÃO** reaproveite copy, imagens, logos, nome de marca ou claims do concorrente — só o esqueleto de layout como direção. A copy vem SEMPRE de `copy-engine/dados.json`, a oferta de `offer-builder/dados.json`, a paleta/tipografia dos `design-signals` da ETAPA 2.

1. Peça a URL: *"Me passa a URL da página de concorrente que você acha boa. Vou pegar só o esqueleto de layout dela (não a copy nem as imagens) e montar a SUA versão por cima."*
2. Capture a estrutura via o subcomando `clone-and-adapt` do `aura_clone.py` (orquestra downloader → analyzer → skeleton-builder numa chamada):
   ```bash
   python3 tools/design-clone/aura_clone.py clone-and-adapt "URL" --output=/tmp/clone-[produto] --product=[produto]
   ```
   Ele emite `skeleton.html` (sections só com estrutura/placeholder, ordem+tipo+layout do concorrente, ZERO copy/imagem/marca) + `skeleton.json`. Esse esqueleto é o que você preenche com a copy de `06` e a oferta de `04`. (Os scripts `downloader.py`/`analyzer.py` rodam por baixo — não os chame soltos; o `analyzer.py` sozinho não gera o skeleton.) Exit codes do wrapper: `0` sucesso · `1` input inválido · `2` pipeline incompleto (ver manifest/stderr).

   **Cascade de captura (degraus 1-2 são AUTOMÁTICOS dentro do wrapper; 3-4 são a degradação):**

   - **Degrau 1 — `downloader.py` (Playwright stealth):** roda primeiro, é o único que extrai DOM com fidelidade máxima.
   - **Degrau 2 — `snapshot.py` (single-file-cli), automático:** se o DOM falhar, o `--engine=auto` (default) já cai sozinho pro motor SingleFile — não precisa invocar nada. Requer Node >= 20; se ausente, o wrapper pula esse degrau e segue a degradação.
   - **Degrau 3 — screenshot→visão (ES1-style):** se nenhuma engine pegou DOM, o wrapper grava `raw/fallback-screenshot.png` e marca `"mode": "screenshot_fallback"` + `"skeleton": null` no manifest. Leia o PNG por visão nativa (Read) pra derivar a estrutura. **EXCEÇÃO — challenge detectado:** se `raw/fallback.json` marcar `challenge_detected: true`, o screenshot é o interstitial do Cloudflare ("Just a moment…"/Turnstile) — NÃO leia por visão (derivaria estrutura de uma tela de bloqueio); vá DIRETO pro degrau 4.
   - **Degrau 4 — MANUAL via extensão SingleFile (vence Cloudflare/login, 1 clique):** peça ao membro, com instrução mastigada:
     > "Instala a extensão **SingleFile** no Chrome (https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle), abre a página do concorrente normalmente no SEU Chrome (logado, sem tela de bloqueio), clica no ícone da extensão — ela salva a página inteira num único arquivo .html em Downloads. Me manda o caminho do arquivo (ou arrasta ele pro chat)."

     Ingira o arquivo com o mesmo pipeline (não precisa de browser nem de Node):
     ```bash
     python3 tools/design-clone/aura_clone.py clone-and-adapt --from-file=<arquivo.html> --output=/tmp/clone-[produto]
     ```
     O browser real do membro é imune a anti-bot — esse degrau resolve o que os automáticos não conseguem. O .html salvo é material de trabalho (referência de concorrente): vive em `/tmp`/workspace, JAMAIS é commitado (rule 11).
3. **Reconcilie com o plano da ETAPA 1.** O esqueleto do concorrente é referência de layout, mas a verdade estratégica é o seu `sections_plan` (que veio do awareness/sophistication do SEU produto). Onde o concorrente tem sections que o seu plano não pede (ex: gift-guide irrelevante), descarte. Onde o seu plano pede sections que o concorrente não tem (ex: `mechanism` porque você tem mecanismo único real), adicione. O layout do concorrente informa hierarquia e ritmo; o conteúdo e a seleção de sections são seus.
4. **Gere `design/page.html`** aplicando: a estrutura reconciliada, a copy REAL de `06`, a oferta de `04`, os `design-signals` da ETAPA 2 (paleta/tipografia/radius/density) e as **imagens do mapa de mídia da 1.6** (`design/assets/` — jamais as imagens do concorrente). Uma única variação fiel ao layout-base é suficiente aqui (o membro já escolheu a referência); ofereça iterar se quiser ajustar densidade/paleta.

**Variante — clone fiel seção a seção (página inteira como sections editáveis):** quando o membro tem o snapshot completo da página de referência (o arquivo .html salvo com a extensão SingleFile — degrau 4 da cascade) e quer a ESTRUTURA INTEIRA reproduzida como sections OS 2.0 (o formato de tema do Shopify em que cada section é editável no theme editor), não só o esqueleto, o trabalho segue 4 passos:

1. **Serializar o DOM por seção**, com estilos computados em desktop E mobile + screenshot de cada seção. O par geometria+imagem é o contrato de fidelidade: os estilos computados dão as medidas exatas, o screenshot mostra como a seção deve ficar — a conversão só está certa quando os dois batem.
2. **Converter seção a seção** — trabalho paralelizável (1 agente por seção). Cada seção vira uma section Liquid com schema completo: todo texto vira setting, toda imagem vira `image_picker`, listas repetíveis viram blocks, e o preset carrega valores de exemplo genéricos ("Your headline here", "[garantia]"). As classes CSS de cada section levam o prefixo `sec` (de section), ex: `.sec-hero-title`, pra o estilo de uma section nunca vazar pra outra.
3. **Montar o template** a partir dos presets das sections e popular com o conteúdo real.
4. **Verificar end-to-end:** renderização desktop+mobile comparada com os screenshots do passo 1, e comércio real funcionando (variantes, add-to-cart, cupom).

A MESMA regra legal e ética acima vale integralmente nesta variante: estrutura/layout sim; copy, imagens, marca e paleta do concorrente NUNCA — o clone nasce com o conteúdo do PRÓPRIO membro injetado (copy de `06`, oferta de `04`, imagens da 1.6, paleta dos signals da ETAPA 2). Os padrões de seção endurecidos (marquee/faixa rolante, sticky add-to-cart, gradiente, badges, drawer, fonte universal) vivem em `.claude/lib/shopify-section-patterns/` — consulte antes de reinventar qualquer um deles.

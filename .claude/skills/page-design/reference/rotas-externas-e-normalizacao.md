# Page Design · Referência: Rotas 2 a 5 e a normalização de HTML externo (sub-etapas 3.4 a 3.6c)

> O handoff do Claude Design, o AIDesigner MCP, o fallback `frontend-design` com direção forte e variações da página inteira, os AI site-builders externos e o procedimento real de normalização (Tailwind vira CSS plano por estilos computados, JS de runtime fora, assets locais, validação self-contained). Abra na sub-etapa da rota escolhida.

### 3.4 Rota 2 — Claude Design (handoff)

O membro desenha a página no canvas visual e entrega o HTML pronto.

1. Instrua exatamente:
   > "Abre o `claude.ai/design`, desenha/itera a página lá no canvas. Quando estiver boa, exporta com **'Export as standalone HTML'** (ou 'Download .zip' / 'Handoff to Claude Code'). Depois cola o HTML aqui, ou me dá o caminho do arquivo/zip que você baixou."
2. Pra dirigir o trabalho dele no canvas, forneça antes: o `section_order` + `sections_plan` da ETAPA 1, os eyebrows criativos, a copy de `06` por section, e os `design-signals` da ETAPA 2 — pra ele não desenhar no escuro.
3. Quando o membro colar/apontar o arquivo, leia-o (Read no path, ou descompacte o .zip), rode a **normalização da §3.6c** (Tailwind→CSS plano, remoção de JS de runtime, validação self-contained), confira que a copy real está dentro (não placeholder do canvas), e salve como `design/page.html`.
   > **NOTA:** o `/design-sync` / DesignSync é só pra design-**SYSTEM** (componentes isolados), NÃO pra puxar página inteira. O caminho de página é sempre o export HTML / handoff manual descrito aqui.

### 3.5 Rota 3 — AIDesigner MCP (se `mcp__aidesigner__` presente)

Só ofereça se as tools `mcp__aidesigner__*` existirem na sessão.

1. Construa o input do MCP a partir do `sections_plan` + copy de `06` + `design-signals` da ETAPA 2 (não desenhe do zero — alimente o MCP com a estrutura e o conteúdo reais).
2. Invoque a(s) tool(s) `mcp__aidesigner__*` disponíveis (descubra em runtime quais existem; não assuma nomes hard-coded) pra gerar a página premium.
3. Salve o HTML/CSS limpo retornado como `design/page.html`.
4. Se o MCP falhar ou retornar vazio, ofereça cair pra rota 1 (clone-and-adapt) ou rota 4 (fallback) — não aborte (emergency-escape-paths).

### 3.6 Rota 4 — frontend-design (fallback, qualidade menor)

Use quando o membro não tem referência (sem URL de concorrente, sem canvas). Deixe explícito que é o fallback e a qualidade é a mais baixa do menu (única rota gerada do zero, sem referência).

**Invoque a skill `frontend-design` UMA vez** pra gerar a **PÁGINA INTEIRA** como HTML+CSS self-contained (vanilla, não Tailwind) — mas **NUNCA de tela em branco.** Sempre com direção forte:

- **(a)** os `design-signals` da ETAPA 2 (paleta role-tagged, heading/body fonts, radius, shadow, density).
- **(b)** uma **referência concreta**: peça ao membro um screenshot de inspiração (qualquer página cujo visual ele curta) e leia-o com visão nativa (Read no PNG) pra extrair direção. Se ele não tiver nenhum, use um dos 8 presets da ETAPA 2 como âncora visual nomeada.
- **(c)** **direção de design explícita**: estilo nomeado (ex: "minimalist editorial"), do/don't, e um anti-genérico (o que NÃO fazer pra não sair "cara de template AI").

Demais inputs idênticos às outras rotas: a copy REAL de `06` já inserida (nada de lorem ipsum), as imagens do mapa de mídia da 1.6 (`design/assets/`), a estrutura do `sections_plan` + `section_order` da ETAPA 1, `page_type` e `hero_type` respeitados. Gere **2-3 variações da PÁGINA INTEIRA** (não 4 só do hero) — tratamentos visuais diferentes do mesmo layout/sections (tipografia editorial vs utilitária, paleta warm vs cool, densidade alta vs respiro, hierarquia de proof diferente) num único HTML navegável com tabs/anchors pra alternar A / B / C. Salve em `design/page.html`.

### 3.6b Rota 5 — AI site-builders (externa; consumo igual à rota 2)

Só quando o membro mencionou que usa v0/Lovable/Manus. O design acontece no app externo; o lado da Aura é fornecer o material e consumir o HTML:

1. Forneça ao membro o mesmo pacote da rota 2: `section_order` + `sections_plan` da ETAPA 1, eyebrows criativos, copy de `06` por section, e os `design-signals` da ETAPA 2 — pra ele não descrever a página no escuro.
2. Quando ele trouxer o HTML exportado, leia o arquivo e rode a **normalização da §3.6c** (obrigatória aqui — v0/Lovable/Manus exportam Tailwind + JS de framework): utilities inlined em CSS plano, JS de runtime removido, self-contained validado. Confira que a copy real de `06` está dentro (não placeholder do gerador), injete os markers `data-aura-section` e salve como `design/page.html`.
3. Lembre o membro do runtime: se o destino for o tema Shopify, a `page-build` compila esse HTML em Liquid normalmente; se ele preferir hospedar no runtime do gerador (landing externa), o deploy sai do fluxo `page-build` e o tracking (`tracking-setup`) precisa ser configurado lá.
4. Registre `design_route: "site-builder"` no `page-plan.json` e siga pra 3.7.

### 3.6c Normalização de HTML externo (rotas 2 e 5 — procedimento real, não "normalize" vago)

HTML de canvas/site-builders vem com Tailwind (classes utilitárias + CDN/build) e JS de framework (React/Vue hydration). O `design/page.html` precisa ser **HTML+CSS plano e self-contained** — é o contrato que o SPLIT/COMPILE da `page-build` assume. Procedimento:

1. **Tailwind/utilities → CSS plano via render computado.** Renderize o HTML original no Playwright (`file://` ou server local, com o CSS do Tailwind ainda ativo). Pra cada elemento estrutural (sections, headings, parágrafos, botões, cards, grids), leia os **computed styles** (`getComputedStyle`) e materialize as propriedades relevantes (display/grid/flex, spacing, tipografia, cor, radius, shadow, breakpoints via re-render em 390px e 1440px) em **classes semânticas próprias** (`.hero`, `.hero-title`, `.tier-card`...) num `<style>` único no `<head>`. Troque as classes utilitárias pelas semânticas no markup e remova o `<script src="...tailwind...">`/`<link>` do framework CSS. (Página pequena com poucas utilities? Traduzir manualmente as classes usadas é aceitável — mesmo resultado.)
2. **JS de runtime → fora.** Remova bundles/hydration de framework (`<script>` de React/Next/Vue, chunks). O HTML final é estático; interações (accordion/tabs/FAQ) são reimplementadas com `<details><summary>`/CSS puro — mesma regra que a `page-build` aplica no compile.
3. **Assets → locais ou estáveis.** Baixe as imagens referenciadas pra `design/assets/` e reescreva os `src` (self-contained de verdade), ou mantenha URL absoluta só se for CDN estável do próprio membro. Nunca deixe `src` apontando pro sandbox temporário do gerador (expira e a página aprova com imagem que vai sumir).
4. **Validação de self-contained (obrigatória):** abra o HTML normalizado no Playwright com requests externos bloqueados (exceto Google Fonts) e confirme por screenshot que renderiza igual ao original nos dois breakpoints; console sem erros; `grep -c '<script'` no arquivo = 0 (zero JS de runtime).
5. Injete os markers `data-aura-section` e siga pra 3.7.

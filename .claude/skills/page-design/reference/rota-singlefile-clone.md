# Page Design · Referência: Rota 2, clonar uma página inteira com o SingleFile (sub-etapa 3.4)

> A regra legal e ética, o salvamento da página pela extensão SingleFile no browser do membro, a ingestão pelo `aura_clone.py`, o atalho automático quando o site não bloqueia, a reconciliação com o plano da ETAPA 1, a geração do `page.html` e o contrato de seções editáveis no editor da Shopify. Abra na sub-etapa 3.4.

### 3.4 Rota 2 — Clonar uma página inteira com o SingleFile

O membro indica uma página de marca de referência que ele acha boa. A Aura pega a **ESTRUTURA** dela (ordem de sections, hierarquia, layout, ritmo) e monta a página do membro por cima, com conteúdo 100% dele. A `page-build` compila o resultado em **sections editáveis no editor da Shopify**, direto na loja dele.

> **REGRA LEGAL E ÉTICA (inegociável):** capturar estrutura/layout e trocar 100% do conteúdo (copy, imagens, marca, paleta) é defensável. Copiar 1:1 não é. **NÃO** reaproveite copy, imagens, logos, nome de marca ou claims da página de referência — só o esqueleto de layout como direção. A copy vem SEMPRE de `copy-engine/dados.json`, a oferta de `offer-builder/dados.json`, a paleta/tipografia dos `design-signals` da ETAPA 2, as imagens do mapa de mídia da 1.6.

**Pré-requisito:** a loja Shopify conectada (declarado no pré-flight e verificado na 3.1 com `shopify theme list --store "$STORE"`). A promessa desta rota é a página no tema do membro com cada seção editável; sem a loja conectada, ofereça instalar e logar a CLI agora (o mesmo passo 6.1 da `page-build`) ou trocar de rota.

#### 1. O membro salva a página com a extensão SingleFile

Instrução mastigada, como está:

> "Instala a extensão **SingleFile** no Chrome (https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle), abre a página da marca de referência normalmente no SEU Chrome (logado, sem tela de bloqueio), clica no ícone da extensão — ela salva a página inteira num único arquivo `.html` em Downloads. Me manda o caminho do arquivo (ou arrasta ele pro chat)."

O browser real do membro é imune a anti-bot: é por isso que este é o caminho principal, e não um fallback. O `.html` salvo é material de trabalho (referência de terceiro): vive em `/tmp` ou no workspace e **JAMAIS é commitado** (rule 11).

**Atalho, quando o site não bloqueia:** se o membro preferir não instalar nada, tente a captura automática com a URL. Ela resolve sozinha em site sem proteção e economiza o passo manual:

```bash
python3 tools/design-clone/aura_clone.py clone-and-adapt "URL" --output=/tmp/clone-[produto] --product=[produto]
```

Cloudflare, login ou conteúdo só-JS derrubam a captura automática (o manifest volta com `"skeleton": null`, ou `raw/fallback.json` marca `challenge_detected: true`). Nesse caso não insista nem leia o screenshot do interstitial: volte pro SingleFile, que é o caminho da rota.

#### 2. Ingerir o arquivo

```bash
python3 tools/design-clone/aura_clone.py clone-and-adapt --from-file=<arquivo.html> --output=/tmp/clone-[produto]
```

O subcomando emite `skeleton.html` (sections só com estrutura e placeholder — ordem, tipo e layout da referência, ZERO copy/imagem/marca) + `skeleton.json`. Esse esqueleto é o que você preenche. Não chame `downloader.py`/`analyzer.py` soltos: eles rodam por baixo, e o `analyzer.py` sozinho não gera o skeleton. Exit codes: `0` sucesso · `1` input inválido · `2` pipeline incompleto (ver manifest/stderr).

#### 3. Reconciliar com o plano da ETAPA 1

O esqueleto é referência de layout; a verdade estratégica é o seu `sections_plan` (que veio do awareness e da sofisticação do SEU produto). Onde a referência tem sections que o plano não pede (gift-guide irrelevante), descarte. Onde o plano pede sections que ela não tem (`mechanism`, porque existe mecanismo único real), acrescente, desenhando no mesmo ritmo e na mesma hierarquia das vizinhas. O layout informa hierarquia e ritmo; o conteúdo e a seleção de sections são do membro.

#### 4. Gerar `design/page.html`

Aplique sobre a estrutura reconciliada: a copy REAL da `copy-engine`, a oferta da `offer-builder`, os `design-signals` da ETAPA 2 (paleta, tipografia, radius, densidade) e as imagens do mapa de mídia da 1.6 (`design/assets/` — jamais as imagens da referência). Uma variação fiel ao layout-base basta (o membro já escolheu a referência); ofereça iterar densidade e paleta se ele quiser.

O arquivo herda HTML de terceiro, então passe pela **normalização da 3.6** antes de salvar: utilities viram CSS plano, JS de runtime sai, assets ficam locais, validação self-contained com zero `<script>`, markers `data-aura-section` injetados.

Os padrões de seção endurecidos (marquee, sticky add-to-cart, gradiente, badges, drawer, fonte universal) vivem em `.claude/lib/shopify-section-patterns/` — consulte antes de reinventar qualquer um deles.

#### 5. Preparar as seções editáveis no editor da Shopify

É o que esta rota promete, e o preparo acontece aqui; a compilação é da `page-build` (conversão por section, não em lote). Quatro passos:

1. **Serializar o DOM por seção**, com estilos computados em desktop E mobile + screenshot de cada seção. O par geometria+imagem é o contrato de fidelidade: os estilos computados dão as medidas exatas, o screenshot mostra como a seção deve ficar — a conversão só está certa quando os dois batem.
2. **Converter seção a seção** — trabalho paralelizável (uma por vez, independentes). Cada seção vira uma section Liquid com schema completo: todo texto vira setting, toda imagem vira `image_picker`, listas repetíveis viram blocks, e o preset carrega valores de exemplo genéricos ("Your headline here", "[garantia]"). As classes CSS de cada section levam o prefixo `sec` (de section), ex: `.sec-hero-title`, pra o estilo de uma nunca vazar pra outra.
3. **Montar o template** a partir dos presets das sections e popular com o conteúdo real.
4. **Verificar end-to-end:** renderização desktop e mobile comparada com os screenshots do passo 1, e comércio real funcionando (variantes, add-to-cart, cupom).

Registre no `page-plan.json`: `design_route: "singlefile-clone"` e, em `design_route_ref`, a URL da página de referência.

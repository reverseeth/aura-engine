# Page Build · Referência: DEPLOY com shopify-theme-safety integral (ETAPA 6)

> Os doze passos do deploy com os comandos exatos: CLI e detecção da loja, produto e oferta de pé na loja com os IDs ligados à página, backup e duplicate, pull com `--nodelete`, instalação dos arquivos e marker `data-aura-build`, provisionamento de web fonts, push, criação da página no admin, marker verification, smoke test, preview e aprovação, PUBLISH com gravação de `manifest.storefront` e o fidelity check por visão. Abra na ETAPA 6.

## ETAPA 6 — DEPLOY (shopify-theme-safety INTEGRAL)

### 6.1 Shopify CLI + detecção da loja

```bash
which shopify && shopify version
```
Se não instalado, instrua (`brew install shopify-cli` ou `npm i -g @shopify/cli @shopify/theme`) e **ABORTE** até confirmar.

**Logue a versão no deploy-report.** O Shopify CLI 4.x (mai/2026+) se **auto-atualiza** via package manager entre sessões e removeu comandos legados (`theme serve` → `theme dev`). Se um deploy que funcionava ontem quebrar hoje com "command not found"/flag inválida, o primeiro suspeito é upgrade automático da CLI — cheque o changelog do release antes de debugar o tema. (Os comandos desta skill — `push/pull/duplicate/list/publish` com `--nodelete`/`--allow-live`/`--json` — continuam válidos no 4.x.)

Detecte `STORE`: leia `manifest.json` (`product_url`/`store_url`), extraia `.myshopify.com`. Se custom domain ou ausente, pergunte: "Qual seu store handle `.myshopify.com`?". Todos os `shopify theme ...` usam `--store "$STORE"`.

### 6.1b Produto e oferta de pé na loja (antes de duplicar o tema)

Leia `reference/produto-e-oferta.md` e siga as seis partes: o que a página promete (bloco `commerce` do `page-plan.json` mais a oferta), o produto criado ou conferido com variante por quantidade, cada formato de oferta pelo caminho nativo (pacote, assinatura, desconto automático, cupom; brinde e frete grátis ficam com a `bonus-delivery` e a `checkout-aov`, registrados como pendência), os IDs de variante ligados a **todas** as superfícies de compra do template em `staging/`, os IDs gravados em `manifest.storefront` pelo script, e o check bloqueante de IDs.

A ordem importa: os IDs entram no template de staging aqui, e é esse template que o 6.4 instala no tema clonado. O check bloqueante de IDs roda antes do 6.5 — push com botão apontando pra ID de exemplo é página no ar que não vende.

### 6.2 Backup + duplicate (Regra 6)

Nunca toque o tema live direto. Duplique primeiro (insurance barata):
```bash
shopify theme list --json --store "$STORE"   # identifica role:"live" → LIVE_THEME_ID
shopify theme duplicate --theme "$LIVE_THEME_ID" --name "[$PRODUTO] Preview (Aura)" --store "$STORE" --force --json   # → NEW_THEME_ID
```

### 6.3 Pull antes de editar (Regras 1+2 — `--nodelete`)

```bash
mkdir -p "$THEME_DIR"
shopify theme pull --theme "$NEW_THEME_ID" --store "$STORE" --path "$THEME_DIR" --nodelete --force
```
> `--nodelete` protege arquivos locais recém-criados. No iteration loop, SEMPRE pull antes de re-push pra não sobrescrever settings que o membro mexeu no theme editor.

### 6.4 Instalar arquivos gerados + marker `data-aura-build` (Regra 4)

```bash
cp "$STAGING_DIR"/sections/page-"$PRODUTO"-*.liquid "$THEME_DIR"/sections/
mkdir -p "$THEME_DIR"/templates
cp "$STAGING_DIR"/templates/page."$PRODUTO".json "$THEME_DIR"/templates/
```

Marker de verificação de push: **atributo de dados no elemento raiz da section hero** (comentário Liquid NÃO renderiza no HTML — jamais serviria pra verificar). Compute e injete:

```bash
HASH8=$(shasum -a 256 "$THEME_DIR/sections/page-${PRODUTO}-hero.liquid" | cut -c1-8)
# adicionar ao elemento raiz do markup da section hero (a tag mais externa, fora do schema):
#   data-aura-build="${PRODUTO}-${HASH8}"
```

O atributo é inerte, identifica o build, e **fica no arquivo** (não há re-push de limpeza; a cada re-compile do hero, recalcule o hash). É o mesmo mecanismo da `shopify-theme-safety.md` Regras 4/5.

### 6.4b Provisionar web fonts (a tipografia aprovada TEM que carregar de verdade)

O CSS das sections declara `font-family` — mas declarar não carrega a fonte. Se as famílias de `design-tokens.json` são web fonts e o tema não as serve, a tipografia aprovada no `design/page.html` **cai silenciosamente pro fallback do sistema** (Georgia onde devia ser Geist) e ninguém percebe até a página estar no ar. Protocolo:

1. Leia `type.families[]` de `design-tokens.json` (espelho do bloco `typography` do `design-signals.json`, gravado na sub-etapa 2.1 da `page-design`). Cada entrada traz `name`, `provision`, `weights` e, quando `provision` é `local_files`, o `files_dir`. Família com `provision: "system"` (`-apple-system`, Georgia, Arial, `system-ui`) → nada a fazer, pule. `design-tokens.json` legado, sem `families[]`: leia `heading_font`/`body_font` e trate como Google Fonts.
2. Pra cada família, confira se o tema clonado JÁ a carrega — `grep -ri 'fonts.googleapis\|@font-face' "$THEME_DIR"/layout/theme.liquid "$THEME_DIR"/assets/*.css | grep -i "<família>"`. Já carrega → pule.
3. **Não carrega → provisione pelo caminho que o `provision` daquela família manda.**

   **Caminho A — `google_fonts`:** injete no `<head>` do `$THEME_DIR/layout/theme.liquid` (antes do primeiro `<link rel="stylesheet">`):
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap">
   ```
   Só as famílias e SÓ OS PESOS de `weights` (cada peso extra é KB no LCP). `display=swap` obrigatório. Fonte que veio de preset: os pesos estão no `google_fonts` do preset base, nomeado no `source_detail` do `design-signals.json`, dentro de `.claude/lib/design-presets/presets.json`.

   **Caminho B — `local_files`** (arquivos que o membro baixou e a `page-design` copiou pra `files_dir`): suba os arquivos como asset do tema e declare o `@font-face` apontando pra eles.
   ```bash
   FONTS_DIR="workspace/${PRODUTO}/page/design/assets/fonts"   # o files_dir da família
   cp "$FONTS_DIR"/* "$THEME_DIR/assets/"
   python3 .claude/lib/design-presets/local_fonts.py css "$FONTS_DIR" \
     --mode asset --family "<nome da família>" --weights 400,500,700
   ```
   O comando devolve o bloco `<style>` com um `@font-face` por arquivo, cada um com o `format()` certo pra extensão e `font-display:swap`. **Esse bloco vai no `<head>` do `theme.liquid`**, junto do Caminho A: dentro de `{% stylesheet %}` de section o Liquid não é processado, e o `asset_url` sairia literal na página. Prefira `.woff2` quando a pasta tiver (carrega mais rápido); `.otf` e `.ttf` funcionam, declarados com o `format()` que o script já escolhe.

   > Arquivo de computador (`.otf`/`.ttf`) é bem mais pesado que arquivo de web (`.woff2`). O GATE 1 mede isso no peso da página; se o orçamento estourar por causa da fonte, avise o membro em uma linha, com o número, e diga que baixar o pacote web da fundição resolve.

4. **O bloco `data-aura-fonts` do design nunca vai pro tema.** Ele carrega a fonte pelo caminho do arquivo de design (`assets/fonts/...`, ou a fonte inteira em base64 quando a `page-design` usou o modo `inline`), e nenhum dos dois existe na loja. O bloco é removido antes do split (ETAPA 1) e substituído aqui pelo asset do tema. Bloco sobrevivente = caminho quebrado no CSS de cada section, ou a fonte inteira duplicada em todas elas.
5. **Validação (obrigatória):** no smoke test (6.8), `curl -s` a preview e confirme que o `<link>` do Google Fonts (ou o `@font-face` do asset) da família está presente no HTML servido; pra família local, confirme também que o arquivo responde (`curl -sI` na URL do `asset_url` renderizado, esperando 200). No fidelity check (6.11), o screenshot confirma visualmente que o heading NÃO caiu pra fallback. Sem esses checks, este passo é teatro.

> `theme.liquid` é template crítico (afeta a loja inteira) — o backup do 6.2 já cobre; a edição é aditiva (só `<link>` e `<style>` no `<head>`), nunca remova nada do arquivo.

### 6.5 Push (Regra 3 — `--nodelete`; `--allow-live` só no tema live)

> Antes do push, o check bloqueante de IDs da 6.1b já passou (nenhum ID de exemplo, todo ID existe na loja e está à venda).

Fluxo padrão = cópia unpublished (`NEW_THEME_ID`). `--allow-live` só quando o push é no tema LIVE (ex: hotfix pós-publicação).
```bash
shopify theme push --theme "$NEW_THEME_ID" --store "$STORE" --path "$THEME_DIR" --nodelete --json
# push no LIVE (exceção, com backup já feito em 6.2):
# shopify theme push --theme "$LIVE_THEME_ID" --store "$STORE" --path "$THEME_DIR" --nodelete --allow-live --json
```
Leia o `--json` procurando `"errors"` (não só `"warning"`). Resolva erro por erro (tabela de debug abaixo).

### 6.6 Criar a página no admin (pré-requisito da verificação)

`shopify page create` NÃO existe na CLI — a página é criada uma vez, manualmente:

> "Abre **Admin → Online Store → Pages → Add page**. Título: `[nome do produto]`. **Confere que o handle (final da URL) ficou exatamente `[produto]`** (edita em 'Edit website SEO' se o Shopify gerou outro). Pode deixar o template default por enquanto — a atribuição do template vem depois da publicação. Salva e me avisa."

- Se houver Admin API token/MCP conectado (`mcp__shopify__*`), crie via `pageCreate` em vez de pedir ao membro.
- No iteration loop (página já existe), pule este passo.
- Enquanto o tema não é publicado, o template `page.[produto]` não aparece no dropdown do admin Pages (só lista templates do tema LIVE) — por isso o preview usa `?view=[produto]`, que força o template alternativo.

### 6.7 Marker verification (Regra 4) — NUNCA pull pós-push não-verificado

```bash
curl -s "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO" | grep data-aura-build
```
- Marker encontrado com o hash atual → push OK.
- Página retorna 404 → a página não foi criada (volte ao 6.6) — NÃO é falha de push, não faça rollback.
- Página 200 mas marker ausente (ou hash ANTIGO) → push rejeitado silenciosamente (theme lock? rate limit 429? compile error? arquivo stale?). Diagnostique pela Regra 5 da `shopify-theme-safety.md` ANTES de qualquer pull. **Nunca pull depois de push não-verificado** (o tema remoto antigo sobrescreveria o trabalho local).

### 6.8 Smoke test (Regra 7) — antes de dizer "tá no ar"

```bash
curl -sI "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO"   # esperar 200
curl -s  "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO" | grep -E "(500|Liquid error)"   # esperar zero
curl -sI "https://$STORE/cart.js"   # esperar 200
```
- 404 aqui = página não criada no admin (6.6) — instrução ao membro, NÃO rollback.
- 500/`Liquid error` no corpo, ou `cart.js` fora do ar → falha real: rollback pro backup duplicado (Regra 6) e reporte antes de tentar de novo (ES4 oferece paths alternativos).
- Cobertura ampliada numa rodada só: `python3 .claude/lib/theme-verify/verify_page.py` checa overflow horizontal, presença das seções e erros de console em desktop+mobile de uma vez.
- **`page_type: quiz`:** carregar a página não é testar o funil. Ande o funil no preview, um caminho por perfil: abertura sozinha, uma tela por clique, o endereço mudando a cada resposta, o botão voltar do navegador andando uma tela, a leitura do resultado saindo no tempo do plano, o link direto pra tela de resultado abrindo nela, e o botão de compra devolvendo o carrinho com a variante certa (`reference/quiz-sections.md`).

### 6.9 Preview links + aprovação do membro

```
Theme editor: https://$STORE/admin/themes/$NEW_THEME_ID/editor?template=page.$PRODUTO
Storefront:   https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO
```
O membro revisa o preview (é o gate humano antes do go-live). Iterou? Volte ao iteration loop. Aprovou? Siga pro 6.10.

### 6.10 PUBLISH (go-live — só com aprovação explícita)

Sem este passo a página vive pra sempre num tema unpublished: a `checkout-aov` editaria o tema errado e a Skill `ad-strategy` mandaria tráfego pago pra uma URL 404. O fluxo:

1. **Confirmação explícita** — publicar troca o tema da loja INTEIRA, não só a página: "Preview aprovado. Posso publicar o tema `[nome]`? Isso torna ele o tema live da loja (a página entra no ar em `https://$STORE/pages/$PRODUTO`)."
2. **Backup do live atual** (mais um rollback point além do 6.2):
   ```bash
   shopify theme duplicate --theme "$LIVE_THEME_ID" --name "BACKUP-$(date +%Y%m%d)-pre-publish" --store "$STORE" --force --json
   ```
3. **Publicar:**
   ```bash
   shopify theme publish --theme "$NEW_THEME_ID" --store "$STORE"
   ```
4. **Atribuir o template à página** (agora o dropdown lista): "Admin → Pages → `[produto]` → Theme template → seleciona `[produto]` → Save." Confirme com `curl -sI "https://$STORE/pages/$PRODUTO"` (200) + grep do `data-aura-build` na URL pública.
5. **Gravar no manifest** (contrato lido pela `checkout-aov` — tema onde a página vive — e pela Skill `ad-strategy` — URL de destino da campanha):
   ```json
   "storefront": { "theme_id": "<NEW_THEME_ID>", "page_url": "https://<STORE>/pages/<produto>", "published_at": "<ISO-8601>" }
   ```

Se o membro NÃO quiser publicar ainda (loja em construção), tudo bem — mas deixe explícito: "A página só existe no preview. Antes da Skill `ad-strategy` (ads), a gente precisa publicar — a campanha usa a URL pública do `manifest.storefront.page_url`." NÃO grave `manifest.storefront` sem publicação (a `ad-strategy` bloqueia sem ele, que é o comportamento certo).

> Aviso anti-drift: depois de publicado, NÃO edite as sections da Aura via Sidekick/AI do theme editor — isso cria drift silencioso entre o design aprovado e o que está no ar. Ajustes passam pelo iteration loop desta skill.

### 6.11 Fidelidade visual (screenshot da página no ar vs design aprovado — antes de encerrar)

"Compilou e passou nos gates" não é "ficou igual ao que o membro aprovou". O último check é olhar a página REAL com os próprios olhos, contra a fonte única de verdade:

1. **Screenshot full-page da página no ar** via Playwright (skill `webapp-testing`), em desktop (1440px) e mobile (390px). Publicou → use a URL pública (`manifest.storefront.page_url`); não publicou → rode sobre a preview URL (6.9) mesmo assim — o check não é opcional.
2. **Screenshot do `design/page.html` aprovado** (file://) nas MESMAS larguras (reuse os screenshots do self-review da `page-design` se ainda refletirem a versão aprovada).
3. **Compare os pares POR VISÃO**, ponto a ponto (com `page_type: quiz`, o par é por TELA, percorrendo o funil pelo endereço nos dois lados, e a altura entre as telas de pergunta entra na comparação: variou no ar e não variava no design = o `min-height` se perdeu na compilação): ordem e presença das sections; tipografia (heading caiu pra serif/sans genérica? → o 6.4b falhou, volte lá); cores/tokens (CTA na cor errada = setting não populada); imagens (slot vazio, placeholder vazado, imagem esticada/cortada); spacing/hierarquia (section colada, padding sumido); FAQ/accordion funcionando (`<details>` renderizado).
4. **Divergência real → corrigir ANTES de encerrar a skill** (via iteration loop: ajuste no HTML aprovado + re-COMPILE da section, ou fix pontual no `.liquid`/template JSON + re-push + re-screenshot). Diferença trivial de rendering (anti-aliasing, scrollbar, fonte com hinting levemente diferente) não conta. **Nunca declare "no ar" com a página divergente do design que o membro aprovou.**
5. Se a página usa fonte custom, rode `python3 .claude/lib/theme-verify/font_census.py` — censo da fonte COMPUTADA elemento a elemento (declarar a família não é carregar); se tem seção animada (marquee/carrossel), rode `motion_check.py` com `--throttle` — bug de animação em mobile real só aparece com rede lenta + cache frio.
6. Registre no `deploy-report.json`: `"fidelity_check": {"passed": true, "compared_at": "<ISO>", "divergences_fixed": ["..."]}`.

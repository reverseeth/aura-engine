# Page Build · Referência: GATE de launch (ETAPA 5)

> A passada de estilo, o contrato de preços com a `offer-builder` (`subscription_architecture`, `onetime_premium_pct`, `main_sku_price`) e o GATE 1 de performance budget com os checks estáticos e o check de peso pós-push. Abra na ETAPA 5.

## ETAPA 5 — GATE de launch (blocking, ANTES do deploy)

**Passada de estilo (antes do gate):** zero travessão em headlines, ≤2 em copy longa (rule 8a); zero emoji na UI da página (rule 7 — ícones SVG); nenhum aviso/disclaimer inserido por conta própria (rule 8b).

**Preços renderizados = arquitetura da oferta (contrato `offer-builder`→`page-build`):** leia `offer-builder/dados.json` → `subscription_architecture`, `onetime_premium_pct`, `pricing.main_sku_price` e use exatamente esses valores nos settings de `pricing_tier`, nas opções do selling plan e na buy box do template JSON: `subscription_first` → assinatura a `main_sku_price` e one-time a `main_sku_price × (1 + onetime_premium_pct/100)`, sem framing "Subscribe & Save X%"; `onetime_plus_sub_no_reorder` → sem selling plan, preço `main_sku_price`; tiers de bundle iguais a `aov_levers.bundles[]`. Campos ausentes (dados.json legado) → comportamento atual.

### GATE 1 — Performance budget (a página aprovada tem que ser rápida no 4G do consumidor)

Página lenta mata o CPA antes do criativo ter chance: cada segundo de LCP a mais derruba conversão de tráfego pago mobile. O alvo real é **LCP mobile < 2.5s**; o gate usa proxies simples e verificáveis.

**Checks estáticos (pré-push, sobre os `.liquid` + template JSON):**
- [ ] Toda imagem renderiza via `image_url | image_tag` com `width:` adequada (o CDN da Shopify serve WebP/AVIF e redimensiona — nunca a original de 4000px) e `loading: 'lazy'` nas sections abaixo da dobra.
- [ ] A imagem do hero SEM lazy (é o candidato a LCP) e COM `width`/`height` no `<img>` (o `image_tag` já emite — confira que ninguém removeu).
- [ ] Zero `<script>` de runtime nos `.liquid` das sections (grep; única exceção: `application/ld+json` da ETAPA 4.5 — não é runtime).
- [ ] CSS filtrado por section (padrão 7 do conversor) — sem N cópias do `page.css` no tema.

**Check de peso (pós-push, junto do smoke test 6.8):**
```bash
curl -s -o /dev/null -w '%{size_download}\n' "https://$STORE/pages/$PRODUTO?preview_theme_id=$NEW_THEME_ID&view=$PRODUTO"   # HTML: alvo ≤ ~200KB
# peso das imagens above-the-fold (hero): curl -sI em cada src do hero e some content-length — alvo ≤ ~300KB
```
Página total (HTML + CSS + imagens + fontes) alvo ≤ ~1.5MB. **Estouro grosseiro (ex: imagem multi-MB no hero) = BLOCK do publish** até corrigir (reduzir `width:` do `image_url`, recomprimir o asset); desvio pequeno = warning com fix aplicado na hora. Registre o resultado em `deploy-report.json.gates.performance`.

**Fonte de arquivo local (`provision: "local_files"` em `type.families[]`) entra na conta.** Some o `content-length` dos arquivos de fonte servidos pelo tema. Arquivo de computador (`.otf`/`.ttf`) pesa bem mais que arquivo de web (`.woff2`), e três pesos de uma família em `.otf` sozinhos comem boa parte do orçamento. Estourou por causa da fonte: **uma linha ao membro, com o número** ("a página ficou em X MB; os arquivos de fonte respondem por Y MB — o pacote web da fundição, em `.woff2`, cortaria isso pra cerca de Z"), e a opção de seguir assim ou trocar os arquivos. Nunca troque a tipografia aprovada por conta própria pra caber no orçamento.

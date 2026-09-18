# Market Research · Referência: Confirmar produto e mercado geográfico (ETAPA 1)

> A confirmação do produto com ou sem link no profile, a confirmação do mercado geográfico a partir de `manifest.market` e o default anglo-saxão para 'global'. Abra na ETAPA 1.

### ETAPA 1 — Confirmar Produto + Mercado Geográfico

Verifique `workspace/profile.md` se já tem `Link do produto principal`.

**SE o profile tem link do produto (ou veio da fase de product research):**
- Confirme: "Vou fazer o market research pro [produto]. Correto?" — espere só "sim" ou correção.

**SE NÃO tem link de produto:**
- Pergunte: "Me descreva o produto: o que é, o que faz, pra quem é, e o link se tiver."

Depois (em qualquer um dos casos acima), confirme o mercado geográfico. Leia `manifest.market` primeiro (o setup grava `"US"` como default) e proponha como default em vez de perguntar do zero:
- "Mercado geográfico principal: **[manifest.market]** — confirma, ou é outro? (US, UK, EU, global)"

Salve o mercado geográfico no documento final da pesquisa E de volta em `manifest.market` (ver seção "Atualize o manifest.json") — toda a análise de awareness, sofisticação, VOC, etc. deve considerar esse mercado específico. Costumes de compra, objeções culturais, e linguagem variam enormemente entre mercados. Se o membro disser "global", analise o mercado anglo-saxão (US+UK+AU+CA) como default.

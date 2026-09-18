# Competitor Analysis · Referência: Levantamento de ads escalados com link, o doc dedicado (ETAPA 3F)

> O método com TrendTrack (busca por domínio e nome, três ordenações deduplicadas, campos por ad, regra de leitura do alcance, achados além dos ads), a versão manual e a saída em `ads-escalados.md`, `.html` e `ads-escalados-dados.json`. Abra na ETAPA 3F.

### ETAPA 3F — Levantamento de Ads Escalados com Link (doc dedicado, recomendado com TrendTrack)

As etapas 3-3E analisam os criativos; esta etapa entrega ao membro o **catálogo navegável**: os ads mais escalados de CADA concorrente, cada um com o link direto da biblioteca de anúncios da Meta, o formato e os números de escala — um doc que ele abre e clica.

**Com TrendTrack conectado** (tools `mcp__trendtrack__*` — case por intenção, nunca por nome fixo de tool, conforme `.claude/lib/trendtrack-integration/README.md`):

1. **Por marca, busque pelo DOMÍNIO primeiro** (search em ads com escopo de domínio); se vier vazio, busque pelo nome da marca. Marcas que vendem via Amazon podem anunciar com landing própria em outro domínio — a busca por nome acha o que a busca por domínio perde.
2. **Três ordenações por marca, depois deduplicar** (mesmo ad id ou mesma collation = 1 entrada): mais duplicatas · maior alcance · mais tempo no ar. **Duplicatas é a métrica primária de escala** (é o mesmo sinal das "aparições" da ETAPA 3: marca só multiplica criativo que paga a própria conta); alcance e dias no ar desempatam.
3. **Por ad, registre**: link da biblioteca (`https://www.facebook.com/ads/library/?id=<ad_id>` — montado SEMPRE com o id real retornado pela tool, nunca inventado), formato (imagem/vídeo/carrossel), hook literal (inglês, verbatim), alcance, dias no ar, duplicatas, status, landing de destino.
4. **Regra de leitura do alcance (vai escrita no doc):** a Meta só publica alcance de anúncios veiculados na União Europeia — ad que roda só nos EUA/Canadá aparece com alcance 0, o que NÃO significa gasto zero; nesses casos a escala se lê por duplicatas + dias no ar. Marque esses casos (ex: `0*`) e explique o asterisco.
5. **Reporte o que a busca revelou além dos ads**: marca com zero ads ativos (pausou — desde quando?), marca escalando OUTRO produto no mesmo domínio, página homônima vendendo outra coisa (registrar como pendência de validação, nunca como fato).

**Sem TrendTrack:** a versão manual — ao documentar os top criativos na ETAPA 3 (Meta Ad Library pública), copie também a URL do ad na biblioteca (cada cartão de ad tem link próprio com `?id=`). O doc sai menor (top 3-5 por concorrente), mas sai com links do mesmo jeito.

**Saída (dual output + dados):** `competitor-analysis/ads-escalados.md` + `.html` (tabela por marca: nº, formato, hook, alcance, dias no ar, duplicatas, status, link clicável — texto integral, nunca truncar hook) e `ads-escalados-dados.json` (todos os campos crus, incluindo gasto estimado e link de mídia quando a fonte trouxer). No `.md` principal da skill, a seção de ads referencia este doc. Preencha também `top_creatives[].ad_library_url` no `dados.json` pros criativos que aparecem nos dois lugares.

# Creator Engine · Referência: Pipeline TikTok Shop, a fábrica de volume (ETAPA 7)

> O reframe do canal como fonte de conteúdo, a operação base com a leitura aditiva da marketplace-engine, a variante de contas dedicadas, a mineração de virais e a nota sobre influencer grande. Abra na ETAPA 7.

### ETAPA 7 — [Fase A] Pipeline TikTok Shop: a fábrica de volume

Opcional — roda pra quem já opera TikTok Shop ou quer o canal COMO FONTE DE CONTEÚDO. A decisão de abrir marketplace como canal de VENDA é outra conversa (regra de entrada própria — skill marketplace-engine).

**O reframe da fonte: o valor do TikTok Shop não é a receita da plataforma — é ser PAGO para gerar conteúdo.** Caso citado: um operador gerou 600 vídeos num mês pra uma marca (faturando ~US$ 250-300k no canal) e passou a reutilizar o acervo como criativo de paid ads. "Most people spend money to get content; you make money to get content."

- **Operação base:** envio de samples (amostras) pra creators do canal, gestão dos afiliados, comissão definida (dois níveis — orgânica vs de ads; a régua vive na `marketplace-engine`), e o fluxo de conteúdo que sustenta as vendas — cada afiliado postando é conteúdo novo que pode virar ad.
- **Leitura aditiva da `marketplace-engine` (se `marketplace-engine/dados.json` existir):** `channels[tiktok_shop].commission_organic_pct`, `samples_policy` e a meta de GMV definidos lá são os números que este pipeline usa — a decisão de abrir/manter o canal de venda continua na `marketplace-engine`; aqui nada se redecide.
- **Variação agressiva da fonte:** contas TikTok dedicadas à marca (caso: 20), cada uma tocada por um creator 100% comissionado (**40-50% de comissão**), produzindo volume diário reutilizado nos paid ads; contas chegam a 20k seguidores em ~6 meses. Comissão agressiva força volume — e o conteúdo vale mais que a margem cedida.
- **Mineração de virais (DailyVirals):** os virais do dia do TikTok/TikTok Shop viram swipe file de UGC — sandbox de breakdowns, transcript downloader (cole a URL, receba o texto), análise por AI do vídeo linha a linha, e o AB compare (viral original vs seu remake, frame a frame, pra diagnosticar por que o seu flopou). O fluxo: transcript do viral → reescrever adaptado ao produto → virar concept no framework do creator (ETAPA 5). Remake próprio, nunca o vídeo alheio no ar (regra 5).
- **Influencer grande é jogada de marca, não de performance** — a fonte viu post de celebridade funcionar como whitelisted ad num caso e flopar como ad noutro. O motor daqui é micro/médio creator em volume.

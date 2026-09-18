# Promo Engine · Referência: Criativos da janela, o brief pra creative-engine (ETAPA 6)

> A doutrina do melhor ad com banner e do static de produto com oferta, as cinco prioridades do brief, a regra de escrever Black Friday Cyber Monday já na sexta e o volume de batches. Abra na ETAPA 6.

### ETAPA 6 — Criativos da janela (brief pra `creative-engine`)

Rode **Blueprint de criativo de sale** (`criativos de sale banner sobre o melhor ad foto do produto com oferta statics BFCM`) e **Revival de winner sazonal** (`religar seasonal winners ads que morreram voltam no mesmo período calendário de desejos`).

**A doutrina da fonte é anticlimática e comprovada ano após ano: os melhores anúncios de sale são (1) o seu melhor ad existente com um banner de oferta por cima e (2) foto simples do produto + oferta.** Statics superam vídeos no pico — o público está em modo most aware, procurando produto + oferta (o melhor ad de um dia de US$ 700k na fonte foi uma FOTO do produto com a oferta). **Não gaste semanas em UGC customizado de sale** — "essas ads nunca ganham spend".

O brief que esta skill entrega pra `creative-engine` (`creative_brief_08` no `dados.json`), em ordem de prioridade:

1. **Winner + banner:** o melhor vídeo da conta (breakthrough do `manifest.ad_classification`; na falta, o spend_winner mais estável) com banner de sale no topo/rodapé (geralmente rolando) ou sticker "Black Friday Sale Live". **Exceção:** se a headline do winner é o que fisga, NÃO cobrir com banner gigante — call-out discreto ("BF 52% off") ao lado; testar as duas vias e dobrar na que ganhar.
2. **Statics de produto + oferta:** call-out grande e claro da sale + produto + prova social + urgência guiando o olho; text-heavy simples deixando claro O QUE se vende; multi-SKU/fashion mostra variantes e cores (+ catalog ads).
3. **Revival sazonal:** religar o que performou out-dez do ano passado (leia `seasonal_vault[]` de rodadas anteriores e a `ad-analysis`) — **com re-banner, porque a oferta mudou** (case da fonte: marca a US$ 500-600/dia religou um ad sazonal de dois anos antes e foi a US$ 3-4k/dia).
4. **Scarcity ads pra early sale:** a única razão de comprar ANTES do pico é escassez real ("sold out 12 times") — filmável com o produto e um post-it; versão pre-order pra quem vai estourar estoque ("due to extreme demand, limited pre-run").
5. **Complementos:** static → GIF (banner animado vira "vídeo" e alimenta a audiência de 95% viewers do WARM60); founder text ad (texto puro, estilo carta, pra quem está em cima do muro — rodar nos 3 ad sets); bundle ads ("life is better when you bundle" — quem clica em bundle leva bundle); whitelisted ad na página de creator.

Escreva já nos criativos da sexta **"Black Friday Cyber Monday Sale"** — os ads de BF **continuam rodando na Cyber Monday** (não desligue no domingo pra lançar campanha nova: o momentum e os dados da semana valem mais; marcas grandes fazem exatamente isso; pode ciclar criativo novo na segunda sem desligar o que roda). Rode `não desligar ads de black friday na cyber monday momentum black friday cyber monday sale no criativo`.

**Volume:** começar com 2-3 batches (~9-12 statics/semana; 3-4 batches pra resposta direta), ver o que roda e fazer mais do que funcionou — swings maiores entre conceitos. Texto do banner conferido contra a matemática da ETAPA 3/4 (o "save up to X%" é o desconto efetivo real) e contra as regras 8a/8b do CLAUDE.md. Copy em inglês US.

A `creative-engine` produz os assets a partir deste brief — handoff nomeado, com o `creative_brief_08.handed_off: true` e a data.

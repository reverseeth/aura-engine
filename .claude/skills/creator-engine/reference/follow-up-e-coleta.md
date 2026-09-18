# Creator Engine · Referência: Follow-up, coleta e o corte em 3 hooks (ETAPA 6)

> A cadência de follow-up, a coleta no Drive, a marcação `dct_ready` pro inventário da creative-engine, os números de expectativa de acerto da fonte e a auditoria de ROI. Abra na ETAPA 6.

### ETAPA 6 — [Fase A] Follow-up, coleta e o corte em 3 hooks

**Cadência:** produto marcado como enviado → avise o creator ("chega em 3-7 dias; me avisa ao receber"). Depois da confirmação de recebimento, **follow-up a cada ~3 dias** (com folga em fim de semana); **nunca passe de 7 dias sem contato**. Perguntas típicas: "did you receive it?", "how's the content coming along?". Creators são pessoas, não robôs — firme e humano. Qualidade fraca: dá pra pedir ajuste com jeito, calibrando a expectativa ("this is free content").

**Coleta:** ao receber, baixe TUDO ("the more content the merrier" — com e sem áudio, fotos, link do post se postou) → Drive → pasta com o nome do creator. Só marque o deal como completo com o conteúdo salvo. Creators excepcionais (entregam em dias, avisam proativamente) → marque como favoritos: são os candidatos naturais a embaixador.

**Marcação de corte:** pra cada entrega, avalie "dá pra cortar em 3 variações e rodar como ad?" → marque `dct_ready: true` (o padrão da casa: **cada vídeo cortado em 3 versões começando em 3 pontos diferentes = 3 hooks**) ou `false` se inutilizável — arquive mesmo assim ("who knows, maybe it would convert"). O conteúdo aprovado entra no inventário que a `creative-engine` lê (`content[]` no `dados.json`) — a `creative-engine` decide o empacotamento e a `ad-strategy` sobe.

**Expectativa de acerto (números da fonte — calibram a paciência, não substituem os do membro):**

- Hit rate (taxa de acerto) de UGC de creators: **~14%** vs **~4%** dos ads produzidos pelo time interno — com custo de operação ~US$ 6k/mês vs ~US$ 40k/mês.
- Conteúdo cru: **~15%** de acerto vs **~5%** do conteúdo editado/polido (3x, por autenticidade).
- Win rate acima de volume, sempre: 20% de acerto em 30 criativos/mês = 6 winners; 1% em 100 = 1. **Volume desestruturado (Shotgun) só é legítimo dentro deste pipeline de creators** (cânone ad-taxonomy §7) — como estratégia criativa deliberada, mata o hit rate.
- Escala do motor: 10 creators fazendo 1-2 vídeos/semana, cortados em 3 = **~130-260 ads extras/mês**; a fonte sustenta marca a US$ 25k/dia assim, e cita marca a US$ 150k/dia com 3x+ ROAS rodando SÓ com volume de creators, sem creative strategy formal.
- O funil típico não é "winner de primeira": o creator faz um vídeo BOM → é contratado → e o SEGUNDO vídeo, já com feedback, vira o super winner.

**Auditoria de ROI (mensal/trimestral):** "gastamos US$ X em conteúdo de creators → quantos winning ads saíram → quanto spend eles sustentaram". Grave em `economics.roi_audit` — é o número que justifica (ou corta) o budget de conteúdo.

# Product Research · Referência: Checagem 1, Google Trends em 5 anos nos US (ETAPA 2)

> Os dois termos por marca, o lote em segundo plano pelo `trends_batch.py` com o comportamento diante do bloqueio, a regra de eliminação por queda de 12 meses ou mais, a leitura conjunta dos dois termos e a classificação de cada termo e do cenário. Abra na ETAPA 2.

### ETAPA 2 — Checagem 1: Google Trends (5 anos, US)

Pra cada marca, rode **duas** consultas no Google Trends: **o problema** que o produto resolve (ex: "bloating", "joint pain", "hair thinning") e **o ingrediente ou mecanismo** da solução (ex: "berberine", "collagen peptides", "psyllium husk"). Janela: **últimos 5 anos**, país: **US**.

Como rodar: monte a lista completa de termos (2 por marca, mais os termos de apoio que surgirem na ETAPA 5) e dispare o **lote em segundo plano** logo no início da ETAPA 1, pra ele rodar enquanto você fecha as fichas e o Trustpilot:

```bash
nohup python3 .claude/lib/web-fetch/trends_batch.py --out <pasta-temporária>/trends "termo 1" "termo 2" ... > <pasta-temporária>/trends.log 2>&1 &
```

O endpoint do Trends aceita ~25-30 consultas seguidas do mesmo IP e depois bloqueia por 30-60 minutos; o lote espaça as consultas (20 s), pausa entre lotes, espera e tenta de novo quando um termo volta bloqueado, e pula o que já foi medido (rodar de novo retoma de onde parou). Cada termo sai como JSON com a série e a classificação (QUEDA / FLAT / SUBINDO / SPIKE) em `<pasta>/<termo_com_underscores>.json`; leia os arquivos quando chegar na ETAPA 2 e confira o `trends.log` (termos que ficaram bloqueados aparecem na última linha). Pra um termo avulso: `python3 .claude/lib/web-fetch/fetch.py "<termo>" --mode trends --json`. NUNCA tente renderizar o site do Trends com `--mode text` — ele recusa navegador automatizado. Termo que continuar bloqueado depois das retentativas: siga com os demais, rode o lote de novo mais tarde (só o que falta) ou peça ao membro pra abrir `trends.google.com`, setar 5 anos / US e colar um print da curva daquele termo — você lê a tendência pela imagem. O membro nunca espera o lote: a skill segue com o resto do trabalho e só volta ao Trends quando os arquivos estiverem prontos.

**Regra de eliminação:** queda constante por 12 meses ou mais, dentro da janela de 5 anos → **elimina** (vale pro problema e pro ingrediente).

**Leitura dos dois termos juntos:**

- **Problema vivo define se o nicho vale a pena.** Problema em queda de 12+ meses = nicho encolhendo, elimina mesmo com ingrediente bom.
- **Ingrediente define se você chegou na hora.**
- **Problema subindo + ingrediente estável** = **melhor cenário** (demanda crescendo, mecanismo maduro e sem hype).
- **Ingrediente ou mecanismo subindo há 6+ meses** = ótimo cenário — a onda ainda está no começo.
- **Problema subindo + ingrediente em pico recente** = tarde. A marca pegou a onda cedo; o membro chegaria no pico. Aqui a jogada é **trocar o mecanismo** (ETAPA 6, padrão 3): manter o ângulo/problema e usar um ingrediente validado por outra marca que não esteja no pico.
- **Subida vertical em 1-3 meses** = **hype**. Na maior parte das vezes cai tão rápido quanto subiu. Não elimina sozinho, mas rebaixa o score e exige mecanismo alternativo.

Classifique cada termo em **QUEDA / ESTÁVEL / SUBINDO / PICO RECENTE / HYPE** e grave o **cenário** da marca (combinação dos dois) na ficha. Marca eliminada aqui sai da análise com o motivo registrado.

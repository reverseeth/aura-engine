# Promo Engine · Referência: A oferta da promo, hierarquia, stacking e progressão (ETAPA 3)

> A hierarquia das ofertas com a tabela por papel na janela, a regra do número que parece maior, o store credit, as regras duras de stacking e linguagem, a progressão dentro da janela e a alternativa de dezembro. Abra na ETAPA 3.

### ETAPA 3 — A oferta da promo

Carregue antes: **Offer Type Menu** (`offer types percent off dollar off buy one get one free gift free ebook free shipping threshold margin`), **Scarcity & Urgency Framework** (`scarcity urgency limited quantity deadline price increase bonus removal consequence of delay real reason` — urgência sempre real, nunca inventada) e **Breakage & Slippage** (`40% dos rebates nunca são resgatados, gift card não usado, custo efetivo do desconto`).

**A hierarquia da fonte (P1) — as duas melhores, disparado: percentage off e dollar off.** Porque qualquer pessoa entende, e porque barateiam exatamente o produto que a pessoa já veio comprar. Regra de escolha: **use o número que PARECE maior** — ticket baixo, percentual soa maior ("25% off" > "save $5" num produto de US$ 20); ticket alto, valor absoluto soa maior ("save $500" > "save 10%" num produto de US$ 5.000).

| Oferta | Papel na janela | Nota da fonte |
|---|---|---|
| **% off / $ off** | **core** | o número que parece maior; desconto uniforme merece "X% off EVERYTHING" |
| **Buy X Get X Free** | core alternativo | se já roda "compre 1 leve 2" no evergreen, escale pra "buy 1 get 2 free" na data; "free" converte melhor que "buy X get X% off" (esta a fonte não recomenda) |
| Free gift, free shipping, bundle & save | **add-ons de stack, nunca core** | *"não quero sua tote bag; quero $15 off do produto que eu vim comprar"* |
| **Buy X, GIFT X free** | teste | mesmo mecanismo do leve-2, enquadrado como presente: mecânica visível por estágio ("compre 1 pra você, adicione o 2º e nós embrulhamos"), razão logística ("resolva seu Natal agora"), resultado em dupla ("treine com um amigo"), embrulho cortesia |
| **Store credit / gift card** | teste de alto potencial | em vez de US$ 20 off, um gift card de US$ 66: custa ~os mesmos US$ 20 (você só paga a margem do valor de face) com valor percebido ~3×; parte nunca é resgatada (a quebra joga a favor — Breakage & Slippage); quem resgata volta a comprar; dá pra presentear |
| Oferta por avatar | teste em landing | simplificar a escolha pela vida do avatar ("comprando pra 1 ou 2 pessoas?" em vez de "1, 2 ou 3 packs") |
| Quiz offer | teste (gifting) | "encontre o presente certo" como funil |

**Stacking e linguagem (regras duras da fonte):**
- Empilhar desconto embutido de bundle + % extra da data e comunicar o total ("save up to 40%") é legítimo — mas **recalcule o preço final a partir do compare-at**: 10% + 20% em cima NÃO é 30%. A matemática errada no banner é bug de confiança.
- Desconto uniforme → **"X% off EVERYTHING"** (mais forte que "site-wide"). **"Up to X% off" só quando o desconto NÃO é uniforme** — e saiba que o consumidor já desconfia do padrão "up to 70%" com 70% só no estoque encalhado. "Biggest sale of the year/ever" só quando for verdade.
- **NUNCA inflar o compare-at price** pra fabricar desconto: *"as pessoas viram seus ads o ano todo; você não está sendo um bom vendedor, está enganando."* É gate ético e de conta.
- Aceitável o ad dizer 25% e o site dar 40% (surpresa positiva); **o inverso destrói a conversão**.
- Toda sale precisa de **razão declarada** — data sem razão vira ruído (a razão é o que a `retention-engine` escreve nos emails).

**Progressão dentro da janela (recomendação 2025 da fonte):** rodar a MELHOR oferta a janela inteira e, no fim de semana do pico, adicionar um bônus por cima ("free gift / gift card — BF weekend only"). Depois da Cyber Monday, **degradar de propósito** pra oferta média no holiday sale — é isso que torna a urgência do pico real. Objeção clássica "cliente novo nunca viu a oferta antiga, por que melhorar?": com CTR de ~2%, 98% de quem viu o ad não clicou, e jornadas de compra de 2-7 meses são comuns — "cliente novo" ≠ "nunca te viu"; oferta melhor gera salto maior.

**Dezembro:** alternativa que preserva margem — **free express shipping "get it by Christmas"** em vez de % off (exige estoque no país); "priority processing" pago (US$ 5-10) só se o backend priorizar de verdade, senão vira chargeback.

Hierarquia e ofertas — rode `hierarquia de ofertas BFCM percentage off dollar off número que parece maior everything site-wide up to compare-at` e `store credit gift card 66 custa 20 valor percebido buy x gift x oferta por avatar quiz`.

Grave `offer` no `dados.json`: tipo core, stack, desconto efetivo total (com a matemática do compare-at conferida), bônus do pico, oferta degradada da cauda, oferta VIP (se ETAPA 2.2 aprovou).

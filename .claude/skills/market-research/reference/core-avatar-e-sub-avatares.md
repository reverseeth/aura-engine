# Market Research · Referência: Core avatar e sub-avatares, a camada que vira ângulo (ETAPA 4.5)

> Os sistemas a puxar, o core avatar com uma categoria só e o desejo de superfície, a escala do específico ao amplo com a quantidade de core avatars por tamanho de operação, as regras dos sub-avatares, o método de três passos que transforma sub-avatar em ângulo, os labels e a saída obrigatória. Abra na ETAPA 4.5.

### ETAPA 4.5 — Core Avatar e Sub-Avatares (a camada que vira ângulo)

**Sistemas a puxar da base antes de montar (rode cada `best_query`):**
- **Core Avatars & Sub-Avatars — The Core Five Categories** (rode `core avatar sub avatar core five categories desire experience emotion behavior demographic`)
- **Desire-First Avatar (over Demographics)** (rode `desire first avatar over demographics avoid combining desires single desire core avatar`)
- **Surface Desire vs Core Desire** (rode `surface level desire vs core desire why behind the desire avatar building`)
- **Desire Power Ranking — Scope / Urgency / Staying Power** (rode `mass desire scope urgency staying power power ranking choose strongest`)

O perfil da ETAPA 4, sozinho, descreve um mercado — não diz PRA QUEM cada peça fala. Esta etapa converte aquele perfil em avatares nomeados e acionáveis. É o único lugar do sistema onde `core_avatar` e `sub_avatars[]` nascem: a Skill `creative-engine` lê os sub-avatares como a variável mestre de cada conceito de criativo, e a Skill `copy-engine` usa o mesmo recorte pra decidir a quem a copy se dirige. Sem esta etapa, as duas ficam sem a informação e voltam a escrever pra "mulheres 45+", que é o mesmo que escrever pra ninguém.

**1. Escolha o core avatar — UMA categoria só.**

Core avatar é o ponto de partida, construído com **uma única** das Core Five. Para praticamente todo produto essa categoria é **desire**, e o desejo usado é o de **superfície**, não o instinto:

- **Desejo de superfície** é o resultado imediato e específico que a pessoa quer: "I want to sleep through the night", "I want smoother and less dry skin", "quero que meu cachorro pare de puxar a guia".
- **Desejo central** é o instinto por trás (saúde, status, sexo, pertencimento, controle, conforto). Orienta tom e mensagem, mas é amplo demais pra construir avatar. Mirar o instinto direto só se justifica pra marca grande com skill de marketing muito alto.
- **Checador de desejo:** cabe na frase "I want X" ou "I need Y"? Se não cabe, não é desejo — é outra categoria disfarçada.
- Reclamação vira desejo espelhado: "por que demora tanto pra escovar os dentes?" → "quero escovar os dentes mais rápido".

Ordene os candidatos por **scope**, **urgency** e **staying power** (o ranking da ETAPA 4). Quanto menor a operação, mais pro lado específico da escala ela precisa operar.

**2. A escala do específico ao amplo — específico sem alienar.**

Avatares vivem num espectro. De um lado, específico a ponto de excluir todo mundo ("dentista de 34 anos em Tampa que dirige Tesla vermelho e toma oat milk latte"): quase ninguém se encaixa e não há escala. Do outro, amplo a ponto de não dizer nada ("mães", "quem quer ser saudável"): é o território das marcas gigantes, não o do membro. **Quanto mais amplo o avatar, melhores precisam ser produto, oferta, marca E skill de marketing**, porque a disputa é de frente com os gigantes. Quanto mais específico sem alienar, mais a especificidade compra confiança e compensa produto, oferta e marca menores.

Quantidade de core avatars por tamanho de operação: **um único core avatar até $100k/mês** (todo o trabalho é aprofundar sub-avatares a partir dele); **2-3 acima de $500k/mês**; **3-10 entre $1M e $10M/mês**. Trocar de core avatar cedo demais rouba foco do que está funcionando.

**3. Construa os sub-avatares — duas categorias ou mais.**

Sub-avatar é o core avatar refinado com pelo menos mais uma categoria: desejo + experiência, desejo + emoção, desejo + comportamento, desejo + demografia, ou combinações de três ("quer que a família toda durma melhor" + "o bebê acorda às 5h por causa da luz da manhã" + "se sente exausto"). Regras inegociáveis:

- **Todo sub-avatar precisa de pelo menos um desejo** — desejo é o que faz comprar.
- **Nunca combine mais de um desejo** no mesmo avatar. Um desejo pode levar a outro, mas o avatar mira um só.
- Quanto mais categorias empilhadas, mais específico o avatar fica. Em mercado sofisticado, os recortes óbvios já foram atacados: empilhe mais categorias.
- Demografia entra **por último** e só quando refina de verdade.

Pesquise **uma categoria por vez**, com a mesma coleta resiliente da ETAPA 4 e buscas simples: emoção (`"lack of sleep is making me feel reddit"`), experiência de produto (`"blackout room sleep reddit"`), demografia (`"night shift workers sleep reddit"`, `"at what age does sleep start getting worse"`). Uma única thread boa costuma render vários sub-avatares. Vale também o caso sem dor ativa (a pessoa 70+ que dorme bem tomando vinho): ela não é avatar de compra, mas vira informação pra um ângulo ("durma melhor sem precisar se intoxicar").

**4. Cada sub-avatar carrega o ângulo que ele gera.**

Sub-avatar existe pra produzir ângulo — essa é a razão de tudo. Método em três passos: (1) olhe o **desejo** (o que a pessoa quer); (2) olhe a **experiência ou o comportamento** (o que ela já tentou ou já faz pra conseguir); (3) nomeie a **lacuna** entre os dois. A lacuna é o ângulo.

Exemplo: desejo "restorative sleep" + comportamento "dorme com fita nasal pra forçar respiração nasal" → ela faz isso e ainda não dorme direito → ângulo **"better than nose strips"**.

**Ângulo é a razão principal que você dá pra alguém comprar**, voltado ao cliente e escrito em frase completa. Se a frase não entrega ao cliente uma razão de compra, ainda não é ângulo — é conceito ou formato. "Comparação", "before & after" e "us vs them" são conceitos: comparação de quê? O "quê" é o ângulo. Trava contra excesso de zelo: **um ângulo por sub-avatar**. Se sobrar ângulo, ele indica um sub-avatar novo — não vira lista solta.

**5. Anote os labels — como o mercado se chama.**

Labels são os apelidos que o próprio mercado usa pra se descrever: "light sleeper", "night shifter", "graveyard shift", "sleep tech user". Colete sempre que aparecerem, em comentários, threads e nos anúncios ativos dos concorrentes na Meta Ad Library (é lá que o concorrente já testou esse jeito de falar com dinheiro real). Servem pra duas coisas: entram literalmente na copy, porque usar as palavras que o mercado usa pra se nomear gera identificação imediata, e viram termo de busca pra achar mais gente igual na rodada seguinte de pesquisa. Grave em **`labels[]`** no `dados.json`.

**Saída obrigatória desta etapa:** `core_avatar` + `sub_avatars[]` + `labels[]` no `dados.json` (schema abaixo). Sub-avatar não tem certo e errado — é hipótese que gera ângulo pra teste. Se o ângulo não performar, na esmagadora maioria das vezes o problema é execução, não o avatar.

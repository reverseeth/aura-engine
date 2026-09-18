# Sourcing · Referência: Qualidade, golden sample, QC ponta a ponta e a matemática do defeito (ETAPA 10)

> Os seis sistemas a puxar, a matemática do defeito com o caso de referência e a fórmula nos números do membro, a golden sample, a cadeia de QC operada à distância com as duas regras que não se dobram, os critérios de aceite por categoria, o atendimento como sensor de defeito e a recuperação de receita com o fornecedor. Abra na ETAPA 10.

### ETAPA 10 — Qualidade: golden sample, QC ponta a ponta e a matemática do defeito

Aqui está a alavanca de margem que quase ninguém puxa. Espremer preço rende pouco e machuca a relação; reduzir defeito rende mais e melhora tudo.

**Puxe antes desta etapa:**
- **Golden Sample + Photographic Evidence QC System** (rode `golden sample assinado evidência fotográfica de cada batch QC remoto`)
- **End-to-End QC Checkpoint Chain** (rode `checkpoints QC do sub-vendor à assembly causa raiz conflito de interesse fulfillment`)
- **Go/No-Go Acceptance Criteria** (rode `go no-go acceptance criteria specs ao milímetro pilot batch accelerated age testing`)
- **Defect Rate Margin Math** (rode `defect rate matemática da margem cada ponto percentual custa $32.000 CAC no refund`)
- **CS-as-Defect-Sensor Tracking System** (rode `tracking de defeitos via customer service troubleshoot antes de refund buckets report limpo`)
- **Warranty & Compensation Play** (rode `warranty policy negociada antes over-shipping crédito próxima ordem double dip`)

**10.1 — A matemática que justifica tudo nesta etapa.**

Vender uma unidade defeituosa custa muito mais do que o preço do produto: custo do produto + frete + **o custo de aquisição do cliente** (a parte que todo mundo esquece) + a recompra que não vai acontecer + o dano de reputação (nota pior faz o custo de mídia subir) + o tempo do atendimento.

O caso de referência, num produto de gadget: preço de venda US$ 49,99; produto US$ 5,80; frete US$ 8,75; com retorno de 2,2 sobre o anúncio, o custo de aquisição fica em US$ 22,72 — sobra **US$ 12,73 por unidade vendida**. Quando essa unidade sai defeituosa e vira **reposição**, entram mais US$ 5,80 de produto e US$ 8,75 de frete: aquele cliente vira **prejuízo de US$ 1,82** (recuperável só se a fábrica repõe o produto, e só depois de revender). Quando vira **reembolso**, a receita é zero e você pagou produto + frete + aquisição — os mesmos US$ 5,80 + 8,75 + 22,72 saem do bolso sem nada entrar.

Rodando isso em 100.000 unidades, metade em reposição e metade em reembolso, sem recompra: **cada ponto percentual de defeito custa cerca de US$ 32.000**. Num produto com recompra de 25% (skincare, assinatura), cerca de US$ 44.000. Traduzido em margem: **cada 1% a menos de defeito vale de 3% a 6% de margem de lucro** (na divisão meio a meio). Se a maioria aceita reposição (75% reposição / 25% reembolso), o ganho fica em 2% a 4%; se a maioria exige reembolso (25%/75%), sobe pra 4% a 8%. O ganho é maior quando a taxa de partida é alta: sair de 7% para 6% vale mais que sair de 3% para 2%. E esses números **não incluem** reputação nem horas de atendimento — o benefício real é maior.

**Como aplicar aos números do membro** (a fórmula, com os dados dele — não repita os do caso):
- Custo de uma unidade reposta = custo do produto entregue + frete até o cliente.
- Custo de uma unidade reembolsada = custo do produto entregue + frete até o cliente + custo de aquisição do cliente.
- **Provisão de defeito por pedido = taxa de defeito × (fatia em reposição × custo da reposição + fatia em reembolso × custo do reembolso).**

Esse número vai pro `dados.json` e alimenta a linha de provisão de reembolso da Skill `offer-builder` (ETAPA 13).

**Referências de mercado quando o membro ainda não tem dado próprio:** gadget entre 6% e 10% é comum; skincare com vazamento fica em torno de 5%. Use como ponto de partida marcado como estimativa (`defect_rate_basis: "benchmark"`), nunca como se fosse medição.

**Quando priorizar redução de defeito:** taxa alta, categoria de recompra alta, clientes preferindo reembolso a reposição, ou escala chegando. Em 100 mil unidades por mês com 5% de defeito são 5.000 chamados de atendimento — o time trava.

**10.2 — Golden sample: a referência que decide tudo depois.**

Uma amostra perfeita, que reflete exatamente a unidade final desejada, **assinada** pelo dono da marca (ou representante). A fábrica guarda uma, você guarda outra. Nunca aceite uma amostra de referência abaixo do padrão: ela vira a régua de tudo — inclusive das cobranças futuras.

**10.3 — QC ponta a ponta (a cadeia inteira, não só o fim).**

Fábricas dividem a inspeção em três momentos: **entrada** (o material que chega), **linha** (durante a produção) e **saída** (antes de embarcar). Para todo componente crítico, isso precisa existir também **no fornecedor do componente**, na saída dele. Sem checkpoint na cadeia inteira, um defeito que nasceu num componente vira discussão de "ele disse, ela disse" e nunca acha a causa.

Caso ilustrativo: brinquedos de pelúcia cujo tecido vinha de outra província com problema de costura e bordado. Havia inspeção de terceiro na montagem e fabricante cooperativo — e só resolveu quando um terceiro investigou a causa raiz na PRIMEIRA fábrica, a do tecido.

Como operar isso à distância:
- Peça o **plano de produção** da fábrica primeiro. Entendendo as etapas, você sabe onde pedir evidência.
- Exija **foto e vídeo de CADA lote em cada etapa** (cor, risco, dimensão, encaixe). Com o tempo você reconhece os rostos e as etapas, e passa a detectar padrão.
- Se o problema persistir, contrate **inspeção de terceiro por amostragem de 5% a 10% do pedido** (inspecionar 100% é caro e desnecessário), com o pacote completo de instruções — sem instrução detalhada, sai caro, lento e aberto a interpretação.
- **Receba o relatório da inspeção ANTES de pagar o saldo.** É por isso que a regra de nunca pagar 100% adiantado (ETAPA 8) e o plano de qualidade são a mesma conversa.
- Aprovação de embarque: se a fábrica escolhe as 5 unidades "aleatórias", ela escolhe as perfeitas. Precisa de alguém imparcial puxando unidade de verdade.

**Duas regras que não se dobram:**
- **Nunca deixe a inspeção exclusivamente com o fornecedor** — os incentivos conflitam: qualidade consistente adiciona tempo de ciclo e custo que ele não colocou no preço.
- **Nunca use a empresa de fulfillment como inspetora.** Ela ganha dinheiro embarcando — é conflito estrutural com o jeito que ela faz dinheiro. Caso real: o fulfillment reportou 100% das unidades riscadas; devolvidas à fábrica e reinspecionadas com foto e vídeo, a maioria estava intacta, e o MESMO lote voltou e passou. Além disso, a inspeção do armazém não conversa com quem controla a produção: sem causa raiz, o problema se repete.

**10.4 — Critérios de aceite (transformar "qualidade" em régua).**

Durante a produção piloto, observe as unidades saindo da linha e classifique as imperfeições entre aceitáveis e reprovadas. Especifique **ao milímetro**: um risco de 1mm × 5mm é aceitável, 1,5mm de largura é rejeitado — com amostras de referência mostrando "esse nível passa, esse não". Perfeição de 100% não é compatível com produção eficiente; as concessões precisam ser conscientes e escritas.

- **Suplemento, skincare e beleza:** em vez de milímetro, exija **lote piloto** com as matérias-primas exatas em pequena escala — misturar, testar textura, cor e cheiro contra a amostra de referência, com laudo de análise e calibração de máquina ANTES de cada produção em massa.
- **Eletrônico:** inspeção de bateria por amostragem acordada + **teste de envelhecimento acelerado** (carga e descarga máximas por 80 a 100 ciclos, medindo capacidade e voltagem). Botão, chave e cabo testados lote a lote. Reprovou, o lote inteiro volta pro fornecedor do componente com nova inspeção completa — conte esse atraso no cronograma.

**10.5 — O atendimento como sensor de defeito (e como recuperar o dinheiro).**

O time de atendimento é o único sensor confiável de taxa de defeito que você tem:
1. Treine pra **diagnosticar antes de reembolsar** — boa parte do que chega como "defeito" é uso errado, por falta de instrução ou expectativa mal calibrada.
2. Reposição ou reembolso só com defeito real confirmado.
3. Classifique em **categorias específicas**: chegou morto, não carrega, componente quebrado, não funciona como esperado.
4. Reporte **semanal, mensal e trimestral** — a taxa, as melhorias e os defeitos novos.
5. Compartilhe com a fábrica em formato **limpo e digerível**, só com defeitos reais. Relatório sujo (misturando erro de uso) destrói a sua credibilidade e trava qualquer compensação — fábrica não reconhece erro de uso, e vai te ensinar a educar o cliente.

**Recuperar receita com o fornecedor** (combinado ANTES, nunca cobrado depois): negocie a política de garantia desde o começo — o que ela cobre, o que ela considera defeito de fabricação, qual formato de relatório ela aceita, e o que cobre em dinheiro (preço cheio da venda incluindo frete e aquisição? só a reposição do produto? algo no meio?). Duas formas que funcionam: **embarque a mais** (com 5% de defeito, a fábrica embarca 5% a mais na próxima ordem — no melhor caso, 5% de crédito E 5% a mais) e crédito na próxima ordem. Esteja disposto a devolver unidades para análise, e chegue com sugestão de correção: eles não conhecem o seu mercado nem o seu cliente. Nunca chegue no fim do trimestre com uma lista gigante de cobrança do nada — mata a taxa de sucesso. E use um defeito grande como alavanca antes do próximo pedido: "tenho 12% de devolução e uma ordem de 10.000 unidades pronta; só coloco se vocês me derem solução pra esse defeito."

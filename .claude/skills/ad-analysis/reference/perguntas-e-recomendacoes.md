# Ad Analysis · Referência: 15 perguntas de feedback e recomendações acionáveis (ETAPAs 7 e 8)

> A checklist das 15 perguntas desta skill e as ações por horizonte (imediato, curto e médio prazo), incluindo a conferência das duas automações de proteção e o gate da espiral do ROAS antes de qualquer ação que reduza spend. Abra nas ETAPAs 7 e 8.

### ETAPA 7 — 15 Perguntas de Feedback (checklist desta skill)

Aplique as 15 perguntas (12 numeradas mais 3b, 3c e 3d) aos dados (checklist próprio desta skill — no cenário padrão da Skill `ad-strategy`, a unidade é o AD dentro do ad set do seu conceito, com a leitura de qual CONCEITO o CBO financiou por cima):

1. Qual ad (criativo) teve maior ROAS e por quê? (em ad set `marksman`, responda também no nível do ângulo: qual dos 3 ângulos de `angles[]` venceu — ETAPA 3)
2. Qual teve menor ROAS e por quê?
3. Qual variável específica dentro dos **breakthroughs** tá puxando mais (persona, avatar, formato, ângulo, tema, benefício vs consequência, senso estético — o mapa da Skill `creative-engine`)?
3b. Hook e Hold: onde os losers do batch perderam a audiência — na abertura (hook baixo) ou no corpo (hook bom, hold baixo)?
3c. Quantos conceitos foram testados e qual o `breakthrough_rate` do batch? Ele subiu ou caiu em relação ao batch anterior, e o volume de criativos subiu ou caiu junto?
3d. O ad log explica algum degrau da janela? Alguma **mudança logada ficou sem o efeito esperado**, ou algum **efeito apareceu sem mudança conhecida**? (Contexto 4g + bloco da ETAPA 2 — os dois achados entram na hipótese causal da pergunta 12)
4. Houve variação significativa de performance por primary text?
5. Alguma headline se destacou?
6. Algum placement (Threads, Audience Network) está comendo spend com CPM baixo sem converter? (breakdown do Pi 4)
7. Frequency subiu mais rápido que esperado em algum ad? (sinal de saturação da entrega)
8. CPM variou muito entre ads? (aponta pra diferenças de resposta da audiência por criativo)
9. CTR variou muito? (indicador de hook strength)
10. Conversão CTR→Purchase variou? (indicador de message match)
11. Retention no site (se tiver) — quanto tempo ficam?
12. Qual a hipótese causal principal pro resultado?

Compile respostas num bloco objetivo.

### ETAPA 8 — Recomendações Acionáveis (Imediato / Curto Prazo / Médio Prazo)

**AÇÕES IMEDIATAS (hoje/24h):**
- Pausar losers identificados na Etapa 3 (especificar quais ADS, por nome/`concept_id`)
- Consertar problemas técnicos identificados no 19-point (se houver)
- **Conferir as duas automações de proteção (cânone §6)** que a Skill `ad-strategy` montou na ETAPA 6 dela — elas nascem DESATIVADAS e só protegem se o membro ligou. Leia o estado em `ad-strategy/dados.json → protections` e confirme no Ads Manager > Automated Rules: **(a)** pico de gasto (spend 5× em 24h → pausar) e **(b)** URL de destino ≠ domínio da loja → desligar o ad. Confira também o `daily maximum` de cada ad set de teste (~3× target CPA/dia). Alguma ausente ou desligada → é essa a ação de automação a recomendar. **Não existe rule de escala nem de kill por performance pra verificar** — o Meta recusa condição de performance em CBO; `pgs_enabled` é campo legado fixo em `false` e nunca autoriza prometer escala automática.

**CURTO PRAZO (3-7 dias):**
- Se tem fadiga: trocar os 1-2 criativos mais fatigados do ad set por conceitos novos da `creative-engine`
- Se falta diversidade de funil: gerar novo batch de conceitos (Skill `creative-engine`) com foco na posição faltante
- Se o breakdown por placement (Pi 4) mostrou placement comendo spend sem converter: documentar e decidir a exceção de opt-out

> **Antes de escrever qualquer ação que REDUZA spend** (pausar em bloco, baixar budget, "voltar pro ROAS de antes"): rode `.claude/lib/unit-economics/README.md` §4. ROAS é adimensional e ignora custo fixo — cortar spend por queda de ROAS pode **aumentar** o prejuízo, porque os fixos não encolhem junto e sobra menos receita pra diluí-los. **Se `finance-engine/dados.json` existir, a conta já está feita:** a ação sai do `roas_spiral.verdict` conforme a tabela do PLAYBOOK item 5 — cortar, segurar ou subir spend até `spend_to_breakeven_with_fixed`, com número, não com aviso. Sem o arquivo da `finance-engine`, vale `budget_viability.fixed_costs_monthly`: faça a conta e recomende o que ela disser (às vezes é **subir** spend aceitando ROAS menor). **Sem os fixos em nenhuma das duas fontes, a ação não é "corte X%" — é a pergunta "quanto você tem de custo fixo por mês?"**. Isso não se aplica a pausar um `loser` individual pela régua de kill: ali o critério é o cânone §3, não o ROAS da conta.

**MÉDIO PRAZO (2-4 semanas):**
- Se há breakthrough estável (~7 dias): a promoção pra **ad set próprio em campanha ABO paralela** é decisão de estrutura da Skill `scale-engine` (o cânone `.claude/lib/ad-taxonomy/README.md` §5 aposentou o champions ad set em favor dessa rota, mantendo o ad original rodando no CBO). Aqui você só sinaliza que ele está pronto. `kpi_winner` **não** entra nessa fila.
- Se CPA está melhor que target consistentemente: reavaliar se dá pra escalar mais (vertical + horizontal — delegar pra Skill `scale-engine`)
- Se oferta parece ser o bloqueio: voltar pra Skill `offer-builder` e ajustar (bundle structure, guarantee, stack)
- Se página parece ser o bloqueio: voltar pra `copy-engine`/`page-design` e iterar

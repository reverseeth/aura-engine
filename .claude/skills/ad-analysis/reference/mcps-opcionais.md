# Ad Analysis · Referência: MCPs opcionais (ETAPAs 0.5 e 0.6)

> TrendTrack e Foreplay como camada de benchmark dos breakthroughs, com os limites de chamada. Abra só se houver tools com esses prefixos na sessão.

### ETAPA 0.5 — TrendTrack MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis. Se SIM, use como camada de comparação contextual:

- **`mcp__trendtrack__scan_ad`** nos **breakthroughs** do membro (após classificar — nunca em `kpi_winner`, que não provou nada) → decomposição com lente de mercado: hook archetype, ângulo, reach estimado, scaling assessment. Compara com benchmarks da vertical pra confirmar se o breakthrough é mediocre ou top-tier do mercado.
- **`mcp__trendtrack__daily_radar`** se concorrentes já foram trackados na skill `competitor-analysis` → reporta movimentos recentes (novos ads dos competitors, mudanças de posicionamento). Adiciona contexto pro `NEXT_BATCH_IDEAS.md` final.

Use 1-3 chamadas por análise. Não desperdiçar créditos em criativo perdedor.

Se TrendTrack NÃO estiver disponível, siga ETAPA 1 normalmente.

### ETAPA 0.6 — Foreplay MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__foreplay__` disponíveis (ad spy — 200M+ ads; mesmo padrão de detecção das skills `competitor-analysis`/`creative-engine`). Se SIM, use como camada de benchmark dos **breakthroughs**: depois de classificar o batch (4Pi + Decision Thresholds), compare hooks e formatos deles com os ads ESCALADOS do nicho (busca por marca/vertical) — análogo ao `scan_ad` do TrendTrack acima. O sinal alimenta duas coisas: (a) confirmar se o breakthrough é top-tier do mercado ou apenas o melhor de um batch fraco, (b) apontar formatos/hooks ativos no nicho que o batch ainda não explorou (vai pro `NEXT_BATCH_IDEAS.md`). Limite: 1-2 chamadas por análise — benchmark de breakthrough, nunca em `kpi_winner` nem em criativo perdedor.

Se Foreplay NÃO estiver disponível (ou uma chamada falhar), fallback silencioso: siga com TrendTrack (se houver) ou só com os dados do próprio batch — nada trava, nada é mencionado ao membro. Setup opcional em `.claude/automations/setup-mcps.md` (3.8).

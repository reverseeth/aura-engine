# Creative Engine · Referência: MCPs opcionais (ETAPAs 0.5, 0.6 e 0.7)

> TrendTrack, Foreplay e Higgsfield: o que cada um acrescenta, os limites de chamada e o que muda no entregável quando o Higgsfield está conectado. Abra só se houver tools com esses prefixos na sessão.

### ETAPA 0.5 — TrendTrack MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis. Se SIM, use ANTES de gerar ângulos na ETAPA 3:

- **`mcp__trendtrack__creative_inspiration_pack`** com vertical do produto → retorna hooks, landing pages, ângulos e media benchmarks já validados no nicho. Use como sinal extra na ideação das 3 verticais (junto com VOC + competitor analysis + base Aura).
- **`mcp__trendtrack__scan_ad`** em ads escalados detectados pela skill `competitor-analysis` → decomposição precisa de hook + ângulo + scaling assessment, alimenta Hooks Bank (ETAPA 7) com archetypes reais.

Não substitui a ideação criativa nem força copy-paste de hooks alheios — é input adicional pra evitar reinventar formatos que sabemos que funcionam ou repetir claims já saturados. Limite: 1-2 chamadas por batch.

Se TrendTrack NÃO estiver disponível, siga ETAPAs 1-8 normalmente.

### ETAPA 0.6 — Foreplay MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__foreplay__` disponíveis (ad spy — 200M+ ads em Facebook/Instagram/TikTok/YouTube/LinkedIn, busca por marca e domain intelligence; o watchlist Spyder já entrega transcrição de hooks). Se SIM, use como fonte ADICIONAL de sinal na ideação da ETAPA 3: hooks e formatos ativos dos concorrentes do nicho, ângulos que estão escalando. Mesmo papel do TrendTrack — input de calibração, nunca copy-paste de hook alheio. Limite: 1-2 chamadas por batch. Se NÃO estiver disponível, siga normalmente (setup opcional documentado em `.claude/automations/setup-mcps.md`).

### ETAPA 0.7 — Higgsfield MCP (opcional, se conectado — muda o ENTREGÁVEL da Rota A)

Verifique se há tools com prefixo `mcp__higgsfield__` disponíveis (MCP oficial da Higgsfield — 30+ modelos incluindo Kling 3.x, Veo 3.1 e Sora 2; OAuth via browser, créditos do plano do membro, sem API key). Se SIM, a ETAPA 5.7 (Ramo A) pode, além de salvar os prompts, **renderizar os vídeos in-session**: a skill gera o prompt, chama a tool de geração e salva o asset pronto no workspace — e roda `bash tools/strip-metadata.sh <pasta-dos-assets>` logo depois (todo asset gerado por IA sobe limpo de metadados de proveniência — EXIF/XMP/C2PA, IDs de job do gerador; o script preserva os pixels e o perfil de cor, e renomeia pra `asset-xxxx`). Confirme com o membro antes de gastar créditos ("Higgsfield conectado — quer que eu já renderize os [N] vídeos ou prefere só os prompts?"). Se NÃO estiver disponível, entregue os prompts como sempre — nada muda no fluxo atual.

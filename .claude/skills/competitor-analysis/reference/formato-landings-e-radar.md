# Competitor Analysis · Referência: Formato dos criativos escalados, páginas de destino com tráfego e radar de monitoramento (ETAPAs 3D e 3E)

> O formato como objeto próprio (`ad_formats[]`), as páginas de destino dos ads escalados (`traffic_landings[]`) e o radar de monitoramento pós-launch (`monitoring_radar[]`). Abra na ETAPA 3D.

### ETAPA 3D — Análise de FORMATO dos Criativos Escalados

O formato é um elemento validado tão valioso quanto o ângulo — dois criativos com a mesma mensagem performam diferente conforme a estrutura. Pra cada criativo do top 10 da ETAPA 3 (e os transcritos na 3C), disseque o FORMATO como objeto próprio:

- **Tipo estrutural**: UGC diário/depoimento · VSL curto/longo · lista invertida ("N razões...") · estático de texto longo (story) · demonstração de produto · future-pacing · comparação
- **Duração** (vídeo): segundos exatos + onde o hook termina e o pitch começa
- **Padrão de iteração do concorrente**: o que ele CONGELA e o que ele TROCA entre variações do mesmo winner (ex: copy congelada + hook do vídeo trocado; estático idêntico + headline nova) — esse padrão revela onde o concorrente acredita que está o valor do criativo
- **Evidência de escala do formato**: aparições/duplicatas/dias rodando (mesma régua da ETAPA 3)

Consolide em `dados.json` → `ad_formats[]`: `{ "format": "", "competitor": "", "duration_s": 0, "structure_notes": "", "iteration_pattern": "", "scale_evidence": "", "scale_signal": "high|medium|low" }`. A Skill `creative-engine` lê esse bloco pra montar o batch com formatos JÁ validados por escala — nunca só com ângulos.

### ETAPA 3E — Páginas de Destino com Tráfego + Radar de Monitoramento

**Páginas de destino (traffic landings):** pra cada concorrente ativo, capture PRA ONDE os ads apontam — a URL literal de destino dos criativos escalados (da Meta Ad Library) e, se disponível (TrendTrack/SimilarWeb), quais páginas do domínio mais recebem tráfego. O membro precisa dos LINKS pra abrir e estudar a página que está convertendo agora. Registre em `dados.json` → `traffic_landings[]`: `{ "competitor": "", "url": "", "page_type": "advertorial|landing|pdp|quiz|listicle", "evidence": "destino de N ads escalados / página top de tráfego", "source": "" }`. No `.md`, tabela com os links clicáveis.

**Radar de monitoramento:** liste o que vale vigiar DEPOIS do launch — concorrentes/movimentos que podem mudar o jogo (ex: concorrente testando agora um ângulo novo; rede de afiliado acelerando; marca adjacente entrando no formato). Cada item: o que observar + onde (link) + qual sinal dispara ação. Registre em `dados.json` → `monitoring_radar[]`: `{ "what": "", "where": "", "trigger_signal": "", "action_if_triggered": "" }`. A Skill `ad-analysis` relê esse bloco nas análises de ads.

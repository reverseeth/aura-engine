# Competitor Analysis · Referência: Formato dos criativos escalados, páginas de destino com tráfego, formato das páginas e radar de monitoramento (ETAPAs 3D e 3E)

> O formato do ad como objeto próprio (`ad_formats[]`), as páginas de destino dos ads escalados (`traffic_landings[]`), o formato de cada uma dessas páginas (`landing_formats[]`, com o `dominant_landing_format` que a `page-design` lê) e o radar de monitoramento pós-launch (`monitoring_radar[]`). Abra na ETAPA 3D.

### ETAPA 3D — Análise de FORMATO dos Criativos Escalados

O formato é um elemento validado tão valioso quanto o ângulo — dois criativos com a mesma mensagem performam diferente conforme a estrutura. Pra cada criativo do top 10 da ETAPA 3 (e os transcritos na 3C), disseque o FORMATO como objeto próprio:

- **Tipo estrutural**: UGC diário/depoimento · VSL curto/longo · lista invertida ("N razões...") · estático de texto longo (story) · demonstração de produto · future-pacing · comparação
- **Duração** (vídeo): segundos exatos + onde o hook termina e o pitch começa
- **Padrão de iteração do concorrente**: o que ele CONGELA e o que ele TROCA entre variações do mesmo winner (ex: copy congelada + hook do vídeo trocado; estático idêntico + headline nova) — esse padrão revela onde o concorrente acredita que está o valor do criativo
- **Evidência de escala do formato**: aparições/duplicatas/dias rodando (mesma régua da ETAPA 3)

Consolide em `dados.json` → `ad_formats[]`: `{ "format": "", "competitor": "", "duration_s": 0, "structure_notes": "", "iteration_pattern": "", "scale_evidence": "", "scale_signal": "high|medium|low" }`. A Skill `creative-engine` lê esse bloco pra montar o batch com formatos JÁ validados por escala — nunca só com ângulos.

### ETAPA 3E — Páginas de destino com tráfego, formato de cada página e radar de monitoramento

**Páginas de destino (traffic landings):** pra cada concorrente ativo, capture PRA ONDE os ads apontam — a URL literal de destino dos criativos escalados (da Meta Ad Library) e, se disponível (TrendTrack/SimilarWeb), quais páginas do domínio mais recebem tráfego. O membro precisa dos LINKS pra abrir e estudar a página que está convertendo agora. Registre em `dados.json` → `traffic_landings[]`: `{ "competitor": "", "url": "", "evidence": "destino de N ads escalados / página top de tráfego", "source": "" }`. No `.md`, tabela com os links clicáveis. O formato da página não entra aqui: ele vive só em `landing_formats[]`, casado pela `url`, pra não existirem duas classificações do mesmo endereço.

**Formato de cada página de destino (`landing_formats[]`):** abra cada URL que é destino de ad escalado (mesma cascade resiliente da ETAPA 2) e classifique o formato dela num dos oito valores abaixo. Página que já foi aberta na ETAPA 2 classifica pelo que você já leu ali, sem buscar de novo. Uma entrada por landing page, nunca por ad: ads diferentes que caem na mesma URL somam no `ads_count` da mesma entrada.

| `format` | O que decide a classificação (o elemento concreto na página) |
|---|---|
| `advertorial` | Abre como matéria: headline jornalística, linha de apoio, às vezes assinatura ou data. Narrativa em primeira ou terceira pessoa. Nenhum botão de compra acima da dobra; o fechamento é um link pra outra página |
| `listicle` | Mesma abertura editorial, corpo em lista numerada ("7 razões...", "5 sinais de..."), cada item com subtítulo próprio. Também sem compra no topo |
| `landing` | Página de venda dedicada a uma oferta só, cabeçalho sem menu de loja, promessa e botão acima da dobra, e o fechamento acontece na própria página |
| `pdp_robust` | Página de produto do catálogo (URL com `/products/`), com seletor de variante e carrinho, e mais de seis blocos de conteúdo abaixo da dobra (mecanismo, prova, comparação, perguntas frequentes) |
| `pdp_lean` | Mesma página de produto do catálogo, com três blocos ou menos abaixo da dobra: preço, prova curta e perguntas frequentes |
| `quiz` | A primeira tela faz uma pergunta e o botão avança pro passo seguinte; a recomendação e o preço só aparecem depois das respostas |
| `vsl` | O vídeo ocupa a dobra e é o corpo da página; o botão aparece abaixo do player ou depois de um tempo de reprodução, com pouco texto ao redor |
| `home` | Página inicial do domínio: menu de categorias e mais de um produto em destaque. É ad sem página dedicada |

Registre em `dados.json` → `landing_formats[]`: `{ "url": "", "competitor": "", "format": "", "ads_count": 0, "evidence": "" }`. O `evidence` é o que na página decidiu a classificação, em uma frase e com o elemento que você viu ("headline de matéria e nenhum botão até o terceiro scroll"), nunca a repetição do nome do formato.

**Formato dominante (`dominant_landing_format`):** o formato com a maior soma de `ads_count`. `home` fica fora da conta, porque ad que cai na página inicial é ausência de página dedicada, não escolha de formato. Empate: vence quem tem mais landing pages distintas; persistindo, o do concorrente com mais ads escalados. Menos de três landings classificadas, grave `null`: três é o piso pra chamar um formato de dominante. O campo entra no `resumo` do `dados.json` e é o terceiro sinal da escolha do `page_type` na `page-design`, que pergunta ao membro quando ele diverge da consciência dominante e do tipo de abertura da copy.

> `dominant_format`, no mesmo `resumo`, é o formato dos ADS (ETAPA 3D). `dominant_landing_format` é o das PÁGINAS de destino.

**Radar de monitoramento:** liste o que vale vigiar DEPOIS do launch — concorrentes/movimentos que podem mudar o jogo (ex: concorrente testando agora um ângulo novo; rede de afiliado acelerando; marca adjacente entrando no formato). Cada item: o que observar + onde (link) + qual sinal dispara ação. Registre em `dados.json` → `monitoring_radar[]`: `{ "what": "", "where": "", "trigger_signal": "", "action_if_triggered": "" }`. A Skill `ad-analysis` relê esse bloco nas análises de ads.

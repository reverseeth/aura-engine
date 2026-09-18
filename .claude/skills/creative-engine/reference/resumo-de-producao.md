# Creative Engine · Referência: Resumo de produção e leitura por conceito (ETAPA 8)

> As tabelas do resumo operacional por rota, a tabela de leitura do batch por método, o loop de feedback de creator e a leitura isolada por conceito e por criativo (UTMs no schema da `ad-strategy`). Abra na ETAPA 8.

### ETAPA 8 — Resumo de Produção

Crie um resumo operacional pro membro executar. As linhas variam conforme a rota (ETAPA 1.0):

**Linhas comuns a qualquer rota:**

| Item | Quantidade | Onde editar/gerar |
|---|---|---|
| Primary texts prontos | [N × 2] | Copy pra colar no Ads Manager |
| Headlines prontas | [N × 2] | Copy pra colar |
| Voiceovers a gerar | [Z] | ElevenLabs com scripts fornecidos (voz recomendada: [voz]) |

**Como ler este batch (declarar sempre — muda a leitura de resultado na Skill `ad-analysis`):**

| Conceito | Método | O que o resultado responde |
|---|---|---|
| [c-01] | Marksman | **qual dos 3 ângulos** o mercado favorece — o vencedor vira o ângulo do próximo batch, em Sniper |
| [c-02] | Sniper | **qual execução** do ângulo [X] extrai mais — ângulo já tem direção |

**Se o batch tem creator humano** (algum conceito com archetype `creator_human`, ou UGC comprado de creator): deixe o loop de feedback armado desde já — puxe o **Feedback Loop de Creator (benchmarks de soft metric)**, rode a `best_query` exata `custom report por creator ad name contains thumb stop ratio 42-48% 3s ate 15s Loom`. O nome do ad carrega o nome do creator (é o que permite à Skill `ad-analysis` montar custom report por "ad name contains" e ler resultado POR creator), e a devolutiva pro creator vai em Loom com os benchmarks: **thumb stop ratio bom fica em 42-48%** (régua exigente específica do feedback de creator; a tabela geral de Hook rate — 21/30/40/50+ — vive no cânone §4 e é a mesma métrica), e a retenção dos 3s até os 15s diz se o corpo segurou quem o hook prendeu. Inclua essa instrução de nomenclatura + devolutiva no resumo de produção sempre que houver creator no batch.

**Se Rota A (ou conceitos `ai` no Mix):**

| Item | Quantidade | Onde editar/gerar |
|---|---|---|
| Vídeos a gerar com IA ([modelo escolhido]) | [Y] | Prompts prontos em `prompts/prompt-c0X-video.txt` (modelo longo = roteiro contínuo único) ou pasta `c0X-slug/` (Higgsfield multi-shot). Link/instrução de generation no fim do prompt. Se o Higgsfield MCP rendeu in-session (ETAPA 0.7), os vídeos prontos já estão em `renders/` |
| Imagens a gerar com GPT Image 2.0 | [W] | Prompts em `prompts/prompt-c0X-image.txt` — colar direto no GPT Image 2.0 |
| Limpar metadados (ÚLTIMO passo, depois da edição) | todos os arquivos finais | 2 cliques em `Limpador de Metadados.command`/`.cmd` na pasta da Aura → arraste os criativos finais → suba só os `asset-xxxx` da pasta `Aura Limpos` (item I da ETAPA 4.5 / regra 12). Renders do MCP em `renders/` já saem limpos |

**Se Rota B (ou conceitos `edl` no Mix):**

| Item | Quantidade | Onde editar/gerar |
|---|---|---|
| Ads a montar (EDL) | [V] | Roteiro de montagem em `concept-0X-edl.md` — seguir a tabela timecode no CapCut/editor, usando SÓ footage licenciado (ver bloco de usage rights) |
| Footage a licenciar (se faltando) | [U beats] | Billo/Insense (UGC), stock pago, ou material próprio — marcado `[FALTA FOOTAGE]` no EDL |

**Tempo estimado de produção:** [Rota A IA: 1-2 dias / Rota B montagem com footage em mãos: 1 dia, com UGC a contratar: 3-7 dias / Mix: combinar]

### Isolar a leitura por conceito e por criativo (estrutura 1 CBO → N ad sets)

Na estrutura da Skill `ad-strategy` (1 campanha com CBO → N ad sets, 1 ad set = 1 conceito), cada criativo entra como um **ad individual** dentro do ad set do seu conceito, então o Ads Manager dá breakdown nativo nos dois níveis: por conceito (o ad set) e por criativo (o ad). Para reforçar a leitura e cruzar com Shopify:
- UTMs seguem o **schema canônico da Skill `ad-strategy`** (fonte única — NÃO inventar formato próprio aqui): `utm_content=[concept-id]-[creative-n]` identifica o CRIATIVO (ex: `rootcause-2` — as 3 execuções do pack 3-2-2 nunca dividem o mesmo `utm_content`), e as macros dinâmicas `utm_id={{ad.id}}` + `utm_term={{adset.id}}` dão os identificadores de máquina no breakdown
- Pós-compra, cruzar com Shopify analytics por UTM (o que o Ads Manager mede como purchase nem sempre bate 1:1 com a venda real)
- O Flexible Ads Format do Meta (combinar variações dentro de UM ad) foi **descontinuado em março/2026** — não existe mais como opção no Ads Manager. O parente vivo mais próximo é o toggle **"Flexible media"** do Advantage+ creative (deixa o Meta remixar as mídias entre placements) — sofre da MESMA limitação de breakdown opaco; manter desligado durante teste pra não perder a leitura por criativo. A estrutura é sempre **1 criativo = 1 ad dentro do ad set do seu conceito**, com breakdown nativo por criativo.

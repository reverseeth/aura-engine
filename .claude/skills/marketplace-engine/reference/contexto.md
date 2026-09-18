# Marketplace Engine · Referência: Índice, fronteira com as vizinhas, quando usar, idioma, pré-flight e contexto a carregar

> O texto integral do índice de frameworks, da fronteira com creator-engine, content-recycler e finance-engine, de quando usar, da regra de idioma, do pré-flight que roda mesmo sem prova de canal primário, do contexto a carregar e da tabela dos dados que a skill pede e nunca estima. Abra antes da ETAPA 1.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (domínio `affiliate-creator-channels`, mais entradas de canal em `meta-ads-strategy`, `scaling` e `creatives-hooks-formats` marcadas pra esta skill; mapa skill→domínio no README). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica.
>
> **Fronteira com as skills vizinhas — decorar antes de rodar:** esta skill é dona do **canal de venda** (onde o produto é vendido além do site). O que é **conteúdo e creator** (recrutar, gerenciar, produzir, testar volume orgânico) é da **skill `creator-engine`**. O que é **portar campanha paga pra outra plataforma de mídia** (AppLovin/Axon, TikTok Ads) é da **skill `content-recycler`, Movimento 4**. O que é **conta financeira por canal** (margem com comissão e fee dentro) é da **skill `finance-engine`**. Esta skill decide e opera o canal; ela não produz criativo, não compra mídia e não fecha a conta financeira de canal nenhum.

## Quando Usar

Quando a pergunta é sobre **vender fora do site próprio**: "vale abrir Amazon?", "e TikTok Shop?", "como monto programa de afiliados?", "tem gente revendendo meu produto na Amazon". Gatilhos: "amazon", "tiktok shop", "marketplace", "afiliados", "expandir canal", "vender fora do site".

**Não é fase do pipeline — é consulta lateral, como a `finance-engine`.** O momento natural é o estágio **scaling**: depois que a `ad-analysis` classificou pelo menos um breakthrough estável e a `finance-engine` mostrou a conta fechando com o custo fixo dentro. Re-rodar é normal: a primeira rodada avalia canais (go/no-go); as seguintes atualizam status e métricas dos canais abertos.

**O que esta skill responde e nenhuma outra respondia:** quando abrir um canal de venda secundário, qual abrir primeiro, o que é preciso ter pronto antes de entrar, e como acompanhar cada canal aberto sem misturar a régua dele com a régua do Meta.

**O que ela NÃO faz:** não recruta nem gerencia creators (`creator-engine`), não escreve copy de listagem (`copy-engine` dá as regras de escrita; aqui só a estrutura do canal), não estrutura campanha de mídia em plataforma nova (`content-recycler` M4), não recalcula margem (`finance-engine`), não decide escala dentro do Meta (`scale-engine`).

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno usa esse idioma. Copy que vai pro consumidor final (texto de listagem, mensagem a creator em marketplace US) permanece em inglês, como sempre.

### Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] Prova de canal primário localizada: `manifest.ad_classification[]` com pelo menos um `breakthrough` (gravado pela `ad-analysis`), OU `manifest.finance` mostrando mês fechado saudável (gravado pela `finance-engine`). **Sem nenhuma das duas, a skill RODA mesmo assim** — mas o gate da ETAPA 1 só pode sair `not_yet` ou `blocked_pending_proof`, nunca `expand`. Não é caso de abortar (rule `emergency-escape-paths.md`): a resposta honesta "ainda não, e falta X" é um output válido e útil.

### Contexto a carregar

1. `workspace/profile.md` — stage e budget (linguagem e apetite; ver `member-stage-awareness.md`). Membro `starter` ou `validating`: o veredito quase sempre é "ainda não" — dito sem rodeio, com o que destrava.
2. `workspace/[produto]/manifest.json` — `stage`, `ad_classification[]`, `manifest.finance` (se existir), `manifest.marketplace` (rodadas anteriores desta skill — canais já avaliados/abertos).
3. `workspace/[produto]/ad-analysis/dados.json` **(se existir)** — breakthroughs e winners: são a prova de que existe demanda criada pelo Meta pra transbordar.
4. `workspace/[produto]/finance-engine/dados.json` **(se existir)** — margem de contribuição e runway. A comissão de afiliado e a fee de marketplace entram como **custo variável do canal**: quem fecha essa conta é a `finance-engine`, nunca esta skill.
5. `workspace/[produto]/competitor-analysis/dados.json` **(se existir)** — concorrentes já presentes em Amazon/TikTok Shop são leitura de sofisticação do canal.
6. Rodadas anteriores em `workspace/[produto]/marketplace-engine/`.

### Dados que a skill pede e nunca estima

| Dado | Onde o membro encontra |
|---|---|
| Busca de marca (volume/tendência) | Google Search Console (queries com o nome da marca) ou Google Trends do termo de marca; busca do nome da marca dentro do TikTok |
| Revendedor na Amazon | Buscar o nome da marca/produto na Amazon e olhar quem vende (o membro cola o que vê) |
| Fees reais do canal | Painel do canal (fee de venda da Amazon por categoria, fee do TikTok Shop) |
| GMV e métricas de canal aberto | Painel do canal — GMV é o total vendido dentro do canal |

Ferramentas pagas (Kalodata, FastMoss) seguem a regra dura da Aura: **a AI nunca finge acessar ferramenta paga sem MCP** — diz exatamente o que olhar e trata o retorno como dado colado pelo membro.

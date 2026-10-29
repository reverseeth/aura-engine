---
name: social-engine
description: Instagram da marca no piloto automático. Monta o board de branding no Pinterest (o feed combina com a loja e parece marca de verdade, não perfil de dropshipping), lê os templates prontos do Marketing Studio de imagem do Higgsfield e escolhe os que casam com a marca, gera 9 imagens por dia num grid 3x3 coerente com o produto e a marca cadastrados no Higgsfield (sem Higgsfield, qualquer IA de imagem), escreve a legenda de cada post em inglês com o mecanismo, a oferta e a linguagem real do cliente, mais hashtags e CTA, passa tudo pelo Limpador de Metadados e publica no Instagram pela cascade (API oficial do Instagram com o System User da Meta → Blotato ou Metricool → pacote pronto pra postar). Fecha criando a rotina diária agendada no Claude do membro, que repete o ciclo todo dia sozinha. É consulta lateral, roda depois da page-design ou da creative-engine. Use quando o membro disser "instagram", "social", "posts", "feed", "redes sociais", "postar todo dia", "marketing studio", "conteúdo orgânico".
---

# Social Engine · Lateral <!-- gen:title -->

## Quando usar

Quando a marca precisa de um Instagram vivo, bonito e consistente sem o membro gastar uma hora por dia nisso. O perfil é a segunda coisa que o cliente frio abre depois do anúncio: feed vazio ou desencontrado derruba a confiança que a página construiu. A skill monta a identidade visual do feed uma vez (ETAPAs 1 e 2), produz e aprova o primeiro lote junto com o membro (ETAPA 3), liga a publicação (ETAPA 4) e entrega a rotina que roda sozinha todo dia (ETAPA 5).

Não é fase do pipeline. Momento natural: logo depois da `page-design` (a direção visual da loja já existe e o feed nasce igual a ela) ou da `creative-engine` (os ângulos e hooks já existem). Não faz anúncio pago (`creative-engine` e `ad-strategy`), não faz conteúdo de creator humano (`creator-engine`) e não responde DM nem comentário (`support-engine`).

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova.

1. `workspace/[produto]/manifest.json` existe. Sem ele, escape ES1: ofereça rodar a `setup` inline.
2. Nada mais é obrigatório, mas a legenda fica genérica sem `market-research` (VOC) e sem `offer-builder` (mecanismo e oferta). Se faltar os dois, diga em uma linha e ofereça rodar antes.
3. `report_language` do profile (default `pt-BR`) no relatório e na conversa. Legenda, hashtag e texto em imagem são copy pro consumidor final: sempre em inglês US (ou na língua do público, se o `profile.md` disser outra).

## Contexto a carregar

1. `profile.md`, `manifest.json` e `brand.md` (paleta, tipografia, tom de voz e imagery guidelines já respondidos valem acima de tudo).
2. `brand/brand-tokens.json` (paleta e fontes da marca; sem ele, `page/design-tokens.json`) e `page/page-plan.json` → bloco `reference_board`, se existirem: a direção visual da loja é o ponto de partida do feed. Loja e Instagram precisam parecer a mesma marca.
3. `offer-builder/dados.json` (`resumo`: mecanismo, oferta, garantia, bônus), `market-research/dados.json` (VOC top 20, sub-avatares, dores e desejos) e `creative-engine/` (ângulos e hooks aprovados), lendo primeiro o `resumo` de cada `dados.json`.
4. Rodadas anteriores em `social-engine/` (`dados.json` → `templates_used[]` e `posts_log[]`), pra não repetir template nem legenda.
5. Integrações pelo prefixo de tool (`.claude/lib/mcp-detect/README.md`): Higgsfield (`mcp__higgsfield__`), Shopify (hospedagem do arquivo limpo) e, como alternativa à API oficial do Instagram, Blotato ou Metricool conectados.

## Fluxo da skill

### ETAPA 1 · Board de branding no Pinterest

Leia `reference/board-pinterest.md`. Reaproveite primeiro: board do Pinterest do membro (link colado entra antes de tudo) e o `reference_board` da `page-design`. Depois colete no Pinterest pela tool `WebSearch` (`site:pinterest.com` com nicho, estilo e formato de feed) e abra os pins pelo fetcher da Aura. Board de 9 a 15 referências de feed, cada uma com o eixo que se tira dela (paleta, tratamento de foto, composição, tipografia sobre imagem, ritmo do grid). Feche na direção de feed em três linhas (sensação, assinatura, proibido) e só siga com a aprovação do membro.

### ETAPA 2 · Templates do Marketing Studio e a fórmula do grid

Leia `reference/templates-marketing-studio.md`. Com o Higgsfield conectado: rode o saldo de créditos, liste a marca e o produto no Ads Studio (cadastre se faltar, com as fotos reais do produto), leia o catálogo inteiro de templates de imagem do Marketing Studio e classifique cada um contra a direção da ETAPA 1. Monte o banco de templates aprovados (mínimo 12, pra a rotina girar sem repetir) e a fórmula do grid 3x3 (o papel de cada uma das 9 posições). Sem Higgsfield: a mesma fórmula com prompts autocontidos pra qualquer IA de imagem.

### ETAPA 3 · Primeiro lote de 9, legendas e aprovação

Leia `reference/legendas-e-hashtags.md`. Antes de gerar, diga o custo em créditos do lote e espere o sim (só na primeira configuração; depois a rotina roda dentro do teto aprovado). Gere as 9 imagens pela fórmula do grid, confira cada uma por visão contra a direção (produto fiel, sem texto quebrado, sem mão deformada; refaça o que falhar) e escreva a legenda de cada post: hook na primeira linha, corpo curto com mecanismo, VOC ou oferta, CTA, 15 a 25 hashtags misturando volume e nicho. Mostre o grid montado ao membro e ajuste até ele aprovar. O lote aprovado vira o padrão que a rotina copia.

### ETAPA 4 · Publicação no Instagram

Leia `reference/publicacao-instagram.md`. O Higgsfield gera, mas não posta no Instagram (no MCP dele só existe publicação pro TikTok). Toda imagem passa antes pelo Limpador de Metadados (`bash tools/strip-metadata.sh <pasta>`, regra 12). Cascade: (1) API oficial do Instagram com o System User da Meta (grátis; conta Business ou Creator ligada a uma página do Facebook; token só como segredo, nunca no chat; uma chamada por vez, cada post confirmado antes do próximo); (2) Blotato ou Metricool, pra quem quer os posts espaçados no dia; (3) pacote pronto pra postar em `social-engine/<data>/` com as 9 imagens limpas e as legendas, mais o atalho de agendamento em lote do Meta Business Suite. Nunca pedir senha nem cookie. Publique em ordem reversa da fórmula, pra o grid aparecer montado no perfil. TikTok pelo Higgsfield entra só se o membro pedir.

### ETAPA 5 · Rotina diária agendada

Leia `reference/rotina-diaria.md`. Escreva `social-engine/rotina-prompt.md`, autocontido (a rotina não enxerga o `workspace/`): direção visual, banco de templates, fórmula do grid, produto e marca do Higgsfield, banco de VOC e ângulos, regras de legenda e hashtag, caminho de publicação, teto diário de créditos e a regra de não repetir. Crie a rotina diária no Claude do membro pela skill `schedule` (agente na nuvem, roda com o computador desligado), com o token do Instagram guardado como segredo de rede do ambiente (`graph.facebook.com`). Dispare a rotina uma vez na hora, confira o resultado e só então declare ligado.

## SALVAR

Leia `reference/salvar-e-dados.md`. Em `workspace/[produto]/social-engine/`: `social-engine.md` (direção de feed, board, banco de templates, fórmula do grid, caminho de publicação e rotina), `social-engine.html` por `python3 tools/render_report.py workspace/[produto]/social-engine/social-engine.md`, `dados.json`, `rotina-prompt.md` e as pastas `board/` e `<data>/` de cada lote. Depois `python3 tools/manifest.py <slug> complete social-engine` e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/salvar-e-dados.md`: direção do feed em uma frase, o grid aprovado, por onde publica, a hora da rotina e o custo diário em créditos, como draft que melhora a cada semana de dados.

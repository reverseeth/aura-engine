# Page Design · Referência: Rota 1, do zero com o Claude Design (sub-etapa 3.3)

> O pacote de direção que impede página genérica, a invocação real do canvas de design dentro do Claude Code (quickstart → criar → preencher), o contrato do `page.html` local como fonte única, a iteração com o membro e o caminho de saída quando o canvas não abre. Abra na sub-etapa 3.3.

### 3.3 Rota 1 — Do zero, com o Claude Design (padrão)

A página nasce inteira aqui dentro: as sections do plano na ordem, a copy real da `copy-engine`, a paleta e a tipografia da ETAPA 2 e as imagens do mapa de mídia nos slots. É a rota padrão.

**Nunca de tela em branco.** Gerar do zero sem direção concreta é a causa raiz de página genérica. Antes de escrever uma linha de HTML, tenha na mão (e use, item por item):

- **(a) Os signals da ETAPA 2:** a paleta escolhida com os 8 roles e os tokens que não são de cor (tipografia, radius, sombra, densidade) LITERAIS do preset base — nada digitado de cabeça.
- **(b) O plano da ETAPA 1:** `section_order`, `sections_plan` com blocks e eyebrows, `page_type` e `hero_type`. A estrutura não é escolha de desenho: já foi decidida pelo awareness e pela copy.
- **(c) A copy REAL da `copy-engine`,** section por section. Zero lorem ipsum, zero frase inventada pra caber no layout.
- **(d) As imagens do mapa de mídia da 1.6** (`design/assets/`), com o requisito de hero que o `hero_type` amarra.
- **(e) Uma referência visual concreta:** peça um screenshot de qualquer página cujo visual o membro curta e leia por visão (Read no PNG) pra extrair direção (ritmo, densidade, tratamento de imagem). Se ele não tiver nenhum, use o preset base da ETAPA 2 como âncora visual nomeada e diga qual é.
- **(f) Direção explícita escrita antes de desenhar:** estilo nomeado (ex: "editorial minimalista, respiro alto, prova em números"), o que fazer e o que não fazer, e o anti-genérico — o que evitar pra não sair com cara de template.

#### Abrir o canvas do Claude Design

O canvas roda dentro do Claude Code, pela tool `Artifact`. Três passos, nesta ordem:

1. **Quickstart** (uma vez por página): `Artifact` com `action: "quickstart"`, `intent: "design"` e `design_systems: false` — os tokens já vieram da ETAPA 2 e a cor da marca do membro não é substituída por design system de terceiro. O resultado nomeia o tipo de Artifact de design da conta e devolve o `type_url` dele. **Use o `type_url` que voltar; nunca guarde uma URL fixa no texto da skill nem reaproveite a de outra sessão.**
2. **Criar o Artifact**: publique com aquele `type_url`, um `title` curto (marca + tipo de página, ex: "Nome da marca — landing"), sem arquivos e com `auto_open: "after_first_write"`, pra ele não abrir vazio na cara do membro. O resultado do create traz as instruções do próprio tipo, as páginas que ele manda ler primeiro e o formato dos arquivos de conteúdo: **siga essas instruções**, elas são a fonte da verdade de como preencher o canvas.
3. **Preencher** com a página inteira, na ordem do `section_order`, publicando no `url` desse Artifact. Toda atualização vai pro MESMO `url` — URL nova a cada rodada espalha o trabalho em vários Artifacts e o membro perde o fio.

Avise em uma linha, antes do primeiro publish, que a página abre como Artifact privado na conta claude.ai dele e que o arquivo local continua sendo a fonte. Não é pedido de permissão, é transparência.

#### O contrato do `page.html` (inegociável, vale acima do canvas)

O entregável da rota continua sendo `workspace/[produto]/page/design/page.html`, e é ele que a `page-build` compila:

- HTML + CSS **plano e self-contained**, num `<style>` único no `<head>`. Sem Tailwind, sem framework, sem CDN de CSS.
- **Zero `<script>`**: interação (accordion, tabs, FAQ) por `<details><summary>` e CSS puro.
- Markers `<section data-aura-section="[id do sections_plan]">` em todas as sections — é o que permite o SPLIT determinístico na `page-build`.
- Imagens por caminho relativo pra `design/assets/`, nunca `src` de sandbox temporário.

Escreva o arquivo local e publique **esse mesmo conteúdo** no canvas, pra o que o membro aprova ser exatamente o que vai virar Liquid. Se o membro editar dentro do canvas e a página voltar diferente, releia o Artifact (`action: "read"`), traga a versão nova pro arquivo local e, se ela voltou com utilities ou JS, passe pela normalização da 3.6 antes de salvar.

#### Iterar com o membro

Os comentários que o membro deixar no Artifact chegam pelo `ArtifactComments`; os do chat chegam direto. Em qualquer um dos dois: ajuste o arquivo local, rode o self-review visual da 3.7 de novo e republique no mesmo `url`. Cada rodada salva versão nova (`page-v2.html`...) e entra no `iterations-log.json`, como em toda rota.

#### Quando o canvas não abre

Se o quickstart ou o publish falhar (conta sem Artifacts, erro de rede), **não aborte** (`emergency-escape-paths`): o arquivo local já existe e é a fonte. Siga pelo caminho normal de revisão — screenshots de 1440 e 390 lidos por visão na 3.7 e o checkpoint com o membro abrindo o `design/page.html` no browser dele. Diga em uma linha que o preview no canvas não abriu e que isso não muda o resultado. Se o membro quiser a superfície visual de qualquer jeito, ofereça trocar pra rota 2 ou 3.

#### Fechamento

Régua de qualidade da 3.7 é **bloqueante** aqui como nas outras rotas: rode o self-review visual e corrija inline antes de o membro ver. Registre `design_route: "claude-design"` e, em `design_route_ref`, a URL do Artifact (ou `null` se o canvas não abriu).

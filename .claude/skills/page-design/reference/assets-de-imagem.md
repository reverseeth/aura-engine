# Page Design · Referência: Assets de imagem, inventário e mapa de mídia por section (sub-etapa 1.6)

> O inventário do que o membro tem, o mapa de necessidade de mídia por section com a tabela hero_type → imagem exigida, a rota de geração AI só pra lifestyle com a doutrina foto-real-primeiro e o gate de aprovação com placeholder explícito e `acquisition_plan`. Abra na sub-etapa 1.6.

### 1.6 — Assets de imagem (inventário + mapa de mídia por section)

Página de conversão sem imagem real é wireframe, não página. Causa recorrente de "design aprovado bonito, página no ar feia": o HTML foi aprovado com caixas cinza/stock genérico e ninguém planejou de onde as imagens REAIS viriam. Esta sub-etapa fecha esse furo ANTES do design nascer.

**1. Inventário do que o membro TEM.** Pergunte em uma mensagem só: fotos do fornecedor (AliExpress/Alibaba — packshots, rótulo, embalagem)? Fotos próprias do produto? UGC/lifestyle (cliente usando, contexto real)? Logos/selos (certificações, mídia)? Peça os arquivos/paths e salve os utilizáveis em `workspace/[produto]/page/design/assets/` (nomeie por uso: `hero-lifestyle.jpg`, `packshot-front.png`).

**2. Mapa de necessidade POR SECTION.** Pra cada section do `sections_plan`, decida o que ela precisa de mídia — e registre no campo `media` (schema na 4.1). O `hero_type` amarra o requisito do hero:

| `hero_type` | Imagem que o hero exige |
|---|---|
| value-prop | packshot limpo do produto (fundo neutro) ou produto em contexto |
| dreamstate | lifestyle do RESULTADO (pessoa no estado desejado, produto presente) |
| problem | cena da dor/frustração (sem o produto como herói) |
| segment | pessoa reconhecível do avatar usando/segurando o produto |
| campaign | key visual da campanha (produto + elemento da Big Idea) |

Demais sections: `before-after` exige pares reais; `social-proof` pede rostos/fotos de review quando existirem; `mechanism`/`ingredients` aceitam diagrama/close do ingrediente; `benefits`/`faq`/`guarantee` normalmente vivem de ícone SVG (`media.required: false`).

**3. Rota de geração AI (só pra LIFESTYLE, com a doutrina foto-real-primeiro da skill `creative-engine`).** Quando falta imagem lifestyle/contexto, gere por AI — mas SEMPRE ancorado na foto REAL do produto (composição image-to-image com o packshot real como referência). **NUNCA gere rótulo/embalagem por prompt de texto puro** — o modelo alucina texto e embalagem, e página com rótulo inventado destrói confiança (e é a mesma regra da `creative-engine` pra vídeo). Packshot não se gera do zero: vem do fornecedor ou de foto própria; se o membro não tem NENHUMA foto real do produto, isso é bloqueio de inventário (peça a foto — é pré-requisito de qualquer rota).

> **Com tools `mcp__higgsfield__` na sessão, este passo roda in-session e tem arquivo próprio: `reference/imagens-higgsfield.md` (sub-etapa 1.6.3).** Ele traz o que se gera e o que nunca se gera por `media.kind`, a confirmação com o número de gerações antes de gastar crédito do membro, como o prompt nasce (a âncora única do produto, a proporção do slot, zero texto no quadro), a régua que lê cada imagem por visão antes dela entrar na página, o teto de 3 tentativas por slot e o caminho do arquivo até o slot (reduzir, limpar os metadados por último, registrar em `media`). Sem essas tools, o passo 3 é só o que está escrito acima: o prompt fica salvo pro membro gerar onde ele quiser, ou o slot vira placeholder explícito.

**4. Gate de aprovação (vale pro checkpoint da ETAPA 3).** O `design/page.html` só é apresentado/aprovado com as imagens REAIS nos slots — OU com placeholder **EXPLÍCITO** (bloco visivelmente marcado, ex: caixa cinza com o texto "PLACEHOLDER: hero lifestyle") + plano de obtenção registrado em `sections_plan[].media.acquisition_plan` no `page-plan.json`. Placeholder implícito é PROIBIDO: stock aleatório que parece final, `{{IMAGE}}` invisível, imagem do concorrente esquecida no slot. A `page-build` bloqueia o deploy de qualquer section com imagem vazia/placeholder — resolver aqui é mais barato.

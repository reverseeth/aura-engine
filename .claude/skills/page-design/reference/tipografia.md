# Page Design · Referência: Tipografia, de onde vem e como entra na página (sub-etapa 2.1)

> De onde vem a tipografia (a marca no `brand-tokens.json` ou a direção da ETAPA 3), o que a skill pede ao membro quando a família é de arquivo, a detecção dos arquivos que ele baixou, o bloco de fontes do `design/page.html` e o que vai parar no `design-tokens.json`. Abra na ETAPA 2 e de novo na ETAPA 4, quando a direção trouxer família nova.

## 2.1 — A tipografia vem da marca ou da direção

A skill não tem família padrão. A ordem é esta:

1. **`brand/brand-tokens.json` com `typography.heading` e `typography.body` preenchidos vence.** É a marca do membro, extraída no setup. A família entra como está, e a direção da ETAPA 3 roda com `--keep palette,type`.
2. **Marca vazia** (`source: "none"`) ou sem tipografia: a família sai da direção escolhida na ETAPA 3, na seção `## Tipografia` do `page/direction.md` (`reference/referencias-e-direcao.md`), uma linha por família com o papel (`heading` ou `body`).
3. **O membro pediu uma família pelo nome:** ela vence as duas acima, e o resto da direção se ajusta a ela.

Quantas famílias e qual o par é decisão da direção, não regra desta etapa: o que se confere depois é que a página usa só as famílias que a direção ou a marca declararam.

**Duas coisas que não acontecem aqui.** A Aura não baixa o arquivo pelo membro nem hospeda a fonte em lugar nenhum, e a pasta de fontes de um membro nunca vai parar no clone de outro. E nenhum texto sobre licença entra no que o membro lê: quando a família é de fundição paga, a skill dá o nome e o link da fundição, pede que ele baixe e guarde em `workspace/fontes/`, e continua.

### 2.1.1 — Família de arquivo: pedir em uma mensagem só

Família do Google Fonts não pede nada do membro. Família de arquivo (fundição, ou a fonte própria da marca):

> "A tipografia da página é a [família], [uma frase do porquê, tirada da direção]. Ela não carrega por link: baixe em [link da fundição], salve a pasta em `workspace/fontes/` e me avise. Enquanto isso eu sigo com [família do Google Fonts mais próxima] no lugar, e troco quando os arquivos chegarem."

### 2.1.2 — Detectar os arquivos que o membro baixou

```bash
mkdir -p workspace/fontes
python3 .claude/lib/design-presets/local_fonts.py scan workspace/fontes
```

A saída lista, por família, cada arquivo com peso, estilo, formato e tamanho. O peso sai do metadado do próprio arquivo quando o formato permite ler, e cai pro nome do arquivo só quando não permite — o que importa porque uma família de nove pesos tem Book, Heavy e Ultra, apelidos que ninguém traduz de cabeça pro número que o navegador entende.

- **Nenhuma família encontrada** (o comando sai com código 1): diga ao membro, em uma linha, que a pasta está vazia, repita o caminho e ofereça seguir com a família do Google Fonts mais próxima enquanto isso. Não trave a skill esperando o download.
- **Mais de uma família na pasta** (pacote de fundição costuma trazer subfamílias e variantes): mostre os nomes encontrados e pergunte qual entra na página. Daí em diante passe `--family "<nome>"` em todo comando.
- **Pesos disponíveis menores que os pesos da página**: use a interseção. Com `400` e `700` na pasta, a página usa 400 e 700, e o peso intermediário sai da escala tipográfica, não de um arquivo que não existe.

### 2.1.3 — Pôr a fonte dentro da página que o membro vai olhar

A fonte fica ao lado do HTML, no mesmo lugar e com o mesmo tratamento das imagens da página. São dois comandos, nesta ordem: copiar os arquivos pra dentro da pasta do produto e gerar o bloco de `@font-face` que aponta pra eles.

```bash
# 1. só os pesos que a página usa, já no formato preferido
python3 .claude/lib/design-presets/local_fonts.py copy workspace/fontes \
  --family "<família>" --weights 400,500,700 \
  --to workspace/[produto]/page/design/assets/fonts

# 2. o bloco de @font-face apontando pra eles
python3 .claude/lib/design-presets/local_fonts.py css \
  workspace/[produto]/page/design/assets/fonts \
  --mode relative --family "<família>"
```

A cópia existe pra `page-build` não depender da pasta pessoal do membro: o design carrega tudo que precisa de dentro da pasta do produto.

O comando devolve um bloco `<style data-aura-fonts="[família]">` pronto. Cole no `<head>` do `design/page.html` (e da comparadora da 2.3), **sempre como primeiro bloco de estilo e sempre com o atributo `data-aura-fonts` intacto**. O atributo não é enfeite: é por ele que a `page-build` acha o carregamento de fonte, tira ele do caminho antes de compilar e troca pelo asset do tema. Sem o atributo, o caminho `assets/fonts/...` vai pro Liquid apontando pra um lugar que não existe na loja, e a página sobe na fonte de fallback.

O modo é sempre `--mode relative`, em toda etapa desta skill (comparadora, `page.html`, captura do QA). Fonte embutida em base64 pesa no `html_css_kb` e foge do contrato que a `page-build` desmonta; o `--mode asset` é só da `page-build`.

Família do Google Fonts não precisa de nada disso: o `<link>` no `<head>` resolve, e os pesos saem do campo `google_fonts` do registro.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<Família>:wght@400;500;600;700&display=swap">
```

### 2.1.4 — A decisão sai na comparadora quando há mais de uma candidata

Com a marca já decidida, não há o que comparar. Sem marca, a direção escolhida na ETAPA 3 já fecha a família; a comparadora da 2.3 só entra quando o membro quer ver duas famílias lado a lado na página real.

### 2.1.5 — O que gravar

A tipografia vive no `page.html`, e é dali que o arquivo de tokens nasce. Duas coisas no HTML:

- `--font-heading` e `--font-body` no `:root`, com a pilha completa e os fallbacks (contrato de variáveis de `reference/design-tokens.md`);
- o bloco `data-aura-fonts` da 2.1.3 com os `@font-face`, ou o `<link>` do Google Fonts com os pesos exatos.

Na ETAPA 6, o `tools/page-qa/tokens.py` lê os dois e grava `type.heading_font`, `type.body_font` e `type.families[]` no `design-tokens.json`, que é o que a `page-build` abre no passo de web fonts:

```json
"families": [
  { "name": "<família>", "role": "heading | body | both", "provision": "local_files", "weights": [400, 500, 700], "files_dir": "page/design/assets/fonts" },
  { "name": "<família>", "role": "body", "provision": "google_fonts", "weights": [400, 600], "files_dir": null }
]
```

- `provision` diz por qual caminho a família carrega: `local_files` (arquivo copiado na 2.1.3), `google_fonts` ou `system`.
- `files_dir` é relativo à pasta do produto e aponta pra cópia guardada na 2.1.3, nunca pra `workspace/fontes/`.
- `weights` sai dos `@font-face` do bloco `data-aura-fonts`: declare só os pesos que a página usa de verdade. Peso declarado e não usado é KB a mais no carregamento.

Ninguém escreve esse bloco à mão. Página antiga (sem `schema_version`) tem o mesmo bloco como `typography` no `design-signals.json`, e a `page-build` continua lendo de lá nesse caso.

### 2.1.6 — Pendência, quando ela existe

A família de arquivo não chegou a tempo e o membro seguiu com a substituta do Google Fonts: registre no `page-plan.json`, em `brand_discovery`, a família pendente e o caminho onde os arquivos são esperados, e diga a ele em uma linha que trocar a fonte depois é rodar a `page-design` de novo a partir da ETAPA 4 — a página é refeita com a tipografia nova, e nada mais muda.

A Aura não baixa nem hospeda fonte, e nada sobre licença entra no que o membro lê.

# Page Design · Referência: Tipografia, as duas sugestões padrão (sub-etapa 2.1)

> As duas famílias que abrem a escolha (ABC Oracle e Geist), o que o membro faz em cada uma, a detecção dos arquivos que ele baixou, o bloco de fontes do `design/page.html` e o que vai parar no `design-signals.json`. Abra no começo da ETAPA 2, antes da cascade de cor.

## 2.1 — A escolha de tipografia abre com duas famílias nomeadas

Antes de qualquer cascade, de qualquer preset e de qualquer referência, a skill mostra duas famílias e só duas. O registro delas é o bloco `suggested_typefaces` de `.claude/lib/design-presets/presets.json`: nome, origem, link, pesos da página e como cada uma é carregada. Leia dali, nunca de cabeça.

| Família | O que ela é | O que o membro faz |
|---|---|---|
| **ABC Oracle** (Dinamo) | Sans serif de contornos suaves e contraste sutil, com um traço mecânico que dá ar de marca autoral. Aguenta título e corpo. | Baixa na página da fundição, https://abcdinamo.com/typefaces/oracle, e coloca a pasta em `workspace/fontes/`. |
| **Geist** (Vercel) | Grotesca de tela, desenhada pra interface: neutra, fácil de ler em qualquer tamanho, faixa de peso larga. | Nada. Carrega por link, na hora. |

**Duas coisas que não acontecem aqui.** A Aura não baixa o arquivo pelo membro nem hospeda a fonte em lugar nenhum, e a pasta de fontes de um membro nunca vai parar no clone de outro. E nenhum texto sobre licença entra no que o membro lê: a skill sugere a fonte, dá o link e continua.

### Antes de perguntar qualquer coisa

1. **`workspace/[produto]/brand.md` com tipografia já definida vence.** O arquivo é a marca do membro, e a ETAPA 2 promete não repetir pergunta que ele já respondeu. Nesse caso a 2.1 não oferece nada: registra a família do `brand.md` e passa direto pra 2.2. Se a família do `brand.md` for de arquivo local, a detecção da 2.1.2 continua valendo.
2. **Uma família só na página inteira é o padrão**, com a hierarquia vindo do peso e do tamanho, não da mistura. Duas famílias entram apenas quando o membro pede ou quando o `brand.md` já traz um par. Nunca mais de duas.

### 2.1.1 — Apresentar e perguntar (uma mensagem só)

> "Pra tipografia da página eu sugiro duas:
> **ABC Oracle**, da fundição Dinamo. [uma frase do campo `vibe`]. Você baixa em https://abcdinamo.com/typefaces/oracle, salva a pasta em `workspace/fontes/` e me avisa.
> **Geist**. [uma frase do campo `vibe`]. Essa não pede nada de você: carrega direto.
> Quer ver as duas aplicadas na sua página? Se não curtir nenhuma, eu tiro a tipografia da referência visual que a gente usar pra cor."

Quer as duas na comparadora e ainda não baixou a Oracle: mande baixar agora, com o link e o caminho. Não quer baixar nada: a comparadora vai com a Geist. Recusou as duas: a tipografia sai da cascade da 2.2, como antes desta etapa existir.

### 2.1.2 — Detectar os arquivos que o membro baixou

```bash
mkdir -p workspace/fontes
python3 .claude/lib/design-presets/local_fonts.py scan workspace/fontes
```

A saída lista, por família, cada arquivo com peso, estilo, formato e tamanho. O peso sai do metadado do próprio arquivo quando o formato permite ler, e cai pro nome do arquivo só quando não permite — o que importa porque uma família de nove pesos tem Book, Heavy e Ultra, apelidos que ninguém traduz de cabeça pro número que o navegador entende.

- **Nenhuma família encontrada** (o comando sai com código 1): diga ao membro, em uma linha, que a pasta está vazia, repita o caminho e ofereça seguir com a Geist enquanto isso. Não trave a skill esperando o download.
- **Mais de uma família na pasta** (a Oracle vem com subfamílias, e o pacote costuma trazer variantes): mostre os nomes encontrados e pergunte qual entra na página. Daí em diante passe `--family "<nome>"` em todo comando.
- **Pesos disponíveis menores que os pesos da página**: use a interseção. Com `400` e `700` na pasta, a página usa 400 e 700, e o peso intermediário sai da escala tipográfica, não de um arquivo que não existe.

### 2.1.3 — Pôr a fonte dentro da página que o membro vai olhar

A fonte fica ao lado do HTML, no mesmo lugar e com o mesmo tratamento das imagens da página. São dois comandos, nesta ordem: copiar os arquivos pra dentro da pasta do produto e gerar o bloco de `@font-face` que aponta pra eles.

```bash
# 1. só os pesos que a página usa, já no formato preferido
python3 .claude/lib/design-presets/local_fonts.py copy workspace/fontes \
  --family "ABC Oracle" --weights 400,500,700 \
  --to workspace/[produto]/page/design/assets/fonts

# 2. o bloco de @font-face apontando pra eles
python3 .claude/lib/design-presets/local_fonts.py css \
  workspace/[produto]/page/design/assets/fonts \
  --mode relative --family "ABC Oracle"
```

A cópia existe pra `page-build` não depender da pasta pessoal do membro: o design carrega tudo que precisa de dentro da pasta do produto.

O comando devolve um bloco `<style data-aura-fonts="[família]">` pronto. Cole no `<head>` do `design/page.html` (e da comparadora da 2.3), **sempre como primeiro bloco de estilo e sempre com o atributo `data-aura-fonts` intacto**. O atributo não é enfeite: é por ele que a `page-build` acha o carregamento de fonte, tira ele do caminho antes de compilar e troca pelo asset do tema. Sem o atributo, o caminho `assets/fonts/...` vai pro Liquid apontando pra um lugar que não existe na loja, e a página sobe na fonte de fallback.

**Quando o HTML precisa viajar sozinho** (o membro quer mandar o arquivo por mensagem, abrir de outro computador, guardar fora da pasta), troque o modo por `--mode inline`: o bloco sai com a fonte embutida em base64, e o arquivo abre certo em qualquer lugar, sem a pasta ao lado. O resto do fluxo é idêntico, inclusive o atributo.

Família do Google Fonts não precisa de nada disso: o `<link>` no `<head>` resolve, e os pesos saem do campo `google_fonts` do registro.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap">
```

### 2.1.4 — A decisão sai na comparadora, não aqui

A tipografia é escolhida olhando, junto da paleta, na página comparadora da 2.3. A 2.1 fecha só o conjunto de candidatas: uma quando o `brand.md` já decidiu ou o membro recusou as duas, duas quando ele quer comparar Oracle e Geist.

**A tipografia decidida aqui vence a que vier da cascade de cor.** O Refero, o print lido por visão e o preset base do gerador trazem família junto com a paleta; quando a 2.1 fechou uma família, dos caminhos da 2.2 entram cor, radius, sombra e densidade, e a tipografia deles é descartada.

### 2.1.5 — O que gravar

No `design-signals.json`, além de `heading_font` e `body_font` (a stack completa, com os fallbacks), grave o bloco `typography`, que é o que a `page-build` lê pra provisionar:

```json
"typography": {
  "provision": "google_fonts | local_files | system | mixed",
  "families": [
    {
      "name": "ABC Oracle",
      "role": "heading | body | both",
      "provision": "local_files",
      "weights": [400, 500, 700],
      "files_dir": "page/design/assets/fonts",
      "formats": ["woff2"]
    },
    {
      "name": "Geist",
      "role": "both",
      "provision": "google_fonts",
      "weights": [400, 500, 600, 700]
    }
  ]
}
```

- `provision` no topo é o resumo do conjunto (`mixed` quando a página usa uma família de cada origem).
- `files_dir` é relativo à pasta do produto e aponta pra cópia guardada na 2.1.3, nunca pra `workspace/fontes/`.
- `weights` lista só os pesos que a página usa de verdade. Peso declarado e não usado é KB a mais no carregamento.
- Família de sistema (Georgia, `-apple-system`) entra com `provision: "system"` e sem `weights`.

O mesmo bloco é espelhado em `type.families[]` no `design-tokens.json` (`reference/design-tokens.md`), que é o arquivo que a `page-build` abre no passo de web fonts.

### 2.1.6 — Pendência, quando ela existe

Membro escolheu a Oracle, a comparadora rodou com a Geist porque os arquivos não chegaram a tempo e ele seguiu assim: registre no `page-plan.json`, em `brand_discovery`, a família pendente e o caminho onde os arquivos são esperados, e diga a ele em uma linha que trocar a fonte depois é rodar a `page-design` de novo a partir da ETAPA 2 — a página é recompilada com a tipografia nova, e nada mais muda.

# Real-People Imagery Director — imagens estáticas de pessoas reais com o produto

> Camada de REGRAS por cima do `gpt-image-2-director.md` (ou de qualquer gerador de imagem que o membro use — Higgsfield, Midjourney, GPT Image). O director de imagem define o FORMATO do prompt; este arquivo define o que o prompt precisa conter quando há **pessoa fotorrealista** na imagem. Vale pra: fotos de review na PDP, seções tipo "a closer look", UGC estático pra ad, unboxing estático, pessoa aplicando/segurando/usando o produto.

## Por que existe

Imagem de pessoa gerada por IA falha de dois jeitos caros: (1) **cara de IA** — pele plástica, modelo genérica, estúdio vazio — que derruba a credibilidade exatamente na seção que existe pra dar prova; (2) **reprovação no Meta** — pele demais, contexto ambíguo. As regras abaixo vêm de iteração real com membros e matam os dois problemas.

## As 7 regras (todas obrigatórias no prompt)

### 1. Pessoa crível, nunca modelo

O prompt NUNCA usa "beautiful woman", "attractive model", "perfect skin". Use: **"real-looking person, pleasant but not model-like"** + textura: `natural skin texture with visible pores, a few stray hairs, natural asymmetry, no retouching`. Review com foto de modelo profissional LÊ como fake — o objetivo é a foto que um cliente de verdade tiraria.

### 2. Públicos mistos, distribuídos POR PESQUISA

Nunca gere um lote de reviews com pessoas do mesmo gênero e da mesma idade — isso não existe em base de clientes real e o membro percebe na hora. Antes de gerar o lote, leia os avatares de `02-market-research/dados.json` e distribua os segmentos conforme o mercado REAL do produto (ex: 60% mulheres 45-65, 25% homens 40-60, 15% mulheres 30-40 — os números vêm da pesquisa, não de chute). Cada prompt do lote nomeia idade aproximada, gênero e um traço de contexto diferente.

### 3. Zero pele exposta (risco de reprovação e ban)

Mesmo quando o produto pede contato com a pele (patch no ombro, creme no rosto): **roupa presente e modesta sempre** — regata/camiseta pra ombro, pijama/sleepwear comportado pra cena de cama, nunca ombros nus + lençol (lê como nudez implícita pro reviewer da plataforma). Escreva a peça de roupa NO prompt (`wearing a soft gray tank top`), não deixe o gerador decidir.

### 4. Embalagem real como referência anexada

Gerador de imagem ALUCINA rótulo e formato de embalagem se não receber referência. Sempre: (a) anexe a foto real da embalagem como referência (`<<<image_1>>>` na convenção dos directors); (b) nomeie o formato correto no prompt — **box** ≠ sachê ≠ pouch ≠ frasco (errar o formato invalida a imagem inteira); (c) instrua `label and packaging exactly as in the reference image, do not redesign`.

### 5. Specs de câmera e luz (o que mata o plástico)

Prompt sem specs de câmera devolve render 3D. Nomeie equipamento e luz reais:

- **Câmera + lente**: `shot on [Hasselblad X2D / Canon R5 / iPhone 15 Pro], [90mm f/2.5 | 35mm f/1.8]` — iPhone pra estética UGC crível; câmera de médio formato pra cena editorial premium.
- **Luz**: `soft window light` / `warm bedside lamp` / `overcast daylight` — nunca "studio lighting" em cena de review.
- **Textura de foto**: `subtle natural grain, slight depth of field, no HDR look`.

### 6. Contexto imperfeito (casa de verdade)

Fundo de review é casa vivida, não estúdio: `slightly cluttered nightstand with a glass of water and a book`, `unmade bed with natural wrinkles`, `kitchen counter with everyday objects softly out of focus`. Um objeto "fora do lugar" por cena é o que faz a foto ler como real.

### 7. Aspect ratio pelo destino

- **9:16** — seções verticais de página (galeria tipo "a closer look", stories).
- **4:5 ou 1:1** — feed, grid de reviews.
- Declare o ratio no prompt; nunca deixe o default do gerador decidir.

## Estrutura do prompt (ordem)

```
[pessoa: idade aproximada + gênero + aparência crível (regra 1) + roupa (regra 3)]
[ação com o produto + embalagem por referência (regra 4)]
[cenário imperfeito (regra 6)]
[luz + câmera/lente + textura (regra 5)]
[aspect ratio (regra 7)]
[negativos: no retouching, no studio look, no model-like features, packaging exactly as reference]
```

**Exemplo genérico (adapte produto/segmento):**

> A woman in her late 50s with natural gray-streaked hair and realistic skin texture (visible pores, no retouching), wearing a soft cotton pajama top, sitting on the edge of an unmade bed, holding the product box from `<<<image_1>>>` — label and packaging exactly as in the reference image, do not redesign. Slightly cluttered nightstand with a water glass and reading glasses, softly out of focus. Soft warm bedside lamp light, shot on iPhone 15 Pro, subtle natural grain, slight depth of field, no HDR. Vertical 9:16. No model-like features, no studio look.

## Pós-processo obrigatório (antes de QUALQUER upload)

1. **Limpar metadados**: `bash tools/strip-metadata.sh <arquivo|pasta>` — remove EXIF/XMP/IPTC/C2PA (incluindo IDs de job do gerador) sem alterar pixels, e renomeia pra `asset-<hex>`. Imagem gerada sobe SEMPRE limpa.
2. **Disclosure continua valendo**: o strip de metadados NÃO substitui o rótulo "AI Info" da Meta — humano fotorrealista gerado por IA exige o disclosure no upload do ad (gate das Skills 08/10). Metadado limpo é higiene de asset; disclosure é obrigação de plataforma.
3. **Review humano do lote**: antes de subir, o membro olha o lote inteiro de uma vez — mão com 6 dedos, texto derretido no rótulo e duplicata de rosto entre "clientes" diferentes são os 3 defeitos que passam batido em foto individual e explodem em conjunto.

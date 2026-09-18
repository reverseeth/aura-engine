# Product Research · Referência: Decomposição em elementos validados (ETAPA 4)

> A tabela dos sete elementos com exemplos, a consolidação do pool cruzado e a régua de saturação (aberto, saturado, não validado) que alimenta `validated_elements[]`. Abra na ETAPA 4.

### ETAPA 4 — Decomposição em elementos validados

Aqui a skill deixa de olhar marca por marca e passa a olhar **peças**. Pra cada finalista, quebre a marca em elementos e registre, ao lado de cada um, a **evidência de validação** (dias no ar do ad mais antigo, ad rank, duplicatas, tráfego da loja, nº de ads ativos no mesmo ângulo):

| Elemento | O que é | Exemplo |
|---|---|---|
| **Mecanismo do problema** | a causa raiz que a marca nomeia pra explicar por que as soluções comuns falham | "your gut lining is leaky, that's why probiotics never worked" |
| **Mecanismo da solução** | o ingrediente/processo/forma que resolve a causa raiz, com nome | "butyrate-first formula", "8-hour release" |
| **Ângulo** | a razão de compra que o ad usa | custo anual da alternativa; "I tried everything"; identidade ("for women over 45") |
| **Formato do produto** | a forma física | gummy, pó em sachê, shot, cápsula, patch |
| **Posicionamento / avatar** | com quem a marca fala e como se enquadra | "a marca do despertar das 3h", "gut health pra quem usa GLP-1" |
| **Formato de criativo** | o tipo de peça que mais escala | native image de copy longa; UGC talking head; demo |
| **Estrutura de oferta** | como a marca sobe o ticket | 3-pack + assinatura + upsell de sono |

Depois, consolide o **pool cruzado de elementos validados** (todas as marcas juntas), agrupando elementos iguais/quase iguais e contando **em quantas marcas escaladas cada um aparece**:

- Elemento presente em **1-2 marcas** escaladas = **validado e ainda aberto** (a melhor matéria-prima).
- Elemento presente em **3+ marcas** no mesmo ângulo = **validado e saturado** naquele ângulo — só entra numa jogada se vier com outro ângulo, outro formato ou aprimorado (ETAPA 6).
- Elemento que nenhuma marca escalada usa = **não validado** — não entra em jogada nenhuma (é criação do zero).

Esse pool é a `validated_elements[]` do `dados.json` e a semente da `validated_library` que a Skill `competitor-analysis` constrói em profundidade.

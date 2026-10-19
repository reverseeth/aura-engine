# Offer Builder · Referência: Oferta irrecusável contra o concorrente (ETAPA 4.5)

> A tabela lado a lado com a oferta do concorrente principal, a regra de vencer em pelo menos 2 eixos visíveis mais um diferencial que ele não tem, o teste "burro de dizer não" como gate de save e o registro em `competitor_comparison`. Abra depois da garantia (ETAPA 4).

### ETAPA 4.5 — Oferta irrecusável

Diferenciar não basta. A oferta precisa ser tão boa que o cliente se sinta burro em dizer não (Hormozi, *$100M Offers*). A equação de valor diz por onde subir: **valor = (resultado sonhado × probabilidade percebida de conseguir) ÷ (tempo até o resultado × esforço e sacrifício)**. Cada item do stack, da garantia e do bônus tem que mexer em pelo menos um desses quatro termos.

**Puxe o sistema antes de montar** (rode a `best_query` exata, `deep=true`): `Hormozi value equation dream outcome perceived likelihood time delay effort sacrifice` e `Hormozi grand slam offer creation problems solutions list trim and stack value`. Não repita se já foi puxado na sessão.

**1. Escolha o concorrente principal.** É o que mais escala no `competitor-analysis/dados.json` (mais dias no ar e mais anúncios ativos no mesmo ângulo). Abra a página dele e leia a oferta como o cliente lê.

**2. Monte a tabela lado a lado** (vai na ficha do doc):

| Eixo | Concorrente principal | Nossa oferta | Quem vence |
|---|---|---|---|
| Preço por unidade ou dose (no bundle mais vendido) | | | |
| Bundle mais vendido (o que leva e por quanto) | | | |
| Bônus e brindes | | | |
| Garantia (prazo e mecânica) | | | |
| Frete | | | |
| Prazo de entrega | | | |
| Diferencial que só a gente tem | — | | Nós |

**3. A régua.** A nossa oferta vence em **pelo menos 2 eixos que o cliente enxerga em 5 segundos** (preço por dose, brinde físico, garantia, frete) **e** tem **1 diferencial que o concorrente não tem** (o mecanismo nomeado, um acessório que acelera o resultado, uma garantia com mecânica que ele não oferece). Sem estoque, prazo de entrega maior é o eixo que a gente perde: compense em dois outros.

Por onde subir quando falta eixo, nesta ordem (o membro prefere físico a digital):
- **Brinde físico** que acelera ou facilita o resultado (acessório de uso, dosador, nécessaire, o complemento que passou no Gate de Complementaridade)
- **More-of-same** no bundle (mais unidades pelo mesmo preço percebido, preço por dose abaixo do concorrente)
- **Garantia mais forte** que a dele (prazo maior, contada da entrega, mecânica de "devolva o pacote vazio")
- **Frete grátis** a partir do bundle mais vendido
- Só então bônus digital, e só se o avatar realmente consome esse formato

Cada mudança volta pra conta da ETAPA 5: o item entra no `cogs_breakdown` ou no stack, e a margem é recalculada.

**4. Teste "burro de dizer não" (gate de save).** Leia a ficha como o avatar do market research, com a objeção número 1 dele na cabeça, e responda: comparando com o concorrente principal e com não fazer nada, recusar esta oferta seria uma decisão burra? Passa quando as três frases abaixo são verdadeiras e cabem na ficha:
- "Por [preço], você leva [o que leva], que no concorrente custa [comparação]."
- "Se não funcionar, [garantia]: o risco é todo nosso."
- "E ainda vem [o diferencial], que ninguém mais oferece."

Não passou: reforce stack, garantia ou brinde físico e refaça a tabela. A oferta só é salva com o teste aprovado.

**Registro em `offer-builder/dados.json`:**

```json
"competitor_comparison": {
  "competitor": "nome da marca",
  "competitor_url": "url da oferta lida",
  "rows": [
    { "axis": "price_per_unit", "competitor": "...", "ours": "...", "winner": "ours | competitor | tie" }
  ],
  "wins_visible": 3,
  "unique_differentiator": "o que só a gente tem, em meia linha",
  "no_brainer_lines": ["as 3 frases do teste, em inglês US, prontas pra copy"],
  "no_brainer_test": "pass"
}
```

A `copy-engine` usa as `no_brainer_lines` como espinha do bloco de oferta da página.

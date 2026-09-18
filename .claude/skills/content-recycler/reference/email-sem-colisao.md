# Content Recycler · Referência: A derivada de email não colide com os flows da retention-engine

> O que a sequência de email desta skill é e o que ela não é, por que ela não valida ângulo, e as três regras para não desligar nem duplicar os flows de lifecycle. Abra ao gerar a derivada de email.

## Email-sequence: não colidir com os flows da Skill `retention-engine`

A derivada `email` que esta skill gera é uma **variação A/B de nutrição derivada do breakthrough** — uma sequência de e-mails que reaproveita o ângulo/hook do criativo pra testar outra mensagem de nutrição. Ela **NÃO é um flow de lifecycle** e **NÃO substitui nem sobrescreve** o welcome / post-purchase / abandoned-cart da **Skill `retention-engine`** (que é a fonte única de verdade dos flows de retenção).

Ela também **não valida nada**: e-mail fala com quem já é cliente ou já é lista, então o resultado dele não diz se o ângulo funciona em tráfego frio. Validação de ângulo e de oferta acontece na Trilha 1, no tráfego pago.

Regras pra não colidir:
- **Nunca** instruir o membro a importar essa sequência "como welcome flow" no Klaviyo — isso desligaria/duplicaria o welcome da `retention-engine`.
- Posicionar como **flow separado / teste paralelo** (ex: segmento de teste, ou campanha one-off), que roda **ao lado** dos flows da `retention-engine`, não no lugar deles.
- Se o membro ainda não rodou a Skill `retention-engine`, recomendar rodar a `retention-engine` primeiro (welcome/post-purchase são baseline de retenção) e usar esta derivada só como variação de teste depois.

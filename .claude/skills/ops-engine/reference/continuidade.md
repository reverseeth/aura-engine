# Ops Engine · Referência: Continuidade, o checklist de backups e o risco de pessoa-chave (ETAPA 2)

> O princípio de planejar pro pior cenário, a tabela dos nove itens do checklist com o que 'pronto' significa em cada um, o recorte para quem está começando, as três perguntas do risco de pessoa-chave com a métrica de dores de cabeça por dólar, e o formato da lista de riscos abertos. Abra na ETAPA 2.

### ETAPA 2 — Continuidade: o checklist de backups e o risco de pessoa-chave

O princípio da fonte primária (P1): planejar pro PIOR cenário, não pro melhor — conta banida, processadora segurando repasse, fábrica sem capacidade, atendimento afogado. Redundância é barata perto do que ela evita, e **"você não pode financiar o caos"**: dívida e float não consertam operação quebrada (a régua de caixa disso é da `finance-engine`).

Monte o checklist COM o membro, item a item, cada um com status confirmado (`ready` / `in_progress` / `missing` / `not_applicable`):

| # | Item | O que "pronto" significa |
|---|---|---|
| 1 | **Business Manager + conta de anúncio reserva** | Estrutura da `setup` viva (pixel isolado num BM próprio, conta de anúncio em outro) E uma conta reserva aquecida com **campanhas pré-montadas e desligadas** — se a conta principal cair no meio da escala, liga-se a reserva no mesmo dia, sem recomeçar do zero. |
| 2 | **3 admins reais em cada BM** | Os mesmos 3 perfis reais (o membro + família/amigos de confiança) em todos os BMs. Nunca perfil comprado. Um admin banido não pode significar perder o acesso a tudo. |
| 3 | **Página fora do BM** | Página criada no perfil pessoal, não dentro do BM (sobrevive a banimento de BM). |
| 4 | **Processadora de pagamento reserva** | Uma segunda processadora (ex.: Stripe ou Airwallex no básico) já configurada e testada com uma transação — não "sei que existe". E o membro sabe o que a processadora principal olha pra segurar repasse (redes sociais da marca, termos de serviço, taxa de chargeback): retenção de repasse acontece MESMO com chargeback baixo, e o risco real de recorrência mal sinalizada não é o reembolso, é perder a processadora. |
| 5 | **Banco reserva** | Segunda conta bancária aberta (ex.: um segundo banco digital) — bloqueio de conta bancária não pode parar folha e fornecedor. |
| 6 | **Domínio reserva** | Um segundo domínio registrado e apontável em horas. Caso real da fonte: uma restrição de política derrubou TODAS as campanhas de um domínio, inclusive de produtos sem relação com a infração — domínio/subdomínio separado isola esse risco. |
| 7 | **Fornecedor reserva** | Identificado e com contato feito (pra suplemento/skincare, um nos EUA além da China). A escolha e a negociação são da `sourcing` — aqui só o status. |
| 8 | **Pre-order pronto pra ligar** | Widget/configuração de pre-order testada na loja + texto de expectativa de prazo escrito. É a válvula dupla: segura a venda quando o estoque acaba (sem pânico → sem chargeback → sem derrubar a conta) e adianta caixa (o dinheiro entra antes de produzir). Com expectativa clara, a conversão quase não cai — caso real da fonte: um novembro de $2,4M vendido em pre-order, mais que o ano anterior inteiro. **Melhor subestimar o estoque e ir pra pre-order do que encalhar.** |
| 9 | **Atendimento dimensionado pra pico** | O atendimento aguenta 3–10x o volume de tickets de um pico (Q4, escala, viral)? Se não: treinar, ou contratar temporário antes do pico. |

Pra membro `starter`, os itens 1–6 são os que valem AGORA (custam quase nada e protegem o que ele tem); 7–9 entram quando houver estoque próprio e volume.

**Risco de pessoa-chave e "dores de cabeça por dólar".** Três perguntas, respondidas com honestidade:

1. Se você adoecer uma semana, a marca degringola?
2. Se a pessoa mais treinada do time sair amanhã, o que quebra?
3. Linha de receita por linha de receita: quantas dores de cabeça por dólar ganho ela gera?

A métrica "dores de cabeça por dólar" existe porque receita cresce junto com problema — o jogo é crescer o dinheiro sem crescer o caos, e linha de receita que fatura bem mas consome o fundador é constraint disfarçada. Quanto mais o membro segura tudo, mais ELE é a pessoa-chave em risco. E o risco tem equivalentes de marketing que entram no mesmo diagnóstico: **1–2 ads puxando todo o gasto, 1 landing page campeã, 1 canal único** — concentração é fragilidade estrutural onde quer que apareça (a resposta de criativo/funil é das skills `creative-engine`/`ad-strategy`/`content-recycler`; aqui só se nomeia o risco). Regra prática pra fechar: todo problema recorrente ganha um conserto definitivo (patch), não um apagão de incêndio repetido.

**Saída da ETAPA:** checklist com status + lista de riscos abertos, cada um com probabilidade (baixa/média/alta), dano se acontecer (baixo/médio/alto), mitigação e dono. Ordene por probabilidade × dano.

# Product Research · Referência: Checagem 2, reviews de 1 e 2 estrelas no Trustpilot (ETAPA 3)

> A URL filtrada e a cascade de coleta, os quatro temas de classificação, as regras de veredito com o porquê (churn de eficácia), o que gravar na ficha, as fontes alternativas sem Trustpilot e a definição dos finalistas. Abra na ETAPA 3.

### ETAPA 3 — Checagem 2: Trustpilot, reviews de 1 e 2 estrelas

O TrendTrack traz o link do Trustpilot da marca. Entre nele e puxe as reviews negativas: `https://www.trustpilot.com/review/<domínio>?stars=1&stars=2&languages=all&sort=recency`. Cascade: `WebFetch` → se barrar, `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode reviews` (rola pra carregar os widgets) → se ainda barrar, o membro abre e cola as 20-30 reviews mais recentes de 1-2 estrelas.

Leia **no mínimo 20-30 reviews negativas** por marca e classifique cada uma em um tema:

- **Cobrança / assinatura** (cobrado sem querer, cancelamento difícil, refund lento)
- **Entrega / logística** (atraso, não chegou, embalagem)
- **Atendimento** (ninguém responde)
- **Eficácia** ("não funcionou", "não senti nada", "zero diferença", "waste of money")

**Regras de veredito:**

- Reviews reclamando de **cobrança e entrega** → dá pra resolver com fornecedor, operador logístico e checkout melhores. **Passa.** (E vira ângulo: "sem assinatura escondida", "cancela em 1 clique" são posicionamentos abertos.)
- Nota **abaixo de 4** mas as reclamações **não são sobre eficácia** → tudo bem. **Passa.**
- A **maioria** das reviews negativas fala de **eficácia** → **elimina.**
- Nota **abaixo de 4** com **muita gente dizendo que o produto não funciona** → **elimina.**

O porquê: produto que não funciona gera refund em massa no mês 2 e 3, quando o efeito prometido não aparece. A marca pode até estar escalando agora — ela está escalando em cima de churn, e o membro herdaria o mesmo churn ao usar o mesmo produto.

Grave na ficha: nota, nº de reviews, mix de temas (% por tema), veredito (**OK / cobrança-entrega / eficácia → eliminar**) e **5-10 frases literais** em inglês (com "tradução livre:" ao lado nos relatórios em pt-BR). As frases de eficácia dos concorrentes são matéria-prima de ângulo pra `market-research`/`copy-engine` ("I tried X for 3 months and nothing" é o hook de quem chega com mecanismo diferente).

**Marcas sem Trustpilot:** procure a mesma leitura em reviews da Amazon (se a marca vende lá), Reddit (`--mode reddit`) e comentários dos próprios ads. Sem NENHUMA fonte de review negativa, a marca segue com o veredito em aberto e o score de eficácia neutro.

Ao fim das ETAPAS 2 e 3, sobram os **finalistas** (alvo: 8-12 marcas). Marca eliminada permanece no banco com status `eliminada` + motivo — é informação de mercado, não lixo.

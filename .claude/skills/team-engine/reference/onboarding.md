# Team Engine · Referência: Onboarding, treinamento na hora certa e confiança por evidência (ETAPA 9)

> A integração técnica do dia zero, o bootcamp de oito semanas em três fases, o QA regressivo que diminui por evidência, a cadência de reuniões, os cheques de compreensão e o diagnóstico de duas semanas. Abra na ETAPA 9.

**PORTA 3 — RODAR (ETAPAs 9-13). Pergunta do membro: "como faço o time performar?"**

### ETAPA 9 — Onboarding: treinamento na hora certa, confiança por evidência

O objetivo declarado da fonte: "construir sistemas onde é impossível a pessoa falhar". O modelo "aqui está a ferramenta, se vira" falha sempre. Duas partes:

**1. Integração técnica (dia zero):** automação de contas/acessos, documento de boas-vindas que abre pelos **valores da empresa** e segue ferramenta a ferramenta, **formulário de conhecer a pessoa** (aniversário, hobbies, como gosta de receber feedback — direto ou com jeito —, reconhecimento público ou privado, tipo de aprendiz) — os dados alimentam a gestão o ano inteiro. Call técnica de ~30 min conferindo acessos (não precisa ser o membro). Velocidade importa: a pessoa começa assim que assina.

**2. Bootcamp de treinamento na hora certa (JIT — o treino chega quando a tarefa chega, não tudo de uma vez), máximo 8 semanas:**

- **Eu faço (semana 1):** o gestor executa ao vivo em 3 camadas — os passos, o como, e as RAZÕES de cada ponto-chave.
- **Nós fazemos (semanas 2-3):** o novato executa explicando passo e porquê; correção na hora.
- **Você faz (semana 4+):** trabalho real, começando por material de baixo risco (nunca no cliente/campanha mais crítica).
- **QA regressivo — supervisão que diminui por evidência, não por tempo de casa:** semana 2 = revisar **100%** de tudo antes de ir ao ar → semana 3 = **50%** → semana 4 = **20-25%** → semana 5+ = **0%**, com conferências aleatórias pra sempre. Grave o estágio de QA de cada pessoa em `dados.json.onboarding[]` — fica gravado como referência disponível pra auditoria de artefatos produzidos por gente nova (`consistency-audit`).
- **Cadência 5-3-1 de reuniões:** semana 1 = 1:1 todo dia; semanas 2-3 = 3×/semana; semanas 4-8 = 1×/semana ("traga suas dúvidas acumuladas" + o gestor traz a lista do QA).
- **Cheques de compreensão por aplicação, nunca "entendeu?"** (gera "sim" preguiçoso): "como você explicaria isso pra outra pessoa do time?", "em que situação isso NÃO funcionaria?".
- **Diagnóstico em 2 semanas:** (a) voando desde o início; (b) KPIs fracos mas melhorando toda semana com esforço visível → mantém; (c) sem progresso → plano de recuperação e busca reaberta. Treinamento passando de 8 semanas só tem dois diagnósticos: pessoa menos experiente que o esperado (ok SE melhora semana a semana) ou contratação errada.
- Sênior não dispensa estrutura — dispensa micro-checklist, não cadência (huddles curtos na semana 1, chegando COM pauta).

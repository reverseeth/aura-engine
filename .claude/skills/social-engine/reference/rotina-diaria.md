# Social Engine · Referência: Rotina diária agendada (ETAPA 5)

> O `rotina-prompt.md` autocontido, as duas formas de agendar (rotina na nuvem pela skill `schedule` ou tarefa local pelo CronCreate), o que a rotina faz em cada execução, as travas de custo e de repetição, o teste na hora e a revisão semanal. Abra na ETAPA 5.

## 1. O prompt da rotina é autocontido

A rotina não enxerga o `workspace/` do membro (na nuvem ele não existe, e localmente ela não deve depender de achar o arquivo certo). Por isso tudo que ela precisa vai escrito em `social-engine/rotina-prompt.md`, que é o texto exato colado na rotina:

1. **Marca:** nome, posicionamento em uma frase, tom de voz, paleta em hex, tipografia.
2. **Direção do feed:** sensação, assinatura e proibido (ETAPA 1).
3. **Higgsfield:** `brand_id`, `product_ids`, o banco de templates com o papel de cada um, a fórmula das 9 posições e o `daily_credit_cap`.
4. **Munição de legenda:** as 20 melhores frases de VOC, o mecanismo pelo nome literal, a oferta em uma linha (bundle, bônus, garantia), os hooks aprovados e as 9 legendas do lote aprovado como exemplo de tom.
5. **Banco de hashtags** por faixa.
6. **Publicação:** o degrau da cascade, a ferramenta, onde hospedar o arquivo limpo, a ordem reversa e o espaçamento.
7. **Regras duras:** nunca repetir o template de uma posição dentro de 7 dias nem o hook de uma legenda dentro de 30; sempre rodar o Limpador antes de publicar; parar e avisar se o saldo não cobre o lote; nunca gastar acima do teto diário.

O prompt manda a rotina checar o histórico recente antes de gerar (hoje `show_marketing_studio_generations` ou `show_generations` do Higgsfield, e o histórico do publicador) pra cumprir a regra de não repetir.

## 2. Onde agendar

- **Rotina na nuvem pela skill `schedule`** (padrão): um agente agendado que roda todo dia no horário escolhido, mesmo com o computador desligado. Ele roda num clone do repositório da Aura, o que traz o `tools/strip-metadata.sh`. Funciona quando os conectores do Higgsfield e do publicador estão ligados na conta do Claude do membro (conectores do claude.ai), porque a rotina na nuvem só enxerga esses.
- **Tarefa agendada local pelo CronCreate:** quando os conectores só existem no Claude Code da máquina do membro. Roda com o Claude Code aberto, enxerga o `workspace/` e salva o pacote do dia direto em `social-engine/<data>/`. Diga essa limitação em uma linha.

Horário padrão: de manhã no fuso do público (o `profile.md` diz o mercado; Estados Unidos por padrão, 7h no horário de Nova York), com a publicação espaçada até a noite quando o publicador aceita agendamento.

## 3. O que cada execução faz

1. Checa o saldo do Higgsfield. Saldo abaixo do lote: para e avisa o membro, sem gerar nada.
2. Escolhe, pra cada uma das 9 posições, um template do banco que não rodou nos últimos 7 dias naquela posição.
3. Gera as 9, confere por visão (produto fiel, texto certo, nada do "Proibido") e refaz o que falhar, até duas vezes.
4. Escreve as 9 legendas pela estrutura da ETAPA 3, com hashtags sorteadas do banco.
5. Baixa, limpa com `bash tools/strip-metadata.sh <pasta>`, hospeda o arquivo limpo e publica pela cascade, em ordem reversa.
6. Registra o lote (data, posição, template, hook, status) e manda ao membro um resumo de três linhas: o que publicou, quantos créditos gastou e qualquer falha.

Se a publicação falhar, a rotina não tenta de novo em loop: deixa o pacote pronto (na nuvem, as imagens na biblioteca do Higgsfield e as legendas no resumo; localmente, em `social-engine/<data>/`) e avisa.

## 4. Teste na hora

Depois de criar a rotina, rode uma execução manual na mesma sessão e confira o resultado com o membro: as 9 imagens, as legendas, o grid no perfil. Só então declare a rotina ligada. Se a execução manual falhou, ajuste o prompt antes de deixar agendado.

## 5. Revisão semanal

Uma vez por semana (pode ser uma segunda rotina, ou o membro dizendo "instagram" de novo): leia os posts da semana, os que tiveram mais salvamentos e comentários, e atualize o `rotina-prompt.md`: template que performa ganha peso, template que ninguém salva sai do banco, hook que funcionou vira modelo. A rotina melhora toda semana em vez de repetir o primeiro lote pra sempre.

## 6. Onde fica salvo

`social-engine/rotina-prompt.md` e, no `dados.json`, `routine`: `{ "scheduler": "schedule | cron_local", "routine_id": "...", "time_local": "07:00", "timezone": "America/New_York", "daily_credit_cap": 0, "tested_at": "ISO-8601" }`.

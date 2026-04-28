# Prompt Directors (lib auxiliar da Skill 07)

Diretores de prompt que convertem conceito de criativo em prompt production-ready pra ferramenta de geração específica. Invocados pela Skill 07 (creative-engine) após geração dos briefings.

## Arquivos

| Director | Ferramenta alvo | Quando invocar |
|---|---|---|
| `marketing-studio-director.md` | Higgsfield Marketing Studio (vídeo) | Para CADA conceito com componente de vídeo (UGC, demo, motion graphic, hyper motion, etc) |
| `gpt-image-2-director.md` | GPT Image 2.0 (imagem) | Para CADA conceito com componente de imagem (PDP-style hero, infografia, mockup com layout denso, ou single-frame cinematic) |

## Como funcionam

Cada director é um SKILL.md com:
- Instruções completas pro modelo seguir
- Routing logic (qual formato de output usar)
- Hard rules (o que sempre fazer / nunca fazer)
- Exemplos

Quando a Skill 07 chega na ETAPA 5.7 (Prompt Generation), ela:
1. Lê o briefing do conceito gerado
2. Decide qual director invocar (vídeo? imagem? ambos?)
3. Carrega o SKILL.md do director
4. Roda o prompt do director sobre o conceito
5. Salva o output (prompt production-ready) em `/workspace/[produto]/07-creatives/prompts/`

## Output esperado

Cada director gera 1 prompt production-ready por conceito, pronto pra colar na ferramenta:

- **marketing-studio-director** → 1 parágrafo único + link de generation Higgsfield
- **gpt-image-2-director** → JSON estruturado OU prosa cinematográfica OU meta-prompt (escolhido pelo director conforme tipo do output)

## Não confundir com

- A Skill 07 em si (que orquestra e gera os briefings de alto nível)
- O briefing do conceito (script segundo-a-segundo, primary texts, headlines) — esses são output da Skill 07 padrão
- Os directors transformam o briefing em prompt EXECUTÁVEL pelas ferramentas externas

## Importação

Esses directors foram importados de `Marketing Studio Skills Bank` (Anthropic Skills format) em 2026-04-28. Atualizar o conteúdo desses arquivos quando releases novas saírem.

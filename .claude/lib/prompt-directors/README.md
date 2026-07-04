# Prompt Directors (lib auxiliar da Skill 08)

Diretores de prompt que convertem conceito de criativo em prompt production-ready pra ferramenta de geração específica. Invocados pela Skill 08 (creative-engine) na **ETAPA 5.7 (Entregável de produção), Ramo A** — a rota de produção por IA. A **Rota B (montagem/EDL) NÃO usa director**: o entregável dela é um roteiro de montagem (`concept-XX-edl.md`) gerado pela própria Skill 08.

## Arquivos

| Director | Ferramenta alvo | Quando invocar |
|---|---|---|
| `marketing-studio-director.md` | Higgsfield Marketing Studio (vídeo, clipe curto ≤15s) | Conceito de VÍDEO gerado no Higgsfield (qualquer formato: UGC, demo, motion graphic, hyper motion, TV spot). Quando o script estoura ~15s, o próprio director divide em MULTI-SHOT (takes autocontidos) |
| `gpt-image-2-director.md` | GPT Image 2.0 (imagem) | Conceito com componente de imagem (PDP-style hero, infografia, mockup com layout denso, ou single-frame cinematic) |

**Modelos de vídeo de geração contínua (Veo 3.1 ~60s, Sora 2 quando o ad cabe, Kling longo) NÃO usam o marketing-studio-director.** O director é canônico SÓ pra Higgsfield. Pra modelo longo, a Skill 08 adapta a saída pra um **roteiro contínuo** único (hook → bridge → hold → CTA encadeados), registrado no `dados.json` como `director: "continuous-script"`. A regra "clipe autocontido sem memória cross-shot" é limite do Higgsfield, não regra universal.

## Como funcionam

Cada director é um arquivo `*-director.md` (formato Anthropic Skills) com:
- Instruções completas pro modelo seguir
- Routing logic (qual formato de output usar)
- Hard rules (o que sempre fazer / nunca fazer)
- Exemplos

Quando a Skill 08 chega na ETAPA 5.7 Ramo A, ela:
1. Lê o briefing do conceito gerado
2. Decide o formato (vídeo? imagem? ambos?) e, pra vídeo, o MODELO — Higgsfield usa director; modelo longo vira roteiro contínuo sem director
3. Carrega o `*-director.md` correspondente
4. Roda o prompt do director sobre o conceito (a copy exata — hook, headline, dialogue — vem do briefing; o director formata, nunca inventa copy nova)
5. Salva o output em `workspace/[produto]/08-creative-engine/prompts/` e atualiza `prompts/prompts-index.json` (director/modelo/preset/formato por conceito)

## Output esperado

- **marketing-studio-director** → clipe único: 1 parágrafo + link de generation. Script >15s: **multi-shot** — pasta `c0X-slug/` com 1 arquivo por take + `_LEIA-PRIMEIRO.txt` na raiz de `prompts/` (ordem dos takes, durações, como juntar no editor com 1 voiceover por cima)
- **gpt-image-2-director** → JSON estruturado OU prosa cinematográfica OU meta-prompt (escolhido pelo director conforme tipo do output)
- **continuous-script (modelo longo, sem director)** → `prompt-c0X-video.txt` único por conceito, com o roteiro contínuo + link/instrução de generation do modelo
- **Higgsfield MCP conectado** (`mcp__higgsfield__*`): além de salvar os prompts, a Skill 08 pode renderizar os vídeos in-session — sempre com confirmação do membro antes de gastar créditos

## Não confundir com

- A Skill 08 em si (que orquestra e gera os briefings de alto nível)
- O briefing do conceito (script segundo-a-segundo, primary texts, headlines) — esses são output da Skill 08 padrão
- O EDL da Rota B (`concept-XX-edl.md`) — roteiro de montagem com footage real, sem prompt de IA
- Os directors transformam o briefing em prompt EXECUTÁVEL pelas ferramentas externas

## Importação

Esses directors foram importados de `Marketing Studio Skills Bank` (Anthropic Skills format) em 2026-04-28. Atualizar o conteúdo desses arquivos quando releases novas saírem.

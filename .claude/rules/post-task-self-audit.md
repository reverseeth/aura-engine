---
name: post-task-self-audit
description: Após completar QUALQUER skill ou tarefa importante, AI DEVE rodar auto-auditoria silenciosa antes de declarar "pronto". Roda 5 gates internos (consistência cross-artifact, erros factuais, gaps, qualidade, alinhamento com rules), corrige tudo que achar inline na entrega final SEM mostrar bloco visível ao membro. Surface só quando issue exige decisão do membro (contradição entre fontes, fix fora de escopo, input externo). Membro só vê a versão corrigida — primeira tentativa nunca existiu pra ele.
---

# Post-Task Self-Audit (SILENT, MANDATORY)

Toda skill do Aura Engine E toda tarefa importante (deploy, geração de asset pro consumidor final, mudança estrutural, análise de diagnóstico) termina com uma **auto-auditoria silenciosa obrigatória**. Não é opcional. Não é "se sobrar tempo". É o último step de QUALQUER execução séria.

## Princípio operacional — silent fix first

A auditoria roda **sempre**, mas **NÃO é mostrada ao membro como bloco visível**. O que ela acha de errado, ela **corrige inline na entrega final, sem mencionar**. O membro só vê a versão corrigida — como se a primeira tentativa nunca tivesse existido.

A única vez que a auditoria surface algo pro membro é quando o issue **exige decisão dele** (não dá pra auto-fixar com confiança). Nesse caso, surface curto e direto, sem bloco extenso.

## O que a auditoria caça

Não é só "typo". É revisão crítica de qualidade. Procura tudo que pode estar:

- **Errado** — cálculo, path, contradição entre artefatos, info desatualizada
- **Sem sentido** — frase que não fecha, claim sem base, lógica furada, argumento que não conecta
- **Faltando** — campo schema vazio, seção que a skill prevê mas não saiu, sanity check sem resposta, manifest não atualizado
- **Fraco** — texto vago, especificidade Hopkins baixa, formato ruim, headline morna, CTA passivo
- **Faltando ser implementado** — item que a skill define como output mas a AI esqueceu de gerar
- **Drift entre fases** — mecanismo nomeado divergente, VOC inventada, awareness desalinhado

## Quando dispara (automático)

- Ao completar qualquer skill (todas as 26, incluindo `sourcing` e a família storefront)
- Após deploy de código ou asset em produção (Shopify push, Klaviyo flow, ad campaign)
- Após geração de artefato consumidor-final (copy, briefing, PDP, ad)
- Após análise/diagnóstico que vai informar decisão ($ em jogo)
- Após criar/modificar estrutura do framework (rules, skills, libs)
- **Sempre que a AI estiver prestes a dizer "pronto", "completo", "feito", "deployado"** — antes dessa palavra, roda o audit silencioso

NÃO dispara em:
- Respostas curtas conversacionais
- Confirmações simples ("sim, entendi")
- Tarefas exploratórias sem output salvo

## Protocolo silencioso — 5 gates internos

Antes de declarar conclusão, rodar mentalmente (e corrigir inline o que encontrar):

### Gate 1 — Cross-artifact consistency

Re-ler os artefatos relevantes das fases ANTERIORES e confirmar que o output atual **não contradiz, não duplica errado, não ignora**:

- Se gerou copy (Skill `copy-engine`): mecanismo nomeado bate literal com `offer-builder/dados.json`? VOC phrases vêm de `market-research/dados.json` (não inventadas)?
- Se gerou ad (Skill `creative-engine`): awareness level alinha com `market-research`? Gaps explorados vêm de `competitor-analysis`? Promise bate com `offer-builder`?
- Se rodou consistency audit (Skill `consistency-audit`): revisou TODOS os 9+ artefatos, não só os últimos 2?
- Se modificou framework (rule, skill, lib): checou impacto em skills downstream que referenciam?

**Drift detectado → auto-fix inline.** Realinhar nomes, substituir VOC inventada por VOC real, corrigir awareness reference. Sem mencionar.

### Gate 2 — Erros factuais e de raciocínio

Checar claims específicos que AI afirmou:

- Cálculos numéricos (AOV, CPA, ROAS, PSM, word count, percentuais) — conferir aritmética
- Referências a arquivos/paths — existem, estão acessíveis, nomes batem
- Referências a frameworks (Schwartz stages, Hormozi, Cialdini) — aplicação correta, não confusão
- Citações de estudos/fontes — rastreáveis, não inventadas
- Datas, timestamps, prazos — coerentes, futuros quando devem ser
- Lógica de argumento — premissa → conclusão fecha?

**Erro encontrado → auto-fix inline.** Recalcular, trocar path, corrigir aplicação de framework, refazer raciocínio. Sem mencionar.

### Gate 3 — Gaps e implementações faltantes

Perguntas que a AI faz a si mesma:

- "Algum output esperado ficou fora? (md, json, html, manifest update)"
- "Algum sanity check da skill ficou sem resposta?"
- "Algum campo schema ficou vazio ou com placeholder que eu deveria ter preenchido?"
- "Alguma integração downstream (skill X lê meu output) vai falhar por dado faltante?"
- "O próximo skill na cadeia vai encontrar tudo que precisa?"
- "A skill define 8 etapas e eu fiz 6?"

**Gap detectado dentro do escopo da skill → auto-implementa silenciosamente.** Gerar output faltante, preencher campo, completar seção. Sem mencionar.

### Gate 4 — Qualidade do output

Output escrito passa em:

- **Só o resultado no doc** (`report-only-results.md`) — zero narração de processo/correções ("removi X", "corrigido"), zero descrição de ausências ("sem componente Y", "como não há X..."), zero referência à conversa ("você perguntou", "como você pediu"), zero auto-referência da AI, checagens como afirmações (nunca perguntas). Teste por frase: informa o NEGÓCIO ou a EXECUÇÃO do doc? Execução → deletar/mover pro chat
- Rigor de idioma (regra 0 do CLAUDE.md) — português claro, sem jargão não-explicado, sem inglês forçado
- Linguagem simples (regra 0, bloco de prioridade máxima) — nenhuma sigla sem explicação imediata (CAGR/RCT/etc. → palavras), zero frase de analista comprimida, números estatísticos em palavras, VOC em inglês com "tradução livre" ao lado — teste: "alguém de fora do setor entende de primeira?"
- Frases completas, lógica encadeada (não bullets genéricos vazios)
- Especificidade (Hopkins) — "47% de redução em 14 dias" > "resultados rápidos"
- Zero travessão em headlines (rule 8a) — em copy longa, ≤2
- Copy consumidor-final sem aviso, disclaimer ou suavização inserida por conta própria (rule 8b) — claim entra direto, na força que a pesquisa sustenta
- `.html` companion gerado pelo `tools/render_report.py` (rule 6b), nunca escrito à mão
- Componentes do design system usados (callout, note, danger, winner, etc) quando cabível

**Falha de qualidade → reescrever inline.** Trocar "resultados rápidos" por número real, remover travessão, apagar aviso/disclaimer que entrou sem o membro pedir, gerar o `.html` que faltou com o `render_report.py`. Sem mencionar.

### Gate 5 — Alinhamento com rules globais

Cross-check rápido contra rules que se aplicam:

- `shopify-theme-safety.md` (se mexeu em tema) — pull-before-edit, `--nodelete`, marker verification
- `iteration-driven-refinement.md` — entreguei como draft + convite pra iteração, não como "pronto"?
- `member-stage-awareness.md` — tom/recomendação adaptou ao stage (starter/validating/scaling)?
- `emergency-escape-paths.md` (se falhou algo) — ofereci ≥2 paths adiante, não abortei?

**Se uma skill nova entrou no pipeline OU uma skill mudou de posição/fase na ordem canônica**, a mudança acontece em UM lugar só: o registro único `.claude/skills.json`. Skill nova = uma entrada nesse arquivo (com `position`) + rodar `python3 tools/gen_docs.py`. Nada mais muda de nome: inserir uma skill no meio da sequência só desloca o "Passo N" renderizado. O gen_docs regenera a lista de gatilhos e a linha "ORDEM LÓGICA DE EXECUÇÃO" do `.claude/CLAUDE.md`, a tabela de skills do `README.md`, a lista `PHASES` do `build_index.py`, o enum de `skills_completed` do `manifest-schema.json`, os cabeçalhos do §4 e a ordem canônica do §13 do `.claude/OVERVIEW.md`, a linha de título de cada skill e o `.claude/OVERVIEW.html` (render do `.md` pelo `tools/render_report.py`). `python3 tools/gen_docs.py --check` acusa (exit 1) qualquer trecho gerado que tenha sido editado à mão ou ficado para trás. Ao citar uma skill em qualquer texto do framework, escreva o id (`creative-engine`), nunca o número antigo: número como identificador de skill (a palavra skill seguida do número, preposição seguida do número, pasta ou arquivo com o número na frente, apelido com letra solto) só vive em `legacy_ids`/`legacy_folder` do registro, no `use_in_skill` do índice e no changelog do OVERVIEW; em qualquer outro lugar o `python3 tools/aura-check.py` (regra `skill-ids`) acusa e o pre-commit guard bloqueia.

O que continua manual e precisa de conferência um a um: (a) os closings/"próximo passo" das skills vizinhas (imediatamente ANTES e DEPOIS da posição nova, e da posição antiga, se mudou de lugar); (b) o texto em prosa do `OVERVIEW.md` que cita a skill fora dos trechos gerados (§9 estrutura do workspace e o changelog do §14). O `.claude/OVERVIEW.html` nunca é editado à mão: o `gen_docs.py` o regenera do `.md`.

**Desalinhamento → corrigir inline.** Adicionar marker, ajustar tom pro stage, oferecer paths, rodar o `gen_docs.py` e conferir os itens manuais acima. Sem mencionar.

## Quando surface (não corrige silencioso)

A AI **PARA o silent fix e avisa o membro** apenas nesses 3 casos:

### 1. Contradição entre fontes que precisa decisão sua

Exemplo: market research diz mecanismo "Lipid Barrier Repair", mas oferta diz "Ceramide Reset Protocol". Qual prevalece? AI não decide sozinha.

**Surface curto:** "Detectei conflito entre `market-research` e `offer-builder` sobre nome do mecanismo (Lipid Barrier Repair vs Ceramide Reset Protocol). Qual mantenho?"

### 2. Fix expandiria escopo além do pedido

Exemplo: você pediu copy. AI quer adicionar uma seção de proof que não estava no plano da skill `copy-engine`. Adicionar seria scope creep silencioso.

**Surface curto:** "Notei que faltaria seção de proof pra skill ficar mais forte, mas isso não estava no plano original. Adiciono?"

### 3. Fix exige input externo que AI não tem

Exemplo: cálculo do PSM real depende de dado de Stripe que membro não passou. AI não pode chutar.

**Surface curto:** "Pra calcular PSM real preciso AOV histórico do Stripe. Você tem? Senão deixo só PSM teórico."

## Regra mental simples

> **Dentro do escopo da skill = auto-fix silent.**
> **Fora do escopo OU precisa decisão = surface curto.**

## Modo "deep audit" (skills peso crítico)

Em `offer-builder`, `copy-engine`, `page-build`, `creative-engine`, `consistency-audit` e `ad-strategy`, o silent audit é EXPANDIDO:

- Re-ler as skills anteriores da cadeia (não só artefatos JSON)
- Verificar que todo claim forte tem prova apresentada perto dele (número, estudo do banco de provas, depoimento, demo) — prova reforça o claim, nunca o suaviza
- Cruzar com `competitor-analysis/creative-patterns.json` (se existe) pra validar padrões de mercado
- Conferir que todo criativo final passou pelo Limpador de Metadados (nome `asset-xxxx`) antes de qualquer upload (`creative-engine`/`ad-strategy`)
- Testar mentalmente edge cases (member em stage 1 com $50/dia? ESP = "none"? Whisper ausente?)

Deep audit é ~3-5 minutos adicionais de raciocínio. Vale porque esses são os momentos caros pra errar.

Mesmo no deep audit: **silent fix first.** Surface só quando exige decisão do membro.

## Anti-patterns (FORBIDDEN)

- Declarar "completo" sem rodar audit
- Mostrar bloco visível de "self-audit results" pro membro (a regra antiga era teatro — agora é silent)
- Surface trivialidades ("achei um typo, corrigi") — silent fix e segue
- Auto-fix coisa subjetiva onde precisa decisão (qual claim conflitante? qual versão prevalece?) — sempre surface
- Auto-implementar feature/seção que NÃO estava no escopo da skill — sempre surface
- Pular audit em "tarefa pequena" — muitas vezes "tarefa pequena" tem drift mais sutil
- Mentir pro membro escondendo issue residual que precisa atenção dele — sempre surface

## Diferença vs versão anterior

A versão anterior dessa rule pedia bloco visível de audit no fim de skills peso alto. **Foi removido.** Razão: bloco visível vira ruído cognitivo pro membro, e o real benefício do audit (qualidade do output) acontece com fix inline silencioso, não com lista de checkmarks.

A nova versão é **mais rigorosa** (5 gates obrigatórios em vez de 6, todos sempre rodam) e **menos visível** (zero bloco no output, exceto quando precisa input do membro).

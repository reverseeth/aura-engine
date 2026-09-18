# Creative Engine · Referência: Mensagem final por rota

> O texto integral da mensagem final nas três rotas (IA, montagem e mix). Abra ao entregar.

## Mensagem Final

A mensagem se adapta à rota escolhida (ETAPA 1.0). Apresente como **draft** convidando iteração (rule iteration-driven-refinement), não como "pronto pra lançar".

**Se Rota A (IA):**

"Primeira versão dos briefings pronta. Como gerar:

- **Vídeos**: abra `workspace/[produto]/creative-engine/prompts/prompt-c0X-video.txt` — cole no [modelo escolhido] (link/instrução de generation no fim do prompt). Modelo longo (Veo/Sora/Kling) = 1 roteiro contínuo por conceito; Higgsfield = pode ter pasta `c0X-slug/` com 1 take por arquivo (gere na ordem e junte sob 1 voiceover). [Se o Higgsfield MCP rendeu in-session: "Os vídeos já estão renderizados em `renders/` — revise antes de editar."]
- **Imagens**: abra `prompts/prompt-c0X-image.txt` — cole no GPT Image 2.0 (formato já ajustado ao tipo)
- **Voiceovers** (se conceito tem): gere no ElevenLabs com os scripts marcados nos briefings
- **Edição**: junte vídeo + voiceover + text overlays no CapCut/Submagic/Captions
- **Limpar metadados (último passo)**: depois de editar, dê 2 cliques em `Limpador de Metadados` na pasta da Aura e arraste os criativos finais pra lá (ou a pasta inteira) — cada arquivo é substituído por uma versão sem nenhum metadado de IA, com a mesma qualidade, renomeada `asset-xxxx`, na mesma pasta. Suba só esses. [Se o Higgsfield MCP rendeu in-session: "Os renders em `renders/` já estão limpos."]

Revisa e me diz o que ajustar (tom, ângulo, hook) antes de você gerar tudo. Quando os criativos estiverem prontos: diga **'agentic readiness'** (`agentic-readiness`) e depois **'consistency audit'** (`consistency-audit` — o GATE de launch); com o audit verde, **'ad strategy'** monta a campanha no Meta."

**Se Rota B (montagem/EDL):**

"Primeira versão dos roteiros de montagem pronta. Como montar:

- **EDL por conceito**: abra `workspace/[produto]/creative-engine/concept-0X-edl.md` — a tabela timecode diz, beat a beat, que clipe entra, o text overlay e a legenda exata. Monte no CapCut/editor seguindo a tabela
- **Footage**: use SÓ material licenciado (leia o bloco de usage rights em cada EDL). Onde falta footage, o EDL marca `[FALTA FOOTAGE]` com as opções (Billo/Insense, stock pago, próprio)
- **Voiceovers** (se conceito tem): gere no ElevenLabs e coloque por cima da montagem

Revisa os EDLs e me diz se o ritmo/estrutura tão certos antes de você montar. Quando os criativos estiverem prontos: diga **'agentic readiness'** (`agentic-readiness`) e depois **'consistency audit'** (`consistency-audit` — o GATE de launch); com o audit verde, **'ad strategy'** monta a campanha no Meta."

**Se Rota C (Mix):** combine as duas mensagens — liste os conceitos `ai` apontando pros prompts e os conceitos `edl` apontando pros arquivos de montagem."

# Stitch Integration (visual blueprint layer)

Integração opcional com Google Stitch — ferramenta de AI design mais bonita hoje
(herdeira do Galileo AI, powered by Gemini 2.5 Pro). **Grátis** via Google Labs.

## Quando usar

Entre Skill 05 (copy) e Skill 06 (page engine), como **visual blueprint layer**:

```
05 copy → [OPCIONAL] Stitch mockup → 06a planning → 06b Liquid → 06c deploy
```

**Vale a pena quando:**
- Membro é mais marketer/criativo que técnico, prefere ver layout antes de aprovar
- Quer explorar 5-10 direções visuais antes de comprometer com Liquid
- Tem referência visual forte (concorrente que quer superar)
- Quer estética premium que supera output direto do Claude

**Não vale a pena quando:**
- Produto é simples, PDP básica, membro confia no output direto
- Já tem design aprovado em outra ferramenta
- Urgência alta (adiciona 15-30min ao fluxo)

## Benefício vs custo

| | Com Stitch | Sem Stitch |
|---|---|---|
| Tempo adicional | +15-30min | 0 |
| Custo | $0 (grátis) | $0 |
| Qualidade visual da PDP | Senior-designer-level | Good-enough |
| Iteração visual pré-Liquid | 5-10 variações | 1 (direto pra código) |
| Drift design vs implementação | Baixo | Médio |
| Curva de aprendizado | 30min primeira vez | 0 |

## Arquivos nesta pasta

- `README.md` — este arquivo (overview + decisão)
- `setup.md` — guia 5min pra criar conta + acessar Stitch
- `prompt-templates.md` — prompts prontos pra gerar PDP/Landing/Advertorial no Stitch
- `importer.md` — spec de como Skill 06b processa o HTML exportado

## Fluxo recomendado

### Primeira vez (30min setup)
1. Ler `setup.md`
2. Criar conta Google Labs + habilitar Stitch
3. Fazer 1 teste: gerar mockup fake (ex: PDP genérica)
4. Export HTML, abrir local pra confirmar que funciona

### Uso recorrente (15-30min por página)
1. Ter copy aprovada (output Skill 05)
2. Pegar prompt template correspondente (`prompt-templates.md`)
3. Rodar no Stitch, gerar 3-5 variações
4. Escolher favorita OU mesclar partes de diferentes
5. Export HTML standalone → salvar em `/workspace/[produto]/06-page/stitch-blueprint.html`
6. Rodar skill 06 normalmente — Aura detecta o blueprint e usa como guide visual

## Limitações

- **Stitch é ferramenta humana** — não há API programática. Member tem que interagir manualmente.
- **350 generations/mês no free tier** — mais que suficiente pra uso típico, mas grandes brands com dezenas de páginas podem bater limite.
- **Acesso via Google Labs** — pode ter limitações geográficas (mas US/EU/BR tudo funciona).
- **Export limitado a HTML standalone + assets** — não mantém sincronia com código Shopify em produção. É one-shot reference.

## Custo

$0/mês permanente (Google Labs free tier).

## Roadmap

Quando (se) Stitch lançar API pública:
- Skill 06a pode chamar Stitch automaticamente
- Gerar 3-5 mockups programaticamente
- Apresentar lado a lado pro membro escolher
- Zero intervenção manual

Por enquanto é opt-in com etapa humana no meio.

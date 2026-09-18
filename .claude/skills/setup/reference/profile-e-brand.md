# Setup · Referência: Salvar o profile e inicializar o brand.md (ETAPAs 5 e 5A)

> O formato completo do `workspace/profile.md`, a cópia do `brand.md.template` com os campos auto-extraídos, o sistema Brand Voice Measurement (query exata) para registrar a voz atual da marca, o aviso ao membro e o escape ES1 quando o template falta. Abra na ETAPA 5.

### ETAPA 5 — Salvar Profile

**Antes de qualquer escrita**, garanta que o diretório de destino exista:

```bash
mkdir -p workspace/
mkdir -p workspace/[produto]/   # onde [produto] = slug gerado a partir do nome do produto (ver Etapa 5B)
```

Use os valores capturados das variáveis `SITUACAO`, `BUDGET`, `TOOLS`, `ESP`, `LINK` e `SHOPIFY_LINK` da Etapa 3 mais os dados extraídos na Etapa 4. Salve em `workspace/profile.md`:

```markdown
# Perfil do Membro

## Idioma dos relatórios
report_language: [pt-BR | en]

## Situação
Situação: [A / B / C / D — por extenso]
Classificação de budget: [starter / standard / escala-inicial / escala-avançada]
Budget diário: $[X]
Data do setup: [YYYY-MM-DD]

## Ferramentas
- TrendTrack: [sim/não]
- SpyBox: [sim/não]
- Higgsfield: [sim/não]
- Notion: [sim/não]
- Shopify: [sim + link / não — vem da pergunta 4]
- ESP (plataforma de email): [klaviyo / omnisend / mailerlite / shopify_email / none]

## Produto (se aplicável)
Link da loja: [url ou "N/A"]
Link do produto principal: [url ou "N/A"]

### Dados extraídos automaticamente da página (se link foi acessível):
- Nome do produto: [...]
- Preço base: [...]
- Bundles detectados: [...]
- Descrição: [...]
- Features/ingredientes principais: [...]
- Hero headline atual: "[...]"
- Sub-headline: "[...]"
- Guarantee atual: [tipo + duração ou "nenhum"]
- Mecanismo único atual: [nome ou "não identificado"]
- Link de checkout: [url]
```

### ETAPA 5A — Inicializar `brand.md` do produto (opcional, mas recomendado)

Se SITUACAO ≠ A (membro já tem produto), copie `.claude/templates/brand.md.template` pra `workspace/[produto]/brand.md` e preencha os fields que conseguiu extrair automaticamente na ETAPA 4 (dados da página):

- `{{ PRODUCT_SLUG }}` → slug do produto
- Paleta de cores: preencha com os hex dominantes (background, texto, accent/CTA) extraídos na ETAPA 4
- Fontes: preencha com as font-families (heading e body) extraídas na ETAPA 4
- Logo path: `workspace/[produto]/brand/logo.svg` (criar diretório; membro upa depois)

**Voz da marca (sistema a puxar — rode a `best_query` exata):** ao preencher os campos de tom/editorial do `brand.md`, puxe **Brand Voice Measurement — Vocabulary / Tone / Cadence** (rode `brand voice measurement vocabulary tone cadence nine voice types grade level`) e capture a voz atual da marca nos três medidores do sistema (vocabulário, tom, cadência) a partir da copy extraída da página na ETAPA 4. É o registro que a skill `market-research` refina depois e a `copy-engine` usa pra escrever no tom da marca.

Fields que NÃO conseguiu extrair (página bloqueada, hex/fontes não detectados) ficam como placeholders `[preencher]`. Avise ao membro:

> "Criei `workspace/[produto]/brand.md` com o que consegui extrair da sua loja. Abre e completa o que ficou como `[preencher]` antes de rodar `page` — isso é single-source-of-truth pra identidade visual e editorial."

Se SITUACAO = A (sem produto ainda), pule essa etapa. A Skill `product-research` cria o `brand.md` do produto vencedor na etapa SALVAR dela (com os fields visuais como `[preencher]`, já que ainda não existe loja pra extrair). A skill `page-design` lê esse arquivo na brand discovery e só pergunta o que faltar.

> **Escape (ES1):** se `.claude/templates/brand.md.template` estiver ausente, não aborte — ofereça **(A)** gerar um `brand.md` mínimo inline com os fields auto-extraídos e o resto como `[preencher]`, OU **(B)** pular a criação do brand.md agora marcando `manifest.skipped_preflight += ["brand.md.template"]` e avisando que recomenda re-executar antes de `page`.

# Retention Engine · Referência: Setup pipeline (Klaviyo MCP ou assets mais setup-guide) e deliverability (ETAPA 6)

> Os dois caminhos da cascade (MCP oficial em draft, assets mais setup-guide pra todos os ESPs, com a nota do Shopify Email), a regra de nunca ativar automaticamente e o checklist de deliverability por email. Abra na ETAPA 6.

## Setup Pipeline — Klaviyo

Cascade resiliente (detecção de prefixo conforme `.claude/lib/mcp-detect/README.md`), **dois caminhos só**: **Klaviyo MCP oficial → HTML + setup-guide**. Não há caminho de session-cookie/internal-API — foi removido por risco de segurança (cookie dava acesso full à conta) e fragilidade (endpoints sem contrato público). Automação confiável = MCP oficial; sem MCP, fallback é assets + guia que o membro importa.

### Caminho 1 (PREFERENCIAL) — Klaviyo MCP oficial

Detecte se há tools com prefixo `mcp__klaviyo__` na sessão (Klaviyo MCP oficial, 25 tools, 2026):

```
klaviyo_mcp_available = existe ao menos 1 tool com prefixo `mcp__klaviyo__` na sessão
```

Se **disponível**, CRIE os flows direto via MCP (com contrato estável, sem scraping):

1. Gerar o HTML de cada email adaptando ao produto (usa `copy-engine/copy-engine.md` pra copy + `market-research/market-research.md` pra VOC + `offer-builder/offer-builder.md` pra mecanismo), mesma geração do caminho de assets.
2. Criar cada flow **da FASE ativa** (Fase A: abandoned cart + post-purchase welcome, + Welcome Email 1 se condicional; Fase B: welcome series completo, win-back, replenishment) via as tools `mcp__klaviyo__*` de flow creation/configuration: trigger, filtros, ações (email/delay/branch), subject + preview + conteúdo HTML.
3. **Flows criados SEMPRE em draft/manual** — nunca ativar automaticamente (regra "NUNCA ativar automaticamente" abaixo vale igual aqui: risco de spam se um email tiver bug). Membro revisa no Klaviyo UI e ativa.
4. Logar `source: "klaviyo_mcp"` no `retention-engine/dados.json` e no `automation-log.jsonl`.
5. Salvar os assets (HTML + flow-metadata.json) em paralelo, pra o membro ter material mesmo que queira ajustar fora do MCP.

Se uma chamada MCP falhar (auth, rate limit, tool indisponível), cair silenciosamente pro **Caminho 2** sem insistir — o membro vê os fluxos prontos pra importar do mesmo jeito.

### Caminho 2 (FALLBACK confiável) — assets + setup-guide

Gerar os assets prontos + setup-guide e o membro importa no Klaviyo UI. Veja a seção "Caminho 2 detalhado — assets + setup-guide" abaixo. Default quando não há Klaviyo MCP. Logar `source: "klaviyo_assets_guide"`. Vale também pra Omnisend/MailerLite/Shopify Email/outros ESPs (que não têm MCP).

### NUNCA ativar automaticamente (vale pros dois caminhos)

Ativar flow via skill — por MCP ou de qualquer outra forma — = risco de spam se algum email tiver bug. Skill SEMPRE deixa em draft/manual. Membro revisa no UI do ESP antes de ativar.

## Caminho 2 detalhado — assets + setup-guide (todos os ESPs)

Este é o caminho confiável e o fallback da skill quando não há MCP — vale pra Klaviyo e pra Omnisend/MailerLite/Shopify Email/outros. Skill gera:

1. `workspace/[produto]/retention-engine/[fluxo]/email-1.html`, `email-2.html`, etc (HTML pronto)
2. `workspace/[produto]/retention-engine/[fluxo]/setup-guide.md` com step-by-step manual no dashboard do ESP (trigger, delays, subject/preview de cada email, onde colar o HTML)

Membro faz o setup manual seguindo o guia, skill entrega os materiais prontos.

**Nota específica pra `esp: "shopify_email"`:** o Shopify Email (com Shopify automations/Flow) cobre bem welcome, abandoned cart e post-purchase, mas os flows com branch/segmentação avançada (win-back por janela de inatividade, replenishment com timing por consumo) são limitados. O setup-guide adapta: usa as automations nativas onde existem, e converte os flows que o Shopify Email não suporta em campanhas agendadas manualmente (com o timing calculado no guia). Avisar no output final: quando o membro passar de ~$5k/mês em receita de email, migrar pra Klaviyo destrava os 5 flows completos + segmentação — recomendar a migração sem forçar.

## Deliverability (cair na inbox, não em Promotions/Spam)

Pra cada email gerado:

- **Subject line**: < 50 chars ideal; sem ALL CAPS; sem emoji excessivo
- **Preview text**: 40-70 chars
- **Unsubscribe link**: no footer (todo ESP exige pra entregar)
- **From name**: "[Brand Name]" — não email genérico tipo "noreply@"
- **Reply-to**: endereço monitorado (replies de cliente vão pra algum lugar)
- **Padrões que derrubam inbox rate (checklist inline):** revisar subject + body contra: "FREE!!!" e variações all-caps, "ACT NOW", "LIMITED TIME!!!", "GUARANTEED", "RISK-FREE", "100% free", excesso de `!` e `$`, subject inteiro em caixa alta, mais de 1 emoji no subject. Esses padrões derrubam inbox rate (caem em Promotions/Spam) — reescrever antes de salvar

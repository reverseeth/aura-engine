# Bonus Delivery · Referência: SALVAR e mensagem final

> Os quatro artefatos com o dual output e as convenções, a atualização do manifest pelo script e o texto integral da mensagem final como draft. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/bonus-delivery/bonuses/` antes de salvar.

1. **`workspace/[produto]/bonus-delivery/bonuses/[bonus-id]/`** — assets do bônus (PDF do e-book, screenshots da config GWP, instruções de fulfillment, etc — conforme type). Estes seguem o **design da marca do membro** (não do Aura) e o **consumidor-final é em inglês**.
2. **`workspace/[produto]/bonus-delivery/bonus-delivery.md`** — doc operacional pra AI ler em skills futuras: cada bônus com type, condition, canal de entrega, trigger, threshold (se cart_threshold), path do asset, KPI esperado, e status da Fase A (pronto pro launch?). Escrito no `report_language`.
3. **`workspace/[produto]/bonus-delivery/bonus-delivery.html`** — visualização humana, gerada com `python3 tools/render_report.py workspace/[produto]/bonus-delivery/bonus-delivery.md` (nunca escrita à mão). No `.md`: uma seção `##` por bônus, o type em negrito, tabela `KPI | Valor` pra take-rate/access rate (quando disponível) e citação `**Atenção:**` pro threshold de GWP (convenções em `.claude/templates/aura-html-components.md`).
4. **`workspace/[produto]/bonus-delivery/dados.json`** — array de snapshots agregados por bônus/período com take-rate/access rate (ETAPA 4, Fase B). Append, nunca sobrescrever.

Atualizar o manifest pelo script: `python3 tools/manifest.py <slug> complete bonus-delivery` (faz backup, valida e grava `updated_at`; nunca editar o JSON à mão).

- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html).

## Mensagem Final (framing de draft — iteration-driven-refinement)

> "Fase A da entrega de bônus pronta pros [N] bônus da oferta:
>
> 1. [Bonus 1 — tipo — condition — canal de entrega / threshold se cart_threshold]
> 2. [Bonus 2 — tipo — canal de entrega]
>
> O GWP tá configurado via [app/Function] conforme a condição da oferta ([auto-add em toda compra / threshold de $X ancorado no seu AOV]). Os e-books/assets digitais tão em `bonuses/` e o link de acesso já aparece na thank-you page — comprador do dia 1 recebe o que a página promete. O payload do email de entrega tá pronto pro fluxo da Skill `retention-engine`.
>
> Testa comprando 1 unidade pra validar que o brinde aparece no cart e o link chega. Me diz se o threshold/condição tá certo ou se quer ajustar.
>
> Próximo passo na ordem de launch: diga **'retention'** (Skill `retention-engine` Fase A — flows de recuperação: abandoned cart + post-purchase; o payload do email de bônus que preparei entra direto no flow post-purchase de lá). Depois de ~30 dias com ads ATIVOS (campanha rodando, não só criada), roda `bonus delivery` de novo (Fase B): eu puxo os agregados do Shopify/Klaviyo, gravo o snapshot no `bonus-delivery/dados.json` e mostro take-rate/access rate por bônus pra gente iterar a oferta."

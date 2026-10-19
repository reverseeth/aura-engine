# Support Engine · Referência: SALVAR, dados.json e mensagem final

> Os arquivos, o schema do `dados.json` e o texto da mensagem final. Abra ao fechar a skill.

## SALVAR (dual output, regra 6b)

`mkdir -p workspace/[produto]/support-engine/`. Outputs:

- **`support-engine.md`**, nesta ordem: o que a Brandwise faz · passo a passo da conta · a base de conhecimento (lista dos arquivos e o que cada um responde) · pendências (o que falta e o que destrava). Só o resultado (`.claude/rules/report-only-results.md`).
- **`support-engine.html`**: `python3 tools/render_report.py workspace/[produto]/support-engine/support-engine.md`, nunca à mão.
- **`base-de-conhecimento/`**: os textos em inglês prontos pra colar. Isentos de `.html` (arquivos operacionais).
- **`dados.json`**:

```json
{
  "resumo": { "platform": "brandwise", "knowledge_base_docs": 0, "shipping_window_days": [] },
  "knowledge_base": { "docs": [], "uploaded": false, "shipping_window_days": [] },
  "pending_inputs": []
}
```

## Mensagem final

Primeira versão é draft (rule `iteration-driven-refinement.md`):

"Suporte pronto pra ligar. A Brandwise é um helpdesk de IA ligado à sua Shopify: responde e resolve sozinha rastreio, troca de endereço, cancelamento, reembolso e devolução, e junta email, chat, comentários dos ads e DMs numa caixa só. O passo a passo da conta está em `support-engine/`, e a base de conhecimento em inglês, montada com a sua oferta, garantia e prazo de envio, está em `support-engine/base-de-conhecimento/`, pronta pra colar. [SE houver pendências: 'Falta você me passar: [endereço de devolução, transportadora].'] Quando a oferta mudar, roda **'suporte'** de novo que eu atualizo a base."

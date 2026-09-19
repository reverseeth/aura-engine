#!/usr/bin/env node
/**
 * Cliente do Jev — a camada de decisão da Aura.
 *
 * Cânone: .claude/lib/jev/README.md
 *
 * Contrato: entra um job em JSON, sai um resultado em JSON. Nunca lança pilha de
 * erro na cara do membro, nunca escreve em workspace, nunca imprime a chave.
 *
 *   node tools/jev.mjs --check
 *   node tools/jev.mjs --job caminho/do/job.json
 *   cat job.json | node tools/jev.mjs
 *
 * Formato do job:
 *   {
 *     "state":     "texto" | {campos} | ["texto", "texto"],
 *     "questions": { "nome": {"type":"choice"|"score"|"boolean", ...} },
 *     "lote":      [ {"id":"item-1","state":...}, ... ]   // opcional, em vez de state
 *   }
 *
 * Códigos de saída — a skill lê o código, não o texto:
 *   0  respondeu
 *   3  INDISPONÍVEL (sem chave, sem pacote, sem rede, modelo fora do ar).
 *      Não é erro: é o degrau três da cascade. A skill segue como segue hoje.
 *   4  job malformado (erro de quem chamou, vale corrigir)
 */

const MODELO = 'typesafe-ai/jev';
const INDISPONIVEL = 3;
const JOB_RUIM = 4;

function sai(codigo, objeto) {
  process.stdout.write(JSON.stringify(objeto, null, 2) + '\n');
  process.exit(codigo);
}

function indisponivel(motivo, comoResolver) {
  // Degrau três: a ausência é normal, então a saída é calma e legível pela skill.
  sai(INDISPONIVEL, { disponivel: false, motivo, como_resolver: comoResolver ?? null });
}

/** Barrada por cota do tier gratuito, que é capacidade e não falha do item. */
function eLimite(msg) {
  return /rate.?limit|quota|too many requests|\b429\b/i.test(String(msg));
}

/** Traduz o erro do gateway na ação concreta, quando ela é conhecida. */
function pista(msg) {
  const m = msg.toLowerCase();
  if (m.includes('credit card')) {
    return 'a conta da Vercel precisa de um cartão cadastrado antes de liberar os créditos; '
         + 'o cadastro é em vercel.com/dashboard, aba AI Gateway';
  }
  if (m.includes('401') || m.includes('unauthorized') || m.includes('invalid api key')) {
    return 'a chave do AI Gateway não foi aceita; gere outra em vercel.com/dashboard, aba AI Gateway';
  }
  if (m.includes('429') || m.includes('rate limit')) {
    return 'o limite de chamadas da conta foi atingido; espere e rode de novo';
  }
  if (m.includes('model') && m.includes('not found')) {
    return 'o modelo saiu do catálogo do gateway ou a conta não tem acesso a ele';
  }
  return null;
}

async function carregarSdk() {
  // Import dinâmico: sem o pacote, isto é indisponibilidade, não quebra.
  try {
    const mod = await import('ai');
    if (typeof mod.experimental_evaluate !== 'function') {
      return { erro: 'o pacote ai está instalado mas não expõe a avaliação; versão antiga',
               fix: 'npm i ai@latest dentro de tools/' };
    }
    return { evaluate: mod.experimental_evaluate };
  } catch {
    return { erro: 'o pacote ai não está instalado',
             fix: 'cd tools && npm i' };
  }
}

function lerJob(texto) {
  let job;
  try { job = JSON.parse(texto); }
  catch (e) { sai(JOB_RUIM, { erro: 'o job não é JSON válido', detalhe: String(e.message) }); }

  if (!job || typeof job !== 'object') sai(JOB_RUIM, { erro: 'o job precisa ser um objeto' });
  if (!job.questions || typeof job.questions !== 'object' || !Object.keys(job.questions).length) {
    sai(JOB_RUIM, { erro: 'o job precisa de ao menos uma pergunta em questions' });
  }
  const temLote = Array.isArray(job.lote) && job.lote.length > 0;
  if (!temLote && job.state === undefined) {
    sai(JOB_RUIM, { erro: 'o job precisa de state, ou de um lote não vazio' });
  }
  return job;
}

/** Uma resposta do SDK vira um objeto plano, com a confiança já ao lado do valor. */
function normalizar(resultado) {
  const confianca = resultado?.providerMetadata?.typesafe?.confidence ?? {};
  const fora = {};
  for (const [nome, r] of Object.entries(resultado?.answers ?? {})) {
    const item = { tipo: r.type ?? null };
    if (r.choice !== undefined) item.escolha = r.choice;
    if (r.score !== undefined) item.nota = r.score;
    if (r.probability !== undefined) item.probabilidade = r.probability;
    if (r.noul !== undefined) item.probabilidade = r.noul;
    if (r.probabilities !== undefined) item.probabilidades = r.probabilities;
    if (r.legend !== undefined) item.legenda = r.legend;
    const c = confianca[nome];
    if (c !== undefined) item.confianca = c;
    fora[nome] = item;
  }
  return fora;
}

async function main() {
  const args = process.argv.slice(2);
  const querChecar = args.includes('--check');
  const iJob = args.indexOf('--job');

  const sdk = await carregarSdk();
  if (sdk.erro) indisponivel(sdk.erro, sdk.fix);

  const temChave = Boolean(process.env.AI_GATEWAY_API_KEY || process.env.VERCEL_OIDC_TOKEN);
  if (!temChave) {
    indisponivel(
      'sem credencial do AI Gateway na máquina',
      'crie uma chave em vercel.com/dashboard, aba AI Gateway, e exporte AI_GATEWAY_API_KEY'
    );
  }

  if (querChecar) {
    // Checagem barata: uma pergunta de sim/não com estado mínimo. Saída é grátis,
    // e a entrada é de poucos tokens, então isto custa perto de zero.
    try {
      const r = await sdk.evaluate({
        model: MODELO,
        state: 'ok',
        questions: { vivo: { type: 'boolean', instructions: 'Este texto diz ok?' } },
      });
      sai(0, { disponivel: true, modelo: MODELO, resposta_de_teste: normalizar(r) });
    } catch (e) {
      const msg = String(e?.message ?? e).slice(0, 400);
      indisponivel(`a chamada de teste falhou: ${msg}`, pista(msg));
    }
  }

  const bruto = iJob >= 0 && args[iJob + 1]
    ? await (await import('node:fs/promises')).readFile(args[iJob + 1], 'utf8')
    : await new Promise((res) => {
        let t = '';
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', (c) => (t += c));
        process.stdin.on('end', () => res(t));
      });

  const job = lerJob(bruto);
  const itens = Array.isArray(job.lote) && job.lote.length
    ? job.lote
    : [{ id: job.id ?? 'unico', state: job.state }];

  const respostas = [];
  let falhas = 0;
  let barradas = 0;
  let barradasSeguidas = 0;

  // Pausa entre itens. O tier gratuito do gateway libera poucas chamadas por
  // janela, então lote sem pausa queima a cota nas primeiras linhas e o resto
  // volta vazio. Medido em 19/09/2026: cinco chamadas passam, a sexta barra.
  const iPausa = args.indexOf('--pausa');
  const pausaMs = iPausa >= 0 && args[iPausa + 1] ? Number(args[iPausa + 1]) : 1200;
  const dormir = (ms) => new Promise((r) => setTimeout(r, ms));

  for (let i = 0; i < itens.length; i++) {
    const item = itens[i];
    if (i > 0 && pausaMs > 0) await dormir(pausaMs);

    let resolvido = false;
    // Barrada por cota não é falha do item: é capacidade. Recua e tenta de novo
    // antes de desistir, porque marcar o item como perdido aqui seria mentir
    // sobre o texto dele.
    for (const recuo of [0, 15000, 45000]) {
      if (recuo) await dormir(recuo);
      try {
        const r = await sdk.evaluate({ model: MODELO, state: item.state, questions: job.questions });
        respostas.push({ id: item.id ?? null, ok: true, respostas: normalizar(r) });
        barradasSeguidas = 0;
        resolvido = true;
        break;
      } catch (e) {
        const msg = String(e?.message ?? e);
        if (!eLimite(msg)) {
          // Regra dura 3 do cânone: falha no meio do lote vira CASO DO MEIO,
          // nunca descarte por omissão. O item volta marcado pra releitura.
          falhas++;
          respostas.push({ id: item.id ?? null, ok: false, caso_do_meio: true, motivo: msg.slice(0, 400) });
          resolvido = true;
          break;
        }
      }
    }

    if (!resolvido) {
      barradas++;
      barradasSeguidas++;
      respostas.push({ id: item.id ?? null, ok: false, barrado_por_cota: true, caso_do_meio: true });
      // Cota esgotada de verdade: insistir item a item levaria horas. Para o
      // lote e devolve o que já respondeu, dizendo onde parou.
      if (barradasSeguidas >= 3) {
        sai(0, {
          disponivel: true,
          modelo: MODELO,
          cota_esgotada: true,
          total: itens.length,
          responderam: respostas.filter((r) => r.ok).length,
          casos_do_meio: falhas,
          barrados_por_cota: barradas,
          parou_no_item: i + 1,
          como_resolver: 'o tier gratuito do gateway limita as chamadas por janela; '
            + 'rode o resto mais tarde, ou compre crédito pra liberar o limite',
          itens: respostas,
        });
      }
    }
  }

  // Lote inteiro sem resposta é indisponibilidade, não resultado.
  const responderam = respostas.filter((r) => r.ok).length;
  if (responderam === 0) {
    indisponivel(
      barradas ? `as ${itens.length} chamadas do lote foram barradas por cota` : `as ${falhas} chamadas do lote falharam`,
      barradas ? 'o tier gratuito do gateway limita as chamadas por janela' : null
    );
  }

  sai(0, {
    disponivel: true,
    modelo: MODELO,
    total: itens.length,
    responderam,
    casos_do_meio: falhas,
    barrados_por_cota: barradas,
    itens: respostas,
  });
}

main().catch((e) => {
  // Rede caiu, processo morreu, qualquer coisa: é indisponibilidade, e a skill segue.
  indisponivel(`falha inesperada: ${String(e?.message ?? e).slice(0, 200)}`, null);
});

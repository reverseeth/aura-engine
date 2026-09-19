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

  for (const item of itens) {
    try {
      const r = await sdk.evaluate({
        model: MODELO,
        state: item.state,
        questions: job.questions,
      });
      respostas.push({ id: item.id ?? null, ok: true, respostas: normalizar(r) });
    } catch (e) {
      // Regra dura 3 do cânone: falha no meio do lote vira CASO DO MEIO, nunca
      // descarte por omissão. O item volta marcado pra releitura, não sumido.
      falhas++;
      respostas.push({
        id: item.id ?? null,
        ok: false,
        caso_do_meio: true,
        motivo: String(e?.message ?? e).slice(0, 400),
      });
    }
  }

  // Lote inteiro falhando é indisponibilidade, não resultado.
  if (falhas === itens.length) {
    indisponivel(`as ${falhas} chamadas do lote falharam`, null);
  }

  sai(0, {
    disponivel: true,
    modelo: MODELO,
    total: itens.length,
    responderam: itens.length - falhas,
    casos_do_meio: falhas,
    itens: respostas,
  });
}

main().catch((e) => {
  // Rede caiu, processo morreu, qualquer coisa: é indisponibilidade, e a skill segue.
  indisponivel(`falha inesperada: ${String(e?.message ?? e).slice(0, 200)}`, null);
});

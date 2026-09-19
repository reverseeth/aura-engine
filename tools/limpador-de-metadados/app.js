#!/usr/bin/env node
'use strict';
/**
 * Aura Engine — Limpador de Metadados (programa de arrastar e soltar)
 *
 * Abre uma janela no navegador (só na sua máquina, 127.0.0.1). Você arrasta os
 * criativos pra lá, ou clica pra escolher pelo seletor do próprio sistema, e o
 * programa remove todos os metadados sem perder qualidade. O arquivo limpo ocupa
 * o lugar do original, renomeado pra asset-xxxx.
 *
 * O navegador é só a janela: quem mexe no disco é este servidor, sempre por
 * caminho absoluto real. Por isso nada é copiado pra pasta nenhuma, nem pra
 * vídeo grande, e nenhum caminho precisa ser digitado.
 *
 * Iniciar: 2 cliques em "Limpador de Metadados.command" (Mac) ou
 *          "Limpador de Metadados.cmd" (Windows) na pasta da Aura,
 *          ou `node tools/limpador-de-metadados/app.js`.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const { spawn, spawnSync } = require('child_process');
const { fileURLToPath } = require('url');
const limpar = require('./limpar');

const PORTA_INICIAL = 47821;
const UI = path.join(__dirname, 'ui.html');

// Token de sessão: vai embutido no HTML servido e é exigido em toda rota /api.
// Uma página de outro site até consegue disparar um POST pra 127.0.0.1, mas não
// consegue ler o HTML (o navegador bloqueia), então nunca tem o token.
const TOKEN = crypto.randomBytes(16).toString('hex');

// Idioma do membro: sai do report_language do profile.md, que a skill `setup`
// grava. Só sugere — quem manda é o botão na janela, que fica guardado.
function idiomaDoPerfil() {
  try {
    const raiz = path.resolve(__dirname, '..', '..');
    const perfil = path.join(raiz, 'workspace', 'profile.md');
    if (!fs.existsSync(perfil)) return '';
    const m = fs.readFileSync(perfil, 'utf8').match(/report_language\s*[:=]\s*["'`]?\s*(pt-BR|pt|en)\b/i);
    if (!m) return '';
    return m[1].toLowerCase().startsWith('pt') ? 'pt' : 'en';
  } catch (e) { return ''; }
}

const ING = idiomaDoPerfil() === 'en';
const SUPORTADAS = new Set([...limpar.IMAGENS, ...limpar.VIDEOS, ...limpar.AUDIOS]);
const ehSuportada = (p) => SUPORTADAS.has(path.extname(p).toLowerCase());

function abrirNoSistema(alvo) {
  const plat = process.platform;
  try {
    if (plat === 'darwin') spawn('open', [alvo], { stdio: 'ignore', detached: true }).unref();
    else if (plat === 'win32') spawn('cmd', ['/c', 'start', '', alvo], { stdio: 'ignore', detached: true, windowsHide: true }).unref();
    else spawn('xdg-open', [alvo], { stdio: 'ignore', detached: true }).unref();
  } catch (_) { /* o usuário abre à mão */ }
}

function lerCorpo(req, limite = 8 * 1024 * 1024) {
  return new Promise((resolve, reject) => {
    const partes = []; let total = 0;
    req.on('data', c => { total += c.length; if (total > limite) { reject(new Error('corpo grande demais')); req.destroy(); } else partes.push(c); });
    req.on('end', () => resolve(Buffer.concat(partes)));
    req.on('error', reject);
  });
}

async function corpoJson(req) {
  try { return JSON.parse((await lerCorpo(req)).toString('utf8') || '{}'); } catch (_) { return {}; }
}

function json(res, status, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body), 'Cache-Control': 'no-store' });
  res.end(body);
}

// ---------------------------------------------------------------------------
// Seletor do próprio sistema — devolve caminhos absolutos reais.
// Mac: osascript · Windows: PowerShell · Linux: zenity/kdialog.
// ---------------------------------------------------------------------------
function seletorDisponivel() {
  if (process.platform === 'darwin') return true;
  if (process.platform === 'win32') return !!(binarioExiste('powershell') || binarioExiste('pwsh'));
  return !!(binarioExiste('zenity') || binarioExiste('kdialog'));
}

function binarioExiste(bin) {
  try {
    const r = spawnSync(process.platform === 'win32' ? 'where' : 'which', [bin], { encoding: 'utf8', windowsHide: true });
    return r.status === 0;
  } catch (_) { return false; }
}

function escolherNoSistema(tipo) {
  const pasta = tipo === 'pasta';
  const titulo = pasta ? (ING ? 'Choose the folder with your creatives' : 'Escolha a pasta com os criativos') : (ING ? 'Choose your creatives' : 'Escolha os criativos');

  if (process.platform === 'darwin') {
    // `tell me to activate` traz o diálogo pra frente sem controlar outro aplicativo,
    // então o macOS não pede permissão de automação pro membro.
    const script = pasta
      ? `tell me to activate\nset alvo to choose folder with prompt "${titulo}"\nreturn POSIX path of alvo`
      : `tell me to activate\nset alvos to choose file with prompt "${titulo}" with multiple selections allowed\nset saida to ""\nrepeat with a in alvos\nset saida to saida & POSIX path of a & linefeed\nend repeat\nreturn saida`;
    const r = spawnSync('osascript', ['-e', script], { encoding: 'utf8' });
    if (r.status !== 0) return { cancelado: /(-128)|User canceled/i.test(r.stderr || ''), caminhos: [], erro: r.status === null ? (ING ? 'could not open the system picker' : 'não consegui abrir o seletor do sistema') : null };
    return { caminhos: linhas(r.stdout) };
  }

  if (process.platform === 'win32') {
    const ps = pasta
      ? `Add-Type -AssemblyName System.Windows.Forms | Out-Null
$topo = New-Object System.Windows.Forms.Form
$topo.TopMost = $true
$d = New-Object System.Windows.Forms.FolderBrowserDialog
$d.Description = '${titulo}'
if ($d.ShowDialog($topo) -eq [System.Windows.Forms.DialogResult]::OK) { Write-Output $d.SelectedPath }`
      : `Add-Type -AssemblyName System.Windows.Forms | Out-Null
$topo = New-Object System.Windows.Forms.Form
$topo.TopMost = $true
$d = New-Object System.Windows.Forms.OpenFileDialog
$d.Multiselect = $true
$d.Title = '${titulo}'
if ($d.ShowDialog($topo) -eq [System.Windows.Forms.DialogResult]::OK) { $d.FileNames | ForEach-Object { Write-Output $_ } }`;
    const exe = binarioExiste('powershell') ? 'powershell' : 'pwsh';
    const b64 = Buffer.from(ps, 'utf16le').toString('base64');
    const r = spawnSync(exe, ['-NoProfile', '-NonInteractive', '-STA', '-ExecutionPolicy', 'Bypass', '-EncodedCommand', b64], { encoding: 'utf8', windowsHide: true });
    if (r.status !== 0) return { caminhos: [], erro: (ING ? 'could not open the system picker' : 'não consegui abrir o seletor do sistema') };
    const caminhos = linhas(r.stdout);
    return { caminhos, cancelado: caminhos.length === 0 };
  }

  if (binarioExiste('zenity')) {
    const args = ['--file-selection', '--separator=\n', `--title=${titulo}`];
    if (pasta) args.push('--directory'); else args.push('--multiple');
    const r = spawnSync('zenity', args, { encoding: 'utf8' });
    if (r.status !== 0) return { cancelado: true, caminhos: [] };
    return { caminhos: linhas(r.stdout) };
  }
  if (binarioExiste('kdialog')) {
    const r = spawnSync('kdialog', pasta ? ['--getexistingdirectory', os.homedir()] : ['--getopenfilename', os.homedir()], { encoding: 'utf8' });
    if (r.status !== 0) return { cancelado: true, caminhos: [] };
    return { caminhos: linhas(r.stdout) };
  }
  return { caminhos: [], erro: 'este sistema não tem um seletor de arquivos que eu consiga abrir — arraste os arquivos pra janela' };
}

function linhas(s) {
  return String(s || '').split('\n').map(l => l.trim()).filter(Boolean);
}

// ---------------------------------------------------------------------------
// Arrastar e soltar — o navegador entrega nome, tamanho e data, nunca o local do
// arquivo. Este índice acha o local real: varre as pastas de uso comum (só as
// extensões que o programa limpa) e casa nome + tamanho + data de modificação.
// Casou com um arquivo só, é ele. Casou com vários ou nenhum, não age.
// ---------------------------------------------------------------------------
const IGNORAR_PASTAS = new Set(['node_modules', 'Library', 'Applications', 'System', 'Volumes', '.git', 'AppData', 'Windows', 'Program Files', 'Program Files (x86)']);
const PROFUNDIDADE = 5;
const TETO_INDICE = 80000;
let indiceCache = { em: 0, mapa: null };

function raizesDeBusca() {
  const home = os.homedir();
  const nomes = ['Desktop', 'Downloads', 'Documents', 'Movies', 'Videos', 'Pictures', 'Área de Trabalho', 'Documentos', 'Imagens', 'Vídeos', 'Transferências'];
  const raizes = nomes.map(n => path.join(home, n)).filter(p => { try { return fs.statSync(p).isDirectory(); } catch (_) { return false; } });
  return raizes.length ? raizes : [home];
}

function indiceDoDisco() {
  if (indiceCache.mapa && Date.now() - indiceCache.em < 20000) return indiceCache.mapa;
  const mapa = new Map();
  let n = 0;
  const visitar = (dir, prof) => {
    if (prof > PROFUNDIDADE || n >= TETO_INDICE) return;
    let entradas;
    try { entradas = fs.readdirSync(dir, { withFileTypes: true }); } catch (_) { return; }
    for (const e of entradas) {
      if (n >= TETO_INDICE) return;
      if (e.name.startsWith('.') || IGNORAR_PASTAS.has(e.name)) continue;
      const p = path.join(dir, e.name);
      if (e.isDirectory()) { visitar(p, prof + 1); continue; }
      if (!e.isFile() || !ehSuportada(e.name)) continue;
      let st; try { st = fs.statSync(p); } catch (_) { continue; }
      const chave = `${e.name}|${st.size}`;
      const lista = mapa.get(chave);
      if (lista) lista.push({ caminho: p, mtime: st.mtimeMs }); else mapa.set(chave, [{ caminho: p, mtime: st.mtimeMs }]);
      n++;
    }
  };
  for (const r of raizesDeBusca()) visitar(r, 0);
  indiceCache = { em: Date.now(), mapa };
  return mapa;
}

function acharNoDisco(item) {
  const cands = indiceDoDisco().get(`${item.nome}|${item.tamanho}`) || [];
  if (cands.length === 1) return cands[0].caminho;
  if (cands.length > 1 && item.mtime) {
    const perto = cands.filter(c => Math.abs(c.mtime - item.mtime) < 2000);
    if (perto.length === 1) return perto[0].caminho;
  }
  return null;
}

function caminhoDeUri(uri) {
  try {
    if (!/^file:/i.test(uri)) return null;
    const p = fileURLToPath(uri);
    return fs.existsSync(p) ? p : null;
  } catch (_) { return null; }
}

// ---------------------------------------------------------------------------
// Servidor
// ---------------------------------------------------------------------------
const servidor = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://127.0.0.1');
  try {
    if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
      const html = fs.readFileSync(UI, 'utf8')
        .replaceAll('__AURA_TOKEN__', TOKEN)
        .replaceAll('__AURA_IDIOMA__', idiomaDoPerfil());
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
      return res.end(html);
    }

    if (url.pathname.startsWith('/api/')) {
      if (req.headers['x-aura-token'] !== TOKEN) return json(res, 403, { erro: ING ? 'invalid session — close the window and open the Cleaner again' : 'sessão inválida — feche a janela e abra o Limpador de novo' });
    }

    if (req.method === 'GET' && url.pathname === '/api/status') {
      return json(res, 200, {
        ffmpeg: limpar.temFfmpeg(),
        plataforma: process.platform,
        node: process.version,
        seletor: seletorDisponivel(),
        instalar_ffmpeg: process.platform === 'darwin' ? 'brew install ffmpeg' : process.platform === 'win32' ? 'winget install Gyan.FFmpeg' : 'sudo apt install ffmpeg',
      });
    }

    // Botão "escolher" — abre o seletor do próprio sistema e devolve os caminhos.
    if (req.method === 'POST' && url.pathname === '/api/escolher') {
      const b = await corpoJson(req);
      return json(res, 200, escolherNoSistema(b.tipo === 'pasta' ? 'pasta' : 'arquivos'));
    }

    // Arrastar e soltar — transforma o que o navegador entregou em caminhos reais.
    if (req.method === 'POST' && url.pathname === '/api/resolver') {
      const b = await corpoJson(req);
      const porUri = (b.uris || []).map(caminhoDeUri).filter(Boolean);
      if (porUri.length) return json(res, 200, { caminhos: porUri, nao_encontrados: [] });
      const caminhos = []; const nao_encontrados = [];
      for (const item of (b.itens || [])) {
        if (!item || !item.nome) continue;
        const achado = acharNoDisco(item);
        if (achado) caminhos.push(achado); else nao_encontrados.push(item.nome);
      }
      return json(res, 200, { caminhos, nao_encontrados });
    }

    // Limpeza — sempre no lugar, sempre entrando nas subpastas. Devolve uma linha
    // JSON por arquivo (NDJSON), pra lista ir aparecendo enquanto roda.
    if (req.method === 'POST' && url.pathname === '/api/limpar') {
      const b = await corpoJson(req);
      const alvos = [...new Set((b.caminhos || []).map(c => String(c || '').trim()).filter(Boolean))];
      const inexistentes = alvos.filter(a => !fs.existsSync(a));
      const arquivos = limpar.coletar(alvos.filter(a => fs.existsSync(a)), true);
      const naoSuportados = alvos.filter(a => { try { return fs.statSync(a).isFile() && !ehSuportada(a); } catch (_) { return false; } }).map(a => path.basename(a));

      res.writeHead(200, { 'Content-Type': 'application/x-ndjson; charset=utf-8', 'Cache-Control': 'no-store' });
      res.write(JSON.stringify({ inicio: true, total: arquivos.length, ignorados: naoSuportados, inexistentes: inexistentes.map(a => path.basename(a)) }) + '\n');
      const usados = new Set();
      for (const arquivo of arquivos) {
        const rel = limpar.limparArquivo(arquivo, { inPlace: true, renomear: true, usados });
        res.write(JSON.stringify(rel) + '\n');
        await new Promise(r => setImmediate(r));
      }
      indiceCache = { em: 0, mapa: null }; // os arquivos mudaram de nome: o índice envelheceu
      return res.end();
    }

    if (req.method === 'POST' && url.pathname === '/api/abrir') {
      const b = await corpoJson(req);
      const alvo = String(b.caminho || '');
      if (!alvo || !fs.existsSync(alvo)) return json(res, 400, { erro: (ING ? 'folder not found' : 'pasta não encontrada') });
      abrirNoSistema(alvo);
      return json(res, 200, { ok: true });
    }

    if (req.method === 'POST' && url.pathname === '/api/sair') {
      json(res, 200, { ok: true });
      setTimeout(() => process.exit(0), 200);
      return;
    }

    res.writeHead(404); res.end('not found');
  } catch (e) {
    if (!res.headersSent) json(res, 500, { erro: e.message || String(e) });
    else res.end();
  }
});

function iniciar(porta) {
  servidor.once('error', (e) => {
    if (e.code === 'EADDRINUSE' && porta < PORTA_INICIAL + 20) return iniciar(porta + 1);
    console.error('erro ao abrir a porta:', e.message);
    process.exit(1);
  });
  servidor.listen(porta, '127.0.0.1', () => {
    const url = `http://127.0.0.1:${porta}/`;
    console.log('');
    if (ING) {
      console.log('  Aura — Metadata Cleaner');
      console.log(`  Open at: ${url}`);
      console.log('  Clean files replace the originals, renamed asset-xxxx.');
      console.log(`  ffmpeg (video): ${limpar.temFfmpeg() ? 'ok' : 'NOT found — images work; for video, install ffmpeg'}`);
      console.log('  To close: close this window or press Ctrl+C.');
    } else {
      console.log('  Aura — Limpador de Metadados');
      console.log(`  Aberto em: ${url}`);
      console.log('  Os arquivos limpos substituem os originais, renomeados asset-xxxx.');
      console.log(`  ffmpeg (vídeo): ${limpar.temFfmpeg() ? 'ok' : 'NÃO encontrado — imagens funcionam; pra vídeo instale o ffmpeg'}`);
      console.log('  Pra fechar: feche esta janela ou aperte Ctrl+C.');
    }
    console.log('');
    if (!process.env.AURA_LIMPADOR_NO_OPEN) abrirNoSistema(url);
  });
}

iniciar(PORTA_INICIAL);

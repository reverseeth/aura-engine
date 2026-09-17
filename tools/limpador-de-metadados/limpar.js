#!/usr/bin/env node
'use strict';
/**
 * Aura Engine — Limpador de Metadados (núcleo + CLI)
 *
 * Remove TODO metadado de proveniência dos criativos antes do upload
 * (EXIF, XMP, IPTC, C2PA/JUMBF, chunks de texto como o `hf-job-id` do Higgsfield,
 * comentários, tags de encoder) e renomeia o arquivo pra `asset-xxxx.<ext>`.
 *
 * ZERO perda de qualidade, por construção:
 *   - PNG / JPEG / WebP / GIF: o container é reescrito byte a byte mantendo só os
 *     blocos que carregam pixels e cor (perfil ICC preservado). Nada é re-encodado.
 *   - Vídeo / áudio: remux via ffmpeg com `-c copy` (stream copy) — os bytes de
 *     vídeo e áudio saem idênticos, só o container é recriado sem metadados.
 *
 * Uso (CLI):
 *   node limpar.js <arquivo|pasta> [...]            (limpa NO LUGAR e renomeia)
 *   node limpar.js <pasta> --saida <dir>            (originais intactos; limpos em <dir>)
 *   node limpar.js <pasta> --recursivo              (entra nas subpastas)
 *   node limpar.js <arquivo> --verificar            (só relata o que existe, não altera)
 *   node limpar.js ... --json                       (saída em JSON, pra scripts)
 *
 * Sem dependências. Requer Node 18+ (já vem com o Claude Code). Vídeo exige ffmpeg.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const IMAGENS = new Set(['.png', '.jpg', '.jpeg', '.webp', '.gif']);
const VIDEOS = new Set(['.mp4', '.m4v', '.mov', '.webm', '.mkv', '.avi']);
const AUDIOS = new Set(['.mp3', '.m4a', '.aac', '.wav', '.flac', '.ogg']);
const EXT_NORMALIZADA = { '.jpeg': '.jpg' };

// ---------------------------------------------------------------------------
// PNG — mantém só chunks de pixel/cor. Tudo que é texto/tempo/EXIF/C2PA cai.
// ---------------------------------------------------------------------------
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const PNG_KEEP = new Set([
  'IHDR', 'PLTE', 'tRNS', 'gAMA', 'cHRM', 'sRGB', 'iCCP', 'sBIT', 'bKGD', 'hIST',
  'pHYs', 'sPLT', 'IDAT', 'IEND', 'acTL', 'fcTL', 'fdAT',
]);

function limparPng(buf) {
  if (buf.length < 8 || !buf.subarray(0, 8).equals(PNG_SIG)) throw new Error('não é um PNG válido');
  const out = [PNG_SIG];
  const removidos = [];
  let p = 8;
  while (p + 8 <= buf.length) {
    const len = buf.readUInt32BE(p);
    const tipo = buf.toString('latin1', p + 4, p + 8);
    const fim = p + 12 + len;
    if (fim > buf.length) throw new Error('PNG truncado');
    if (PNG_KEEP.has(tipo)) out.push(buf.subarray(p, fim));
    else removidos.push(tipo);
    p = fim;
    if (tipo === 'IEND') break;
  }
  return { buf: Buffer.concat(out), removidos, tipo: 'png' };
}

// ---------------------------------------------------------------------------
// JPEG — mantém só segmentos estruturais + JFIF + ICC + Adobe (cor). Dropa
// APP1 (EXIF/XMP), APP11 (C2PA/JUMBF), APP13 (IPTC/Photoshop), COM e os demais APPn.
// Os dados comprimidos (entropy-coded) são copiados intactos.
// ---------------------------------------------------------------------------
const JPEG_NOMES = { 0xe1: 'APP1 (EXIF/XMP)', 0xeb: 'APP11 (C2PA/JUMBF)', 0xed: 'APP13 (IPTC/Photoshop)', 0xfe: 'COM' };

function limparJpeg(buf) {
  if (buf.length < 4 || buf[0] !== 0xff || buf[1] !== 0xd8) throw new Error('não é um JPEG válido');
  const out = [Buffer.from([0xff, 0xd8])];
  const removidos = [];
  let p = 2;
  while (p < buf.length) {
    if (buf[p] !== 0xff) throw new Error(`JPEG: marcador esperado na posição ${p}`);
    while (p < buf.length && buf[p] === 0xff) p++; // bytes de preenchimento
    if (p >= buf.length) break;
    const m = buf[p]; p++;
    if (m === 0xd9) { out.push(Buffer.from([0xff, 0xd9])); break; } // EOI — o que vier depois é lixo/trailer
    if (m === 0xd8 || (m >= 0xd0 && m <= 0xd7) || m === 0x01) { out.push(Buffer.from([0xff, m])); continue; }
    if (p + 2 > buf.length) throw new Error('JPEG truncado');
    const len = buf.readUInt16BE(p);
    const seg = buf.subarray(p - 2, p + len);
    let manter = true;
    if (m === 0xe0) {
      const id = seg.toString('latin1', 4, 9);
      manter = id === 'JFIF\0' || id === 'JFXX\0';
    } else if (m === 0xe2) {
      manter = seg.toString('latin1', 4, 16) === 'ICC_PROFILE\0';
    } else if (m === 0xee) {
      manter = seg.toString('latin1', 4, 9) === 'Adobe';
    } else if ((m >= 0xe1 && m <= 0xef) || m === 0xfe) {
      manter = false;
    }
    if (manter) out.push(seg);
    else removidos.push(JPEG_NOMES[m] || `APP${m - 0xe0}`);
    p += len;
    if (m === 0xda) { // SOS: copia os dados comprimidos até o próximo marcador real
      const inicio = p;
      while (p < buf.length) {
        if (buf[p] === 0xff) {
          const n = buf[p + 1];
          if (n === 0x00 || (n >= 0xd0 && n <= 0xd7)) { p += 2; continue; }
          if (n === 0xff) { p++; continue; }
          break;
        }
        p++;
      }
      out.push(buf.subarray(inicio, p));
    }
  }
  return { buf: Buffer.concat(out), removidos, tipo: 'jpeg' };
}

// ---------------------------------------------------------------------------
// WebP — RIFF: mantém VP8/VP8L/VP8X/ALPH/ANIM/ANMF/ICCP; dropa EXIF, XMP e chunks
// desconhecidos (onde o C2PA mora). Limpa as flags EXIF/XMP do VP8X.
// ---------------------------------------------------------------------------
const WEBP_KEEP = new Set(['VP8 ', 'VP8L', 'VP8X', 'ALPH', 'ANIM', 'ANMF', 'ICCP']);

function limparWebp(buf) {
  if (buf.length < 12 || buf.toString('latin1', 0, 4) !== 'RIFF' || buf.toString('latin1', 8, 12) !== 'WEBP') {
    throw new Error('não é um WebP válido');
  }
  const chunks = [];
  const removidos = [];
  let p = 12;
  while (p + 8 <= buf.length) {
    const id = buf.toString('latin1', p, p + 4);
    const size = buf.readUInt32LE(p + 4);
    const padded = size + (size & 1);
    const chunk = Buffer.from(buf.subarray(p, Math.min(buf.length, p + 8 + padded)));
    if (WEBP_KEEP.has(id)) chunks.push({ id, chunk });
    else removidos.push(id.trim());
    p += 8 + padded;
  }
  for (const c of chunks) if (c.id === 'VP8X' && c.chunk.length > 8) c.chunk[8] &= ~(0x08 | 0x04);
  const body = Buffer.concat(chunks.map(c => c.chunk));
  const header = Buffer.alloc(12);
  header.write('RIFF', 0, 'latin1');
  header.writeUInt32LE(4 + body.length, 4);
  header.write('WEBP', 8, 'latin1');
  return { buf: Buffer.concat([header, body]), removidos, tipo: 'webp' };
}

// ---------------------------------------------------------------------------
// GIF — mantém cabeçalho, paletas, frames e controle gráfico; dropa comentários,
// texto simples e extensões de aplicação (XMP mora aí), exceto o loop NETSCAPE.
// ---------------------------------------------------------------------------
function limparGif(buf) {
  if (buf.length < 13 || !/^GIF8[79]a$/.test(buf.toString('latin1', 0, 6))) throw new Error('não é um GIF válido');
  const out = [];
  const removidos = [];
  const fimSubBlocos = (q) => { while (q < buf.length) { const l = buf[q]; q++; if (l === 0) return q; q += l; } return q; };
  let fim = 13;
  if (buf[10] & 0x80) fim += 3 * (1 << ((buf[10] & 7) + 1));
  out.push(buf.subarray(0, fim));
  let p = fim;
  while (p < buf.length) {
    const b = buf[p];
    if (b === 0x3b) { out.push(buf.subarray(p, p + 1)); break; }
    if (b === 0x2c) {
      let q = p + 10;
      if (buf[p + 9] & 0x80) q += 3 * (1 << ((buf[p + 9] & 7) + 1));
      q += 1;
      q = fimSubBlocos(q);
      out.push(buf.subarray(p, q)); p = q; continue;
    }
    if (b === 0x21) {
      const label = buf[p + 1];
      const q = fimSubBlocos(p + 2);
      if (label === 0xf9) out.push(buf.subarray(p, q));
      else if (label === 0xff) {
        const appId = buf.toString('latin1', p + 3, p + 3 + buf[p + 2]);
        if (/^(NETSCAPE2\.0|ANIMEXTS1\.0)/.test(appId)) out.push(buf.subarray(p, q));
        else removidos.push(`APP:${appId.trim() || '?'}`);
      } else if (label === 0xfe) removidos.push('COMMENT');
      else if (label === 0x01) removidos.push('PLAINTEXT');
      else removidos.push(`EXT:0x${label.toString(16)}`);
      p = q; continue;
    }
    throw new Error(`GIF: bloco desconhecido 0x${b.toString(16)} na posição ${p}`);
  }
  return { buf: Buffer.concat(out), removidos, tipo: 'gif' };
}

// ---------------------------------------------------------------------------
// Vídeo / áudio — ffmpeg stream copy. Nenhum frame é re-encodado.
// ---------------------------------------------------------------------------
function ffmpegPath() {
  const candidatos = [
    process.env.AURA_FFMPEG,
    'ffmpeg',
    '/opt/homebrew/bin/ffmpeg', '/usr/local/bin/ffmpeg', '/usr/bin/ffmpeg',
    process.env.LOCALAPPDATA && path.join(process.env.LOCALAPPDATA, 'Microsoft', 'WinGet', 'Links', 'ffmpeg.exe'),
    'C:\\ffmpeg\\bin\\ffmpeg.exe',
  ].filter(Boolean);
  for (const c of candidatos) {
    try {
      const r = spawnSync(c, ['-version'], { encoding: 'utf8', windowsHide: true });
      if (r.status === 0) return c;
    } catch (_) { /* tenta o próximo */ }
  }
  return null;
}

function temFfmpeg() { return !!ffmpegPath(); }

function limparAV(entrada, saida, ext, ehAudio) {
  const ff = ffmpegPath();
  if (!ff) throw new Error('ffmpeg não encontrado — Mac: brew install ffmpeg · Windows: winget install Gyan.FFmpeg');
  const args = ['-y', '-hide_banner', '-loglevel', 'error', '-nostdin', '-i', entrada];
  if (ehAudio) args.push('-map', '0:a:0');
  else args.push('-map', '0:v:0', '-map', '0:a?');
  args.push(
    '-map_metadata', '-1', '-map_metadata:s:v', '-1', '-map_metadata:s:a', '-1', '-map_chapters', '-1',
    '-c', 'copy', '-fflags', '+bitexact', '-flags:v', '+bitexact', '-flags:a', '+bitexact',
  );
  if (['.mp4', '.m4v', '.mov', '.m4a'].includes(ext)) args.push('-movflags', '+faststart');
  args.push(saida);
  const r = spawnSync(ff, args, { encoding: 'utf8', windowsHide: true, maxBuffer: 1 << 24 });
  if (r.status !== 0) {
    try { fs.unlinkSync(saida); } catch (_) { /* nada */ }
    throw new Error(`ffmpeg falhou: ${(r.stderr || '').trim().split('\n').slice(-2).join(' ') || 'erro desconhecido'}`);
  }
  return { removidos: ['metadados do container (global, streams e capítulos)', 'tags de encoder'], tipo: ehAudio ? 'audio' : 'video' };
}

// ---------------------------------------------------------------------------
// Verificação — varre o arquivo limpo procurando assinaturas conhecidas.
// ---------------------------------------------------------------------------
const ASSINATURAS = [
  ['c2pa', 'C2PA'], ['jumb', 'JUMBF'], ['urn:uuid:c2pa', 'C2PA'], ['hf-job', 'Higgsfield job id'],
  ['http://ns.adobe.com/xap', 'XMP'], ['<x:xmpmeta', 'XMP'], ['Exif\0\0', 'EXIF'],
  ['Photoshop 3.0', 'IPTC/Photoshop'], ['AIGC', 'tag de IA'], ['Made with AI', 'tag de IA'],
  ['DigitalSourceType', 'IPTC digital source'], ['trainedAlgorithmicMedia', 'IPTC AI'],
  ['openai', 'OpenAI'], ['midjourney', 'Midjourney'], ['higgsfield', 'Higgsfield'], ['stable diffusion', 'Stable Diffusion'],
  ['Lavf', 'tag do ffmpeg'], ['x264', 'tag do encoder'],
];

function verificarBuffer(buf) {
  const achados = new Set();
  const lower = buf.toString('latin1').toLowerCase();
  for (const [ass, nome] of ASSINATURAS) {
    if (nome === 'tag do encoder') continue; // "x264" pode aparecer no bitstream legítimo do H.264
    if (lower.includes(ass.toLowerCase())) achados.add(nome);
  }
  return [...achados];
}

function verificarArquivo(arquivo) {
  const st = fs.statSync(arquivo);
  const JANELA = 8 * 1024 * 1024;
  if (st.size <= 2 * JANELA) return verificarBuffer(fs.readFileSync(arquivo));
  const fd = fs.openSync(arquivo, 'r');
  try {
    const a = Buffer.alloc(JANELA); fs.readSync(fd, a, 0, JANELA, 0);
    const b = Buffer.alloc(JANELA); fs.readSync(fd, b, 0, JANELA, st.size - JANELA);
    return [...new Set([...verificarBuffer(a), ...verificarBuffer(b)])];
  } finally { fs.closeSync(fd); }
}

// ---------------------------------------------------------------------------
// Nome novo — asset-xxxx (a-z0-9), sem colisão na pasta de destino.
// ---------------------------------------------------------------------------
const PADRAO_ASSET = /^asset-[a-z0-9]{4,8}\.[a-z0-9]+$/i;

function nomeAsset(dir, ext, usados) {
  const alfabeto = 'abcdefghijklmnopqrstuvwxyz0123456789';
  for (let tentativa = 0; tentativa < 50; tentativa++) {
    let id = '';
    const bytes = crypto.randomBytes(4);
    for (let i = 0; i < 4; i++) id += alfabeto[bytes[i] % alfabeto.length];
    const nome = `asset-${id}${ext}`;
    if (!usados.has(nome) && !fs.existsSync(path.join(dir, nome))) { usados.add(nome); return nome; }
  }
  throw new Error('não consegui gerar um nome único');
}

// ---------------------------------------------------------------------------
// Limpeza de um arquivo
// ---------------------------------------------------------------------------
function limparArquivo(arquivo, opts = {}) {
  const { saida = null, inPlace = false, renomear = true, nomeOriginal = null, usados = new Set() } = opts;
  const origem = path.resolve(arquivo);
  const nomeBase = nomeOriginal || path.basename(origem);
  const extOrig = path.extname(nomeBase).toLowerCase();
  const ext = EXT_NORMALIZADA[extOrig] || extOrig;
  const dirDestino = inPlace ? path.dirname(origem) : (saida ? path.resolve(saida) : path.join(path.dirname(origem), 'limpos'));
  const rel = { origem, nome_original: nomeBase, tipo: null, removidos: [], bytes_antes: 0, bytes_depois: 0, residuos: [], destino: null, erro: null };
  try {
    const st = fs.statSync(origem);
    rel.bytes_antes = st.size;
    fs.mkdirSync(dirDestino, { recursive: true });
    const manterNome = !renomear || PADRAO_ASSET.test(nomeBase);
    const nomeNovo = manterNome ? nomeBase.replace(/\.[^.]+$/, ext) : nomeAsset(dirDestino, ext, usados);
    const destino = path.join(dirDestino, nomeNovo);
    const tmp = path.join(dirDestino, `.aura-tmp-${process.pid}-${crypto.randomBytes(3).toString('hex')}${ext}`);

    if (IMAGENS.has(ext)) {
      const buf = fs.readFileSync(origem);
      const r = ext === '.png' ? limparPng(buf) : ext === '.jpg' ? limparJpeg(buf) : ext === '.webp' ? limparWebp(buf) : limparGif(buf);
      fs.writeFileSync(tmp, r.buf);
      rel.tipo = r.tipo; rel.removidos = r.removidos;
    } else if (VIDEOS.has(ext) || AUDIOS.has(ext)) {
      const r = limparAV(origem, tmp, ext, AUDIOS.has(ext));
      rel.tipo = r.tipo; rel.removidos = r.removidos;
    } else {
      throw new Error(`formato ${ext || 'sem extensão'} não suportado — exporte como PNG/JPG/WebP/GIF ou MP4/MOV`);
    }

    if (inPlace) {
      fs.unlinkSync(origem);
      if (fs.existsSync(destino) && destino !== origem) fs.unlinkSync(destino);
    }
    fs.renameSync(tmp, destino);
    rel.destino = destino;
    rel.bytes_depois = fs.statSync(destino).size;
    rel.residuos = verificarArquivo(destino);
  } catch (e) {
    rel.erro = e.message || String(e);
  }
  return rel;
}

// ---------------------------------------------------------------------------
// Coleta de caminhos (arquivo ou pasta)
// ---------------------------------------------------------------------------
function coletar(caminhos, recursivo = false) {
  const lista = [];
  const visitar = (p, profundidade) => {
    let st; try { st = fs.statSync(p); } catch (_) { return; }
    if (st.isFile()) {
      const ext = path.extname(p).toLowerCase();
      if (IMAGENS.has(ext) || VIDEOS.has(ext) || AUDIOS.has(ext)) lista.push(p);
      return;
    }
    if (st.isDirectory()) {
      if (path.basename(p) === 'limpos' && profundidade > 0) return;
      for (const nome of fs.readdirSync(p)) {
        if (nome.startsWith('.')) continue;
        const filho = path.join(p, nome);
        const stf = fs.statSync(filho);
        if (stf.isDirectory() ? (recursivo && path.basename(filho) !== 'limpos') : true) visitar(filho, profundidade + 1);
      }
    }
  };
  for (const c of caminhos) visitar(path.resolve(c), 0);
  return lista;
}

function limparCaminhos(caminhos, opts = {}) {
  const arquivos = coletar(caminhos, !!opts.recursivo);
  const usados = new Set();
  return arquivos.map(a => limparArquivo(a, { ...opts, usados }));
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function cli(argv) {
  const args = argv.slice();
  const opts = { inPlace: true, saida: null, recursivo: false, json: false, verificar: false, renomear: true };
  const alvos = [];
  while (args.length) {
    const a = args.shift();
    if (a === '--saida' || a === '--out') { opts.saida = args.shift(); opts.inPlace = false; }
    else if (a === '--in-place') opts.inPlace = true;
    else if (a === '--recursivo' || a === '-r') opts.recursivo = true;
    else if (a === '--json') opts.json = true;
    else if (a === '--verificar' || a === '--check') opts.verificar = true;
    else if (a === '--sem-renomear') opts.renomear = false;
    else if (a === '-h' || a === '--help') { console.log(fs.readFileSync(__filename, 'utf8').split('\n').slice(2, 22).join('\n')); return 0; }
    else alvos.push(a);
  }
  if (!alvos.length) { console.error('uso: bash tools/strip-metadata.sh <arquivo|pasta> [--saida <dir>] [--recursivo] [--verificar] [--json]'); return 2; }

  if (opts.verificar) {
    const arquivos = coletar(alvos, opts.recursivo);
    const rel = arquivos.map(a => ({ arquivo: a, residuos: verificarArquivo(a) }));
    if (opts.json) console.log(JSON.stringify(rel, null, 2));
    else for (const r of rel) console.log(`${r.residuos.length ? '⚠' : '✓'} ${r.arquivo}${r.residuos.length ? '  →  ' + r.residuos.join(', ') : '  limpo'}`);
    return rel.some(r => r.residuos.length) ? 1 : 0;
  }

  const rel = limparCaminhos(alvos, opts);
  if (opts.json) { console.log(JSON.stringify(rel, null, 2)); return rel.some(r => r.erro) ? 1 : 0; }
  let ok = 0, erros = 0;
  for (const r of rel) {
    if (r.erro) { erros++; console.log(`✗ ${r.nome_original}\n    ${r.erro}`); continue; }
    ok++;
    const rem = r.removidos.length ? r.removidos.join(', ') : 'nenhum metadado encontrado';
    console.log(`✓ ${r.nome_original}  →  ${path.basename(r.destino)}   [${r.tipo}]`);
    console.log(`    removido: ${rem}`);
    if (r.residuos.length) console.log(`    AVISO — ainda aparece: ${r.residuos.join(', ')}`);
  }
  console.log(`\nconcluído: ${ok} limpo(s), ${erros} erro(s)${rel.length && rel[0].destino ? `\npasta: ${path.dirname(rel.find(r => r.destino).destino)}` : ''}`);
  return erros ? 1 : 0;
}

module.exports = { limparArquivo, limparCaminhos, coletar, verificarArquivo, temFfmpeg, ffmpegPath, IMAGENS, VIDEOS, AUDIOS };

if (require.main === module) process.exit(cli(process.argv.slice(2)));

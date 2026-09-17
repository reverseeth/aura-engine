#!/usr/bin/env node
'use strict';
/**
 * Aura Engine — Limpador de Metadados (programa de arrastar e soltar)
 *
 * Abre uma janela no navegador (só na sua máquina, 127.0.0.1). Você arrasta os
 * criativos pra lá (ou clica pra escolher), o programa remove todos os metadados
 * sem perder qualidade, renomeia pra asset-xxxx e salva numa pasta de saída.
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
const { spawn } = require('child_process');
const limpar = require('./limpar');

const PORTA_INICIAL = 47821;
const UI = path.join(__dirname, 'ui.html');

function pastaSaidaPadrao() {
  const desktop = path.join(os.homedir(), 'Desktop');
  const base = fs.existsSync(desktop) ? desktop : os.homedir();
  return path.join(base, 'Aura Limpos');
}

function abrirNoSistema(alvo) {
  const plat = process.platform;
  try {
    if (plat === 'darwin') spawn('open', [alvo], { stdio: 'ignore', detached: true }).unref();
    else if (plat === 'win32') spawn('cmd', ['/c', 'start', '', alvo], { stdio: 'ignore', detached: true, windowsHide: true }).unref();
    else spawn('xdg-open', [alvo], { stdio: 'ignore', detached: true }).unref();
  } catch (_) { /* o usuário abre à mão */ }
}

function lerCorpo(req, limite = 64 * 1024 * 1024) {
  return new Promise((resolve, reject) => {
    const partes = []; let total = 0;
    req.on('data', c => { total += c.length; if (total > limite) { reject(new Error('corpo grande demais')); req.destroy(); } else partes.push(c); });
    req.on('end', () => resolve(Buffer.concat(partes)));
    req.on('error', reject);
  });
}

function salvarCorpoEmTmp(req, nome) {
  return new Promise((resolve, reject) => {
    const dir = path.join(os.tmpdir(), 'aura-limpador');
    fs.mkdirSync(dir, { recursive: true });
    const tmp = path.join(dir, `${crypto.randomBytes(4).toString('hex')}-${nome.replace(/[^\w.\-]+/g, '_')}`);
    const ws = fs.createWriteStream(tmp);
    req.pipe(ws);
    ws.on('finish', () => resolve(tmp));
    ws.on('error', reject);
    req.on('error', reject);
  });
}

function json(res, status, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body) });
  res.end(body);
}

let saidaAtual = pastaSaidaPadrao();
const usados = new Set();

const servidor = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://127.0.0.1');
  try {
    if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return res.end(fs.readFileSync(UI));
    }
    if (req.method === 'GET' && url.pathname === '/api/status') {
      return json(res, 200, {
        ffmpeg: limpar.temFfmpeg(),
        plataforma: process.platform,
        saida: saidaAtual,
        node: process.version,
        instalar_ffmpeg: process.platform === 'darwin' ? 'brew install ffmpeg' : process.platform === 'win32' ? 'winget install Gyan.FFmpeg' : 'sudo apt install ffmpeg',
      });
    }
    if (req.method === 'POST' && url.pathname === '/api/saida') {
      const b = JSON.parse((await lerCorpo(req)).toString('utf8') || '{}');
      if (b.saida && String(b.saida).trim()) saidaAtual = path.resolve(String(b.saida).trim());
      fs.mkdirSync(saidaAtual, { recursive: true });
      return json(res, 200, { saida: saidaAtual });
    }
    if (req.method === 'POST' && url.pathname === '/api/limpar') {
      const nome = decodeURIComponent(url.searchParams.get('nome') || 'arquivo');
      const tmp = await salvarCorpoEmTmp(req, nome);
      const rel = limpar.limparArquivo(tmp, { saida: saidaAtual, renomear: true, nomeOriginal: nome, usados });
      try { fs.unlinkSync(tmp); } catch (_) { /* já foi movido ou limpo */ }
      return json(res, 200, rel);
    }
    if (req.method === 'POST' && url.pathname === '/api/limpar-pasta') {
      const b = JSON.parse((await lerCorpo(req)).toString('utf8') || '{}');
      const caminho = String(b.caminho || '').trim();
      if (!caminho || !fs.existsSync(caminho)) return json(res, 400, { erro: 'pasta ou arquivo não encontrado' });
      const rel = limpar.limparCaminhos([caminho], { inPlace: !!b.substituir, saida: b.substituir ? null : saidaAtual, recursivo: !!b.recursivo, renomear: true });
      return json(res, 200, rel);
    }
    if (req.method === 'POST' && url.pathname === '/api/abrir') {
      const b = JSON.parse((await lerCorpo(req)).toString('utf8') || '{}');
      const alvo = b.caminho ? String(b.caminho) : saidaAtual;
      fs.mkdirSync(alvo, { recursive: true });
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
    json(res, 500, { erro: e.message || String(e) });
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
    fs.mkdirSync(saidaAtual, { recursive: true });
    console.log('');
    console.log('  Aura — Limpador de Metadados');
    console.log(`  Aberto em: ${url}`);
    console.log(`  Arquivos limpos vão pra: ${saidaAtual}`);
    console.log(`  ffmpeg (vídeo): ${limpar.temFfmpeg() ? 'ok' : 'NÃO encontrado — imagens funcionam; pra vídeo instale o ffmpeg'}`);
    console.log('  Pra fechar: feche esta janela ou aperte Ctrl+C.');
    console.log('');
    if (!process.env.AURA_LIMPADOR_NO_OPEN) abrirNoSistema(url);
  });
}

iniciar(PORTA_INICIAL);

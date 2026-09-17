#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trends_batch.py — roda vários termos no Google Trends com ritmo, retentativa e retomada.

Por que existe: o endpoint que o próprio site do Trends usa aceita ~25-30 consultas
seguidas do mesmo IP e depois responde 429 por um tempo (na prática, 30-60 minutos).
Uma rodada de product research mede 30-40 termos, então sem ritmo a metade final
volta como "blocked". Este script:

  1. espaça as consultas (--gap, padrão 20 s);
  2. pausa entre lotes (--batch N termos, --pause segundos);
  3. quando um termo volta bloqueado, espera --cooldown e tenta de novo (até --retries);
  4. pula termos que já têm série salva na pasta de saída (retomável).

Uso:
  python3 .claude/lib/web-fetch/trends_batch.py --out <pasta> "termo 1" "termo 2" ...
  python3 .claude/lib/web-fetch/trends_batch.py --out <pasta> --terms termos.txt   (1 por linha)

Saída: <pasta>/<termo_com_underscores>.json (mesmo JSON do `fetch.py --mode trends --json`)
       e um resumo no stdout com a classificação (SUBINDO / FLAT / SPIKE / QUEDA) de cada termo.
Sai com código 2 se algum termo continuou bloqueado depois das retentativas.
"""
import argparse, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
FETCH = os.path.join(HERE, "fetch.py")

def fname(term):
    return term.strip().lower().replace(" ", "_").replace("/", "_") + ".json"

def has_series(path):
    try:
        d = json.load(open(path))
        return bool((d.get("trend") or {}).get("series"))
    except Exception:
        return False

def run_one(term, out):
    path = os.path.join(out, fname(term))
    with open(path, "w") as fh:
        subprocess.run([sys.executable, FETCH, term, "--mode", "trends", "--json"], stdout=fh, stderr=subprocess.DEVNULL)
    return path, has_series(path)

def summary(path, term):
    d = json.load(open(path)); t = d.get("trend") or {}; s = t.get("series") or []
    v = [x for _, x in s]
    last12 = sum(v[-12:]) / 12; prev12 = sum(v[-24:-12]) / 12 if len(v) >= 24 else 0
    peak = s[v.index(max(v))][0]
    return f"{term}: {t.get('verdict')} | agora={v[-1]} pico={max(v)} ({peak}) | média 12 sem={last12:.0f} vs 12 anteriores={prev12:.0f}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--terms", dest="terms_file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--gap", type=float, default=20)
    ap.add_argument("--batch", type=int, default=20)
    ap.add_argument("--pause", type=float, default=600)
    ap.add_argument("--cooldown", type=float, default=900)
    ap.add_argument("--retries", type=int, default=2)
    a = ap.parse_args()
    terms = list(a.terms)
    if a.terms_file:
        terms += [l.strip() for l in open(a.terms_file) if l.strip() and not l.startswith("#")]
    os.makedirs(a.out, exist_ok=True)
    pending = [t for t in terms if not has_series(os.path.join(a.out, fname(t)))]
    print(f"[trends_batch] {len(terms)} termos, {len(terms)-len(pending)} já medidos, {len(pending)} a medir", flush=True)
    blocked = []
    for i, term in enumerate(pending, 1):
        ok = False
        for attempt in range(a.retries + 1):
            path, ok = run_one(term, a.out)
            if ok:
                print("  " + summary(path, term), flush=True); break
            if attempt < a.retries:
                print(f"  {term}: bloqueado, esperando {a.cooldown:.0f}s antes de tentar de novo", flush=True)
                time.sleep(a.cooldown)
        if not ok:
            blocked.append(term); print(f"  {term}: BLOQUEADO depois de {a.retries+1} tentativas", flush=True)
        if i < len(pending):
            time.sleep(a.pause if i % a.batch == 0 else a.gap)
    if blocked:
        print("[trends_batch] ainda bloqueados: " + ", ".join(blocked) + " — rode de novo mais tarde (o script retoma de onde parou) ou peça o print do Trends ao membro.")
        sys.exit(2)
    print("[trends_batch] todos os termos medidos.")

if __name__ == "__main__":
    main()

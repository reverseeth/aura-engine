#!/usr/bin/env python3
"""Aura Engine — merge seguro de template JSON do Shopify.

Regenerar um `templates/*.json` a partir dos presets das sections APAGA tudo que o
membro configurou no theme editor: fotos (image_picker), textos editados, ordem de
blocks, variant IDs. Este script existe para nunca mais fazer isso.

Fluxo correto ao adicionar/remover uma section:

    shopify theme pull --theme <id> --store <loja> --path <dir> --nodelete --only "templates/index.json"
    python3 tools/theme-template-merge.py <dir>/templates/index.json \
        --add nova-section:page-3am-nova --after research
    shopify theme push --theme <id> --store <loja> --path <dir> --nodelete --only "templates/index.json"

O que o merge faz: preserva byte a byte todas as sections existentes (settings e blocks),
mexendo apenas no que foi pedido. Sem --add/--remove/--move, ele só valida e relata.
"""
import argparse, json, sys
from pathlib import Path


def carregar(p: Path):
    raw = p.read_text(encoding="utf-8")
    inicio = raw.find("{")
    return raw[:inicio], json.loads(raw[inicio:])


def salvar(p: Path, cabecalho: str, dados: dict):
    p.write_text(cabecalho + json.dumps(dados, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template", type=Path)
    ap.add_argument("--add", help="id:type da section a adicionar (ex: club:page-3am-club)")
    ap.add_argument("--after", help="id da section que deve vir antes da nova")
    ap.add_argument("--remove", help="id da section a remover")
    ap.add_argument("--move", help="id:posicao (ex: club:7) para reordenar")
    args = ap.parse_args()

    cabecalho, d = carregar(args.template)
    antes = len(d.get("sections", {}))

    if args.add:
        sid, stype = args.add.split(":", 1)
        if sid in d["sections"]:
            print(f"'{sid}' já existe no template — nada a fazer (settings preservados)")
        else:
            d["sections"][sid] = {"type": stype, "settings": {}}
            if args.after and args.after in d["order"]:
                d["order"].insert(d["order"].index(args.after) + 1, sid)
            else:
                d["order"].append(sid)
            print(f"section '{sid}' adicionada" + (f" depois de '{args.after}'" if args.after else " no fim"))

    if args.remove:
        d["sections"].pop(args.remove, None)
        if args.remove in d["order"]:
            d["order"].remove(args.remove)
        print(f"section '{args.remove}' removida")

    if args.move:
        sid, pos = args.move.split(":", 1)
        if sid in d["order"]:
            d["order"].remove(sid)
            d["order"].insert(int(pos), sid)
            print(f"section '{sid}' movida para a posição {pos}")

    # integridade
    erros = [s for s in d["order"] if s not in d["sections"]]
    orfas = [s for s in d["sections"] if s not in d["order"]]
    if erros:
        print("ERRO: em 'order' mas sem definição:", erros); sys.exit(1)
    if orfas:
        print("AVISO: definidas mas fora de 'order':", orfas)

    # o que seria perdido se alguém regenerasse do zero
    mantidos = []
    for sid, sec in d["sections"].items():
        n = len(sec.get("settings") or {})
        for b in (sec.get("blocks") or {}).values():
            n += len(b.get("settings") or {})
        if n:
            mantidos.append(f"{sid}({n})")
    if args.add or args.remove or args.move:
        salvar(args.template, cabecalho, d)
    print(f"sections: {antes} → {len(d['sections'])} | configurações preservadas: {', '.join(mantidos) or 'nenhuma'}")


if __name__ == "__main__":
    main()

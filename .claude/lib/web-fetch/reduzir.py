#!/usr/bin/env python3
"""
Reduz o texto cru de uma página de venda ao NÚCLEO PERSUASIVO.

Por que existe: o texto que sai de um scraper é, em boa parte, moldura. Banner
de cookie, gaveta do carrinho, grade de produtos relacionados, rodapé, e o
letreiro de "Buy 2 Get 1 Free" repetido quarenta vezes. Numa página real medida
em 19/09/2026, os primeiros três mil caracteres não tinham UMA linha de copy: a
primeira menção ao problema que a marca resolve aparecia no caractere 10.105.

Quem lê esse texto sem reduzir julga a moldura, não a página. Vale pro modelo de
raciocínio e vale em dobro pra camada de decisão rápida, que responde com
confiança zero quando o estado é metade ruído.

Uso:
    python3 .claude/lib/web-fetch/reduzir.py <arquivo.json|arquivo.txt> [--max 8000]
    cat pagina.txt | python3 .claude/lib/web-fetch/reduzir.py --max 8000

Entra texto (ou o JSON do fetch.py, que tem o campo "text"), sai o núcleo.
"""
import json
import re
import sys

# Linhas que são moldura em qualquer loja. Comparação em minúsculas, por trecho.
MOLDURA = (
    "we use cookies", "cookie", "privacy policy", "terms of service", "skip to content",
    "your cart", "cart is empty", "continue to checkout", "estimated total",
    "taxes included", "calculated at checkout", "add to cart", "view cart",
    "customers also bought", "you may also like", "related products", "recently viewed",
    "sign up for", "subscribe to our", "follow us", "all rights reserved",
    "loading...", "preferences", "accept", "reject", "search", "menu", "close",
    "log in", "sign in", "create account", "my account", "track order",
    "choose options", "quick view", "sold out", "back to top",
)

# Linha que é só preço, só moeda, só número, ou só um rótulo de vitrine.
SO_PRECO = re.compile(r"^[\s€$£R]*[\d.,]+\s*(eur|usd|gbp|brl)?\s*$", re.I)
ROTULO_VITRINE = re.compile(
    r"^(bestseller|best seller|top rated|new arrival|trending|customer favorite|"
    r"people'?s choice|sale|new|popular|featured|limited)$", re.I)

def e_moldura(linha):
    b = linha.strip().lower()
    if not b:
        return True
    if SO_PRECO.match(b) or ROTULO_VITRINE.match(b):
        return True
    return any(m in b for m in MOLDURA)

def vale_a_pena(linha):
    """Fica a linha que carrega argumento: frase, claim com número, ou manchete."""
    b = linha.strip()
    if len(b) >= 45:
        return True                                  # prosa
    if re.search(r"\d", b) and len(b) >= 12:
        return True                                  # claim com número
    if len(b) >= 18 and re.search(r"[a-z]", b):
        return True                                  # manchete curta
    return False

def sem_listas(linhas, minimo=6):
    """Derruba corrida de linhas curtas sem pontuação: é menu, grade de produto
    ou lista de países do frete. Uma lista de benefícios sobrevive, porque
    benefício termina em ponto."""
    def solta(l):
        return len(l) < 45 and not re.search(r"[.!?:]$", l)
    fora, bloco = [], []
    for l in linhas + [None]:
        if l is not None and solta(l):
            bloco.append(l)
            continue
        if len(bloco) < minimo:
            fora.extend(bloco)
        bloco = []
        if l is not None:
            fora.append(l)
    return fora

def reduzir(texto, max_chars=8000, repeticoes=1):
    linhas = [l.strip() for l in texto.splitlines()]
    vistas = {}
    saida = []
    for l in linhas:
        if e_moldura(l) or not vale_a_pena(l):
            continue
        chave = l.lower()
        vistas[chave] = vistas.get(chave, 0) + 1
        if vistas[chave] > repeticoes:               # letreiro repetido
            continue
        saida.append(l)
    saida = sem_listas(saida)
    texto = "\n".join(saida)
    texto = re.sub(r"\n{3,}", "\n\n", texto).strip()
    return texto[:max_chars]

def main():
    args = [a for a in sys.argv[1:]]
    max_chars = 8000
    if "--max" in args:
        i = args.index("--max")
        max_chars = int(args[i + 1])
        del args[i:i + 2]
    bruto = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()
    try:
        d = json.loads(bruto)
        bruto = d.get("text") or d.get("content") or ""
    except (json.JSONDecodeError, AttributeError):
        pass
    sys.stdout.write(reduzir(bruto, max_chars))

if __name__ == "__main__":
    main()

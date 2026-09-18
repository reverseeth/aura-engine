#!/usr/bin/env python3
"""
palette_engine.py — 3 paletas candidatas, com motivo, geradas a partir dos 8 presets.

Por que existe: oferecer ao membro um menu de 8 presets fixos deixava a página com a paleta
do preset mais próximo, nunca com a paleta daquele produto; e paleta escolhida por amostra de
cor solta é escolha às cegas. Este gerador parte dos MESMOS 8 presets (o perfil de claridade e
de saturação de cada role sai de `presets.json`), troca o matiz por um que carrega significado
na vertical do produto e devolve exatamente 3 candidatas: nome curto, motivo em uma frase, a
relação de matiz declarada e os tokens completos. A `page-design` (ETAPA 2, Caminho 4) monta a
comparadora com as 3 aplicadas à página real e o membro escolhe vendo a cor no contexto.

O que o script garante antes de devolver (nenhuma paleta sai sem passar nos quatro testes):
  1. saturação   `primary` e `accent` acima do piso de 0.35 em HSL: cor viva, nunca cinza
  2. harmonia    a distância de matiz entre `primary` e `accent` bate com a relação declarada
                 (análoga, complementar dividida ou tríade), nunca sorteada
  3. contraste   WCAG AA (4.5:1) em `foreground` e `muted` contra `background` E contra `surface`,
                 e em `on_primary`/`primary`; 3:1 em `accent`/`background` (elemento gráfico).
                 Candidata que não passa é corrigida na claridade e revalidada, nunca entregue
                 com aviso; se não convergir, o script sai com erro em vez de imprimir a paleta
  4. distinção   as 3 candidatas têm matiz de `primary` a 25 graus ou mais uma da outra

Cada candidata também carrega os tokens que não são de cor (`heading_font`, `body_font`,
`google_fonts`, `radius`, `shadow`, `density`) LITERAIS do preset que serviu de base: escolher a
paleta é escolher também o caráter tipográfico e de forma, sem a skill inventar nada em runtime.

Mesma entrada devolve sempre a mesma saída: a variação entre membros vem do hash das entradas
(vertical, avatar, ceticismo, sementes), nunca de sorteio.

Uso:
  python3 .claude/lib/design-presets/palette_engine.py --vertical supplements
  python3 .claude/lib/design-presets/palette_engine.py --vertical beauty --skepticism alto \
      --avatar "mulheres de 45 a 65 anos que já tentaram de tudo"
  python3 .claude/lib/design-presets/palette_engine.py --vertical home --seed "#C66B3D,#9CAF88"
  python3 .claude/lib/design-presets/palette_engine.py --vertical health \
      --signals workspace/<slug>/page/design-signals.json --format json --out /tmp/paletas.json
  python3 .claude/lib/design-presets/palette_engine.py --vertical other --format css

  --vertical    obrigatório; mesmo eixo do seletor de espécimes do `swipe-models`
                (supplements, health, beauty, home, relationship, other)
  --avatar      linha do avatar central da `market-research` (entra no motivo de cada paleta)
  --skepticism  baixo | médio | alto (default médio); alto pede tom mais sóbrio
  --seed        hex da marca ou da referência do membro, separados por vírgula
  --signals     `design-signals.json` já gravado; as cores dele entram como semente
  --lang        pt-BR (default) ou en; muda nome, motivo e rótulos
  --theme       auto (default), light ou dark
  --format      md (default), json ou css (blocos de token em trio R,G,B pra comparadora)
  --out         salva a saída no caminho em vez de imprimir

Só biblioteca padrão. Exit 0 = 3 paletas válidas; 1 = valor ou arquivo de entrada inválido;
2 = uso incorreto (argparse); 3 = não convergiu, e aí nada é impresso.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRESETS_FILE = HERE / "presets.json"

ROLES = ("background", "surface", "foreground", "primary", "on_primary", "accent", "muted", "border")
NEUTRAL_ROLES = ("background", "surface", "foreground", "border", "muted")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

# Pisos e alvos que o validador cobra. Mexer aqui muda o framework inteiro.
SATURATION_FLOOR = 0.35          # HSL; abaixo disso a cor lê como cinza
CONTRAST_AA = 4.5                # texto normal, WCAG AA
CONTRAST_GRAPHIC = 3.0           # elemento gráfico (accent sobre o fundo), WCAG AA
ACCENT_CONTRAST_CEILING = 7.5    # acima disso a cor de apoio deixa de ser cor e vira tinta
YELLOW_BAND = (40.0, 95.0)       # faixa de matiz que escurece virando marrom, nunca fica escura
MIN_HUE_SPREAD = 25.0            # graus entre os `primary` das 3 candidatas
SPREAD_MARGIN = 5.0              # folga que o gerador guarda acima do piso, pro arredondamento
PALETTE_COUNT = 3

HARMONY_ORDER = ("analogous", "split-complementary", "triad")
HARMONY_OFFSET = {"analogous": 32.0, "split-complementary": 152.0, "triad": 120.0}
HARMONY_RANGE = {"analogous": (20.0, 50.0), "split-complementary": (140.0, 180.0), "triad": (105.0, 135.0)}
HARMONY_LABEL = {
    "analogous": {
        "pt-BR": "análoga (a cor de apoio é vizinha no círculo de cores)",
        "en": "analogous (support color sits next to it on the wheel)",
    },
    "split-complementary": {
        "pt-BR": "complementar dividida (a cor de apoio vem do lado oposto, sem bater de frente)",
        "en": "split-complementary (support color comes from the opposite side, without clashing)",
    },
    "triad": {
        "pt-BR": "tríade (as duas cores ficam a um terço do círculo uma da outra)",
        "en": "triad (the two colors sit a third of the wheel apart)",
    },
}

# Faixas de matiz: o nome e o que a cor comunica. Serve pra nomear QUALQUER matiz, inclusive o
# que veio da semente do membro. Grau sempre com casa decimal, aqui e na tabela de verticais.
HUE_FAMILIES = (
    (350.0, 15.0, "vermelho", "red", "chama atenção e acelera a decisão", "grabs attention and speeds the decision up"),
    (15.0, 34.0, "terracota", "terracotta", "lê como comida de verdade e feito à mão", "reads as real food, made by hand"),
    (34.0, 49.0, "âmbar", "amber", "lê como calor e recompensa", "reads as warmth and reward"),
    (49.0, 67.0, "dourado", "gold", "lê como prêmio e cuidado antigo", "reads as premium and old-world care"),
    (67.0, 89.0, "oliva", "olive", "lê como campo e sobriedade", "reads as field-grown and sober"),
    (89.0, 141.0, "verde", "green", "lê como natural e vivo", "reads as natural and alive"),
    (141.0, 171.0, "verde de farmácia", "apothecary green", "lê como natural e testado ao mesmo tempo", "reads as natural and tested at once"),
    (171.0, 196.0, "turquesa", "teal", "lê como limpeza e cuidado clínico", "reads as clean and clinical care"),
    (196.0, 226.0, "azul clínico", "clinical blue", "lê como confiança e método", "reads as trust and method"),
    (226.0, 261.0, "azul profundo", "deep blue", "lê como autoridade serena", "reads as calm authority"),
    (261.0, 296.0, "violeta", "violet", "lê como transformação", "reads as transformation"),
    (296.0, 326.0, "magenta", "magenta", "lê como energia e desejo", "reads as energy and desire"),
    (326.0, 350.0, "rosa antigo", "dusty rose", "lê como pele e cuidado íntimo", "reads as skin and intimate care"),
)

# Direções por vertical: matiz com significado no mercado + o preset que empresta o perfil de
# claridade, a tipografia e a forma. Quatro por vertical, três entram em cada rodada.
VERTICALS = {
    "supplements": ((158.0, "apothecary-calm"), (26.0, "warm-lifestyle"), (206.0, "modern-clean"), (96.0, "atelier-document")),
    "health": ((202.0, "modern-clean"), (168.0, "apothecary-calm"), (12.0, "bold-editorial"), (232.0, "tech-sharp")),
    "beauty": ((338.0, "premium-minimal"), (24.0, "warm-lifestyle"), (276.0, "luxe-magazine"), (186.0, "modern-clean")),
    "home": ((30.0, "warm-lifestyle"), (88.0, "atelier-document"), (206.0, "modern-clean"), (350.0, "bold-editorial")),
    "relationship": ((348.0, "bold-editorial"), (40.0, "warm-lifestyle"), (284.0, "luxe-magazine"), (160.0, "apothecary-calm")),
    "other": ((222.0, "modern-clean"), (152.0, "apothecary-calm"), (22.0, "bold-editorial"), (268.0, "premium-minimal")),
}

SKEPTICISM = {
    "baixo": {
        "primary_s": 0.68, "accent_s": 0.58,
        "pt-BR": "num tom convidativo, porque o mercado ainda não está armado contra promessa",
        "en": "in an inviting tone, because the market is not yet armed against promises",
    },
    "médio": {
        "primary_s": 0.62, "accent_s": 0.50,
        "pt-BR": "com calor suficiente pra não parecer laboratório",
        "en": "warm enough not to look like a lab",
    },
    "alto": {
        "primary_s": 0.52, "accent_s": 0.44,
        "pt-BR": "num tom sóbrio, pra quem já testou de tudo e desconfia",
        "en": "in a sober tone, for someone who tried everything and distrusts it",
    },
}
SKEPTICISM_ALIASES = {"low": "baixo", "medium": "médio", "medio": "médio", "high": "alto", "média": "médio", "media": "médio"}

# Claridade dos neutros quando o tema pedido é o contrário do tema do preset. O preset continua
# emprestando a saturação, o matiz vem da direção, e o contraste é corrigido depois.
MIRROR_L = {
    True: {"background": 0.08, "surface": 0.13, "foreground": 0.93, "border": 0.22, "muted": 0.62},
    False: {"background": 0.97, "surface": 0.94, "foreground": 0.12, "border": 0.88, "muted": 0.45},
}

NEUTRAL_S_CAP = {"background": 0.10, "surface": 0.16, "foreground": 0.18, "border": 0.16, "muted": 0.16}
NEUTRAL_S_MIN = {"background": 0.04, "surface": 0.06, "foreground": 0.06, "border": 0.05, "muted": 0.05}


# ---------------------------------------------------------------- cor, matemática pura

def clamp(value, low, high):
    return max(low, min(high, value))


def hex_to_rgb(value):
    value = value.strip()
    if not HEX_RE.match(value):
        raise ValueError(f"hex inválido: {value!r}")
    v = value.lstrip("#")
    return (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16))


def rgb_to_hex(rgb):
    return "#%02X%02X%02X" % tuple(int(round(clamp(c, 0, 255))) for c in rgb)


def rgb_to_hsl(rgb):
    r, g, b = (c / 255.0 for c in rgb)
    high, low = max(r, g, b), min(r, g, b)
    light = (high + low) / 2.0
    if high == low:
        return (0.0, 0.0, light)
    delta = high - low
    sat = delta / (2.0 - high - low) if light > 0.5 else delta / (high + low)
    if high == r:
        hue = ((g - b) / delta) % 6.0
    elif high == g:
        hue = (b - r) / delta + 2.0
    else:
        hue = (r - g) / delta + 4.0
    return (hue * 60.0 % 360.0, sat, light)


def hsl_to_rgb(hue, sat, light):
    hue = hue % 360.0
    sat = clamp(sat, 0.0, 1.0)
    light = clamp(light, 0.0, 1.0)
    c = (1.0 - abs(2.0 * light - 1.0)) * sat
    x = c * (1.0 - abs((hue / 60.0) % 2.0 - 1.0))
    m = light - c / 2.0
    idx = int(hue // 60.0) % 6
    r, g, b = ((c, x, 0.0), (x, c, 0.0), (0.0, c, x), (0.0, x, c), (x, 0.0, c), (c, 0.0, x))[idx]
    return ((r + m) * 255.0, (g + m) * 255.0, (b + m) * 255.0)


def hsl_to_hex(hue, sat, light):
    return rgb_to_hex(hsl_to_rgb(hue, sat, light))


def hex_to_hsl(value):
    return rgb_to_hsl(hex_to_rgb(value))


def relative_luminance(value):
    out = []
    for c in hex_to_rgb(value):
        c = c / 255.0
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def contrast_ratio(a, b):
    la, lb = relative_luminance(a), relative_luminance(b)
    high, low = max(la, lb), min(la, lb)
    return (high + 0.05) / (low + 0.05)


def hue_delta(a, b):
    """Distância circular entre dois matizes, de 0 a 180 graus."""
    d = abs((a % 360.0) - (b % 360.0)) % 360.0
    return 360.0 - d if d > 180.0 else d


def hue_family(hue, lang="pt-BR"):
    hue = hue % 360.0
    for start, end, label_pt, label_en, reads_pt, reads_en in HUE_FAMILIES:
        inside = (start <= hue < end) if start < end else (hue >= start or hue < end)
        if inside:
            return {
                "label": label_pt if lang == "pt-BR" else label_en,
                "reads_as": reads_pt if lang == "pt-BR" else reads_en,
            }
    return {"label": "neutro" if lang == "pt-BR" else "neutral", "reads_as": "" }


def rgb_triplet(value):
    """Formato do sistema de tokens da comparadora: `246,245,241`."""
    return ",".join(str(c) for c in hex_to_rgb(value))


# ---------------------------------------------------------------- montagem de uma paleta

def load_presets(path=None):
    data = json.loads(Path(path or PRESETS_FILE).read_text(encoding="utf-8"))
    return data["presets"]


def preset_profile(preset):
    """Extrai de um preset o perfil de claridade e saturação por role, e se o tema é escuro."""
    profile = {}
    for role, value in preset["palette"].items():
        hue, sat, light = hex_to_hsl(value)
        profile[role] = {"s": sat, "l": light}
    return profile, profile["background"]["l"] < 0.5


def _tune(hue, sat, light, measure, target, prefer_down, low=0.03, high=0.99, step=0.01):
    """Anda com a claridade até o contraste medido bater o alvo. Determinístico: primeiro no
    sentido preferido, depois no contrário. Devolve (hex, razão) do melhor que encontrou."""
    best = None
    for direction in ((-1, 1) if prefer_down else (1, -1)):
        current = light
        for _ in range(int((high - low) / step) + 2):
            value = hsl_to_hex(hue, sat, current)
            ratio = measure(value)
            if best is None or ratio > best[1]:
                best = (value, ratio)
            if ratio >= target:
                return value, ratio
            current += direction * step
            if current < low or current > high:
                break
    return best


def _tune_window(hue, sat, light, background, low_target, high_target, prefer_down):
    """Coloca a cor dentro de uma FAIXA de contraste contra o fundo. Só com o piso, uma cor de
    apoio de matiz naturalmente escuro (azul, violeta) para em 13:1 e vira uma segunda tinta em
    vez de cor de apoio; o teto puxa ela de volta pra ser vista como cor."""
    value = hsl_to_hex(hue, sat, light)
    ratio = contrast_ratio(value, background)
    if ratio < low_target:
        return _tune(hue, sat, light, lambda v: contrast_ratio(v, background), low_target, prefer_down)
    if ratio <= high_target:
        return value, ratio
    direction = 1 if prefer_down else -1   # em fundo claro, clarear a cor baixa o contraste
    current = light
    best = (value, ratio)
    for _ in range(90):
        current += direction * 0.01
        if not 0.03 <= current <= 0.99:
            break
        candidate = hsl_to_hex(hue, sat, current)
        candidate_ratio = contrast_ratio(candidate, background)
        if candidate_ratio < low_target:
            break
        best = (candidate, candidate_ratio)
        if candidate_ratio <= high_target:
            break
    return best


def _make_primary(hue, sat, light, dark):
    """Devolve (primary, on_primary, razão). O texto do botão sai da própria paleta: papel
    tingido, branco puro, tinta tingida ou preto quase absoluto.

    Duas passadas. A primeira persegue o padrão do mercado (botão escuro com texto claro no tema
    claro, e o inverso no tema escuro), movendo a claridade no máximo 0.26 pra
    não trocar de família. A segunda é a rede de segurança, com a busca aberta nos dois
    sentidos."""
    paper = hsl_to_hex(hue, 0.08, 0.98)
    ink = hsl_to_hex(hue, 0.14, 0.09)
    light_text = (paper, "#FFFFFF")
    dark_text = (ink, "#0B0B0C")
    # dourado, âmbar, mostarda e verde-limão só aceitam texto claro virando marrom: nessa faixa
    # o certo é o contrário, botão claro com texto escuro
    keeps_family = not (YELLOW_BAND[0] <= hue % 360.0 < YELLOW_BAND[1])
    first, second = (light_text, dark_text) if (keeps_family and not dark) else (dark_text, light_text)

    step = -0.02 if first is light_text else 0.02
    for i in range(14):
        candidate = hsl_to_hex(hue, sat, clamp(light + step * i, 0.12, 0.88))
        for option in first:
            ratio = contrast_ratio(option, candidate)
            if ratio >= CONTRAST_AA:
                return candidate, option, ratio

    deltas = [0.0]
    for i in range(1, 26):
        deltas.extend([0.02 * i, -0.02 * i] if step > 0 else [-0.02 * i, 0.02 * i])
    for delta in deltas:
        candidate = hsl_to_hex(hue, sat, clamp(light + delta, 0.12, 0.88))
        for option in second + first:
            ratio = contrast_ratio(option, candidate)
            if ratio >= CONTRAST_AA:
                return candidate, option, ratio
    return None, None, 0.0


def build_palette(hue, harmony, sign, preset, tuning, dark_override=None):
    """Monta uma paleta completa: neutros tingidos no matiz da cor principal, `primary` no matiz
    da direção, `accent` no matiz que a relação declarada manda, e todo contraste corrigido."""
    profile, dark = preset_profile(preset)
    mirror = None
    if dark_override is not None and dark_override != dark:
        dark, mirror = dark_override, MIRROR_L[dark_override]
    palette = {}

    for role in NEUTRAL_ROLES:
        sat = clamp(max(profile[role]["s"], NEUTRAL_S_MIN[role]), NEUTRAL_S_MIN[role], NEUTRAL_S_CAP[role])
        light = mirror[role] if mirror else profile[role]["l"]
        palette[role] = hsl_to_hex(hue, sat, light)

    # texto e texto secundário precisam de AA contra o fundo E contra a superfície: o texto
    # secundário vive dentro de cartão (oferta, FAQ, prova), não só sobre o fundo
    bg, surface = palette["background"], palette["surface"]
    for role in ("foreground", "muted"):
        sat, light = clamp(max(profile[role]["s"], NEUTRAL_S_MIN[role]), 0.0, NEUTRAL_S_CAP[role]), hex_to_hsl(palette[role])[2]
        tuned = _tune(hue, sat, light,
                      lambda value: min(contrast_ratio(value, bg), contrast_ratio(value, surface)),
                      CONTRAST_AA, prefer_down=not dark)
        palette[role] = tuned[0]

    primary_s = clamp(max(profile["primary"]["s"], tuning["primary_s"]), SATURATION_FLOOR + 0.08, 0.92)
    primary_l = clamp(profile["primary"]["l"], 0.30, 0.52) if not dark else clamp(max(profile["primary"]["l"], 0.46), 0.46, 0.70)
    primary, on_primary, _ = _make_primary(hue, primary_s, primary_l, dark)
    if primary is None:
        return None
    palette["primary"], palette["on_primary"] = primary, on_primary

    accent_hue = (hue + sign * HARMONY_OFFSET[harmony]) % 360.0
    accent_s = clamp(max(profile["accent"]["s"], tuning["accent_s"]), SATURATION_FLOOR + 0.08, 0.92)
    accent_l = clamp(profile["accent"]["l"], 0.34, 0.56) if not dark else clamp(max(profile["accent"]["l"], 0.48), 0.48, 0.72)
    palette["accent"] = _tune_window(accent_hue, accent_s, accent_l, bg, CONTRAST_GRAPHIC, ACCENT_CONTRAST_CEILING, prefer_down=not dark)[0]

    # a borda fica entre a superfície e o texto secundário, sem exigência de contraste
    border_l = hex_to_hsl(palette["surface"])[2]
    palette["border"] = hsl_to_hex(hue, NEUTRAL_S_CAP["border"] * 0.8, clamp(border_l - 0.06 if not dark else border_l + 0.08, 0.03, 0.99))

    return {role: palette[role] for role in ROLES}


# ---------------------------------------------------------------- validação

def validate_palette(entry):
    """Devolve a lista de falhas de uma candidata. Lista vazia = paleta entregável."""
    fails = []
    palette = entry.get("palette") or {}
    missing = [role for role in ROLES if not HEX_RE.match(str(palette.get(role, "")))]
    if missing:
        return [f"roles ausentes ou com hex inválido: {', '.join(missing)}"]

    for role in ("primary", "accent"):
        sat = hex_to_hsl(palette[role])[1]
        if sat < SATURATION_FLOOR:
            fails.append(f"{role} com saturação {sat:.2f}, abaixo do piso de {SATURATION_FLOOR:.2f} (lê como cinza)")

    harmony = entry.get("harmony")
    if harmony not in HARMONY_RANGE:
        fails.append(f"relação de matiz não declarada ou desconhecida: {harmony!r}")
    else:
        low, high = HARMONY_RANGE[harmony]
        delta = hue_delta(hex_to_hsl(palette["primary"])[0], hex_to_hsl(palette["accent"])[0])
        if not low <= delta <= high:
            fails.append(f"harmonia declarada {harmony} pede de {low:.0f} a {high:.0f} graus, e a paleta tem {delta:.0f}")

    checks = (
        ("foreground", "background", CONTRAST_AA),
        ("on_primary", "primary", CONTRAST_AA),
        ("muted", "background", CONTRAST_AA),
        ("foreground", "surface", CONTRAST_AA),
        ("muted", "surface", CONTRAST_AA),
        ("accent", "background", CONTRAST_GRAPHIC),
    )
    for front, back, target in checks:
        ratio = contrast_ratio(palette[front], palette[back])
        if ratio < target:
            fails.append(f"contraste {front}/{back} em {ratio:.2f}:1, abaixo de {target:.1f}:1")
    return fails


def validate_set(entries):
    """Falhas do conjunto: quantidade e distância de matiz entre os `primary`."""
    fails = []
    if len(entries) != PALETTE_COUNT:
        fails.append(f"o conjunto tem {len(entries)} paletas, e são sempre {PALETTE_COUNT}")
    hues = [hex_to_hsl(e["palette"]["primary"])[0] for e in entries if e.get("palette", {}).get("primary")]
    for i in range(len(hues)):
        for j in range(i + 1, len(hues)):
            delta = hue_delta(hues[i], hues[j])
            if delta < MIN_HUE_SPREAD:
                fails.append(
                    f"paletas {i + 1} e {j + 1} com matiz de primary a {delta:.0f} graus, "
                    f"abaixo dos {MIN_HUE_SPREAD:.0f} que separam uma cor da outra"
                )
    return fails


# ---------------------------------------------------------------- geração

def _digest(*parts):
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).digest()


def _spread(hues, minimum=MIN_HUE_SPREAD + SPREAD_MARGIN):
    """Afasta matizes que ficaram perto demais, sempre pro mesmo lado, pra saída seguir igual.

    A margem existe porque o matiz final é medido no hex já arredondado pra 8 bits e já corrigido
    na claridade: separar exatamente no piso deixaria o conjunto reprovando por meio grau."""
    out = list(hues)
    for i in range(1, len(out)):
        for _ in range(72):
            if all(hue_delta(out[i], out[j]) >= minimum for j in range(i)):
                break
            out[i] = (out[i] + 5.0) % 360.0
    return out


SMALL_WORDS = ("de", "da", "do", "com", "e", "of", "with", "and")


def _titlecase(text):
    words = text.split()
    out = [w if i and w.lower() in SMALL_WORDS else w[:1].upper() + w[1:] for i, w in enumerate(words)]
    return " ".join(out)


def _name_for(primary_hue, accent_hue, lang, taken):
    name = _titlecase(hue_family(primary_hue, lang)["label"])
    if name in taken:
        accent = _titlecase(hue_family(accent_hue, lang)["label"])
        name = f"{name} com {accent}" if lang == "pt-BR" else f"{name} with {accent}"
    return name


def _why(primary_hue, accent_hue, lang, tuning, avatar):
    primary = hue_family(primary_hue, lang)
    accent = hue_family(accent_hue, lang)
    if lang == "pt-BR":
        head = f"{primary['label'].capitalize()} com {accent['label']} de apoio."
        tail = f"{primary['reads_as'].capitalize()}, {tuning['pt-BR']}"
        if avatar:
            tail += f", pra {avatar}"
    else:
        head = f"{primary['label'].capitalize()} with {accent['label']} in support."
        tail = f"{primary['reads_as'].capitalize()}, {tuning['en']}"
        if avatar:
            tail += f", for {avatar}"
    return f"{head} {tail}."


def generate(vertical, avatar="", skepticism="médio", seeds=(), lang="pt-BR", theme="auto", presets=None):
    """Devolve o dicionário com as 3 candidatas válidas. Levanta RuntimeError se não convergir."""
    if vertical not in VERTICALS:
        raise ValueError(f"vertical desconhecida: {vertical!r}")
    skepticism = SKEPTICISM_ALIASES.get(skepticism, skepticism)
    if skepticism not in SKEPTICISM:
        raise ValueError(f"ceticismo desconhecido: {skepticism!r}")
    if lang not in ("pt-BR", "en"):
        raise ValueError(f"idioma desconhecido: {lang!r}")
    presets = presets or load_presets()
    tuning = SKEPTICISM[skepticism]

    seeds = [s.strip().upper() for s in seeds if s and HEX_RE.match(s.strip())]
    digest = _digest(vertical, avatar, skepticism, ",".join(seeds), lang, theme)

    directions = VERTICALS[vertical]
    start = digest[0] % len(directions)
    chosen = [directions[(start + i) % len(directions)] for i in range(PALETTE_COUNT)]
    hues = [float(h) for h, _ in chosen]

    # a cor da marca ou da referência manda na primeira candidata, desde que tenha cor de verdade
    # (um off-white de fundo não define matiz nenhum)
    anchor = None
    if seeds:
        candidate = max(seeds, key=lambda value: hex_to_hsl(value)[1])
        if hex_to_hsl(candidate)[1] >= 0.12:
            anchor = candidate
            hues[0] = hex_to_hsl(candidate)[0]
    hues = _spread(hues)

    harmony_start = digest[1] % len(HARMONY_ORDER)
    dark_override = {"light": False, "dark": True}.get(theme)

    entries, taken = [], []
    for index, hue in enumerate(hues):
        preset_key = chosen[index][1]
        harmony = HARMONY_ORDER[(harmony_start + index) % len(HARMONY_ORDER)]
        sign = 1.0 if (digest[2] >> index) & 1 else -1.0
        preset = presets[preset_key]
        palette = build_palette(hue, harmony, sign, preset, tuning, dark_override)
        if palette is None:
            raise RuntimeError(f"não foi possível fechar a paleta {index + 1} com contraste AA")
        accent_hue = hex_to_hsl(palette["accent"])[0]
        name = _name_for(hue, accent_hue, lang, taken)
        taken.append(name)
        entry = {
            "id": f"p{index + 1}",
            "name": name,
            "why": _why(hue, accent_hue, lang, tuning, avatar),
            "harmony": harmony,
            "harmony_label": HARMONY_LABEL[harmony][lang],
            "base_preset": preset_key,
            "hue": {"primary": round(hue % 360.0, 1), "accent": round(accent_hue, 1)},
            "palette": palette,
            "tokens_rgb": {role: rgb_triplet(value) for role, value in palette.items()},
            "contrast": {
                "foreground_on_background": round(contrast_ratio(palette["foreground"], palette["background"]), 2),
                "on_primary_on_primary": round(contrast_ratio(palette["on_primary"], palette["primary"]), 2),
                "muted_on_background": round(contrast_ratio(palette["muted"], palette["background"]), 2),
                "accent_on_background": round(contrast_ratio(palette["accent"], palette["background"]), 2),
            },
            "non_color_tokens": {
                "heading_font": preset["heading_font"],
                "body_font": preset["body_font"],
                "google_fonts": preset["google_fonts"],
                "radius": preset["radius"],
                "shadow": preset["shadow"],
                "density": preset["density"],
            },
        }
        fails = validate_palette(entry)
        if fails:
            raise RuntimeError(f"paleta {index + 1} ({name}) não passou: " + "; ".join(fails))
        entries.append(entry)

    fails = validate_set(entries)
    if fails:
        raise RuntimeError("conjunto não passou: " + "; ".join(fails))

    return {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "input": {
            "vertical": vertical,
            "avatar": avatar,
            "skepticism": skepticism,
            "seeds": seeds,
            "anchor": anchor,
            "lang": lang,
            "theme": theme,
        },
        "rules": {
            "saturation_floor": SATURATION_FLOOR,
            "contrast_text": CONTRAST_AA,
            "contrast_graphic": CONTRAST_GRAPHIC,
            "min_hue_spread_deg": MIN_HUE_SPREAD,
        },
        "palettes": entries,
    }


# ---------------------------------------------------------------- saída

def render_md(result):
    lang = result["input"]["lang"]
    pt = lang == "pt-BR"
    head = "Paletas candidatas" if pt else "Candidate palettes"
    lines = [
        f"# {head}",
        "",
        (f"Vertical **{result['input']['vertical']}** · ceticismo **{result['input']['skepticism']}**"
         if pt else
         f"Vertical **{result['input']['vertical']}** · skepticism **{result['input']['skepticism']}**"),
        "",
    ]
    for entry in result["palettes"]:
        lines.append(f"## {entry['id'].upper()} · {entry['name']}")
        lines.append("")
        lines.append(entry["why"])
        lines.append("")
        lines.append((f"Relação de matiz: {entry['harmony_label']}. Base: preset `{entry['base_preset']}`."
                      if pt else
                      f"Hue relation: {entry['harmony_label']}. Base: preset `{entry['base_preset']}`."))
        lines.append("")
        lines.append("| role | hex | r,g,b |")
        lines.append("|---|---|---|")
        for role in ROLES:
            lines.append(f"| `{role}` | `{entry['palette'][role]}` | `{entry['tokens_rgb'][role]}` |")
        lines.append("")
        c = entry["contrast"]
        lines.append(
            (f"Contraste: texto/fundo {c['foreground_on_background']}:1 · texto do botão/botão "
             f"{c['on_primary_on_primary']}:1 · texto secundário/fundo {c['muted_on_background']}:1 · "
             f"apoio/fundo {c['accent_on_background']}:1"
             if pt else
             f"Contrast: text/background {c['foreground_on_background']}:1 · button text/button "
             f"{c['on_primary_on_primary']}:1 · secondary text/background {c['muted_on_background']}:1 · "
             f"accent/background {c['accent_on_background']}:1"))
        lines.append("")
        n = entry["non_color_tokens"]
        lines.append(
            (f"Tokens que vêm do preset: títulos {n['heading_font']}, corpo {n['body_font']}, "
             f"radius {n['radius']['base_px']}px, shadow {n['shadow']}, density {n['density']}."
             if pt else
             f"Tokens inherited from the preset: headings {n['heading_font']}, body {n['body_font']}, "
             f"radius {n['radius']['base_px']}px, shadow {n['shadow']}, density {n['density']}."))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_css(result):
    """Blocos de token da comparadora: um por candidata, cor em trio R,G,B."""
    out = []
    for entry in result["palettes"]:
        out.append(f"/* {entry['id']} · {entry['name']} */")
        out.append(f"[data-palette=\"{entry['id']}\"] {{")
        for role in ROLES:
            out.append(f"  --tk-{role.replace('_', '-')}: {entry['tokens_rgb'][role]};")
        out.append("}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="3 paletas candidatas com motivo, a partir dos 8 presets.")
    parser.add_argument("--vertical", required=True, choices=sorted(VERTICALS))
    parser.add_argument("--avatar", default="")
    parser.add_argument("--skepticism", default="médio")
    parser.add_argument("--seed", default="")
    parser.add_argument("--signals", default="")
    parser.add_argument("--lang", default="pt-BR", choices=("pt-BR", "en"))
    parser.add_argument("--theme", default="auto", choices=("auto", "light", "dark"))
    parser.add_argument("--format", dest="fmt", default="md", choices=("md", "json", "css"))
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)

    seeds = [s for s in args.seed.split(",") if s.strip()]
    if args.signals:
        path = Path(args.signals)
        if not path.exists():
            print(f"erro: arquivo de signals não encontrado: {path}", file=sys.stderr)
            return 1
        try:
            palette = json.loads(path.read_text(encoding="utf-8")).get("palette") or {}
        except json.JSONDecodeError as exc:
            print(f"erro: signals inválido ({exc})", file=sys.stderr)
            return 1
        seeds.extend(str(v) for v in palette.values())

    try:
        result = generate(args.vertical, args.avatar, args.skepticism, seeds, args.lang, args.theme)
    except ValueError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3

    text = {"md": render_md, "css": render_css}.get(args.fmt, lambda r: json.dumps(r, ensure_ascii=False, indent=2) + "\n")(result)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"salvo em {args.out}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

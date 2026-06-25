#!/usr/bin/env python3
"""
design_canon.py — Aplica uma DISCIPLINA de design a QUALQUER design system e emite tokens.

Modelo central: disciplina ⊥ marca.

  DISCIPLINA (preset)  = o método. Razão da escala de tipo, set de grids, pesos de régua,
                         regras de alinhamento, semântica da cor (identificador vs. livre),
                         estratégia de face/fallback. É a régua.
  MARCA (input)        = os valores. Paleta, fontes, tamanho base. Entra por --config (JSON)
                         e/ou flags (--primary, --base, --face). É o conteúdo.

Você renderiza os valores da SUA marca ATRAVÉS de uma disciplina escolhida. Vignelli é só um
preset; `blank` é passthrough sem opiniões; `swiss` é o estilo tipográfico internacional.

Determinístico — zero rede, zero credencial. Os presets vivem embutidos aqui (fonte de verdade),
então o gerador roda mesmo sem nenhum arquivo de referência carregado.

USO:
  python3 design_canon.py                                   # preset blank, CSS, base 16px
  python3 design_canon.py --preset vignelli                 # a disciplina Vignelli, defaults dela
  python3 design_canon.py --preset vignelli --primary "#0039A6"   # troca só a cor identificadora
  python3 design_canon.py --config ds.json --format tailwind      # SEU DS no @theme do Tailwind v4
  python3 design_canon.py --config ds.json --preset swiss --format style-dictionary
  python3 design_canon.py --format w3c                      # W3C Design Tokens (design-tokens.org)
  python3 design_canon.py --preset vignelli --grid 4x8      # mapa coluna x módulo de um grid
  python3 design_canon.py --preset vignelli --signage       # tabela de painéis (só presets com signage)
  python3 design_canon.py --list-presets

Formatos: css (default) | scss | tailwind | json | w3c | style-dictionary

NOTA DE RENDER (regra dura, generalizada do Vignelli Canon): a house face de uma grotesca não
existe na maioria dos ambientes headless. Ao rasterizar SVG/HTML (cairosvg, Chromium headless) ou
alimentar arte num modelo de imagem com uma pilha tipo `Helvetica`/`Arial`/`sans-serif`, o renderer
cai silenciosamente para Noto Sans (lê como Calibri) e quebra a grotesca. Por isso o engine ANEXA
um fallback de métrica compatível instalado ('Liberation Sans' antes de Arial e do genérico) a toda
família sans. Confirme com `fc-match` no ambiente antes de publicar. Sempre confira um render.
"""

import argparse, json, sys

# Fallbacks de rasterização por classe de fonte (métrica compatível, geralmente instalados).
RASTER_FALLBACK = {
    "sans":  ["Liberation Sans", "Arial", "sans-serif"],
    "serif": ["Liberation Serif", "Georgia", "serif"],
    "mono":  ["Liberation Mono", "Menlo", "monospace"],
}

# --- PRESETS (disciplinas embutidas) ----------------------------------------
# Cada preset é uma DISCIPLINA: define a estrutura, não os valores da marca. Os valores da marca
# (paleta, fontes, base) preenchem os slots. A marca pode sobrescrever tudo; o preset garante o
# método (quais degraus de tipo existem, grids, réguas, alinhamento, semântica de cor, fallback).

PRESETS = {
    # ---- blank: passthrough sem opiniões. O caminho "qualquer DS" ----------
    "blank": {
        "label": "Blank (passthrough sem opiniões)",
        "prefix": "ds",
        "color_semantics": "free",      # paleta livre, sem aviso de diluição
        "max_type_sizes": None,         # sem limite doutrinário
        "type_steps": {                 # escala modular padrão (~1.25), em múltiplos do body
            "xs": 0.64, "sm": 0.8, "base": 1.0, "lg": 1.25,
            "xl": 1.563, "2xl": 1.953, "3xl": 2.441, "4xl": 3.052,
        },
        "leading": {"body": 1.5, "heading": 1.15},
        "grids": {"12col": (12, 1), "8col": (8, 1), "4col": (4, 1)},
        "rulers_pt": None,              # régua é um Vignelli-ismo; blank não impõe
        "alignment": {"default": "left", "justify_allowed": True, "center": "free"},
        "default_palette": {"primary": "#2D2D2D", "bg": "#FFFFFF", "fg": "#111111"},
        "default_fonts": {"sans": "Inter", "serif": "Georgia", "mono": "ui-monospace"},
        "rules": [
            "Sem disciplina imposta — os valores da marca passam direto pra tokens.",
            "Use quando você só quer normalizar um DS existente em tokens multi-formato.",
        ],
        "signage": None,
    },

    # ---- vignelli: o Canon, preservado como preset showcase ----------------
    "vignelli": {
        "label": "Vignelli Canon",
        "prefix": "v",
        "color_semantics": "identifier",   # cor identifica, nunca enfeita; 1 por linha/sistema
        "max_type_sizes": 2,               # dois tamanhos vivos por página; heading ~2x body
        "type_steps": {
            "caption": 0.75, "body": 1.0, "lead": 1.5,
            "heading": 2.0, "display": 4.0, "mega": 8.0,
        },
        "leading": {"body": 1.2, "heading": 1.05},
        "grids": {"2x4": (2, 4), "5x4": (5, 4), "3x6": (3, 6), "6x6": (6, 6), "4x8": (4, 8)},
        "rulers_pt": {"major": 2.0, "minor": 1.0, "hair": 0.5},
        "alignment": {"default": "left", "justify_allowed": False, "center": "lapidary-only"},
        "default_palette": {
            "primary": "#F04E23",   # vermilion da capa do Canon — identificador
            "blue":    "#0039A6",   # signal blue metrô NYC / Grandi Stazioni
            "yellow":  "#FFCC00",   # signal yellow
            "ink":     "#0A0A0A",
            "paper":   "#F4F1EA",
            "white":   "#FFFFFF",
        },
        "default_fonts": {"sans": "Helvetica Neue, Helvetica", "serif": "Times", "mono": "monospace"},
        "rules": [
            "Procure o significado antes da forma (semântica primeiro).",
            "Máximo dois tamanhos de tipo por página; o heading é ~2x o body. O resto é peso.",
            "Flush left, nunca justificado. Centralizado só para texto lapidar.",
            "Cor é identificador, não decoração — uma cor por linha/sistema.",
            "O branco faz o preto cantar — proteja o silêncio.",
            "Se você consegue ver o layout, é um layout ruim.",
        ],
        "signage": {
            "id_color_key": "blue", "text_color_key": "white",
            "panels": [
                ("Identificacao de estacao (predio)", 600, 100, "Cap height 100mm, iluminado internamente"),
                ("Direcional (suspenso)",             300, 75,  "Seta compartilha a cap box; flush left"),
                ("Informacao / regulatorio",          150, 25,  "Pendura numa regua de 2pt"),
                ("Numero de plataforma (bandeira)",   250, 250, "Numeral num quadrado, dupla face"),
            ],
        },
    },

    # ---- swiss: International Typographic Style -----------------------------
    "swiss": {
        "label": "Swiss / International Typographic Style",
        "prefix": "sw",
        "color_semantics": "identifier",
        "max_type_sizes": 3,
        "type_steps": {
            "caption": 0.694, "body": 1.0, "sub": 1.2,
            "heading": 1.728, "display": 2.986, "mega": 5.16,
        },
        "leading": {"body": 1.5, "heading": 1.1},
        "grids": {"3col": (3, 1), "4col": (4, 1), "6col": (6, 1), "12col": (12, 1)},
        "rulers_pt": {"major": 1.0, "minor": 0.5, "hair": 0.25},
        "alignment": {"default": "left", "justify_allowed": False, "center": "free"},
        "default_palette": {"primary": "#E2231A", "ink": "#111111", "paper": "#FFFFFF"},
        "default_fonts": {"sans": "Helvetica Neue, Akzidenz-Grotesk", "serif": "Times", "mono": "monospace"},
        "rules": [
            "Grade matemática é a estrutura; objetividade acima da expressão.",
            "Flush left (rag right), nunca justificado.",
            "Escala modular consistente; máximo três tamanhos vivos.",
            "Cor é identificador funcional.",
        ],
        "signage": None,
    },
}


# --- Resolução: disciplina + marca ------------------------------------------

def load_brand(config_path, primary, base, face, prefix):
    """Lê o config da marca (se houver) e aplica overrides de flag por cima."""
    brand = {"name": None, "base_px": None, "palette": {}, "fonts": {}, "prefix": None}
    if config_path:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        brand["name"] = data.get("name")
        brand["base_px"] = data.get("base_px")
        brand["palette"] = dict(data.get("palette", {}))
        brand["fonts"] = dict(data.get("fonts", {}))
        brand["prefix"] = data.get("prefix")
    if primary:
        brand["palette"]["primary"] = primary
    if base:
        brand["base_px"] = base
    if face:
        brand["fonts"]["sans"] = face
    if prefix:
        brand["prefix"] = prefix
    return brand


def resolve(preset_name, brand):
    """Funde disciplina (estrutura) + marca (valores). Emite (resolved, warnings)."""
    if preset_name not in PRESETS:
        raise SystemExit(f"Preset '{preset_name}' desconhecido. Opções: {', '.join(PRESETS)}")
    d = PRESETS[preset_name]
    warnings = []

    base = brand["base_px"] or 16.0
    prefix = brand["prefix"] or d["prefix"]
    palette = dict(d["default_palette"]); palette.update(brand["palette"])
    fonts = dict(d["default_fonts"]); fonts.update(brand["fonts"])

    # Escala de tipo: degraus da disciplina x base da marca.
    type_scale = {k: round(base * mult, 2) for k, mult in d["type_steps"].items()}

    # Aviso de disciplina: cor como identificador é diluída por paletas grandes.
    if d["color_semantics"] == "identifier":
        accent_like = [k for k in palette if k not in ("ink", "paper", "white", "bg", "fg")]
        if len(accent_like) > 3:
            warnings.append(
                f"disciplina '{preset_name}' trata cor como IDENTIFICADOR (uma por linha/sistema); "
                f"a paleta tem {len(accent_like)} cores de acento — risco de virar decoração.")

    # Aviso de disciplina: limite de tamanhos vivos por página.
    if d["max_type_sizes"]:
        warnings.append(
            f"disciplina '{preset_name}': use no máximo {d['max_type_sizes']} tamanho(s) de tipo "
            f"VIVO(s) por página (ex.: body + heading); os demais degraus são para capas/specs.")

    return {
        "preset": preset_name, "label": d["label"], "prefix": prefix,
        "base_px": base, "palette": palette, "fonts": fonts,
        "type_scale": type_scale, "leading": d["leading"],
        "grids": d["grids"], "rulers_pt": d["rulers_pt"], "alignment": d["alignment"],
        "rules": d["rules"], "signage": d["signage"], "brand_name": brand["name"],
    }, warnings


GENERIC_FAMILIES = {"serif", "sans-serif", "monospace", "ui-monospace",
                    "ui-sans-serif", "ui-serif", "system-ui", "cursive", "fantasy"}


def font_stack(family, klass):
    """Anexa fallbacks de métrica compatível para sobreviver a render headless.
    Famílias com espaço são aspeadas; keywords genéricas (sans-serif…) vão pro fim."""
    names = [f.strip() for f in str(family).split(",") if f.strip()]
    names += RASTER_FALLBACK.get(klass, ["sans-serif"])
    specific, generic, seen = [], [], set()
    for f in names:
        if f in seen:
            continue
        seen.add(f)
        if f.lower() in GENERIC_FAMILIES:
            generic.append(f.lower())
        else:
            specific.append(f"'{f}'" if (" " in f or "-" in f) else f)
    return ", ".join(specific + generic)


# --- Emissores ---------------------------------------------------------------

def emit_css(r):
    p = r["prefix"]; L = [f":root {{",
        f"  /* design-canon — disciplina '{r['preset']}' aplicada"
        + (f" a {r['brand_name']}" if r['brand_name'] else "") + " */"]
    for k, v in r["palette"].items():
        L.append(f"  --{p}-color-{k}: {v};")
    L.append("")
    for k, klass in (("sans", "sans"), ("serif", "serif"), ("mono", "mono")):
        if r["fonts"].get(k):
            L.append(f"  --{p}-font-{k}: {font_stack(r['fonts'][k], klass)};")
    L.append("")
    for k, v in r["type_scale"].items():
        L.append(f"  --{p}-text-{k}: {v}px;")
    for k, v in r["leading"].items():
        L.append(f"  --{p}-leading-{k}: {v};")
    if r["rulers_pt"]:
        L.append("")
        for k, v in r["rulers_pt"].items():
            L.append(f"  --{p}-rule-{k}: {v}px;")
    L.append("}")
    if r["rulers_pt"]:
        L += ["", "/* o tipo pendura DA régua */",
              f".{p}-rule {{ border-top: var(--{p}-rule-major) solid var(--{p}-color-ink, #0A0A0A); }}"]
    if not r["alignment"]["justify_allowed"]:
        L.append(f".{p}-flush-left {{ text-align: left; }} /* default; nunca justificar */")
    L.append("")
    for name, (cols, mods) in r["grids"].items():
        L.append(f".{p}-grid-{name} {{ display:grid; grid-template-columns: repeat({cols}, 1fr); "
                 f"grid-template-rows: repeat({mods}, 1fr); gap: 1rem; }}")
    return "\n".join(L)


def emit_scss(r):
    p = r["prefix"]; L = [f"// design-canon — disciplina '{r['preset']}' (SCSS map)"]
    L.append(f"$color: (")
    for k, v in r["palette"].items():
        L.append(f"  '{k}': {v},")
    L.append(");")
    L.append("$type: (")
    for k, v in r["type_scale"].items():
        L.append(f"  '{k}': {v}px,")
    L.append(");")
    if r["rulers_pt"]:
        L.append("$rule: (")
        for k, v in r["rulers_pt"].items():
            L.append(f"  '{k}': {v}px,")
        L.append(");")
    L.append("$font: (")
    for k, klass in (("sans", "sans"), ("serif", "serif"), ("mono", "mono")):
        if r["fonts"].get(k):
            L.append(f"  '{k}': ({font_stack(r['fonts'][k], klass)}),")
    L.append(");")
    return "\n".join(L)


def emit_tailwind(r):
    """Tailwind v4 @theme — namespaces que o Tailwind reconhece pra gerar utilitários."""
    L = ["@theme {",
         f"  /* design-canon — disciplina '{r['preset']}'"
         + (f" · {r['brand_name']}" if r['brand_name'] else "") + " */"]
    for k, v in r["palette"].items():
        L.append(f"  --color-{k}: {v};")
    L.append("")
    for k, klass in (("sans", "sans"), ("serif", "serif"), ("mono", "mono")):
        if r["fonts"].get(k):
            L.append(f"  --font-{k}: {font_stack(r['fonts'][k], klass)};")
    L.append("")
    for k, v in r["type_scale"].items():
        L.append(f"  --text-{k}: {v}px;")
    L.append("}")
    return "\n".join(L)


def emit_json(r):
    payload = {
        "discipline": r["preset"], "label": r["label"], "brand": r["brand_name"],
        "base_px": r["base_px"], "prefix": r["prefix"],
        "palette": r["palette"],
        "fonts": {k: font_stack(v, k) for k, v in r["fonts"].items() if v},
        "type_scale_px": r["type_scale"], "leading": r["leading"],
        "grids": {k: {"columns": c, "modules": m} for k, (c, m) in r["grids"].items()},
        "rulers_pt": r["rulers_pt"], "alignment": r["alignment"], "rules": r["rules"],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def emit_w3c(r):
    """W3C Design Tokens (design-tokens.org): grupos com $value/$type."""
    color = {k: {"$value": v, "$type": "color"} for k, v in r["palette"].items()}
    fontSize = {k: {"$value": f"{v}px", "$type": "dimension"} for k, v in r["type_scale"].items()}
    fontFamily = {k: {"$value": font_stack(v, k).replace("'", ""), "$type": "fontFamily"}
                  for k, v in r["fonts"].items() if v}
    out = {
        "$description": f"design-canon — disciplina '{r['preset']}'",
        "color": color, "fontSize": fontSize, "fontFamily": fontFamily,
    }
    if r["rulers_pt"]:
        out["strokeWidth"] = {k: {"$value": f"{v}px", "$type": "dimension"}
                              for k, v in r["rulers_pt"].items()}
    return json.dumps(out, indent=2, ensure_ascii=False)


def emit_style_dictionary(r):
    """Config de entrada do Style Dictionary: nós aninhados com 'value'."""
    out = {
        "color": {k: {"value": v} for k, v in r["palette"].items()},
        "size": {
            "font": {k: {"value": f"{v}px"} for k, v in r["type_scale"].items()},
        },
        "font": {k: {"value": font_stack(v, k)} for k, v in r["fonts"].items() if v},
    }
    if r["rulers_pt"]:
        out["size"]["rule"] = {k: {"value": f"{v}px"} for k, v in r["rulers_pt"].items()}
    return json.dumps(out, indent=2, ensure_ascii=False)


EMITTERS = {
    "css": emit_css, "scss": emit_scss, "tailwind": emit_tailwind,
    "json": emit_json, "w3c": emit_w3c, "style-dictionary": emit_style_dictionary,
}


# --- Subcomandos auxiliares --------------------------------------------------

def print_grid(r, name):
    if name not in r["grids"]:
        print(f"Grid '{name}' nao existe na disciplina '{r['preset']}'. "
              f"Opcoes: {', '.join(r['grids'])}"); return
    cols, mods = r["grids"][name]
    print(f"{name} grid ({r['preset']}) — {cols} colunas x {mods} modulos")
    for _ in range(mods):
        print("  " + "  ".join("[]" for _ in range(cols)))


def print_signage(r):
    s = r["signage"]
    if not s:
        print(f"Disciplina '{r['preset']}' nao define sinalizacao."); return
    idc = r["palette"].get(s["id_color_key"], "#0039A6")
    txt = r["palette"].get(s["text_color_key"], "#FFFFFF")
    print(f"Sinalizacao — disciplina '{r['preset']}'")
    print(f"  Cor identificadora: {idc}   Texto/Pictogramas: {txt}")
    print(f"  {'Painel':36} {'Painel mm':>9} {'Cap mm':>7}  Nota")
    for name, panel, cap, note in s["panels"]:
        print(f"  {name:36} {panel:>9} {cap:>7}  {note}")


def main():
    ap = argparse.ArgumentParser(description="Aplica uma disciplina de design a qualquer DS e emite tokens.")
    ap.add_argument("--preset", default="blank", help=f"disciplina: {', '.join(PRESETS)}")
    ap.add_argument("--config", help="JSON do design system da marca (palette, fonts, base_px)")
    ap.add_argument("--primary", help="override da cor identificadora (hex)")
    ap.add_argument("--base", type=float, help="override do tamanho base do body em px")
    ap.add_argument("--face", help="override da house face sans")
    ap.add_argument("--prefix", help="override do namespace de token (default: o do preset)")
    ap.add_argument("--format", choices=list(EMITTERS), default="css")
    ap.add_argument("--grid", help="imprime um mapa de grid, ex.: 4x8")
    ap.add_argument("--signage", action="store_true", help="imprime a tabela de sinalizacao do preset")
    ap.add_argument("--list-presets", action="store_true", help="lista as disciplinas disponiveis")
    a = ap.parse_args()

    if a.list_presets:
        for name, d in PRESETS.items():
            print(f"{name:10} {d['label']}")
        return

    brand = load_brand(a.config, a.primary, a.base, a.face, a.prefix)
    r, warnings = resolve(a.preset, brand)

    for w in warnings:
        print(f"[aviso] {w}", file=sys.stderr)

    if a.grid:
        print_grid(r, a.grid); return
    if a.signage:
        print_signage(r); return
    print(EMITTERS[a.format](r))


if __name__ == "__main__":
    main()

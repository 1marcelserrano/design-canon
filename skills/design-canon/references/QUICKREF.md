# Design Canon — cola de uma página

**Modelo:** disciplina (preset, a régua) ⊥ marca (config/flags, os valores). Renderize SUA marca ATRAVÉS de uma disciplina.

## Comandos

```bash
python3 scripts/design_canon.py --list-presets
python3 scripts/design_canon.py --config DS.json --format tailwind      # @theme Tailwind v4
python3 scripts/design_canon.py --config DS.json --preset vignelli       # CSS, Canon
python3 scripts/design_canon.py --preset vignelli --primary "#0039A6"    # troca a cor-ID
python3 scripts/design_canon.py --config DS.json --format w3c            # W3C Design Tokens
python3 scripts/design_canon.py --config DS.json --format style-dictionary
python3 scripts/design_canon.py --preset vignelli --grid 4x8             # mapa do grid
python3 scripts/design_canon.py --preset vignelli --signage              # painéis
```

## Presets
`blank` (default, sem opiniões) · `vignelli` (Canon: cor=ID, 2 tamanhos, régua, 5 grids) · `swiss` (grade, escala modular, máx 3 tamanhos)

## Formatos
`css` · `scss` · `tailwind` (@theme) · `json` · `w3c` ($value/$type) · `style-dictionary`

## Config mínimo
```json
{ "name":"Marca", "base_px":16, "palette":{"primary":"#B4C636"}, "fonts":{"sans":"Inter Tight"} }
```

## Precedência
flag > config > default do preset

## Regras duras
1. disciplina ⊥ marca · 2. fallback de render anexado (`'Liberation Sans'` antes de Arial) · 3. genérico de fonte por último · 4. avisos → stderr · 5. determinístico · 6. cor=ID sob vignelli/swiss · 7. 2 tamanhos + flush-left + régua sob vignelli

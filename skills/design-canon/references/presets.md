# Presets (disciplinas)

Cada preset é uma **disciplina**: define a *estrutura* (método), não os *valores* da marca. Os valores entram por `--config`/flags. Os presets vivem embutidos em `scripts/design_canon.py` no dict `PRESETS` — fonte de verdade, deterministicamente carregada.

## Anatomia de um preset

```python
"nome": {
    "label": "Texto humano",
    "prefix": "ds",                 # namespace de token default (--{prefix}-...)
    "color_semantics": "identifier" | "free",   # 'identifier' avisa quando a paleta dilui
    "max_type_sizes": 2 | None,     # tamanhos VIVOS por página (doutrina; gera aviso)
    "type_steps": {"body": 1.0, "heading": 2.0, ...},   # múltiplos do base_px
    "leading": {"body": 1.2, "heading": 1.05},
    "grids": {"4x8": (4, 8), ...},  # nome -> (colunas, módulos)
    "rulers_pt": {"major": 2.0, ...} | None,
    "alignment": {"default": "left", "justify_allowed": False, "center": "lapidary-only"},
    "default_palette": {"primary": "#...", ...},   # preenche slots que a marca não declara
    "default_fonts": {"sans": "...", "serif": "...", "mono": "..."},
    "rules": ["frase curta de método", ...],
    "signage": {...} | None,        # só presets com wayfinding (ex.: vignelli)
}
```

## Presets que acompanham

### `blank` — passthrough sem opiniões (default)
Sem disciplina imposta. Escala modular ~1.25 (`xs`→`4xl`), grids de coluna (12/8/4), sem régua, `color_semantics: free`. Use quando você só quer **normalizar** um DS existente em tokens multi-formato sem nenhum julgamento de método.

### `vignelli` — o Canon
Cor = identificador (uma por linha/sistema), dois tamanhos vivos (heading ≈ 2× body), cinco grids canônicos (`2x4 5x4 3x6 6x6 4x8`), réguas 2/1/0.5pt, flush-left, signage Grandi Stazioni. Detalhe completo do método em `vignelli.md`. Preserva a skill `vignelli-canon-mscs` original como um preset.

### `swiss` — International Typographic Style
Grade matemática, escala modular (~1.2/1.44), máximo três tamanhos vivos, flush-left, réguas finas (1/0.5/0.25pt), cor como identificador funcional.

## Adicionar um preset

1. Acrescente uma entrada no dict `PRESETS` seguindo a anatomia acima.
2. Toda chave é obrigatória; use `None` onde a disciplina não opina (`rulers_pt`, `signage`, `max_type_sizes`).
3. `type_steps` são múltiplos do `base_px` — defina os degraus que a disciplina reconhece.
4. Se a disciplina trata cor como identificador, use `"color_semantics": "identifier"` para herdar o aviso de diluição.
5. Rode `python3 scripts/design_canon.py --preset <nome> --format css` e confira os seis formatos.

## Precedência de resolução

`flag` (--primary/--base/--face/--prefix) **>** `--config` (valores da marca) **>** `default_*` do preset.

A marca **adiciona e sobrescreve** chaves de paleta/fonte; ela não apaga os defaults do preset. Se quiser uma paleta limpa (sem as cores default da disciplina), declare todas as chaves que você quer no config.

# Preset `vignelli` — o Canon

A disciplina de Massimo Vignelli, preservada como preset showcase. Aplique-a a qualquer marca com `--preset vignelli`; troque a cor identificadora com `--primary`.

## Os 12 intangíveis (decidir antes de desenhar)

A disposição mental antes da forma: semântica · sintática · pragmática · disciplina · adequação · ambiguidade (evitá-la) · "design é um" (coerência total) · poder visual · elegância intelectual · atemporalidade · responsabilidade · equidade. Procure o significado antes da forma. **Se você consegue ver o layout, é um layout ruim.**

## Os tangíveis

**Grid — 5 grids canônicos.** `2x4 · 5x4 · 3x6 · 6x6 · 4x8` (colunas × módulos). Gutters apertados (~uma linha de tipo). Margens externas tensionadas. O grid é estrutura, não sugestão.

**Tipografia — house face e dois tamanhos.** Seis faces bastam uma carreira (Garamond 1532 → Bodoni → Century → Futura → Times → Helvetica 1957). Helvetica é a house face. **Dois tamanhos por página, no máximo** — heading ≈ 2× body. Todo o resto é peso, não tamanho. Flush left por padrão; justificado proibido; centralizado só para texto lapidar.

**Régua — o tipo pendura.** 2pt major, 1pt minor, 0.5pt hair. O tipo pendura DA régua, não flutua perto dela.

**Paleta — cor é identificador.** Hexes do Canon (vermilion `#F04E23`, signal blue `#0039A6`, signal yellow `#FFCC00`), não decorativos. Uma cor por linha/sistema. Cor identifica, nunca enfeita.

**Espaço branco.** "É o branco que faz o preto cantar." Proteja o silêncio.

## Sinalização / wayfinding

Painel azul `#0039A6`, Helvetica branca, flush left. Ângulos 45° / 90° só. Dot sólido = a linha para na estação; anel vazado = a linha passa sem parar. Uma cor por linha. Seta compartilha a cap box do texto. Tabela de painéis: `python3 scripts/design_canon.py --preset vignelli --signage` ou `signage_spec.md`.

## Como o preset materializa o Canon

| Intangível/tangível | No preset |
|---|---|
| Dois tamanhos, heading ≈ 2× body | `type_steps` body 1.0 / heading 2.0; `max_type_sizes: 2` (gera aviso) |
| Cinco grids | `grids` = os cinco pares canônicos |
| Régua, o tipo pendura | `rulers_pt` 2/1/0.5; CSS emite `.v-rule { border-top: ... }` |
| Cor = identificador | `color_semantics: identifier` (avisa se a paleta dilui) |
| Flush left, nunca justificado | `alignment.justify_allowed: False`; CSS emite `.v-flush-left` |
| House face em headless | fallback `'Liberation Sans'` anexado antes de Arial |

## Diferença vs. a skill `vignelli-canon-mscs`

A skill original **ensina e tranca** o método Vignelli (paleta canônica = lei, não trocar pela marca). Aqui o Canon é **uma disciplina entre outras**, aplicável a qualquer marca: você mantém o rigor (dois tamanhos, régua, grid, cor-identificador) mas alimenta os valores da SUA marca. Para o método Vignelli puro como referência de design, use a skill original; para gerar tokens disciplinados de qualquer DS, use esta.

---
name: design-canon
description: Aplica uma DISCIPLINA de design (preset) aos tokens de QUALQUER design system e emite em CSS, SCSS, Tailwind v4 @theme, JSON, W3C Design Tokens e Style Dictionary. Modelo — disciplina ⊥ marca - o preset traz o método (razão de escala de tipo, grids, pesos de régua, semântica de cor, fallback de fonte); a marca traz os valores (paleta, fontes, base) via config JSON ou flags. Presets - vignelli (Canon), swiss (estilo internacional), blank (passthrough). Determinístico, zero rede. MANDATORY TRIGGERS — design tokens, tokens de design, design system, gerar/exportar tokens, Tailwind theme, @theme, W3C design tokens, style dictionary, escala de tipo, type scale, set de grid, pesos de régua, paleta como identificador, handoff dev, normalizar design system, método Vignelli, estilo suíço, swiss style, converter paleta em tokens. Use SEMPRE que o pedido for gerar, normalizar, exportar ou disciplinar tokens de design a partir de paleta/tipografia/grid — mesmo sem citar a skill.
---

# Design Canon — engine de disciplina de design

Gera tokens de design determinísticos aplicando uma **disciplina** (método) aos **valores** de qualquer design system. Emite seis formatos sem dependência externa.

## O MODELO: disciplina ⊥ marca

Duas coisas ortogonais. Não as confunda — é o eixo inteiro da skill.

| | O quê | De onde vem |
|---|---|---|
| **Disciplina** (preset) | O método: razão da escala de tipo, set de grids canônicos, pesos de régua, regras de alinhamento, semântica de cor (identificador vs. livre), estratégia de fallback de fonte. **A régua.** | `--preset` (embutido no script) ou um config custom |
| **Marca** (input) | Os valores: paleta, fontes, tamanho base. **O conteúdo.** | `--config DS.json` e/ou flags (`--primary`, `--base`, `--face`) |

Você renderiza os valores da marca **através de** uma disciplina. O mesmo DS da MSCS pode sair pela disciplina Vignelli (cor = identificador, dois tamanhos, régua dura) ou pela `blank` (sem opiniões, só normaliza). A disciplina nunca troca os valores da marca — ela impõe a *estrutura* e *avisa* quando a marca viola o método.

## QUANDO USAR

- Tokens de design para handoff dev a partir de uma paleta/tipografia (qualquer marca)
- Normalizar um DS existente em tokens multi-formato (CSS / SCSS / Tailwind / JSON / W3C / Style Dictionary)
- Aplicar rigor de método (Vignelli, suíço) a um DS de cliente ou ao DS da casa
- Sistema de identidade: grid + escala de tipo + cor como identificador
- Spec de sinalização / wayfinding (presets que definem signage, ex.: vignelli)

**Quando NÃO usar:** redigir copy de marca (isso é `mscreative-voice`/`supercopy`); desenhar layout final no navegador (isso é trabalho de front-end, não de tokens). Esta skill produz os *tokens* e o *método*, não a peça.

## GERADOR

Script único, autocontido, em `scripts/design_canon.py`. Os presets vivem embutidos nele (fonte de verdade), então roda mesmo sem nenhuma referência carregada.

```bash
python3 scripts/design_canon.py --list-presets                          # disciplinas disponíveis
python3 scripts/design_canon.py --config DS.json --format tailwind       # SEU DS no @theme do Tailwind v4
python3 scripts/design_canon.py --config DS.json --preset vignelli --format css
python3 scripts/design_canon.py --preset vignelli --primary "#0039A6"    # troca só a cor identificadora
python3 scripts/design_canon.py --config DS.json --format w3c            # W3C Design Tokens
python3 scripts/design_canon.py --config DS.json --format style-dictionary
python3 scripts/design_canon.py --config DS.json --format scss
python3 scripts/design_canon.py --preset vignelli --grid 4x8             # mapa coluna × módulo
python3 scripts/design_canon.py --preset vignelli --signage              # tabela de painéis
```

Flags batem sobre o config (precedência: flag > config > default do preset). Avisos de disciplina (paleta diluindo a cor-identificador, limite de tamanhos de tipo) saem em `stderr` — não poluem o token output.

### Config da marca (JSON)

```json
{
  "name": "MSCS DS V3.0",
  "base_px": 16,
  "prefix": "ms",
  "palette": { "primary": "#B4C636", "bg": "#0A0A0E", "fg": "#B2A898" },
  "fonts": { "serif": "Fraunces", "sans": "Inter Tight", "mono": "IBM Plex Mono" }
}
```

Só `palette` é o mínimo útil. O resto cai no default do preset. Schema completo: `references/config_schema.md`. Exemplo pronto: `assets/examples/mscs_ds_v3.json`.

### Formatos de saída

`css` (`:root` custom properties) · `scss` (maps) · `tailwind` (bloco `@theme` v4, namespaces `--color-*`/`--font-*`/`--text-*`) · `json` (payload legível) · `w3c` (Design Tokens spec, `$value`/`$type`) · `style-dictionary` (nós aninhados com `value`).

## PRESETS (disciplinas)

| Preset | Disciplina | Quando |
|---|---|---|
| `blank` | Passthrough sem opiniões. Escala modular ~1.25, grids de coluna comuns, sem régua, sem semântica de cor. | Só normalizar um DS existente em tokens. **Default.** |
| `vignelli` | O Canon: cor = identificador (uma por linha), dois tamanhos de tipo (heading ≈ 2× body), cinco grids, réguas 2/1/0.5pt, flush-left, signage Grandi Stazioni. | Rigor editorial/identidade. Detalhe em `references/vignelli.md`. |
| `swiss` | Estilo tipográfico internacional: grade matemática, escala modular, máx. três tamanhos, flush-left. | Objetividade, sistemas densos de informação. |

Documentação dos presets e como adicionar um: `references/presets.md`.

## REGRAS DURAS (não violar)

Invariantes do método. Quebrar descaracteriza a engine.

1. **Disciplina ⊥ marca.** O preset impõe estrutura; a marca fornece valores. Nunca deixe um valor de marca virar regra de método, nem um default de disciplina sobrescrever um valor que a marca declarou.
2. **Fallback de render é obrigatório.** Toda família de fonte recebe um fallback de métrica compatível instalado (`'Liberation Sans'` antes de Arial e do genérico) — senão o headless cai para Noto/Calibri e quebra a grotesca. Confirme com `fc-match` antes de publicar.
3. **Keyword genérica de fonte vai por último** (`sans-serif`, `monospace`…); famílias com espaço são aspeadas.
4. **Avisos de disciplina vão pra `stderr`**, nunca misturados no token output.
5. **Gerador determinístico.** Zero rede, zero credencial. Presets embutidos no script.
6. **Sob disciplina `identifier` (vignelli/swiss):** cor é identificador, uma por linha/sistema. O engine avisa se a paleta tem acentos demais — respeite o aviso ou troque de preset.
7. **Sob `vignelli`:** dois tamanhos de tipo vivos por página (heading ≈ 2× body), flush-left, o tipo pendura na régua. Os demais degraus existem só para capas/specs.

## ARMADILHA — Helvetica/house face em headless

A house face de uma grotesca não existe na maioria dos ambientes headless. Ao rasterizar (cairosvg, Chromium headless) ou alimentar arte para um modelo de imagem, o render cai para Noto Sans (lê como Calibri) e quebra a grotesca. O engine já anexa `'Liberation Sans'` antes de Arial em toda família sans por isso. **Sempre confira um render** com `fc-match <fonte>` no ambiente antes de publicar.

## FALLBACK_INLINE

> Usar quando `scripts/` e `references/` não carregarem.

### Tokens mínimos (CSS, disciplina blank, base 16px)

```css
:root{
  --ds-color-primary:#2D2D2D; --ds-color-bg:#FFFFFF; --ds-color-fg:#111111;
  --ds-font-sans:'Inter','Liberation Sans',Arial,sans-serif;
  --ds-text-base:16px; --ds-text-lg:20px; --ds-text-3xl:39px;   /* escala ~1.25 */
}
```

Sob Vignelli: troque para dois tamanhos (`--v-text-body:16px; --v-text-heading:32px`), adicione réguas (`--v-rule-major:2pt; --v-rule-minor:.5pt`), paleta-identificador, flush-left.

### QA mínimo

- [ ] Disciplina e marca não se contaminaram (preset = estrutura; config = valores)
- [ ] Toda família sans tem `'Liberation Sans'` antes de Arial / do genérico
- [ ] Keyword genérica (`sans-serif`/`monospace`) está por último
- [ ] Formato pedido bate (Tailwind = `@theme` com `--color-*`/`--text-*`; W3C = `$value`/`$type`)
- [ ] Avisos de disciplina foram pra stderr, não pro arquivo de tokens
- [ ] Sob `vignelli`/`swiss`: paleta não diluiu a cor-identificador

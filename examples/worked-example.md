# Worked example — design-canon

Três rodadas reais do gerador, copiadas verbatim da saída. Determinístico: rode os mesmos comandos e recebe o mesmo resultado.

## 1. DS da casa → Tailwind v4 (disciplina `blank`)

A marca passa direto pra tokens, sem julgamento de método. O `blank` só normaliza.

```bash
python3 scripts/design_canon.py --config assets/examples/mscs_ds_v3.json --format tailwind
```

```css
@theme {
  /* design-canon — disciplina 'blank' · MSCS DS V3.0 */
  --color-primary: #B4C636;
  --color-bg: #0A0A0E;
  --color-fg: #B2A898;
  --color-bg-2: #111114;
  --color-ceremonial: #E8C547;

  --font-sans: 'Inter Tight', 'Liberation Sans', Arial, sans-serif;
  --font-serif: Fraunces, 'Liberation Serif', Georgia, serif;
  --font-mono: 'IBM Plex Mono', 'Liberation Mono', Menlo, monospace;

  --text-xs: 10.24px;
  --text-sm: 12.8px;
  --text-base: 16.0px;
  --text-lg: 20.0px;
  --text-xl: 25.01px;
  --text-2xl: 31.25px;
  --text-3xl: 39.06px;
  --text-4xl: 48.83px;
}
```

## 2. A mesma marca sob a disciplina Vignelli, cor identificadora trocada → CSS

Agora o método entra: dois tamanhos vivos (body 16 / heading 32 = 2×), cinco grids, réguas 2/1/0.5pt, flush-left. O aviso de disciplina (máx. 2 tamanhos) sai em `stderr`, fora do arquivo.

```bash
python3 scripts/design_canon.py --preset vignelli --primary "#0039A6" --format css
```

```css
:root {
  /* design-canon — disciplina 'vignelli' aplicada */
  --v-color-primary: #0039A6;
  --v-color-blue: #0039A6;
  --v-color-yellow: #FFCC00;
  --v-color-ink: #0A0A0A;
  --v-color-paper: #F4F1EA;
  --v-color-white: #FFFFFF;

  --v-font-sans: 'Helvetica Neue', Helvetica, 'Liberation Sans', Arial, sans-serif;
  --v-font-serif: Times, 'Liberation Serif', Georgia, serif;
  --v-font-mono: 'Liberation Mono', Menlo, monospace;

  --v-text-caption: 12.0px;
  --v-text-body: 16.0px;
  --v-text-lead: 24.0px;
  --v-text-heading: 32.0px;
  --v-text-display: 64.0px;
  --v-text-mega: 128.0px;
  --v-leading-body: 1.2;
  --v-leading-heading: 1.05;

  --v-rule-major: 2.0px;
  --v-rule-minor: 1.0px;
  --v-rule-hair: 0.5px;
}

/* o tipo pendura DA régua */
.v-rule { border-top: var(--v-rule-major) solid var(--v-color-ink, #0A0A0A); }
.v-flush-left { text-align: left; } /* default; nunca justificar */

.v-grid-2x4 { display:grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: repeat(4, 1fr); gap: 1rem; }
.v-grid-5x4 { display:grid; grid-template-columns: repeat(5, 1fr); grid-template-rows: repeat(4, 1fr); gap: 1rem; }
.v-grid-3x6 { display:grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(6, 1fr); gap: 1rem; }
.v-grid-6x6 { display:grid; grid-template-columns: repeat(6, 1fr); grid-template-rows: repeat(6, 1fr); gap: 1rem; }
.v-grid-4x8 { display:grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(8, 1fr); gap: 1rem; }
```

## 3. DS de cliente sob a disciplina suíça → Style Dictionary

Input por arquivo, escala modular suíça derivada da base 17px, réguas finas, paleta do cliente preservada exata.

```bash
python3 scripts/design_canon.py --config assets/examples/client_acme_ds.json --preset swiss --format style-dictionary
```

```json
{
  "color": {
    "primary": {
      "value": "#0B5FFF"
    },
    "ink": {
      "value": "#0C1116"
    },
    "paper": {
      "value": "#FFFFFF"
    },
    "success": {
      "value": "#0FA958"
    }
  },
  "size": {
    "font": {
      "caption": {
        "value": "11.8px"
      },
      "body": {
        "value": "17.0px"
      },
      "sub": {
        "value": "20.4px"
      },
      "heading": {
        "value": "29.38px"
      },
      "display": {
        "value": "50.76px"
      },
      "mega": {
        "value": "87.72px"
      }
    },
    "rule": {
      "major": {
        "value": "1.0px"
      },
      "minor": {
        "value": "0.5px"
      },
      "hair": {
        "value": "0.25px"
      }
    }
  },
  "font": {
    "sans": {
      "value": "Söhne, 'Liberation Sans', Arial, sans-serif"
    },
    "serif": {
      "value": "Times, 'Liberation Serif', Georgia, serif"
    },
    "mono": {
      "value": "'Söhne Mono', 'Liberation Mono', Menlo, monospace"
    }
  }
}
```

---

Em todas: as cores que você declarou continuam com os nomes que você deu, os hexes que você passou. O fallback de render (`Liberation Sans` antes de Arial) é anexado às fontes — a única adição, e ela existe pra sua tipografia não quebrar em headless.

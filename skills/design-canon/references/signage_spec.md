# Spec de Sinalização / Wayfinding (preset `vignelli`)

> Saída de referência de `python3 scripts/design_canon.py --preset vignelli --signage`. Template de wayfinding.
> Painel azul `#0039A6`, Helvetica branca, flush left. Ângulos 45° / 90° só. A cor identificadora segue a paleta do config — sob `vignelli` o default é `blue` (`#0039A6`).

## Hierarquia de painel (lógica Grandi Stazioni)

Cap-heights escalam por módulo fixo. Setas e pictogramas compartilham a cap box do texto.

| Painel | Painel mm | Cap mm | Nota |
|---|---:|---:|---|
| Identificação de estação (prédio) | 600 | 100 | Cap height 100mm, iluminado internamente |
| Direcional (suspenso) | 300 | 75 | Seta compartilha a cap box; flush left |
| Informação / regulatório | 150 | 25 | Pendura numa régua de 2pt |
| Número de plataforma (bandeira) | 250 | 250 | Numeral num quadrado, dupla face |

## Cores

| Função | Chave de paleta | Hex default |
|---|---|---|
| Painel identificador | `blue` | `#0039A6` (signal blue) |
| Texto / pictogramas | `white` | `#FFFFFF` |
| Acento de alerta | `yellow` | `#FFCC00` (signal yellow) |

As cores vêm da paleta resolvida — passe `--config` com `blue`/`white`/`yellow` para uma marca própria.

## Regras de diagrama de linha

- **Uma cor por linha.** A cor identifica a linha, não enfeita o mapa.
- **Dot sólido** = a linha **para** naquela estação.
- **Anel vazado** = a linha **passa** sem parar.
- Traçados só em **45° ou 90°**. Sem curvas orgânicas, sem diagonais soltas.
- Texto de estação flush left, pendurado na grade.

## Checklist de spec

- [ ] Painel identificador, texto branco, flush left
- [ ] Cap heights seguem o módulo (100 / 75 / 25 mm)
- [ ] Setas dentro da cap box do texto
- [ ] Uma cor por linha
- [ ] Dot sólido (para) vs. anel vazado (passa) consistentes
- [ ] Ângulos só 45° / 90°
- [ ] Render conferido em Helvetica / Liberation Sans (não Noto)

# Changelog

Todas as mudanças notáveis deste projeto são documentadas aqui.
Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versionamento: [SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] — 2026-06-25

Primeiro release público. Empacota a engine de disciplina de design como skill instalável do Claude.

### Adicionado
- `skills/design-canon/SKILL.md` — o corpo canônico da skill: modelo disciplina ⊥ marca, os 3 presets, os 6 formatos de saída, 7 regras duras, armadilha de render headless, FALLBACK_INLINE.
- `skills/design-canon/scripts/design_canon.py` — o gerador determinístico. Presets embutidos (`blank`, `vignelli`, `swiss`); emissores CSS, SCSS, Tailwind v4 `@theme`, JSON, W3C Design Tokens, Style Dictionary; fallback de render anexado a toda família de fonte.
- `skills/design-canon/references/` — presets, vignelli (o Canon como preset showcase), config_schema, signage_spec, QUICKREF.
- `skills/design-canon/assets/examples/` — DS da MSCS e DS de cliente como configs de exemplo.
- `README.md` — landing: o problema (tokens infiéis e não-determinísticos), o mecanismo (disciplina ⊥ marca), como funciona, quando usar, exemplo, instalar, FAQ.
- `examples/worked-example.md` — três rodadas reais, copiadas verbatim da saída do gerador.
- `design-canon.skill` — skill empacotada na raiz pra install sem terminal.
- `assets/social-preview.html` — fonte DS V3.0 do card social.

### Créditos
- A disciplina `vignelli` implementa o método de Massimo Vignelli (*The Vignelli Canon*, 2010). A disciplina `swiss` segue o estilo tipográfico internacional. Os formatos W3C Design Tokens e Style Dictionary seguem suas specs públicas.

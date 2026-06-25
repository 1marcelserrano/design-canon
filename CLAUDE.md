# CLAUDE.md — design-canon

## O que é este repo

Uma skill do Claude distribuída como repo público. A fonte de verdade é
`skills/design-canon/SKILL.md` + `skills/design-canon/scripts/design_canon.py`.
Toda mudança de comportamento começa ali.

A skill aplica uma **disciplina** de design (preset) aos **valores** de qualquer
design system e emite tokens em seis formatos. Modelo central: disciplina ⊥ marca.
O repo é vitrine — o README é landing, não só doc.

## O que editar

| Arquivo | O que controla |
|---|---|
| `skills/design-canon/SKILL.md` | Comportamento da skill — triggers, modelo, formatos. O corpo que o agente carrega. Canônico. |
| `skills/design-canon/scripts/design_canon.py` | O gerador. Presets embutidos no dict `PRESETS`. Os 6 emissores. Adicionar preset = nova entrada no dict. |
| `skills/design-canon/references/` | presets, vignelli (o Canon como exemplo), config_schema, signage_spec, QUICKREF. |
| `README.md` (raiz) | Porta de entrada do produto. Otimizar pra quem precisa de tokens de design. |
| `examples/worked-example.md` | Rodadas reais, copiadas verbatim da saída do gerador. Manter fiel. |
| `assets/social-preview.html` | Fonte DS V3.0 do card social do GitHub. |
| `page/index.html` | Cópia da página Vercel publicada. |

## O que NÃO editar

- Não editar a skill canônica no monorepo privado `mscs-skills` a partir daqui — este repo é espelho publicado. Mudanças de comportamento fluem pelo `skills-sync`.
- Manter o frontmatter do SKILL.md (`name`, `description`) intacto — `npx skills` e o loader de plugin do Claude parseiam ele.
- Não fabricar números. O gerador é determinístico; qualquer exemplo sai da saída real.
- Nunca commitar `.env`, tokens ou credenciais.

## Convenções

- Idioma: README/página em PT-BR, registro Tradutor. Frases curtas, voz ativa, zero floreio. Sem léxico inflado, sem paralelismo negativo.
- Commits: Conventional Commits. Push só com SHA verificado (local = remote).
- `design-canon.skill` na raiz: zip de `skills/design-canon`, recriável via `skills-sync` — não editar à mão.

## Licença

MIT. Contribuições bem-vindas. Veja CONTRIBUTING.md.

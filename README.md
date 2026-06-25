# design-canon

**Aplica uma disciplina de design — Vignelli, suíça ou nenhuma — aos tokens de qualquer design system e exporta em seis formatos.**

Você tem uma paleta, umas fontes e um tamanho-base. Quer isso virar tokens prontos pro dev — CSS, Tailwind v4, Style Dictionary — sem reescrever à mão a cada formato, e sem o modelo "designar demais" e inventar cor que você não pediu. A `design-canon` separa duas coisas que costumam grudar: a **disciplina** (o método) e a **marca** (os valores). Um arquivo Python, sem dependência, sem rede, sem credencial.

[Instalar](#instalar) · [Como funciona](#como-funciona) · [Quando usar](#quando-usar) · [Exemplo](#exemplo) · [FAQ](#faq) · [Página](https://design-canon-page.vercel.app)

---

## O problema

Pede pra um modelo "gerar os design tokens da minha marca" e ele entrega algo bonito e infiel. Renomeia suas cores (`primary` vira `lime`), inventa uma rampa de cinza que não existe no seu DS, cria tints e shades que você nunca aprovou, e escolhe um formato que não é o que seu time usa. Cada vez sai diferente. Para um handoff de dev, isso é ruído: você queria os *seus* valores, normalizados, num formato fixo.

A causa é simples. "Gerar tokens" mistura duas decisões que deveriam ser separadas: **qual o método** (quantos tamanhos de tipo, que grids, como a cor se comporta) e **quais os valores** (seus hexes, suas fontes). Quando as duas viram uma coisa só, o modelo preenche os buracos chutando — e o chute é a parte que você não controla.

## Como funciona

O modelo central é **disciplina ⊥ marca**. São ortogonais.

| | O quê | De onde vem |
|---|---|---|
| **Disciplina** (preset) | O método: razão da escala de tipo, set de grids, pesos de régua, alinhamento, semântica de cor, fallback de fonte. A régua. | `--preset` (embutido no script) |
| **Marca** (input) | Os valores: paleta, fontes, tamanho-base. O conteúdo. | `--config DS.json` e/ou flags |

Você renderiza os valores da sua marca **através de** uma disciplina. O gerador é determinístico: a mesma entrada dá sempre a mesma saída. A disciplina nunca troca seus valores — ela impõe a *estrutura* e *avisa* (em `stderr`, fora do arquivo) quando a marca viola o método.

```
config da marca  ─┐
                  ├─►  design-canon (disciplina escolhida)  ─►  tokens [css | scss | tailwind | json | w3c | style-dictionary]
preset/flags     ─┘
```

**Três disciplinas** acompanham: `blank` (passthrough, sem opiniões — só normaliza), `vignelli` (o Canon de Massimo Vignelli: cor como identificador, dois tamanhos, cinco grids, réguas) e `swiss` (estilo tipográfico internacional). **Seis formatos** de saída: CSS custom properties, SCSS maps, Tailwind v4 `@theme`, JSON, W3C Design Tokens e Style Dictionary.

## Quando usar

**Use quando:**
- Você tem um DS (paleta + fontes + base) e quer tokens prontos pro dev
- Precisa do mesmo DS em mais de um formato (ex.: Tailwind no app, Style Dictionary no build multiplataforma)
- Quer aplicar rigor de método (Vignelli, suíço) a uma marca de cliente ou à da casa
- Está montando sistema de identidade: grid + escala de tipo + cor como identificador

**Não use quando:**
- Você quer redigir copy de marca ou nomear a oferta (isso é outra ferramenta)
- Está desenhando o layout final no navegador — a `design-canon` produz os *tokens*, não a página
- Precisa de um sistema de cor algorítmico (gerar tints/shades automáticos) — aqui os valores são os que você declara, de propósito

## Exemplo

Você descreve a marca num JSON:

```json
{
  "name": "MSCS DS V3.0",
  "base_px": 16,
  "palette": { "primary": "#B4C636", "bg": "#0A0A0E", "fg": "#B2A898" },
  "fonts": { "serif": "Fraunces", "sans": "Inter Tight", "mono": "IBM Plex Mono" }
}
```

Roda pedindo Tailwind v4:

```bash
python3 scripts/design_canon.py --config ds.json --format tailwind
```

Sai um bloco `@theme` pronto pro `globals.css` — seus valores exatos, com fallback de render anexado às fontes (porque a house face some em ambiente headless):

```css
@theme {
  --color-primary: #B4C636;
  --color-bg: #0A0A0E;
  --color-fg: #B2A898;

  --font-sans: 'Inter Tight', 'Liberation Sans', Arial, sans-serif;
  --font-serif: Fraunces, 'Liberation Serif', Georgia, serif;
  --font-mono: 'IBM Plex Mono', 'Liberation Mono', Menlo, monospace;

  --text-base: 16.0px;
  --text-lg: 20.0px;
  --text-3xl: 39.06px;
  /* … */
}
```

`primary` continua `primary`. Nenhuma cor renomeada, nenhuma rampa inventada. Rodada completa — incluindo a mesma marca sob a disciplina Vignelli e um DS de cliente sob a suíça — em [examples/worked-example.md](./examples/worked-example.md).

## Instalar

```bash
# Via skills CLI (recomendado)
npx skills add 1marcelserrano/design-canon

# Ou manualmente — faça backup antes, se a pasta já existir:
# mv ~/.claude/skills/design-canon ~/.claude/skills/design-canon.backup
git clone https://github.com/1marcelserrano/design-canon.git
cp -r design-canon/skills/design-canon ~/.claude/skills/
```

**Verificar:** abra uma sessão nova do Claude e rode `/skills` (ou pergunte "quais skills você tem?"). `design-canon` deve aparecer. Se não, confira que `~/.claude/skills/design-canon/SKILL.md` existe e reinicie a sessão.

**Sem terminal?** Baixe [`design-canon.skill`](./design-canon.skill) e suba no Claude (Cowork / claude.ai → Skills).

**Testar sem instalar:** o gerador roda sozinho. `python3 skills/design-canon/scripts/design_canon.py --list-presets`.

**Atualizar:** `git pull` no repo clonado e re-copie. Mudanças ficam no [CHANGELOG.md](./CHANGELOG.md).

## FAQ

**Manda meus dados pra algum lugar?**
Não. A skill é um arquivo que o Claude lê localmente, e o gerador é um script Python sem rede. Sua paleta e seus tokens ficam na sua máquina.

**Por que Vignelli é só um preset, e não a lei?**
Porque o valor é o *método*, não a marca de ninguém. A disciplina de Vignelli (dois tamanhos, régua, grid, cor como identificador) vira uma régua aplicável a qualquer paleta — a sua, a do cliente. Quem quiser o Canon puro como referência de design usa a skill `vignelli-canon`; aqui ele é uma das disciplinas.

**O que é "fallback de render"?**
A house face de uma grotesca (Helvetica, Söhne, Inter) não existe na maioria dos ambientes headless. Ao rasterizar — Chromium headless, um modelo de imagem — o render cai para Noto Sans e quebra a tipografia. O gerador anexa uma fonte de métrica compatível instalada (`'Liberation Sans'` antes de Arial) a toda família, pra sobreviver a isso.

**Funciona com qual stack?**
Os tokens saem em CSS, SCSS, Tailwind v4, JSON, W3C Design Tokens e Style Dictionary — então encaixam em praticamente qualquer pipeline de front. O gerador é Python 3, roda em macOS, Linux e Windows.

**Como desinstalo?**
`rm -rf ~/.claude/skills/design-canon`. Seus arquivos ficam intactos.

**Vai ter manutenção?**
Sim. Versões seguem o [CHANGELOG.md](./CHANGELOG.md). Atualize com `git pull` ou rode `npx skills add` de novo.

## Sobre o autor

Feito por [Marcel Serrano](https://github.com/1marcelserrano), founder da [MSCREATIVE.SYSTEMS™](https://mscreative.systems) — Barcelona.

Mais sobre trabalhar com IA sem perder a própria voz: [Fronteirista](https://fronteirista.substack.com) — a newsletter gratuita onde esses sistemas são construídos à vista.

## Contribuir

PRs são bem-vindos. Veja [CONTRIBUTING.md](./CONTRIBUTING.md).

## Licença

MIT — veja [LICENSE](./LICENSE). Faz fork, modifica, rebatiza — só mantém os créditos intactos. A disciplina Vignelli é de Massimo Vignelli (*The Vignelli Canon*, 2010); o preset implementa o método, o crédito é dele.

---

<sub>Forjado na [MSCREATIVE.SYSTEMS™](https://mscreative.systems) — Barcelona</sub>

# Contribuir com a design-canon

Obrigado por considerar uma contribuição.

## O que editar

Fonte de verdade: `skills/design-canon/SKILL.md` e o gerador
`skills/design-canon/scripts/design_canon.py`. Toda mudança de comportamento vai
ali primeiro. O `README.md` da raiz é a porta do produto e atualiza depois que o
corpo da skill estabiliza.

## Como testar localmente

1. Clone o repo.
2. Rode o gerador direto — não precisa instalar nada:
   `python3 skills/design-canon/scripts/design_canon.py --list-presets`
3. Pra testar como skill: copie `skills/design-canon/` pro seu diretório de skills
   (`~/.claude/skills/` no macOS/Linux), reinicie o Claude e dispare com uma frase do README.

## Adicionar um preset (disciplina)

O caminho mais útil de contribuição. Acrescente uma entrada ao dict `PRESETS` no
gerador seguindo a anatomia documentada em `skills/design-canon/references/presets.md`.
Rode os seis formatos e confira que nenhum quebra. Uma disciplina nova bem-feita
(Bauhaus, brutalista, Material) é muito bem-vinda.

## Diretrizes de PR

- **Conventional Commits.** `feat:`, `fix:`, `docs:`, `refactor:`.
- **Uma preocupação por PR.** Um ajuste de doc e uma mudança de comportamento vão separados.
- **Mostre antes/depois** pra qualquer mudança no gerador. Uma frase do porquê.
- **Mantenha os comandos de instalação corretos.** Um install quebrado custa usuários reais.
- **Determinismo é regra.** Sem rede, sem credencial, sem número fabricado. A mesma entrada dá a mesma saída.

## Uma nota sobre Vignelli

A disciplina `vignelli` implementa o método de Massimo Vignelli (*The Vignelli
Canon*). Melhorias em *como o preset aplica o método* entram aqui; o método em si
é dele.

## Licença

Ao contribuir, você concorda que sua contribuição é licenciada sob MIT.

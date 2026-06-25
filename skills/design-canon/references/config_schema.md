# Schema do config da marca

JSON passado em `--config`. Descreve os **valores** da marca; a estrutura vem do preset.

```json
{
  "name": "string — rótulo humano, aparece nos comentários do output (opcional)",
  "base_px": 16,
  "prefix": "ms",
  "palette": {
    "primary": "#B4C636",
    "bg": "#0A0A0E",
    "fg": "#B2A898",
    "<qualquer-nome>": "#hex"
  },
  "fonts": {
    "sans": "Inter Tight",
    "serif": "Fraunces",
    "mono": "IBM Plex Mono"
  }
}
```

## Campos

| Campo | Tipo | Default | Nota |
|---|---|---|---|
| `name` | string | `null` | Só aparece no comentário de cabeçalho do output. |
| `base_px` | número | `16` | Tamanho do body em px. Toda a escala de tipo deriva dele × `type_steps` do preset. |
| `prefix` | string | o do preset | Namespace de token (`--{prefix}-...`) nos formatos css/scss/json. Tailwind ignora (usa namespaces próprios). |
| `palette` | objeto | merge com `default_palette` do preset | Chave → hex. Nomes livres. `primary` é a cor identificadora sob disciplinas `identifier`. |
| `fonts` | objeto | merge com `default_fonts` do preset | Chaves reconhecidas: `sans`, `serif`, `mono`. Cada uma recebe fallback de render anexado. Pode passar lista CSV (`"Inter Tight, system-ui"`). |

## Mínimo útil

```json
{ "palette": { "primary": "#B4C636" } }
```

Tudo o que faltar cai no default do preset escolhido.

## Overrides por flag

- `--primary "#hex"` → `palette.primary`
- `--base 18` → `base_px`
- `--face "Inter Tight"` → `fonts.sans`
- `--prefix ms` → `prefix`

Precedência: **flag > config > default do preset**.

## Notas de merge

- A paleta da marca **adiciona/sobrescreve** chaves; não apaga os defaults da disciplina. Para uma paleta limpa, declare todas as chaves desejadas.
- Fontes ganham fallback de métrica compatível automaticamente (`'Liberation Sans'` etc.) — não inclua o fallback você mesmo, o engine anexa e deduplica.

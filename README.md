# contrashittification.com

A collection of things that run the other way: long-run data showing the world getting
better, and things that have not been enshittified, with the reason each one held.

Static. No framework, no build step at serve time.

| | |
|---|---|
| `build/make-site.py` | writes `index.html`: the posts and the inline SVG charts live here |
| `build/make-images.py` | writes `og-image.png` and the PNG favicons |
| `build/data/` | the OWID World series the charts draw, with a README naming each provider |
| `changelog.json` | the design changelog; render with the vault's `changelog.py render contrashittification` |

Rebuild:

```
/opt/homebrew/bin/python3 build/make-site.py
```

Design is the family language (vault: `zz_System/Claudesidian/design-language-system.md`):
paper ground, one ink, pen for links, gold inside charts and nowhere else, hard edges,
640 measure. The runbook, including what is still owed, is in the vault at
`A6 Business and Career/Websites/contrashittification/contrashittification-runbook.md`.

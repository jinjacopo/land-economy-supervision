# Quarto website

The interactive website of the project: **Is Milan absorbing the North?**

| Page | Content |
| --- | --- |
| `index.qmd` | The question, the answer, key numbers and the verdict on each hypothesis |
| `part1.qmd` | Part 1: is the North becoming a single core? (shares, home market ratio, graduates) |
| `part2.qmd` | Part 2: did Turin and Genoa stall because of their industries? (shift-share, specialisation) |
| `map.qmd` | Map of the 47 northern provinces |
| `method.qmd` | Theory, hypotheses, tests, data, limitations, reproducibility, AI use |
| `_setup.qmd` | Shared chart settings (city colours), included in each page |

The charts are written in Observable JS (built into Quarto) and read the files in `data/`, which are produced by `code/09_site_data.py` (run the scripts in `analysis.md` first).

With [Quarto installed](https://quarto.org/docs/get-started/), run from this folder:

```sh
quarto preview
```

Run `quarto render` to build the site in `_site/`. The site must be opened through a web server (as `quarto preview` does), not by double-clicking the HTML files, because the charts load their data files.

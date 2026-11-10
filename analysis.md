# Analysis

- Software / dependencies: Python 3.9 with the packages in `requirements.txt` (pandas, numpy, matplotlib, requests, openpyxl).
  Setup: `python3 -m venv .venv` then `.venv/bin/pip install -r requirements.txt`.
- Input files and locations: downloaded by the scripts into `data/raw/` (not committed; see `sources.md`). Tidied files go to `data/processed/`.
- Steps or commands, in order (run from the project folder):
  1. `.venv/bin/python code/01_download_eurostat.py`: Eurostat jobs, GDP and population by province.
  2. `.venv/bin/python code/02_download_istat_bes.py`: ISTAT Bes dei territori 2025.
  3. `.venv/bin/python code/03_download_ustat.py`: graduates by university.
  4. `.venv/bin/python code/04_download_census.py`: censuses 2001, 2011, 2021 (the 2021 part is slow, about a minute per request).
  5. `.venv/bin/python code/05_prepare_eurostat.py`: keeps the 47 northern provinces and 2008–2023.
  6. `.venv/bin/python code/06_part1_shares.py`: Part 1, shares and home market ratio (T1, T4, T9, P4).
  7. `.venv/bin/python code/07_part1_who_moves.py`: Part 1, graduates (T2, T3, T8).
  8. `.venv/bin/python code/08_part2_industry.py`: Part 2, shift-share and specialisation (T5, T6).
  9. `.venv/bin/python code/09_site_data.py`: exports the data used by the website to `quarto/data/` (and downloads the GISCO province boundaries for the map).
  10. Website: install [Quarto](https://quarto.org/docs/get-started/) (version 1.11 used), then from the `quarto/` folder run `quarto render` (builds the site in `quarto/_site/`) or `quarto preview` (opens it in a browser). The interactive charts use Observable JS, which is built into Quarto, so the website needs no extra Python packages.
- Output files: see `outputs.md`.
- Main choices (see `framework.md`): northern Italy = 47 provinces; jobs and GDP 2008–2023 only (series break in 2008); knowledge jobs = ICT + finance + professional/administrative services; shift-share reference = Italy, 11 sectors; census comparisons use shares only, with Milan and Monza combined.

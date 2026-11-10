"""Step 3: download graduates by university from the Ministry of University (USTAT).

"Laureati per ateneo, 2001-2024": number of graduates per university, year and
gender. Used for T8 ("Turin trains, Milan employs"): how many graduates the
universities in each city produce. Saved, unchanged, in data/raw/.

Source page: https://dati-ustat.mur.gov.it/dataset/laureati/resource/88acd482-9d75-44d1-ab16-aa04524f5d94
Licence: Italian Open Data License v2.0 (IODL 2.0)

Run from the project folder:  .venv/bin/python code/03_download_ustat.py
"""

from datetime import date
from pathlib import Path

import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

URL = ("https://dati-ustat.mur.gov.it/dataset/ca0b9831-c9ef-49d4-b792-6bd963e4d837/"
       "resource/88acd482-9d75-44d1-ab16-aa04524f5d94/download/02_laureatixateneo.csv")

response = requests.get(URL, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
response.raise_for_status()
(RAW / "ustat_laureati_per_ateneo.csv").write_bytes(response.content)
(RAW / "download_log_ustat.txt").write_text(
    f"ustat_laureati_per_ateneo.csv\t{date.today()}\t{len(response.content)} bytes\t{URL}\n"
)
print("saved", RAW / "ustat_laureati_per_ateneo.csv")

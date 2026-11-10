"""Step 1: download the Eurostat tables used in the project.

Downloads three regional tables (NUTS3 = Italian provinces) from the Eurostat
dissemination API and saves them, unchanged, in data/raw/.

    nama_10r_3empers  employment (thousand persons) by NUTS3 region and sector
    nama_10r_3gdp     GDP at current market prices by NUTS3 region
    nama_10r_3popgdp  average annual population by NUTS3 region

Run from the project folder:  .venv/bin/python code/01_download_eurostat.py
"""

from datetime import date
from pathlib import Path

import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

TABLES = ["nama_10r_3empers", "nama_10r_3gdp", "nama_10r_3popgdp"]
URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{}?format=TSV&compressed=true"

log = []
for table in TABLES:
    response = requests.get(URL.format(table), timeout=120)
    response.raise_for_status()
    path = RAW / f"{table}.tsv.gz"
    path.write_bytes(response.content)
    log.append(f"{table}\t{date.today()}\t{len(response.content)} bytes\t{URL.format(table)}")
    print("saved", path)

# Record when each file was downloaded, so the version can be traced.
(RAW / "download_log_eurostat.txt").write_text("\n".join(log) + "\n")

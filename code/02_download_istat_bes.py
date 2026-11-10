"""Step 2: download ISTAT's "Bes dei territori" (2025 edition, latest available).

Provincial (NUTS3) well-being indicators in historical series, including
the education indicators used in the project (graduates aged 25-39 and
graduate mobility). The zip is saved, unchanged, in data/raw/ and unpacked
into data/raw/bes_2025/.

Source page: https://www.istat.it/notizia/bes-dei-territori-edizione-2025/

Run from the project folder:  .venv/bin/python code/02_download_istat_bes.py
"""

import zipfile
from datetime import date
from pathlib import Path

import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

URL = "https://www.istat.it/wp-content/uploads/2025/06/Bes_dei_territori_edizione_2025.zip"
zip_path = RAW / "Bes_dei_territori_edizione_2025.zip"

response = requests.get(URL, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
response.raise_for_status()
zip_path.write_bytes(response.content)

with zipfile.ZipFile(zip_path) as z:
    z.extractall(RAW / "bes_2025")

(RAW / "download_log_istat_bes.txt").write_text(
    f"Bes_dei_territori_edizione_2025.zip\t{date.today()}\t{len(response.content)} bytes\t{URL}\n"
)
print("saved and unpacked", zip_path)

"""Step 4: download census data on graduates by province (2001, 2011, 2021).

BES graduate data only starts in 2018, so the censuses give the long-run view
of where graduates live. Three sources, saved unchanged in data/raw/census/:

    2001  Eurostat table cens_01rews: population by educational attainment
          (ISCED 1997) and NUTS3 region. NUTS 2006 codes: Milan is ITC45
          (still including Monza) and the North-East uses ITD instead of ITH.
    2011  ISTAT census 2011, "Grado di istruzione della popolazione residente
          di 6 anni e piu" (bulk zip from IstatData).
    2021  ISTAT permanent census, dataflow DF_DCSS_ISTR_LAV_PEN_2_TV_1:
          resident population aged 9+ by educational attainment, provinces,
          2018-2024 (via the IstatData SDMX API: the nine cities and the
          North-West and North-East totals, one file each in permanent_census_2021/).

Files already present are not downloaded again.

Run from the project folder:  .venv/bin/python code/04_download_census.py
"""

import zipfile
from datetime import date
from pathlib import Path

import requests

OUT = Path("data/raw/census")
OUT.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0"}
log = []


def save(url, path, **kwargs):
    if path.exists():
        print("already downloaded", path)
        return
    response = requests.get(url, timeout=600, headers={**HEADERS, **kwargs.get("headers", {})})
    response.raise_for_status()
    path.write_bytes(response.content)
    log.append(f"{path.name}\t{date.today()}\t{len(response.content)} bytes\t{url}")
    print("saved", path)


# 2001: Eurostat
save("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/cens_01rews?format=TSV&compressed=true",
     OUT / "cens_01rews.tsv.gz")

# 2011: ISTAT bulk file
zip_2011 = OUT / "DICA_GRADOISTR-data.zip"
save("https://esploradati.istat.it/databrowser/DWL/censtatv5db/Popolazione/DICA_GRADOISTR-data.zip", zip_2011)
with zipfile.ZipFile(zip_2011) as z:
    z.extractall(OUT / "census_2011")

# 2021 (and 2018-2024): ISTAT permanent census. The server is slow (about a minute per
# request), so only what the analysis needs is downloaded: the nine cities of the project
# and the two macro-area totals, North-West (ITC) and North-East (ITD), which together are
# northern Italy. IstatData uses its own territory codes here: NUTS 2006-style codes
# (Milan = ITC45, North-East = ITD..) and IT108 for Monza.
needed = ["ITC", "ITD",                       # North-West and North-East totals
          "ITC11", "ITC33", "ITC45", "IT108",  # Turin, Genoa, Milan, Monza
          "ITD55", "ITD31", "ITD36",           # Bologna, Verona, Padua
          "ITC46", "ITC47"]                    # Bergamo, Brescia
# One request per area, saved one file per area so that an interrupted download can
# resume. All breakdowns are kept and filtered in the analysis.
parts_dir = OUT / "permanent_census_2021"
parts_dir.mkdir(exist_ok=True)
for code in needed:
    part = parts_dir / f"{code}.csv"
    if part.exists():
        continue
    url = f"https://esploradati.istat.it/SDMXWS/rest/data/IT1,DF_DCSS_ISTR_LAV_PEN_2_TV_1,1.0/A.{code}........"
    response = requests.get(url, timeout=600,
                            headers={**HEADERS, "Accept": "application/vnd.sdmx.data+csv;version=1.0.0"})
    response.raise_for_status()
    part.write_text(response.text)
    print("downloaded", code, flush=True)
log.append(f"permanent_census_2021/<area>.csv\t{date.today()}\t{len(needed)} areas\t"
           "https://esploradati.istat.it/SDMXWS/rest/data/IT1,DF_DCSS_ISTR_LAV_PEN_2_TV_1,1.0/A.<province>........")

(OUT / "download_log_census.txt").write_text("\n".join(log) + "\n")

"""Step 9: prepare the data files used by the interactive website (quarto/data/).

The website does no calculations of its own: it only draws what this script
exports from data/processed/ and outputs/tables/. It also downloads the official
EU province boundaries (Eurostat GISCO, NUTS 2021, 1:20 million) for the map and
keeps the 47 northern provinces.

Outputs in quarto/data/:
    shares.csv                share of northern Italy by province, year and measure
    provinces.csv             one row per northern province: growth and specialisation
    census_graduates.csv      copy of outputs/tables/part1_census_graduates.csv
    graduate_mobility.csv     BES graduate mobility, long format
    trains_vs_keeps.csv       copy of outputs/tables/part1_trains_vs_keeps.csv
    shift_share.csv           copy of outputs/tables/part2_shift_share.csv
    shift_share_by_sector.csv copy of outputs/tables/part2_local_effect_by_sector.csv
    north_provinces.geojson   boundaries of the 47 northern provinces

Run from the project folder, after steps 1-8:  .venv/bin/python code/09_site_data.py
"""

import json
from datetime import date
from pathlib import Path

import pandas as pd
import requests

from common import FIRST_YEAR, LAST_YEAR, NAMES

DATA, TAB, RAW = Path("data/processed"), Path("outputs/tables"), Path("data/raw")
OUT = Path("quarto/data")
OUT.mkdir(parents=True, exist_ok=True)
north = list(NAMES.values())

jobs = pd.read_csv(DATA / "jobs_by_sector.csv")
pop = pd.read_csv(DATA / "population.csv")
gdp = pd.read_csv(DATA / "gdp.csv")


def shares(df, value, label):
    df = df[df.province.isin(north)]
    wide = df.pivot_table(index="year", columns="province", values=value, aggfunc="sum")
    s = wide.div(wide.sum(axis=1), axis=0) * 100
    return s.stack().rename("share").reset_index().assign(measure=label)


knowledge = jobs[jobs.sector.isin(["J", "K", "M_N"])]
long = pd.concat([
    shares(jobs[jobs.sector == "TOTAL"], "jobs", "Jobs"),
    shares(knowledge, "jobs", "Knowledge jobs"),
    shares(knowledge[knowledge.sector != "K"], "jobs", "Knowledge jobs (without finance)"),
    shares(pop, "population", "Population"),
    shares(gdp, "gdp", "GDP"),
])
long.round(4).to_csv(OUT / "shares.csv", index=False)

# One row per province, for the map and the specialisation chart
w = jobs.pivot_table(index=["province", "year"], columns="sector", values="jobs")
w08, w23 = w.xs(FIRST_YEAR, level="year"), w.xs(LAST_YEAR, level="year")
p = pop.pivot_table(index="province", columns="year", values="population")
k08 = w08[["J", "K", "M_N"]].sum(axis=1)
k23 = w23[["J", "K", "M_N"]].sum(axis=1)
code_of = {v: k for k, v in NAMES.items()}
prov = pd.DataFrame({
    "code": [code_of[n] for n in north],
    "jobs_growth": (w23.TOTAL / w08.TOTAL - 1).loc[north] * 100,
    "knowledge_jobs_growth": (k23 / k08 - 1).loc[north] * 100,
    "population_growth": (p[LAST_YEAR] / p[FIRST_YEAR] - 1).loc[north] * 100,
    "manufacturing_lq_2008": ((w08.C / w08.TOTAL) / (w08.loc["Italy", "C"] / w08.loc["Italy", "TOTAL"])).loc[north],
    "jobs_2023_thousands": w23.TOTAL.loc[north],
}, index=north).rename_axis("province").reset_index()
prov.round(3).to_csv(OUT / "provinces.csv", index=False)

# Graduate mobility in long format
mob = pd.read_csv(TAB / "part1_graduate_mobility.csv", index_col=0)
mob = mob.drop(columns="average_2019_2023").stack().rename("net_per_1000").reset_index()
mob.columns = ["city", "year", "net_per_1000"]
mob.to_csv(OUT / "graduate_mobility.csv", index=False)

for src, dst in [("part1_census_graduates.csv", "census_graduates.csv"),
                 ("part1_trains_vs_keeps.csv", "trains_vs_keeps.csv"),
                 ("part2_shift_share.csv", "shift_share.csv"),
                 ("part2_local_effect_by_sector.csv", "shift_share_by_sector.csv")]:
    df = pd.read_csv(TAB / src).rename(columns={"Unnamed: 0": "city"})
    df.columns = [c.replace("_%", "_pct") for c in df.columns]  # simpler names for the website code
    df.to_csv(OUT / dst, index=False)

# Province boundaries (GISCO), downloaded once
url = ("https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/"
       "NUTS_RG_20M_2021_4326_LEVL_3.geojson")
raw_geo = RAW / "gisco" / "NUTS_RG_20M_2021_4326_LEVL_3.geojson"
if not raw_geo.exists():
    raw_geo.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    raw_geo.write_bytes(response.content)
    (raw_geo.parent / "download_log_gisco.txt").write_text(
        f"{raw_geo.name}\t{date.today()}\t{len(response.content)} bytes\t{url}\n")
geo = json.loads(raw_geo.read_text())


def signed_area(ring):
    """Shoelace formula: positive = anticlockwise (with x = longitude, y = latitude)."""
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:])) / 2


def rewind(polygon):
    """The map library (d3) expects outer rings clockwise and holes anticlockwise,
    the opposite of the GeoJSON standard used by GISCO."""
    return [r if (signed_area(r) < 0) == (i == 0) else r[::-1] for i, r in enumerate(polygon)]


geo["features"] = [f for f in geo["features"] if f["properties"]["NUTS_ID"] in NAMES]
for f in geo["features"]:
    g = f["geometry"]
    g["coordinates"] = (rewind(g["coordinates"]) if g["type"] == "Polygon"
                        else [rewind(poly) for poly in g["coordinates"]])
    f["properties"] = {"code": f["properties"]["NUTS_ID"], "province": NAMES[f["properties"]["NUTS_ID"]]}
assert len(geo["features"]) == 47, len(geo["features"])
(OUT / "north_provinces.geojson").write_text(json.dumps(geo))
print("site data written to", OUT, [p.name for p in sorted(OUT.iterdir())])

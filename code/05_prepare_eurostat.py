"""Step 5: tidy the Eurostat tables into small files for the analysis.

Keeps the 47 northern provinces, years 2008-2023 only (same methodology:
the provincial series has a break in 2008), and saves to data/processed/:

    jobs_by_sector.csv   jobs (thousands) by province, year and sector
    population.csv       average population (thousands) by province and year
    gdp.csv              GDP (million euro, current prices) by province and year

Run from the project folder:  .venv/bin/python code/05_prepare_eurostat.py
"""

from pathlib import Path

from common import FIRST_YEAR, LAST_YEAR, NAMES, NORTH, read_eurostat

RAW, OUT = Path("data/raw"), Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)
years = lambda df: df[df.year.between(FIRST_YEAR, LAST_YEAR)]

# Jobs by sector. These ten sectors do not overlap and add up to the total;
# C (manufacturing) is kept too, for the specialisation test (it is part of B-E).
SECTORS = ["A", "B-E", "F", "G-I", "J", "K", "L", "M_N", "O-Q", "R-U"]
jobs = read_eurostat(RAW / "nama_10r_3empers.tsv.gz")
jobs = years(jobs[(jobs.unit == "THS") & (jobs.wstatus == "EMP") & jobs.geo.isin(NORTH + ["IT"])
                  & jobs.nace_r2.isin(SECTORS + ["C", "TOTAL"])])
jobs = jobs[["geo", "year", "nace_r2", "value"]].rename(columns={"nace_r2": "sector", "value": "jobs"})

# Check: the ten sectors add up to the total in every province and year
wide = jobs.pivot_table(index=["geo", "year"], columns="sector", values="jobs")
gap = (wide[SECTORS].sum(axis=1) - wide["TOTAL"]).abs().max()
print(f"largest gap between sum of sectors and total: {gap:.1f} thousand jobs")
assert jobs.jobs.notna().all(), "missing job values"

pop = read_eurostat(RAW / "nama_10r_3popgdp.tsv.gz")
pop = years(pop[(pop.unit == "THS") & pop.geo.isin(NORTH + ["IT"])])
pop = pop[["geo", "year", "value"]].rename(columns={"value": "population"})

gdp = read_eurostat(RAW / "nama_10r_3gdp.tsv.gz")
gdp = years(gdp[(gdp.unit == "MIO_EUR") & gdp.geo.isin(NORTH + ["IT"])])
gdp = gdp[["geo", "year", "value"]].rename(columns={"value": "gdp"}).dropna()

for name, df in [("jobs_by_sector", jobs), ("population", pop), ("gdp", gdp)]:
    df.insert(1, "province", df.geo.map(NAMES).fillna("Italy"))
    df.to_csv(OUT / f"{name}.csv", index=False)
    print(f"saved {name}.csv: {df.geo.nunique()} areas, {df.year.min()}-{df.year.max()}")

"""Step 7 (Part 1, tests T2, T3, T8): who is moving?

Three pieces of evidence on graduates, the mobile factor in the
Forslid-Ottaviano model:

1. Census 2001, 2011, 2021: each city's share of northern Italy's graduates
   compared with its share of population (prediction P1: the mobile factor
   concentrates in Milan faster than people do). Milan and Monza are combined
   ("Milan area") because Monza was part of Milan in 2001.
   Graduates: 2001 ISCED 5-6; 2011 university degree + AFAM; 2021 bachelor's
   + master's/PhD. Definitions differ slightly, so only shares are compared.
2. ISTAT BES 2019-2023: net migration of Italian graduates aged 25-39 per 1,000
   resident graduates (P3: do graduates leave Turin?).
3. "Turin trains, Milan employs" (T8): each city's share of graduates *produced*
   by northern universities (USTAT, average 2019-2023) vs its share of
   *resident* graduates aged 25-49 (census 2021).

Outputs:
    outputs/tables/part1_census_graduates.csv
    outputs/tables/part1_graduate_mobility.csv
    outputs/tables/part1_trains_vs_keeps.csv
    outputs/figures/fig4_graduate_share_census.png
    outputs/figures/fig5_graduate_mobility.png
    outputs/figures/fig6_trains_vs_keeps.png

Run from the project folder:  .venv/bin/python code/07_part1_who_moves.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from common import CITY_COLOURS, INK, INK2, MUTED, NAMES, read_eurostat, style

RAW, FIG, TAB = Path("data/raw"), Path("outputs/figures"), Path("outputs/tables")
plt.rcParams.update({"font.family": "sans-serif", "font.size": 10})

CITIES6 = ["Milan area", "Turin", "Genoa", "Bologna", "Verona", "Padua", "Bergamo", "Brescia"]
names = {**NAMES, "ITC4C": "Milan area", "ITC4D": "Milan area"}
north_codes = list(NAMES)

# ---------------------------------------------------------------- 1. censuses
# 2001 (Eurostat, NUTS 2006 codes: Milan incl. Monza = ITC45; North-East = ITD)
c01 = read_eurostat(RAW / "census/cens_01rews.tsv.gz")
c01 = c01[(c01.wstatus == "POP") & (c01.age == "TOTAL") & (c01.sex == "T") & (c01.unit == "PER")]
c01["geo"] = c01.geo.str.replace("^ITD", "ITH", regex=True).replace({"ITC45": "ITC4C"})
c01 = c01[c01.geo.isin(north_codes)].pivot_table(index="geo", columns="isced97", values="value")
c01 = pd.DataFrame({"graduates": c01["ED5_6"], "population": c01["ED_NED"]})  # ED_NED = all levels

# 2011 (ISTAT; NUTS 2006 codes, Monza = IT108)
f11 = RAW / "census/census_2011/CSV - DATI CODICI E DESCRIZIONI - DATA AND DESCRIPTION/DICA_GRADOISTR-data-en.csv"
c11 = pd.read_csv(f11, sep="|", dtype=str)
c11 = c11[(c11.TIPO_DATO_CENS_POP == "RESPOP_AV") & (c11.SEXISTAT1 == "9") & (c11.ETA1 == "Y_GE6")
          & (c11.CITTADINANZA == "TOTAL") & (c11.ISO1 == "ALL")]
c11["geo"] = (c11.ITTER107.str.replace("^ITD", "ITH", regex=True)
              .replace({"ITC45": "ITC4C", "IT108": "ITC4D"}))
c11 = c11[c11.geo.isin(north_codes)]
c11["Value"] = pd.to_numeric(c11.Value)
c11 = c11.pivot_table(index="geo", columns="TITOLO_STUDIO", values="Value", aggfunc="sum")
c11 = pd.DataFrame({"graduates": c11["50"] + c11["34"], "population": c11["99"]})

# 2021 (ISTAT permanent census): one file per city plus the North-West (ITC) and
# North-East (ITD) totals, which together give northern Italy. ISTAT codes -> NUTS 2021.
p21 = pd.concat([pd.read_csv(f, dtype=str) for f in sorted((RAW / "census/permanent_census_2021").glob("*.csv"))])
p21["REF_AREA"] = p21.REF_AREA.replace({"ITC": "NORTH", "ITD": "NORTH"})
p21["REF_AREA"] = (p21.REF_AREA.str.replace("^ITD", "ITH", regex=True)
                   .replace({"ITC45": "ITC4C", "IT108": "ITC4D"}))
p21 = p21[(p21.INDICATOR == "RESPOP_AV") & (p21.GENDER == "T") & (p21.CITIZENSHIP == "TOTAL")
          & (p21.CUR_ACT_STAT == "99") & (p21.LOC_DEST == "ALL") & (p21.REAS_COMMUTING == "ALL")
          & (p21.TIME_PERIOD == "2021")]
p21["OBS_VALUE"] = pd.to_numeric(p21.OBS_VALUE)
tert = ["BL", "ML_RDD"]


def census21(age):
    """Graduates and population by area (cities + 'NORTH') in 2021, for one age group."""
    d = p21[p21.AGE_NOCLASS == age].pivot_table(index="REF_AREA", columns="EDU_ATTAIN", values="OBS_VALUE",
                                                aggfunc="sum")
    d = pd.DataFrame({"graduates": d[tert].sum(axis=1), "population": d["ALL"]})
    return d.groupby(d.index.map(lambda c: names.get(c, c))).sum()


c21 = census21("Y_GE9")
assert {"NORTH", *CITIES6} <= set(c21.index), "2021 census: missing cities or northern total"

rows = []
for year, df in [(2001, c01), (2011, c11), (2021, c21)]:
    if year < 2021:  # all 47 provinces available: northern total = their sum
        df = df.groupby(df.index.map(names)).sum()  # also combines Milan + Monza
        total = df.sum()
    else:            # northern total = North-West + North-East
        total = df.loc["NORTH"]
    share = df / total * 100
    for city in CITIES6:
        rows.append({"year": year, "city": city, "share_of_graduates": share.loc[city, "graduates"],
                     "share_of_population": share.loc[city, "population"],
                     "graduates_per_100_people": df.loc[city, "graduates"] / df.loc[city, "population"] * 100})
census = pd.DataFrame(rows)
census["graduate_concentration"] = census.share_of_graduates / census.share_of_population
census.round(3).to_csv(TAB / "part1_census_graduates.csv", index=False)
print(census.round(2).to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
for c in ["Milan area", "Turin", "Genoa"]:
    d = census[census.city == c]
    colour = CITY_COLOURS[c.replace(" area", "")]
    axes[0].plot(d.year, d.share_of_graduates, color=colour, linewidth=2, marker="o", markersize=6)
    axes[0].plot(d.year, d.share_of_population, color=colour, linewidth=1.5, linestyle="--")
    axes[0].text(2021.6, d.share_of_graduates.iloc[-1], c, va="center", fontsize=9, color=INK)
    axes[1].plot(d.year, d.graduate_concentration, color=colour, linewidth=2, marker="o", markersize=6)
    axes[1].text(2021.6, d.graduate_concentration.iloc[-1], f"{c} {d.graduate_concentration.iloc[-1]:.2f}",
                 va="center", fontsize=9, color=INK)
axes[0].set_title("Share of northern graduates (solid)\nand of population (dashed), %", loc="left", fontsize=11)
axes[1].axhline(1, color=MUTED, linestyle="--", linewidth=1)
axes[1].set_title("Graduate concentration:\nshare of graduates ÷ share of population", loc="left", fontsize=11)
for ax in axes:
    style(ax)
    ax.set_xticks([2001, 2011, 2021])
    ax.set_xlim(1999, 2027)
    ax.set_ylim(0, None)
fig.text(0.01, 0.01, "Milan area = Milan + Monza. Sources: Eurostat cens_01rews (2001); ISTAT census 2011; "
         "ISTAT permanent census 2021.", color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(FIG / "fig4_graduate_share_census.png", dpi=200)

# ---------------------------------------------------------------- 2. BES graduate mobility
bes = pd.read_excel(RAW / "bes_2025/Indicatori_per_provincia_sesso_ed.2025.xlsx", dtype=str)
it_names = {"Milano": "Milan", "Monza e della Brianza": "Monza-Brianza", "Torino": "Turin", "Genova": "Genoa",
            "Bologna": "Bologna", "Verona": "Verona", "Padova": "Padua", "Bergamo": "Bergamo", "Brescia": "Brescia",
            "Nord": "Northern Italy", "Italia": "Italy"}
mob = bes[(bes.CODICE == "11RIC025") & bes.SESSO.str.startswith("Tot") & bes.TERRITORIO.isin(it_names)]
years = [f"V{y}" for y in range(2019, 2024)]
mob = mob.set_index(mob.TERRITORIO.map(it_names))[years]
mob = mob.apply(lambda s: pd.to_numeric(s.str.replace(",", "."), errors="coerce"))
mob.columns = [int(c[1:]) for c in mob.columns]
mob["average_2019_2023"] = mob.mean(axis=1)
mob.round(1).to_csv(TAB / "part1_graduate_mobility.csv")
print("\nNet migration of graduates aged 25-39, per 1,000 resident graduates\n", mob.round(1).to_string())

order = ["Milan", "Turin", "Genoa", "Bologna", "Verona", "Padua", "Monza-Brianza", "Bergamo", "Brescia"]
fig, ax = plt.subplots(figsize=(8, 5))
vals = mob.loc[order[::-1], "average_2019_2023"]
colours = [CITY_COLOURS.get(c, "#86b6ef") for c in vals.index]
ax.barh(vals.index, vals, color=colours, height=0.6)
for i, v in enumerate(vals):
    ax.text(max(v, 0) + 0.8, i, f"{v:+.1f}", va="center", ha="left", fontsize=9, color=INK)
ax.axvline(0, color="#c3c2b7", linewidth=1)
north_avg = mob.loc["Northern Italy", "average_2019_2023"]
ax.axvline(north_avg, color=MUTED, linewidth=1, linestyle="--")
ax.text(north_avg + 0.4, len(vals) - 0.45, f"northern Italy {north_avg:+.1f}", fontsize=8, color=MUTED)
style(ax)
ax.grid(axis="y", visible=False)
ax.grid(axis="x", color="#e1e0d9", linewidth=0.8)
ax.set_xlabel("net graduates gained (+) or lost (−) per 1,000 resident graduates, average 2019–2023",
              color=INK2)
ax.set_title("Where do young graduates move? Net migration, ages 25–39", loc="left", color=INK, fontsize=12)
fig.text(0.01, 0.01, "Includes moves within Italy and abroad. 2023 provisional. Source: ISTAT, Bes dei "
         "territori 2025 (indicator 11RIC025).", color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(FIG / "fig5_graduate_mobility.png", dpi=200)

# ---------------------------------------------------------------- 3. trains vs keeps (T8)
u = pd.read_csv(RAW / "ustat_laureati_per_ateneo.csv", sep=";", encoding="latin-1")
u["province_code"] = u.AteneoCOD // 100  # USTAT code = ISTAT province code x 100 + number
northern_provinces = set(range(1, 41)) | {96, 97, 98, 99, 103, 108}
u = u[u.province_code.isin(northern_provinces) & ~u.AteneoNOME.str.contains("telematica")
      & u.AnnoS.between(2019, 2023)]
by_prov = u.groupby("province_code").Lau.sum() / 5  # average graduates per year
city_of = {1: "Turin", 10: "Genoa", 15: "Milan area", 37: "Bologna", 23: "Verona", 28: "Padua",
           16: "Bergamo", 17: "Brescia"}
produced = (by_prov / by_prov.sum() * 100).rename(index=city_of)

young = census21("Y25-49")
resident = young.graduates / young.loc["NORTH", "graduates"] * 100

t8 = pd.DataFrame({"share_of_graduates_produced_%": produced.reindex(CITIES6),
                   "share_of_resident_graduates_25_49_%": resident.reindex(CITIES6)})
t8["keeps_ratio"] = t8["share_of_resident_graduates_25_49_%"] / t8["share_of_graduates_produced_%"]
t8.round(2).to_csv(TAB / "part1_trains_vs_keeps.csv")
print("\nTurin trains, Milan employs?\n", t8.round(2).to_string())

fig, ax = plt.subplots(figsize=(8, 5))
x = range(len(t8))
ax.bar([i - 0.2 for i in x], t8.iloc[:, 0], width=0.38, color="#2a78d6", label="share of graduates produced by local universities")
ax.bar([i + 0.2 for i in x], t8.iloc[:, 1], width=0.38, color="#eb6834", label="share of graduates aged 25–49 living there")
ax.set_xticks(list(x))
ax.set_xticklabels(t8.index, fontsize=9)
style(ax)
ax.set_ylabel("% of northern Italy", color=INK2)
ax.set_title("Turin trains, Milan employs? Graduates produced vs graduates resident", loc="left",
             color=INK, fontsize=12)
ax.legend(frameon=False, fontsize=9)
fig.text(0.01, 0.01, "Produced: average 2019–2023, northern universities, online universities excluded (USTAT). "
         "Resident: census 2021 (ISTAT).", color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(FIG / "fig6_trains_vs_keeps.png", dpi=200)
print("figures saved")

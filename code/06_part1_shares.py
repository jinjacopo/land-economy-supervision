"""Step 6 (Part 1, tests T1, T4, T9): who is gaining share of northern Italy?

For each of the nine cities, computes its share of northern Italy's
(47 provinces) jobs, knowledge jobs, population and GDP, 2008-2023.

Knowledge jobs = ICT (J) + finance (K) + professional and administrative
services (M_N), as agreed in framework.md.

Home market ratio (prediction P4) = share of northern knowledge jobs divided
by share of northern population. Above 1 means the city has more than its
"fair share" of knowledge firms; rising means concentration is increasing.

Outputs:
    outputs/tables/part1_shares.csv
    outputs/figures/fig1_job_share_triangle.png
    outputs/figures/fig2_change_in_share.png
    outputs/figures/fig3_home_market_ratio.png

Run from the project folder:  .venv/bin/python code/06_part1_shares.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from common import CITIES, CITY_COLOURS, FIRST_YEAR, GROUPS, INK, INK2, LAST_YEAR, MUTED, NAMES, style

DATA, FIG, TAB = Path("data/processed"), Path("outputs/figures"), Path("outputs/tables")
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

jobs = pd.read_csv(DATA / "jobs_by_sector.csv")
pop = pd.read_csv(DATA / "population.csv")
gdp = pd.read_csv(DATA / "gdp.csv")
north = list(NAMES.values())


def shares(df, value):
    """Each province's share (%) of the northern total, by year."""
    df = df[df.province.isin(north)]
    wide = df.pivot_table(index="year", columns="province", values=value, aggfunc="sum")
    return wide.div(wide.sum(axis=1), axis=0) * 100


s_jobs = shares(jobs[jobs.sector == "TOTAL"], "jobs")
s_know = shares(jobs[jobs.sector.isin(["J", "K", "M_N"])], "jobs")
s_pop = shares(pop, "population")
s_gdp = shares(gdp, "gdp")
hm_ratio = s_know / s_pop

# Summary table: shares in the first and last year and their relative change
gdp_last = s_gdp.index.max()
rows = []
for group, cities in GROUPS.items():
    for c in cities:
        rows.append({
            "group": group, "city": c,
            "jobs_2008": s_jobs.loc[FIRST_YEAR, c], "jobs_2023": s_jobs.loc[LAST_YEAR, c],
            "knowledge_jobs_2008": s_know.loc[FIRST_YEAR, c], "knowledge_jobs_2023": s_know.loc[LAST_YEAR, c],
            "population_2008": s_pop.loc[FIRST_YEAR, c], "population_2023": s_pop.loc[LAST_YEAR, c],
            "gdp_2008": s_gdp.loc[FIRST_YEAR, c], f"gdp_{gdp_last}": s_gdp.loc[gdp_last, c],
            "home_market_ratio_2008": hm_ratio.loc[FIRST_YEAR, c],
            "home_market_ratio_2023": hm_ratio.loc[LAST_YEAR, c],
        })
table = pd.DataFrame(rows)
for m in ["jobs", "knowledge_jobs", "population"]:
    table[f"{m}_change_%"] = (table[f"{m}_{LAST_YEAR}"] / table[f"{m}_{FIRST_YEAR}"] - 1) * 100
table["gdp_change_%"] = (table[f"gdp_{gdp_last}"] / table["gdp_2008"] - 1) * 100
table.round(2).to_csv(TAB / "part1_shares.csv", index=False)
pd.set_option("display.width", 200)
print(table.round(2).to_string(index=False))

plt.rcParams.update({"font.family": "sans-serif", "font.size": 10})

# Figure 1: share of northern jobs, the three triangle cities
fig, ax = plt.subplots(figsize=(8, 4.5))
for c in ["Milan", "Turin", "Genoa"]:
    ax.plot(s_jobs.index, s_jobs[c], color=CITY_COLOURS[c], linewidth=2)
    ax.text(LAST_YEAR + 0.3, s_jobs.loc[LAST_YEAR, c], f"{c} {s_jobs.loc[LAST_YEAR, c]:.1f}%",
            va="center", color=INK, fontsize=9)
style(ax)
ax.set_ylim(0, None)
ax.set_xlim(FIRST_YEAR, LAST_YEAR + 3)
ax.set_xticks(range(FIRST_YEAR, LAST_YEAR + 1, 3))
ax.set_ylabel("% of all jobs in northern Italy", color=INK2)
ax.set_title("Share of northern Italy's jobs, 2008–2023", loc="left", color=INK, fontsize=12)
fig.text(0.01, 0.01, "Source: Eurostat nama_10r_3empers. Northern Italy = 47 provinces.", color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(FIG / "fig1_job_share_triangle.png", dpi=200)

# Figure 2: relative change in share, 2008-2023, for the nine cities and three measures
measures = [("jobs_change_%", "Jobs", "#2a78d6"),
            ("knowledge_jobs_change_%", "Knowledge jobs", "#eb6834"),
            ("population_change_%", "Population", "#1baf7a")]
fig, ax = plt.subplots(figsize=(8, 6))
order = table.set_index("city").loc[CITIES[::-1]]
y = range(len(order))
h = 0.26
for i, (col, label, colour) in enumerate(measures):
    ax.barh([v + (1 - i) * h for v in y], order[col], height=h - 0.03, color=colour, label=label)
ax.axvline(0, color="#c3c2b7", linewidth=1)
ax.set_yticks(list(y))
ax.set_yticklabels(order.index)
style(ax)
ax.grid(axis="y", visible=False)
ax.grid(axis="x", color="#e1e0d9", linewidth=0.8)
ax.set_xlabel("% change in the city's share of northern Italy, 2008 to 2023", color=INK2)
ax.set_title("Who gained share of northern Italy, 2008–2023?", loc="left", color=INK, fontsize=12)
ax.legend(frameon=False, loc="lower right", fontsize=9)
for pos in [2.5, 5.5]:  # separate the three groups of cities
    ax.axhline(pos, color="#e1e0d9", linewidth=0.8)
fig.text(0.01, 0.01, "Above 0: the city's share grew. Source: Eurostat nama_10r_3empers, nama_10r_3popgdp.",
         color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(FIG / "fig2_change_in_share.png", dpi=200)

# Figure 3: home market ratio over time
fig, ax = plt.subplots(figsize=(8, 4.5))
for c in ["Milan", "Turin", "Genoa"]:
    ax.plot(hm_ratio.index, hm_ratio[c], color=CITY_COLOURS[c], linewidth=2)
    ax.text(LAST_YEAR + 0.3, hm_ratio.loc[LAST_YEAR, c], f"{c} {hm_ratio.loc[LAST_YEAR, c]:.2f}",
            va="center", color=INK, fontsize=9)
ax.axhline(1, color=MUTED, linewidth=1, linestyle="--")
ax.text(FIRST_YEAR + 0.1, 0.85, "1 = knowledge jobs in proportion to population", color=MUTED, fontsize=8)
style(ax)
ax.set_xlim(FIRST_YEAR, LAST_YEAR + 3)
ax.set_xticks(range(FIRST_YEAR, LAST_YEAR + 1, 3))
ax.set_ylim(0, None)
ax.set_ylabel("share of knowledge jobs ÷ share of population", color=INK2)
ax.set_title("Home market ratio: knowledge jobs relative to population", loc="left", color=INK, fontsize=12)
fig.text(0.01, 0.01, "Knowledge jobs = ICT + finance + professional and administrative services. Source: Eurostat.",
         color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(FIG / "fig3_home_market_ratio.png", dpi=200)
print("figures saved")

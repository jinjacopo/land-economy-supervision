"""Step 8 (Part 2, tests T5 and T6): did Turin and Genoa stall because of their industries?

T5, shift-share. For a city and a period, the change in jobs is split into:

    national effect      = sum over sectors of  E_start * g_Italy
    industry-mix effect  = sum over sectors of  E_start * (g_sector_Italy - g_Italy)
    local effect         = sum over sectors of  E_start * (g_sector_city - g_sector_Italy)

where E_start is the city's jobs in a sector at the start of the period and g is a
growth rate over the period. The three add up exactly to the actual change.
Results are shown as % of the city's jobs at the start of the period.
Industry mix = hypothesis B (the city had declining industries); local = how the
city did within each industry, where Milan's pull (hypothesis A) would show up.
Periods: 2008-14 and 2014-23 (no years before 2008: series break).

Sectors: the Eurostat A*10 breakdown, with manufacturing (C) separated from the
rest of industry (B, D, E = mining, energy, water, waste).

Robustness: Turin's finance jobs jump from about 17,000 (2017) to 30,000 (2023),
possibly a change in where a large firm registers its staff. The local effect is
therefore also shown without finance.

T6, specialisation. For the 47 northern provinces: manufacturing location quotient
in 2008 (share of the province's jobs in manufacturing / same share for Italy)
against total job growth 2008-2023, with a straight-line fit.

Outputs:
    outputs/tables/part2_shift_share.csv
    outputs/tables/part2_local_effect_by_sector.csv   (all nine cities)
    outputs/tables/part2_specialisation.csv
    outputs/figures/fig7_shift_share.png
    outputs/figures/fig8_specialisation.png

Run from the project folder:  .venv/bin/python code/08_part2_industry.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import CITIES, CITY_COLOURS, INK, INK2, MUTED, NAMES, style

DATA, FIG, TAB = Path("data/processed"), Path("outputs/figures"), Path("outputs/tables")
plt.rcParams.update({"font.family": "sans-serif", "font.size": 10})

j = pd.read_csv(DATA / "jobs_by_sector.csv")
wide = j.pivot_table(index=["province", "year"], columns="sector", values="jobs")
wide["BDE"] = wide["B-E"] - wide["C"]  # industry other than manufacturing
SECTORS = ["A", "C", "BDE", "F", "G-I", "J", "K", "L", "M_N", "O-Q", "R-U"]
LABELS = {"A": "Agriculture", "C": "Manufacturing", "BDE": "Mining, energy, water", "F": "Construction",
          "G-I": "Trade, transport, hotels", "J": "ICT", "K": "Finance", "L": "Real estate",
          "M_N": "Professional & admin", "O-Q": "Public admin, education, health", "R-U": "Other services"}
assert (wide[SECTORS].sum(axis=1) - wide["TOTAL"]).abs().max() < 0.5
PERIODS = [(2008, 2014), (2014, 2023)]


def shift_share(city, t0, t1, sectors=SECTORS):
    e0, e1 = wide.loc[(city, t0), sectors], wide.loc[(city, t1), sectors]
    n0, n1 = wide.loc[("Italy", t0), sectors], wide.loc[("Italy", t1), sectors]
    g_it = n1.sum() / n0.sum() - 1          # Italy, all sectors
    g_sec = n1 / n0 - 1                     # Italy, each sector
    g_city = e1 / e0 - 1                    # city, each sector
    parts = pd.DataFrame({"national": e0 * g_it, "industry_mix": e0 * (g_sec - g_it),
                          "local": e0 * (g_city - g_sec)})
    assert abs(parts.values.sum() - (e1.sum() - e0.sum())) < 1e-6
    return parts, e0.sum()


rows, by_sector = [], []
for city in CITIES:
    for t0, t1 in PERIODS:
        parts, start = shift_share(city, t0, t1)
        no_k, start_no_k = shift_share(city, t0, t1, [s for s in SECTORS if s != "K"])
        tot = parts.sum()
        rows.append({"city": city, "period": f"{t0}-{t1}", "jobs_start_thousands": start,
                     "actual_change_%": (tot.sum()) / start * 100,
                     "national_%": tot.national / start * 100,
                     "industry_mix_%": tot.industry_mix / start * 100,
                     "local_%": tot.local / start * 100,
                     "local_without_finance_%": no_k.local.sum() / start_no_k * 100})
        for s, r in parts.iterrows():
            by_sector.append({"city": city, "period": f"{t0}-{t1}", "sector": LABELS[s],
                              "national_thousand_jobs": r.national,
                              "industry_mix_thousand_jobs": r.industry_mix,
                              "local_thousand_jobs": r.local})
ss = pd.DataFrame(rows)
ss.round(2).to_csv(TAB / "part2_shift_share.csv", index=False)
pd.set_option("display.width", 200)
print(ss.round(1).to_string(index=False))
bs = pd.DataFrame(by_sector)
bs.round(2).to_csv(TAB / "part2_local_effect_by_sector.csv", index=False)
print("\nTurin and Genoa, effects by sector (thousand jobs)")
print(bs[bs.city.isin(["Turin", "Genoa"])].round(1).to_string(index=False))

# Figure 7: shift-share components for the triangle, two periods
fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), sharey=True)
comp = [("national_%", "National effect", "#86b6ef"), ("industry_mix_%", "Industry-mix effect (B)", "#eb6834"),
        ("local_%", "Local effect (A)", "#2a78d6")]
triangle = ["Milan", "Turin", "Genoa"]
for ax, (t0, t1) in zip(axes, PERIODS):
    d = ss[(ss.period == f"{t0}-{t1}")].set_index("city").loc[triangle[::-1]]
    y = np.arange(len(d))
    h = 0.24
    for i, (col, label, colour) in enumerate(comp):
        ax.barh(y + (1 - i) * h, d[col], height=h - 0.03, color=colour, label=label)
    ax.scatter(d["actual_change_%"], y, marker="D", s=40, color=INK, zorder=3, label="Actual change")
    for yi, v in zip(y, d["actual_change_%"]):
        ax.text(v, yi - 0.42, f"total {v:+.1f}%", ha="center", fontsize=8, color=INK2)
    ax.axvline(0, color="#c3c2b7", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(d.index)
    style(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color="#e1e0d9", linewidth=0.8)
    ax.set_title(f"{t0}–{t1}", loc="left", fontsize=11, color=INK)
    ax.set_xlabel("% of the city's jobs at the start of the period", color=INK2)
axes[1].legend(frameon=False, fontsize=8, loc="lower right")
fig.suptitle("Shift-share: why did jobs change in the old industrial triangle?", x=0.01, ha="left",
             fontsize=12, color=INK)
fig.text(0.01, 0.01, "Reference: Italy. 11 sectors, manufacturing separate. Source: Eurostat nama_10r_3empers.",
         color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 0.95))
fig.savefig(FIG / "fig7_shift_share.png", dpi=200)

# T6: specialisation across the 47 northern provinces
north = list(NAMES.values())
w08, w23 = wide.xs(2008, level="year"), wide.xs(2023, level="year")
lq = (w08["C"] / w08["TOTAL"]) / (w08.loc["Italy", "C"] / w08.loc["Italy", "TOTAL"])
growth = (w23["TOTAL"] / w08["TOTAL"] - 1) * 100
spec = pd.DataFrame({"manufacturing_LQ_2008": lq, "job_growth_2008_2023_%": growth}).loc[north]
slope, intercept = np.polyfit(spec.iloc[:, 0], spec.iloc[:, 1], 1)
spec["predicted_growth_%"] = intercept + slope * spec.iloc[:, 0]
spec["above_or_below_line_pp"] = spec.iloc[:, 1] - spec["predicted_growth_%"]
r = np.corrcoef(spec.iloc[:, 0], spec.iloc[:, 1])[0, 1]
spec.sort_values("manufacturing_LQ_2008").round(2).to_csv(TAB / "part2_specialisation.csv")
print(f"\nT6: slope {slope:.2f} pp of growth per +1 in LQ; correlation {r:.2f}; R2 {r**2:.2f}; n={len(spec)}")
print(spec.loc[["Milan", "Turin", "Genoa", "Bologna", "Verona", "Padua", "Bergamo", "Brescia",
                "Monza-Brianza"]].round(2).to_string())

fig, ax = plt.subplots(figsize=(8, 5.5))
others = spec.drop(index=list(CITY_COLOURS))
ax.scatter(others.iloc[:, 0], others.iloc[:, 1], s=45, color="#86b6ef", edgecolor="white", linewidth=1,
           label="other northern provinces")
for c, colour in CITY_COLOURS.items():
    ax.scatter(spec.loc[c].iloc[0], spec.loc[c].iloc[1], s=70, color=colour, edgecolor="white", linewidth=1.5,
               zorder=3)
    ax.annotate(c, (spec.loc[c].iloc[0], spec.loc[c].iloc[1]), xytext=(6, 4), textcoords="offset points",
                fontsize=9, color=INK)
for c in ["Bologna", "Verona", "Padua", "Bergamo", "Brescia"]:
    point = spec.loc[c].iloc[0], spec.loc[c].iloc[1]
    ax.scatter(*point, s=45, color=INK2, edgecolor="white", linewidth=1, zorder=3)
    left = c == "Bologna"  # Bologna has a close neighbour on its right
    ax.annotate(c, point, xytext=(-6 if left else 6, 4), textcoords="offset points",
                ha="right" if left else "left", fontsize=8, color=INK2)
xs = np.linspace(spec.iloc[:, 0].min(), spec.iloc[:, 0].max(), 50)
ax.plot(xs, intercept + slope * xs, color=MUTED, linewidth=1.5, linestyle="--")
ax.axvline(1, color="#e1e0d9", linewidth=1)
ax.axhline(0, color="#c3c2b7", linewidth=1)
style(ax)
ax.grid(axis="x", color="#e1e0d9", linewidth=0.8)
ax.set_xlabel("manufacturing specialisation in 2008 (location quotient; 1 = Italian average)", color=INK2)
ax.set_ylabel("job growth 2008–2023, %", color=INK2)
ax.set_title("Did manufacturing-specialised provinces grow less?", loc="left", color=INK, fontsize=12)
ax.text(0.99, 0.02, f"dashed line: best fit, slope {slope:+.1f} pp per +1 LQ, correlation {r:.2f}",
        transform=ax.transAxes, ha="right", fontsize=8, color=MUTED)
fig.text(0.01, 0.01, "47 northern provinces. Source: Eurostat nama_10r_3empers.", color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(FIG / "fig8_specialisation.png", dpi=200)
print("figures saved")

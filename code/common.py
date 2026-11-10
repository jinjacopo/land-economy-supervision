"""Shared helpers: reading Eurostat files, province names and chart colours."""

import numpy as np
import pandas as pd

# The 47 provinces of northern Italy (NUTS 2021 codes; NUTS1 ITC North-West + ITH North-East)
NAMES = {
    "ITC11": "Turin", "ITC12": "Vercelli", "ITC13": "Biella", "ITC14": "Verbano-Cusio-Ossola",
    "ITC15": "Novara", "ITC16": "Cuneo", "ITC17": "Asti", "ITC18": "Alessandria",
    "ITC20": "Aosta", "ITC31": "Imperia", "ITC32": "Savona", "ITC33": "Genoa",
    "ITC34": "La Spezia", "ITC41": "Varese", "ITC42": "Como", "ITC43": "Lecco",
    "ITC44": "Sondrio", "ITC46": "Bergamo", "ITC47": "Brescia", "ITC48": "Pavia",
    "ITC49": "Lodi", "ITC4A": "Cremona", "ITC4B": "Mantua", "ITC4C": "Milan",
    "ITC4D": "Monza-Brianza", "ITH10": "Bolzano", "ITH20": "Trento", "ITH31": "Verona",
    "ITH32": "Vicenza", "ITH33": "Belluno", "ITH34": "Treviso", "ITH35": "Venice",
    "ITH36": "Padua", "ITH37": "Rovigo", "ITH41": "Pordenone", "ITH42": "Udine",
    "ITH43": "Gorizia", "ITH44": "Trieste", "ITH51": "Piacenza", "ITH52": "Parma",
    "ITH53": "Reggio Emilia", "ITH54": "Modena", "ITH55": "Bologna", "ITH56": "Ferrara",
    "ITH57": "Ravenna", "ITH58": "Forli-Cesena", "ITH59": "Rimini",
}
NORTH = list(NAMES)

# The nine cities of the project, in the order used in tables and charts
GROUPS = {
    "Old industrial triangle": ["Milan", "Turin", "Genoa"],
    "Successful comparison": ["Bologna", "Verona", "Padua"],
    "Around Milan": ["Monza-Brianza", "Bergamo", "Brescia"],
}
CITIES = [c for group in GROUPS.values() for c in group]

FIRST_YEAR, LAST_YEAR = 2008, 2023  # same methodology only (series break in 2008)

# Chart colours (validated default palette of the dataviz guidelines)
INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
CITY_COLOURS = {"Milan": "#2a78d6", "Turin": "#eb6834", "Genoa": "#1baf7a"}


def read_eurostat(path):
    """Read a Eurostat TSV (wide, one column per year) into a long table."""
    df = pd.read_csv(path, sep="\t")
    first = df.columns[0]
    keys = first.split("\\")[0].split(",")
    df[keys] = df[first].str.split(",", expand=True)
    df = df.drop(columns=first)
    df.columns = [c.strip() for c in df.columns]
    df = df.melt(id_vars=keys, var_name="year", value_name="value")
    # Values can carry flags such as "123.4 p" or ":" for missing
    df["value"] = pd.to_numeric(
        df["value"].astype(str).str.replace(r"[^0-9.\-]", "", regex=True).replace("", np.nan),
        errors="coerce",
    )
    df["year"] = df["year"].astype(int)
    return df


def style(ax):
    """Recessive axes and grid, as in the dataviz guidelines."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c3c2b7")
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_facecolor(SURFACE)

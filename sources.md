# Sources

All files are downloaded by the scripts in `code/` and saved, unchanged, in `data/raw/`. That folder is not committed (see `.gitignore`); run the scripts to re-create it. Download dates are in `data/raw/download_log_*.txt`.

## Dataset 1: Eurostat regional employment by sector

- Provider and URL: Eurostat, table `nama_10r_3empers`, https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nama_10r_3empers?format=TSV&compressed=true
- Version / dates: downloaded 2026-11-09; years 2000–2023 for Italy (2024 not yet published).
- Download steps: `code/01_download_eurostat.py`
- Coverage and unit of observation: NUTS3 regions (Italian provinces); 47 provinces in northern Italy (NUTS1 ITC North-West + ITH North-East). Monza (ITC4D) has back-calculated figures from 2000.
- Variables and units: employment, thousand persons (`unit=THS`, `wstatus=EMP`), by NACE Rev. 2 sector: A, B-E, C (manufacturing), F, G-I, J (ICT), K (finance), L, M_N (professional + administrative services), O-Q, R-U, TOTAL. Employment is counted by place of work.
- Access / reuse terms: Eurostat copyright policy, free reuse with acknowledgement.
- Note: Milan's and Turin's totals jump between 2007 and 2008 (Milan +5.4%), while northern Italy grows by only 0.7%. This is a possible break in the provincial series, to be checked.

## Dataset 2: Eurostat GDP and population by province

- Provider and URL: Eurostat, tables `nama_10r_3gdp` (GDP at current market prices) and `nama_10r_3popgdp` (average annual population, thousands), same API as above.
- Version / dates: downloaded 2026-11-09; population 2000–2024.
- Download steps: `code/01_download_eurostat.py`
- Coverage and unit of observation: NUTS3 regions.
- Access / reuse terms: as above.

## Dataset 3: ISTAT, "Bes dei territori", 2025 edition

- Provider and URL: ISTAT, https://www.istat.it/notizia/bes-dei-territori-edizione-2025/ (zip: https://www.istat.it/wp-content/uploads/2025/06/Bes_dei_territori_edizione_2025.zip)
- Version / dates: 2025 edition (latest; no 2026 edition found on 2026-11-09).
- Download steps: `code/02_download_istat_bes.py`
- Coverage and unit of observation: 107 provinces and metropolitan cities.
- Variables and units:
  - `02IST003P-N22`, graduates and other tertiary qualifications, aged 25–39, % of population. **Years 2018–2024 only** (new series after the 2021 change to the labour force survey).
  - `11RIC025`, mobility of Italian graduates aged 25–39: net migration balance of graduates per 1,000 resident graduates; positive means the province gains graduates. **Years 2019–2023 only**; 2023 provisional. Source: population registers (changes of residence). Earlier editions (2021, 2023) do not have a longer series.
- Access / reuse terms: ISTAT, CC BY 3.0 IT.

## Dataset 4: Ministry of University (USTAT), graduates by university

- Provider and URL: MUR, Ufficio di Statistica, "Laureati per ateneo", https://dati-ustat.mur.gov.it/dataset/laureati/resource/88acd482-9d75-44d1-ab16-aa04524f5d94
- Version / dates: downloaded 2026-11-09; years 2001–2025.
- Download steps: `code/03_download_ustat.py`
- Coverage and unit of observation: university, year (calendar year of graduation), sex.
- Variables and units: number of graduates. Turin = Università di Torino (101) + Politecnico di Torino (102); Milan = Statale, Politecnico, Bocconi, Cattolica, IULM, San Raffaele, Bicocca, Humanitas; Genoa = Università di Genova. File encoding is Latin-1, separator `;`.
- Access / reuse terms: Italian Open Data License v2.0 (IODL 2.0).

## Dataset 5: Population censuses 2001, 2011, 2021 (graduates by province)

- Provider and URL:
  - 2001: Eurostat, table `cens_01rews`, https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/cens_01rews?format=TSV&compressed=true
  - 2011: ISTAT census 2011, "Grado di istruzione della popolazione residente di 6 anni e più", bulk file https://esploradati.istat.it/databrowser/DWL/censtatv5db/Popolazione/DICA_GRADOISTR-data.zip
  - 2021: ISTAT permanent census, IstatData dataflow `DF_DCSS_ISTR_LAV_PEN_2_TV_1` (resident population aged 9+ by educational attainment, 2018–2024), SDMX API https://esploradati.istat.it/SDMXWS/rest/data/IT1,DF_DCSS_ISTR_LAV_PEN_2_TV_1,1.0/A.<province>........
- Version / dates: downloaded 2026-11-09.
- Download steps: `code/04_download_census.py` (the 2021 part is slow, about a minute per province, and resumes if interrupted).
- Coverage and unit of observation: provinces. Territory codes differ between sources: 2001 uses NUTS 2006 (Milan incl. Monza = ITC45; North-East = ITD); 2011 and 2021 use ISTAT codes (Milan = ITC45, Monza = IT108, North-East = ITD). All are converted to NUTS 2021 in the analysis, with Milan and Monza combined as "Milan area".
- Variables and units: number of residents by highest qualification.
  - Graduates in 2001: ISCED 1997 levels 5–6.
  - Graduates in 2011: university degree (code 50) + post-secondary AFAM diploma (34).
  - Graduates in 2021: bachelor's/first-level diploma (BL) + master's/PhD (ML_RDD).
  - Population: all residents aged 6+ (2001, 2011) or 9+ (2021).
  - Definitions differ slightly, so only *shares* of the northern total are compared.
- Access / reuse terms: Eurostat copyright policy; ISTAT CC BY 3.0 IT.

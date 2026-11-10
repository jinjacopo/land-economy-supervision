# Framework: assumptions, hypotheses and tests

*Agreed on 2026-11-09, before looking at any data; methodology agreed the same day. Question and scope: see `question.md`.*

## How the project works

1. **Assumptions:** what I take as given. They come from the core–periphery model, and I judged each one believable using my own observations of Turin and Milan.
2. **Hypotheses:** three possible answers (A, B, C) to why Milan is pulling away while Turin and Genoa stall.
3. **Tests:** I check each hypothesis against actual data, and only then reach a conclusion that supports or rejects A, B or C.

My personal observations are used to *generate ideas and judge whether assumptions are believable*, never as evidence. Each one is paired with a way to check it in data.

## 1. Assumptions

| # | Assumption | In plain words |
| --- | --- | --- |
| 1 | Graduates move to wherever their career prospects are better | A graduate compares Turin and Milan on wages *and* the number and variety of suitable jobs, and moves if Milan is better. |
| 2 | Firms need to be near skilled workers and near customers | This is why firms follow graduates, and graduates then follow firms: the loop at the heart of the model. |
| 3 | Manufacturing workers stay put | Their skills fit one local industry (cars in Turin), so moving would cost them. Their spending keeps Turin's local economy going. |
| 4 | The cost of doing business between cities has fallen | EU integration, the euro and digital tools made it easier for one city to serve a whole region. In the model, this starts the move towards a single core. |
| 5 | We can treat it as Milan against the rest | The model has two regions; we have nine provinces. We simplify by comparing Milan with each other city. |

### Assumption 1: details

- **Model version:** graduates move to the city with the higher real wage (salary after living costs).
- **Adjusted version:** graduates move to wherever their **career prospects** are better ("labour market matching": a bigger market has more employers and better job fits). Matching is not in the basic model, but it pushes the same way: it makes the big city even more attractive.

| What I observe | What it would mean if true in general | How we could check it |
| --- | --- | --- |
| Students move to Milan to study | Milan's universities attract students from Turin and elsewhere | University enrolment by students' home province (Ministry of University data) |
| Graduates move to Milan for jobs after graduating | Turin loses graduates to Milan | ISTAT changes of residence by education; AlmaLaurea surveys on where graduates work |
| Finance has its offices in Milan, not Turin (from my internship search) | Finance jobs are concentrated in Milan | Jobs in finance by province (Eurostat) compared with each city's share of all jobs |

- **Example to verify:** Intesa Sanpaolo's registered office is (I believe) in Turin, but finance graduate jobs are mostly in Milan. *To check myself.*

### Assumption 2: details

| What I observe | What it would mean if true in general | How we could check it |
| --- | --- | --- |
| At the Politecnico di Torino, the big firms offering opportunities to students are mainly Intesa Sanpaolo and Stellantis; the rest are traditional small and medium enterprises | Turin has few large employers of graduates, so fewer and less varied skilled jobs, which makes Milan more attractive to talent from all over Italy | Number of large firms (250+ employees) and their employment by province (ISTAT business register, ASIA); where Politecnico graduates end up working (AlmaLaurea) |

- **Caveat to check:** Turin does have other large firms with headquarters there (e.g. Reply, Lavazza, Iveco Group, Leonardo's aerospace activities). The point may be less "there are only two big firms" and more "big firms that recruit graduates in *many different fields* are concentrated in Milan". The data on large firms by province will show which is true.
- **Link to hypothesis B:** if many of Turin's small and medium firms are suppliers to the car industry, the city depends on one industry even more than its big firms suggest.

## 2. Hypotheses

| | Hypothesis | The story in one sentence |
| --- | --- | --- |
| **A** | **Milan's pull** (inside the core–periphery model) | Graduates move to Milan, firms follow them, so Milan becomes even more attractive and draws more graduates, while Turin is left behind. |
| **B** | **Industry decline** (a shock from outside the model) | Cars, steel and shipbuilding shrank for global reasons. Turin and Genoa stalled because they depended on them, and would have stalled even without Milan. |
| **C** | **Both, in sequence** (the answer I find most realistic) | The industry decline weakened Turin first, then Milan's pull made it worse. |

## 3. Methodology

Two parts, one for each half of the question.

### Part 1: Is the North becoming a single core around Milan?

**Theory:** Forslid & Ottaviano (2003), the footloose entrepreneur version of Krugman's core–periphery model.

- **Skilled workers (graduates)** can move, to wherever their real wage (for us: career prospects) is higher.
- **Unskilled workers (the less mobile population, incl. manufacturing workers with industry-specific skills)** stay where they are.
- **Knowledge-intensive firms** need skilled workers to exist, hire unskilled workers to produce, and have increasing returns, so they locate where the skilled workers are.
- **Traditional activity** uses only unskilled workers and is spread everywhere.
- **Mechanism:** when trade between regions gets cheaper, a small advantage grows (more graduates → more firms → more varied jobs → more graduates). Past the break point, skilled workers and their firms concentrate in one region; the unskilled stay.

| Model prediction | What we measure | Test |
| --- | --- | --- |
| P1. The mobile factor concentrates | Milan's share of graduates aged 25–39 among the nine cities; graduate mobility (ISTAT BES) | T2 |
| P2. Firms follow the skilled | Milan's share of jobs in ICT, finance and professional services | T2 |
| P3. The immobile stay | Turin's population vs its graduate mobility | T3 |
| P4. Home market effect: the core has a more than proportional share of knowledge firms | Milan's share of knowledge jobs ÷ its share of population (above 1 and rising) | T1 |
| P5. Everyone else loses share, even the successful cities | Shares of Bologna, Verona, Padua | T4 |
| P6. The core spreads into its surroundings as Milan gets more expensive (Helpman 1998) | Growth of Monza, Bergamo, Brescia | T9 |
| "Turin trains, Milan employs" | Graduates produced by Turin's universities (USTAT) vs Turin's graduate mobility (BES) | T8 |

- **Presentation:** one set of charts on shares over time (T1, T4, T9) and one on who moves (T2, T3, T8 together).
- **Measure:** jobs and population, not GDP per head (Milan's GDP per head is inflated by commuters). A job located in Milan is part of the core wherever its worker lives.
- **Limit:** the model's end state is either an even split or full concentration; reality is in between. We test the *direction* of change, not whether full concentration has been reached.

### Part 2: Did Turin and Genoa stall because their industries declined?

**Theory:** hypothesis B (an external shock to their industries) and hypothesis C (shock, then amplification by Milan's pull). T5 looks closely at the two old industrial-triangle cities; T6 checks whether the pattern holds across the whole North.

#### T5: shift-share analysis for Turin and Genoa (with Milan for comparison)

A standard method in regional economics (not in the Michaelmas lecture list; see Dunn 1960). Splits the change in a city's employment between two years, $\Delta E$, into three parts:

$$\Delta E_{city} = \text{National effect} + \text{Industry-mix effect} + \text{Local effect}$$

- **National effect:** jobs the city would have gained if every one of its industries had grown at the Italian average.
- **Industry-mix effect:** the extra gain or loss from having industries that did well or badly nationally. This is the external shock, **hypothesis B**.
- **Local effect:** what is left: how the city did *within* the same industries compared with Italy. This is where Milan's pull would show up, **hypothesis A**, the model's mechanism.

**Periods:** 2008–14 (from the financial crisis to the Fiat–Chrysler merger) and 2014–23 (up to and after Stellantis, 2021). Years before 2008 are not used, because the provincial job series has a methodological break in 2008 (see Limitations).

| If... | Industry-mix effect | Local effect |
| --- | --- | --- |
| A is right | Small | Negative in all periods |
| B is right | Large and negative | Close to zero |
| C is right | Negative early | More negative in later periods |

#### T6: manufacturing specialisation across the whole North

- **Measure:** each northern province's location quotient for manufacturing in 2008 (its share of jobs in manufacturing ÷ Italy's share), plotted against its job growth 2008–23. One point per province, for all ~47 northern provinces.
- **If B is right:** a downward slope (more specialised → slower growth).
- **Turin and Genoa:** on the line means their slow growth is what their specialisation predicts (supports B); below the line means they did worse than specialisation explains (supports A or C).
- **Possible finding:** Emilia-Romagna and Veneto are also very specialised in manufacturing and did well. A flat slope would suggest that *which* manufacturing and *how it is organised* (a few big firms vs many SMEs) matter more than manufacturing as such.

### Limitations

- **Manufacturing is treated as one broad sector.** Eurostat does not separate cars from food or machinery. In T5, part of the car industry's decline may be counted in the local effect instead of the industry-mix effect, which biases the test *against* hypothesis B. In T6, the location quotient measures manufacturing in general, not dependence on cars or heavy industry. (Possible extension if time allows: ISTAT business censuses 2001 and 2011, which separate car manufacturing.)
- The results show patterns and direction of change, not proof of cause.
- **Graduate data by province is short (checked 2026-11-09).** ISTAT BES has graduates aged 25–39 only for 2018–2024 and graduate mobility only for 2019–2023. So the graduate side of T2/T3 and the timing test against the 2008 and 2014 shocks cannot use BES. Over 2008–2023, the "who moves" side relies on knowledge jobs (Eurostat). For the long run, graduates by province come from the population censuses (2001, 2011, 2021). The censuses are a separate source, not affected by the 2008 break, but the 2021 census is register-based while 2001 and 2011 were traditional counts, so only *shares* (not levels) are compared. Milan and Monza are combined in the census comparison, because Monza was still part of Milan in 2001.
- **Series break in 2008 (checked 2026-11-09): only 2008–2023 is used for jobs and GDP.** Regional totals are smooth through 2008, but jobs are reallocated between provinces within each region in that year: the average gap between a province's growth and its region's is 2.5 percentage points in 2008, against about 1 in other years; Milan +5.4% vs Lombardy +0.9%. The likely cause is the switch to the NACE Rev. 2 classification in 2008, with earlier provincial figures estimated backwards. Decision: use only years with the same methodology, 2008–2023. Cost: the years before the crisis are lost, so hypothesis C's "industry decline first" is tested from 2008 onwards.

### Data (to check and download next)

| Source | Use |
| --- | --- |
| Eurostat `nama_10r_3empers` (jobs by province and sector; used 2008–2023) | T1, T2, T4, T5, T6, T9 |
| Eurostat `nama_10r_3gdp` and provincial population tables | T1, T3, T4, T9 |
| ISTAT BES dei territori (graduate mobility; share of graduates aged 25–39) | T2, T3, T8 |
| Ministry of University, USTAT (graduates produced by university) | T8 |

## Focus: "Turin trains, Milan employs"

*An important part of the project, not the headline. The question in `question.md` is unchanged.*

- **The idea:** Turin is a big university city (Politecnico, University of Turin), so it may *produce* many graduates but not *keep* them; Milan employs them.
- **Why it matters:** it is the sharpest test of hypothesis A, because A is mainly about graduates moving.
- **Link to the model:** graduates are the mobile factor, while universities cannot move. Turin can keep producing the mobile factor while losing it to the core.
- **Link to hypothesis C:** if the industry decline triggered the drain, graduates should leave Turin *more* after the shocks (2008–09, 2014, 2021) than before.
- **Test:** T8, shown together with T2 and T3 in Part 1 of the methodology.
- **Data risk:** depends on finding data on where graduates go after university (AlmaLaurea, ISTAT). Not yet checked. If unavailable, it stays as an untested hypothesis.

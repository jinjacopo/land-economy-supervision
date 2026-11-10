# Report

## Question

Is northern Italy collapsing into a single core around Milan, as the core–periphery model predicts, or did the old industrial cities (Turin, Genoa) stall because of what they specialised in? Or did the decline of their industries trigger the move towards Milan? (Full framing, theory and hypotheses A, B and C: `question.md` and `framework.md`.)

**Conclusion.** Northern Italy is not collapsing into a single core around Milan. Milan is the North's strongest labour market, and its lead in jobs has grown. But graduates and knowledge jobs, the mobile factors that the core–periphery model says should concentrate in the core, are no more concentrated in Milan today than they were in 2008 (knowledge jobs) or 2001 (graduates), and several other cities have grown alongside it. Turin's and Genoa's weaker performance is better explained by problems specific to each city than by Milan's pull.

## Findings

**Is the North becoming a single core?** Milan's share of northern jobs rose from 14.2% to 15.9% between 2008 and 2023. That is about twice the relative increase in its population share (11.2% to 11.8%), and Milan beat national trends in almost every sector. However, its home market ratio for knowledge jobs barely moved (2.20 in 2008, 2.19 in 2023), and its graduate concentration ratio did not rise (1.36 in 2001, 1.32 in 2021). Bologna, Verona and Padua all increased their share of northern jobs (+5% to +9%) and knowledge jobs (+7% to +13%). Bologna attracts more young graduates relative to its graduate population than Milan does (+40 against +36 per 1,000). Turin also gains young graduates on net (+14 per 1,000, above the northern average of +9.5). Where Milan does reshape its surroundings, it does so as a place to live rather than to work. Monza, Bergamo and Brescia gained population share but lost 6–8% of their knowledge-job share. This is consistent with Milan's housing costs pushing residents outwards while the jobs stay in the city, although housing costs were not measured here.

**Did Turin and Genoa stall because of their industries?** Manufacturing in general does not explain slow growth. Manufacturing specialisation in 2008 is uncorrelated with job growth from 2008 to 2023 across the 47 northern provinces (r = −0.09). Verona (1.29) and Padua (1.40) are more specialised in manufacturing than Turin (1.21), and Bologna about as specialised (1.19), yet they grew about 11–15% while Turin grew 3%. Turin's weakness instead has a specific timing and a specific sector. Between 2008 and 2014, Turin matched Italy's performance, with services offsetting manufacturing losses. After 2014 it fell behind within sectors: manufacturing employment ran 14,300 jobs below national trends and ICT ran 11,200 below. The manufacturing gap is most likely the car industry, although the sector data cannot isolate it. Genoa's decline is of a different kind. Its −5.2% local effect after 2014 is concentrated in trade, transport and hotels (−15,600 jobs), a group that includes the port and logistics. Genoa also lost 8% of its population share and 10% of its GDP share.

## Interpretation and limitations

**Which hypothesis fits?** Hypothesis A fails in its strong form: Milan grows, but it does not absorb the North. Hypothesis B holds only in a narrow form. Turin's problem lies in its particular industry, not in manufacturing as such. Hypothesis C fits Turin's timing (no underperformance during the crisis, then decline after 2014 that spreads into ICT). Its mechanism is not visible in the data, however: Turin shows no graduate outflow, and knowledge jobs are not shifting to Milan. The best overall account combines a narrow version of B for Turin with a separate, logistics-related decline for Genoa, while Milan grows alongside other cities rather than at their expense.

**What the theory gets right and wrong.** The two-region core–periphery model assumes a single core, but the North is polycentric: Milan, Bologna and the Veneto all grow, so agglomeration gains are spread across several centres. The model's dispersion forces are visible, in the form of housing costs (Helpman, 1998) spreading Milan's population into its belt. Martin's (1999) critique also applies, because the model ignores firm structure and institutions. Turin's industry has historically been organised around one dominant car producer, while Bologna and the Veneto are known for networks of SMEs. This difference, which this project did not measure, may explain why similar levels of manufacturing specialisation produced different outcomes.

**Limitations.** Six limits apply:

- The car industry is hidden inside "manufacturing", so hypothesis B is inferred for Turin rather than measured.
- Jobs data starts only in 2008.
- Jobs are counted at the workplace and graduates at residence, so commuting into Milan blurs the comparison.
- Turin's finance jobs almost double between 2017 and 2023 for reasons we could not establish (possibly a change in where a large bank registers its staff). Results that depend on finance are reported with and without it.
- Graduate migration data covers only 2019–2023, so Turin's net gain of graduates is a recent snapshot.
- The methods are descriptive: they show patterns consistent with or against each hypothesis, not proof of cause.

**Next step.** The natural extension is to test the car industry directly, using ISTAT data on detailed sectors, so that hypothesis B for Turin is measured rather than inferred.

## References

- Brakman, S., Garretsen, H. and van Marrewijk, C. (2019) *An Introduction to Geographical and Urban Economics: A Spiky World*. 3rd edn. Cambridge: Cambridge University Press.
- Dunn, E. S. (1960) 'A statistical and analytical technique for regional analysis', *Papers and Proceedings of the Regional Science Association*, 6, pp. 97–112.
- Forslid, R. and Ottaviano, G. I. P. (2003) 'An analytically solvable core–periphery model', *Journal of Economic Geography*, 3(3), pp. 229–240.
- Helpman, E. (1998) 'The size of regions', in Pines, D., Sadka, E. and Zilcha, I. (eds) *Topics in Public Economics*. Cambridge: Cambridge University Press, pp. 33–54.
- Krugman, P. (1991) 'Increasing returns and economic geography', *Journal of Political Economy*, 99(3), pp. 483–499.
- Martin, R. (1999) 'The new "geographical turn" in economics: some critical reflections', *Cambridge Journal of Economics*, 23(1), pp. 65–91.

Data sources (Eurostat, ISTAT, Ministry of University) are listed in full in `sources.md`.

## Links to accompanying files

- Question and hypotheses: [`question.md`](question.md)
- Assumptions, predictions and methodology: [`framework.md`](framework.md)
- Data sources: [`sources.md`](sources.md)
- How to reproduce the analysis: [`analysis.md`](analysis.md)
- Figures and tables: [`outputs.md`](outputs.md) (figures in `outputs/figures/`, tables in `outputs/tables/`)
- Decisions, checks and AI assistance: [`workflow.md`](workflow.md)
- Code: `code/01_download_eurostat.py` to `code/08_part2_industry.py`

# Briefing for Claude Code — Paper 7 Supervision 3

This file explains who I am, what this repository is for, where I am in the project, and how I want you to help. Read it at the start of every session.

## Who I am and what this is
- I am Jacopo, a second-year Land Economy student at Cambridge. This repository is my work for **Paper 7: Regional Economics and Policy, Supervision 3**, supervised by **Nicholas Sweeney**.
- It is my **fork** of my supervisor's repository (`npsweeney/land-economy-supervision`). I work only on the branch **`my-supervision`**, and I send him the link to that branch at the end.
- I save and upload my work myself with **GitHub Desktop** (commit, then push). Don't push for me unless I ask.

## The assignment (summary of the supervisor's brief)
**Part A: what could good regional economics research look like in a time of rapid technological change?**
- Because LLMs make the labour-intensive parts of research easy, the supervisor says there is now a **premium on setting interesting questions and communicating the answers concisely**.
- In two stages: (1) **set my own question** about something in Paper 7 I want to understand better, based on the lectures; (2) **answer it in the format I think best**: essay, graph, map, website or slides.
- **6–10 hours** in total, with no word limit. Submit my best effort.
- If I use data, my **workflow, sources and code must be recorded** so he can follow and reproduce them.
- Using LLMs is allowed but optional; I've chosen to use you.

**Part B:** a short private note on what I've found difficult in the course so far. I will write that myself.

**Format decided:** a **Quarto website** (the template is in `quarto/`), built from code in this repo.

## Where I am now: the question is NOT decided yet
**This is the most important part of the supervision**, as the supervisor stressed, and it is where I need your help first.

**My area of interest:**
- **The North–South divide in Italy:** why the North is so much richer than the South.
- Possibly **why Milan seems to be the only city in the North that is really thriving**. I'm not sure that premise is true (Turin, Bologna, Veneto and Emilia-Romagna are also rich), so checking it could be part of the question.

**What I need from you, in this order:**
1. **Help me develop and sharpen the research question.** Ask me questions, propose alternatives and push back. Explain the trade-offs between possible questions: how interesting each is, whether it can be answered in 6–10 hours, with what data, and whether the answer could surprise me.
2. **Help me choose and apply a theoretical framework from the lectures.** I must apply theory, not just describe data. For each candidate question, explain which course theory applies, **what it predicts** for Italy, and what pattern in the data would support or contradict it. A good question is one where the theory gives a clear, testable prediction.
3. Only **after I have decided**: help me plan the data, the analysis and the website.

## How I want you to work with me
- **Don't decide for me.** Guide me to my own question with options, questions and explanations. The question and the conclusions must be mine; I need to be able to defend them in the supervision.
- **Explain from zero.** When you use a concept, model or method, explain it step by step in plain language before using technical terms, and link it to my lectures (listed below). I learn by understanding, not by being handed answers.
- **Write in flowing, natural text**, not mechanical templates. Include only the equations that are essential, and explain what each is for.
- **Be honest about limits:** say when something is correlation not causation, when data can't answer a question, or when a premise is shaky.
- **Ask before downloading data or installing anything.**
- **Keep the record:** after each working step, add an entry to `workflow.md` (copy it from `templates/` the first time). Include the **"Tools / AI assistance"** section: what I asked you, what you contributed, and what I checked myself. The supervisor wants this.
- Use the supervisor's templates in `templates/` (question, sources, analysis, outputs, report, workflow) as the backbone of the project.

## What I have learnt so far (theory I can use)
Michaelmas lectures by Dr Johan P Larsson. The main textbook is Brakman, Garretsen & van Marrewijk (2019), *An Introduction to Geographical and Urban Economics: A Spiky World*.

1. **Introduction to regional economics (Lectures 1–2).** The "spiky world": economic activity is highly concentrated. Urbanisation and income go together. The **spatial impossibility theorem**: without increasing returns or differences between places, there would be no cities or trade. Agglomeration economies; spatial equilibrium (people move until no one gains from moving).
2. **Monopolistic competition and the home market effect (Lectures 3–4).**
   - The Dixit–Stiglitz model: increasing returns, love of variety.
   - Trade costs ("phi-ness").
   - The **home market effect**: a region with a larger market attracts a more than proportional share of industry and becomes an exporter of it.
   - Path dependence.
3. **Gravity, trade and market potential (Lectures 5–6).**
   - The **gravity model**: trade rises with size and falls with distance.
   - The **distance puzzle**: distance matters more over time.
   - **Border effects**.
   - **Market potential** (Harris: $MP_i = \sum_j Y_j/d_{ij}$) and accessibility: places close to big markets are richer.
   - Evidence: access predicts income; market potential and density both raise wages.
4. **New Economic Geography (Lectures 7–8).** Krugman's (1991) **core–periphery model**:
   - **Circular cumulative causation**: mobile workers and firms move together; backward and forward linkages; pecuniary externalities.
   - **Falling trade costs** can tip an economy from dispersion to full concentration in one region (the **break** and **sustain points**, the **black hole** condition).
   - **History and expectations** decide which region becomes the core; **lock-in** and agglomeration rents.
   - Martin's (1999) critique: not new, not real geography, over-formalised (no institutions or culture).
5. **Measuring spatial concentration (Lectures 9–10).**
   - Concentration indices: Gini, Isard, Herfindahl, **Theil (decomposes into between- and within-group inequality)**, location quotients, density, Ellison–Glaeser.
   - The **modifiable areal unit problem** (results change with the spatial units).
   - Description vs causation: fixed effects, instruments, difference-in-differences, synthetic control, regression discontinuity.
6. **Still to come this term:** exogenous and endogenous **growth** in a regional context (human capital); **social capital** (bonding vs bridging; Putnam's work on Italy is the classic study of this divide); **regional entrepreneurship**. Lent term covers **place-based policy**.

**Supervisions so far:**
- **S1:** the home market effect. My own example was the Italian espresso-machine industry, using Eurostat trade data.
- **S2:** market potential, gravity and **Head & Mayer (2010)**, "Gravity, market potential and economic development": market access raises income per capita across countries (an elasticity of about 0.35 with instruments). Also multilateral resistance and the distance puzzle.

## Possible directions I've discussed (not decisions)
These are starting points to explore with me, not a plan to execute.
- **Is the divide a "Milan story"?** Is the North–South gap driven by Milan or spread across the North? Is Milan pulling away within the North? (Description; Theil decomposition from Lectures 9–10.)
- **Can market access explain the divide?** Compute market potential for Italian provinces or regions and test whether the South's lower income disappears once market access is controlled for. (Lectures 5–6, NEG, Head & Mayer.)
- **Why Milan?** Cumulative causation and path dependence: the historical industrial triangle (Milan–Turin–Genoa) and lock-in. (Lectures 7–8.)
- **The alternative explanation:** social capital and institutions (Putnam), to set against market access.

**Data I know of:** Eurostat regional GDP per capita (NUTS2 `nama_10r_2gdp`, NUTS3 `nama_10r_3gdp`), population, and GISCO NUTS boundary files; ISTAT for Italian detail.

## First task
Start by reading `README.md` and `templates/question.md`. Then help me work through the research question, as described in "Where I am now". **Don't set up folders, download data or write code until I've decided on the question.**

# Survey Readiness Gap Analysis

This repository is now strong enough for an Awesome-style public bibliography. It is not yet a complete survey paper by itself.

Current assessment after the survey-readiness expansion: **about 80/100** for survey-paper readiness.

## What Is Now Strong

- Coverage across politics, geopolitics, policymaking, strategic studies, forecasting, diplomacy, wargaming, social simulation, political text, and influence operations.
- Clear separation between non-AI foundation papers, classical political NLP/information extraction, and LLM-era technical papers.
- Better coverage of evaluation validity, including social-simulation validation, contamination, temporal leakage, political-worldview robustness, and LLM-as-measurement inference.
- Better multilingual and geopolitical-bias coverage, including territorial disputes, U.S.-China bilingual framing, Pakistani languages, democracy-authoritarianism framing, and cross-lingual ideology steering.
- Stronger institutional-strategy coverage through UN benchmarks, foreign-policy decision benchmarks, Diplomacy harnesses, crisis escalation measurement, and adviser aggregation in foreign-policy decision-making.

## What A Survey Paper Still Needs

1. A unified problem definition.

The survey should define "LLMs for strategy" as the use of language-model systems to represent, measure, simulate, forecast, advise, or influence political and strategic decision-making under uncertainty.

2. A role taxonomy.

Papers should be analyzed by the role the model plays:

- Measurement instrument: political text, ideology, public opinion, event extraction.
- Simulator: agents, synthetic populations, political role-play, crisis games.
- Forecaster: event forecasting, prediction tournaments, temporal reasoning.
- Adviser: policy brief generation, strategic decision support, wargaming support.
- Negotiator or strategic actor: Diplomacy, bargaining, social dilemmas, coalition behavior.
- Persuader or influence operator: deliberation, microtargeting, propaganda, information operations.
- Object of governance: bias, safety, alignment, institutional control.

3. An evaluation-validity matrix.

Every technical paper should be graded on at least these validity dimensions:

- Construct validity: does the benchmark measure the political/strategic concept it claims to measure?
- Temporal validity: does the setup prevent leakage, retrospective contamination, and knowledge-cutoff artifacts?
- Behavioral validity: do simulated agents match observed human or institutional behavior?
- Mechanism validity: can the model explain why an outcome occurred, not just reproduce a pattern?
- External validity: does the result generalize across countries, languages, institutions, crises, and model families?
- Institutional validity: is the system evaluated inside a realistic workflow with human decision-makers or domain constraints?

4. A benchmark and dataset map.

The survey should turn the bibliography into a table of datasets and benchmarks, including task, domain, unit of analysis, time span, language coverage, evaluation metric, leakage controls, and whether human/domain-expert validation exists.

5. An evidence grading scheme.

The current `Core`, `Important`, `Curated`, and `Watchlist` labels are useful for the repository. A survey paper should additionally rate evidence type:

- Field or institutional validation.
- Human-subject or domain-expert experiment.
- Historical backtest with leakage controls.
- Static benchmark.
- Simulation-only study.
- Conceptual essay or position paper.

## Remaining Coverage Gaps

- Real institutional workflows: more evidence from governments, multilaterals, diplomacy, intelligence analysis, emergency management, and military planning.
- Non-Western and multilingual politics beyond U.S./Europe/China/Pakistan: Africa, Latin America, Southeast Asia, Middle East regional politics, and low-resource languages remain thin.
- Longitudinal and post-deployment evidence: few studies observe human organizations using LLM systems over time.
- Mechanistic strategic behavior: the list has many strategic games, but fewer papers explaining belief formation, signaling, commitment, escalation, and deception mechanisms in politically realistic environments.
- Governance and accountability: still not enough work on auditability, responsibility chains, red teaming, procurement, and model-use constraints in public institutions.

## Recommended Next Work

- Stop broad expansion unless a missing cluster is clearly identified.
- Build a benchmark/dataset inventory from `data/processed/thematic_papers.csv`.
- Add a `docs/survey_outline.md` that converts the role taxonomy and validity matrix into a survey-paper structure.
- Add an evidence-grade column only after defining the rubric, because evidence grading is more subjective than citation count or theme placement.

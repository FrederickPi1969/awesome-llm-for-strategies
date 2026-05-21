# Selection Criteria

This repository is a curated map of LLMs for political strategy, geopolitics, policymaking, strategic studies, and high-stakes decision-making. It is not a general LLM bibliography.

## Inclusion Tests

A paper should satisfy at least one test:

- Direct LLM relevance: studies LLMs or LLM agents in politics, geopolitics, policymaking, diplomacy, wargaming, public opinion, forecasting, governance, social simulation, or strategic decision-making.
- Strategic or political task fit: evaluates reasoning, prediction, persuasion, negotiation, escalation, conflict, policy, or institutional decision support in a political or strategic context.
- Benchmark, dataset, or method value: contributes a benchmark, dataset, evaluation design, event extraction method, political measurement method, or agent-simulation method directly useful for the scope.
- Foundation value: is a canonical political-science, international-relations, strategic-studies, intelligence-analysis, or forecasting work needed to interpret LLM-for-strategy work.

## Exclusion Rules

Exclude:

- Finance-only LLMs, trading systems, stock prediction, portfolio management, crypto, and generic financial benchmarks.
- Generic foundation-model, NLP, or agent papers without a direct political, policy, geopolitical, strategic, or decision-making link.
- Generic AI safety papers unless the risk is political, institutional, strategic, influence-related, or national-security relevant.
- Pure business strategy and management papers unless they explicitly concern public, political, institutional, or geopolitical decision-making.
- Blog posts, newsletters, slides, or commentary unless they are canonical and no paper-like source exists.
- Citation-neighborhood candidates surfaced only by weak keyword overlap.

## Labels

- `Core`: field-shaping work, necessary background, or a central benchmark/application for this repository.
- `Important`: strong empirical, methodological, benchmark, dataset, or research value, but not necessary background for every reader.
- `Curated`: relevant and in-scope, but not essential for the README route.
- `Watchlist`: recent, low-citation, unresolved, or borderline work kept visible for follow-up review.

The README highlights `Core` and `Important` papers. The full bibliography keeps `Curated` and `Watchlist` entries visible.

## Evidence Types

Recommended evidence-type tags for future contributions:

- `theory`: domain foundation or formal theory
- `survey`: literature review or systematic overview
- `benchmark`: evaluation benchmark
- `dataset`: reusable dataset or corpus
- `empirical`: empirical study or experiment
- `method`: measurement, extraction, simulation, or evaluation method
- `position`: conceptual or policy position paper
- `system`: implemented agent, tool, or framework

## Data Provenance

The main metadata source is Semantic Scholar Graph API. Citation counts and metadata are useful but imperfect, especially for books, preprints, duplicate editions, and newly published papers. When Semantic Scholar metadata is misleading, generated files may display `n/a` or use a manually supplied year.

Raw expansion longlists are not part of the public bibliography by default. A paper must pass manual scope and relevance review before being merged into `data/processed/thematic_papers.csv`.

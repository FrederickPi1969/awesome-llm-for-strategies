# Data Notes

This repository is scoped to LLMs for political strategy, geopolitics, policymaking, strategic studies, and high-stakes decision-making.

Current generated coverage:

- Full thematic bibliography: 378 unique papers
- README highlights: Core and Important papers only
- Theme count: 10 public-facing reader-oriented themes
- Citation source: Semantic Scholar Graph API
- Citation metadata date: 2026-05-21

## Files

- `README.md`: curated public route through the literature.
- `docs/full-bibliography.md`: complete generated bibliography, including Curated and Watchlist entries.
- `data/processed/thematic_papers.csv`: canonical merged table used to build both Markdown files.
- `docs/selection-criteria.md`: inclusion rules, labels, rejection rules, and provenance notes.
- `docs/survey_readiness_gap_analysis.md`: critique-informed gap analysis for turning the repository into a survey paper.

## Source Inputs

- `data/raw/core_seed_papers.csv`: original strategy-only seed list.
- `data/raw/classical_political_nlp_ie_seed.csv`: curated political NLP, text-as-data, and event-data foundations.
- `data/raw/fog_of_war_related_work_seed.csv`: targeted Fog of War related-work and foundation list.
- `data/raw/strategic_studies_foundation_seed.csv`: strategic studies, deterrence, bargaining, intelligence, and crisis-decision foundations.
- `data/raw/critique_priority_expansion_seeds.csv`: critique-selected high-priority expansion seeds.
- `data/raw/critique_next_expansion_seeds.csv`: next-round critique seeds for escalation-risk and Political-LLM tracing.
- `data/raw/critique_followup_expansion_seeds.csv`: critique-followup seeds for ForecastBench, democratic deliberation, and WARBENCH tracing.
- `data/raw/critique_followup_search_queries.csv`: targeted Semantic Scholar query-search terms for forecasting, deliberation, and military decision-making.
- `data/raw/critique_round3_expansion_seeds.csv`: critique-round-3 seeds for influence operations, Diplomacy, and synthetic-population tracing.
- `data/raw/critique_round3_search_queries.csv`: targeted Semantic Scholar query-search terms for influence operations, diplomacy, and social simulation.
- `data/raw/survey_readiness_expansion_seeds.csv`: critique-selected seeds for survey-readiness gaps in validity, multilingual/geopolitical bias, diplomacy, and strategic reasoning.
- `data/raw/survey_readiness_search_queries.csv`: targeted Semantic Scholar query-search terms for those survey-readiness gaps.
- `data/raw/institutional_workflow_expansion_seeds.csv`: critique-selected seeds for public-sector and institutional decision-support workflows.
- `data/raw/institutional_workflow_search_queries.csv`: targeted Semantic Scholar query-search terms for public-sector workflow gaps.

Processed curated CSVs hold Semantic Scholar metadata, citation counts, authors, venues, DOI/arXiv IDs, URLs, abstracts, and source provenance where available.

## Merge Process

The build script merges source rows by normalized title, applies a manually maintained theme/subtheme assignment table, removes explicit out-of-scope titles, normalizes importance labels, and writes `data/processed/thematic_papers.csv`.

`Source rows checked before merge` means all rows loaded from curated source CSVs before title deduplication. `Duplicate source rows removed during merge` means normalized title collisions across sources, not necessarily bad records.

## Selection and Review

Entries are manually curated after Semantic Scholar expansion. Raw citation-neighborhood longlists and edge dumps are treated as local intermediate files because they can contain finance, business, biomedical, generic NLP, or other off-scope noise.

Preprints are allowed when they are highly relevant to the repository scope, especially for fast-moving LLM benchmark, wargaming, forecasting, and political-simulation work. Low-citation or recent papers are kept as Curated or Watchlist unless they are central to a topic.

The critique-next expansion traced `Escalation Risks from Language Models in Military and Diplomatic Decision-Making` and `Political-LLM: Large Language Models in Political Science`, then accepted 27 non-duplicate papers into the taxonomy.

The critique-followup expansion traced `ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities`, `AI can help humans find common ground in democratic deliberation`, and `WARBENCH: A Comprehensive Benchmark for Evaluating LLMs in Military Decision-Making`. It also ran targeted Semantic Scholar query searches for event forecasting, democratic deliberation, and military decision-making. After critique review, it accepted 33 non-duplicate papers into the taxonomy and explicitly rejected retail forecasting, finance-specific forecasting, generic time-series forecasting, and generic defense-AI items.

The critique-round-3 expansion traced `Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations`, `Human-level play in the game of Diplomacy by combining language models with strategic reasoning`, and the Semantic Scholar record for `Generative Agent Simulations of 1,000 People` (`LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals`). It also ran targeted query searches for political influence operations, AI diplomacy/strategic negotiation, and validated synthetic-population simulation. After critique review, it accepted 41 non-duplicate papers and explicitly rejected economic negotiation, generic games, generic social agents, generic misinformation/safety, corporate/marketing persuasion, and finance/trading/time-series-adjacent items.

The survey-readiness expansion traced validation/social-simulation, forecasting-evaluation, multilingual/geopolitical-bias, UN/diplomacy, and strategic-reasoning seeds. It also ran targeted query searches for validity, temporal leakage, multilingual political bias, non-Western politics, institutional diplomacy, and strategic negotiation. After critique review, it accepted 33 non-duplicate papers, added two more precise subthemes (`Evaluation, validity, and contamination`; `Multilingual and geopolitical bias`), and rejected generic agent papers, generic/economic negotiation, finance-specific temporal-modeling papers, and broad multilingual-bias papers without political relevance.

The institutional-workflow expansion traced `The LLM Effect`, `Biased LLMs can Influence Political Decision-Making`, `Sci2Pol`, `Generative Artificial Intelligence and Evaluating Strategic Decisions`, `WhatIf`, and `Surfacing citizens' policy perspectives`. It also ran targeted query searches for public-sector decision support, briefing notes, government workflows, auditability, procurement/accountability, and science-to-policy translation. After critique review, it accepted 23 non-duplicate papers, added public-sector workflow and public-sector AI governance subthemes, and rejected generic agent bias, business/management decision-making, finance/trading, healthcare-only decision support, and operations papers without a policy or public-administration link.

## Semantic Scholar Limitations

Citation counts and metadata can be incomplete, stale, duplicated across editions, or wrong for books and classic articles. Known undercounts are displayed as `n/a` when they would mislead readers. Year fields that cannot be resolved to a single year are normalized to `n.d.` in generated outputs.

The README should remain a curated guide. The full bibliography and CSV are the appropriate place for long-tail coverage and provenance details.

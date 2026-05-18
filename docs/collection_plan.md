# Collection Plan

## Objective

Build a high-impact Awesome-style repository for LLMs in strategic decision-making: finance, investment, geoeconomics, geopolitics, governance, forecasting, policy analysis, diplomatic simulation, and multi-agent strategy environments.

## Round 0: Seed Consolidation

- Normalize the two source CSVs into one combined seed table.
- Resolve each seed paper against Semantic Scholar.
- Store citation counts, venues, authors, URLs, abstracts, and match status.
- Keep unresolved and low-confidence rows for manual inspection instead of dropping them.

Current status: complete for the 110-paper combined seed list.

## Round 1: Citation and Reference Expansion

- Expand high-confidence, high-priority seeds through both citations and references.
- Aggregate duplicate papers across all seed neighborhoods.
- Remove existing seeds and near-duplicate title variants.
- Score candidates using topic evidence, seed overlap, citation count, and recency.
- Split generic foundation-model papers into a separate context table.

Current status: 65 seeds expanded, 9,454 raw edges collected, 3,815 longlist candidates exported, 405 preliminary domain additions separated from 20 foundation/context papers.

## Round 2: Manual Curation

- Promote accepted papers into a readable Awesome-style README.
- Add decision columns such as `accepted`, `deferred`, `reject_reason`, and `curator_notes`.
- Review low-confidence seed resolutions before using them for later expansion.
- Promote geoeconomics, forecasting, governance, and strategy papers only when they support the repository's LLM-for-strategic-decision-making thesis.
- Keep generic ML/NLP foundation papers in a short background/context section only when they are repeatedly cited by the domain literature.

## Round 3: Deeper Expansion

- Re-run citation/reference expansion on manually accepted additions.
- Add tags for task, domain, method, asset type, benchmark, dataset, model, code, and evaluation setting.
- Add GitHub, dataset, model, and project links where available.
- Create issue and pull request templates for community submissions.
- Add a paper-status workflow: proposed, accepted, background, rejected, needs verification.

## Review Criteria

- Direct relevance to LLMs, foundation models, agents, retrieval, reasoning, forecasting, simulation, or language-centric benchmarks.
- Clear strategic domain relevance: finance, markets, macro, geopolitics, governance, policy, diplomacy, wargaming, or multi-agent social simulation.
- High citation count, high-quality venue, or repeated appearance across multiple seed-paper neighborhoods.
- Practical value for readers building systems for investment research, financial analysis, macro/geopolitical forecasting, strategic simulation, policy support, or governance analysis.

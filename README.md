# Awesome LLM for Strategies

An Awesome-style curated research repository for large language models in strategic decision-making: finance, investment, geoeconomics, geopolitics, governance, forecasting, policy analysis, diplomatic simulation, and multi-agent strategy environments.

> Status: preliminary public seed. This repository starts from 110 seed papers and a first systematic Semantic Scholar expansion over papers that cite them and papers they cite.

## Scope

This repository is broader than finance-only. The organizing question is:

> How are LLMs and LLM agents being used to reason, forecast, simulate, and act in high-stakes strategic domains?

Current tracks:

- Finance and investment strategy
- Financial-domain LLMs, benchmarks, and agents
- SEC filings, financial reports, XBRL, and risk analytics
- Macroeconomic and market forecasting
- Geoeconomics and geopolitical risk
- Political science, governance, democracy, and policy generation
- Diplomatic, military, wargame, and strategic simulation
- Multi-agent social simulation and agent-based modeling

## Latest Expansion Pass

- Seeds inspected: 110
- Seeds resolved in Semantic Scholar: 100
- Seeds expanded through citations and references: 65 high-confidence/high-priority matches
- Raw citation/reference edges collected: 9,454
- Relevance-filtered longlist candidates: 3,815
- Preliminary curated additions for human review: 405
- Generic foundation/context papers separated from domain additions: 20

Primary review file:

- `data/processed/curated_additions_preliminary_110.csv`

## Data Files

- `data/raw/seed_papers_original_110.csv`: normalized combined seed list from the finance and strategy/geoeconomics/governance CSVs.
- `data/processed/seed_papers_enriched_110.csv`: seed metadata with Semantic Scholar IDs, abstracts, citation counts, URLs, and match status.
- `data/raw/semantic_scholar_related_work_edges_110.csv`: raw citation/reference edges from the first 110-seed expansion pass.
- `data/processed/related_work_longlist_110.csv`: broad relevance-filtered candidate longlist.
- `data/processed/curated_additions_preliminary_110.csv`: higher-signal non-seed candidate additions for manual review.
- `data/processed/foundation_context_papers_110.csv`: generic foundation/model papers that are useful context but should not dominate the list.
- `data/processed/run_summary_110.json`: run statistics.
- `data/processed/resolve_failures_110.csv`: resolution failures; currently only the header because the run had no request failures.

## Collection Method

1. Start with the combined 110-paper seed list.
2. Resolve each seed through Semantic Scholar and keep match confidence.
3. Expand only high-confidence, high-priority seeds.
4. Fetch both papers that cite each seed and papers each seed cites.
5. Aggregate duplicate candidate papers across seed neighborhoods.
6. Remove existing seed papers and near-duplicate title variants.
7. Split generic foundation papers from domain-specific strategy candidates.
8. Rank candidates by topical relevance, seed overlap, citation count, and recency.

## Preliminary Review Priorities

Start manual review from `data/processed/curated_additions_preliminary_110.csv`.

High-priority additions should satisfy at least one of:

- Directly studies LLMs, foundation models, or LLM agents in finance, investment, markets, macroeconomics, geopolitics, governance, policy, or strategic simulation.
- Provides a benchmark, dataset, evaluation protocol, or system for strategic reasoning or forecasting.
- Appears around multiple high-quality seed papers and has clear title/abstract relevance.
- Is a highly cited domain method or dataset repeatedly used by the LLM-for-strategy literature.

Foundation papers such as Transformer, BERT, GPT, RAG, and chain-of-thought should stay in `foundation_context_papers_110.csv` unless the README later needs a short background section.

## Scripts

- `scripts/expand_semantic_scholar.py`: resolves seeds, fetches citations/references, and writes raw expansion tables.
- `scripts/build_curated_views.py`: builds the curated review CSV and foundation/context CSV from the longlist.
- `scripts/fetch_seed_metadata.py`: helper for standalone seed enrichment.

The expansion script reads Semantic Scholar API keys from `semantic_scholar_api_keys.json` by default, or from `SEMANTIC_SCHOLAR_API_KEYS_FILE` / `--api-keys-file`. API keys are not committed.

## Contributing

Open an issue or pull request with title, year, link, category, and a short note explaining why the paper belongs in the list. Good additions should make the strategy angle explicit, not just mention LLMs generically.

## Attribution

Paper metadata in `data/` was collected from the seed CSVs and the Semantic Scholar Graph API. Abstracts and third-party metadata remain subject to their original rights and provider terms.

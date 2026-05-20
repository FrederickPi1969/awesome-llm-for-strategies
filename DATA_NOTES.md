# Data Notes

This repository is now scoped to five areas only:

- Politics
- Geopolitics
- Policymaking
- Strategic studies
- Decision-making

The current homepage is built from `data/processed/thematic_papers.csv`. It contains 159 unique papers organized into thematic sections and subthemes.

The original public seed table is `data/raw/core_seed_papers.csv`. It contains 40 papers selected from the politics/geopolitics/governance seed list and excludes finance, trading, stock prediction, portfolio management, and generic financial LLM material.

The earlier mixed 110-seed expansion artifacts were removed because they blended finance/trading candidates with the strategy literature and were not suitable for the repository homepage.

Future expansion should use `core_seed_papers.csv` as the seed set, not the previous combined finance dataset.

The strategy-only Semantic Scholar collection produced:

- `data/processed/core_seed_papers_enriched.csv`: Semantic Scholar citation counts and metadata for core seeds.
- `data/processed/thematic_papers.csv`: merged theme-assigned paper table used for the README.
- `data/processed/candidate_additions_strategy.csv`: manually filtered high-citation/high-relevance related papers used as provenance for the thematic table.
- `data/processed/targeted_related_works_strategy.csv`: targeted related-work additions from the "Generative Artificial Intelligence and Evaluating Strategic Decisions" trace.
- `data/raw/classical_political_nlp_ie_seed.csv`: curated seed list for classical political NLP, text-as-data, legislative text classification, and event-data information extraction.
- `data/processed/classical_political_nlp_ie_enriched.csv`: Semantic Scholar metadata for the classical political NLP and IE additions.
- `data/processed/run_summary.json`: request and expansion summary.

The classical political NLP and IE pass adds 30 pre-LLM and bridge papers covering Wordscores/Wordfish-style policy-position extraction, political text-as-data methods, congressional speech and bill text classification, and KEDS/CAMEO/IDEA/GDELT/PETRARCH-style event extraction.

Raw longlists and edge dumps are treated as local intermediate files because they can contain citation-neighborhood noise outside the repository scope. The README should remain a paper-first thematic map, not a pipeline report.

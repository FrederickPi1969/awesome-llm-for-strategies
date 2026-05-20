# Collection Plan

## Objective

Build a high-quality Awesome-style paper list for LLMs in politics, geopolitics, policymaking, strategic studies, and decision-making.

## Scope

Included:

- Political science and computational social science with LLMs
- Geopolitical, diplomatic, military, and wargame simulation
- Policy analysis, policy generation, governance, democracy, and political influence
- Forecasting, event prediction, and decision-making benchmarks
- Multi-agent social and political simulation
- Geopolitical risk and policy-signal measurement

Excluded:

- Finance-only LLMs
- Trading systems
- Stock prediction
- Portfolio management
- Generic financial benchmarks
- Generic foundation-model papers without a direct politics/geopolitics/policy/strategy/decision-making link

## Round 0: Homepage Cleanup

- Replace the data-heavy homepage with a paper-first Awesome list.
- Remove mixed finance/trading expansion artifacts.
- Keep one clean seed file: `data/raw/core_seed_papers.csv`.
- Make the README categories match the five focus areas.

Current status: complete.

## Round 1: Strategy-Only Expansion

- Use `data/raw/core_seed_papers.csv` as the only expansion seed set.
- Resolve each paper with Semantic Scholar.
- Fetch citations and references only for high-confidence matches.
- Filter candidates by the five focus areas before adding them to the README.
- Keep finance/trading candidates out unless the paper is directly about policymaking, geopolitics, or strategic decision-making.

Current status: complete for the first strategy-only pass. The README now includes Semantic Scholar citation counts for core papers and a manually filtered set of high-citation/high-relevance expansion candidates.

## Round 2: Manual Curation

- Add accepted papers to the README under the correct category.
- Use short inclusion notes only when they clarify strategic relevance.
- Track deferred/rejected candidates separately if needed.
- Avoid turning the README into a data report; data and pipeline details belong below the paper list or in docs.

Current status: complete. The homepage now uses a thematic structure with 129 unique papers across 8 themes and 31 subthemes.

## Targeted Related-Work Tracing

- Use targeted Semantic Scholar traces when a specific high-value paper should be expanded.
- Keep selected additions strict: they must fit politics, geopolitics, policymaking, strategic studies, or decision-making.
- Add accepted targeted papers to `data/processed/targeted_related_works_strategy.csv`, then rebuild the thematic README.

Current status: complete for `Generative Artificial Intelligence and Evaluating Strategic Decisions`.

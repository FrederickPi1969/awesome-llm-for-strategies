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

Current status: superseded by the curated-guide pass. The full bibliography now contains 355 unique papers across 10 reader-oriented themes, while the README highlights only Core and Important papers.

## Targeted Related-Work Tracing

- Use targeted Semantic Scholar traces when a specific high-value paper should be expanded.
- Keep selected additions strict: they must fit politics, geopolitics, policymaking, strategic studies, or decision-making.
- Add accepted targeted papers to `data/processed/targeted_related_works_strategy.csv`, then rebuild the thematic README.

Current status: complete for `Generative Artificial Intelligence and Evaluating Strategic Decisions`.

## Classical Political NLP and Information Extraction Foundations

- Add pre-LLM political NLP and information-extraction papers that form the methodological base for current LLM-for-strategy work.
- Cover political text-as-data, policy-position extraction, legislative speech and bill-text classification, media-frame annotation, international-relations extraction, and political event-data systems.
- Prioritize high-citation classics and directly relevant bridge work over generic NLP.
- Keep this as a methods/foundations theme, not a finance/trading expansion.

Current status: complete for the first pass. The README now includes 30 classical political NLP and IE papers, including Text as Data, Wordscores, Wordfish-style scaling, Hopkins-King content analysis, congressional debate stance extraction, King-Lowe event IE, KEDS, CAMEO, IDEA, GDELT, PETRARCH/Open Event Data, Phoenix/POLECAT bridge work, and neural event coding.

## Public Repository Quality Pass

- Make the README a curated route through the literature rather than a full generated bibliography.
- Keep complete coverage in `docs/full-bibliography.md` and `data/processed/thematic_papers.csv`.
- Add reader guidance, Start Here papers, public label definitions, selection criteria, and stricter contribution standards.
- Normalize public theme names around reader intent: foundations, political text, public opinion, policy support, geopolitics/wargaming, forecasting, strategic games, social simulation, and risk.

Current status: complete for the first pass. The README highlights Core and Important papers only, and `docs/full-bibliography.md` preserves the full generated bibliography.

## Critique-Guided Next Expansion

- Use Critique's priority recommendation to trace `Escalation Risks from Language Models in Military and Diplomatic Decision-Making` and `Political-LLM: Large Language Models in Political Science`.
- Reject title variants already present in the bibliography.
- Keep only papers that fit the existing taxonomy: military/diplomatic decision-making, political LLM methods, public opinion, democratic deliberation, political bias, strategic intelligence, nuclear escalation, and influence operations.
- Mark low-citation but precise 2025-2026 papers as `Curated` or `Watchlist` unless they are central enough to highlight.

Current status: complete for this pass. The trace scanned 144 citation/reference edges and added 27 non-duplicate papers.

## Critique-Followup Expansion

- Use Critique's next recommendation to trace `ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities`, `AI can help humans find common ground in democratic deliberation`, and a small-radius `WARBENCH: A Comprehensive Benchmark for Evaluating LLMs in Military Decision-Making` pass.
- Add targeted Semantic Scholar query searches for forecasting benchmarks, democratic deliberation, citizen policy representation, consensus generation, and military decision-making.
- Reject retail forecasting, finance-specific forecasting, generic time-series forecasting, generic business strategy, generic safety/security, and defense AI without LLM-based military decision evaluation.
- Mark low-citation 2025-2026 papers as `Curated` or `Watchlist` unless they are unusually central, preregistered, field-validated, or directly political/policy/military.

Current status: complete for this pass. The trace scanned 367 citation/reference edges, the query-search screened 98 Semantic Scholar results, and the critique-reviewed merge added 33 non-duplicate papers.

## Critique Round 3: Influence Operations, Diplomacy, and Social Simulation

- Use Critique's recommendation to trace `Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations`, `Human-level play in the game of Diplomacy by combining language models with strategic reasoning`, and the Semantic Scholar record behind `Generative Agent Simulations of 1,000 People`.
- Add targeted Semantic Scholar query searches for LLM-enabled influence operations, political microtargeting, state-sponsored information operations, AI diplomacy, strategic negotiation, and validated synthetic-population simulation.
- Accept influence-operations papers only when they are political, electoral, state-actor, or strategic-information-environment papers.
- Accept social-simulation papers only when they include validation, calibration, public-opinion evidence, political behavior, policy scenario evaluation, or reusable datasets/benchmarks.
- Reject economic negotiation, generic games, generic agent platforms, generic misinformation/safety, corporate/marketing persuasion, and finance/trading/time-series-adjacent candidates.

Current status: complete for this pass. The trace scanned 1,064 influence/diplomacy citation-reference edges, 304 social-simulation related-work edges, and 132 Semantic Scholar query results. The critique-reviewed merge added 41 non-duplicate papers.

## Survey-Readiness Expansion

- Use Critique's survey-paper gap assessment to target validity/evaluation, multilingual and geopolitical bias, institutional diplomacy, foreign-policy decision-making, and strategic-reasoning mechanisms.
- Trace existing high-value seeds rather than starting a broad discovery pass.
- Add two narrower subthemes: `Evaluation, validity, and contamination` and `Multilingual and geopolitical bias`.
- Keep generic LLM evaluation only when it directly supports contamination, temporal leakage, or validity standards for political-strategic tasks.
- Reject generic agent papers, economic negotiation, finance-specific forecasting, and generic multilingual-bias work without political or geopolitical content.

Current status: complete for this pass. The trace scanned 721 citation/reference edges and 166 Semantic Scholar query results. The critique-reviewed merge added 33 non-duplicate papers, bringing the full bibliography to 355 unique papers. See `docs/survey_readiness_gap_analysis.md` for the remaining survey-paper gaps.

## Institutional Workflow Expansion

- Use Critique's top priority cluster to deepen public-sector and institutional decision-support evidence.
- Trace `The LLM Effect`, `Biased LLMs can Influence Political Decision-Making`, `Sci2Pol`, `Generative Artificial Intelligence and Evaluating Strategic Decisions`, `WhatIf`, and `Surfacing citizens' policy perspectives`.
- Accept papers only when they improve coverage of policy analyst workflows, briefing notes, public-sector algorithmic advice, emergency-management simulation, public administration, data governance, auditability, accountability, or institutionalized AI in public agencies.
- Add two narrower subthemes: `Public-sector decision support and institutional workflow` and `Accountability, auditing, and public-sector AI governance`.
- Reject generic AI decision-making, business/management strategy, finance/trading, healthcare-only decision support, generic agent bias, and operations/logistics papers without a public-sector governance link.

Current status: complete for this pass. The trace scanned 273 citation/reference edges and 339 Semantic Scholar query results. The critique-reviewed merge added 23 non-duplicate papers, bringing the full bibliography to 378 unique papers.

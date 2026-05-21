# Repository Operating Principles

This repository is an Awesome-style paper list for LLMs and AI systems in politics, geopolitics, policymaking, strategic studies, and decision-making. Keep the homepage paper-first, selective, and thematically organized.

## Scope

Include papers that directly support at least one of these focus areas:

- Politics
- Geopolitics
- Policymaking
- Strategic studies
- Decision-making

Exclude finance-only, trading, stock prediction, portfolio management, cryptocurrency, generic financial LLM benchmarks, and generic foundation-model papers unless there is a direct politics, geopolitics, policy, strategic-studies, or decision-making link.

## Theme Discipline

- Always distinguish `theme` and `subtheme`.
- Every accepted paper must belong to exactly one theme and one subtheme.
- Do not create catch-all sections.
- Do not keep "first-order expansion" or "second-order expansion" sections in the README. Expansion provenance belongs in data files; accepted papers must be merged into thematic sections.
- Add a new theme only when the existing themes would mix genuinely different literatures.
- When adding a source table, update `scripts/build_readme.py` so the generated README, `docs/full-bibliography.md`, and `data/processed/thematic_papers.csv` include every accepted paper.
- Prefer adding narrower subthemes over overloading broad ones when a survey-paper gap becomes visible. Current examples include `Evaluation, validity, and contamination` and `Multilingual and geopolitical bias`.

## Foundation Papers

Keep foundation papers separate from AI technical papers.

Use a dedicated top-level category named `Political Science and Strategic Judgment Foundations` for non-AI classics in political science, international relations, strategic judgment, forecasting, intelligence analysis, crisis decision-making, hindsight bias, and expert judgment. These papers explain the domain and evaluation logic, but they are not LLM or AI systems papers.

Keep this category separate from `Foundations, Surveys, and Methods`. The latter is for LLM-era surveys and technical-methods overview papers; the former is for non-AI domain foundations.

Use `Classical Political NLP and Information Extraction` for pre-LLM or bridge-era computational work such as political text-as-data, policy-position extraction, legislative text classification, event coding, KEDS, CAMEO, IDEA, GDELT, PETRARCH, Phoenix, POLECAT, and related political information extraction.

Keep AI/LLM benchmarks, agents, model evaluations, simulations, forecasting systems, and decision-support systems in the AI technical themes, not in the foundation category.

## Inclusion Bar

Add papers through two lanes:

- Recent and highly relevant: usually 2024 or later, possibly low citation count, but directly on this repository's target themes.
- High-citation and highly relevant: older or classical papers with strong influence and clear relevance to the domain or methodology.

Reject papers that are merely adjacent, generic, or only connected by a broad keyword. A paper should help someone understand LLMs or AI systems for politics, geopolitics, policymaking, strategic studies, or decision-making.

For targeted deep dives, be stricter than for broad discovery. If the seed is about fog-of-war reasoning, military decision-making, escalation, or crisis forecasting, accepted additions should be directly about those topics or a clearly necessary foundation for evaluating them.

## Semantic Scholar Workflow

- Use the Semantic Scholar Graph API for paper resolution, citation counts, references, and citing-paper traces.
- Respect the local skill rule of 1 request per second per API token.
- Do not fetch TLDR fields unless explicitly requested.
- Prefer exact title matches. Inspect fuzzy or unresolved matches manually.
- Use `citationCount` from Semantic Scholar when available. Use `n/a` only when the paper cannot be reliably resolved.
- Never invent citation counts, venues, abstracts, authors, DOIs, or arXiv IDs.
- Preserve source URLs. Prefer Semantic Scholar URLs for resolved papers and primary URLs when Semantic Scholar cannot resolve the paper.
- Never commit or expose API keys in this public repository.

## Critique-Guided Expansion

- Use the `critique` agent as a gatekeeper for major expansion rounds.
- Ask critique to choose seed papers, state the preferred expansion mode, define acceptance standards, and name directions to pause.
- Ask critique to review shortlists before merging low-citation or broad candidates.
- Critique should not edit files directly; implementation and merge decisions stay in the main repository workflow.
- Preserve critique decisions through explicit seed files, curated-addition files, and collection-plan notes.
- Treat critique's reject/downgrade decisions as binding unless there is new metadata that clearly changes the case. Especially reject generic agent papers, economic negotiation, finance-specific forecasting, generic LLM evaluation, and generic multilingual bias unless there is a direct political, geopolitical, policy, strategic-studies, or decision-making link.

## Data Workflow

- Put curated seed files in `data/raw/`.
- Put enriched metadata and accepted curated tables in `data/processed/`.
- Keep raw longlists, edge dumps, and noisy citation-neighborhood outputs out of the README.
- Use explicit provenance filenames for targeted traces, for example a seed file and an enriched file named after the target paper or topic.
- If a new accepted source table is added, wire it into `scripts/build_readme.py`.
- Every accepted source title must have a theme assignment in `scripts/build_readme.py` and must appear in the generated full bibliography. The README intentionally highlights only `Core` and `Important` items.
- The build should fail if a curated source row lacks a theme assignment or if an assignment has no source row.

## README Standard

- The README should open with scope and a curated paper route, not pipeline details.
- Every paper line should include title, URL, year, importance label when useful, and citation count.
- Keep the "Data and Collection" section concise.
- Do not fill the homepage with raw logs, scripts, or process notes.
- Do not duplicate the same paper in multiple themes. If a paper spans multiple areas, choose its primary role in this repository.

## Validation Before Commit

Run these checks after changing papers, themes, data files, or build scripts:

```bash
python3 scripts/build_readme.py
python3 -m py_compile scripts/*.py
git diff --check
```

Also verify source coverage and out-of-scope leakage:

```bash
python3 - <<'PY'
import csv

source_paths = [
    'data/raw/core_seed_papers.csv',
    'data/processed/candidate_additions_strategy.csv',
    'data/processed/priority_expansion_seeds.csv',
    'data/processed/second_order_candidate_additions_strategy.csv',
    'data/processed/targeted_related_works_strategy.csv',
    'data/processed/classical_political_nlp_ie_enriched.csv',
    'data/processed/fog_of_war_related_works_enriched.csv',
    'data/processed/strategic_studies_foundation_enriched.csv',
    'data/processed/critique_priority_expansion/curated_additions.csv',
    'data/processed/critique_next_expansion/curated_additions.csv',
    'data/processed/critique_followup_expansion/curated_additions.csv',
    'data/processed/critique_round3_expansion/curated_additions.csv',
    'data/processed/survey_readiness_expansion/curated_additions.csv',
]

def norm(value):
    return ' '.join((value or '').lower().split())

excluded_titles = {
    norm(title)
    for title in [
        'Generative AI in Managerial Decision-Making: Redefining Boundaries through Ambiguity Resolution and Sycophancy Analysis',
        'Effect of Generative Artificial Intelligence on Strategic Decision Making in Entrepreneurial Business Initiatives: A Systematic Literature Review',
        'The role of artificial intelligence in international strategic decision-making for SMEs',
        'When Artificial Intelligence Does Strategy: Learning, Good Times, Lock-in, and Human-Driven Strategic Renewal',
        'AI in strategic alliance formation: a framework for human-AI collaboration',
        'Reliance on AI in augmented strategic decision-making: Navigating cultural and national dynamics',
        'How AI-assisted scenario thinking develops agile minds for a successful digital strategy?',
    ]
}

source = []
for path in source_paths:
    for row in csv.DictReader(open(path, newline='', encoding='utf-8')):
        title = norm(row['title'])
        if title not in excluded_titles:
            source.append(title)

thematic = [
    norm(row['title'])
    for row in csv.DictReader(open('data/processed/thematic_papers.csv', newline='', encoding='utf-8'))
]

print('source_rows', len(source))
print('source_unique', len(set(source)))
print('thematic_rows', len(thematic))
print('thematic_unique', len(set(thematic)))
print('missing_after_merge', sorted(set(source) - set(thematic))[:20])
print('extra_after_merge', sorted(set(thematic) - set(source))[:20])
PY
```

```bash
python3 - <<'PY'
import csv
import re

bad = re.compile(r'finance|financial|trading|stock|portfolio|investment|bitcoin|cryptocurrency|banking', re.I)

hits = []
for row in csv.DictReader(open('data/processed/thematic_papers.csv', newline='', encoding='utf-8')):
    text = f"{row['theme']} {row['subtheme']} {row['title']}"
    if bad.search(text):
        hits.append(row['title'])

print('out_of_scope_keyword_hits', len(hits))
for title in hits:
    print(title)
PY
```

If new source tables are added, update the validation snippet to include them.

## Curation Notes

- Prefer fewer highly relevant additions over broad noisy coverage.
- New papers with low citations can be included if they are directly on-topic and useful.
- High-citation papers should still be rejected if they are generic or only loosely related.
- For classical or foundation work, explain why it is foundational through placement, not by mixing it into AI technical sections.
- Keep abstracts and metadata in CSV files; keep README entries compact.
- Update `DATA_NOTES.md` and `docs/collection_plan.md` when the repository structure, scope, or collection strategy changes.

## Git Hygiene

- Check `git status --short` before editing.
- Do not revert user or other-agent changes unless explicitly asked.
- Keep commits scoped to the actual change.
- Do not commit local API-key files, private credentials, or unrelated intermediate artifacts.

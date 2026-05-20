#!/usr/bin/env python3
"""Build README and curated expansion CSV for Awesome LLM for Strategies."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORE_SEEDS = ROOT / "data" / "raw" / "core_seed_papers.csv"
ENRICHED_SEEDS = ROOT / "data" / "processed" / "core_seed_papers_enriched.csv"
CANDIDATES = ROOT / "data" / "processed" / "candidate_related_papers_preliminary.csv"
RUN_SUMMARY = ROOT / "data" / "processed" / "run_summary.json"
CURATED_CANDIDATES = ROOT / "data" / "processed" / "candidate_additions_strategy.csv"
PRIORITY_EXPANSION_SEEDS = ROOT / "data" / "processed" / "priority_expansion_seeds.csv"
SECOND_ORDER_SUMMARY = ROOT / "data" / "processed" / "second_order" / "run_summary.json"
SECOND_ORDER_CANDIDATES = ROOT / "data" / "processed" / "second_order_candidate_additions_strategy.csv"
README = ROOT / "README.md"

SECTION_ORDER = [
    "Politics and Political Science",
    "Geopolitics, Diplomacy, and Strategic Simulation",
    "Forecasting and Decision-Making",
    "Governance, Democracy, and Policymaking",
    "Multi-Agent Social and Political Simulation",
    "Geopolitical Risk and Policy Signals",
]

CANDIDATE_SELECTION = [
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "Human-level play in the game of Diplomacy by combining language models with strategic reasoning",
    ),
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "Playing repeated games with large language models",
    ),
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "War and Peace (WarAgent): Large Language Model-based Multi-Agent Simulation of World Wars",
    ),
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "Strategic behavior of large language models and the role of game structure versus contextual framing",
    ),
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "On Large Language Models in National Security Applications",
    ),
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "Do Large Language Models Know Conflict? Investigating Parametric vs. Non-Parametric Knowledge of LLMs for Conflict Forecasting",
    ),
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "When AI Navigates the Fog of War",
    ),
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "Managing Escalation in Off-the-Shelf Large Language Models",
    ),
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "Effective and responsible use of large language models in strategic wargaming",
    ),
    (
        "Geopolitics, Diplomacy, and Strategic Simulation",
        "Causal Reasoning and Large Language Models for Military Decision-Making: Rethinking the Command Structures in the Era of Generative AI",
    ),
    (
        "Politics, Governance, and Public Opinion",
        "Whose Opinions Do Language Models Reflect?",
    ),
    (
        "Politics, Governance, and Public Opinion",
        "AI can help humans find common ground in democratic deliberation",
    ),
    (
        "Politics, Governance, and Public Opinion",
        "Large language models as a substitute for human experts in annotating political text",
    ),
    (
        "Politics, Governance, and Public Opinion",
        "Demonstrations of the Potential of AI-based Political Issue Polling",
    ),
    (
        "Politics, Governance, and Public Opinion",
        "Emergence of human-like polarization among large language model agents",
    ),
    (
        "Politics, Governance, and Public Opinion",
        "Echoes of Power: Investigating Geopolitical Bias in US and China Large Language Models",
    ),
    (
        "Politics, Governance, and Public Opinion",
        "A Large-Scale Simulation on Large Language Models for Decision-Making in Political Science",
    ),
    (
        "Forecasting and Decision-Making",
        "Forecasting Future World Events with Neural Networks",
    ),
    (
        "Forecasting and Decision-Making",
        "Wisdom of the silicon crowd: LLM ensemble prediction capabilities rival human crowd accuracy",
    ),
    (
        "Forecasting and Decision-Making",
        "Large Language Model Prediction Capabilities: Evidence from a Real-World Forecasting Tournament",
    ),
    (
        "Forecasting and Decision-Making",
        "Are LLMs Prescient? A Continuous Evaluation using Daily News as the Oracle",
    ),
    (
        "Multi-Agent Social and Political Simulation",
        "From Individual to Society: A Survey on Social Simulation Driven by Large Language Model-based Agents",
    ),
    (
        "Multi-Agent Social and Political Simulation",
        "Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents",
    ),
    (
        "Multi-Agent Social and Political Simulation",
        "Validation is the central challenge for generative social simulation: a critical review of LLMs in agent-based modeling",
    ),
    (
        "Multi-Agent Social and Political Simulation",
        "ElectionSim: Massive Population Election Simulation Powered by Large Language Model Driven Agents",
    ),
    (
        "Multi-Agent Social and Political Simulation",
        "Network formation and dynamics among multi-LLMs",
    ),
    (
        "Multi-Agent Social and Political Simulation",
        "Generative Exaggeration in LLM Social Agents: Consistency, Bias, and Toxicity",
    ),
]

BUCKET_LABELS = {
    "recent_relevant_2024_plus": "Recent and Highly Relevant (2024+)",
    "high_citation_relevant": "High-Citation and Highly Relevant",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_csv_if_exists(path: Path) -> list[dict[str, str]]:
    return read_csv(path) if path.exists() else []


def read_json_if_exists(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def normalize(value: str) -> str:
    return " ".join((value or "").lower().split())


def title_tokens(value: str) -> set[str]:
    stopwords = {"a", "an", "and", "as", "at", "for", "from", "in", "of", "on", "the", "to", "with"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", normalize(value))
        if len(token) > 1 and token not in stopwords
    }


def title_similarity(left: str, right: str) -> float:
    left_tokens = title_tokens(left)
    right_tokens = title_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def citation_display(seed: dict[str, str], enriched: dict[str, str] | None) -> str:
    if not enriched:
        return "n/a"
    method = enriched.get("resolution_method", "")
    resolved_title = enriched.get("resolved_title", "")
    trusted = method in {"arxiv", "title_exact"} or title_similarity(seed["title"], resolved_title) >= 0.7
    if not trusted:
        return "n/a"
    value = enriched.get("citationCount", "")
    return value if value != "" else "n/a"


def markdown_link(title: str, url: str) -> str:
    return f"[{title}]({url})" if url else title


def row_url(row: dict[str, str]) -> str:
    return row.get("url") or row.get("source_url") or (f"https://arxiv.org/abs/{row['arxiv']}" if row.get("arxiv") else "")


def bucket_rows(rows: list[dict[str, str]], bucket_field: str, bucket: str) -> list[dict[str, str]]:
    selected = [row for row in rows if bucket in row.get(bucket_field, "").split("; ")]
    return sorted(
        selected,
        key=lambda row: (
            -as_int(row.get("citationCount")),
            row.get("category") or row.get("curated_category") or "",
            row.get("title", "").lower(),
        ),
    )


def build_candidate_rows() -> list[dict[str, str]]:
    if not CANDIDATES.exists() and CURATED_CANDIDATES.exists():
        return read_csv(CURATED_CANDIDATES)

    candidates = read_csv(CANDIDATES)
    by_title = {normalize(row["title"]): row for row in candidates}
    rows: list[dict[str, str]] = []

    for category, title in CANDIDATE_SELECTION:
        row = by_title.get(normalize(title))
        if not row:
            raise RuntimeError(f"Selected candidate not found: {title}")
        rows.append({"curated_category": category, **row})

    rows.sort(
        key=lambda row: (
            row["curated_category"],
            -as_int(row.get("citationCount")),
            -as_int(row.get("seed_overlap_count")),
            row.get("title", "").lower(),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["curated_rank"] = str(index)
    return rows


def write_candidate_csv(rows: list[dict[str, str]]) -> None:
    columns = [
        "curated_rank",
        "curated_category",
        "paperId",
        "title",
        "year",
        "citationCount",
        "seed_overlap_count",
        "relevance_score",
        "relation_summary",
        "source_seed_titles",
        "url",
        "doi",
        "arxiv",
        "venue",
        "authors",
        "abstract",
    ]
    CURATED_CANDIDATES.parent.mkdir(parents=True, exist_ok=True)
    with CURATED_CANDIDATES.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def build_readme() -> str:
    seeds = read_csv(CORE_SEEDS)
    enriched_rows = read_csv(ENRICHED_SEEDS)
    enriched_by_title = {normalize(row["title"]): row for row in enriched_rows}
    candidates = build_candidate_rows()
    write_candidate_csv(candidates)
    summary = json.loads(RUN_SUMMARY.read_text(encoding="utf-8"))
    priority_seeds = read_csv_if_exists(PRIORITY_EXPANSION_SEEDS)
    second_order_candidates = read_csv_if_exists(SECOND_ORDER_CANDIDATES)
    second_order_summary = read_json_if_exists(SECOND_ORDER_SUMMARY)

    by_section: dict[str, list[dict[str, str]]] = defaultdict(list)
    for seed in seeds:
        by_section[seed["awesome_section"]].append(seed)

    candidate_sections: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidates:
        candidate_sections[row["curated_category"]].append(row)

    second_order_sections: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in second_order_candidates:
        second_order_sections[row["selection_bucket"]][row["curated_category"]].append(row)

    lines = [
        "# Awesome LLM for Strategies",
        "",
        "A curated paper list on large language models for politics, geopolitics, policymaking, strategic studies, and decision-making.",
        "",
        "This repository focuses on how LLMs and LLM agents analyze political behavior, forecast events, support policy reasoning, simulate social and diplomatic systems, and behave in strategic environments.",
        "",
        "Out of scope: finance, trading, stock prediction, portfolio management, generic financial LLM benchmarks, and generic foundation-model papers unless they directly support one of the five focus areas above.",
        "",
        "Citation counts are from the Semantic Scholar Graph API, collected on 2026-05-20.",
        "",
        "## Contents",
        "",
        "- [Core Papers](#core-papers)",
        "- [First-Order Expansion Candidates](#first-order-expansion-candidates)",
        "- [Priority Seeds for Second-Order Expansion](#priority-seeds-for-second-order-expansion)",
        "- [Second-Order Expansion Results](#second-order-expansion-results)",
        "- [Data and Collection](#data-and-collection)",
        "",
        "## Core Papers",
        "",
    ]

    for section in SECTION_ORDER:
        if section not in by_section:
            continue
        lines.extend([f"### {section}", ""])
        for seed in by_section[section]:
            enriched = enriched_by_title.get(normalize(seed["title"]))
            citation_count = citation_display(seed, enriched)
            lines.append(
                f"- {markdown_link(seed['title'], seed['source_url'])} "
                f"({seed['year_or_timeframe']}) - {seed['priority']}; citations: {citation_count}."
            )
        lines.append("")

    lines.extend(
        [
            "## First-Order Expansion Candidates",
            "",
            "These papers were surfaced by expanding the core list through Semantic Scholar citations and references, then filtering for relevance to politics, geopolitics, policymaking, strategic studies, and decision-making. They are strong first-round candidates for promotion into the main sections after manual review.",
            "",
        ]
    )
    for section in sorted(candidate_sections):
        lines.extend([f"### {section}", ""])
        for row in candidate_sections[section]:
            lines.append(
                f"- {markdown_link(row['title'], row_url(row))} ({row.get('year') or 'n.d.'}) - "
                f"citations: {row.get('citationCount') or '0'}; seed hits: {row.get('seed_overlap_count') or '0'}."
            )
        lines.append("")

    if priority_seeds:
        lines.extend(
            [
                "## Priority Seeds for Second-Order Expansion",
                "",
                "These are the first-order papers selected for deeper citation/reference expansion because they are either recent and strongly relevant, highly cited and strongly relevant, or both.",
                "",
            ]
        )
        for bucket, label in BUCKET_LABELS.items():
            rows = bucket_rows(priority_seeds, "expansion_bucket", bucket)
            if not rows:
                continue
            lines.extend([f"### {label}", ""])
            for row in rows:
                lines.append(
                    f"- {markdown_link(row['title'], row_url(row))} ({row.get('year_or_timeframe') or 'n.d.'}) - "
                    f"citations: {row.get('citationCount') or '0'}; seed hits: {row.get('seed_overlap_count') or '0'}; "
                    f"category: {row.get('category') or 'n/a'}."
                )
            lines.append("")

    if second_order_candidates:
        lines.extend(
            [
                "## Second-Order Expansion Results",
                "",
                "These papers came from expanding the priority seeds above. The longlist was filtered again, and only highly relevant papers are shown here.",
                "",
            ]
        )
        for bucket, label in BUCKET_LABELS.items():
            sections = second_order_sections.get(bucket, {})
            if not sections:
                continue
            lines.extend([f"### {label}", ""])
            for section in sorted(sections):
                lines.extend([f"#### {section}", ""])
                for row in sections[section]:
                    lines.append(
                        f"- {markdown_link(row['title'], row_url(row))} ({row.get('year') or 'n.d.'}) - "
                        f"citations: {row.get('citationCount') or '0'}; seed hits: {row.get('seed_overlap_count') or '0'}."
                    )
                lines.append("")

    lines.extend(
        [
            "## Data and Collection",
            "",
            f"- Core seeds: {summary['seed_count']}",
            f"- Resolved seeds: {summary['resolved_seed_count']}",
            f"- Expanded high-confidence/high-priority seeds: {summary['expanded_seed_count']}",
            f"- Raw citation/reference edges: {summary['edge_count']}",
            f"- Relevance-filtered candidate longlist: {summary['candidate_count_after_filter']}",
            f"- Curated candidate additions in README: {len(candidates)}",
            f"- Priority seeds for second-order expansion: {len(priority_seeds)}",
            f"- Second-order expanded seeds: {second_order_summary.get('expanded_seed_count', 0)}",
            f"- Second-order citation/reference edges: {second_order_summary.get('edge_count', 0)}",
            f"- Second-order longlist candidates: {second_order_summary.get('candidate_count_after_filter', 0)}",
            f"- Curated second-order additions in README: {len(second_order_candidates)}",
            "",
            "Data files:",
            "",
            "- `data/raw/core_seed_papers.csv`: current homepage seed list.",
            "- `data/processed/core_seed_papers_enriched.csv`: seed metadata with citation counts, authors, venues, abstracts, and resolution method.",
            "- `data/processed/candidate_additions_strategy.csv`: selected high-citation/high-relevance expansion candidates shown above.",
            "- `data/processed/priority_expansion_seeds.csv`: first-order papers selected for deeper expansion.",
            "- `data/processed/second_order/run_summary.json`: second-order Semantic Scholar expansion summary.",
            "- `data/processed/second_order_candidate_additions_strategy.csv`: selected recent and high-citation second-order additions shown above.",
            "",
            "Scripts:",
            "",
            "- `scripts/expand_semantic_scholar.py`: resolves seeds, fetches citations/references, and writes expansion tables.",
            "- `scripts/fetch_seed_metadata.py`: enriches seed papers with Semantic Scholar metadata.",
            "- `scripts/build_priority_expansion.py`: selects priority expansion seeds and curated second-order additions.",
            "- `scripts/build_readme.py`: rebuilds this README and the curated candidate CSV from processed data.",
            "",
            "## Contributing",
            "",
            "Additions should clearly fit one of the five focus areas: politics, geopolitics, policymaking, strategic studies, or decision-making. Please include title, year, URL, category, citation count if available, and a short reason for inclusion.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    README.write_text(build_readme(), encoding="utf-8")


if __name__ == "__main__":
    main()

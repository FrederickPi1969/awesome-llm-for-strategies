#!/usr/bin/env python3
"""Select curated additions from the institutional-workflow expansion pass."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_LONG_LIST = ROOT / "data" / "processed" / "institutional_workflow_expansion" / "candidate_related_papers_preliminary.csv"
SEARCH_LONG_LIST = ROOT / "data" / "processed" / "institutional_workflow_expansion" / "search_results_preliminary.csv"
OUTPUT = ROOT / "data" / "processed" / "institutional_workflow_expansion" / "curated_additions.csv"

SELECTIONS = [
    {
        "raw_title": "The End of the Policy Analyst? Testing the Capability of Artificial Intelligence to Generate Plausible, Persuasive, and Useful Policy Analysis",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy translation and policy brief generation",
        "reason": "Critique accepted as Important because it directly tests AI-generated briefing notes with senior public-service evaluators.",
    },
    {
        "raw_title": 'Human-AI Interactions in Public Sector Decision-Making:"Automation Bias"and"Selective Adherence"to Algorithmic Advice',
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Public-sector decision support and institutional workflow",
        "reason": "Critique accepted as Important public-sector evidence on automation bias and selective adherence to algorithmic advice.",
    },
    {
        "raw_title": "Determinants of LLM-assisted Decision-Making",
        "importance": "Curated",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Evaluation, validity, and contamination",
        "reason": "Broad LLM-assisted decision-making review retained as curated support for human-LLM decision design, not promoted because it is generic.",
    },
    {
        "raw_title": "What Makes LLM Agent Simulations Useful for Policy? Insights From an Iterative Design Engagement in Emergency Preparedness",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Public-sector decision support and institutional workflow",
        "reason": "Critique accepted as Important because it studies policy-useful LLM simulation through emergency-preparedness engagement.",
    },
    {
        "raw_title": "Are We Asking the Right Questions?: Designing for Community Stakeholders’ Interactions with AI in Policing",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Public-sector decision support and institutional workflow",
        "reason": "Public-sector policing decision-support paper retained as curated HCI and stakeholder evidence.",
    },
    {
        "raw_title": "Agent-based modeling as organizational and public policy simulators",
        "importance": "Curated",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Social simulation and agent-based modeling reviews",
        "reason": "Classic public-policy and organizational simulation background retained as curated foundation material.",
    },
    {
        "raw_title": "Decision Making under Deep Uncertainty: From Theory to Practice",
        "importance": "Curated",
        "theme": "Political Science and Strategic Judgment Foundations",
        "subtheme": "Policy analysis and decision-making under deep uncertainty",
        "reason": "Deep-uncertainty decision-making foundation for policy workflows and LLM-supported planning.",
    },
    {
        "raw_title": "A Methodology to Develop Agent-Based Models for Policy Support Via Qualitative Inquiry",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Public-sector decision support and institutional workflow",
        "reason": "Policy-support ABM methodology retained as background for policy-facing simulation design.",
    },
    {
        "raw_title": "Automating public policy: a comparative study of conversational artificial intelligence models and human expertise in crafting briefing notes",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy translation and policy brief generation",
        "reason": "Critique accepted as Important because it directly compares conversational AI and human expertise in briefing-note writing.",
    },
    {
        "raw_title": "An Institutional Theory Framework for Leveraging Large Language Models for Policy Analysis and Intervention Design",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Public-sector decision support and institutional workflow",
        "reason": "Institutional-theory framework for LLM policy analysis and intervention design; relevant but framework-heavy.",
    },
    {
        "raw_title": "DataGovBench: Benchmarking LLM Agents for Real-World Data Governance Workflows",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Accountability, auditing, and public-sector AI governance",
        "reason": "Critique accepted as Important because it benchmarks LLM agents on real-world data-governance workflows.",
    },
    {
        "raw_title": "Audit Trails for Accountability in Large Language Models",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Accountability, auditing, and public-sector AI governance",
        "reason": "Critique accepted as Important because it directly addresses auditability and accountability for LLMs in consequential decisions.",
    },
    {
        "raw_title": "More than an IT system in the government: The work divide challenges in human-AI coworking context",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Public-sector decision support and institutional workflow",
        "reason": "Government-agency human-AI coworking study retained for public-sector workflow evidence.",
    },
    {
        "raw_title": "Replacing or enhancing the human coder? Multiclass classification of policy documents with large language models",
        "importance": "Curated",
        "theme": "Classical Political NLP and Information Extraction",
        "subtheme": "Political text as data and policy-position extraction",
        "reason": "Policy-document classification paper retained as political-text measurement and policy-analysis infrastructure.",
    },
    {
        "raw_title": "Large Language Model–Powered Public Service Platforms for Automated Case Assistance and Decision Support",
        "importance": "Watchlist",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Public-sector decision support and institutional workflow",
        "reason": "Direct public-service LLM platform paper, but zero-citation and likely application-oriented, so kept on watchlist.",
    },
    {
        "raw_title": "Informing Human Decision-Making in Public Administration through NLP Algorithm Audits",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Accountability, auditing, and public-sector AI governance",
        "reason": "Public-administration NLP audit paper retained as governance and decision-support evidence.",
    },
    {
        "raw_title": "Human‑Centered Governance for AI‑Augmented Decision Support in Public‑Sector Logistics",
        "importance": "Watchlist",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Public-sector decision support and institutional workflow",
        "reason": "Public-sector logistics governance paper kept on watchlist because the policy connection is plausible but operations-heavy.",
    },
    {
        "raw_title": "Impacts of AI-based anti-corruption audits on risk aversion in decision-making: a case study of the Brazilian ALICE tool",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Accountability, auditing, and public-sector AI governance",
        "reason": "Brazilian anti-corruption audit case retained as concrete public-sector AI institutional evidence.",
    },
    {
        "raw_title": "AI and Corruption: Legal Liability in Algorithmic Decision-Making",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Accountability, auditing, and public-sector AI governance",
        "reason": "Public-service AI liability paper retained for governance and corruption-risk accountability.",
    },
    {
        "raw_title": "Institutionalizing Predictive AI in Public Administration: Algorithmic Governance and the Case of a Wildfire Forecasting System",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Public-sector decision support and institutional workflow",
        "reason": "Critique accepted as Important because it studies predictive AI institutionalization in a public-administration wildfire system.",
    },
    {
        "raw_title": "Governing AI with trust: an adaptive framework for institutional legitimacy in the UK public sector",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Accountability, auditing, and public-sector AI governance",
        "reason": "UK public-sector AI legitimacy framework retained as curated governance material.",
    },
    {
        "raw_title": "Social Policy of Large Language Models: How GPT, Claude, DeepSeek and Grok Allocate Social Budgets in Spain and Germany",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic and institutional decision support",
        "reason": "Direct social-budget allocation audit across countries and models; low citation count keeps it Curated.",
    },
    {
        "raw_title": "Who Does What? Archetypes of Roles Assigned to LLMs During Human-AI Decision-Making",
        "importance": "Watchlist",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Evaluation, validity, and contamination",
        "reason": "Human-LLM role taxonomy is useful for survey structure, but kept on watchlist because it is not public-sector specific.",
    },
]


def normalize(value: str) -> str:
    return " ".join((value or "").lower().split())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def clean_csv_value(value: Any) -> str:
    return " ".join(str(value or "").split())


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean_csv_value(row.get(column, "")) for column in columns})


def row_quality(row: dict[str, str]) -> tuple[int, int]:
    return (1 if row.get("abstract") else 0, int(row.get("citationCount") or 0))


def indexed_rows() -> dict[str, dict[str, str]]:
    by_title: dict[str, dict[str, str]] = {}
    for row in [*read_csv(SEARCH_LONG_LIST), *read_csv(TRACE_LONG_LIST)]:
        key = normalize(row["title"])
        if key not in by_title or row_quality(row) > row_quality(by_title[key]):
            by_title[key] = row
    return by_title


def main() -> None:
    by_title = indexed_rows()
    output: list[dict[str, Any]] = []

    for rank, selection in enumerate(SELECTIONS, start=1):
        row = by_title.get(normalize(selection["raw_title"]))
        if not row:
            raise RuntimeError(f"Selected institutional-workflow paper not found: {selection['raw_title']}")
        output.append(
            {
                "selected_rank": rank,
                "importance": selection["importance"],
                "theme": selection["theme"],
                "subtheme": selection["subtheme"],
                "selection_reason": selection["reason"],
                **row,
            }
        )

    columns = [
        "selected_rank",
        "importance",
        "theme",
        "subtheme",
        "selection_reason",
        "paperId",
        "title",
        "year",
        "citationCount",
        "seed_overlap_count",
        "relevance_score",
        "relation_summary",
        "source_seed_titles",
        "query_ids",
        "focus_areas",
        "url",
        "doi",
        "arxiv",
        "venue",
        "authors",
        "abstract",
    ]
    write_csv(OUTPUT, output, columns)
    print(f"institutional_workflow_curated_additions={len(output)}")


if __name__ == "__main__":
    main()

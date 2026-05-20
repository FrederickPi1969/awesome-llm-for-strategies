#!/usr/bin/env python3
"""Build curated targeted related-work CSVs from Semantic Scholar traces."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LONG_LIST = ROOT / "data" / "processed" / "targeted_strategic_decisions" / "candidate_related_papers_preliminary.csv"
OUTPUT = ROOT / "data" / "processed" / "targeted_related_works_strategy.csv"

SELECTIONS = [
    {
        "raw_title": "How Well Can AI Do Strategy? Empirical Benchmarking Using Strategy Simulations",
        "title": "How Well Can AI Do Strategy? Empirical Benchmarking Using Strategy Simulations",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Direct strategy benchmark for LLMs under uncertainty, competition, and interdependence.",
    },
    {
        "raw_title": "AI-Augmented Strategic Decision-Making Under Time Constraints: An Experimental Study on Mental Representations and Strategic Foresight",
        "title": "AI-Augmented Strategic Decision-Making Under Time Constraints: An Experimental Study on Mental Representations and Strategic Foresight",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Directly studies LLM-assisted strategic foresight and decision representations.",
    },
    {
        "raw_title": "Reproducing and Extending Experiments in Behavioral Strategy with Large Language Models",
        "title": "Reproducing and Extending Experiments in Behavioral Strategy with Large Language Models",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic evaluation, bias, and foresight",
        "reason": "Uses LLM agents to reproduce behavioral strategy experiments.",
    },
    {
        "raw_title": "AI strategy under institutional pressure: strategic conformity and decision-making in large language models",
        "title": "AI strategy under institutional pressure: strategic conformity and decision-making in large language models",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic evaluation, bias, and foresight",
        "reason": "Connects institutional pressure, strategic conformity, and LLM decision behavior.",
    },
    {
        "raw_title": "Bias in, symbolic compliance out?\n GPT\n 's reliance on gender and race in strategic evaluations",
        "title": "Bias in, symbolic compliance out? GPT's reliance on gender and race in strategic evaluations",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic evaluation, bias, and foresight",
        "reason": "Directly evaluates bias in LLM-supported strategic evaluation.",
    },
    {
        "raw_title": "Generative AI in Managerial Decision-Making: Redefining Boundaries through Ambiguity Resolution and Sycophancy Analysis",
        "title": "Generative AI in Managerial Decision-Making: Redefining Boundaries through Ambiguity Resolution and Sycophancy Analysis",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Relevant to ambiguity, sycophancy, and strategic managerial advice.",
    },
    {
        "raw_title": "Effect of Generative Artificial Intelligence on Strategic Decision Making in Entrepreneurial Business Initiatives: A Systematic Literature Review",
        "title": "Effect of Generative Artificial Intelligence on Strategic Decision Making in Entrepreneurial Business Initiatives: A Systematic Literature Review",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Systematic review of GenAI for strategic decision-making.",
    },
    {
        "raw_title": "Towards Using Prompt Engineering in Large Language Models to Assist Decision Making",
        "title": "Towards Using Prompt Engineering in Large Language Models to Assist Decision Making",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Prompting-focused paper on LLM-assisted decision-making.",
    },
    {
        "raw_title": "Beyond Black Boxes: Designing and Testing Agentic AI Systems for Strategy",
        "title": "Beyond Black Boxes: Designing and Testing Agentic AI Systems for Strategy",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Directly about designing agentic AI systems for strategy work.",
    },
    {
        "raw_title": "The role of artificial intelligence in\xa0international strategic decision-making for SMEs",
        "title": "The role of artificial intelligence in international strategic decision-making for SMEs",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Studies AI in international strategic decision-making.",
    },
    {
        "raw_title": "When Artificial Intelligence Does Strategy: Learning, Good Times, Lock-in, and Human-Driven Strategic Renewal",
        "title": "When Artificial Intelligence Does Strategy: Learning, Good Times, Lock-in, and Human-Driven Strategic Renewal",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Models delegation of strategy choices to AI agents.",
    },
    {
        "raw_title": "AI in strategic alliance formation: a framework for human–AI collaboration",
        "title": "AI in strategic alliance formation: a framework for human-AI collaboration",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Human-AI framework for strategic alliance formation.",
    },
    {
        "raw_title": "From Problems to Solutions in Strategic Decision-Making: The Effects of Generative AI on Problem Formulation",
        "title": "From Problems to Solutions in Strategic Decision-Making: The Effects of Generative AI on Problem Formulation",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic evaluation, bias, and foresight",
        "reason": "Directly studies GenAI effects on strategic problem formulation.",
    },
    {
        "raw_title": "Can AI Do Strategy?",
        "title": "Can AI Do Strategy?",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Conceptual framing paper for whether AI can perform strategy.",
    },
    {
        "raw_title": "How AI-assisted scenario thinking develops “agile minds” for a successful digital strategy?",
        "title": "How AI-assisted scenario thinking develops agile minds for a successful digital strategy?",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic evaluation, bias, and foresight",
        "reason": "Scenario thinking and strategic foresight under uncertainty.",
    },
    {
        "raw_title": "Reliance on AI in augmented strategic decision-making: Navigating cultural and national dynamics",
        "title": "Reliance on AI in augmented strategic decision-making: Navigating cultural and national dynamics",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Studies reliance on AI in augmented strategic decision-making.",
    },
    {
        "raw_title": "Advancing Decision-Making through AI-Human Collaboration: A Systematic Review and Conceptual Framework",
        "title": "Advancing Decision-Making through AI-Human Collaboration: A Systematic Review and Conceptual Framework",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Review and framework for human-AI decision-making collaboration.",
    },
    {
        "raw_title": "Can AI Do Strategy? A Dialogue and Debate",
        "title": "Can AI Do Strategy? A Dialogue and Debate",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "AI-assisted strategy and managerial decision-making",
        "reason": "Follow-on debate directly tied to AI strategy capability.",
    },
]


def normalize(value: str) -> str:
    return " ".join((value or "").lower().split())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean_csv_value(row.get(column, "")) for column in columns})


def clean_csv_value(value: Any) -> str:
    return " ".join(str(value or "").split())


def main() -> None:
    long_rows = read_csv(LONG_LIST)
    by_title = {normalize(row["title"]): row for row in long_rows}
    output: list[dict[str, Any]] = []

    for rank, selection in enumerate(SELECTIONS, start=1):
        row = by_title.get(normalize(selection["raw_title"]))
        if not row:
            raise RuntimeError(f"Selected targeted related work not found: {selection['raw_title']}")
        output.append(
            {
                "selected_rank": rank,
                "theme": selection["theme"],
                "subtheme": selection["subtheme"],
                "selection_reason": selection["reason"],
                **row,
                "title": selection["title"],
            }
        )

    columns = [
        "selected_rank",
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
        "url",
        "doi",
        "arxiv",
        "venue",
        "authors",
        "abstract",
    ]
    write_csv(OUTPUT, output, columns)
    print(f"targeted_related_works={len(output)}")


if __name__ == "__main__":
    main()

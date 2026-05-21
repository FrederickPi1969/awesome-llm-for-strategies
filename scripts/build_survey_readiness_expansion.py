#!/usr/bin/env python3
"""Select curated additions from the survey-readiness expansion pass."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_LONG_LIST = ROOT / "data" / "processed" / "survey_readiness_expansion" / "candidate_related_papers_preliminary.csv"
SEARCH_LONG_LIST = ROOT / "data" / "processed" / "survey_readiness_expansion" / "search_results_preliminary.csv"
OUTPUT = ROOT / "data" / "processed" / "survey_readiness_expansion" / "curated_additions.csv"

SELECTIONS = [
    {
        "raw_title": "AI Agents Alone Are Not (Yet) Sufficient for Social Simulation",
        "importance": "Important",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Evaluation, validity, and contamination",
        "reason": "Critique accepted as Important because it directly challenges the validity assumptions behind LLM social simulation.",
    },
    {
        "raw_title": "LLM-Based Social Simulations Require a Boundary",
        "importance": "Important",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Evaluation, validity, and contamination",
        "reason": "Critique accepted as Important because it offers boundary-setting and heterogeneity criteria for LLM social simulations.",
    },
    {
        "raw_title": "Integrating LLM in Agent-Based Social Simulation: Opportunities and Challenges",
        "importance": "Curated",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Social simulation and agent-based modeling reviews",
        "reason": "Position paper on LLM-integrated social simulation architectures, limitations, and validation strategies.",
    },
    {
        "raw_title": "Generative Agents in Agent-Based Modeling: Overview, Validation, and Emerging Challenges",
        "importance": "Curated",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Social simulation and agent-based modeling reviews",
        "reason": "Survey-style overview of generative agents in agent-based modeling with a validation focus.",
    },
    {
        "raw_title": "Leak, Cheat, Repeat: Data Contamination and Evaluation Malpractices in Closed-Source LLMs",
        "importance": "Curated",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Evaluation, validity, and contamination",
        "reason": "High-citation contamination and benchmark-validity paper retained as methodology support for political-strategic evaluation.",
    },
    {
        "raw_title": "The Consequences of Generative AI for Democracy, Governance and War",
        "importance": "Watchlist",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Political science and computational social science overviews",
        "reason": "Broad democracy, governance, and war essay; kept on the watchlist rather than promoted.",
    },
    {
        "raw_title": "Using Imperfect Surrogates for Downstream Inference: Design-based Supervised Learning for Social Science Applications of Large Language Models",
        "importance": "Important",
        "theme": "Classical Political NLP and Information Extraction",
        "subtheme": "Political text as data and policy-position extraction",
        "reason": "Critique accepted as Important because it gives validity guarantees for LLM-derived social-science labels and downstream inference.",
    },
    {
        "raw_title": "Applications of GPT in Political Science Research: Extracting Information from Unstructured Text",
        "importance": "Curated",
        "theme": "Classical Political NLP and Information Extraction",
        "subtheme": "Political event data and conflict information extraction",
        "reason": "Political-science information-extraction bridge paper using GPT for unstructured political data collection.",
    },
    {
        "raw_title": "Beyond Prompt Brittleness: Evaluating the Reliability and Consistency of Political Worldviews in LLMs",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Critique accepted as Important because it evaluates reliability and consistency of LLM political worldviews across EU voting-advice instruments.",
    },
    {
        "raw_title": "Political Compass or Spinning Arrow? Towards More Meaningful Evaluations for Values and Opinions in Large Language Models",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Critique accepted as Important because it challenges artificial survey-style evaluations of LLM values and political opinions.",
    },
    {
        "raw_title": "Measuring Political Bias in Large Language Models: What Is Said and How It Is Said",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Fine-grained political-bias measurement paper retained as curated because it overlaps with existing bias coverage.",
    },
    {
        "raw_title": "The Political Biases of ChatGPT",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "High-citation early ChatGPT political-bias audit, kept below Important because the genre is now well covered.",
    },
    {
        "raw_title": "Assessing political bias in large language models",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "European political-bias audit using German voter-advice data; relevant but overlapping.",
    },
    {
        "raw_title": "This Land is Your, My Land: Evaluating Geopolitical Bias in Language Models through Territorial Disputes",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Multilingual and geopolitical bias",
        "reason": "Critique accepted as Important because it evaluates multilingual geopolitical bias on territorial disputes.",
    },
    {
        "raw_title": "Mapping Geopolitical Bias in 11 Large Language Models: A Bilingual, Dual-Framing Analysis of U.S.-China Tensions",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Multilingual and geopolitical bias",
        "reason": "Critique accepted as Important because it uses bilingual and dual-framing prompts to audit U.S.-China geopolitical bias.",
    },
    {
        "raw_title": "Political biases and inconsistencies in bilingual GPT models—the cases of the U.S. and China",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Multilingual and geopolitical bias",
        "reason": "Cross-language U.S.-China political-bias paper retained as a focused multilingual/geopolitical item.",
    },
    {
        "raw_title": "International political bias in large language models: a critical discourse analysis of narratives in ChatGPT, LLaMA, Gemini, and DeepSeek",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Multilingual and geopolitical bias",
        "reason": "Recent comparative geopolitical-bias analysis covering U.S., Russia, China, Iran, and Israel narratives.",
    },
    {
        "raw_title": "Framing Political Bias in Multilingual LLMs Across Pakistani Languages",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Multilingual and geopolitical bias",
        "reason": "Critique accepted as Important because it fills the non-Western, low-resource multilingual political-bias gap.",
    },
    {
        "raw_title": "Democratic or Authoritarian? Probing a New Dimension of Political Biases in Large Language Models",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Multilingual and geopolitical bias",
        "reason": "Critique accepted as Important because it evaluates LLM alignment along a democracy-authoritarianism geopolitical value axis.",
    },
    {
        "raw_title": "Bias Beyond Borders: Political Ideology Evaluation and Steering in Multilingual LLMs",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Multilingual and geopolitical bias",
        "reason": "Critique accepted as Important because it spans many countries and languages and includes cross-lingual ideology steering.",
    },
    {
        "raw_title": "What Is The Political Content in LLMs' Pre- and Post-Training Data?",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Critique accepted as Important because it studies the data provenance of political bias before and after LLM training.",
    },
    {
        "raw_title": "From Pretraining Data to Language Models to Downstream Tasks: Tracking the Trails of Political Biases Leading to Unfair NLP Models",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "High-citation political-bias provenance paper retained as curated due to generic NLP-fairness drift.",
    },
    {
        "raw_title": "John vs. Ahmed: Debate-Induced Bias in Multilingual LLMs",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Multilingual and geopolitical bias",
        "reason": "Multilingual debate-induced bias paper with political and cultural bias settings.",
    },
    {
        "raw_title": "Diversity and language technology: how language modeling bias causes epistemic injustice",
        "importance": "Watchlist",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Bias, toxicity, and cultural alignment risks",
        "reason": "Broad linguistic-bias theory retained only as watchlist support for multilingual political evaluation.",
    },
    {
        "raw_title": "Opportunities and Risks of LLMs for Scalable Deliberation with Polis",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Critique accepted as Important because it directly addresses LLM support for scalable democratic deliberation with Polis.",
    },
    {
        "raw_title": "Democratizing Diplomacy: A Harness for Evaluating Any Large Language Model on Full-Press Diplomacy",
        "importance": "Important",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "Diplomacy and international institutions",
        "reason": "Critique accepted as Important because it provides an evaluation harness for full-press Diplomacy without frontier-model dependence.",
    },
    {
        "raw_title": "When Reasoning Models Hurt Behavioral Simulation: A Solver-Sampler Mismatch in Multi-Agent LLM Negotiation",
        "importance": "Curated",
        "theme": "Strategic Reasoning, Games, Negotiation, and Cooperation",
        "subtheme": "Negotiation, bargaining, and communication games",
        "reason": "Policy-facing negotiation simulation paper retained for the solver-sampler mismatch validity issue.",
    },
    {
        "raw_title": "Why Do LLMs Struggle in Strategic Play? Broken Links Between Observations, Beliefs, and Actions",
        "importance": "Curated",
        "theme": "Strategic Reasoning, Games, Negotiation, and Cooperation",
        "subtheme": "Game-theoretic and strategic reasoning benchmarks",
        "reason": "Strategic-play failure analysis retained as curated because it is generic but methodologically useful.",
    },
    {
        "raw_title": "Communication Enhances LLMs' Stability in Strategic Thinking",
        "importance": "Curated",
        "theme": "Strategic Reasoning, Games, Negotiation, and Cooperation",
        "subtheme": "Cooperation and social dilemmas",
        "reason": "Cheap-talk and repeated-game stability study relevant to multi-agent strategic behavior.",
    },
    {
        "raw_title": "CHBench: A Cognitive Hierarchy Benchmark for Evaluating Strategic Reasoning Capability of LLMs",
        "importance": "Curated",
        "theme": "Strategic Reasoning, Games, Negotiation, and Cooperation",
        "subtheme": "Behavioral game tests and human-like strategy",
        "reason": "Cognitive-hierarchy benchmark retained as curated because it is useful for strategic reasoning but not political-specific.",
    },
    {
        "raw_title": "LLM-Deliberation: Evaluating LLMs with Interactive Multi-Agent Negotiation Games",
        "importance": "Curated",
        "theme": "Strategic Reasoning, Games, Negotiation, and Cooperation",
        "subtheme": "Negotiation, bargaining, and communication games",
        "reason": "Interactive multi-agent negotiation benchmark retained as a strategic-deliberation baseline.",
    },
    {
        "raw_title": "What is Escalation? Measuring Crisis Dynamics in International Relations with Human and LLM Generated Event Data",
        "importance": "Important",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "Conflict, escalation, and geopolitical simulation",
        "reason": "Critique accepted as Important because it directly links IR crisis dynamics, escalation measurement, and LLM-generated event data.",
    },
    {
        "raw_title": "Advisers and Aggregation in Foreign Policy Decision Making",
        "importance": "Important",
        "theme": "Political Science and Strategic Judgment Foundations",
        "subtheme": "International politics, intelligence, and crisis judgment",
        "reason": "Critique accepted as Important decision-process foundation for foreign-policy deliberation and adviser aggregation.",
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
            raise RuntimeError(f"Selected survey-readiness paper not found: {selection['raw_title']}")
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
    print(f"survey_readiness_curated_additions={len(output)}")


if __name__ == "__main__":
    main()

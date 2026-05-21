#!/usr/bin/env python3
"""Select curated additions from the critique-next Semantic Scholar trace."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LONG_LIST = ROOT / "data" / "processed" / "critique_next_expansion" / "candidate_related_papers_preliminary.csv"
OUTPUT = ROOT / "data" / "processed" / "critique_next_expansion" / "curated_additions.csv"

SELECTIONS = [
    {
        "raw_title": "Intelligent Computing Social Modeling and Methodological Innovations in Political Science in the Era of Large Language Models",
        "importance": "Important",
        "theme": "Foundations, Surveys, and Methods",
        "subtheme": "Political science and computational social science overviews",
        "reason": "Political-science methods overview surfaced from the Political-LLM citation neighborhood.",
    },
    {
        "raw_title": "Large Means Left: Political Bias in Large Language Models Increases with Their Number of Parameters",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Direct political-bias audit with nontrivial early citation signal.",
    },
    {
        "raw_title": "PoliCon: Evaluating LLMs on Achieving Diverse Political Consensus Objectives",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "European Parliament consensus benchmark for policy deliberation and political compromise.",
    },
    {
        "raw_title": "An evaluation of LLMs for political bias in Western media: Israel-Hamas and Ukraine-Russia wars",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Geopolitical media-bias audit focused on conflict coverage.",
    },
    {
        "raw_title": "Analysing LLM Persona Generation and Fairness Interpretation in Polarised Geopolitical Contexts",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Persona-generation audit in a polarized geopolitical context.",
    },
    {
        "raw_title": "AlignSurvey: A Comprehensive Benchmark for Human Preferences Alignment in Social Surveys",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Public opinion, polling, and political annotation",
        "reason": "Benchmark for survey-style human preference alignment, relevant to LLM public-opinion simulation.",
    },
    {
        "raw_title": "ParlAI Vote: A Web Platform for Analyzing Gender and Political Bias in Large Language Models",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Legislative and political-agent simulation",
        "reason": "European Parliament vote platform for LLM political-bias and vote-prediction analysis.",
    },
    {
        "raw_title": "The LLM Effect: Are Humans Truly Using LLMs, or Are They Being Influenced By Them Instead?",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic and institutional decision support",
        "reason": "Empirical human-LLM policy-study workflow paper with evidence on model influence over expert users.",
    },
    {
        "raw_title": "Ignore All Previous Instructions: Jailbreaking as a de-escalatory peace building practise to resist LLM social media bots",
        "importance": "Watchlist",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Borderline but directly about LLM social-media bots, conflict escalation, and de-escalation tactics.",
    },
    {
        "raw_title": "Battlefield information and tactics engine (BITE): a multimodal large language model approach for battlespace management",
        "importance": "Curated",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "Military decision-making and wargaming",
        "reason": "Direct LLM defense decision-support system for battlespace management.",
    },
    {
        "raw_title": "Waltzing into uncertainty: AI in nuclear decision making and the challenge of divergent deterrence logics",
        "importance": "Curated",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "Conflict, escalation, and geopolitical simulation",
        "reason": "AI and nuclear decision-making paper focused on deterrence logic and inadvertent escalation.",
    },
    {
        "raw_title": "Artificial Intelligence in Political Forecasting: Possibilities and Limitations",
        "importance": "Watchlist",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting performance and aggregation",
        "reason": "Recent political-forecasting paper kept for review because it is relevant but currently low-signal.",
    },
    {
        "raw_title": "When Two LLMs Debate, Both Think They'll Win",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Deliberation, persuasion, and information environments",
        "reason": "Dynamic adversarial policy-debate study of LLM confidence updating.",
    },
    {
        "raw_title": "Do we Still Need People? Comparing Human and LLM Personas in Political Modeling and Simulation",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Direct comparison of human and synthetic LLM personas in political simulation.",
    },
    {
        "raw_title": "Can AI Truly Represent Your Voice in Deliberations? A Comprehensive Study of Large-Scale Opinion Aggregation with LLMs",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Direct democratic-deliberation and opinion-aggregation evaluation with fairness concerns.",
    },
    {
        "raw_title": "Ideology-Based LLMs for Content Moderation",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Evaluates ideology-conditioned LLM behavior for moderation and fairness.",
    },
    {
        "raw_title": "Integrators at War: Mediating in AI-assisted Resort-to-Force Decisions",
        "importance": "Curated",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "Military decision-making and wargaming",
        "reason": "AI-assisted resort-to-force decision paper focused on the human-machine integration layer.",
    },
    {
        "raw_title": "LLM Analysis of 150+ years of German Parliamentary Debates on Migration Reveals Shift from Post-War Solidarity to Anti-Solidarity in the Last Decade",
        "importance": "Curated",
        "theme": "Classical Political NLP and Information Extraction",
        "subtheme": "Legislative speech and policy text classification",
        "reason": "LLM bridge paper for validated large-scale parliamentary text analysis.",
    },
    {
        "raw_title": "ParliaBench: An Evaluation and Benchmarking Framework for LLM-Generated Parliamentary Speech",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Legislative and political-agent simulation",
        "reason": "Benchmark for parliamentary speech generation and political authenticity.",
    },
    {
        "raw_title": "Charting the Landscape of Nefarious Uses of Generative Artificial Intelligence for Online Election Interference",
        "importance": "Important",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Election-interference paper on GenAI/LLM misuse with direct democratic-risk relevance.",
    },
    {
        "raw_title": "Media Source Matters More Than Content: Unveiling Political Bias in LLM-Generated Citations",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Political-bias audit of LLM-generated citations and source preferences.",
    },
    {
        "raw_title": "Simulating Misinformation Vulnerabilities with Agent Personas",
        "importance": "Curated",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "LLM-agent simulation of misinformation vulnerability, trust, polarization, and susceptibility.",
    },
    {
        "raw_title": "Governing Automated Strategic Intelligence",
        "importance": "Curated",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "National security applications and doctrine",
        "reason": "Direct governance paper for AI-enabled strategic intelligence and nation-state competition.",
    },
    {
        "raw_title": "Hacking Nuclear Stability: Wargaming Technology, Uncertainty, and Escalation",
        "importance": "Important",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "Conflict, escalation, and geopolitical simulation",
        "reason": "High-relevance cyber-nuclear wargaming study referenced by the escalation-risk seed.",
    },
    {
        "raw_title": "AI\n in Conflict Resolution: Practical Considerations, Opportunities and Challenges",
        "title": "AI in Conflict Resolution: Practical Considerations, Opportunities and Challenges",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "LLM-focused overview for conflict-resolution practitioners and researchers.",
    },
    {
        "raw_title": "Can AI reflect public opinion? Evidence from replicating Hainmueller and Hopkins' immigration experiment with LLMs",
        "importance": "Watchlist",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Public opinion, polling, and political annotation",
        "reason": "Recent public-opinion replication study retained as a watchlist item pending stronger metadata.",
    },
    {
        "raw_title": "Upskilling human actors against AI automation bias in strategic decision making on the resort to force",
        "importance": "Curated",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "Military decision-making and wargaming",
        "reason": "Human-centered mitigation paper for AI automation bias in resort-to-force decisions.",
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


def main() -> None:
    long_rows = read_csv(LONG_LIST)
    by_title = {normalize(row["title"]): row for row in long_rows}
    output: list[dict[str, Any]] = []

    for rank, selection in enumerate(SELECTIONS, start=1):
        row = by_title.get(normalize(selection["raw_title"]))
        if not row:
            raise RuntimeError(f"Selected critique-next paper not found: {selection['raw_title']}")
        output.append(
            {
                "selected_rank": rank,
                "importance": selection["importance"],
                "theme": selection["theme"],
                "subtheme": selection["subtheme"],
                "selection_reason": selection["reason"],
                **row,
                "title": selection.get("title", row["title"]),
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
        "url",
        "doi",
        "arxiv",
        "venue",
        "authors",
        "abstract",
    ]
    write_csv(OUTPUT, output, columns)
    print(f"critique_next_curated_additions={len(output)}")


if __name__ == "__main__":
    main()

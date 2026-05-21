#!/usr/bin/env python3
"""Select curated additions from the critique-round-3 expansion pass."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_LONG_LIST = ROOT / "data" / "processed" / "critique_round3_expansion" / "candidate_related_papers_preliminary.csv"
SEARCH_LONG_LIST = ROOT / "data" / "processed" / "critique_round3_expansion" / "search_results_preliminary.csv"
SOCIAL_TRACE = ROOT / "data" / "processed" / "critique_round3_expansion" / "social_simulation_seed_trace_preliminary.csv"
OUTPUT = ROOT / "data" / "processed" / "critique_round3_expansion" / "curated_additions.csv"

SELECTIONS = [
    {
        "raw_title": "Evaluating the persuasive influence of political microtargeting with large language models",
        "importance": "Important",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Critique accepted as Important because it is a PNAS political microtargeting experiment with LLM-generated persuasion.",
    },
    {
        "raw_title": "Assessing the risks and opportunities posed by AI-enhanced influence operations on social media",
        "importance": "Important",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Critique accepted as Important because it directly covers AI-enhanced influence operations, synthetic media, bots, and social engineering.",
    },
    {
        "raw_title": "Do Bots Do It Better? Analyzing the Effectiveness of Automated Agents in State-Sponsored Information Operations",
        "importance": "Important",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Critique accepted as Important because it studies automated agents inside state-sponsored information operations.",
    },
    {
        "raw_title": "Characterizing the 2016 Russian IRA influence campaign",
        "importance": "Important",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Critique accepted as Important as a high-citation empirical foundation for state influence operations and election manipulation.",
    },
    {
        "raw_title": "ClausewitzGPT Framework: A New Frontier in Theoretical Large Language Model Enhanced Information Operations",
        "importance": "Curated",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "LLM-enhanced information-operations framework; relevant but more conceptual than empirical.",
    },
    {
        "raw_title": "Navigating the Web of Disinformation and Misinformation: Large Language Models as Double-Edged Swords",
        "importance": "Curated",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Broad LLM misinformation/disinformation survey retained only as curated context for influence operations.",
    },
    {
        "raw_title": "Generative artificial intelligence in the electoral processes of 2024 in the world: disinformation campaigns and online trolls",
        "importance": "Curated",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Election-focused generative-AI disinformation and troll-campaign paper.",
    },
    {
        "raw_title": "AI-Slop and Political Propaganda: The Role of AI-Generated Content in Memes and Influence Campaigns",
        "importance": "Curated",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Political propaganda and AI-generated meme/influence-campaign analysis.",
    },
    {
        "raw_title": "Exposing influence campaigns in the age of LLMs: a behavioral-based AI approach to detecting state-sponsored trolls",
        "importance": "Curated",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "State-sponsored troll detection paper relevant to LLM-era influence-operation monitoring.",
    },
    {
        "raw_title": "Recent Trends in Online Foreign Influence Efforts",
        "importance": "Curated",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Foreign-influence operations context for the LLM-enabled influence-ops literature.",
    },
    {
        "raw_title": "How Strategic Information Operations Affect Peacekeeping: Two Case Studies from the Central African Republic",
        "importance": "Curated",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Strategic information-operations case study tied to peacekeeping and conflict settings.",
    },
    {
        "raw_title": "The Language You Ask In: Language-Conditioned Ideological Divergence in LLM Analysis of Contested Political Documents",
        "importance": "Watchlist",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Recent zero-citation political-bias paper on contested documents and prompt language, retained for monitoring.",
    },
    {
        "raw_title": "Whose story wins? LLM-powered chatbots as sites and agents of memory-political contestation and corporate greenwashing",
        "importance": "Watchlist",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Memory-politics angle is relevant, but corporate-greenwashing drift keeps it on the watchlist.",
    },
    {
        "raw_title": "ALGORITHMIC DIPLOMACY: THE ROLE OF ARTIFICIAL INTELLIGENCE IN SHAPING 21ST CENTURY FOREIGN POLICY DECISIONS",
        "importance": "Watchlist",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "Diplomacy and international institutions",
        "reason": "Foreign-policy decision-making title is on-scope, but the paper is new, uncited, and likely conceptual.",
    },
    {
        "raw_title": "Strategic Reasoning with Language Models",
        "importance": "Curated",
        "theme": "Strategic Reasoning, Games, Negotiation, and Cooperation",
        "subtheme": "Game-theoretic and strategic reasoning benchmarks",
        "reason": "High-citation LLM strategic-reasoning paper retained as curated because it is generic rather than diplomatic or political.",
    },
    {
        "raw_title": "Simulating Strategic Reasoning: Comparing the Ability of Single LLMs and Multi-Agent Systems to Replicate Human Behavior",
        "importance": "Curated",
        "theme": "Strategic Reasoning, Games, Negotiation, and Cooperation",
        "subtheme": "Behavioral game tests and human-like strategy",
        "reason": "Strategic-reasoning simulation paper with policy/planning motivation, but generic game setting.",
    },
    {
        "raw_title": "Beyond Nash Equilibrium: Bounded Rationality of LLMs and humans in Strategic Decision-making",
        "importance": "Curated",
        "theme": "Strategic Reasoning, Games, Negotiation, and Cooperation",
        "subtheme": "Behavioral game tests and human-like strategy",
        "reason": "LLM bounded-rationality evaluation in behavioral games; relevant but not political enough for Important.",
    },
    {
        "raw_title": "LLM Generated Persona is a Promise with a Catch",
        "importance": "Important",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Critique accepted as Important because it audits persona generation using election forecasting and public-opinion survey tasks.",
    },
    {
        "raw_title": "Large Language Models as Subpopulation Representative Models: A Review",
        "importance": "Important",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Critique accepted as Important because it reviews LLMs as subpopulation representative models for opinion measurement.",
    },
    {
        "raw_title": "Vox Populi, Vox AI? Using Language Models to Estimate German Public Opinion",
        "importance": "Important",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Critique accepted as Important because it evaluates LLM synthetic samples against German election and public-opinion survey data.",
    },
    {
        "raw_title": "Valid Survey Simulations with Limited Human Data: The Roles of Prompting, Fine-Tuning, and Rectification",
        "importance": "Important",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Critique accepted as Important because it studies bias reduction and rectification for LLM survey simulations including politics.",
    },
    {
        "raw_title": "Simulating Public Opinion: Comparing Distributional and Individual-Level Predictions from LLMs and Random Forests",
        "importance": "Important",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Critique accepted as Important because it compares LLM public-opinion simulations against ANES political survey data.",
    },
    {
        "raw_title": "Understanding Online Polarization Through Human-Agent Interaction in a Synthetic LLM-Based Social Network",
        "importance": "Important",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Social networks, movements, and polarization",
        "reason": "Critique accepted as Important because it validates a synthetic LLM social network with human participants and polarization outcomes.",
    },
    {
        "raw_title": "Characterizing the ability of LLMs to recapitulate Americans'distributional responses to public opinion polling questions across political issues",
        "importance": "Important",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Critique accepted as Important because it directly evaluates political-issue polling distributions using LLMs.",
    },
    {
        "raw_title": "Before You Simulate: A Pre-Study Benchmark for Large Language Model Stability in Political Role-Playing Simulations",
        "importance": "Important",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Critique accepted as Important because it benchmarks stability in political role-playing simulations.",
    },
    {
        "raw_title": "Persona-driven Simulation of Voting Behavior in the European Parliament with Large Language Models",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Legislative and political-agent simulation",
        "reason": "Critique accepted as Important because it simulates European Parliament voting behavior with politician personas and policy votes.",
    },
    {
        "raw_title": "Psychologically-Valid Generative Agents: A Novel Approach to Agent-Based Modeling in Social Sciences",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Social-science generative-agent modeling framework with validation emphasis.",
    },
    {
        "raw_title": "Donald Trumps in the Virtual Polls: Simulating and Predicting Public Opinions in Surveys Using Large Language Models",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "LLM survey and election-outcome simulation paper retained as curated due to narrower evidence.",
    },
    {
        "raw_title": "This human study did not involve human subjects: Validating LLM simulations as behavioral evidence",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Broad but useful validation paper for synthetic behavioral evidence.",
    },
    {
        "raw_title": "BluePrint: A Social Media User Dataset for LLM Persona Evaluation and Training",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Social networks, movements, and polarization",
        "reason": "Political-discourse social-media persona dataset for evaluating LLM agents.",
    },
    {
        "raw_title": "TwinVoice: A Multi-dimensional Benchmark Towards Digital Twins via LLM Persona Simulation",
        "importance": "Watchlist",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "General digital-twin benchmark retained only as watchlist pending stronger political/public-opinion linkage.",
    },
    {
        "raw_title": "Human Preferences in Large Language Model Latent Space: A Technical Analysis on the Reliability of Synthetic Data in Voting Outcome Prediction",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Voting-outcome synthetic-data reliability paper with direct political-simulation relevance.",
    },
    {
        "raw_title": "Surveying with AI: Simulating Human Responses Using Personalized LLM Agents and Social Media Data",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Personalized LLM survey simulation using social-media data, but not explicitly political enough for Important.",
    },
    {
        "raw_title": "Can A Society of Generative Agents Simulate Human Behavior and Inform Public Health Policy? A Case Study on Vaccine Hesitancy",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic and institutional decision support",
        "reason": "Policy-simulation case study for vaccine hesitancy with generative agents.",
    },
    {
        "raw_title": "Validating Generative Agent-Based Models of Social Norm Enforcement: From Replication to Novel Predictions",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Synthetic populations and human samples",
        "reason": "Validation framework for generative agent-based models of social norm enforcement.",
    },
    {
        "raw_title": "Simulating Online Social Media Conversations on Controversial Topics Using AI Agents Calibrated on Real-World Data",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Social networks, movements, and polarization",
        "reason": "Calibrated LLM-agent simulation of controversial online political conversations.",
    },
    {
        "raw_title": "Adaptive political surveys and GPT-4: Tackling the cold start problem with simulated user interactions",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Public opinion, polling, and political annotation",
        "reason": "Adaptive political-survey paper using GPT-4 generated interaction data.",
    },
    {
        "raw_title": "LLM Agents Predict Social Media Reactions but Do Not Outperform Text Classifiers: Benchmarking Simulation Accuracy Using 120K+ Personas of 1511 Humans",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Social networks, movements, and polarization",
        "reason": "Large-persona benchmark for predicting social-media reactions, relevant to platform governance and democratic resilience.",
    },
    {
        "raw_title": "LLM Powered Social Digital Twins: A Framework for Simulating Population Behavioral Response to Policy Interventions",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic and institutional decision support",
        "reason": "LLM social digital twin framework for population response to policy interventions.",
    },
    {
        "raw_title": "POSIM: A Multi-Agent Simulation Framework for Social Media Public Opinion Evolution and Governance",
        "importance": "Curated",
        "theme": "Multi-Agent Social Simulation and Synthetic Societies",
        "subtheme": "Social networks, movements, and polarization",
        "reason": "LLM social-media public-opinion simulation framework for governance use cases.",
    },
    {
        "raw_title": "WhatIf: Interactive Exploration of LLM-Powered Social Simulations for Policy Reasoning",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Strategic and institutional decision support",
        "reason": "Interactive LLM-powered social simulation system for policy reasoning under uncertainty.",
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


def indexed_rows() -> dict[str, dict[str, str]]:
    rows = read_csv(SEARCH_LONG_LIST)
    rows.extend(read_csv(TRACE_LONG_LIST))
    rows.extend(read_csv(SOCIAL_TRACE))
    by_title: dict[str, dict[str, str]] = {}
    for row in rows:
        by_title[normalize(row["title"])] = row
    return by_title


def main() -> None:
    by_title = indexed_rows()
    output: list[dict[str, Any]] = []

    for rank, selection in enumerate(SELECTIONS, start=1):
        row = by_title.get(normalize(selection["raw_title"]))
        if not row:
            raise RuntimeError(f"Selected critique-round-3 paper not found: {selection['raw_title']}")
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
        "relation",
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
    print(f"critique_round3_curated_additions={len(output)}")


if __name__ == "__main__":
    main()

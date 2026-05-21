#!/usr/bin/env python3
"""Select curated additions from the critique-followup expansion pass."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_LONG_LIST = ROOT / "data" / "processed" / "critique_followup_expansion" / "candidate_related_papers_preliminary.csv"
SEARCH_LONG_LIST = ROOT / "data" / "processed" / "critique_followup_expansion" / "search_results_preliminary.csv"
OUTPUT = ROOT / "data" / "processed" / "critique_followup_expansion" / "curated_additions.csv"

SELECTIONS = [
    {
        "raw_title": "AI-Augmented Predictions: LLM Assistants Improve Human Forecasting Accuracy",
        "importance": "Important",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting performance and aggregation",
        "reason": "Critique accepted as Important because it is a strong human-plus-LLM forecasting experiment with nontrivial citation signal.",
    },
    {
        "raw_title": "AutoCast++: Enhancing World Event Prediction with Zero-shot Ranking-based Context Retrieval",
        "importance": "Important",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Geopolitical event prediction systems",
        "reason": "Critique accepted as Important because it is an ICLR world-event prediction paper tied to text-based forecasting.",
    },
    {
        "raw_title": "Automating Forecasting Question Generation and Resolution for AI Evaluation",
        "importance": "Curated",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting benchmarks and datasets",
        "reason": "Benchmark infrastructure for generating and resolving diverse real-world forecasting questions.",
    },
    {
        "raw_title": "PROPHET: An Inferable Future Forecasting Benchmark with Causal Intervened Likelihood Estimation",
        "importance": "Curated",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting benchmarks and datasets",
        "reason": "Future-event forecasting benchmark that screens whether questions are inferable from supporting evidence.",
    },
    {
        "raw_title": "Scaling Open-Ended Reasoning to Predict the Future",
        "importance": "Curated",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting performance and aggregation",
        "reason": "Open-ended forecasting system trained and tested on global event questions with leakage controls.",
    },
    {
        "raw_title": "LLM-as-a-Prophet: Understanding Predictive Intelligence with Prophet Arena",
        "importance": "Curated",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting benchmarks and datasets",
        "reason": "Live forecasting arena for evaluating predictive intelligence in LLMs.",
    },
    {
        "raw_title": "Crowdsourced versus large language models forecasting: evidence for the accuracy–correlation effect",
        "importance": "Curated",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting performance and aggregation",
        "reason": "ForecastBench-based comparison of LLM and human aggregate forecasting behavior.",
    },
    {
        "raw_title": "Scattered Hypothesis Generation for Open-Ended Event Forecasting",
        "importance": "Watchlist",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting performance and aggregation",
        "reason": "Recent open-ended event-forecasting method kept for monitoring until citation and benchmark signal improves.",
    },
    {
        "raw_title": "OracleProto: A Reproducible Framework for Benchmarking LLM Native Forecasting via Knowledge Cutoff and Temporal Masking",
        "importance": "Watchlist",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting benchmarks and datasets",
        "reason": "Recent reproducible forecasting benchmark framework with explicit knowledge-cutoff controls.",
    },
    {
        "raw_title": "TruthTensor: Evaluating LLMs through Human Imitation on Prediction Market under Drift and Holistic Reasoning",
        "importance": "Watchlist",
        "theme": "Forecasting, Geopolitical Risk, and Foresight",
        "subtheme": "Forecasting benchmarks and datasets",
        "reason": "Prediction-market evaluation framework retained as a watchlist item because it is relevant but may drift toward generic market forecasting.",
    },
    {
        "raw_title": "DeliberationBench: A Normative Benchmark for the Influence of Large Language Models on Users'Views",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Critique accepted as Important because it is a large preregistered policy-proposal benchmark for LLM influence in deliberation.",
    },
    {
        "raw_title": "Bringing Everyone to the Table: An Experimental Study of LLM-Facilitated Group Decision Making",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Critique accepted as Important because it is a preregistered group decision-making experiment with LLM facilitation.",
    },
    {
        "raw_title": "An Emergent Understanding of Human-AI Collaboration in Deliberation",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Critique accepted as Important because citizen assemblies make the deliberation setting directly democratic and policy-relevant.",
    },
    {
        "raw_title": "Hyperdemocracy: Towards Creative Consensus Building between Humans and AI",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Critique accepted as Important because it reports field validation in fragmented political contexts.",
    },
    {
        "raw_title": "Surfacing citizens’ policy perspectives at scale in the age of large language models",
        "importance": "Important",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Democratic governance and augmentation",
        "reason": "Critique accepted as Important because it directly targets citizen policy representation for public decision-making.",
    },
    {
        "raw_title": "Looking Under the Hood: How LLMs Attempt Political Persuasion and Microtargeting",
        "importance": "Important",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Deliberation, persuasion, and information environments",
        "reason": "Critique accepted as Important because it directly studies political persuasion and microtargeting by LLMs.",
    },
    {
        "raw_title": "Generative Social Choice",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "High-citation social-choice method for open-ended democratic aggregation with LLM-generated text.",
    },
    {
        "raw_title": "Prompt Injection Vulnerability of Consensus Generating Applications in Digital Democracy",
        "importance": "Curated",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Security risk paper tied narrowly to consensus-generating LLM applications in digital democracy.",
    },
    {
        "raw_title": "Leveraging AI in peace processes: A framework for digital dialogues",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "AI-assisted deliberation framework for peace processes and conflict-affected environments.",
    },
    {
        "raw_title": "PTFA: An LLM-based Agent that Facilitates Online Consensus Building through Parallel Thinking",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Consensus-building agent using LLM facilitation; retained as a narrow deliberation method paper.",
    },
    {
        "raw_title": "Can AI Deliberate? Evaluating Deliberative Quality and Stance Flow in Multi-Agent LLMs",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Evaluates multi-agent LLM deliberation quality on policy-relevant issue contexts.",
    },
    {
        "raw_title": "Can AI mediation improve democratic deliberation?",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Direct reflection on AI mediation for participation, equality, and deliberative quality in democracy.",
    },
    {
        "raw_title": "Generating Fair Consensus Statements with Social Choice on Token-Level MDPs",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Social-choice method for fair consensus statement generation from free-form opinions.",
    },
    {
        "raw_title": "Assessing the Political Fairness of Multilingual LLMs: A Case Study based on a 21-way Multiparallel EuroParl Dataset",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "Political fairness audit using European Parliament speech translation across multilingual parliamentary data.",
    },
    {
        "raw_title": "A Multi-Dimensional Audit of Politically Aligned Large Language Models",
        "importance": "Curated",
        "theme": "Politics, Democracy, Public Opinion, and Persuasion",
        "subtheme": "Political ideology, representation, and bias",
        "reason": "New audit framework for politically aligned LLMs across effectiveness, fairness, truthfulness, and persuasiveness.",
    },
    {
        "raw_title": "Simulating Policy Discussions with Digital Footprints and Large Language Models",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Democratic governance and augmentation",
        "reason": "Policy-discussion simulation using parliamentary digital traces and LLMs.",
    },
    {
        "raw_title": "Preserving Disagreement: Architectural Heterogeneity and Coherence Validation in Multi-Agent Policy Simulation",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Policy simulation paper focused on disagreement preservation rather than artificial consensus.",
    },
    {
        "raw_title": "Toward an artificial deliberation? On Google DeepMind’s Habermas Machine",
        "importance": "Curated",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Policy persuasion and democratic deliberation",
        "reason": "Analysis of the Habermas Machine and whether LLM mediation satisfies deliberative-democracy ideals.",
    },
    {
        "raw_title": "Digital Homunculi and Institutional Design: Breaking Through the Experimentation Bottleneck",
        "importance": "Watchlist",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Democratic governance and augmentation",
        "reason": "Institutional-design simulation paper retained as a watchlist item pending stronger validation signal.",
    },
    {
        "raw_title": "Democracy-in-Silico: Institutional Design as Alignment in AI-Governed Polities",
        "importance": "Watchlist",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Democratic governance and augmentation",
        "reason": "AI-governed polity simulation retained as a watchlist item because it is precise but very new.",
    },
    {
        "raw_title": "Using LLMs to Enhance Democracy",
        "importance": "Watchlist",
        "theme": "Policymaking, Governance, and Institutional Decision Support",
        "subtheme": "Democratic governance and augmentation",
        "reason": "Direct democracy-focused position paper kept for review because it is broad and low-citation.",
    },
    {
        "raw_title": "New parameters of power: On LLM-based manipulation and control and the spectre of strategic AI",
        "importance": "Watchlist",
        "theme": "AI Safety, Influence Operations, and Societal Risk",
        "subtheme": "Influence operations and persuasion risk",
        "reason": "Recent power/manipulation paper retained as watchlist because the political-power link is relevant but broad.",
    },
    {
        "raw_title": "Integrating Generative AI into Tactical Military Decision-Making",
        "importance": "Watchlist",
        "theme": "Geopolitics, Diplomacy, National Security, and Wargaming",
        "subtheme": "Military decision-making and wargaming",
        "reason": "WARBENCH-adjacent tactical military decision-making paper kept as watchlist pending stronger evaluation evidence.",
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
            raise RuntimeError(f"Selected critique-followup paper not found: {selection['raw_title']}")
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
    print(f"critique_followup_curated_additions={len(output)}")


if __name__ == "__main__":
    main()

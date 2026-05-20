#!/usr/bin/env python3
"""Select priority expansion seeds and second-order candidates."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIRST_ORDER = ROOT / "data" / "processed" / "candidate_additions_strategy.csv"
CORE_SEEDS = ROOT / "data" / "raw" / "core_seed_papers.csv"
PRIORITY_SEEDS = ROOT / "data" / "processed" / "priority_expansion_seeds.csv"
SECOND_ORDER_LONG = ROOT / "data" / "processed" / "second_order" / "candidate_related_papers_preliminary.csv"
SECOND_ORDER_SELECTED = ROOT / "data" / "processed" / "second_order_candidate_additions_strategy.csv"

EXCLUDE_RE = re.compile(
    r"\b("
    r"finance|financial|stock|stocks|trading|portfolio|investment|investor|"
    r"banking|bitcoin|cryptocurrenc|accounting|earnings|fund|retail investing|"
    r"healthcare|medical|clinical|surgical|vaccine|autonomous vehicles|robotics"
    r")\b",
    re.I,
)

INCLUDE_RE = re.compile(
    r"\b("
    r"politic|geopolitic|governance|democracy|election|policy|policymak|"
    r"diplomac|diplomacy|military|wargam|war\b|conflict|national security|"
    r"foreign policy|strategic|strategy|decision[- ]making|forecast|forecasting|"
    r"world events|international events|event prediction|prediction market|"
    r"social simulation|social agents|human samples|negotiation|cooperation|"
    r"polarization|legislative|public opinion|polling"
    r")\b",
    re.I,
)

GENERIC_TITLE_RE = re.compile(
    r"\b("
    r"llama|gpt-4|bert|tree of thoughts|reflexion|attention is all you need|"
    r"chain[- ]of[- ]thought|retrieval[- ]augmented generation|direct preference optimization|"
    r"large language model based multi-agents: a survey|agentbench|agentverse|"
    r"making pre-trained language models better few-shot learners"
    r")\b",
    re.I,
)

SECOND_ORDER_SELECTION = [
    ("recent_relevant_2024_plus", "Behavioral and Opinion Simulation", "A Turing test of whether AI chatbots are behaviorally similar to humans"),
    ("recent_relevant_2024_plus", "Politics, Governance, and Public Opinion", "Generative Echo Chamber? Effect of LLM-Powered Search Systems on Diverse Information Seeking"),
    ("recent_relevant_2024_plus", "Strategic Risk and Safety", "Multi-Agent Risks from Advanced AI"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Generative Artificial Intelligence and Evaluating Strategic Decisions"),
    ("recent_relevant_2024_plus", "Politics, Governance, and Public Opinion", "Systematic Biases in LLM Simulations of Debates"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "LLM as a Mastermind: A Survey of Strategic Reasoning with Large Language Models"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations"),
    ("recent_relevant_2024_plus", "Multi-Agent Social and Political Simulation", "OASIS: Open Agent Social Interaction Simulations with One Million Agents"),
    ("recent_relevant_2024_plus", "Politics, Governance, and Public Opinion", "Performance and biases of Large Language Models in public opinion simulation"),
    ("recent_relevant_2024_plus", "Multi-Agent Social and Political Simulation", "Unveiling the Truth and Facilitating Change: Towards Agent-based Large-scale Social Movement Simulation"),
    ("recent_relevant_2024_plus", "Politics, Governance, and Public Opinion", "From Skepticism to Acceptance: Simulating the Attitude Dynamics Toward Fake News"),
    ("recent_relevant_2024_plus", "Politics, Governance, and Public Opinion", "Hidden Persuaders: LLMs’ Political Leaning and Their Influence on Voters"),
    ("recent_relevant_2024_plus", "Politics, Governance, and Public Opinion", "LLM-generated messages can persuade humans on policy issues"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "GameBench: Evaluating Strategic Reasoning Abilities of LLM Agents"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "How Far Are We on the Decision-Making of LLMs? Evaluating LLMs' Gaming Ability in Multi-Agent Environments"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Nicer Than Humans: How do Large Language Models Behave in the Prisoner's Dilemma?"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Game-theoretic LLM: Agent Workflow for Negotiation Games"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Decision-Making Behavior Evaluation Framework for LLMs under Uncertain Context"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Simulating Human Strategic Behavior: Comparing Single and Multi-agent LLMs"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Shall We Team Up: Exploring Spontaneous Cooperation of Competing LLM Agents"),
    ("recent_relevant_2024_plus", "Politics, Governance, and Public Opinion", "Random Silicon Sampling: Simulating Human Sub-Population Opinion Using a Large Language Model Based on Group-Level Demographic Information"),
    ("recent_relevant_2024_plus", "Behavioral and Opinion Simulation", "Beyond Demographics: Aligning Role-playing LLM-based Agents Using Human Belief Networks"),
    ("recent_relevant_2024_plus", "Multi-Agent Social and Political Simulation", "GenSim: A General Social Simulation Platform with Large Language Model based Agents"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Measuring Bargaining Abilities of LLMs: A Benchmark and A Buyer-Enhancement Method"),
    ("recent_relevant_2024_plus", "Multi-Agent Social and Political Simulation", "SocioVerse: A World Model for Social Simulation Powered by LLM Agents and A Pool of 10 Million Real-World Users"),
    ("recent_relevant_2024_plus", "Multi-Agent Social and Political Simulation", "Agent-Based Modelling Meets Generative AI in Social Network Simulations"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Game Theory Meets Large Language Models: A Systematic Survey"),
    ("recent_relevant_2024_plus", "Politics, Governance, and Public Opinion", "Decoding Echo Chambers: LLM-Powered Simulations Revealing Polarization in Social Networks"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Multi-Agent, Human-Agent and Beyond: A Survey on Cooperation in Social Dilemmas"),
    ("recent_relevant_2024_plus", "Geopolitics, Diplomacy, and Strategic Simulation", "COA-GPT: Generative Pre-Trained Transformers for Accelerated Course of Action Development in Military Operations"),
    ("recent_relevant_2024_plus", "Geopolitics, Diplomacy, and Strategic Simulation", "BattleAgent: Multi-modal Dynamic Emulation on Historical Battles to Complement Historical Analysis"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "Cultural Evolution of Cooperation among LLM Agents"),
    ("recent_relevant_2024_plus", "Strategic Reasoning and Decision-Making", "A Survey on Large Language Model-Based Social Agents in Game-Theoretic Scenarios"),
    ("recent_relevant_2024_plus", "Politics, Governance, and Public Opinion", "A Public Dataset Tracking Social Media Discourse about the 2024 U.S. Presidential Election on Twitter/X"),
    ("high_citation_relevant", "Politics, Governance, and Public Opinion", "More human than human: measuring ChatGPT political bias"),
    ("high_citation_relevant", "Politics, Governance, and Public Opinion", "Should ChatGPT be Biased? Challenges and Risks of Bias in Large Language Models"),
    ("high_citation_relevant", "Politics, Governance, and Public Opinion", "The political ideology of conversational AI: Converging evidence on ChatGPT's pro-environmental, left-libertarian orientation"),
    ("high_citation_relevant", "Politics, Governance, and Public Opinion", "Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations"),
    ("high_citation_relevant", "Strategic Risk and Safety", "AI deception: A survey of examples, risks, and potential solutions"),
    ("high_citation_relevant", "Politics, Governance, and Public Opinion", "Cultural bias and cultural alignment of large language models"),
    ("high_citation_relevant", "Strategic Reasoning and Decision-Making", "SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents"),
    ("high_citation_relevant", "Strategic Reasoning and Decision-Making", "Exploring Large Language Models for Communication Games: An Empirical Study on Werewolf"),
    ("high_citation_relevant", "Strategic Reasoning and Decision-Making", "Improving Language Model Negotiation with Self-Play and In-Context Learning from AI Feedback"),
    ("high_citation_relevant", "Multi-Agent Social and Political Simulation", "Social Simulacra: Creating Populated Prototypes for Social Computing Systems"),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def normalize(value: str) -> str:
    return " ".join((value or "").lower().split())


def as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def looks_relevant(row: dict[str, str]) -> bool:
    text = f"{row.get('title', '')} {row.get('abstract', '')}"
    if EXCLUDE_RE.search(text):
        return False
    if GENERIC_TITLE_RE.search(row.get("title", "")):
        return False
    return bool(INCLUDE_RE.search(text))


def build_priority_seeds() -> list[dict[str, str]]:
    rows = read_csv(FIRST_ORDER)
    selected: dict[str, dict[str, str]] = {}

    for row in rows:
        year = as_int(row.get("year"))
        citations = as_int(row.get("citationCount"))
        seed_hits = as_int(row.get("seed_overlap_count"))
        title = row["title"]
        buckets = []
        reasons = []

        if year >= 2024 and (citations >= 20 or (citations >= 5 and seed_hits >= 2)):
            buckets.append("recent_relevant_2024_plus")
            reasons.append(f"recent ({year}), citations={citations}, seed_hits={seed_hits}")

        if citations >= 100:
            buckets.append("high_citation_relevant")
            reasons.append(f"high citation count ({citations})")

        if not buckets:
            continue

        selected[normalize(title)] = {
            "expansion_bucket": "; ".join(buckets),
            "selection_reason": "; ".join(reasons),
            "id": row.get("curated_rank", ""),
            "priority": "Core",
            "category": row.get("curated_category", ""),
            "title": title,
            "year_or_timeframe": row.get("year", ""),
            "citationCount": row.get("citationCount", ""),
            "seed_overlap_count": row.get("seed_overlap_count", ""),
            "source_url": row.get("url", ""),
            "notes": "Selected from first-order Semantic Scholar expansion for second-order expansion.",
        }

    output = sorted(
        selected.values(),
        key=lambda row: (
            "recent_relevant_2024_plus" not in row["expansion_bucket"],
            -as_int(row["citationCount"]),
            row["title"].lower(),
        ),
    )
    columns = [
        "expansion_bucket",
        "selection_reason",
        "id",
        "priority",
        "category",
        "title",
        "year_or_timeframe",
        "citationCount",
        "seed_overlap_count",
        "source_url",
        "notes",
    ]
    write_csv(PRIORITY_SEEDS, output, columns)
    return output


def build_second_order_candidates() -> list[dict[str, str]]:
    if not SECOND_ORDER_LONG.exists():
        return []

    rows = read_csv(SECOND_ORDER_LONG)
    by_title = {normalize(row["title"]): row for row in rows}
    selected_rows: list[dict[str, str]] = []

    for bucket, category, title in SECOND_ORDER_SELECTION:
        row = by_title.get(normalize(title))
        if not row:
            raise RuntimeError(f"Selected second-order candidate not found: {title}")
        citations = as_int(row.get("citationCount"))
        seed_hits = as_int(row.get("seed_overlap_count"))
        selected_rows.append(
            {
                "selection_bucket": bucket,
                "curated_category": category,
                "selection_reason": f"manual high-relevance selection; citations={citations}; seed_hits={seed_hits}",
                **row,
            }
        )

    output = sorted(
        selected_rows,
        key=lambda row: (
            row["selection_bucket"] != "recent_relevant_2024_plus",
            row["curated_category"],
            -as_int(row.get("citationCount")),
            -as_int(row.get("seed_overlap_count")),
            row.get("title", "").lower(),
        ),
    )

    for index, row in enumerate(output, start=1):
        row["selected_rank"] = str(index)

    columns = [
        "selected_rank",
        "selection_bucket",
        "curated_category",
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
    write_csv(SECOND_ORDER_SELECTED, output, columns)
    return output


def build_second_order_candidates_auto() -> list[dict[str, str]]:
    if not SECOND_ORDER_LONG.exists():
        return []

    rows = read_csv(SECOND_ORDER_LONG)
    known_titles = {normalize(row["title"]) for row in read_csv(CORE_SEEDS)}
    known_titles.update(normalize(row["title"]) for row in read_csv(FIRST_ORDER))
    known_titles.update(normalize(row["title"]) for row in read_csv(PRIORITY_SEEDS))

    selected: dict[str, dict[str, str]] = {}
    for row in rows:
        title_key = normalize(row.get("title", ""))
        if not title_key or title_key in known_titles or title_key in selected:
            continue
        if not looks_relevant(row):
            continue

        year = as_int(row.get("year"))
        citations = as_int(row.get("citationCount"))
        seed_hits = as_int(row.get("seed_overlap_count"))
        buckets = []
        reasons = []

        if year >= 2024 and (citations >= 10 or (citations >= 3 and seed_hits >= 2)):
            buckets.append("recent_relevant_2024_plus")
            reasons.append(f"recent ({year}), citations={citations}, seed_hits={seed_hits}")

        if citations >= 100:
            buckets.append("high_citation_relevant")
            reasons.append(f"high citation count ({citations})")

        if not buckets:
            continue

        selected[title_key] = {
            "selection_bucket": "; ".join(buckets),
            "curated_category": "",
            "selection_reason": "; ".join(reasons),
            **row,
        }

    output = sorted(
        selected.values(),
        key=lambda row: (
            "recent_relevant_2024_plus" not in row["selection_bucket"],
            -as_int(row.get("citationCount")),
            -as_int(row.get("seed_overlap_count")),
            row.get("title", "").lower(),
        ),
    )[:60]

    for index, row in enumerate(output, start=1):
        row["selected_rank"] = str(index)

    columns = [
        "selected_rank",
        "selection_bucket",
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
    write_csv(SECOND_ORDER_SELECTED, output, columns)
    return output


def main() -> None:
    priority = build_priority_seeds()
    print(f"priority_expansion_seeds={len(priority)}")
    second_order = build_second_order_candidates()
    if second_order:
        print(f"second_order_selected={len(second_order)}")
    else:
        print("second_order_selected=0 (run second-order expansion first)")


if __name__ == "__main__":
    main()

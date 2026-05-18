#!/usr/bin/env python3
"""Build human-reviewable CSV views from the raw Semantic Scholar expansion."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "between",
    "for",
    "from",
    "in",
    "into",
    "of",
    "on",
    "the",
    "to",
    "using",
    "with",
}

DOMAIN_TERMS = {
    "finance",
    "financial",
    "investment",
    "investing",
    "stock",
    "stocks",
    "trading",
    "trade",
    "portfolio",
    "equity",
    "market",
    "markets",
    "bank",
    "banking",
    "sec",
    "filing",
    "10-k",
    "xbrl",
    "finbert",
    "fingpt",
    "geopolitical",
    "geopolitics",
    "geoeconomic",
    "macroeconomic",
    "policy",
    "political",
    "politics",
    "governance",
    "democracy",
    "diplomatic",
    "diplomacy",
    "wargame",
    "military",
    "supply",
    "forecast",
    "forecasting",
}

LLM_TERMS = {
    "llm",
    "llms",
    "large",
    "language",
    "model",
    "models",
    "chatgpt",
    "gpt",
    "generative",
    "agent",
    "agents",
}

GENERIC_DUPLICATE_TOKENS = DOMAIN_TERMS | LLM_TERMS | {
    "survey",
    "benchmark",
    "benchmarks",
    "dataset",
    "datasets",
    "evaluation",
    "reasoning",
    "analysis",
    "applications",
    "framework",
    "system",
    "domain",
    "real-time",
    "large-scale",
}

OUTPUT_COLUMNS = [
    "rank",
    "curated_category",
    "paperId",
    "title",
    "year",
    "citationCount",
    "venue",
    "relevance_score",
    "seed_overlap_count",
    "relation_summary",
    "source_seed_titles",
    "why_include",
    "url",
    "doi",
    "arxiv",
    "authors",
    "abstract",
]


def normalize(value: str) -> str:
    return " ".join((value or "").lower().split())


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", normalize(value))
        if len(token) > 1 and token not in STOPWORDS
    }


def title_similarity(left: str, right: str) -> float:
    left_tokens = tokens(left)
    right_tokens = tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def is_seed_duplicate(title: str, seed_titles: list[str]) -> bool:
    candidate_tokens = tokens(title)
    distinctive_candidate_tokens = {
        token
        for token in candidate_tokens
        if len(token) >= 7 and token not in GENERIC_DUPLICATE_TOKENS
    }
    for seed_title in seed_titles:
        similarity = title_similarity(title, seed_title)
        if similarity >= 0.52:
            return True
        seed_tokens = tokens(seed_title)
        distinctive_seed_tokens = {
            token
            for token in seed_tokens
            if len(token) >= 7 and token not in GENERIC_DUPLICATE_TOKENS
        }
        if distinctive_candidate_tokens & distinctive_seed_tokens:
            return True
    return False


def as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def category_for(row: dict[str, str]) -> str:
    text = f"{row.get('title', '')} {row.get('abstract', '')}".lower()
    title = row.get("title", "").lower()
    if "survey" in title or "review" in title or "overview" in title:
        return "Surveys and overviews"
    if any(term in text for term in ["politic", "governance", "democracy", "diplomatic", "wargame", "military"]):
        return "Strategy, governance, and political simulation"
    if any(term in text for term in ["macro", "geopolitical", "geoeconomic", "forecast", "central bank"]):
        return "Macro, forecasting, and geoeconomics"
    if any(term in text for term in ["xbrl", "sec filing", "10-k", "annual report", "financial statement"]):
        return "Financial reports, filings, and accounting"
    if any(term in text for term in ["trading", "stock", "portfolio", "equity", "investment", "market"]):
        return "Markets, trading, and investment agents"
    if any(term in title for term in ["finbert", "fingpt", "financial language", "financial large language", "finance large language"]):
        return "Financial domain language models"
    if any(term in text for term in ["benchmark", "dataset", "evaluation", "qa", "question answering"]):
        return "Financial benchmarks and datasets"
    if any(term in title for term in ["financial", "finance", "fingpt"]):
        return "Financial domain language models"
    return "Other high-signal candidate"


def has_domain_signal(row: dict[str, str]) -> bool:
    text_tokens = tokens(f"{row.get('title', '')} {row.get('abstract', '')[:1200]}")
    return bool(text_tokens & DOMAIN_TERMS)


def has_llm_signal(row: dict[str, str]) -> bool:
    text_tokens = tokens(f"{row.get('title', '')} {row.get('abstract', '')[:1200]}")
    return bool(text_tokens & LLM_TERMS)


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    seed_path = base / "data" / "seeds_enriched.csv"
    candidate_path = base / "data" / "candidate_related_papers_preliminary.csv"
    if not seed_path.exists():
        seed_path = base / "data" / "processed" / "seed_papers_enriched_110.csv"
    if not candidate_path.exists():
        candidate_path = base / "data" / "processed" / "related_work_longlist_110.csv"
    seeds = read_csv(seed_path)
    candidates = read_csv(candidate_path)

    seed_titles = []
    for seed in seeds:
        if seed.get("seed_title"):
            seed_titles.append(seed["seed_title"])
        if seed.get("resolved_title"):
            seed_titles.append(seed["resolved_title"])

    additions: list[dict[str, Any]] = []
    foundation: list[dict[str, Any]] = []
    seen_titles: set[str] = set()

    for row in candidates:
        title = row.get("title", "")
        normalized_title = normalize(title)
        if not title or normalized_title in seen_titles:
            continue
        seen_titles.add(normalized_title)
        if is_seed_duplicate(title, seed_titles):
            continue

        domain_signal = has_domain_signal(row)
        llm_signal = has_llm_signal(row)
        score = as_float(row.get("relevance_score"))
        overlap = as_int(row.get("seed_overlap_count"))
        citation_count = as_int(row.get("citationCount"))

        if domain_signal and (score >= 24 or overlap >= 2 or citation_count >= 50):
            curated = {**row, "curated_category": category_for(row)}
            additions.append(curated)
        elif llm_signal and citation_count >= 1000 and overlap >= 3:
            foundation.append({**row, "curated_category": "Foundation/context paper"})

    additions.sort(key=lambda row: (-as_float(row.get("relevance_score")), -as_int(row.get("citationCount"))))
    foundation.sort(key=lambda row: (-as_int(row.get("citationCount")), str(row.get("title", "")).lower()))

    for idx, row in enumerate(additions, start=1):
        row["rank"] = idx
    for idx, row in enumerate(foundation, start=1):
        row["rank"] = idx

    write_csv(base / "data" / "processed" / "curated_additions_preliminary_110.csv", additions[:500], OUTPUT_COLUMNS)
    write_csv(base / "data" / "processed" / "foundation_context_papers_110.csv", foundation[:100], OUTPUT_COLUMNS)
    print(f"curated_additions={min(len(additions), 500)}")
    print(f"foundation_context={min(len(foundation), 100)}")


if __name__ == "__main__":
    main()

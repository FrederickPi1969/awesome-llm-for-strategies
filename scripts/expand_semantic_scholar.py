#!/usr/bin/env python3
"""Expand seed paper lists through Semantic Scholar citations/references.

The script is intentionally conservative: it enriches every seed paper it can
resolve, expands only high-priority seeds by default, then ranks missing papers
by topical relevance, citation count, and how often they appear around seeds.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any


BASE_URL = "https://api.semanticscholar.org/graph/v1"
DEFAULT_KEYS_FILE = Path(os.environ.get("SEMANTIC_SCHOLAR_API_KEYS_FILE", "semantic_scholar_api_keys.json"))

PAPER_FIELD_NAMES = [
    "paperId",
    "title",
    "year",
    "citationCount",
    "referenceCount",
    "venue",
    "publicationVenue",
    "publicationTypes",
    "authors",
    "externalIds",
    "url",
    "abstract",
]

PAPER_FIELDS = ",".join(PAPER_FIELD_NAMES)

EDGE_FIELDS = ",".join(
    [
        "intents",
        "isInfluential",
        *(f"citingPaper.{field}" for field in PAPER_FIELD_NAMES),
    ]
)

REFERENCE_FIELDS = ",".join(
    [
        "intents",
        "isInfluential",
        *(f"citedPaper.{field}" for field in PAPER_FIELD_NAMES),
    ]
)

TOPIC_KEYWORDS = {
    "llm": 5,
    "large language model": 5,
    "language models": 4,
    "generative ai": 3,
    "chatgpt": 4,
    "agent": 2,
    "agents": 2,
    "politics": 5,
    "political": 5,
    "political science": 5,
    "policy": 5,
    "policymaking": 5,
    "governance": 5,
    "democracy": 4,
    "election": 4,
    "legislative": 4,
    "geopolitical": 5,
    "geopolitics": 5,
    "diplomatic": 5,
    "diplomacy": 5,
    "foreign policy": 5,
    "military": 4,
    "wargame": 5,
    "strategic": 5,
    "strategy": 5,
    "decision-making": 5,
    "decision making": 5,
    "risk": 3,
    "uncertainty": 3,
    "macroeconomic": 2,
    "forecast": 3,
    "forecasting": 3,
    "event prediction": 4,
    "social simulation": 4,
    "agent-based modeling": 4,
}

STRONG_TOPIC_TERMS = {
    "geopolitical",
    "geopolitics",
    "political",
    "politics",
    "policy",
    "policymaking",
    "governance",
    "democracy",
    "diplomatic",
    "diplomacy",
    "foreign policy",
    "strategic",
    "strategy",
    "decision-making",
    "decision making",
    "wargame",
    "military",
    "forecast",
    "forecasting",
    "event prediction",
    "social simulation",
}

SEED_COLUMNS = [
    "seed_file",
    "seed_id",
    "seed_priority",
    "seed_category",
    "seed_title",
    "seed_short_name",
    "seed_source_url",
    "seed_notes",
    "resolved_paperId",
    "resolved_title",
    "match_status",
    "year",
    "citationCount",
    "referenceCount",
    "venue",
    "publicationTypes",
    "authors",
    "doi",
    "arxiv",
    "url",
    "abstract",
]

CANDIDATE_COLUMNS = [
    "rank",
    "paperId",
    "title",
    "year",
    "citationCount",
    "referenceCount",
    "venue",
    "publicationTypes",
    "authors",
    "doi",
    "arxiv",
    "url",
    "relevance_score",
    "keyword_score",
    "seed_overlap_count",
    "relation_summary",
    "source_seed_titles",
    "why_include",
    "abstract",
]

EDGE_COLUMNS = [
    "source_seed_title",
    "source_seed_priority",
    "source_seed_category",
    "source_paperId",
    "relation",
    "isInfluential",
    "intents",
    "candidate_paperId",
    "candidate_title",
    "candidate_year",
    "candidate_citationCount",
]


def normalize_title(value: str) -> str:
    return " ".join((value or "").lower().split())


def title_tokens(value: str) -> set[str]:
    stopwords = {
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
    return {
        token
        for token in re.findall(r"[a-z0-9]+", normalize_title(value))
        if len(token) > 1 and token not in stopwords
    }


def title_similarity(left: str, right: str) -> float:
    left_tokens = title_tokens(left)
    right_tokens = title_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def canonical_key(paper: dict[str, Any]) -> str:
    return paper.get("paperId") or f"{normalize_title(paper.get('title', ''))}|{paper.get('year', '')}"


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def authors_to_string(authors_raw: Any) -> str:
    if not isinstance(authors_raw, list):
        return ""
    names = []
    for author in authors_raw:
        if isinstance(author, dict) and author.get("name"):
            names.append(str(author["name"]).strip())
    return "; ".join(names)


def paper_to_row(paper: dict[str, Any]) -> dict[str, Any]:
    external = paper.get("externalIds") or {}
    publication_types = paper.get("publicationTypes") or []
    return {
        "paperId": paper.get("paperId") or "",
        "title": paper.get("title") or "",
        "year": paper.get("year") if paper.get("year") is not None else "",
        "citationCount": paper.get("citationCount") if paper.get("citationCount") is not None else "",
        "referenceCount": paper.get("referenceCount") if paper.get("referenceCount") is not None else "",
        "venue": paper.get("venue") or "",
        "publicationTypes": "; ".join(publication_types) if isinstance(publication_types, list) else "",
        "authors": authors_to_string(paper.get("authors")),
        "doi": external.get("DOI") or "",
        "arxiv": external.get("ArXiv") or "",
        "url": paper.get("url") or "",
        "abstract": paper.get("abstract") or "",
    }


class SemanticScholarClient:
    def __init__(self, api_keys: list[str], min_interval_seconds: float, timeout_seconds: int) -> None:
        keys = []
        seen = set()
        for key in api_keys:
            key = key.strip()
            if key and key not in seen:
                keys.append(key)
                seen.add(key)
        if not keys:
            raise ValueError("No Semantic Scholar API keys were provided.")
        self.api_keys = keys
        self.min_interval_seconds = max(1.0, min_interval_seconds)
        self.timeout_seconds = timeout_seconds
        self.next_allowed = [0.0 for _ in keys]
        self.next_index = 0
        self.request_count = 0

    def _acquire_key(self) -> tuple[int, str]:
        while True:
            now = time.monotonic()
            for offset in range(len(self.api_keys)):
                idx = (self.next_index + offset) % len(self.api_keys)
                if now >= self.next_allowed[idx]:
                    self.next_index = (idx + 1) % len(self.api_keys)
                    return idx, self.api_keys[idx]
            time.sleep(max(0.05, min(self.next_allowed) - now))

    def get_json(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        query = urllib.parse.urlencode(params, doseq=True)
        url = f"{BASE_URL}{path}?{query}"
        last_error = ""
        for attempt in range(6):
            idx, key = self._acquire_key()
            request = urllib.request.Request(
                url,
                headers={"x-api-key": key, "Accept": "application/json"},
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    self.next_allowed[idx] = time.monotonic() + self.min_interval_seconds
                    self.request_count += 1
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                self.next_allowed[idx] = time.monotonic() + self.min_interval_seconds
                self.request_count += 1
                last_error = f"HTTP {exc.code}: {body[:300]}"
                if exc.code == 429:
                    retry_after = exc.headers.get("Retry-After")
                    try:
                        delay = float(retry_after) if retry_after else self.min_interval_seconds
                    except ValueError:
                        delay = self.min_interval_seconds
                    self.next_allowed[idx] = max(self.next_allowed[idx], time.monotonic() + delay)
                    continue
                if 500 <= exc.code < 600:
                    time.sleep(max(self.min_interval_seconds, 2**attempt))
                    continue
                raise RuntimeError(f"{last_error} for {url}") from exc
            except urllib.error.URLError as exc:
                last_error = str(exc)
                time.sleep(max(self.min_interval_seconds, 2**attempt))
        raise RuntimeError(f"Request failed for {url}: {last_error}")


def load_api_keys(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    keys = payload.get("api_keys")
    if not isinstance(keys, list):
        raise ValueError(f"Expected api_keys array in {path}")
    return [str(key) for key in keys if str(key).strip()]


def read_seed_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def seed_record(path: Path, row: dict[str, str]) -> dict[str, str]:
    return {
        "seed_file": path.name,
        "seed_id": row.get("id", ""),
        "seed_priority": row.get("priority", ""),
        "seed_category": row.get("primary_category") or row.get("category", ""),
        "seed_title": row.get("title", ""),
        "seed_short_name": row.get("short_name", ""),
        "seed_source_url": row.get("source_url", ""),
        "seed_notes": row.get("notes", ""),
    }


def should_expand(seed: dict[str, str]) -> bool:
    priority = (seed.get("seed_priority") or "").lower()
    return priority in {"core", "important"} or "important" in priority


def resolve_paper(client: SemanticScholarClient, title: str) -> tuple[dict[str, Any] | None, str]:
    payload = client.get_json(
        "/paper/search",
        {"query": title, "limit": 10, "fields": PAPER_FIELDS},
    )
    candidates = payload.get("data") or []
    if not candidates:
        return None, "not_found"
    target = normalize_title(title)
    for candidate in candidates:
        if normalize_title(candidate.get("title", "")) == target:
            return candidate, "exact"
    best = max(candidates, key=lambda candidate: title_similarity(title, candidate.get("title", "")))
    similarity = title_similarity(title, best.get("title", ""))
    if similarity >= 0.72:
        return best, "near"
    return best, "low_confidence_top_result"


def fetch_relation(
    client: SemanticScholarClient,
    paper_id: str,
    relation: str,
    max_rows: int,
) -> list[dict[str, Any]]:
    if relation == "citation":
        endpoint, fields, paper_key = "citations", EDGE_FIELDS, "citingPaper"
    else:
        endpoint, fields, paper_key = "references", REFERENCE_FIELDS, "citedPaper"

    rows: list[dict[str, Any]] = []
    offset = 0
    while len(rows) < max_rows:
        limit = min(1000, max_rows - len(rows))
        payload = client.get_json(
            f"/paper/{paper_id}/{endpoint}",
            {"offset": offset, "limit": limit, "fields": fields},
        )
        for edge in payload.get("data") or []:
            paper = edge.get(paper_key) or {}
            if paper.get("paperId") or paper.get("title"):
                rows.append(
                    {
                        "paper": paper,
                        "intents": "; ".join(edge.get("intents") or []),
                        "isInfluential": bool(edge.get("isInfluential", False)),
                    }
                )
        next_offset = payload.get("next")
        if next_offset is None:
            break
        offset = int(next_offset)
    return rows


def keyword_score(title: str, abstract: str, venue: str) -> int:
    haystack = f"{title} {abstract[:1600]} {venue}".lower()
    score = 0
    for term, weight in TOPIC_KEYWORDS.items():
        if term in haystack:
            score += weight
    has_llm = any(term in haystack for term in ["llm", "large language model", "language models", "chatgpt"])
    has_topic = any(term in haystack for term in STRONG_TOPIC_TERMS)
    if has_llm and has_topic:
        score += 8
    return score


def relation_summary(relations: list[str]) -> str:
    counts: dict[str, int] = defaultdict(int)
    for relation in relations:
        counts[relation] += 1
    return "; ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def inclusion_reason(row: dict[str, Any]) -> str:
    parts = []
    if row["seed_overlap_count"] >= 2:
        parts.append(f"appears around {row['seed_overlap_count']} seeds")
    citation_count = as_int(row.get("citationCount"))
    if citation_count >= 500:
        parts.append("very high citation count")
    elif citation_count >= 100:
        parts.append("high citation count")
    if row["keyword_score"] >= 18:
        parts.append("strong title/abstract topical match")
    elif row["keyword_score"] >= 10:
        parts.append("clear topical match")
    return "; ".join(parts) or "candidate surfaced by citation/reference expansion"


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", action="append", required=True, help="Seed CSV path. Repeatable.")
    parser.add_argument("--out-dir", required=True, help="Output directory.")
    parser.add_argument("--api-keys-file", default=str(DEFAULT_KEYS_FILE))
    parser.add_argument("--max-related-per-direction", type=int, default=250)
    parser.add_argument("--max-expansion-seeds", type=int, default=80)
    parser.add_argument("--min-interval-seconds", type=float, default=1.0)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--min-candidate-score", type=float, default=18.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir).expanduser().resolve()
    client = SemanticScholarClient(
        api_keys=load_api_keys(Path(args.api_keys_file).expanduser()),
        min_interval_seconds=args.min_interval_seconds,
        timeout_seconds=args.timeout_seconds,
    )

    seeds: list[dict[str, str]] = []
    for seed_path_raw in args.seed:
        seed_path = Path(seed_path_raw).expanduser().resolve()
        for row in read_seed_csv(seed_path):
            record = seed_record(seed_path, row)
            if record["seed_title"]:
                seeds.append(record)

    enriched_seeds: list[dict[str, Any]] = []
    seed_keys: set[str] = set()
    expandable: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for idx, seed in enumerate(seeds, start=1):
        print(f"[resolve {idx}/{len(seeds)}] {seed['seed_title']}", flush=True)
        try:
            paper, match_status = resolve_paper(client, seed["seed_title"])
        except Exception as exc:
            failures.append({"title": seed["seed_title"], "stage": "resolve", "error": str(exc)})
            paper, match_status = None, "error"
        paper_row = paper_to_row(paper or {})
        enriched = {**seed, **{f"resolved_{k}": v for k, v in paper_row.items() if k == "paperId"}}
        enriched["resolved_paperId"] = paper_row.get("paperId", "")
        enriched["resolved_title"] = paper_row.get("title", "")
        enriched["match_status"] = match_status
        for key, value in paper_row.items():
            if key != "paperId":
                enriched[key] = value
        enriched_seeds.append(enriched)
        if paper and match_status != "low_confidence_top_result":
            seed_keys.add(canonical_key(paper))
            seed_keys.add(normalize_title(seed["seed_title"]))
            seed_keys.add(normalize_title(paper.get("title", "")))
            if should_expand(seed):
                expandable.append({**seed, "paper": paper})

    expandable = expandable[: args.max_expansion_seeds]
    candidates: dict[str, dict[str, Any]] = {}
    candidate_sources: dict[str, set[str]] = defaultdict(set)
    candidate_relations: dict[str, list[str]] = defaultdict(list)
    edges: list[dict[str, Any]] = []

    for idx, seed in enumerate(expandable, start=1):
        paper = seed["paper"]
        source_id = paper.get("paperId", "")
        print(f"[expand {idx}/{len(expandable)}] {paper.get('title')}", flush=True)
        for relation in ["citation", "reference"]:
            try:
                related = fetch_relation(client, source_id, relation, args.max_related_per_direction)
            except Exception as exc:
                failures.append({"title": seed["seed_title"], "stage": relation, "error": str(exc)})
                continue
            for edge in related:
                candidate = edge["paper"]
                key = canonical_key(candidate)
                if not key:
                    continue
                candidates.setdefault(key, paper_to_row(candidate))
                candidate_sources[key].add(seed["seed_title"])
                candidate_relations[key].append(relation)
                edges.append(
                    {
                        "source_seed_title": seed["seed_title"],
                        "source_seed_priority": seed["seed_priority"],
                        "source_seed_category": seed["seed_category"],
                        "source_paperId": source_id,
                        "relation": relation,
                        "isInfluential": edge["isInfluential"],
                        "intents": edge["intents"],
                        "candidate_paperId": candidate.get("paperId", ""),
                        "candidate_title": candidate.get("title", ""),
                        "candidate_year": candidate.get("year", ""),
                        "candidate_citationCount": candidate.get("citationCount", ""),
                    }
                )

    ranked: list[dict[str, Any]] = []
    for key, row in candidates.items():
        title_norm = normalize_title(row.get("title", ""))
        if key in seed_keys or title_norm in seed_keys:
            continue
        k_score = keyword_score(row.get("title", ""), row.get("abstract", ""), row.get("venue", ""))
        citation_count = as_int(row.get("citationCount"))
        overlap = len(candidate_sources[key])
        recency_bonus = max(0, as_int(row.get("year")) - 2020) * 0.8
        relevance_score = k_score + min(18.0, math.log10(citation_count + 1) * 5.0) + overlap * 4 + recency_bonus
        if relevance_score < args.min_candidate_score:
            continue
        candidate_row = {
            **row,
            "keyword_score": k_score,
            "seed_overlap_count": overlap,
            "relation_summary": relation_summary(candidate_relations[key]),
            "source_seed_titles": " | ".join(sorted(candidate_sources[key])[:12]),
            "relevance_score": round(relevance_score, 2),
        }
        candidate_row["why_include"] = inclusion_reason(candidate_row)
        ranked.append(candidate_row)

    ranked.sort(
        key=lambda row: (
            -float(row["relevance_score"]),
            -as_int(row["seed_overlap_count"]),
            -as_int(row["citationCount"]),
            str(row["title"]).lower(),
        )
    )
    for idx, row in enumerate(ranked, start=1):
        row["rank"] = idx

    write_csv(out_dir / "seeds_enriched.csv", enriched_seeds, SEED_COLUMNS)
    write_csv(out_dir / "candidate_related_papers_preliminary.csv", ranked, CANDIDATE_COLUMNS)
    write_csv(out_dir / "expansion_edges_preliminary.csv", edges, EDGE_COLUMNS)
    write_csv(out_dir / "resolve_failures.csv", failures, ["title", "stage", "error"])

    summary = {
        "seed_count": len(seeds),
        "resolved_seed_count": sum(1 for row in enriched_seeds if row.get("resolved_paperId")),
        "expanded_seed_count": len(expandable),
        "edge_count": len(edges),
        "candidate_count_after_filter": len(ranked),
        "failure_count": len(failures),
        "requests": client.request_count,
        "max_related_per_direction": args.max_related_per_direction,
        "min_candidate_score": args.min_candidate_score,
    }
    (out_dir / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()

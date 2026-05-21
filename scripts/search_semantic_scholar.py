#!/usr/bin/env python3
"""Run conservative Semantic Scholar query searches for expansion passes."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from expand_semantic_scholar import (
    PAPER_FIELDS,
    DEFAULT_KEYS_FILE,
    SemanticScholarClient,
    load_api_keys,
    paper_to_row,
)


OUTPUT_COLUMNS = [
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
    "query_ids",
    "focus_areas",
    "queries",
    "abstract",
]


def normalize(value: str) -> str:
    return " ".join((value or "").lower().split())


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def read_queries(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", required=True, help="CSV with id, focus, query, max_results columns.")
    parser.add_argument("--out-dir", required=True, help="Output directory.")
    parser.add_argument("--api-keys-file", default=str(DEFAULT_KEYS_FILE))
    parser.add_argument("--default-max-results", type=int, default=50)
    parser.add_argument("--min-interval-seconds", type=float, default=1.0)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir).expanduser().resolve()
    client = SemanticScholarClient(
        api_keys=load_api_keys(Path(args.api_keys_file).expanduser()),
        min_interval_seconds=args.min_interval_seconds,
        timeout_seconds=args.timeout_seconds,
    )
    queries = read_queries(Path(args.queries).expanduser().resolve())

    by_key: dict[str, dict[str, Any]] = {}
    query_ids: dict[str, set[str]] = defaultdict(set)
    focus_areas: dict[str, set[str]] = defaultdict(set)
    query_texts: dict[str, set[str]] = defaultdict(set)
    failures: list[dict[str, str]] = []

    for idx, query in enumerate(queries, start=1):
        query_id = query.get("id", f"query-{idx}")
        text = query.get("query", "")
        if not text:
            continue
        max_results = as_int(query.get("max_results"), args.default_max_results)
        max_results = min(max(1, max_results), 100)
        print(f"[search {idx}/{len(queries)}] {query_id}: {text}", flush=True)
        try:
            payload = client.get_json(
                "/paper/search",
                {"query": text, "limit": max_results, "fields": PAPER_FIELDS},
            )
        except Exception as exc:
            failures.append({"id": query_id, "query": text, "error": str(exc)})
            continue
        for paper in payload.get("data") or []:
            key = paper.get("paperId") or f"{normalize(paper.get('title', ''))}|{paper.get('year', '')}"
            if not key:
                continue
            by_key.setdefault(key, paper_to_row(paper))
            query_ids[key].add(query_id)
            focus_areas[key].add(query.get("focus", ""))
            query_texts[key].add(text)

    rows = []
    for key, row in by_key.items():
        rows.append(
            {
                **row,
                "query_ids": "; ".join(sorted(query_ids[key])),
                "focus_areas": "; ".join(sorted(value for value in focus_areas[key] if value)),
                "queries": " | ".join(sorted(query_texts[key])),
            }
        )
    rows.sort(
        key=lambda row: (
            -len(row["query_ids"].split("; ")) if row.get("query_ids") else 0,
            -as_int(row.get("citationCount")),
            str(row.get("title", "")).lower(),
        )
    )
    for idx, row in enumerate(rows, start=1):
        row["rank"] = idx

    write_csv(out_dir / "search_results_preliminary.csv", rows, OUTPUT_COLUMNS)
    write_csv(out_dir / "search_failures.csv", failures, ["id", "query", "error"])
    summary = {
        "query_count": len(queries),
        "result_count": len(rows),
        "failure_count": len(failures),
        "requests": client.request_count,
    }
    (out_dir / "search_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()

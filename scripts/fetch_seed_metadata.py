#!/usr/bin/env python3
"""Enrich seed papers with Semantic Scholar metadata.

The script resolves each seed by arXiv id when possible, falling back to title
search. It writes one CSV with citation counts, authors, external ids, URL, and
abstracts for repository curation.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


BASE_URL = "https://api.semanticscholar.org/graph/v1"
FIELDS = ",".join(
    [
        "paperId",
        "title",
        "year",
        "citationCount",
        "influentialCitationCount",
        "venue",
        "authors",
        "externalIds",
        "url",
        "abstract",
        "publicationDate",
        "publicationTypes",
        "openAccessPdf",
    ]
)


def normalize_title(value: str) -> str:
    return " ".join(value.lower().split())


def parse_arxiv_id(url: str) -> str:
    match = re.search(r"arxiv\.org/(?:abs|html|pdf)/([^/?#]+)", url or "", re.I)
    if not match:
        return ""
    return re.sub(r"v\d+$", "", match.group(1).replace(".pdf", ""))


def load_api_keys(path: str | None, api_keys_csv: str | None) -> list[str]:
    if api_keys_csv:
        return [key.strip() for key in api_keys_csv.split(",") if key.strip()]
    if not path:
        return []
    payload = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    return [str(key).strip() for key in payload.get("api_keys", []) if str(key).strip()]


class SemanticScholarClient:
    def __init__(self, api_keys: list[str], min_interval_seconds: float) -> None:
        self.api_keys = api_keys or [""]
        self.min_interval_seconds = max(min_interval_seconds, 1.0)
        self.next_allowed = [0.0 for _ in self.api_keys]
        self.next_key = 0
        self.request_count = 0

    def _key(self) -> tuple[int, str]:
        while True:
            now = time.monotonic()
            for offset in range(len(self.api_keys)):
                idx = (self.next_key + offset) % len(self.api_keys)
                if now >= self.next_allowed[idx]:
                    self.next_key = (idx + 1) % len(self.api_keys)
                    return idx, self.api_keys[idx]
            time.sleep(max(0.01, min(self.next_allowed) - now))

    def get_json(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        query = urllib.parse.urlencode(params, doseq=True)
        url = f"{BASE_URL}{path}?{query}"
        last_error = ""
        for attempt in range(6):
            idx, api_key = self._key()
            headers = {"Accept": "application/json"}
            if api_key:
                headers["x-api-key"] = api_key
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    self.next_allowed[idx] = time.monotonic() + self.min_interval_seconds
                    self.request_count += 1
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                self.next_allowed[idx] = time.monotonic() + self.min_interval_seconds
                self.request_count += 1
                if exc.code == 429 and attempt < 5:
                    retry_after = exc.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else self.min_interval_seconds
                    self.next_allowed[idx] = time.monotonic() + max(delay, self.min_interval_seconds)
                    continue
                if 500 <= exc.code < 600 and attempt < 5:
                    time.sleep(max(self.min_interval_seconds, 2**attempt))
                    continue
                raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
            except urllib.error.URLError as exc:
                last_error = str(exc)
                if attempt < 5:
                    time.sleep(max(self.min_interval_seconds, 2**attempt))
                    continue
        raise RuntimeError(f"request failed: {url}: {last_error}")


def paper_to_output(row: dict[str, str], paper: dict[str, Any], resolution: str, error: str = "") -> dict[str, str]:
    external = paper.get("externalIds") or {}
    authors = "; ".join(author.get("name", "") for author in paper.get("authors") or [] if author.get("name"))
    publication_types = "; ".join(paper.get("publicationTypes") or [])
    pdf = paper.get("openAccessPdf") or {}
    return {
        **row,
        "resolved_paperId": paper.get("paperId") or "",
        "resolved_title": paper.get("title") or "",
        "resolved_year": paper.get("year") or "",
        "citationCount": paper.get("citationCount") if paper.get("citationCount") is not None else "",
        "influentialCitationCount": paper.get("influentialCitationCount")
        if paper.get("influentialCitationCount") is not None
        else "",
        "venue": paper.get("venue") or "",
        "authors": authors,
        "doi": external.get("DOI") or "",
        "arxiv": external.get("ArXiv") or "",
        "semantic_scholar_url": paper.get("url") or "",
        "publicationDate": paper.get("publicationDate") or "",
        "publicationTypes": publication_types,
        "openAccessPdf": pdf.get("url") or "",
        "abstract": paper.get("abstract") or "",
        "resolution_method": resolution,
        "resolution_error": error,
    }


def resolve_by_title(client: SemanticScholarClient, title: str) -> tuple[dict[str, Any], str]:
    payload = client.get_json("/paper/search", {"query": title, "limit": 10, "fields": FIELDS})
    candidates = payload.get("data") or []
    if not candidates:
        raise RuntimeError("title search returned no candidates")
    target = normalize_title(title)
    for candidate in candidates:
        if normalize_title(candidate.get("title") or "") == target:
            return candidate, "title_exact"
    return candidates[0], "title_top_result"


def resolve_paper(client: SemanticScholarClient, row: dict[str, str]) -> tuple[dict[str, Any], str]:
    arxiv_id = parse_arxiv_id(row.get("source_url", ""))
    if arxiv_id:
        paper_key = urllib.parse.quote(f"arXiv:{arxiv_id}", safe=":")
        try:
            return client.get_json(f"/paper/{paper_key}", {"fields": FIELDS}), "arxiv"
        except RuntimeError:
            pass
    return resolve_by_title(client, row.get("title", ""))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--api-keys-file")
    parser.add_argument("--api-keys")
    parser.add_argument("--min-interval-seconds", type=float, default=1.0)
    args = parser.parse_args()

    keys = load_api_keys(args.api_keys_file, args.api_keys)
    client = SemanticScholarClient(keys, args.min_interval_seconds)

    with Path(args.input).open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    output_rows: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        try:
            paper, method = resolve_paper(client, row)
            output_rows.append(paper_to_output(row, paper, method))
            print(f"[{index}/{len(rows)}] ok {row.get('id')} {method}", flush=True)
        except Exception as exc:  # noqa: BLE001
            output_rows.append(paper_to_output(row, {}, "unresolved", str(exc)))
            print(f"[{index}/{len(rows)}] error {row.get('id')}: {exc}", flush=True)

    original_cols = list(rows[0].keys()) if rows else []
    added_cols = [
        "resolved_paperId",
        "resolved_title",
        "resolved_year",
        "citationCount",
        "influentialCitationCount",
        "venue",
        "authors",
        "doi",
        "arxiv",
        "semantic_scholar_url",
        "publicationDate",
        "publicationTypes",
        "openAccessPdf",
        "abstract",
        "resolution_method",
        "resolution_error",
    ]
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.output).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=original_cols + added_cols)
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"requests={client.request_count}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()

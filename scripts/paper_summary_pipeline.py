#!/usr/bin/env python3
"""Download, extract, and summarize papers with Frederick's Local LLM service.

The pipeline keeps copyrighted full text in data/paper_cache/, which is ignored
by git. Generated metadata and summaries live under data/processed/paper_summaries/.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "processed" / "thematic_papers.csv"
CACHE_DIR = ROOT / "data" / "paper_cache"
DOWNLOAD_DIR = CACHE_DIR / "downloads"
TEXT_DIR = CACHE_DIR / "text"
MANUAL_DIR = CACHE_DIR / "manual"
OUT_DIR = ROOT / "data" / "processed" / "paper_summaries"
DOWNLOAD_MANIFEST = OUT_DIR / "download_manifest.csv"
TEXT_MANIFEST = OUT_DIR / "text_manifest.csv"
SUMMARY_JSONL = OUT_DIR / "paper_summaries.jsonl"
SUMMARY_CSV = OUT_DIR / "paper_summaries.csv"
MANUAL_DOWNLOADS = OUT_DIR / "manual_downloads.csv"
REPORT_MD = ROOT / "docs" / "paper_summary_report.md"

LOCAL_LLM_BASE = os.environ.get("LOCAL_LLM_BASE", "")
LOCAL_LLM_TOKEN = os.environ.get("LOCAL_LLM_TOKEN", "")
DEFAULT_MODEL = "Qwen/Qwen3.6-35B-A3B"
DEFAULT_MAX_MODEL_CHARS = 50_000
USER_AGENT = "awesome-llm-for-strategies-paper-pipeline/0.1"


@dataclass(frozen=True)
class CandidateURL:
    url: str
    kind: str
    reason: str


class TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "nav", "footer", "header", "noscript"}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "nav", "footer", "header", "noscript"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        data = " ".join(data.split())
        if data:
            self.parts.append(data)

    def text(self) -> str:
        return clean_text(" ".join(self.parts))


def ensure_dirs() -> None:
    for path in [DOWNLOAD_DIR, TEXT_DIR, MANUAL_DIR, OUT_DIR, REPORT_MD.parent]:
        path.mkdir(parents=True, exist_ok=True)


def normalize(value: str) -> str:
    return " ".join((value or "").lower().split())


def slug_for(title: str) -> str:
    words = re.findall(r"[a-z0-9]+", normalize(title))
    stem = "-".join(words[:10]) or "paper"
    digest = hashlib.sha1(normalize(title).encode("utf-8")).hexdigest()[:10]
    return f"{stem[:80]}-{digest}"


def as_int(value: str, default: int = 0) -> int:
    try:
        if value in {"", "n/a", None}:  # type: ignore[comparison-overlap]
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def title_tokens(value: str) -> set[str]:
    stopwords = {"a", "an", "and", "as", "at", "for", "from", "in", "of", "on", "the", "to", "with"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", normalize(value))
        if len(token) > 1 and token not in stopwords
    }


def title_similarity(left: str, right: str) -> float:
    left_tokens = title_tokens(left)
    right_tokens = title_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def read_catalog(args: argparse.Namespace) -> list[dict[str, str]]:
    rows = list(csv.DictReader(CATALOG.open(newline="", encoding="utf-8")))
    if args.title_regex:
        rx = re.compile(args.title_regex, re.I)
        rows = [row for row in rows if rx.search(row["title"])]
    if args.only_core_important:
        rows = [row for row in rows if row.get("importance") in {"Core", "Important"}]
    if args.include_watchlist is False:
        rows = [row for row in rows if row.get("importance") != "Watchlist"]
    if args.limit:
        rows = rows[: args.limit]
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: (value.rstrip() if isinstance(value, str) else value) for key, value in row.items()})


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def manifest_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_csv_by_slug(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    return {row["slug"]: row for row in csv.DictReader(path.open(newline="", encoding="utf-8"))}


def read_api_key() -> str:
    if os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        return os.environ["SEMANTIC_SCHOLAR_API_KEY"]
    key_file = ROOT / "semantic_scholar_api_keys.json"
    if not key_file.exists():
        return ""
    try:
        data = json.loads(key_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    if isinstance(data, dict):
        for key in ["SEMANTIC_SCHOLAR_API_KEY", "semantic_scholar_api_key", "api_key", "key"]:
            if data.get(key):
                return str(data[key])
        for value in data.values():
            if isinstance(value, str) and value.strip():
                return value.strip()
    return ""


def arxiv_pdf_url(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    match = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", value)
    return f"https://arxiv.org/pdf/{match.group(1)}.pdf" if match else ""


def semantic_scholar_id(url: str) -> str:
    match = re.search(r"semanticscholar\.org/paper/(?:[^/]+/)?([0-9a-f]{40})", url or "", re.I)
    return match.group(1) if match else ""


def fetch_json(url: str, api_key: str = "", timeout: int = 45) -> dict[str, Any]:
    headers = {"User-Agent": USER_AGENT}
    if api_key:
        headers["x-api-key"] = api_key
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def fetch_text(url: str, timeout: int = 45) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace"), response.geturl()


def semantic_scholar_candidates(row: dict[str, str], api_key: str, timeout: int) -> list[CandidateURL]:
    paper_id = semantic_scholar_id(row.get("url", ""))
    if not paper_id:
        return []
    fields = "openAccessPdf,externalIds,url,title"
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields={urllib.parse.quote(fields)}"
    try:
        data = fetch_json(url, api_key=api_key, timeout=timeout)
    except Exception as exc:
        return [CandidateURL("", "error", f"semantic_scholar_lookup_failed: {exc}")]
    candidates: list[CandidateURL] = []
    oa = data.get("openAccessPdf") or {}
    if isinstance(oa, dict) and oa.get("url"):
        candidates.append(CandidateURL(str(oa["url"]), "pdf", "semantic_scholar_open_access_pdf"))
    external = data.get("externalIds") or {}
    if isinstance(external, dict):
        if external.get("ArXiv"):
            candidates.append(CandidateURL(arxiv_pdf_url(str(external["ArXiv"])), "pdf", "semantic_scholar_arxiv"))
        if external.get("DOI"):
            doi_pdf = doi_to_arxiv_pdf(str(external["DOI"]))
            if doi_pdf:
                candidates.append(CandidateURL(doi_pdf, "pdf", "semantic_scholar_doi_arxiv"))
    return [candidate for candidate in candidates if candidate.url]


def doi_to_arxiv_pdf(doi: str) -> str:
    if not doi:
        return ""
    if "10.48550/arxiv." in doi.lower():
        return arxiv_pdf_url(doi)
    return ""


def direct_url_candidates(row: dict[str, str]) -> list[CandidateURL]:
    candidates: list[CandidateURL] = []
    url = (row.get("url") or "").strip()
    arxiv = arxiv_pdf_url(row.get("arxiv", "")) or doi_to_arxiv_pdf(row.get("doi", ""))
    if arxiv:
        candidates.append(CandidateURL(arxiv, "pdf", "arxiv"))
    if url:
        lower = url.lower()
        if lower.endswith(".pdf"):
            candidates.append(CandidateURL(url, "pdf", "direct_pdf"))
        if "arxiv.org/abs/" in lower or "arxiv.org/html/" in lower or "arxiv.org/pdf/" in lower:
            pdf = arxiv_pdf_url(url)
            if pdf:
                candidates.append(CandidateURL(pdf, "pdf", "arxiv_url"))
        if "aclanthology.org/" in lower:
            if lower.endswith("/"):
                candidates.append(CandidateURL(url.rstrip("/") + ".pdf", "pdf", "acl_anthology_pdf"))
            elif not lower.endswith(".pdf"):
                candidates.append(CandidateURL(url + ".pdf", "pdf", "acl_anthology_pdf"))
        if lower.endswith(".html") or any(domain in lower for domain in ["nature.com/", "cambridge.org/", "nber.org/", "frontiersin.org/"]):
            candidates.append(CandidateURL(url, "html", "publisher_html"))
        if lower.startswith("http") and "semanticscholar.org" not in lower:
            candidates.append(CandidateURL(url, "html", "source_landing_page"))
    seen: set[str] = set()
    deduped: list[CandidateURL] = []
    for candidate in candidates:
        if candidate.url and candidate.url not in seen:
            deduped.append(candidate)
            seen.add(candidate.url)
    return deduped


def doi_candidate_urls(doi: str) -> list[CandidateURL]:
    doi = (doi or "").strip()
    if not doi:
        return []
    lowered = doi.lower()
    candidates: list[CandidateURL] = []
    arxiv = doi_to_arxiv_pdf(doi)
    if arxiv:
        candidates.append(CandidateURL(arxiv, "pdf", "doi_arxiv"))
    if lowered.startswith("10.18653/v1/"):
        acl_id = doi.split("/", 1)[1].removeprefix("v1/")
        candidates.append(CandidateURL(f"https://aclanthology.org/{acl_id}.pdf", "pdf", "doi_acl_anthology"))
    if lowered.startswith("10.1073/"):
        candidates.append(CandidateURL(f"https://www.pnas.org/doi/pdf/{doi}", "pdf", "doi_pnas_pdf"))
    if lowered.startswith("10.1038/"):
        suffix = doi.split("/", 1)[1]
        candidates.append(CandidateURL(f"https://www.nature.com/articles/{suffix}.pdf", "pdf", "doi_nature_pdf"))
    if lowered.startswith("10.1371/"):
        candidates.append(CandidateURL(f"https://journals.plos.org/plosone/article/file?id={doi}&type=printable", "pdf", "doi_plos_pdf"))
    candidates.append(CandidateURL(f"https://doi.org/{doi}", "html", "doi_landing_page"))
    return candidates


def recover_candidates(row: dict[str, str], args: argparse.Namespace, api_key: str) -> list[CandidateURL]:
    candidates: list[CandidateURL] = []
    candidates.extend(direct_url_candidates(row))

    doi_candidates = doi_candidate_urls(row.get("doi", ""))
    candidates.extend([candidate for candidate in doi_candidates if candidate.reason != "doi_landing_page"])

    openalex = openalex_candidates(row, args.timeout)
    candidates.extend(openalex)
    if openalex:
        time.sleep(args.openalex_delay)

    landing = doi_landing_candidates(row, args.timeout)
    candidates.extend(landing)
    if landing:
        time.sleep(args.doi_delay)

    arxiv = arxiv_title_candidates(row, args.timeout)
    candidates.extend(arxiv)
    if arxiv:
        time.sleep(args.arxiv_delay)

    if args.semantic_scholar_lookup and api_key:
        semantic = semantic_scholar_candidates(row, api_key, args.timeout)
        candidates.extend(semantic)
        time.sleep(args.semantic_scholar_delay)

    candidates.extend([candidate for candidate in doi_candidates if candidate.reason == "doi_landing_page"])
    return dedupe_candidates(candidates)


def extract_meta_urls(html_text: str, final_url: str) -> list[CandidateURL]:
    candidates: list[CandidateURL] = []
    patterns = [
        r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url["\']',
        r'<meta[^>]+name=["\']citation_fulltext_html_url["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_fulltext_html_url["\']',
    ]
    for pattern in patterns:
        for match in re.findall(pattern, html_text, flags=re.I):
            url = html.unescape(match)
            if url.startswith("//"):
                parsed = urllib.parse.urlparse(final_url)
                url = f"{parsed.scheme}:{url}"
            if url.startswith("/"):
                url = urllib.parse.urljoin(final_url, url)
            kind = "pdf" if ".pdf" in url.lower() or "type=printable" in url.lower() else "html"
            candidates.append(CandidateURL(url, kind, "doi_landing_meta"))
    return dedupe_candidates(candidates)


def doi_landing_candidates(row: dict[str, str], timeout: int) -> list[CandidateURL]:
    doi = (row.get("doi") or "").strip()
    if not doi:
        return []
    try:
        text, final_url = fetch_text(f"https://doi.org/{doi}", timeout=timeout)
    except Exception:
        return []
    return extract_meta_urls(text[:2_000_000], final_url)


def openalex_candidates(row: dict[str, str], timeout: int) -> list[CandidateURL]:
    urls: list[str] = []
    doi = (row.get("doi") or "").strip()
    if doi:
        urls.append(f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(doi, safe='')}")
    title = (row.get("title") or "").strip()
    if title:
        urls.append(f"https://api.openalex.org/works?search={urllib.parse.quote(title)}&per-page=5")
    candidates: list[CandidateURL] = []
    for url in urls:
        try:
            data = fetch_json(url, timeout=timeout)
        except Exception:
            continue
        works = data.get("results", data if isinstance(data, dict) else [])
        if isinstance(works, dict):
            works = [works]
        if not isinstance(works, list):
            continue
        for work in works:
            if not isinstance(work, dict):
                continue
            work_title = str(work.get("title") or "")
            if title and work_title and title_similarity(title, work_title) < 0.55:
                continue
            for location_key in ["primary_location", "best_oa_location"]:
                location = work.get(location_key) or {}
                if isinstance(location, dict):
                    candidates.extend(openalex_location_candidates(location))
            for location in work.get("locations") or []:
                if isinstance(location, dict):
                    candidates.extend(openalex_location_candidates(location))
    return dedupe_candidates(candidates)


def openalex_location_candidates(location: dict[str, Any]) -> list[CandidateURL]:
    candidates: list[CandidateURL] = []
    pdf_url = location.get("pdf_url")
    landing = location.get("landing_page_url")
    if pdf_url:
        candidates.append(CandidateURL(str(pdf_url), "pdf", "openalex_pdf_url"))
    if landing:
        candidates.append(CandidateURL(str(landing), "html", "openalex_landing_page"))
    return candidates


def arxiv_title_candidates(row: dict[str, str], timeout: int) -> list[CandidateURL]:
    title = (row.get("title") or "").strip()
    if not title:
        return []
    query = urllib.parse.quote(f'ti:"{title}"')
    url = f"https://export.arxiv.org/api/query?search_query={query}&start=0&max_results=5"
    try:
        xml_text, _ = fetch_text(url, timeout=timeout)
    except Exception:
        return []
    candidates: list[CandidateURL] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", ns):
        entry_title = clean_text(" ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split()))
        if title_similarity(title, entry_title) < 0.62:
            continue
        arxiv_id = entry.findtext("atom:id", default="", namespaces=ns) or ""
        pdf = arxiv_pdf_url(arxiv_id)
        if pdf:
            candidates.append(CandidateURL(pdf, "pdf", "arxiv_title_search"))
    return dedupe_candidates(candidates)


def dedupe_candidates(candidates: list[CandidateURL]) -> list[CandidateURL]:
    seen: set[str] = set()
    deduped: list[CandidateURL] = []
    for candidate in candidates:
        if candidate.url and candidate.url not in seen:
            deduped.append(candidate)
            seen.add(candidate.url)
    return deduped


def manual_file_for(slug: str) -> Path | None:
    for suffix in [".pdf", ".txt", ".html", ".htm"]:
        path = MANUAL_DIR / f"{slug}{suffix}"
        if path.exists():
            return path
    matches = sorted(MANUAL_DIR.glob(f"{slug}.*"))
    return matches[0] if matches else None


def content_ext(content_type: str, data: bytes, fallback_kind: str) -> str:
    lowered = (content_type or "").lower()
    head = data[:256].lstrip()
    if head.startswith(b"%PDF") or "application/pdf" in lowered:
        return ".pdf"
    if b"<html" in head.lower() or "text/html" in lowered:
        return ".html"
    if fallback_kind == "html":
        return ".html"
    return ".bin"


def download_url(candidate: CandidateURL, dest_base: Path, timeout: int) -> tuple[str, Path, str, int, str]:
    request = urllib.request.Request(
        candidate.url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/pdf,text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
        content_type = response.headers.get("content-type", "")
        final_url = response.geturl()
    ext = content_ext(content_type, data, candidate.kind)
    if ext == ".bin" or len(data) < 500:
        raise RuntimeError(f"unexpected content type={content_type!r}, bytes={len(data)}")
    path = dest_base.with_suffix(ext)
    path.write_bytes(data)
    return final_url, path, content_type, len(data), ext


def command_download(args: argparse.Namespace) -> None:
    ensure_dirs()
    rows = read_catalog(args)
    existing = load_csv_by_slug(DOWNLOAD_MANIFEST)
    api_key = read_api_key()
    manifest: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        slug = slug_for(row["title"])
        if args.resume and slug in existing and existing[slug].get("status") in {"downloaded", "manual"}:
            manifest.append(existing[slug])
            continue
        manual = manual_file_for(slug)
        if manual:
            manifest.append(
                download_manifest_row(
                    row,
                    slug,
                    "manual",
                    "",
                    repo_relative(manual),
                    manual.suffix,
                    manual.stat().st_size,
                    "",
                    "",
                )
            )
            print(f"[{index}/{len(rows)}] manual {row['title']}", flush=True)
            continue
        error_messages: list[str] = []
        downloaded = try_candidates(row, slug, direct_url_candidates(row), args, manifest, error_messages, index, len(rows))
        if not downloaded and args.semantic_scholar_lookup:
            candidates = semantic_scholar_candidates(row, api_key, args.timeout)
            time.sleep(args.semantic_scholar_delay)
            downloaded = try_candidates(row, slug, candidates, args, manifest, error_messages, index, len(rows))
        if not downloaded:
            hint = repo_relative(MANUAL_DIR / f"{slug}.pdf")
            manifest.append(download_manifest_row(row, slug, "manual_needed", "", "", "", 0, "", " | ".join(error_messages)[:1500], hint))
            print(f"[{index}/{len(rows)}] manual_needed {row['title']}", flush=True)
    if args.resume:
        for slug, row in existing.items():
            if slug not in {item["slug"] for item in manifest}:
                manifest.append(row)
    columns = [
        "slug",
        "title",
        "year",
        "importance",
        "theme",
        "subtheme",
        "citationCount",
        "status",
        "download_url",
        "file_path",
        "file_type",
        "bytes",
        "download_reason",
        "error",
        "manual_path_hint",
        "source_url",
        "doi",
        "arxiv",
    ]
    write_csv(DOWNLOAD_MANIFEST, sorted(manifest, key=lambda item: item["title"].lower()), columns)
    write_manual_downloads()


def try_candidates(
    row: dict[str, str],
    slug: str,
    candidates: list[CandidateURL],
    args: argparse.Namespace,
    manifest: list[dict[str, Any]],
    error_messages: list[str],
    index: int,
    total: int,
) -> bool:
    for candidate in candidates:
            if not candidate.url:
                if candidate.reason:
                    error_messages.append(candidate.reason)
                continue
            try:
                final_url, path, content_type, size, ext = download_url(candidate, DOWNLOAD_DIR / slug, args.timeout)
            except Exception as exc:
                error_messages.append(f"{candidate.reason}: {exc}")
                continue
            manifest.append(
                download_manifest_row(
                    row,
                    slug,
                    "downloaded",
                    final_url,
                    repo_relative(path),
                    ext.lstrip("."),
                    size,
                    candidate.reason,
                    "",
                )
            )
            print(f"[{index}/{total}] downloaded {row['title']} via {candidate.reason}", flush=True)
            return True
    return False


def download_manifest_row(
    row: dict[str, str],
    slug: str,
    status: str,
    download_url_value: str,
    file_path: str,
    file_type: str,
    size: int,
    reason: str,
    error: str,
    manual_path_hint: str = "",
) -> dict[str, Any]:
    return {
        "slug": slug,
        "title": row.get("title", ""),
        "year": row.get("year", ""),
        "importance": row.get("importance", ""),
        "theme": row.get("theme", ""),
        "subtheme": row.get("subtheme", ""),
        "citationCount": row.get("citationCount", ""),
        "status": status,
        "download_url": download_url_value,
        "file_path": file_path,
        "file_type": file_type,
        "bytes": size,
        "download_reason": reason,
        "error": error,
        "manual_path_hint": manual_path_hint,
        "source_url": row.get("url", ""),
        "doi": row.get("doi", ""),
        "arxiv": row.get("arxiv", ""),
    }


def write_manual_downloads() -> None:
    rows = [
        row
        for row in csv.DictReader(DOWNLOAD_MANIFEST.open(newline="", encoding="utf-8"))
        if row.get("status") == "manual_needed"
    ]
    columns = [
        "title",
        "year",
        "importance",
        "theme",
        "subtheme",
        "source_url",
        "doi",
        "arxiv",
        "manual_path_hint",
        "error",
    ]
    write_csv(MANUAL_DOWNLOADS, rows, columns)


def command_recover_manual(args: argparse.Namespace) -> None:
    ensure_dirs()
    existing_rows = load_csv_by_slug(DOWNLOAD_MANIFEST)
    catalog_by_slug = {slug_for(row["title"]): row for row in read_catalog(argparse.Namespace(**{**vars(args), "limit": None}))}
    selected_slugs = {slug_for(row["title"]) for row in read_catalog(args)}
    api_key = read_api_key()

    manual_slugs = [
        slug
        for slug, row in sorted(existing_rows.items(), key=lambda item: item[1].get("title", "").lower())
        if row.get("status") == "manual_needed" and (not selected_slugs or slug in selected_slugs)
    ]
    total = len(manual_slugs)
    recovered = 0
    output_rows = dict(existing_rows)

    for index, slug in enumerate(manual_slugs, start=1):
        manifest_row = existing_rows[slug]
        catalog_row = catalog_by_slug.get(slug, {})
        row = {**catalog_row, **manifest_row}
        if not row.get("url"):
            row["url"] = row.get("source_url", "")

        manual = manual_file_for(slug)
        if manual:
            output_rows[slug] = download_manifest_row(
                row,
                slug,
                "manual",
                "",
                repo_relative(manual),
                manual.suffix.lstrip("."),
                manual.stat().st_size,
                "local_manual_file",
                "",
            )
            recovered += 1
            print(f"[{index}/{total}] recovered local_manual {row.get('title', slug)}", flush=True)
            continue

        candidates = recover_candidates(row, args, api_key)
        errors: list[str] = []
        downloaded = False
        for candidate in candidates:
            if not candidate.url:
                if candidate.reason:
                    errors.append(candidate.reason)
                continue
            try:
                final_url, path, _content_type, size, ext = download_url(candidate, DOWNLOAD_DIR / slug, args.timeout)
            except Exception as exc:
                errors.append(f"{candidate.reason}: {exc}")
                continue
            output_rows[slug] = download_manifest_row(
                row,
                slug,
                "downloaded",
                final_url,
                repo_relative(path),
                ext.lstrip("."),
                size,
                f"recover_manual:{candidate.reason}",
                "",
            )
            recovered += 1
            downloaded = True
            print(f"[{index}/{total}] recovered {row.get('title', slug)} via {candidate.reason}", flush=True)
            break

        if not downloaded:
            error = " | ".join(errors)[:1500] if errors else "recover_manual: no candidates found"
            output_rows[slug] = {**manifest_row, "error": error}
            print(f"[{index}/{total}] still_manual_needed {row.get('title', slug)}", flush=True)

    columns = [
        "slug",
        "title",
        "year",
        "importance",
        "theme",
        "subtheme",
        "citationCount",
        "status",
        "download_url",
        "file_path",
        "file_type",
        "bytes",
        "download_reason",
        "error",
        "manual_path_hint",
        "source_url",
        "doi",
        "arxiv",
    ]
    write_csv(DOWNLOAD_MANIFEST, sorted(output_rows.values(), key=lambda item: item["title"].lower()), columns)
    write_manual_downloads()
    print(f"Recovered {recovered}/{total} manual-needed papers.", flush=True)


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = value.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
    value = value.replace("\x00", " ")
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def extract_pdf_with_pypdf(path: Path, max_chars: int) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except Exception as exc:
            raise RuntimeError("Install pypdf or provide manual .txt files") from exc
    reader = PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            continue
        if sum(len(part) for part in parts) >= max_chars:
            break
    return clean_text("\n\n".join(parts))[:max_chars]


def extract_pdf_with_cli(path: Path, max_chars: int) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext not found")
    result = subprocess.run(
        [pdftotext, "-layout", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    return clean_text(result.stdout)[:max_chars]


def extract_text_from_file(path: Path, max_chars: int) -> tuple[str, str, str]:
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return clean_text(path.read_text(encoding="utf-8", errors="replace"))[:max_chars], "manual_txt", ""
    if suffix in {".html", ".htm"}:
        parser = TextHTMLParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        return parser.text()[:max_chars], "html", ""
    if suffix == ".pdf":
        try:
            return extract_pdf_with_pypdf(path, max_chars), "pdf_pypdf", ""
        except Exception as first_exc:
            try:
                return extract_pdf_with_cli(path, max_chars), "pdf_pdftotext", ""
            except Exception as second_exc:
                return "", "pdf_failed", f"{first_exc}; {second_exc}"
    return "", "unsupported", f"unsupported file suffix {suffix}"


def command_extract(args: argparse.Namespace) -> None:
    ensure_dirs()
    catalog_by_slug = {slug_for(row["title"]): row for row in read_catalog(argparse.Namespace(**{**vars(args), "limit": None}))}
    download_rows = load_csv_by_slug(DOWNLOAD_MANIFEST)
    existing = load_csv_by_slug(TEXT_MANIFEST)
    selected = read_catalog(args)
    selected_slugs = {slug_for(row["title"]) for row in selected}
    output_rows: list[dict[str, Any]] = []
    for slug in selected_slugs:
        row = download_rows.get(slug)
        catalog = catalog_by_slug.get(slug, {})
        existing_row = existing.get(slug, {})
        existing_text_path = existing_row.get("text_path", "")
        existing_text_ready = bool(existing_text_path) and manifest_path(existing_text_path).exists() and as_int(existing_row.get("text_chars", "")) >= 100
        if args.resume and slug in existing and existing[slug].get("status") in {"extracted", "abstract_only"} and existing_text_ready:
            output_rows.append(existing[slug])
            continue
        if not row or row.get("status") not in {"downloaded", "manual"}:
            abstract = clean_text(catalog.get("abstract", ""))
            if abstract:
                text_path = TEXT_DIR / f"{slug}.txt"
                text_path.write_text(abstract, encoding="utf-8")
                output_rows.append(
                    text_manifest_row(
                        catalog,
                        slug,
                        "abstract_only",
                        repo_relative(text_path),
                        "abstract_missing_download",
                        len(abstract),
                        False,
                        "download_missing; abstract fallback",
                    )
                )
            else:
                output_rows.append(text_manifest_row(catalog, slug, "missing_download", "", "", 0, False, "download_missing"))
            continue
        path = manifest_path(row["file_path"])
        text, source, error = extract_text_from_file(path, args.extract_chars)
        status = "extracted" if len(text) >= args.min_text_chars else "abstract_only"
        if status == "abstract_only":
            abstract = catalog.get("abstract", "")
            if abstract:
                text = clean_text(abstract)
                source = "abstract"
                error = error or "downloaded file had too little extractable text"
            else:
                status = "missing_text"
                text = ""
                error = error or "no extractable text and no abstract"
        text_path = TEXT_DIR / f"{slug}.txt"
        if text:
            text_path.write_text(text, encoding="utf-8")
        output_rows.append(
            text_manifest_row(
                catalog,
                slug,
                status,
                repo_relative(text_path) if text else "",
                source,
                len(text),
                len(text) >= args.max_model_chars,
                error,
            )
        )
        print(f"{status:<14} {len(text):>7} chars | {catalog.get('title', slug)}")
    if args.resume:
        for slug, row in existing.items():
            if slug not in {item["slug"] for item in output_rows}:
                output_rows.append(row)
    columns = [
        "slug",
        "title",
        "year",
        "importance",
        "theme",
        "subtheme",
        "citationCount",
        "status",
        "text_path",
        "text_source",
        "text_chars",
        "truncated_for_model",
        "error",
    ]
    write_csv(TEXT_MANIFEST, sorted(output_rows, key=lambda item: item["title"].lower()), columns)


def text_manifest_row(
    row: dict[str, str],
    slug: str,
    status: str,
    text_path: str,
    text_source: str,
    text_chars: int,
    truncated: bool,
    error: str,
) -> dict[str, Any]:
    return {
        "slug": slug,
        "title": row.get("title", ""),
        "year": row.get("year", ""),
        "importance": row.get("importance", ""),
        "theme": row.get("theme", ""),
        "subtheme": row.get("subtheme", ""),
        "citationCount": row.get("citationCount", ""),
        "status": status,
        "text_path": text_path,
        "text_source": text_source,
        "text_chars": text_chars,
        "truncated_for_model": str(bool(truncated)),
        "error": error,
    }


def local_llm_chat(messages: list[dict[str, str]], model: str, max_tokens: int, timeout: int) -> str:
    if not LOCAL_LLM_BASE:
        raise RuntimeError("Set LOCAL_LLM_BASE before calling the Local LLM service.")
    if not LOCAL_LLM_TOKEN:
        raise RuntimeError("Set LOCAL_LLM_TOKEN before calling the Local LLM service.")
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0,
        "max_tokens": max_tokens,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{LOCAL_LLM_BASE.rstrip('/')}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {LOCAL_LLM_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8", errors="replace"))
    return body["choices"][0]["message"]["content"]


def check_model(args: argparse.Namespace) -> None:
    if not LOCAL_LLM_BASE:
        raise RuntimeError("Set LOCAL_LLM_BASE before calling the Local LLM service.")
    if not LOCAL_LLM_TOKEN:
        raise RuntimeError("Set LOCAL_LLM_TOKEN before calling the Local LLM service.")
    request = urllib.request.Request(
        f"{LOCAL_LLM_BASE.rstrip('/')}/models",
        headers={"Authorization": f"Bearer {LOCAL_LLM_TOKEN}", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=args.timeout) as response:
        data = json.loads(response.read().decode("utf-8", errors="replace"))
    model_ids = [item.get("id", "") for item in data.get("data", [])]
    print("\n".join(model_ids))
    if args.model not in model_ids:
        raise SystemExit(f"model not found: {args.model}")


def build_prompt(row: dict[str, str], text: str, max_model_chars: int) -> list[dict[str, str]]:
    excerpt = text[:max_model_chars]
    metadata = {
        "title": row.get("title", ""),
        "year": row.get("year", ""),
        "importance": row.get("importance", ""),
        "theme": row.get("theme", ""),
        "subtheme": row.get("subtheme", ""),
        "citationCount": row.get("citationCount", ""),
        "url": row.get("url", ""),
        "doi": row.get("doi", ""),
        "venue": row.get("venue", ""),
        "authors": row.get("authors", ""),
        "abstract": row.get("abstract", ""),
    }
    system = (
        "你是一个严谨的政治科学、地缘政治、政策制定与战略研究文献助理。"
        "只输出合法 JSON，不要 Markdown，不要解释你的步骤。"
        "不要长篇引用原文；如果正文来自付费墙或手动文件，只做短摘录式概括。"
    )
    user = f"""
请根据 metadata、abstract 和 paper_text_excerpt 生成一份短报告。报告面向人工筛读，不要过长。

要求：
1. 摘录核心内容，包括：(a) 重要摘要与结果，(b) Deliverables，(c) Method，(d) Paywall/manual/full-text 内能看到的实质内容。
2. 如果只有 abstract 或摘录不足，请明确写出 limitation。
3. 给 10 到 20 个 tags，tags 用英文小写短语，便于后续检索。
4. 判断它对本 repo 主题 Large Language Models for Political Science & Political Strategies 的相关性。
5. 输出 JSON，schema 固定如下：
{{
  "title": "...",
  "year": "...",
  "summary_zh": "...不超过 180 个中文字...",
  "important_results": ["...", "...", "..."],
  "deliverables": ["...", "..."],
  "method": ["...", "..."],
  "paywall_or_fulltext_notes": "...",
  "repo_relevance": "core|important|peripheral|watchlist",
  "tags": ["tag1", "tag2"],
  "confidence": "high|medium|low"
}}

metadata:
{json.dumps(metadata, ensure_ascii=False, indent=2)}

paper_text_excerpt:
<<<BEGIN_EXCERPT
{excerpt}
END_EXCERPT>>>
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user.strip()}]


def parse_json_response(raw: str) -> tuple[dict[str, Any], str]:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        cleaned = cleaned[start : end + 1]
    try:
        return json.loads(cleaned), ""
    except json.JSONDecodeError as exc:
        return {"raw_response": raw}, str(exc)


def load_jsonl_by_slug(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    rows: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if item.get("slug"):
            rows[item["slug"]] = item
    return rows


def successful_summary(item: dict[str, Any]) -> bool:
    return bool(item.get("summary")) and not item.get("error") and not item.get("parse_error")


def append_jsonl(path: Path, item: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def command_summarize(args: argparse.Namespace) -> None:
    ensure_dirs()
    catalog = {slug_for(row["title"]): row for row in read_catalog(argparse.Namespace(**{**vars(args), "limit": None}))}
    text_rows = load_csv_by_slug(TEXT_MANIFEST)
    completed = load_jsonl_by_slug(SUMMARY_JSONL) if args.resume else {}
    selected = read_catalog(args)
    for index, row in enumerate(selected, start=1):
        slug = slug_for(row["title"])
        if slug in completed and successful_summary(completed[slug]):
            print(f"[{index}/{len(selected)}] skip {row['title']}", flush=True)
            continue
        text_row = text_rows.get(slug)
        if not text_row or text_row.get("status") not in {"extracted", "abstract_only"} or not text_row.get("text_path"):
            print(f"[{index}/{len(selected)}] missing_text {row['title']}", flush=True)
            continue
        text_path = manifest_path(text_row["text_path"])
        if not text_path.exists():
            print(f"[{index}/{len(selected)}] missing_text_file {row['title']}", flush=True)
            continue
        text = text_path.read_text(encoding="utf-8", errors="replace")
        merged_row = {**catalog.get(slug, {}), **row}
        messages = build_prompt(merged_row, text, args.max_model_chars)
        for attempt in range(1, args.retries + 1):
            try:
                raw = local_llm_chat(messages, args.model, args.max_tokens, args.timeout)
                parsed, parse_error = parse_json_response(raw)
                item = {
                    "slug": slug,
                    "title": row["title"],
                    "year": row.get("year", ""),
                    "importance": row.get("importance", ""),
                    "theme": row.get("theme", ""),
                    "subtheme": row.get("subtheme", ""),
                    "citationCount": row.get("citationCount", ""),
                    "text_source": text_row.get("text_source", ""),
                    "text_chars": text_row.get("text_chars", ""),
                    "model": args.model,
                    "max_model_chars": args.max_model_chars,
                    "summary": parsed,
                    "parse_error": parse_error,
                }
                append_jsonl(SUMMARY_JSONL, item)
                print(f"[{index}/{len(selected)}] summarized {row['title']}", flush=True)
                break
            except Exception as exc:
                if attempt == args.retries:
                    append_jsonl(
                        SUMMARY_JSONL,
                        {
                            "slug": slug,
                            "title": row["title"],
                            "year": row.get("year", ""),
                            "importance": row.get("importance", ""),
                            "theme": row.get("theme", ""),
                            "subtheme": row.get("subtheme", ""),
                            "citationCount": row.get("citationCount", ""),
                            "text_source": text_row.get("text_source", ""),
                            "model": args.model,
                            "summary": {},
                            "error": str(exc),
                        },
                    )
                    print(f"[{index}/{len(selected)}] failed {row['title']}: {exc}", flush=True)
                else:
                    time.sleep(args.retry_sleep * attempt)
    write_summary_csv()


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str) and value:
        return [value]
    return []


def write_summary_csv() -> None:
    items = list(load_jsonl_by_slug(SUMMARY_JSONL).values())
    text_rows = load_csv_by_slug(TEXT_MANIFEST)
    rows: list[dict[str, str]] = []
    for item in sorted(items, key=lambda row: (row.get("theme", ""), row.get("title", ""))):
        text_row = text_rows.get(item.get("slug", ""))
        if not text_row or text_row.get("status") not in {"extracted", "abstract_only"} or not text_row.get("text_path"):
            continue
        summary = item.get("summary") or {}
        rows.append(
            {
                "title": item.get("title", ""),
                "year": item.get("year", ""),
                "importance": item.get("importance", ""),
                "theme": item.get("theme", ""),
                "subtheme": item.get("subtheme", ""),
                "citationCount": item.get("citationCount", ""),
                "summary_zh": str(summary.get("summary_zh", "")),
                "important_results": " | ".join(as_list(summary.get("important_results"))),
                "deliverables": " | ".join(as_list(summary.get("deliverables"))),
                "method": " | ".join(as_list(summary.get("method"))),
                "paywall_or_fulltext_notes": str(summary.get("paywall_or_fulltext_notes", "")),
                "repo_relevance": str(summary.get("repo_relevance", "")),
                "tags": "; ".join(as_list(summary.get("tags"))),
                "confidence": str(summary.get("confidence", "")),
                "text_source": item.get("text_source", ""),
                "model": item.get("model", ""),
                "error": item.get("error", "") or item.get("parse_error", ""),
            }
        )
    columns = [
        "title",
        "year",
        "importance",
        "theme",
        "subtheme",
        "citationCount",
        "summary_zh",
        "important_results",
        "deliverables",
        "method",
        "paywall_or_fulltext_notes",
        "repo_relevance",
        "tags",
        "confidence",
        "text_source",
        "model",
        "error",
    ]
    write_csv(SUMMARY_CSV, rows, columns)


def command_report(args: argparse.Namespace) -> None:
    write_summary_csv()
    rows = list(csv.DictReader(SUMMARY_CSV.open(newline="", encoding="utf-8"))) if SUMMARY_CSV.exists() else []
    if args.only_core_important:
        rows = [row for row in rows if row.get("importance") in {"Core", "Important"}]
    if args.limit:
        rows = rows[: args.limit]
    by_theme: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_theme.setdefault(row.get("theme", "Other"), []).append(row)
    lines = [
        "# Paper Summary Report",
        "",
        f"Generated from `{SUMMARY_JSONL.relative_to(ROOT)}`.",
        f"Summaries included: **{len(rows)}**.",
        "",
        "Each entry is intentionally compact; full-text caches remain local under `data/paper_cache/` and are not committed.",
        "",
    ]
    for theme, items in by_theme.items():
        lines.extend([f"## {theme}", ""])
        for row in sorted(items, key=lambda item: (item.get("importance", ""), item.get("title", ""))):
            tags = row.get("tags", "")
            lines.append(f"### {row.get('title', '')} ({row.get('year', '')}; {row.get('importance', '')}; citations: {row.get('citationCount', '')})")
            if tags:
                lines.append(f"Tags: {tags}")
            if row.get("summary_zh"):
                lines.append(row["summary_zh"])
            if row.get("deliverables"):
                lines.append(f"Deliverables: {row['deliverables']}")
            if row.get("method"):
                lines.append(f"Method: {row['method']}")
            if row.get("paywall_or_fulltext_notes"):
                lines.append(f"Full-text notes: {row['paywall_or_fulltext_notes']}")
            if row.get("error"):
                lines.append(f"Pipeline note: {row['error']}")
            lines.append("")
    REPORT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(REPORT_MD)


def command_run_all(args: argparse.Namespace) -> None:
    command_download(args)
    command_recover_manual(args)
    command_extract(args)
    command_summarize(args)
    command_report(args)


def add_common_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--title-regex", default="")
    parser.add_argument("--only-core-important", action="store_true")
    parser.add_argument("--include-watchlist", action=argparse.BooleanOptionalAction, default=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check-model", help="Verify Local LLM aggregate exposes the requested model")
    check.add_argument("--model", default=DEFAULT_MODEL)
    check.add_argument("--timeout", type=int, default=30)
    check.set_defaults(func=check_model)

    download = subparsers.add_parser("download", help="Download PDFs/HTML or write manual download queue")
    add_common_filters(download)
    download.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    download.add_argument("--timeout", type=int, default=60)
    download.add_argument("--semantic-scholar-lookup", action=argparse.BooleanOptionalAction, default=True)
    download.add_argument("--semantic-scholar-delay", type=float, default=1.0)
    download.set_defaults(func=command_download)

    recover = subparsers.add_parser("recover-manual", help="Search again for manual-needed PDFs/HTML and update the download manifest")
    add_common_filters(recover)
    recover.add_argument("--timeout", type=int, default=45)
    recover.add_argument("--openalex-delay", type=float, default=0.2)
    recover.add_argument("--doi-delay", type=float, default=0.2)
    recover.add_argument("--arxiv-delay", type=float, default=1.0)
    recover.add_argument("--semantic-scholar-lookup", action=argparse.BooleanOptionalAction, default=True)
    recover.add_argument("--semantic-scholar-delay", type=float, default=1.0)
    recover.set_defaults(func=command_recover_manual)

    extract = subparsers.add_parser("extract", help="Extract local full text for model input")
    add_common_filters(extract)
    extract.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    extract.add_argument("--extract-chars", type=int, default=120_000)
    extract.add_argument("--max-model-chars", type=int, default=DEFAULT_MAX_MODEL_CHARS)
    extract.add_argument("--min-text-chars", type=int, default=800)
    extract.set_defaults(func=command_extract)

    summarize = subparsers.add_parser("summarize", help="Summarize extracted text with Local LLM")
    add_common_filters(summarize)
    summarize.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    summarize.add_argument("--model", default=DEFAULT_MODEL)
    summarize.add_argument("--max-model-chars", type=int, default=DEFAULT_MAX_MODEL_CHARS)
    summarize.add_argument("--max-tokens", type=int, default=1400)
    summarize.add_argument("--timeout", type=int, default=240)
    summarize.add_argument("--retries", type=int, default=2)
    summarize.add_argument("--retry-sleep", type=float, default=8.0)
    summarize.set_defaults(func=command_summarize)

    report = subparsers.add_parser("report", help="Build compact Markdown report from summary JSONL")
    add_common_filters(report)
    report.set_defaults(func=command_report)

    run_all = subparsers.add_parser("run-all", help="Run download, extract, summarize, and report")
    add_common_filters(run_all)
    run_all.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    run_all.add_argument("--timeout", type=int, default=240)
    run_all.add_argument("--semantic-scholar-lookup", action=argparse.BooleanOptionalAction, default=True)
    run_all.add_argument("--semantic-scholar-delay", type=float, default=1.0)
    run_all.add_argument("--openalex-delay", type=float, default=0.2)
    run_all.add_argument("--doi-delay", type=float, default=0.2)
    run_all.add_argument("--arxiv-delay", type=float, default=1.0)
    run_all.add_argument("--extract-chars", type=int, default=120_000)
    run_all.add_argument("--max-model-chars", type=int, default=DEFAULT_MAX_MODEL_CHARS)
    run_all.add_argument("--min-text-chars", type=int, default=800)
    run_all.add_argument("--model", default=DEFAULT_MODEL)
    run_all.add_argument("--max-tokens", type=int, default=1400)
    run_all.add_argument("--retries", type=int, default=2)
    run_all.add_argument("--retry-sleep", type=float, default=8.0)
    run_all.set_defaults(func=command_run_all)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

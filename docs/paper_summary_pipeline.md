# Paper Summary Pipeline

This repository includes a resumable pipeline for downloading papers, extracting text, and summarizing every entry in `data/processed/thematic_papers.csv` with Frederick's Local LLM aggregate service.

The pipeline is intentionally conservative about storage:

- Downloaded PDFs, HTML pages, manual files, and extracted full text stay under `data/paper_cache/`.
- `data/paper_cache/` is ignored by Git because many papers are copyrighted or paywalled.
- Generated manifests and summaries are written to `data/processed/paper_summaries/`.
- The compact human-readable report is written to `docs/paper_summary_report.md`.

## Setup

```bash
python3 -m venv .venv-paper-pipeline
.venv-paper-pipeline/bin/python -m pip install -r requirements-paper-pipeline.txt
export LOCAL_LLM_BASE=<local-llm-base>
export LOCAL_LLM_TOKEN=<local-token>
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py check-model --model Qwen/Qwen3.6-35B-A3B
```

The Local LLM defaults come from the `localllm-call` skill:

- Base URL: read from `LOCAL_LLM_BASE`
- Token: read from `LOCAL_LLM_TOKEN`
- Model: `Qwen/Qwen3.6-35B-A3B`
- Thinking disabled through `chat_template_kwargs.enable_thinking=false`

Override with environment variables only when needed:

```bash
LOCAL_LLM_BASE=<local-llm-base> LOCAL_LLM_TOKEN=<local-token> \
  .venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py check-model
```

## Full Run

```bash
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py run-all \
  --max-model-chars 50000 \
  --model Qwen/Qwen3.6-35B-A3B \
  --timeout 300
```

This performs:

1. `download`: resolve open PDFs/HTML from arXiv, ACL Anthology, publisher URLs, and Semantic Scholar open-access metadata.
2. `recover-manual`: search unresolved entries again through DOI publisher templates, DOI landing metadata, OpenAlex OA locations, arXiv title search, and Semantic Scholar open-access metadata.
3. `extract`: extract local text from PDF/HTML/TXT files and cap model input at 50,000 characters. If the file cannot be recovered but the catalog has an abstract, the pipeline writes an `abstract_missing_download` fallback.
4. `summarize`: call Qwen 3.6 35B and write structured JSONL/CSV summaries.
5. `report`: build a compact Markdown report for human reading.

All commands are resumable by default. Re-run the same command after interruptions.

## Unresolved Downloads

Some papers are books, publisher pages, paywalled articles, or very new papers without stable open files. The pipeline searches these again itself before leaving them unresolved. Remaining unresolved entries are listed here:

```text
data/processed/paper_summaries/manual_downloads.csv
```

To run only that second search stage:

```bash
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py recover-manual --timeout 45
```

If a local copy becomes available later, place it at the exact `manual_path_hint`, usually:

```text
data/paper_cache/manual/<slug>.pdf
```

Supported manual file types:

- `.pdf`
- `.txt`
- `.html`
- `.htm`

Then rerun:

```bash
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py extract
```

## Useful Partial Runs

Smoke test one paper:

```bash
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py run-all \
  --title-regex "ForecastBench: A Dynamic Benchmark" \
  --max-model-chars 50000 \
  --model Qwen/Qwen3.6-35B-A3B
```

Run only Core and Important papers first:

```bash
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py run-all \
  --only-core-important \
  --max-model-chars 50000 \
  --model Qwen/Qwen3.6-35B-A3B
```

Only retry unresolved-paper search:

```bash
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py recover-manual --timeout 45
```

Only retry extraction after adding local files or recovering new downloads:

```bash
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py extract
```

Only continue LLM summarization:

```bash
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py summarize \
  --max-model-chars 50000 \
  --model Qwen/Qwen3.6-35B-A3B \
  --timeout 300
```

Rebuild the report from existing summaries:

```bash
.venv-paper-pipeline/bin/python scripts/paper_summary_pipeline.py report
```

## Output Schema

Each JSONL row contains paper metadata and a `summary` object:

```json
{
  "summary_zh": "short Chinese summary",
  "important_results": ["key result"],
  "deliverables": ["dataset, benchmark, code, framework, typology, etc."],
  "method": ["study design or method"],
  "paywall_or_fulltext_notes": "what was visible from full text/manual text",
  "repo_relevance": "core|important|peripheral|watchlist",
  "tags": ["10-20 searchable tags"],
  "confidence": "high|medium|low"
}
```

If only the abstract is available, `paywall_or_fulltext_notes` records that limitation.

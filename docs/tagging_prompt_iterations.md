# Tagging Prompt Iterations

This note records the small-batch prompt tuning used before generating `paper_tags_curated_v1`.

## Goal

Generate high-precision discovery tags for the paper corpus without rewriting summaries.

Target behavior:

- Prefer 8-10 tags for substantial/partial text, 7-9 for abstract-only records, and 5-7 for metadata-only records.
- Use tags that help filter a 350-paper repository by method, task, domain object, dataset/context, and evaluation/risk.
- Avoid generic tags such as `large language models`, `generative ai`, `ai ethics`, `political science`, `computational social science`, `policy analysis`, and `decision support`.
- Avoid author-name, venue, model-name, and source-quality tags.

## Sample Used

The prompt was iterated on a representative mix:

- `Fightin' Words`
- `Media Source Matters More Than Content`
- `Effective and responsible use of large language models in strategic wargaming`
- `Psychology of Intelligence Analysis`
- `Generative Artificial Intelligence and Evaluating Strategic Decisions`
- `The End of the Policy Analyst?`
- `Approaching Human-Level Forecasting with Language Models`
- `DiplomacyAgent`

## Iterations

1. **Round 1: simple high-signal tags.** Improved over the old tags, but still allowed broad labels such as `policy analysis`, `decision support`, and `international relations`.
2. **Round 2: grouped tags.** Added primary/method/domain/risk groups and source-sensitive handling. Better organization, but broad tags still leaked in and metadata-only records had too many content-level tags.
3. **Round 3: bad-to-better examples.** Added explicit replacement examples. This removed most generic tags but over-constrained output, producing too few tags for some records.
4. **Round 4: quantity targets.** Restored useful tag counts, but the model still used forbidden substrings inside compound tags such as `decision support`.
5. **Round 5: flat curated tags.** Switched to a simpler flat tag list and moved enforcement into code. The prompt asks for curated discovery tags; the pipeline hard-filters forbidden substrings, model names, author names, source-quality tags, and over-broad labels.

## Final Enforcement

The final `retag` command uses both prompt constraints and deterministic post-processing:

- Lowercases and normalizes tags.
- Removes underscores and most punctuation.
- Drops tags containing broad or forbidden substrings.
- Drops model-name and author-name tags.
- Drops source-quality tags such as `metadata only`.
- Fills with filtered prior tags only when the LLM output falls short.
- Caps tag count and total tag tokens.

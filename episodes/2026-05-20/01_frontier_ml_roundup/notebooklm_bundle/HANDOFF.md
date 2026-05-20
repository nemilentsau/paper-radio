# NotebookLM Handoff

## NotebookLM Settings

- Format: Deep Dive
- Length: Long
- Do not choose Debate.

## Episode

- Episode ID: episode-2026-05-20-01-frontier-ml-roundup
- Title: Frontier ML roundup for 2026-05-20
- Episode type: frontier_ml_roundup

## Papers

- `arxiv-2605.20164`
- `arxiv-2605.20167`
- `arxiv-2605.20170`
- `arxiv-2605.20172`
- `arxiv-2605.20173`
- `arxiv-2605.20174`
- `arxiv-2605.20176`
- `arxiv-2605.20177`
- `arxiv-2605.20179`
- `arxiv-2605.20182`

## Recommended NotebookLM Upload Set

Upload exactly these files for the normal production run:

- `episodes/2026-05-20/01_frontier_ml_roundup/notebooklm_bundle/research_dossier.md`
- `data/papers/pdfs/arxiv-2605.20176.pdf`
- `data/papers/pdfs/arxiv-2605.20174.pdf`

Keep `research_dossier.md` as the controlling source even when anchor papers are added.

## LLM Upload Decision

The source-dossier job chose these original paper sources:

- `data/papers/pdfs/arxiv-2605.20176.pdf` (arxiv-2605.20176, paper_pdf): ClinSeekAgent is the episode's strongest anchor for active evidence acquisition. NotebookLM would benefit from the original tables and methods because the critique depends on task-family deltas, tool access, inference budgets, and curated-versus-raw evidence controls.
- `data/papers/pdfs/arxiv-2605.20174.pdf` (arxiv-2605.20174, paper_pdf): AUDITS is the benchmark anchor. The original paper is worth upload budget because its value and critique depend on protocol details: source/manipulation splits, detector tables, ambiguous-pixel scoring, human-quality labels, and external transfer results.

## Optional Focus Papers

- The source-dossier job may recommend at most two original paper sources.
- Add only the recommended files from the upload set above.
- Prefer the PDF when NotebookLM imports it cleanly; use the paper markdown if the PDF import is slow, noisy, or fails.

Candidate original paper sources:

- `arxiv-2605.20164`: `data/papers/pdfs/arxiv-2605.20164.pdf` or `data/papers/arxiv-2605.20164.md`
- `arxiv-2605.20167`: `data/papers/pdfs/arxiv-2605.20167.pdf` or `data/papers/arxiv-2605.20167.md`
- `arxiv-2605.20170`: `data/papers/pdfs/arxiv-2605.20170.pdf` or `data/papers/arxiv-2605.20170.md`
- `arxiv-2605.20172`: `data/papers/pdfs/arxiv-2605.20172.pdf` or `data/papers/arxiv-2605.20172.md`
- `arxiv-2605.20173`: `data/papers/pdfs/arxiv-2605.20173.pdf` or `data/papers/arxiv-2605.20173.md`
- `arxiv-2605.20174`: `data/papers/pdfs/arxiv-2605.20174.pdf` or `data/papers/arxiv-2605.20174.md`
- `arxiv-2605.20176`: `data/papers/pdfs/arxiv-2605.20176.pdf` or `data/papers/arxiv-2605.20176.md`
- `arxiv-2605.20177`: `data/papers/pdfs/arxiv-2605.20177.pdf` or `data/papers/arxiv-2605.20177.md`
- `arxiv-2605.20179`: `data/papers/pdfs/arxiv-2605.20179.pdf` or `data/papers/arxiv-2605.20179.md`
- `arxiv-2605.20182`: `data/papers/pdfs/arxiv-2605.20182.pdf` or `data/papers/arxiv-2605.20182.md`

## Local Provenance

Do not upload these provenance files by default. Use them to audit or debug the generated dossier.
Raw review JSONs contain detailed critique fields and citation pointers, but they are machine-oriented local
provenance. Important review details should be synthesized into `research_dossier.md`, not uploaded as raw JSON.

- `episodes/2026-05-20/01_frontier_ml_roundup/script.json`
- `data/reviews/arxiv-2605.20164.json`
- `data/reviews/arxiv-2605.20167.json`
- `data/reviews/arxiv-2605.20170.json`
- `data/reviews/arxiv-2605.20172.json`
- `data/reviews/arxiv-2605.20173.json`
- `data/reviews/arxiv-2605.20174.json`
- `data/reviews/arxiv-2605.20176.json`
- `data/reviews/arxiv-2605.20177.json`
- `data/reviews/arxiv-2605.20179.json`
- `data/reviews/arxiv-2605.20182.json`

## Custom Prompt

```text
Use the uploaded research dossier as the controlling factual source material for a NotebookLM Deep Dive.
Keep the tone analytical and concrete.
Preserve critique, uncertainty, and paper-to-paper comparisons.
Discuss both research quality and podcast value.
If one or two original paper sources are also uploaded, use them only to sharpen details about those anchor papers.
Do not invent paper details beyond the source dossier.
Do not turn the notes into a debate format.
Do not add stage directions, host banter, or scripted dialogue from outside the source material.
```

## Operator Checklist

- Upload exactly the files listed in Recommended NotebookLM Upload Set.
- Choose Deep Dive.
- Choose Long.
- Paste the custom prompt above.
- Confirm NotebookLM is generating conversation from source material, not from a performed script.

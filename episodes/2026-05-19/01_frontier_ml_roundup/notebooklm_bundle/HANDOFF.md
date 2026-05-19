# NotebookLM Handoff

## NotebookLM Settings

- Format: Deep Dive
- Length: Long
- Do not choose Debate.

## Episode

- Episode ID: episode-2026-05-19-01-frontier-ml-roundup
- Title: Frontier ML roundup for 2026-05-19
- Episode type: frontier_ml_roundup

## Papers

- `arxiv-2605.18732`
- `arxiv-2605.18735`
- `arxiv-2605.18738`
- `arxiv-2605.18740`
- `arxiv-2605.18743`
- `arxiv-2605.18745`
- `arxiv-2605.18746`
- `arxiv-2605.18747`
- `arxiv-2605.18750`
- `arxiv-2605.18753`

## Recommended NotebookLM Upload Set

Upload exactly these files for the normal production run:

- `episodes/2026-05-19/01_frontier_ml_roundup/notebooklm_bundle/research_dossier.md`
- `data/papers/pdfs/arxiv-2605.18746.pdf`
- `data/papers/pdfs/arxiv-2605.18738.pdf`

Keep `research_dossier.md` as the controlling source even when anchor papers are added.

## LLM Upload Decision

The source-dossier job chose these original paper sources:

- `data/papers/pdfs/arxiv-2605.18746.pdf` (arxiv-2605.18746, paper_pdf): ESI-Bench is the best episode anchor and its passive/active/oracle evaluation design, task taxonomy, and behavioral diagnostics would benefit from NotebookLM seeing the original figures, tables, and setup directly.
- `data/papers/pdfs/arxiv-2605.18738.pdf` (arxiv-2605.18738, paper_pdf): The clinical-ethics paper is another anchor, and the value-profile GLM, entropy results, physician comparison, and Overton-style reasoning analysis are subtle enough that the original paper is worth the limited upload budget.

## Optional Focus Papers

- The source-dossier job may recommend at most two original paper sources.
- Add only the recommended files from the upload set above.
- Prefer the PDF when NotebookLM imports it cleanly; use the paper markdown if the PDF import is slow, noisy, or fails.

Candidate original paper sources:

- `arxiv-2605.18732`: `data/papers/pdfs/arxiv-2605.18732.pdf` or `data/papers/arxiv-2605.18732.md`
- `arxiv-2605.18735`: `data/papers/pdfs/arxiv-2605.18735.pdf` or `data/papers/arxiv-2605.18735.md`
- `arxiv-2605.18738`: `data/papers/pdfs/arxiv-2605.18738.pdf` or `data/papers/arxiv-2605.18738.md`
- `arxiv-2605.18740`: `data/papers/pdfs/arxiv-2605.18740.pdf` or `data/papers/arxiv-2605.18740.md`
- `arxiv-2605.18743`: `data/papers/pdfs/arxiv-2605.18743.pdf` or `data/papers/arxiv-2605.18743.md`
- `arxiv-2605.18745`: `data/papers/pdfs/arxiv-2605.18745.pdf` or `data/papers/arxiv-2605.18745.md`
- `arxiv-2605.18746`: `data/papers/pdfs/arxiv-2605.18746.pdf` or `data/papers/arxiv-2605.18746.md`
- `arxiv-2605.18747`: `data/papers/pdfs/arxiv-2605.18747.pdf` or `data/papers/arxiv-2605.18747.md`
- `arxiv-2605.18750`: `data/papers/pdfs/arxiv-2605.18750.pdf` or `data/papers/arxiv-2605.18750.md`
- `arxiv-2605.18753`: `data/papers/pdfs/arxiv-2605.18753.pdf` or `data/papers/arxiv-2605.18753.md`

## Local Provenance

Do not upload these provenance files by default. Use them to audit or debug the generated dossier.
Raw review JSONs contain detailed critique fields and citation pointers, but they are machine-oriented local
provenance. Important review details should be synthesized into `research_dossier.md`, not uploaded as raw JSON.

- `episodes/2026-05-19/01_frontier_ml_roundup/script.json`
- `data/reviews/arxiv-2605.18732.json`
- `data/reviews/arxiv-2605.18735.json`
- `data/reviews/arxiv-2605.18738.json`
- `data/reviews/arxiv-2605.18740.json`
- `data/reviews/arxiv-2605.18743.json`
- `data/reviews/arxiv-2605.18745.json`
- `data/reviews/arxiv-2605.18746.json`
- `data/reviews/arxiv-2605.18747.json`
- `data/reviews/arxiv-2605.18750.json`
- `data/reviews/arxiv-2605.18753.json`

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

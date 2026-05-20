# NotebookLM Handoff

## NotebookLM Settings

- Format: Deep Dive
- Length: Long
- Do not choose Debate.

## Episode

- Episode ID: episode-2026-05-20-02-applied-domain-llm-roundup
- Title: Applied-domain LLM roundup
- Episode type: applied_domain_llm_roundup

## Papers

- `arxiv-2605.19674`
- `arxiv-2605.19677`
- `arxiv-2605.19747`
- `arxiv-2605.19895`
- `arxiv-2605.20025`
- `arxiv-2605.20098`
- `arxiv-2605.20158`
- `arxiv-2605.20176`

## Recommended NotebookLM Upload Set

Upload exactly these files for the normal production run:

- `episodes/2026-05-20/02_applied_domain_llm_roundup/notebooklm_bundle/research_dossier.md`
- `data/papers/pdfs/arxiv-2605.19677.pdf`
- `data/papers/pdfs/arxiv-2605.20176.pdf`

Keep `research_dossier.md` as the controlling source even when anchor papers are added.

## LLM Upload Decision

The source-dossier job chose these original paper sources:

- `data/papers/pdfs/arxiv-2605.19677.pdf` (arxiv-2605.19677, paper_pdf): This is the cleanest applied closed-loop case study in the episode. NotebookLM would benefit from the primary paper’s formulation tables, iteration details, and viability-versus-patch-formation caveats.
- `data/papers/pdfs/arxiv-2605.20176.pdf` (arxiv-2605.20176, paper_pdf): This paper anchors the episode’s evidence-acquisition theme. The paired curated-input versus automated evidence-seeking setup, tool inventory, and task-family breakdowns are central mechanisms worth exposing directly to NotebookLM.

## Optional Focus Papers

- The source-dossier job may recommend at most two original paper sources.
- Add only the recommended files from the upload set above.
- Prefer the PDF when NotebookLM imports it cleanly; use the paper markdown if the PDF import is slow, noisy, or fails.

Candidate original paper sources:

- `arxiv-2605.19674`: `data/papers/pdfs/arxiv-2605.19674.pdf` or `data/papers/arxiv-2605.19674.md`
- `arxiv-2605.19677`: `data/papers/pdfs/arxiv-2605.19677.pdf` or `data/papers/arxiv-2605.19677.md`
- `arxiv-2605.19747`: `data/papers/pdfs/arxiv-2605.19747.pdf` or `data/papers/arxiv-2605.19747.md`
- `arxiv-2605.19895`: `data/papers/pdfs/arxiv-2605.19895.pdf` or `data/papers/arxiv-2605.19895.md`
- `arxiv-2605.20025`: `data/papers/pdfs/arxiv-2605.20025.pdf` or `data/papers/arxiv-2605.20025.md`
- `arxiv-2605.20098`: `data/papers/pdfs/arxiv-2605.20098.pdf` or `data/papers/arxiv-2605.20098.md`
- `arxiv-2605.20158`: `data/papers/pdfs/arxiv-2605.20158.pdf` or `data/papers/arxiv-2605.20158.md`
- `arxiv-2605.20176`: `data/papers/pdfs/arxiv-2605.20176.pdf` or `data/papers/arxiv-2605.20176.md`

## Local Provenance

Do not upload these provenance files by default. Use them to audit or debug the generated dossier.
Raw review JSONs contain detailed critique fields and citation pointers, but they are machine-oriented local
provenance. Important review details should be synthesized into `research_dossier.md`, not uploaded as raw JSON.

- `episodes/2026-05-20/02_applied_domain_llm_roundup/script.json`
- `data/reviews/arxiv-2605.19674.json`
- `data/reviews/arxiv-2605.19677.json`
- `data/reviews/arxiv-2605.19747.json`
- `data/reviews/arxiv-2605.19895.json`
- `data/reviews/arxiv-2605.20025.json`
- `data/reviews/arxiv-2605.20098.json`
- `data/reviews/arxiv-2605.20158.json`
- `data/reviews/arxiv-2605.20176.json`

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

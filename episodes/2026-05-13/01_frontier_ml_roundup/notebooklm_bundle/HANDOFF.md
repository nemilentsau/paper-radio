# NotebookLM Handoff

## NotebookLM Settings

- Format: Deep Dive
- Length: Long
- Do not choose Debate.

## Episode

- Episode ID: episode-2026-05-13-01-frontier-ml-roundup
- Title: Frontier ML roundup: agent memory, post-training, and multimodal generation
- Episode type: frontier_ml_roundup

## Papers

- `arxiv-2605.12477`
- `arxiv-2605.12480`
- `arxiv-2605.12481`
- `arxiv-2605.12483`
- `arxiv-2605.12484`
- `arxiv-2605.12487`
- `arxiv-2605.12491`
- `arxiv-2605.12492`
- `arxiv-2605.12493`
- `arxiv-2605.12495`

## Recommended NotebookLM Upload Set

Upload exactly these files for the normal production run:

- `episodes/2026-05-13/01_frontier_ml_roundup/notebooklm_bundle/research_dossier.md`
- `data/papers/pdfs/arxiv-2605.12477.pdf`
- `data/papers/pdfs/arxiv-2605.12495.pdf`

Keep `research_dossier.md` as the controlling source even when anchor papers are added.

## LLM Upload Decision

The source-dossier job chose these original paper sources:

- `data/papers/pdfs/arxiv-2605.12477.pdf` (arxiv-2605.12477, paper_pdf): MEME is the cleanest anchor for the agent-memory part of the episode. NotebookLM would benefit from seeing the original task taxonomy, Cascade and Absence setup, and benchmark design details directly.
- `data/papers/pdfs/arxiv-2605.12495.pdf` (arxiv-2605.12495, paper_pdf): AlphaGRPO is the best anchor for multimodal post-training and reward-design discussion. The DVReward decomposition, AR-plus-flow trajectory objective, and self-reflective refinement caveats are mechanism-heavy enough to deserve direct source access.

## Optional Focus Papers

- The source-dossier job may recommend at most two original paper sources.
- Add only the recommended files from the upload set above.
- Prefer the PDF when NotebookLM imports it cleanly; use the paper markdown if the PDF import is slow, noisy, or fails.

Candidate original paper sources:

- `arxiv-2605.12477`: `data/papers/pdfs/arxiv-2605.12477.pdf` or `data/papers/arxiv-2605.12477.md`
- `arxiv-2605.12480`: `data/papers/pdfs/arxiv-2605.12480.pdf` or `data/papers/arxiv-2605.12480.md`
- `arxiv-2605.12481`: `data/papers/pdfs/arxiv-2605.12481.pdf` or `data/papers/arxiv-2605.12481.md`
- `arxiv-2605.12483`: `data/papers/pdfs/arxiv-2605.12483.pdf` or `data/papers/arxiv-2605.12483.md`
- `arxiv-2605.12484`: `data/papers/pdfs/arxiv-2605.12484.pdf` or `data/papers/arxiv-2605.12484.md`
- `arxiv-2605.12487`: `data/papers/pdfs/arxiv-2605.12487.pdf` or `data/papers/arxiv-2605.12487.md`
- `arxiv-2605.12491`: `data/papers/pdfs/arxiv-2605.12491.pdf` or `data/papers/arxiv-2605.12491.md`
- `arxiv-2605.12492`: `data/papers/pdfs/arxiv-2605.12492.pdf` or `data/papers/arxiv-2605.12492.md`
- `arxiv-2605.12493`: `data/papers/pdfs/arxiv-2605.12493.pdf` or `data/papers/arxiv-2605.12493.md`
- `arxiv-2605.12495`: `data/papers/pdfs/arxiv-2605.12495.pdf` or `data/papers/arxiv-2605.12495.md`

## Local Provenance

Do not upload these provenance files by default. Use them to audit or debug the generated dossier.
Raw review JSONs contain detailed critique fields and citation pointers, but they are machine-oriented local
provenance. Important review details should be synthesized into `research_dossier.md`, not uploaded as raw JSON.

- `episodes/2026-05-13/01_frontier_ml_roundup/script.json`
- `data/reviews/arxiv-2605.12477.json`
- `data/reviews/arxiv-2605.12480.json`
- `data/reviews/arxiv-2605.12481.json`
- `data/reviews/arxiv-2605.12483.json`
- `data/reviews/arxiv-2605.12484.json`
- `data/reviews/arxiv-2605.12487.json`
- `data/reviews/arxiv-2605.12491.json`
- `data/reviews/arxiv-2605.12492.json`
- `data/reviews/arxiv-2605.12493.json`
- `data/reviews/arxiv-2605.12495.json`

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

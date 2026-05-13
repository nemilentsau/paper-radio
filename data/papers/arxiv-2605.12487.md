# Task-Adaptive Embedding Refinement via Test-time LLM Guidance

## Metadata
- Paper ID: arxiv-2605.12487
- Source: arxiv
- Source ID: 2605.12487
- Authors: Ariel Gera, Shir Ashury-Tahan, Gal Bloch, Ohad Eytan, Assaf Toledo
- Published: 2026-05-12T17:58:27Z
- Updated: 2026-05-12T17:58:27Z
- Categories: cs.CL, cs.IR, cs.LG
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: The abstract describes a concrete method with broad benchmark coverage and reproducible code, which makes it worth a closer look. The claim is application-focused rather than obviously field-defining, so it belongs in the review queue rather than advancing directly.
- Research score estimate: 6.8
- Podcast score estimate: 6.1
- Local PDF path: data/papers/pdfs/arxiv-2605.12487.pdf
- Full text path: data/papers/fulltext/arxiv-2605.12487.txt
- Abstract URL: https://arxiv.org/abs/2605.12487
- PDF URL: https://arxiv.org/pdf/2605.12487

## Abstract
We explore the effectiveness of an LLM-guided query refinement paradigm for extending the usability of embedding models to challenging zero-shot search and classification tasks. Our approach refines the embedding representation of a user query using feedback from a generative LLM on a small set of documents, enabling embeddings to adapt in real time to the target task. We conduct extensive experiments with state-of-the-art text embedding models across a diverse set of challenging search and classification benchmarks. Empirical results indicate that LLM-guided query refinement yields consistent gains across all models and datasets, with relative improvements of up to +25% in literature search, intent detection, key-point matching, and nuanced query-instruction following. The refined queries improve ranking quality and induce clearer binary separation across the corpus, enabling the embedding space to better reflect the nuanced, task-specific constraints of each ad-hoc user query. Importantly, this expands the range of practical settings in which embedding models can be effectively deployed, making them a compelling alternative when costly LLM pipelines are not viable at corpus-scale. We release our experimental code for reproducibility, at https://github.com/IBM/task-aware-embedding-refinement.

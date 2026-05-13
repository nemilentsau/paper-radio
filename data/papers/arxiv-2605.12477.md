# MEME: Multi-entity & Evolving Memory Evaluation

## Metadata
- Paper ID: arxiv-2605.12477
- Source: arxiv
- Source ID: 2605.12477
- Authors: Seokwon Jung, Alexander Rubinstein, Arnas Uselis, Sangdoo Yun, Seong Joon Oh
- Published: 2026-05-12T17:55:10Z
- Updated: 2026-05-12T17:55:10Z
- Categories: cs.LG, cs.CL
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: This looks like a solid benchmark paper with a clear gap analysis and concrete failure modes, which makes it useful for review. It is narrower than a breakthrough methods paper, but the controlled evaluation and practical cost tradeoff make it relevant and discussable.
- Research score estimate: 7.6
- Podcast score estimate: 7.9
- Local PDF path: data/papers/pdfs/arxiv-2605.12477.pdf
- Full text path: data/papers/fulltext/arxiv-2605.12477.txt
- Abstract URL: https://arxiv.org/abs/2605.12477
- PDF URL: https://arxiv.org/pdf/2605.12477

## Abstract
LLM-based agents increasingly operate in persistent environments where they must store, update, and reason over information across many sessions. While prior benchmarks evaluate only single-entity updates, MEME defines six tasks spanning the full space defined by the multi-entity and evolving axes, including three not scored by prior work: Cascade and Absence (dependency reasoning) and Deletion (post-removal state). Evaluating six memory systems spanning three memory paradigms on 100 controlled episodes, we find that all systems collapse on dependency reasoning under the default configuration (Cascade: 3%, Absence: 1% in average accuracy) despite adequate static retrieval performance. Prompt optimization, deeper retrieval, reduced filler noise, and most stronger LLMs fail to close this gap. Only a file-based agent paired with Claude Opus 4.7 as its internal LLM partially closes the gap, but at ~70x the baseline cost, indicating closure currently depends on configurations that are not practical at scale. Code and data are available on the project page: https://seokwonjung-jay.github.io/meme-eval/.

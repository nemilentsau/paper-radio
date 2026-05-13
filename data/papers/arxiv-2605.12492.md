# Pion: A Spectrum-Preserving Optimizer via Orthogonal Equivalence Transformation

## Metadata
- Paper ID: arxiv-2605.12492
- Source: arxiv
- Source ID: 2605.12492
- Authors: Kexuan Shi, Hanxuan Li, Zeju Qiu, Yandong Wen, Simon Buchholz, Weiyang Liu
- Published: 2026-05-12T17:59:34Z
- Updated: 2026-05-12T17:59:34Z
- Categories: cs.LG, stat.ML
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: The paper proposes a clearly technical optimizer mechanism with a concrete mathematical constraint and claims both convergence analysis and empirical competitiveness, which makes it worth review. It is still a methods paper about training optimization rather than a broader result, so it is better queued than auto-advanced.
- Research score estimate: 6.5
- Podcast score estimate: 5.5
- Local PDF path: data/papers/pdfs/arxiv-2605.12492.pdf
- Full text path: data/papers/fulltext/arxiv-2605.12492.txt
- Abstract URL: https://arxiv.org/abs/2605.12492
- PDF URL: https://arxiv.org/pdf/2605.12492

## Abstract
We introduce Pion, a spectrum-preserving optimizer for large language model (LLM) training based on orthogonal equivalence transformation. Unlike additive optimizers such as Adam and Muon, Pion updates each weight matrix through left and right orthogonal transformations, preserving its singular values throughout training. This yields an optimization mechanism that modulates the geometry of weight matrices while keeping their spectral norm fixed. We derive the Pion update rule, systematically examine its design choices, and analyze its convergence behavior along with several key properties. Empirical results show that Pion offers a stable and competitive alternative to standard optimizers for both LLM pretraining and finetuning.

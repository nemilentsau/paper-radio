# Streamlined Constraint Reasoning via CNN Pattern Recognition on Enumerated Solutions

## Metadata
- Paper ID: arxiv-2605.19895
- Source: arxiv
- Source ID: 2605.19895
- Authors: Patrick Spracklen
- Published: 2026-05-19T14:25:39Z
- Updated: 2026-05-19T14:25:39Z
- Categories: cs.AI
- Source signals: arxiv_applied_domain, applied_domain:finance_modeling
- Triage decision: advance_to_review
- Triage rationale: This looks like a genuinely novel hybrid of pattern learning and constraint-program synthesis, with concrete benchmark gains and specific discovered streamliners rather than a benchmark-only LLM application. The evidence is still narrow to constraint-programming benchmarks, but the method and results are substantial enough to merit review.
- Research score estimate: 7.8
- Podcast score estimate: 6.7
- Local PDF path: data/papers/pdfs/arxiv-2605.19895.pdf
- Full text path: data/papers/fulltext/arxiv-2605.19895.txt
- Abstract URL: https://arxiv.org/abs/2605.19895
- PDF URL: https://arxiv.org/pdf/2605.19895

## Abstract
Constraint programming practitioners accelerate hard problems through a layered set of techniques applied in order of risk. Standard hardening (symmetry-breaking and implied constraints) is applied first and preserves satisfiability. Streamliner constraints, which restrict search to a structural sub-family of solutions, do not preserve satisfiability and are reserved as a final lever. Existing automated streamliner-synthesis approaches either search a constraint grammar or prompt a Large Language Model directly on the problem model. We propose a different approach: enumerate feasible solutions, train a Convolutional Neural Network contrastively against perturbed non-solutions to detect structural patterns, and translate the CNN's discriminative signal into candidate MiniZinc streamliners through LLM-driven synthesis. The CNN grounds the LLM's constraint generation in observed solution structure rather than model text alone. We evaluate on hardened benchmark models where streamliner discovery is the residual performance lever. Our pipeline achieves 98.8% portfolio time reduction on hardened Vessel Loading, 98.6% on hardened Social Golfers, and 89.4% on Black Hole, with best-single streamliners reaching geometric-mean speedups of 932x, 356x, and 1103x respectively. Discovered streamliners include class-based packing constraints on Vessel Loading, beyond-hardening canonicalisations on Social Golfers, and layout-coordinate bounds on Black Hole.

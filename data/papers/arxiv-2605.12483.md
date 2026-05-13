# Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training

## Metadata
- Paper ID: arxiv-2605.12483
- Source: arxiv
- Source ID: 2605.12483
- Authors: Yuanda Xu, Hejian Sang, Zhengze Zhou, Ran He, Zhipeng Wang, Alborz Geramifard
- Published: 2026-05-12T17:57:48Z
- Updated: 2026-05-12T17:57:48Z
- Categories: cs.LG, cs.AI
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: The paper has a clear and testable training-data allocation claim, with concrete comparative results across GRPO, distillation, and bridge procedures on math benchmarks. It is methodologically focused and likely useful for readers tracking post-training recipes, though the evidence appears narrow to a specific Qwen3/Llama setup and a single reward-allocation framing.
- Research score estimate: 7.2
- Podcast score estimate: 6.8
- Local PDF path: data/papers/pdfs/arxiv-2605.12483.pdf
- Full text path: data/papers/fulltext/arxiv-2605.12483.txt
- Abstract URL: https://arxiv.org/abs/2605.12483
- PDF URL: https://arxiv.org/pdf/2605.12483

## Abstract
In settings where labeled verifiable training data is the binding constraint, each checked example should be allocated carefully. The standard practice is to use this data directly on the model that will be deployed, for example by running GRPO on the deployment student. We argue that this is often an inefficient allocation because it overlooks a reward-density principle: sparse sequence-level reward should train models where exploration is productive, while dense token-level teacher reward should be used where the aim is to compress behavior into a smaller model. In this view, GRPO-style sparse RL and OPD-style dense teacher supervision are not separate recipes; they are different reward-density regimes. The allocation rule is simple: use scarce labeled training data upstream on the strongest model that can turn it into reward-shaped behavior, then transfer that behavior downstream as dense supervision. We evaluate this rule on verifiable math with Qwen3 and Llama models. At fixed Qwen3-1.7B deployment-student size, an RL-improved 8B teacher distilled through the dense bridge outperforms direct GRPO on the same student, while transfer from the same teacher before RL underperforms. The bridge is important: a forward-KL warmup on teacher rollouts followed by OPD on student rollouts is consistently strongest on MATH before any post-bridge student-side sparse RL, and also gives the best pre-Stage~3 AIME endpoints for the canonical 8B/14B teachers. The bridge also makes later student-side sparse RL effective: GRPO that is weak on a cold student lifts MATH from $75.4\%$ to $78.5\%$ after the bridge and outperforms a matched replay control by $2.8$ points. The operational principal is to avoid using scarce labeled data on the least prepared policy: use sparse reward for teacher-side discovery, dense transfer for student compression, and student-side sparse reward only after the bridge.

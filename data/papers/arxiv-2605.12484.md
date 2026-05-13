# Learning, Fast and Slow: Towards LLMs That Adapt Continually

## Metadata
- Paper ID: arxiv-2605.12484
- Source: arxiv
- Source ID: 2605.12484
- Authors: Rishabh Tiwari, Kusha Sareen, Lakshya A Agrawal, Joseph E. Gonzalez, Matei Zaharia, Kurt Keutzer, Inderjit S Dhillon, Rishabh Agarwal, Devvrit Khatri
- Published: 2026-05-12T17:58:20Z
- Updated: 2026-05-12T17:58:20Z
- Categories: cs.LG, cs.AI
- Source signals: arxiv_recent
- Triage decision: advance_to_review
- Triage rationale: This looks like a substantive ML systems/methods paper with a clear algorithmic proposal and multiple concrete claims about sample efficiency, forgetting, and continual adaptation. It is a good candidate for review because the abstract describes a useful comparison against standard RL fine-tuning and a likely broadly relevant training pattern for LLMs.
- Research score estimate: 7.8
- Podcast score estimate: 7.1
- Local PDF path: data/papers/pdfs/arxiv-2605.12484.pdf
- Full text path: data/papers/fulltext/arxiv-2605.12484.txt
- Abstract URL: https://arxiv.org/abs/2605.12484
- PDF URL: https://arxiv.org/pdf/2605.12484

## Abstract
Large language models (LLMs) are trained for downstream tasks by updating their parameters (e.g., via RL). However, updating parameters forces them to absorb task-specific information, which can result in catastrophic forgetting and loss of plasticity. In contrast, in-context learning with fixed LLM parameters can cheaply and rapidly adapt to task-specific requirements (e.g., prompt optimization), but cannot by itself typically match the performance gains available through updating LLM parameters. There is no good reason for restricting learning to being in-context or in-weights. Moreover, humans also likely learn at different time scales (e.g., System 1 vs 2). To this end, we introduce a fast-slow learning framework for LLMs, with model parameters as "slow" weights and optimized context as "fast" weights. These fast "weights" can learn from textual feedback to absorb the task-specific information, while allowing slow weights to stay closer to the base model and persist general reasoning behaviors. Fast-Slow Training (FST) is up to 3x more sample-efficient than only slow learning (RL) across reasoning tasks, while consistently reaching a higher performance asymptote. Moreover, FST-trained models remain closer to the base LLM (up to 70% less KL divergence), resulting in less catastrophic forgetting than RL-training. This reduced drift also preserves plasticity: after training on one task, FST trained models adapt more effectively to a subsequent task than parameter-only trained models. In continual learning scenarios, where task domains change on the fly, FST continues to acquire each new task while parameter-only RL stalls.

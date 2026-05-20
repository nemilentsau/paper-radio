# Not Every Rubric Teaches Equally: Policy-Aware Rubric Rewards for RLVR

## Metadata
- Paper ID: arxiv-2605.20164
- Source: arxiv
- Source ID: 2605.20164
- Authors: Utkarsh Tyagi, Xingang Guo, MohammadHossein Rezaei, Daniel George, Anas Mahmoud, Jackson Lee, Bing Liu, Yunzhong He
- Published: 2026-05-19T17:50:18Z
- Updated: 2026-05-19T17:50:18Z
- Categories: cs.AI
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: This looks like a solid methods paper with a clear training-side contribution and measurable claims across multiple policies and datasets, but the abstract suggests an incremental optimization improvement rather than a fundamentally new problem setting. It is worth review because rubric-based reward design and policy-aware weighting could be practically useful and easy to discuss, even if the evidence is still limited to the authors' benchmark setup.
- Research score estimate: 6.8
- Podcast score estimate: 6.5
- Local PDF path: data/papers/pdfs/arxiv-2605.20164.pdf
- Full text path: data/papers/fulltext/arxiv-2605.20164.txt
- Abstract URL: https://arxiv.org/abs/2605.20164
- PDF URL: https://arxiv.org/pdf/2605.20164

## Abstract
Reinforcement learning with verifiable rewards has made post-training highly effective when correctness can be checked automatically. However, many important model behaviors require satisfying several qualitative criteria at once. Rubric-based rewards address this setting by grading prompt-specific criteria and aggregating them into a scalar reward. Yet standard static aggregations conflate a criterion's human-assigned importance with its current usefulness as an optimization signal. We show that this assumption breaks down in rubric RL: many important criteria are already saturated or currently unreachable, while criteria that distinguish rollouts are not necessarily those with the largest human weights. We introduce POW3R, a policy-aware rubric reward framework that preserves human weights and category balance as the rubric objective while adapting criterion-level reward weights during training. POW3R uses rollout-level contrast to emphasize criteria that currently separate the policy's outputs, making the GRPO reward more informative without changing the underlying evaluation target. Across three base policies on two datasets spanning multimodal and text-only settings, POW3R wins $24$ of $30$ base-policy/metric comparisons, improving both mean rubric reward and strict completion (the fraction of prompts whose response satisfies every required rubric criterion) over vanilla GRPO with rubric rewards, and reaches the same plateau in $2.5$--$4\times$ fewer training steps. Rubric rewards should therefore distinguish what should matter in the final answer from what can teach the current policy.

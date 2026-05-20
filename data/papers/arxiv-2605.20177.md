# From Seeing to Thinking: Decoupling Perception and Reasoning Improves Post-Training of Vision-Language Models

## Metadata
- Paper ID: arxiv-2605.20177
- Source: arxiv
- Source ID: 2605.20177
- Authors: Juncheng Wu, Hardy Chen, Haoqin Tu, Xianfeng Tang, Freda Shi, Hui Liu, Hanqing Lu, Cihang Xie, Yuyin Zhou
- Published: 2026-05-19T17:58:40Z
- Updated: 2026-05-19T17:58:40Z
- Categories: cs.CL, cs.CV
- Source signals: arxiv_recent
- Triage decision: advance_to_review
- Triage rationale: The abstract describes a concrete training methodology with clear empirical comparisons across multiple VLMs and named benchmark gains, which makes it likely to be technically substantive. It also has strong podcast potential because it challenges the common assumption that longer reasoning traces are the main lever for VLM improvement.
- Research score estimate: 8.1
- Podcast score estimate: 7.8
- Local PDF path: data/papers/pdfs/arxiv-2605.20177.pdf
- Full text path: data/papers/fulltext/arxiv-2605.20177.txt
- Abstract URL: https://arxiv.org/abs/2605.20177
- PDF URL: https://arxiv.org/pdf/2605.20177

## Abstract
Recent advances in vision-language models (VLMs) emphasize long chain-of-thought reasoning; yet, we find that their performance on visual tasks is primarily limited by a lack of visual perception as opposed to reasoning itself. In this work, we systematically study the interplay between perception and reasoning in VLM post-training by decomposing their capabilities into three separate training stages: visual perception, visual reasoning, and textual reasoning, incorporating specialized training data. We demonstrate that visual perception (a) requires targeted optimization with specialized data; (b) serves as a fundamental scaffold that should be solidified through staged training before refining visual reasoning; and (c) is more effectively learned via RL than caption-based SFT. Our experiments across multiple VLMs demonstrate that staged training consistently improves both visual perception and reasoning performance over merged training. Notably, models trained with our approach achieve 1.5% higher reasoning accuracy with 20.8% shorter reasoning traces, suggesting that superior perception reduces the need for excessive reasoning. Furthermore, we show that this capability-based staging represents a new curriculum dimension orthogonal to traditional difficulty-based curricula, and combining both yields further additive gains. Our staged-training models achieve superior performance among open-weight VLMs, establishing advanced results on several visual math and perception (e.g., +5.2% on WeMath and +3.7% on RealWorldQA) tasks compared with the base counterpart.

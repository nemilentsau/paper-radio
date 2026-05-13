# AlphaGRPO: Unlocking Self-Reflective Multimodal Generation in UMMs via Decompositional Verifiable Reward

## Metadata
- Paper ID: arxiv-2605.12495
- Source: arxiv
- Source ID: 2605.12495
- Authors: Runhui Huang, Jie Wu, Rui Yang, Zhe Liu, Hengshuang Zhao
- Published: 2026-05-12T17:59:47Z
- Updated: 2026-05-12T17:59:47Z
- Categories: cs.CV, cs.AI, cs.LG
- Source signals: arxiv_recent
- Triage decision: advance_to_review
- Triage rationale: This looks like a substantive methods paper with a clear technical contribution: a new training framework plus a reward decomposition scheme aimed at improving multimodal generation. It also has strong podcast potential because it connects RL, multimodal generation, and self-correction, though the abstract still reads benchmark-driven rather than broadly validated.
- Research score estimate: 7.2
- Podcast score estimate: 7.8
- Local PDF path: data/papers/pdfs/arxiv-2605.12495.pdf
- Full text path: data/papers/fulltext/arxiv-2605.12495.txt
- Abstract URL: https://arxiv.org/abs/2605.12495
- PDF URL: https://arxiv.org/pdf/2605.12495

## Abstract
In this paper, we propose AlphaGRPO, a novel framework that applies Group Relative Policy Optimization (GRPO) to AR-Diffusion Unified Multimodal Models (UMMs) to enhance multimodal generation capabilities without an additional cold-start stage. Our approach unlocks the model's intrinsic potential to perform advanced reasoning tasks: Reasoning Text-to-Image Generation, where the model actively infers implicit user intents, and Self-Reflective Refinement, where it autonomously diagnoses and corrects misalignments in generated outputs. To address the challenge of providing stable supervision for real-world multimodal generation, we introduce the Decompositional Verifiable Reward (DVReward). Unlike holistic scalar rewards, DVReward utilizes an LLM to decompose complex user requests into atomic, verifiable semantic and quality questions, which are then evaluated by a general MLLM to provide reliable and interpretable feedback. Extensive experiments demonstrate that AlphaGRPO yields robust improvements across multimodal generation benchmarks, including GenEval, TIIF-Bench, DPG-Bench and WISE, while also achieving significant gains in editing tasks on GEdit without training on editing tasks. These results validate that our self-reflective reinforcement approach effectively leverages inherent understanding to guide high-fidelity generation. Project page: https://huangrh99.github.io/AlphaGRPO/

# OmniNFT: Modality-wise Omni Diffusion Reinforcement for Joint Audio-Video Generation

## Metadata
- Paper ID: arxiv-2605.12480
- Source: arxiv
- Source ID: 2605.12480
- Authors: Guohui Zhang, XiaoXiao Ma, Jie Huang, Hang Xu, Hu Yu, Siming Fu, Yuming Li, Zeyue Xue, Lin Song, Haoyang Huang, Nan Duan, Feng Zhao
- Published: 2026-05-12T17:56:59Z
- Updated: 2026-05-12T17:56:59Z
- Categories: cs.CV, cs.AI
- Source signals: arxiv_recent
- Triage decision: queue_for_review
- Triage rationale: The abstract describes a concrete method for a timely multimodal generation problem and names specific failure modes, which makes it worth reviewer attention. It is not yet clearly a must-advance paper because the evidence is limited to reported improvements on named benchmarks and the claims are method-centric rather than obviously field-defining.
- Research score estimate: 6.7
- Podcast score estimate: 7.4
- Local PDF path: data/papers/pdfs/arxiv-2605.12480.pdf
- Full text path: data/papers/fulltext/arxiv-2605.12480.txt
- Abstract URL: https://arxiv.org/abs/2605.12480
- PDF URL: https://arxiv.org/pdf/2605.12480

## Abstract
Recent advances in joint audio-video generation have been remarkable, yet real-world applications demand strong per-modality fidelity, cross-modal alignment, and fine-grained synchronization. Reinforcement Learning (RL) offers a promising paradigm, but its extension to multi-objective and multi-modal joint audio-video generation remains unexplored. Notably, our in-depth analysis first reveals that the primary obstacles to applying RL in this stem from: (i) multi-objective advantages inconsistency, where the advantages of multimodal outputs are not always consistent within a group; (ii) multi-modal gradients imbalance, where video-branch gradients leak into shallow audio layers responsible for intra-modal generation; (iii) uniform credit assignment, where fine-grained cross-modal alignment regions fail to get efficient exploration. These shortcomings suggest that vanilla RL fine-tuning strategy with a single global advantage often leads to suboptimal results. To address these challenges, we propose OmniNFT, a novel modality-aware online diffusion RL framework with three key innovations: (1) Modality-wise advantage routing, which routes independent per-reward advantages to their respective modality generation branches. (2) Layer-wise gradient surgery, which selectively detaches video-branch gradients on shallow audio layers while retaining those for cross-modal interaction layers. (3) Region-wise loss reweighting, which modulates policy optimization toward critical regions related to audio-video synchronization and fine-grained alignment. Extensive experiments on JavisBench and VBench with the LTX-2 backbone demonstrate that OmniNFT achieves comprehensive improvements in audio and video perceptual quality, cross-modal alignment, and audio-video synchronization.
